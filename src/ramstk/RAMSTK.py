#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ramstk.RAMSTK.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""This is the main program for the RAMSTK application."""

# Standard Library Imports
from datetime import date

# Third Party Imports
from pubsub import pub
from sqlalchemy.orm import scoped_session
from treelib import Tree

# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import (
    dmFMEA, dmFunction, dmHardware, dmOptions, dmPoF,
    dmRequirement, dmRevision, dmStakeholder, dmValidation
)
from ramstk.db.base import BaseDatabase
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import GdkPixbuf, Gtk, _
from ramstk.models.commondb import RAMSTKSiteInfo
from ramstk.modules.exports import dtcExports
from ramstk.modules.imports import dtcImports
from ramstk.modules.preferences import dtcPreferences


class Model():
    """
    This is the RAMSTK data model class.

    The attributes of a RAMSTK data model are:

    :ivar site_dao: the data access object used to communicate with the RAMSTK
        Common database.
    :type site_dao: :class:`ramstk.dao.BaseDatabase.BaseDatabase()`
    :ivar program_dao: the data access object used to communicate with the
        RAMSTK Program database
    :type program_dao: :class:`ramstk.dao.BaseDatabase.BaseDatabase()`
    """

    def __init__(self, sitedao, programdao):
        """
        Initialize an instance of the RAMSTK data model.

        :param sitedao: the :class:`ramstk.dao.BaseDatabase.BaseDatabase` instance connected to
                        the RAMSTK Common database.
        :param programdao: the :class:`ramstk.dao.BaseDatabase.BaseDatabase` instance connected
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
        site_session = self.site_dao.session
        site_session.configure(
            bind=self.site_dao.engine,
            autoflush=False,
            expire_on_commit=False,
        )
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
            program_session = self.program_dao.session
            program_session.configure(
                bind=self.program_dao.engine,
                autoflush=False,
                expire_on_commit=False,
            )
            self.program_session = scoped_session(program_session)

        else:
            _error_code = 1001
            _msg = (
                'RAMSTK ERROR: Failed to open RAMSTK Program '
                'database {0:s}.'
            ).format(database)

        return _error_code, _msg

    def do_close_program(self):
        """Close the open RAMSTK Program database."""
        self.program_dao.db_close()

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


class RAMSTK():
    """
    Class representing the RAMSTK data controller.

    This is the master controller for the entire RAMSTK application.
    Attributes of a RAMSTK data controller are:

    :ivar dict dic_controllers: dictionary of data controllers available in the
        running instance of RAMSTK. Keys are:

            'function'
            'hardware'
            'revision'
            'requirement'
            'validation'
            'survival'
            'matrices'
            'fmea'
            'pof'
            'stakeholder'
            'growth'
            'options'
            'imports'

        Values are the instance of each RAMSTK data controller.
    :ivar dict dic_books: dictionary of GUI books used by the running instance
        of RAMSTK. Keys are:

            'listbook'
            'modulebook'
            'workbook'

        Values are the instance of each RAMSTK book.
    :ivar ramstk_model: the instance of :class:`ramstk.RAMSTK.Model` managed by
        this data controller.
    """
    RAMSTK_CONFIGURATION = RAMSTKUserConfiguration()

    def __init__(self, **kwargs):
        """Initialize an instance of the RAMSTK data controller."""
        # Read the site configuration file.
        self.RAMSTK_CONFIGURATION.set_site_variables()
        if self.RAMSTK_CONFIGURATION.set_user_variables():
            _prompt = _(
                "A user-specific configuration directory could not "
                "be found at {0:s}.  You will be given the option to "
                "create and populate this directory.  If you choose "
                "not to, you will recieve this prompt every time you "
                "execute RAMSTK.  Would you like to create and populate "
                "a user-specific configuration directory?", ).format(
                    self.RAMSTK_CONFIGURATION.RAMSTK_HOME_DIR
                    + "/.config/RAMSTK", )
            _dialog = ramstk.RAMSTKMessageDialog(_prompt, '', 'question')
            _response = _dialog.do_run()
            _dialog.do_destroy()

            if _response == Gtk.ResponseType.YES:
                self.RAMSTK_CONFIGURATION.create_user_configuration()

            self.RAMSTK_CONFIGURATION.set_user_variables(first_run=False)

        self.RAMSTK_CONFIGURATION.get_user_configuration()

        # Initialize private dictionary instance attributes.

        # Initialize private list instance attributes.
        self.__test = kwargs['test']
        self._lst_modules = [
            'requirement',
            'function',
            'hardware',
            'validation',
        ]

        # Initialize private scalar instance attributes.

        # Initialize public dictionary instance attributes.
        self.dic_controllers = {
            'options': None,
            'function': None,
            'revision': None,
            'requirement': None,
            'hardware': None,
            'validation': None,
            'matrices': None,
            'ffmea': None,
            'fmea': None,
            'pof': None,
            'stakeholder': None,
            'imports': None,
            'exports': None,
        }

        # Define public list attributes.

        # Define public scalar attributes.
        self.icoStatus = Gtk.StatusIcon()
        self.RAMSTK_CONFIGURATION.loaded = False

        # Connect to the RAMSTK Common database.
        _database = None
        if self.RAMSTK_CONFIGURATION.RAMSTK_COM_BACKEND == 'sqlite':
            _database = self.RAMSTK_CONFIGURATION.RAMSTK_COM_BACKEND + \
                        ':///' + \
                        self.RAMSTK_CONFIGURATION.RAMSTK_COM_INFO['database']
        _dao = BaseDatabase()
        _dao.db_connect(_database)

        # Create an instance of the RAMSTK Data Model and load global constants.
        self.ramstk_model = Model(_dao, BaseDatabase())

        # Create an Options module instance and read the Site options.
        _attributes = {'site': True, 'program': False, 'user': True}
        self.dic_controllers['options'] = dmOptions(
            self.ramstk_model.program_dao,
            common_dao=_dao
        )
        self.dic_controllers['options'].request_do_select_all(_attributes)

        # Create a Preferences module instance and read the user preferences.
        self.dic_controllers['preferences'] = dtcPreferences(
            self.ramstk_model.program_dao,
            self.RAMSTK_CONFIGURATION,
            site_dao=_dao,
            test=False,
        )
        self.dic_controllers['preferences'].request_do_select_all(_attributes)

        # Create an Import module instance.
        self.dic_controllers['imports'] = dtcImports(
            self.ramstk_model.program_dao,
            self.RAMSTK_CONFIGURATION,
            test=False,
        )

        # Create an Export module instance.
        self.dic_controllers['exports'] = dtcExports(
            self.ramstk_model.program_dao,
            self.RAMSTK_CONFIGURATION,
            test=False,
        )

        # Validate the license.
        # if self._validate_license():
        #    sys.exit(2)

        _icon = self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/db-disconnected.png'
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(_icon, 22, 22)
        self.icoStatus.set_from_pixbuf(_icon)
        # Deprecated since version 3.14: Use Gio.Notification and Gtk.Application to provide status notifications; there is no direct replacement for this function
        #self.icoStatus.set_tooltip(
        #    _(u"RAMSTK is not currently connected to a "
        #      u"project database."))

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.request_do_open_program, 'request_do_open_program')

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
            self.dic_controllers['revision'] = dmRevision(
                self.ramstk_model.program_dao
            )
            self.dic_controllers['function'] = dmFunction(
                self.ramstk_model.program_dao
            )
            self.dic_controllers['requirement'] = dmRequirement(
                self.ramstk_model.program_dao
            )
            self.dic_controllers['hardware'] = dmHardware(
                self.ramstk_model.program_dao
            )
            self.dic_controllers['validation'] = dmValidation(
                self.ramstk_model.program_dao
            )
            self.dic_controllers['ffmea'] = dmFMEA(
                self.ramstk_model.program_dao,
                functional=True
            )
            self.dic_controllers['stakeholder'] = dmStakeholder(
                self.ramstk_model.program_dao
            )
            self.dic_controllers['dfmeca'] = dmFMEA(
                self.ramstk_model.program_dao,
                functional=False
            )
            self.dic_controllers['pof'] = dmPoF(
                self.ramstk_model.program_dao
            )

            # Find which modules are active for the program being opened.
            _attributes = {'site': False, 'program': True}
            self.dic_controllers['options'].request_do_select_all(_attributes)
            _program_info = self.dic_controllers[
                'options'
            ].request_get_options(
                site=False,
                program=True,
            )
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
                        _page
                    ] = _module
                    _page += 1

            # ISSUE: See issue #228 at https://github.com/ReliaQualAssociates/ramstk/issues/228
            _icon = self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
                '/32x32/db-connected.png'
            _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(_icon, 22, 22)
            self.icoStatus.set_from_pixbuf(_icon)
            # Deprecated since version 3.14: Use Gio.Notification and Gtk.Application to provide status notifications; there is no direct replacement for this function
            #self.icoStatus.set_tooltip(
            #    _(u"RAMSTK is connected to program database "
            #      u"{0:s}.".format(
            #          self.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO['database'])))

            self.RAMSTK_CONFIGURATION.loaded = True

            self.RAMSTK_CONFIGURATION.RAMSTK_USER_LOG.info(_msg)
            if not self.__test:
                _attributes = {'revision_id': -1}
                self.dic_controllers['revision'].request_do_select_all(
                    _attributes, )

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
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(_icon, 22, 22)
        self.icoStatus.set_from_pixbuf(_icon)
        self.icoStatus.set_tooltip(
            _(
                "RAMSTK is not currently connected to a "
                "project database.", ), )

        if not self.__test:
            pub.sendMessage('closed_program')

        if not self.ramstk_model.do_close_program():
            self.RAMSTK_CONFIGURATION.loaded = False

    def request_do_save_program(self):
        """
        Request the open RAMSTK Program database be saved.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _error_code, _msg = self.ramstk_model.do_save_program()

        if _error_code == 0:
            self.RAMSTK_CONFIGURATION.RAMSTK_USER_LOG.info(_msg)

            if not self.__test:
                pub.sendMessage('savedProgram')
        else:
            self.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def __del__(self):
        """Delete the running instance of RAMSTK."""
        del self
