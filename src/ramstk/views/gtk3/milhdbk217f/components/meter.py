# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.meter.py is part of the RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Meter Results Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry


class MeterMilHdbk217FResultPanel(MilHdbk217FResultPanel):
    """Display Meter assessment results attribute data in the RAMSTK Work Book.

    The Meter assessment result view displays all the assessment results
    for the selected meter.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a meter assessment result view are:

    :ivar txtPiA: displays the application factor for the panel meter.
    :ivar txtPiF: displays the function factor for the panel meter.
    :ivar txtPiT: displays the temperature stress factor for the elapsed time
        meter.
    """

    # Define private class dict class attributes.
    _dic_part_stress: Dict[int, str] = {
        1: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>\u03C0<sub>A</sub>\u03C0<sub>F</sub>\u03C0<sub>Q"
        "</sub>\u03C0<sub>E</sub></span>",
        2: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>E</sub></span> ",
    }

    # Define private class list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Meter MIL-HDBK-217F Results")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Meter assessment result view."""
        super().__init__()

        # Initialize widgets.
        self.txtPiA: RAMSTKEntry = RAMSTKEntry()
        self.txtPiF: RAMSTKEntry = RAMSTKEntry()
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
                        "The assessment model used to calculate the meter hazard rate."
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
                    "tooltip": _("The base hazard rate for the meter."),
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
                    "tooltip": _("The quality factor for the meter."),
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
                    "tooltip": _("The environment factor for the meter."),
                },
                "\u03C0<sub>E</sub>:",
            ],
            "pi_a": [
                12,
                self.txtPiA,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The application factor for the meter."),
                },
                "\u03C0<sub>A</sub>:",
            ],
            "pi_f": [
                20,
                self.txtPiF,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The function factor for the meter."),
                },
                "\u03C0<sub>F</sub>:",
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
                        "The temperature stress factor for the elapsed time meter."
                    ),
                },
                "\u03C0<sub>T</sub>:",
            ],
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().do_set_properties()
        super().do_make_panel()

        # Subscribe to PyPubSub messages.

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load the meter assessment results page.

        :param attributes: the attributes dictionary for the selected
            Meter.
        :return: None
        :rtype: None
        """
        super().do_load_entries(attributes)

        self.txtPiA.set_sensitive(False)
        self.txtPiF.set_sensitive(False)
        self.txtPiT.set_sensitive(False)

        if self.category_id == 9 and self._hazard_rate_method_id == 2:
            self.txtPiA.do_update(str(self.fmt.format(attributes["piA"])))
            self.txtPiF.do_update(str(self.fmt.format(attributes["piF"])))
            self.txtPiT.do_update(str(self.fmt.format(attributes["piT"])))
