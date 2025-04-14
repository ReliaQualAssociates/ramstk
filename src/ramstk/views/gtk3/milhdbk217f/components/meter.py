# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.meter.py is part of the RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Meter Results panel module."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry, WidgetConfig, make_widget_config


class MeterMilHdbk217FResultPanel(MilHdbk217FResultPanel):
    """Display Meter assessment results attribute data in the RAMSTK Work Book.

    The Meter assessment result view displays all the assessment results
    for the selected meter.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a meter assessment result view are:

    :ivar txtPiA: displays the application factor for the panel meter.
    :ivar txtPiF: displays the function factor for the panel meter.
    :ivar txtPiT: displays the temperature stress factor for the elapsed time
        meter.
    """

    # Define private class attributes.
    _dic_part_stress: Dict[int, str] = {
        1: '<span foreground="blue">\u03bb<sub>p</sub> = '
        "\u03bb<sub>b</sub>\u03c0<sub>A</sub>\u03c0<sub>F</sub>\u03c0<sub>Q"
        "</sub>\u03c0<sub>E</sub></span>",
        2: '<span foreground="blue">\u03bb<sub>p</sub> = '
        "\u03bb<sub>b</sub>\u03c0<sub>T</sub>\u03c0<sub>E</sub></span> ",
    }
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Meter MIL-HDBK-217F Results")

    def __init__(self) -> None:
        """Initialize an instance of the Meter assessment result view."""
        super().__init__()

        # Initialize widgets.
        self.txtPiA: RAMSTKEntry = RAMSTKEntry()
        self.txtPiF: RAMSTKEntry = RAMSTKEntry()
        self.txtPiT: RAMSTKEntry = RAMSTKEntry()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.lblModel,
                {
                    "datatype": "",
                    "default": "",
                    "field": "hazard_rate_model",
                    "index": 13,
                    "label_text": "",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "The assessment model used to calculate the meter hazard rate."
                    ),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtLambdaB,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "lambda_b",
                    "index": 23,
                    "label_text": "\u03bb<sub>b</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The base hazard rate for the meter."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiQ,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_q",
                    "index": 30,
                    "label_text": "\u03c0<sub>Q</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The quality factor for the meter."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiE,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_e",
                    "index": 19,
                    "label_text": "\u03c0<sub>E</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The environment factor for the meter."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiA,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_a",
                    "index": 12,
                    "label_text": "\u03c0<sub>A</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The application factor for the meter."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiF,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_f",
                    "index": 20,
                    "label_text": "\u03c0<sub>F</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The function factor for the meter."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiT,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_t",
                    "index": 33,
                    "label_text": "\u03c0<sub>T</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "The temperature stress factor for the elapsed time meter."
                    ),
                    "editable": True,
                    "visible": True,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load the meter assessment results page.

        :param attributes: the attributes dictionary for the selected Meter.
        """
        super().do_load_entries(attributes)
        super().do_set_widget_sensitivity(
            [
                self.txtPiA,
                self.txtPiF,
                self.txtPiT,
            ],
            False,
        )

        if self.category_id == 9 and self._hazard_rate_method_id == 2:
            self.lblModel.do_update(
                {"hazard_rate_model": self._dic_part_stress[self.subcategory_id]}
            )
            self.txtPiA.do_update({"piA": str(self.fmt.format(attributes["piA"]))})
            self.txtPiF.do_update({"piF": str(self.fmt.format(attributes["piF"]))})
            self.txtPiT.do_update({"piT": str(self.fmt.format(attributes["piT"]))})
