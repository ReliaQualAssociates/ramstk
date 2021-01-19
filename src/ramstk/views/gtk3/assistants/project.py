# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.assistants.project.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Open Project Assistant Module."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.db.base import BaseDatabase
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets.dialog import (
    RAMSTKDatabaseSelect, RAMSTKDialog, RAMSTKMessageDialog
)
from ramstk.views.gtk3.widgets.label import RAMSTKLabel


class CreateProject:
    """The class used to create a new RAMSTK Project database."""

    RAMSTK_USER_CONFIGURATION: RAMSTKUserConfiguration = None  # type: ignore

    def __init__(self, __button: Gtk.ToolButton,
                 configuration: RAMSTKUserConfiguration,
                 parent: object) -> None:
        """Initialize an instance of the Create Project Assistant.

        :param __button: the Gtk.ToolButton() that launched this class.
        :param configuration: the RAMSTKUserConfiguration class instance.
        :param parent: the parent window associated with the dialog.
        """
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._parent: object = parent

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.RAMSTK_USER_CONFIGURATION = configuration

        self._do_request_create_project()

    def _do_confirm_overwrite(self, database: str) -> None:
        """Raise dialog to confirm overwriting existing RAMSTK database.

        :param database: the name of the existing database that is to be
            confirmed for overwrite.
        :return: None
        :rtype: None
        """
        _dialog = RAMSTKDialog(_("RAMSTK - Confirm Overwrite"),
                               dlgbuttons=(Gtk.STOCK_YES, Gtk.ResponseType.YES,
                                           Gtk.STOCK_NO, Gtk.ResponseType.NO),
                               dlgparent=self._parent)

        _label = RAMSTKLabel(
            _("RAMSTK Program database already exists:"
              "\n\n\t\t{0:s}\n\nOverwrite?").format(database))
        _label.do_set_properties(width=-1, height=-1, bold=False, wrap=True)
        _dialog.vbox.pack_start(_label, True, True, 0)
        _dialog.show_all()

        if _dialog.run() == Gtk.ResponseType.YES:
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO[
                'database'] = database
        else:
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO['database'] = ''

        _dialog.destroy()

    def _do_request_create_project(self) -> None:
        """Request to create a new RAMSTK Project Database.

        :return: None
        :rtype: None
        """
        _dialog = RAMSTKDatabaseSelect(
            dlgtitle=("Select RAMSTK Program "
                      "Database on the {0:s} Server".format(
                          self.RAMSTK_USER_CONFIGURATION.
                          RAMSTK_PROG_INFO['dialect'])),
            dlgparent=self._parent,
            dao=BaseDatabase(),
            database=self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO,
            icons={
                'refresh':
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR
                + '/icons/32x32/view-refresh.png',
                'save':
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR
                + '/icons/32x32/save.png'
            })

        if _dialog.do_run() == Gtk.ResponseType.OK:
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO = \
                _dialog.database

            if _dialog.exists:
                self._do_confirm_overwrite(_dialog.database['database'])

            pub.sendMessage(
                'request_create_program',
                program_db=BaseDatabase(),
                database=self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO)

        _dialog.destroy()


class OpenProject:
    """Assistant to guide user through process of creating RAMSTK Project."""

    RAMSTK_USER_CONFIGURATION: RAMSTKUserConfiguration = None  # type: ignore

    def __init__(self, __button: Gtk.ToolButton,
                 configuration: RAMSTKUserConfiguration,
                 parent: object) -> None:
        """Initialize an instance of the Create Project Assistant.

        :param __button: the Gtk.ToolButton() that launched an instance of this
            class.
        :param configuration: the RAMSTKUserConfiguration class instance.
        """
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._parent: object = parent

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.RAMSTK_USER_CONFIGURATION = configuration

        self._do_request_open_project()

    def _do_request_open_project(self) -> None:
        """Open or connect to a RAMSTK Program database.

        :return: None
        :rtype: None
        """
        if self.RAMSTK_USER_CONFIGURATION.loaded:
            self.__project_is_open()
        else:
            _dialog = RAMSTKDatabaseSelect(
                dlgtitle=("Select RAMSTK Program "
                          "Database on the {0:s} Server".format(
                              self.RAMSTK_USER_CONFIGURATION.
                              RAMSTK_PROG_INFO['dialect'])),
                dlgparent=self._parent,
                dao=BaseDatabase(),
                database=self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO,
                icons={
                    'refresh':
                    self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR
                    + '/icons/32x32/view-refresh.png',
                    'save':
                    self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR
                    + '/icons/32x32/save.png'
                })

            if _dialog.do_run() == Gtk.ResponseType.OK:
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO = \
                    _dialog.database

                if _dialog.exists:
                    pub.sendMessage('request_open_program',
                                    program_db=BaseDatabase(),
                                    database=self.RAMSTK_USER_CONFIGURATION.
                                    RAMSTK_PROG_INFO)
                else:
                    pub.sendMessage('request_create_program',
                                    program_db=BaseDatabase(),
                                    database=self.RAMSTK_USER_CONFIGURATION.
                                    RAMSTK_PROG_INFO)

                if _dialog.btnSave.get_active():
                    self.RAMSTK_USER_CONFIGURATION.set_user_configuration()

            _dialog.do_destroy()

    def __project_is_open(self) -> None:
        """Raise dialog explaining a project is already open.

        :return: None
        """
        _prompt = _("A database is already open.  Only one database can "
                    "be open at a time in RAMSTK.  You must close the "
                    "currently open RAMSTK database before a new "
                    "database can be opened.")
        _dialog = RAMSTKMessageDialog(parent=self._parent)
        _dialog.do_set_message(_prompt)
        _dialog.do_set_message_type('information')

        if _dialog.run() == Gtk.ResponseType.OK:
            _dialog.destroy()
