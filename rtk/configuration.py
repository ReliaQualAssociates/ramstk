#!/usr/bin/env python
"""
This file contains configuration information and functions for RTK.
"""

__author__ = 'Andrew Rowland <andrew.rowland@reliaqual.com>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       configuration.py is part of The RTK Project
#
# All rights reserved.

import ConfigParser
from os import environ, path, mkdir, name

# Add localization support.
import locale
import gettext
_ = gettext.gettext

# Import other RTK modules.
import utilities as _util
import widgets as _widg

# Path to the directory containing icon files used by RTK.  Defaults to
# /usr/share/pixmaps/RTK/ on POSIX systems.
ICON_DIR = ''

# Path to the directory containing data files used by RTK.  Defaults to
# /usr/share/RTK/ on POSIX systems.
DATA_DIR = ''

# Path to the directory containing configuration files used by RTK.
# Defaults to $HOME/.config/RTK/ on POSIX systems.
# Defaults to C:\\Users\<USER NAME>\config\RTK\ on NT systems.
CONF_DIR = ''

# Path to the directory containing log files used by RTK.
# Defaults to $HOME/.config/RTK/logs/ on POSIX systems.
# Defaults to C:\\Users\<USER NAME>\config\RTK\logs\ on NT systems.
LOG_DIR = ''

# Global list containing the path to the format files to use for various
# widgets.
#
#    Position 00: Revision Tree formatting.
#    Position 01: Function Tree formatting.
#    Position 02: Requirements Tree formatting.
#    Position 03: Hardware Tree formatting.
#    Position 04: Validation Tree formatting.
#    Position 05: Reliability Growth Tree formatting.
#    Position 06: Field Incidents List formatting.
#    Position 07: Parts List formatting.
#    Position 08: Similar Item Analysis formatting.
#    Position 09: FMECA worksheet formatting.
#    Position 10:  formatting.
#    Position 11: Test Planning List formatting.
#    Position 12:  formatting.
#    Position 13:  formatting.
#    Position 14:  formatting.
#    Position 15: Software Tree formatting.
#    Position 16: Dataset Tree formatting.
#    Position 17: Risk Analysis formatting.
RTK_FORMAT_FILE = []

# Global list containing the colors to use for various widgets.
#
#    Position 00: Revision row background color
#    Position 01: Revision row foreground color
#    Position 02: Function row background color
#    Position 03: Function row foreground color
#    Position 04: Requirement row background color
#    Position 05: Requirement row foreground color
#    Position 06: Assembly row background color
#    Position 07: Assembly row foreground color
#    Position 08: Validation row background color
#    Position 09: Validation row foreground color
#    Position 10: Reliability Testing row background color
#    Position 11: Reliability Testing row foreground color
#    Position 12: Program Incident row background color
#    Position 13: Program Incident row foreground color
# Dataset row background color
# Dataset row foreground color
#    Position 14: Part List row background color
#    Position 15: Part List row foreground color
#    Position 16: Overstressed Part row background color
#    Position 17: Overstressed Part row foreground color
#    Position 18: Tagged Part row background color
#    Position 19: Tagged Part row foreground color
#    Position 20: Part with no failure rate model row foreground color
RTK_COLORS = []

# Global variable list to house information about the prefix and next index
# to use when adding new revisions, functions, assemblies, parts,
# FMECA items, FMECA modes, FMECA effects, and FMECA causes.
#
#    Position 00: Revision prefix
#    Position 01: Next revision index
#    Position 02: Function prefix
#    Position 03: Next function index
#    Position 04: Assembly prefix
#    Position 05: Next assembly index
#    Position 06: Part prefix
#    Position 07: Next part index
#    Position 08: FMECA item prefix
#    Position 09: Next FMECA item index
#    Position 10: FMECA mode prefix
#    Position 11: Next FMECA mode index
#    Position 12: FMECA effect prefix
#    Position 13: NExt FMECA effect index
#    Position 14: FMECA cause prefix
#    Position 15: Next FMECA cause index
#    Position 16: Software prefix
#    Position 17: Next Software prefix
RTK_PREFIX = []

# Global list to house information about the active modules.
#    1 = active, 0 = inactive.
#
#    Position 00: Revision module status
#    Position 01: Requirements module status
#    Position 02: Function module status
#    Position 03: Hardware module status
#    Position 04: Software module status
#    Position 05: Validation module status
#    Position 06: Testing module status
#    Position 07: Maintenance Policy module status
#    Position 08: Field Incidents module status
#    Position 09: FMECA module status
#    Position 10: Survival Analysis module status
#    Position 11: RBD module status
#    Position 12: FTA module status
RTK_MODULES = []
RTK_PAGE_NUMBER = []

# Global list for MySQL or SQLite3 connection information to the common
# database.
#
#    Position 00: Host name
#    Position 01: Host port
#    Position 02: Database name
#    Position 03: User name
#    Position 04: User password
RTK_COM_INFO = []

# Global list for
RTK_RISK_POINTS = [3, 9]

# Global list for MySQL or SQLite3 connection information to the Program
# database.
#
#    Position 00: Host name
#    Position 01: Host port
#    Position 02: Database name
#    Position 03: User name
#    Position 04: User password
RTK_PROG_INFO = []

# Variables to hold the backend database type for the program and common
# database.
BACKEND = ''
COM_BACKEND = ''

# Variables to support native language support.
LOCALE = 'en_US'

OS = ''

# Variables to control the display of numerical information.
FRMULT = 1.0
PLACES = 6
MTIME = 100.0

# Variables to control GUI options.
TABPOS = ['top', 'bottom', 'bottom']

# Variables to hold various control parameters.
METHOD= 'STANDARD'                          # STANDARD or LRM
FMECA = 0                                   # 0=qualitative, 1=quantitative CA

class RTKConf:
    """ The RTK configuration class. """

    def __init__(self, level='site'):
        """
        Initializes the RTK configuration parser.

        Keyword Arguments:
        level -- indicates which configuration file is to be read.
                 One of 'site' or 'user'.
        """

        if(name == 'posix'):
            self.OS = 'Linux'
            _SITEDIR = '/etc/RTK/'
            _DATADIR = '/usr/share/RTK/'
            _ICONDIR = '/usr/share/pixmaps/RTK/'
            _LOGDIR = '/var/log/RTK/'
            _HOMEDIR = environ['HOME']

        elif(name == 'nt'):
            self.OS = 'Windows'
            _HOMEDIR = environ['USERPROFILE']
            _DATADIR = _HOMEDIR + '/.config/RTK/'
            _SITEDIR = _HOMEDIR + '/.config/RTK/'
            _ICONDIR = _HOMEDIR + '/.config/RTK/icons/'
            _LOGDIR = _HOMEDIR + '/.config/RTK/logs/'

        if(level == 'site'):
            if(_util.dir_exists(_SITEDIR)):
                self.conf_dir = _SITEDIR
            else:
                self.conf_dir = _HOMEDIR + '/.config/RTK/'

            if(_util.dir_exists(_DATADIR)):
                self.data_dir = _DATADIR
            else:
                self.data_dir = _HOMEDIR + '/.config/RTK/data/'

            if(_util.dir_exists(_ICONDIR)):
                self.icon_dir = _ICONDIR
            else:
                self.icon_dir = _HOMEDIR + '/.config/RTK/icons'

            if(_util.dir_exists(_LOGDIR)):
                self.log_dir = _LOGDIR
            else:
                self.log_dir = _HOMEDIR + '/.config/RTK/logs/'

            self._conf_file = self.conf_dir + '/site.conf'

        elif(level == 'user'):
            self.conf_dir = _HOMEDIR + '/.config/RTK/'

            if(_util.dir_exists(_DATADIR)):
                self.data_dir = _DATADIR
            else:
                self.data_dir = _HOMEDIR + '/.config/RTK/data/'

            if(_util.dir_exists(_ICONDIR)):
                self.icon_dir = _ICONDIR
            else:
                self.icon_dir = _HOMEDIR + '/.config/RTK/icons'

            if(_util.dir_exists(_LOGDIR)):
                self.log_dir = _LOGDIR
            else:
                self.log_dir = _HOMEDIR + '/.config/RTK/logs/'

            self._conf_file = self.conf_dir + 'RTK.conf'

        if not _util.file_exists(self._conf_file):
            self.create_default_configuration()

    def create_default_configuration(self):
        """
        Creates a default configuration file in the user's configuration
        directory.
        """
        from os.path import basename

        if(_util.dir_exists(self.conf_dir)):

            config = ConfigParser.ConfigParser()

            if(basename(self._conf_file) == 'site.conf'):
                dialog = _widg.make_dialog(_(u"RTK common database information..."))

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
                y_pos += 30

                fixed.show_all()
                dialog.vbox.pack_start(fixed)
                response = dialog.run()

                if(response == -3):
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

            elif(basename(self._conf_file) == 'RTK.conf'):
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
                config.set('Files', 'rgincidentformat', 'rgincident_format.xml')
                config.set('Files', 'partformat', 'part_format.xml')
                config.set('Files', 'requirementformat', 'requirement_format.xml')
                config.set('Files', 'revisionformat', 'revision_format.xml')
                config.set('Files', 'riskformat', 'risk_format.xml')
                config.set('Files', 'siaformat', 'sia_format.xml')
                config.set('Files', 'softwareformat', 'software_format.xml')
                config.set('Files', 'testformat', 'testing_format.xml')
                config.set('Files', 'validationformat', 'validation_format.xml')
# TODO: Remove the following format files from RTK.
                config.set('Files', 'rgformat', 'rgincident_format.xml')
                config.set('Files', 'fracaformat', 'incident_format.xml')
                config.set('Files', 'modeformat', 'incident_format.xml')
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
        """ Writes changes to the user's configuration file. """

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

# =========================================================================== #
# The following writes to the Files section.  This is the section containing
# the list of files describing the format of the various gtk.TreeView used in
# the application.
#
#       Position        Tree to Format
#           0           Revision Tree
#           1           Function Tree
#           2           Requirements Tree
#           3           Hardware Tree
#           4           Validation Tree
#           5           Parts List
#           8           Similar Item Analysis
#           9           FMECA worksheet
#          10           Failure Modes List
#          11           Failure Effects List
#          12           Failure Mechanisms List
# =========================================================================== #
            config.add_section('Files')
            config.set('Files', 'revisionformat', path.basename(RTK_FORMAT_FILE[0]))
            config.set('Files', 'functionformat', path.basename(RTK_FORMAT_FILE[1]))
            config.set('Files', 'requirementformat', path.basename(RTK_FORMAT_FILE[2]))
            config.set('Files', 'hardwareformat', path.basename(RTK_FORMAT_FILE[3]))
            config.set('Files', 'validationformat', path.basename(RTK_FORMAT_FILE[4]))
            config.set('Files', 'rgformat', path.basename(RTK_FORMAT_FILE[5]))
            config.set('Files', 'fracaformat', path.basename(RTK_FORMAT_FILE[6]))
            config.set('Files', 'partformat', path.basename(RTK_FORMAT_FILE[7]))
            config.set('Files', 'siaformat', path.basename(RTK_FORMAT_FILE[8]))
            config.set('Files', 'fmecaformat', path.basename(RTK_FORMAT_FILE[9]))
            config.set('Files', 'modeformat', path.basename(RTK_FORMAT_FILE[10]))
            config.set('Files', 'testformat', path.basename(RTK_FORMAT_FILE[11]))
            config.set('Files', 'mechanismformat', path.basename(RTK_FORMAT_FILE[12]))
            config.set('Files', 'rgincidentformat', path.basename(RTK_FORMAT_FILE[13]))
            config.set('Files', 'incidentformat', path.basename(RTK_FORMAT_FILE[14]))
            config.set('Files', 'softwareformat', path.basename(RTK_FORMAT_FILE[15]))
            config.set('Files', 'datasetformat', path.basename(RTK_FORMAT_FILE[16]))
            config.set('Files', 'riskformat', path.basename(RTK_FORMAT_FILE[17]))

# =========================================================================== #
# The following write to the Colors section.  This is the section containing
# the forground (text) and background color of the cells in the various
# gtk.TreeView used in the application.
#
#       Position        Tree to Color
#           0           Revision Tree background color
#           1           Revision Tree foreground color
#           2           Function Tree background color
#           3           Function Tree foreground color
#           4           Requirement Tree background color
#           5           Requirement Tree foreground color
#           6           Assembly Tree background color
#           7           Assembly Tree foreground color
#           8           Validation Tree background color
#           9           Validation Tree foreground color
#          10           Reliability Growth Tree background color
#          11           Reliability Growth Tree foreground color
#          12           Field Incident Tree background color
#          13           Field Incident Tree foreground color
#          14           Part List Tree background color
#          15           Part List Tree foreground color
#          16           Overstressed Part Tree background color
#          17           Overstressed Part Tree foreground color
#          18           Tagged Part Tree background color
#          19           Tagged Part Tree foreground color
#          20           Part with no failure rate model row foreground color
# =========================================================================== #
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
                parser = open(self._conf_file,'w')
                config.write(parser)
                parser.close()
            except EnvironmentError:
                print _("Could not save your RTK configuration.")

    def read_configuration(self):
        """ Reads the user's configuration file. """

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
            print _("There is a problem with your configuration file. Please, remove %s.") % self._conf_file
