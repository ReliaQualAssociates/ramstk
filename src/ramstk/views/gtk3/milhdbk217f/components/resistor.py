# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.resistor.py is part of the RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Resistor Results Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry


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

    _lambda_p = '<span foreground="blue">\u03BB<sub>p</sub> = '
    _function_1 = (
        "\u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>"
        "\u03C0<sub>E</sub></span>"
    )
    _function_2 = (
        "\u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>"
        "\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
    )

    # Define private dict class attributes.
    _dic_part_stress: Dict[int, str] = {
        1: _lambda_p + _function_1,
        2: _lambda_p + _function_1,
        3: _lambda_p + _function_1,
        4: _lambda_p
        + "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>NR</sub>\u03C0<sub>Q"
        "</sub>\u03C0<sub>E</sub></span>",
        5: _lambda_p + _function_1,
        6: _lambda_p + _function_1,
        7: _lambda_p + _function_1,
        8: _lambda_p + "\u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        9: _lambda_p + _function_2,
        10: _lambda_p
        + "\u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>C</sub>\u03C0<sub"
        ">R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub"
        "></span>",
        11: _lambda_p + _function_2,
        12: _lambda_p
        + "\u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub"
        ">V</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub"
        "></span>",
        13: _lambda_p + _function_2,
        14: _lambda_p + _function_2,
        15: _lambda_p + _function_2,
    }

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Resistor MIL-HDBK-217F Results")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

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

        # Initialize private dict attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "hazard_rate_model": [
                13,
                self.lblModel,
                "",
                None,
                "",
                "",
                {
                    "tooltip": _(
                        "The assessment model used to calculate the resistor hazard "
                        "rate."
                    ),
                },
                "",
            ],
            "lambda_b": [
                23,
                self.txtLambdaB,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _("The base hazard rate for the resistor."),
                },
                "\u03BB<sub>b</sub>:",
            ],
            "pi_q": [
                30,
                self.txtPiQ,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The quality factor for the resistor."),
                },
                "\u03C0<sub>Q</sub>:",
            ],
            "pi_e": [
                19,
                self.txtPiE,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The environment factor for the resistor."),
                },
                "\u03C0<sub>E</sub>:",
            ],
            "pi_r": [
                31,
                self.txtPiR,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The resistance factor for the resistor."),
                },
                "\u03C0<sub>R</sub>:",
            ],
            "pi_t": [
                33,
                self.txtPiT,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The temperature factor for the resistor."),
                },
                "\u03C0<sub>T</sub>:",
            ],
            "pi_nr": [
                27,
                self.txtPiNR,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "The number of resistors factor for the resistor network."
                    ),
                },
                "\u03C0<sub>NR</sub>:",
            ],
            "pi_taps": [
                34,
                self.txtPiTAPS,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The potentiometer taps factor for the resistor."),
                },
                "\u03C0<sub>TAPS</sub>:",
            ],
            "pi_v": [
                36,
                self.txtPiV,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The voltage factor for the resistor."),
                },
                "\u03C0<sub>V</sub>:",
            ],
            "pi_c": [
                13,
                self.txtPiC,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The construction class factor for the resistor."),
                },
                "\u03C0<sub>C</sub>:",
            ],
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().do_set_properties()
        super().do_make_panel()

        # Subscribe to PyPubSub messages.

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load the Resistor assessment results page.

        :param attributes: the attributes dictionary for the selected
            Resistor.
        :return: None
        :rtype: None
        """
        super().do_load_entries(attributes)

        self.txtPiC.set_sensitive(False)
        self.txtPiNR.set_sensitive(False)
        self.txtPiR.set_sensitive(False)
        self.txtPiT.set_sensitive(False)
        self.txtPiTAPS.set_sensitive(False)
        self.txtPiV.set_sensitive(False)

        if self.category_id == 3 and self._hazard_rate_method_id == 2:
            self.txtPiR.do_update(str(self.fmt.format(attributes["piR"])))
            self.txtPiT.do_update(str(self.fmt.format(attributes["piT"])))
            self.txtPiNR.do_update(str(self.fmt.format(attributes["piNR"])))
            self.txtPiTAPS.do_update(str(self.fmt.format(attributes["piTAPS"])))
            self.txtPiV.do_update(str(self.fmt.format(attributes["piV"])))
            self.txtPiC.do_update(str(self.fmt.format(attributes["piC"])))
