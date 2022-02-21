# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.capacitor.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor Results Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry


class CapacitorMilHdbk217FResultPanel(MilHdbk217FResultPanel):
    """Displays capacitor assessment results attribute data.

    The capacitor assessment result view displays all the assessment results
    for the selected capacitor.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a capacitor assessment result view are:

    :cvar dict _dic_part_stress: dictionary of MIL-HDBK-217F part stress
        models.  The key is the subcategory ID attribute of the component.

    :ivar list _lst_labels: list of label text to display for the capacitor
        MIL-HDBK-217 input parameters.

    :ivar self.txtLambdaB: displays the base hazard rate for the Hardware
        item.
    :ivar txtPiCV: displays the capacitance factor for the capacitor.
    :ivar txtPiCF: displays the configuration factor for the capacitor.
    :ivar txtPiC: displays the construction factor for the capacitor.
    """

    _lambda_p = '<span foreground="blue">\u03BB<sub>p</sub> = '
    _function_1 = (
        "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>"
        "\u03C0<sub>E</sub></span>"
    )
    _function_2 = "\u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    # Define private dict class attributes.
    _dic_part_stress: Dict[int, str] = {
        1: _lambda_p + _function_1,
        2: _lambda_p + _function_1,
        3: _lambda_p + _function_1,
        4: _lambda_p + _function_1,
        5: _lambda_p + _function_1,
        6: _lambda_p + _function_1,
        7: _lambda_p + _function_1,
        8: _lambda_p + _function_1,
        9: _lambda_p + _function_1,
        10: _lambda_p + _function_1,
        11: _lambda_p + _function_1,
        12: _lambda_p
        + "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>SR</sub>\u03C0<sub"
        ">Q</sub>\u03C0<sub>E</sub></span>",
        13: _lambda_p
        + "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>C</sub>\u03C0<sub>Q"
        "</sub>\u03C0<sub>E</sub></span>",
        14: _lambda_p + _function_1,
        15: _lambda_p + _function_1,
        16: _lambda_p + _function_2,
        17: _lambda_p + _function_2,
        18: _lambda_p + _function_2,
        19: _lambda_p
        + "\u03BB<sub>b</sub>\u03C0<sub>CF</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
    }

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Capacitor MIL-HDBK-217F Results")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Capacitor assessment result view."""
        super().__init__()

        # Initialize widgets.
        self.txtPiCV: RAMSTKEntry = RAMSTKEntry()
        self.txtPiCF: RAMSTKEntry = RAMSTKEntry()
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()

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
                        "The assessment model used to calculate the capacitor hazard "
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
                    "tooltip": _("The base hazard rate for the capacitor."),
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
                    "tooltip": _("The quality factor for the capacitor."),
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
                    "tooltip": _("The environment factor for the capacitor."),
                },
                "\u03C0<sub>E</sub>:",
            ],
            "pi_cv": [
                17,
                self.txtPiCV,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The capacitance factor for the capacitor."),
                },
                "\u03C0<sub>CV</sub>:",
            ],
            "pi_cf": [
                15,
                self.txtPiCF,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The configuration factor for the capacitor."),
                },
                "\u03C0<sub>CF</sub>:",
            ],
            "pi_c": [
                13,
                self.txtPiC,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The construction factor for the capacitor."),
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
        """Set widget sensitivity as needed for the selected capacitor.

        :return: None
        :rtype: None
        """
        super().do_load_entries(attributes)

        self.txtPiCV.set_sensitive(False)
        self.txtPiCF.set_sensitive(False)
        self.txtPiC.set_sensitive(False)

        # MIL-HDBK-217F, Parts Stress
        if self.category_id == 4 and self._hazard_rate_method_id == 2:
            self.lblModel.do_update(self._dic_part_stress[self.subcategory_id])
            self.txtPiCV.do_update(
                str(self.fmt.format(attributes["piCV"])),
                signal="changed",
            )
            self.txtPiCF.do_update(
                str(self.fmt.format(attributes["piCF"])),
                signal="changed",
            )
            self.txtPiC.do_update(
                str(self.fmt.format(attributes["piC"])),
                signal="changed",
            )
