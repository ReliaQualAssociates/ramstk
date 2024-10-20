# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.components.integrated_circuit.py is part of
#       the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Integrated Circuit Input Panel."""


# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry, RAMSTKFixedPanel

IC_TECHNOLOGY_DICT: Dict[int, List[List[str]]] = {
    1: [["MOS"], [_("Bipolar")]],
    2: [
        ["TTL"],
        ["ASTTL"],
        ["CML"],
        ["HTTL"],
        ["FTTL"],
        ["DTL"],
        ["ECL"],
        ["ALSTTL"],
        ["FLTTL"],
        ["STTL"],
        ["BiCMOS"],
        ["LSTTL"],
        ["III"],
        ["IIIL"],
        ["ISL"],
    ],
    3: [["MOS"], [_("Bipolar")]],
    4: [["MOS"], [_("Bipolar")]],
    5: [["MOS"], [_("Bipolar")]],
    6: [["MOS"], [_("Bipolar")]],
    7: [["MOS"], [_("Bipolar")]],
    8: [["MOS"], [_("Bipolar")]],
    9: [["MMIC"], [_("Digital")]],
}
IC_TYPE_DICT = {
    9: [["MMIC"], [_("Digital")]],
    10: [[_("Logic and Custom")], [_("Gate Array")]],
}


class ICDesignElectricInputPanel(RAMSTKFixedPanel):
    """Display IC assessment input attribute data in the RAMSTK Work Book.

    The Integrated Circuit assessment input view displays all the assessment
    inputs for the selected integrated circuit.  This includes, currently,
    inputs for MIL-HDBK-217FN2.  The attributes of an integrated circuit
    assessment input view are:

    :cvar dict _dic_technology: dictionary of integrated circuit package
        technologies.  Key is integrated circuit subcategory ID; values are
        lists of technologies.

    :ivar cmbApplication: select and display the application of the integrated
        circuit.
    :ivar cmbConstruction: select and display the construction of the
        integrated circuit.
    :ivar cmbECC: select and display the error correction code used by the
        EEPROM.
    :ivar cmbManufacturing: select and display the manufacturing approach for
        the integrated circuit.
    :ivar cmbPackage: select and display the package type of the integrated
        circuit.
    :ivar cmbTechnology: select and display the technology used in the
        integrated circuit.
    :ivar cmbType: select and display the type of the integrated circuit.

    :ivar txtArea: enter and display the die area of the integrated circuit.
    :ivar txtFeatureSize: enter and display the feature size (in microns) of
        the VLSI.
    :ivar txtNActivePins: enter and display the number of active pins.
    :ivar txtNCycles: enter and display the number of programming cycles over
        the life of the PROM.
    :ivar txtNElements: enter and display the number of elements (transistors,
        gates, etc.) in the integrated circuit.
    :ivar txtOperatingLife: enter and display the operating life of the
        integrated circuit.
    :ivar txtThetaJC: enter and display the junction - case thermal resistance
        of the integrated circuit.
    :ivar txtVoltageESD: enter and display the ESD threshold voltage of the
        VLSI.
    :ivar txtYearsInProduction: enter and display the number of years the
        integrated circuit type has been in production.
    """

    # Define private dict class attributes.
    _dic_technology: Dict[int, List[List[str]]] = IC_TECHNOLOGY_DICT
    _dic_types: Dict[int, List[List[str]]] = IC_TYPE_DICT

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "hardware_id"
    _select_msg = "succeed_get_design_electric_attributes"
    _tag = "design_electric"
    _title = _("Integrated Circuit Design Inputs")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the IC assessment input view."""
        super().__init__()

        # Initialize widgets.
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbECC: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbManufacturing: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbPackage: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbTechnology: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()
        self.txtArea: RAMSTKEntry = RAMSTKEntry()
        self.txtFeatureSize: RAMSTKEntry = RAMSTKEntry()
        self.txtNActivePins: RAMSTKEntry = RAMSTKEntry()
        self.txtNCycles: RAMSTKEntry = RAMSTKEntry()
        self.txtNElements: RAMSTKEntry = RAMSTKEntry()
        self.txtOperatingLife: RAMSTKEntry = RAMSTKEntry()
        self.txtThetaJC: RAMSTKEntry = RAMSTKEntry()
        self.txtVoltageESD: RAMSTKEntry = RAMSTKEntry()
        self.txtYearsInProduction: RAMSTKEntry = RAMSTKEntry()

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

    # pylint: disable=unused-argument
    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the integrated circuit RAMSTKComboBox()s.

        :param subcategory_id: the subcategory ID of the selected IC. This is unused in
            this method but required because this method is a PyPubSub listener.
        :return: None
        :rtype: None
        """
        self.subcategory_id = subcategory_id

        self.cmbQuality.do_load_combo(
            [
                [_("Class S")],
                [_("Class B")],
                [_("Class B-1")],
            ],
            signal="changed",
        )
        self.cmbConstruction.do_load_combo(
            [
                ["FLOTOX"],
                [_("Textured Poly")],
            ],
            signal="changed",
        )
        self.cmbECC.do_load_combo(
            [
                [_("No on-chip ECC")],
                [_("On-chip Hamming code")],
                [_("Two-Needs-One redundant cell approach")],
            ],
            signal="changed",
        )
        self.cmbManufacturing.do_load_combo(
            [
                ["QML or QPL"],
                ["Non-QML or non-QPL"],
            ],
            signal="changed",
        )
        self.cmbPackage.do_load_combo(
            [
                [_("Hermetic DIP w/ Solder or Weld Seal")],
                [_("Hermetic Pin Grid Array (PGA)")],
                [_("Hermetic SMT (Leaded and Nonleaded)")],
                [_("DIP w/ Glass Seal")],
                [_("Flatpacks w/ Axial Leads")],
                ["Can"],
                [_("Nonhermetic DIP")],
                [_("Nonhermetic Pin Grid Array (PGA)")],
                [_("Nonhermetic SMT")],
            ],
            signal="changed",
        )
        self.cmbTechnology.do_load_combo(
            self._get_technology_list(),
            signal="changed",
        )
        self.cmbType.do_load_combo(
            self._dic_types.get(self.subcategory_id, []),
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
                    "tooltip": _("The quality level of the integrated circuit."),
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
                    "tooltip": _("The type of package housing the integrated circuit."),
                },
                _("Package:"),
                "gint",
            ],
            "area": [
                3,
                self.txtArea,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _(
                        "The die area (in mil<sup>2</sup>) of the integrated circuit."
                    ),
                    "width": 125,
                },
                _("Die Area:"),
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
                        "The number of active elements in the integrated circuit."
                    ),
                    "width": 125,
                },
                _("N Elements:"),
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
                    "tooltip": _("The junction to case thermal resistance."),
                    "width": 125,
                },
                _("\u0398<sub>JC</sub>:"),
                "gfloat",
            ],
            "n_active_pins": [
                22,
                self.txtNActivePins,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _(
                        "The number of active pins on the integrated circuit."
                    ),
                    "width": 125,
                },
                _("Active Pins:"),
                "gint",
            ],
            "technology_id": [
                37,
                self.cmbTechnology,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _(
                        "The technology used to construct the integrated circuit."
                    ),
                },
                _("Technology:"),
                "gint",
            ],
            "years_in_production": [
                55,
                self.txtYearsInProduction,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                2,
                {
                    "tooltip": _(
                        "The number of years the generic device type has been in "
                        "production."
                    ),
                    "width": 125,
                },
                _("Years in Production:"),
                "gfloat",
            ],
            "construction_id": [
                6,
                self.cmbConstruction,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _(
                        "The method of construction of the integrated circuit."
                    ),
                },
                _("Construction:"),
                "gint",
            ],
            "n_cycles": [
                24,
                self.txtNCycles,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _(
                        "The total number of programming cycles over the EEPROM life."
                    ),
                    "width": 125,
                },
                _("Programming Cycles:"),
                "gint",
            ],
            "operating_life": [
                28,
                self.txtOperatingLife,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _("The system lifetime operating hours."),
                    "width": 125,
                },
                _("Operating Life:"),
                "gfloat",
            ],
            "family_id": [
                15,
                self.cmbECC,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The error correction code used by the EEPROM."),
                },
                _("Error Correction Code:"),
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
                    "tooltip": _("The application of the integrated circuit."),
                },
                _("Application:"),
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
                    "tooltip": _("The type of GaAs or VLSI device."),
                },
                _("Device Type:"),
                "gint",
            ],
            "feature_size": [
                16,
                self.txtFeatureSize,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _("The feature size (in microns) of the VLSI device."),
                    "width": 125,
                },
                _("Feature Size:"),
                "gfloat",
            ],
            "manufacturing_id": [
                20,
                self.cmbManufacturing,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The manufacturing process for the VLSI device."),
                },
                _("Manufacturing Process:"),
                "gint",
            ],
            "voltage_esd": [
                51,
                self.txtVoltageESD,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _(
                        "The ESD susceptibility threshold voltage of the VLSI device."
                    ),
                    "width": 125,
                },
                _("ESD Threshold Voltage:"),
                "gfloat",
            ],
        }

    def _do_load_application_combo(self, attributes: Dict[str, Any]) -> None:
        """Load the IC application RAMSTKComboBox().

        :param attributes: the attributes dict for the selected integrated circuit.
        :return: None
        """
        self.cmbApplication.do_load_combo(
            self._get_application_list(attributes["construction_id"]),
            signal="changed",
        )

    @staticmethod
    def _get_application_list(construction_id: int) -> List[List[str]]:
        """Return the list of IC applications.

        :param construction_id: ID of the IC construction method.
        :return: list of IC applications.
        :rtype: list
        """
        return (
            [
                [_("Low Noise and Low Power (\u2264 100mW)")],
                [_("Driver and High Power (> 100mW)")],
                [_("Unknown")],
            ]
            if construction_id == 1
            else [[_("All digital devices")]]
        )

    def _get_part_count_technology_list(self) -> List[List[str]]:
        """Return technology list based on the subcategory for part count method.

        :return: list of IC technologies.
        :rtype: list
        """
        if self.subcategory_id == 9:
            return [
                ["MMIC"],
                [_("Digital")],
            ]
        return [
            ["Bipolar"],
            ["MOS"],
        ]

    def _get_technology_list(self) -> List[List[str]]:
        """Return the list of IC technologies.

        :return: list of IC technologies.
        :rtype: list
        """
        try:
            if self._hazard_rate_method_id == 1:
                return self._get_part_count_technology_list()
            return self._dic_technology.get(self.subcategory_id, [])
        except KeyError:
            return []

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
        """Set widget sensitivity as needed for the selected IC.

        :return: None
        :rtype: None
        """
        # Reset all widgets to be insensitive.
        super().set_widget_sensitivity(
            [
                self.cmbApplication,
                self.cmbConstruction,
                self.cmbECC,
                self.cmbManufacturing,
                self.cmbPackage,
                self.cmbTechnology,
                self.cmbType,
                self.txtArea,
                self.txtFeatureSize,
                self.txtNActivePins,
                self.txtNCycles,
                self.txtNElements,
                self.txtOperatingLife,
                self.txtThetaJC,
                self.txtVoltageESD,
                self.txtYearsInProduction,
            ],
            False,
        )

        # Define sensitivity map for each subcategory
        _sensitivity_map = {
            1: [self.txtNElements],  # Linear IC
            2: [
                self.txtNElements,
                self.txtNActivePins,
                self.txtYearsInProduction,
            ],  # Logic IC
            3: [
                self.cmbTechnology,
                self.txtNElements,
            ],  # PAL/PLA
            4: [
                self.cmbTechnology,
                self.txtNElements,
                self.txtNActivePins,
                self.txtYearsInProduction,
            ],  # Microprocessor
            5: [
                self.cmbTechnology,
                self.txtNElements,
            ],  # ROM
            6: [
                self.cmbTechnology,
                self.cmbECC,
                self.cmbConstruction,
                self.txtNElements,
                self.txtNActivePins,
                self.txtNCycles,
                self.txtOperatingLife,
            ],  # EEPROM
            7: [self.txtNElements],  # DRAM
            8: [self.txtNElements],  # SRAM
            9: [
                self.cmbTechnology,
                self.txtNElements,
                self.txtNActivePins,
                self.txtYearsInProduction,
            ],  # GaAs IC
            10: [
                self.txtNElements,
                self.txtNActivePins,
                self.txtYearsInProduction,
            ],  # VHSIC/VLSI
        }

        # Set widget sensitivity based on subcategory and hazard rate method
        super().set_widget_sensitivity(_sensitivity_map.get(self.subcategory_id, []))

        # For Part Stress, add extra sensitivity.
        if self._hazard_rate_method_id == 2:
            super().set_widget_sensitivity(
                [
                    self.cmbPackage,
                    self.txtThetaJC,
                    self.txtNElements,
                ]
            )
