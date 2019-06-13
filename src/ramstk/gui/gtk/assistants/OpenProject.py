# -*- coding: utf-8 -*-
#
#       gui.gtk.assistants.OpenProject.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Open Project Assistant Module."""

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import RAMSTKMessageDialog
from ramstk.gui.gtk.ramstk.Widget import Gtk, _


class OpenProject():
    """Assistant to guide user through process of creating RAMSTK Project."""

    def __init__(self, __button, controller):
        """
        Initialize an instance of the Create Project Assistant.

        :param Gtk.ToolButton __button: the Gtk.ToolButton() that launched this
                                        class.
        :param controller: the :class:`RAMSTK.RAMSTK` master data
                           controller.
        """
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._mdcRAMSTK = controller

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self._do_request_open_project()

    def _do_request_open_project(self):
        """
        Open or connect to a RAMSTK Program database.

        :return: None
        :rtype: None
        """
        if self._mdcRAMSTK.loaded:
            _prompt = _(
                "A database is already open.  Only one database can "
                "be open at a time in RAMSTK.  You must close the "
                "currently open RAMSTK database before a new "
                "database can be opened.",
            )
            _icon = (
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
                '/32x32/information.png'
            )
            _dialog = RAMSTKMessageDialog(_prompt, _icon, 'information')
            if _dialog.run() == Gtk.ResponseType.OK:
                _dialog.destroy()

        else:
            _dialog = Gtk.FileChooserDialog(
                title=_("RAMSTK - Open Program"),
                buttons=(
                    Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT,
                    Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                ),
            )
            _dialog.set_current_folder(
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_PROG_DIR,
            )

            # Set some filters to select all files or only some text files.
            _filter = Gtk.FileFilter()
            _filter.set_name(_("RAMSTK Program Databases"))
            _filter.add_pattern("*.rtk")
            _dialog.add_filter(_filter)

            _filter = Gtk.FileFilter()
            _filter.set_name(_("All files"))
            _filter.add_pattern("*")
            _dialog.add_filter(_filter)

            if _dialog.run() == Gtk.ResponseType.ACCEPT:
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO['database'] = \
                    _dialog.get_filename()

            _dialog.destroy()

            self._mdcRAMSTK.request_do_open_program()
