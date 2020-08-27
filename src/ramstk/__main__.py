#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ramstk.__main__.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""This is the main program for the RAMSTK application."""

# Standard Library Imports
from time import sleep

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk import RAMSTKProgramManager
from ramstk.configuration import (RAMSTKSiteConfiguration,
                                  RAMSTKUserConfiguration)
from ramstk.controllers import (
    amFMEA, amFunction, amHardware, amStakeholder, amValidation, dmFMEA,
    dmFunction, dmHardware, dmOptions, dmPoF, dmRequirement, dmRevision,
    dmStakeholder, dmValidation, mmFunction, mmHardware, mmRequirement,
    mmValidation)
from ramstk.db.base import BaseDatabase
from ramstk.db.common import do_load_variables
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, RAMSTKDesktop


def do_read_site_configuration(logger: RAMSTKLogManager) -> \
        RAMSTKSiteConfiguration:
    """
    Create a site configuration instance.

    :param logger: the logging.Logger() instance to use for writing to the
        runtime log file.
    :type logger: :class:`logging.Logger`
    :return: _configuration; the RAMSTKSiteConfiguraion() instance to use for
        this run of RAMSTK.
    :rtype: :class:`ramstk.configuration.RAMSTKSiteConfiguration`
    """
    def on_fail_create_site_configuration(error_message: str) -> None:
        logger.do_log_error(__name__, error_message)

    pub.subscribe(on_fail_create_site_configuration,
                  'fail_create_site_configuration')

    _configuration = RAMSTKSiteConfiguration()
    _configuration.set_site_directories()
    _configuration.get_site_configuration()

    return _configuration


def do_read_user_configuration() -> RAMSTKUserConfiguration:
    """
    Create a user configuration instance.

    :return: _configuration; the RAMSTKUserConfiguraion() instance to use for
        this run of RAMSTK.
    :rtype: :class:`ramstk.configuration.RAMSTKUserConfiguration`
    """
    def on_fail_create_user_configuration(error_message: str) -> None:
        print(error_message)

    pub.subscribe(on_fail_create_user_configuration,
                  'fail_create_user_configuration')

    _configuration = RAMSTKUserConfiguration()
    _configuration.set_user_directories()
    _configuration.get_user_configuration()

    return _configuration


def the_one_ring() -> None:
    """Execute the main function for RAMSTK."""
    # // TODO: Implement splash screen.
    # //
    # // Add a splash screen to the launch of RAMSTK.
    # splScreen = SplashScreen()

    # Read the user configuration file and create a logger.  The user
    # configuration file contains information needed to create the logger so
    # it must come first.
    user_configuration = do_read_user_configuration()
    _logger: RAMSTKLogManager = RAMSTKLogManager(
        user_configuration.RAMSTK_USER_LOG)
    _logger.do_create_logger(__name__,
                             user_configuration.RAMSTK_LOGLEVEL,
                             to_tty=True)

    _logger.do_log_info(__name__, "Reading the site configuration file.")
    site_configuration = do_read_site_configuration(_logger)
    _logger.do_log_info(__name__, "Read the site configuration file.")

    _logger.do_log_info(
        __name__, "Connecting to the RAMSTK common database {0:s}.".format(
            site_configuration.RAMSTK_COM_INFO['database']))
    _site_db = (site_configuration.RAMSTK_COM_BACKEND + ':///'
                + site_configuration.RAMSTK_COM_INFO['database'])
    site_db = BaseDatabase()
    site_db.do_connect(site_configuration.RAMSTK_COM_INFO)
    _logger.do_log_info(
        __name__, "Connected to the RAMSTK common database {0:s}.".format(
            site_configuration.RAMSTK_COM_INFO['database']))

    _logger.do_log_debug(__name__, "Validating the RAMSTK license.")
    _logger.do_log_debug(__name__, "Validated the RAMSTK license.")

    _logger.do_log_info(__name__,
                        "Loading global RAMSTK configuration variables.")
    do_load_variables(site_db, site_configuration)
    _logger.do_log_info(__name__,
                        "Loaded global RAMSTK configuration variables.")

    # Copy some site-level configuration variables to the user-level
    # configuration.  These are used to load RAMSTKComboBox widgets with
    # information during initialization.  This is the easiest way to make
    # this information available without refactoring all the views to pass
    # the site configuration object in addition to the user configuration
    # object.
    user_configuration.RAMSTK_AFFINITY_GROUPS = \
        site_configuration.RAMSTK_AFFINITY_GROUPS
    user_configuration.RAMSTK_REQUIREMENT_TYPE = \
        site_configuration.RAMSTK_REQUIREMENT_TYPE
    user_configuration.RAMSTK_STAKEHOLDERS = \
        site_configuration.RAMSTK_STAKEHOLDERS
    user_configuration.RAMSTK_WORKGROUPS = site_configuration.RAMSTK_WORKGROUPS
    user_configuration.RAMSTK_VALIDATION_TYPE = \
        site_configuration.RAMSTK_VALIDATION_TYPE
    user_configuration.RAMSTK_MEASUREMENT_UNITS = \
        site_configuration.RAMSTK_MEASUREMENT_UNITS
    user_configuration.RAMSTK_CATEGORIES = \
        site_configuration.RAMSTK_CATEGORIES
    user_configuration.RAMSTK_SUBCATEGORIES = \
        site_configuration.RAMSTK_SUBCATEGORIES
    user_configuration.RAMSTK_MANUFACTURERS = \
        site_configuration.RAMSTK_MANUFACTURERS
    user_configuration.RAMSTK_USERS = site_configuration.RAMSTK_USERS
    user_configuration.RAMSTK_ACTION_CATEGORY = \
        site_configuration.RAMSTK_ACTION_CATEGORY
    user_configuration.RAMSTK_ACTION_STATUS = \
        site_configuration.RAMSTK_ACTION_STATUS
    user_configuration.RAMSTK_RPN_SEVERITY = \
        site_configuration.RAMSTK_RPN_SEVERITY
    user_configuration.RAMSTK_RPN_OCCURRENCE = \
        site_configuration.RAMSTK_RPN_OCCURRENCE
    user_configuration.RAMSTK_RPN_DETECTION = \
        site_configuration.RAMSTK_RPN_DETECTION
    user_configuration.RAMSTK_DAMAGE_MODELS = \
        site_configuration.RAMSTK_DAMAGE_MODELS
    user_configuration.RAMSTK_MEASURABLE_PARAMETERS = \
        site_configuration.RAMSTK_MEASURABLE_PARAMETERS
    user_configuration.RAMSTK_LOAD_HISTORY = \
        site_configuration.RAMSTK_LOAD_HISTORY

    _logger.do_log_info(__name__, "Initializing the RAMSTK application.")
    _program_mgr = RAMSTKProgramManager()
    _program_mgr.dic_managers['revision']['data'] = dmRevision()
    _program_mgr.dic_managers['function']['data'] = dmFunction()
    _program_mgr.dic_managers['function']['matrix'] = mmFunction()
    _program_mgr.dic_managers['function']['analysis'] = amFunction(
        user_configuration)
    # _program_mgr.dic_managers['ffmea']['analysis'] = amFMEA(user_configuration)
    # _program_mgr.dic_managers['ffmea']['data'] = dmFMEA(functional=True)
    _program_mgr.dic_managers['requirement']['data'] = dmRequirement()
    _program_mgr.dic_managers['requirement']['matrix'] = mmRequirement()
    _program_mgr.dic_managers['stakeholder']['analysis'] = amStakeholder(
        user_configuration)
    _program_mgr.dic_managers['stakeholder']['data'] = dmStakeholder()
    _program_mgr.dic_managers['hardware']['analysis'] = amHardware(
        user_configuration)
    _program_mgr.dic_managers['hardware']['data'] = dmHardware()
    _program_mgr.dic_managers['hardware']['matrix'] = mmHardware()
    _program_mgr.dic_managers['fmea']['analysis'] = amFMEA(user_configuration)
    _program_mgr.dic_managers['fmea']['data'] = dmFMEA()
    _program_mgr.dic_managers['pof']['data'] = dmPoF()
    _program_mgr.dic_managers['validation']['analysis'] = amValidation(
        user_configuration)
    _program_mgr.dic_managers['validation']['data'] = dmValidation()
    _program_mgr.dic_managers['validation']['matrix'] = mmValidation()
    _program_mgr.dic_managers['options']['data'] = dmOptions(
        common_dao=site_db,
        site_configuration=site_configuration,
        user_configuration=user_configuration)
    _program_mgr.user_configuration = user_configuration
    _logger.do_log_info(__name__, "Initialized the RAMSTK application.")

    _logger.do_log_info(__name__, "Launching RAMSTK GUI.")
    # If you don't do this, the splash screen will show, but won't render it's
    # contents
    # while Gtk.events_pending():
    #     Gtk.main_iteration()

    sleep(1)
    # splScreen.window.destroy()

    # Create the RAMSTK Book.  This needs to be initialized after reading the
    # configuration and creating the logger.
    RAMSTKDesktop([user_configuration, site_configuration], _logger)

    _logger.do_log_info(__name__, "Launched RAMSTK GUI.")

    Gtk.main()
