# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.components.semiconductor.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Semiconductor Input Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry, RAMSTKFixedPanel

# Key is subcategory ID; index is application ID.
SEMICONDUCTOR_APPLICATION_DICT = {
    2: [
        [_("Varactor, Voltage Control")],
        [_("Varactor, Multiplier")],
        [_("All Other Diodes")],
    ],
    3: [[_("Linear Amplification")], [_("Switching")]],
    4: [
        [_("Linear Amplification")],
        [_("Small Signal Switching")],
        [_("Non-Linear (2W < Pr < 5W)")],
        [_("Non-Linear (5W < Pr < 50W)")],
        [_("Non-Linear (50W < Pr < 250W)")],
        [_("Non-Linear (Pr > 250W)")],
    ],
    7: [["CW"], [_("Pulsed")]],
    8: [[_("All Lower Power and Pulsed")], ["CW"]],
    13: [["CW"], [_("Pulsed")]],
}
# Key is subcategory ID; index is matching ID.
SEMICONDUCTOR_MATCHING_DICT = {
    7: [[_("Input and Output")], [_("Input Only")], [_("None")]],
    8: [[_("Input and Output")], [_("Input Only")], [_("None")]],
}
SEMICONDUCTOR_QUALITY_DICT = {
    1: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")], [_("Plastic")]],
    2: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")], [_("Plastic")]],
    3: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")], [_("Plastic")]],
    4: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")], [_("Plastic")]],
    5: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")], [_("Plastic")]],
    6: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")]],
    7: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")]],
    8: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")]],
    9: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")]],
    10: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")], [_("Plastic")]],
    11: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")], [_("Plastic")]],
    12: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")], [_("Plastic")]],
    13: [
        [_("Hermetic Package")],
        [_("Nonhermetic with Facet Coating")],
        [_("Nonhermetic without Facet Coating")],
    ],
}
# Key is subcategory ID; index is type ID.
SEMICONDUCTOR_TYPE_DICT = {
    1: [
        [_("General Purpose Analog")],
        [_("Switching")],
        [_("Power Rectifier, Fast Recovery")],
        [_("Power Rectifier/Schottky Power Diode")],
        [_("Power Rectifier with High Voltage Stacks")],
        [_("Transient Suppressor/Varistor")],
        [_("Current Regulator")],
        [_("Voltage Regulator and Voltage Reference (Avalanche and Zener)")],
    ],
    2: [
        [_("Si IMPATT (<35 GHz)")],
        [_("Gunn/Bulk Effect")],
        [_("Tunnel and Back (Including Mixers, Detectors)")],
        [_("PIN")],
        [
            _(
                "Schottky Barrier (Including Detectors) and Point Contact "
                "(200 MHz < Frequency < 35MHz)"
            )
        ],
        [_("Varactor and Step Recovery")],
    ],
    3: [["NPN/PNP (f < 200MHz)"], [_("Power NPN/PNP (f < 200 MHz)")]],
    4: [["MOSFET"], ["JFET"]],
    7: [[_("Gold Metallization")], [_("Aluminum Metallization")]],
    8: [["GaAs FET (P < 100mW)"], ["GaAs FET (P > 100mW)"]],
    9: [["MOSFET"], ["JFET"]],
    11: [
        [_("Photo-Transistor")],
        [_("Photo-Diode")],
        [_("Photodiode Output, Single Device")],
        [_("Phototransistor Output, Single Device")],
        [_("Photodarlington Output, Single Device")],
        [_("Light Sensitive Resistor, Single Device")],
        [_("Photodiode Output, Dual Device")],
        [_("Phototransistor Output, Dual Device")],
        [_("Photodarlington Output, Dual Device")],
        [_("Light Sensitive Resistor, Dual Device")],
        [_("Infrared Light Emitting Diode (IRLED)")],
        [_("Light Emitting Diode")],
    ],
    12: [[_("Segment Display")], [_("Diode Array Display")]],
    13: [["GaAs/Al GaAs"], ["In GaAs/In GaAsP"]],
}
SEMICONDUCTOR_PACKAGES_LIST = [
    ["TO-1"],
    ["TO-3"],
    ["TO-5"],
    ["TO-8"],
    ["TO-9"],
    ["TO-12"],
    ["TO-18"],
    ["TO-28"],
    ["TO-33"],
    ["TO-39"],
    ["TO-41"],
    ["TO-44"],
    ["TO-46"],
    ["TO-52"],
    ["TO-53"],
    ["TO-57"],
    ["TO-59"],
    ["TO-60"],
    ["TO-61"],
    ["TO-63"],
    ["TO-66"],
    ["TO-71"],
    ["TO-72"],
    ["TO-83"],
    ["TO-89"],
    ["TO-92"],
    ["TO-94"],
    ["TO-99"],
    ["TO-126"],
    ["TO-127"],
    ["TO-204"],
    ["TO-204AA"],
    ["TO-205AD"],
    ["TO-205AF"],
    ["TO-220"],
    ["DO-4"],
    ["DO-5"],
    ["DO-7"],
    ["DO-8"],
    ["DO-9"],
    ["DO-13"],
    ["DO-14"],
    ["DO-29"],
    ["DO-35"],
    ["DO-41"],
    ["DO-45"],
    ["DO-204MB"],
    ["DO-205AB"],
    ["PA-42A,B"],
    ["PD-36C"],
    ["PD-50"],
    ["PD-77"],
    ["PD-180"],
    ["PD-319"],
    ["PD-262"],
    ["PD-975"],
    ["PD-280"],
    ["PD-216"],
    ["PT-2G"],
    ["PT-2G"],
    ["PT-6B"],
    ["PH-13"],
    ["PH-16"],
    ["PH-56"],
    ["PY-58"],
    ["PY-373"],
]


class SemiconductorDesignElectricInputPanel(RAMSTKFixedPanel):
    """Display Semiconductor assessment input attribute data.

    The Semiconductor assessment input view displays all the assessment inputs
    for the selected semiconductor.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Semiconductor assessment input view
    are:

    :cvar dict _dic_applications: dictionary of semiconductor applications.
        Key is semiconductor subcategory ID; values are lists of applications.
    :cvar dict _dic_matchings: dictionary of network matching types.  Key is
        semiconductor subcategory ID; values are lists of network matching
        types.
    :cvar dict _dic_quality: dictionary of semiconductor quality levels.  Key
        is semiconductor subcategory ID; values are lists of quality levels.
    :cvar dict _dic_types: dictionary of semiconductor types.  Key is the
        semiconductor subcategory ID; values are lists of semiconductor types.

    :ivar cmbApplication: select and display the application of the
        semiconductor.
    :ivar cmbConstruction: select and display the construction of the
        semiconductor.
    :ivar cmbMatching: select and display the matching arrangement for the
        semiconductor.
    :ivar cmbPackage: select and display the type of package for the
        semiconductor.
    :ivar cmbType: select and display the type of semiconductor.
    :ivar txtFrequencyOperating: enter and display the operating frequency of
        the semiconductor.
    :ivar txtNElements: enter and display the number of elements in the
        optoelectronic display.
    :ivar txtThetaJC: enter and display the junction-case thermal resistance.
    """

    # Define private dict class attributes.
    _dic_quality: Dict[int, List[List[str]]] = SEMICONDUCTOR_QUALITY_DICT
    _dic_types: Dict[int, List[List[str]]] = SEMICONDUCTOR_TYPE_DICT
    _dic_applications: Dict[int, List[List[str]]] = SEMICONDUCTOR_APPLICATION_DICT
    _dic_matchings: Dict[int, List[List[str]]] = SEMICONDUCTOR_MATCHING_DICT

    # Define private list class attributes.
    _lst_packages: List[List[str]] = SEMICONDUCTOR_PACKAGES_LIST

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Semiconductor Design Inputs")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize instance of the Semiconductor assessment input view."""
        super().__init__()

        # Initialize widgets.
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbMatching: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbPackage: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()
        self.txtFrequencyOperating: RAMSTKEntry = RAMSTKEntry()
        self.txtNElements: RAMSTKEntry = RAMSTKEntry()
        self.txtThetaJC: RAMSTKEntry = RAMSTKEntry()

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
                "succeed_get_reliability_attributes": self._set_reliability_attributes,
            }
        )

    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the Semiconductor RAMSTKComboBox()s.

        :param subcategory_id: the subcategory ID of the selected semiconductor.
        :return: None
        :rtype: None
        """
        self.subcategory_id = subcategory_id

        self.cmbApplication.do_load_combo(
            self._dic_applications.get(self.subcategory_id, []),
            signal="changed",
        )
        self.cmbConstruction.do_load_combo(
            [
                [_("Metallurgically Bonded")],
                [_("Non-Metallurgically Bonded and Spring Loaded Contacts")],
            ],
            signal="changed",
        )
        self.cmbMatching.do_load_combo(
            self._dic_matchings.get(self.subcategory_id, []),
            signal="changed",
        )
        self.cmbPackage.do_load_combo(
            self._lst_packages,
            signal="changed",
        )
        self.cmbQuality.do_load_combo(
            self._get_quality_list(),
            signal="changed",
        )
        self.cmbType.do_load_combo(
            self._get_type_list,
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
                    "tooltip": _("The quality level of the semiconductor."),
                },
                _("Quality Level:"),
                "gint",
            ],
            "package_id": [
                30,
                self.cmbPackage,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The package type for the semiconductor."),
                },
                _("Package:"),
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
                    "tooltip": _("The type of semiconductor."),
                },
                _("Type:"),
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
                    "tooltip": _("The application of the semiconductor."),
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
                    "tooltip": _("The method of construction of the semiconductor."),
                },
                _("Construction:"),
                "gint",
            ],
            "matching_id": [
                6,
                self.cmbMatching,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The matching network of the semiconductor."),
                },
                _("Matching Network:"),
                "gint",
            ],
            "frequency_operating": [
                2,
                self.txtFrequencyOperating,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _("The operating frequency of the semiconductor."),
                },
                _("Operating Frequency (GHz):"),
                "gfloat",
            ],
            "n_elements": [
                25,
                self.txtNElements,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _(
                        "The number of characters in the optoelectronic display."
                    ),
                },
                _("Number of Characters:"),
                "gint",
            ],
            "theta_jc": [
                47,
                self.txtThetaJC,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _(
                        "The junction-case thermal resistance of the semiconductor."
                    ),
                },
                "\u03B8<sub>JC</sub>:",
                "gfloat",
            ],
        }

    def _get_quality_list(self) -> List[List[str]]:
        """Return the list of semiconductor quality levels.

        :return: list of semiconductor quality levels.
        :rtype: list
        """
        if self._hazard_rate_method_id == 1:
            return self._get_part_count_quality_list()
        return self._dic_quality.get(self.subcategory_id, [])

    def _get_part_count_quality_list(self) -> List[List[str]]:
        """Return the quality list to load into the quality level RAMSTKComboBox().

        :return: list of semiconductor quality levels.
        :rtype: list
        """
        if self.subcategory_id == 13:
            return [
                [_("Hermetic Package")],
                [_("Nonhermetic with Facet Coating")],
                [_("Nonhermetic without Facet Coating")],
            ]
        else:
            return [
                ["JANTXV"],
                ["JANTX"],
                ["JAN"],
                [_("Lower")],
                [_("Plastic")],
            ]

    def _get_type_list(self) -> List[List[str]]:
        """Return the type list to load into the type RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        _default_type_list = [
            [_("Photodetector")],
            [_("Opto-Isolator")],
            [_("Emitter")],
        ]
        return (
            _default_type_list
            if self._hazard_rate_method_id == 1 and self.subcategory_id == 11
            else self._dic_types.get(self.subcategory_id, [[""]])
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
        super.set_widget_sensitivity([self.cmbQuality])
        self.cmbQuality.do_update(
            self._quality_id,
            signal="changed",
        )

    def _set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected semiconductor.

        :return: None
        :rtype: None
        """
        # Define all widgets that could be sensitive
        _all_widgets = [
            self.cmbApplication,
            self.cmbConstruction,
            self.cmbMatching,
            self.cmbPackage,
            self.cmbType,
            self.txtFrequencyOperating,
            self.txtNElements,
            self.txtThetaJC,
        ]

        # Reset all widgets to be insensitive.
        super.set_widget_sensitivity(
            _all_widgets,
            False,
        )

        # Set cmbPackage and txtThetaJC sensitive if hazard_rate_method_id is 2
        if self._hazard_rate_method_id == 2:
            self.cmbPackage.set_sensitive(True)
            self.txtThetaJC.set_sensitive(True)

        # Define a sensitivity map for different widgets based on hazard rate method
        # and subcategory
        _sensitivity_map = {
            1: {
                1: [self.cmbType],
                2: [self.cmbType],
                3: [self.cmbType],
                8: [self.cmbType],
                11: [self.cmbType],
                13: [self.cmbType],
            },
            2: {
                1: [
                    self.cmbConstruction,
                    self.cmbType,
                ],
                2: [
                    self.cmbApplication,
                    self.cmbType,
                ],
                3: [self.cmbApplication],
                4: [
                    self.cmbApplication,
                    self.cmbType,
                ],
                7: [
                    self.cmbApplication,
                    self.cmbMatching,
                    self.cmbType,
                    self.txtNElements,
                    self.txtFrequencyOperating,
                ],
                8: [
                    self.cmbApplication,
                    self.cmbMatching,
                    self.txtNElements,
                    self.txtFrequencyOperating,
                ],
                9: [self.cmbType],
                11: [self.cmbType],
                12: [
                    self.cmbConstruction,
                    self.cmbType,
                ],
                13: [
                    self.cmbApplication,
                    self.cmbType,
                ],
            },
        }

        super().set_widget_sensitivity(
            _sensitivity_map.get(self._hazard_rate_method_id, {}).get(
                self.subcategory_id, []
            )
        )
