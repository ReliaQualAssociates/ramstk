# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.integrated_circuit.py is part of
#       the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Integrated Circuit Work View."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
# noinspection PyPackageRequirements
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry

# RAMSTK Local Imports
from .panels import RAMSTKAssessmentInputPanel, RAMSTKAssessmentResultPanel


class AssessmentInputPanel(RAMSTKAssessmentInputPanel):
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
        2: [["TTL"], ["ASTTL"], ["CML"], ["HTTL"], ["FTTL"], ["DTL"], ["ECL"],
            ["ALSTTL"], ["FLTTL"], ["STTL"], ["BiCMOS"], ["LSTTL"], ["III"],
            ["IIIL"], ["ISL"]],
        3: [["MOS"], [_("Bipolar")]],
        4: [["MOS"], [_("Bipolar")]],
        5: [["MOS"], [_("Bipolar")]],
        6: [["MOS"], [_("Bipolar")]],
        7: [["MOS"], [_("Bipolar")]],
        8: [["MOS"], [_("Bipolar")]],
        9: [["MMIC"], [_("Digital")]]
    }

    _dic_types: Dict[int, List[Any]] = {
        9: [["MMIC"], [_("Digital")]],
        10: [[_("Logic and Custom")], [_("Gate Array")]]
    }

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the IC assessment input view."""
        super().__init__()

        # Initialize private dictionary attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            0: ['quality_id', 'integer'],
            1: ['application_id', 'integer'],
            2: ['construction_id', 'integer'],
            3: ['type_id', 'integer'],
            4: ['manufacturing_id', 'integer'],
            5: ['package_id', 'integer'],
            6: ['technology_id', 'integer'],
            7: ['type_id', 'integer'],
            8: ['area', 'float'],
            9: ['feature_size', 'float'],
            10: ['n_active_pins', 'integer'],
            11: ['n_cycles', 'integer'],
            12: ['n_elements', 'integer'],
            13: ['operating_life', 'float'],
            14: ['theta_jc', 'float'],
            15: ['voltage_esd', 'float'],
            16: ['years_in_production', 'float'],
        }

        # Initialize private list attributes.
        self._lst_labels: List[str] = [
            _("Quality Level:"),
            _("Package:"),
            _("Die Area:"),
            _("N Elements:"),
            _("\u0398<sub>JC</sub>:"),
            _("Active Pins:"),
            _("Technology:"),
            _("Years in Production:"),
            _("Construction"),
            _("Programming Cycles:"),
            _("Operating Life:"),
            _("Error Correction Code:"),
            _("Application:"),
            _("Device Type:"),
            _("Feature Size:"),
            _("Manufacturing Process:"),
            _("ESD Threshold Voltage:"),
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbECC: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbManufacturing: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbPackage: RAMSTKComboBox = RAMSTKComboBox()
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

        self._dic_attribute_updater = {
            'quality_id': [self.cmbQuality.do_update, 'changed', 0],
            'application_id': [self.cmbApplication.do_update, 'changed', 1],
            'construction_id': [self.cmbConstruction.do_update, 'changed', 2],
            'manufacturing_id':
            [self.cmbManufacturing.do_update, 'changed', 3],
            'package_id': [self.cmbPackage.do_update, 'changed', 4],
            'technology_id': [self.cmbTechnology.do_update, 'changed', 5],
            'type_id': [self.cmbType.do_update, 'changed', 6],
            'area': [self.txtArea.do_update, 'changed', 7],
            'feature_size': [self.txtFeatureSize, 'changed', 8],
            'n_active_pins': [self.txtNActivePins.do_update, 'changed', 9],
            'n_cycles': [self.txtNCycles, 'changed', 10],
            'n_elements': [self.txtNElements, 'changed', 11],
            'operating_life': [self.txtOperatingLife, 'changed', 12],
            'theta_jc': [self.txtThetaJC, 'changed', 13],
            'voltage_esd': [self.txtVoltageESD, 'changed', 14],
            'years_in_production': [self.txtYearsInProduction, 'changed', 15],
        }
        self._lst_widgets = [
            self.cmbQuality,
            self.cmbPackage,
            self.txtArea,
            self.txtNElements,
            self.txtThetaJC,
            self.txtNActivePins,
            self.cmbTechnology,
            self.txtYearsInProduction,
            self.cmbConstruction,
            self.txtNCycles,
            self.txtOperatingLife,
            self.cmbECC,
            self.cmbApplication,
            self.cmbType,
            self.txtFeatureSize,
            self.cmbManufacturing,
            self.txtVoltageESD,
        ]
        self._lst_tooltips: List[str] = [
            _("The quality level of the integrated circuit."),
            _("The method of construction of the integrated circuit."),
            _("The die area (in mil<sup>2</sup>) of the integrated circuit."),
            _("The number of active elements in the integrated circuit."),
            _("The junction to case thermal resistance."),
            _("The number of active pins on the integrated circuit."),
            _("The technology used to construct the integrated circuit."),
            _("The number of years the generic device type has been in "
              "production."),
            _("The integrated circuit method of construction."),
            _("The total number of programming cycles over the EEPROM life."),
            _("The system lifetime operating hours."),
            _("The error correction code used by the EEPROM."),
            _("The application of the integrated circuit."),
            _("The type of GaAs or VLSI device."),
            _("The feature size (in microns) of the VLSI device."),
            _("The manufacturing process for the VLSI device."),
            _("The ESD susceptibility threshold voltage of the VLSI device."),
        ]

        self.__set_properties()
        super().do_make_panel_fixed()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_comboboxes, 'changed_subcategory')

        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    # pylint: disable=unused-argument
    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the integrated circuit RAMSTKComboBox()s.

        :param subcategory_id: the subcategory ID of the selected IC.  This is
            unused in this method but required because this method is a
            PyPubSub listener.
        :return: None
        :rtype: None
        """
        # Load the quality level RAMSTKComboBox().
        self.cmbQuality.do_load_combo([[_("Class S")], [_("Class B")],
                                       [_("Class B-1")]])

        # Load the Construction RAMSTKComboBox().
        self.cmbConstruction.do_load_combo([["FLOTOX"], [_("Textured Poly")]],
                                           signal='changed')

        # Load the error correction code RAMSTKComboBox().
        self.cmbECC.do_load_combo(
            [[_("No on-chip ECC")], [_("On-chip Hamming code")],
             [_("Two-Needs-One redundant cell approach")]],
            signal='changed')

        # Load the manufacturing process RAMSTKComboBox().
        self.cmbManufacturing.do_load_combo(
            [["QML or QPL"], ["Non-QML or non-QPL"]], signal='changed')

        # Load the package RAMSTKComboBox().
        self.cmbPackage.do_load_combo(
            [[_("Hermetic DIP w/ Solder or Weld Seal")],
             [_("Hermetic Pin Grid Array (PGA)")],
             [_("Hermetic SMT (Leaded and Nonleaded)")],
             [_("DIP w/ Glass Seal")], [_("Flatpacks w/ Axial Leads")],
             ["Can"], [_("Nonhermetic DIP")],
             [_("Nonhermetic Pin Grid Array (PGA)")], [_("Nonhermetic SMT")]],
            signal='changed')

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
        self.cmbTechnology.do_load_combo(_data, signal='changed')

        # Load the device type RAMSTKComboBox().
        try:
            _data = self._dic_types[subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data, signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Integrated Circuit assessment input widgets.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        super().do_load_common(attributes)

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
            _dic_method[self._subcategory_id](attributes)
        except KeyError:
            pass

        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            self.txtNElements.do_update(
                str(attributes['n_elements']),
                signal='changed',
            )
        elif self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbPackage.do_update(
                attributes['package_id'],
                signal='changed',
            )
            self.txtArea.do_update(
                str(self.fmt.format(attributes['area'])),
                signal='changed',
            )
            self.txtNElements.do_update(
                str(attributes['n_elements']),
                signal='changed',
            )
            self.txtThetaJC.do_update(
                str(self.fmt.format(attributes['theta_jc'])),
                signal='changed',
            )

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected IC.

        :return: None
        :rtype: None
        """
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
            1: self.__do_set_linear_sensitive,
            2: self.__do_set_logic_sensitive,
            3: self.__do_set_pal_pla_sensitive,
            4: self.__do_set_microprocessor_microcontroller_sensitive,
            5: self.__do_set_rom_sensitive,
            6: self.__do_set_eeprom_sensitive,
            7: self.__do_set_dram_sensitive,
            8: self.__do_set_sram_sensitive,
            9: self.__do_set_gaas_sensitive,
            10: self.__do_set_vhsic_vlsi_sensitive,
        }
        try:
            _dic_method[self._subcategory_id]()
        except KeyError:
            pass

        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbPackage.set_sensitive(True)
            self.txtArea.set_sensitive(True)
            self.txtNElements.set_sensitive(True)
            self.txtThetaJC.set_sensitive(True)

    def _do_load_application_combo(self, attributes: Dict[str, Any]) -> None:
        """Load the IC application RAMSTKComboBox().

        :param attributes: the attributes dict for the selected integrated
            circuit.
        :return: None
        """
        if attributes['construction_id'] == 1:
            self.cmbApplication.do_load_combo(
                [[_("Low Noise and Low Power (\u2264 100mW)")],
                 [_("Driver and High Power (> 100mW)")], [_("Unknown")]],
                signal='changed')
        else:
            self.cmbApplication.do_load_combo([[_("All digital devices")]],
                                              signal='changed')

    def __do_load_dram(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display DRAM information.

        :param attributes: the attributes dictionary for the selected
            integrated circuit.
        :return: None
        """
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbTechnology.do_update(attributes['technology_id'])

    def __do_load_eeprom(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display EEPROM information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbConstruction.do_update(attributes['construction_id'],
                                           signal='changed')
            self.cmbTechnology.do_update(attributes['technology_id'],
                                         signal='changed')
            self.cmbType.do_update(attributes['type_id'],
                                   signal='changed')  # Use for ECC.
            self.txtNCycles.do_update(str(attributes['n_cycles']),
                                      signal='changed')
            self.txtOperatingLife.do_update(str(
                self.fmt.format(attributes['operating_life'])),
                                            signal='changed')  # noqa

    def __do_load_gaas(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display GaAs IC information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbApplication.do_update(attributes['application_id'],
                                          signal='changed')
            self.cmbType.do_update(attributes['type_id'], signal='changed')
            self.txtYearsInProduction.do_update(str(
                attributes['years_in_production']),
                                                signal='changed')  # noqa

    def __do_load_linear(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display linear (analog) information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(attributes['technology_id'],
                                     signal='changed')
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.txtNActivePins.do_update(str(attributes['n_active_pins']),
                                          signal='changed')
            self.txtYearsInProduction.do_update(str(
                attributes['years_in_production']),
                                                signal='changed')  # noqa

    def __do_load_logic(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display digital IC information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(attributes['technology_id'],
                                     signal='changed')
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.txtNActivePins.do_update(str(attributes['n_active_pins']),
                                          signal='changed')
            self.txtYearsInProduction.do_update(str(
                attributes['years_in_production']),
                                                signal='changed')  # noqa

    def __do_load_microprocessor_microcontroller(
            self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display microprocessor information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(attributes['technology_id'],
                                     signal='changed')
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.txtNActivePins.do_update(str(attributes['n_active_pins']),
                                          signal='changed')
            self.txtYearsInProduction.do_update(str(
                attributes['years_in_production']),
                                                signal='changed')  # noqa

    def __do_load_pal_pla(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display DRAM information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(attributes['technology_id'],
                                     signal='changed')
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.txtNActivePins.do_update(str(attributes['n_active_pins']),
                                          signal='changed')
            self.txtYearsInProduction.do_update(str(
                attributes['years_in_production']),
                                                signal='changed')  # noqa

    def __do_load_rom(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display ROM information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(attributes['technology_id'],
                                     signal='changed')

    def __do_load_sram(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display SRAM information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(attributes['technology_id'],
                                     signal='changed')

    def __do_load_vhsic_vlsi(self, attributes: Dict[str, Any]) -> None:
        """Load the widgets that display VHSIC/VLSI information.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        if self._subcategory_id == 10:
            self.cmbManufacturing.do_update(attributes['manufacturing_id'],
                                            signal='changed')
            self.cmbType.do_update(attributes['type_id'])
            self.txtArea.do_update(str(self.fmt.format(attributes['area'])),
                                   signal='changed')
            self.txtFeatureSize.do_update(str(
                self.fmt.format(attributes['feature_size'])),
                                          signal='changed')  # noqa
            self.txtVoltageESD.do_update(str(
                self.fmt.format(attributes['voltage_esd'])),
                                         signal='changed')  # noqa

    def __do_set_dram_sensitive(self) -> None:
        """Set the widgets that display DRAM information sensitive.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            pub.sendMessage('wvw_editing_hardware',
                            node_id=self._record_id,
                            package={'technology_id': 2})
            self.txtNElements.set_sensitive(True)
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbTechnology.set_sensitive(True)

    def __do_set_eeprom_sensitive(self) -> None:
        """Set the widgets that display EEPROM information sensitive.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            pub.sendMessage('wvw_editing_hardware',
                            node_id=self._record_id,
                            package={'technology_id': 2})
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
        if self._subcategory_id == 10:
            self.cmbManufacturing.set_sensitive(True)
            self.cmbType.set_sensitive(True)
            self.txtArea.set_sensitive(True)
            self.txtFeatureSize.set_sensitive(True)
            self.txtNActivePins.set_sensitive(False)
            self.txtVoltageESD.set_sensitive(True)

    def __set_callbacks(self) -> None:
        """Set callback methods for IC assessment input widgets.

        :return: None
        :rtype: None
        """
        # ----- COMBOBOXES
        self.cmbQuality.dic_handler_id['changed'] = self.cmbQuality.connect(
            'changed',
            super().on_changed_combo, 0, 'wvw_editing_hardware')
        self.cmbApplication.dic_handler_id[
            'changed'] = self.cmbApplication.connect('changed',
                                                     super().on_changed_combo,
                                                     1, 'wvw_editing_hardware')
        self.cmbConstruction.dic_handler_id[
            'changed'] = self.cmbConstruction.connect('changed',
                                                      super().on_changed_combo,
                                                      2,
                                                      'wvw_editing_hardware')
        self.cmbECC.dic_handler_id['changed'] = self.cmbECC.connect(
            'changed',
            super().on_changed_combo, 3, 'wvw_editing_hardware')
        self.cmbManufacturing.dic_handler_id[
            'changed'] = self.cmbManufacturing.connect(
                'changed',
                super().on_changed_combo, 4, 'wvw_editing_hardware')
        self.cmbPackage.dic_handler_id['changed'] = self.cmbPackage.connect(
            'changed',
            super().on_changed_combo, 5, 'wvw_editing_hardware')
        self.cmbTechnology.dic_handler_id[
            'changed'] = self.cmbTechnology.connect('changed',
                                                    super().on_changed_combo,
                                                    6, 'wvw_editing_hardware')
        self.cmbType.dic_handler_id['changed'] = self.cmbType.connect(
            'changed',
            super().on_changed_combo, 7, 'wvw_editing_hardware')

        # ----- ENTRIES
        self.txtArea.dic_handler_id['changed'] = self.txtArea.connect(
            'changed',
            super().on_changed_entry, 8, 'wvw_editing_hardware')
        self.txtFeatureSize.dic_handler_id[
            'changed'] = self.txtFeatureSize.connect('changed',
                                                     super().on_changed_entry,
                                                     9, 'wvw_editing_hardware')
        self.txtNActivePins.dic_handler_id[
            'changed'] = self.txtNActivePins.connect('changed',
                                                     super().on_changed_entry,
                                                     10,
                                                     'wvw_editing_hardware')
        self.txtNCycles.dic_handler_id['changed'] = self.txtNCycles.connect(
            'changed',
            super().on_changed_entry, 11, 'wvw_editing_hardware')
        self.txtNElements.dic_handler_id[
            'changed'] = self.txtNElements.connect('changed',
                                                   super().on_changed_entry,
                                                   12, 'wvw_editing_hardware')
        self.txtOperatingLife.dic_handler_id[
            'changed'] = self.txtOperatingLife.connect(
                'changed',
                super().on_changed_entry, 13, 'wvw_editing_hardware')
        self.txtThetaJC.dic_handler_id['changed'] = self.txtThetaJC.connect(
            'changed',
            super().on_changed_entry, 14, 'wvw_editing_hardware')
        self.txtVoltageESD.dic_handler_id[
            'changed'] = self.txtVoltageESD.connect('changed',
                                                    super().on_changed_entry,
                                                    15, 'wvw_editing_hardware')
        self.txtYearsInProduction.dic_handler_id[
            'changed'] = self.txtYearsInProduction.connect(
                'changed',
                super().on_changed_entry, 16, 'wvw_editing_hardware')

    def __set_properties(self) -> None:
        """Set properties for Integrated Circuit assessment input widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties()

        # ----- ENTRIES
        self.txtArea.do_set_properties(tooltip=self._lst_tooltips[2],
                                       width=125)
        self.txtFeatureSize.do_set_properties(tooltip=self._lst_tooltips[14],
                                              width=125)
        self.txtNActivePins.do_set_properties(tooltip=self._lst_tooltips[5],
                                              width=125)
        self.txtNCycles.do_set_properties(tooltip=self._lst_tooltips[9],
                                          width=125)
        self.txtNElements.do_set_properties(tooltip=self._lst_tooltips[3],
                                            width=125)
        self.txtOperatingLife.do_set_properties(tooltip=self._lst_tooltips[10],
                                                width=125)
        self.txtThetaJC.do_set_properties(tooltip=self._lst_tooltips[4],
                                          width=125)
        self.txtVoltageESD.do_set_properties(tooltip=self._lst_tooltips[16],
                                             width=125)
        self.txtYearsInProduction.do_set_properties(
            tooltip=self._lst_tooltips[7], width=125)


class AssessmentResultPanel(RAMSTKAssessmentResultPanel):
    """Display IC assessment results attribute data in the RAMSTK Work Book.

    The Integrated Circuit assessment result view displays all the assessment
    results for the selected integrated circuit.  This includes, currently,
    results for MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress
    methods.  The attributes of a integrated circuit assessment result view
    are:

    :ivar txtC1: displays the die complexity hazard rate of the integrated
        circuit.
    :ivar txtPiT: displays the temperature factor for the integrated circuit.
    :ivar txtC2: displays the package failure rate for the integrated circuit.
    :ivar txtPiL: displays the learning factor for the integrated circuit.
    :ivar txtLambdaCYC: displays the read/write cycling induced hazard rate for
        the EEPROM.
    :ivar txtLambdaBD: displays the die base hazard rate for the VLSI device.
    :ivar txtPiMFG: displays the manufacturing process correction factor for
        VLSI device.
    :ivar txtPiCD: displays the die complexity correction factor for the VLSI
        device.
    :ivar txtLambdaBP: displays the package base hazard rate for the VLSI
        device.
    :ivar txtPiPT: displays the package type correction factor for the VLSI
        device.
    :ivar txtLambdaEOS: displays the electrical overstress hazard rate for the
        VLSI device.
    :ivar txtPiA: displays the application factor for the integrated circuit.
    """

    # Define private class dict class attributes.
    _dic_part_stress: Dict[int, str] = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = ("
        "C<sub>1</sub>\u03C0<sub>T</sub> + "
        "C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub"
        "></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = ("
        "C<sub>1</sub>\u03C0<sub>T</sub> + "
        "C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub"
        "></span>",
        3:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = ("
        "C<sub>1</sub>\u03C0<sub>T</sub> + "
        "C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub"
        "></span>",
        4:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = ("
        "C<sub>1</sub>\u03C0<sub>T</sub> + "
        "C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub"
        "></span>",
        5:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = ("
        "C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + "
        "\u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        6:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = ("
        "C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + "
        "\u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        7:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = ("
        "C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + "
        "\u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        8:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = ("
        "C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + "
        "\u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        9:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = ("
        "C<sub>1</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub> + "
        "C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>L</sub>\u03C0<sub>Q</sub"
        "></span>",
        10:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>BD</sub>\u03C0<sub>MFG</sub>\u03C0<sub>T</sub>\u03C0<sub"
        ">CD</sub> + \u03BB<sub>BP</sub>\u03C0<sub>E</sub>\u03C0<sub>Q</sub"
        ">\u03C0<sub>PT</sub> + \u03BB<sub>EOS</sub></span> "
    }

    # Define private class list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the IC assessment result view."""
        super().__init__()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels = [
            "",
            "\u03BB<sub>b</sub>:",
            "\u03C0<sub>Q</sub>:",
            "\u03C0<sub>E</sub>:",
            "C1",
            '\u03C0<sub>T</sub>:',
            "C2",
            '\u03C0<sub>L</sub>:',
            '\u03C0<sub>CYC</sub>:',
            '\u03C0<sub>BD</sub>:',
            '\u03C0<sub>MFG</sub>:',
            '\u03C0<sub>CD</sub>:',
            '\u03C0<sub>BP</sub>:',
            '\u03C0<sub>PT</sub>:',
            '\u03C0<sub>EOS</sub>:',
            '\u03C0<sub>A</sub>:',
        ]
        self._lst_tooltips: List[str] = [
            _("The assessment model used to calculate the integrated circuit "
              "hazard rate."),
            _('The base hazard rate for the integrated circuit.'),
            _('The quality factor for the integrated circuit.'),
            _('The environment factor for the integrated circuit.'),
            _('The die complexity factor for the integrated circuit.'),
            _('The temperature correction factor for the integrated circuit.'),
            _('The package hazard rate for the integrated circuit.'),
            _('The learning factor for the integrated circuit.'),
            _('The read/write cycling induced hazard rate for the integrated '
              'circuit.'),
            _('The die base hazard rate for the integrated circuit.'),
            _('The manufacturing process correction factor for the integrated '
              'circuit.'),
            _('The die complexity correction factor for the integrated '
              'circuit.'),
            _('The package base hazard rate for the integrated circuit.'),
            _('The package type factor for the integrated circuit.'),
            _('The electrical overstress hazard rate for the integrated '
              'circuit.'),
            _('The application factor for the integrated circuit.'),
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtC1: RAMSTKEntry = RAMSTKEntry()
        self.txtC2: RAMSTKEntry = RAMSTKEntry()
        self.txtLambdaBD: RAMSTKEntry = RAMSTKEntry()
        self.txtLambdaBP: RAMSTKEntry = RAMSTKEntry()
        self.txtLambdaCYC: RAMSTKEntry = RAMSTKEntry()
        self.txtLambdaEOS: RAMSTKEntry = RAMSTKEntry()
        self.txtPiA: RAMSTKEntry = RAMSTKEntry()
        self.txtPiCD: RAMSTKEntry = RAMSTKEntry()
        self.txtPiL: RAMSTKEntry = RAMSTKEntry()
        self.txtPiMFG: RAMSTKEntry = RAMSTKEntry()
        self.txtPiPT: RAMSTKEntry = RAMSTKEntry()
        self.txtPiT: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.lblModel,
            self.txtLambdaB,
            self.txtPiQ,
            self.txtPiE,
            self.txtC1,
            self.txtPiT,
            self.txtC2,
            self.txtPiL,
            self.txtLambdaCYC,
            self.txtLambdaBD,
            self.txtPiMFG,
            self.txtPiCD,
            self.txtLambdaBP,
            self.txtPiPT,
            self.txtLambdaEOS,
            self.txtPiA,
        ]

        super().do_set_properties()
        super().do_make_panel_fixed()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the integrated circuit assessment results page.

        :param attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        super().do_load_common(attributes)

        self.txtC1.do_update(str(self.fmt.format(attributes['C1'])))
        self.txtPiT.do_update(str(self.fmt.format(attributes['piT'])))
        self.txtC2.do_update(str(self.fmt.format(attributes['C2'])))
        self.txtPiL.do_update(str(self.fmt.format(attributes['piL'])))
        self.txtLambdaCYC.do_update(
            str(self.fmt.format(attributes['lambdaCYC'])), )
        self.txtLambdaBD.do_update(str(self.fmt.format(
            attributes['lambdaBD'])))
        self.txtPiMFG.do_update(str(self.fmt.format(attributes['piMFG'])))
        self.txtPiCD.do_update(str(self.fmt.format(attributes['piCD'])))
        self.txtLambdaBP.do_update(str(self.fmt.format(
            attributes['lambdaBP'])))
        self.txtPiPT.do_update(str(self.fmt.format(attributes['piPT'])))
        self.txtLambdaEOS.do_update(
            str(self.fmt.format(attributes['lambdaEOS'])), )
        self.txtPiA.do_update(str(self.fmt.format(attributes['piA'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected IC.

        :return: None
        :rtype: None
        """
        self.txtLambdaB.set_sensitive(True)
        self.txtPiQ.set_sensitive(True)
        self.txtPiE.set_sensitive(False)

        self.txtC1.set_sensitive(False)
        self.txtPiT.set_sensitive(False)
        self.txtC2.set_sensitive(False)
        self.txtPiL.set_sensitive(False)
        self.txtLambdaCYC.set_sensitive(False)
        self.txtLambdaBD.set_sensitive(False)
        self.txtPiMFG.set_sensitive(False)
        self.txtPiCD.set_sensitive(False)
        self.txtLambdaBP.set_sensitive(False)
        self.txtPiPT.set_sensitive(False)
        self.txtLambdaEOS.set_sensitive(False)
        self.txtPiA.set_sensitive(False)

        if self._subcategory_id == 10:
            self.txtLambdaB.set_sensitive(False)
            self.txtLambdaB.set_visible(False)
            self.txtLambdaBD.set_sensitive(True)
            self.txtPiMFG.set_sensitive(True)
            self.txtPiCD.set_sensitive(True)
            self.txtLambdaBP.set_sensitive(True)
            self.txtPiPT.set_sensitive(True)
            self.txtLambdaEOS.set_sensitive(True)
            self.txtPiE.set_sensitive(True)

        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            self.txtLambdaB.set_sensitive(True)
        elif self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.__do_set_part_stress_sensitive()

    def __do_set_part_stress_sensitive(self) -> None:
        """Set the widgets displaying MIL-HDBK-217F part stress info sensitive.

        :return: None
        :rtype: None
        """
        self.txtPiT.set_sensitive(True)
        self.txtPiE.set_sensitive(True)
        self.txtPiQ.set_sensitive(True)

        if self._subcategory_id in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            self.txtC1.set_sensitive(True)
            self.txtC2.set_sensitive(True)
            self.txtPiL.set_sensitive(True)

        if self._subcategory_id in [5, 6, 7, 8]:
            self.txtLambdaCYC.set_sensitive(True)

        if self._subcategory_id == 9:
            self.txtPiA.set_sensitive(True)
