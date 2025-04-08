# pylint: disable=unused-import, missing-docstring
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.options.view.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Options view module."""

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKBasePanel
from ramstk.views.gtk3.widgets.dialogs import RAMSTKBaseDialog

# RAMSTK Local Imports
from . import OptionsPanel


class OptionsDialog(RAMSTKBaseDialog):
    """Provide a GUI to set various RAMSTK configuration options.

    RAMSTK options are stored in the RAMSTK Common database and the RAMSTK Program
    database.  RAMSTK options are site-specific or program-specific and apply to all
    users.  Options should not be confused with user-specific configurations preferences
    which are stored in RAMSTK.conf in each user's $HOME/.config/RAMSTK directory and
    are applicable only to that specific user. Configuration preferences are edited with
    the Preferences assistant.

    Attributes of the EditOptions are:
    """

    def __init__(self, parent: object = None) -> None:
        """Initialize an instance of the Options assistant.

        :param parent: the parent window for this assistant.
        """
        super().__init__(_("RAMSTK Program Options Assistant"), parent)

        # Initialize widgets.
        self._pnlPanel: RAMSTKBasePanel = OptionsPanel()

        self.__make_ui()

    def _cancel(self, __button: Gtk.Button):
        """Destroy the assistant when the 'Cancel' button is pressed.

        :param __button: the Gtk.Button() that called this method.
        :type __button: :class:`Gtk.Button`
        """
        self.do_destroy()

    def __make_ui(self) -> None:
        """Build the user interface."""
        self.set_default_size(800, 500)

        self.vbox.pack_start(self._pnlPanel, True, True, 0)

        self.show_all()
