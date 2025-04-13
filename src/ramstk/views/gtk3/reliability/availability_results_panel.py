# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.reliability.availability_results_panel.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Availability Results panel module."""

# Standard Library Imports
import locale
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKEntry, RAMSTKFixedPanel, WidgetConfig


class AvailabilityResultsPanel(RAMSTKFixedPanel):
    """Panel to display availability results for the selected Hardware item."""

    # Define private class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_reliability_attributes"
    _tag: str = "reliability"
    _title: str = _("Availability Assessment Results")

    def __init__(self) -> None:
        """Initialize an instance of the Availability Results panel."""
        super().__init__()

        # Initialize widgets.
        self.txtCostFailure: RAMSTKEntry = RAMSTKEntry()
        self.txtCostHour: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsAt: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsAtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionAt: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionAtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtPartCount: RAMSTKEntry = RAMSTKEntry()
        self.txtTotalCost: RAMSTKEntry = RAMSTKEntry()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": self.txtLogisticsAt,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "availability_logistics",
                    "index": 3,
                    "label_text": _("Logistics Availability [A(t)]:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": False,
                    "tooltip": _(
                        "Displays the logistics availability for the selected hardware "
                        "item."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtLogisticsAtVar,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "avail_log_variance",
                    "index": 5,
                    "label_text": "",
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": False,
                    "tooltip": _(
                        "Displays the variance on the logistics availability for the "
                        "selected hardware item."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtMissionAt,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "availability_mission",
                    "index": 4,
                    "label_text": _("Mission A(t):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": False,
                    "tooltip": _(
                        "Displays the mission availability for the selected hardware "
                        "item."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtMissionAtVar,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "avail_mis_variance",
                    "index": 6,
                    "label_text": "",
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": False,
                    "tooltip": _(
                        "Displays the variance on the mission availability for the "
                        "selected hardware item."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtTotalCost,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "total_cost",
                    "index": 31,
                    "label_text": _("Total Cost:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": False,
                    "tooltip": _(
                        "Displays the total cost of the selected hardware item."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtCostFailure,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost_failure",
                    "index": 8,
                    "label_text": _("Cost/Failure:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": False,
                    "tooltip": _(
                        "Displays the cost per failure of the selected hardware item."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtCostHour,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "cost_hour",
                    "index": 9,
                    "label_text": _("Cost/Hour:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": False,
                    "tooltip": _(
                        "Displays the failure cost per life time hour for the selected "
                        "hardware item."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtPartCount,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "total_part_count",
                    "index": 32,
                    "label_text": _("Total # of Parts:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": False,
                    "tooltip": _(
                        "Displays the total part count for the selected hardware item."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()
        super().do_set_widget_callbacks()
        self.__do_nudge_widgets()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "succeed_get_hardware_attributes": self._do_load_entries_hardware,
            }
        )

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load contents of the RAMSTKEntry() widgets.

        This method ensures results RAMSTKEntry() widgets are set insensitive and loads
        the contents.  The PyPubSub subscriber is in the metaclass.
        """
        # FIXME: Is this method needed?  The metaclass do_load_panel should take care
        #  of this.
        self.txtLogisticsAt.do_update(
            {
                "availability_logistics": str(
                    self.fmt.format(attributes["availability_logistics"] or 1.0)
                ),
            }
        )
        self.txtLogisticsAtVar.do_update(
            {
                "avail_log_variance": str(
                    self.fmt.format(attributes["avail_log_variance"] or 0.0)
                )
            },
        )
        self.txtMissionAt.do_update(
            {
                "availability_mission": str(
                    self.fmt.format(attributes["availability_mission"] or 1.0)
                )
            },
        )
        self.txtMissionAtVar.do_update(
            {
                "avail_mis_variance": str(
                    self.fmt.format(attributes["avail_mis_variance"] or 0.0)
                )
            },
        )

    def _do_load_entries_hardware(self, attributes: Dict[str, Any]) -> None:
        """Load contents of the RAMSTKEntry() widgets.

        This method ensures results RAMSTKEntry() widgets are set insensitive and loads
        the contents.  The PyPubSub subscriber is in the metaclass.
        """
        # FIXME: Is this method needed?  The metaclass do_load_panel should take care
        #  of this.
        self.txtTotalCost.do_update(
            {"total_cost": str(locale.currency(attributes["total_cost"]))},
        )
        self.txtCostFailure.do_update(
            {"cost_failure": str(locale.currency(attributes["cost_failure"]))},
        )
        self.txtCostHour.do_update(
            {"cost_hour": str(locale.currency(attributes["cost_hour"]))},
        )
        self.txtPartCount.do_update(
            {"total_part_count": str(f"{attributes['total_part_count']}")},
        )

    def __do_nudge_widgets(self) -> None:
        """Adjust widgets from their default positions."""
        _lst_labels: List[object] = []
        _x_pos: List[int] = [
            0,
            self.txtLogisticsAt.get_preferred_size()[0].width + 5,
        ]
        _y_pos: List[int] = []
        _n_rows: int = 0

        _fixed = self.get_children()[0].get_children()[0].get_children()[0]
        _widgets = (
            self.get_children()[0].get_children()[0].get_children()[0].get_children()
        )

        for _widget in _widgets[::2]:
            _y_pos.append(_fixed.child_get_property(_widget, "y"))
            if _widget.get_text():
                _lst_labels.append(_widget)
                _x_pos[0] = max(_x_pos[0], _widget.get_preferred_size()[0].width)
                _n_rows += 1

        _x_pos[0] += 10
        _x_pos[1] = _x_pos[0] + _x_pos[1] + 5
        for _idx, _pos in enumerate(_y_pos[:_n_rows]):
            _fixed.move(_lst_labels[_idx], 5, _pos)

        _fixed.move(self.txtLogisticsAtVar, _x_pos[1], _y_pos[0])
        _fixed.move(self.txtMissionAt, _x_pos[0], _y_pos[1])
        _fixed.move(self.txtMissionAtVar, _x_pos[1], _y_pos[1])
        _fixed.move(self.txtTotalCost, _x_pos[0], _y_pos[2])
        _fixed.move(self.txtCostFailure, _x_pos[0], _y_pos[3])
        _fixed.move(self.txtCostHour, _x_pos[0], _y_pos[4])
        _fixed.move(self.txtPartCount, _x_pos[0], _y_pos[5])
