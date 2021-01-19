#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ramstk.__main__.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The main program for the RAMSTK application."""

# Standard Library Imports
import os
import shutil
import sys
from time import sleep
from typing import Tuple

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk import RAMSTKProgramManager
from ramstk.configuration import (
    RAMSTKSiteConfiguration, RAMSTKUserConfiguration
)
from ramstk.controllers import (
    amAllocation, amFMEA, amHardware, amHazards, amSimilarItem,
    amStakeholder, amValidation, dmAllocation, dmFailureDefinition,
    dmFMEA, dmFunction, dmHardware, dmHazards, dmOptions, dmPoF,
    dmPreferences, dmProgramStatus, dmRequirement, dmRevision,
    dmSimilarItem, dmStakeholder, dmUsageProfile, dmValidation
)
from ramstk.db.base import BaseDatabase
from ramstk.db.common import do_load_variables
from ramstk.exim import Export, Import
from ramstk.logger import RAMSTKLogManager
from ramstk.utilities import file_exists
from ramstk.views.gtk3 import Gtk, RAMSTKDesktop, _
from ramstk.views.gtk3.widgets import RAMSTKDatabaseSelect


def do_connect_to_site_db(conn_info) -> BaseDatabase:
    """Connect to the site (common) database.

    :param conn_info: the site database connection information.
    :return: _site_db
    :rtype: BaseDatabase
    """
    pub.sendMessage(
        'do_log_info_msg',
        logger_name='INFO',
        message="Connecting to the RAMSTK common database {0} on {1} "
        "using port {2}.".format(conn_info['database'], conn_info['host'],
                                 conn_info['port']))

    _site_db = BaseDatabase()
    _site_db.do_connect(conn_info)
    pub.sendMessage(
        'do_log_info_msg',
        logger_name='INFO',
        message="Connected to the RAMSTK common database {0:s}.".format(
            conn_info['database']))

    return _site_db


def do_first_run(configuration: RAMSTKSiteConfiguration) -> None:
    """Raise dialog to setup site database.

    :param configuration: the RAMSTKSiteConfiguration() instance.
    :return: _site_db
    :rtype: dict
    """
    _dialog = RAMSTKDatabaseSelect(
        dlgtitle=_("Set up RAMSTK Site Database Server Connection"),
        dao=BaseDatabase(),
        database=configuration.RAMSTK_COM_INFO,
        icons={
            'refresh':
            configuration.RAMSTK_SITE_DIR + '/icons/32x32/view-refresh.png',
            'save': configuration.RAMSTK_SITE_DIR + '/icons/32x32/save.png'
        })

    if _dialog.do_run() == Gtk.ResponseType.OK:
        _site_dir = configuration.RAMSTK_SITE_DIR
        _home = os.path.expanduser('~')
        _user_dir = _home + '/.config/RAMSTK'
        if not os.path.isdir(_user_dir):
            shutil.copytree(_site_dir + '/icons', _user_dir + '/icons/')
            shutil.copytree(_site_dir + '/layouts', _user_dir + '/layouts/')
            shutil.copy(_site_dir + '/RAMSTK.toml', _user_dir)
            shutil.copy(_site_dir + '/postgres_program_db.sql', _user_dir)
            os.makedirs(_user_dir + '/logs')

        configuration.RAMSTK_COM_INFO = _dialog.database
    else:
        sys.exit(0)

    _dialog.do_destroy()


def do_initialize_loggers(log_file: str, log_level: str) -> RAMSTKLogManager:
    """Initialize the loggers for the current instance of RAMSTK.

    :param log_file: the absolute path to the file used to capture logs.
    :param log_level: the lowest level of messages to log as defined by the
        user's configuration.
    :return: _logger; the RAMSTKLogManager() managing the loggers.
    :rtype: :class:`RAMSTKLogManager`
    """
    if file_exists(log_file):
        os.remove(log_file)

    _logger: RAMSTKLogManager = RAMSTKLogManager(log_file)

    for _level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        _logger.do_create_logger(_level,
                                 log_level,
                                 to_tty={
                                     'DEBUG': False,
                                     'INFO': False,
                                     'WARNING': False,
                                     'ERROR': True,
                                     'CRITICAL': True
                                 }[_level])

    return _logger


def do_read_site_configuration() -> RAMSTKSiteConfiguration:
    """Create a site configuration instance.

    :return: _configuration; the RAMSTKSiteConfiguraion() instance to use for
        this run of RAMSTK.
    :rtype: :class:`ramstk.configuration.RAMSTKSiteConfiguration`
    """
    def on_fail_create_site_configuration(error_message: str) -> None:
        """Log error message when there's a failure to create the site conf.

        :param error_message: the error message raised by the failure.
        :return: None
        :rtype: None
        """
        pub.sendMessage('do_log_debug_msg',
                        logger_name='DEBUG',
                        message=error_message)

    pub.subscribe(on_fail_create_site_configuration,
                  'fail_create_site_configuration')

    pub.sendMessage('do_log_info_msg',
                    logger_name='INFO',
                    message="Reading the site configuration file.")

    _configuration = RAMSTKSiteConfiguration()
    _configuration.set_site_directories()
    _configuration.get_site_configuration()

    pub.sendMessage('do_log_info_msg',
                    logger_name='INFO',
                    message="Read the site configuration file.")

    return _configuration


def do_read_user_configuration(
) -> Tuple[RAMSTKUserConfiguration, RAMSTKLogManager]:
    """Create a user configuration instance.

    :return: _configuration; the RAMSTKUserConfiguraion() instance to use for
        this run of RAMSTK.
    :rtype: :class:`ramstk.configuration.RAMSTKUserConfiguration`
    """
    def on_fail_create_user_configuration(error_message: str) -> None:
        """Log error message when there's a failure to create the user conf.

        :param error_message: the error message raised by the failure.
        :return: None
        :rtype: None
        """
        print(error_message)

    pub.subscribe(on_fail_create_user_configuration,
                  'fail_create_user_configuration')

    _configuration = RAMSTKUserConfiguration()

    _configuration.set_user_directories()
    _configuration.get_user_configuration()

    if _configuration.RAMSTK_DATA_DIR == '':
        _configuration.RAMSTK_DATA_DIR = _configuration.RAMSTK_CONF_DIR + \
                                         '/layouts'
        _configuration.set_user_configuration()

    if _configuration.RAMSTK_ICON_DIR == '':
        _configuration.RAMSTK_ICON_DIR = _configuration.RAMSTK_CONF_DIR + \
                                         '/icons'
        _configuration.set_user_configuration()

    if _configuration.RAMSTK_LOG_DIR == '':
        _configuration.RAMSTK_LOG_DIR = _configuration.RAMSTK_CONF_DIR + \
                                         '/logs'
        _configuration.set_user_configuration()

    _logger = do_initialize_loggers(_configuration.RAMSTK_USER_LOG,
                                    _configuration.RAMSTK_LOGLEVEL)

    return _configuration, _logger


def the_one_ring() -> None:
    """Execute the main function for RAMSTK."""
    # ISSUE: Implement splash screen.
    # //
    # // Add a splash screen to the launch of RAMSTK.
    # //
    # // labels: globalbacklog, normal
    # splScreen = SplashScreen()
    site_configuration = do_read_site_configuration()

    if site_configuration.RAMSTK_COM_INFO['user'] == 'first_run':
        do_first_run(site_configuration)
        site_configuration.set_site_configuration()

    # Read the user configuration file and create a logger.  The user
    # configuration file contains information needed to create the logger so
    # it must come first.
    user_configuration, _logger = do_read_user_configuration()

    pub.sendMessage('do_log_debug_msg',
                    logger_name='DEBUG',
                    message="Validating the RAMSTK license.")
    pub.sendMessage('do_log_debug_msg',
                    logger_name='DEBUG',
                    message="Validated the RAMSTK license.")

    site_db = do_connect_to_site_db(site_configuration.RAMSTK_COM_INFO)

    do_load_variables(site_db, user_configuration)

    pub.sendMessage('do_log_info_msg',
                    logger_name='INFO',
                    message="Initializing the RAMSTK application.")

    _program_mgr = RAMSTKProgramManager()
    _program_mgr.dic_managers['allocation']['analysis'] = amAllocation(
        user_configuration)
    _program_mgr.dic_managers['allocation']['data'] = dmAllocation()
    _program_mgr.dic_managers['revision']['data'] = dmRevision()
    _program_mgr.dic_managers['function']['data'] = dmFunction()
    _program_mgr.dic_managers['hazards']['analysis'] = amHazards(
        user_configuration)
    _program_mgr.dic_managers['hazards']['data'] = dmHazards()
    _program_mgr.dic_managers['requirement']['data'] = dmRequirement()
    _program_mgr.dic_managers['similar_item']['analysis'] = amSimilarItem(
        user_configuration)
    _program_mgr.dic_managers['similar_item']['data'] = dmSimilarItem()
    _program_mgr.dic_managers['stakeholder']['analysis'] = amStakeholder(
        user_configuration)
    _program_mgr.dic_managers['stakeholder']['data'] = dmStakeholder()
    _program_mgr.dic_managers['hardware']['analysis'] = amHardware(
        user_configuration)
    _program_mgr.dic_managers['hardware']['data'] = dmHardware()
    _program_mgr.dic_managers['failure_definition'][
        'data'] = dmFailureDefinition()
    _program_mgr.dic_managers['fmea']['analysis'] = amFMEA(user_configuration)
    _program_mgr.dic_managers['fmea']['data'] = dmFMEA()
    _program_mgr.dic_managers['pof']['data'] = dmPoF()
    _program_mgr.dic_managers['preferences']['data'] = dmPreferences()
    _program_mgr.dic_managers['program_status']['data'] = dmProgramStatus()
    _program_mgr.dic_managers['usage_profile']['data'] = dmUsageProfile()
    _program_mgr.dic_managers['validation']['analysis'] = amValidation(
        user_configuration)
    _program_mgr.dic_managers['validation']['data'] = dmValidation()
    _program_mgr.dic_managers['exim']['export'] = Export()
    _program_mgr.dic_managers['exim']['import'] = Import()
    _program_mgr.user_configuration = user_configuration

    # noinspection PyTypeChecker
    _program_mgr.dic_managers['options']['data'] = dmOptions()
    _program_mgr.dic_managers['options']['data'].dao = site_db
    _program_mgr.dic_managers['options']['data'].do_select_all({'site_id': 1})

    pub.sendMessage('do_log_info_msg',
                    logger_name='INFO',
                    message="Initialized the RAMSTK application.")
    pub.sendMessage('do_log_info_msg',
                    logger_name='INFO',
                    message="Launching RAMSTK GUI.")

    # If you don't do this, the splash screen will show, but won't render it's
    # contents
    # while Gtk.events_pending():
    #     Gtk.main_iteration()

    sleep(1)
    # splScreen.window.destroy()

    # Create the RAMSTK Book.  This needs to be initialized after reading the
    # configuration and creating the logger.
    RAMSTKDesktop([user_configuration, site_configuration], _logger)

    pub.sendMessage(
        'do_log_info_msg',
        logger_name='INFO',
        message="Launched RAMSTK GUI.",
    )

    Gtk.main()
