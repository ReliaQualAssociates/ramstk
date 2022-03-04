# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.components.resistor.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Resistor Input Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry, RAMSTKFixedPanel


class ResistorDesignElectricInputPanel(RAMSTKFixedPanel):
    """Display Resistor assessment input attribute data.

    The Resistor assessment input view displays all the assessment inputs for
    the selected resistor.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Resistor assessment input view are:

    :cvar dict _dic_specifications: dictionary of resistor MIL-SPECs.  Key is
        resistor subcategory ID; values are lists of specifications.
    :cvar dict _dic_styles: dictionary of resistor styles defined in the
        MIL-SPECs.  Key is resistor subcategory ID; values are lists of styles.

    :ivar cmbSpecification: select and display the governing specification of
        the resistor.
    :ivar cmbType: select and display the type of thermistor.
    :ivar cmbConstruction: select and display the method of construction of the
        resistor.
    :ivar txtResistance: enter and display the resistance of the resistor.
    :ivar txtNElements: enter and display the number of active resistors in a
        resistor network or the number of potentiometers taps.
    """

    # Define private dict class attributes.
    _dic_quality: Dict[int, List[List[str]]] = {
        1: [["S"], ["R"], ["P"], ["M"], ["MIL-R-11"], [_("Lower")]],
        2: [
            ["S"],
            ["R"],
            ["P"],
            ["M"],
            ["MIL-R-10509"],
            ["MIL-R-22684"],
            [_("Lower")],
        ],
        3: [["MIL-SPEC"], [_("Lower")]],
        4: [["MIL-SPEC"], [_("Lower")]],
        5: [["S"], ["R"], ["P"], ["M"], ["MIL-R-93"], [_("Lower")]],
        6: [["S"], ["R"], ["P"], ["M"], ["MIL-R-26"], [_("Lower")]],
        7: [["S"], ["R"], ["P"], ["M"], ["MIL-R-18546"], [_("Lower")]],
        8: [["MIL-SPEC"], [_("Lower")]],
        9: [["S"], ["R"], ["P"], ["M"], ["MIL-R-27208"], [_("Lower")]],
        10: [["MIL-SPEC"], [_("Lower")]],
        11: [["MIL-SPEC"], [_("Lower")]],
        12: [["MIL-SPEC"], [_("Lower")]],
        13: [["S"], ["R"], ["P"], ["M"], ["MIL-R-22097"], [_("Lower")]],
        14: [["MIL-SPEC"], [_("Lower")]],
        15: [["MIL-SPEC"], [_("Lower")]],
    }
    # Key is subcategory ID; index is specification ID.
    _dic_specifications: Dict[int, List[List[str]]] = {
        2: [
            ["MIL-R-10509"],
            ["MIL-R-22684"],
            ["MIL-R-39017"],
            ["MIL-R-55182"],
        ],
        6: [["MIL-R-26"], ["MIL-R-39007"]],
        7: [["MIL-R-18546"], ["MIL-R-39009"]],
        15: [["MIL-R-23285"], ["MIL-R-39023"]],
    }
    # Key is subcategory ID, index is type ID.
    _dic_types: Dict[int, List[List[str]]] = {
        1: [["RCR"], ["RC"]],
        2: [["RLR"], ["RL"], ["RNR"], ["RN"]],
        5: [["RBR"], ["RB"]],
        6: [["RWR"], ["RW"]],
        7: [["RER"], ["RE"]],
        9: [["RTR"], ["RT"]],
        11: [["RA"], ["RK"]],
        13: [["RJR"], ["RJ"]],
        15: [["RO"], ["RVC"]],
    }
    # First key is subcategory ID; second key is specification ID.
    # Index is style ID.
    _dic_styles: Dict[int, Dict[int, List[List[str]]]] = {
        6: {
            1: [
                ["RWR 71"],
                ["RWR 74"],
                ["RWR 78"],
                ["RWR 80"],
                ["RWR 81"],
                ["RWR 82"],
                ["RWR 84"],
                ["RWR 89"],
            ],
            2: [
                ["RW 10"],
                ["RW 11"],
                ["RW 12"],
                ["RW 13"],
                ["RW 14"],
                ["RW 15"],
                ["RW 16"],
                ["RW 20"],
                ["RW 21 "],
                ["RW 22"],
                ["RW 23"],
                ["RW 24"],
                ["RW 29"],
                ["RW 30"],
                ["RW 31"],
                ["RW 32"],
                ["RW 33"],
                ["RW 34"],
                ["RW 35"],
                ["RW 36"],
                ["RW 37"],
                ["RW 38"],
                ["RW 39"],
                ["RW 47"],
                ["RW 55"],
                ["RW 56"],
                ["RW 67"],
                ["RW 68"],
                ["RW 69"],
                ["RW 70"],
                ["RW 74"],
                ["RW 78"],
                ["RW 79"],
                ["RW 80"],
                ["RW 81"],
            ],
        },
        7: {
            1: [
                ["RE 60/RER 60"],
                ["RE 65/RER 65"],
                ["RE 70/RER 70"],
                ["RE 75/RER 75"],
                ["RE 77"],
                ["RE 80"],
            ],
            2: [
                ["RE 60/RER40"],
                ["RE 65/RER 45"],
                ["RE 70/ RER 50"],
                ["RE 75/RER 55"],
                ["RE 77"],
                ["RE 80"],
            ],
        },
    }
    # Key is subcategory ID; index is construction ID.
    _dic_construction: Dict[int, List[List[str]]] = {
        10: [
            ["RR0900A2A9J103"],
            ["RR0900A3A9J103"],
            ["RR0900A4A9J103"],
            ["RR0900A5A9J103"],
        ],
        12: [[_("Enclosed")], [_("Unenclosed")]],
    }

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Resistor Design Inputs")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Resistor assessment input view."""
        super().__init__()

        # Initialize widgets.
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbSpecification: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbStyle: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()
        self.txtNElements: RAMSTKEntry = RAMSTKEntry()
        self.txtResistance: RAMSTKEntry = RAMSTKEntry()

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
                    "tooltip": _("The quality level of the resistor."),
                },
                _("Quality Level:"),
                "gint",
            ],
            "resistance": [
                35,
                self.txtResistance,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The resistance (in \u03A9) of the resistor."),
                },
                _("Resistance (\u03A9):"),
                "gfloat",
            ],
            "specification_id": [
                36,
                self.cmbSpecification,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The governing specification for the resistor."),
                },
                _("Specification:"),
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
                    "tooltip": _("The type of thermistor."),
                },
                _("Type:"),
                "gint",
            ],
            "family_id": [
                15,
                self.cmbStyle,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The style of resistor."),
                },
                _("Style:"),
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
                    "tooltip": _("The method of construction of the resistor."),
                },
                _("Construction:"),
                "gint",
            ],
            "n_elements": [
                2,
                self.txtNElements,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _(
                        "The number of active resistors in a resistor network or the "
                        "number of potentiometer taps."
                    ),
                },
                _("Number of Elements:"),
                "gint",
            ],
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.category_id: int = 0
        self.subcategory_id: int = 0

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

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
        """Load the Resistor RKTComboBox()s.

        :param subcategory_id: the subcategory ID of the selected capacitor.
            This is unused in this method but required because this method is a
            PyPubSub listener.
        :return: None
        :rtype: None
        """
        self.subcategory_id = subcategory_id

        self.__do_load_quality_combo()
        self.__do_load_specification_combo()
        self.__do_load_type_combo()
        self.__do_load_style_combo()
        self.__do_load_construction_combo()

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
        """Set widget sensitivity as needed for the selected resistor.

        :param attributes: the dict of design electric attributes.
        :return: None
        :rtype: None
        """
        self.cmbConstruction.set_sensitive(False)
        self.cmbSpecification.set_sensitive(False)
        self.cmbStyle.set_sensitive(False)
        self.cmbType.set_sensitive(False)
        self.txtNElements.set_sensitive(False)

        if self._hazard_rate_method_id == 2:
            self.txtResistance.set_sensitive(True)
        else:
            self.txtResistance.set_sensitive(False)

        self.__do_set_construction_combo_sensitive()
        self.__do_set_elements_entry_sensitive()
        self.__do_set_specification_combo_sensitive()
        self.__do_set_style_combo_sensitive()
        self.__do_set_type_combo_sensitive()

    def __do_load_construction_combo(self) -> None:
        """Load the Resistor construction RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        try:
            _data = self._dic_construction[self.subcategory_id]
        except KeyError:
            _data = []
        self.cmbConstruction.do_load_combo(
            _data,
            signal="changed",
        )

    def __do_load_quality_combo(self) -> None:
        """Load the Resistor quality RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        try:
            if self._hazard_rate_method_id == 1:
                _quality: List[List[str]] = [
                    ["S"],
                    ["R"],
                    ["P"],
                    ["M"],
                    ["MIL-SPEC"],
                    [_("Lower")],
                ]
            else:
                _quality = self._dic_quality[self.subcategory_id]
        except KeyError:
            _quality = [[""]]
        self.cmbQuality.do_load_combo(
            entries=_quality,
            signal="changed",
        )

    def __do_load_specification_combo(self) -> None:
        """Load the Resistor specification RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        try:
            _data = self._dic_specifications[self.subcategory_id]
        except KeyError:
            _data = []
        self.cmbSpecification.do_load_combo(
            _data,
            signal="changed",
        )

    def __do_load_style_combo(self) -> None:
        """Load the Resistor style RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        _specification_id = int(self.cmbSpecification.get_active())
        try:
            _styles: List[List[str]] = self._dic_styles[self.subcategory_id][
                _specification_id
            ]
        except (KeyError, IndexError):
            _styles = [[""]]
        self.cmbStyle.do_load_combo(
            entries=_styles,
            signal="changed",
        )

    def __do_load_type_combo(self) -> None:
        """Load the Resistor (thermistor) type RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        try:
            if self._hazard_rate_method_id == 1:
                _types: List[Any] = self._dic_types[self.subcategory_id]
            else:
                _types = [[_("Bead")], [_("Disk")], [_("Rod")]]
        except KeyError:
            _types = []
        self.cmbType.do_load_combo(
            entries=_types,
            signal="changed",
        )

    def __do_set_construction_combo_sensitive(self) -> None:
        """Set the Resistor construction RAMSTKComboBox() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2 and self.subcategory_id in [
            10,
            12,
        ]:
            self.cmbConstruction.set_sensitive(True)

    def __do_set_elements_entry_sensitive(self) -> None:
        """Set Resistor number of elements RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2 and self.subcategory_id in [
            4,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
        ]:
            self.txtNElements.set_sensitive(True)

    def __do_set_specification_combo_sensitive(self) -> None:
        """Set the Resistor specification RAMSTKComboBox() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2 and self.subcategory_id in [
            2,
            6,
            7,
            15,
        ]:
            self.cmbSpecification.set_sensitive(True)

    def __do_set_style_combo_sensitive(self) -> None:
        """Set the Resistor style RAMSTKComboBox() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2 and self.subcategory_id in [6, 7]:
            self.cmbStyle.set_sensitive(True)

    def __do_set_type_combo_sensitive(self) -> None:
        """Set the Resistor type RAMSTKComboBox() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1 and self.subcategory_id in [
            1,
            2,
            5,
            6,
            7,
            9,
            11,
            13,
            15,
        ]:
            self.cmbType.set_sensitive(True)
        elif self._hazard_rate_method_id == 2 and self.subcategory_id == 8:
            self.cmbType.set_sensitive(True)
