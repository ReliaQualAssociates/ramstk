#!/usr/bin/env python
"""
This is the main program for the RTK application.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       RTK.py is part of the RTK Project
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
from gui.gtk.mwi.ListBook import ListView
from gui.gtk.mwi.WorkBook import WorkView

import configuration as _conf
import utilities as _util

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


def _read_configuration():
    """
    Reads the site configuration and RTK configuration files.

    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    # Set the gtk+ theme on Windows.
    if sys.platform.startswith('win'):
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
        gtk.rc_parse("C:\\Program Files (x86)\\Common Files\\GTK\\2.0\\share\\themes\\MurrinaBlue\\gtk-2.0\\gtkrc")

    # Import the test data file if we are executing in developer mode.
    if len(sys.argv) > 1 and sys.argv[1] == 'devmode':
        _conf.MODE = 'developer'

    # Read the configuration file.
    _util.read_configuration()

    if os.name == 'posix':
        _conf.OS = 'Linux'
    elif os.name == 'nt':
        _conf.OS = 'Windows'

    return False


def _initialize_loggers():
    """
    Creates loggers for the RTK application.

    :return: (_debug_log, _user_log, _import_log)
    :rtype: tuple
    """

    # Create loggers for the application.  The first is to store log
    # information for RTK developers.  The second is to log errors for the
    # user.  The user can use these errors to help find problems with their
    # inputs and sich.
    __user_log = _conf.LOG_DIR + '/RTK_user.log'
    __error_log = _conf.LOG_DIR + '/RTK_error.log'
    __import_log = _conf.LOG_DIR + '/RTK_import.log'

    if not _util.dir_exists(_conf.LOG_DIR):
        os.makedirs(_conf.LOG_DIR)

    if _util.file_exists(__user_log):
        os.remove(__user_log)
    if _util.file_exists(__error_log):
        os.remove(__error_log)
    if _util.file_exists(__import_log):
        os.remove(__import_log)

    _debug_log = _util.create_logger("RTK.debug", logging.DEBUG,
                                     __error_log)
    _user_log = _util.create_logger("RTK.user", logging.WARNING,
                                    __user_log)
    _import_log = _util.create_logger("RTK.import", logging.WARNING,
                                      __import_log)

    return(_debug_log, _user_log, _import_log)


class RTK(object):
    """
    This is the RTK controller class.
    """

    def __init__(self):
        """
        Method to initialize the RTK controller.
        """

        RTK_INTERFACE = 1

        # Initialize public scalar attributes.
        self.loaded = False

        # Read the site configuration file.
        _read_configuration()

        # Connect to the site database.
        _database = _conf.SITE_DIR + '/' + _conf.RTK_COM_INFO[2] + '.rfb'
        self.site_dao = DAO(_database)

        # Validate the license.
        if self._validate_license():
            sys.exit(2)

        # Create loggers.
        (self.debug_log,
         self.user_log,
         self.import_log) = _initialize_loggers()

        # Load common lists and variables.
        self._load_commons()

        # Create data controllers.
        self.dtcMatrices = Matrix()
        self.dtcRevision = Revision()
        dtcProfile = UsageProfile()
        dtcDefinitions = FailureDefinition()
        dtcFunction = Function()
        dtcFMEA = FMEA()
        dtcRequirement = Requirement()
        dtcStakeholder = Stakeholder()
        dtcHardwareBoM = HardwareBoM()
        dtcAllocation = Allocation()
        dtcHazard = Hazard()
        dtcSimilarItem = SimilarItem()
        dtcPoF = PoF()
        dtcSoftwareBoM = SoftwareBoM()
        dtcTesting = Testing()
        dtcGrowth = Growth()
        dtcValidation = Validation()
        dtcIncident = Incident()
        dtcAction = Action()
        dtcComponent = Component()

        # Initialize RTK views.
        if RTK_INTERFACE == 0:              # Single window.
            pass
        else:                               # Multiple windows.
            self.module_book = ModuleView(self)
            self.list_book = self.module_book.create_listview()
            self.work_book = self.module_book.create_workview(self.site_dao)

        # Plug-in each of the RTK module views.
        _modview = self.module_book.create_module_page(mvwRevision,
                                                       self.dtcRevision, -1,
                                                       dtcProfile,
                                                       dtcDefinitions)
        _conf.RTK_MODULES.append(_modview)
        _modview = self.module_book.create_module_page(mvwFunction,
                                                       dtcFunction, -1,
                                                       dtcFMEA,
                                                       dtcProfile,
                                                       self.dtcMatrices)
        _conf.RTK_MODULES.append(_modview)
        _modview = self.module_book.create_module_page(mvwRequirement,
                                                       dtcRequirement, -1,
                                                       dtcStakeholder,
                                                       self.dtcMatrices,
                                                       self.site_dao)
        _conf.RTK_MODULES.append(_modview)
        _modview = self.module_book.create_module_page(mvwHardware,
                                                       dtcHardwareBoM, -1,
                                                       dtcAllocation,
                                                       dtcHazard,
                                                       dtcSimilarItem,
                                                       dtcFMEA, dtcPoF)
        _conf.RTK_MODULES.append(_modview)
        _modview = self.module_book.create_module_page(mvwSoftware,
                                                       dtcSoftwareBoM, -1)
        _conf.RTK_MODULES.append(_modview)
        _modview = self.module_book.create_module_page(mvwTesting,
                                                       dtcTesting, -1,
                                                       dtcGrowth)
        _conf.RTK_MODULES.append(_modview)
        _modview = self.module_book.create_module_page(mvwValidation,
                                                       dtcValidation, -1)
        _conf.RTK_MODULES.append(_modview)
        _modview = self.module_book.create_module_page(mvwIncident,
                                                       dtcIncident, -1,
                                                       dtcAction, dtcComponent)
        _conf.RTK_MODULES.append(_modview)

        self.icoStatus = gtk.StatusIcon()
        _icon = _conf.ICON_DIR + '32x32/db-disconnected.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        self.icoStatus.set_from_pixbuf(_icon)
        self.icoStatus.set_tooltip(_(u"RTK is not currently connected to a "
                                     u"program database."))
        #self.open_project()
        self.module_book.present()

    def _validate_license(self):
        """
        Method to validate the license and the license expiration date.

        :return: False if successful or true if an error is encountered.
        :rtype: boolean
        """

        # Read the license file and compare to the product key in the site
        # database.  If they are not equal, quit the application.
        _license_file = _conf.DATA_DIR + '/license.key'
        try:
            _license_file = open(_license_file, 'r')
        except IOError:
            _util.rtk_warning(_(u"Cannot find license file %s.  "
                                u"If your license file is elsewhere, "
                                u"please place it in %s." %
                                (_license_file, _conf.DATA_DIR)))
            return True

        _license_key = _license_file.readline().rstrip('\n')
        _license_file.close()

        _query = "SELECT fld_product_key, fld_expire_date \
                  FROM tbl_site_info"
        (_results, _error_code, __) = self.site_dao.execute(_query, None)

        if _license_key != _results[0][0]:
            _util.rtk_error(_(u"Invalid license (Invalid key).  Your license "
                              u"key is incorrect.  Closing the RTK "
                              u"application."))
            return True

        if datetime.datetime.today().toordinal() > _results[0][1]:
            _expire_date = str(datetime.datetime.fromordinal(int(
                _results[0][1])).strftime('%Y-%m-%d'))
            _util.rtk_error(_(u"Invalid license (Expired).  Your license "
                              u"expired on %s.  Closing RTK application." %
                              _expire_date))
            return True

        return False

    def _load_commons(self):
        """
        Reads the common database and assigns results to global configuration
        variables.  These variables will be available to all RTK modules.

        :return:
        :rtype:
        """

        _query = "SELECT * FROM tbl_severity"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_SEVERITY = _results

        _query = "SELECT * FROM tbl_failure_probability"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_FAILURE_PROBABILITY = _results

        # Retrieve RPN categories.
        _query = "SELECT * FROM tbl_rpn_severity"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_RPN_SEVERITY = _results

        _query = "SELECT fld_occurrence_id, fld_occurrence_name, \
                         fld_occurrence_description \
                  FROM tbl_rpn_occurrence \
                  WHERE fld_fmeca_type=0"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_RPN_OCCURRENCE = _results

        _query = "SELECT fld_detection_id, fld_detection_name, \
                         fld_detection_description \
                  FROM tbl_rpn_detection \
                  WHERE fld_fmeca_type=0"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_RPN_DETECTION = _results

        _conf.RTK_CONTROL_TYPES = [_(u"Prevention"), _(u"Detection")]

        # Retrieve the list of hazards to include in the hazard analysis
        # worksheet.
        _query = "SELECT fld_category, fld_subcategory \
                  FROM tbl_hazards"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_HAZARDS = _results

        #_conf.RTK_ACTIVE_ENVIRONMENTS
        #_conf.RTK_DORMANT_ENVIRONMENTS
        #_conf.RTK_QUALITY_LEVELS
        _query = "SELECT fld_criticality_id, fld_criticality_name, \
                         fld_criticality_cat \
                  FROM tbl_criticality"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_CRITICALITY = _results

        _query = "SELECT fld_action_name FROM tbl_action_category"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_ACTION_CATEGORY = [i[0] for i in _results]

        _query = "SELECT fld_status_name FROM tbl_status"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_STATUS = _results

        _query = "SELECT fld_user_lname, fld_user_fname FROM tbl_users"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_USERS = _results

        _query = "SELECT fld_validation_type_desc FROM tbl_validation_type"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_TASK_TYPE = [_task[0] for _task in _results]

        _query = "SELECT fld_measurement_code FROM tbl_measurement_units"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_MEASUREMENT_UNITS = [_unit[0] for _unit in _results]

        _query = "SELECT fld_user_lname || ', ' || fld_user_fname \
                  FROM tbl_users \
                  ORDER BY fld_user_lname ASC"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_USERS = [_user[0] for _user in _results]

        _query = "SELECT fld_incident_cat_name FROM tbl_incident_category"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_INCIDENT_CATEGORY = [_category[0] for _category in _results]

        _query = "SELECT fld_incident_type_name FROM tbl_incident_type"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_INCIDENT_TYPE = [_type[0] for _type in _results]

        _query = "SELECT fld_status_name FROM tbl_status"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_INCIDENT_STATUS = [_status[0] for _status in _results]

        _query = "SELECT fld_criticality_name FROM tbl_criticality"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_INCIDENT_CRITICALITY = [_crit[0] for _crit in _results]

        _query = "SELECT fld_lifecycle_name FROM tbl_lifecycles"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_LIFECYCLE = [_lifecycle[0] for _lifecycle in _results]

        _query = "SELECT fld_detection_method FROM rtk_detection_methods"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _conf.RTK_DETECTION_METHODS = [_method[0] for _method in _results]

        return False

    def open_project(self):
        """
        Method to open an RTK Program database and load it into the views.
        """

        self.module_book.statusbar.push(2, _(u"Opening Program Database..."))

        # Connect to the project database.
        #_database = '/home/andrew/projects/RTKTestDB.rtk'
        self.project_dao = DAO(_conf.RTK_PROG_INFO[2])

        self.project_dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.dtcMatrices._dao = self.project_dao

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
        _conf.RTK_PREFIX = [_element for _element in _results[0]]

        _icon = _conf.ICON_DIR + '32x32/db-connected.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        self.icoStatus.set_from_pixbuf(_icon)
        self.icoStatus.set_tooltip(_(u"RTK is connected to program database "
                                     u"%s." % _conf.RTK_PROG_INFO[2]))
        self.module_book.set_title(_(u"RTK - Analyzing %s" %
                                   _conf.RTK_PROG_INFO[2]))

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
        _first_revision = None
        for _module in _results[0]:
            if _module == 1 and i < len(_conf.RTK_MODULES):
                self.module_book.load_module_page(_conf.RTK_MODULES[i],
                                                  self.project_dao,
                                                  _first_revision)
                if i == 0:
                    _first_revision = min(self.dtcRevision.dicRevisions.keys())
                _conf.RTK_PAGE_NUMBER.append(i)
            else:
                self.module_book.notebook.remove_page(i)
            i += 1

        #_conf.METHOD = results[0][36]

        self.module_book.statusbar.pop(2)

        self.loaded = True

if __name__ == '__main__':

    main()
