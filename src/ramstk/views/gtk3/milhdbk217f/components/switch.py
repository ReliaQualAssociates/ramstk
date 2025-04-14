# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.switch.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Switch Results panel module."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry, WidgetConfig, make_widget_config


class SwitchMilHdbk217FResultPanel(MilHdbk217FResultPanel):
    """Display Switch assessment results attribute data.

    The Switch assessment result view displays all the assessment results
    for the selected switch.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a switch assessment result view are:

    :ivar txtPiC: displays the contact form and quantity factor for the switch.
    :ivar txtPiCYC: displays the cycling factor for the switch.
    :ivar txtPiL: displays the load stress factor for the switch.
    :ivar txtPiN: displays the number of active contacts factor for the switch.
    :ivar txtPiU: displays the use factor for the breaker.
    """

    # Define private class attributes.
    _dic_part_stress: Dict[int, str] = {
        1: '<span foreground="blue">\u03bb<sub>p</sub> = '
        "\u03bb<sub>b</sub>\u03c0<sub>CYC</sub>\u03c0<sub>L</sub>\u03c0<sub"
        ">C</sub>\u03c0<sub>E</sub></span>",
        2: '<span foreground="blue">\u03bb<sub>p</sub> = '
        "\u03bb<sub>b</sub>\u03c0<sub>CYC</sub>\u03c0<sub>L</sub>\u03c0<sub"
        ">E</sub></span>",
        3: '<span foreground="blue">\u03bb<sub>p</sub> = '
        "\u03bb<sub>b</sub>\u03c0<sub>CYC</sub>\u03c0<sub>L</sub>\u03c0<sub"
        ">E</sub></span>",
        4: '<span foreground="blue">\u03bb<sub>p</sub> = (\u03bb<sub>b1</sub> '
        "+ \u03c0<sub>N</sub>\u03bb<sub>b2</sub>)\u03c0<sub>CYC</sub>\u03c0"
        "<sub>L</sub>\u03c0<sub>E</sub></span>",
        5: '<span foreground="blue">\u03bb<sub>p</sub> = '
        "\u03bb<sub>b</sub>\u03c0<sub>C</sub>\u03c0<sub>U</sub>\u03c0<sub>Q"
        "</sub>\u03c0<sub>E</sub></span> ",
    }
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Switch MIL-HDBK-217F Results")

    def __init__(self) -> None:
        """Initialize an instance of the Switch assessment result view."""
        super().__init__()

        # Initialize widgets.
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiCYC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiL: RAMSTKEntry = RAMSTKEntry()
        self.txtPiN: RAMSTKEntry = RAMSTKEntry()
        self.txtPiU: RAMSTKEntry = RAMSTKEntry()

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
                        "The assessment model used to calculate the switch hazard rate."
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
                    "tooltip": _("The base hazard rate for the switch."),
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
                    "tooltip": _("The quality factor for the switch."),
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
                    "tooltip": _("The environment factor for the switch."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiCYC,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_cyc",
                    "index": 18,
                    "label_text": "\u03c0<sub>CYC</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The cycling factor for the switch."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiL,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_l",
                    "index": 23,
                    "label_text": "\u03c0<sub>L</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The load stress factor for the switch."),
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
                        "The number of active contacts factor for the switch."
                    ),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiN,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_n",
                    "index": 26,
                    "label_text": "\u03c0<sub>N</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "The contact form and quantity factor for the switch.  This is "
                        "the configuration factor for a circuit breaker."
                    ),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiU,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_u",
                    "index": 35,
                    "label_text": "\u03c0<sub>U</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The use factor for the switch."),
                    "editable": True,
                    "visible": True,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load the switch assessment results page.

        :param attributes: the attributes of the selected switch assessment
        """
        super().do_load_entries(attributes)
        super().do_set_widget_sensitivity(
            [
                self.txtPiCYC,
                self.txtPiL,
                self.txtPiC,
                self.txtPiN,
                self.txtPiU,
            ],
            False,
        )

        if self.category_id == 7 and self._hazard_rate_method_id == 2:
            self.lblModel.do_update(
                {"hazard_rate_model": self._dic_part_stress[self.subcategory_id]}
            )
            self.txtPiCYC.do_update(
                {"piCYC": str(self.fmt.format(attributes["piCYC"]))}
            )
            self.txtPiL.do_update({"piL": str(self.fmt.format(attributes["piL"]))})
            self.txtPiC.do_update({"piC": str(self.fmt.format(attributes["piC"]))})
            self.txtPiN.do_update({"piN": str(self.fmt.format(attributes["piN"]))})
            self.txtPiU.do_update({"piU": str(self.fmt.format(attributes["piU"]))})
