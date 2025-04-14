# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.resistor.py is part of the RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Resistor Results panel module."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry, WidgetConfig, make_widget_config


class ResistorMilHdbk217FResultPanel(MilHdbk217FResultPanel):
    """Display Resistor assessment results attribute data.

    The Resistor assessment result view displays all the assessment results
    for the selected resistor.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a Resistor assessment result view are:

    :ivar txtPiR: displays the resistance factor for the resistor.
    :ivar txtPiT: displays the temperature factor for the resistor.
    :ivar txtPiNR: displays the number of resistors factor for the resistor.
    :ivar txtPiTAPS: displays the potentiometer taps factor for the resistor.
    :ivar txtPiV: displays the voltage factor for the resistor.
    :ivar txtPiC: displays the construction class factor for the resistor.
    """

    # Define private class attributes.
    _lambda_p = '<span foreground="blue">\u03bb<sub>p</sub> = '
    _function_1 = (
        "\u03bb<sub>b</sub>\u03c0<sub>R</sub>\u03c0<sub>Q</sub>"
        "\u03c0<sub>E</sub></span>"
    )
    _function_2 = (
        "\u03bb<sub>b</sub>\u03c0<sub>TAPS</sub>\u03c0<sub>R</sub>"
        "\u03c0<sub>V</sub>\u03c0<sub>Q</sub>\u03c0<sub>E</sub></span>"
    )
    _dic_part_stress: Dict[int, str] = {
        1: _lambda_p + _function_1,
        2: _lambda_p + _function_1,
        3: _lambda_p + _function_1,
        4: _lambda_p
        + "\u03bb<sub>b</sub>\u03c0<sub>T</sub>\u03c0<sub>NR</sub>\u03c0<sub>Q"
        "</sub>\u03c0<sub>E</sub></span>",
        5: _lambda_p + _function_1,
        6: _lambda_p + _function_1,
        7: _lambda_p + _function_1,
        8: _lambda_p + "\u03bb<sub>b</sub>\u03c0<sub>Q</sub>\u03c0<sub>E</sub></span>",
        9: _lambda_p + _function_2,
        10: _lambda_p
        + "\u03bb<sub>b</sub>\u03c0<sub>TAPS</sub>\u03c0<sub>C</sub>\u03c0<sub"
        ">R</sub>\u03c0<sub>V</sub>\u03c0<sub>Q</sub>\u03c0<sub>E</sub"
        "></span>",
        11: _lambda_p + _function_2,
        12: _lambda_p
        + "\u03bb<sub>b</sub>\u03c0<sub>TAPS</sub>\u03c0<sub>R</sub>\u03c0<sub"
        ">V</sub>\u03c0<sub>C</sub>\u03c0<sub>Q</sub>\u03c0<sub>E</sub"
        "></span>",
        13: _lambda_p + _function_2,
        14: _lambda_p + _function_2,
        15: _lambda_p + _function_2,
    }
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Resistor MIL-HDBK-217F Results")

    def __init__(self) -> None:
        """Initialize an instance of the Resistor assessment result view."""
        super().__init__()

        # Initialize widgets.
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiNR: RAMSTKEntry = RAMSTKEntry()
        self.txtPiR: RAMSTKEntry = RAMSTKEntry()
        self.txtPiT: RAMSTKEntry = RAMSTKEntry()
        self.txtPiTAPS: RAMSTKEntry = RAMSTKEntry()
        self.txtPiV: RAMSTKEntry = RAMSTKEntry()

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
                        "The assessment model used to calculate the resistor hazard "
                        "rate."
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
                    "tooltip": _("The base hazard rate for the resistor."),
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
                    "tooltip": _("The quality factor for the resistor."),
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
                    "tooltip": _("The environment factor for the resistor."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiR,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_r",
                    "index": 31,
                    "label_text": "\u03c0<sub>R</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The resistance factor for the resistor."),
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
                    "tooltip": _("The temperature factor for the resistor."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiNR,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_nr",
                    "index": 27,
                    "label_text": "\u03c0<sub>NR</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "The number of resistors factor for the resistor network."
                    ),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiTAPS,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_taps",
                    "index": 34,
                    "label_text": "\u03c0<sub>TAPS</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The potentiometer taps factor for the resistor."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiV,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_v",
                    "index": 36,
                    "label_text": "\u03c0<sub>V</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The voltage factor for the resistor."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiC,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_c",
                    "index": 13,
                    "label_text": "\u03c0<sub>C</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The construction class factor for the resistor."),
                    "editable": True,
                    "visible": True,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load the Resistor assessment results page.

        :param attributes: the attributes dictionary for the selected Resistor.
        """
        super().do_load_entries(attributes)
        super().do_set_widget_sensitivity(
            [
                self.txtPiC,
                self.txtPiNR,
                self.txtPiR,
                self.txtPiT,
                self.txtPiTAPS,
                self.txtPiV,
            ],
            False,
        )

        if self.category_id == 3 and self._hazard_rate_method_id == 2:
            self.txtPiR.do_update({"piR": str(self.fmt.format(attributes["piR"]))})
            self.txtPiT.do_update({"piT": str(self.fmt.format(attributes["piT"]))})
            self.txtPiNR.do_update({"piNR": str(self.fmt.format(attributes["piNR"]))})
            self.txtPiTAPS.do_update(
                {"piTAPS": str(self.fmt.format(attributes["piTAPS"]))}
            )
            self.txtPiV.do_update({"piV": str(self.fmt.format(attributes["piV"]))})
            self.txtPiC.do_update({"piC": str(self.fmt.format(attributes["piC"]))})
