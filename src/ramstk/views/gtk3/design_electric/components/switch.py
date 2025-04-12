# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.components.switch.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Switch Input Panel."""


# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.constants.switch import (
    SWITCH_APPLICATION_DICT,
    SWITCH_CONSTRUCTION_DICT,
    SWITCH_CONTACT_FORM_DICT,
)
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    WidgetConfig,
)


class SwitchDesignElectricInputPanel(RAMSTKFixedPanel):
    """Display Switch assessment input attribute data in the RAMSTK Work Book.

    The Switch assessment input view displays all the assessment inputs for the selected
    switch.  This includes, currently, inputs for MIL-HDBK-217FN2.  The attributes of a
    switch assessment input view are:

    :ivar cmbApplication: select and display the switch application.
    :ivar cmbConstruction: select and display the switch construction method.
    :ivar cmbContactForm: select and display the switch contact form.
    :ivar txtNCycles: enter and display the number of switch cycles/hour.
    :ivar txtNElements: enter and display the number of switch wafers.
    """

    # Define private class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Switch Design Inputs")

    def __init__(self) -> None:
        """Initialize an instance of the Switch assessment input view."""
        super().__init__()

        # Initialize widgets.
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbContactForm: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()
        self.txtNCycles: RAMSTKEntry = RAMSTKEntry()
        self.txtNElements: RAMSTKEntry = RAMSTKEntry()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": self.cmbQuality,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "quality_id",
                    "index": 32,
                    "label_text": _("Quality Level:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The quality level of the switch."),
                    "visible": True,
                },
            },
            {
                "widget": self.cmbApplication,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "application_id",
                    "index": 2,
                    "label_text": _("Application:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The application of the switch."),
                    "visible": True,
                },
            },
            {
                "widget": self.cmbConstruction,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "construction_id",
                    "index": 6,
                    "label_text": _("Construction:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The construction method for the switch."),
                    "visible": True,
                },
            },
            {
                "widget": self.cmbContactForm,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "contact_form_id",
                    "index": 7,
                    "label_text": _("Contact Form:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The contact form and quantity of the switch."),
                    "visible": True,
                },
            },
            {
                "widget": self.txtNCycles,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "n_cycles",
                    "index": 24,
                    "label_text": _("Number of Cycles/Hour:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The number of cycles per hour of the switch."),
                    "visible": True,
                },
            },
            {
                "widget": self.txtNElements,
                "attributes": {
                    "datatype": "gint",
                    "default": 1,
                    "field": "n_elements",
                    "index": 25,
                    "label_text": _("Number of Active Contacts:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The number of active contacts in the switch."),
                    "visible": True,
                },
            },
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
        self._do_load_quality()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "changed_subcategory": self.on_subcategory_change,
                "succeed_get_reliability_attributes": self._set_reliability_attributes,
            }
        )

    def on_subcategory_change(self, subcategory_id: int) -> None:
        """Load the switch RAMSTKComboBoxes with subcategory specific entries.

        :param subcategory_id: the subcategory ID of the selected switch.
        """
        self.subcategory_id = subcategory_id

        self.cmbApplication.do_load_combo(
            SWITCH_APPLICATION_DICT.get(self.subcategory_id, []),
        )
        self.cmbConstruction.do_load_combo(
            self._get_construction_list(),
        )
        self.cmbContactForm.do_load_combo(
            SWITCH_CONTACT_FORM_DICT.get(self.subcategory_id, [[""]]),
        )

        self._set_sensitive()

    def _do_load_quality(self) -> None:
        """Load the quality RAMSTKComboBox with quality levels."""
        self.cmbQuality.do_load_combo(
            [["MIL-SPEC"], [_("Lower")]],
        )

    def _get_construction_list(self) -> List[List[str]]:
        """Return the list of switch construction methods.

        :return: list of switch construction methods.
        :rtype: list
        """
        _default_construction_list = [[_("Thermal")], [_("Magnetic")]]
        return (
            _default_construction_list
            if self._hazard_rate_method_id == 1
            else SWITCH_CONSTRUCTION_DICT.get(self.subcategory_id, [[""]])
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
        """Set widget sensitivity as needed for the selected switch."""
        # Define all widgets that could be sensitive
        _all_widgets = [
            self.cmbApplication,
            self.cmbConstruction,
            self.cmbContactForm,
            self.txtNCycles,
            self.txtNElements,
        ]

        # Reset all widgets to be insensitive.
        super().set_widget_sensitivity(
            _all_widgets,
            False,
        )

        # Set cmbApplication sensitive if hazard_rate_method_id is 2
        if self._hazard_rate_method_id == 2:
            self.cmbApplication.set_sensitive(True)

        # Define a sensitivity map for different widgets based on hazard rate method
        # and subcategory
        _sensitivity_map = {
            1: {5: [self.cmbConstruction]},
            2: {
                1: [
                    self.cmbConstruction,
                    self.cmbContactForm,
                    self.txtNCycles,
                ],
                2: [
                    self.cmbConstruction,
                    self.txtNCycles,
                    self.txtNElements,
                ],
                3: [
                    self.cmbConstruction,
                    self.txtNCycles,
                    self.txtNElements,
                ],
                4: [
                    self.txtNCycles,
                    self.txtNElements,
                ],
                5: [
                    self.cmbConstruction,
                    self.cmbContactForm,
                ],
            },
        }
