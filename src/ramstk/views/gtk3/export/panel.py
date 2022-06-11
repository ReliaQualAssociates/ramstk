# pylint: disable=unused-import, missing-docstring
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.export.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK GTK3 Project Export Panels."""

# Standard Library Imports
import os
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton,
    RAMSTKEntry,
    RAMSTKFileChooserButton,
    RAMSTKFixedPanel,
    RAMSTKLabel,
    RAMSTKMessageDialog,
)


class ExportPanel(RAMSTKFixedPanel):
    """The panel to display exprot options."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = ""
    _tag = "export"
    _title = _("Export Modules")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, analysis_path: str = "", parent: Gtk.Window = None) -> None:
        """Initialize an instance of the Export panel."""
        super().__init__()

        # Initialize widgets.
        self.btnFileName = RAMSTKFileChooserButton()
        self.chkRevisions: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Export Revision Data")
        )
        self.chkFunctions: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Export Function Data")
        )
        self.chkRequirements: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Export Requirement Data")
        )
        self.chkHardware: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Export Hardware Data")
        )
        self.chkValidation: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Export Validation Data")
        )
        self.chkHazards: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Export Hazards Analysis Data")
        )
        self.chkStakeholder: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Export Stakeholder Data")
        )
        self.chkAllocation: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Export R(t) Allocation Data")
        )
        self.chkSimilarItem: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Export Similar Item Analysis Data")
        )
        self.chkFMEA: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Export FMEA/FMECA Data")
        )
        self.chkPoF: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Export Physics of Failure (PoF) Data")
        )
        self.chkUsageProfile: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Export Usage Profile Data")
        )
        self.txtFileName = RAMSTKEntry()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.
        self._analysis_path: str = analysis_path
        self._parent: Gtk.Window = parent

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "export_revision": [
                0,
                self.chkRevisions,
                "toggled",
                None,
                "",
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _(""),
                "gint",
            ],
            "export_function": [
                1,
                self.chkFunctions,
                "toggled",
                None,
                "",
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _(""),
                "gint",
            ],
            "export_requirement": [
                2,
                self.chkRequirements,
                "toggled",
                None,
                "",
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _(""),
                "gint",
            ],
            "export_hardware": [
                3,
                self.chkHardware,
                "toggled",
                None,
                "",
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _(""),
                "gint",
            ],
            "export_validation": [
                4,
                self.chkValidation,
                "toggled",
                None,
                "",
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _(""),
                "gint",
            ],
            "export_hazards": [
                5,
                self.chkHazards,
                "toggled",
                None,
                "",
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _(""),
                "gint",
            ],
            "export_stakeholder": [
                6,
                self.chkStakeholder,
                "toggled",
                None,
                "",
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _(""),
                "gint",
            ],
            "export_allocation": [
                7,
                self.chkAllocation,
                "toggled",
                None,
                "",
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _(""),
                "gint",
            ],
            "export_similar_item": [
                8,
                self.chkSimilarItem,
                "toggled",
                None,
                "",
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _(""),
                "gint",
            ],
            "export_fmea": [
                9,
                self.chkFMEA,
                "toggled",
                None,
                "",
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _(""),
                "gint",
            ],
            "export_pof": [
                10,
                self.chkPoF,
                "toggled",
                None,
                "",
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _(""),
                "gint",
            ],
            "export_usage_profile": [
                11,
                self.chkUsageProfile,
                "toggled",
                None,
                "",
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _(""),
                "gint",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        self.__make_ui()

        # Subscribe to PyPubSub messages.

    def do_set_file(self, button) -> None:
        """Retrieve the selected filename.

        :param button: the RAMSTKFileChooserButton() calling this method.
        :return: None
        :rtype: None
        """
        _file_name = button.get_filename()

        if os.path.exists(_file_name):
            _dialog = RAMSTKMessageDialog(self._parent)
            _dialog.do_set_message(_(f"File {_file_name} already exists.  Overwrite?"))
            _dialog.do_set_message_type("question")
            _response = _dialog.do_run()
            if _response == Gtk.ResponseType.YES:
                os.remove(_file_name)
                self.txtFileName.do_update(_file_name, "changed")

            _dialog.destroy()

    def __make_ui(self) -> None:
        """Adjust position of widgets from default one column to two columns.

        :return: None
        :rtype: None
        """
        self.btnFileName.set_filename(f"{self._analysis_path}/untitled")
        self.txtFileName.do_set_properties(width=300)
        _lblFileName = RAMSTKLabel(_("Select file for export:"))

        _fixed = self.get_children()[0].get_children()[0].get_children()[0]
        _widgets = _fixed.get_children()

        _y_pos = [_fixed.child_get_property(_label, "y") for _label in _widgets[:13:2]]

        # The meta-class method do_make_panel() places all the widgets in a single
        # column.  Here we are adjusting the widgets into two columns.  See #1085.
        for _idx, _label in enumerate(_widgets[13::2]):
            _fixed.move(_label, 300, _y_pos[_idx])

        for _idx, _button in enumerate(_widgets[14::2]):
            _fixed.move(_button, 300, _y_pos[_idx])

        _fixed.put(_lblFileName, 10, _y_pos[-1] + 70)
        _fixed.put(self.txtFileName, 250, _y_pos[-1] + 70)
        _fixed.put(self.btnFileName, 550, _y_pos[-1] + 70)

        self.btnFileName.connect("file-set", self.do_set_file)
