# -*- coding: utf-8 -*-
#
#       ramstk.Configuration.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Configuration information and methods for RAMSTK."""

# Standard Library Imports
import gettext
import glob
import sys
# pylint: disable=no-name-in-module
from distutils import dir_util, file_util
# pylint: disable=no-name-in-module
from distutils.errors import DistutilsFileError
from os import environ, makedirs
from typing import Any, Dict, List, Tuple

# Third Party Imports
# noinspection PyPackageRequirements
import toml
from pubsub import pub

# RAMSTK Package Imports
from ramstk.utilities import dir_exists, file_exists, get_install_prefix

_ = gettext.gettext

# Define global list constants.
RAMSTK_ACTIVE_ENVIRONMENTS = [[_("Ground, Benign")], [_("Ground, Fixed")],
                              [_("Ground, Mobile")], [_("Naval, Sheltered")],
                              [_("Naval, Unsheltered")],
                              [_("Airborne, Inhabited, Cargo")],
                              [_("Airborne, Inhabited, Fighter")],
                              [_("Airborne, Uninhabited, Cargo")],
                              [_("Airborne, Uninhabited, Fighter")],
                              [_("Airborne, Rotary Wing")],
                              [_("Space, Flight")], [_("Missile, Flight")],
                              [_("Missile, Launch")]]
RAMSTK_DORMANT_ENVIRONMENTS = [[_("Airborne")], [_("Ground")], [_("Naval")],
                               [_("Space")]]

RAMSTK_ALLOCATION_MODELS = [["Equal Apportionment"], ["ARINC Apportionment"],
                            ["AGREE Apportionment"],
                            ["Feasibility of Objectives"],
                            ["Repairable Systems Apportionment"]]

RAMSTK_HR_TYPES = [[_("Assessed")], [_("Defined, Hazard Rate")],
                   [_("Defined, MTBF")], [_("Defined, Distribution")]]
RAMSTK_HR_MODELS = [[_("MIL-HDBK-217F Parts Count")],
                    [_("MIL-HDBK-217F Parts Stress")], [_("NSWC-11")]]
RAMSTK_HR_DISTRIBUTIONS = [[_("1P Exponential")], [_("2P Exponential")],
                           [_("Gaussian")], [_("Lognormal")],
                           [_("2P Weibull")], [_("3P Weibull")]]

RAMSTK_CONTROL_TYPES = [_("Prevention"), _("Detection")]
RAMSTK_COST_TYPES = [[_("Defined")], [_("Calculated")]]
RAMSTK_MTTR_TYPES = [[_("Defined")], [_("Calculated")]]

RAMSTK_CRITICALITY = [
    [
        _("Catastrophic"),
        _("Could result in death, permanent total disability, loss "
          "exceeding $1M, or irreversible severe environmental damage that "
          "violates law or regulation."), "I", 4
    ],
    [
        _("Critical"),
        _("Could result in permanent partial disability, injuries or "
          "occupational illness that may result in hospitalization of at "
          "least three personnel, loss exceeding $200K but less than $1M, "
          "or reversible environmental damage causing a violation of law or "
          "regulation."), "II", 3
    ],
    [
        _("Marginal"),
        _("Could result in injury or occupational illness resulting in one "
          "or more lost work days(s), loss exceeding $10K but less than "
          "$200K, or mitigatible environmental damage without violation of "
          "law or regulation where restoration activities can be "
          "accomplished."), "III", 2
    ],
    [
        _("Negligble"),
        _("Could result in injury or illness not resulting in a lost work "
          "day, loss exceeding $2K but less than $10K, or minimal "
          "environmental damage not violating law or regulation."), "IV", 1
    ]
]
RAMSTK_FAILURE_PROBABILITY = [[_("Level E - Extremely Unlikely"), 1],
                              [_("Level D - Remote"), 2],
                              [_("Level C - Occasional"), 3],
                              [_("Level B - Reasonably Probable"), 4],
                              [_("Level A - Frequent"), 5]]

RAMSTK_SW_DEV_ENVIRONMENTS = [[_("Organic"), 1.0, 0.76],
                              [_("Semi-Detached"), 1.0, 1.0],
                              [_("Embedded"), 1.0, 1.3]]
RAMSTK_SW_DEV_PHASES = [[_("Concept/Planning (PCP)")],
                        [_("Requirements Analysis (SRA)")],
                        [_("Preliminary Design Review (PDR)")],
                        [_("Critical Design Review (CDR)")],
                        [_("Test Readiness Review (TRR)")], [_("Released")]]
RAMSTK_SW_LEVELS = [[_("Software System"), 0], [_("Software Module"), 0],
                    [_("Software Unit"), 0]]
RAMSTK_SW_APPLICATION = [[_("Airborne"), 0.0128, 6.28],
                         [_("Strategic"), 0.0092, 1.2],
                         [_("Tactical"), 0.0078, 13.8],
                         [_("Process Control"), 0.0018, 3.8],
                         [_("Production Center"), 0.0085, 23.0],
                         [_("Developmental"), 0.0123, 132.6]]
RAMSTK_SW_TEST_METHODS = [[
    _("Code Reviews"),
    _("Code review is a systematic examination (often known as peer "
      "review) of computer source code."),
], [
    _("Error/Anomaly Detection"),
    _(""),
], [
    _("Structure Analysis"),
    _(""),
], [
    _("Random Testing"),
    _(""),
], [
    _("Functional Testing"),
    _(""),
], [
    _("Branch Testing"),
    _(""),
]]

RAMSTK_LIFECYCLE = [[_("Design")], [_("Reliability Growth")],
                    [_("Reliability Qualification")], [_("Production")],
                    [_("Storage")], [_("Operation")], [_("Disposal")]]
RAMSTK_S_DIST = [["Constant Probability"], ["Exponential"], ["Gaussian"],
                 ["LogNormal"], ["Uniform"], ["Weibull"]]


class RAMSTKSiteConfiguration:
    """Class for site-wide RAMSTK configuration settings."""
    def __init__(self) -> None:
        """Initialize the RAMSTK site configuration class."""
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._INSTALL_PREFIX = get_install_prefix()

        # Initialize public dictionary attributes.
        self.RAMSTK_COM_INFO: Dict[str, str] = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.RAMSTK_COM_BACKEND = ""
        if sys.platform == "linux" or sys.platform == "linux2":
            self.RAMSTK_SITE_DIR = self._INSTALL_PREFIX + "/share/RAMSTK"
        elif sys.platform == "win32":
            self.RAMSTK_SITE_DIR = environ["PYTHONPATH"] + "/RAMSTK"

        self.RAMSTK_SITE_CONF = self.RAMSTK_SITE_DIR + "/Site.toml"

    def do_create_site_configuration(self) -> None:
        """Create the default site configuration file.

        :return: None
        :rtype: None
        """
        _dic_site_configuration = {
            "title": "RAMSTK Site Configuration",
            "backend": {
                "dialect": "postgres",
                "host": "",
                "port": "5432",
                "database": 'ramstk_common_ramstk',
                "user": "first_run",
                "password": ""
            }
        }

        try:
            toml.dump(_dic_site_configuration, open(self.RAMSTK_SITE_CONF,
                                                    "w"))
            pub.sendMessage('succeed_create_site_configuration')
        except FileNotFoundError:
            _error_msg = (
                "Failed to write site configuration file {0:s}.".format(
                    self.RAMSTK_SITE_CONF))
            pub.sendMessage('fail_create_site_configuration',
                            error_message=_error_msg)

    def get_site_configuration(self) -> None:
        """Read the site configuration file.

        :return: None
        :rtype: None
        """
        if file_exists(self.RAMSTK_SITE_CONF):
            _config = toml.load(self.RAMSTK_SITE_CONF)

            self.RAMSTK_COM_BACKEND = _config['backend']['dialect']
            self.RAMSTK_COM_INFO["dialect"] = _config['backend']['dialect']
            self.RAMSTK_COM_INFO["host"] = _config['backend']['host']
            self.RAMSTK_COM_INFO["port"] = _config['backend']['port']
            self.RAMSTK_COM_INFO["database"] = _config['backend']['database']
            self.RAMSTK_COM_INFO["user"] = _config['backend']['user']
            self.RAMSTK_COM_INFO["password"] = _config['backend']['password']

        else:
            _error_msg = ("Failed to read Site configuration file "
                          "{0:s}.").format(self.RAMSTK_SITE_CONF)
            pub.sendMessage('fail_get_site_configuration',
                            error_message=_error_msg)

    def set_site_configuration(self) -> None:
        """Set the site-wide RAMSTK configuration file values."""
        _dic_site_configuration: Dict[str, Any] = {
            "title": "RAMSTK Site Configuration",
            "backend": {
                "dialect": self.RAMSTK_COM_INFO["dialect"],
                "host": str(self.RAMSTK_COM_INFO["host"]),
                "port": str(self.RAMSTK_COM_INFO["port"]),
                "database": str(self.RAMSTK_COM_INFO["database"]),
                "user": str(self.RAMSTK_COM_INFO["user"]),
                "password": str(self.RAMSTK_COM_INFO["password"])
            }
        }
        toml.dump(_dic_site_configuration, open(self.RAMSTK_SITE_CONF, "w"))

    def set_site_directories(self) -> None:
        """Set the site-wide RAMSTK directories.

        :return: None
        :rtype: None
        """
        self.RAMSTK_SITE_DIR = self._INSTALL_PREFIX + "/share/RAMSTK"
        self.RAMSTK_SITE_CONF = self.RAMSTK_SITE_DIR + "/Site.toml"

        if not file_exists(self.RAMSTK_SITE_CONF):
            self.do_create_site_configuration()


class RAMSTKUserConfiguration:  # pylint: disable=too-many-instance-attributes
    """RAMSTK configuration class.

    Attributes of the Configuration class are:

    :ivar dict RAMSTK_FORMAT_FILE: Dictionary containing the path to the format
        files to use for various widgets.  Keys are the name of the RAMSTK
        work stream module, values are the absolute path to the format file
        for that work stream module.
    :ivar dict RAMSTK_COLORS: Dictionary containing the colors to use for
        various widgets.
    :ivar dict RAMSTK_COM_INFO: Dictionary for the RAMSTK common database
        connection information.  The information contained is:

            +----------+-------------------------------+
            |   Key    | Information                   |
            +==========+===============================+
            |   host   | Host name                     |
            +----------+-------------------------------+
            |   port   | Host port                     |
            +----------+-------------------------------+
            | database | Database name                 |
            +----------+-------------------------------+
            |   user   | User name                     |
            +----------+-------------------------------+
            | password | User password                 |
            +----------+-------------------------------+

    :ivar dict RAMSTK_PROG_INFO: Dictionary for RAMSTK Program database
        connection information.  The information contained is:

            +----------+-------------------------------+
            |   Key    | Information                   |
            +==========+===============================+
            |   host   | Host name                     |
            +----------+-------------------------------+
            |   port   | Host port                     |
            +----------+-------------------------------+
            | database | Database name                 |
            +----------+-------------------------------+
            |   user   | User name                     |
            +----------+-------------------------------+
            | password | User password                 |
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

    :ivar dict RAMSTK_SEVERITY: Dictionary for failure severity categories.
    :ivar dict RAMSTK_HAZARDS: Dictionary for potential hazards.
    :ivar dict RAMSTK_REQUIREMENT_TYPES: Dictionary of requirement types.
    :ivar dict RAMSTK_RPN_SEVERITY: Dictionary for RPN Severity categories.
    :ivar dict RAMSTK_RPN_OCCURRENCE: Dictionary for RPN Occurrence categories.
    :ivar dict RAMSTK_RPN_DETECTION: Dictionary for RPN Detection categories.
    :ivar dict RAMSTK_MODULES: Dictionary of active modules in the open RAMSTK
        Program database.  Where 1 = active and 0 = inactive.  Keys are:

            * Function
            * Hardware
            * Requirements
            * Revision
            * Validation

    :ivar list RAMSTK_PAGE_NUMBER: Dictionary indicating which page each RAMSTK
        module occupies in the ModuleBook.
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
        files used by RAMSTK.
    :ivar str RAMSTK_DATA_DIR: Path to the directory containing data files used
        by RAMSTK.
    :ivar str RAMSTK_ICON_DIR: Path to the directory containing icon files used
        by RAMSTK.
    :ivar str RAMSTK_LOG_DIR: Path to the directory containing log files used
        by RAMSTK.
    :ivar str RAMSTK_PROG_DIR: Path to the base directory containing RAMSTK
        Program database files.  This is only used when the backend is SQLite3.
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

    # pylint: disable=too-many-statements
    def __init__(self) -> None:
        """Class for user-specific RAMSTK configuration settings."""
        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_colors = [
            'allocationbg', 'allocationfg', 'fmeabg', 'fmeafg',
            'failure_definitionbg', 'failure_definitionfg', 'functionbg',
            'functionfg', 'hardwarebg', 'hardwarefg', 'hazardbg', 'hazardfg',
            'pofbg', 'poffg', 'revisionbg', 'revisionfg', 'requirementfg',
            'requirementbg', 'validationbg', 'validationfg', 'similar_itembg',
            'similar_itemfg', 'stakeholderbg', 'stakeholderfg'
        ]
        self._lst_format_files = [
            "allocation", "failure_definitions", "fmea", "function",
            "hardware", "hazard", "pof", "requirement", "revision",
            "similar_item", "stakeholders", "usage_profile", "validation"
        ]
        self._lst_categories = [
            'integratedcircuit', 'semiconductor', 'resistor', 'capacitor',
            'inductor', 'relay', 'switch', 'connection', 'meter',
            'miscellaneous'
        ]

        # Initialize private scalar attributes.
        self._INSTALL_PREFIX = get_install_prefix()
        self._data_sub_dir = "/layouts"
        self._icon_sub_dir = "/icons"
        self._logs_sub_dir = "/logs"

        # Initialize public dictionary attributes.
        self.RAMSTK_ACTION_CATEGORY: Dict[str, Tuple[str, str, str, str]] = {}
        self.RAMSTK_ACTION_STATUS: Dict[str, Tuple[str, str, str]] = {}
        self.RAMSTK_AFFINITY_GROUPS: Dict[str, Tuple[str, str]] = {}  # User.
        self.RAMSTK_CATEGORIES: Dict[str, str] = {}  # Static.
        self.RAMSTK_DAMAGE_MODELS: Dict[str, str] = {}  # User.
        self.RAMSTK_DETECTION_METHODS: Dict[str, Tuple[str, str, str]] = {}
        self.RAMSTK_FAILURE_MODES: Dict[str, str] = {}  # User.
        self.RAMSTK_HAZARDS: Dict[str, Tuple[str, str]] = {}  # User.
        self.RAMSTK_INCIDENT_CATEGORY: Dict[str, Tuple[str, str, str,
                                                       str]] = {}
        self.RAMSTK_INCIDENT_STATUS: Dict[str, Tuple[str, str, str]] = {}
        self.RAMSTK_INCIDENT_TYPE: Dict[str, Tuple[str, str, str]] = {}
        self.RAMSTK_LOAD_HISTORY: Dict[int, str] = {}  # User.
        self.RAMSTK_MANUFACTURERS: Dict[str, Tuple[str, str,
                                                   str]] = {}  # User.
        self.RAMSTK_MEASURABLE_PARAMETERS: Dict[int, Tuple[str, str,
                                                           str]] = {}  # User.
        self.RAMSTK_MEASUREMENT_UNITS: Dict[str, Tuple[str, str,
                                                       str]] = {}  # Admin.
        self.RAMSTK_MODULES: Dict[str, str] = {}  # Static.
        self.RAMSTK_REQUIREMENT_TYPE: Dict[str, Tuple[str, str, str]] = {}
        self.RAMSTK_RPN_DETECTION: Dict[int, str] = {}  # User.
        self.RAMSTK_RPN_OCCURRENCE: Dict[int, str] = {}  # User.
        self.RAMSTK_RPN_SEVERITY: Dict[int, str] = {}  # User.
        self.RAMSTK_SEVERITY: Dict[str, Tuple[str, str, str,
                                              str]] = {}  # Admin
        self.RAMSTK_STAKEHOLDERS: Dict[str, str] = {}  # User.
        self.RAMSTK_STRESS_LIMITS: Dict[int, List[float]] = {}  # User.
        self.RAMSTK_SUBCATEGORIES: Dict[str, Dict[str, str]] = {}  # Static.
        self.RAMSTK_USERS: Dict[str, Tuple[str, str, str, str,
                                           str]] = {}  # Admin.
        self.RAMSTK_VALIDATION_TYPE: Dict[str, Tuple[str, str,
                                                     str]] = {}  # Admin.

        self.RAMSTK_COLORS: Dict[str, str] = {}
        self.RAMSTK_FORMAT_FILE: Dict[str, str] = {}
        self.RAMSTK_PAGE_NUMBER: Dict[int, str] = {
            0: 'revision',
            1: 'function',
            2: 'requirement',
            3: 'hardware',
            4: 'validation',
        }
        self.RAMSTK_PROG_INFO: Dict[str, str] = {
            "dialect": '',
            "host": '',
            "port": '',
            "database": '',
            "user": '',
            "password": ''
        }
        self.RAMSTK_TABPOS = {
            "listbook": "top",
            "modulebook": "bottom",
            "workbook": "bottom",
        }
        self.RAMSTK_WORKGROUPS: Dict[str, Tuple[str, str]] = {}  # Admin.

        # Initialize public list attributes.
        self.RAMSTK_FAILURE_PROBABILITY = [
            [_("Level E - Extremely Unlikely"), 1], [_("Level D - Remote"), 2],
            [_("Level C - Occasional"), 3],
            [_("Level B - Reasonably Probable"), 4],
            [_("Level A - Frequent"), 5]
        ]
        self.RAMSTK_RISK_POINTS = [4, 10]

        # Initialize public scalar attributes.
        self.RAMSTK_MODE = ""
        self.RAMSTK_MODE_SOURCE = 1  # 1=FMD-97
        self.RAMSTK_BACKEND = ""
        self.RAMSTK_REPORT_SIZE = "letter"
        self.RAMSTK_HR_MULTIPLIER = 1.0
        self.RAMSTK_DEC_PLACES = 6
        self.RAMSTK_MTIME = 100.0
        self.RAMSTK_GUI_LAYOUT = "advanced"
        self.RAMSTK_METHOD = "STANDARD"  # STANDARD or LRM
        self.RAMSTK_LOCALE = "en_US.UTF8"
        self.RAMSTK_LOGLEVEL = "INFO"
        if sys.platform == "linux" or sys.platform == "linux2":
            self.RAMSTK_OS = "Linux"
            self.RAMSTK_CONF_DIR = self._INSTALL_PREFIX + "/share/RAMSTK"
            self.RAMSTK_HOME_DIR = environ["HOME"]
        elif sys.platform == "win32":
            self.RAMSTK_OS = "Windows"
            self.RAMSTK_CONF_DIR = environ["PYTHONPATH"] + "/RAMSTK"
            self.RAMSTK_HOME_DIR = environ["USERPROFILE"]

        self.RAMSTK_DATA_DIR = self.RAMSTK_CONF_DIR + self._data_sub_dir
        self.RAMSTK_ICON_DIR = self.RAMSTK_CONF_DIR + self._icon_sub_dir
        self.RAMSTK_LOG_DIR = self.RAMSTK_CONF_DIR + self._logs_sub_dir
        self.RAMSTK_PROG_DIR = self.RAMSTK_HOME_DIR + "/analyses/ramstk/"

        self.RAMSTK_PROG_CONF = self.RAMSTK_CONF_DIR + "/RAMSTK.toml"
        self.RAMSTK_USER_LOG = self.RAMSTK_LOG_DIR + "/ramstk_run.log"
        self.RAMSTK_IMPORT_LOG = self.RAMSTK_LOG_DIR + "/ramstk_import.log"

        self.loaded = False

    def _do_make_configuration_dir(self) -> None:
        """Create the user configuration directory.

        :return: None
        :rtype: None
        """
        self.RAMSTK_CONF_DIR = self.RAMSTK_HOME_DIR + "/.config/RAMSTK"
        if not dir_exists(self.RAMSTK_CONF_DIR):
            try:
                makedirs(self.RAMSTK_CONF_DIR)
                self.RAMSTK_PROG_CONF = self.RAMSTK_CONF_DIR + "/RAMSTK.toml"
            except OSError:
                _error_msg = ("User's configuration directory {0:s} does not "
                              "exist and could not be created when attempting "
                              "to create a new user configuration "
                              "file.".format(self.RAMSTK_CONF_DIR))
                pub.sendMessage('fail_create_user_configuration',
                                error_message=_error_msg)

    def _do_make_data_dir(self) -> None:
        """Create the user data directory.

        :return: None
        :rtype: None
        """
        self.RAMSTK_DATA_DIR = self.RAMSTK_CONF_DIR + self._data_sub_dir
        if not dir_exists(self.RAMSTK_DATA_DIR):
            try:
                makedirs(self.RAMSTK_DATA_DIR)
            except OSError:
                _error_msg = ("User's data directory {0:s} does not exist and "
                              "could not be created when attempting to create "
                              "a new user configuration file.".format(
                                  self.RAMSTK_DATA_DIR))
                pub.sendMessage('fail_create_user_configuration',
                                error_message=_error_msg)

    def _do_make_icon_dir(self) -> None:
        """Create the user icon directory.

        :return: None
        :rtype: None
        """
        self.RAMSTK_ICON_DIR = self.RAMSTK_CONF_DIR + self._icon_sub_dir

        if not dir_exists(self.RAMSTK_ICON_DIR):
            try:
                makedirs(self.RAMSTK_ICON_DIR)
            except OSError:
                _error_msg = ("User's icon directory {0:s} does not exist and "
                              "could not be created when attempting to create "
                              "a new user configuration file.".format(
                                  self.RAMSTK_ICON_DIR))
                pub.sendMessage('fail_create_user_configuration',
                                error_message=_error_msg)

    def _do_make_log_dir(self) -> None:
        """Create the user log directory.

        :return: None
        :rtype: None
        """
        self.RAMSTK_LOG_DIR = self.RAMSTK_CONF_DIR + self._logs_sub_dir

        if not dir_exists(self.RAMSTK_LOG_DIR):
            try:
                makedirs(self.RAMSTK_LOG_DIR)
            except OSError:
                _error_msg = ("User's log directory {0:s} does not exist and "
                              "could not be created when attempting to create "
                              "a new user configuration file.".format(
                                  self.RAMSTK_LOG_DIR))
                pub.sendMessage('fail_create_user_configuration',
                                error_message=_error_msg)

    def _do_make_program_dir(self) -> None:
        """Create the user program directory.

        :return: None
        :rtype: None
        """
        if not dir_exists(self.RAMSTK_PROG_DIR):
            try:
                makedirs(self.RAMSTK_PROG_DIR)
            except OSError:
                _error_msg = ("Program directory {0:s} does not exist and "
                              "could not be created when attempting to create "
                              "a new user configuration file.".format(
                                  self.RAMSTK_PROG_DIR))
                pub.sendMessage('fail_create_user_configuration',
                                error_message=_error_msg)

    def do_create_user_configuration(self) -> None:
        """Create the default user configuration file.

        :return: None
        :rtype: None
        """
        # Create the directories needed for the user.  Always prefer the RAMSTK
        # directories in the user's $HOME over the system-wide directories.
        # Configuration directory.
        self._do_make_configuration_dir()
        self._do_make_data_dir()
        self._do_make_icon_dir()
        self._do_make_log_dir()
        self._do_make_program_dir()

        # Copy format files from RAMSTK_SITE_DIR (system) to the user's
        # RAMSTK_CONF_DIR.
        for _file in glob.glob(self._INSTALL_PREFIX
                               + "/share/RAMSTK/layouts/*.toml"):
            file_util.copy_file(_file, self.RAMSTK_DATA_DIR)

        # Copy the icons from RAMSTK_SITE_DIR (system) to the user's
        # RAMSTK_ICON_DIR.
        try:
            dir_util.copy_tree(self._INSTALL_PREFIX + "/share/RAMSTK/icons/",
                               self.RAMSTK_ICON_DIR)
        except DistutilsFileError:
            _error_msg = ('Attempt to copy RAMSTK icons from site-wide icon '
                          'directory {0:s} to user\'s icon directory {1:s} '
                          'failed.'.format(
                              self._INSTALL_PREFIX + "/share/RAMSTK/icons/",
                              self.RAMSTK_ICON_DIR))
            pub.sendMessage('fail_copy_icons_to_user',
                            error_message=_error_msg)

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
                "worktabpos": "bottom",
                "loglevel": "INFO"
            },
            "backend": {
                "dialect": "postgres",
                "host": "localhost",
                "port": "5432",
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
                "allocation": "allocation.toml",
                "failure_definitions": "failure_definition.toml",
                "fmea": "fmea.toml",
                "function": "function.toml",
                "hardware": "hardware.toml",
                "hazard": "hazops.toml",
                "pof": "pof.toml",
                "requirement": "requirement.toml",
                "revision": "revision.toml",
                "similar_item": "similar_item.toml",
                "stakeholders": "stakeholder.toml",
                "usage_profile": "usage_profile.toml",
                "validation": "validation.toml"
            },
            "colors": {
                'allocationbg': '#FFFFFF',
                'allocationfg': '#000000',
                'failure_definitionbg': '#FFFFFF',
                'failure_definitionfg': '#000000',
                'fmeabg': '#FFFFFF',
                'fmeafg': '#000000',
                'functionbg': '#FFFFFF',
                'functionfg': '#000000',
                'hardwarebg': '#FFFFFF',
                'hardwarefg': '#000000',
                'hazardbg': '#FFFFFF',
                'hazardfg': '#000000',
                'pofbg': '#FFFFFF',
                'poffg': '#000000',
                'requirementbg': '#FFFFFF',
                'requirementfg': '#000000',
                'revisionbg': '#FFFFFF',
                'revisionfg': '#000000',
                'similar_itembg': '#FFFFFF',
                'similar_itemfg': '#000000',
                'stakeholderbg': '#FFFFFF',
                'stakeholderfg': '#000000',
                'validationbg': '#FFFFFF',
                'validationfg': '#000000'
            },
            "stress": {
                'integratedcircuit':
                [0.8, 0.9, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
                'semiconductor':
                [1.0, 1.0, 0.7, 0.9, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
                'resistor':
                [1.0, 1.0, 0.5, 0.9, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
                'capacitor':
                [1.0, 1.0, 1.0, 1.0, 0.6, 0.9, 10.0, 0.0, 125.0, 125.0],
                'inductor':
                [0.6, 0.9, 1.0, 1.0, 0.5, 0.9, 15.0, 0.0, 125.0, 125.0],
                'relay':
                [0.75, 0.9, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
                'switch':
                [0.75, 0.9, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
                'connection':
                [0.7, 0.9, 1.0, 1.0, 0.7, 0.9, 25.0, 0.0, 125.0, 125.0],
                'meter':
                [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
                'miscellaneous':
                [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0]
            }
        }

        try:
            toml.dump(_dic_user_configuration, open(self.RAMSTK_PROG_CONF,
                                                    "w"))
            pub.sendMessage('succeed_create_user_configuration')
        except TypeError:
            _error_msg = ("User configuration file {0} is not a file.".format(
                self.RAMSTK_PROG_CONF))
            pub.sendMessage('fail_create_user_configuration',
                            error_message=_error_msg)

    def get_user_configuration(self) -> None:
        """Read the RAMSTK user configuration file.

        :return: None
        :rtype: None
        """
        # Try to read the user's configuration file.  If it doesn't exist,
        # create a new one.  If those options fail, read the system-wide
        # configuration file and keep going.
        if file_exists(self.RAMSTK_PROG_CONF):
            _config = toml.load(self.RAMSTK_PROG_CONF)

            for _color in self._lst_colors:
                self.RAMSTK_COLORS[_color] = _config["colors"][_color]

            for _file in self._lst_format_files:
                self.RAMSTK_FORMAT_FILE[_file] = _config["layouts"][_file]

            # Hardware categories are stored as integers, but configuration
            # file keys are human-readable nouns.  This converts the noun key
            # to the equivalent integer key.
            for _category in enumerate(self._lst_categories):
                self.RAMSTK_STRESS_LIMITS[
                    _category[0] + 1] = _config["stress"][_category[1]]

            self.RAMSTK_BACKEND = _config["backend"]["dialect"]
            self.RAMSTK_PROG_INFO["dialect"] = _config["backend"]["dialect"]
            self.RAMSTK_PROG_INFO["host"] = _config["backend"]["host"]
            self.RAMSTK_PROG_INFO["port"] = _config["backend"]["port"]
            self.RAMSTK_PROG_INFO["database"] = _config["backend"]["database"]
            self.RAMSTK_PROG_INFO["user"] = _config["backend"]["user"]
            self.RAMSTK_PROG_INFO["password"] = _config["backend"]["password"]

            self.RAMSTK_DATA_DIR = _config["directories"]["datadir"]
            self.RAMSTK_ICON_DIR = _config["directories"]["icondir"]
            self.RAMSTK_LOG_DIR = _config["directories"]["logdir"]
            self.RAMSTK_PROG_DIR = _config["directories"]["progdir"]

            self.RAMSTK_REPORT_SIZE = _config["general"]["reportsize"]
            self.RAMSTK_HR_MULTIPLIER = float(
                _config["general"]["frmultiplier"])
            self.RAMSTK_DEC_PLACES = int(_config["general"]["decimal"])
            self.RAMSTK_MTIME = float(_config["general"]["calcreltime"])
            self.RAMSTK_MODE_SOURCE = _config["general"]["modesource"]
            self.RAMSTK_TABPOS["listbook"] = _config["general"]["listtabpos"]
            self.RAMSTK_TABPOS["modulebook"] = _config["general"][
                "moduletabpos"]
            self.RAMSTK_TABPOS["workbook"] = _config["general"]["worktabpos"]
            self.RAMSTK_LOGLEVEL = _config["general"]["loglevel"]
            if self.RAMSTK_LOG_DIR == '':
                self.RAMSTK_USER_LOG = "./ramstk_run.log"
                self.RAMSTK_IMPORT_LOG = "./ramstk_import.log"
            else:
                self.RAMSTK_USER_LOG = (self.RAMSTK_LOG_DIR
                                        + "/ramstk_run.log")
                self.RAMSTK_IMPORT_LOG = (self.RAMSTK_LOG_DIR
                                          + "/ramstk_import.log")

        else:
            _error_msg = ("Failed to read User configuration file "
                          "{0:s}.").format(self.RAMSTK_PROG_CONF)
            pub.sendMessage('fail_get_user_configuration',
                            error_message=_error_msg)

    def set_user_configuration(self) -> None:
        """Write changes to the user's configuration file.

        :return: None
        :rtype: None
        """
        _dic_user_configuration: Dict[str, Any] = {
            "title": "RAMSTK User Configuration",
            "general": {
                "reportsize": self.RAMSTK_REPORT_SIZE,
                "frmultiplier": str(self.RAMSTK_HR_MULTIPLIER),
                "calcreltime": str(self.RAMSTK_MTIME),
                "decimal": str(self.RAMSTK_DEC_PLACES),
                "modesource": str(self.RAMSTK_MODE_SOURCE),
                "moduletabpos": self.RAMSTK_TABPOS["modulebook"],
                "listtabpos": self.RAMSTK_TABPOS["listbook"],
                "worktabpos": self.RAMSTK_TABPOS["workbook"],
                "loglevel": self.RAMSTK_LOGLEVEL
            },
            "backend": {
                "dialect": self.RAMSTK_PROG_INFO["dialect"],
                "host": str(self.RAMSTK_PROG_INFO["host"]),
                "port": str(self.RAMSTK_PROG_INFO["port"]),
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
                "failure_definitions":
                self.RAMSTK_FORMAT_FILE['failure_definitions'],
                "fmea":
                self.RAMSTK_FORMAT_FILE['fmea'],
                "function":
                self.RAMSTK_FORMAT_FILE['function'],
                "hardware":
                self.RAMSTK_FORMAT_FILE['hardware'],
                "hazard":
                self.RAMSTK_FORMAT_FILE['hazard'],
                "pof":
                self.RAMSTK_FORMAT_FILE['pof'],
                "requirement":
                self.RAMSTK_FORMAT_FILE['requirement'],
                "revision":
                self.RAMSTK_FORMAT_FILE['revision'],
                "similar_item":
                self.RAMSTK_FORMAT_FILE['similar_item'],
                "stakeholders":
                self.RAMSTK_FORMAT_FILE['stakeholders'],
                "usage_profile":
                self.RAMSTK_FORMAT_FILE['usage_profile'],
                "validation":
                self.RAMSTK_FORMAT_FILE['validation']
            },
            "colors": {
                'allocationbg': self.RAMSTK_COLORS['allocationbg'],
                'allocationfg': self.RAMSTK_COLORS['allocationbg'],
                'failure_definitionbg':
                self.RAMSTK_COLORS['failure_definitionbg'],
                'failure_definitionfg':
                self.RAMSTK_COLORS['failure_definitionbg'],
                'fmeabg': self.RAMSTK_COLORS['fmeabg'],
                'fmeafg': self.RAMSTK_COLORS['fmeafg'],
                "functionbg": self.RAMSTK_COLORS['functionbg'],
                "functionfg": self.RAMSTK_COLORS['functionfg'],
                "hardwarebg": self.RAMSTK_COLORS['hardwarebg'],
                "hardwarefg": self.RAMSTK_COLORS['hardwarefg'],
                "hazardbg": self.RAMSTK_COLORS['hazardbg'],
                "hazardfg": self.RAMSTK_COLORS['hazardfg'],
                'pofbg': self.RAMSTK_COLORS['pofbg'],
                'poffg': self.RAMSTK_COLORS['poffg'],
                "requirementbg": self.RAMSTK_COLORS['requirementbg'],
                "requirementfg": self.RAMSTK_COLORS['requirementfg'],
                "revisionbg": self.RAMSTK_COLORS['revisionbg'],
                "revisionfg": self.RAMSTK_COLORS['revisionfg'],
                'similar_itembg': self.RAMSTK_COLORS['similar_itembg'],
                'similar_itemfg': self.RAMSTK_COLORS['similar_itemfg'],
                "stakeholderbg": self.RAMSTK_COLORS['stakeholderbg'],
                "stakeholderfg": self.RAMSTK_COLORS['stakeholderfg'],
                "validationbg": self.RAMSTK_COLORS['validationbg'],
                "validationfg": self.RAMSTK_COLORS['validationfg']
            },
            "stress": {
                "integratedcircuit": self.RAMSTK_STRESS_LIMITS[1],
                "semiconductor": self.RAMSTK_STRESS_LIMITS[2],
                "resistor": self.RAMSTK_STRESS_LIMITS[3],
                "capacitor": self.RAMSTK_STRESS_LIMITS[4],
                "inductor": self.RAMSTK_STRESS_LIMITS[5],
                "relay": self.RAMSTK_STRESS_LIMITS[6],
                "switch": self.RAMSTK_STRESS_LIMITS[7],
                "connection": self.RAMSTK_STRESS_LIMITS[8],
                "meter": self.RAMSTK_STRESS_LIMITS[9],
                "miscellaneous": self.RAMSTK_STRESS_LIMITS[10]
            }
        }

        toml.dump(_dic_user_configuration, open(self.RAMSTK_PROG_CONF, "w"))

    def set_user_directories(self) -> None:
        """Set the user-specific configuration directories.

        :return: None
        :rtype: None
        """
        # Prefer user-specific directories in their $HOME directory over the
        # system-wide directories.
        if dir_exists(self.RAMSTK_HOME_DIR + "/.config/RAMSTK"):
            self.RAMSTK_CONF_DIR = self.RAMSTK_HOME_DIR + "/.config/RAMSTK"
        else:
            self.RAMSTK_CONF_DIR = self._INSTALL_PREFIX + "/share/RAMSTK"

        self.RAMSTK_PROG_CONF = self.RAMSTK_CONF_DIR + "/RAMSTK.toml"

        if dir_exists(self.RAMSTK_CONF_DIR + self._data_sub_dir):
            self.RAMSTK_DATA_DIR = self.RAMSTK_CONF_DIR + self._data_sub_dir
        else:
            self.RAMSTK_DATA_DIR = (self._INSTALL_PREFIX
                                    + "/share/RAMSTK/layouts")

        if dir_exists(self.RAMSTK_CONF_DIR + self._icon_sub_dir):
            self.RAMSTK_ICON_DIR = self.RAMSTK_CONF_DIR + self._icon_sub_dir
        else:
            self.RAMSTK_ICON_DIR = self._INSTALL_PREFIX + "/share/RAMSTK/icons"

        if dir_exists(self.RAMSTK_CONF_DIR + self._logs_sub_dir):
            self.RAMSTK_LOG_DIR = self.RAMSTK_CONF_DIR + self._logs_sub_dir
        else:
            self.RAMSTK_LOG_DIR = self._INSTALL_PREFIX + "/share/RAMSTK"

        if dir_exists(self.RAMSTK_HOME_DIR + "/analyses/ramstk"):
            self.RAMSTK_PROG_DIR = self.RAMSTK_HOME_DIR + "/analyses/ramstk"
        else:
            self.RAMSTK_PROG_DIR = self.RAMSTK_HOME_DIR
