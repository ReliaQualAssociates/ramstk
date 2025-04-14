# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.semiconductor.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Semiconductor Results panel module."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry, WidgetConfig, make_widget_config


class SemiconductorMilHdbk217FResultPanel(MilHdbk217FResultPanel):
    """Display semiconductor assessment results attribute data.

    The semiconductor assessment result view displays all the assessment
    results for the selected semiconductor.  This includes, currently, results
    for MIL-HDBK-217FN2 parts count and part stress methods.  The attributes of
    a semiconductor assessment result view are:

    :ivar txtPiT: displays the temperature factor for the semiconductor.
    :ivar txtPiA: displays the application factor for the semiconductor.
    :ivar txtPiC: displays the construction factor for the semiconductor.
    :ivar txtPiI: displays the forward current factor for the semiconductor.
    :ivar txtPiM: displays the matching network factor for the semiconductor.
    :ivar txtPiP: displays the power degradation factor for the semiconductor.
    :ivar txtPiR: displays the power rating factor for the semiconductor.
    :ivar txtPiS: displays the electrical stress factor for the semiconductor.
    """

    # Define private class attributes.
    _lambda_p = '<span foreground="blue">\u03bb<sub>p</sub> = '
    _function_1 = (
        "\u03bb<sub>b</sub>\u03c0<sub>T</sub>\u03c0<sub>Q</sub>"
        "\u03c0<sub>E</sub></span>"
    )
    _dic_part_stress: Dict[int, str] = {
        1: _lambda_p
        + "\u03bb<sub>b</sub>\u03c0<sub>T</sub>\u03c0<sub>S</sub>\u03c0<sub>Q"
        "</sub>\u03c0<sub>E</sub></span>",
        2: _lambda_p
        + "\u03bb<sub>b</sub>\u03c0<sub>T</sub>\u03c0<sub>A</sub>\u03c0<sub>R"
        "</sub>\u03c0<sub>Q</sub>\u03c0<sub>E</sub></span>",
        3: _lambda_p
        + "\u03bb<sub>b</sub>\u03c0<sub>T</sub>\u03c0<sub>A</sub>\u03c0<sub>R"
        "</sub>\u03c0<sub>S</sub>\u03c0<sub>Q</sub>\u03c0<sub>E</sub></span>",
        4: _lambda_p
        + "\u03bb<sub>b</sub>\u03c0<sub>T</sub>\u03c0<sub>A</sub>\u03c0<sub>Q"
        "</sub>\u03c0<sub>E</sub></span>",
        5: _lambda_p + _function_1,
        6: _lambda_p
        + "\u03bb<sub>b</sub>\u03c0<sub>T</sub>\u03c0<sub>R</sub>\u03c0<sub>S"
        "</sub>\u03c0<sub>Q</sub>\u03c0<sub>E</sub></span>",
        7: _lambda_p
        + "\u03bb<sub>b</sub>\u03c0<sub>T</sub>\u03c0<sub>A</sub>\u03c0<sub>M"
        "</sub>\u03c0<sub>Q</sub>\u03c0<sub>E</sub></span>",
        8: _lambda_p
        + "\u03bb<sub>b</sub>\u03c0<sub>T</sub>\u03c0<sub>A</sub>\u03c0<sub>M"
        "</sub>\u03c0<sub>Q</sub>\u03c0<sub>E</sub></span>",
        9: _lambda_p + _function_1,
        10: _lambda_p
        + "\u03bb<sub>b</sub>\u03c0<sub>T</sub>\u03c0<sub>R</sub>\u03c0<sub>S"
        "</sub>\u03c0<sub>Q</sub>\u03c0<sub>E</sub></span>",
        11: _lambda_p + _function_1,
        12: _lambda_p + _function_1,
        13: _lambda_p
        + "\u03bb<sub>b</sub>\u03c0<sub>T</sub>\u03c0<sub>Q</sub>\u03c0<sub>I"
        "</sub>\u03c0<sub>A</sub>\u03c0<sub>P</sub>\u03c0<sub>E</sub></span> ",
    }
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Semiconductor MIL-HDBK-217F Results")

    def __init__(self) -> None:
        """Initialize instance of the Semiconductor assessment result view."""
        super().__init__()

        # Initialize widgets.
        self.txtPiA: RAMSTKEntry = RAMSTKEntry()
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiI: RAMSTKEntry = RAMSTKEntry()
        self.txtPiM: RAMSTKEntry = RAMSTKEntry()
        self.txtPiP: RAMSTKEntry = RAMSTKEntry()
        self.txtPiR: RAMSTKEntry = RAMSTKEntry()
        self.txtPiS: RAMSTKEntry = RAMSTKEntry()
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
                        "The assessment model used to calculate the semiconductor "
                        "hazard rate."
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
                    "tooltip": _("The base hazard rate for the semiconductor."),
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
                    "tooltip": _("The quality factor for the semiconductor."),
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
                    "tooltip": _("The environment factor for the semiconductor."),
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
                    "tooltip": _("The temperature factor for the semiconductor."),
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
                    "tooltip": _("The application factor for the semiconductor."),
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
                    "tooltip": _(
                        "The contact construction factor for the semiconductor."
                    ),
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
                    "tooltip": _("The power rating factor for the semiconductor."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiM,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_m",
                    "index": 24,
                    "label_text": "\u03c0<sub>M</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The matching network factor for the semiconductor."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiI,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_i",
                    "index": 21,
                    "label_text": "\u03c0<sub>I</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The forward current factor for the semiconductor."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiP,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_p",
                    "index": 28,
                    "label_text": "\u03c0<sub>P</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The power degradation factor for the semiconductor."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiS,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_s",
                    "index": 31,
                    "label_text": "\u03c0<sub>S</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The electrical stress factor for the semiconductor."),
                    "editable": True,
                    "visible": True,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load the semiconductor assessment results page.

        :param attributes: the attributes dictionary for the selected Semiconductor.
        """
        super().do_load_entries(attributes)

        super().do_set_widget_sensitivity(
            [
                self.txtPiA,
                self.txtPiC,
                self.txtPiI,
                self.txtPiM,
                self.txtPiP,
                self.txtPiR,
                self.txtPiS,
                self.txtPiT,
            ],
            False,
        )

        if self.category_id == 2 and self._hazard_rate_method_id == 2:
            self.lblModel.do_update(
                {"hazard_rate_model": self._dic_part_stress[self.subcategory_id]}
            )
            self.txtPiA.do_update({"piA": str(self.fmt.format(attributes["piA"]))})
            self.txtPiC.do_update({"piC": str(self.fmt.format(attributes["piC"]))})
            self.txtPiI.do_update({"piI": str(self.fmt.format(attributes["piI"]))})
            self.txtPiM.do_update({"piM": str(self.fmt.format(attributes["piM"]))})
            self.txtPiP.do_update({"piP": str(self.fmt.format(attributes["piP"]))})
            self.txtPiR.do_update({"piR": str(self.fmt.format(attributes["piR"]))})
            self.txtPiS.do_update({"piS": str(self.fmt.format(attributes["piS"]))})
            self.txtPiT.do_update({"piT": str(self.fmt.format(attributes["piT"]))})
