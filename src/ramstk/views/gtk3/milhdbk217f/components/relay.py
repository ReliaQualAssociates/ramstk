# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.relay.py is part of the RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Relay Results panel module."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry, WidgetConfig, make_widget_config


class RelayMilHdbk217FResultPanel(MilHdbk217FResultPanel):
    """Display Relay assessment results attribute data in the RAMSTK Work Book.

    The Relay assessment result view displays all the assessment results
    for the selected relay.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a relay assessment result view are:

    :ivar txtPiC: displays the contact form factor for the relay.
    :ivar txtPiCYC: displays the cycling factor for the relay.
    :ivar txtPiL: displays the load stress factor for the relay.
    :ivar txtPiF: displays the application and construction factor for the
    relay.
    """

    # Define private class attributes.
    _dic_part_stress: Dict[int, str] = {
        1: '<span foreground="blue">\u03bb<sub>p</sub> = '
        "\u03bb<sub>b</sub>\u03c0<sub>L</sub>\u03c0<sub>C</sub>\u03c0<sub"
        ">CYC</sub>\u03c0<sub>F</sub>\u03c0<sub>Q</sub>\u03c0<sub>E</sub"
        "></span>",
        2: '<span foreground="blue">\u03bb<sub>p</sub> = '
        "\u03bb<sub>b</sub>\u03c0<sub>Q</sub>\u03c0<sub>E</sub></span> ",
    }
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Relay MIL-HDBK-217F Results")

    def __init__(self) -> None:
        """Initialize an instance of the Relay assessment result view."""
        super().__init__()

        # Initialize widgets
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiCYC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiF: RAMSTKEntry = RAMSTKEntry()
        self.txtPiL: RAMSTKEntry = RAMSTKEntry()

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
                        "The assessment model used to calculate the relay hazard rate."
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
                    "tooltip": _("The base hazard rate for the relay."),
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
                    "tooltip": _("The quality factor for the relay."),
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
                    "tooltip": _("The environment factor for the relay."),
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
                    "tooltip": _("The contact form factor for the relay."),
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
                    "tooltip": _("The cycling factor for the relay."),
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
                    "tooltip": _(
                        "The application and construction factor for the relay."
                    ),
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
                    "tooltip": _("The load stress factor for the relay."),
                    "editable": True,
                    "visible": True,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load the Relay assessment results widgets.

        :param attributes: the attributes dictionary for the selected relay.
        """
        super().do_load_entries(attributes)
        super().do_set_widget_sensitivity(
            [
                self.txtPiC,
                self.txtPiCYC,
                self.txtPiF,
                self.txtPiL,
            ],
            False,
        )

        if self.category_id == 6 and self._hazard_rate_method_id == 2:
            self.txtPiC.do_update({"piC": str(self.fmt.format(attributes["piC"]))})
            self.txtPiCYC.do_update(
                {"piCYC": str(self.fmt.format(attributes["piCYC"]))}
            )
            self.txtPiF.do_update({"piF": str(self.fmt.format(attributes["piF"]))})
            self.txtPiL.do_update({"piL": str(self.fmt.format(attributes["piL"]))})
