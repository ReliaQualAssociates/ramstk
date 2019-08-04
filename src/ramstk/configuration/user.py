# -*- coding: utf-8 -*-
#
#       ramstk.configuration.user.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK User Configuration module."""

# Standard Library Imports
import glob
import sys
from distutils import dir_util, file_util  # pylint: disable=no-name-in-module
from os import environ, makedirs
from typing import Dict

# Third Party Imports
import toml
from pubsub import pub

# RAMSTK Package Imports
import ramstk.Utilities as Utilities


class RAMSTKUserConfiguration:
    r"""
    RAMSTK user configuration class.

    Attributes of the user configuration class are:

    :ivar dict RAMSTK_FORMAT_FILE: Dictionary containing the path to the format
        files to use for various widgets.  Keys for this dictionary are:

            * revision
            * function
            * requirement
            * hardware
            * validation
            * sia
            * fmeca
            * stakeholder
            * ffmeca

    :ivar dict RAMSTK_COLORS: Dictionary containing the colors to use for
        various widgets.  Keys for this dictionary are:

            * revisionbg - Revision Tree background
            * revisionfg - Revision Tree foreground
            * functionbg - Function Tree background
            * functionfg - Function Tree foreground
            * requirementbg - Requirement Tree background
            * requirementfg - Requirement Tree foreground
            * hardwarebg - Hardware Tree background
            * hardwarefg - Hardware Tree foreground
            * validationbg - Validation Tree background
            * validationfg - Validation Tree foreground

    :ivar dict RAMSTK_COM_INFO: Dictionary for the RAMSTK common database
        connection information.  The information contained is:

            +----------+-------------------------------+
            |   Key    | Information                   |
            +==========+===============================+
            |   host   | Host name (MySQL only)        |
            +----------+-------------------------------+
            |  socket  | Host port (MySQL only)        |
            +----------+-------------------------------+
            | database | Database name                 |
            +----------+-------------------------------+
            |   user   | User name (MySQL only)        |
            +----------+-------------------------------+
            | password | User password (MySQL only)    |
            +----------+-------------------------------+

    :ivar dict RAMSTK_PROG_INFO: Dictionary for RAMSTK Program database
        connection information.  The information contained is:

            +----------+-------------------------------+
            |   Key    | Information                   |
            +==========+===============================+
            |   host   | Host name (MySQL only)        |
            +----------+-------------------------------+
            |  socket  | Host port (MySQL only)        |
            +----------+-------------------------------+
            | database | Database name                 |
            +----------+-------------------------------+
            |   user   | User name (MySQL only)        |
            +----------+-------------------------------+
            | password | User password (MySQL only)    |
            +----------+-------------------------------+

    :ivar dict RAMSTK_TABPOS: Dictionary containing the location of tabs in the
        three main Gtk.Notebook() widgets.  Can be one of:

            * Top
            * Bottom
            * Left
            * Right

            +------------+---------------+----------+
            |    Key     | Notebook      | Default  |
            +============+===============+==========+
            |  listbook  | Module Book   |  *top*   |
            +------------+---------------+----------+
            | modulebook | Work Book     | *bottom* |
            +------------+---------------+----------+
            |  workbook  | List Book     | *bottom* |
            +------------+---------------+----------+

    :ivar dict RAMSTK_MODULES: Dictionary of active modules in the open RAMSTK
        Program database.  Where 1 = active and 0 = inactive.  Keys are:

            * Function
            * Hardware
            * Requirements
            * Revision
            * Validation

    :ivar list RAMSTK_RISK_POINTS: List for risk level cutoffs.  Cutoffs are:

        +-------+---------------------------+
        | Index | Risk Level Cutoff Value   |
        +=======+===========================+
        |   0   | Low to medium             |
        +-------+---------------------------+
        |   1   | Medium to high            |
        +-------+---------------------------+

    :ivar float RAMSTK_HR_MULTIPLIER: The failure rate multiplier.  All failure
        rates will be multiplied by this value for display.  This allows
        failure rates to display without using scientific notation.  Set to one
        to use scientific notation.  Default value is *1000000.0*.
    :ivar float RAMSTK_MTIME: The default mission time for new RAMSTK Programs.
    :ivar int RAMSTK_DEC_PLACES: Number of decimal places to show in numerical
        results.  Default value is *6*.
    :ivar int RAMSTK_MODE_SOURCE: Indicator variable used to determine which
        failure mode source to use.  Sources are:

            1. FMD-97
            2. MIL-STD-338

    :ivar str RAMSTK_CONF_DIR: Path to the directory containing configuration
        files used by RAMSTK.  Default values are:

            - POSIX default: *$HOME/.config/RAMSTK*
            - Windows default: *C:\\\Users\\\<USER NAME>\\\config\\\RAMSTK*

    :ivar str RAMSTK_DATA_DIR: Path to the directory containing data files used
        by RAMSTK.  Default values are:

            - POSIX default: */usr/share/RAMSTK*
            - Windows default: *None*

    :ivar str RAMSTK_ICON_DIR: Path to the directory containing icon files used
        by RAMSTK.  Default values are:

            - POSIX default: */usr/share/RAMSTK/icons*
            - Windows default: *None*

    :ivar str RAMSTK_LOG_DIR: Path to the directory containing log files used
        by RAMSTK.  Default values are:

            - POSIX default: */var/log*
            - Windows default: *C:\\\Users\\\<USER NAME>\\\config\\\RAMSTK\\\logs*

    :ivar str RAMSTK_PROG_DIR: Path to the base directory containing RAMSTK
        Program database files.  This is only used when the backend is SQLite3.
        Default values are:

            - POSIX default: *$HOME/analyses/ramstk*
            - Windows default: *C:\\\Users\\\<USER NAME>\\\analyses\\\ramstk*

    :ivar str RAMSTK_GUI_LAYOUT: Layout of the GUI to use.  Possible options
        are:

            * basic - a single window embedded with the Module Book, Work Book,
                and List Book.
            * advanced - multiple windows; one each for the Module Book, Work
                Book, and List Book.

        Default value is *basic*.

    :ivar str RAMSTK_COM_BACKEND: RAMSTK common database backend to use.
        Options are:

            * mysql (future)
            * sqlite

    :ivar str RAMSTK_BACKEND: RAMSTK Program database backend to use.  Options
        are:

            * mysql (future)
            * sqlite

    :ivar str RAMSTK_LOCALE: The language locale to use with RAMSTK.  Default
        value is *en_US*.
    :ivar str RAMSTK_OS: The operating system RAMSTK is currently running on.
    """
    def __init__(self):
        """Initialize the RAMSTK configuration parser."""
        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_colors = [
            "revisionfg",
            "functionfg",
            "requirementfg",
            "hardwarefg",
            "validationfg",
            "revisionbg",
            "functionbg",
            "requirementbg",
            "hardwarebg",
            "validationbg",
            "stakeholderbg",
            "stakeholderfg",
        ]
        self._lst_format_files = [
            "allocation",
            "failure_definition",
            "fmea",
            "function",
            "hardware",
            "hazops",
            "pof",
            "requirement",
            "revision",
            "similaritem",
            "stakeholder",
            "validation",
        ]

        # Initialize private scalar attributes.
        self._INSTALL_PREFIX = Utilities.prefix()

        # Initialize public dictionary attributes.
        self.RAMSTK_FORMAT_FILE: Dict[str, str] = {}
        self.RAMSTK_COLORS: Dict[str, str] = {}
        self.RAMSTK_COM_INFO: Dict[str, str] = {}
        self.RAMSTK_PROG_INFO: Dict[str, str] = {}
        self.RAMSTK_TABPOS = {
            "listbook": "top",
            "modulebook": "bottom",
            "workbook": "bottom",
        }

        # Initialize public list attributes.
        self.RAMSTK_RISK_POINTS = [4, 10]

        # Initialize public scalar attributes.
        if sys.platform == "linux" or sys.platform == "linux2":
            self.RAMSTK_OS = "Linux"
            self.RAMSTK_SITE_DIR = self._INSTALL_PREFIX + "/share/RAMSTK"
            self.RAMSTK_HOME_DIR = environ["HOME"]
            self.RAMSTK_LOG_DIR = "/var/log/RAMSTK"

        elif sys.platform == "win32":
            self.RAMSTK_OS = "Windows"
            self.RAMSTK_SITE_DIR = environ["PYTHONPATH"] + "/RAMSTK"
            self.RAMSTK_HOME_DIR = environ["USERPROFILE"]
            self.RAMSTK_LOG_DIR = self.RAMSTK_SITE_DIR + "/logs"

        self.RAMSTK_DATA_DIR = self.RAMSTK_SITE_DIR + "/layouts"
        self.RAMSTK_ICON_DIR = self.RAMSTK_SITE_DIR + "/icons"
        self.RAMSTK_PROG_DIR = self.RAMSTK_HOME_DIR + "/analyses/ramstk/"
        self.RAMSTK_CONF_DIR = self.RAMSTK_SITE_DIR

        self.RAMSTK_SITE_CONF = ""
        self.RAMSTK_PROG_CONF = ""
        self.RAMSTK_DEBUG_LOG = ""
        self.RAMSTK_IMPORT_LOG = ""
        self.RAMSTK_USER_LOG = ""

        self.RAMSTK_MODE = ""
        self.RAMSTK_MODE_SOURCE = 1  # 1=FMD-97
        self.RAMSTK_COM_BACKEND = ""
        self.RAMSTK_BACKEND = ""
        self.RAMSTK_REPORT_SIZE = "letter"
        self.RAMSTK_HR_MULTIPLIER = 1000000.0
        self.RAMSTK_DEC_PLACES = 6
        self.RAMSTK_MTIME = 100.0
        self.RAMSTK_GUI_LAYOUT = "advanced"
        self.RAMSTK_METHOD = "STANDARD"  # STANDARD or LRM
        self.RAMSTK_LOCALE = "en_US"

        self.RAMSTK_MODULES: Dict[str, str] = {}  # Static.

    def _do_make_configuration_dir(self):
        """
        Creates the user configuration directory.

        :return: None
        :rtype: None
        """
        self.RAMSTK_CONF_DIR = self.RAMSTK_HOME_DIR + "/.config/RAMSTK"
        try:
            makedirs(self.RAMSTK_CONF_DIR)
            self.RAMSTK_PROG_CONF = self.RAMSTK_CONF_DIR + "/RAMSTK.toml"
        except OSError:
            _error_msg = ("User's configuration directory {0:s} does not "
                          "exist and could not be created when attempting to "
                          "create a new user configuration file.".format(
                              self.RAMSTK_CONF_DIR))
            pub.sendMessage('fail_create_user_configuration',
                            error_message=_error_msg)

    def _do_make_data_dir(self):
        """
        Creates the user data directory.

        :return: None
        :rtype: None
        """
        self.RAMSTK_DATA_DIR = self.RAMSTK_CONF_DIR + "/layouts"
        if not Utilities.dir_exists(self.RAMSTK_DATA_DIR):
            try:
                makedirs(self.RAMSTK_DATA_DIR)
            except OSError:
                _error_msg = ("User's data directory {0:s} does not exist and "
                              "could not be created when attempting to create "
                              "a new user configuration file.".format(
                                  self.RAMSTK_DATA_DIR))
                pub.sendMessage('fail_create_user_configuration',
                                error_message=_error_msg)

    def _do_make_icon_dir(self):
        """
        Creates the user icon directory.

        :return: None
        :rtype: None
        """
        self.RAMSTK_ICON_DIR = self.RAMSTK_CONF_DIR + "/icons"

        if not Utilities.dir_exists(self.RAMSTK_ICON_DIR):
            try:
                makedirs(self.RAMSTK_ICON_DIR)
            except OSError:
                _error_msg = ("User's icon directory {0:s} does not exist and "
                              "could not be created when attempting to create "
                              "a new user configuration file.".format(
                                  self.RAMSTK_ICON_DIR))
                pub.sendMessage('fail_create_user_configuration',
                                error_message=_error_msg)

    def _do_make_log_dir(self):
        """
        Creates the user log directory.

        :return: None
        :rtype: None
        """
        self.RAMSTK_LOG_DIR = self.RAMSTK_CONF_DIR + "/logs"

        if not Utilities.dir_exists(self.RAMSTK_LOG_DIR):
            try:
                makedirs(self.RAMSTK_LOG_DIR)
            except OSError:
                _error_msg = ("User's log directory {0:s} does not exist and "
                              "could not be created when attempting to create "
                              "a new user configuration file.".format(
                                  self.RAMSTK_LOG_DIR))
                pub.sendMessage('fail_create_user_configuration',
                                error_message=_error_msg)

    def _do_make_program_dir(self):
        """
        Creates the user program directory.

        :return: None
        :rtype: None
        """
        if not Utilities.dir_exists(self.RAMSTK_PROG_DIR):
            try:
                makedirs(self.RAMSTK_PROG_DIR)
            except OSError:
                _error_msg = ("Program directory {0:s} does not exist and "
                              "could not be created when attempting to create "
                              "a new user configuration file.".format(
                                  self.RAMSTK_PROG_DIR))
                pub.sendMessage('fail_create_user_configuration',
                                error_message=_error_msg)

    def do_create_user_configuration(self):
        """
        Create the default user configuration file.

        :return: None
        :rtype: None
        """
        # Create the directories needed for the user.  Always prefer the RAMSTK
        # directories in the user's $HOME over the system-wide directories.
        self._do_make_configuration_dir()
        self._do_make_data_dir()
        self._do_make_icon_dir()
        self._do_make_log_dir()
        self._do_make_program_dir()

        # Copy format files from RAMSTK_SITE_DIR (system) to the user's
        # RAMSTK_CONF_DIR.
        for _file in glob.glob(self.RAMSTK_SITE_DIR + "/layouts/*.toml"):
            file_util.copy_file(_file, self.RAMSTK_DATA_DIR)

        # Copy the icons from RAMSTK_SITE_DIR (system) to the user's
        # RAMSTK_ICON_DIR.
        try:
            dir_util.copy_tree(
                self.RAMSTK_SITE_DIR + "/icons/",
                self.RAMSTK_ICON_DIR,
            )
        except IOError as _error:
            # TODO: Handle this error by broadcasting an appropriate fail
            # message.
            print(_error)

        # Create the default RAMSTK user configuration file.
        _dic_user_configuration = {
            "title": "RAMSTK User Configuration",
            "general": {
                "firstrun": "True",
                "reportsize": "letter",
                "frmultiplier": "1000000.0",
                "calcreltime": "100.0",
                "decimal": "6",
                "modesource": "1",
                "moduletabpos": "top",
                "listtabpos": "bottom",
                "worktabpos": "bottom"
            },
            "backend": {
                "type": "sqlite",
                "host": "localhost",
                "socket": "3306",
                "database": "",
                "user": "",
                "password": ""
            },
            "directories": {
                "datadir": self.RAMSTK_DATA_DIR,
                "icondir": self.RAMSTK_ICON_DIR,
                "logdir": self.RAMSTK_LOG_DIR,
                "progdir": self.RAMSTK_PROG_DIR
            },
            "layouts": {
                "allocation": "Allocation.xml",
                "failure_definition": "FailureDefinition.xml",
                "fmea": "FMEA.xml",
                "function": "Function.xml",
                "hardware": "Hardware.xml",
                "hazops": "HazOps.xml",
                "pof": "PoF.xml",
                "requirement": "Requirement.xml",
                "revision": "Revision.xml",
                "similaritem": "SimilarItem.xml",
                "stakeholder": "Stakeholder.xml",
                "validation": "Validation.xml"
            },
            "colors": {
                "functionbg": "#FFFFFF",
                "functionfg": "#000000",
                "hardwarebg": "#FFFFFF",
                "hardwarefg": "#000000",
                "requirementbg": "#FFFFFF",
                "requirementfg": "#000000",
                "revisionbg": "#FFFFFF",
                "revisionfg": "#000000",
                "stakeholderbg": "#FFFFFF",
                "stakeholderfg": "#000000",
                "validationbg": "#FFFFFF",
                "validationfg": "#000000"
            }
        }

        toml.dump(_dic_user_configuration, open(self.RAMSTK_PROG_CONF, "w"))

        pub.sendMessage('succeed_create_user_configuration')

    def get_user_configuration(self):
        """
        Read the RAMSTK configuration file.

        :return: None
        :rtype: None
        """
        # Try to read the user's configuration file.  If it doesn't exist,
        # create a new one.  If those options fail, read the system-wide
        # configuration file and keep going.
        if Utilities.file_exists(self.RAMSTK_PROG_CONF):
            _config = toml.load(self.RAMSTK_PROG_CONF)

            for _color in _config['colors']:
                self.RAMSTK_COLORS[_color] = _config['colors'][_color]

            for _file in _config['layouts']:
                self.RAMSTK_FORMAT_FILE[_file] = _config['layouts'][_file]

            self.RAMSTK_BACKEND = _config['backend']['type']
            self.RAMSTK_PROG_INFO["host"] = _config['backend']['host']
            self.RAMSTK_PROG_INFO["socket"] = _config['backend']['socket']
            self.RAMSTK_PROG_INFO["database"] = _config['backend']['database']
            self.RAMSTK_PROG_INFO["user"] = _config['backend']['user']
            self.RAMSTK_PROG_INFO["password"] = _config['backend']['password']

            self.RAMSTK_DATA_DIR = _config['directories']['datadir']
            self.RAMSTK_ICON_DIR = _config['directories']['icondir']
            self.RAMSTK_LOG_DIR = _config['directories']['logdir']
            self.RAMSTK_PROG_DIR = _config['directories']['progdir']

            self.RAMSTK_REPORT_SIZE = _config['general']['reportsize']
            self.RAMSTK_HR_MULTIPLIER = float(
                _config['general']['frmultiplier'])
            self.RAMSTK_DEC_PLACES = int(_config['general']['decimal'])
            self.RAMSTK_MTIME = float(_config['general']['calcreltime'])
            self.RAMSTK_MODE_SOURCE = _config['general']['modesource']
            self.RAMSTK_TABPOS["listbook"] = _config['general']['listtabpos']
            self.RAMSTK_TABPOS["modulebook"] = _config['general'][
                'moduletabpos']
            self.RAMSTK_TABPOS["workbook"] = _config['general']['worktabpos']
        else:
            _error_msg = ("Failed to read user's RAMSTK configuration file "
                          "{0:s}.").format(self.RAMSTK_PROG_CONF)
            pub.sendMessage('fail_get_user_configuration',
                            error_message=_error_msg)

    def set_user_configuration(self):
        """
        Write changes to the user's configuration file.

        :return: None
        :rtype: None
        :raises: KeyError if global dict variables are missing information.
        """
        if Utilities.file_exists(self.RAMSTK_PROG_CONF):
            _dic_user_configuration = {
                "title": "RAMSTK User Configuration",
                "general": {
                    "firstrun": "False",
                    "reportsize": str(self.RAMSTK_REPORT_SIZE),
                    "frmultiplier": str(self.RAMSTK_HR_MULTIPLIER),
                    "calcreltime": str(self.RAMSTK_MTIME),
                    "decimal": str(self.RAMSTK_DEC_PLACES),
                    "modesource": str(self.RAMSTK_MODE_SOURCE),
                    "moduletabpos": self.RAMSTK_TABPOS["modulebook"],
                    "listtabpos": self.RAMSTK_TABPOS["listbook"],
                    "worktabpos": self.RAMSTK_TABPOS["workbook"]
                },
                "backend": {
                    "type": str(self.RAMSTK_BACKEND),
                    "host": str(self.RAMSTK_PROG_INFO["host"]),
                    "socket": str(self.RAMSTK_PROG_INFO["socket"]),
                    "database": str(self.RAMSTK_PROG_INFO["database"]),
                    "user": str(self.RAMSTK_PROG_INFO["user"]),
                    "password": str(self.RAMSTK_PROG_INFO["password"])
                },
                "directories": {
                    "datadir": self.RAMSTK_DATA_DIR,
                    "icondir": self.RAMSTK_ICON_DIR,
                    "logdir": self.RAMSTK_LOG_DIR,
                    "progdir": self.RAMSTK_PROG_DIR
                },
                "layouts": {
                    "allocation":
                    self.RAMSTK_FORMAT_FILE['allocation'],
                    "failure_definition":
                    self.RAMSTK_FORMAT_FILE['failure_definition'],
                    "fmea":
                    self.RAMSTK_FORMAT_FILE['fmea'],
                    "function":
                    self.RAMSTK_FORMAT_FILE['function'],
                    "hardware":
                    self.RAMSTK_FORMAT_FILE['hardware'],
                    "hazops":
                    self.RAMSTK_FORMAT_FILE['hazops'],
                    "pof":
                    self.RAMSTK_FORMAT_FILE['pof'],
                    "requirement":
                    self.RAMSTK_FORMAT_FILE['requirement'],
                    "revision":
                    self.RAMSTK_FORMAT_FILE['revision'],
                    "similaritem":
                    self.RAMSTK_FORMAT_FILE['similaritem'],
                    "stakeholder":
                    self.RAMSTK_FORMAT_FILE['stakeholder'],
                    "validation":
                    self.RAMSTK_FORMAT_FILE['validation']
                },
                "colors": {
                    "functionbg": self.RAMSTK_COLORS['functionbg'],
                    "functionfg": self.RAMSTK_COLORS['functionfg'],
                    "hardwarebg": self.RAMSTK_COLORS['hardwarebg'],
                    "hardwarefg": self.RAMSTK_COLORS['hardwarefg'],
                    "requirementbg": self.RAMSTK_COLORS['requirementbg'],
                    "requirementfg": self.RAMSTK_COLORS['requirementfg'],
                    "revisionbg": self.RAMSTK_COLORS['revisionbg'],
                    "revisionfg": self.RAMSTK_COLORS['revisionfg'],
                    "stakeholderbg": self.RAMSTK_COLORS['stakeholderbg'],
                    "stakeholderfg": self.RAMSTK_COLORS['stakeholderfg'],
                    "validationbg": self.RAMSTK_COLORS['validationbg'],
                    "validationfg": self.RAMSTK_COLORS['validationfg']
                }
            }

            _config = toml.dump(_dic_user_configuration,
                                open(self.RAMSTK_PROG_CONF, "w"))
            pub.sendMessage('succeed_set_user_configuration',
                            configuration=_config)

    def set_user_directories(self, first_run=True):
        """
        Set the user-specific configuration directories.

        :keyword bool first_run: indicates whether this is the first time
            RAMSTK has been run by this user on a machine.  If so, there would
            be no user configuration directory or files.
        :return: True if the first run, False otherwise.
        :rtype: bool
        """
        # Prefer user-specific directories in their $HOME directory over the
        # system-wide directories.
        if Utilities.dir_exists(self.RAMSTK_HOME_DIR + "/.config/RAMSTK"):
            self.RAMSTK_CONF_DIR = self.RAMSTK_HOME_DIR + "/.config/RAMSTK"
        else:
            self.RAMSTK_CONF_DIR = self.RAMSTK_SITE_DIR

        self.RAMSTK_PROG_CONF = self.RAMSTK_CONF_DIR + "/RAMSTK.toml"

        return first_run
