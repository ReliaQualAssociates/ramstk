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

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry, RAMSTKFixedPanel


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
    _dic_technology: Dict[int, List[Any]] = {
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

    _dic_types: Dict[int, List[Any]] = {
        9: [["MMIC"], [_("Digital")]],
        10: [[_("Logic and Custom")], [_("Gate Array")]],
    }

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "selected_hardware"
    _tag = "design_electric"
    _title = _("Electronic Component Inputs")

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
        self.dic_attribute_index_map = {
            32: ["quality_id", "integer"],
            2: ["application_id", "integer"],
            3: ["area", "float"],
            6: ["construction_id", "integer"],
            15: ["family_id", "integer"],
            16: ["feature_size", "float"],
            20: ["manufacturing_id", "integer"],
            22: ["n_active_pins", "integer"],
            24: ["n_cycles", "integer"],
            25: ["n_elements", "integer"],
            28: ["operating_life", "float"],
            30: ["package_id", "integer"],
            37: ["technology_id", "integer"],
            47: ["theta_jc", "float"],
            48: ["type_id", "integer"],
            51: ["voltage_esd", "float"],
            55: ["years_in_production", "float"],
        }
        self.dic_attribute_widget_map = {
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
            ],
            "package_id": [
                30,
                self.cmbPackage,
                "changed",
                super().on_changed_combo,
                "wvw_editing_design_electric",
                0,
                {
                    "tooltip": _("The type of package housing the integrated circuit."),
                },
                _("Package:"),
            ],
            "area": [
                3,
                self.txtArea,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                0.0,
                {
                    "tooltip": _(
                        "The die area (in mil<sup>2</sup>) of the integrated circuit."
                    ),
                    "width": 125,
                },
                _("Die Area:"),
            ],
            "n_elements": [
                25,
                self.txtNElements,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                0,
                {
                    "tooltip": _(
                        "The number of active elements in the integrated circuit."
                    ),
                    "width": 125,
                },
                _("N Elements:"),
            ],
            "theta_jc": [
                47,
                self.txtThetaJC,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                0.0,
                {
                    "tooltip": _("The junction to case thermal resistance."),
                    "width": 125,
                },
                _("\u0398<sub>JC</sub>:"),
            ],
            "n_active_pins": [
                22,
                self.txtNActivePins,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                0,
                {
                    "tooltip": _(
                        "The number of active pins on the integrated circuit."
                    ),
                    "width": 125,
                },
                _("Active Pins:"),
            ],
            "technology_id": [
                37,
                self.cmbTechnology,
                "changed",
                super().on_changed_combo,
                "wvw_editing_design_electric",
                0,
                {
                    "tooltip": _(
                        "The technology used to construct the integrated circuit."
                    ),
                },
                _("Technology:"),
            ],
            "years_in_production": [
                55,
                self.txtYearsInProduction,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                2,
                {
                    "tooltip": _(
                        "The number of years the generic device type has been in "
                        "production."
                    ),
                    "width": 125,
                },
                _("Years in Production:"),
            ],
            "construction_id": [
                6,
                self.cmbConstruction,
                "changed",
                super().on_changed_combo,
                "wvw_editing_design_electric",
                0,
                {
                    "tooltip": _(
                        "The method of construction of the integrated circuit."
                    ),
                },
                _("Construction"),
            ],
            "n_cycles": [
                24,
                self.txtNCycles,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                0,
                {
                    "tooltip": _(
                        "The total number of programming cycles over the EEPROM life."
                    ),
                    "width": 125,
                },
                _("Programming Cycles:"),
            ],
            "operating_life": [
                28,
                self.txtOperatingLife,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                0.0,
                {
                    "tooltip": _("The system lifetime operating hours."),
                    "width": 125,
                },
                _("Operating Life:"),
            ],
            "family_id": [
                15,
                self.cmbECC,
                "changed",
                super().on_changed_combo,
                "wvw_editing_design_electric",
                0,
                {
                    "tooltip": _("The error correction code used by the EEPROM."),
                },
                _("Error Correction Code:"),
            ],
            "application_id": [
                2,
                self.cmbApplication,
                "changed",
                super().on_changed_combo,
                "wvw_editing_design_electric",
                0,
                {
                    "tooltip": _("The application of the integrated circuit."),
                },
                _("Application:"),
            ],
            "type_id": [
                48,
                self.cmbType,
                "changed",
                super().on_changed_combo,
                "wvw_editing_design_electric",
                0,
                {
                    "tooltip": _("The type of GaAs or VLSI device."),
                },
                _("Device Type:"),
            ],
            "feature_size": [
                16,
                self.txtFeatureSize,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                0.0,
                {
                    "tooltip": _("The feature size (in microns) of the VLSI device."),
                    "width": 125,
                },
                _("Feature Size:"),
            ],
            "manufacturing_id": [
                20,
                self.cmbManufacturing,
                "changed",
                super().on_changed_combo,
                "wvw_editing_design_electric",
                0,
                {
                    "tooltip": _("The manufacturing process for the VLSI device."),
                },
                _("Manufacturing Process:"),
            ],
            "voltage_esd": [
                51,
                self.txtVoltageESD,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                0.0,
                {
                    "tooltip": _(
                        "The ESD susceptibility threshold voltage of the VLSI device."
                    ),
                    "width": 125,
                },
                _("ESD Threshold Voltage:"),
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

    # pylint: disable=unused-argument
    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the integrated circuit RAMSTKComboBox()s.

        :param subcategory_id: the subcategory ID of the selected IC.  This is
            unused in this method but required because this method is a
            PyPubSub listener.
        :return: None
        :rtype: None
        """
        self.subcategory_id = subcategory_id

        # Load the quality level RAMSTKComboBox().
        self.cmbQuality.do_load_combo(
            [[_("Class S")], [_("Class B")], [_("Class B-1")]]
        )

        # Load the Construction RAMSTKComboBox().
        self.cmbConstruction.do_load_combo(
            [["FLOTOX"], [_("Textured Poly")]], signal="changed"
        )

        # Load the error correction code RAMSTKComboBox().
        self.cmbECC.do_load_combo(
            [
                [_("No on-chip ECC")],
                [_("On-chip Hamming code")],
                [_("Two-Needs-One redundant cell approach")],
            ],
            signal="changed",
        )

        # Load the manufacturing process RAMSTKComboBox().
        self.cmbManufacturing.do_load_combo(
            [["QML or QPL"], ["Non-QML or non-QPL"]], signal="changed"
        )

        # Load the package RAMSTKComboBox().
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

        # Load the technology RAMSTKComboBox().
        try:
            if self._hazard_rate_method_id == 1:
                if subcategory_id == 9:
                    _data = [["MMIC"], [_("Digital")]]
                else:
                    _data = [["Bipolar"], ["MOS"]]
            else:
                _data = self._dic_technology[subcategory_id]
        except KeyError:
            _data = []
        self.cmbTechnology.do_load_combo(_data, signal="changed")

        # Load the device type RAMSTKComboBox().
        try:
            _data = self._dic_types[subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data, signal="changed")

    def _do_set_reliability_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        :return: None
        :rtype: None
        """
        if attributes["hardware_id"] == self._record_id:
            self._hazard_rate_method_id = attributes["hazard_rate_method_id"]
            self._quality_id = attributes["quality_id"]

    def _do_set_sensitive(self, attributes: Dict[str, Any]) -> None:
        """Set widget sensitivity as needed for the selected IC.

        :return: None
        :rtype: None
        """
        self.cmbQuality.do_update(
            self._quality_id,
            signal="changed",
        )

        self.cmbApplication.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.cmbECC.set_sensitive(False)
        self.cmbManufacturing.set_sensitive(False)
        self.cmbPackage.set_sensitive(False)
        self.cmbTechnology.set_sensitive(False)
        self.cmbType.set_sensitive(False)
        self.txtArea.set_sensitive(False)
        self.txtFeatureSize.set_sensitive(False)
        self.txtNActivePins.set_sensitive(False)
        self.txtNCycles.set_sensitive(False)
        self.txtNElements.set_sensitive(False)
        self.txtOperatingLife.set_sensitive(False)
        self.txtThetaJC.set_sensitive(False)
        self.txtVoltageESD.set_sensitive(False)
        self.txtYearsInProduction.set_sensitive(False)

        _dic_method = {
            1: self.__do_load_linear,
            2: self.__do_load_logic,
            3: self.__do_load_pal_pla,
            4: self.__do_load_microprocessor_microcontroller,
            5: self.__do_load_rom,
            6: self.__do_load_eeprom,
            7: self.__do_load_dram,
            8: self.__do_load_sram,
            9: self.__do_load_gaas,
            10: self.__do_load_vhsic_vlsi,
        }
        try:
            # noinspection PyArgumentList
            _dic_method[self.subcategory_id](attributes)
        except KeyError:
            pass

        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbPackage.set_sensitive(True)
            self.cmbPackage.do_update(
                attributes["package_id"],
                signal="changed",
            )
            self.txtNElements.set_sensitive(True)
            self.txtNElements.do_update(
                str(attributes["n_elements"]),
                signal="changed",
            )
            self.txtThetaJC.set_sensitive(True)
            self.txtThetaJC.do_update(
                str(attributes["theta_jc"]),
                signal="changed",
            )
            self.txtNActivePins.do_update(
                str(attributes["n_active_pins"]),
                signal="changed",
            )

    def _do_load_application_combo(self, attributes: Dict[str, Any]) -> None:
        """Load the IC application RAMSTKComboBox().

        :param attributes: the attributes dict for the selected integrated circuit.
        :return: None
        """
        if attributes["construction_id"] == 1:
            self.cmbApplication.do_load_combo(
                [
                    [_("Low Noise and Low Power (\u2264 100mW)")],
                    [_("Driver and High Power (> 100mW)")],
                    [_("Unknown")],
                ],
                signal="changed",
            )
        else:
            self.cmbApplication.do_load_combo(
                [[_("All digital devices")]],
                signal="changed",
            )

    def __do_load_dram(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display DRAM information.

        :param attributes: the attributes dictionary for the selected
            integrated circuit.
        :return: None
        """
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbTechnology.do_update(
                attributes["technology_id"],
                signal="changed",
            )
        self.__do_set_dram_sensitive()

    def __do_load_eeprom(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display EEPROM information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbConstruction.do_update(
                attributes["construction_id"],
                signal="changed",
            )
            self.cmbTechnology.do_update(
                attributes["technology_id"],
                signal="changed",
            )
            self.cmbECC.do_update(
                attributes["family_id"],
                signal="changed",
            )
            self.txtNCycles.do_update(
                str(attributes["n_cycles"]),
                signal="changed",
            )
            self.txtOperatingLife.do_update(
                str(self.fmt.format(attributes["operating_life"])),
                signal="changed",
            )
        self.__do_set_eeprom_sensitive()

    def __do_load_gaas(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display GaAs IC information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbApplication.do_update(
                attributes["application_id"],
                signal="changed",
            )
            self.cmbType.do_update(
                attributes["type_id"],
                signal="changed",
            )
            self.txtYearsInProduction.do_update(
                str(attributes["years_in_production"]),
                signal="changed",
            )
        self.__do_set_gaas_sensitive()

    def __do_load_linear(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display linear (analog) information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(
            attributes["technology_id"],
            signal="changed",
        )
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.txtNActivePins.do_update(
                str(attributes["n_active_pins"]),
                signal="changed",
            )
            self.txtYearsInProduction.do_update(
                str(attributes["years_in_production"]),
                signal="changed",
            )

        self.__do_set_linear_sensitive()

    def __do_load_logic(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display digital IC information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(
            attributes["technology_id"],
            signal="changed",
        )
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.txtNActivePins.do_update(
                str(attributes["n_active_pins"]),
                signal="changed",
            )
            self.txtYearsInProduction.do_update(
                str(attributes["years_in_production"]),
                signal="changed",
            )

        self.__do_set_logic_sensitive()

    def __do_load_microprocessor_microcontroller(
        self, attributes: Dict[str, Any]
    ) -> None:
        """Load the widgets that display microprocessor information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(
            attributes["technology_id"],
            signal="changed",
        )
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.txtNActivePins.do_update(
                str(attributes["n_active_pins"]),
                signal="changed",
            )
            self.txtYearsInProduction.do_update(
                str(attributes["years_in_production"]),
                signal="changed",
            )

        self.__do_set_microprocessor_microcontroller_sensitive()

    def __do_load_pal_pla(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display DRAM information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(
            attributes["technology_id"],
            signal="changed",
        )
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.txtNActivePins.do_update(
                str(attributes["n_active_pins"]),
                signal="changed",
            )
            self.txtYearsInProduction.do_update(
                str(attributes["years_in_production"]),
                signal="changed",
            )

        self.__do_set_pal_pla_sensitive()

    def __do_load_rom(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display ROM information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(
            attributes["technology_id"],
            signal="changed",
        )
        self.__do_set_rom_sensitive()

    def __do_load_sram(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display SRAM information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(
            attributes["technology_id"],
            signal="changed",
        )
        self.__do_set_sram_sensitive()

    def __do_load_vhsic_vlsi(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display VHSIC/VLSI information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbManufacturing.do_update(
            attributes["manufacturing_id"],
            signal="changed",
        )
        self.cmbType.do_update(attributes["type_id"])
        self.txtArea.do_update(
            str(self.fmt.format(attributes["area"])),
            signal="changed",
        )
        self.txtFeatureSize.do_update(
            str(self.fmt.format(attributes["feature_size"])),
            signal="changed",
        )
        self.txtVoltageESD.do_update(
            str(self.fmt.format(attributes["voltage_esd"])),
            signal="changed",
        )
        self.__do_set_vhsic_vlsi_sensitive()

    def __do_set_dram_sensitive(self) -> None:
        """Set the widgets that display DRAM information sensitive.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            pub.sendMessage(
                "wvw_editing_hardware",
                node_id=self._record_id,
                package={"technology_id": 2},
            )
            self.txtNElements.set_sensitive(True)
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbTechnology.set_sensitive(True)

    def __do_set_eeprom_sensitive(self) -> None:
        """Set the widgets that display EEPROM information sensitive.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            pub.sendMessage(
                "wvw_editing_design_electric",
                node_id=self._record_id,
                package={"technology_id": 2},
            )
            self.txtNElements.set_sensitive(True)
        elif self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbConstruction.set_sensitive(True)
            self.cmbECC.set_sensitive(True)
            self.cmbTechnology.set_sensitive(True)
            self.txtNActivePins.set_sensitive(True)
            self.txtNCycles.set_sensitive(True)
            self.txtOperatingLife.set_sensitive(True)

    def __do_set_gaas_sensitive(self) -> None:
        """Set the widgets that display GaAs IC information sensitive.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            self.cmbTechnology.set_sensitive(True)
            self.txtNElements.set_sensitive(True)
        elif self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbApplication.set_sensitive(True)
            self.cmbType.set_sensitive(True)
            self.txtNActivePins.set_sensitive(True)
            self.txtYearsInProduction.set_sensitive(True)

    def __do_set_linear_sensitive(self) -> None:
        """Set the widgets that display linear (analog) information sensitive.

        :return: None
        :rtype: None
        """
        self.cmbTechnology.set_sensitive(True)
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            self.txtNElements.set_sensitive(True)

        elif self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.txtNActivePins.set_sensitive(True)
            self.txtYearsInProduction.set_sensitive(True)

    def __do_set_logic_sensitive(self) -> None:
        """Set the widgets that display digital IC information sensitive.

        :return: None
        :rtype: None
        """
        self.cmbTechnology.set_sensitive(True)
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            self.txtNElements.set_sensitive(True)
        elif self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.txtNActivePins.set_sensitive(True)
            self.txtYearsInProduction.set_sensitive(True)

    def __do_set_microprocessor_microcontroller_sensitive(self) -> None:
        """Set the widgets that display microprocessor information sensitive.

        :return: None
        :rtype: None
        """
        self.cmbTechnology.set_sensitive(True)
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            self.txtNElements.set_sensitive(True)
        elif self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.txtNActivePins.set_sensitive(True)
            self.txtYearsInProduction.set_sensitive(True)

    def __do_set_pal_pla_sensitive(self) -> None:
        """Set the widgets that display DRAM information sensitive.

        :return: None
        :rtype: None
        """
        self.cmbTechnology.set_sensitive(True)
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            self.txtNElements.set_sensitive(True)
        elif self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.txtNActivePins.set_sensitive(True)
            self.txtYearsInProduction.set_sensitive(True)

    def __do_set_rom_sensitive(self) -> None:
        """Set the widgets that display ROM information sensitive.

        :return: None
        :rtype: None
        """
        self.cmbTechnology.set_sensitive(True)
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            self.txtNElements.set_sensitive(True)

    def __do_set_sram_sensitive(self) -> None:
        """Set the widgets that display SRAM information sensitive.

        :return: None
        :rtype: None
        """
        self.cmbTechnology.set_sensitive(True)
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            self.txtNElements.set_sensitive(True)

    def __do_set_vhsic_vlsi_sensitive(self) -> None:
        """Set the widgets that display VHSIC/VLSI information sensitive.

        :return: None
        :rtype: None
        """
        self.cmbManufacturing.set_sensitive(True)
        self.cmbType.set_sensitive(True)
        self.txtArea.set_sensitive(True)
        self.txtFeatureSize.set_sensitive(True)
        self.txtNActivePins.set_sensitive(False)
        self.txtVoltageESD.set_sensitive(True)
