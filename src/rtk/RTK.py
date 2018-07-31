#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.RTK.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""This is the main program for the RTK application."""

import logging
import os
from datetime import date

from sqlalchemy.orm import scoped_session  # pylint: disable=E0401
from pubsub import pub  # pylint: disable=E0401
from treelib import Tree  # pylint: disable=E0401

# Import other RTK modules.
# pylint: disable=E0401
from Configuration import Configuration
import Utilities
from rtk.dao.DAO import DAO
from rtk.dao.commondb.RTKCategory import RTKCategory
from rtk.dao.commondb.RTKCondition import RTKCondition
from rtk.dao.commondb.RTKFailureMode import RTKFailureMode
from rtk.dao.commondb.RTKGroup import RTKGroup
from rtk.dao.commondb.RTKHazards import RTKHazards
from rtk.dao.commondb.RTKLoadHistory import RTKLoadHistory
from rtk.dao.commondb.RTKManufacturer import RTKManufacturer
from rtk.dao.commondb.RTKMeasurement import RTKMeasurement
from rtk.dao.commondb.RTKMethod import RTKMethod
from rtk.dao.commondb.RTKModel import RTKModel
from rtk.dao.commondb.RTKSiteInfo import RTKSiteInfo
from rtk.dao.commondb.RTKStakeholders import RTKStakeholders
from rtk.dao.commondb.RTKStatus import RTKStatus
from rtk.dao.commondb.RTKSubCategory import RTKSubCategory
from rtk.dao.commondb.RTKType import RTKType
from rtk.dao.commondb.RTKUser import RTKUser
from rtk.dao.commondb.RTKRPN import RTKRPN
from rtk.modules.revision import dtcRevision
from rtk.modules.usage import dtcUsageProfile
from rtk.modules.failure_definition import dtcFailureDefinition
from rtk.modules.function import dtcFunction
from rtk.modules.fmea import dtcFMEA
from rtk.modules.requirement import dtcRequirement
from rtk.modules.stakeholder import dtcStakeholder
from rtk.modules.hardware import dtcHardwareBoM
from rtk.modules.allocation import dtcAllocation
from rtk.modules.hazops import dtcHazardAnalysis
from rtk.modules.similar_item import dtcSimilarItem
from rtk.modules.pof import dtcPoF
from rtk.modules.validation import dtcValidation
from rtk.modules.options import dtcOptions
from rtk.modules.preferences import dtcPreferences

from rtk.gui.gtk.rtk.Widget import _, gtk
from rtk.gui.gtk import rtk
from rtk.gui.gtk.mwi import ListBook
from rtk.gui.gtk.mwi import ModuleBook
from rtk.gui.gtk.mwi import WorkBook

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2016 Andrew "weibullguy" Rowland'


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

    return (_debug_log, _user_log, _import_log)


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

    def do_create_program(self, database):
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

        if self.program_dao.db_create_program(database):
            _error_code = 1
            _msg = 'RTK ERROR: Failed to create RTK Program database {0:s}.'.\
                format(database)

        return _error_code, _msg

    def do_open_program(self, database):
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

    def do_close_program(self):
        """Close the open RTK Program database."""
        self.program_dao.db_close()

        return None

    def do_save_program(self):
        """
        Save the open RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = self.program_dao.db_update(self.program_session)

        return _error_code, _msg

    def do_delete_program(self):
        """
        Delete an existing RTK Program database.

        :return:
        """
        pass

    # pylint: disable=too-many-branches
    def do_load_globals(self, configuration):
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

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKCategory.                                 #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKCategory).\
                filter(RTKCategory.cat_type == 'action').all():
            _attributes = _record.get_attributes()
            configuration.RTK_ACTION_CATEGORY[_record.category_id] = (
                _attributes['name'], _attributes['description'],
                _attributes['category_type'], _attributes['value'])

        for _record in self.site_session.query(RTKCategory).\
                filter(RTKCategory.cat_type == 'incident').all():
            _attributes = _record.get_attributes()
            configuration.RTK_INCIDENT_CATEGORY[_record.category_id] = (
                _attributes['name'], _attributes['description'],
                _attributes['category_type'], _attributes['value'])

        for _record in self.site_session.query(RTKCategory).\
                filter(RTKCategory.cat_type == 'risk').all():
            _attributes = _record.get_attributes()
            configuration.RTK_SEVERITY[_record.category_id] = (
                _attributes['name'], _attributes['description'],
                _attributes['category_type'], _attributes['value'])

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKGroup.                                    #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKGroup).\
                filter(RTKGroup.group_type == 'affinity').all():
            _attributes = _record.get_attributes()
            configuration.RTK_AFFINITY_GROUPS[_record.group_id] = (
                _attributes['description'], _attributes['group_type'])

        for _record in self.site_session.query(RTKGroup).\
                filter(RTKGroup.group_type == 'workgroup').all():
            _attributes = _record.get_attributes()
            configuration.RTK_WORKGROUPS[_record.group_id] = (
                _attributes['description'], _attributes['group_type'])

        # ------------------------------------------------------------------- #
        # Load the dictionaries from RTKMethod.                               #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKMethod).\
                filter(RTKMethod.method_type == 'detection').all():
            _attributes = _record.get_attributes()
            configuration.RTK_DETECTION_METHODS[_record.method_id] = (
                _attributes['name'], _attributes['description'],
                _attributes['method_type'])

        # ------------------------------------------------------------------- #
        # Load the dictionaries from RTKModel.                                #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKModel).\
            filter(RTKModel.model_type == 'damage').all():
            _attributes = _record.get_attributes()
            configuration.RTK_DAMAGE_MODELS[_record.model_id] = (
                _attributes['description'], )

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKRPN.                                      #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKRPN).\
                filter(RTKRPN.rpn_type == 'detection').all():
            configuration.RTK_RPN_DETECTION[_record.value] = \
                _record.get_attributes()

        for _record in self.site_session.query(RTKRPN).\
                filter(RTKRPN.rpn_type == 'occurrence').all():
            configuration.RTK_RPN_OCCURRENCE[_record.value] = \
                _record.get_attributes()

        for _record in self.site_session.query(RTKRPN). \
                filter(RTKRPN.rpn_type == 'severity').all():
            configuration.RTK_RPN_SEVERITY[_record.value] = \
                _record.get_attributes()

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKStatus.                                   #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKStatus).\
                filter(RTKStatus.status_type == 'action').all():
            _attributes = _record.get_attributes()
            configuration.RTK_ACTION_STATUS[_record.status_id] = (
                _attributes['name'], _attributes['description'],
                _attributes['status_type'])

        for _record in self.site_session.query(RTKStatus).\
                filter(RTKStatus.status_type == 'incident').all():
            _attributes = _record.get_attributes()
            configuration.RTK_INCIDENT_STATUS[_record.status_id] = (
                _attributes['name'], _attributes['description'],
                _attributes['status_type'])

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKType.                                     #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKType).\
                filter(RTKType.type_type == 'incident').all():
            _attributes = _record.get_attributes()
            configuration.RTK_INCIDENT_TYPE[_record.type_id] = (
                _attributes['code'], _attributes['description'],
                _attributes['type_type'])

        for _record in self.site_session.query(RTKType).\
                filter(RTKType.type_type == 'requirement').all():
            _attributes = _record.get_attributes()
            configuration.RTK_REQUIREMENT_TYPE[_record.type_id] = (
                _attributes['code'], _attributes['description'],
                _attributes['type_type'])

        for _record in self.site_session.query(RTKType).\
                filter(RTKType.type_type == 'validation').all():
            _attributes = _record.get_attributes()
            configuration.RTK_VALIDATION_TYPE[_record.type_id] = (
                _attributes['code'], _attributes['description'],
                _attributes['type_type'])

        # ------------------------------------------------------------------- #
        # Load dictionaries from tables not requiring a filter.               #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RTKHazards).all():
            _attributes = _record.get_attributes()
            configuration.RTK_HAZARDS[_record.hazard_id] = (
                _attributes['category'], _attributes['subcategory'])

        for _record in self.site_session.query(RTKLoadHistory).all():
            _attributes = _record.get_attributes()
            configuration.RTK_LOAD_HISTORY[_record.history_id] = (
                _attributes['description'], )

        for _record in self.site_session.query(RTKManufacturer).all():
            _attributes = _record.get_attributes()
            configuration.RTK_MANUFACTURERS[_record.manufacturer_id] = (
                _attributes['description'], _attributes['location'],
                _attributes['cage_code'])

        for _record in self.site_session.query(RTKMeasurement).\
                filter(RTKMeasurement.measurement_type == 'unit').all():
            _attributes = _record.get_attributes()
            configuration.RTK_MEASUREMENT_UNITS[_record.measurement_id] = (
                _attributes['code'], _attributes['description'],
                _attributes['measurement_type'])

        for _record in self.site_session.query(RTKMeasurement).\
                filter(RTKMeasurement.measurement_type == 'damage').all():
            _attributes = _record.get_attributes()
            configuration.RTK_MEASURABLE_PARAMETERS[_record.measurement_id] = (
                _attributes['code'], _attributes['description'],
                _attributes['measurement_type'])

        for _record in self.site_session.query(RTKStakeholders).all():
            _attributes = _record.get_attributes()
            configuration.RTK_STAKEHOLDERS[_record.stakeholders_id] = (
                _attributes['stakeholder'], )

        for _record in self.site_session.query(RTKUser).all():
            _attributes = _record.get_attributes()
            configuration.RTK_USERS[_record.user_id] = (
                _attributes['user_lname'], _attributes['user_fname'],
                _attributes['user_email'], _attributes['user_phone'],
                _attributes['user_group_id'])

        return _return

    def do_validate_license(self, license_key):
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
                                    'allocation'
                                    'function'
                                    'hardware'
                                    'revision'
                                    'requirement'
                                    'validation'
                                    'survival'
                                    'matrices'
                                    'profile'
                                    'definition'
                                    'fmea'
                                    'stakeholder'
                                    'hazard'
                                    'similaritem'
                                    'pof'
                                    'growth'
                                    'options'
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

    def __init__(self, **kwargs):
        """Initialize an instance of the RTK data controller."""
        # Read the site configuration file.
        self.RTK_CONFIGURATION.set_site_variables()
        if self.RTK_CONFIGURATION.set_user_variables():
            _prompt = _(
                u"A user-specific configuration directory could not "
                u"be found at {0:s}.  You will be given the option to "
                u"create and populate this directory.  If you choose "
                u"not to, you will recieve this prompt every time you "
                u"execute RTK.  Would you like to create and populate "
                u"a user-specific configuration directory?").format(
                    self.RTK_CONFIGURATION.RTK_HOME_DIR + "/.config/RTK")
            _dialog = rtk.RTKMessageDialog(_prompt, '', 'question')
            _response = _dialog.do_run()
            _dialog.do_destroy()

            if _response == gtk.RESPONSE_YES:
                self.RTK_CONFIGURATION.create_user_configuration()

            self.RTK_CONFIGURATION.set_user_variables(first_run=False)

        self.RTK_CONFIGURATION.get_user_configuration()

        # Create loggers.
        (self.RTK_CONFIGURATION.RTK_DEBUG_LOG,
         self.RTK_CONFIGURATION.RTK_USER_LOG,
         self.RTK_CONFIGURATION.RTK_IMPORT_LOG) = \
            _initialize_loggers(self.RTK_CONFIGURATION)

        # Initialize private dictionary instance attributes.

        # Initialize private list instance attributes.
        self.__test = kwargs['test']
        self._lst_modules = [
            'function', 'requirement', 'hardware', 'validation'
        ]

        # Initialize private scalar instance attributes.

        # Initialize public dictionary instance attributes.
        self.dic_controllers = {
            'options': None,
            'allocation': None,
            'definition': None,
            'function': None,
            'revision': None,
            'requirement': None,
            'hardware': None,
            'validation': None,
            'matrices': None,
            'profile': None,
            'ffmea': None,
            'fmea': None,
            'stakeholder': None,
            'hazard': None,
            'similaritem': None,
            'pof': None,
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
        self.request_do_load_globals()

        # Create an Options module instance and read the Site options.
        self.dic_controllers['options'] = dtcOptions(
            self.rtk_model.program_dao,
            self.RTK_CONFIGURATION,
            site_dao=_dao,
            test=False)
        self.dic_controllers['options'].request_do_select_all(
            site=True, program=False)

        # Create a Preferences module instance and read the user preferences.
        self.dic_controllers['preferences'] = dtcPreferences(
            self.rtk_model.program_dao,
            self.RTK_CONFIGURATION,
            site_dao=_dao,
            test=False)
        self.dic_controllers['preferences'].request_do_select_all(
            site=True, user=True)

        # Validate the license.
        # if self._validate_license():
        #    sys.exit(2)

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

    def request_do_create_program(self):
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

        _error_code, _msg = self.rtk_model.do_create_program(_database)
        if _error_code == 0:
            self.request_open_program()
            self.RTK_CONFIGURATION.RTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('createdProgram')
        else:
            self.RTK_CONFIGURATION.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_do_load_globals(self):
        """
        Request to load all the global Configuration variables.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self.rtk_model.do_load_globals(self.RTK_CONFIGURATION)

    def request_do_open_program(self):
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
        _error_code, _msg = self.rtk_model.do_open_program(_database)
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
            self.dic_controllers['validation'] = dtcValidation(
                self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)
            self.dic_controllers['profile'] = dtcUsageProfile(
                self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)
            self.dic_controllers['definition'] = dtcFailureDefinition(
                self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)
            self.dic_controllers['ffmea'] = dtcFMEA(
                self.rtk_model.program_dao,
                self.RTK_CONFIGURATION,
                test=False,
                functional=True)
            self.dic_controllers['stakeholder'] = dtcStakeholder(
                self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)
            self.dic_controllers['allocation'] = dtcAllocation(
                self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)
            self.dic_controllers['hazops'] = dtcHazardAnalysis(
                self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)
            self.dic_controllers['similaritem'] = dtcSimilarItem(
                self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)
            self.dic_controllers['dfmeca'] = dtcFMEA(
                self.rtk_model.program_dao,
                self.RTK_CONFIGURATION,
                test=False,
                functional=False)
            self.dic_controllers['pof'] = dtcPoF(
                self.rtk_model.program_dao, self.RTK_CONFIGURATION, test=False)

            # Find which modules are active for the program being opened.
            self.dic_controllers['options'].request_do_select_all(
                site=False, program=True)
            _program_info = self.dic_controllers[
                'options'].request_get_options(site=False, program=True)
            self.RTK_CONFIGURATION.RTK_MODULES['function'] = \
                _program_info['function_active']
            self.RTK_CONFIGURATION.RTK_MODULES['requirement'] = \
                _program_info['requirement_active']
            self.RTK_CONFIGURATION.RTK_MODULES['hardware'] = \
                _program_info['hardware_active']
            self.RTK_CONFIGURATION.RTK_MODULES['validation'] = \
                _program_info['vandv_active']

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

    def request_do_close_program(self):
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

        if not self.rtk_model.do_close_program():
            self.loaded = False

        return self.loaded

    def request_do_save_program(self):
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

        _error_code, _msg = self.rtk_model.do_save_program()

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

    def request_do_validate_license(self):
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
            rtk_warning(
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
            rtk_error(
                _(u"Invalid license (Invalid key).  Your "
                  u"license key is incorrect.  Closing the RTK "
                  u"application."))
            _return = True
        elif _error_code == 2:
            # noinspection PyUnresolvedReferences
            rtk_error(
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
