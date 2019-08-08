# -*- coding: utf-8 -*-
#
#       gui.gtk.assistants.CreateProject.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Create Project Assistant Module."""

# Standard Library Imports
from os import remove

# RAMSTK Package Imports
from ramstk import file_exists
from ramstk.gui.gtk.ramstk import RAMSTKDialog, RAMSTKLabel
from ramstk.gui.gtk.ramstk.Widget import Gtk, _


class CreateProject():
    """This is the class used to create a new RAMSTK Project database."""

    def __init__(self, __button, controller):
        """
        Initialize an instance of the Create Project Assistant.

        :param __button: the Gtk.ToolButton() that launched this class.
        :type __button: :class:`Gtk.ToolButton`
        :param controller: the RAMSTK master data controller.
        :type controller: :py:class:`RAMSTK.RAMSTK`
        """
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._mdcRAMSTK = controller

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self._request_create_sqlite3_project()

    def _request_create_sqlite3_project(self):
        """Create a RAMSTK Project database using SQLite3."""
        _dialog = Gtk.FileChooserDialog(
            title=_("Create a RAMSTK Program Database"),
            action=Gtk.FileChooserAction.SAVE,
            buttons=(
                Gtk.STOCK_NEW, Gtk.ResponseType.ACCEPT, Gtk.STOCK_CANCEL,
                Gtk.ResponseType.REJECT,
            ),
        )
        _dialog.set_current_folder(
            self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_PROG_DIR,
        )

        if _dialog.run() == Gtk.ResponseType.ACCEPT:
            _new_program = _dialog.get_filename()
            _new_program = _new_program + '.ramstk'

            if file_exists(_new_program):
                _dlgConfirm = RAMSTKDialog(
                    _("RAMSTK - Confirm Overwrite"),
                    dlgbuttons=(
                        Gtk.STOCK_YES, Gtk.ResponseType.YES,
                        Gtk.STOCK_NO, Gtk.ResponseType.NO,
                    ),
                )

                _label = RAMSTKLabel(
                    _(
                        "RAMSTK Program database already exists. "
                        "\n\n{0:s}\n\nOverwrite?",
                    ).format(_new_program),
                    width=-1,
                    height=-1,
                    bold=False,
                    wrap=True,
                )
                _dlgConfirm.vbox.pack_start(_label, True, True, 0)
                _label.show()

                if _dlgConfirm.run() == Gtk.ResponseType.YES:
                    _dlgConfirm.destroy()
                    remove(_new_program)
                else:
                    _dlgConfirm.destroy()
                    _dialog.destroy()

            self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO['database'] = \
                _new_program

        _dialog.destroy()

        self._mdcRAMSTK.request_do_create_program()

    def _cancel(self, __button):
        """
        Destroy the Create Project Assistant.

        :param __button: the Gtk.Button() that called this method.
        :type __button: :class:`Gtk.Button `
        :return: True
        :rtype: boolean
        """
        self.assistant.destroy()

        return True
