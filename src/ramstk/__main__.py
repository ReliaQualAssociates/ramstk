#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ramstk.__main__.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
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
from ramstk.configuration import RAMSTKSiteConfiguration, RAMSTKUserConfiguration
from ramstk.exceptions import DataAccessError
from ramstk.exim import Export, Import
from ramstk.logger import RAMSTKLogManager
from ramstk.models.db import BaseDatabase, RAMSTKCommonDB, RAMSTKProgramDB
from ramstk.models.dbtables import (
    RAMSTKActionTable,
    RAMSTKAllocationTable,
    RAMSTKCauseTable,
    RAMSTKControlTable,
    RAMSTKDesignElectricTable,
    RAMSTKDesignMechanicTable,
    RAMSTKEnvironmentTable,
    RAMSTKFailureDefinitionTable,
    RAMSTKFunctionTable,
    RAMSTKHardwareTable,
    RAMSTKHazardTable,
    RAMSTKMechanismTable,
    RAMSTKMILHDBK217FTable,
    RAMSTKMissionPhaseTable,
    RAMSTKMissionTable,
    RAMSTKModeTable,
    RAMSTKNSWCTable,
    RAMSTKOpLoadTable,
    RAMSTKOpStressTable,
    RAMSTKProgramInfoTable,
    RAMSTKProgramStatusTable,
    RAMSTKReliabilityTable,
    RAMSTKRequirementTable,
    RAMSTKRevisionTable,
    RAMSTKSimilarItemTable,
    RAMSTKSiteInfoTable,
    RAMSTKStakeholderTable,
    RAMSTKTestMethodTable,
    RAMSTKValidationTable,
)
from ramstk.models.dbviews import (
    RAMSTKFMEAView,
    RAMSTKHardwareBoMView,
    RAMSTKPoFView,
    RAMSTKUsageProfileView,
)
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
        "do_log_info_msg",
        logger_name="INFO",
        message=f"Connecting to the RAMSTK common database {conn_info['database']} on "
        f"{conn_info['host']} using port {conn_info['port']}.",
    )

    _site_db = BaseDatabase()
    try:
        _site_db.do_connect(conn_info)
    except DataAccessError:
        sys.exit(
            "\033[35mUNABLE TO CONNECT TO RAMSTK COMMON DATABASE!  Check the "
            "logs for more information.\033[0m"
        )

    pub.sendMessage(
        "do_log_info_msg",
        logger_name="INFO",
        message=f"Connected to the RAMSTK common database {conn_info['database']}.",
    )

    return _site_db


def do_first_run(configuration: RAMSTKSiteConfiguration) -> None:
    """Raise dialog to set up site database.

    :param configuration: the RAMSTKSiteConfiguration() instance.
    :return: None
    :rtype: None
    """
    _dialog = RAMSTKDatabaseSelect(
        dlgtitle=_("Set up RAMSTK Site Database Server Connection"),
        dao=BaseDatabase(),
        database=configuration.RAMSTK_COM_INFO,
        icons={
            "refresh": f"{configuration.RAMSTK_SITE_DIR}/icons/32x32/view-refresh.png",
            "save": f"{configuration.RAMSTK_SITE_DIR}/icons/32x32/save.png",
        },
    )

    if _dialog.do_run() == Gtk.ResponseType.OK:
        _site_dir = configuration.RAMSTK_SITE_DIR
        _home = os.path.expanduser("~")
        _user_dir = f"{_home}/.config/RAMSTK"
        if not os.path.isdir(_user_dir):
            shutil.copytree(f"{_site_dir}/icons", f"{_user_dir}/icons/")
            shutil.copytree(f"{_site_dir}/layouts", f"{_user_dir}/layouts/")
            shutil.copy(f"{_site_dir}/RAMSTK.toml", _user_dir)
            shutil.copy(f"{_site_dir}/postgres_program_db.sql", _user_dir)
            os.makedirs(f"{_user_dir}/logs")

        configuration.RAMSTK_COM_INFO = _dialog.database
    else:
        sys.exit(0)

    _dialog.do_destroy()


def do_initialize_databases(
    configuration: RAMSTKUserConfiguration, site_db: BaseDatabase
) -> Tuple[RAMSTKProgramDB, RAMSTKCommonDB]:
    """Initialize the databases for the current instance of RAMSTK.

    :param configuration: the instance of the user configuration object to associate
        with this database model.
    :param site_db: the instance of the site data access object to associate with
        this database model.
    :return: _program_db, _site_db
    :rtype: RAMSTKProgramDB, RAMSTKCommonDB
    """
    _program_db = RAMSTKProgramDB()
    _site_db = RAMSTKCommonDB()

    _program_db.dic_tables["action"] = RAMSTKActionTable()
    _program_db.dic_tables["allocation"] = RAMSTKAllocationTable()
    _program_db.dic_tables["cause"] = RAMSTKCauseTable()
    _program_db.dic_tables["control"] = RAMSTKControlTable()
    _program_db.dic_tables["design_electric"] = RAMSTKDesignElectricTable()
    _program_db.dic_tables["design_mechanic"] = RAMSTKDesignMechanicTable()
    _program_db.dic_tables["environment"] = RAMSTKEnvironmentTable()
    _program_db.dic_tables["failure_definition"] = RAMSTKFailureDefinitionTable()
    _program_db.dic_tables["function"] = RAMSTKFunctionTable()
    _program_db.dic_tables["hardware"] = RAMSTKHardwareTable()
    _program_db.dic_tables["hazards"] = RAMSTKHazardTable()
    _program_db.dic_tables["mechanism"] = RAMSTKMechanismTable()
    _program_db.dic_tables["milhdbk217f"] = RAMSTKMILHDBK217FTable()
    _program_db.dic_tables["mission"] = RAMSTKMissionTable()
    _program_db.dic_tables["mission_phase"] = RAMSTKMissionPhaseTable()
    _program_db.dic_tables["mode"] = RAMSTKModeTable()
    _program_db.dic_tables["nswc"] = RAMSTKNSWCTable()
    _program_db.dic_tables["opload"] = RAMSTKOpLoadTable()
    _program_db.dic_tables["opstress"] = RAMSTKOpStressTable()
    _program_db.dic_tables["program_info"] = RAMSTKProgramInfoTable()
    _program_db.dic_tables["program_status"] = RAMSTKProgramStatusTable()
    _program_db.dic_tables["reliability"] = RAMSTKReliabilityTable()
    _program_db.dic_tables["requirement"] = RAMSTKRequirementTable()
    _program_db.dic_tables["revision"] = RAMSTKRevisionTable()
    _program_db.dic_tables["similar_item"] = RAMSTKSimilarItemTable()
    _program_db.dic_tables["stakeholder"] = RAMSTKStakeholderTable()
    _program_db.dic_tables["test_method"] = RAMSTKTestMethodTable()
    _program_db.dic_tables["validation"] = RAMSTKValidationTable()
    _program_db.dic_tables["export"] = Export()
    _program_db.dic_tables["import"] = Import()
    _program_db.user_configuration = configuration

    _program_db.dic_views["fmea"] = RAMSTKFMEAView()
    _program_db.dic_views["hardwarebom"] = RAMSTKHardwareBoMView(
        hr_multiplier=configuration.RAMSTK_HR_MULTIPLIER
    )
    _program_db.dic_views["pof"] = RAMSTKPoFView()
    _program_db.dic_views["usage_profile"] = RAMSTKUsageProfileView()

    # noinspection PyTypeChecker
    _site_db.common_dao = site_db
    _site_db.dic_tables["options"] = RAMSTKSiteInfoTable()
    _site_db.dic_tables["options"].dao = site_db  # type: ignore
    _site_db.dic_tables["options"].do_select_all({"site_id": 1})  # type: ignore

    return _program_db, _site_db


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

    for _level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        _logger.do_create_logger(
            _level,
            log_level,
            to_tty={
                "DEBUG": False,
                "INFO": False,
                "WARNING": False,
                "ERROR": True,
                "CRITICAL": True,
            }[_level],
        )

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
        pub.sendMessage("do_log_debug_msg", logger_name="DEBUG", message=error_message)

    pub.subscribe(on_fail_create_site_configuration, "fail_create_site_configuration")

    pub.sendMessage(
        "do_log_info_msg",
        logger_name="INFO",
        message="Reading the site configuration file.",
    )

    _configuration = RAMSTKSiteConfiguration()
    _configuration.set_site_directories()
    _configuration.get_site_configuration()

    if _configuration.RAMSTK_COM_INFO["user"] == "first_run":
        do_first_run(_configuration)
        _configuration.set_site_configuration()

    pub.sendMessage(
        "do_log_info_msg",
        logger_name="INFO",
        message="Read the site configuration file.",
    )

    return _configuration


def do_read_user_configuration() -> Tuple[RAMSTKUserConfiguration, RAMSTKLogManager]:
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

    pub.subscribe(on_fail_create_user_configuration, "fail_create_user_configuration")

    _configuration = RAMSTKUserConfiguration()

    _configuration.set_user_directories()
    _configuration.get_user_configuration()

    if _configuration.RAMSTK_DATA_DIR == "":
        _configuration.RAMSTK_DATA_DIR = _configuration.RAMSTK_CONF_DIR + "/layouts"
        _configuration.set_user_configuration()

    if _configuration.RAMSTK_ICON_DIR == "":
        _configuration.RAMSTK_ICON_DIR = _configuration.RAMSTK_CONF_DIR + "/icons"
        _configuration.set_user_configuration()

    if _configuration.RAMSTK_LOG_DIR == "":
        _configuration.RAMSTK_LOG_DIR = _configuration.RAMSTK_CONF_DIR + "/logs"
        _configuration.set_user_configuration()

    _logger = do_initialize_loggers(
        _configuration.RAMSTK_USER_LOG, _configuration.RAMSTK_LOGLEVEL
    )

    return _configuration, _logger


def the_one_ring() -> None:
    """Execute the main function for RAMSTK."""
    # See ISSUE #354
    # splScreen = SplashScreen()
    # If you don't do this, the splash screen will show, but won't render it's
    # contents
    # while Gtk.events_pending():
    #     Gtk.main_iteration()

    site_configuration = do_read_site_configuration()

    # Read the user configuration file and create a logger.  The user
    # configuration file contains information needed to create the logger so
    # it must come first.
    user_configuration, _logger = do_read_user_configuration()

    pub.sendMessage(
        "do_log_debug_msg",
        logger_name="DEBUG",
        message="Validating the RAMSTK license.",
    )
    pub.sendMessage(
        "do_log_debug_msg",
        logger_name="DEBUG",
        message="Validated the RAMSTK license.",
    )

    site_db = do_connect_to_site_db(site_configuration.RAMSTK_COM_INFO)

    pub.sendMessage(
        "do_log_info_msg",
        logger_name="INFO",
        message="Initializing the RAMSTK application.",
    )

    (
        _program_db,  # pylint: disable=unused-variable
        _site_db,
    ) = do_initialize_databases(user_configuration, site_db)

    user_configuration = _site_db.do_load_site_variables(user_configuration)

    pub.sendMessage(
        "do_log_info_msg",
        logger_name="INFO",
        message="Initialized the RAMSTK application.",
    )
    pub.sendMessage(
        "do_log_info_msg", logger_name="INFO", message="Launching RAMSTK GUI."
    )

    # Create the RAMSTK Book.  This needs to be initialized after reading the
    # configuration and creating the logger.
    RAMSTKDesktop([user_configuration, site_configuration], _logger)

    pub.sendMessage(
        "do_log_info_msg",
        logger_name="INFO",
        message="Launched RAMSTK GUI.",
    )

    sleep(1)
    # splScreen.window.destroy()

    Gtk.main()
