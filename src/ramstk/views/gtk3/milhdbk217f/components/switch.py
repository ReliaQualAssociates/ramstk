# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.switch.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Switch Results Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry


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

    # Define private dict class attributes.
    _dic_part_stress: Dict[int, str] = {
        1: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub"
        ">C</sub>\u03C0<sub>E</sub></span>",
        2: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub"
        ">E</sub></span>",
        3: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub"
        ">E</sub></span>",
        4: '<span foreground="blue">\u03BB<sub>p</sub> = (\u03BB<sub>b1</sub> '
        "+ \u03C0<sub>N</sub>\u03BB<sub>b2</sub>)\u03C0<sub>CYC</sub>\u03C0"
        "<sub>L</sub>\u03C0<sub>E</sub></span>",
        5: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>\u03C0<sub>C</sub>\u03C0<sub>U</sub>\u03C0<sub>Q"
        "</sub>\u03C0<sub>E</sub></span> ",
    }

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Switch MIL-HDBK-217F Results")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Switch assessment result view."""
        super().__init__()

        # Initialize widgets.
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiCYC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiL: RAMSTKEntry = RAMSTKEntry()
        self.txtPiN: RAMSTKEntry = RAMSTKEntry()
        self.txtPiU: RAMSTKEntry = RAMSTKEntry()

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
                        "The assessment model used to calculate the switch hazard rate."
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
                    "tooltip": _("The base hazard rate for the switch."),
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
                    "tooltip": _("The quality factor for the switch."),
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
                    "tooltip": _("The environment factor for the switch."),
                },
                "\u03C0<sub>E</sub>:",
            ],
            "pi_cyc": [
                18,
                self.txtPiCYC,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The cycling factor for the switch."),
                },
                "\u03C0<sub>CYC</sub>:",
            ],
            "pi_l": [
                23,
                self.txtPiL,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The load stress factor for the switch."),
                },
                "\u03C0<sub>L</sub>:",
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
                        "The number of active contacts factor for the switch."
                    ),
                },
                "\u03C0<sub>C</sub>:",
            ],
            "pi_n": [
                26,
                self.txtPiN,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "The contact form and quantity factor for the switch.  This is "
                        "the configuration factor for a circuit breaker."
                    ),
                },
                "\u03C0<sub>N</sub>:",
            ],
            "pi_u": [
                35,
                self.txtPiU,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The use factor for the switch."),
                },
                "\u03C0<sub>U</sub>:",
            ],
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().do_set_properties()
        super().do_make_panel()

        # Subscribe to PyPubSub messages.

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load the switch assessment results page.

        :return: None
        :rtype: None
        """
        super().do_load_entries(attributes)

        self.txtPiCYC.set_sensitive(False)
        self.txtPiL.set_sensitive(False)
        self.txtPiC.set_sensitive(False)
        self.txtPiN.set_sensitive(False)
        self.txtPiU.set_sensitive(False)

        if self.category_id == 7 and self._hazard_rate_method_id == 2:
            self.txtPiCYC.do_update(str(self.fmt.format(attributes["piCYC"])))
            self.txtPiL.do_update(str(self.fmt.format(attributes["piL"])))
            self.txtPiC.do_update(str(self.fmt.format(attributes["piC"])))
            self.txtPiN.do_update(str(self.fmt.format(attributes["piN"])))
            self.txtPiU.do_update(str(self.fmt.format(attributes["piU"])))
