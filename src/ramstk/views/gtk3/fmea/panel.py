# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.fmea.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 FMEA Panels."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple, Union

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models import RAMSTKCauseRecord, RAMSTKMechanismRecord
from ramstk.views.gtk3 import GdkPixbuf, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton,
    RAMSTKFixedPanel,
    RAMSTKLabel,
    RAMSTKTextView,
    RAMSTKTreePanel,
)


class FMEAMethodPanel(RAMSTKFixedPanel):
    """Panel to display FMEA criticality methods."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "mode_id"
    _select_msg = "succeed_retrieve_fmea"
    _tag = "fmea"
    _title = _("FMEA Risk Analysis Method")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self):
        """Initialize an instance of the FMEA methods panel."""
        super().__init__()

        # Initialize widgets.
        self.chkCriticality: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Calculate Criticality")
        )
        self.chkRPN: RAMSTKCheckButton = RAMSTKCheckButton(label=_("Calculate RPNs"))
        self.txtItemCriticality: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._on_edit_message = f"wvw_editing_{self._tag}"

        # Initialize public dictionary attributes.
        self.dic_attribute_widget_map = {
            "type_id": [
                27,
                self.chkCriticality,
                "toggled",
                super().on_toggled,
                self._on_edit_message,
                1,
                {
                    "tooltip": _(
                        "Select this option to calculate the MIL-STD-1629, Task 102 "
                        "criticality analysis."
                    ),
                },
                _("Calculate Criticality"),
                "gint",
            ],
            "rpn": [
                27,
                self.chkRPN,
                "toggled",
                super().on_toggled,
                self._on_edit_message,
                1,
                {
                    "tooltip": _(
                        "Select this option to calculate the Risk Priority Number "
                        "(RPN)."
                    ),
                },
                _("Calculate RPN"),
                "gint",
            ],
            "item_criticality": [
                28,
                self.txtItemCriticality,
                "changed",
                super().on_changed_entry,
                "",
                "",
                {
                    "bold": True,
                    "editable": False,
                    "height": 125,
                    "tooltip": _(
                        "Displays the MIL-STD-1629A, Task 102 item criticality for "
                        "the selected hardware item."
                    ),
                },
                _("Item Criticality:"),
                "gchararray",
            ],
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        # Move the item criticality RAMSTKTextView() below it's label.
        _fixed: Gtk.Fixed = self.get_children()[0].get_children()[0].get_child()
        _label: RAMSTKLabel = _fixed.get_children()[-2]
        _x_pos: int = _fixed.child_get_property(_label, "x")
        _y_pos: int = _fixed.child_get_property(_label, "y") + 25
        _fixed.move(self.txtItemCriticality.scrollwindow, _x_pos, _y_pos)

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self._do_load_item_criticality,
            "succeed_calculate_mode_criticality",
        )

    def _do_load_item_criticality(self, item_criticality: Dict[str, float]) -> None:
        """Update the item criticality RAMSTKTextView() with the results.

        :param item_criticality: the item criticality for the selected
            hardware item.
        :return: None
        :rtype: None
        """
        _item_criticality = ""
        for _key, _value in item_criticality.items():
            _item_criticality = _item_criticality + _key + ": " + str(_value) + "\n"

        self.txtItemCriticality.do_update(_item_criticality, "changed")


class FMEATreePanel(RAMSTKTreePanel):
    """Panel to display FMEA analysis."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_retrieve_modes"
    _tag = "fmea"
    _title = _("Failure Mode and Effects Analysis")

    # Define public dictionary class attributes.

    # Define public dictionary list attributes.

    # Define public dictionary scalar attributes.

    # Define private dictionary class attributes.

    def __init__(self):
        """Initialize an instance of the FMEA analysis panel."""
        super().__init__()

        # Initialize private dictionary attributes.
        self._dic_mission_phases: Dict[str, List[str]] = {"": [""]}
        self.tvwTreeView.dic_row_loader = {
            "mode": self.__do_load_mode,
            "mechanism": self.__do_load_mechanism,
            "cause": self.__do_load_cause,
            "control": self.__do_load_control,
            "action": self.__do_load_action,
        }
        self._dic_visible_mask: Dict[str, List[str]] = {
            "mode": [
                "False",
                "False",
                "True",
                "False",
                "False",
                "False",
                "False",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "True",
                "True",
                "False",
                "True",
                "False",
            ],
            "mechanism": [
                "False",
                "False",
                "False",
                "True",
                "False",
                "False",
                "False",
                "True",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "True",
                "True",
                "True",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "True",
                "True",
                "True",
                "False",
                "False",
                "True",
                "False",
                "False",
            ],
            "cause": [
                "False",
                "False",
                "False",
                "False",
                "True",
                "False",
                "False",
                "True",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "True",
                "True",
                "True",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "True",
                "True",
                "True",
                "False",
                "False",
                "False",
                "False",
                "False",
            ],
            "control": [
                "False",
                "False",
                "False",
                "False",
                "False",
                "True",
                "False",
                "True",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
            ],
            "action": [
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "True",
                "True",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "True",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
            ],
        }

        # Initialize private list attributes.
        self._lst_missions: List[str] = [""]

        # Initialize private scalar attributes.
        self._on_edit_message: str = f"wvw_editing_{self._tag}"

        # Initialize public dictionary attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "revision_id": [
                0,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Revision ID"),
                "gint",
            ],
            "hardware_id": [
                1,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Hardware ID"),
                "gint",
            ],
            "mode_id": [
                2,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Mode ID"),
                "gint",
            ],
            "mechanism_id": [
                3,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Mechanism ID"),
                "gint",
            ],
            "cause_id": [
                4,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Cause ID"),
                "gint",
            ],
            "control_id": [
                5,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Control ID"),
                "gint",
            ],
            "action_id": [
                6,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Action ID"),
                "gint",
            ],
            "description": [
                7,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Description"),
                "gchararray",
            ],
            "mission": [
                8,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Applicable Mission"),
                "gchararray",
            ],
            "mission_phase": [
                9,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_toggled,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Applicable Mission Phase"),
                "gchararray",
            ],
            "effect_local": [
                10,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Local Effect"),
                "gchararray",
            ],
            "effect_next": [
                11,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Next Effect"),
                "gchararray",
            ],
            "effect_end": [
                12,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("End Effect"),
                "gchararray",
            ],
            "detection_method": [
                13,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Detection Method"),
                "gchararray",
            ],
            "other_indications": [
                14,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Other Indications"),
                "gchararray",
            ],
            "isolation_method": [
                15,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Isolation Method"),
                "gchararray",
            ],
            "design_provisions": [
                16,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Design Provisions"),
                "gchararray",
            ],
            "operator_actions": [
                17,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Operator Actions"),
                "gchararray",
            ],
            "severity_class": [
                18,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Safety Severity"),
                "gchararray",
            ],
            "hazard_rate_source": [
                19,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Hazard Rate Data Source"),
                "gchararray",
            ],
            "mode_probability": [
                20,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Failure Probability"),
                "gchararray",
            ],
            "effect_probability": [
                21,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Effect Probability (beta)"),
                "gfloat",
            ],
            "mode_ratio": [
                22,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Mode Ratio (alpha)"),
                "gfloat",
            ],
            "mode_hazard_rate": [
                23,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Mode Hazard Rate"),
                "gfloat",
            ],
            "mode_op_time": [
                24,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Mode Operating Time"),
                "gfloat",
            ],
            "mode_criticality": [
                25,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Mode Criticality (Cm)"),
                "gfloat",
            ],
            "type_id": [
                26,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Control Type"),
                "gchararray",
            ],
            "rpn_severity": [
                27,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("RPN Severity"),
                "gint",
            ],
            "rpn_occurrence": [
                28,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("RPN Occurrence"),
                "gint",
            ],
            "rpn_detection": [
                29,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("RPN Detection"),
                "gint",
            ],
            "rpn": [
                30,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("RPN"),
                "gint",
            ],
            "action_category": [
                31,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Action Category"),
                "gchararray",
            ],
            "action_owner": [
                32,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Action Owner"),
                "gchararray",
            ],
            "action_due_date": [
                33,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Action Due Date"),
                "gchararray",
            ],
            "action_status": [
                34,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Action Status"),
                "gchararray",
            ],
            "action_taken": [
                35,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Action Taken"),
                "gchararray",
            ],
            "action_approved": [
                36,
                Gtk.CellRendererToggle(),
                "toggled",
                super().on_cell_toggled,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Action Approved"),
                "gint",
            ],
            "action_approve_date": [
                37,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Approval Date"),
                "gchararray",
            ],
            "action_closed": [
                38,
                Gtk.CellRendererToggle(),
                "toggled",
                super().on_cell_toggled,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Action Closed"),
                "gint",
            ],
            "action_close_date": [
                39,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Action Closure Date"),
                "gchararray",
            ],
            "rpn_severity_new": [
                40,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("New RPN Severity"),
                "gint",
            ],
            "rpn_occurrence_new": [
                41,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("New RPN Occurence"),
                "gint",
            ],
            "rpn_detection_new": [
                42,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("New RPN Detection"),
                "gint",
            ],
            "rpn_new": [
                43,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("New RPN"),
                "gint",
            ],
            "critical_item": [
                44,
                Gtk.CellRendererToggle(),
                "toggled",
                super().on_cell_toggled,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Critical Item"),
                "gint",
            ],
            "single_point": [
                45,
                Gtk.CellRendererToggle(),
                "toggled",
                super().on_cell_toggled,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Single Point"),
                "gint",
            ],
            "pof_include": [
                46,
                Gtk.CellRendererToggle(),
                "toggled",
                super().on_cell_toggled,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Include in PoF"),
                "gint",
            ],
            "remarks": [
                47,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Remarks"),
                "gchararray",
            ],
        }
        self.dic_icons: Dict[str, str] = {}

        # Initialize public list attributes.
        self.lst_action_category: List[str] = []
        self.lst_action_status: List[str] = []
        self.lst_control_types: List[str] = []
        self.lst_rpn_detection: List[str] = []
        self.lst_rpn_occurrence: List[str] = []
        self.lst_rpn_severity: List[str] = []
        self.lst_mode_probability: List[str] = []
        self.lst_severity_class: List[str] = []
        self.lst_users: List[str] = []

        # Initialize public scalar attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.tvwTreeView.set_tooltip_text(
            _(
                "Displays the (Design) Failure Mode and Effects "
                "(and Criticality) Analysis [(D)FME(C)A] for the "
                "currently selected Hardware item."
            )
        )

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_panel, "succeed_retrieve_hardware_fmea")
        pub.subscribe(super().do_load_panel, "succeed_calculate_rpn")
        pub.subscribe(super().do_load_panel, "succeed_delete_action")
        pub.subscribe(super().do_load_panel, "succeed_delete_cause")
        pub.subscribe(super().do_load_panel, "succeed_delete_control")
        pub.subscribe(super().do_load_panel, "succeed_delete_mechanism")
        pub.subscribe(super().do_load_panel, "succeed_delete_mode")
        pub.subscribe(self._on_insert, "succeed_insert_action")
        pub.subscribe(self._on_insert, "succeed_insert_cause")
        pub.subscribe(self._on_insert, "succeed_insert_control")
        pub.subscribe(self._on_insert, "succeed_insert_mechanism")
        pub.subscribe(self._on_insert, "succeed_insert_mode")

        pub.subscribe(self.__do_load_missions, "succeed_retrieve_usage_profile")

    def do_load_comboboxes(self) -> None:
        """Load the Gtk.CellRendererCombo()s.

        :return: None
        :rtype: None
        """
        self.__do_load_action_category()
        self.__do_load_action_status()
        self.__do_load_control_type()
        self.__do_load_mode_probability()
        self.__do_load_rpn_detection()
        self.__do_load_rpn_occurrence()
        self.__do_load_rpn_severity()
        self.__do_load_severity_class()
        self.__do_load_users()

        _cell = self.tvwTreeView.get_column(
            self.tvwTreeView.position["mission"]
        ).get_cells()
        _cell[0].connect("edited", self._on_mission_change)

    # noinspection PyUnusedLocal
    def _on_insert(
        self, node_id: int, tree: treelib.Tree  # pylint: disable=unused-argument
    ) -> None:
        """This is a wrapper method for the metaclass' do_load_panel().

        The do_insert() method sends a message with node_id and the updated tree as
        data packages.  The metaclass' do_load_panel() only wants the tree passed to
        it.

        :return: None
        :rtype:
        """
        return super().do_load_panel(tree)

    def _on_mission_change(
        self, __combo: Gtk.CellRendererCombo, path: str, new_text: str
    ) -> None:
        """Load the mission phases whenever the mission combo is changed.

        :param __combo: the mission list Gtk.CellRendererCombo().  Unused in
            this method.
        :param path: the path identifying the edited cell.
        :param new_text: the new text (mission description).
        :return: None
        :rtype: None
        """
        self.__do_load_mission_phases(new_text)

        _model = self.tvwTreeView.get_model()
        _model[path][self.tvwTreeView.position["mission_phase"]] = ""

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the FMEA Work View RAMSTKTreeView().

        This method is called whenever a RAMSTKTreeView() row is activated.

        :param selection: the current Gtk.TreeViewSelection() in the
            FMEA RAMSTKTreView().
        :type selection: :class:`Gtk.TreeViewSelection`
        :return: None
        :rtype: None
        """
        _model, _row = selection.get_selected()

        if _row is not None:
            if _model.get_value(_row, 3) == 0:
                _level = "mode"
            elif _model.get_value(_row, 4) == 0:
                _level = "mechanism"
            elif _model.get_value(_row, 5) == 0:
                _level = "cause"
            elif _model.get_value(_row, 6) == 0:
                _level = "control"
            else:
                _level = "action"

            self.tvwTreeView.visible = self._dic_visible_mask[_level]
            self.tvwTreeView.do_set_visible_columns()

            _mission = _model.get_value(_row, 8)
            self.__do_load_mission_phases(_mission)

    def __do_get_rpn_names(
        self, entity: Union[RAMSTKCauseRecord, RAMSTKMechanismRecord]
    ) -> Tuple[str, str, str, str]:
        """Retrieve the RPN category for the selected mechanism or cause.

        :param entity: the RAMSTKMechanism or RAMSTKCause object to be read.
        :return: (_occurrence, _detection, _occurrence_new, _detection_new)
        :rtype: tuple
        """
        _occurrence = str(self.lst_occurrence[entity.rpn_occurrence])
        _detection = str(self.lst_detection[entity.rpn_detection])
        _occurrence_new = str(self.lst_occurrence[entity.rpn_occurrence_new])
        _detection_new = str(self.lst_detection[entity.rpn_detection_new])

        return _occurrence, _detection, _occurrence_new, _detection_new

    def __do_load_action(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load an action record into the RAMSTKTreeView().

        :param node: the treelib Node() with the action data to load.
        :param row: the parent row of the action to load into the FMEA form.
        :return: _new_row; the row that was just populated with action data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None
        _date_format = "%Y-%m-%d"

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.dic_icons["action"], 22, 22)

        _attributes = [
            _entity.revision_id,
            _entity.hardware_id,
            _entity.mode_id,
            _entity.mechanism_id,
            _entity.cause_id,
            _entity.control_id,
            _entity.action_id,
            _entity.action_recommended,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            "",
            "",
            "",
            "",
            0,
            _entity.action_category,
            _entity.action_owner,
            _entity.action_due_date.strftime(_date_format),
            _entity.action_status,
            _entity.action_taken,
            _entity.action_approved,
            _entity.action_approve_date.strftime(_date_format),
            _entity.action_closed,
            _entity.action_close_date.strftime(_date_format),
            "",
            "",
            "",
            0,
            0,
            0,
            0,
            "",
            _icon,
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading failure cause action {0:s} "
                "in the FMEA.  This might indicate it was missing it's data "
                "package, some of the data in the package was missing, or "
                "some of the data was the wrong type.  Row data was: "
                "{1}"
            ).format(str(node.identifier), _attributes)
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row

    def __do_load_action_category(self) -> None:
        """Load the action category Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["action_category"], self.lst_action_category
        )

    def __do_load_action_status(self) -> None:
        """Load the action status Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["action_status"], self.lst_action_status
        )

    def __do_load_cause(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure cause record into the RAMSTKTreeView().

        :param node: the treelib Node() with the cause data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the cause to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with cause data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        (
            _occurrence,
            _detection,
            _occurrence_new,
            _detection_new,
        ) = self.__do_get_rpn_names(_entity)

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.dic_icons["cause"], 22, 22)

        _attributes = [
            _entity.revision_id,
            _entity.hardware_id,
            _entity.mode_id,
            _entity.mechanism_id,
            _entity.cause_id,
            0,
            0,
            _entity.description,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            "",
            "",
            _occurrence,
            _detection,
            _entity.rpn,
            "",
            "",
            "",
            "",
            "",
            0,
            "",
            0,
            "",
            "",
            _occurrence_new,
            _detection_new,
            _entity.rpn_new,
            0,
            0,
            0,
            "",
            _icon,
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                f"An error occurred when loading failure cause {node.identifier} in "
                f"the FMEA.  This might indicate it was missing it's data package, "
                f"some of the data in the package was missing, or some of the "
                f"data was the wrong type.  Row data was: {_attributes}"
            )
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row

    def __do_load_control(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a control record into the RAMSTKTreeView().

        :param node: the treelib Node() with the control data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the control to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with control data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons["control"], 22, 22
        )

        _attributes = [
            _entity.revision_id,
            _entity.hardware_id,
            _entity.mode_id,
            _entity.mechanism_id,
            _entity.cause_id,
            _entity.control_id,
            0,
            _entity.description,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            _entity.type_id,
            "",
            "",
            "",
            0,
            "",
            "",
            "",
            "",
            "",
            0,
            "",
            0,
            "",
            "",
            "",
            "",
            0,
            0,
            0,
            0,
            "",
            _icon,
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                f"An error occurred when loading failure cause control "
                f"{node.identifier} in the FMEA.  This might indicate it was missing "
                f"it's data package, some of the data in the package was missing, or "
                f"some of the data was the wrong type.  Row data was: {_attributes}"
            )
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row

    def __do_load_control_type(self) -> None:
        """Load the control type Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["type_id"], self.lst_control_types
        )

    def __do_load_mechanism(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter:
        """Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the mechanism to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with mechanism data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        (
            _occurrence,
            _detection,
            _occurrence_new,
            _detection_new,
        ) = self.__do_get_rpn_names(_entity)

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons["mechanism"], 22, 22
        )

        _attributes = [
            _entity.revision_id,
            _entity.hardware_id,
            _entity.mode_id,
            _entity.mechanism_id,
            0,
            0,
            0,
            _entity.description,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            "",
            "",
            _occurrence,
            _detection,
            _entity.rpn,
            "",
            "",
            "",
            "",
            "",
            0,
            "",
            0,
            "",
            "",
            _occurrence_new,
            _detection_new,
            _entity.rpn_new,
            0,
            0,
            _entity.pof_include,
            "",
            _icon,
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                f"An error occurred when loading failure mechanism {node.identifier} "
                f"in the FMEA.  This might indicate it was missing it's data "
                f"package, some of the data in the package was missing, or "
                f"some of the data was the wrong type.  Row data was: {_attributes}"
            )
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row

    # noinspection PyUnusedLocal
    # pylint: disable=unused-argument
    def __do_load_missions(
        self,
        tree: treelib.Tree = treelib.Tree(),
        node_id: Any = "",
        row: Gtk.TreeIter = None,
    ) -> None:
        """Load the mission and mission phase dicts.

        :param tree: the treelib usage profile treelib.Tree().
        :param node_id: unused in this function.  Required so this method
            compatible with other listeners for the
            'succeed_retrieve_usage_profile' message.
        :param row: unused in this function.  Required so this method
            compatible with other listeners for the
            'succeed_retrieve_usage_profile' message.
        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_cell_model(self.tvwTreeView.position["mission"])

        self._lst_missions = []
        _model.append([""])
        for _node in tree.children(tree.root):
            _lst_phases: List[str] = [""]

            _mission = _node.data["usage_profile"].get_attributes()["description"]
            _model.append([_mission])
            self._lst_missions.append(_mission)

            for _node2 in tree.children(_node.identifier):
                _mission_phase = _node2.data["usage_profile"].get_attributes()[
                    "description"
                ]
                _lst_phases.append(_mission_phase)
            self._dic_mission_phases[_mission] = _lst_phases

    def __do_load_mission_phases(self, mission: str) -> None:
        """Load the mission phase Gtk.CellRendererCombo().

        :param mission: the mission that was selected.
        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_cell_model(
            self.tvwTreeView.position["mission_Phase"]
        )
        _model.clear()
        _model.append([""])

        try:
            for _phase in self._dic_mission_phases[mission]:
                _model.append([_phase])
        except KeyError:
            pass

    def __do_load_mode(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure mode record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the FMEA form.
        :return: _new_row; the row that was just populated with mode data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        _severity = self.lst_severity[_entity.rpn_severity]
        _severity_new = self.lst_severity[_entity.rpn_severity_new]

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.dic_icons["mode"], 22, 22)

        _attributes = [
            _entity.revision_id,
            _entity.hardware_id,
            _entity.mode_id,
            0,
            0,
            0,
            0,
            _entity.description,
            _entity.mission,
            _entity.mission_phase,
            _entity.effect_local,
            _entity.effect_next,
            _entity.effect_end,
            _entity.detection_method,
            _entity.other_indications,
            _entity.isolation_method,
            _entity.design_provisions,
            _entity.operator_actions,
            _entity.severity_class,
            _entity.hazard_rate_source,
            _entity.mode_probability,
            _entity.effect_probability,
            _entity.mode_ratio,
            _entity.mode_hazard_rate,
            _entity.mode_op_time,
            _entity.mode_criticality,
            "",
            _severity,
            "",
            "",
            0,
            "",
            "",
            "",
            "",
            "",
            0,
            "",
            0,
            "",
            _severity_new,
            "",
            "",
            0,
            _entity.critical_item,
            _entity.single_point,
            0,
            _entity.remarks,
            _icon,
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                f"An error occurred when loading failure mode {node.identifier} in the "
                f"FMEA.  This might indicate it was missing it's data package, "
                f"some of the data in the package was missing, or some of the "
                f"data was the wrong type.  Row data was: {_attributes}"
            )
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row

    def __do_load_mode_probability(self) -> None:
        """Load the mode probability Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["mode_probability"], self.lst_mode_probability
        )

    def __do_load_rpn_detection(self) -> None:
        """Load the RPN detection Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        for _key in ["rpn_detection", "rpn_detection_new"]:
            self.tvwTreeView.do_load_combo_cell(
                self.tvwTreeView.position[_key], self.lst_rpn_detection
            )

    def __do_load_rpn_occurrence(self) -> None:
        """Load the RPN occurrence Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        for _key in ["rpn_occurrence", "rpn_occurrence_new"]:
            self.tvwTreeView.do_load_combo_cell(
                self.tvwTreeView.position[_key], self.lst_rpn_occurrence
            )

    def __do_load_rpn_severity(self) -> None:
        """Load the RPN severity Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        for _key in ["rpn_severity", "rpn_severity_new"]:
            self.tvwTreeView.do_load_combo_cell(
                self.tvwTreeView.position[_key], self.lst_rpn_severity
            )

    def __do_load_severity_class(self) -> None:
        """Load the severity classification Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["severity_class"], self.lst_severity_class
        )

    def __do_load_users(self) -> None:
        """Load the RAMSTK users Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["action_owner"], self.lst_users
        )
