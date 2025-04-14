# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.integrated_circuit.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Integrated Circuit Results panel module."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry, WidgetConfig, make_widget_config


class ICMilHdbk217FResultPanel(MilHdbk217FResultPanel):
    """Display IC assessment results attribute data in the RAMSTK Work Book.

    The Integrated Circuit assessment result view displays all the assessment
    results for the selected integrated circuit.  This includes, currently,
    results for MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress
    methods.  The attributes of an integrated circuit assessment result view
    are:

    :ivar txtC1: displays the die complexity hazard rate of the integrated
        circuit.
    :ivar txtPiT: displays the temperature factor for the integrated circuit.
    :ivar txtC2: displays the package failure rate for the integrated circuit.
    :ivar txtPiL: displays the learning factor for the integrated circuit.
    :ivar txtLambdaCYC: displays the read/write cycling induced hazard rate for
        the EEPROM.
    :ivar txtLambdaBD: displays the die base hazard rate for the VLSI device.
    :ivar txtPiMFG: displays the manufacturing process correction factor for
        VLSI device.
    :ivar txtPiCD: displays the die complexity correction factor for the VLSI
        device.
    :ivar txtLambdaBP: displays the package base hazard rate for the VLSI
        device.
    :ivar txtPiPT: displays the package type correction factor for the VLSI
        device.
    :ivar txtLambdaEOS: displays the electrical overstress hazard rate for the
        VLSI device.
    :ivar txtPiA: displays the application factor for the integrated circuit.
    """

    # Define private class attributes.
    _lambda_p = '<span foreground="blue">\u03bb<sub>p</sub> = '
    _function_1 = "(C<sub>1</sub>\u03c0<sub>T</sub> + C<sub>2</sub>\u03c0<sub>E</sub>)"
    _function_2 = "\u03c0<sub>Q</sub>\u03c0<sub>L</sub></span>"
    _function_3 = "\u03bb<sub>CYC</sub>)" + _function_2
    _dic_part_stress: Dict[int, str] = {
        1: _lambda_p + _function_1 + _function_2,
        2: _lambda_p + _function_1 + _function_2,
        3: _lambda_p + _function_1 + _function_2,
        4: _lambda_p + _function_1 + _function_2,
        5: _lambda_p + _function_1 + _function_3,
        6: _lambda_p + _function_1 + _function_3,
        7: _lambda_p + _function_1 + _function_3,
        8: _lambda_p + _function_1 + _function_3,
        9: _lambda_p + "(C<sub>1</sub>\u03c0<sub>T</sub>\u03c0<sub>A</sub> + "
        "C<sub>2</sub>\u03c0<sub>E</sub>)\u03c0<sub>L</sub>\u03c0<sub>Q</sub"
        "></span>",
        10: _lambda_p
        + "\u03bb<sub>BD</sub>\u03c0<sub>MFG</sub>\u03c0<sub>T</sub>\u03c0<sub"
        ">CD</sub> + \u03bb<sub>BP</sub>\u03c0<sub>E</sub>\u03c0<sub>Q</sub"
        ">\u03c0<sub>PT</sub> + \u03bb<sub>EOS</sub></span> ",
    }
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Integrated Circuit MIL-HDBK-217F Results")

    def __init__(self) -> None:
        """Initialize an instance of the IC assessment result view."""
        super().__init__()

        # Initialize widgets.
        self.txtC1: RAMSTKEntry = RAMSTKEntry()
        self.txtC2: RAMSTKEntry = RAMSTKEntry()
        self.txtLambdaBD: RAMSTKEntry = RAMSTKEntry()
        self.txtLambdaBP: RAMSTKEntry = RAMSTKEntry()
        self.txtLambdaCYC: RAMSTKEntry = RAMSTKEntry()
        self.txtLambdaEOS: RAMSTKEntry = RAMSTKEntry()
        self.txtPiA: RAMSTKEntry = RAMSTKEntry()
        self.txtPiCD: RAMSTKEntry = RAMSTKEntry()
        self.txtPiL: RAMSTKEntry = RAMSTKEntry()
        self.txtPiMFG: RAMSTKEntry = RAMSTKEntry()
        self.txtPiPT: RAMSTKEntry = RAMSTKEntry()
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
                        "The assessment model used to calculate the integrated circuit "
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
                    "tooltip": _("The base hazard rate for the integrated circuit."),
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
                    "tooltip": _("The quality factor for the integrated circuit."),
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
                    "tooltip": _("The environment factor for the integrated circuit."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtC1,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "C1",
                    "index": 6,
                    "label_text": "C1:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "The die complexity factor for the integrated circuit."
                    ),
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
                        "The temperature correction factor for the integrated circuit."
                    ),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtC2,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "C2",
                    "index": 7,
                    "label_text": "C2:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The package hazard rate for the integrated circuit."),
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
                    "tooltip": _("The learning factor for the integrated circuit."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtLambdaCYC,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "lambdaCYC",
                    "index": 10,
                    "label_text": "\u03bb<sub>CYC</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "The read/write cycling induced hazard rate for the "
                        "integrated circuit."
                    ),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtLambdaBD,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "lambdaBD",
                    "index": 8,
                    "label_text": "\u03bb<sub>BD</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "The die base hazard rate for the integrated circuit."
                    ),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiMFG,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_mfg",
                    "index": 25,
                    "label_text": "\u03c0<sub>MFG</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "The manufacturing process correction factor for the "
                        "integrated circuit."
                    ),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiCD,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_cd",
                    "index": 14,
                    "label_text": "\u03c0<sub>CD</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "The die complexity correction factor for the integrated "
                        "circuit."
                    ),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtLambdaBP,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "lambdaBP",
                    "index": 9,
                    "label_text": "\u03bb<sub>BP</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "The package base hazard rate for the integrated circuit."
                    ),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiPT,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_pt",
                    "index": 29,
                    "label_text": "\u03c0<sub>PT</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The package type factor for the integrated circuit."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtLambdaEOS,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "lambdaEOS",
                    "index": 11,
                    "label_text": "\u03bb<sub>EOS</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "The electrical overstress hazard rate for the integrated "
                        "circuit."
                    ),
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
                    "tooltip": _("The application factor for the integrated circuit."),
                    "editable": True,
                    "visible": True,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load the integrated circuit assessment results page.

        :param attributes: the attributes dictionary for the selected Integrated
            Circuit.
        """
        super().do_load_entries(attributes)
        super().do_set_widget_sensitivity(
            [
                self.txtC1,
                self.txtPiT,
                self.txtC2,
                self.txtPiL,
                self.txtLambdaCYC,
                self.txtLambdaBD,
                self.txtPiMFG,
                self.txtPiCD,
                self.txtLambdaBP,
                self.txtPiPT,
                self.txtLambdaEOS,
                self.txtPiA,
            ],
            False,
        )

        if self.category_id == 1 and self._hazard_rate_method_id == 2:
            self.txtC1.do_update({"C1": str(self.fmt.format(attributes["C1"]))})
            self.txtPiT.do_update({"piT": str(self.fmt.format(attributes["piT"]))})
            self.txtC2.do_update({"C2": str(self.fmt.format(attributes["C2"]))})
            self.txtPiL.do_update({"piL": str(self.fmt.format(attributes["piL"]))})
            self.txtLambdaCYC.do_update(
                {"lambdaCYC": str(self.fmt.format(attributes["lambdaCYC"]))},
            )
            self.txtLambdaBD.do_update(
                {"lambdaBD": str(self.fmt.format(attributes["lambdaBD"]))}
            )
            self.txtPiMFG.do_update(
                {"piMFG": str(self.fmt.format(attributes["piMFG"]))}
            )
            self.txtPiCD.do_update({"piCD": str(self.fmt.format(attributes["piCD"]))})
            self.txtLambdaBP.do_update(
                {"lambdaBP": str(self.fmt.format(attributes["lambdaBP"]))}
            )
            self.txtPiPT.do_update({"piPT": str(self.fmt.format(attributes["piPT"]))})
            self.txtLambdaEOS.do_update(
                {"lambdaEOS": str(self.fmt.format(attributes["lambdaEOS"]))},
            )
            self.txtPiA.do_update({"piA": str(self.fmt.format(attributes["piA"]))})
