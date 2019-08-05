# -*- coding: utf-8 -*-
#
#       ramstk.configuration.user.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK User Configuration module."""

# Standard Library Imports
import sys
from os import environ
from typing import Dict

# Third Party Imports
import toml
from pubsub import pub

# RAMSTK Package Imports
from ramstk.Utilities import dir_exists, file_exists, prefix


class RAMSTKSiteConfiguration:
    r"""
    RAMSTK site configuration class.

    Attributes of the site configuration class are:
    """
    # Define private scalar attributes.
    _INSTALL_PREFIX = prefix()

    # Define public dictionary attributes.
    RAMSTK_COM_INFO: Dict[str, str] = {}
    RAMSTK_ACTION_CATEGORY: Dict[str, str] = {}
    RAMSTK_ACTION_STATUS: Dict[str, str] = {}
    RAMSTK_AFFINITY_GROUPS: Dict[str, str] = {}  # User.
    RAMSTK_CATEGORIES: Dict[str, str] = {}  # Static.
    RAMSTK_DAMAGE_MODELS: Dict[str, str] = {}  # User.
    RAMSTK_DETECTION_METHODS: Dict[str, str] = {}
    RAMSTK_FAILURE_MODES: Dict[str, str] = {}  # User.
    RAMSTK_HAZARDS: Dict[str, str] = {}  # User.
    RAMSTK_INCIDENT_CATEGORY: Dict[str, str] = {}
    RAMSTK_INCIDENT_STATUS: Dict[str, str] = {}
    RAMSTK_INCIDENT_TYPE: Dict[str, str] = {}
    RAMSTK_LOAD_HISTORY: Dict[str, str] = {}  # User.
    RAMSTK_MANUFACTURERS: Dict[str, str] = {}  # User.
    RAMSTK_MEASURABLE_PARAMETERS: Dict[str, str] = {}  # User.
    RAMSTK_MEASUREMENT_UNITS: Dict[str, str] = {}  # Admin.
    RAMSTK_MODULES: Dict[str, str] = {}  # Static.
    RAMSTK_PAGE_NUMBER: Dict[str, str] = {}
    RAMSTK_REQUIREMENT_TYPE: Dict[str, str] = {}
    RAMSTK_RPN_DETECTION: Dict[int, str] = {}  # User.
    RAMSTK_RPN_OCCURRENCE: Dict[int, str] = {}  # User.
    RAMSTK_RPN_SEVERITY: Dict[int, str] = {}  # User.
    RAMSTK_SEVERITY: Dict[str, str] = {}
    RAMSTK_STAKEHOLDERS: Dict[str, str] = {}  # User.
    RAMSTK_STRESS_LIMITS: Dict[str, str] = {}  # User.
    RAMSTK_SUBCATEGORIES: Dict[str, str] = {}  # Static.
    RAMSTK_USERS: Dict[str, str] = {}  # Admin.
    RAMSTK_VALIDATION_TYPE: Dict[str, str] = {}    # Admin.
    RAMSTK_WORKGROUPS: Dict[str, str] = {}  # Admin.

    # Define public list attributes.

    # Define public scalar attributes.
    if sys.platform == "linux" or sys.platform == "linux2":
        RAMSTK_SITE_DIR = _INSTALL_PREFIX + "/share/RAMSTK"
        RAMSTK_HOME_DIR = environ["HOME"]
    elif sys.platform == "win32":
        RAMSTK_SITE_DIR = environ["PYTHONPATH"] + "/RAMSTK"
        RAMSTK_HOME_DIR = environ["USERPROFILE"]
    RAMSTK_CONF_DIR = RAMSTK_SITE_DIR
    RAMSTK_SITE_CONF = RAMSTK_SITE_DIR + '/Site.toml'

    RAMSTK_DATA_DIR = RAMSTK_SITE_DIR + "/layouts"
    RAMSTK_ICON_DIR = RAMSTK_SITE_DIR + "/icons"
    RAMSTK_LOG_DIR = '/var/log/ramstk'
    RAMSTK_PROG_DIR = RAMSTK_HOME_DIR + "/analyses/ramstk/"

    RAMSTK_COM_BACKEND = ''

    def __init__(self):
        """Initialize the RAMSTK site configuration."""
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def _do_create_site_configuration(self):
        """
        Create the default site configuration file.

        :return: None
        :rtype: None
        """
        _dic_site_configuration = {
            "title": "RAMSTK Site Configuration",
            "backend": {
                "type": "sqlite",
                "host": "localhost",
                "socket": "3306",
                "database": self.RAMSTK_SITE_DIR + "/ramstk_common.ramstk",
                "user": "ramstk",
                "password": "ramstk"
            }
        }

        toml.dump(_dic_site_configuration, open(self.RAMSTK_SITE_CONF, "w"))

        pub.sendMessage('succeed_create_site_configuration')

    def get_site_configuration(self):
        """
        Read the site configuration file.

        :return: None
        :rtype: None
        """
        if file_exists(self.RAMSTK_SITE_CONF):
            _config = toml.load(self.RAMSTK_SITE_CONF)

            self.RAMSTK_COM_BACKEND = _config['backend']['type']
            self.RAMSTK_COM_INFO["host"] = _config['backend']['host']
            self.RAMSTK_COM_INFO["socket"] = _config['backend']['socket']
            self.RAMSTK_COM_INFO["database"] = _config['backend']['database']
            self.RAMSTK_COM_INFO["user"] = _config['backend']['user']
            self.RAMSTK_COM_INFO["password"] = _config['backend']['password']

        else:
            _error_msg = ("Failed to read Site configuration file "
                          "{0:s}.").format(self.RAMSTK_PROG_CONF)
            pub.sendMessage('fail_get_site_configuration',
                            error_message=_error_msg)

    def set_site_directories(self):
        """
        Set the site directories.

        :return: None
        :rtype: None
        """
        print(self._INSTALL_PREFIX)
        self.RAMSTK_SITE_DIR = self._INSTALL_PREFIX + "/share/RAMSTK"

        # Prefer user-specific directories in their $HOME directory over the
        # system-wide directories.
        if dir_exists(self.RAMSTK_HOME_DIR + "/.config/RAMSTK"):
            self.RAMSTK_CONF_DIR = self.RAMSTK_HOME_DIR + "/.config/RAMSTK"
        else:
            self.RAMSTK_CONF_DIR = self.RAMSTK_SITE_DIR

        self.RAMSTK_DATA_DIR = self.RAMSTK_CONF_DIR + '/layouts'
        self.RAMSTK_ICON_DIR = self.RAMSTK_CONF_DIR + '/icons'

        if dir_exists(self.RAMSTK_HOME_DIR + "/.config/RAMSTK"):
            self.RAMSTK_LOG_DIR = self.RAMSTK_HOME_DIR + "/.config/RAMSTK/logs"
        else:
            self.RAMSTK_LOG_DIR = '/var/log/RAMSTK'

        self.RAMSTK_SITE_CONF = self.RAMSTK_CONF_DIR + "/Site.conf"

        if not file_exists(self.RAMSTK_SITE_CONF):
            self._do_create_site_configuration()
