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
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry, RAMSTKFixedPanel

# Key is subcategory ID; index is application ID.
SWITCH_APPLICATION_DICT = {
    1: [[_("Resistive")], [_("Inductive")], [_("Lamp")]],
    2: [[_("Resistive")], [_("Inductive")], [_("Lamp")]],
    3: [[_("Resistive")], [_("Inductive")], [_("Lamp")]],
    4: [[_("Resistive")], [_("Inductive")], [_("Lamp")]],
    5: [
        [_("Not Used as a Power On/Off Switch")],
        [_("Also Used as a Power On/Off Switch")],
    ],
}
# Key is subcategory ID; index is construction ID.
SWITCH_CONSTRUCTION_DICT = {
    1: [[_("Snap Action")], [_("Non-Snap Action")]],
    2: [
        [_("Actuation Differential > 0.002 inches")],
        [_("Actuation Differential < 0.002 inches")],
    ],
    3: [[_("Ceramic RF Wafers")], [_("Medium Power Wafers")]],
    5: [[_("Magnetic")], [_("Thermal")], [_("Thermal-Magnetic")]],
}
# Key is subcategory ID; index is contact form ID.
SWITCH_CONTACT_FORM_DICT = {
    1: [
        ["SPST"],
        ["DPST"],
        ["SPDT"],
        ["3PST"],
        ["4PST"],
        ["DPDT"],
        ["3PDT"],
        ["4PDT"],
        ["6PDT"],
    ],
    5: [["SPST"], ["DPST"], ["3PST"], ["4PST"]],
}


class SwitchDesignElectricInputPanel(RAMSTKFixedPanel):
    """Display Switch assessment input attribute data in the RAMSTK Work Book.

    The Switch assessment input view displays all the assessment inputs for
    the selected switch.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a switch assessment input view are:

    :cvar dict _dic_applications: dictionary of switch applications.  Key is
        switch subcategory ID; values are lists of applications.
    :cvar dict _dic_construction: dictionary of switch construction methods.
        Key is switch subcategory ID; values are lists of construction methods.
    :cvar dict _dic_contact_forms: dictionary of switch contact forms.  Key is
        switch subcategory ID; values are lists of contact forms.

    :ivar cmbApplication: select and display the switch application.
    :ivar cmbConstruction: select and display the switch construction method.
    :ivar cmbContactForm: select and display the switch contact form.
    :ivar txtNCycles: enter and display the number of switch cycles/hour.
    :ivar txtNElements: enter and display the number of switch wafers.
    """

    # Define private dict class attributes.
    _dic_applications: Dict[int, List[List[str]]] = SWITCH_APPLICATION_DICT
    _dic_constructions: Dict[int, List[List[str]]] = SWITCH_CONSTRUCTION_DICT
    _dic_contact_forms: Dict[int, List[List[str]]] = SWITCH_CONTACT_FORM_DICT

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Switch Design Inputs")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

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

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hazard_rate_method_id: int = 0
        self._quality_id: int = 0

        # Initialize public dictionary attributes.
        self.dic_attribute_widget_map = self._do_initialize_attribute_widget_map()

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.category_id: int = 0
        self.subcategory_id: int = 0

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "changed_subcategory": self.do_load_comboboxes,
                "succeed_get_reliability_attributes": self._do_set_reliability_attributes,
            }
        )

    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the switch RAMSTKComboBox()s.

        :param subcategory_id: the subcategory ID of the selected switch.
        :return: None
        :rtype: None
        """
        self.subcategory_id = subcategory_id

        self.cmbApplication.do_load_combo(
            self._get_application_list(),
            signal="changed",
        )
        self.cmbConstruction.do_load_combo(
            self._get_construction_list(),
            signal="changed",
        )
        self.cmbQuality.do_load_combo(
            [["MIL-SPEC"], [_("Lower")]],
            signal="changed",
        )
        self.cmbContactForm.do_load_combo(
            self._get_contact_form_list(),
            signal="changed",
        )

        self._set_sensitive()

    def _do_initialize_attribute_widget_map(self) -> Dict[str, Any]:
        """Initialize the attribute widget map."""
        return {
            "quality_id": [
                32,
                self.cmbQuality,
                "changed",
                super().on_changed_combo,
                "wvw_editing_reliability",
                0,
                {
                    "tooltip": _("The quality level of the switch."),
                },
                _("Quality Level:"),
                "gint",
            ],
            "application_id": [
                2,
                self.cmbApplication,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The application of the switch."),
                },
                _("Application:"),
                "gint",
            ],
            "construction_id": [
                6,
                self.cmbConstruction,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The construction method for the switch."),
                },
                _("Construction:"),
                "gint",
            ],
            "contact_form_id": [
                7,
                self.cmbContactForm,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The contact form and quantity of the switch."),
                },
                _("Contact Form:"),
                "gint",
            ],
            "n_cycles": [
                24,
                self.txtNCycles,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _("The number of cycles per hour of the switch."),
                },
                _("Number of Cycles/Hour:"),
                "gfloat",
            ],
            "n_elements": [
                25,
                self.txtNElements,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                1,
                {
                    "tooltip": _("The number of active contacts in the switch."),
                },
                _("Number of Active Contacts:"),
                "gint",
            ],
        }

    def _do_set_reliability_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        :return: None
        :rtype: None
        """
        self._hazard_rate_method_id = attributes["hazard_rate_method_id"]
        self._quality_id = attributes["quality_id"]

        self.cmbQuality.set_sensitive(True)
        self.cmbQuality.do_update(
            self._quality_id,
            signal="changed",
        )

        self._set_sensitive()

    def _get_application_list(self) -> List[List[str]]:
        """Return the list of switch applications.

        :return: list of switch applications.
        :rtype: list
        """
        return self._dic_applications.get(self.subcategory_id, [])

    def _get_construction_list(self) -> List[List[str]]:
        """Return the list of switch construction methods.

        :return: list of switch construction methods.
        :rtype: list
        """
        _default_construction_list = [[_("Thermal")], [_("Magnetic")]]
        return (
            _default_construction_list
            if self._hazard_rate_method_id == 1
            else self._dic_constructions.get(self.subcategory_id, [[""]])
        )

    def _get_contact_form_list(self) -> List[List[str]]:
        """Return the list of sqitch contact forms.

        :return: list of switch contact forms.
        :rtype: list
        """
        return self._dic_contact_forms.get(self.subcategory_id, [[""]])

    def _set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected switch.

        :return: None
        :rtype: None
        """
        # Define all widgets that could be sensitive
        _all_widgets = [
            self.cmbApplication,
            self.cmbConstruction,
            self.cmbContactForm,
            self.txtNCycles,
            self.txtNElements,
        ]

        # Reset all widgets to be insensitive.
        super.set_widget_sensitivity(
            _all_widgets,
            False,
        )

        # Set cmbApplication sensitive if hazard_rate_method_id is 2
        if self._hazard_rate_method_id == 2:
            self.cmbApplication.set_sensitive(True)

        # Define a sensitivity map for different widgets based on hazard rate method and subcategory
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
