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

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry, RAMSTKFixedPanel


class RelayDesignElectricInputPanel(RAMSTKFixedPanel):
    """Display Relay assessment input attribute data in the RAMSTK Work Book.

    The Relay assessment input view displays all the assessment inputs for
    the selected relay.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Relay assessment input view are:

    :cvar dict _dic_specifications: dictionary of relay MIL-SPECs.  Key is
        relay subcategory ID; values are lists of specifications.
    :cvar dict _dic_styles: dictionary of relay styles defined in the
        MIL-SPECs.  Key is relay subcategory ID; values are lists of styles.

    :ivar cmbType: select and display the type of relay.
    :ivar cmbLoadType: select and display the type of load the relay is
        switching.
    :ivar cmbContactForm: select and display the form of the relay contacts.
    :ivar cmbContactRating: select and display the rating of the relay
        contacts.
    :ivar cmbApplication: select and display the relay application.
    :ivar cmbConstruction: select and display the relay's method of
        construction.
    :ivar txtCycles: enter and display the number of relay cycles per hour.
    """

    _balanced_armature: str = _("Balanced Armature")
    _dry_reed: str = _("Dry Reed")
    _magnetic_latching: str = _("Magnetic Latching")
    _mechanical_latching: str = _("Mechanical Latching")
    _mercury_wetted: str = _("Mercury Wetted")
    _meter_movement: str = _("Meter Movement")
    _solenoid: str = _("Solenoid")

    # Define private dict class attributes.
    _dic_quality: Dict[int, List[List[str]]] = {
        1: [["S"], ["R"], ["P"], ["M"], ["MIL-C-15305"], [_("Lower")]],
        2: [["MIL-SPEC"], [_("Lower")]],
    }
    # Key is subcategory ID.  Index is type ID.
    _dic_pc_types: Dict[int, List[List[str]]] = {
        1: [
            [_("General Purpose")],
            [_("Contactor, High Current")],
            [_("Latching")],
            [_("Reed")],
            [_("Thermal, Bi-Metal")],
            [_meter_movement],
        ],
        2: [[_("Solid State")], [_("Hybrid and Solid State Time Delay")]],
    }
    # Key is subcategory ID, index is type ID.
    _dic_types: Dict[int, List[List[str]]] = {
        1: [[_("85C Rated")], [_("125C Rated")]],
        2: [[_("Solid State")], [_("Solid State Time Delay")], [_("Hybrid")]],
    }
    # Key is contact rating ID.  Index is application ID.
    _dic_application: Dict[int, List[List[str]]] = {
        1: [[_("Dry Circuit")]],
        2: [
            [_("General Purpose")],
            [_("Sensitive (0 - 100mW)")],
            [_("Polarized")],
            [_("Vibrating Reed")],
            [_("High Speed")],
            [_("Thermal Time Delay")],
            [_("Electronic Time Delay, Non-Thermal")],
            [_magnetic_latching],
        ],
        3: [[_("High Voltage")], [_("Medium Power")]],
        4: [[_("Contactors, High Current")]],
    }
    # First key is contact rating ID, second key is application ID.  Index is
    # construction ID.
    _dic_construction: Dict[int, Dict[int, List[List[str]]]] = {
        1: {
            1: [
                [_("Armature (Long)")],
                [_dry_reed],
                [_mercury_wetted],
                [_magnetic_latching],
                [_balanced_armature],
                [_solenoid],
            ]
        },
        2: {
            1: [[_("Armature (Long)")], [_balanced_armature], [_solenoid]],
            2: [
                [_("Armature (Long and Short)")],
                [_mercury_wetted],
                [_magnetic_latching],
                [_meter_movement],
                [_balanced_armature],
            ],
            3: [[_("Armature (Short)")], [_meter_movement]],
            4: [[_dry_reed], [_mercury_wetted]],
            5: [[_("Armature (Balanced and Short)")], [_dry_reed]],
            6: [[_("Bimetal")]],
            8: [
                [_dry_reed],
                [_mercury_wetted],
                [_balanced_armature],
            ],
        },
        3: {
            1: [[_("Vacuum (Glass)")], [_("Vacuum (Ceramic)")]],
            2: [
                [_("Armature (Long and Short)")],
                [_mercury_wetted],
                [_magnetic_latching],
                [_mechanical_latching],
                [_balanced_armature],
                [_solenoid],
            ],
        },
        4: {
            1: [
                [_("Armature (Short)")],
                [_mechanical_latching],
                [_balanced_armature],
                [_solenoid],
            ]
        },
    }

    # Define private list class attributes.

    # Index is the technology ID (load type).
    _lst_technology: List[List[str]] = [
        [_("Resistive")],
        [_("Inductive")],
        [_("Lamp")],
    ]

    # Index is the contact form ID.
    _lst_contact_form: List[List[str]] = [
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
    _lst_contact_rating: List[List[str]] = [
        [_("Signal Current (low mV and mA)")],
        [_("0 - 5 Amp")],
        [_("5 - 20 Amp")],
        [_("20 - 600 Amp")],
    ]

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
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
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
        pub.subscribe(
            self.do_load_comboboxes,
            "changed_subcategory",
        )
        pub.subscribe(
            self._do_set_reliability_attributes,
            "succeed_get_reliability_attributes",
        )

    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the Relay RAMSTKComboBox()s.

        :param subcategory_id: the subcategory ID of the selected relay.
        :return: None
        :rtype: None
        """
        self.subcategory_id = subcategory_id

        self.__do_load_quality_combo()
        self.__do_load_type_combo()

        self.cmbLoadType.do_load_combo(self._lst_technology, signal="changed")
        self.cmbContactForm.do_load_combo(self._lst_contact_form, signal="changed")
        self.cmbContactRating.do_load_combo(self._lst_contact_rating, signal="changed")

        self._do_set_sensitive()

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

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected relay.

        :return: None
        :rtype: None
        """
        self.cmbType.set_sensitive(True)
        self.cmbLoadType.set_sensitive(False)
        self.cmbContactForm.set_sensitive(False)
        self.cmbContactRating.set_sensitive(False)
        self.cmbApplication.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.txtCycles.set_sensitive(False)

        if self._hazard_rate_method_id == 2 and self.subcategory_id == 1:
            self.cmbLoadType.set_sensitive(True)
            self.cmbContactForm.set_sensitive(True)
            self.cmbContactRating.set_sensitive(True)
            self.cmbApplication.set_sensitive(True)
            self.cmbConstruction.set_sensitive(True)
            self.txtCycles.set_sensitive(True)

            self.__do_load_application_combo()
            self.__do_load_construction_combo()

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
            |   4   | cmbContactRating |   5   | cmbApplication   |
            +-------+------------------+-------+------------------+

        :return: None
        :rtype: None
        """
        if index == 4:
            self.__do_load_application_combo()
        elif index == 5:
            self.__do_load_construction_combo()

    def __do_load_application_combo(self) -> None:
        """Load the selections in the Relay application RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        _contact_rating_id = int(self.cmbContactRating.get_active())
        try:
            _data = self._dic_application[_contact_rating_id]
        except KeyError:
            _data = []
        self.cmbApplication.do_load_combo(_data, signal="changed")

    def __do_load_construction_combo(self) -> None:
        """Load the selections in the Relay construction RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        _application_id = int(self.cmbApplication.get_active())
        _contact_rating_id = int(self.cmbContactRating.get_active())
        try:
            _data = self._dic_construction[_contact_rating_id][_application_id]
        except KeyError:
            _data = []
        self.cmbConstruction.do_load_combo(_data, signal="changed")

    def __do_load_quality_combo(self) -> None:
        """Load the selections in the Relay quality RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1:
            _data = [
                [_("Established Reliability")],
                ["MIL-SPEC"],
                [_("Lower")],
            ]
        else:
            try:
                _data = self._dic_quality[self.subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data, signal="changed")

    def __do_load_type_combo(self) -> None:
        """Load the selections in the Relay type RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        try:
            _data = self._dic_types[self.subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data, signal="changed")
