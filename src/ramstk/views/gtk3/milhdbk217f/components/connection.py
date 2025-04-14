# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.connection.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Connection Results panel module."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.milhdbk217f import MilHdbk217FResultPanel
from ramstk.views.gtk3.widgets import RAMSTKEntry, WidgetConfig, make_widget_config


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

    # Define private class attributes.
    _dic_part_stress = {
        1: '<span foreground="blue">\u03bb<sub>p</sub> = '
        "\u03bb<sub>b</sub>\u03c0<sub>K</sub>\u03c0<sub>P</sub>\u03c0"
        "<sub>E</sub></span>",
        2: '<span foreground="blue">\u03bb<sub>p</sub> = '
        "\u03bb<sub>b</sub>\u03c0<sub>K</sub>\u03c0<sub>P</sub>\u03c0"
        "<sub>E</sub></span>",
        3: '<span foreground="blue">\u03bb<sub>p</sub> = '
        "\u03bb<sub>b</sub>\u03c0<sub>P</sub>\u03c0<sub>E</sub></span>",
        4: '<span foreground="blue">\u03bb<sub>p</sub> = '
        "\u03bb<sub>b</sub>[N<sub>1</sub>\u03c0<sub>C</sub> + "
        "N<sub>2</sub>(\u03c0<sub>C</sub> + "
        "13)]\u03c0<sub>Q</sub>\u03c0<sub>E</sub></span>",
        5: '<span foreground="blue">\u03bb<sub>p</sub> = '
        "\u03bb<sub>b</sub>\u03c0<sub>Q</sub>\u03c0<sub>E</sub></span>",
    }
    _record_field: str = "hardware_id"
    _tag: str = "milhdbk217f"
    _title: str = _("Connection MIL-HDBK-217F Results")

    def __init__(self) -> None:
        """Initialize an instance of the Connection assessment result view."""
        super().__init__()

        # Initialize widgets.
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiK: RAMSTKEntry = RAMSTKEntry()
        self.txtPiP: RAMSTKEntry = RAMSTKEntry()

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
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "The assessment model used to calculate the connection hazard "
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
                    "send_topic": None,
                },
                {
                    "tooltip": _("The base hazard rate for the connection."),
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
                    "send_topic": None,
                },
                {
                    "tooltip": _("The quality factor for the connection."),
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
                    "send_topic": None,
                },
                {
                    "tooltip": _("The environment factor for the connection."),
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
                    "send_topic": None,
                },
                {
                    "tooltip": _("The mating/unmating factor for the connection."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiK,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_k",
                    "index": 22,
                    "label_text": "\u03c0<sub>K</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The active pins factor for the connection."),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPiP,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "pi_p",
                    "index": 28,
                    "label_text": "\u03c0<sub>P</sub>:",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _("The complexity factor for the connection."),
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

        :param attributes: the dict of attributes to load into the widgets.
        """
        super().do_load_entries(attributes)
        super().do_set_widget_sensitivity(
            [
                self.txtPiK,
                self.txtPiP,
                self.txtPiC,
            ],
            False,
        )

        # MIL-HDBK-217F, Parts Stress
        if self.category_id == 8 and self._hazard_rate_method_id == 2:
            self.lblModel.do_update(
                {"hazard_rate_model": self._dic_part_stress[self.subcategory_id]}
            )
            self.txtPiC.do_update({"piC": str(self.fmt.format(attributes["piC"]))})
            self.txtPiK.do_update({"piK": str(self.fmt.format(attributes["piK"]))})
            self.txtPiP.do_update({"piP": str(self.fmt.format(attributes["piP"]))})
