# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.inductor.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Inductor Results panel module."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry, WidgetConfig, make_widget_config


class InductorMilHdbk217FResultPanel(MilHdbk217FResultPanel):
    """Displays Inductor assessment results attribute data.

    The Inductor assessment result view displays all the assessment results
    for the selected inductor.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and part stress methods.  The attributes of an
    Inductor assessment result view are:

    :cvar dict _dic_part_stress: dictionary of MIL-HDBK-217F part stress
        models.  The key is the subcategory ID attribute of the component.

    :ivar list _lst_labels: list of label text to display for the capacitor
        MIL-HDBK-217 input parameters.

    :ivar self.txtLambdaB: displays the base hazard rate for the Hardware
        item.
    :ivar txtPiC: displays the construction factor for the Hardware item.
    """

    # Define private class attributes.
    _dic_part_stress: Dict[int, str] = {
        1: '<span foreground="blue">\u03bb<sub>p</sub> = '
        "\u03bb<sub>b</sub>\u03c0<sub>C</sub>\u03c0<sub>Q</sub>\u03c0"
        "<sub>E</sub></span>",
        2: '<span foreground="blue">\u03bb<sub>p</sub> = '
        "\u03bb<sub>b</sub>\u03c0<sub>Q</sub>\u03c0<sub>E</sub></span>",
    }
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Inductive Device MIL-HDBK-217F Results")

    def __init__(self) -> None:
        """Initialize an instance of the Inductor assessment result view."""
        super().__init__()

        # Initialize widgets.
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()

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
                    "send_topic": "wvw_editing_milhdbk217f",
                },
                {
                    "tooltip": _(
                        "The assessment model used to calculate the inductive device's "
                        "failure rate."
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
                    "send_topic": "wvw_editing_milhdbk217f",
                },
                {
                    "tooltip": _("The base hazard rate for the inductive device."),
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
                    "send_topic": "wvw_editing_milhdbk217f",
                },
                {
                    "tooltip": _("The quality factor for the inductive device."),
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
                    "send_topic": "wvw_editing_milhdbk217f",
                },
                {
                    "tooltip": _("The environment factor for the inductive device."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiC,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_c",
                    "index": 13,
                    "label_text": "\u03c0<sub>C</sub>:",
                    "listen_topic": None,
                    "send_topic": "wvw_editing_milhdbk217f",
                },
                {
                    "tooltip": _("The construction factor for the inductive device."),
                    "editable": True,
                    "visible": True,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Set widget sensitivity as needed for the selected capacitor.

        :param attributes: the dict of attributes for the selected inductor.
        """
        super().do_load_entries(attributes)
        super().do_set_widget_sensitivity([self.txtPiC], False)

        # MIL-HDBK-217F, Parts Stress
        if self.category_id == 5 and self._hazard_rate_method_id == 2:
            self.lblModel.do_update(
                {"hazard_rate_model": self._dic_part_stress[self.subcategory_id]}
            )
            self.txtPiC.do_update({"piC": str(self.fmt.format(attributes["piC"]))})
