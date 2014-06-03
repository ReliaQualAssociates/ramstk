#!/usr/bin/env python
"""
This file contains configuration information and functions for RTK.
"""

__author__ = 'Andrew Rowland <andrew.rowland@reliaqual.com>'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       configuration.py is part of The RTK Project
#
# All rights reserved.

import ConfigParser
from os import environ, path, mkdir, name

# Add localization support.
import gettext
_ = gettext.gettext

# Import other RTK modules.
import utilities as _util
import widgets as _widg

MODE = ''
""" Sets the mode of operation.  Defaults to '' for user-mode.  Will be set to
'developer' when devmode is passed as a CLI argument.  The 'developer' mode is
used during testing and enables the use of built-in test cases."""

ICON_DIR = ''
""" Path to the directory containing icon files used by RTK.\n
Defaults to /usr/share/pixmaps/RTK/ on POSIX systems."""

DATA_DIR = ''
""" Path to the directory containing data files used by RTK.\n
Defaults to /usr/share/RTK/ on POSIX systems."""

CONF_DIR = ''
""" Path to the directory containing configuration files used by RTK.\n
Defaults to $HOME/.config/RTK/ on POSIX systems.\n
Defaults to C:\\Users\<USER NAME>\config\RTK\ on NT systems."""

LOG_DIR = ''
""" Path to the directory containing log files used by RTK.\n
Defaults to $HOME/.config/RTK/logs/ on POSIX systems.\n
Defaults to C:\\Users\<USER NAME>\config\RTK\logs\ on NT systems."""

PROG_DIR = ''
""" Path to the base directory containing RTK Program database files.  This is
only used when the backend is SQLite3.\n
Defaults to $HOME/analyses/rtk on POSIX systems.\n
Defaults to C:\\Users\<USER NAME>\analyses\rtk\ on NT systems."""

RTK_FORMAT_FILE = []
""" Global list containing the path to the format files to use for various
widgets.\n\n

Position  Tree Format\n
    0     Revision Tree\n
    1     Function Tree\n
    2     Requirements Tree\n
    3     Hardware Tree\n
    4     Validation Tree\n
    5     Reliability Growth Tree\n
    6     Field Incidents List\n
    7     Parts List\n
    8     Similar Item Analysis\n
    9     Hardware FMECA\n
   10     Stakeholder Input\n
   11     Test Planning List\n
   12     Future Use\n
   13     Future Use\n
   14     Future Use\n
   15     Software Tree\n
   16     Dataset Tree\n
   17     Risk Analysis\n
   18     Functional FMECA\n
   19     Software FMECA"""

RTK_COLORS = []
""" Global list containing the colors to use for various widgets.\n\n

Position    Tree Color\n
    0       Revision Tree background\n
    1       Revision Tree foreground\n
    2       Function Tree background\n
    3       Function Tree foreground\n
    4       Requirement Tree background\n
    5       Requirement Tree foreground\n
    6       Hardware Tree background\n
    7       Hardware Tree foreground\n
    8       Validation Tree background\n
    9       Validation Tree foreground\n
   10       Reliability Testing Tree background\n
   11       Reliability Testing Tree foreground\n
   12       Program Incident Tree background\n
   13       Program Incident Tree foreground\n
   14       Dataset Tree background color\n
   15       Dataset Tree foreground color\n
   16       Part List Tree background\n
   17       Part List Tree foreground\n
   18       Overstressed Part background\n
   19       Overstressed Part foreground\n
   20       Tagged Part background\n
   21       Tagged Part foreground\n
   22       Part with no failure rate model foreground"""

RTK_PREFIX = []
""" Global variable list to house information about the prefix and next index
to use when adding new revisions, functions, assemblies, parts, FMECA items,
FMECA modes, FMECA effects, and FMECA causes.\n\n

Position    Index/Prefix\n
    0       Revision prefix\n
    1       Next Revision index\n
    2       Function prefix\n
    3       Next Function index\n
    4       Hardware prefix\n
    5       Next Hardware index\n
    6       Part prefix\n
    7       Next Part index\n
    8       FMECA item prefix\n
    9       Next FMECA item index\n
   10       FMECA mode prefix\n
   11       Next FMECA mode index\n
   12       FMECA effect prefix\n
   13       Next FMECA effect index\n
   14       FMECA cause prefix\n
   15       Next FMECA cause index\n
   16       Software prefix\n
   17       Next Software index"""

RTK_MODULES = []
""" Global list to house information about the active modules.  Where
1 = active and 0 = inactive.\n\n

Position    Module Status\n
    0       Revision\n
    1       Function\n
    2       Requirements\n
    3       Hardware\n
    4       Software\n
    5       Validation\n
    6       Testing\n
    7       Incidents\n
    8       Dataset\n
    9       FMECA\n
   10       RCM\n
   11       RBD\n
   12       FTA"""

RTK_PAGE_NUMBER = []

RTK_COM_INFO = []
""" Global list for the RTK common database connection information.\n\n

Position    Information\n
    0       Host name (MySQL only)\n
    1       Host port (MySQL only)\n
    2       Database name\n
    3       User name (MySQL only)\n
    4       User password (MySQL only)"""

RTK_PROG_INFO = []
""" Global list for RTK Program database connection information.\n\n

Position    Information\n
    0       Host name (MySQL only)\n
    1       Host port (MySQL only)\n
    2       Database name\n
    3       User name (MySQL only)\n
    4       User password (MySQL only)"""

RTK_RISK_POINTS = [4, 10]
""" Global list for risk level cutoffs.\n\n

Index   Risk Level Cutoff Value\n
  0     Low to medium\n
  1     Medium to high"""

# Variables to hold the backend database type for the program and common
# database.
COM_BACKEND = ''
""" RTK common database backend to use; mysql or sqlite3."""
BACKEND = ''
""" RTK Program database backend to use; mysql or sqlite3."""

# Variables to support native language support.
LOCALE = 'en_US'
""" The language locale to use with RTK."""
OS = ''
""" The operating system RTK is currently running on."""

# Variables to control the display of numerical information.
FRMULT = 1.0
""" The failure rate multiplier.  All failure rates will be multiplied by this
value for display.  This allows failure rates to display without using
scientific notation."""
PLACES = 6
""" Number of decimal places to show in numerical results."""
MTIME = 100.0
""" The default mission time for new RTK Programs."""

# Variables to control GUI options.
TABPOS = ['top', 'bottom', 'bottom']
""" Location of tabs in the three main gtk.Notebook() widgets.\n\n
Index   Notebook\n
  0     Module Book\n
  1     Work Book\n
  2     List Book"""

# Variables to hold various control parameters.
METHOD = 'STANDARD'                         # STANDARD or LRM
FMECA = 0                                   # 0=qualitative, 1=quantitative CA


class RTKConf(object):
    """
    The RTK configuration class.
    """

    def __init__(self, level='site'):
        """
        Initializes the RTK configuration parser.

        @param level: indicates which configuration file is to be read.
                      One of 'site' or 'user'.
        @type level: string
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
            _DATADIR = _HOMEDIR + '/.config/RTK/'
            _SITEDIR = _HOMEDIR + '/.config/RTK/'
            _ICONDIR = _HOMEDIR + '/.config/RTK/icons/'
            _LOGDIR = _HOMEDIR + '/.config/RTK/logs/'
            _PROGDIR = _HOMEDIR + '/analyses/rtk/'

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

            self._conf_file = self.conf_dir + '/site.conf'

        elif level == 'user':
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

        from os.path import basename

        if _util.dir_exists(self.conf_dir):

            config = ConfigParser.ConfigParser()

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

            elif basename(self._conf_file) == 'RTK.conf':
                config.add_section('General')
                config.set('General', 'reportsize', 'letter')
                config.set('General', 'failtimeunit', 'hours')
                config.set('General', 'repairtimeunit', 'hours')
                config.set('General', 'frmultiplier', 1000000.0)
                config.set('General', 'calcreltime', 100.0)
                config.set('General', 'autoaddlistitems', 'False')
                config.set('General', 'decimal', 6)
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

                config.add_section('Files')
                config.set('Files', 'datasetformat', 'dataset_format.xml')
                config.set('Files', 'fmecaformat', 'fmeca_format.xml')
                config.set('Files', 'functionformat', 'function_format.xml')
                config.set('Files', 'hardwareformat', 'hardware_format.xml')
                config.set('Files', 'incidentformat', 'incident_format.xml')
                config.set('Files', 'rgincidentformat',
                           'rgincident_format.xml')
                config.set('Files', 'partformat', 'part_format.xml')
                config.set('Files', 'requirementformat',
                           'requirement_format.xml')
                config.set('Files', 'revisionformat', 'revision_format.xml')
                config.set('Files', 'riskformat', 'risk_format.xml')
                config.set('Files', 'siaformat', 'sia_format.xml')
                config.set('Files', 'softwareformat', 'software_format.xml')
                config.set('Files', 'testformat', 'testing_format.xml')
                config.set('Files', 'validationformat',
                           'validation_format.xml')
# TODO: Remove the following format files from RTK.
                config.set('Files', 'rgformat', 'rgincident_format.xml')
                config.set('Files', 'fracaformat', 'incident_format.xml')
                config.set('Files', 'stakeholderformat',
                           'stakeholder_format.xml')
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

                print _("RTK default configuration created.")
                return True
            except EnvironmentError:
                print _("Could not save your RTK configuration.")
                return False

        else:
            try:
                mkdir(self.conf_dir)
                print _("RTK configuration directory (%s) created.") % \
                    self.conf_dir
                mkdir(self.data_dir)
                print _("RTK data directory (%s) created.") % \
                    self.data_dir
                mkdir(self.log_dir)
                print _("RTK log file directory (%s) created.") % \
                    self.log_dir
                mkdir(self.icon_dir)
                print _("RTK icon directory (%s) created.") % \
                    self.icon_dir
                self.__init__()
            except EnvironmentError:
                print _("Could not create RTK default configuration.")

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
            config.set('General', 'calcreltime', MTIME)
            config.set('General', 'autoaddlistitems', 'False')
            config.set('General', 'decimal', PLACES)
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

            try:
                parser = open(self._conf_file, 'w')
                config.write(parser)
                parser.close()
            except EnvironmentError:
                print _("Could not save your RTK configuration.")

    def read_configuration(self):
        """
        Reads the user's configuration file.
        """

        # Try to read the user's configuration file.  If it doesn't exist,
        # create a new one.  If those options fail, read the system-wide
        # configuration file and keep going.
        try:
            if _util.file_exists(self._conf_file):
                config = ConfigParser.ConfigParser()
                config.read(self._conf_file)
                return config
            else:
                self.create_default_configuration()
                self.read_configuration()
        except:
            _util.rtk_error(_(u"There is a problem with your configuration "
                              u"file. Please, remove %s.") % self._conf_file)
