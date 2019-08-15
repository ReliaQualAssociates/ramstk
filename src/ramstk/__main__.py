#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ramstk.__main__.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""This is the main program for the RAMSTK application."""

# Standard Library Imports
from logging import Logger

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKSiteConfiguration, RAMSTKUserConfiguration
)
from ramstk.db.base import BaseDatabase
from ramstk.db.common import do_load_variables
from ramstk.utilities import do_create_logger


def do_read_site_configuration(logger: Logger) -> RAMSTKSiteConfiguration:
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
        logger.error(error_message)

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
    # splScreen = SplashScreen()

    # Read the user configuration file and create a logger.  The user
    # configuration file contains information needed to create the logger so
    # it must come first.
    user_configuration = do_read_user_configuration()
    _logger: Logger = do_create_logger(__name__,
                                       user_configuration.RAMSTK_LOGLEVEL,
                                       user_configuration.RAMSTK_USER_LOG,
                                       True)

    _logger.info("Reading the site configuration file.")
    site_configuration = do_read_site_configuration(_logger)
    _logger.info("Read the site configuration file.")

    _logger.info("Connecting to the RAMSTK common database {0:s}.".format(
        site_configuration.RAMSTK_COM_INFO['database']))
    _site_db = (site_configuration.RAMSTK_COM_BACKEND + ':///'
                + site_configuration.RAMSTK_COM_INFO['database'])
    site_db = BaseDatabase()
    site_db.do_connect(_site_db)
    _logger.info("Connected to the RAMSTK common database {0:s}.".format(
        site_configuration.RAMSTK_COM_INFO['database']))

    _logger.debug("Validating the RAMSTK license.")
    _logger.debug("Validated the RAMSTK license.")

    _logger.info("Loading global RAMSTK configuration variables.")
    do_load_variables(site_db, site_configuration)
    _logger.info("Loaded global RAMSTK configuration variables.")

    _logger.info(
        "Initializing RAMSTK analysis managers, data managers, and matrix "
        "managers."
    )
    _logger.info(
        "Initialized RAMSTK analysis managers, data managers, and matrix "
        "managers."
    )

    _logger.info("Launching RAMSTK GUI.")
    _logger.info("Launched RAMSTK GUI.")

    # If you don't do this, the splash screen will show, but won't render it's
    # contents
    # while Gtk.events_pending():
    #     Gtk.main_iteration()

    # sleep(3)
    #_app = RAMSTK(test=False)

    # splScreen.window.destroy()

    # Create RAMSTK Books.  These need to be initialized after reading the
    # configuration.
    #if _app.RAMSTK_CONFIGURATION.RAMSTK_GUI_LAYOUT == 'basic':  # Single window.
    #    pass
    #else:  # Multiple windows.
    #   ListBook(_app.RAMSTK_CONFIGURATION)
    #    ModuleBook(_app.RAMSTK_CONFIGURATION)
    #    WorkBook(_app.RAMSTK_CONFIGURATION)

    #Gtk.main()


the_one_ring()
