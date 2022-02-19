# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.miscellaneous.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Miscellaneous Results Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry


class MiscellaneousMilHdbk217FResultPanel(MilHdbk217FResultPanel):
    """Display Misc assessment results attribute data in the RAMSTK Work Book.

    The Miscellaneous hardware item assessment result view displays all the
    assessment results for the selected miscellaneous hardware item.  This
    includes, currently, results for MIL-HDBK-217FN2 parts count and
    MIL-HDBK-217FN2 part stress methods.  The attributes of a miscellaneous
    hardware item assessment result view are:

    :ivar txtPiA: displays the application factor for the miscellaneous
        hardware item.
    :ivar txtPiU: displays the utilization factor for the miscellaneous
        hardware item.
    """

    # Define private dict class attributes.
    _dic_part_stress: Dict[int, str] = {
        1: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        3: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>\u03C0<sub>E</sub></span>",
        4: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>\u03C0<sub>U</sub>\u03C0<sub>A</sub>\u03C0<sub>E"
        "</sub></span> ",
    }

    # Define private class list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Miscellaneous Component MIL-HDBK-217F Results")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize instance of the Miscellaneous assessment result view."""
        super().__init__()

        # Initialize widgets.
        self.txtPiA: RAMSTKEntry = RAMSTKEntry()
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
                        "The assessment model used to calculate the hazard rate."
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
                    "tooltip": _("The base hazard rate."),
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
                    "tooltip": _("The quality factor."),
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
                    "tooltip": _("The environment factor."),
                },
                "\u03C0<sub>E</sub>:",
            ],
            "pi_u": [
                35,
                self.txtPiU,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The utilization factor."),
                },
                "\u03C0<sub>U</sub>:",
            ],
            "pi_a": [
                12,
                self.txtPiA,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The application factor."),
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
        """Load the miscellaneous devices assessment results page.

        :param attributes: the attributes dictionary for the selected
            Miscellaneous item.
        :return: None
        :rtype: None
        """
        super().do_load_entries(attributes)

        self.txtPiU.set_sensitive(False)
        self.txtPiA.set_sensitive(False)

        if self.category_id == 10 and self._hazard_rate_method_id == 2:
            self.txtPiU.do_update(str(self.fmt.format(attributes["piU"])))
            self.txtPiA.do_update(str(self.fmt.format(attributes["piA"])))
