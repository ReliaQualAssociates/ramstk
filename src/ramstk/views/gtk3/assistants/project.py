# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.assistants.project.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Open Project Assistant Module."""

# Standard Library Imports
import os

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.db.base import BaseDatabase
from ramstk.utilities import file_exists
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets.dialog import RAMSTKDialog, RAMSTKMessageDialog
from ramstk.views.gtk3.widgets.label import RAMSTKLabel


class CreateProject():
    """This is the class used to create a new RAMSTK Project database."""

    RAMSTK_USER_CONFIGURATION = None

    def __init__(self, __button: Gtk.ToolButton,
                 configuration: RAMSTKUserConfiguration) -> None:
        """
        Initialize an instance of the Create Project Assistant.

        :param __button: the Gtk.ToolButton() that launched this class.
        :type __button: :class:`Gtk.ToolButton`
        :param controller: the RAMSTK master data controller.
        :type controller: :class:`RAMSTK.RAMSTK`
        """
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.RAMSTK_USER_CONFIGURATION = configuration

        self._request_create_sqlite3_project()

    def _request_create_sqlite3_project(self) -> None:
        """Create a RAMSTK Project database using SQLite3."""
        _dialog = Gtk.FileChooserDialog(
            title=_("Create a RAMSTK Program Database"),
            action=Gtk.FileChooserAction.SAVE,
            buttons=(Gtk.STOCK_NEW, Gtk.ResponseType.ACCEPT, Gtk.STOCK_CANCEL,
                     Gtk.ResponseType.REJECT))
        _dialog.set_current_folder(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_DIR)

        if _dialog.run() == Gtk.ResponseType.ACCEPT:
            _new_program = _dialog.get_filename()
            _new_program = _new_program + '.ramstk'

            if file_exists(_new_program):
                _dlgConfirm = RAMSTKDialog(
                    _("RAMSTK - Confirm Overwrite"),
                    dlgbuttons=(Gtk.STOCK_YES, Gtk.ResponseType.YES,
                                Gtk.STOCK_NO, Gtk.ResponseType.NO))

                _label = RAMSTKLabel(
                    _("RAMSTK Program database already exists. "
                      "\n\n{0:s}\n\nOverwrite?").format(_new_program))
                _label.do_set_properties(width=-1,
                                         height=-1,
                                         bold=False,
                                         wrap=True)
                _dlgConfirm.vbox.pack_start(_label, True, True, 0)
                _label.show()

                if _dlgConfirm.run() == Gtk.ResponseType.YES:
                    _dlgConfirm.destroy()
                    os.remove(_new_program)
                else:
                    _dlgConfirm.destroy()
                    _dialog.destroy()

            self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO['database'] = (
                _new_program)

        _dialog.destroy()

        pub.sendMessage('request_create_program',
                        program_db=BaseDatabase(),
                        database=self.RAMSTK_USER_CONFIGURATION.
                        RAMSTK_PROG_INFO['database'])

    def _cancel(self, __button: Gtk.Button) -> None:
        """
        Destroy the Create Project Assistant.

        :param __button: the Gtk.Button() that called this method.
        :type __button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        self.assistant.destroy()


class OpenProject():
    """Assistant to guide user through process of creating RAMSTK Project."""

    RAMSTK_USER_CONFIGURATION = None

    def __init__(self, __button: Gtk.ToolButton,
                 configuration: RAMSTKUserConfiguration) -> None:
        """
        Initialize an instance of the Create Project Assistant.

        :param __button: the Gtk.ToolButton() that launched an instance of this
            class.
        :type __button: :class:`Gtk.ToolButton`
        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        """
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.RAMSTK_USER_CONFIGURATION = configuration

        self._do_request_open_project()

    def _do_request_open_project(self) -> None:
        """
        Open or connect to a RAMSTK Program database.

        :return: None
        :rtype: None
        """
        if self.RAMSTK_USER_CONFIGURATION.loaded:
            _prompt = _("A database is already open.  Only one database can "
                        "be open at a time in RAMSTK.  You must close the "
                        "currently open RAMSTK database before a new "
                        "database can be opened.")
            _icon = (self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
                     + '/32x32/information.png')
            _dialog = RAMSTKMessageDialog(_prompt, _icon, 'information')
            if _dialog.run() == Gtk.ResponseType.OK:
                _dialog.destroy()

        else:
            _dialog = Gtk.FileChooserDialog(
                title=_("RAMSTK - Open Program"),
                parent=None,
                buttons=(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT,
                         Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT))
            _dialog.set_current_folder(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_DIR)

            # Set some filters to select all files or only some text files.
            _filter = Gtk.FileFilter()
            _filter.set_name(_("RAMSTK Program Databases"))
            _filter.add_pattern("*.ramstk")
            _dialog.add_filter(_filter)

            _filter = Gtk.FileFilter()
            _filter.set_name(_("All files"))
            _filter.add_pattern("*")
            _dialog.add_filter(_filter)

            if _dialog.run() == Gtk.ResponseType.ACCEPT:
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO['database'] = (
                    _dialog.get_filename())

            _dialog.destroy()

            _database = (str(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_BACKEND + ':///'
                + self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO['database']))

            pub.sendMessage('request_open_program',
                            program_db=BaseDatabase(),
                            database=_database)
