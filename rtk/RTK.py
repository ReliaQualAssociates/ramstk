#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.RTK.py is part of the RTK Project
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

"""
This is the main program for the RTK application.
"""

import gettext
import logging
import os
import sys
from datetime import date, timedelta

from sqlalchemy.orm import scoped_session
from pubsub import pub

from treelib import Tree

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
from Configuration import Configuration
import Utilities
from dao.DAO import DAO
from dao.RTKCommonDB import RTK_SITE_SESSION, RTK_PROGRAM_SESSION
from dao.RTKApplication import RTKApplication
from dao.RTKCategory import RTKCategory
from dao.RTKCriticality import RTKCriticality
from dao.RTKDistribution import RTKDistribution
from dao.RTKEnviron import RTKEnviron
from dao.RTKFailureMode import RTKFailureMode
from dao.RTKGroup import RTKGroup
from dao.RTKHazards import RTKHazards
from dao.RTKLevel import RTKLevel
from dao.RTKManufacturer import RTKManufacturer
from dao.RTKMethod import RTKMethod
from dao.RTKModel import RTKModel
from dao.RTKPhase import RTKPhase
from dao.RTKRPN import RTKRPN
from dao.RTKSiteInfo import RTKSiteInfo
from dao.RTKStakeholders import RTKStakeholders
from dao.RTKStatus import RTKStatus
from dao.RTKSubCategory import RTKSubCategory
from dao.RTKType import RTKType
from dao.RTKUnit import RTKUnit
from dao.RTKUser import RTKUser
# from datamodels.matrix.Matrix import Matrix
# from revision.Revision import Revision
# from usage.UsageProfile import UsageProfile
# from failure_definition.FailureDefinition import FailureDefinition
# from function.Function import Function
# from analyses.fmea.FMEA import FMEA
# from requirement.Requirement import Requirement
# from stakeholder.Stakeholder import Stakeholder
# from hardware.BoM import BoM as HardwareBoM
# from analyses.allocation.Allocation import Allocation
# from analyses.hazard.Hazard import Hazard
# from analyses.similar_item.SimilarItem import SimilarItem
# from analyses.pof.PhysicsOfFailure import PoF
# from software.BoM import BoM as SoftwareBoM
# from testing.Testing import Testing
# from testing.growth.Growth import Growth
# from validation.Validation import Validation
# from incident.Incident import Incident
# from incident.action.Action import Action
# from incident.component.Component import Component
# from survival.Survival import Survival

import gui.gtk.Widgets as Widgets
from gui.gtk.mwi.ListBook import ListView
from gui.gtk.mwi.ModuleBook import ModuleView
from gui.gtk.mwi.WorkBook import WorkView

# from revision.ModuleBook import ModuleView as mvwRevision
# from function.ModuleBook import ModuleView as mvwFunction
# from requirement.ModuleBook import ModuleView as mvwRequirement
# from hardware.ModuleBook import ModuleView as mvwHardware
# from software.ModuleBook import ModuleView as mvwSoftware
# from testing.ModuleBook import ModuleView as mvwTesting
# from incident.ModuleBook import ModuleView as mvwIncident
# from validation.ModuleBook import ModuleView as mvwValidation
# from survival.ModuleBook import ModuleView as mvwSurvival

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


def _initialize_loggers(configuration):
    """
    Function to create loggers for the RTK application.

    :param configuration: the RTK Configuration() object instance holding all
                          the configuration values for the current instance of
                          RTK.
    :type configuration: :py:class:`rtk.Configuration.Configuration()`
    :return: (_debug_log, _user_log, _import_log)
    :rtype: tuple
    """

    # Create loggers for the application.  The first is to store log
    # information for RTK developers.  The second is to log errors for the
    # user.  The user can use these errors to help find problems with their
    # inputs and sich.
    __user_log = configuration.RTK_LOG_DIR + '/RTK_user.log'
    __error_log = configuration.RTK_LOG_DIR + '/RTK_debug.log'
    __import_log = configuration.RTK_LOG_DIR + '/RTK_import.log'

    if not Utilities.dir_exists(configuration.RTK_LOG_DIR):
        os.makedirs(configuration.RTK_LOG_DIR)

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

    :ivar site_dao: the data access object used to communicate with the RTK
                    Common database.
    :type site_dao: :py:class:`rtk.dao.DAO.DAO()`
    :ivar program_dao: the data access object used to communicate with the RTK
                       Program database
    :type program_dao: :py:class:`rtk.dao.DAO.DAO()`
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
        self.tree = Tree()

        self.site_dao = sitedao
        self.program_dao = programdao

        # Create a session for communicating with the RTK Common database
        site_session = RTK_SITE_SESSION
        site_session.configure(bind=self.site_dao.engine, autoflush=False,
                               expire_on_commit=False)
        self.site_session = scoped_session(site_session)
        self.program_session = None

    def create_program(self, database):
        """
        Method to create a new RTK Program database.

        :param str database: the RFC1738 URL path to the database to connect
                             with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        self.program_dao.db_connect(database)

        _session = scoped_session(RTK_PROGRAM_SESSION)
        _session.configure(bind=self.program_dao.engine,
                           autoflush=False, expire_on_commit=False)

        if not self.program_dao.db_create_program(database, _session):
            pub.sendMessage('createdProgram')
        else:
            _return = True

        _session.close()

        return _return

    def read_program_info(self):
        """
        Method to read the program info table from the RTK Program database.

        :return:
        :rtype: ()
        """

        # Find the prefix to use for each module.
        _query = "SELECT fld_revision_prefix, fld_function_prefix, \
                         fld_assembly_prefix, fld_part_prefix, \
                         fld_fmeca_prefix, fld_mode_prefix, \
                         fld_effect_prefix, fld_cause_prefix, \
                         fld_software_prefix \
                  FROM rtk_program_info"
        _prefixes = self.program_dao.db_query(_query, self.program_session)

        # Find which modules are active in this program.
        _query = "SELECT fld_revision_active, fld_function_active, \
                         fld_requirement_active, fld_hardware_active, \
                         fld_software_active, fld_vandv_active, \
                         fld_testing_active, fld_fraca_active, \
                         fld_survival_active, fld_rcm_active, \
                         fld_rbd_active, fld_fta_active\
                  FROM rtk_program_info"
        _actives = self.program_dao.db_query(_query, self.program_session)

        return _prefixes, _actives

    def open_program(self, database):
        """
        Method to open an RTK Program database for analyses.

        :param str database: the RFC1738 URL path to the database to connect
                             with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if not self.program_dao.db_connect(database):
            program_session = RTK_PROGRAM_SESSION
            program_session.configure(bind=self.program_dao.engine,
                                      autoflush=False, expire_on_commit=False)
            self.program_session = scoped_session(program_session)
            pub.sendMessage('openedProgram')
        else:
            _return = True

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

    def load_globals(self, configuration):
        """
        Method to load the RTK Program global constants managed by the RTK
        Configuration class.

        :param configuration: the currently active RTK Program Configuration()
                              object.
        :type configuration: :py:class:`rtk.Configuration.Configuration()`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        # ------------------------------------------------------------------- #
        # Build the component category, component subcategory, failure modes  #
        # tree.                                                               #
        # ------------------------------------------------------------------- #
        self.tree.create_node('Components', -1)
        for _category in self.site_session.query(RTKCategory).\
                filter(RTKCategory.type == 'hardware').all():
            self.tree.create_node(_category.name, _category.category_id,
                                  parent=-1,
                                  data=_category.get_attributes()[1:])

        for _subcategory in self.site_session.query(RTKSubCategory).all():
            # We need to create a unique identifer for each subcategory because
            # we can't have two nodes in the tree with the same ID, but we can
            # have a category and subcategory with the same ID in the database.
            # This simple method guarantees a unique ID for the subcategory for
            # the tree.
            _identifier = str(_subcategory.category_id) + \
                          str(_subcategory.subcategory_id)
            self.tree.create_node(_subcategory.description, _identifier,
                                  parent=_subcategory.category_id,
                                  data=_subcategory.get_attributes()[2:])

        for _mode in self.site_session.query(RTKFailureMode).all():
            # We need to create a unique identifer for each mode because
            # we can't have two nodes in the tree with the same ID, but we can
            # have a category, subcategory, and/or mode with the same ID in the
            # database.  This simple method guarantees a unique ID for the mode
            # for the tree.  For the same reason we have to create the parent
            # ID.
            _identifier = str(_mode.category_id) + \
                          str(_mode.subcategory_id) + \
                          str(_mode.mode_id)
            _parent = str(_mode.category_id) + str(_mode.subcategory_id)
            self.tree.create_node(_mode.description, _identifier,
                                  parent=_parent,
                                  data=_mode.get_attributes()[3:])

        for _stakeholder in self.site_session.query(RTKStakeholders).all():
            configuration.RTK_STAKEHOLDERS[_stakeholder.stakeholders_id] = \
                _stakeholder.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKCategory.                                 #
        # ------------------------------------------------------------------- #
        for _category in self.site_session.query(RTKCategory).\
                filter(RTKCategory.category_id == 'action').all():
            configuration.RTK_ACTION_CATEGORY[_category.category_id] = \
                _category.get_attributes()[1:]

        for _category in self.site_session.query(RTKCategory).\
                filter(RTKCategory.type == 'incident').all():
            configuration.RTK_INCIDENT_CATEGORY[_category.category_id] = \
                _category.get_attributes()[1:]

        for _severity in self.site_session.query(RTKCategory).\
                filter(RTKCategory.type == 'risk').all():
            configuration.RTK_SEVERITY[_severity.category_id] = \
                _severity.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKEnviron.                                  #
        # ------------------------------------------------------------------- #
        for _environ in self.site_session.query(RTKEnviron).\
                filter(RTKEnviron.type == 'active').all():
            configuration.RTK_ACTIVE_ENVIRONMENTS[_environ.environ_id] = \
                _environ.get_attributes()[1:]

        for _environ in self.site_session.query(RTKEnviron).\
                filter(RTKEnviron.type == 'dormant').all():
            configuration.RTK_DORMANT_ENVIRONMENTS[_environ.environ_id] = \
                _environ.get_attributes()[1:]

        for _environ in self.site_session.query(RTKEnviron).\
                filter(RTKEnviron.type == 'development').all():
            configuration.RTK_SW_DEV_ENVIRONMENTS[_environ.environ_id] = \
                _environ.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKGroup.                                    #
        # ------------------------------------------------------------------- #
        for _group in self.site_session.query(RTKGroup).\
                filter(RTKGroup.type == 'affinity').all():
            configuration.RTK_AFFINITY_GROUPS[_group.group_id] = \
                _group.get_attributes()[1:]

        for _group in self.site_session.query(RTKGroup).\
                filter(RTKGroup.type == 'workgroup').all():
            configuration.RTK_WORKGROUPS[_group.group_id] = \
                _group.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKLevel.                                    #
        # ------------------------------------------------------------------- #
        for _level in self.site_session.query(RTKLevel).\
                filter(RTKLevel.type == 'probability').all():
            configuration.RTK_FAILURE_PROBABILITY[_level.level_id] = \
                _level.get_attributes()[1:]

        for _level in self.site_session.query(RTKLevel).\
                filter(RTKLevel.type == 'software').all():
            configuration.RTK_SW_LEVELS[_level.level_id] = \
                _level.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load the dictionaries from RTKMethod.                               #
        # ------------------------------------------------------------------- #
        for _method in self.site_session.query(RTKMethod).\
                filter(RTKMethod.type == 'detection').all():
            configuration.RTK_DETECTION_METHODS[_method.method_id] = \
                _method.get_attributes[1:]

        for _method in self.site_session.query(RTKMethod).\
                filter(RTKMethod.type == 'test').all():
            configuration.RTK_SW_TEST_METHODS[_method.method_id] = \
                _method.get_attributes[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKModel.                                    #
        # ------------------------------------------------------------------- #
        for _model in self.site_session.query(RTKModel).\
                filter(RTKModel.type == 'allocation').all():
            configuration.RTK_ALLOCATION_MODELS[_model.model_id] = \
                _model.get_attributes()[1:]
        for _model in self.site_session.query(RTKModel).\
                filter(RTKModel.type == 'rprediction').all():
            configuration.RTK_HR_MODEL[_model.model_id] = \
                _model.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load the dictionaries from RTKPhase.                                #
        # ------------------------------------------------------------------- #
        for _phase in self.site_session.query(RTKPhase).\
                filter(RTKPhase.type == 'lifecycle').all():
            configuration.RTK_LIFECYCLE[_phase.phase_id] = \
                _phase.get_atrributes()[1:]

        for _phase in self.site_session.query(RTKPhase).\
                filter(RTKPhase.type == 'development').all():
            configuration.RTK_SW_DEV_PHASES[_phase.phase_id] = \
                _phase.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKRPN.                                      #
        # ------------------------------------------------------------------- #
        for _rpn in self.site_session.query(RTKRPN).\
                filter(RTKRPN.type == 'detection').all():
            configuration.RTK_RPN_DETECTION[_rpn.rpn_id] = \
                _rpn.get_attributes()[1:]

        for _rpn in self.site_session.query(RTKRPN).\
                filter(RTKRPN.type == 'occurrence').all():
            configuration.RTK_RPN_OCCURRENCE[_rpn.rpn_id] = \
                _rpn.get_attributes()[1:]

        for _rpn in self.site_session.query(RTKRPN). \
                filter(RTKRPN.type == 'severity').all():
            configuration.RTK_RPN_SEVERITY[_rpn.rpn_id] = \
                _rpn.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKStatus.                                   #
        # ------------------------------------------------------------------- #
        for _status in self.site_session.query(RTKStatus).\
                filter(RTKStatus.type == 'action').all():
            configuration.RTK_ACTION_STATUS[_status.status_id] = \
                _status.get_attributes()[1:]

        for _status in self.site_session.query(RTKStatus).\
                filter(RTKStatus.type == 'incident').all():
            configuration.RTK_INCIDENT_STATUS[_status.status_id] = \
                _status.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKType.                                     #
        # ------------------------------------------------------------------- #
        configuration.RTK_CONTROL_TYPES = [_(u"Prevention"), _(u"Detection")]

        for _type in self.site_session.query(RTKType). \
                filter(RTKType.type == 'cost').all():
            configuration.RTK_COST_TYPE[_type.type_id] = \
                _type.get_attributes()[1:]

        for _type in self.site_session.query(RTKType).\
                filter(RTKType.type == 'mtbf').all():
            configuration.RTK_HR_TYPE[_type.type_id] = \
                _type.get_attributes()[1:]

        for _type in self.site_session.query(RTKType).\
                filter(RTKType.type == 'incident').all():
            configuration.RTK_INCIDENT_TYPE[_type.type_id] = \
                _type.get_attributes[1:]

        for _type in self.site_session.query(RTKType).\
                filter(RTKType.type == 'mttr').all():
            configuration.RTK_MTTR_TYPE[_type.type_id] = \
                _type.get_attributes()[1:]

        for _type in self.site_session.query(RTKType).\
                filter(RTKType.type == 'requirement').all():
            configuration.RTK_REQUIREMENT_TYPE[_type.type_id] = \
                _type.get_attributes()[1:]

        for _type in self.site_session.query(RTKType).\
                filter(RTKType.type == 'validation').all():
            configuration.RTK_VALIDATION_TYPE[_type.type_id] = \
                _type.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from tables not requiring a filter.               #
        # ------------------------------------------------------------------- #
        for _application in self.site_session.query(RTKApplication).all():
            configuration.RTK_SW_APPLICATION[_application.application_id] = \
                _application.get_attributes()[1:]

        for _crit in self.site_session.query(RTKCriticality).all():
            configuration.RTK_CRITICALITY[_crit.criticality_id] = \
                _crit.get_attributes()[1:]

        for _dist in self.site_session.query(RTKDistribution).all():
            configuration.RTK_S_DIST[_dist.distribution_id] = \
                _dist.get_attributes()[1:]

        for _hazard in self.site_session.query(RTKHazards).all():
            configuration.RTK_HAZARDS[_hazard.hazard_id] = \
                _hazard.get_attributes()[1:]

        for _manufacturer in self.site_session.query(RTKManufacturer).all():
            configuration.RTK_MANUFACTURERS[_manufacturer.manufacturer_id] = \
                _manufacturer.get_attributes()[1:]

        for _unit in self.site_session.query(RTKUnit).\
                filter(RTKUnit.type == 'measurement').all():
            configuration.RTK_MEASUREMENT_UNITS[_unit.unit_id] = \
                _unit.get_attributes()[1:]

        for _user in self.site_session.query(RTKUser).all():
            configuration.RTK_USERS[_user.user_id] = \
                _user.get_attributes()[1:]

        return _return

    def validate_license(self, license_key):
        """
        Method to validate the license and the license expiration date.

        :param str license_key: the license key for the current RTK
                                installation.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = 'RTK SUCCESS: Validating RTK License.'

        _site_info = self.site_session.query(RTKSiteInfo).first()

        if license_key != _site_info.product_key:
            _error_code = 1
            _msg = 'RTK ERROR: Invalid license (Invalid key).  Your license ' \
                   'key is incorrect.  Closing the RTK application.'

        _today = date.today().strftime('%Y-%m-%d')
        _expire_date = _site_info.expire_on.strftime('%Y-%m-%d')
        if _today > _expire_date:
            _error_code = 2
            _msg = 'RTK ERROR: Invalid license (Expired).  Your license ' \
                   'expired on {0:s}.  Closing the RTK application.'. \
                format(_expire_date)

        return _error_code, _msg


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

    RTK_CONFIGURATION = Configuration()

    def __init__(self):  # pylint: disable=R0914
        """
        Method to initialize an instance of the RTK data controller.
        """

        # Read the site configuration file.
        self.RTK_CONFIGURATION.set_site_variables()
        self.RTK_CONFIGURATION.set_user_variables()
        self.RTK_CONFIGURATION.read_configuration()

        # Create loggers.
        (self.RTK_CONFIGURATION.RTK_DEBUG_LOG,
         self.RTK_CONFIGURATION.RTK_USER_LOG,
         self.RTK_CONFIGURATION.RTK_IMPORT_LOG) = \
            _initialize_loggers(self.RTK_CONFIGURATION)

        # Validate the license.
        # if self._validate_license():
        #    sys.exit(2)

        # Initialize private dictionary instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dictionary instance attributes.
        self.dic_controllers = {'revision': None,
                                'function': None,
                                'requirement': None,
                                'hardware': None,
                                'software': None,
                                'testing': None,
                                'validation': None,
                                'incident': None,
                                'survival': None,
                                'matrices': None,
                                'profile': None,
                                'definition': None,
                                'fmea': None,
                                'stakeholder': None,
                                'allocation': None,
                                'hazard': None,
                                'similaritem': None,
                                'pof': None,
                                'growth': None,
                                'action': None,
                                'component': None}
        self.dic_books = {'listview': None,
                          'moduleview': None,
                          'workview': None}

        # Define public list attributes.

        # Define public scalar attributes.
        self.icoStatus = gtk.StatusIcon()

        # Connect to the RTK Common database.
        _database = None
        if self.RTK_CONFIGURATION.RTK_COM_BACKEND == 'sqlite':
            _database = self.RTK_CONFIGURATION.RTK_COM_BACKEND + ':///' + \
                        self.RTK_CONFIGURATION.RTK_COM_INFO['database']
        _dao = DAO()
        _dao.db_connect(_database)

        # Create an instance of the RTK Data Model and load global constants.
        self.rtk_model = Model(_dao, DAO())
        self.request_load_globals()

        # Create RTK Books.  These need to be initialized after reading the
        # configuration.
        if self.RTK_CONFIGURATION.RTK_GUI_LAYOUT == 'basic':  # Single window.
            pass
        else:  # Multiple windows.
            self.dic_books['listview'] = ListView()
            self.dic_books['moduleview'] = ModuleView(self)
            self.dic_books['workview'] = WorkView()

    def request_create_program(self):
        """
        Method to request a new RTK Program database be created.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if self.RTK_CONFIGURATION.RTK_BACKEND == 'sqlite':
            _database = self.RTK_CONFIGURATION.RTK_BACKEND + ':///' + \
                        self.RTK_CONFIGURATION.RTK_PROG_INFO['database']

        _return = self.rtk_model.create_program(_database)
        if not _return:
            self.request_open_program()
            self.RTK_CONFIGURATION.RTK_USER_LOG.info('RTK SUCCESS: Creating '
                                                     'RTK Program database '
                                                     '{0:s}.'. \
                                                     format(_database))
        else:
            self.RTK_CONFIGURATION.RTK_DEBUG_LOG.error('RTK ERROR: Failed to '
                                                       'create RTK Program '
                                                       'database {0:s}.'. \
                                                       format(_database))

        return _return

    def request_load_globals(self):
        """
        Method to load all the global Configuration variables from the RTK
        Site database.

        :param session: the SQLAlchemy scoped_session to use for querying the
                        RTK Common database.
        :type session: :py:class:`sqlalchemy.orm.scoped_session`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self.rtk_model.load_globals(self.RTK_CONFIGURATION)

    def request_open_program(self):
        """
        Method to request an RTK Program database be opened for analyses.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if self.RTK_CONFIGURATION.RTK_BACKEND == 'sqlite':
            _database = self.RTK_CONFIGURATION.RTK_BACKEND + ':///' + \
                        self.RTK_CONFIGURATION.RTK_PROG_INFO['database']

        # If the database was successfully opened, create an instance of each
        # of the slave data controllers.
        if not self.rtk_model.open_program(_database):
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
            _prefixes, _actives = self.rtk_model.read_program_info()
            for _row in _prefixes:
                self.RTK_CONFIGURATION.RTK_PREFIX = \
                    [_prefix for _prefix in _row]

            for _row in _actives:
                self.RTK_CONFIGURATION.RTK_MODULES = \
                    [_active for _active in _row]

            # TODO: Move this code to the ModuleBook.
            _message = _(u"Opening Program Database {0:s}"). \
                format(self.RTK_CONFIGURATION.RTK_PROG_INFO['database'])
            self.dic_books['moduleview'].statusbar.push(2, _message)
            self.dic_books['moduleview'].set_title(
                    _(u"RTK - Analyzing {0:s}").format(
                            self.RTK_CONFIGURATION.RTK_PROG_INFO['database']))

            # TODO: Where to put this code for the status icon?
            _icon = self.RTK_CONFIGURATION.RTK_ICON_DIR + \
                    '/32x32/db-connected.png'
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
            self.icoStatus.set_from_pixbuf(_icon)
            self.icoStatus.set_tooltip(
                    _(u"RTK is connected to program database "
                      u"{0:s}.".format(
                            self.RTK_CONFIGURATION.RTK_PROG_INFO['database'])))

            # TODO: Move this code to the ModuleBook.
            self.dic_books['moduleview'].statusbar.pop(2)

            self.RTK_CONFIGURATION.RTK_USER_LOG.info('RTK SUCCESS: Opening '
                                                     'RTK Program database '
                                                     '{0:s}.'. \
                                                     format(_database))
        else:
            self.RTK_CONFIGURATION.RTK_DEBUG_LOG.error('RTK ERROR: Failed to '
                                                       'open RTK Program '
                                                       'database {0:s}.'. \
                                                       format(_database))
            _return = True

        return _return

    def request_close_program(self):
        """
        Method to request the open RTK Program database be closed.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _icon = self.RTK_CONFIGURATION.RTK_ICON_DIR + \
                '32x32/db-disconnected.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        self.icoStatus.set_from_pixbuf(_icon)
        self.icoStatus.set_tooltip(_(u"RTK is not currently connected to a "
                                     u"project database."))

        return self.rtk_model.close_program()

    def request_save_program(self):
        """
        Method to request the open RTK Program database be saved.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        # TODO: Move this to the ModuleBook.
        _message = _(u"Saving Program Database {0:s}"). \
            format(self.RTK_CONFIGURATION.RTK_PROG_INFO['database'])
        self.dic_books['moduleview'].statusbar.push(2, _message)

        _return = self.rtk_model.save_program()

        # TODO: Move this to the ModuleBook.
        self.dic_books['moduleview'].statusbar.pop(2)

        return _return

    def request_validate_license(self):
        """
        Method to request the RTK license be validated.

        :return:
        """

        _return = False

        # Read the license file and compare to the product key in the site
        # database.  If they are not equal, quit the application.
        _license_file = self.RTK_CONFIGURATION.RTK_DATA_DIR + '/license.key'
        try:
            _license_file = open(_license_file, 'r')
        except IOError:
            Widgets.rtk_warning(_(u"Cannot find license file {0:s}.  If your "
                                  u"license file is elsewhere, please place "
                                  u"it in {1:s}.").format(
                    _license_file, self.RTK_CONFIGURATION.RTK_DATA_DIR))
            _return = True

        _license_key = _license_file.readline().rstrip('\n')
        _expire_date = _license_file.readline().rstrip('\n')
        _license_file.close()

        _error_code, _msg = self.rtk_model.validate_license(_license_key)
        if _error_code == 1:
            Widgets.rtk_error(_(u"Invalid license (Invalid key).  Your "
                                u"license key is incorrect.  Closing the RTK "
                                u"application."))
            _return = True
        elif _error_code == 2:
            Widgets.rtk_error(_(u"Invalid license (Expired).  Your license "
                                u"expired on {0:s}.  Closing the RTK "
                                u"application."). \
                              format(_expire_date.strftime('%Y-%d-%m')))
            _return = True

        return _return

    def __del__(self):
        del self

    def open_project(self):
        """
        Method to open an RTK Project database and load it into the views.
        """

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
