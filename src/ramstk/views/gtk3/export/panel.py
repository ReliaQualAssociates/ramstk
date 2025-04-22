# pylint: disable=unused-import, missing-docstring
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.export.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Project Export panel module."""

# Standard Library Imports
import os
from typing import List

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton,
    RAMSTKEntry,
    RAMSTKFileChooserButton,
    RAMSTKFixedPanel,
    RAMSTKLabel,
    RAMSTKMessageDialog,
    WidgetConfig,
    make_widget_config,
)


class ExportPanel(RAMSTKFixedPanel):
    """The panel to display export options."""

    # Define private class attributes.
    _select_msg = ""
    _tag = "export"
    _title = _("Export Modules")

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

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.chkRevisions,
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "export_revision",
                    "index": 0,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                self.chkFunctions,
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "export_function",
                    "index": 1,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                self.chkRequirements,
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "export_requirement",
                    "index": 2,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkHardware,
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "export_hardware",
                    "index": 3,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkValidation,
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "export_validation",
                    "index": 4,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                self.chkHazards,
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "export_hazards",
                    "index": 5,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkStakeholder,
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "export_stakeholder",
                    "index": 6,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkAllocation,
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "export_allocation",
                    "index": 7,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkSimilarItem,
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "export_similar_item",
                    "index": 8,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkFMEA,
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "export_fmea",
                    "index": 9,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkPoF,
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "export_pof",
                    "index": 10,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkUsageProfile,
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "export_usage_profile",
                    "index": 11,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
        ]
        self._analysis_path: str = analysis_path
        self._parent: Gtk.Window = parent

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel(n_columns=2)
        self.__make_ui()

    def do_set_file(self, button) -> None:
        """Retrieve the selected filename.

        :param button: the RAMSTKFileChooserButton calling this method.
        """
        _file_name = button.get_filename()

        if os.path.exists(_file_name):
            _dialog = RAMSTKMessageDialog(_("Select File"), self._parent)
            _dialog.do_set_message(_(f"File {_file_name} already exists.  Overwrite?"))
            _dialog.do_set_message_type("question")
            _response = _dialog.do_run()
            if _response == Gtk.ResponseType.YES:
                os.remove(_file_name)
                self.txtFileName.do_update({"": _file_name})

            _dialog.destroy()

    def __make_ui(self) -> None:
        """Adjust position of widgets from default one column to two columns."""
        self.btnFileName.set_filename(f"{self._analysis_path}/untitled")
        self.txtFileName.do_set_properties({"width_request": 300})
        _lblFileName = RAMSTKLabel(_("Select file for export:"))

        _fixed = self.get_children()[0].get_children()[0].get_children()[0]
        _widgets = _fixed.get_children()

        _y_pos = [_fixed.child_get_property(_label, "y") for _label in _widgets[:12:2]]

        _fixed.put(_lblFileName, 10, _y_pos[-1] + 70)
        _fixed.put(self.txtFileName, 250, _y_pos[-1] + 70)
        _fixed.put(self.btnFileName, 550, _y_pos[-1] + 70)

        self.btnFileName.connect("file-set", self.do_set_file)
