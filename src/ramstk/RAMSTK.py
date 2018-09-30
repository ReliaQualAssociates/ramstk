#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ramstk.RAMSTK.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""This is the main program for the RAMSTK application."""

import logging
import os
from datetime import date

from sqlalchemy.orm import scoped_session  # pylint: disable=E0401
from pubsub import pub  # pylint: disable=E0401
from treelib import Tree  # pylint: disable=E0401

# Import other RAMSTK modules.
# pylint: disable=E0401
from Configuration import Configuration
import Utilities
from ramstk.dao.DAO import DAO
from ramstk.dao.commondb.RAMSTKCategory import RAMSTKCategory
from ramstk.dao.commondb.RAMSTKFailureMode import RAMSTKFailureMode
from ramstk.dao.commondb.RAMSTKGroup import RAMSTKGroup
from ramstk.dao.commondb.RAMSTKHazards import RAMSTKHazards
from ramstk.dao.commondb.RAMSTKLoadHistory import RAMSTKLoadHistory
from ramstk.dao.commondb.RAMSTKManufacturer import RAMSTKManufacturer
from ramstk.dao.commondb.RAMSTKMeasurement import RAMSTKMeasurement
from ramstk.dao.commondb.RAMSTKMethod import RAMSTKMethod
from ramstk.dao.commondb.RAMSTKModel import RAMSTKModel
from ramstk.dao.commondb.RAMSTKSiteInfo import RAMSTKSiteInfo
from ramstk.dao.commondb.RAMSTKStakeholders import RAMSTKStakeholders
from ramstk.dao.commondb.RAMSTKStatus import RAMSTKStatus
from ramstk.dao.commondb.RAMSTKSubCategory import RAMSTKSubCategory
from ramstk.dao.commondb.RAMSTKType import RAMSTKType
from ramstk.dao.commondb.RAMSTKUser import RAMSTKUser
from ramstk.dao.commondb.RAMSTKRPN import RAMSTKRPN
from ramstk.modules.revision import dtcRevision
from ramstk.modules.usage import dtcUsageProfile
from ramstk.modules.failure_definition import dtcFailureDefinition
from ramstk.modules.function import dtcFunction
from ramstk.modules.fmea import dtcFMEA
from ramstk.modules.requirement import dtcRequirement
from ramstk.modules.stakeholder import dtcStakeholder
from ramstk.modules.hardware import dtcHardwareBoM
from ramstk.modules.allocation import dtcAllocation
from ramstk.modules.hazops import dtcHazardAnalysis
from ramstk.modules.similar_item import dtcSimilarItem
from ramstk.modules.pof import dtcPoF
from ramstk.modules.validation import dtcValidation
from ramstk.modules.options import dtcOptions
from ramstk.modules.preferences import dtcPreferences
from ramstk.modules.imports import dtcImports
from ramstk.modules.exports import dtcExports

from ramstk.gui.gtk.ramstk.Widget import _, gtk
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.mwi import ListBook
from ramstk.gui.gtk.mwi import ModuleBook
from ramstk.gui.gtk.mwi import WorkBook

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2016 Doyle "weibullguy" Rowland'


def main():
    """Launch the RAMSTK application."""
    # splScreen = SplashScreen()

    # If you don't do this, the splash screen will show, but wont render it's
    # contents
    # while gtk.events_pending():
    #     gtk.main_iteration()

    # sleep(3)
    RAMSTK(test=False)

    # splScreen.window.destroy()

    gtk.main()

    return 0


def _initialize_loggers(configuration):
    """
    Create loggers for the RAMSTK application.

    :param configuration: the RAMSTK Configuration() object instance holding all
                          the configuration values for the current instance of
                          RAMSTK.
    :type configuration: :class:`ramstk.Configuration.Configuration()`
    :return: (_debug_log, _user_log, _import_log)
    :rtype: tuple
    """
    # Create loggers for the application.  The first is to store log
    # information for RAMSTK developers.  The second is to log errors for the
    # user.  The user can use these errors to help find problems with their
    # inputs and sich.  The third is for logging errors encountered when
    # importing data to RAMSTK.
    __error_log = configuration.RAMSTK_LOG_DIR + '/RAMSTK_debug.log'
    __user_log = configuration.RAMSTK_LOG_DIR + '/RAMSTK_user.log'
    __import_log = configuration.RAMSTK_LOG_DIR + '/RAMSTK_import.log'

    if not Utilities.dir_exists(configuration.RAMSTK_LOG_DIR):
        os.makedirs(configuration.RAMSTK_LOG_DIR)

    if Utilities.file_exists(__user_log):
        try:
            os.remove(__user_log)
        except WindowsError as _error:
            print("Could not delete {0:s} because {1:s}.").format(
                __user_log, _error)
    if Utilities.file_exists(__error_log):
        try:
            os.remove(__error_log)
        except WindowsError as _error:
            print("Could not delete {0:s} because {1:s}.").format(
                __user_log, _error)
    if Utilities.file_exists(__import_log):
        try:
            os.remove(__import_log)
        except WindowsError as _error:
            print("Could not delete {0:s} because {1:s}.").format(
                __user_log, _error)

    _debug_log = Utilities.create_logger("RAMSTK.debug", logging.DEBUG,
                                         __error_log)
    _user_log = Utilities.create_logger("RAMSTK.user", logging.WARNING,
                                        __user_log)
    _import_log = Utilities.create_logger("RAMSTK.import", logging.WARNING,
                                          __import_log)

    return (_debug_log, _user_log, _import_log)


class NoOptionError(Exception):
    """Raise error when no option is available in the configuration file."""

    pass


class Model(object):
    """
    This is the RAMSTK data model class.

    The attributes of a RAMSTK data model are:

    :ivar site_dao: the data access object used to communicate with the RAMSTK
                    Common database.
    :type site_dao: :class:`ramstk.dao.DAO.DAO()`
    :ivar program_dao: the data access object used to communicate with the RAMSTK
                       Program database
    :type program_dao: :class:`ramstk.dao.DAO.DAO()`
    """

    def __init__(self, sitedao, programdao):
        """
        Initialize an instance of the RAMSTK data model.

        :param sitedao: the `:class:ramstk.dao.DAO.DAO` instance connected to
                        the RAMSTK Common database.
        :param programdao: the `:class:ramstk.dao.DAO.DAO` instance connected
                           to the RAMSTK Program database.
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

        # Create a session for communicating with the RAMSTK Common database
        site_session = self.site_dao.RAMSTK_SESSION
        site_session.configure(
            bind=self.site_dao.engine, autoflush=False, expire_on_commit=False)
        self.site_session = scoped_session(site_session)
        self.program_session = None

    def do_create_program(self, database):
        """
        Create a new RAMSTK Program database.

        :param str database: the RFC1738 URL path to the database to connect
                             with.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RAMSTK SUCCESS: Creating RAMSTK Program database {0:s}.'.\
            format(database)

        if self.program_dao.db_create_program(database):
            _error_code = 1
            _msg = 'RAMSTK ERROR: Failed to create RAMSTK Program database ' \
                   '{0:s}.'.format(database)

        return _error_code, _msg

    def do_open_program(self, database):
        """
        Open an RAMSTK Program database for analyses.

        :param str database: the RFC1738 URL path to the database to connect
                             with.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RAMSTK SUCCESS: Opening RAMSTK Program database {0:s}.'.\
            format(database)

        if not self.program_dao.db_connect(database):
            program_session = self.program_dao.RAMSTK_SESSION
            program_session.configure(
                bind=self.program_dao.engine,
                autoflush=False,
                expire_on_commit=False)
            self.program_session = scoped_session(program_session)

        else:
            _error_code = 1001
            _msg = ('RAMSTK ERROR: Failed to open RAMSTK Program '
                    'database {0:s}.').format(database)

        return _error_code, _msg

    def do_close_program(self):
        """Close the open RAMSTK Program database."""
        self.program_dao.db_close()

        return None

    def do_save_program(self):
        """
        Save the open RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = self.program_dao.db_update(self.program_session)

        return _error_code, _msg

    def do_delete_program(self):
        """
        Delete an existing RAMSTK Program database.

        :return:
        """
        pass

    # pylint: disable=too-many-branches
    def do_load_globals(self, configuration):
        """
        Load the RAMSTK Program global constants.

        :param configuration: the currently active RAMSTK Program Configuration()
                              object.
        :type configuration: :class:`ramstk.Configuration.Configuration()`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # ------------------------------------------------------------------- #
        # Build the component category, component subcategory, failure modes  #
        # tree.                                                               #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RAMSTKCategory).\
                filter(RAMSTKCategory.cat_type == 'hardware').all():

            _subcats = {}
            configuration.RAMSTK_FAILURE_MODES[_record.category_id] = {}

            for _subcat in self.site_session.query(RAMSTKSubCategory).\
                    filter(RAMSTKSubCategory.category_id == _record.category_id).\
                    all():
                _subcats[_subcat.subcategory_id] = _subcat.description

                _modes = {}
                configuration.RAMSTK_FAILURE_MODES[_record.category_id][
                    _subcat.subcategory_id] = {}

                for _mode in self.site_session.query(RAMSTKFailureMode).\
                        filter(RAMSTKFailureMode.category_id == _record.category_id).\
                        filter(RAMSTKFailureMode.subcategory_id == _subcat.subcategory_id).\
                        all():
                    _modes[_mode.mode_id] = [
                        _mode.description, _mode.mode_ratio, _mode.source
                    ]

                configuration.RAMSTK_FAILURE_MODES[_record.category_id][
                    _subcat.subcategory_id] = _modes

            configuration.RAMSTK_CATEGORIES[
                _record.category_id] = _record.description
            configuration.RAMSTK_SUBCATEGORIES[_record.category_id] = _subcats

        # ------------------------------------------------------------------- #
        # Load dictionaries from RAMSTKCategory.                                 #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RAMSTKCategory).\
                filter(RAMSTKCategory.cat_type == 'action').all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_ACTION_CATEGORY[_record.category_id] = (
                _attributes['name'], _attributes['description'],
                _attributes['category_type'], _attributes['value'])

        for _record in self.site_session.query(RAMSTKCategory).\
                filter(RAMSTKCategory.cat_type == 'incident').all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_INCIDENT_CATEGORY[_record.category_id] = (
                _attributes['name'], _attributes['description'],
                _attributes['category_type'], _attributes['value'])

        for _record in self.site_session.query(RAMSTKCategory).\
                filter(RAMSTKCategory.cat_type == 'risk').all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_SEVERITY[_record.category_id] = (
                _attributes['name'], _attributes['description'],
                _attributes['category_type'], _attributes['value'])

        # ------------------------------------------------------------------- #
        # Load dictionaries from RAMSTKGroup.                                    #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RAMSTKGroup).\
                filter(RAMSTKGroup.group_type == 'affinity').all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_AFFINITY_GROUPS[_record.group_id] = (
                _attributes['description'], _attributes['group_type'])

        for _record in self.site_session.query(RAMSTKGroup).\
                filter(RAMSTKGroup.group_type == 'workgroup').all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_WORKGROUPS[_record.group_id] = (
                _attributes['description'], _attributes['group_type'])

        # ------------------------------------------------------------------- #
        # Load the dictionaries from RAMSTKMethod.                               #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RAMSTKMethod).\
                filter(RAMSTKMethod.method_type == 'detection').all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_DETECTION_METHODS[_record.method_id] = (
                _attributes['name'], _attributes['description'],
                _attributes['method_type'])

        # ------------------------------------------------------------------- #
        # Load the dictionaries from RAMSTKModel.                                #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RAMSTKModel).\
            filter(RAMSTKModel.model_type == 'damage').all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_DAMAGE_MODELS[_record.model_id] = (
                _attributes['description'], )

        # ------------------------------------------------------------------- #
        # Load dictionaries from RAMSTKRPN.                                      #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RAMSTKRPN).\
                filter(RAMSTKRPN.rpn_type == 'detection').all():
            configuration.RAMSTK_RPN_DETECTION[_record.value] = \
                _record.get_attributes()

        for _record in self.site_session.query(RAMSTKRPN).\
                filter(RAMSTKRPN.rpn_type == 'occurrence').all():
            configuration.RAMSTK_RPN_OCCURRENCE[_record.value] = \
                _record.get_attributes()

        for _record in self.site_session.query(RAMSTKRPN). \
                filter(RAMSTKRPN.rpn_type == 'severity').all():
            configuration.RAMSTK_RPN_SEVERITY[_record.value] = \
                _record.get_attributes()

        # ------------------------------------------------------------------- #
        # Load dictionaries from RAMSTKStatus.                                   #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RAMSTKStatus).\
                filter(RAMSTKStatus.status_type == 'action').all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_ACTION_STATUS[_record.status_id] = (
                _attributes['name'], _attributes['description'],
                _attributes['status_type'])

        for _record in self.site_session.query(RAMSTKStatus).\
                filter(RAMSTKStatus.status_type == 'incident').all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_INCIDENT_STATUS[_record.status_id] = (
                _attributes['name'], _attributes['description'],
                _attributes['status_type'])

        # ------------------------------------------------------------------- #
        # Load dictionaries from RAMSTKType.                                     #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RAMSTKType).\
                filter(RAMSTKType.type_type == 'incident').all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_INCIDENT_TYPE[_record.type_id] = (
                _attributes['code'], _attributes['description'],
                _attributes['type_type'])

        for _record in self.site_session.query(RAMSTKType).\
                filter(RAMSTKType.type_type == 'requirement').all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_REQUIREMENT_TYPE[_record.type_id] = (
                _attributes['code'], _attributes['description'],
                _attributes['type_type'])

        for _record in self.site_session.query(RAMSTKType).\
                filter(RAMSTKType.type_type == 'validation').all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_VALIDATION_TYPE[_record.type_id] = (
                _attributes['code'], _attributes['description'],
                _attributes['type_type'])

        # ------------------------------------------------------------------- #
        # Load dictionaries from tables not requiring a filter.               #
        # ------------------------------------------------------------------- #
        for _record in self.site_session.query(RAMSTKHazards).all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_HAZARDS[_record.hazard_id] = (
                _attributes['category'], _attributes['subcategory'])

        for _record in self.site_session.query(RAMSTKLoadHistory).all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_LOAD_HISTORY[_record.history_id] = (
                _attributes['description'], )

        for _record in self.site_session.query(RAMSTKManufacturer).all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_MANUFACTURERS[_record.manufacturer_id] = (
                _attributes['description'], _attributes['location'],
                _attributes['cage_code'])

        for _record in self.site_session.query(RAMSTKMeasurement).\
                filter(RAMSTKMeasurement.measurement_type == 'unit').all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_MEASUREMENT_UNITS[_record.measurement_id] = (
                _attributes['code'], _attributes['description'],
                _attributes['measurement_type'])

        for _record in self.site_session.query(RAMSTKMeasurement).\
                filter(RAMSTKMeasurement.measurement_type == 'damage').all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_MEASURABLE_PARAMETERS[
                _record.measurement_id] = (_attributes['code'],
                                           _attributes['description'],
                                           _attributes['measurement_type'])

        for _record in self.site_session.query(RAMSTKStakeholders).all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_STAKEHOLDERS[_record.stakeholders_id] = (
                _attributes['stakeholder'], )

        for _record in self.site_session.query(RAMSTKUser).all():
            _attributes = _record.get_attributes()
            configuration.RAMSTK_USERS[_record.user_id] = (
                _attributes['user_lname'], _attributes['user_fname'],
                _attributes['user_email'], _attributes['user_phone'],
                _attributes['user_group_id'])

        return _return

    def do_validate_license(self, license_key):
        """
        Validate the license and the license expiration date.

        :param str license_key: the license key for the current RAMSTK
                                installation.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RAMSTK SUCCESS: Validating RAMSTK License.'

        _site_info = self.site_session.query(RAMSTKSiteInfo).first()

        if license_key != _site_info.product_key:
            _error_code = 1
            _msg = 'RAMSTK ERROR: Invalid license (Invalid key).  Your license ' \
                   'key is incorrect.  Closing the RAMSTK application.'

        _today = date.today().strftime('%Y-%m-%d')
        _expire_date = _site_info.expire_on.strftime('%Y-%m-%d')
        if _today > _expire_date:
            _error_code = 2
            _msg = 'RAMSTK ERROR: Invalid license (Expired).  Your license ' \
                   'expired on {0:s}.  Closing the RAMSTK application.'. \
                format(_expire_date)

        return _error_code, _msg


class RAMSTK(object):
    """
    Class representing the RAMSTK data controller.

    This is the master controller for the entire RAMSTK application.  Attributes
    of an RAMSTK data controller are:

    :ivar dict dic_controllers: dictionary of data controllers available in the
                                running instance of RAMSTK.

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
                                    'imports'
                                Values are the instance of each RAMSTK data
                                controller.

    :ivar dict dic_books: dictionary of GUI books used by the running instance
                          of RAMSTK.

                          Keys are:
                              'listbook'
                              'modulebook'
                              'workbook'
                          Values are the instance of each RAMSTK book.

    :ivar ramstk_model: the instance of :class:`ramstk.RAMSTK.Model` managed by this
                     data controller.
    """
    RAMSTK_CONFIGURATION = Configuration()

    def __init__(self, **kwargs):
        """Initialize an instance of the RAMSTK data controller."""
        # Read the site configuration file.
        self.RAMSTK_CONFIGURATION.set_site_variables()
        if self.RAMSTK_CONFIGURATION.set_user_variables():
            _prompt = _(
                u"A user-specific configuration directory could not "
                u"be found at {0:s}.  You will be given the option to "
                u"create and populate this directory.  If you choose "
                u"not to, you will recieve this prompt every time you "
                u"execute RAMSTK.  Would you like to create and populate "
                u"a user-specific configuration directory?").format(
                    self.RAMSTK_CONFIGURATION.RAMSTK_HOME_DIR +
                    "/.config/RAMSTK")
            _dialog = ramstk.RAMSTKMessageDialog(_prompt, '', 'question')
            _response = _dialog.do_run()
            _dialog.do_destroy()

            if _response == gtk.RESPONSE_YES:
                self.RAMSTK_CONFIGURATION.create_user_configuration()

            self.RAMSTK_CONFIGURATION.set_user_variables(first_run=False)

        self.RAMSTK_CONFIGURATION.get_user_configuration()

        # Create loggers.
        (self.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG,
         self.RAMSTK_CONFIGURATION.RAMSTK_USER_LOG,
         self.RAMSTK_CONFIGURATION.RAMSTK_IMPORT_LOG) = \
            _initialize_loggers(self.RAMSTK_CONFIGURATION)

        # Initialize private dictionary instance attributes.

        # Initialize private list instance attributes.
        self.__test = kwargs['test']
        self._lst_modules = [
            'requirement', 'function', 'hardware', 'validation'
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
            'imports': None,
            'exports': None,
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

        # Connect to the RAMSTK Common database.
        _database = None
        if self.RAMSTK_CONFIGURATION.RAMSTK_COM_BACKEND == 'sqlite':
            _database = self.RAMSTK_CONFIGURATION.RAMSTK_COM_BACKEND + \
                        ':///' + \
                        self.RAMSTK_CONFIGURATION.RAMSTK_COM_INFO['database']
        _dao = DAO()
        _dao.db_connect(_database)

        # Create an instance of the RAMSTK Data Model and load global constants.
        self.ramstk_model = Model(_dao, DAO())
        self.request_do_load_globals()

        # Create an Options module instance and read the Site options.
        self.dic_controllers['options'] = dtcOptions(
            self.ramstk_model.program_dao,
            self.RAMSTK_CONFIGURATION,
            site_dao=_dao,
            test=False)
        self.dic_controllers['options'].request_do_select_all(
            site=True, program=False)

        # Create a Preferences module instance and read the user preferences.
        self.dic_controllers['preferences'] = dtcPreferences(
            self.ramstk_model.program_dao,
            self.RAMSTK_CONFIGURATION,
            site_dao=_dao,
            test=False)
        self.dic_controllers['preferences'].request_do_select_all(
            site=True, user=True)

        # Create an Import module instance.
        self.dic_controllers['imports'] = dtcImports(
            self.ramstk_model.program_dao, self.RAMSTK_CONFIGURATION, test=False)

        # Create an Export module instance.
        self.dic_controllers['exports'] = dtcExports(
            self.ramstk_model.program_dao, self.RAMSTK_CONFIGURATION, test=False)

        # Validate the license.
        # if self._validate_license():
        #    sys.exit(2)

        # Create RAMSTK Books.  These need to be initialized after reading the
        # configuration.
        if self.RAMSTK_CONFIGURATION.RAMSTK_GUI_LAYOUT == 'basic':  # Single window.
            pass
        else:  # Multiple windows.
            self.dic_books['listbook'] = ListBook(self)
            self.dic_books['modulebook'] = ModuleBook(self)
            self.dic_books['workbook'] = WorkBook(self)

        _icon = self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/db-disconnected.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        self.icoStatus.set_from_pixbuf(_icon)
        self.icoStatus.set_tooltip(
            _(u"RAMSTK is not currently connected to a "
              u"project database."))

    def request_do_create_program(self):
        """
        Request a new RAMSTK Program database be created.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _database = None

        if self.RAMSTK_CONFIGURATION.RAMSTK_BACKEND == 'sqlite':
            _database = self.RAMSTK_CONFIGURATION.RAMSTK_BACKEND + ':///' + \
                self.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO['database']

        _error_code, _msg = self.ramstk_model.do_create_program(_database)
        if _error_code == 0:
            self.request_do_open_program()
            self.RAMSTK_CONFIGURATION.RAMSTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('createdProgram')
        else:
            self.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_do_load_globals(self):
        """
        Request to load all the global Configuration variables.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self.ramstk_model.do_load_globals(self.RAMSTK_CONFIGURATION)

    def request_do_open_program(self):
        """
        Request an RAMSTK Program database be opened for analyses.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _database = None

        if self.RAMSTK_CONFIGURATION.RAMSTK_BACKEND == 'sqlite':
            _database = self.RAMSTK_CONFIGURATION.RAMSTK_BACKEND + ':///' + \
                self.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO['database']

        # If the database was successfully opened, create an instance of each
        # of the slave data controllers.
        _error_code, _msg = self.ramstk_model.do_open_program(_database)
        if _error_code == 0:
            pub.sendMessage('requestOpen')
            self.dic_controllers['revision'] = dtcRevision(
                self.ramstk_model.program_dao,
                self.RAMSTK_CONFIGURATION,
                test=False)
            self.dic_controllers['function'] = dtcFunction(
                self.ramstk_model.program_dao,
                self.RAMSTK_CONFIGURATION,
                test=False)
            self.dic_controllers['requirement'] = dtcRequirement(
                self.ramstk_model.program_dao,
                self.RAMSTK_CONFIGURATION,
                test=False)
            self.dic_controllers['hardware'] = dtcHardwareBoM(
                self.ramstk_model.program_dao,
                self.RAMSTK_CONFIGURATION,
                test=False)
            self.dic_controllers['validation'] = dtcValidation(
                self.ramstk_model.program_dao,
                self.RAMSTK_CONFIGURATION,
                test=False)
            self.dic_controllers['profile'] = dtcUsageProfile(
                self.ramstk_model.program_dao,
                self.RAMSTK_CONFIGURATION,
                test=False)
            self.dic_controllers['definition'] = dtcFailureDefinition(
                self.ramstk_model.program_dao,
                self.RAMSTK_CONFIGURATION,
                test=False)
            self.dic_controllers['ffmea'] = dtcFMEA(
                self.ramstk_model.program_dao,
                self.RAMSTK_CONFIGURATION,
                test=False,
                functional=True)
            self.dic_controllers['stakeholder'] = dtcStakeholder(
                self.ramstk_model.program_dao,
                self.RAMSTK_CONFIGURATION,
                test=False)
            self.dic_controllers['allocation'] = dtcAllocation(
                self.ramstk_model.program_dao,
                self.RAMSTK_CONFIGURATION,
                test=False)
            self.dic_controllers['hazops'] = dtcHazardAnalysis(
                self.ramstk_model.program_dao,
                self.RAMSTK_CONFIGURATION,
                test=False)
            self.dic_controllers['similaritem'] = dtcSimilarItem(
                self.ramstk_model.program_dao,
                self.RAMSTK_CONFIGURATION,
                test=False)
            self.dic_controllers['dfmeca'] = dtcFMEA(
                self.ramstk_model.program_dao,
                self.RAMSTK_CONFIGURATION,
                test=False,
                functional=False)
            self.dic_controllers['pof'] = dtcPoF(
                self.ramstk_model.program_dao,
                self.RAMSTK_CONFIGURATION,
                test=False)

            # Find which modules are active for the program being opened.
            self.dic_controllers['options'].request_do_select_all(
                site=False, program=True)
            _program_info = self.dic_controllers[
                'options'].request_get_options(
                    site=False, program=True)
            self.RAMSTK_CONFIGURATION.RAMSTK_MODULES['function'] = \
                _program_info['function_active']
            self.RAMSTK_CONFIGURATION.RAMSTK_MODULES['requirement'] = \
                _program_info['requirement_active']
            self.RAMSTK_CONFIGURATION.RAMSTK_MODULES['hardware'] = \
                _program_info['hardware_active']
            self.RAMSTK_CONFIGURATION.RAMSTK_MODULES['validation'] = \
                _program_info['vandv_active']

            _page = 1
            for _module in self._lst_modules:
                if self.RAMSTK_CONFIGURATION.RAMSTK_MODULES[_module] == 1:
                    self.RAMSTK_CONFIGURATION.RAMSTK_PAGE_NUMBER[
                        _page] = _module
                    _page += 1

            # TODO: Where to put this code for the status icon?
            _icon = self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
                '/32x32/db-connected.png'
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
            self.icoStatus.set_from_pixbuf(_icon)
            self.icoStatus.set_tooltip(
                _(u"RAMSTK is connected to program database "
                  u"{0:s}.".format(
                      self.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO['database'])))

            self.loaded = True

            self.RAMSTK_CONFIGURATION.RAMSTK_USER_LOG.info(_msg)
            if not self.__test:
                pub.sendMessage('openedProgram')

        else:
            self.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_do_close_program(self):
        """
        Request the open RAMSTK Program database be closed.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _icon = self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/db-disconnected.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        self.icoStatus.set_from_pixbuf(_icon)
        self.icoStatus.set_tooltip(
            _(u"RAMSTK is not currently connected to a "
              u"project database."))

        if not self.__test:
            pub.sendMessage('closedProgram')

        if not self.ramstk_model.do_close_program():
            self.loaded = False

        return self.loaded

    def request_do_save_program(self):
        """
        Request the open RAMSTK Program database be saved.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # TODO: Move this to the ModuleBook.
        _message = _(u"Saving Program Database {0:s}"). \
            format(self.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO['database'])
        self.dic_books['modulebook'].statusbar.push(2, _message)

        _error_code, _msg = self.ramstk_model.do_save_program()

        if _error_code == 0:
            self.RAMSTK_CONFIGURATION.RAMSTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('savedProgram')
        else:
            self.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(_msg)
            _return = True

        # TODO: Move this to the ModuleBook.
        self.dic_books['modulebook'].statusbar.pop(2)

        return _return

    def request_do_validate_license(self):
        """
        Request the RAMSTK license be validated.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Read the license file and compare to the product key in the site
        # database.  If they are not equal, quit the application.
        _license_file = self.RAMSTK_CONFIGURATION.RAMSTK_DATA_DIR + '/license.key'
        try:
            _license_file = open(_license_file, 'r')
        except IOError:
            ramstk_warning(
                _(u"Cannot find license file {0:s}.  If your "
                  u"license file is elsewhere, please place "
                  u"it in {1:s}.").format(
                      _license_file,
                      self.RAMSTK_CONFIGURATION.RAMSTK_DATA_DIR))
            _return = True

        _license_key = _license_file.readline().rstrip('\n')
        _expire_date = _license_file.readline().rstrip('\n')
        _license_file.close()

        _error_code, _msg = self.ramstk_model.validate_license(_license_key)
        if _error_code == 1:
            ramstk_error(
                _(u"Invalid license (Invalid key).  Your "
                  u"license key is incorrect.  Closing the RAMSTK "
                  u"application."))
            _return = True
        elif _error_code == 2:
            # noinspection PyUnresolvedReferences
            ramstk_error(
                _(u"Invalid license (Expired).  Your license "
                  u"expired on {0:s}.  Closing the RAMSTK "
                  u"application.").format(_expire_date.strftime('%Y-%d-%m')))
            _return = True

        return _return

    def __del__(self):
        """Delete the running instance of RAMSTK."""
        del self


if __name__ == '__main__':
    main()
