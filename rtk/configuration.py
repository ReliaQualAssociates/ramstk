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

__author__ = 'Andrew Rowland <andrew.rowland@reliaqual.com>'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.configuration.py is part of The RTK Project
#
# All rights reserved.

import ConfigParser
from os import environ, path, makedirs, name

# Add localization support.
import gettext
_ = gettext.gettext

# Import other RTK modules.
import utilities as _util
import widgets as _widg

MODE = ''

SITE_DIR = ''
ICON_DIR = ''
DATA_DIR = ''
CONF_DIR = ''
LOG_DIR = ''
PROG_DIR = ''

RTK_FORMAT_FILE = []
RTK_COLORS = []
RTK_PREFIX = []

RTK_MODULES = []
RTK_PAGE_NUMBER = []

RTK_COM_INFO = []
RTK_PROG_INFO = []

RTK_HARDWARE_LIST = []
RTK_SOFTWARE_LIST = []

# ------------------------------------------------------------------------- #
# Requirement analysis configuration options.                               #
# ------------------------------------------------------------------------- #
RTK_STAKEHOLDERS = []
RTK_AFFINITY_GROUPS = []

# ------------------------------------------------------------------------- #
# Risk analyses configuration options.                                      #
# ------------------------------------------------------------------------- #
RTK_SEVERITY = []
RTK_FAILURE_PROBABILITY = []
RTK_HAZARDS = []
RTK_RISK_POINTS = [4, 10]

# ------------------------------------------------------------------------- #
# FMEA configuration options.                                               #
# ------------------------------------------------------------------------- #
RTK_MODE_SOURCE = 1                         # 1=FMD-97
RTK_FMECA_METHOD = 1                        # 1=Task 102, 2=RPN

RTK_RPN_FORMAT = 0                          # RPN at mechanism level.
RTK_RPN_SEVERITY = []
RTK_RPN_OCCURRENCE = []
RTK_RPN_DETECTION = []

# ------------------------------------------------------------------------- #
# PoF configuration options.                                                #
# ------------------------------------------------------------------------- #
# TODO: Add tables to the common database for these.
RTK_DAMAGE_MODELS = []
RTK_OPERATING_PARAMETERS = []

# ------------------------------------------------------------------------- #
# Hardware configuration options.                                           #
# ------------------------------------------------------------------------- #
RTK_CATEGORIES = {}
RTK_SUBCATEGORIES = {}

# ------------------------------------------------------------------------- #
# Validation configuration options.                                         #
# ------------------------------------------------------------------------- #
RTK_TASK_TYPE = []
RTK_MEASUREMENT_UNITS = []

# ------------------------------------------------------------------------- #
# Incident configuration options.                                           #
# ------------------------------------------------------------------------- #
RTK_USERS = []
RTK_INCIDENT_CATEGORY = []
RTK_INCIDENT_TYPE = []
RTK_INCIDENT_STATUS = []
RTK_INCIDENT_CRITICALITY = []
RTK_LIFECYCLE = []
RTK_DETECTION_METHODS = []

COM_BACKEND = ''
BACKEND = ''

LOCALE = 'en_US'
OS = ''

FRMULT = 1000000.0
PLACES = 6
RTK_MTIME = 10.0

TABPOS = ['top', 'bottom', 'bottom']

RTK_GUI_LAYOUT = 'basic'

METHOD = 'STANDARD'                         # STANDARD or LRM


class RTKConf(object):
    """
    The RTK configuration class.
    """

    def __init__(self, level='site'):
        """
        Initializes the RTK configuration parser.

        :param str level: indicates which configuration file is to be read.
                          One of 'site' or 'user'.
        """

        if name == 'posix':
            self.OS = 'Linux'
            _SITEDIR = '/etc/RTK/'
            _DATADIR = '/usr/share/RTK/'
            _ICONDIR = '/usr/share/pixmaps/RTK/'
            _LOGDIR = '/var/log/RTK/'
            _HOMEDIR = environ['HOME']
            _PROGDIR = _HOMEDIR + '/analyses/rtk/'

        elif name == 'nt':
            self.OS = 'Windows'
            _HOMEDIR = environ['USERPROFILE']
            _SITEDIR = environ['COMMONPROGRAMFILES(X86)'] + '/RTK/'
            _DATADIR = _SITEDIR + 'data/'
            _ICONDIR = _SITEDIR + 'icons/'
            _LOGDIR = _SITEDIR + 'logs/'
            _PROGDIR = _HOMEDIR + '/analyses/rtk/'

        self.SITE_DIR = _SITEDIR

        if level == 'site':
            if _util.dir_exists(_SITEDIR):
                self.conf_dir = _SITEDIR
            else:
                self.conf_dir = _HOMEDIR + '/.config/RTK/'

            if _util.dir_exists(_DATADIR):
                self.data_dir = _DATADIR
            else:
                self.data_dir = _HOMEDIR + '/.config/RTK/data/'

            if _util.dir_exists(_ICONDIR):
                self.icon_dir = _ICONDIR
            else:
                self.icon_dir = _HOMEDIR + '/.config/RTK/icons'

            if _util.dir_exists(_LOGDIR):
                self.log_dir = _LOGDIR
            else:
                self.log_dir = _HOMEDIR + '/.config/RTK/logs/'

            self._conf_file = self.conf_dir + 'site.conf'

        elif level == 'user':
            self.conf_dir = _HOMEDIR + '/.config/RTK/'

            if _util.dir_exists(_HOMEDIR + '/.config/RTK/data/'):
                self.data_dir = _HOMEDIR + '/.config/RTK/data/'
            else:
                self.data_dir = _DATADIR

            if _util.dir_exists(_HOMEDIR + '/.config/RTK/icons'):
                self.icon_dir = _HOMEDIR + '/.config/RTK/icons'
            else:
                self.icon_dir = _ICONDIR

            if _util.dir_exists(_HOMEDIR + '/.config/RTK/logs/'):
                self.log_dir = _HOMEDIR + '/.config/RTK/logs/'
            else:
                self.log_dir = _LOGDIR

            if _util.dir_exists(_PROGDIR):
                self.prog_dir = _PROGDIR
            else:
                self.prog_dir = _HOMEDIR

            self._conf_file = self.conf_dir + 'RTK.conf'

            if not _util.file_exists(self._conf_file):
                self.create_default_configuration()

    def create_default_configuration(self):
        """
        Creates a default configuration file in the user's configuration
        directory.
        """

        import glob
        import shutil
        from os.path import basename

        config = ConfigParser.ConfigParser()

        if name == 'posix':
            _SITEDIR = '/etc/RTK/'
            _HOMEDIR = environ['HOME']

        elif name == 'nt':
            _SITEDIR = environ['COMMONPROGRAMFILES(X86)'] + '/RTK/'
            _HOMEDIR = environ['USERPROFILE']

        _PROGDIR = _HOMEDIR + '/analyses/rtk/'

        if basename(self._conf_file) == 'site.conf':
            dialog = _widg.make_dialog(_(u"RTK common database "
                                         u"information..."))

            fixed = _widg.make_fixed()

            y_pos = 10
            label = _widg.make_label(_(u"RTK common database host name:"),
                                     width=340)
            txtDBHost = _widg.make_entry()
            txtDBHost.set_text(_(u"localhost"))
            fixed.put(label, 5, y_pos)
            fixed.put(txtDBHost, 345, y_pos)
            y_pos += 30

            label = _widg.make_label(_(u"RTK common database socket:"),
                                     width=340)
            txtDBSocket = _widg.make_entry()
            txtDBSocket.set_text("3306")
            fixed.put(label, 5, y_pos)
            fixed.put(txtDBSocket, 345, y_pos)
            y_pos += 30

            label = _widg.make_label(_(u"RTK common database name:"),
                                     width=340)
            txtDBName = _widg.make_entry()
            txtDBName.set_text("RTKcom")
            fixed.put(label, 5, y_pos)
            fixed.put(txtDBName, 345, y_pos)
            y_pos += 30

            label = _widg.make_label(_(u"RTK common database user name:"),
                                     width=340)
            txtDBUser = _widg.make_entry()
            txtDBUser.set_text("RTKcom")
            fixed.put(label, 5, y_pos)
            fixed.put(txtDBUser, 345, y_pos)
            y_pos += 30

            label = _widg.make_label(_(u"RTK common database password:"),
                                     width=340)
            txtDBPassword = _widg.make_entry()
            txtDBPassword.set_invisible_char("*")
            txtDBPassword.set_visibility(False)
            txtDBPassword.set_text("RTKcom")
            fixed.put(label, 5, y_pos)
            fixed.put(txtDBPassword, 345, y_pos)
            y_pos += 30

            label = _widg.make_label(_(u"RTK common database type:"),
                                     width=340)
            cmbDBType = _widg.make_combo()
            _widg.load_combo(cmbDBType, [["mysql"], ["sqlite3"]])
            fixed.put(label, 5, y_pos)
            fixed.put(cmbDBType, 345, y_pos)

            fixed.show_all()
            dialog.vbox.pack_start(fixed)   # pylint: disable=E1101

            if dialog.run() == -3:
                RTKcomlist = []
                RTKcomlist.append(txtDBHost.get_text())
                try:
                    RTKcomlist.append(int(txtDBSocket.get_text()))
                except ValueError:
                    RTKcomlist.append(txtDBSocket.get_text())
                RTKcomlist.append(txtDBName.get_text())
                RTKcomlist.append(txtDBUser.get_text())
                RTKcomlist.append(txtDBPassword.get_text())
                RTKcomlist.append(cmbDBType.get_active_text())

            dialog.destroy()

            config.add_section('Modules')
            config.set('Modules', 'prediction', 'True')
            config.set('Modules', 'fmeca', 'True')
            config.set('Modules', 'maintainability', 'True')
            config.set('Modules', 'maintenance', 'True')
            config.set('Modules', 'fraca', 'True')

            config.add_section('Backend')
            config.set('Backend', 'host', RTKcomlist[0])
            config.set('Backend', 'socket', RTKcomlist[1])
            config.set('Backend', 'database', RTKcomlist[2])
            config.set('Backend', 'user', RTKcomlist[3])
            config.set('Backend', 'password', RTKcomlist[4])
            config.set('Backend', 'type', RTKcomlist[5])
            config.set('Backend', 'path', self.SITE_DIR)

        elif basename(self._conf_file) == 'RTK.conf':

            # Create the directories needed for the user.
            if not _util.dir_exists(self.conf_dir):
                makedirs(self.conf_dir)

            if not _util.dir_exists(_HOMEDIR + '/.config/RTK/data/'):
                makedirs(_HOMEDIR + '/.config/RTK/data/')

            if not _util.dir_exists(_HOMEDIR + '/.config/RTK/logs/'):
                makedirs(_HOMEDIR + '/.config/RTK/logs/')

            # Copy format files from _SITEDIR to the user's _CONFDIR.
            for _file in glob.glob(_SITEDIR + '*.xml'):
                shutil.copy(_file, self.conf_dir)

            # Copy SQL files from _SITEDIR to the user's _DATADIR.
            for _file in glob.glob(_SITEDIR + '/data/*.sql'):
                shutil.copy(_file, self.conf_dir + '/data/')

            # Copy the icons from _SITEDIR to the user's _CONFDIR.
            shutil.copytree(_SITEDIR + '/icons/', self.conf_dir + '/icons/')

            # Copy the common data base from _SITEDIR to the user's _CONFDIR.
            shutil.copy(_SITEDIR + '/rtkcom.rfb', self.conf_dir)

            # Create the default RTK configuration file.
            config.add_section('General')
            config.set('General', 'reportsize', 'letter')
            config.set('General', 'failtimeunit', 'hours')
            config.set('General', 'repairtimeunit', 'hours')
            config.set('General', 'frmultiplier', 1000000.0)
            config.set('General', 'calcreltime', 10.0)
            config.set('General', 'autoaddlistitems', 'False')
            config.set('General', 'decimal', 6)
            config.set('General', 'modesource', 1)
            config.set('General', 'parallelcalcs', 'False')
            config.set('General', 'treetabpos', 'top')
            config.set('General', 'listtabpos', 'bottom')
            config.set('General', 'booktabpos', 'bottom')

            config.add_section('Backend')
            config.set('Backend', 'type', 'sqlite3')
            config.set('Backend', 'host', 'localhost')
            config.set('Backend', 'socket', 3306)
            config.set('Backend', 'database', '')
            config.set('Backend', 'user', '')
            config.set('Backend', 'password', '')

            config.add_section('Directories')
            config.set('Directories', 'datadir', 'data')
            config.set('Directories', 'icondir', 'icons')
            config.set('Directories', 'logdir', 'log')
            config.set('Directories', 'progdir', 'analyses/rtk')

            config.add_section('Files')
            config.set('Files', 'datasetformat', 'dataset_format.xml')
            config.set('Files', 'fmecaformat', 'fmeca_format.xml')
            config.set('Files', 'ffmecaformat', 'ffmeca_format.xml')
            config.set('Files', 'sfmecaformat', 'sfmeca_format.xml')
            config.set('Files', 'functionformat', 'function_format.xml')
            config.set('Files', 'hardwareformat', 'hardware_format.xml')
            config.set('Files', 'incidentformat', 'incident_format.xml')
            config.set('Files', 'rgincidentformat', 'rgincident_format.xml')
            config.set('Files', 'partformat', 'part_format.xml')
            config.set('Files', 'requirementformat', 'requirement_format.xml')
            config.set('Files', 'revisionformat', 'revision_format.xml')
            config.set('Files', 'riskformat', 'risk_format.xml')
            config.set('Files', 'siaformat', 'sia_format.xml')
            config.set('Files', 'softwareformat', 'software_format.xml')
            config.set('Files', 'testformat', 'testing_format.xml')
            config.set('Files', 'validationformat', 'validation_format.xml')
            config.set('Files', 'rgformat', 'rgincident_format.xml')
            config.set('Files', 'fracaformat', 'incident_format.xml')
            config.set('Files', 'stakeholderformat', 'stakeholder_format.xml')
            config.set('Files', 'mechanismformat', 'incident_format.xml')

            config.add_section('Colors')
            config.set('Colors', 'revisionbg', '#FFFFFF')
            config.set('Colors', 'revisionfg', '#000000')
            config.set('Colors', 'functionbg', '#FFFFFF')
            config.set('Colors', 'functionfg', '#0000FF')
            config.set('Colors', 'requirementbg', '#FFFFFF')
            config.set('Colors', 'requirementfg', '#000000')
            config.set('Colors', 'assemblybg', '#FFFFFF')
            config.set('Colors', 'assemblyfg', '#000000')
            config.set('Colors', 'softwarebg', '#FFFFFF')
            config.set('Colors', 'softwarefg', '#000000')
            config.set('Colors', 'validationbg', '#FFFFFF')
            config.set('Colors', 'validationfg', '#00FF00')
            config.set('Colors', 'rgbg', '#FFFFFF')
            config.set('Colors', 'rgfg', '#000000')
            config.set('Colors', 'fracabg', '#FFFFFF')
            config.set('Colors', 'fracafg', '#000000')
            config.set('Colors', 'partbg', '#FFFFFF')
            config.set('Colors', 'partfg', '#000000')
            config.set('Colors', 'overstressbg', '#FF0000')
            config.set('Colors', 'overstressfg', '#FFFFFF')
            config.set('Colors', 'taggedbg', '#00FF00')
            config.set('Colors', 'taggedfg', '#FFFFFF')
            config.set('Colors', 'nofrmodelfg', '#A52A2A')

        try:
            parser = open(self._conf_file, 'w')
            config.write(parser)
            parser.close()
            return True

        except EnvironmentError:
            print _(u"Could not save your RTK configuration.")
            return False

    def write_configuration(self):
        """
        Writes changes to the user's configuration file.
        """

        if _util.file_exists(self._conf_file):
            config = ConfigParser.ConfigParser()
            config.add_section('General')
            config.set('General', 'reportsize', 'letter')
            config.set('General', 'repairtimeunit', 'hours')
            config.set('General', 'parallelcalcs', 'False')
            config.set('General', 'frmultiplier', FRMULT)
            config.set('General', 'failtimeunit', 'hours')
            config.set('General', 'calcreltime', RTK_MTIME)
            config.set('General', 'autoaddlistitems', 'False')
            config.set('General', 'decimal', PLACES)
            config.set('General', 'modesource', RTK_MODE_SOURCE)
            config.set('General', 'treetabpos', TABPOS[0])
            config.set('General', 'listtabpos', TABPOS[1])
            config.set('General', 'booktabpos', TABPOS[2])

            config.add_section('Backend')
            config.set('Backend', 'type', BACKEND)
            config.set('Backend', 'host', RTK_PROG_INFO[0])
            config.set('Backend', 'socket', RTK_PROG_INFO[1])
            config.set('Backend', 'database', '')
            config.set('Backend', 'user', RTK_PROG_INFO[3])
            config.set('Backend', 'password', RTK_PROG_INFO[4])

            config.add_section('Directories')
            config.set('Directories', 'datadir', 'data')
            config.set('Directories', 'icondir', 'icons')
            config.set('Directories', 'logdir', 'log')

            config.add_section('Files')
            config.set('Files', 'revisionformat',
                       path.basename(RTK_FORMAT_FILE[0]))
            config.set('Files', 'functionformat',
                       path.basename(RTK_FORMAT_FILE[1]))
            config.set('Files', 'requirementformat',
                       path.basename(RTK_FORMAT_FILE[2]))
            config.set('Files', 'hardwareformat',
                       path.basename(RTK_FORMAT_FILE[3]))
            config.set('Files', 'validationformat',
                       path.basename(RTK_FORMAT_FILE[4]))
            config.set('Files', 'rgformat',
                       path.basename(RTK_FORMAT_FILE[5]))
            config.set('Files', 'fracaformat',
                       path.basename(RTK_FORMAT_FILE[6]))
            config.set('Files', 'partformat',
                       path.basename(RTK_FORMAT_FILE[7]))
            config.set('Files', 'siaformat',
                       path.basename(RTK_FORMAT_FILE[8]))
            config.set('Files', 'fmecaformat',
                       path.basename(RTK_FORMAT_FILE[9]))
            config.set('Files', 'stakeholderformat',
                       path.basename(RTK_FORMAT_FILE[10]))
            config.set('Files', 'testformat',
                       path.basename(RTK_FORMAT_FILE[11]))
            config.set('Files', 'mechanismformat',
                       path.basename(RTK_FORMAT_FILE[12]))
            config.set('Files', 'rgincidentformat',
                       path.basename(RTK_FORMAT_FILE[13]))
            config.set('Files', 'incidentformat',
                       path.basename(RTK_FORMAT_FILE[14]))
            config.set('Files', 'softwareformat',
                       path.basename(RTK_FORMAT_FILE[15]))
            config.set('Files', 'datasetformat',
                       path.basename(RTK_FORMAT_FILE[16]))
            config.set('Files', 'riskformat',
                       path.basename(RTK_FORMAT_FILE[17]))

            config.add_section('Colors')
            config.set('Colors', 'revisionbg', RTK_COLORS[0])
            config.set('Colors', 'revisionfg', RTK_COLORS[1])
            config.set('Colors', 'functionbg', RTK_COLORS[2])
            config.set('Colors', 'functionfg', RTK_COLORS[3])
            config.set('Colors', 'requirementbg', RTK_COLORS[4])
            config.set('Colors', 'requirementfg', RTK_COLORS[5])
            config.set('Colors', 'assemblybg', RTK_COLORS[6])
            config.set('Colors', 'assemblyfg', RTK_COLORS[7])
            config.set('Colors', 'validationbg', RTK_COLORS[8])
            config.set('Colors', 'validationfg', RTK_COLORS[9])
            config.set('Colors', 'rgbg', RTK_COLORS[10])
            config.set('Colors', 'rgfg', RTK_COLORS[11])
            config.set('Colors', 'fracabg', RTK_COLORS[12])
            config.set('Colors', 'fracafg', RTK_COLORS[13])
            config.set('Colors', 'partbg', RTK_COLORS[14])
            config.set('Colors', 'partfg', RTK_COLORS[15])
            config.set('Colors', 'overstressbg', RTK_COLORS[16])
            config.set('Colors', 'overstressfg', RTK_COLORS[17])
            config.set('Colors', 'taggedbg', RTK_COLORS[18])
            config.set('Colors', 'taggedfg', RTK_COLORS[19])
            config.set('Colors', 'nofrmodelfg', RTK_COLORS[20])
            config.set('Colors', 'softwarebg', RTK_COLORS[21])
            config.set('Colors', 'softwarefg', RTK_COLORS[22])

            try:
                parser = open(self._conf_file, 'w')
                config.write(parser)
                parser.close()
            except EnvironmentError:
                print _(u"Could not save your RTK configuration.")

    def read_configuration(self):
        """
        Reads the user's configuration file.
        """

        # Try to read the user's configuration file.  If it doesn't exist,
        # create a new one.  If those options fail, read the system-wide
        # configuration file and keep going.
        if _util.file_exists(self._conf_file):
            config = ConfigParser.ConfigParser()
            config.read(self._conf_file)
        else:
            config = None

        return config
