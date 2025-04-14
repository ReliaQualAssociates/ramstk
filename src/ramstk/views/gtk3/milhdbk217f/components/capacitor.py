# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.capacitor.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor Results panel module."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry, WidgetConfig, make_widget_config


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

    # Define private class attributes.
    _lambda_p = '<span foreground="blue">\u03bb<sub>p</sub> = '
    _function_1 = (
        "\u03bb<sub>b</sub>\u03c0<sub>CV</sub>\u03c0<sub>Q</sub>"
        "\u03c0<sub>E</sub></span>"
    )
    _function_2 = "\u03bb<sub>b</sub>\u03c0<sub>Q</sub>\u03c0<sub>E</sub></span>"
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
        + "\u03bb<sub>b</sub>\u03c0<sub>CV</sub>\u03c0<sub>SR</sub>\u03c0<sub"
        ">Q</sub>\u03c0<sub>E</sub></span>",
        13: _lambda_p
        + "\u03bb<sub>b</sub>\u03c0<sub>CV</sub>\u03c0<sub>C</sub>\u03c0<sub>Q"
        "</sub>\u03c0<sub>E</sub></span>",
        14: _lambda_p + _function_1,
        15: _lambda_p + _function_1,
        16: _lambda_p + _function_2,
        17: _lambda_p + _function_2,
        18: _lambda_p + _function_2,
        19: _lambda_p
        + "\u03bb<sub>b</sub>\u03c0<sub>CF</sub>\u03c0<sub>Q</sub>\u03c0<sub>E"
        "</sub></span>",
    }
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Capacitor MIL-HDBK-217F Results")

    def __init__(self) -> None:
        """Initialize an instance of the Capacitor assessment result view."""
        super().__init__()

        # Initialize widgets.
        self.txtPiCV: RAMSTKEntry = RAMSTKEntry()
        self.txtPiCF: RAMSTKEntry = RAMSTKEntry()
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
                        "The assessment model used to calculate the capacitor hazard "
                        "rate."
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
                    "tooltip": _("The base hazard rate for the capacitor."),
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
                    "tooltip": _("The quality factor for the capacitor."),
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
                    "tooltip": _("The environment factor for the capacitor."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiCV,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_cv",
                    "index": 17,
                    "label_text": "\u03c0<sub>CV</sub>:",
                    "listen_topic": None,
                    "send_topic": "wvw_editing_milhdbk217f",
                },
                {
                    "tooltip": _("The capacitance factor for the capacitor."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiCF,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_cf",
                    "index": 15,
                    "label_text": "\u03c0<sub>CF</sub>:",
                    "listen_topic": None,
                    "send_topic": "wvw_editing_milhdbk217f",
                },
                {
                    "tooltip": _("The configuration factor for the capacitor."),
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
                    "tooltip": _("The construction factor for the capacitor."),
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

        :param attributes: the attributes of the selected capacitor assessment result.
        """
        super().do_load_entries(attributes)
        super().do_set_widget_sensitivity(
            [
                self.txtPiCV,
                self.txtPiCF,
                self.txtPiC,
            ],
            False,
        )

        # MIL-HDBK-217F, Parts Stress
        if self.category_id == 4 and self._hazard_rate_method_id == 2:
            self.lblModel.do_update(
                {"hazard_rate_model": self._dic_part_stress[self.subcategory_id]}
            )
            self.txtPiCV.do_update({"piCV": str(self.fmt.format(attributes["piCV"]))})
            self.txtPiCF.do_update({"piCF": str(self.fmt.format(attributes["piCF"]))})
            self.txtPiC.do_update({"piC": str(self.fmt.format(attributes["piC"]))})
