# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.connection.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Connection Results Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry


class ConnectionMilHdbk217FResultPanel(MilHdbk217FResultPanel):
    """Displays connection assessment results attribute data.

    The connection assessment result view displays all the assessment results
    for the selected connection.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a connection assessment result view are:

    :cvar dict _dic_part_stress: dictionary of MIL-HDBK-217F part stress
        models.  The key is the subcategory ID attribute of the component.

    :ivar list _lst_labels: list of label text to display for the capacitor
        MIL-HDBK-217 input parameters.

    :ivar _hazard_rate_method_id: the ID of the method to use for estimating
        the Hardware item's hazard rate.
    :ivar _subcategory_id: the ID of the Hardware item's subcategory.

    :ivar fmt: the formatting to use when displaying float values.
    :ivar lblModel: displays the hazard rate model use to estimate the
        Hardware item's hazard rate.
    :ivar self.txtLambdaB: displays the base hazard rate for the Hardware
        item.
    :ivar txtPiC: displays the construction factor for the connection.
        :ivar txtPiE: displays the environment factor for the Hardware item.
    :ivar txtPiK: displays the capacitance factor for the connection.
    :ivar txtPiP: displays the configuration factor for the connection.
    :ivar txtPiQ: displays the quality factor for the Hardware item.
    """

    # Define private dict class attributes.
    _dic_part_stress = {
        1: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>\u03C0<sub>K</sub>\u03C0<sub>P</sub>\u03C0"
        "<sub>E</sub></span>",
        2: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>\u03C0<sub>K</sub>\u03C0<sub>P</sub>\u03C0"
        "<sub>E</sub></span>",
        3: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>\u03C0<sub>P</sub>\u03C0<sub>E</sub></span>",
        4: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>[N<sub>1</sub>\u03C0<sub>C</sub> + "
        "N<sub>2</sub>(\u03C0<sub>C</sub> + "
        "13)]\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        5: '<span foreground="blue">\u03BB<sub>p</sub> = '
        "\u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
    }

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Connection MIL-HDBK-217F Results")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Connection assessment result view."""
        super().__init__()

        # Initialize widgets.
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiK: RAMSTKEntry = RAMSTKEntry()
        self.txtPiP: RAMSTKEntry = RAMSTKEntry()

        # Initialize private dict attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dict attributes.
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
                        "The assessment model used to calculate the connection "
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
                    "tooltip": _("The base hazard rate for the connection."),
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
                    "tooltip": _("The quality factor for the connection."),
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
                    "tooltip": _("The environment factor for the connection."),
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
                    "tooltip": _("The mating/unmating factor for the connection."),
                },
                "\u03C0<sub>C</sub>:",
            ],
            "pi_k": [
                22,
                self.txtPiK,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The active pins factor for the connection."),
                },
                "\u03C0<sub>K</sub>:",
            ],
            "pi_p": [
                28,
                self.txtPiP,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _("The complexity factor for the connection."),
                },
                "\u03C0<sub>P</sub>:",
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

        self.txtPiK.set_sensitive(False)
        self.txtPiP.set_sensitive(False)
        self.txtPiC.set_sensitive(False)

        # MIL-HDBK-217F, Parts Stress
        if self.category_id == 8 and self._hazard_rate_method_id == 2:
            self.lblModel.do_update(self._dic_part_stress[self.subcategory_id])

            self.txtPiC.do_update(
                str(self.fmt.format(attributes["piC"])),
                signal="changed",
            )
            self.txtPiK.do_update(
                str(self.fmt.format(attributes["piK"])),
                signal="changed",
            )
            self.txtPiP.do_update(
                str(self.fmt.format(attributes["piP"])),
                signal="changed",
            )
