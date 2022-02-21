# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.semiconductor.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Semiconductor Results Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry


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

    _lambda_p = '<span foreground="blue">\u03BB<sub>p</sub> = '
    _function_1 = (
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>"
        "\u03C0<sub>E</sub></span>"
    )

    # Define private dict class attributes.
    _dic_part_stress: Dict[int, str] = {
        1: _lambda_p
        + "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>S</sub>\u03C0<sub>Q"
        "</sub>\u03C0<sub>E</sub></span>",
        2: _lambda_p
        + "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>R"
        "</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        3: _lambda_p
        + "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>R"
        "</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        4: _lambda_p
        + "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>Q"
        "</sub>\u03C0<sub>E</sub></span>",
        5: _lambda_p + _function_1,
        6: _lambda_p
        + "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>R</sub>\u03C0<sub>S"
        "</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        7: _lambda_p
        + "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>M"
        "</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        8: _lambda_p
        + "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>M"
        "</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        9: _lambda_p + _function_1,
        10: _lambda_p
        + "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>R</sub>\u03C0<sub>S"
        "</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        11: _lambda_p + _function_1,
        12: _lambda_p + _function_1,
        13: _lambda_p
        + "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>I"
        "</sub>\u03C0<sub>A</sub>\u03C0<sub>P</sub>\u03C0<sub>E</sub></span> ",
    }

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Semiconductor MIL-HDBK-217F Results")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

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

        # Initialize private dictionary attributes.

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
                        "The assessment model used to calculate the semiconductor "
                        "hazard rate."
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
                    "tooltip": _("The base hazard rate for the semiconductor."),
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
                    "tooltip": _("The quality factor for the semiconductor."),
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
                    "tooltip": _("The environment factor for the semiconductor."),
                },
                "\u03C0<sub>E</sub>:",
            ],
            "pi_t": [
                33,
                self.txtPiT,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The temperature factor for the semiconductor."),
                },
                "\u03C0<sub>T</sub>:",
            ],
            "pi_a": [
                12,
                self.txtPiA,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The application factor for the semiconductor."),
                },
                "\u03C0<sub>A</sub>:",
            ],
            "pi_c": [
                13,
                self.txtPiC,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "The contact construction factor for the semiconductor."
                    ),
                },
                "\u03C0<sub>C</sub>:",
            ],
            "pi_r": [
                31,
                self.txtPiR,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The power rating factor for the semiconductor."),
                },
                "\u03C0<sub>R</sub>:",
            ],
            "pi_m": [
                24,
                self.txtPiM,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The matching network factor for the semiconductor."),
                },
                "\u03C0<sub>M</sub>:",
            ],
            "pi_i": [
                21,
                self.txtPiI,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The forward current factor for the semiconductor."),
                },
                "\u03C0<sub>I</sub>:",
            ],
            "pi_p": [
                28,
                self.txtPiP,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The power degradation factor for the semiconductor."),
                },
                "\u03C0<sub>P</sub>:",
            ],
            "pi_s": [
                31,
                self.txtPiS,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The electrical stress factor for the semiconductor."),
                },
                "\u03C0<sub>S</sub>:",
            ],
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().do_set_properties()
        super().do_make_panel()

        # Subscribe to PyPubSub messages.

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load the semiconductor assessment results page.

        :param attributes: the attributes dictionary for the selected
            Semiconductor.
        :return: None
        :rtype: None
        """
        super().do_load_entries(attributes)

        self.txtPiA.set_sensitive(False)
        self.txtPiC.set_sensitive(False)
        self.txtPiI.set_sensitive(False)
        self.txtPiM.set_sensitive(False)
        self.txtPiP.set_sensitive(False)
        self.txtPiR.set_sensitive(False)
        self.txtPiS.set_sensitive(False)
        self.txtPiT.set_sensitive(False)

        if self.category_id == 2 and self._hazard_rate_method_id == 2:
            self.txtPiA.do_update(str(self.fmt.format(attributes["piA"])))
            self.txtPiC.do_update(str(self.fmt.format(attributes["piC"])))
            self.txtPiI.do_update(str(self.fmt.format(attributes["piI"])))
            self.txtPiM.do_update(str(self.fmt.format(attributes["piM"])))
            self.txtPiP.do_update(str(self.fmt.format(attributes["piP"])))
            self.txtPiR.do_update(str(self.fmt.format(attributes["piR"])))
            self.txtPiS.do_update(str(self.fmt.format(attributes["piS"])))
            self.txtPiT.do_update(str(self.fmt.format(attributes["piT"])))
