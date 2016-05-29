#!/usr/bin/env python
"""
This is the main program for the RTK application.
"""

# -*- coding: utf-8 -*-
#
#       rtk.RTK.py is part of the RTK Project
#
# All rights reserved.

import datetime
import gettext
import logging
import os
import sys

try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)

from gui.gtk.mwi.ModuleBook import ModuleView

import Configuration
import Utilities
import gui.gtk.Widgets as Widgets

from dao.DAO import DAO
from datamodels.matrix.Matrix import Matrix
from revision.Revision import Revision
from revision.ModuleBook import ModuleView as mvwRevision
from usage.UsageProfile import UsageProfile
from failure_definition.FailureDefinition import FailureDefinition
from function.Function import Function
from function.ModuleBook import ModuleView as mvwFunction
from analyses.fmea.FMEA import FMEA
from requirement.Requirement import Requirement
from requirement.ModuleBook import ModuleView as mvwRequirement
from stakeholder.Stakeholder import Stakeholder
from hardware.BoM import BoM as HardwareBoM
from hardware.ModuleBook import ModuleView as mvwHardware
from analyses.allocation.Allocation import Allocation
from analyses.hazard.Hazard import Hazard
from analyses.similar_item.SimilarItem import SimilarItem
from analyses.pof.PhysicsOfFailure import PoF
from software.BoM import BoM as SoftwareBoM
from software.ModuleBook import ModuleView as mvwSoftware
from testing.Testing import Testing
from testing.growth.Growth import Growth
from testing.ModuleBook import ModuleView as mvwTesting
from validation.Validation import Validation
from validation.ModuleBook import ModuleView as mvwValidation
from incident.Incident import Incident
from incident.action.Action import Action
from incident.component.Component import Component
from incident.ModuleBook import ModuleView as mvwIncident
from survival.Survival import Survival
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

    # splScr = SplashScreen()

    # If you don't do this, the splash screen will show, but wont render it's
    # contents
    # while gtk.events_pending():
    #     gtk.main_iteration()

    # sleep(3)

    RTK()

    # splScr.window.destroy()

    gtk.main()

    return 0


def _read_site_configuration():
    """
    Function to read the site configuration file.

    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    _return = False

    if os.name == 'posix':
        Configuration.OS = 'Linux'
    elif os.name == 'nt':
        Configuration.OS = 'Windows'

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
        gtk.rc_parse("C:\\Program Files (x86)\\Common Files\\RTK\\share\\themes\\MurrinaBlue\\gtk-2.0\\gtkrc")

    # Get a config instance for the site configuration file.
    _config = Configuration.RTKConf('site')
    if not Utilities.file_exists(_config.conf_file):
        Widgets.rtk_warning(_(u"Site configuration file {0:s} not found.  "
                              u"This typically indicates RTK was installed "
                              u"improperly or RTK files have been corrupted.  "
                              u"You may try to uninstall and "
                              u"re-install RTK.").format(_config.conf_file))
        _return = True
    else:
        Configuration.COM_BACKEND = _config.read_configuration().get('Backend',
                                                                     'type')
        Configuration.SITE_DIR = _config.read_configuration().get('Backend',
                                                                  'path')

        Configuration.RTK_COM_INFO.append(
            _config.read_configuration().get('Backend', 'host'))
        Configuration.RTK_COM_INFO.append(
            _config.read_configuration().get('Backend', 'socket'))
        Configuration.RTK_COM_INFO.append(
            _config.read_configuration().get('Backend', 'database'))
        Configuration.RTK_COM_INFO.append(
            _config.read_configuration().get('Backend', 'user'))
        Configuration.RTK_COM_INFO.append(
            _config.read_configuration().get('Backend', 'password'))

    return _return


def _read_program_configuration():
    """
    Function to read the program configuration file.

    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    _return = False

    if os.name == 'posix':
        _homedir = os.environ['HOME']
    elif os.name == 'nt':
        _homedir = os.environ['USERPROFILE']

    # Get a config instance for the user configuration file.
    _config = Configuration.RTKConf('user')

    Configuration.BACKEND = _config.read_configuration().get('Backend', 'type')
    Configuration.RTK_PROG_INFO.append(
        _config.read_configuration().get('Backend', 'host'))
    Configuration.RTK_PROG_INFO.append(
        _config.read_configuration().get('Backend', 'socket'))
    Configuration.RTK_PROG_INFO.append(
        _config.read_configuration().get('Backend', 'database'))
    Configuration.RTK_PROG_INFO.append(
        _config.read_configuration().get('Backend', 'user'))
    Configuration.RTK_PROG_INFO.append(
        _config.read_configuration().get('Backend', 'password'))

    Configuration.FRMULT = float(_config.read_configuration().get('General',
                                                                  'frmultiplier'))
    Configuration.PLACES = _config.read_configuration().get('General',
                                                            'decimal')
    Configuration.RTK_MODE_SOURCE = _config.read_configuration().get('General',
                                                                     'modesource')
    Configuration.TABPOS[0] = _config.read_configuration().get('General',
                                                               'treetabpos')
    Configuration.TABPOS[1] = _config.read_configuration().get('General',
                                                               'listtabpos')
    Configuration.TABPOS[2] = _config.read_configuration().get('General',
                                                               'booktabpos')

    # Get directory and file information.
    _datadir = _config.read_configuration().get('Directories', 'datadir')
    _icondir = _config.read_configuration().get('Directories', 'icondir')
    _logdir = _config.read_configuration().get('Directories', 'logdir')
    _progdir = _config.read_configuration().get('Directories', 'progdir')

    Configuration.CONF_DIR = _config.conf_dir
    if not Utilities.dir_exists(Configuration.CONF_DIR):
        Widgets.rtk_warning(_(u"Configuration directory {0:s} does not "
                              u"exist.  "
                              u"Creating").format(Configuration.CONF_DIR))
        os.makedirs(Configuration.CONF_DIR)
        # TODO: Copy format files (*.conf, *.xml, RTKCommon.rtk) from system SITE_DIR to CONF_DIR

    Configuration.DATA_DIR = Configuration.CONF_DIR + _datadir + '/'
    if not Utilities.dir_exists(Configuration.DATA_DIR):
        Widgets.rtk_warning(_(u"Data directory {0:s} does not exist.  "
                              u"Creating").format(Configuration.DATA_DIR))
        os.makedirs(Configuration.DATA_DIR)
        # TODO: Copy data files (*.sql, *.map) from system data_dir to DATA_DIR

    Configuration.ICON_DIR = Configuration.CONF_DIR + _icondir + '/'
    if not Utilities.dir_exists(Configuration.ICON_DIR):
        Widgets.rtk_warning(_(u"Icon directory {0:s} does not exist.  "
                              u"Creating").format(Configuration.ICON_DIR))
        os.makedirs(Configuration.ICON_DIR)
        # TODO: Copy icons from system icon_dir to ICON_DIR

    Configuration.LOG_DIR = Configuration.CONF_DIR + _logdir + '/'
    if not Utilities.dir_exists(Configuration.LOG_DIR):
        Widgets.rtk_warning(_(u"Log directory {0:s} does not exist.  "
                              u"Creating").format(Configuration.LOG_DIR))
        os.makedirs(Configuration.LOG_DIR)

    Configuration.PROG_DIR = _progdir
    if not Utilities.dir_exists(Configuration.PROG_DIR):
        Widgets.rtk_warning(_(u"RTK Project directory {0:s} does not exist.  "
                              u"Using default RTK Project directory "
                              u"{1:s}.").format(Configuration.PROG_DIR,
                                                _homedir + '/analyses/rtk/'))
        Configuration.PROG_DIR = _homedir + '/analyses/rtk/'
        if not Utilities.dir_exists(Configuration.PROG_DIR):
            os.makedirs(Configuration.PROG_DIR)

    # Get list of format files.
    _formatfile = _config.read_configuration().get('Files', 'revisionformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'functionformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files',
                                                   'requirementformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'hardwareformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'validationformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'rgformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'fracaformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'partformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'siaformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'fmecaformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files',
                                                   'stakeholderformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'testformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'mechanismformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'rgincidentformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'incidentformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'softwareformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'datasetformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'riskformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'ffmecaformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)
    _formatfile = _config.read_configuration().get('Files', 'sfmecaformat')
    Configuration.RTK_FORMAT_FILE.append(Configuration.CONF_DIR + _formatfile)

    # Get color information.
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'revisionbg'))
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'revisionfg'))
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'functionbg'))
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'functionfg'))
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'requirementbg'))
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'requirementfg'))
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'assemblybg'))
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'assemblyfg'))
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'validationbg'))
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'validationfg'))
    Configuration.RTK_COLORS.append(_config.read_configuration().get('Colors',
                                                                     'rgbg'))
    Configuration.RTK_COLORS.append(_config.read_configuration().get('Colors',
                                                                     'rgfg'))
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'fracabg'))
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'fracafg'))
    Configuration.RTK_COLORS.append(_config.read_configuration().get('Colors',
                                                                     'partbg'))
    Configuration.RTK_COLORS.append(_config.read_configuration().get('Colors',
                                                                     'partfg'))
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'overstressbg'))
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'overstressfg'))
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'taggedbg'))
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'taggedfg'))
    Configuration.RTK_COLORS.append(
        _config.read_configuration().get('Colors', 'nofrmodelfg'))
    try:
        Configuration.RTK_COLORS.append(
            _config.read_configuration().get('Colors', 'softwarebg'))
    except NoOptionError:
        Configuration.RTK_COLORS.append('#FFFFFF')
    try:
        Configuration.RTK_COLORS.append(
            _config.read_configuration().get('Colors', 'softwarefg'))
    except NoOptionError:
        Configuration.RTK_COLORS.append('#FFFFFF')

    return _return


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
    __user_log = Configuration.LOG_DIR + '/RTK_user.log'
    __error_log = Configuration.LOG_DIR + '/RTK_error.log'
    __import_log = Configuration.LOG_DIR + '/RTK_import.log'

    if not Utilities.dir_exists(Configuration.LOG_DIR):
        os.makedirs(Configuration.LOG_DIR)

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

    return(_debug_log, _user_log, _import_log)


class NoOptionError(Exception):
    """
    Exception raised when no option is available in the configuration file.
    """

    pass


class RTK(object):
    """
    This is the RTK controller class.  The attributes of RTK are:

    :ivar bool loaded:
    :ivar site_dao: the :py:class:`rtk.DAO.DAO` used to communicate with the
                    site database.
    :ivar project_dao: the :py:class:`rtk.DAO.DAO` used to communicate with the
                       open RTK Project database.
    :ivar dtcMatrices: the :py:class:`rtk.datamodels.Matrix.Matrix` data
                       controller.
    :ivar dtcRevision: the :py:class:`rtk.revision.Revision.Revision` data
                       controller.
    :ivar dtcProfile: the :py:class:`rtk.usage.UsageProfile.UsageProfile` data
                      controller.
    :ivar dtcDefinitions: the :py:class:`rtk.failure_definition.FailureDefinition.FailureDefinition`
                          data controller.
    :ivar dtcFunction: the :py:class:`rtk.function.Function.Function` data
                       controller.
    :ivar dtcFMEA: the :py:class:`rtk.analyses.fmea.FMEA.FMEA` data
                   controller.
    :ivar dtcRequirement: the
                          :py:class:`rtk.requirement.Requirement.Requirement`
                          data controller.
    :ivar dtcStakeholder: the
                          :py:class:`rtk.stakeholder.Stakeholder.Stakeholder`
                          data controller.
    :ivar dtcHardwareBoM: the :py:class:`rtk.hardware.BoM.BoM` data controller.
    :ivar dtcAllocation: the :py:class:`rtk.analyses.allocation.Allocation.Allocation`
                         data controller.
    :ivar dtcHazard: the :py:class:`rtk.analyses.hazard.Hazard.Hazard` data
                     controller.
    :ivar dtcSimilarItem: the :py:class:`rtk.analyses.similar_item.SimilarItem.SimilarItem`
                          data controller.
    :ivar dtcPoF: the :py:class:`rtk.analyses.pof.PoF.PoF` data controller.
    :ivar dtcSoftwareBoM: the :py:class:`rtk.software.BoM.BoM` data controller.
    :ivar dtcTesting: the :py:class:`rtk.testing.Testing.Testing` data
                      controller.
    :ivar dtcGrowth: the :py:class:`rtk.testing.growth.Growth.Growth` data
                     controller.
    :ivar dtcValidation: the :py:class:`rtk.validation.Validation.Validation`
                         data controller.
    :ivar dtcIncident: the :py:class:`rtk.incident.Incident.Incident` data
                       controller.
    :ivar dtcAction: the :py:class:`rtk.incident.action.Action.Action` data
                     controller.
    :ivar dtcComponent: the
                        :py:class:`rtk.incident.component.Component.Component`
                        data controller.
    :ivar dtcSurvival: the :py:class:`rtk.survival.Survival.Survival` data
                       controller.
    :ivar gtk.StatusIcon() icoStatus: the WM bar status icon.
    :ivar list_book: the :py:class:`rtk.gui.gtk.mwi.ListBook.ListView`
                     for the current instance of RTK.
    :ivar module_book: the :py:class:`rtk.gui.gtk.mwi.ModuleBook.ModuleView`
                       for the current instance of RTK.
    :ivar work_book: the :py:class:`rtk.gui.gtk.mwi.WorkBook.WorkView`
                     for the current instance of RTK.
    """

    def __init__(self):                     # pylint: disable=R0914
        """
        Method to initialize the RTK controller.
        """

        # Read the site configuration file.
        _read_site_configuration()

        # Read the program configuration file.
        _read_program_configuration()

        RTK_INTERFACE = 1

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.loaded = False
        self.site_dao = None
        self.project_dao = None
        self.revision_id = None

        # Data controllers.
        self.dtcMatrices = Matrix()
        self.dtcRevision = Revision()
        self.dtcProfile = UsageProfile()
        self.dtcDefinitions = FailureDefinition()
        self.dtcFunction = Function()
        self.dtcFMEA = FMEA()
        self.dtcRequirement = Requirement()
        self.dtcStakeholder = Stakeholder()
        self.dtcHardwareBoM = HardwareBoM()
        self.dtcAllocation = Allocation()
        self.dtcHazard = Hazard()
        self.dtcSimilarItem = SimilarItem()
        self.dtcPoF = PoF()
        self.dtcSoftwareBoM = SoftwareBoM()
        self.dtcTesting = Testing()
        self.dtcGrowth = Growth()
        self.dtcValidation = Validation()
        self.dtcIncident = Incident()
        self.dtcAction = Action()
        self.dtcComponent = Component()
        self.dtcSurvival = Survival()

        self.icoStatus = gtk.StatusIcon()

        self.module_book = None
        self.list_book = None
        self.work_book = None

        # Connect to the site database.
        _database = Configuration.SITE_DIR + '/' + \
                    Configuration.RTK_COM_INFO[2] + '.rfb'
        self.site_dao = DAO(_database)

        # Create RTK views.  These need to be initialized after reading the
        # configuration.
        if RTK_INTERFACE == 0:              # Single window.
            pass
        else:                               # Multiple windows.
            self.module_book = ModuleView(self)
            self.list_book = self.module_book.create_listview()
            self.work_book = self.module_book.create_workview()

        # Validate the license.
        # if self._validate_license():
        #    sys.exit(2)

        # Create loggers.
        (self.debug_log,
         self.user_log,
         self.import_log) = _initialize_loggers()

        # Load common lists and variables.
        self._load_commons()

        # Plug-in each of the RTK module views.
        _modview = self.module_book.create_module_page(mvwRevision, self, -1)
        Configuration.RTK_MODULES.append(_modview)
        _modview = self.module_book.create_module_page(mvwFunction, self, -1)   # pylint: disable=R0204
        Configuration.RTK_MODULES.append(_modview)
        _modview = self.module_book.create_module_page(mvwRequirement,
                                                       self, -1)                # pylint: disable=R0204
        Configuration.RTK_MODULES.append(_modview)
        _modview = self.module_book.create_module_page(mvwHardware, self, -1)   # pylint: disable=R0204
        Configuration.RTK_MODULES.append(_modview)
        _modview = self.module_book.create_module_page(mvwSoftware, self, -1)   # pylint: disable=R0204
        Configuration.RTK_MODULES.append(_modview)
        _modview = self.module_book.create_module_page(mvwTesting, self, -1)    # pylint: disable=R0204
        Configuration.RTK_MODULES.append(_modview)
        _modview = self.module_book.create_module_page(mvwValidation, self, -1) # pylint: disable=R0204
        Configuration.RTK_MODULES.append(_modview)
        _modview = self.module_book.create_module_page(mvwIncident, self, -1)   # pylint: disable=R0204
        Configuration.RTK_MODULES.append(_modview)
        _modview = self.module_book.create_module_page(mvwSurvival, self, -1)   # pylint: disable=R0204
        Configuration.RTK_MODULES.append(_modview)

        _icon = Configuration.ICON_DIR + '32x32/db-disconnected.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        self.icoStatus.set_from_pixbuf(_icon)
        self.icoStatus.set_tooltip(_(u"RTK is not currently connected to a "
                                     u"program database."))

        self.module_book.present()

        # This is a hack to get the List View to display for the Revision
        # module when first launching RTK.
        self.module_book.notebook.next_page()
        self.module_book.notebook.prev_page()

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

    def _load_commons(self):                # pylint: disable=R0914
        """
        Reads the common database and assigns results to global configuration
        variables.  These variables will be available to all RTK modules.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# TODO: Re-write _load_commons; current McCabe Complexity metrix = 25.
        _query = "SELECT fld_group_name, fld_group_id \
                  FROM tbl_groups \
                  ORDER BY fld_group_name ASC"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_WORKGROUPS = _results

        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        # Load the component category and component sub-category lists.     #
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        _query = "SELECT * FROM tbl_category \
                  ORDER BY fld_category_noun ASC"
        (_cats, _error_code, __) = self.site_dao.execute(_query, commit=False)
        try:
            _n_cats = len(_cats)
        except TypeError:
            _n_cats = 0

        _query = "SELECT * FROM tbl_subcategory \
                  ORDER BY fld_category_id ASC"
        (_subcats, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)

        for i in range(_n_cats):
            Configuration.RTK_CATEGORIES[i + 1] = [_cats[i][1], _cats[i][0]]
            Configuration.RTK_SUBCATEGORIES[i + 1] = [x[1:] for x in _subcats
                                                      if x[0] == i + 1]

        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        # Load the Requirements lists.                                      #
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        _query = "SELECT fld_requirement_type_desc, \
                         fld_requirement_type_code, \
                         fld_requirement_type_id \
                  FROM tbl_requirement_type"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_REQUIREMENT_TYPES = _results

        _query = "SELECT DISTINCT fld_stakeholder \
                  FROM tbl_stakeholders \
                  ORDER BY fld_stakeholder ASC"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_STAKEHOLDERS = _results

        _query = "SELECT DISTINCT fld_group \
                  FROM rtk_affinity_groups \
                  ORDER BY fld_group ASC"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_AFFINITY_GROUPS = _results

        _query = "SELECT * FROM tbl_severity"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_SEVERITY = _results

        _query = "SELECT * FROM tbl_failure_probability"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_FAILURE_PROBABILITY = _results

        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        # Load the RPN category lists.                                      #
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        _query = "SELECT * FROM tbl_rpn_severity"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_RPN_SEVERITY = _results

        _query = "SELECT fld_occurrence_id, fld_occurrence_name, \
                         fld_occurrence_description \
                  FROM tbl_rpn_occurrence \
                  WHERE fld_fmeca_type=0"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_RPN_OCCURRENCE = _results

        _query = "SELECT fld_detection_id, fld_detection_name, \
                         fld_detection_description \
                  FROM tbl_rpn_detection \
                  WHERE fld_fmeca_type=0"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_RPN_DETECTION = _results

        Configuration.RTK_CONTROL_TYPES = [_(u"Prevention"), _(u"Detection")]

        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        # Load the hazards list.                                            #
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        _query = "SELECT fld_category, fld_subcategory \
                  FROM tbl_hazards"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_HAZARDS = _results

        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        # Load the active and dormant environment lists.                    #
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        _query = "SELECT fld_active_environ_code, fld_active_environ_noun \
                  FROM tbl_active_environs"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_ACTIVE_ENVIRON = [[_environ[1], _environ[0]]
                                            for _environ in _results]

        _query = "SELECT fld_dormant_environ_noun \
                  FROM tbl_dormant_environs"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_DORMANT_ENVIRON = [_environ[0] for _environ
                                             in _results]

        # Configuration.RTK_QUALITY_LEVELS
        _query = "SELECT fld_criticality_id, fld_criticality_name, \
                         fld_criticality_cat \
                  FROM tbl_criticality"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_CRITICALITY = _results

        _query = "SELECT fld_action_name FROM tbl_action_category"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_ACTION_CATEGORY = [i[0] for i in _results]

        _query = "SELECT fld_status_name FROM tbl_status"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_STATUS = _results

        _query = "SELECT fld_validation_type_desc FROM tbl_validation_type"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_TASK_TYPE = [_task[0] for _task in _results]

        _query = "SELECT fld_measurement_code FROM tbl_measurement_units"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_MEASUREMENT_UNITS = [_unit[0] for _unit in _results]

        _query = "SELECT fld_user_lname || ', ' || fld_user_fname \
                  FROM tbl_users \
                  ORDER BY fld_user_lname ASC"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_USERS = [_user[0] for _user in _results]

        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        # Load the program incident lists.                                  #
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        _query = "SELECT fld_incident_cat_name FROM tbl_incident_category"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_INCIDENT_CATEGORY = [_category[0] for _category
                                               in _results]

        _query = "SELECT fld_incident_type_name FROM tbl_incident_type"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_INCIDENT_TYPE = [_type[0] for _type in _results]

        _query = "SELECT fld_status_name FROM tbl_status"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_INCIDENT_STATUS = [_status[0] for _status
                                             in _results]

        _query = "SELECT fld_criticality_name FROM tbl_criticality"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_INCIDENT_CRITICALITY = [_crit[0] for _crit
                                                  in _results]

        _query = "SELECT fld_lifecycle_name FROM tbl_lifecycles"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_LIFECYCLE = [_lifecycle[0] for _lifecycle
                                       in _results]

        _query = "SELECT fld_detection_method FROM rtk_detection_methods"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_DETECTION_METHODS = [_method[0] for _method
                                               in _results]

        _query = "SELECT fld_manufacturers_noun, fld_location, fld_cage_code \
                  FROM tbl_manufacturers \
                  ORDER BY fld_manufacturers_noun ASC"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_MANUFACTURERS = [[_man[0], _man[1], _man[2]]
                                           for _man in _results]

        _query = "SELECT fld_hr_type_noun FROM tbl_hr_type"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_HR_TYPE = [_type[0] for _type in _results]

        _query = "SELECT fld_model_noun FROM tbl_calculation_model"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_HR_MODEL = [_model[0] for _model in _results]

        _query = "SELECT fld_distribution_noun FROM tbl_distributions"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_S_DIST = [_dist[0] for _dist in _results]

        _query = "SELECT fld_mttr_type_noun FROM tbl_mttr_type"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_MTTR_TYPE = [_type[0] for _type in _results]

        _query = "SELECT fld_cost_type_noun FROM tbl_cost_type"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_COST_TYPE = [_type[0] for _type in _results]

        _query = "SELECT fld_level_desc, fld_level_id FROM tbl_software_level"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_SW_LEVELS = [_level[0] for _level in _results]

        _query = "SELECT fld_category_name, fld_category_id, \
                         fld_category_description \
                  FROM tbl_software_category"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_SW_APPLICATION = [_app[0] for _app in _results]

        _query = "SELECT fld_phase_desc, fld_phase_id \
                  FROM tbl_development_phase"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        Configuration.RTK_SW_DEV_PHASES = [_phase[0] for _phase in _results]

        return False

    def create_project(self):
        """
        Method to request a new RTK Project database be created.
        """

        if Configuration.BACKEND == 'mysql':
            self._create_mysql_project()
        elif Configuration.BACKEND == 'sqlite3':
            # Connect to the new database.
            _database = Configuration.PROG_DIR + '/' + \
                        Configuration.RTK_PROG_INFO[2]
            _dao = DAO(_database)

            # Add all the tables to the new database.
            _sqlfile = open(Configuration.DATA_DIR +
                            'newprogram_sqlite3.sql', 'r')
            for _query in _sqlfile.read().split(';'):
                _dao.execute(_query, commit=True)

        # Close the connection.
        _dao.close()

        self.request_open_project()

        return False

    def open_project(self):
        """
        Method to open an RTK Project database and load it into the views.
        """

        _message = _(u"Opening Program "
                     u"Database {0:s}".format(Configuration.RTK_PROG_INFO[2]))
        self.module_book.statusbar.push(2, _message)

        # Connect to the project database.
        self.project_dao = DAO(Configuration.RTK_PROG_INFO[2])
        self.project_dao.execute("PRAGMA foreign_keys=ON", commit=False)

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
                                                               commit=None)
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
        (_results, _error_code, __) = self.project_dao.execute(_query, None)

        # For the active RTK modules, load the data.  For the RTK modules
        # that aren't active in the project, remove the page from the
        # RTK Module view.
        i = 0
        for _module in _results[0]:
            if _module == 1 and i < len(Configuration.RTK_MODULES):
                self.module_book.load_module_page(Configuration.RTK_MODULES[i])
                if i == 0:
                    self.revision_id = min(self.dtcRevision.dicRevisions.keys())
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
