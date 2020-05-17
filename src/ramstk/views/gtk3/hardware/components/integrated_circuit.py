# -*- coding: utf-8 -*-
#
#       gui.gtk.workviews.components.IntegratedCircuit.py is part of the
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2018 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Integrated Circuit Work View."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
# noinspection PyPackageRequirements
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry

# RAMSTK Local Imports
from .workview import RAMSTKAssessmentInputs, RAMSTKAssessmentResults


class AssessmentInputs(RAMSTKAssessmentInputs):
    """
    Display IC assessment input attribute data in the RAMSTK Work Book.

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
    :ivar txtYearsProduction: enter and display the number of years the
        integrated circuit type has been in production.

    Callbacks signals in _lst_handler_id:

    +-------+-------------------------------------------+
    | Index | Widget - Signal                           |
    +=======+===========================================+
    |   0   | cmbQuality - `changed`                    |
    +-------+-------------------------------------------+
    |   1   | cmbApplication - `changed`                |
    +-------+-------------------------------------------+
    |   2   | cmbConstruction - `changed`               |
    +-------+-------------------------------------------+
    |   3   | cmbECC - `changed`                        |
    +-------+-------------------------------------------+
    |   4   | cmbManufacturing - `changed`              |
    +-------+-------------------------------------------+
    |   5   | cmbPackage - `changed`                    |
    +-------+-------------------------------------------+
    |   6   | cmbTechnology - `changed`                 |
    +-------+-------------------------------------------+
    |   7   | cmbType - `changed`                       |
    +-------+-------------------------------------------+
    |   8   | txtArea - `changed`                       |
    +-------+-------------------------------------------+
    |   9   | txtFeatureSize - `changed`                |
    +-------+-------------------------------------------+
    |  10   | txtNActivePins - `changed`                |
    +-------+-------------------------------------------+
    |  11   | txtNCycles - `changed`                    |
    +-------+-------------------------------------------+
    |  12   | txtNElements - `changed`                  |
    +-------+-------------------------------------------+
    |  13   | txtOperatingLife - `changed`              |
    +-------+-------------------------------------------+
    |  14   | txtThetaJC - `changed`                    |
    +-------+-------------------------------------------+
    |  15   | txtVoltageESD - `changed`                 |
    +-------+-------------------------------------------+
    |  16   | txtYearsInProduction - `changed`          |
    +-------+-------------------------------------------+
    """

    # Define private dict attributes.
    _dic_keys = {
        0: 'quality_id',
        1: 'application_id',
        2: 'construction_id',
        3: 'type_id',
        4: 'manufacturing_id',
        5: 'package_id',
        6: 'technology_id',
        7: 'type_id',
        8: 'area',
        9: 'feature_size',
        10: 'n_active_pins',
        11: 'n_cycles',
        12: 'n_elements',
        13: 'operating_life',
        14: 'theta_jc',
        15: 'voltage_esd',
        16: 'years_in_production'
    }

    _dic_technology = {
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

    _dic_types = {
        9: [["MMIC"], [_("Digital")]],
        10: [[_("Logic and Custom")], [_("Gate Array")]]
    }

    # Define private list attributes.
    _lst_labels = [
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
        _("ESD Threshold Voltage:")
    ]

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'integrated_circuit') -> None:
        """
        Initialize an instance of the IC assessment input view.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param str module: the name of the RAMSTK workflow module.
        """
        super().__init__(configuration, logger, module=module)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

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

        self._lst_widgets = [
            self.cmbQuality, self.cmbPackage, self.txtArea, self.txtNElements,
            self.txtThetaJC, self.txtNActivePins, self.cmbTechnology,
            self.txtYearsInProduction, self.cmbConstruction, self.txtNCycles,
            self.txtOperatingLife, self.cmbECC, self.cmbApplication,
            self.cmbType, self.txtFeatureSize, self.cmbManufacturing,
            self.txtVoltageESD
        ]

        self.__set_properties()
        self.__set_callbacks()
        self.make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_comboboxes, 'changed_subcategory')

        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def __set_callbacks(self) -> None:
        """
        Set callback methods for Integrated Circuit assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbQuality.dic_handler_id['changed'] = self.cmbQuality.connect(
            'changed', self._on_combo_changed, 0)
        # TODO: See issue #310.  The _lst_handler_id attribute will be
        #  retired once issue #310 is implemented completely.
        self._lst_handler_id.append(self.cmbQuality.dic_handler_id['changed'])

        self.cmbApplication.dic_handler_id[
            'changed'] = self.cmbApplication.connect('changed',
                                                     self._on_combo_changed, 1)
        self.cmbConstruction.dic_handler_id[
            'changed'] = self.cmbConstruction.connect('changed',
                                                      self._on_combo_changed,
                                                      2)
        self.cmbECC.dic_handler_id['changed'] = self.cmbECC.connect(
            'changed', self._on_combo_changed, 3)
        self.cmbManufacturing.dic_handler_id[
            'changed'] = self.cmbManufacturing.connect('changed',
                                                       self._on_combo_changed,
                                                       4)
        self.cmbPackage.dic_handler_id['changed'] = self.cmbPackage.connect(
            'changed', self._on_combo_changed, 5)
        self.cmbTechnology.dic_handler_id[
            'changed'] = self.cmbTechnology.connect('changed',
                                                    self._on_combo_changed, 6)
        self.cmbType.dic_handler_id['changed'] = self.cmbType.connect(
            'changed', self._on_combo_changed, 7)

        self.txtArea.dic_handler_id['changed'] = self.txtArea.connect(
            'focus-out-event', self._on_focus_out, 8)
        self.txtFeatureSize.dic_handler_id[
            'changed'] = self.txtFeatureSize.connect('focus-out-event',
                                                     self._on_focus_out, 9)
        self.txtNActivePins.dic_handler_id[
            'changed'] = self.txtNActivePins.connect('focus-out-event',
                                                     self._on_focus_out, 10)
        self.txtNCycles.dic_handler_id['changed'] = self.txtNCycles.connect(
            'focus-out-event', self._on_focus_out, 11)
        self.txtNElements.dic_handler_id[
            'changed'] = self.txtNElements.connect('focus-out-event',
                                                   self._on_focus_out, 12)
        self.txtOperatingLife.dic_handler_id[
            'changed'] = self.txtOperatingLife.connect('focus-out-event',
                                                       self._on_focus_out, 13)
        self.txtThetaJC.dic_handler_id['changed'] = self.txtThetaJC.connect(
            'focus-out-event', self._on_focus_out, 14)
        self.txtVoltageESD.dic_handler_id[
            'changed'] = self.txtVoltageESD.connect('focus-out-event',
                                                    self._on_focus_out, 15)
        self.txtYearsInProduction.dic_handler_id[
            'changed'] = self.txtYearsInProduction.connect(
                'focus-out-event', self._on_focus_out, 16)

    def __set_properties(self) -> None:
        """
        Set properties for Integrated Circuit assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbApplication.do_set_properties(
            tooltip=_("The application of the integrated circuit."))
        self.cmbConstruction.do_set_properties(
            tooltip=_("The integrated circuit method of construction."))
        self.cmbECC.do_set_properties(
            tooltip=_("The error correction code used by the EEPROM."))
        self.cmbManufacturing.do_set_properties(
            tooltip=_("The manufacturing process for the VLSI device."))
        self.cmbPackage.do_set_properties(
            tooltip=_("The method of construction of the integrated circuit."))
        self.cmbTechnology.do_set_properties(tooltip=_(
            "The technology used to construct the integrated circuit."))
        self.cmbType.do_set_properties(
            tooltip=_("The type of GaAs or VLSI device."))

        self.txtArea.do_set_properties(
            width=125,
            tooltip=_(
                "The die area (in mil<sup>2</sup>) of the integrated circuit.")
        )
        self.txtFeatureSize.do_set_properties(
            width=125,
            tooltip=_("The feature size (in microns) of the VLSI device."))
        self.txtNActivePins.do_set_properties(
            width=125,
            tooltip=_("The number of active pins on the integrated circuit."))
        self.txtNCycles.do_set_properties(
            width=125,
            tooltip=_(
                "The total number of programming cycles over the EEPROM life.")
        )
        self.txtNElements.do_set_properties(
            width=125,
            tooltip=_(
                "The number of active elements in the integrated circuit."))
        self.txtOperatingLife.do_set_properties(
            width=125, tooltip=_("The system lifetime operating hours."))
        self.txtThetaJC.do_set_properties(
            width=125, tooltip=_("The junction to case thermal resistance."))
        self.txtVoltageESD.do_set_properties(
            width=125,
            tooltip=_(
                "The ESD susceptibility threshold voltage of the VLSI device.")
        )
        self.txtYearsInProduction.do_set_properties(
            width=125,
            tooltip=_(
                "The number of years the generic device type has been in "
                "production."))

    def __do_load_application_combo(self, attributes: Dict[str, Any]) -> None:
        """
        Load the IC application RAMSTKComboBox().

        :param dict attributes: the attributes dict for the selected
            integrated circuit.
        :return: None
        :rtype: Nont
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
        """
        Load the widgets that display DRAM information.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbTechnology.do_update(attributes['technology_id'])

    def __do_load_eeprom(self, attributes: Dict[str, Any]) -> None:
        """
        Load the widgets that display EEPROM information.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbConstruction.do_update(attributes['construction_id'])
            self.cmbTechnology.do_update(attributes['technology_id'])
            self.cmbType.do_update(attributes['type_id'])  # Use for ECC.
            self.txtNCycles.do_update(str(attributes['n_cycles']))
            self.txtOperatingLife.do_update(
                str(self.fmt.format(attributes['operating_life'])))

    def __do_load_gaas(self, attributes: Dict[str, Any]) -> None:
        """
        Load the widgets that display GaAs IC information.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbApplication.do_update(attributes['application_id'])
            self.cmbType.do_update(attributes['type_id'])
            self.txtYearsInProduction.do_update(
                str(attributes['years_in_production']))

    def __do_load_linear(self, attributes: Dict[str, Any]) -> None:
        """
        Load the widgets that display linear (analog) information.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(attributes['technology_id'])
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.txtNActivePins.do_update(str(attributes['n_active_pins']))
            self.txtYearsInProduction.do_update(
                str(attributes['years_in_production']))

    def __do_load_logic(self, attributes: Dict[str, Any]) -> None:
        """
        Load the widgets that display digital IC information.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(attributes['technology_id'])
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.txtNActivePins.do_update(str(attributes['n_active_pins']))
            self.txtYearsInProduction.do_update(
                str(attributes['years_in_production']))

    def __do_load_microprocessor_microcontroller(self,
                                                 attributes: Dict[str, Any]
                                                 ) -> None:
        """
        Load the widgets that display microprocessor information.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(attributes['technology_id'])
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.txtNActivePins.do_update(str(attributes['n_active_pins']))
            self.txtYearsInProduction.do_update(
                str(attributes['years_in_production']))

    def __do_load_pal_pla(self, attributes: Dict[str, Any]) -> None:
        """
        Load the widgets that display DRAM information.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(attributes['technology_id'])
        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.txtNActivePins.do_update(str(attributes['n_active_pins']))
            self.txtYearsInProduction.do_update(
                str(attributes['years_in_production']))

    def __do_load_rom(self, attributes: Dict[str, Any]) -> None:
        """
        Load the widgets that display ROM information.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(attributes['technology_id'])

    def __do_load_sram(self, attributes: Dict[str, Any]) -> None:
        """
        Load the widgets that display SRAM information.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.do_update(attributes['technology_id'])

    def __do_load_vhsic_vlsi(self, attributes: Dict[str, Any]) -> None:
        """
        Load the widgets that display VHSIC/VLSI information.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        if self._subcategory_id == 10:
            self.cmbManufacturing.do_update(attributes['manufacturing_id'])
            self.cmbType.do_update(attributes['type_id'])
            self.txtArea.do_update(str(self.fmt.format(attributes['area'])))
            self.txtFeatureSize.do_update(
                str(self.fmt.format(attributes['feature_size'])))
            self.txtVoltageESD.do_update(
                str(self.fmt.format(attributes['voltage_esd'])))

    def __do_set_dram_sensitive(self) -> None:
        """
        Set the widgets that display DRAM information sensitive.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
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
        """
        Set the widgets that display EEPROM information sensitive.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
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
        """
        Set the widgets that display GaAs IC information sensitive.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
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
        """
        Set the widgets that display linear (analog) information sensitive.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
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
        """
        Set the widgets that display digital IC information sensitive.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
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
        """
        Set the widgets that display microprocessor information sensitive.
        Set the widgets that display microprocessor information sensitive.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
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
        """
        Set the widgets that display DRAM information sensitive.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
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
        """
        Set the widgets that display ROM information sensitive.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.set_sensitive(True)
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            self.txtNElements.set_sensitive(True)

    def __do_set_sram_sensitive(self) -> None:
        """
        Set the widgets that display SRAM information sensitive.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        self.cmbTechnology.set_sensitive(True)
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            self.txtNElements.set_sensitive(True)

    def __do_set_vhsic_vlsi_sensitive(self) -> None:
        """
        Set the widgets that display VHSIC/VLSI information sensitive.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
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

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Integrated Circuit assesment input widgets.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        super().do_load_page(attributes)

        self.__do_load_application_combo(attributes)
        _method = {
            1: self.__do_load_linear,
            2: self.__do_load_logic,
            3: self.__do_load_pal_pla,
            4: self.__do_load_microprocessor_microcontroller,
            5: self.__do_load_rom,
            6: self.__do_load_eeprom,
            7: self.__do_load_dram,
            8: self.__do_load_sram,
            9: self.__do_load_gaas,
            10: self.__do_load_vhsic_vlsi
        }
        try:
            _method[self._subcategory_id](attributes)
        except KeyError:
            pass

        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            self.txtNElements.do_update(str(attributes['n_elements']))
        elif self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbPackage.do_update(attributes['package_id'])
            self.txtArea.do_update(str(self.fmt.format(attributes['area'])))
            self.txtNElements.do_update(str(attributes['n_elements']))
            self.txtThetaJC.do_update(
                str(self.fmt.format(attributes['theta_jc'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """
        Set widget sensitivity as needed for the selected integrated circuit.

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

        _method = {
            1: self.__do_set_linear_sensitive,
            2: self.__do_set_logic_sensitive,
            3: self.__do_set_pal_pla_sensitive,
            4: self.__do_set_microprocessor_microcontroller_sensitive,
            5: self.__do_set_rom_sensitive,
            6: self.__do_set_eeprom_sensitive,
            7: self.__do_set_dram_sensitive,
            8: self.__do_set_sram_sensitive,
            9: self.__do_set_gaas_sensitive,
            10: self.__do_set_vhsic_vlsi_sensitive
        }
        try:
            _method[self._subcategory_id]()
        except KeyError:
            pass

        if self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            self.cmbPackage.set_sensitive(True)
            self.txtArea.set_sensitive(True)
            self.txtNElements.set_sensitive(True)
            self.txtThetaJC.set_sensitive(True)

    def _on_combo_changed(self, combo: RAMSTKComboBox, index: int) -> None:
        """
        Retrieve RAMSTKCombo() changes and assign to IC attribute.

        This method is called by:

            * Gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
        :param int index: the position in the signal handler list associated
            with the calling RAMSTKComboBox().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbQuality       |    4    | cmbManufacturing |
            +---------+------------------+---------+------------------+
            |    1    | cmbApplication   |    5    | cmbPackage       |
            +---------+------------------+---------+------------------+
            |    2    | cmbContruction   |    6    | cmbTechnology    |
            +---------+------------------+---------+------------------+
            |    3    | cmbECC           |    7    | cmbType          |
            +---------+------------------+---------+------------------+

        :return: None
        :rtype: None
        """
        super().on_combo_changed(combo, index, 'wvw_editing_component')

    def _on_focus_out(
            self,
            entry: object,
            __event: Gdk.EventFocus,  # pylint: disable=unused-argument
            index: int) -> None:
        """
        Retrieve changes made in RAMSTKEntry() widgets.

        This method is called by:

            * RAMSTKEntry() 'on-focus-out' signal
            * RAMSTKTextView() 'changed' signal

        :param object entry: the RAMSTKEntry() or RAMSTKTextView() that
            called this method.
        :param __event: the Gdk.EventFocus that triggered the signal.
        :type __event: :class:`Gdk.EventFocus`
        :param int index: the position in the Hardware class Gtk.TreeModel()
            associated with the data from the calling Gtk.Widget().  Indices
            are:

            +-------+----------------------+-------+----------------------+
            | Index | Widget               | Index | Widget               |
            +=======+======================+=======+======================+
            |   8   | txtArea              |   13  | txtOperatingLife     |
            +-------+----------------------+-------+----------------------+
            |   9   | txtFeatureSize       |   14  | txtThetaJC           |
            +-------+----------------------+-------+----------------------+
            |  10   | txtNActivePins       |   15  | txtVoltageESD        |
            +-------+----------------------+-------+----------------------+
            |  11   | txtNCycles           |   16  | txtYearsProduction   |
            +-------+----------------------+-------+----------------------+
            |  12   | txtNElements         |       |                      |
            +-------+----------------------+-------+----------------------+

        :return: None
        :rtype: None
        """
        super().on_focus_out(entry, index, 'wvw_editing_component')

    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """
        Load the integrated circuit RAMSTKComboBox()s.

        :param int subcategory_id: the newly selected integrated circuit
            subcategory ID.
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


class AssessmentResults(RAMSTKAssessmentResults):
    """
    Display IC assessment results attribute data in the RAMSTK Work Book.

    The Integrated Circuit assessment result view displays all the assessment
    results for the selected integrated circuit.  This includes, currently,
    results for MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress
    methods.  The attributes of a integrated circuit assessment result view
    are:

    :ivar txtC1: displays the die complexity hazard rate of the integrated
        circuit.
    :ivar txtPiT: displays the temperature factor for the integrated circuit.
    :ivar txtC2: displays the package failure rate for the integrated circuit.
    :ivar txtPiE: displays the environment factor for the integrated circuit.
    :ivar txtPiQ: displays the quality factor for the integrated circuit.
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

    # Define private class dict attributes.
    _dic_part_stress: Dict[int, str] = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        3:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        4:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        5:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + \u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        6:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + \u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        7:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + \u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        8:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + \u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        9:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>L</sub>\u03C0<sub>Q</sub></span>",
        10:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>BD</sub>\u03C0<sub>MFG</sub>\u03C0<sub>T</sub>\u03C0<sub>CD</sub> + \u03BB<sub>BP</sub>\u03C0<sub>E</sub>\u03C0<sub>Q</sub>\u03C0<sub>PT</sub> + \u03BB<sub>EOS</sub></span>"
    }

    # Define private class list attributes.
    _lst_tooltips = [
        _("The assessment model used to calculate the integrated circuit "
          "failure rate."),
        _("The base hazard rate of the integrated circuit."),
        _("The quality factor for the integrated circuit."),
        _("The environment factor for the integrated circuit."),
        _("The die complexity hazard rate of the integrated circuit."),
        _("The temperature factor for the integrated circuit."),
        _("The package hazard rate for the integrated circuit."),
        _("The construction factor for the integrated circuit."),
        _("The learning factor for the integrated circuit."),
        _("The read/write cycling induced hazard rate for the EEPROM."),
        _("The die base hazard rate for the VLSI device."),
        _("The manufacturing process correction factor for the VLSI "
          "device."),
        _("The die complexity correction factor for the VLSI device."),
        _("The package base hazard rate for the VLSI device."),
        _("The package type correction factor for the VLSI device."),
        _("The electrical overstress hazard rate for the VLSI device."),
        _("The application correction factor for the GaAs device.")
    ]

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'integrated_circuit') -> None:
        """
        Initialize an instance of the IC assessment result view.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param str module: the name of the RAMSTK workflow module.
        """
        super().__init__(configuration, logger, module=module)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append("C1:")
        self._lst_labels.append("\u03C0<sub>T</sub>:")
        self._lst_labels.append("C2:")
        self._lst_labels.append("\u03C0<sub>C</sub>")
        self._lst_labels.append("\u03C0<sub>L</sub>:")
        self._lst_labels.append("\u03BB<sub>CYC</sub>:")
        self._lst_labels.append("\u03BB<sub>BD</sub>")
        self._lst_labels.append("\u03C0<sub>MFG</sub>")
        self._lst_labels.append("\u03C0<sub>CD</sub>")
        self._lst_labels.append("\u03BB<sub>BP</sub>")
        self._lst_labels.append("\u03C0<sub>PT</sub>")
        self._lst_labels.append("\u03BB<sub>EOS</sub>")
        self._lst_labels.append("\u03C0<sub>A</sub>")

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtC1: RAMSTKEntry = RAMSTKEntry()
        self.txtPiT: RAMSTKEntry = RAMSTKEntry()
        self.txtC2: RAMSTKEntry = RAMSTKEntry()
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiL: RAMSTKEntry = RAMSTKEntry()
        self.txtLambdaCYC: RAMSTKEntry = RAMSTKEntry()
        self.txtLambdaBD: RAMSTKEntry = RAMSTKEntry()
        self.txtPiMFG: RAMSTKEntry = RAMSTKEntry()
        self.txtPiCD: RAMSTKEntry = RAMSTKEntry()
        self.txtLambdaBP: RAMSTKEntry = RAMSTKEntry()
        self.txtPiPT: RAMSTKEntry = RAMSTKEntry()
        self.txtLambdaEOS: RAMSTKEntry = RAMSTKEntry()
        self.txtPiA: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets.append(self.txtC1)
        self._lst_widgets.append(self.txtPiT)
        self._lst_widgets.append(self.txtC2)
        self._lst_widgets.append(self.txtPiC)
        self._lst_widgets.append(self.txtPiL)
        self._lst_widgets.append(self.txtLambdaCYC)
        self._lst_widgets.append(self.txtLambdaBD)
        self._lst_widgets.append(self.txtPiMFG)
        self._lst_widgets.append(self.txtPiCD)
        self._lst_widgets.append(self.txtLambdaBP)
        self._lst_widgets.append(self.txtPiPT)
        self._lst_widgets.append(self.txtLambdaEOS)
        self._lst_widgets.append(self.txtPiA)

        self.set_properties()
        self.make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')
        pub.subscribe(self._do_load_page, 'succeed_calculate_hardware')

    def __do_set_part_stress_sensitive(self) -> None:
        """
        Sets the widgets displaying MIL-HDBK-217F part stress info sensitive.

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

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the integrated circuit assessment results page.

        :param dict attributes: the attributes dictionary for the selected
            Integrated Circuit.
        :return: None
        :rtype: None
        """
        super().do_load_page(attributes)

        # TODO: See issue #305.
        self.txtC1.set_text(str(self.fmt.format(attributes['C1'])))
        self.txtPiT.set_text(str(self.fmt.format(attributes['piT'])))
        self.txtC2.set_text(str(self.fmt.format(attributes['C2'])))
        self.txtPiL.set_text(str(self.fmt.format(attributes['piL'])))
        self.txtLambdaCYC.set_text(
            str(self.fmt.format(attributes['lambdaCYC'])), )
        self.txtLambdaBD.set_text(str(self.fmt.format(attributes['lambdaBD'])))
        self.txtPiMFG.set_text(str(self.fmt.format(attributes['piMFG'])))
        self.txtPiCD.set_text(str(self.fmt.format(attributes['piCD'])))
        self.txtLambdaBP.set_text(str(self.fmt.format(attributes['lambdaBP'])))
        self.txtPiPT.set_text(str(self.fmt.format(attributes['piPT'])))
        self.txtLambdaEOS.set_text(
            str(self.fmt.format(attributes['lambdaEOS'])), )
        self.txtPiA.set_text(str(self.fmt.format(attributes['piA'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """
        Set widget sensitivity as needed for the selected integrated circuit.

        :return: None
        :rtype: None
        """
        super().do_set_sensitive()

        self.txtLambdaB.set_sensitive(False)
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
        elif self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Part Stress
            self.__do_set_part_stress_sensitive()
