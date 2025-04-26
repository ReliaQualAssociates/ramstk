# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.allocation.goal_method_panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Allocation goal and methods panel module."""

# Standard Library Imports
from typing import Dict, List, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    WidgetConfig,
    make_widget_config,
)


class AllocationGoalMethodPanel(RAMSTKFixedPanel):
    """Panel to display reliability Allocation goals and method."""

    # Define private class attributes.
    _record_field = "hardware_id"
    _select_msg = "succeed_get_allocation_attributes"
    _tag = "allocation"
    _title = _("Allocation Goals and Method")

    def __init__(self):
        """Initialize an instance of the Allocation goals and method panel."""
        super().__init__()

        # Initialize widgets.
        self.cmbAllocationGoal: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbAllocationMethod: RAMSTKComboBox = RAMSTKComboBox()
        self.txtHazardRateGoal: RAMSTKEntry = RAMSTKEntry()
        self.txtMTBFGoal: RAMSTKEntry = RAMSTKEntry()
        self.txtReliabilityGoal: RAMSTKEntry = RAMSTKEntry()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.cmbAllocationGoal,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "goal_measure_id",
                    "index": 23,
                    "label_text": _("Select Goal Metric:"),
                    "listen_topic": "mvw_editing_allocation",
                    "send_topic": "wvw_editing_allocation",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "Selects the goal measure for the selected hardware assembly."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbAllocationMethod,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "allocation_method_id",
                    "index": 24,
                    "label_text": _("Select Goal Method:"),
                    "listen_topic": "mvw_editing_allocation",
                    "send_topic": "wvw_editing_allocation",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "Selects the goal measure for the selected hardware assembly."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtReliabilityGoal,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "reliability_goal",
                    "index": 25,
                    "label_text": _("R(t) Goal:"),
                    "listen_topic": "mvw_editing_allocation",
                    "send_topic": "wvw_editing_allocation",
                },
                {
                    "editable": True,
                    "width": 125,
                    "tooltip": _(
                        "Displays the reliability goal for the selected hardware item."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtHazardRateGoal,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "hazard_rate_goal",
                    "index": 26,
                    "label_text": _("h(t) Goal:"),
                    "listen_topic": "mvw_editing_allocation",
                    "send_topic": "wvw_editing_allocation",
                },
                {
                    "editable": True,
                    "width": 125,
                    "tooltip": _(
                        "Displays the hazard rate goal for the selected hardware item."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtMTBFGoal,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "mtbf_goal",
                    "index": 27,
                    "label_text": _("MTBF Goal:"),
                    "listen_topic": "mvw_editing_allocation",
                    "send_topic": "wvw_editing_allocation",
                },
                {
                    "editable": True,
                    "width": 125,
                    "tooltip": _(
                        "Displays the MTBF goal for the selected hardware item."
                    ),
                    "visible": True,
                },
            ),
        ]
        self._goal_id: int = 0

        # Initialize public instance attributes.
        self.method_id: int = 0

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_fixed_panel()
        self._do_set_widget_callbacks()
        self._do_load_allocation_goal()
        self._do_load_allocation_methods()

    def _do_load_allocation_goal(self) -> None:
        """Load the allocation goal RAMSTKComboBox."""
        self.cmbAllocationGoal.do_load_combo(
            entries=[
                [_("Reliability"), 0],
                [_("Hazard Rate"), 1],
                [_("MTBF"), 2],
            ],
        )

    def _do_load_allocation_methods(self) -> None:
        """Load the allocation method RAMSTKComboBox."""
        self.cmbAllocationMethod.do_load_combo(
            entries=[
                [_("Equal Apportionment"), 0],
                [_("AGREE Apportionment"), 1],
                [_("ARINC Apportionment"), 2],
                [_("Feasibility of Objectives"), 3],
            ],
        )

    def _do_set_sensitive(self, attributes: Dict[str, Union[float, int, str]]) -> None:
        """Set widget sensitivity as needed for the selected R(t) goal."""
        self.cmbAllocationGoal.set_sensitive(True)
        self.cmbAllocationGoal.do_update(
            {"goal_measure_id": attributes["goal_measure_id"]}
        )
        self.cmbAllocationMethod.set_sensitive(True)
        self.cmbAllocationMethod.do_update(
            {"allocation_method_id": attributes["allocation_method_id"]}
        )
        self.txtReliabilityGoal.set_sensitive(False)
        self.txtMTBFGoal.set_sensitive(False)
        self.txtHazardRateGoal.set_sensitive(False)

        if self._goal_id == 1:  # Expressed as reliability.
            self.txtReliabilityGoal.set_sensitive(True)
            self.txtReliabilityGoal.do_update(
                {"reliability_goal": attributes["reliability_goal"]}
            )
        elif self._goal_id == 2:  # Expressed as a hazard rate.
            self.txtHazardRateGoal.set_sensitive(True)
            self.txtHazardRateGoal.do_update(
                {"hazard_rate_goal": attributes["hazard_rate_goal"]}
            )
        elif self._goal_id == 3:  # Expressed as an MTBF.
            self.txtMTBFGoal.set_sensitive(True)
            self.txtMTBFGoal.do_update({"mtbf_goal": attributes["mtbf_goal"]})

    def _do_set_widget_callbacks(self) -> None:
        """Set the callback methods for the Allocation goal and method panel."""
        self.cmbAllocationGoal.dic_handler_id["changed"] = (
            self.cmbAllocationGoal.connect(
                "changed",
                self._on_goal_changed,
            )
        )
        self.cmbAllocationMethod.dic_handler_id["changed"] = (
            self.cmbAllocationMethod.connect(
                "changed",
                self._on_method_changed,
            )
        )

    def _on_goal_changed(self, combo: RAMSTKComboBox) -> None:
        """Let others know when allocation goal combo changes.

        :param combo: the allocation goal type RAMSTKComboBox.
        """
        self._goal_id = combo.get_active()
        if self._goal_id == 1:  # Expressed as reliability.
            self.txtReliabilityGoal.set_sensitive(True)
        elif self._goal_id == 2:  # Expressed as a hazard rate.
            self.txtHazardRateGoal.set_sensitive(True)
        elif self._goal_id == 3:  # Expressed as an MTBF.
            self.txtMTBFGoal.set_sensitive(True)

    def _on_method_changed(self, combo: RAMSTKComboBox) -> None:
        """Let others know when allocation method combo changes.

        :param combo: the allocation calculation method RAMSTKComboBox.
        """
        self.method_id = combo.get_active()

        pub.sendMessage(
            "succeed_change_allocation_method",
            method_id=self.method_id,
        )
