#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.RTK.py is part of the RTK Project
#
# All rights reserved.

"""
This is the main program for the RTK application.
"""

import datetime
import gettext
import glob
import logging
import os
import shutil
import sys

from sqlalchemy.orm import scoped_session
from pubsub import pub

try:
    import pygtk

    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)

# Import other RTK modules.
import Configuration
import Utilities
from dao.DAO import DAO
from dao.RTKCommonDB import SiteSession, ProgSession
from datamodels.matrix.Matrix import Matrix
from revision.Revision import Revision
from usage.UsageProfile import UsageProfile
from failure_definition.FailureDefinition import FailureDefinition
from function.Function import Function
from analyses.fmea.FMEA import FMEA
from requirement.Requirement import Requirement
from stakeholder.Stakeholder import Stakeholder
from hardware.BoM import BoM as HardwareBoM
from analyses.allocation.Allocation import Allocation
from analyses.hazard.Hazard import Hazard
from analyses.similar_item.SimilarItem import SimilarItem
from analyses.pof.PhysicsOfFailure import PoF
from software.BoM import BoM as SoftwareBoM
from testing.Testing import Testing
from testing.growth.Growth import Growth
from validation.Validation import Validation
from incident.Incident import Incident
from incident.action.Action import Action
from incident.component.Component import Component
# from survival.Survival import Survival

import gui.gtk.Widgets as Widgets
from gui.gtk.mwi.ListBook import ListView
from gui.gtk.mwi.ModuleBook import ModuleView
from gui.gtk.mwi.WorkBook import WorkView

from revision.ModuleBook import ModuleView as mvwRevision
from function.ModuleBook import ModuleView as mvwFunction
from requirement.ModuleBook import ModuleView as mvwRequirement
from hardware.ModuleBook import ModuleView as mvwHardware
from software.ModuleBook import ModuleView as mvwSoftware
from testing.ModuleBook import ModuleView as mvwTesting
from incident.ModuleBook import ModuleView as mvwIncident
from validation.ModuleBook import ModuleView as mvwValidation
from survival.ModuleBook import ModuleView as mvwSurvival

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2016 Andrew "weibullguy" Rowland'

# Add localization support.
_ = gettext.gettext


def main():
    """
    This is the main function for the RTK application.
    """

    # splScreen = SplashScreen()

    # If you don't do this, the splash screen will show, but wont render it's
    # contents
    # while gtk.events_pending():
    #     gtk.main_iteration()

    # sleep(3)
    RTK()

    # splScreen.window.destroy()

    gtk.main()

    return 0


def _read_site_configuration():
    """
    Function to read the site configuration file.

    :return: (_error_code, _msg); the error code and associated error message.
    :rtype: (int, str)
    """

    _error_code = 0
    _msg = 'RTK SUCCESS: Parsing site configuration file.'

    if os.name == 'posix':
        Configuration.RTK_OS = 'Linux'
    elif os.name == 'nt':
        Configuration.RTK_OS = 'Windows'

        # Set the gtk+ theme on Windows.
        # These themes perform well on Windows.
        # Amaranth
        # Aurora
        # Bluecurve
        # Blueprint
        # Blueprint-Green
        # Candido-Calm
        # CleanIce
        # CleanIce - Dark
        # Clearlooks
        # Metal
        # MurrinaBlue
        # Nodoka-Midnight
        # Rezlooks-Snow

        # These themes perform poorly.
        # Bluecurve-BerriesAndCream
        # MurrinaChrome
        gtk.rc_parse(
            "C:\\Program Files (x86)\\Common Files\\RTK\\share\\themes\\MurrinaBlue\\gtk-2.0\\gtkrc")

    # Get a config instance for the site configuration file.
    _config = Configuration.RTKConf('site')
    if not Utilities.file_exists(_config.conf_file):
        _error_code = 100
        _msg = _(u"Site configuration file {0:s} not found.  This typically "
                 u"indicates RTK was installed improperly or RTK files have "
                 u"been corrupted.  You may try to uninstall and re-install "
                 u"RTK.").format(_config.conf_file)
    else:
        Configuration.RTK_COM_BACKEND = \
            _config.read_configuration().get('Backend', 'type')
        Configuration.RTK_SITE_DIR = \
            _config.read_configuration().get('Backend', 'path')

        Configuration.RTK_COM_INFO['host'] = \
            _config.read_configuration().get('Backend', 'host')
        Configuration.RTK_COM_INFO['socket'] = \
            _config.read_configuration().get('Backend', 'socket')
        Configuration.RTK_COM_INFO['database'] = \
            _config.read_configuration().get('Backend', 'database')
        Configuration.RTK_COM_INFO['user'] = \
            _config.read_configuration().get('Backend', 'user')
        Configuration.RTK_COM_INFO['password'] = \
            _config.read_configuration().get('Backend', 'password')

    return _error_code, _msg


def _read_program_configuration():
    """
    Function to read the program configuration file.

    :return: (_error_code, _msg); the error code and associated error message.
    :rtype: (int, str)
    """

    _error_code = 0
    _msg = 'RTK SUCCESS: Parsing program configuration file.'

    _homedir = None

    _lst_format_files = ['revision', 'function', 'requirement', 'hardware',
                         'software', 'incident', 'validation', 'test', 'part',
                         'sia', 'fmeca', 'rgincident', 'stakeholder',
                         'dataset', 'risk', 'ffmeca', 'sfmeca']
    _lst_bg_colors = ['revisionbg', 'functionbg', 'requirementbg',
                      'hardwarebg', 'partbg', 'overstressbg', 'taggedbg',
                      'softwarebg', 'incidentbg', 'validationbg', 'testbg',
                      'survivalbg']
    _lst_fg_colors = ['revisionfg', 'functionfg', 'requirementfg',
                      'hardwarefg', 'partfg', 'overstressfg', 'taggedfg',
                      'nofrmodelfg', 'softwarefg', 'incidentfg',
                      'validationfg', 'testfg', 'survivalfg']

    if os.name == 'posix':
        _homedir = os.environ['HOME']
    elif os.name == 'nt':
        _homedir = os.environ['USERPROFILE']

    # Get a config instance for the user configuration file.
    _config = Configuration.RTKConf('user')

    Configuration.RTK_BACKEND = _config.read_configuration().get('Backend',
                                                                 'type')
    Configuration.RTK_PROG_INFO['host'] = \
        _config.read_configuration().get('Backend', 'host')
    Configuration.RTK_PROG_INFO['socket'] = \
        _config.read_configuration().get('Backend', 'socket')
    Configuration.RTK_PROG_INFO['database'] = \
        _config.read_configuration().get('Backend', 'database')
    Configuration.RTK_PROG_INFO['user'] = \
        _config.read_configuration().get('Backend', 'user')
    Configuration.RTK_PROG_INFO['password'] = \
        _config.read_configuration().get('Backend', 'password')

    Configuration.RTK_HR_MULTIPLIER = float(
            _config.read_configuration().get('General', 'frmultiplier'))
    Configuration.RTK_DEC_PLACES = _config.read_configuration().get('General',
                                                                    'decimal')
    Configuration.RTK_MODE_SOURCE = \
        _config.read_configuration().get('General', 'modesource')
    Configuration.RTK_TABPOS['listbook'] = \
        _config.read_configuration().get('General', 'listtabpos')
    Configuration.RTK_TABPOS['modulebook'] = \
        _config.read_configuration().get('General', 'treetabpos')
    Configuration.RTK_TABPOS['workbook'] = \
        _config.read_configuration().get('General', 'booktabpos')

    # Get directory and file information.
    _datadir = _config.read_configuration().get('Directories', 'datadir')
    _icondir = _config.read_configuration().get('Directories', 'icondir')
    _logdir = _config.read_configuration().get('Directories', 'logdir')
    _progdir = _config.read_configuration().get('Directories', 'progdir')

    Configuration.CONF_DIR = _config.conf_dir
    if not Utilities.dir_exists(Configuration.CONF_DIR):
        _error_code = 101
        _msg = _(u"Configuration directory {0:s} does not exist.  "
                 u"Creating...").format(Configuration.CONF_DIR)
        os.makedirs(Configuration.CONF_DIR)
        for _file in glob.glob(Configuration.SITE_DIR + '*.conf'):
            shutil.copy2(_file, Configuration.CONF_DIR)
        for _file in glob.glob(Configuration.SITE_DIR + '*.xml'):
            shutil.copy2(_file, Configuration.CONF_DIR)
        shutil.copy2(Configuration.SITE_DIR + '/RTKCommon.rtk',
                     Configuration.CONF_DIR)

    Configuration.DATA_DIR = Configuration.CONF_DIR + _datadir + '/'
    if not Utilities.dir_exists(Configuration.DATA_DIR):
        _error_code = 105
        _msg = _(u"Data directory {0:s} does not exist.  "
                 u"Creating...").format(Configuration.DATA_DIR)
        os.makedirs(Configuration.DATA_DIR)
        for _file in glob.glob(Configuration.data_dir + '*.map'):
            shutil.copy2(_file, Configuration.DATA_DIR)
        for _file in glob.glob(Configuration.data_dir + '*.sql'):
            shutil.copy2(_file, Configuration.DATA_DIR)

    Configuration.ICON_DIR = Configuration.CONF_DIR + _icondir + '/'
    if not Utilities.dir_exists(Configuration.ICON_DIR):
        _error_code = 105
        _msg = _(u"Icon directory {0:s} does not exist.  "
                 u"Creating...").format(Configuration.ICON_DIR)
        os.makedirs(Configuration.ICON_DIR)
        shutil.copytree(Configuration.icon_dir, Configuration.ICON_DIR,
                        symlinks=True)

    Configuration.LOG_DIR = Configuration.CONF_DIR + _logdir + '/'
    if not Utilities.dir_exists(Configuration.LOG_DIR):
        _error_code = 105
        _msg = _(u"Log directory {0:s} does not exist.  "
                 u"Creating...").format(Configuration.LOG_DIR)
        os.makedirs(Configuration.LOG_DIR)

    Configuration.PROG_DIR = _progdir
    if not Utilities.dir_exists(Configuration.PROG_DIR):
        _error_code = 105
        _msg = _(u"RTK Project directory {0:s} does not exist.  Using default "
                 u"RTK Project directory "
                 u"{1:s}.").format(Configuration.PROG_DIR,
                                   _homedir + '/analyses/rtk/')
        Configuration.PROG_DIR = _homedir + '/analyses/rtk/'
        if not Utilities.dir_exists(Configuration.PROG_DIR):
            os.makedirs(Configuration.PROG_DIR)

    # Load dictionary of format files.
    for _format_file in _lst_format_files:
        _formatfile = _config.read_configuration().get('Files', _format_file)
        _formatfile = Configuration.CONF_DIR + _formatfile
        Configuration.RTK_FORMAT_FILE[_format_file] = _formatfile

    # Load dictionary with background color information.
    for _bg_color in _lst_bg_colors:
        try:
            _bgcolor = _config.read_configuration().get('Colors', _bg_color)
            Configuration.RTK_COLORS[_bg_color] = _bgcolor
        except NoOptionError:
            Configuration.RTK_COLORS[_bg_color] = '#FFFFFF'

    # Load dictionary with foreground colors.
    for _fg_color in _lst_fg_colors:
        try:
            _fgcolor = _config.read_configuration().get('Colors', _fg_color)
            Configuration.RTK_COLORS[_fg_color] = _fgcolor
        except NoOptionError:
            Configuration.RTK_COLORS[_fg_color] = '#000000'

    return _error_code, _msg


def _initialize_loggers():
    """
    Function to create loggers for the RTK application.

    :return: (_debug_log, _user_log, _import_log)
    :rtype: tuple
    """

    # Create loggers for the application.  The first is to store log
    # information for RTK developers.  The second is to log errors for the
    # user.  The user can use these errors to help find problems with their
    # inputs and sich.
    __user_log = Configuration.RTK_LOG_DIR + '/RTK_user.log'
    __error_log = Configuration.RTK_LOG_DIR + '/RTK_debug.log'
    __import_log = Configuration.RTK_LOG_DIR + '/RTK_import.log'

    if not Utilities.dir_exists(Configuration.RTK_LOG_DIR):
        os.makedirs(Configuration.RTK_LOG_DIR)

    if Utilities.file_exists(__user_log):
        os.remove(__user_log)
    if Utilities.file_exists(__error_log):
        os.remove(__error_log)
    if Utilities.file_exists(__import_log):
        os.remove(__import_log)

    _debug_log = Utilities.create_logger("RTK.debug", logging.DEBUG,
                                         __error_log)
    _user_log = Utilities.create_logger("RTK.user", logging.WARNING,
                                        __user_log)
    _import_log = Utilities.create_logger("RTK.import", logging.WARNING,
                                          __import_log)

    return _debug_log, _user_log, _import_log


class NoOptionError(Exception):
    """
    Exception raised when no option is available in the configuration file.
    """

    pass


class Model(object):
    """
    This is the RTK data model class.  The attributes of a RTK data model are:

    :ivar site_dao:
    :ivar program_dao:
    """

    def __init__(self, sitedao, programdao):
        """
        Method to initialize an instance of the RTK data model.

        :param sitedao: the `:py:class:rtk.dao.DAO.DAO` instance connected to
                        the RTK Common database.
        :param programdao: the `:py:class:rtk.dao.DAO.DAO` instance connected
                           to the RTK Program database.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.site_dao = sitedao
        self.program_dao = programdao

        # Connect to the RTK Common database.
        _database = None
        if Configuration.RTK_COM_INFO['type'] == 'sqlite':
            _database = Configuration.RTK_COM_INFO['type'] + ':///' + \
                        Configuration.RTK_COM_INFO['database']
        self.site_dao.db_connect(_database)

        site_session = SiteSession
        program_session = ProgSession

        site_session.configure(bind=self.site_dao.engine, autoflush=False,
                               expire_on_commit=False)
        self.site_session = scoped_session(site_session)
        self.site_dao.db_load_globals(self.site_session)

        program_session.configure(bind=self.program_dao.engine,
                                  autoflush=False, expire_on_commit=False)
        self.program_session = scoped_session(program_session)

    def create_program(self):
        """
        Method to create a new RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _session = scoped_session(ProgSession)
        _session.configure(bind=self.program_dao.engine,
                           autoflush=False, expire_on_commit=False)

        if Configuration.RTK_PROG_INFO['type'] == 'sqlite':
            _database = Configuration.RTK_PROG_INFO['type'] + ':///' + \
                        Configuration.RTK_PROG_INFO['database']

        if not self.program_dao.db_create_program(_session):
            Configuration.RTK_USER_LOG.info('RTK SUCCESS: Creating RTK '
                                            'Program database {0:s}.'. \
                                            format(_database))
            pub.sendMessage('createdProgram')
        else:
            _return = True
            Configuration.RTK_DEBUG_LOG.error('RTK ERROR: Failed to create '
                                              'RTK Program database {0:s}.'. \
                                              format(_database))

        _session.close()

        return _return

    def open_program(self):
        """
        Method to open an RTK Program database for analyses.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if Configuration.RTK_PROG_INFO['type'] == 'sqlite':
            _database = Configuration.RTK_PROG_INFO['type'] + ':///' + \
                        Configuration.RTK_PROG_INFO['database']

        if not self.program_dao.db_connect(_database):
            Configuration.RTK_USER_LOG.info('RTK SUCCESS: Opening RTK ' 
                                            'Program database {0:s}.'. \
                                            format(_database))
            pub.sendMessage('openedProgram')
        else:
            _return = True
            Configuration.RTK_DEBUG_LOG.error('RTK ERROR: Failed to open ' 
                                              'RTK Program database {0:s}.'. \
                                              format(_database))

        return _return

    def close_program(self):
        """
        Method to close the open RTK Program database.
        """

        self.program_dao.db_close()

        pub.sendMessage('closedProgram')

        return

    def save_program(self):
        """
        Method to save the open RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code, _msg = self.program_dao.db_update(self.program_session)

        if _error_code == 0:
            pub.sendMessage('savedProgram')

        return _error_code, _msg

    def delete_program(self):
        """
        Method to delete an existing RTK Program database.

        :return:
        """

        pass


class RTK(object):
    """
    Class representing the RTK data controller.  This is the master controller
    for the entire RTK application.  Attributes of an RTK data controller are:

    :ivar dict dic_controllers: dictionary of data controllers available in the
                                running instance of RTK.

                                Keys are:
                                    'revision'
                                    'function'
                                    'requirement'
                                    'hardware'
                                    'software'
                                    'test'
                                    'validation'
                                    'incident'
                                    'survival'
                                    'matrices'
                                    'profile'
                                    'definition'
                                    'fmea'
                                    'stakeholder'
                                    'allocation'
                                    'hazard'
                                    'similaritem'
                                    'pof'
                                    'growth'
                                    'action'
                                    'component'
                                Values are the instance of each RTK data
                                controller.

    :ivar dict dic_books: dictionary of GUI books used by the running instance
                          of RTK.

                          Keys are:
                              'listbook'
                              'modulebook'
                              'workbook'
                          Values are the instance of each RTK book.

    :ivar rtk_model: the instance of `:py:class:rtk.RTK.Model` managed by this
                     data controller.
    """

    def __init__(self):  # pylint: disable=R0914
        """
        Method to initialize an instance of the RTK data controller.
        """

        RTK_INTERFACE = 1

        # Read the site configuration file.
        _error_code, _msg = _read_site_configuration()
        # if _error_code != 0:

        # Read the program configuration file.
        _error_code, _msg = _read_program_configuration()
        # if _error_code != 0:

        # Create loggers.
        (Configuration.RTK_DEBUG_LOG,
         Configuration.RTK_USER_LOG,
         Configuration.RTK_IMPORT_LOG) = _initialize_loggers()

        # Validate the license.
        # if self._validate_license():
        #    sys.exit(2)

        # Initialize private dictionary instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dictionary instance attributes.
        self.dic_controllers = {'revision'   : None,
                                'function'   : None,
                                'requirement': None,
                                'hardware'   : None,
                                'software'   : None,
                                'test'       : None,
                                'validation' : None,
                                'incident'   : None,
                                'survival'   : None,
                                'matrices'   : None,
                                'profile'    : None,
                                'definition' : None,
                                'fmea'       : None,
                                'stakeholder': None,
                                'allocation' : None,
                                'hazard'     : None,
                                'similaritem': None,
                                'pof'        : None,
                                'growth'     : None,
                                'action'     : None,
                                'component'  : None}
        self.dic_books = {'listview'  : None,
                          'moduleview': None,
                          'workview'  : None}

        # Define public list attributes.

        # Define public scalar attributes.
        _database = Configuration.RTK_COM_INFO['database']
        self.rtk_model = Model(DAO(_database), DAO(None))

        # Create RTK Books.  These need to be initialized after reading the
        # configuration.
        if RTK_INTERFACE == 0:  # Single window.
            pass
        else:  # Multiple windows.
            self.dic_books['listview'] = ListView()
            self.dic_books['moduleview'] = ModuleView(self)
            self.dic_books['workview'] = WorkView()

        # Subscribe this controller to RTK control messages.
        pub.subscribe(self.request_open_program, 'createdProgram')

    def request_create_program(self):
        """
        Method to request a new RTK Program database be created.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self.rtk_model.create_program()

    def request_open_program(self):
        """
        Method to request an RTK Program database be opened for analyses.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        # If the database was successfully opened, create an instance of each
        # of the slave data controllers.
        if not self.rtk_model.open_program():
            # self.dic_controllers['revision'] = Revision()
            # self.dic_controllers['function'] = Function()
            # self.dic_controllers['requirement'] = Requirement()
            # self.dic_controllers['hardware'] = HardwareBoM()
            # self.dic_controllers['software'] = SoftwareBoM()
            # self.dic_controllers['test'] = Test()
            # self.dic_controllers['validation'] = Validation()
            # self.dic_controllers['incident'] = Incident()
            # self.dic_controllers['survival'] = Survival()

            # self.dic_controllers['matrices'] = Matrix()
            # self.dic_controllers['profile'] = UsageProfile()
            # self.dic_controllers['definition'] = FailureDefinition()
            # self.dic_controllers['fmea'] = FMEA()
            # self.dic_controllers['stakeholder'] = Stakeholder()
            # self.dic_controllers['allocation'] = Allocation()
            # self.dic_controllers['hazard'] = Hazard()
            # self.dic_controllers['similaritem'] = SimilarItem()
            # self.dic_controllers['pof'] = PoF()
            # self.dic_controllers['growth'] = Growth()
            # self.dic_controllers['action'] = Action()
            # self.dic_controllers['component'] = Component()
            pass
        else:
            _return = True

        return _return

    def request_close_program(self):
        """
        Method to request the open RTK Program database be closed.
        """

        return self.rtk_model.close_program()

    def request_save_program(self):
        """
        Method to request the open RTK Program database be saved.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        return self.rtk_model.save_program()

    def __del__(self):
        del self

    def _validate_license(self):
        """
        Method to validate the license and the license expiration date.

        :return: False if successful or true if an error is encountered.
        :rtype: bool
        """

        # Read the license file and compare to the product key in the site
        # database.  If they are not equal, quit the application.
        _license_file = Configuration.DATA_DIR + '/license.key'
        try:
            _license_file = open(_license_file, 'r')
        except IOError:
            Widgets.rtk_warning(_(u"Cannot find license file {0:s}.  If your "
                                  u"license file is elsewhere, please place "
                                  u"it in {1:s}.").format(
                    _license_file, Configuration.DATA_DIR))
            return True

        _license_key = _license_file.readline().rstrip('\n')
        _license_file.close()

        _query = "SELECT fld_product_key, fld_expire_date \
                  FROM tbl_site_info"
        (_results, _error_code, __) = self.site_dao.execute(_query, None)

        if _license_key != _results[0][0]:
            Widgets.rtk_error(_(u"Invalid license (Invalid key).  Your "
                                u"license key is incorrect.  Closing the RTK "
                                u"application."))
            return True

        if datetime.datetime.today().toordinal() > _results[0][1]:
            _expire_date = str(datetime.datetime.fromordinal(int(
                    _results[0][1])).strftime('%Y-%m-%d'))
            Widgets.rtk_error(_(u"Invalid license (Expired).  Your license "
                                u"expired on {0:s}.  Closing the RTK "
                                u"application.").format(_expire_date))
            return True

        return False

    def open_project(self):
        """
        Method to open an RTK Project database and load it into the views.
        """

        _message = _(u"Opening Program Database {0:s}"). \
            format(Configuration.RTK_PROG_INFO[2])
        self.module_book.statusbar.push(2, _message)

        # Connect to the project database.
        self.project_dao = DAO('')
        self.project_dao.db_connect('sqlite:///' +
                                    Configuration.RTK_PROG_INFO[2])
        # self.project_dao.execute("PRAGMA foreign_keys=ON", commit=False)

        # Set the data access object for each data controller.
        self.mvwRevision.load_revision_tree(self.project_dao)

        self.dtcMatrices.dao = self.project_dao
        self.dtcRevision.dao = self.project_dao
        self.dtcProfile.dao = self.project_dao
        self.dtcDefinitions.dao = self.project_dao
        self.dtcFunction.dao = self.project_dao
        self.dtcFMEA.dao = self.project_dao
        self.dtcRequirement.dao = self.project_dao
        self.dtcStakeholder.dao = self.project_dao
        self.dtcHardwareBoM.dao = self.project_dao
        self.dtcAllocation.dao = self.project_dao
        self.dtcHazard.dao = self.project_dao
        self.dtcSimilarItem.dao = self.project_dao
        # self.dtcPoF.dao = self.project_dao
        # self.dtcSoftwareBoM.dao = self.project_dao
        # self.dtcTesting.dao = self.project_dao
        # self.dtcGrowth.dao = self.project_dao
        # self.dtcValidation.dao = self.project_dao
        # self.dtcIncident.dao = self.project_dao
        # self.dtcAction.dao = self.project_dao
        # self.dtcComponent.dao = self.project_dao
        # self.dtcSurvival.dao = self.project_dao

        # Get a connection to the program database and then retrieve the
        # program information.
        _query = "SELECT fld_revision_prefix, fld_revision_next_id, \
                         fld_function_prefix, fld_function_next_id, \
                         fld_assembly_prefix, fld_assembly_next_id, \
                         fld_part_prefix, fld_part_next_id, \
                         fld_fmeca_prefix, fld_fmeca_next_id, \
                         fld_mode_prefix, fld_mode_next_id, \
                         fld_effect_prefix, fld_effect_next_id, \
                         fld_cause_prefix, fld_cause_next_id, \
                         fld_software_prefix, fld_software_next_id \
                  FROM tbl_program_info"
        (_results, _error_code, __) = self.project_dao.execute(_query,
                                                               commit=False)
        Configuration.RTK_PREFIX = [_element for _element in _results[0]]

        _icon = Configuration.ICON_DIR + '32x32/db-connected.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        self.icoStatus.set_from_pixbuf(_icon)
        self.icoStatus.set_tooltip(_(u"RTK is connected to program database "
                                     u"{0:s}.".format(
                Configuration.RTK_PROG_INFO[2])))
        self.module_book.set_title(_(u"RTK - Analyzing {0:s}".format(
                Configuration.RTK_PROG_INFO[2])))

        # Find which modules are active in this project.
        _query = "SELECT fld_revision_active, fld_function_active, \
                         fld_requirement_active, fld_hardware_active, \
                         fld_software_active, fld_vandv_active, \
                         fld_testing_active, fld_fraca_active, \
                         fld_survival_active, fld_rcm_active, \
                         fld_rbd_active, fld_fta_active\
                  FROM tbl_program_info"
        (_results, _error_code, __) = self.project_dao.execute(_query,
                                                               commit=False)

        # For the active RTK modules, load the data.  For the RTK modules
        # that aren't active in the project, remove the page from the
        # RTK Module view.
        i = 0
        for _module in _results[0]:
            if _module == 1 and i < len(Configuration.RTK_MODULES):
                self.module_book.load_module_page(Configuration.RTK_MODULES[i])
                if i == 0:
                    self.revision_id = min(
                        self.dtcRevision.dicRevisions.keys())
                Configuration.RTK_PAGE_NUMBER.append(i)
            else:
                self.module_book.notebook.remove_page(i)
            i += 1

        # Configuration.METHOD = results[0][36]

        self.module_book.statusbar.pop(2)

        self.loaded = True

        return False

    def save_project(self):
        """
        Method to save the entire RTK Project to the open RTK Project database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if not self.loaded:
            return True

        _message = _(u"Saving Program "
                     u"Database {0:s}".format(Configuration.RTK_PROG_INFO[2]))
        self.module_book.statusbar.push(2, _message)

        self.dtcRevision.save_all_revisions()
        self.dtcRequirement.save_all_requirements()
        self.dtcStakeholder.save_all_inputs()
        self.dtcFunction.save_all_functions()
        self.dtcHardwareBoM.save_bom()
        self.dtcSoftwareBoM.save_bom()
        self.dtcSurvival.save_all_survivals()
        self.dtcGrowth.save_all_tests()
        self.dtcValidation.save_all_tasks()

        # Save everything that is revision-specific for each revision.
        for _revision_id in self.dtcRevision.dicRevisions.keys():
            self.dtcDefinitions.save_definitions(_revision_id)
            self.dtcProfile.save_profile(_revision_id)

        # Update the next ID for each type of object.
        _query = "UPDATE tbl_program_info \
                  SET fld_revision_next_id={0:d}, fld_function_next_id={1:d}, \
                      fld_assembly_next_id={2:d}, fld_part_next_id={3:d}, \
                      fld_fmeca_next_id={4:d}, fld_mode_next_id={5:d}, \
                      fld_effect_next_id={6:d}, fld_cause_next_id={7:d}, \
                      fld_software_next_id={8:d} \
                  WHERE fld_program_id={9:d}".format(
                Configuration.RTK_PREFIX[1], Configuration.RTK_PREFIX[3],
                Configuration.RTK_PREFIX[5], Configuration.RTK_PREFIX[7],
                Configuration.RTK_PREFIX[9],
                Configuration.RTK_PREFIX[11],
                Configuration.RTK_PREFIX[13],
                Configuration.RTK_PREFIX[15],
                Configuration.RTK_PREFIX[17], 1)
        self.project_dao.execute(_query, commit=True)

        _query = "VACUUM"
        self.project_dao.execute(_query, commit=False)

        self.module_book.statusbar.pop(2)

        return False

    def close_project(self):
        """
        Method to close the currently open RTK Project database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _moduleview in Configuration.RTK_MODULES:
            _moduleview.treeview.get_model().clear()

        self.project_dao.close()

        _icon = Configuration.ICON_DIR + '32x32/db-disconnected.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        self.icoStatus.set_from_pixbuf(_icon)
        self.icoStatus.set_tooltip(_(u"RTK is not currently connected to a "
                                     u"project database."))

        self.loaded = False

        return False

    def load_revision(self, revision_id):
        """
        Method to load the active RTK module data whenever a new Revision is
        selected.

        :param int revision_id: the ID of the Revision to load data for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.revision_id = revision_id

        for _moduleview in Configuration.RTK_MODULES[1:]:
            self.module_book.load_module_page(_moduleview)

        return False


if __name__ == '__main__':
    main()
