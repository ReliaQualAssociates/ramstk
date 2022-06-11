# pylint: disable=unused-import, missing-docstring
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.export.view.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK GTK3 Project Export Views."""

# Standard Library Imports
import os
from typing import Dict, Tuple

# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKDialog, RAMSTKPanel

# RAMSTK Local Imports
from . import ExportPanel


class ExportDialog(RAMSTKDialog):
    """Provide a GUI to guide RAMSTK module exports/reporting."""

    # Define private dict class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, parent: object = None
    ) -> None:
        """Initialize an instance of the project export assistant.

        :param parent: the parent window for this assistant.
        """
        super().__init__(_("RAMSTK Program Export Assistant"), dlgparent=parent)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._default_path = f"{configuration.RAMSTK_PROG_DIR}"
        self._default_file_name = "ramstk_export.txt"
        self._pnlPanel: RAMSTKPanel = ExportPanel(
            analysis_path=configuration.RAMSTK_PROG_DIR,
            parent=parent,
        )

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.

    def do_get_export_information(self) -> Tuple[Dict[str, bool], str]:
        """Retrieve the modules to export and file name to receive export.

        :return: dictionary of modules to export and file name to export to.
        :rtype: tuple
        """
        _dic_modules = {
            "revision": self._pnlPanel.chkRevisions.get_active(),
            "requirement": self._pnlPanel.chkRequirements.get_active(),
            "function": self._pnlPanel.chkFunctions.get_active(),
            "hardware": self._pnlPanel.chkHardware.get_active(),
            "validation": self._pnlPanel.chkValidation.get_active(),
            "usage_profile": self._pnlPanel.chkUsageProfile.get_active(),
            "stakeholder": self._pnlPanel.chkStakeholder.get_active(),
            "hazard": self._pnlPanel.chkHazards.get_active(),
            "allocation": self._pnlPanel.chkAllocation.get_active(),
            "similar_item": self._pnlPanel.chkSimilarItem.get_active(),
            "fmeca": self._pnlPanel.chkFMEA.get_active(),
            "pof": self._pnlPanel.chkPoF.get_active(),
        }
        _file_name = self._pnlPanel.txtFileName.get_text()
        if _file_name == "":
            _file_name = f"{self._default_path}/{self._default_file_name}"

        if os.path.dirname(_file_name) == "":
            _file_name = f"{self._default_path}/{_file_name}"

        return _dic_modules, _file_name

    def _cancel(self, __button: Gtk.Button):
        """Destroy the assistant when the 'Cancel' button is pressed.

        :param __button: the Gtk.Button() that called this method.
        :type __button: :class:`Gtk.Button`
        """
        self.do_destroy()

    def __make_ui(self) -> None:
        """Build the user interface.

        :return: None
        :rtype: None
        """
        self.set_default_size(800, 500)

        self.vbox.pack_start(self._pnlPanel, True, True, 0)

        self.show_all()
