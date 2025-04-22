# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.components.meter.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Meter Input Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.constants.meter import METER_QUALITY_DICT, METER_TYPE_DICT
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox,
    RAMSTKFixedPanel,
    WidgetConfig,
    make_widget_config,
)


class MeterDesignElectricInputPanel(RAMSTKFixedPanel):
    """Display Meter assessment input attribute data in the RAMSTK Work Book.

    The Meter assessment input view displays all the assessment inputs for the selected
    Meter item.  This includes, currently, inputs for MIL-HDBK-217FN2.  The attributes
    of a Meter assessment input view are:

    :ivar cmbApplication: select and display the application of the meter.
    :ivar cmbType: select and display the type of meter.
    """

    # Define private class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Meter Design Inputs")

    def __init__(self) -> None:
        """Initialize an instance of the Meter assessment input view."""
        super().__init__()

        # Initialize widgets.
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.cmbQuality,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "quality_id",
                    "index": 32,
                    "label_text": _("Quality Level:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                {
                    "editable": True,
                    "tooltip": _("The quality level of the meter."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbType,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "type_id",
                    "index": 48,
                    "label_text": _("Meter Type:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The type of meter."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbApplication,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "application_id",
                    "index": 2,
                    "label_text": _("Meter Function:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The application of the panel meter."),
                    "visible": True,
                },
            ),
        ]
        self._hazard_rate_method_id: int = 0
        self._quality_id: int = 0

        # Initialize public instance attributes.
        self.category_id: int = 0
        self.subcategory_id: int = 0

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()
        super().do_set_widget_callbacks()
        self._do_load_application()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "changed_subcategory": self.on_subcategory_change,
                "succeed_get_reliability_attributes": self._set_reliability_attributes,
            }
        )

    def on_subcategory_change(self, subcategory_id: int) -> None:
        """Load the meter RAMSTKComboBoxes with subcategory specific entries.

        :param subcategory_id: the subcategory ID of the selected meter.
        """
        self.subcategory_id = subcategory_id

        self.cmbQuality.do_load_combo(
            self._get_quality_list(),
        )
        self.cmbType.do_load_combo(
            METER_TYPE_DICT.get(self.subcategory_id, []),
        )

        self._set_sensitive()

    def _do_load_application(self) -> None:
        """Load the RAMSTKComboBox with the meter application list."""
        self.cmbApplication.do_load_combo(
            [
                [_("Ammeter")],
                [_("Voltmeter")],
                [_("Other")],
            ],
        )

    def _get_quality_list(self) -> List[List[str]]:
        """Return the list of quality levels to load into the RAMSTKComboBox().

        :return: list of meter quality levels.
        :rtype: list
        """
        _default_quality_list = [
            ["MIL-SPEC"],
            [_("Lower")],
        ]

        return (
            _default_quality_list
            if self._hazard_rate_method_id == 1
            else METER_QUALITY_DICT.get(self.subcategory_id, [[""]])
        )

    def _set_reliability_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        """
        self._hazard_rate_method_id = attributes["hazard_rate_method_id"]
        self._quality_id = attributes["quality_id"]

        self._set_sensitive()
        super().set_widget_sensitivity([self.cmbQuality])
        self.cmbQuality.do_update(
            {"quality_id": self._quality_id},
        )

    def _set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected meter."""
        self.cmbApplication.set_sensitive(False)
        self.cmbType.set_sensitive(True)

        if self._hazard_rate_method_id == 2 and self.subcategory_id == 2:
            self.cmbApplication.set_sensitive(True)
