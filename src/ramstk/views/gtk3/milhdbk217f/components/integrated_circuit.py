# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.integrated_circuit.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Integrated Circuit Results Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry


class ICMilHdbk217FResultPanel(MilHdbk217FResultPanel):
    """Display IC assessment results attribute data in the RAMSTK Work Book.

    The Integrated Circuit assessment result view displays all the assessment
    results for the selected integrated circuit.  This includes, currently,
    results for MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress
    methods.  The attributes of a integrated circuit assessment result view
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

    _lambda_p = '<span foreground="blue">\u03BB<sub>p</sub> = '
    _function_1 = "(C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)"
    _function_2 = "\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"
    _function_3 = "\u03BB<sub>CYC</sub>)" + _function_2

    # Define private class dict class attributes.
    _dic_part_stress: Dict[int, str] = {
        1: _lambda_p + _function_1 + _function_2,
        2: _lambda_p + _function_1 + _function_2,
        3: _lambda_p + _function_1 + _function_2,
        4: _lambda_p + _function_1 + _function_2,
        5: _lambda_p + _function_1 + _function_3,
        6: _lambda_p + _function_1 + _function_3,
        7: _lambda_p + _function_1 + _function_3,
        8: _lambda_p + _function_1 + _function_3,
        9: _lambda_p + "(C<sub>1</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub> + "
        "C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>L</sub>\u03C0<sub>Q</sub"
        "></span>",
        10: _lambda_p
        + "\u03BB<sub>BD</sub>\u03C0<sub>MFG</sub>\u03C0<sub>T</sub>\u03C0<sub"
        ">CD</sub> + \u03BB<sub>BP</sub>\u03C0<sub>E</sub>\u03C0<sub>Q</sub"
        ">\u03C0<sub>PT</sub> + \u03BB<sub>EOS</sub></span> ",
    }

    # Define private class list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Integrated Circuit MIL-HDBK-217F Results")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

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
                        "The assessment model used to calculate the integrated circuit "
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
                    "tooltip": _("The base hazard rate for the integrated circuit."),
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
                    "tooltip": _("The quality factor for the integrated circuit."),
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
                    "tooltip": _("The environment factor for the integrated circuit."),
                },
                "\u03C0<sub>E</sub>:",
            ],
            "C1": [
                6,
                self.txtC1,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "The die complexity factor for the integrated circuit."
                    ),
                },
                "C1:",
            ],
            "pi_t": [
                33,
                self.txtPiT,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "The temperature correction factor for the integrated circuit."
                    ),
                },
                "\u03C0<sub>T</sub>:",
            ],
            "C2": [
                7,
                self.txtC2,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The package hazard rate for the integrated circuit."),
                },
                "C2:",
            ],
            "pi_l": [
                23,
                self.txtPiL,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The learning factor for the integrated circuit."),
                },
                "\u03C0<sub>L</sub>:",
            ],
            "lambdaCYC": [
                10,
                self.txtLambdaCYC,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "The read/write cycling induced hazard rate for the integrated "
                        "circuit."
                    ),
                },
                "\u03BB<sub>CYC</sub>:",
            ],
            "lambdaBD": [
                8,
                self.txtLambdaBD,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "The die base hazard rate for the integrated circuit."
                    ),
                },
                "\u03BB<sub>BD</sub>:",
            ],
            "pi_mfg": [
                25,
                self.txtPiMFG,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "The manufacturing process correction factor for the "
                        "integrated circuit."
                    ),
                },
                "\u03C0<sub>MFG</sub>:",
            ],
            "pi_cd": [
                14,
                self.txtPiCD,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "The die complexity correction factor for the integrated "
                        "circuit."
                    ),
                },
                "\u03C0<sub>CD</sub>:",
            ],
            "lambdaBP": [
                9,
                self.txtLambdaBP,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "The package base hazard rate for the integrated circuit."
                    ),
                },
                "\u03BB<sub>BP</sub>:",
            ],
            "pi_pt": [
                29,
                self.txtPiPT,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The package type factor for the integrated circuit."),
                },
                "\u03C0<sub>PT</sub>:",
            ],
            "lambdaEOS": [
                11,
                self.txtLambdaEOS,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "The electrical overstress hazard rate for the integrated "
                        "circuit."
                    ),
                },
                "\u03BB<sub>EOS</sub>:",
            ],
            "pi_a": [
                12,
                self.txtPiA,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The application factor for the integrated circuit."),
                },
                "\u03C0<sub>A</sub>:",
            ],
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().do_set_properties()
        super().do_make_panel()

        # Subscribe to PyPubSub messages.

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load the integrated circuit assessment results page.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        super().do_load_entries(attributes)

        self.txtC1.set_sensitive(False)
        self.txtPiT.set_sensitive(False)
        self.txtC2.set_sensitive(False)
        self.txtPiL.set_sensitive(False)
        self.txtLambdaCYC.set_sensitive(False)
        self.txtLambdaBD.set_sensitive(False)
        self.txtPiMFG.set_sensitive(False)
        self.txtPiCD.set_sensitive(False)
        self.txtLambdaBP.set_sensitive(False)
        self.txtPiPT.set_sensitive(False)
        self.txtLambdaEOS.set_sensitive(False)
        self.txtPiA.set_sensitive(False)

        if self.category_id == 1 and self._hazard_rate_method_id == 2:
            self.txtC1.do_update(str(self.fmt.format(attributes["C1"])))
            self.txtPiT.do_update(str(self.fmt.format(attributes["piT"])))
            self.txtC2.do_update(str(self.fmt.format(attributes["C2"])))
            self.txtPiL.do_update(str(self.fmt.format(attributes["piL"])))
            self.txtLambdaCYC.do_update(
                str(self.fmt.format(attributes["lambdaCYC"])),
            )
            self.txtLambdaBD.do_update(str(self.fmt.format(attributes["lambdaBD"])))
            self.txtPiMFG.do_update(str(self.fmt.format(attributes["piMFG"])))
            self.txtPiCD.do_update(str(self.fmt.format(attributes["piCD"])))
            self.txtLambdaBP.do_update(str(self.fmt.format(attributes["lambdaBP"])))
            self.txtPiPT.do_update(str(self.fmt.format(attributes["piPT"])))
            self.txtLambdaEOS.do_update(
                str(self.fmt.format(attributes["lambdaEOS"])),
            )
            self.txtPiA.do_update(str(self.fmt.format(attributes["piA"])))
