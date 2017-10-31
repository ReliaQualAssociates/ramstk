#!/usr/bin/env python
"""
This file contains configuration information and methods for RTK.
"""
# -*- coding: utf-8 -*-
#
#       rtk.Configuration.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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


class Configuration(object):
    """
    The RTK configuration class.  Class attributes of the Configuration class
    are:

    :cvar dict RTK_FORMAT_FILE: Dictionary containing the path to the format
                                files to use for various widgets.  Keys for
                                this dictionary are:

                                * revision
                                * function
                                * requirement
                                * hardware
                                * software
                                * incident
                                * validation
                                * testing
                                * part
                                * sia
                                * fmeca
                                * rgincident
                                * stakeholder
                                * dataset
                                * risk
                                * ffmeca
                                * sfmeca

    :cvar dict RTK_COLORS: Dictionary containing the colors to use for various
                           widgets.  Keys for this dictionary are:

                           * revisionbg - Revision Tree background
                           * revisionfg - Revision Tree foreground
                           * functionbg - Function Tree background
                           * functionfg - Function Tree foreground
                           * requirementbg - Requirement Tree background
                           * requirementfg - Requirement Tree foreground
                           * assemblybg - Hardware Tree background for
                             assemblies
                           * assemblyfg - Hardware Tree foreground for
                             assemblies
                           * partbg - Part List Tree background
                           * partfg - Part List Tree foreground
                           * overstressbg - Overstressed Part background
                           * overstressfg - Overstressed Part foreground
                           * taggedbg - Tagged Part background
                           * taggedfg - Tagged Part foreground
                           * nofrmodelfg - Part with no failure rate model
                             foreground
                           * softwarebg - Software Tree background color
                           * softwarefg - Software Tree foreground color
                           * validationbg - Validation Tree background
                           * validationfg - Validation Tree foreground
                           * testbg - Reliability Testing Tree background
                           * testfg - Reliability Testing Tree foreground
                           * incidentbg - Program Incident Tree background
                           * incidentfg - Program Incident Tree foreground
                           * survivalbg - Dataset Tree background color
                           * survivalfg - Dataset Tree foreground color
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
    :cvar dict RTK_FAILURE_PROBABILITY: Dictionary for qualitative failure
                                        probability categories.
    :cvar dict RTK_SEVERITY: Dictionary for failure severity categories.
    :cvar dict RTK_HAZARDS: Dictionary for potential hazards.
    :cvar dict RTK_REQUIREMENT_TYPES: Dictionary of requirement types.
    :cvar dict RTK_RPN_SEVERITY: Dictionary for RPN Severity categories.
    :cvar dict RTK_RPN_OCCURRENCE: Dictionary for RPN Occurrence categories.
    :cvar dict RTK_RPN_DETECTION: Dictionary for RPN Detection categories.

    :cvar list RTK_PREFIX: List of prefixes to use for each RTK module.
                           Prefixes in the list are:

                           +-------+---------------------------+
                           | Index | Next Prefix               |
                           +=======+===========================+
                           |   0   | Revision prefix           |
                           +-------+---------------------------+
                           |   1   | Function prefix           |
                           +-------+---------------------------+
                           |   2   | Hardware prefix           |
                           +-------+---------------------------+
                           |   3   | Part prefix               |
                           +-------+---------------------------+
                           |   4   | FMECA item prefix         |
                           +-------+---------------------------+
                           |   5   | FMECA mode prefix         |
                           +-------+---------------------------+
                           |   6   | FMECA effect prefix       |
                           +-------+---------------------------+
                           |   7   | FMECA cause prefix        |
                           +-------+---------------------------+
                           |   8   | Software prefix           |
                           +-------+---------------------------+

    :cvar list RTK_MODULES: List to of active modules in the open RTK Program
                            database.  Where 1 = active and 0 = inactive.

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

    :cvar int RTK_FMECA_METHOD: Indicator variable for the criticality method
                                used.  Available methods are:

                                1. MIL-STD-216A, Task 102
                                2. Risk Priority Number (RPN)

    :cvar int RTK_RPN_FORMAT: Indicator variable for the level that the RPN is
                              calculated.  Available levels are:

                              0. Mechanism
                              1. Cause

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
    RTK_TABPOS = {'listbook': 'top', 'modulebook': 'bottom',
                  'workbook': 'bottom'}

    RTK_ACTION_CATEGORY = {}
    RTK_INCIDENT_CATEGORY = {}
    RTK_SEVERITY = {}
    RTK_ACTIVE_ENVIRONMENTS = {}
    RTK_DORMANT_ENVIRONMENTS = {}
    RTK_SW_DEV_ENVIRONMENTS = {}
    RTK_AFFINITY_GROUPS = {}
    RTK_WORKGROUPS = {}
    RTK_FAILURE_PROBABILITY = {}
    RTK_SW_LEVELS = {}
    RTK_DETECTION_METHODS = {}
    RTK_SW_TEST_METHODS = {}
    RTK_ALLOCATION_MODELS = {}
    RTK_DAMAGE_MODELS = {}
    RTK_HR_MODEL = {}
    RTK_LIFECYCLE = {}
    RTK_SW_DEV_PHASES = {}
    RTK_RPN_DETECTION = {}
    RTK_RPN_SEVERITY = {}
    RTK_RPN_OCCURRENCE = {}
    RTK_ACTION_STATUS = {}
    RTK_INCIDENT_STATUS = {}
    RTK_COST_TYPE = {}
    RTK_HR_TYPE = {}
    RTK_INCIDENT_TYPE = {}
    RTK_MTTR_TYPE = {}
    RTK_REQUIREMENT_TYPE = {}
    RTK_VALIDATION_TYPE = {}
    RTK_SW_APPLICATION = {}
    RTK_CATEGORIES = {}
    RTK_CRITICALITY = {}
    RTK_FAILURE_MODES = {}                      # Default failure modes.
    RTK_HAZARDS = {}
    RTK_MANUFACTURERS = {}
    RTK_MEASUREMENT_UNITS = {}
    RTK_OPERATING_PARAMETERS = {}  # TODO: Add table to common db for this.
    RTK_S_DIST = {}
    RTK_STAKEHOLDERS = {}
    RTK_SUBCATEGORIES = {}
    RTK_USERS = {}
    RTK_PREFIX = {}
    RTK_MODULES = {}
    RTK_PAGE_NUMBER = {}

    # Define public list class attributes.
    RTK_CONTROL_TYPES = []
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
    RTK_FMECA_METHOD = 1  # 1=Task 102, 2=RPN
    RTK_RPN_FORMAT = 0  # RPN at mechanism level.
    RTK_COM_BACKEND = ''
    RTK_BACKEND = ''
    RTK_HR_MULTIPLIER = 1000000.0
    RTK_DEC_PLACES = 6
    RTK_MTIME = 10.0
    RTK_GUI_LAYOUT = 'advanced'
    RTK_METHOD = 'STANDARD'  # STANDARD or LRM
    RTK_LOCALE = 'en_US'
    RTK_OS = ''

    def __init__(self):
        """
        Method to initialize the RTK configuration parser.
        """

        self._lst_colors = ['revisionfg', 'functionfg', 'requirementfg',
                            'assemblyfg', 'partfg', 'overstressfg', 'taggedfg',
                            'nofrmodelfg', 'softwarefg', 'incidentfg',
                            'validationfg', 'testfg', 'survivalfg',
                            'revisionbg', 'functionbg', 'requirementbg',
                            'assemblybg', 'partbg', 'overstressbg', 'taggedbg',
                            'softwarebg', 'incidentbg', 'validationbg',
                            'testbg', 'survivalbg']
        self._lst_format_files = ['revision', 'function', 'requirement',
                                  'hardware', 'software', 'incident',
                                  'validation', 'testing', 'part', 'sia',
                                  'fmeca', 'rgincident', 'stakeholder',
                                  'dataset', 'risk', 'ffmeca', 'sfmeca']
        if name == 'posix':
            self.RTK_OS = 'Linux'
            self.RTK_SITE_DIR = '/etc/RTK'
            self.RTK_HOME_DIR = environ['HOME']
            self.RTK_DATA_DIR = '/usr/share/RTK'
            self.RTK_ICON_DIR = '/usr/share/pixmaps/RTK'
            self.RTK_LOG_DIR = '/var/log/RTK'
            self.RTK_PROG_DIR = self.RTK_HOME_DIR + '/analyses/rtk'
            self.RTK_CONF_DIR = ''

        elif name == 'nt':
            self.RTK_OS = 'Windows'
            self.RTK_SITE_DIR = environ['COMMONPROGRAMFILES(X86)'] + '/RTK/'
            self.RTK_HOME_DIR = environ['USERPROFILE']
            self.RTK_DATA_DIR = self.RTK_SITE_DIR + 'data/'
            self.RTK_ICON_DIR = self.RTK_SITE_DIR + 'icons/'
            self.RTK_LOG_DIR = self.RTK_SITE_DIR + 'logs/'
            self.RTK_PROG_DIR = self.RTK_HOME_DIR + '/analyses/rtk/'
            self.RTK_CONF_DIR = ''

    def set_site_variables(self):
        """
        Method to set the site configuration variables.

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

        self.RTK_SITE_CONF = self.RTK_CONF_DIR + '/site.conf'

        if not Utilities.file_exists(self.RTK_SITE_CONF):
            self._create_site_configuration()

        self._read_site_configuration()

        return False

    def set_user_variables(self):
        """
        Method to set the user-specific configuration variables.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.RTK_PROG_CONF = self.RTK_CONF_DIR + '/RTK.conf'

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
        _config.set('Backend', 'type', 'sqlite')

        try:
            _parser = open(self.RTK_SITE_CONF, 'w')
            _config.write(_parser)
            _parser.close()

        except EnvironmentError:
            _return = True

        return _return

    def create_user_configuration(self):
        """
        Method to create the default user configuration file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        import glob
        from distutils import dir_util, file_util

        _return = False

        _config = ConfigParser.ConfigParser()

        # Create the directories needed for the user.  Always prefer the RTK
        # directories in the user's $HOME over the system-wide directories.
        # Configuration directory.
        if not Utilities.dir_exists(self.RTK_HOME_DIR + '/.config/RTK'):
            try:
                makedirs(self.RTK_HOME_DIR + '/.config/RTK')
                self.RTK_CONF_DIR = self.RTK_HOME_DIR + '/.config/RTK'
            except OSError:
                pass

        # Data directory.
        if not Utilities.dir_exists(self.RTK_HOME_DIR + '/.config/RTK/data'):
            try:
                makedirs(self.RTK_HOME_DIR + '/.config/RTK/data')
                self.RTK_DATA_DIR = self.RTK_HOME_DIR + '/.config/RTK/data'
            except OSError:
                pass

        # Icon directory.
        if not Utilities.dir_exists(self.RTK_HOME_DIR + '/.config/RTK/icons'):
            try:
                makedirs(self.RTK_HOME_DIR + '/.config/RTK/icons')
                self.RTK_ICON_DIR = self.RTK_HOME_DIR + '/.config/RTK/icons'
            except OSError:
                pass

        # Log directory.
        if not Utilities.dir_exists(self.RTK_HOME_DIR + '/.config/RTK/logs'):
            try:
                makedirs(self.RTK_HOME_DIR + '/.config/RTK/logs')
                self.RTK_LOG_DIR = self.RTK_HOME_DIR + '/.config/RTK/logs'
            except OSError:
                pass

        # Program directory.
        if not Utilities.dir_exists(self.RTK_HOME_DIR + '/analyses/RTK'):
            try:
                makedirs(self.RTK_HOME_DIR + '/analyses/RTK')
                self.RTK_PROG_DIR = self.RTK_HOME_DIR + '/analyses/RTK'
            except OSError:
                pass

        # Copy format files from RTK_SITE_DIR (system) to the user's
        # RTK_CONF_DIR.
        for _file in glob.glob(self.RTK_SITE_DIR + '/*.xml'):
            file_util.copy_file(_file, self.RTK_CONF_DIR)

        # Copy the icons from RTK_SITE_DIR (system) to the user's RTK_ICON_DIR.
        try:
            dir_util.copy_tree(self.RTK_SITE_DIR + '/icons/',
                               self.RTK_ICON_DIR)
        except IOError:
            print self.RTK_CONF_DIR

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
        _config.set('Files', 'dataset', 'dataset_format.xml')
        _config.set('Files', 'fmeca', 'fmeca_format.xml')
        _config.set('Files', 'ffmeca', 'ffmeca_format.xml')
        _config.set('Files', 'sfmeca', 'sfmeca_format.xml')
        _config.set('Files', 'function', 'function_format.xml')
        _config.set('Files', 'hardware', 'hardware_format.xml')
        _config.set('Files', 'incident', 'incident_format.xml')
        _config.set('Files', 'rgincident', 'rgincident_format.xml')
        _config.set('Files', 'part', 'part_format.xml')
        _config.set('Files', 'requirement', 'requirement_format.xml')
        _config.set('Files', 'revision', 'revision_format.xml')
        _config.set('Files', 'risk', 'risk_format.xml')
        _config.set('Files', 'sia', 'sia_format.xml')
        _config.set('Files', 'software', 'software_format.xml')
        _config.set('Files', 'stakeholder', 'stakeholder_format.xml')
        _config.set('Files', 'testing', 'testing_format.xml')
        _config.set('Files', 'validation', 'validation_format.xml')

        _config.add_section('Colors')
        _config.set('Colors', 'revisionbg', '#FFFFFF')
        _config.set('Colors', 'revisionfg', '#000000')
        _config.set('Colors', 'functionbg', '#FFFFFF')
        _config.set('Colors', 'functionfg', '#0000FF')
        _config.set('Colors', 'requirementbg', '#FFFFFF')
        _config.set('Colors', 'requirementfg', '#000000')
        _config.set('Colors', 'assemblybg', '#FFFFFF')
        _config.set('Colors', 'assemblyfg', '#000000')
        _config.set('Colors', 'partbg', '#FFFFFF')
        _config.set('Colors', 'partfg', '#000000')
        _config.set('Colors', 'overstressbg', '#FF0000')
        _config.set('Colors', 'overstressfg', '#FFFFFF')
        _config.set('Colors', 'taggedbg', '#00FF00')
        _config.set('Colors', 'taggedfg', '#FFFFFF')
        _config.set('Colors', 'nofrmodelfg', '#A52A2A')
        _config.set('Colors', 'softwarebg', '#FFFFFF')
        _config.set('Colors', 'softwarefg', '#000000')
        _config.set('Colors', 'validationbg', '#FFFFFF')
        _config.set('Colors', 'validationfg', '#00FF00')
        _config.set('Colors', 'testbg', '#FFFFFF')
        _config.set('Colors', 'testfg', '#000000')
        _config.set('Colors', 'incidentbg', '#FFFFFF')
        _config.set('Colors', 'incidentfg', '#000000')
        _config.set('Colors', 'survivalbg', '#FFFFFF')
        _config.set('Colors', 'survivalfg', '#000000')

        try:
            _parser = open(self.RTK_PROG_CONF, 'w')
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

        if Utilities.file_exists(self.RTK_PROG_CONF):
            _config = ConfigParser.ConfigParser()
            _config.add_section('General')
            _config.set('General', 'reportsize', 'letter')
            _config.set('General', 'repairtimeunit', 'hours')
            _config.set('General', 'parallelcalcs', 'False')
            _config.set('General', 'frmultiplier', self.RTK_HR_MULTIPLIER)
            _config.set('General', 'failtimeunit', 'hours')
            _config.set('General', 'calcreltime', self.RTK_MTIME)
            _config.set('General', 'autoaddlistitems', 'False')
            _config.set('General', 'decimal', self.RTK_DEC_PLACES)
            _config.set('General', 'modesource', self.RTK_MODE_SOURCE)
            _config.set('General', 'treetabpos', self.RTK_TABPOS['modulebook'])
            _config.set('General', 'listtabpos', self.RTK_TABPOS['listbook'])
            _config.set('General', 'booktabpos', self.RTK_TABPOS['workbook'])

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

    def _read_site_configuration(self):
        """
        Method to read the site configuration file.

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

    def read_configuration(self):
        """
        Method to read the configuration file.

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

            self.RTK_HR_MULTIPLIER = _config.get('General', 'frmultiplier')
            self.RTK_DEC_PLACES = _config.get('General', 'decimal')
            self.RTK_MTIME = _config.get('General', 'calcreltime')
            self.RTK_MODE_SOURCE = _config.get('General', 'modesource')
            self.RTK_TABPOS['listbook'] = _config.get('General', 'listtabpos')
            self.RTK_TABPOS['modulebook'] = _config.get('General',
                                                        'treetabpos')
            self.RTK_TABPOS['workbook'] = _config.get('General', 'booktabpos')

        else:
            _return = True

        return _return
