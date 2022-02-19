# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.relay.py is part of the RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Relay Results Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry


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

    # Define private dict class attributes.
    _dic_part_stress: Dict[int, str] = {
        1: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>\u03C0<sub>L</sub>\u03C0<sub>C</sub>\u03C0<sub"
        ">CYC</sub>\u03C0<sub>F</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub"
        "></span>",
        2: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span> ",
    }

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Relay MIL-HDBK-217F Results")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Relay assessment result view."""
        super().__init__()

        # Initialize widgets
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiCYC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiF: RAMSTKEntry = RAMSTKEntry()
        self.txtPiL: RAMSTKEntry = RAMSTKEntry()

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
                        "The assessment model used to calculate the relay hazard rate."
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
                    "tooltip": _("The base hazard rate for the relay."),
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
                    "tooltip": _("The quality factor for the relay."),
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
                    "tooltip": _("The environment factor for the relay."),
                },
                "\u03C0<sub>E</sub>:",
            ],
            "pi_c": [
                13,
                self.txtPiC,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The contact form factor for the relay."),
                },
                "\u03C0<sub>C</sub>:",
            ],
            "pi_cyc": [
                18,
                self.txtPiCYC,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The cycling factor for the relay."),
                },
                "\u03C0<sub>CYC</sub>:",
            ],
            "pi_f": [
                20,
                self.txtPiF,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "The application and construction factor for the relay."
                    ),
                },
                "\u03C0<sub>F</sub>:",
            ],
            "pi_l": [
                23,
                self.txtPiL,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The load stress factor for the relay."),
                },
                "\u03C0<sub>L</sub>:",
            ],
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().do_set_properties()
        super().do_make_panel()

        # Subscribe to PyPubSub messages.

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load the Relay assessment results widgets.

        :param attributes: the attributes dictionary for the selected relay.
        :return: None
        """
        super().do_load_entries(attributes)

        self.txtPiC.set_sensitive(False)
        self.txtPiCYC.set_sensitive(False)
        self.txtPiF.set_sensitive(False)
        self.txtPiL.set_sensitive(False)

        if self.category_id == 6 and self._hazard_rate_method_id == 2:
            self.txtPiC.do_update(str(self.fmt.format(attributes["piC"])))
            self.txtPiCYC.do_update(str(self.fmt.format(attributes["piCYC"])))
            self.txtPiF.do_update(str(self.fmt.format(attributes["piF"])))
            self.txtPiL.do_update(str(self.fmt.format(attributes["piL"])))
