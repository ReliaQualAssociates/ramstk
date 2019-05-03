# -*- coding: utf-8 -*-
#
#       ramstk.Configuration.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Configuration information and methods for RAMSTK."""

import ConfigParser
from os import environ, path, makedirs
import sys

# Add localization support.
import gettext

# Import other RAMSTK modules.
import ramstk.Utilities as Utilities

_ = gettext.gettext

__author__ = 'Doyle Rowland <doyle.rowland@reliaqual.com>'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Doyle "weibullguy" Rowland'

# Define global list constants.
RAMSTK_ACTIVE_ENVIRONMENTS = [[_(u"Ground, Benign")], [_(u"Ground, Fixed")], [
    _(u"Ground, Mobile")
], [_(u"Naval, Sheltered")], [_(u"Naval, Unsheltered")], [
    _(u"Airborne, Inhabited, Cargo")
], [_(u"Airborne, Inhabited, Fighter")], [_(u"Airborne, Uninhabited, Cargo")],
                              [_(u"Airborne, Uninhabited, Fighter")], [
                                  _(u"Airborne, Rotary Wing")
                              ], [_(u"Space, Flight")],
                              [_(u"Missile, Flight")], [_(u"Missile, Launch")]]
RAMSTK_DORMANT_ENVIRONMENTS = [[_(u"Airborne")], [_(u"Ground")], [_(u"Naval")],
                               [_(u"Space")]]

RAMSTK_ALLOCATION_MODELS = [[u'Equal Apportionment'], [u'ARINC Apportionment'],
                            [u'AGREE Apportionment'], [
                                u'Feasibility of Objectives'
                            ], [u'Repairable Systems Apportionment']]

RAMSTK_HR_TYPES = [[_(u"Assessed")], [_(u"Defined, Hazard Rate")],
                   [_(u"Defined, MTBF")], [_(u"Defined, Distribution")]]
RAMSTK_HR_MODELS = [[_(u"MIL-HDBK-217F Parts Count")],
                    [_(u"MIL-HDBK-217F Parts Stress")], [_(u"NSWC-11")]]
RAMSTK_HR_DISTRIBUTIONS = [[_(u"1P Exponential")], [_(u"2P Exponential")],
                           [_(u"Gaussian")], [_(u"Lognormal")],
                           [_(u"2P Weibull")], [_(u"3P Weibull")]]

RAMSTK_CONTROL_TYPES = [_(u"Prevention"), _(u"Detection")]
RAMSTK_COST_TYPES = [[_(u"Defined")], [_(u"Calculated")]]
RAMSTK_MTTR_TYPES = [[_(u"Defined")], [_(u"Calculated")]]

RAMSTK_CRITICALITY = [[
    _(u"Catastrophic"),
    _(u"Could result in death, permanent total disability, loss exceeding "
      u"$1M, or irreversible severe environmental damage that violates law "
      u"or regulation."), "I", 4
], [
    _(u"Critical"),
    _(u"Could result in permanent partial disability, injuries or "
      u"occupational illness that may result in hospitalization of at least "
      u"three personnel, loss exceeding $200K but less than $1M, or "
      u"reversible environmental damage causing a violation of law or "
      u"regulation."), "II", 3
], [
    _(u"Marginal"),
    _(u"Could result in injury or occupational illness resulting in one or "
      u"more lost work days(s), loss exceeding $10K but less than $200K, or "
      u"mitigatible environmental damage without violation of law or "
      u"regulation where restoration activities can be accomplished."), "III",
    2
], [
    _(u"Negligble"),
    _(u"Could result in injury or illness not resulting in a lost work day, "
      u"loss exceeding $2K but less than $10K, or minimal environmental "
      u"damage not violating law or regulation."), "IV", 1
]]
RAMSTK_FAILURE_PROBABILITY = [[_(u"Level E - Extremely Unlikely"),
                               1], [_(u"Level D - Remote"),
                                    2], [_(u"Level C - Occasional"), 3],
                              [_(u"Level B - Reasonably Probable"),
                               4], [_(u"Level A - Frequent"), 5]]

RAMSTK_SW_DEV_ENVIRONMENTS = [[_(u"Organic"), 1.0,
                               0.76], [_(u"Semi-Detached"), 1.0, 1.0],
                              [_(u"Embedded"), 1.0, 1.3]]
RAMSTK_SW_DEV_PHASES = [[_(u"Concept/Planning (PCP)")], [
    _(u"Requirements Analysis (SRA)")
], [_(u"Preliminary Design Review (PDR)")],
                        [_(u"Critical Design Review (CDR)")],
                        [_(u"Test Readiness Review (TRR)")], [_(u"Released")]]
RAMSTK_SW_LEVELS = [[_(u"Software System"), 0], [_(u"Software Module"), 0],
                    [_(u"Software Unit"), 0]]
RAMSTK_SW_APPLICATION = [[_(u"Airborne"), 0.0128,
                          6.28], [_(u"Strategic"), 0.0092,
                                  1.2], [_(u"Tactical"), 0.0078, 13.8],
                         [_(u"Process Control"), 0.0018,
                          3.8], [_(u"Production Center"), 0.0085,
                                 23.0], [_(u"Developmental"), 0.0123, 132.6]]
RAMSTK_SW_TEST_METHODS = [[
    _(u"Code Reviews"),
    _(u"Code review is a systematic examination (often known as peer review) "
      u"of computer source code.")
], [_(u"Error/Anomaly Detection"), _(u"")], [_(u"Structure Analysis"),
                                             _(u"")],
                          [_(u"Random Testing"),
                           _(u"")], [_(u"Functional Testing"),
                                     _(u"")], [_(u"Branch Testing"),
                                               _(u"")]]

RAMSTK_LIFECYCLE = [[_(u"Design")], [_(u"Reliability Growth")],
                    [_(u"Reliability Qualification")], [_(u"Production")],
                    [_(u"Storage")], [_(u"Operation")], [_(u"Disposal")]]
RAMSTK_S_DIST = [["Constant Probability"], ["Exponential"], ["Gaussian"],
                 ["LogNormal"], ["Uniform"], ["Weibull"]]


class Configuration(object):
    r"""
    RAMSTK configuration class.

    Class attributes of the Configuration class are:

    :cvar dict RAMSTK_FORMAT_FILE: Dictionary containing the path to the format
                                files to use for various widgets.  Keys for
                                this dictionary are:

                                * revision
                                * function
                                * requirement
                                * hardware
                                * validation
                                * sia
                                * fmeca
                                * stakeholder
                                * ffmeca

    :cvar dict RAMSTK_COLORS: Dictionary containing the colors to use for various
                           widgets.  Keys for this dictionary are:

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
    :cvar dict RAMSTK_COM_INFO: Dictionary for the RAMSTK common database connection
                             information.  The information contained is:

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
    :cvar dict RAMSTK_PROG_INFO: Dictionary for RAMSTK Program database connection
                              information.  The information contained is:

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
    :cvar dict RAMSTK_TABPOS: Dictionary containing the location of tabs in the
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

    :cvar dict RAMSTK_SEVERITY: Dictionary for failure severity categories.
    :cvar dict RAMSTK_HAZARDS: Dictionary for potential hazards.
    :cvar dict RAMSTK_REQUIREMENT_TYPES: Dictionary of requirement types.
    :cvar dict RAMSTK_RPN_SEVERITY: Dictionary for RPN Severity categories.
    :cvar dict RAMSTK_RPN_OCCURRENCE: Dictionary for RPN Occurrence categories.
    :cvar dict RAMSTK_RPN_DETECTION: Dictionary for RPN Detection categories.

    :cvar list RAMSTK_MODULES: Dictionary of active modules in the open RAMSTK
                            Program database.  Where 1 = active and
                            0 = inactive.  Keys are:

                            * Function
                            * Hardware
                            * Requirements
                            * Revision
                            * Validation

    :cvar list RAMSTK_PAGE_NUMBER: List indicating which page each RAMSTK module
                                occupies in the ModuleBook.
    :cvar list RAMSTK_RISK_POINTS: List for risk level cutoffs.  Cutoffs are:

                                +-------+---------------------------+
                                | Index | Risk Level Cutoff Value   |
                                +=======+===========================+
                                |   0   | Low to medium             |
                                +-------+---------------------------+
                                |   1   | Medium to high            |
                                +-------+---------------------------+

    :cvar float RAMSTK_HR_MULTIPLIER: The failure rate multiplier.  All failure
                                   rates will be multiplied by this value for
                                   display.  This allows failure rates to
                                   display without using scientific notation.
                                   Set to one to use scientific notation.
                                   Default value is *1000000.0*.
    :cvar float RAMSTK_MTIME: The default mission time for new RAMSTK Programs.
    :cvar int RAMSTK_DEC_PLACES: Number of decimal places to show in numerical
                              results.  Default value is *6*.
    :cvar int RAMSTK_MODE_SOURCE: Indicator variable used to determine which
                               failure mode source to use.  Sources are:

                               1. FMD-97
                               2. MIL-STD-338

    :cvar str RAMSTK_CONF_DIR: Path to the directory containing configuration
                            files used by RAMSTK.  Default values are:

                            - POSIX default: *$HOME/.config/RAMSTK*
                            - Windows default: *C:\\\Users\\\<USER NAME>\\\config\\\RAMSTK*

    :cvar str RAMSTK_DATA_DIR: Path to the directory containing data files used by
                            RAMSTK.  Default values are:

                            - POSIX default: */usr/share/RAMSTK*
                            - Windows default: *None*

    :cvar str RAMSTK_ICON_DIR: Path to the directory containing icon files used
                            by RAMSTK.  Default values are:

                            - POSIX default: */usr/share/pixmaps/RAMSTK*
                            - Windows default: *None*

    :cvar str RAMSTK_LOG_DIR: Path to the directory containing log files used by
                           RAMSTK.  Default values are:

                           - POSIX default: *$HOME/.config/RAMSTK/logs*
                           - Windows default: *C:\\\Users\\\<USER NAME>\\\config\\\RAMSTK\\\logs*

    :cvar str RAMSTK_PROG_DIR: Path to the base directory containing RAMSTK Program
                            database files.  This is only used when the
                            backend is SQLite3.  Default values are:

                            - POSIX default: *$HOME/analyses/ramstk*
                            - Windows default: *C:\\\Users\\\<USER NAME>\\\analyses\\\ramstk*

    :cvar str RAMSTK_GUI_LAYOUT: Layout of the GUI to use.  Possible options are:

                              * basic - a single window embedded with the
                                        Module Book, Work Book, and List Book.
                              * advanced - multiple windows; one each for the
                                           Module Book, Work Book, and List
                                           Book.

                              Default value is *basic*.
    :cvar str RAMSTK_COM_BACKEND: RAMSTK common database backend to use.  Options
                               are:

                               * mysql
                               * sqlite

    :cvar str RAMSTK_BACKEND: RAMSTK Program database backend to use.  Options are:

                           * mysql
                           * sqlite

    :cvar str RAMSTK_LOCALE: The language locale to use with RAMSTK.  Default value
                          is *en_US*.
    :cvar str RAMSTK_OS: The operating system RAMSTK is currently running on.
    """

    # Define public dictionary class attributes.
    RAMSTK_FORMAT_FILE = {}
    RAMSTK_COLORS = {}
    RAMSTK_COM_INFO = {}  # RAMSTK Common database info.
    RAMSTK_PROG_INFO = {}  # RAMSTK Program database info.
    RAMSTK_TABPOS = {
        'listbook': 'top',
        'modulebook': 'bottom',
        'workbook': 'bottom'
    }

    # The following global dicts are loaded from information in the RAMSTK
    # Common database.
    RAMSTK_ACTION_CATEGORY = {}
    RAMSTK_ACTION_STATUS = {}
    RAMSTK_AFFINITY_GROUPS = {}  # User updateable
    RAMSTK_CATEGORIES = {}  # Static.
    RAMSTK_DAMAGE_MODELS = {}  # User updateable.
    RAMSTK_DETECTION_METHODS = {}
    RAMSTK_FAILURE_MODES = {}  # User updateable.
    RAMSTK_HAZARDS = {}  # User updateable.
    RAMSTK_INCIDENT_CATEGORY = {}
    RAMSTK_INCIDENT_STATUS = {}
    RAMSTK_INCIDENT_TYPE = {}
    RAMSTK_LOAD_HISTORY = {}  # User updateable.
    RAMSTK_MANUFACTURERS = {}
    RAMSTK_MEASURABLE_PARAMETERS = {}  # User updateable.
    RAMSTK_MEASUREMENT_UNITS = {}
    RAMSTK_MODULES = {}  # Static.
    RAMSTK_PAGE_NUMBER = {}
    RAMSTK_REQUIREMENT_TYPE = {}
    RAMSTK_RPN_DETECTION = {}  # User updateable.
    RAMSTK_RPN_OCCURRENCE = {}  # User updateable.
    RAMSTK_RPN_SEVERITY = {}  # User updateable.
    RAMSTK_SEVERITY = {}
    RAMSTK_STAKEHOLDERS = {}  # User updateable.
    RAMSTK_SUBCATEGORIES = {}  # Static.
    RAMSTK_USERS = {}  # Admin updateable.
    RAMSTK_VALIDATION_TYPE = {}
    RAMSTK_WORKGROUPS = {}  # Admin updateable.

    # Define global list class attributes.
    RAMSTK_RISK_POINTS = [4, 10]

    # Define public scalar class attributes.
    RAMSTK_MODE = ''
    RAMSTK_SITE_CONF = ''
    RAMSTK_PROG_CONF = ''
    RAMSTK_HOME_DIR = ''
    RAMSTK_SITE_DIR = ''
    RAMSTK_ICON_DIR = ''
    RAMSTK_DATA_DIR = ''
    RAMSTK_CONF_DIR = ''
    RAMSTK_LOG_DIR = ''
    RAMSTK_PROG_DIR = ''
    RAMSTK_DEBUG_LOG = ''
    RAMSTK_IMPORT_LOG = ''
    RAMSTK_USER_LOG = ''
    RAMSTK_MODE_SOURCE = 1  # 1=FMD-97
    RAMSTK_COM_BACKEND = ''
    RAMSTK_BACKEND = ''
    RAMSTK_REPORT_SIZE = 'letter'
    RAMSTK_HR_MULTIPLIER = 1000000.0
    RAMSTK_DEC_PLACES = 6
    RAMSTK_MTIME = 100.0
    RAMSTK_GUI_LAYOUT = 'advanced'
    RAMSTK_METHOD = 'STANDARD'  # STANDARD or LRM
    RAMSTK_LOCALE = 'en_US'
    RAMSTK_OS = ''

    def __init__(self):
        """Initialize the RAMSTK configuration parser."""
        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_colors = [
            'revisionfg', 'functionfg', 'requirementfg', 'hardwarefg',
            'validationfg', 'revisionbg', 'functionbg', 'requirementbg',
            'hardwarebg', 'validationbg', 'stakeholderbg', 'stakeholderfg'
        ]
        self._lst_format_files = [
            'allocation', 'dfmeca', 'failure_definition', 'ffmea', 'function',
            'hardware', 'hazops', 'pof', 'requirement', 'revision',
            'similaritem', 'stakeholder', 'validation'
        ]

        # Initialize private scalar attributes.
        self._INSTALL_PREFIX = Utilities.prefix()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        if sys.platform == 'linux2':
            self.RAMSTK_OS = 'Linux'
            self.RAMSTK_SITE_DIR = self._INSTALL_PREFIX + '/share/RAMSTK'
            self.RAMSTK_HOME_DIR = environ['HOME']
            self.RAMSTK_LOG_DIR = '/var/log/RAMSTK'

        elif sys.platform == 'win32':
            self.RAMSTK_OS = 'Windows'
            self.RAMSTK_SITE_DIR = environ['PYTHONPATH'] + '/RAMSTK'
            self.RAMSTK_HOME_DIR = environ['USERPROFILE']
            self.RAMSTK_LOG_DIR = self.RAMSTK_SITE_DIR + '/logs'

        self.RAMSTK_DATA_DIR = self.RAMSTK_SITE_DIR + '/layouts'
        self.RAMSTK_ICON_DIR = self.RAMSTK_SITE_DIR + '/icons'
        self.RAMSTK_PROG_DIR = self.RAMSTK_HOME_DIR + '/analyses/ramstk/'
        self.RAMSTK_CONF_DIR = self.RAMSTK_SITE_DIR

    def get_site_configuration(self):
        """
        Read the site configuration file.

        :return: False of successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Try to read the user's configuration file.  If it doesn't exist,
        # create a new one.  If those options fail, read the system-wide
        # configuration file and keep going.
        if Utilities.file_exists(self.RAMSTK_SITE_CONF):
            _config = ConfigParser.ConfigParser()
            _config.read(self.RAMSTK_SITE_CONF)

            self.RAMSTK_COM_BACKEND = _config.get('Backend', 'type')
            self.RAMSTK_COM_INFO['host'] = _config.get('Backend', 'host')
            self.RAMSTK_COM_INFO['socket'] = _config.get('Backend', 'socket')
            self.RAMSTK_COM_INFO['database'] = _config.get(
                'Backend', 'database')
            self.RAMSTK_COM_INFO['user'] = _config.get('Backend', 'user')
            self.RAMSTK_COM_INFO['password'] = _config.get(
                'Backend', 'password')
            self.RAMSTK_COM_INFO['path'] = _config.get('Backend', 'password')

        return _return

    def _set_site_configuration(self):
        """
        Create the default site configuration file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _common_db = self.RAMSTK_SITE_DIR + '/ramstk_common.rtk'

        _config = ConfigParser.ConfigParser()

        _config.add_section('Backend')
        _config.set('Backend', 'host', 'localhost')
        _config.set('Backend', 'socket', 3306)
        _config.set('Backend', 'database', _common_db)
        _config.set('Backend', 'user', 'ramstk')
        _config.set('Backend', 'password', 'ramstk')
        _config.set('Backend', 'type', 'sqlite')
        _config.set('Backend', 'path', self.RAMSTK_SITE_DIR)

        try:
            _parser = open(self.RAMSTK_SITE_CONF, 'w')
            _config.write(_parser)
            _parser.close()
        except EnvironmentError:
            _return = True

        return _return

    def create_user_configuration(self):
        """
        Create the default user configuration file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        import glob
        from distutils import dir_util, file_util  # pylint: disable=no-name-in-module

        _return = False

        _config = ConfigParser.ConfigParser()

        # Create the directories needed for the user.  Always prefer the RAMSTK
        # directories in the user's $HOME over the system-wide directories.
        # Configuration directory.
        self.RAMSTK_CONF_DIR = self.RAMSTK_HOME_DIR + '/.config/RAMSTK'
        try:
            makedirs(self.RAMSTK_CONF_DIR)
            self.RAMSTK_PROG_CONF = self.RAMSTK_CONF_DIR + '/RAMSTK.conf'
        except OSError:
            pass

        # Data directory.
        self.RAMSTK_DATA_DIR = self.RAMSTK_CONF_DIR + '/layouts'
        if not Utilities.dir_exists(self.RAMSTK_DATA_DIR):
            try:
                makedirs(self.RAMSTK_DATA_DIR)
            except OSError:
                pass

        # Icon directory.
        self.RAMSTK_ICON_DIR = self.RAMSTK_CONF_DIR + '/icons'
        if not Utilities.dir_exists(self.RAMSTK_ICON_DIR):
            try:
                makedirs(self.RAMSTK_ICON_DIR)
            except OSError:
                pass

        # Log directory.
        self.RAMSTK_LOG_DIR = self.RAMSTK_CONF_DIR + '/logs'
        if not Utilities.dir_exists(self.RAMSTK_LOG_DIR):
            try:
                makedirs(self.RAMSTK_LOG_DIR)
            except OSError:
                pass

        # Program directory.
        if not Utilities.dir_exists(self.RAMSTK_PROG_DIR):
            try:
                makedirs(self.RAMSTK_PROG_DIR)
            except OSError:
                pass

        # Copy format files from RAMSTK_SITE_DIR (system) to the user's
        # RAMSTK_CONF_DIR.
        for _file in glob.glob(self.RAMSTK_SITE_DIR + '/layouts/*.xml'):
            file_util.copy_file(_file, self.RAMSTK_DATA_DIR)

        # Copy the icons from RAMSTK_SITE_DIR (system) to the user's
        # RAMSTK_ICON_DIR.
        try:
            dir_util.copy_tree(self.RAMSTK_SITE_DIR + '/icons/',
                               self.RAMSTK_ICON_DIR)
        except IOError:
            _return = True

        # Create the default RAMSTK user configuration file.
        _config.add_section('General')
        _config.set('General', 'firstrun', True)
        _config.set('General', 'reportsize', 'letter')
        _config.set('General', 'frmultiplier', 1000000.0)
        _config.set('General', 'calcreltime', 100.0)
        _config.set('General', 'autoaddlistitems', 'False')
        _config.set('General', 'decimal', 6)
        _config.set('General', 'modesource', 1)
        _config.set('General', 'parallelcalcs', 'False')
        _config.set('General', 'moduletabpos', 'top')
        _config.set('General', 'listtabpos', 'bottom')
        _config.set('General', 'worktabpos', 'bottom')

        _config.add_section('Backend')
        _config.set('Backend', 'type', 'sqlite')
        _config.set('Backend', 'host', 'localhost')
        _config.set('Backend', 'socket', 3306)
        _config.set('Backend', 'database', '')
        _config.set('Backend', 'user', '')
        _config.set('Backend', 'password', '')

        _config.add_section('Directories')
        _config.set('Directories', 'datadir', self.RAMSTK_DATA_DIR)
        _config.set('Directories', 'icondir', self.RAMSTK_ICON_DIR)
        _config.set('Directories', 'logdir', self.RAMSTK_LOG_DIR)
        _config.set('Directories', 'progdir', self.RAMSTK_PROG_DIR)

        _config.add_section('Files')
        _config.set('Files', 'allocation', 'Allocation.xml')
        _config.set('Files', 'dfmeca', 'DFMECA.xml')
        _config.set('Files', 'failure_definition', 'FailureDefinition.xml')
        _config.set('Files', 'ffmea', 'FFMEA.xml')
        _config.set('Files', 'function', 'Function.xml')
        _config.set('Files', 'hardware', 'Hardware.xml')
        _config.set('Files', 'hazops', 'HazOps.xml')
        _config.set('Files', 'pof', 'PoF.xml')
        _config.set('Files', 'requirement', 'Requirement.xml')
        _config.set('Files', 'revision', 'Revision.xml')
        _config.set('Files', 'similaritem', 'SimilarItem.xml')
        _config.set('Files', 'stakeholder', 'Stakeholder.xml')
        _config.set('Files', 'validation', 'Validation.xml')

        _config.add_section('Colors')
        _config.set('Colors', 'functionbg', '#FFFFFF')
        _config.set('Colors', 'functionfg', '#000000')
        _config.set('Colors', 'hardwarebg', '#FFFFFF')
        _config.set('Colors', 'hardwarefg', '#000000')
        _config.set('Colors', 'requirementbg', '#FFFFFF')
        _config.set('Colors', 'requirementfg', '#000000')
        _config.set('Colors', 'revisionbg', '#FFFFFF')
        _config.set('Colors', 'revisionfg', '#000000')
        _config.set('Colors', 'stakeholderbg', '#FFFFFF')
        _config.set('Colors', 'stakeholderfg', '#000000')
        _config.set('Colors', 'validationbg', '#FFFFFF')
        _config.set('Colors', 'validationfg', '#000000')

        try:
            _parser = open(self.RAMSTK_PROG_CONF, 'w')
            _config.write(_parser)
            _parser.close()
        except EnvironmentError:
            _return = True

        self._set_site_configuration()

        return _return

    def get_user_configuration(self):
        """
        Read the RAMSTK configuration file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Try to read the user's configuration file.  If it doesn't exist,
        # create a new one.  If those options fail, read the system-wide
        # configuration file and keep going.
        if Utilities.file_exists(self.RAMSTK_PROG_CONF):
            _config = ConfigParser.ConfigParser()
            _config.read(self.RAMSTK_PROG_CONF)

            for _color in self._lst_colors:
                self.RAMSTK_COLORS[_color] = _config.get('Colors', _color)

            for _file in self._lst_format_files:
                self.RAMSTK_FORMAT_FILE[_file] = _config.get('Files', _file)

            self.RAMSTK_BACKEND = _config.get('Backend', 'type')
            self.RAMSTK_PROG_INFO['host'] = _config.get('Backend', 'host')
            self.RAMSTK_PROG_INFO['socket'] = _config.get('Backend', 'socket')
            self.RAMSTK_PROG_INFO['database'] = _config.get(
                'Backend', 'database')
            self.RAMSTK_PROG_INFO['user'] = _config.get('Backend', 'user')
            self.RAMSTK_PROG_INFO['password'] = _config.get(
                'Backend', 'password')

            self.RAMSTK_DATA_DIR = _config.get('Directories', 'datadir')
            self.RAMSTK_ICON_DIR = _config.get('Directories', 'icondir')
            self.RAMSTK_LOG_DIR = _config.get('Directories', 'logdir')
            self.RAMSTK_PROG_DIR = _config.get('Directories', 'progdir')

            self.RAMSTK_REPORT_SIZE = _config.get('General', 'reportsize')
            self.RAMSTK_HR_MULTIPLIER = _config.get('General', 'frmultiplier')
            self.RAMSTK_DEC_PLACES = _config.get('General', 'decimal')
            self.RAMSTK_MTIME = _config.get('General', 'calcreltime')
            self.RAMSTK_MODE_SOURCE = _config.get('General', 'modesource')
            self.RAMSTK_TABPOS['listbook'] = _config.get(
                'General', 'listtabpos')
            self.RAMSTK_TABPOS['modulebook'] = _config.get(
                'General', 'moduletabpos')
            self.RAMSTK_TABPOS['workbook'] = _config.get(
                'General', 'worktabpos')
        else:
            _return = True

        return _return

    def set_site_variables(self):
        """
        Set the site configuration variables.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Prefer user-specific directories in their $HOME directory over the
        # system-wide directories.
        if Utilities.dir_exists(self.RAMSTK_HOME_DIR + '/.config/RAMSTK'):
            self.RAMSTK_CONF_DIR = self.RAMSTK_HOME_DIR + '/.config/RAMSTK'
        else:
            self.RAMSTK_CONF_DIR = self.RAMSTK_SITE_DIR

        if Utilities.dir_exists(self.RAMSTK_HOME_DIR + '/.config/RAMSTK/data'):
            self.RAMSTK_DATA_DIR = self.RAMSTK_HOME_DIR + \
            '/.config/RAMSTK/data'

        if Utilities.dir_exists(self.RAMSTK_HOME_DIR +
                                '/.config/RAMSTK/icons'):
            self.RAMSTK_ICON_DIR = self.RAMSTK_HOME_DIR + \
            '/.config/RAMSTK/icons'

        if Utilities.dir_exists(self.RAMSTK_HOME_DIR + '/.config/RAMSTK/logs'):
            self.RAMSTK_LOG_DIR = self.RAMSTK_HOME_DIR + '/.config/RAMSTK/logs'

        self.RAMSTK_SITE_CONF = self.RAMSTK_CONF_DIR + '/Site.conf'

        if not Utilities.file_exists(self.RAMSTK_SITE_CONF):
            self._set_site_configuration()

        self.get_site_configuration()

        return False

    def set_user_configuration(self):
        """
        Write changes to the user's configuration file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if Utilities.file_exists(self.RAMSTK_PROG_CONF):
            _config = ConfigParser.ConfigParser()
            _config.add_section('General')
            _config.set('General', 'reportsize', self.RAMSTK_REPORT_SIZE)
            _config.set('General', 'parallelcalcs', 'False')
            _config.set('General', 'frmultiplier', self.RAMSTK_HR_MULTIPLIER)
            _config.set('General', 'calcreltime', self.RAMSTK_MTIME)
            _config.set('General', 'autoaddlistitems', 'False')
            _config.set('General', 'decimal', self.RAMSTK_DEC_PLACES)
            _config.set('General', 'modesource', self.RAMSTK_MODE_SOURCE)
            _config.set('General', 'moduletabpos',
                        self.RAMSTK_TABPOS['modulebook'])
            _config.set('General', 'listtabpos',
                        self.RAMSTK_TABPOS['listbook'])
            _config.set('General', 'worktabpos',
                        self.RAMSTK_TABPOS['workbook'])

            _config.add_section('Backend')
            _config.set('Backend', 'type', self.RAMSTK_BACKEND)
            _config.set('Backend', 'host', self.RAMSTK_PROG_INFO['host'])
            _config.set('Backend', 'socket',
                        int(self.RAMSTK_PROG_INFO['socket']))
            _config.set('Backend', 'database',
                        self.RAMSTK_PROG_INFO['database'])
            _config.set('Backend', 'user', self.RAMSTK_PROG_INFO['user'])
            _config.set('Backend', 'password',
                        self.RAMSTK_PROG_INFO['password'])

            _config.add_section('Directories')
            _config.set('Directories', 'datadir', self.RAMSTK_DATA_DIR)
            _config.set('Directories', 'icondir', self.RAMSTK_ICON_DIR)
            _config.set('Directories', 'logdir', self.RAMSTK_LOG_DIR)
            _config.set('Directories', 'progdir', self.RAMSTK_PROG_DIR)

            _config.add_section('Files')
            for _file in self._lst_format_files:
                _config.set('Files', _file,
                            path.basename(self.RAMSTK_FORMAT_FILE[_file]))

            _config.add_section('Colors')
            for _color in self._lst_colors:
                _config.set('Colors', _color, self.RAMSTK_COLORS[_color])

            try:
                _parser = open(self.RAMSTK_PROG_CONF, 'w')
                _config.write(_parser)
                _parser.close()
            except EnvironmentError:
                _return = True

        return _return

    def set_user_variables(self, first_run=True):
        """
        Set the user-specific configuration variables.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Prefer user-specific directories in their $HOME directory over the
        # system-wide directories.
        if Utilities.dir_exists(self.RAMSTK_HOME_DIR + '/.config/RAMSTK'):
            self.RAMSTK_CONF_DIR = self.RAMSTK_HOME_DIR + '/.config/RAMSTK'
        else:
            self.RAMSTK_CONF_DIR = self.RAMSTK_SITE_DIR
            _return = first_run

        self.RAMSTK_PROG_CONF = self.RAMSTK_CONF_DIR + '/RAMSTK.conf'

        return _return
