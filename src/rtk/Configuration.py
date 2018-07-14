# -*- coding: utf-8 -*-
#
#       rtk.Configuration.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Configuration information and methods for RTK."""

import ConfigParser
from os import environ, path, makedirs
import sys

# Add localization support.
import gettext

# Import other RTK modules.
import rtk.Utilities as Utilities

_ = gettext.gettext

__author__ = 'Andrew Rowland <andrew.rowland@reliaqual.com>'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

# Define global list constants.
RTK_ACTIVE_ENVIRONMENTS = [[_(u"Ground, Benign")], [_(u"Ground, Fixed")], [
    _(u"Ground, Mobile")
], [_(u"Naval, Sheltered")], [_(u"Naval, Unsheltered")], [
    _(u"Airborne, Inhabited, Cargo")
], [_(u"Airborne, Inhabited, Fighter")], [_(u"Airborne, Uninhabited, Cargo")],
                           [_(u"Airborne, Uninhabited, Fighter")], [
                               _(u"Airborne, Rotary Wing")
                           ], [_(u"Space, Flight")], [_(u"Missile, Flight")],
                           [_(u"Missile, Launch")]]
RTK_DORMANT_ENVIRONMENTS = [[_(u"Airborne")], [_(u"Ground")], [_(u"Naval")],
                            [_(u"Space")]]

RTK_ALLOCATION_MODELS = [[u'Equal Apportionment'], [u'ARINC Apportionment'], [
    u'AGREE Apportionment'
], [u'Feasibility of Objectives'], [u'Repairable Systems Apportionment']]

RTK_HR_TYPES = [[_(u"Assessed")], [_(u"Defined, Hazard Rate")],
                [_(u"Defined, MTBF")], [_(u"Defined, Distribution")]]
RTK_HR_MODELS = [[_(u"MIL-HDBK-217F Parts Count")],
                 [_(u"MIL-HDBK-217F Parts Stress")], [_(u"NSWC-11")]]
RTK_HR_DISTRIBUTIONS = [[_(u"1P Exponential")], [_(u"2P Exponential")],
                        [_(u"Gaussian")], [_(u"Lognormal")],
                        [_(u"2P Weibull")], [_(u"3P Weibull")]]

RTK_CONTROL_TYPES = [_(u"Prevention"), _(u"Detection")]
RTK_COST_TYPES = [[_(u"Defined")], [_(u"Calculated")]]
RTK_MTTR_TYPES = [[_(u"Defined")], [_(u"Calculated")]]

RTK_CRITICALITY = [[
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
RTK_FAILURE_PROBABILITY = [[_(u"Level E - Extremely Unlikely"),
                            1], [_(u"Level D - Remote"),
                                 2], [_(u"Level C - Occasional"), 3],
                           [_(u"Level B - Reasonably Probable"),
                            4], [_(u"Level A - Frequent"), 5]]

RTK_SW_DEV_ENVIRONMENTS = [[_(u"Organic"), 1.0,
                            0.76], [_(u"Semi-Detached"), 1.0, 1.0],
                           [_(u"Embedded"), 1.0, 1.3]]
RTK_SW_DEV_PHASES = [[_(u"Concept/Planning (PCP)")], [
    _(u"Requirements Analysis (SRA)")
], [_(u"Preliminary Design Review (PDR)")],
                     [_(u"Critical Design Review (CDR)")],
                     [_(u"Test Readiness Review (TRR)")], [_(u"Released")]]
RTK_SW_LEVELS = [[_(u"Software System"), 0], [_(u"Software Module"), 0],
                 [_(u"Software Unit"), 0]]
RTK_SW_APPLICATION = [[_(u"Airborne"), 0.0128,
                       6.28], [_(u"Strategic"), 0.0092,
                               1.2], [_(u"Tactical"), 0.0078, 13.8],
                      [_(u"Process Control"), 0.0018,
                       3.8], [_(u"Production Center"), 0.0085,
                              23.0], [_(u"Developmental"), 0.0123, 132.6]]
RTK_SW_TEST_METHODS = [[
    _(u"Code Reviews"),
    _(u"Code review is a systematic examination (often known as peer review) "
      u"of computer source code.")
], [_(u"Error/Anomaly Detection"), _(u"")], [_(u"Structure Analysis"),
                                             _(u"")],
                       [_(u"Random Testing"),
                        _(u"")], [_(u"Functional Testing"),
                                  _(u"")], [_(u"Branch Testing"),
                                            _(u"")]]

RTK_LIFECYCLE = [[_(u"Design")], [_(u"Reliability Growth")],
                 [_(u"Reliability Qualification")], [_(u"Production")],
                 [_(u"Storage")], [_(u"Operation")], [_(u"Disposal")]]
RTK_S_DIST = [["Constant Probability"], ["Exponential"], ["Gaussian"],
              ["LogNormal"], ["Uniform"], ["Weibull"]]


class Configuration(object):
    r"""
    RTK configuration class.

    Class attributes of the Configuration class are:

    :cvar dict RTK_FORMAT_FILE: Dictionary containing the path to the format
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

    :cvar dict RTK_COLORS: Dictionary containing the colors to use for various
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
    :cvar dict RTK_COM_INFO: Dictionary for the RTK common database connection
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
    :cvar dict RTK_PROG_INFO: Dictionary for RTK Program database connection
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
    :cvar dict RTK_TABPOS: Dictionary containing the location of tabs in the
                           three main gtk.Notebook() widgets.  Can be one of:

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

    :cvar dict RTK_SEVERITY: Dictionary for failure severity categories.
    :cvar dict RTK_HAZARDS: Dictionary for potential hazards.
    :cvar dict RTK_REQUIREMENT_TYPES: Dictionary of requirement types.
    :cvar dict RTK_RPN_SEVERITY: Dictionary for RPN Severity categories.
    :cvar dict RTK_RPN_OCCURRENCE: Dictionary for RPN Occurrence categories.
    :cvar dict RTK_RPN_DETECTION: Dictionary for RPN Detection categories.

    :cvar list RTK_MODULES: Dictionary of active modules in the open RTK
                            Program database.  Where 1 = active and
                            0 = inactive.  Keys are:

                            * Function
                            * Hardware
                            * Requirements
                            * Revision
                            * Validation

    :cvar list RTK_PAGE_NUMBER: List indicating which page each RTK module
                                occupies in the ModuleBook.
    :cvar list RTK_RISK_POINTS: List for risk level cutoffs.  Cutoffs are:

                                +-------+---------------------------+
                                | Index | Risk Level Cutoff Value   |
                                +=======+===========================+
                                |   0   | Low to medium             |
                                +-------+---------------------------+
                                |   1   | Medium to high            |
                                +-------+---------------------------+

    :cvar float RTK_HR_MULTIPLIER: The failure rate multiplier.  All failure
                                   rates will be multiplied by this value for
                                   display.  This allows failure rates to
                                   display without using scientific notation.
                                   Set to one to use scientific notation.
                                   Default value is *1000000.0*.
    :cvar float RTK_MTIME: The default mission time for new RTK Programs.
    :cvar int RTK_DEC_PLACES: Number of decimal places to show in numerical
                              results.  Default value is *6*.
    :cvar int RTK_MODE_SOURCE: Indicator variable used to determine which
                               failure mode source to use.  Sources are:

                               1. FMD-97
                               2. MIL-STD-338

    :cvar str RTK_CONF_DIR: Path to the directory containing configuration
                            files used by RTK.  Default values are:

                            - POSIX default: *$HOME/.config/RTK*
                            - Windows default: *C:\\\Users\\\<USER NAME>\\\config\\\RTK*

    :cvar str RTK_DATA_DIR: Path to the directory containing data files used by
                            RTK.  Default values are:

                            - POSIX default: */usr/share/RTK*
                            - Windows default: *None*

    :cvar str RTK_ICON_DIR: Path to the directory containing icon files used
                            by RTK.  Default values are:

                            - POSIX default: */usr/share/pixmaps/RTK*
                            - Windows default: *None*

    :cvar str RTK_LOG_DIR: Path to the directory containing log files used by
                           RTK.  Default values are:

                           - POSIX default: *$HOME/.config/RTK/logs*
                           - Windows default: *C:\\\Users\\\<USER NAME>\\\config\\\RTK\\\logs*

    :cvar str RTK_PROG_DIR: Path to the base directory containing RTK Program
                            database files.  This is only used when the
                            backend is SQLite3.  Default values are:

                            - POSIX default: *$HOME/analyses/rtk*
                            - Windows default: *C:\\\Users\\\<USER NAME>\\\analyses\\\rtk*

    :cvar str RTK_GUI_LAYOUT: Layout of the GUI to use.  Possible options are:

                              * basic - a single window embedded with the
                                        Module Book, Work Book, and List Book.
                              * advanced - multiple windows; one each for the
                                           Module Book, Work Book, and List
                                           Book.

                              Default value is *basic*.
    :cvar str RTK_COM_BACKEND: RTK common database backend to use.  Options
                               are:

                               * mysql
                               * sqlite

    :cvar str RTK_BACKEND: RTK Program database backend to use.  Options are:

                           * mysql
                           * sqlite

    :cvar str RTK_LOCALE: The language locale to use with RTK.  Default value
                          is *en_US*.
    :cvar str RTK_OS: The operating system RTK is currently running on.
    """

    # Define public dictionary class attributes.
    RTK_FORMAT_FILE = {}
    RTK_COLORS = {}
    RTK_COM_INFO = {}  # RTK Common database info.
    RTK_PROG_INFO = {}  # RTK Program database info.
    RTK_TABPOS = {
        'listbook': 'top',
        'modulebook': 'bottom',
        'workbook': 'bottom'
    }

    # The following global dicts are loaded from information in the RTK
    # Common database.
    RTK_ACTION_CATEGORY = {}
    RTK_ACTION_STATUS = {}
    RTK_AFFINITY_GROUPS = {}  # User updateable
    RTK_CATEGORIES = {}  # Static.
    RTK_DAMAGE_MODELS = {}  # User updateable.
    RTK_DETECTION_METHODS = {}
    RTK_FAILURE_MODES = {}  # User updateable.
    RTK_HAZARDS = {}  # User updateable.
    RTK_INCIDENT_CATEGORY = {}
    RTK_INCIDENT_STATUS = {}
    RTK_INCIDENT_TYPE = {}
    RTK_LOAD_HISTORY = {}  # User updateable.
    RTK_MANUFACTURERS = {}
    RTK_MEASURABLE_PARAMETERS = {}  # User updateable.
    RTK_MEASUREMENT_UNITS = {}
    RTK_MODULES = {}  # Static.
    RTK_PAGE_NUMBER = {}
    RTK_REQUIREMENT_TYPE = {}
    RTK_RPN_DETECTION = {}  # User updateable.
    RTK_RPN_OCCURRENCE = {}  # User updateable.
    RTK_RPN_SEVERITY = {}  # User updateable.
    RTK_SEVERITY = {}
    RTK_STAKEHOLDERS = {}  # User updateable.
    RTK_SUBCATEGORIES = {}  # Static.
    RTK_USERS = {}  # Admin updateable.
    RTK_VALIDATION_TYPE = {}
    RTK_WORKGROUPS = {}  # Admin updateable.

    # Define global list class attributes.
    RTK_RISK_POINTS = [4, 10]

    # Define public scalare class attributes.
    RTK_MODE = ''
    RTK_SITE_CONF = ''
    RTK_PROG_CONF = ''
    RTK_HOME_DIR = ''
    RTK_SITE_DIR = ''
    RTK_ICON_DIR = ''
    RTK_DATA_DIR = ''
    RTK_CONF_DIR = ''
    RTK_LOG_DIR = ''
    RTK_PROG_DIR = ''
    RTK_DEBUG_LOG = ''
    RTK_IMPORT_LOG = ''
    RTK_USER_LOG = ''
    RTK_MODE_SOURCE = 1  # 1=FMD-97
    RTK_COM_BACKEND = ''
    RTK_BACKEND = ''
    RTK_HR_MULTIPLIER = 1000000.0
    RTK_DEC_PLACES = 6
    RTK_MTIME = 100.0
    RTK_GUI_LAYOUT = 'advanced'
    RTK_METHOD = 'STANDARD'  # STANDARD or LRM
    RTK_LOCALE = 'en_US'
    RTK_OS = ''

    def __init__(self):
        """Initialize the RTK configuration parser."""
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
            self.RTK_OS = 'Linux'
            self.RTK_SITE_DIR = self._INSTALL_PREFIX + '/share/RTK'
            self.RTK_HOME_DIR = environ['HOME']
            self.RTK_LOG_DIR = '/var/log/RTK'

        elif sys.platform == 'win32':
            self.RTK_OS = 'Windows'
            self.RTK_SITE_DIR = environ['COMMONPROGRAMFILES(X86)'] + '/RTK'
            self.RTK_HOME_DIR = environ['USERPROFILE']
            self.RTK_LOG_DIR = self.RTK_SITE_DIR + '/logs'

        self.RTK_DATA_DIR = self.RTK_SITE_DIR + '/layouts'
        self.RTK_ICON_DIR = self.RTK_SITE_DIR + '/icons'
        self.RTK_PROG_DIR = self.RTK_HOME_DIR + '/analyses/rtk/'
        self.RTK_CONF_DIR = self.RTK_SITE_DIR

    def _get_site_configuration(self):
        """
        Read the site configuration file.

        :return: False of successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Try to read the user's configuration file.  If it doesn't exist,
        # create a new one.  If those options fail, read the system-wide
        # configuration file and keep going.
        if Utilities.file_exists(self.RTK_SITE_CONF):
            _config = ConfigParser.ConfigParser()
            _config.read(self.RTK_SITE_CONF)

            self.RTK_COM_BACKEND = _config.get('Backend', 'type')
            self.RTK_COM_INFO['host'] = _config.get('Backend', 'host')
            self.RTK_COM_INFO['socket'] = _config.get('Backend', 'socket')
            self.RTK_COM_INFO['database'] = _config.get('Backend', 'database')
            self.RTK_COM_INFO['user'] = _config.get('Backend', 'user')
            self.RTK_COM_INFO['password'] = _config.get('Backend', 'password')

        return _return

    def _set_site_configuration(self):
        """
        Create the default site configuration file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _config = ConfigParser.ConfigParser()

        _config.add_section('Modules')
        _config.set('Modules', 'function', 'True')
        _config.set('Modules', 'hardware', 'True')
        _config.set('Modules', 'requirement', 'True')
        _config.set('Modules', 'revision', 'True')
        _config.set('Modules', 'validation', 'True')

        _config.add_section('Backend')
        _config.set('Backend', 'host', 'localhost')
        _config.set('Backend', 'socket', 3306)
        _config.set('Backend', 'database', '')
        _config.set('Backend', 'user', 'user')
        _config.set('Backend', 'password', 'password')
        _config.set('Backend', 'type', 'sqlite')
        _config.set('Backend', 'path', self.RTK_SITE_DIR)

        try:
            _parser = open(self.RTK_SITE_CONF, 'w')
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

        # Create the directories needed for the user.  Always prefer the RTK
        # directories in the user's $HOME over the system-wide directories.
        # Configuration directory.
        self.RTK_CONF_DIR = self.RTK_HOME_DIR + '/.config/RTK2'
        try:
            makedirs(self.RTK_CONF_DIR)
            self.RTK_PROG_CONF = self.RTK_CONF_DIR + '/RTK.conf'
        except OSError:
            pass

        # Data directory.
        self.RTK_DATA_DIR = self.RTK_CONF_DIR + '/layouts'
        if not Utilities.dir_exists(self.RTK_DATA_DIR):
            try:
                makedirs(self.RTK_DATA_DIR)
            except OSError:
                pass

        # Icon directory.
        self.RTK_ICON_DIR = self.RTK_CONF_DIR + '/icons'
        if not Utilities.dir_exists(self.RTK_ICON_DIR):
            try:
                makedirs(self.RTK_ICON_DIR)
            except OSError:
                pass

        # Log directory.
        self.RTK_LOG_DIR = self.RTK_CONF_DIR + '/logs'
        if not Utilities.dir_exists(self.RTK_LOG_DIR):
            try:
                makedirs(self.RTK_LOG_DIR)
            except OSError:
                pass

        # Program directory.
        if not Utilities.dir_exists(self.RTK_PROG_DIR):
            try:
                makedirs(self.RTK_PROG_DIR)
            except OSError:
                pass

        # Copy format files from RTK_SITE_DIR (system) to the user's
        # RTK_CONF_DIR.
        for _file in glob.glob(self.RTK_SITE_DIR + '/layouts/*.xml'):
            file_util.copy_file(_file, self.RTK_DATA_DIR)

        # Copy the icons from RTK_SITE_DIR (system) to the user's RTK_ICON_DIR.
        try:
            dir_util.copy_tree(self.RTK_SITE_DIR + '/icons/',
                               self.RTK_ICON_DIR)
        except IOError:
            _return = True

        # Create the default RTK user configuration file.
        _config.add_section('General')
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
        _config.set('Directories', 'datadir', self.RTK_DATA_DIR)
        _config.set('Directories', 'icondir', self.RTK_ICON_DIR)
        _config.set('Directories', 'logdir', self.RTK_LOG_DIR)
        _config.set('Directories', 'progdir', self.RTK_PROG_DIR)

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
            _parser = open(self.RTK_PROG_CONF, 'w')
            _config.write(_parser)
            _parser.close()
        except EnvironmentError:
            _return = True

        return _return

    def get_user_configuration(self):
        """
        Read the RTK configuration file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Try to read the user's configuration file.  If it doesn't exist,
        # create a new one.  If those options fail, read the system-wide
        # configuration file and keep going.
        if Utilities.file_exists(self.RTK_PROG_CONF):
            _config = ConfigParser.ConfigParser()
            _config.read(self.RTK_PROG_CONF)

            for _color in self._lst_colors:
                self.RTK_COLORS[_color] = _config.get('Colors', _color)

            for _file in self._lst_format_files:
                self.RTK_FORMAT_FILE[_file] = _config.get('Files', _file)

            self.RTK_BACKEND = _config.get('Backend', 'type')
            self.RTK_PROG_INFO['host'] = _config.get('Backend', 'host')
            self.RTK_PROG_INFO['socket'] = _config.get('Backend', 'socket')
            self.RTK_PROG_INFO['database'] = _config.get('Backend', 'database')
            self.RTK_PROG_INFO['user'] = _config.get('Backend', 'user')
            self.RTK_PROG_INFO['password'] = _config.get('Backend', 'password')

            self.RTK_DATA_DIR = _config.get('Directories', 'datadir')
            self.RTK_ICON_DIR = _config.get('Directories', 'icondir')
            self.RTK_LOG_DIR = _config.get('Directories', 'logdir')
            self.RTK_PROG_DIR = _config.get('Directories', 'progdir')

            self.RTK_HR_MULTIPLIER = _config.get('General', 'frmultiplier')
            self.RTK_DEC_PLACES = _config.get('General', 'decimal')
            self.RTK_MTIME = _config.get('General', 'calcreltime')
            self.RTK_MODE_SOURCE = _config.get('General', 'modesource')
            self.RTK_TABPOS['listbook'] = _config.get('General', 'listtabpos')
            self.RTK_TABPOS['modulebook'] = _config.get(
                'General', 'moduletabpos')
            self.RTK_TABPOS['workbook'] = _config.get('General', 'worktabpos')
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
        if Utilities.dir_exists(self.RTK_HOME_DIR + '/.config/RTK'):
            self.RTK_CONF_DIR = self.RTK_HOME_DIR + '/.config/RTK'
        else:
            self.RTK_CONF_DIR = self.RTK_SITE_DIR

        if Utilities.dir_exists(self.RTK_HOME_DIR + '/.config/RTK/data'):
            self.RTK_DATA_DIR = self.RTK_HOME_DIR + '/.config/RTK/data'

        if Utilities.dir_exists(self.RTK_HOME_DIR + '/.config/RTK/icons'):
            self.RTK_ICON_DIR = self.RTK_HOME_DIR + '/.config/RTK/icons'

        if Utilities.dir_exists(self.RTK_HOME_DIR + '/.config/RTK/logs'):
            self.RTK_LOG_DIR = self.RTK_HOME_DIR + '/.config/RTK/logs'

        self.RTK_SITE_CONF = self.RTK_CONF_DIR + '/Site.conf'

        if not Utilities.file_exists(self.RTK_SITE_CONF):
            self._set_site_configuration()

        self._get_site_configuration()

        return False

    def set_user_configuration(self):
        """
        Write changes to the user's configuration file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if Utilities.file_exists(self.RTK_PROG_CONF):
            _config = ConfigParser.ConfigParser()
            _config.add_section('General')
            _config.set('General', 'reportsize', 'letter')
            _config.set('General', 'parallelcalcs', 'False')
            _config.set('General', 'frmultiplier', self.RTK_HR_MULTIPLIER)
            _config.set('General', 'calcreltime', self.RTK_MTIME)
            _config.set('General', 'autoaddlistitems', 'False')
            _config.set('General', 'decimal', self.RTK_DEC_PLACES)
            _config.set('General', 'modesource', self.RTK_MODE_SOURCE)
            _config.set('General', 'moduletabpos',
                        self.RTK_TABPOS['modulebook'])
            _config.set('General', 'listtabpos', self.RTK_TABPOS['listbook'])
            _config.set('General', 'worktabpos', self.RTK_TABPOS['workbook'])

            _config.add_section('Backend')
            _config.set('Backend', 'type', self.RTK_BACKEND)
            _config.set('Backend', 'host', self.RTK_PROG_INFO['host'])
            _config.set('Backend', 'socket', int(self.RTK_PROG_INFO['socket']))
            _config.set('Backend', 'database', self.RTK_PROG_INFO['database'])
            _config.set('Backend', 'user', self.RTK_PROG_INFO['user'])
            _config.set('Backend', 'password', self.RTK_PROG_INFO['password'])

            _config.add_section('Directories')
            _config.set('Directories', 'datadir', self.RTK_DATA_DIR)
            _config.set('Directories', 'icondir', self.RTK_ICON_DIR)
            _config.set('Directories', 'logdir', self.RTK_LOG_DIR)
            _config.set('Directories', 'progdir', self.RTK_PROG_DIR)

            _config.add_section('Files')
            for _file in self._lst_format_files:
                _config.set('Files', _file,
                            path.basename(self.RTK_FORMAT_FILE[_file]))

            _config.add_section('Colors')
            for _color in self._lst_colors:
                _config.set('Colors', _color, self.RTK_COLORS[_color])

            try:
                _parser = open(self.RTK_PROG_CONF, 'w')
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
        if Utilities.dir_exists(self.RTK_HOME_DIR + '/.config/RTK'):
            self.RTK_CONF_DIR = self.RTK_HOME_DIR + '/.config/RTK'
        else:
            self.RTK_CONF_DIR = self.RTK_SITE_DIR
            _return = first_run

        self.RTK_PROG_CONF = self.RTK_CONF_DIR + '/RTK.conf'

        return _return
