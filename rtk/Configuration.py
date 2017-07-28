#!/usr/bin/env python
"""
This file contains configuration information and functions for RTK.

:const ICON_DIR: Default value: ''
Path to the directory containing icon files used by RTK. \n
POSIX default: /usr/share/pixmaps/RTK \n
Windows default: None

:const DATA_DIR: Default value: ''
Path to the directory containing data files used by RTK. \n
POSIX default: /usr/share/RTK \n
Windows default: None

:const CONF_DIR: Default value: ''
Path to the directory containing configuration files used by RTK.\n
POSIX default: $HOME/.config/RTK \n
Windows default: C:\\\Users\\\<USER NAME>\\\config\\\RTK

:const LOG_DIR: Default value: ''
Path to the directory containing log files used by RTK. \n
POSIX default: $HOME/.config/RTK/logs \n
Windows default: C:\\\Users\\\<USER NAME>\\\config\\\RTK\\\logs

:const PROG_DIR: Default value: ''
Path to the base directory containing RTK Program database files.  This is only
used when the backend is SQLite3. \n
POSIX default: $HOME/analyses/rtk \n
Windows default: C:\\\Users\\\<USER NAME>\\\analyses\\\rtk

:const RTK_MODE_SOURCE: Default value: 1
Indicator variable used to determine which failure mode source to use.

:const RTK_FORMAT_FILE: Default value: []
Global list containing the path to the format files to use for various widgets.

+-------+----------------------------+
| Index | Tree Format                |
+=======+============================+
|    0  | Revision Tree              |
+-------+----------------------------+
|    1  | Function Tree              |
+-------+----------------------------+
|    2  | Requirements Tree          |
+-------+----------------------------+
|    3  | Hardware Tree              |
+-------+----------------------------+
|    4  | Validation Tree            |
+-------+----------------------------+
|    5  | Reliability Growth Tree    |
+-------+----------------------------+
|    6  | Field Incidents List       |
+-------+----------------------------+
|    7  | Parts List                 |
+-------+----------------------------+
|    8  | Similar Item Analysis      |
+-------+----------------------------+
|    9  | Hardware FMECA             |
+-------+----------------------------+
|   10  | Stakeholder Input          |
+-------+----------------------------+
|   11  | Test Planning List         |
+-------+----------------------------+
|   12  | Future Use                 |
+-------+----------------------------+
|   13  | Future Use                 |
+-------+----------------------------+
|   14  | Future Use                 |
+-------+----------------------------+
|   15  | Software Tree              |
+-------+----------------------------+
|   16  | Dataset Tree               |
+-------+----------------------------+
|   17  | Risk Analysis              |
+-------+----------------------------+
|   18  | Functional FMECA           |
+-------+----------------------------+
|   19  | Software FMECA             |
+-------+----------------------------+

:const RTK_COLORS: Default value: []
Global list containing the colors to use for various widgets.

+-------+-----------------------------------------------+
| Index | Tree Color                                    |
+=======+===============================================+
|   0   | Revision Tree background                      |
+-------+-----------------------------------------------+
|   1   | Revision Tree foreground                      |
+-------+-----------------------------------------------+
|   2   | Function Tree background                      |
+-------+-----------------------------------------------+
|   3   | Function Tree foreground                      |
+-------+-----------------------------------------------+
|   4   | Requirement Tree background                   |
+-------+-----------------------------------------------+
|   5   | Requirement Tree foreground                   |
+-------+-----------------------------------------------+
|   6   | Hardware Tree background                      |
+-------+-----------------------------------------------+
|   7   | Hardware Tree foreground                      |
+-------+-----------------------------------------------+
|   8   | Validation Tree background                    |
+-------+-----------------------------------------------+
|   9   | Validation Tree foreground                    |
+-------+-----------------------------------------------+
|  10   | Reliability Testing Tree background           |
+-------+-----------------------------------------------+
|  11   | Reliability Testing Tree foreground           |
+-------+-----------------------------------------------+
|  12   | Program Incident Tree background              |
+-------+-----------------------------------------------+
|  13   | Program Incident Tree foreground              |
+-------+-----------------------------------------------+
|  14   | Dataset Tree background color                 |
+-------+-----------------------------------------------+
|  15   | Dataset Tree foreground color                 |
+-------+-----------------------------------------------+
|  16   | Part List Tree background                     |
+-------+-----------------------------------------------+
|  17   | Part List Tree foreground                     |
+-------+-----------------------------------------------+
|  18   | Overstressed Part background                  |
+-------+-----------------------------------------------+
|  19   | Overstressed Part foreground                  |
+-------+-----------------------------------------------+
|  20   | Tagged Part background                        |
+-------+-----------------------------------------------+
|  21   | Tagged Part foreground                        |
+-------+-----------------------------------------------+
|  22   | Part with no failure rate model foreground    |
+-------+-----------------------------------------------+
|  23   | Software Tree background color                |
+-------+-----------------------------------------------+
|  24   | Software Tree foreground color                |
+-------+-----------------------------------------------+

:const RTK_PREFIX: Default value: []
Global variable list to house information about the prefix and next index to
use when adding new revisions, functions, assemblies, parts, FMECA items,
FMECA modes, FMECA effects, and FMECA causes.

+-------+---------------------------+
| Index | Next Prefix/Index         |
+=======+===========================+
|   0   | Revision prefix           |
+-------+---------------------------+
|   1   | Next Revision index       |
+-------+---------------------------+
|   2   | Function prefix           |
+-------+---------------------------+
|   3   | Next Function index       |
+-------+---------------------------+
|   4   | Hardware prefix           |
+-------+---------------------------+
|   5   | Next Hardware index       |
+-------+---------------------------+
|   6   | Part prefix               |
+-------+---------------------------+
|   7   | Next Part index           |
+-------+---------------------------+
|   8   | FMECA item prefix         |
+-------+---------------------------+
|   9   | Next FMECA item index     |
+-------+---------------------------+
|  10   | FMECA mode prefix         |
+-------+---------------------------+
|  11   | Next FMECA mode index     |
+-------+---------------------------+
|  12   | FMECA effect prefix       |
+-------+---------------------------+
|  13   | Next FMECA effect index   |
+-------+---------------------------+
|  14   | FMECA cause prefix        |
+-------+---------------------------+
|  15   | Next FMECA cause index    |
+-------+---------------------------+
|  16   | Software prefix           |
+-------+---------------------------+
|  17   | Next Software index       |
+-------+---------------------------+

:const RTK_MODULES: Default value: []
Global list to house information about the active modules.  Where 1 = active
and 0 = inactive.

+-------+---------------+
| Index | Module        |
+=======+===============+
|   0   | Revision      |
+-------+---------------+
|   1   | Function      |
+-------+---------------+
|   2   | Requirements  |
+-------+---------------+
|   3   | Hardware      |
+-------+---------------+
|   4   | Software      |
+-------+---------------+
|   5   | Validation    |
+-------+---------------+
|   6   | Testing       |
+-------+---------------+
|   7   | Incidents     |
+-------+---------------+
|   8   | Dataset       |
+-------+---------------+
|   9   | FMECA         |
+-------+---------------+
|  10   | RCM           |
+-------+---------------+
|  11   | RBD           |
+-------+---------------+
|  12   | FTA           |
+-------+---------------+

:const RTK_PAGE_NUMBER: Default value: []

:const RTK_COM_INFO: Default value: []
Global list for the RTK common database connection information.

+-------+-------------------------------+
| Index | Information                   |
+=======+===============================+
|   0   | Host name (MySQL only)        |
+-------+-------------------------------+
|   1   | Host port (MySQL only)        |
+-------+-------------------------------+
|   2   | Database name                 |
+-------+-------------------------------+
|   3   | User name (MySQL only)        |
+-------+-------------------------------+
|   4   | User password (MySQL only)    |
+-------+-------------------------------+

:const RTK_PROG_INFO: Default value: []
Global list for RTK Program database connectioninformation.

+-------+-------------------------------+
| Index | Information                   |
+=======+===============================+
|   0   | Host name (MySQL only)        |
+-------+-------------------------------+
|   1   | Host port (MySQL only)        |
+-------+-------------------------------+
|   2   | Database name                 |
+-------+-------------------------------+
|   3   | User name (MySQL only)        |
+-------+-------------------------------+
|   4   | User password (MySQL only)    |
+-------+-------------------------------+

:const RTK_FAILURE_PROBABILITY: default value: []
Global list for qualitative failure probability categories.

:const RTK_SEVERITY: default value: []
Global list for failure severity categories.

:const RTK_HAZARDS: default value: []
Global list for potential hazards.

:const RTK_RISK_POINTS: default value: [4, 10]
Global list for risk level cutoffs.

+-------+---------------------------+
| Index | Risk Level Cutoff Value   |
+=======+===========================+
|   0   | Low to medium             |
+-------+---------------------------+
|   1   | Medium to high            |
+-------+---------------------------+

:const RTK_REQUIREMENT_TYPES: default value: []
Global list of requirement types.

:const RTK_FMECA_METHOD: default value: 1
Global indicator variable for the criticality method used.  1=Task 102, 2=RPN.

:const RTK_RPN_FORMAT: default value: 0
Global indicator variable for the level that the RPN is calculated.  0=Mechanism, 1=Cause.

:const RTK_RPN_SEVERITY: default value: []
Global list for RPN Severity categories.

:const RTK_RPN_OCCURRENCE: default value: []
Global list for RPN Occurrence categories.

:const RTK_RPN_DETECTION: default value: []
Global list for RPN Detection categories.

:const COM_BACKEND: Default value: ''
RTK common database backend to use; mysql or sqlite3.

:const BACKEND: Default value: ''
RTK Program database backend to use; mysql or sqlite3.

:const LOCALE: Default value: en_US
The language locale to use with RTK.

:const OS: Default value: ''
The operating system RTK is currently running on.

:const FRMULT: Default value: 1.0
The failure rate multiplier.  All failure rates will be multiplied by this
value for display.  This allows failure rates to display without using
scientific notation.

:const PLACES: Default value: 6
Number of decimal places to show in numerical results.

:const RTK_MTIME: Default value: 10.0
The default mission time for new RTK Programs.

:const TABPOS: Default value: ['Top', 'Bottom', 'Bottom']
Location of tabs in the three main gtk.Notebook() widgets.  Can be 'Top',
'Bottom', 'Left', or 'Right'.

+-------+---------------+
| Index | Notebook      |
+=======+===============+
|   0   | Module Book   |
+-------+---------------+
|   1   | Work Book     |
+-------+---------------+
|   2   | List Book     |
+-------+---------------+

:const RTK_GUI_LAYOUT: Layout of the GUI to use.  Possible options are:
    * basic: a single window embedded with the Module Book, Work Book, and List
             Book.
    * advanced: multiple windows; one each for the Module Book, Work Book, and
                List Book.
"""

# -*- coding: utf-8 -*-
#
#       rtk.Configuration.py is part of The RTK Project
#
# All rights reserved.

import ConfigParser
from os import environ, path, makedirs, name

# Add localization support.
import gettext

# Import other RTK modules.
import Utilities

_ = gettext.gettext

__author__ = 'Andrew Rowland <andrew.rowland@reliaqual.com>'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

RTK_MODE = ''
MODE = ''                               # TODO: Retire this variable.

RTK_SITE_DIR = ''
SITE_DIR = ''                           # TODO: Retire this variable.
RTK_ICON_DIR = ''
ICON_DIR = ''                           # TODO: Retire this variable.
RTK_DATA_DIR = ''
DATA_DIR = ''                           # TODO: Retire this variable.
RTK_CONF_DIR = ''
CONF_DIR = ''                           # TODO: Retire this variable.
RTK_LOG_DIR = ''
LOG_DIR = ''                            # TODO: Retire this variable.
RTK_PROG_DIR = ''
PROG_DIR = ''                           # TODO: Retire this variable.

# --------------------------------------------------------------------- #
# Log files.                                                            #
# --------------------------------------------------------------------- #
RTK_DEBUG_LOG = ''
RTK_IMPORT_LOG = ''
RTK_USER_LOG = ''

# --------------------------------------------------------------------- #
# Format files.                                                         #
# --------------------------------------------------------------------- #
RTK_FORMAT_FILE = {}
RTK_COLORS = {}
RTK_PREFIX = {}

# --------------------------------------------------------------------- #
# Dictionaries filled by RTK Common DB table RTKCategory.               #
# --------------------------------------------------------------------- #
RTK_ACTION_CATEGORY = {}
RTK_INCIDENT_CATEGORY = {}
RTK_SEVERITY = {}

# --------------------------------------------------------------------- #
# Dictionaries filled by RTK Common DB table RTKEnviron.                #
# --------------------------------------------------------------------- #
RTK_ACTIVE_ENVIRONMENTS = {}
RTK_DORMANT_ENVIRONMENTS = {}
RTK_SW_DEV_ENVIRONMENTS = {}

# --------------------------------------------------------------------- #
# Dictionaries filled by RTK Common DB table RTKGroup.                  #
# --------------------------------------------------------------------- #
RTK_AFFINITY_GROUPS = {}
RTK_WORKGROUPS = {}

# --------------------------------------------------------------------- #
# Dictionaries filled by RTK Common DB table RTKLevel.                  #
# --------------------------------------------------------------------- #
RTK_FAILURE_PROBABILITY = {}
RTK_SW_LEVELS = {}

# --------------------------------------------------------------------- #
# Dictionaries filled by RTK Common DB table RTKMethod.                 #
# --------------------------------------------------------------------- #
RTK_DETECTION_METHODS = {}
RTK_SW_TEST_METHODS = {}

# --------------------------------------------------------------------- #
# Dictionaries filled by RTK Common DB table RTKModel.                  #
# --------------------------------------------------------------------- #
RTK_ALLOCATION_MODELS = {}
RTK_DAMAGE_MODELS = {}
RTK_HR_MODEL = {}

# --------------------------------------------------------------------- #
# Dictionaries filled by RTK Common DB table RTKPhase.                  #
# --------------------------------------------------------------------- #
RTK_LIFECYCLE = {}
RTK_SW_DEV_PHASES = {}

# --------------------------------------------------------------------- #
# Dictionaries filled by RTK Common DB table RTKRPN.                    #
# --------------------------------------------------------------------- #
RTK_RPN_DETECTION = {}
RTK_RPN_SEVERITY = {}
RTK_RPN_OCCURRENCE = {}

# --------------------------------------------------------------------- #
# Dictionaries filled by RTK Common DB table RTKStatus.                 #
# --------------------------------------------------------------------- #
RTK_ACTION_STATUS = {}
RTK_INCIDENT_STATUS = {}

# --------------------------------------------------------------------- #
# Dictionaries filled by RTK Common DB table RTKType.                   #
# --------------------------------------------------------------------- #
RTK_CONTROL_TYPES = []
RTK_COST_TYPE = {}
RTK_HR_TYPE = {}
RTK_INCIDENT_TYPE = {}
RTK_MTTR_TYPE = {}
RTK_REQUIREMENT_TYPE = {}
RTK_VALIDATION_TYPE = {}

# --------------------------------------------------------------------- #
# Dictionaries filled from RTK Common DB tables that require no filter. #
# --------------------------------------------------------------------- #
RTK_SW_APPLICATION = {}
RTK_CATEGORIES = {}
RTK_CRITICALITY = {}
RTK_FAILURE_MODES = {}                  # Default failure modes.
RTK_HAZARDS = {}
RTK_MANUFACTURERS = {}
RTK_MEASUREMENT_UNITS = {}
RTK_OPERATING_PARAMETERS = {}           # TODO: Add table to common db for this.
RTK_S_DIST = {}
RTK_STAKEHOLDERS = {}
RTK_SUBCATEGORIES = {}
RTK_USERS = {}

# --------------------------------------------------------------------- #
# Risk analyses configuration options.                                  #
# --------------------------------------------------------------------- #
RTK_RISK_POINTS = [4, 10]

# --------------------------------------------------------------------- #
# FMEA configuration options.                                           #
# --------------------------------------------------------------------- #
RTK_MODE_SOURCE = 1                     # 1=FMD-97
RTK_FMECA_METHOD = 1                    # 1=Task 102, 2=RPN
RTK_RPN_FORMAT = 0                      # RPN at mechanism level.

# --------------------------------------------------------------------- #
# RTK Database configuration options.                                   #
# --------------------------------------------------------------------- #
RTK_COM_BACKEND = ''
COM_BACKEND = ''                        # TODO: Retire this variable.
RTK_BACKEND = ''
BACKEND = ''                            # TODO: Retire this variable.

RTK_COM_INFO = {}                       # RTK Common database info.
RTK_PROG_INFO = {}                      # RTK Program database info.

# --------------------------------------------------------------------- #
RTK_MODULES = []
RTK_PAGE_NUMBER = []

RTK_HARDWARE_LIST = []                  # TODO: Retire this variable.
RTK_SOFTWARE_LIST = []                  # TODO: Retire this variable.

RTK_HR_MULTIPLIER = 1000000.0
FRMULT = 1000000.0                      # TODO: Retire this variable.
RTK_DEC_PLACES = 6
PLACES = 6                              # TODO: Retire this variable.
RTK_MTIME = 10.0

RTK_TABPOS = {'listbook' : 'top', 'modulebook' : 'bottom',
              'workbook' : 'bottom'}
TABPOS = ['top', 'bottom', 'bottom']    # TODO: Retire this variable.

RTK_GUI_LAYOUT = 'basic'

METHOD = 'STANDARD'                     # TODO: Retire this variable.
RTK_METHOD = 'STANDARD'                 # STANDARD or LRM

LOCALE = 'en_US'
OS = ''


class RTKConf(object):
    """
    The RTK configuration class.
    """

    def __init__(self, level='site'):
        """
        Method to initialize the RTK configuration parser.

        :param str level: indicates which configuration file is to be read.
                          One of 'site' or 'user'.
        """

        _DIRS = {}

        if name == 'posix':
            self.OS = 'Linux'
            self.SITE_DIR = '/etc/RTK/'
            _DIRS['HOME'] = environ['HOME']
            _DIRS['DATA'] = '/usr/share/RTK/'
            _DIRS['ICON'] = '/usr/share/pixmaps/RTK/'
            _DIRS['LOG'] = '/var/log/RTK/'
            _DIRS['PROG'] = _DIRS['HOME'] + '/analyses/rtk/'

        elif name == 'nt':
            self.OS = 'Windows'
            self.SITE_DIR = environ['COMMONPROGRAMFILES(X86)'] + '/RTK/'
            _DIRS['HOME'] = environ['USERPROFILE']
            _DIRS['DATA'] = self.SITE_DIR + 'data/'
            _DIRS['ICON'] = self.SITE_DIR + 'icons/'
            _DIRS['LOG'] = self.SITE_DIR + 'logs/'
            _DIRS['PROG'] = _DIRS['HOME'] + '/analyses/rtk/'

        if level == 'site':
            self._set_site_variables(_DIRS)

        elif level == 'user':
            self._set_user_variables(_DIRS)

    def _set_site_variables(self, directories):
        """
        Method to set the site configuration variables.

        :param dict directories: dictionary of directory paths.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if Utilities.dir_exists(self.SITE_DIR):
            self.conf_dir = self.SITE_DIR
        else:
            self.conf_dir = directories['HOME'] + '/.config/RTK/'

        if Utilities.dir_exists(directories['DATA']):
            self.data_dir = directories['DATA']
        else:
            self.data_dir = directories['HOME'] + '/.config/RTK/data/'

        if Utilities.dir_exists(directories['ICON']):
            self.icon_dir = directories['ICON']
        else:
            self.icon_dir = directories['HOME'] + '/.config/RTK/icons'

        if Utilities.dir_exists(directories['LOG']):
            self.log_dir = directories['LOG']
        else:
            self.log_dir = directories['HOME'] + '/.config/RTK/logs/'

        self.conf_file = self.conf_dir + 'site.conf'

        return False

    def _set_user_variables(self, directories):
        """
        Method to set the user-specific configuration variables.

        :param dict directories: dictionary of directory paths.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.conf_dir = directories['HOME'] + '/.config/RTK/'

        if Utilities.dir_exists(directories['HOME'] + '/.config/RTK/data/'):
            self.data_dir = directories['HOME'] + '/.config/RTK/data/'
        else:
            self.data_dir = directories['DATA']

        if Utilities.dir_exists(directories['HOME'] + '/.config/RTK/icons'):
            self.icon_dir = directories['HOME'] + '/.config/RTK/icons'
        else:
            self.icon_dir = directories['ICON']

        if Utilities.dir_exists(directories['HOME'] + '/.config/RTK/logs/'):
            self.log_dir = directories['HOME'] + '/.config/RTK/logs/'
        else:
            self.log_dir = directories['LOG']

        if Utilities.dir_exists(directories['PROG']):
            self.prog_dir = directories['PROG']
        else:
            self.prog_dir = directories['HOME']

        self.conf_file = self.conf_dir + 'RTK.conf'

        if not Utilities.file_exists(self.conf_file):
            self.create_default_configuration()

        return False

    def create_default_configuration(self):     # pylint: disable=R0914
        """
        Method to create a default configuration file in the site or user's
        configuration directory.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from os.path import basename

        if basename(self.conf_file) == 'site.conf':
            self._create_site_configuration()

        elif basename(self.conf_file) == 'RTK.conf':
            self._create_user_configuration()

        return False

    def _create_site_configuration(self):
        """
        Method to create the default site configuration file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _config = ConfigParser.ConfigParser()

        _config.add_section('Modules')
        _config.set('Modules', 'function', 'True')
        _config.set('Modules', 'requirement', 'True')
        _config.set('Modules', 'hardware', 'True')
        _config.set('Modules', 'prediction', 'True')
        _config.set('Modules', 'fmeca', 'True')
        _config.set('Modules', 'maintainability', 'True')
        _config.set('Modules', 'software', 'True')
        _config.set('Modules', 'testing', 'True')
        _config.set('Modules', 'validation', 'True')
        _config.set('Modules', 'incident', 'True')
        _config.set('Modules', 'survival', 'True')

        _config.add_section('Backend')
        _config.set('Backend', 'host', 'localhost')
        _config.set('Backend', 'socket', 3306)
        _config.set('Backend', 'database', '')
        _config.set('Backend', 'user', 'user')
        _config.set('Backend', 'password', 'password')
        _config.set('Backend', 'type', 'sqlite3')
        _config.set('Backend', 'path', self.SITE_DIR)

        try:
            _parser = open(self.conf_file, 'w')
            _config.write(_parser)
            _parser.close()

        except EnvironmentError:
            _return = True

        return _return

    def _create_user_configuration(self):
        """
        Method to create the default user configuration file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        import glob
        from distutils import dir_util, file_util

        _return = False

        _config = ConfigParser.ConfigParser()

        if name == 'posix':
            _HOMEDIR = environ['HOME']

        elif name == 'nt':
            _HOMEDIR = environ['USERPROFILE']

        # Create the directories needed for the user.
        if not Utilities.dir_exists(self.conf_dir):
            try:
                makedirs(self.conf_dir)
            except OSError:
                pass

        if not Utilities.dir_exists(_HOMEDIR + '/.config/RTK/data/'):
            try:
                makedirs(_HOMEDIR + '/.config/RTK/data/')
            except OSError:
                pass

        if not Utilities.dir_exists(_HOMEDIR + '/.config/RTK/logs/'):
            try:
                makedirs(_HOMEDIR + '/.config/RTK/logs/')
            except OSError:
                pass

        # Copy format files from SITE_DIR to the user's _CONFDIR.
        for _file in glob.glob(self.SITE_DIR + '*.xml'):
            file_util.copy_file(_file, self.conf_dir)

        # Copy SQL files from SITE_DIR to the user's _DATADIR.
        for _file in glob.glob(self.SITE_DIR + '/data/*.sql'):
            file_util.copy_file(_file, self.conf_dir + '/data/')

        # Copy the icons from SITE_DIR to the user's _CONFDIR.
        if not Utilities.dir_exists(self.conf_dir + '/icons/'):
            makedirs(self.conf_dir + '/icons/')
        try:
            dir_util.copy_tree(self.SITE_DIR + '/icons/',
                               self.conf_dir + '/icons/')
        except IOError:
            print self.conf_dir

        # Create the default RTK user configuration file.
        _config.add_section('General')
        _config.set('General', 'reportsize', 'letter')
        _config.set('General', 'failtimeunit', 'hours')
        _config.set('General', 'repairtimeunit', 'hours')
        _config.set('General', 'frmultiplier', 1000000.0)
        _config.set('General', 'calcreltime', 100.0)
        _config.set('General', 'autoaddlistitems', 'False')
        _config.set('General', 'decimal', 6)
        _config.set('General', 'modesource', 1)
        _config.set('General', 'parallelcalcs', 'False')
        _config.set('General', 'treetabpos', 'top')
        _config.set('General', 'listtabpos', 'bottom')
        _config.set('General', 'booktabpos', 'bottom')

        _config.add_section('Backend')
        _config.set('Backend', 'type', 'sqlite3')
        _config.set('Backend', 'host', 'localhost')
        _config.set('Backend', 'socket', 3306)
        _config.set('Backend', 'database', '')
        _config.set('Backend', 'user', '')
        _config.set('Backend', 'password', '')

        _config.add_section('Directories')
        _config.set('Directories', 'datadir', 'data')
        _config.set('Directories', 'icondir', 'icons')
        _config.set('Directories', 'logdir', 'logs')
        _config.set('Directories', 'progdir', 'analyses/rtk')

        _config.add_section('Files')
        _config.set('Files', 'datasetformat', 'dataset_format.xml')
        _config.set('Files', 'fmecaformat', 'fmeca_format.xml')
        _config.set('Files', 'ffmecaformat', 'ffmeca_format.xml')
        _config.set('Files', 'sfmecaformat', 'sfmeca_format.xml')
        _config.set('Files', 'functionformat', 'function_format.xml')
        _config.set('Files', 'hardwareformat', 'hardware_format.xml')
        _config.set('Files', 'incidentformat', 'incident_format.xml')
        _config.set('Files', 'rgincidentformat', 'rgincident_format.xml')
        _config.set('Files', 'partformat', 'part_format.xml')
        _config.set('Files', 'requirementformat', 'requirement_format.xml')
        _config.set('Files', 'revisionformat', 'revision_format.xml')
        _config.set('Files', 'riskformat', 'risk_format.xml')
        _config.set('Files', 'siaformat', 'sia_format.xml')
        _config.set('Files', 'softwareformat', 'software_format.xml')
        _config.set('Files', 'testformat', 'testing_format.xml')
        _config.set('Files', 'validationformat', 'validation_format.xml')

        _config.add_section('Colors')
        _config.set('Colors', 'revisionbg', '#FFFFFF')
        _config.set('Colors', 'revisionfg', '#000000')
        _config.set('Colors', 'functionbg', '#FFFFFF')
        _config.set('Colors', 'functionfg', '#0000FF')
        _config.set('Colors', 'requirementbg', '#FFFFFF')
        _config.set('Colors', 'requirementfg', '#000000')
        _config.set('Colors', 'assemblybg', '#FFFFFF')
        _config.set('Colors', 'assemblyfg', '#000000')
        _config.set('Colors', 'softwarebg', '#FFFFFF')
        _config.set('Colors', 'softwarefg', '#000000')
        _config.set('Colors', 'validationbg', '#FFFFFF')
        _config.set('Colors', 'validationfg', '#00FF00')
        _config.set('Colors', 'rgbg', '#FFFFFF')
        _config.set('Colors', 'rgfg', '#000000')
        _config.set('Colors', 'fracabg', '#FFFFFF')
        _config.set('Colors', 'fracafg', '#000000')
        _config.set('Colors', 'partbg', '#FFFFFF')
        _config.set('Colors', 'partfg', '#000000')
        _config.set('Colors', 'overstressbg', '#FF0000')
        _config.set('Colors', 'overstressfg', '#FFFFFF')
        _config.set('Colors', 'taggedbg', '#00FF00')
        _config.set('Colors', 'taggedfg', '#FFFFFF')
        _config.set('Colors', 'nofrmodelfg', '#A52A2A')

        try:
            _parser = open(self.conf_file, 'w')
            _config.write(_parser)
            _parser.close()
        except EnvironmentError:
            _return = True

        return _return

    def write_configuration(self):
        """
        Method to write changes to the user's configuration file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if Utilities.file_exists(self.conf_file):
            _config = ConfigParser.ConfigParser()
            _config.add_section('General')
            _config.set('General', 'reportsize', 'letter')
            _config.set('General', 'repairtimeunit', 'hours')
            _config.set('General', 'parallelcalcs', 'False')
            _config.set('General', 'frmultiplier', self.FRMULT)
            _config.set('General', 'failtimeunit', 'hours')
            _config.set('General', 'calcreltime', self.RTK_MTIME)
            _config.set('General', 'autoaddlistitems', 'False')
            _config.set('General', 'decimal', self.PLACES)
            _config.set('General', 'modesource', self.RTK_MODE_SOURCE)
            _config.set('General', 'treetabpos', self.TABPOS[0])
            _config.set('General', 'listtabpos', self.TABPOS[1])
            _config.set('General', 'booktabpos', self.TABPOS[2])

            _config.add_section('Backend')
            _config.set('Backend', 'type', self.BACKEND)
            _config.set('Backend', 'host', self.RTK_PROG_INFO[0])
            _config.set('Backend', 'socket', self.RTK_PROG_INFO[1])
            _config.set('Backend', 'database', self.RTK_PROG_INFO[2])
            _config.set('Backend', 'user', self.RTK_PROG_INFO[3])
            _config.set('Backend', 'password', self.RTK_PROG_INFO[4])

            _config.add_section('Directories')
            _config.set('Directories', 'datadir', 'data')
            _config.set('Directories', 'icondir', 'icons')
            _config.set('Directories', 'logdir', 'log')

            _config.add_section('Files')
            _config.set('Files', 'revisionformat',
                        path.basename(self.RTK_FORMAT_FILE[0]))
            _config.set('Files', 'functionformat',
                        path.basename(self.RTK_FORMAT_FILE[1]))
            _config.set('Files', 'requirementformat',
                        path.basename(self.RTK_FORMAT_FILE[2]))
            _config.set('Files', 'hardwareformat',
                        path.basename(self.RTK_FORMAT_FILE[3]))
            _config.set('Files', 'validationformat',
                        path.basename(self.RTK_FORMAT_FILE[4]))
            _config.set('Files', 'partformat',
                        path.basename(self.RTK_FORMAT_FILE[5]))
            _config.set('Files', 'siaformat',
                        path.basename(self.RTK_FORMAT_FILE[6]))
            _config.set('Files', 'fmecaformat',
                        path.basename(self.RTK_FORMAT_FILE[7]))
            _config.set('Files', 'testformat',
                        path.basename(self.RTK_FORMAT_FILE[8]))
            _config.set('Files', 'rgincidentformat',
                        path.basename(self.RTK_FORMAT_FILE[9]))
            _config.set('Files', 'stakeholderformat',
                        path.basename(self.RTK_FORMAT_FILE[10]))
            _config.set('Files', 'incidentformat',
                        path.basename(self.RTK_FORMAT_FILE[11]))
            _config.set('Files', 'softwareformat',
                        path.basename(self.RTK_FORMAT_FILE[12]))
            _config.set('Files', 'datasetformat',
                        path.basename(self.RTK_FORMAT_FILE[13]))
            _config.set('Files', 'riskformat',
                        path.basename(self.RTK_FORMAT_FILE[14]))

            _config.add_section('Colors')
            _config.set('Colors', 'revisionbg', self.RTK_COLORS[0])
            _config.set('Colors', 'revisionfg', self.RTK_COLORS[1])
            _config.set('Colors', 'functionbg', self.RTK_COLORS[2])
            _config.set('Colors', 'functionfg', self.RTK_COLORS[3])
            _config.set('Colors', 'requirementbg', self.RTK_COLORS[4])
            _config.set('Colors', 'requirementfg', self.RTK_COLORS[5])
            _config.set('Colors', 'assemblybg', self.RTK_COLORS[6])
            _config.set('Colors', 'assemblyfg', self.RTK_COLORS[7])
            _config.set('Colors', 'validationbg', self.RTK_COLORS[8])
            _config.set('Colors', 'validationfg', self.RTK_COLORS[9])
            _config.set('Colors', 'rgbg', self.RTK_COLORS[10])
            _config.set('Colors', 'rgfg', self.RTK_COLORS[11])
            _config.set('Colors', 'fracabg', self.RTK_COLORS[12])
            _config.set('Colors', 'fracafg', self.RTK_COLORS[13])
            _config.set('Colors', 'partbg', self.RTK_COLORS[14])
            _config.set('Colors', 'partfg', self.RTK_COLORS[15])
            _config.set('Colors', 'overstressbg', self.RTK_COLORS[16])
            _config.set('Colors', 'overstressfg', self.RTK_COLORS[17])
            _config.set('Colors', 'taggedbg', self.RTK_COLORS[18])
            _config.set('Colors', 'taggedfg', self.RTK_COLORS[19])
            _config.set('Colors', 'nofrmodelfg', self.RTK_COLORS[20])
            _config.set('Colors', 'softwarebg', self.RTK_COLORS[21])
            _config.set('Colors', 'softwarefg', self.RTK_COLORS[22])

            try:
                _parser = open(self.conf_file, 'w')
                _config.write(_parser)
                _parser.close()
            except EnvironmentError:
                _return = True

        return _return

    def read_configuration(self):
        """
        Method to read the configuration file.

        :return: _config
        :rtype: ConfigParser.ConfigParser()
        """

        # Try to read the user's configuration file.  If it doesn't exist,
        # create a new one.  If those options fail, read the system-wide
        # configuration file and keep going.
        if Utilities.file_exists(self.conf_file):
            _config = ConfigParser.ConfigParser()
            _config.read(self.conf_file)
        else:
            _config = None

        return _config
