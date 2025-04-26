# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.reliability.reliability_results_panel.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Reliability Results panel module."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKEntry,
    RAMSTKFixedPanel,
    WidgetConfig,
    make_widget_config,
)


class ReliabilityResultsPanel(RAMSTKFixedPanel):
    """Panel to display reliability results for the selected Hardware item."""

    # Define private class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_reliability_attributes"
    _tag: str = "reliability"
    _title: str = _("Reliability Assessment Results")

    def __init__(self) -> None:
        """Initialize an instance of the Reliability Results panel."""
        super().__init__()

        # Initialize widgets.
        self.txtActiveHt: RAMSTKEntry = RAMSTKEntry()
        self.txtActiveHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtDormantHt: RAMSTKEntry = RAMSTKEntry()
        self.txtDormantHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsHt: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsMTBF: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsMTBFVar: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsRt: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsRtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionHt: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionMTBF: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionMTBFVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionRt: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionRtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtPercentHt: RAMSTKEntry = RAMSTKEntry()
        self.txtSoftwareHt: RAMSTKEntry = RAMSTKEntry()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.txtActiveHt,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "hazard_rate_active",
                    "index": 8,
                    "label_text": _("Active Failure Intensity [\u03bb(t)]:"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the active failure intensity for the selected "
                        "hardware item."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtActiveHtVar,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "hr_active_variance",
                    "index": 18,
                    "label_text": "",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the variance on the active failure intensity for "
                        "the selected hardware item."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtDormantHt,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "hazard_rate_dormant",
                    "index": 9,
                    "label_text": _("Dormant \u03bb(t):"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the dormant failure intensity for the selected "
                        "hardware item."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtDormantHtVar,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "hr_dormant_variance",
                    "index": 19,
                    "label_text": "",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the variance on the dormant failure intensity for "
                        "the selected hardware item."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtSoftwareHt,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "hazard_rate_software",
                    "index": 15,
                    "label_text": _("Software \u03bb(t):"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the software failure intensity for the selected "
                        "hardware item."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtLogisticsHt,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "hazard_rate_logistics",
                    "index": 10,
                    "label_text": _("Logistics \u03bb(t):"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the logistics failure intensity for the selected "
                        "hardware item. This is the sum of the active, dormant, and "
                        "software hazard rates."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtLogisticsHtVar,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "hr_logistics_variance",
                    "index": 20,
                    "label_text": "",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the variance on the logistics failure intensity for "
                        "the selected hardware item."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtMissionHt,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "hazard_rate_mission",
                    "index": 12,
                    "label_text": _("Mission \u03bb(t):"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the mission failure intensity for the selected "
                        "hardware item."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtMissionHtVar,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "hr_mission_variance",
                    "index": 21,
                    "label_text": "",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the variance on the mission failure intensity for "
                        "the selected hardware item."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtPercentHt,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "hazard_rate_percent",
                    "index": 14,
                    "label_text": _("Percent \u03bb(t):"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the percentage of the system failure intensity the "
                        "selected hardware item represents."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtLogisticsMTBF,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "mtbf_logistics",
                    "index": 25,
                    "label_text": _("Logistics MTBF:"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the logistics mean time between failure (MTBF) for "
                        "the selected hardware item."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtLogisticsMTBFVar,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "mtbf_logistics_variance",
                    "index": 28,
                    "label_text": "",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the variance on the logistics MTBF for the selected "
                        "hardware item."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtMissionMTBF,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "mtbf_mission",
                    "index": 26,
                    "label_text": _("Mission MTBF:"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the mission mean time between failure (MTBF) for "
                        "the selected hardware item."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtMissionMTBFVar,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "mtbf_mission_variance",
                    "index": 29,
                    "label_text": "",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the variance on the mission MTBF for the selected "
                        "hardware item."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtLogisticsRt,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "reliability_logistics",
                    "index": 35,
                    "label_text": _("Logistics Reliability [R(t)]:"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the logistics reliability for the selected hardware "
                        "item."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtLogisticsRtVar,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "reliability_log_variance",
                    "index": 37,
                    "label_text": "",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the variance on the logistics reliability for the "
                        "selected hardware item."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtMissionRt,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "reliability_mission",
                    "index": 36,
                    "label_text": _("Mission R(t):"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the mission reliability for the selected hardware "
                        "item."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtMissionRtVar,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "reliability_miss_variance",
                    "index": 38,
                    "label_text": "",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "Displays the variance on the mission reliability for the "
                        "selected hardware item."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_fixed_panel()
        super().do_set_widget_callbacks()
        self.__do_nudge_widgets()

        do_subscribe_to_messages(
            {
                "succeed_get_reliability_attributes": self._do_load_entries,
            }
        )

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load contents of the RAMSTKEntry() widgets.

        This method ensures results RAMSTKEntry() widgets are set insensitive and loads
        the contents.  The PyPubSub subscriber is in the metaclass.
        """
        # FIXME: Is this method needed?  The metaclass do_load_panel should take care
        #  of this.
        self._do_load_entries_hazard_rate(attributes)
        self._do_load_entries_mtbf(attributes)
        self._do_load_entries_reliability(attributes)

    def _do_load_entries_hazard_rate(self, attributes: Dict[str, Any]) -> None:
        """Load contents of the hazard rate RAMSTKEntry()."""
        # FIXME: Is this method needed?  The metaclass do_load_panel should take care
        #  of this.
        self.txtActiveHt.do_update(
            {
                "hazard_rate_active": str(
                    self.fmt.format(attributes.get("hazard_rate_active", 0.0))
                )
            },
        )
        self.txtActiveHtVar.do_update(
            {
                "hr_active_variance": str(
                    self.fmt.format(attributes.get("hr_active_variance", 0.0))
                )
            },
        )
        self.txtDormantHt.do_update(
            {
                "hazard_rate_dormant": str(
                    self.fmt.format(attributes.get("hazard_rate_dormant", 0.0))
                )
            },
        )
        self.txtDormantHtVar.do_update(
            {
                "hr_dormant_variance": str(
                    self.fmt.format(attributes.get("hr_dormant_variance", 0.0))
                )
            },
        )
        self.txtSoftwareHt.do_update(
            {
                "hazard_rate_software": str(
                    self.fmt.format(attributes.get("hazard_rate_software", 0.0))
                )
            },
        )
        self.txtLogisticsHt.do_update(
            {
                "hazard_rate_logistics": str(
                    self.fmt.format(attributes.get("hazard_rate_logistics", 0.0))
                )
            },
        )
        self.txtLogisticsHtVar.do_update(
            {
                "hr_logistics_variance": str(
                    self.fmt.format(attributes.get("hr_logistics_variance", 0.0))
                )
            },
        )
        self.txtMissionHt.do_update(
            {
                "hazard_rate_mission": str(
                    self.fmt.format(attributes.get("hazard_rate_mission", 0.0))
                )
            },
        )
        self.txtMissionHtVar.do_update(
            {
                "hr_mission_variance": str(
                    self.fmt.format(attributes.get("hr_mission_variance", 0.0))
                )
            },
        )
        self.txtPercentHt.do_update(
            {
                "hazard_rate_percent": str(
                    self.fmt.format(attributes.get("hazard_rate_percent", 0.0))
                )
            },
        )

    def _do_load_entries_mtbf(self, attributes: Dict[str, Any]) -> None:
        """Load contents of MTBF RAMSTKEntry()."""
        # FIXME: Is this method needed?  The metaclass do_load_panel should take care
        #  of this.
        self.txtLogisticsMTBF.do_update(
            {
                "mtbf_logistics": str(
                    self.fmt.format(attributes.get("mtbf_logistics", 0.0))
                )
            },
        )
        self.txtLogisticsMTBFVar.do_update(
            {
                "mtbf_logistics_variance": str(
                    self.fmt.format(attributes.get("mtbf_logistics_variance", 0.0))
                )
            },
        )
        self.txtMissionMTBF.do_update(
            {
                "mtbf_mission": str(
                    self.fmt.format(attributes.get("mtbf_mission", 0.0))
                ),
            },
        )
        self.txtMissionMTBFVar.do_update(
            {
                "mtbf_mission_variance": str(
                    self.fmt.format(attributes.get("mtbf_mission_variance", 0.0))
                )
            },
        )

    def _do_load_entries_reliability(self, attributes: Dict[str, Any]) -> None:
        """Load contents of reliability RAMSTKEntry()."""
        # FIXME: Is this method needed?  The metaclass do_load_panel should take care
        #  of this.
        self.txtLogisticsRt.do_update(
            {
                "reliability_logistics": str(
                    self.fmt.format(attributes.get("reliability_logistics", 1.0))
                )
            },
        )
        self.txtLogisticsRtVar.do_update(
            {
                "reliability_log_variance": str(
                    self.fmt.format(attributes.get("reliability_log_variance", 0.0))
                )
            },
        )
        self.txtMissionRt.do_update(
            {
                "reliability_mission": str(
                    self.fmt.format(attributes.get("reliability_mission", 1.0))
                )
            },
        )
        self.txtMissionRtVar.do_update(
            {
                "reliability_miss_variance": str(
                    self.fmt.format(attributes.get("reliability_miss_variance", 0.0))
                )
            },
        )

    def __do_nudge_widgets(self) -> None:
        """Adjust widgets from their default positions."""
        # HACK: This method is a hack to adjust the positions of the widgets on the
        #     RAMSTKFixedPanel.
        _lst_labels: List[object] = []
        _x_pos: List[int] = [
            0,
            self.txtActiveHt.get_preferred_size()[0].width + 5,
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

        _fixed.move(self.txtActiveHtVar, _x_pos[1], _y_pos[0])
        _fixed.move(self.txtDormantHt, _x_pos[0], _y_pos[1])
        _fixed.move(self.txtDormantHtVar, _x_pos[1], _y_pos[1])
        _fixed.move(self.txtSoftwareHt, _x_pos[0], _y_pos[2])
        _fixed.move(self.txtLogisticsHt, _x_pos[0], _y_pos[3])
        _fixed.move(self.txtLogisticsHtVar, _x_pos[1], _y_pos[3])
        _fixed.move(self.txtMissionHt, _x_pos[0], _y_pos[4])
        _fixed.move(self.txtMissionHtVar, _x_pos[1], _y_pos[4])
        _fixed.move(self.txtPercentHt, _x_pos[0], _y_pos[5])
        _fixed.move(self.txtLogisticsMTBF, _x_pos[0], _y_pos[6])
        _fixed.move(self.txtLogisticsMTBFVar, _x_pos[1], _y_pos[6])
        _fixed.move(self.txtMissionMTBF, _x_pos[0], _y_pos[7])
        _fixed.move(self.txtMissionMTBFVar, _x_pos[1], _y_pos[7])
        _fixed.move(self.txtLogisticsRt, _x_pos[0], _y_pos[8])
        _fixed.move(self.txtLogisticsRtVar, _x_pos[1], _y_pos[8])
        _fixed.move(self.txtMissionRt, _x_pos[0], _y_pos[9])
        _fixed.move(self.txtMissionRtVar, _x_pos[1], _y_pos[9])
