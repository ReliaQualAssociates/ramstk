#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.RTK.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""This is the main program for the RTK application."""

import gettext
import logging
import os
import sys
from datetime import date

from sqlalchemy.orm import scoped_session  # pylint: disable=E0401
from pubsub import pub  # pylint: disable=E0401
from sortedcontainers import SortedDict  # pylint: disable=E0401
from treelib import Tree  # pylint: disable=E0401

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
# pylint: disable=E0401
from Configuration import Configuration
import Utilities
from rtk.dao.DAO import DAO
from rtk.dao.RTKProgramInfo import RTKProgramInfo
from rtk.dao.RTKApplication import RTKApplication
from rtk.dao.RTKCategory import RTKCategory
from rtk.dao.RTKCriticality import RTKCriticality
from rtk.dao.RTKDistribution import RTKDistribution
from rtk.dao.RTKEnviron import RTKEnviron
from rtk.dao.RTKFailureMode import RTKFailureMode
from rtk.dao.RTKGroup import RTKGroup
from rtk.dao.RTKHazards import RTKHazards
from rtk.dao.RTKLevel import RTKLevel
from rtk.dao.RTKManufacturer import RTKManufacturer
from rtk.dao.RTKMethod import RTKMethod
from rtk.dao.RTKModel import RTKModel
from rtk.dao.RTKPhase import RTKPhase
from rtk.dao.RTKRPN import RTKRPN
from rtk.dao.RTKSiteInfo import RTKSiteInfo
from rtk.dao.RTKStakeholders import RTKStakeholders
from rtk.dao.RTKStatus import RTKStatus
from rtk.dao.RTKSubCategory import RTKSubCategory
from rtk.dao.RTKType import RTKType
from rtk.dao.RTKUnit import RTKUnit
from rtk.dao.RTKUser import RTKUser
# from datamodels.matrix.Matrix import Matrix
from rtk.modules.revision import dtcRevision
from rtk.usage import dtcUsageProfile
from rtk.failure_definition import dtcFailureDefinition
from rtk.modules.function import dtcFunction
from rtk.modules.fmea import dtcFMEA
from rtk.requirement import dtcRequirement
from rtk.stakeholder import dtcStakeholder
from rtk.hardware import dtcHardwareBoM
from rtk.modules.allocation import dtcAllocation
# from rtk.modules.hazops import dtcHazard
# from rtk.modules.similar_item.SimilarItem import dtcSimilarItem
# from rtk.modules.pof import dtcPoF
# from rtk.software.BoM import BoM as SoftwareBoM
# from rtk.testing.Testing import Testing
# from rtk.testing.growth.Growth import Growth
from rtk.validation import dtcValidation
# from rtk.incident.Incident import Incident
# from rtk.incident.action.Action import Action
# from rtk.incident.component.Component import Component
# from rtk.survival.Survival import Survival

import rtk.gui.gtk.rtk.Widget as Widgets
from rtk.gui.gtk.mwi import ListBook
from rtk.gui.gtk.mwi import ModuleBook
from rtk.gui.gtk.mwi import WorkBook

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2016 Andrew "weibullguy" Rowland'

# Add localization support.
_ = gettext.gettext


def main():
    """Launch the RTK application."""
    # splScreen = SplashScreen()

    # If you don't do this, the splash screen will show, but wont render it's
    # contents
    # while gtk.events_pending():
    #     gtk.main_iteration()

    # sleep(3)
    RTK(test=False)

    # splScreen.window.destroy()

    gtk.main()

    return 0


def _initialize_loggers(configuration):
    """
    Create loggers for the RTK application.

    :param configuration: the RTK Configuration() object instance holding all
                          the configuration values for the current instance of
                          RTK.
    :type configuration: :class:`rtk.Configuration.Configuration()`
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
    """Raise error when no option is available in the configuration file."""

    pass


class Model(object):
    """
    This is the RTK data model class.

    The attributes of a RTK data model are:

    :ivar site_dao: the data access object used to communicate with the RTK
                    Common database.
    :type site_dao: :class:`rtk.dao.DAO.DAO()`
    :ivar program_dao: the data access object used to communicate with the RTK
                       Program database
    :type program_dao: :class:`rtk.dao.DAO.DAO()`
    """

    def __init__(self, sitedao, programdao):
        """
        Initialize an instance of the RTK data model.

        :param sitedao: the `:class:rtk.dao.DAO.DAO` instance connected to
                        the RTK Common database.
        :param programdao: the `:class:rtk.dao.DAO.DAO` instance connected
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
        site_session = self.site_dao.RTK_SESSION
        site_session.configure(
            bind=self.site_dao.engine, autoflush=False, expire_on_commit=False)
        self.site_session = scoped_session(site_session)
        self.program_session = None

    def create_program(self, database):
        """
        Create a new RTK Program database.

        :param str database: the RFC1738 URL path to the database to connect
                             with.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RTK SUCCESS: Creating RTK Program database {0:s}.'.\
            format(database)

        self.program_dao.db_connect(database)

        _session = scoped_session(self.program_dao.RTK_SESSION)
        _session.configure(
            bind=self.program_dao.engine,
            autoflush=False,
            expire_on_commit=False)

        if self.program_dao.db_create_program(database, _session):
            _error_code = 1001
            _msg = 'RTK ERROR: Failed to create RTK Program database {0:s}.'.\
                format(database)

        _session.close()

        return _error_code, _msg

    def read_program_info(self):
        """
        Read the program info table from the RTK Program database.

        :return: the list of RTKProgramInfo objects for each row in the
                 rtk_program_info table in the RTK Program database.
        :rtype: :class:`dao.RTKProgramInfo.RTKProgramInfo`
        """
        return self.program_session.query(RTKProgramInfo).all()

    def open_program(self, database):
        """
        Open an RTK Program database for analyses.

        :param str database: the RFC1738 URL path to the database to connect
                             with.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RTK SUCCESS: Opening RTK Program database {0:s}.'.\
            format(database)

        if not self.program_dao.db_connect(database):
            program_session = self.program_dao.RTK_SESSION
            program_session.configure(
                bind=self.program_dao.engine,
                autoflush=False,
                expire_on_commit=False)
            self.program_session = scoped_session(program_session)

        else:
            _error_code = 1001
            _msg = 'RTK ERROR: Failed to open RTK Program database {0:s}.'.\
                format(database)

        return _error_code, _msg

    def close_program(self):
        """Close the open RTK Program database."""
        self.program_dao.db_close()

        return None

    def save_program(self):
        """
        Save the open RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = self.program_dao.db_update(self.program_session)

        return _error_code, _msg

    def delete_program(self):
        """
        Delete an existing RTK Program database.

        :return:
        """
        pass

    # pylint: disable=too-many-branches
    def load_globals(self, configuration):
        """
        Load the RTK Program global constants.

        :param configuration: the currently active RTK Program Configuration()
                              object.
        :type configuration: :class:`rtk.Configuration.Configuration()`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # ------------------------------------------------------------------- #
        # Build the component category, component subcategory, failure modes  #
        # tree.                                                               #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKCategory).\
                filter(RTKCategory.cat_type == 'hardware').all():

            _subcats = {}
            configuration.RTK_FAILURE_MODES[_record.category_id] = {}

            for _subcat in self.site_session.query(RTKSubCategory).\
                    filter(RTKSubCategory.category_id == _record.category_id).\
                    all():
                _subcats[_subcat.subcategory_id] = _subcat.description

                _modes = {}
                configuration.RTK_FAILURE_MODES[_record.category_id][
                    _subcat.subcategory_id] = {}

                for _mode in self.site_session.query(RTKFailureMode).\
                        filter(RTKFailureMode.category_id == _record.category_id).\
                        filter(RTKFailureMode.subcategory_id == _subcat.subcategory_id).\
                        all():
                    _modes[_mode.mode_id] = [
                        _mode.description, _mode.mode_ratio, _mode.source
                    ]

                configuration.RTK_FAILURE_MODES[_record.category_id][
                    _subcat.subcategory_id] = _modes

            configuration.RTK_CATEGORIES[
                _record.category_id] = _record.description
            configuration.RTK_SUBCATEGORIES[_record.category_id] = _subcats

        for _record in self.site_session.query(RTKStakeholders).all():
            configuration.RTK_STAKEHOLDERS[_record.stakeholders_id] = \
                _record.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKCategory.                                 #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKCategory).\
                filter(RTKCategory.category_id == 'action').all():
            configuration.RTK_ACTION_CATEGORY[_record.category_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKCategory).\
                filter(RTKCategory.cat_type == 'incident').all():
            configuration.RTK_INCIDENT_CATEGORY[_record.category_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKCategory).\
                filter(RTKCategory.cat_type == 'risk').all():
            configuration.RTK_SEVERITY[_record.category_id] = \
                _record.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKEnviron.                                  #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKEnviron).\
                filter(RTKEnviron.environ_type == 'development').all():
            configuration.RTK_SW_DEV_ENVIRONMENTS[_record.environ_id] = \
                _record.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKGroup.                                    #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKGroup).\
                filter(RTKGroup.group_type == 'affinity').all():
            configuration.RTK_AFFINITY_GROUPS[_record.group_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKGroup).\
                filter(RTKGroup.group_type == 'workgroup').all():
            configuration.RTK_WORKGROUPS[_record.group_id] = \
                _record.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKLevel.                                    #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKLevel).\
                filter(RTKLevel.level_type == 'probability').all():
            configuration.RTK_FAILURE_PROBABILITY[_record.level_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKLevel).\
                filter(RTKLevel.level_type == 'software').all():
            configuration.RTK_SW_LEVELS[_record.level_id] = \
                _record.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load the dictionaries from RTKMethod.                               #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKMethod).\
                filter(RTKMethod.method_type == 'detection').all():
            configuration.RTK_DETECTION_METHODS[_record.method_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKMethod).\
                filter(RTKMethod.method_type == 'test').all():
            configuration.RTK_SW_TEST_METHODS[_record.method_id] = \
                _record.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKModel.                                    #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKModel).\
                filter(RTKModel.model_type == 'allocation').all():
            configuration.RTK_ALLOCATION_MODELS[_record.model_id] = \
                _record.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load the dictionaries from RTKPhase.                                #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKPhase).\
                filter(RTKPhase.phase_type == 'lifecycle').all():
            configuration.RTK_LIFECYCLE[_record.phase_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKPhase).\
                filter(RTKPhase.phase_type == 'development').all():
            configuration.RTK_SW_DEV_PHASES[_record.phase_id] = \
                _record.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKRPN.                                      #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKRPN).\
                filter(RTKRPN.rpn_type == 'detection').all():
            configuration.RTK_RPN_DETECTION[_record.rpn_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKRPN).\
                filter(RTKRPN.rpn_type == 'occurrence').all():
            configuration.RTK_RPN_OCCURRENCE[_record.rpn_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKRPN). \
                filter(RTKRPN.rpn_type == 'severity').all():
            configuration.RTK_RPN_SEVERITY[_record.rpn_id] = \
                _record.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKStatus.                                   #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKStatus).\
                filter(RTKStatus.status_type == 'action').all():
            configuration.RTK_ACTION_STATUS[_record.status_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKStatus).\
                filter(RTKStatus.status_type == 'incident').all():
            configuration.RTK_INCIDENT_STATUS[_record.status_id] = \
                _record.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKType.                                     #
        # ------------------------------------------------------------------- #
        configuration.RTK_CONTROL_TYPES = [_(u"Prevention"), _(u"Detection")]

        for _record in self.site_session.query(RTKType). \
                filter(RTKType.type_type == 'cost').all():
            configuration.RTK_COST_TYPE[_record.type_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKType).\
                filter(RTKType.type_type == 'incident').all():
            configuration.RTK_INCIDENT_TYPE[_record.type_id] = \
                _record.get_attributes[1:]

        for _record in self.site_session.query(RTKType).\
                filter(RTKType.type_type == 'mttr').all():
            configuration.RTK_MTTR_TYPE[_record.type_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKType).\
                filter(RTKType.type_type == 'requirement').all():
            configuration.RTK_REQUIREMENT_TYPE[_record.type_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKType).\
                filter(RTKType.type_type == 'validation').all():
            configuration.RTK_VALIDATION_TYPE[_record.type_id] = \
                _record.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from tables not requiring a filter.               #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKApplication).all():
            configuration.RTK_SW_APPLICATION[_record.application_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKCriticality).all():
            configuration.RTK_CRITICALITY[_record.criticality_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKDistribution).all():
            configuration.RTK_S_DIST[_record.distribution_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKHazards).all():
            configuration.RTK_HAZARDS[_record.hazard_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKManufacturer).all():
            configuration.RTK_MANUFACTURERS[_record.manufacturer_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKUnit).\
                filter(RTKUnit.unit_type == 'measurement').all():
            configuration.RTK_MEASUREMENT_UNITS[_record.unit_id] = \
                _record.get_attributes()[1:]

        for _record in self.site_session.query(RTKUser).all():
            configuration.RTK_USERS[_record.user_id] = \
                _record.get_attributes()[1:]

        return _return

    def validate_license(self, license_key):
        """
        Validate the license and the license expiration date.

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
    Class representing the RTK data controller.

    This is the master controller for the entire RTK application.  Attributes
    of an RTK data controller are:

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

    :ivar rtk_model: the instance of :class:`rtk.RTK.Model` managed by this
                     data controller.
    """

    RTK_CONFIGURATION = Configuration()

    def __init__(self, **kwargs):  # pylint: disable=R0914
        """Initialize an instance of the RTK data controller."""
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
        self.__test = kwargs['test']
        self._lst_modules = [
            'revision', 'function', 'requirement', 'hardware', 'software',
            'testing', 'validation', 'incident', 'survival'
        ]

        # Initialize private scalar instance attributes.

        # Initialize public dictionary instance attributes.
        self.dic_controllers = {
            'revision': None,
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
            'ffmea': None,
            'fmea': None,
            'stakeholder': None,
            'allocation': None,
            'hazard': None,
            'similaritem': None,
            'pof': None,
            'growth': None,
            'action': None,
            'component': None
        }
        self.dic_books = {
            'listbook': None,
            'modulebook': None,
            'workbook': None
        }

        # Define public list attributes.

        # Define public scalar attributes.
        self.icoStatus = gtk.StatusIcon()
        self.loaded = False

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
            self.dic_books['listbook'] = ListBook(self)
            self.dic_books['modulebook'] = ModuleBook(self)
            self.dic_books['workbook'] = WorkBook(self)

        _icon = self.RTK_CONFIGURATION.RTK_ICON_DIR + \
            '/32x32/db-disconnected.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        self.icoStatus.set_from_pixbuf(_icon)
        self.icoStatus.set_tooltip(
            _(u"RTK is not currently connected to a "
              u"project database."))

    def request_create_program(self):
        """
        Request a new RTK Program database be created.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _database = None

        if self.RTK_CONFIGURATION.RTK_BACKEND == 'sqlite':
            _database = self.RTK_CONFIGURATION.RTK_BACKEND + ':///' + \
                self.RTK_CONFIGURATION.RTK_PROG_INFO['database']

        _error_code, _msg = self.rtk_model.create_program(_database)
        if _error_code == 0:
            self.request_open_program()
            self.RTK_CONFIGURATION.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('createdProgram')
        else:
            self.RTK_CONFIGURATION.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_load_globals(self):
        """
        Request to load all the global Configuration variables.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self.rtk_model.load_globals(self.RTK_CONFIGURATION)

    def request_open_program(self):
        """
        Request an RTK Program database be opened for analyses.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _database = None

        if self.RTK_CONFIGURATION.RTK_BACKEND == 'sqlite':
            _database = self.RTK_CONFIGURATION.RTK_BACKEND + ':///' + \
                self.RTK_CONFIGURATION.RTK_PROG_INFO['database']

        # If the database was successfully opened, create an instance of each
        # of the slave data controllers.
        _error_code, _msg = self.rtk_model.open_program(_database)
        if _error_code == 0:
            pub.sendMessage('requestOpen')
            self.dic_controllers['revision'] = dtcRevision(
                self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)
            self.dic_controllers['function'] = dtcFunction(
                self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)
            self.dic_controllers['requirement'] = dtcRequirement(
                self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)
            self.dic_controllers['hardware'] = dtcHardwareBoM(
                self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)
            # self.dic_controllers['software'] = SoftwareBoM()
            # self.dic_controllers['test'] = Test()
            self.dic_controllers['validation'] = dtcValidation(
                self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)
            # self.dic_controllers['incident'] = Incident()
            # self.dic_controllers['survival'] = Survival()

            # self.dic_controllers['matrices'] = Matrix()
            self.dic_controllers['profile'] = dtcUsageProfile(
                self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)
            self.dic_controllers['definition'] = dtcFailureDefinition(
                self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)
            self.dic_controllers['ffmea'] = dtcFMEA(
                self.rtk_model.program_dao,
                self.RTK_CONFIGURATION,
                test=False,
                functional=True)
            # self.dic_controllers['fmea'] = FMEA()
            self.dic_controllers['stakeholder'] = dtcStakeholder(
                self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)
            self.dic_controllers['allocation'] = Allocation(
               self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)
            # self.dic_controllers['hazard'] = Hazard()
            # self.dic_controllers['similaritem'] = SimilarItem()
            # self.dic_controllers['pof'] = PoF()
            # self.dic_controllers['growth'] = Growth()
            # self.dic_controllers['action'] = Action()
            # self.dic_controllers['component'] = Component()
            _program_info = self.rtk_model.read_program_info()[0]

            self.RTK_CONFIGURATION.RTK_PREFIX['revision'] = \
                [_program_info.revision_prefix, _program_info.revision_next_id]
            self.RTK_CONFIGURATION.RTK_PREFIX['function'] = \
                [_program_info.function_prefix, _program_info.function_next_id]
            self.RTK_CONFIGURATION.RTK_PREFIX['requirement'] = \
                [_program_info.requirement_prefix,
                 _program_info.requirement_next_id]
            self.RTK_CONFIGURATION.RTK_PREFIX['assembly'] = \
                [_program_info.assembly_prefix, _program_info.assembly_next_id]
            self.RTK_CONFIGURATION.RTK_PREFIX['part'] = \
                [_program_info.part_prefix, _program_info.part_next_id]
            self.RTK_CONFIGURATION.RTK_PREFIX['fmeca'] = \
                [_program_info.fmeca_prefix, _program_info.fmeca_next_id]
            self.RTK_CONFIGURATION.RTK_PREFIX['mode'] = \
                [_program_info.mode_prefix, _program_info.mode_next_id]
            self.RTK_CONFIGURATION.RTK_PREFIX['effect'] = \
                [_program_info.effect_prefix, _program_info.effect_next_id]
            self.RTK_CONFIGURATION.RTK_PREFIX['cause'] = \
                [_program_info.cause_prefix, _program_info.cause_next_id]
            self.RTK_CONFIGURATION.RTK_PREFIX['software'] = \
                [_program_info.software_prefix, _program_info.software_next_id]

            self.RTK_CONFIGURATION.RTK_MODULES['revision'] = \
                _program_info.revision_active
            self.RTK_CONFIGURATION.RTK_MODULES['function'] = \
                _program_info.function_active
            self.RTK_CONFIGURATION.RTK_MODULES['requirement'] = \
                _program_info.requirement_active
            self.RTK_CONFIGURATION.RTK_MODULES['hardware'] = \
                _program_info.hardware_active
            self.RTK_CONFIGURATION.RTK_MODULES['software'] = \
                _program_info.software_active
            self.RTK_CONFIGURATION.RTK_MODULES['testing'] = \
                _program_info.testing_active
            self.RTK_CONFIGURATION.RTK_MODULES['validation'] = \
                _program_info.vandv_active
            self.RTK_CONFIGURATION.RTK_MODULES['incident'] = \
                _program_info.fraca_active
            self.RTK_CONFIGURATION.RTK_MODULES['survival'] = \
                _program_info.survival_active
            self.RTK_CONFIGURATION.RTK_MODULES['rcm'] = \
                _program_info.rcm_active
            self.RTK_CONFIGURATION.RTK_MODULES['rbd'] = \
                _program_info.rbd_active
            self.RTK_CONFIGURATION.RTK_MODULES['fta'] = \
                _program_info.fta_active

            _page = 0
            for _module in self._lst_modules:
                if self.RTK_CONFIGURATION.RTK_MODULES[_module] == 1:
                    self.RTK_CONFIGURATION.RTK_PAGE_NUMBER[_page] = _module
                    _page += 1

            # TODO: Where to put this code for the status icon?
            _icon = self.RTK_CONFIGURATION.RTK_ICON_DIR + \
                '/32x32/db-connected.png'
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
            self.icoStatus.set_from_pixbuf(_icon)
            self.icoStatus.set_tooltip(
                _(u"RTK is connected to program database "
                  u"{0:s}.".format(
                      self.RTK_CONFIGURATION.RTK_PROG_INFO['database'])))

            self.loaded = True

            self.RTK_CONFIGURATION.RTK_USER_LOG.info(_msg)
            if not self.__test:
                pub.sendMessage('openedProgram')

        else:
            self.RTK_CONFIGURATION.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_close_program(self):
        """
        Request the open RTK Program database be closed.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _icon = self.RTK_CONFIGURATION.RTK_ICON_DIR + \
            '/32x32/db-disconnected.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        self.icoStatus.set_from_pixbuf(_icon)
        self.icoStatus.set_tooltip(
            _(u"RTK is not currently connected to a "
              u"project database."))

        if not self.__test:
            pub.sendMessage('closedProgram')

        return self.rtk_model.close_program()

    def request_save_program(self):
        """
        Request the open RTK Program database be saved.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # TODO: Move this to the ModuleBook.
        _message = _(u"Saving Program Database {0:s}"). \
            format(self.RTK_CONFIGURATION.RTK_PROG_INFO['database'])
        self.dic_books['modulebook'].statusbar.push(2, _message)

        _error_code, _msg = self.rtk_model.save_program()

        if _error_code == 0:
            self.RTK_CONFIGURATION.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('savedProgram')
        else:
            self.RTK_CONFIGURATION.RTK_DEBUG_LOG.error(_msg)
            _return = True

        # TODO: Move this to the ModuleBook.
        self.dic_books['modulebook'].statusbar.pop(2)

        return _return

    def request_validate_license(self):
        """
        Request the RTK license be validated.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Read the license file and compare to the product key in the site
        # database.  If they are not equal, quit the application.
        _license_file = self.RTK_CONFIGURATION.RTK_DATA_DIR + '/license.key'
        try:
            _license_file = open(_license_file, 'r')
        except IOError:
            Widgets.rtk_warning(
                _(u"Cannot find license file {0:s}.  If your "
                  u"license file is elsewhere, please place "
                  u"it in {1:s}.").format(_license_file,
                                          self.RTK_CONFIGURATION.RTK_DATA_DIR))
            _return = True

        _license_key = _license_file.readline().rstrip('\n')
        _expire_date = _license_file.readline().rstrip('\n')
        _license_file.close()

        _error_code, _msg = self.rtk_model.validate_license(_license_key)
        if _error_code == 1:
            Widgets.rtk_error(
                _(u"Invalid license (Invalid key).  Your "
                  u"license key is incorrect.  Closing the RTK "
                  u"application."))
            _return = True
        elif _error_code == 2:
            # noinspection PyUnresolvedReferences
            Widgets.rtk_error(
                _(u"Invalid license (Expired).  Your license "
                  u"expired on {0:s}.  Closing the RTK "
                  u"application.").format(_expire_date.strftime('%Y-%d-%m')))
            _return = True

        return _return

    def __del__(self):
        """Delete the running instance of RTK."""
        del self


if __name__ == '__main__':
    main()
