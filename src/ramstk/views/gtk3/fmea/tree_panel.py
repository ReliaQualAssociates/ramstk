# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.fmea.tree_panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The FMEA tree panel module."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple, Union

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import GdkPixbuf, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCellRendererCombo,
    RAMSTKCellRendererText,
    RAMSTKCellRendererToggle,
    RAMSTKTreePanel,
    WidgetConfig,
    make_widget_config,
)


class FMEATreePanel(RAMSTKTreePanel):
    """Panel to display FMEA analysis."""

    # Define private class attributes.
    _dic_visible_mask: Dict[str, List[bool]] = {
        "mode": [
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            True,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            True,
            True,
            True,
            False,
            True,
        ],
        "mechanism": [
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            True,
            False,
            False,
            True,
            False,
        ],
        "cause": [
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ],
        "control": [
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ],
        "action": [
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ],
    }
    _select_msg = "succeed_retrieve_fmeca"
    _tag = "fmeca"
    _title = _("Failure Mode and Effects Analysis")

    # Define public class attributes.
    lst_control_types = ["", "Detection", "Prevention"]

    def __init__(self):
        """Initialize an instance of the FMEA analysis panel."""
        super().__init__()

        # Initialize private instance attributes.
        self._dic_mission_phases: Dict[str, List[str]] = {"": [""]}
        self._lst_missions: List[str] = [""]
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "revision_id",
                    "index": 0,
                    "label_text": _("Revision ID"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "hardware_id",
                    "index": 1,
                    "label_text": _("Hardware ID"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "mode_id",
                    "index": 2,
                    "label_text": _("Mode ID"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "mechanism_id",
                    "index": 3,
                    "label_text": _("Mechanism ID"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "cause_id",
                    "index": 4,
                    "label_text": _("Cause ID"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "control_id",
                    "index": 5,
                    "label_text": _("Control ID"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "action_id",
                    "index": 6,
                    "label_text": _("Action ID"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "description",
                    "index": 7,
                    "label_text": _("Description"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "mission",
                    "index": 8,
                    "label_text": _("Applicable Mission"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "mission_phase",
                    "index": 9,
                    "label_text": _("Applicable Mission Phase"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "effect_local",
                    "index": 10,
                    "label_text": _("Local Effect"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "effect_next",
                    "index": 11,
                    "label_text": _("Next Effect"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "effect_end",
                    "index": 12,
                    "label_text": _("End Effect"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "detection_method",
                    "index": 13,
                    "label_text": _("Detection Method"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "other_indications",
                    "index": 14,
                    "label_text": _("Other Indications"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "isolation_method",
                    "index": 15,
                    "label_text": _("Isolation Method"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "design_provisions",
                    "index": 16,
                    "label_text": _("Design Provisions"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "operator_actions",
                    "index": 17,
                    "label_text": _("Operator Actions"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "severity_class",
                    "index": 18,
                    "label_text": _("Safety Severity"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "hazard_rate_source",
                    "index": 19,
                    "label_text": _("Hazard Rate Data Source"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "mode_probability",
                    "index": 20,
                    "label_text": _("Failure Probability"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "effect_probability",
                    "index": 21,
                    "label_text": _("Effect Probability (beta)"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "mode_ratio",
                    "index": 22,
                    "label_text": _("Mode Ratio (alpha)"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "mode_hazard_rate",
                    "index": 23,
                    "label_text": _("Mode Hazard Rate"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "mode_op_time",
                    "index": 24,
                    "label_text": _("Mode Operating Time"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "mode_criticality",
                    "index": 25,
                    "label_text": _("Mode Criticality (Cm)"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "type_id",
                    "index": 26,
                    "label_text": _("Control Type"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "rpn_severity",
                    "index": 27,
                    "label_text": _("RPN Severity"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "rpn_occurrence",
                    "index": 28,
                    "label_text": _("RPN Occurrence"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_mechanism",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "rpn_detection",
                    "index": 29,
                    "label_text": _("RPN Detection"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_mechanism",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "rpn",
                    "index": 30,
                    "label_text": _("RPN"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_mechanism",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "action_category",
                    "index": 31,
                    "label_text": _("Action Category"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_action",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "action_owner",
                    "index": 32,
                    "label_text": _("Action Owner"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_action",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "action_due_date",
                    "index": 33,
                    "label_text": _("Action Due Date"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_action",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "action_status",
                    "index": 34,
                    "label_text": _("Action Status"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_action",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "action_taken",
                    "index": 35,
                    "label_text": _("Action Taken"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_action",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererToggle(),
                {
                    "datatype": "gboolean",
                    "default": False,
                    "field": "action_approved",
                    "index": 36,
                    "label_text": _("Action Approved"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_action",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "action_approve_date",
                    "index": 37,
                    "label_text": _("Action Approve Date"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_action",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererToggle(),
                {
                    "datatype": "gboolean",
                    "default": False,
                    "field": "action_closed",
                    "index": 38,
                    "label_text": _("Action Closed"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_action",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "action_close_date",
                    "index": 39,
                    "label_text": _("Action Close Date"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_action",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "rpn_severity_new",
                    "index": 40,
                    "label_text": _("RPN Severity (New)"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_mechanism",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "rpn_occurrence_new",
                    "index": 41,
                    "label_text": _("RPN Occurrence (New)"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_mechanism",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "rpn_detection_new",
                    "index": 42,
                    "label_text": _("RPN Detection (New)"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_mechanism",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "rpn_new",
                    "index": 43,
                    "label_text": _("RPN (New)"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_mechanism",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererToggle(),
                {
                    "datatype": "gboolean",
                    "default": False,
                    "field": "critical_item",
                    "index": 44,
                    "label_text": _("Critical Item"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererToggle(),
                {
                    "datatype": "gboolean",
                    "default": False,
                    "field": "single_point",
                    "index": 45,
                    "label_text": _("Single Point Failure"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererToggle(),
                {
                    "datatype": "gboolean",
                    "default": False,
                    "field": "pof_include",
                    "index": 46,
                    "label_text": _("Include in PoF"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "remarks",
                    "index": 47,
                    "label_text": _("Remarks"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
        ]
        self._filtered_tree = True
        self._on_edit_message: str = f"wvw_editing_{self._tag}"

        # Initialize public instance attributes.
        self.dic_icons: Dict[str, str] = {}
        self.lst_control_types: List[str] = []
        self.clear_modes: bool = False
        self.level: str = "mode"

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_tree_panel()
        super().do_set_widget_callbacks()
        self._do_load_control_types()

        self.tvwTreeView.dic_row_loader = {
            "mode": self.__do_load_mode,
            "mechanism": self.__do_load_mechanism,
            "cause": self.__do_load_cause,
            "control": self.__do_load_control,
            "action": self.__do_load_action,
        }
        self.tvwTreeView.set_tooltip_text(
            _(
                "Displays the (Design) Failure Mode and Effects (and Criticality) "
                "Analysis [(D)FME(C)A] for the currently selected Hardware item."
            )
        )

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "succeed_retrieve_fmeca": super().do_load_tree_panel,
                "succeed_calculate_rpn": super().do_load_tree_panel,
                "selected_hardware": self._on_select_hardware,
                "hardware_category_changed": self.__do_clear_modes_on_category_change,
                "changed_subcategory": self.__do_clear_modes_on_subcategory_change,
                "succeed_retrieve_usage_profile": self.__do_load_missions,
            }
        )

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_filter_tree(
        self, model: Gtk.TreeModel, row: Gtk.TreeIter, data: Any
    ) -> bool:
        """Filter FMEA to show only those rows associated with the selected Hardware.

        :param model: the filtered model for the FMEA RAMSTKTreeView.
        :param row: the iter to check against condition(s).
        :param data: unused in this method; required by Gtk.TreeModelFilter() widget.
        :return: True if row should be visible, False else.
        :rtype: bool
        """
        return model[row][1] == self._parent_id

    def do_get_fmea_level(self, model: Gtk.TreeModel, row: Gtk.TreeIter) -> None:
        """Determine the FMEA level of the selected FMEA row.

        :param model: the FMEA Gtk.TreeModel().
        :param row: the selected Gtk.TreeIter() in the FMECA.
        """
        _cid = ""

        for _col in [2, 3, 4, 5, 6]:
            _cid = f"{_cid}{int(bool(model.get_value(row, _col)))}"

        self.level = {
            "10000": "mode",
            "11000": "mechanism",
            "11100": "cause",
            "11110": "control",
            "11101": "action",
        }[_cid]

    def do_load_comboboxes(self) -> None:
        """Load the RAMSTKCellRendererCombos."""
        _cell = self.tvwTreeView.get_column(
            self.tvwTreeView.dic_field_position_map["mission"]
        ).get_cells()
        _cell[0].connect("edited", self._on_mission_change)

    # noinspection PyUnusedLocal
    def _on_cell_edit(
        self,
        cell: Gtk.CellRenderer,
        path: str,
        new_text: str,
        key: str,
        message: str,  # pylint: disable=unused-argument
    ) -> None:
        """Handle edits of description column to ensure proper level is updated.

        :param cell: the Gtk.CellRenderer() that was edited.
        :param path: the RAMSTKTreeView() path of the Gtk.CellRenderer() that was
            edited.
        :param new_text: the new text in the edited Gtk.CellRenderer().
        :param key: the column key of the edited Gtk.CellRenderer().
        :param message: the PyPubSub message to publish.
        :return: None
        """
        super().on_cell_edit(
            cell,
            path,
            new_text,
            key,
            f"wvw_editing_{self.level}",
        )

    def _on_mission_change(
        self, __combo: RAMSTKCellRendererCombo, path: str, new_text: str
    ) -> None:
        """Load the mission phases whenever the mission combo is changed.

        :param __combo: the mission list RAMSTKCellRendererCombo(). Unused in this
            method.
        :param path: the path identifying the edited cell.
        :param new_text: the new text (mission description).
        """
        self.__do_load_mission_phases(new_text)

        _model = self.tvwTreeView.get_model()
        _model[path][self.tvwTreeView.position["mission_phase"]] = ""

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the FMEA Work View RAMSTKTreeView().

        This method is called whenever a RAMSTKTreeView() row is activated.

        :param selection: the current Gtk.TreeViewSelection() in the FMECA
            RAMSTKTreView().
        """
        _model, _row = selection.get_selected()
        if _row is None:
            return

        _attributes = super().on_row_change(selection)
        try:
            _attributes["type_id"] = self.lst_control_types.index(
                _attributes["type_id"]
            )
        except ValueError:
            _attributes["type_id"] = 0

        self.do_get_fmea_level(_model, _row)
        self._record_id = _attributes[f"{self.level}_id"]
        super().do_set_visible_columns()

        self.__do_load_mission_phases(_model.get_value(_row, 8))

        pub.sendMessage(
            f"selected_{self.level}",
            attributes=_attributes,
        )

    def _on_select_hardware(
        self, attributes: Dict[str, Union[int, float, str]]
    ) -> None:
        """Filter FMEA when Hardware is selected.

        :param attributes: the dict of attributes for the selected Hardware.
        """
        self._parent_id = attributes["hardware_id"]
        self.tvwTreeView.filt_model.refilter()

    def __do_clear_modes(self) -> None:
        """Clear existing failure modes from the FMEA worksheet and RAMSTK database."""
        _row = self.tvwTreeView.get_model().get_iter_first()

        while _row is not None:
            pub.sendMessage(
                "request_delete_mode",
                node_id=self.tvwTreeView.get_model().get_value(_row, 2),
            )
            _row = self.tvwTreeView.get_model().iter_next(_row)

    # noinspection PyUnusedLocal
    def __do_clear_modes_on_category_change(
        self,
        attributes: Dict[str, int],  # pylint: disable=unused-argument
    ) -> None:
        """Clear existing failure modes when a new component category is selected.

        This is a wrapper for __do_clear_modes().

        :param attributes: the ID of the newly selected component category.
        """
        if self.clear_modes:
            self.__do_clear_modes()

    # noinspection PyUnusedLocal
    def __do_clear_modes_on_subcategory_change(
        self,
        subcategory_id: int,  # pylint: disable=unused-argument
    ) -> None:
        """Clear existing failure modes when a new component subcategory is selected.

        This is a wrapper for __do_clear_modes().

        :param subcategory_id: the ID of the newly selected component subcategory.
        """
        if self.clear_modes:
            self.__do_clear_modes()

    def __do_get_rpn_names(
        self,
        entity: object,
    ) -> Tuple[str, str, str, str]:
        """Retrieve the RPN category for the selected mechanism or cause.

        :param entity: the RAMSTKMechanism or RAMSTKCause object to be read.
        :return: (_occurrence, _detection, _occurrence_new, _detection_new)
        :rtype: tuple
        """
        _occurrence = str(
            self.lst_rpn_occurrence[entity.rpn_occurrence],  # type: ignore
        )
        _detection = str(self.lst_rpn_detection[entity.rpn_detection])  # type: ignore
        _occurrence_new = str(
            self.lst_rpn_occurrence[entity.rpn_occurrence_new],  # type: ignore
        )
        _detection_new = str(
            self.lst_rpn_detection[entity.rpn_detection_new],  # type: ignore
        )

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

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.dic_icons["action"], 22, 22)

        _attributes = [
            _entity.revision_id,
            _entity.hardware_id,
            _entity.mode_id,
            _entity.mechanism_id,
            _entity.cause_id,
            0,
            _entity.action_id,
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
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
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

    def do_load_action_category(
        self, categories: Dict[int, Tuple[str, str, int]]
    ) -> None:
        """Load the action category RAMSTKCellRendererCombo.

        :param categories: the dict of action category records to load.
        """
        _categories = [categories[_category][1] for _category in categories]
        self.tvwTreeView.do_load_cellrenderercombo(
            "action_category",
            _categories,
        )

    def do_load_action_status(self, status: Dict[int, Tuple[str, str]]) -> None:
        """Load the action status RAMSTKCellRendererCombo.

        :param status: the dict of action status records to load.
        """
        _status = [status[_stat][0] for _stat in status]
        self.tvwTreeView.do_load_cellrenderercombo("action_status", _status)

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
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
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
            self._lst_control_type[_entity.type_id],
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
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
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

    def _do_load_control_types(self) -> None:
        """Load the control type RAMSTKCellRendererCombo."""
        self.tvwTreeView.do_load_cellrenderercombo("type_id", self.lst_control_types)

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
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
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
        node_id: str = "",
        row: Gtk.TreeIter = None,
    ) -> None:
        """Load the mission and mission phase dicts.

        :param tree: the treelib usage profile treelib.Tree().
        :param node_id: unused in this function. Required so this method compatible with
            other listeners for the 'succeed_retrieve_usage_profile' message.
        :param row: unused in this function. Required so this method compatible with
            other listeners for the 'succeed_retrieve_usage_profile' message.
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
        """Load the mission phase RAMSTKCellRendererCombo.

        :param mission: the mission that was selected.
        """
        _model = self.tvwTreeView.get_cell_model(
            self.tvwTreeView.position["mission_phase"]
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
        # FIXME: There should only be one loading method that handles everything (
        #  modes, mechanisms, causes, actions, and controls).
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _severity = self.lst_rpn_severity[_entity.rpn_severity]
        _severity_new = self.lst_rpn_severity[_entity.rpn_severity_new]

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
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
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

    def do_load_mode_probability(
        self, probabilities: List[List[Union[str, int]]]
    ) -> None:
        """Load the mode probability RAMSTKCellRendererCombo.

        :param probabilities: the list of mode probabilities to load.
        """
        _probabilities = [_probability[0] for _probability in probabilities]
        self.tvwTreeView.do_load_cellrenderercombo(
            "mode_probability",
            _probabilities,
        )

    def do_load_rpn_detection(self, detections: Dict[int, Tuple[str]]) -> None:
        """Load the RPN detection RAMSTKCellRendererCombo.

        :param detections: the dict of RPN detection records to load.
        """
        _detections = [detections[_detection][0] for _detection in detections]
        for _key in ["rpn_detection", "rpn_detection_new"]:
            self.tvwTreeView.do_load_cellrenderercombo(_key, _detections)

    def do_load_rpn_occurrence(self, occurrences: Dict[int, Tuple[str]]) -> None:
        """Load the RPN occurrence RAMSTKCellRendererCombo.

        :param occurrences: the dict of RPN occurrence records to load.
        """
        _occurrences = [occurrences[_occurrence][0] for _occurrence in occurrences]
        for _key in ["rpn_occurrence", "rpn_occurrence_new"]:
            self.tvwTreeView.do_load_cellrenderercombo(_key, _occurrences)

    def do_load_rpn_severity(self, severities: Dict[int, Tuple[str]]) -> None:
        """Load the RPN severity RAMSTKCellRendererCombo.

        :param severities: the dict of RPN severity records to load.
        """
        _severities = [severities[_severity][0] for _severity in severities]
        for _key in ["rpn_severity", "rpn_severity_new"]:
            self.tvwTreeView.do_load_cellrenderercombo(_key, _severities)

    def do_load_severity_class(self, severities: List[List[Union[int, str]]]) -> None:
        """Load the severity classification RAMSTKCellRendererCombo.

        :param severities: the list of severity classification records to load.
        """
        _severities = [f"{_severity[2]} - {_severity[0]}" for _severity in severities]
        self.tvwTreeView.do_load_cellrenderercombo("severity_class", _severities)

    def do_load_users(self, users: Dict[int, Tuple[str, str, str, str, str]]) -> None:
        """Load the RAMSTK users RAMSTKCellRendererCombo.

        :param users: a dict containing the RAMSTK user information.
        """
        _users = [f"{users[_user][0]}, {users[_user][1]}" for _user in users]
        self.tvwTreeView.do_load_cellrenderercombo("action_owner", _users)
