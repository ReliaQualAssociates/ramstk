# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.components.relay.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Relay Input Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry, RAMSTKFixedPanel

# Key is contact rating ID.  Index is application ID.
RELAY_APPLICATION_DICT = {
    1: [[_("Dry Circuit")]],
    2: [
        [_("General Purpose")],
        [_("Sensitive (0 - 100mW)")],
        [_("Polarized")],
        [_("Vibrating Reed")],
        [_("High Speed")],
        [_("Thermal Time Delay")],
        [_("Electronic Time Delay, Non-Thermal")],
        [_("Magnetic Latching")],
    ],
    3: [
        [_("High Voltage")],
        [_("Medium Power")],
    ],
    4: [[_("Contactors, High Current")]],
}
# First key is contact rating ID, second key is application ID.
# Index is construction ID.
RELAY_CONSTRUCTION_DICT = {
    1: {
        1: [
            [_("Armature (Long)")],
            [_("Dry Reed")],
            [_("Mercury Wetted")],
            [_("Magnetic Latching")],
            [_("Balanced Armature")],
            [_("Solenoid")],
        ]
    },
    2: {
        1: [
            [_("Armature (Long)")],
            [_("Balanced Armature")],
            [_("Solenoid")],
        ],
        2: [
            [_("Armature (Long and Short)")],
            [_("Mercury Wetted")],
            [_("Magnetic Latching")],
            [_("Meter Movement")],
            [_("Balanced Armature")],
        ],
        3: [
            [_("Armature (Short)")],
            [_("Meter Movement")],
        ],
        4: [
            [_("Dry Reed")],
            [_("Mercury Wetted")],
        ],
        5: [
            [_("Armature (Balanced and Short)")],
            [_("Dry Reed")],
        ],
        6: [[_("Bimetal")]],
        8: [
            [_("Dry Reed")],
            [_("Mercury Wetted")],
            [_("Balanced Armature")],
        ],
    },
    3: {
        1: [
            [_("Vacuum (Glass)")],
            [_("Vacuum (Ceramic)")],
        ],
        2: [
            [_("Armature (Long and Short)")],
            [_("Mercury Wetted")],
            [_("Magnetic Latching")],
            [_("Mechanical Latching")],
            [_("Balanced Armature")],
            [_("Solenoid")],
        ],
    },
    4: {
        1: [
            [_("Armature (Short)")],
            [_("Magnetic Latching")],
            [_("Balanced Armature")],
            [_("Solenoid")],
        ]
    },
}
RELAY_QUALITY_DICT = {
    1: [
        ["S"],
        ["R"],
        ["P"],
        ["M"],
        ["MIL-C-15305"],
        [_("Lower")],
    ],
    2: [
        ["MIL-SPEC"],
        [_("Lower")],
    ],
}
# Key is subcategory ID.  Index is type ID.
RELAY_TYPE_DICT = {
    1: [
        [_("General Purpose")],
        [_("Contactor, High Current")],
        [_("Latching")],
        [_("Reed")],
        [_("Thermal, Bi-Metal")],
        [_("Meter Movement")],
    ],
    2: [
        [_("Solid State")],
        [_("Hybrid and Solid State Time Delay")],
    ],
}
# Index is the contact form ID.
RELAY_CONTACT_FORM_LIST = [
    ["SPST"],
    ["DPST"],
    ["SPDT"],
    ["3PST"],
    ["4PST"],
    ["DPDT"],
    ["3PDT"],
    ["4PDT"],
    ["6PDT"],
]
# Index is contact rating ID.
RELAY_CONTACT_RATING_LIST = [
    [_("Signal Current (low mV and mA)")],
    [_("0 - 5 Amp")],
    [_("5 - 20 Amp")],
    [_("20 - 600 Amp")],
]
# Index is the technology ID (load type).
RELAY_TECHNOLOGY_LIST = [
    [_("Resistive")],
    [_("Inductive")],
    [_("Lamp")],
]


class RelayDesignElectricInputPanel(RAMSTKFixedPanel):
    """Display Relay assessment input attribute data in the RAMSTK Work Book.

    The Relay assessment input view displays all the assessment inputs for the selected
    relay.  This includes, currently, inputs for MIL-HDBK-217FN2.  The attributes of a
    Relay assessment input view are:

    :cvar dict _dic_specifications: dictionary of relay MIL-SPECs.  Key is     relay
    subcategory ID; values are lists of specifications. :cvar dict _dic_styles:
    dictionary of relay styles defined in the     MIL-SPECs.  Key is relay subcategory
    ID; values are lists of styles.

    :ivar cmbType: select and display the type of relay. :ivar cmbLoadType: select and
    display the type of load the relay is     switching. :ivar cmbContactForm: select
    and display the form of the relay contacts. :ivar cmbContactRating: select and
    display the rating of the relay     contacts. :ivar cmbApplication: select and
    display the relay application. :ivar cmbConstruction: select and display the relay's
    method of     construction. :ivar txtCycles: enter and display the number of relay
    cycles per hour.
    """

    # Define private dict class attributes.
    _dic_application: Dict[int, List[List[str]]] = RELAY_APPLICATION_DICT
    _dic_construction: Dict[int, Dict[int, List[List[str]]]] = RELAY_CONSTRUCTION_DICT
    _dic_quality: Dict[int, List[List[str]]] = RELAY_QUALITY_DICT
    _dic_types: Dict[int, List[List[str]]] = RELAY_TYPE_DICT

    # Define private list class attributes.
    _lst_technology: List[List[str]] = RELAY_TECHNOLOGY_LIST
    _lst_contact_form: List[List[str]] = RELAY_CONTACT_FORM_LIST
    _lst_contact_rating: List[List[str]] = RELAY_CONTACT_RATING_LIST

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Relay Design Inputs")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Relay assessment input view."""
        super().__init__()

        # Initialize widgets.
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbContactForm: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbContactRating: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbLoadType: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()
        self.txtCycles: RAMSTKEntry = RAMSTKEntry()

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

        self.cmbContactRating.connect("changed", self._on_combo_changed, 4)
        self.cmbApplication.connect("changed", self._on_combo_changed, 5)

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "changed_subcategory": self.do_load_comboboxes,
                "succeed_get_reliability_attributes": self._set_reliability_attributes,
            }
        )

    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the Relay RAMSTKComboBox()s.

        :param subcategory_id: the subcategory ID of the selected relay.
        :return: None
        :rtype: None
        """
        self.subcategory_id = subcategory_id

        self.cmbContactForm.do_load_combo(
            self._lst_contact_form,
            signal="changed",
        )
        self.cmbContactRating.do_load_combo(
            self._lst_contact_rating,
            signal="changed",
        )
        self.cmbLoadType.do_load_combo(
            self._lst_technology,
            signal="changed",
        )
        self.cmbQuality.do_load_combo(
            self._get_quality_list(),
            signal="changed",
        )
        self.cmbType.do_load_combo(
            self._dic_types.get(self.subcategory_id, [[""]]),
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
                    "tooltip": _("The quality level."),
                },
                _("Quality Level:"),
                "gint",
            ],
            "type_id": [
                48,
                self.cmbType,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The relay type."),
                },
                _("Type:"),
                "gint",
            ],
            "technology_id": [
                37,
                self.cmbLoadType,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The type of load the relay is switching."),
                },
                _("Load Type:"),
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
                    "tooltip": _("The contact form of the relay."),
                },
                _("Contact Form:"),
                "gint",
            ],
            "contact_rating_id": [
                9,
                self.cmbContactRating,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The rating of the relay contacts."),
                },
                _("Contact Rating:"),
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
                    "tooltip": _("The type of relay application."),
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
                    "tooltip": _("The method of construction of the relay."),
                },
                _("Construction:"),
                "gint",
            ],
            "n_cycles": [
                2,
                self.txtCycles,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _("The number of relay on/off cycles per hour."),
                },
                _("Number of Cycles/Hour:"),
                "gfloat",
            ],
        }

    def _get_application_list(self) -> List[List[str]]:
        """Return the list of relay applications.

        :return: list of relay applications.
        :rtype: list
        """
        _contact_rating_id = int(self.cmbContactRating.get_active())
        return self._dic_application.get(_contact_rating_id, [])

    def _get_construction_list(self) -> List[List[str]]:
        """Return the list of relay construction methods.

        :return: list of relay construction methods.
        :rtype: list
        """
        _application_id = int(self.cmbApplication.get_active())
        _contact_rating_id = int(self.cmbContactRating.get_active())
        return self._dic_construction.get(_contact_rating_id, {}).get(
            _application_id, []
        )

    def _get_quality_list(self) -> List[List[str]]:
        """Return the list of relay qualities.

        :return: list of relay qualities.
        :rtype: list
        """
        _default_quality_list = [
            [_("Established Reliability")],
            ["MIL-SPEC"],
            [_("Lower")],
        ]
        return (
            _default_quality_list
            if self._hazard_rate_method_id == 1
            else self._dic_quality.get(self.subcategory_id, [[""]])
        )

    def _on_combo_changed(self, __combo: RAMSTKComboBox, index: int) -> None:
        """Retrieve RAMSTKCombo() changes and assign to Relay attribute.

        This method is called by:

            * Gtk.Combo() 'changed' signal

        :param __combo: the RAMSTKCombo() that called this method.  This
            parameter is unused in this method but is required because the
            widget provides it to the callback function.
        :param index: the position in the signal handler list associated
            with the calling RAMSTKComboBox().  Indices are:

            +-------+------------------+-------+------------------+
            | Index | Widget           | Index | Widget           |
            +=======+==================+=======+==================+
            |   4   | cmbCApplication  |   5   | cmbConstruction  |
            +-------+------------------+-------+------------------+

        :return: None
        :rtype: None
        """
        if index == 4:
            self.cmbApplication.do_load_combo(
                self._get_application_list(),
                signal="changed",
            )
        elif index == 5:
            self.cmbConstruction.do_load_combo(
                self._get_construction_list(),
                signal="changed",
            )

    def _set_reliability_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        :return: None
        :rtype: None
        """
        self._hazard_rate_method_id = attributes["hazard_rate_method_id"]
        self._quality_id = attributes["quality_id"]

        self._set_sensitive()
        super().set_widget_sensitivity([self.cmbQuality])
        self.cmbQuality.do_update(
            self._quality_id,
            signal="changed",
        )

    def _set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected relay.

        :return: None
        :rtype: None
        """
        # Define all widgets that could be sensitive
        _all_widgets = [
            self.cmbApplication,
            self.cmbConstruction,
            self.cmbContactForm,
            self.cmbContactRating,
            self.cmbLoadType,
            self.cmbType,
            self.txtCycles,
        ]

        # Reset all widgets to be insensitive.
        super().set_widget_sensitivity(
            _all_widgets,
            False,
        )

        super().set_widget_sensitivity([self.cmbType])

        if self.subcategory_id == 1 and self._hazard_rate_method_id != 1:
            _additional_widgets = [
                self.cmbApplication,
                self.cmbConstruction,
                self.cmbContactForm,
                self.cmbContactRating,
                self.cmbLoadType,
                self.txtCycles,
            ]
            super().set_widget_sensitivity(_additional_widgets)

            self.cmbApplication.do_load_combo(
                self._get_application_list,
                signal="changed",
            )
            self.cmbConstruction.do_load_combo(
                self._get_construction_list,
                signal="changed",
            )
