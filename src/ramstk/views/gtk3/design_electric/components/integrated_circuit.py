# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.components.integrated_circuit.py is part of
#       the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""THe Integrated Circuit input panel module."""


# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.constants.integrated_circuit import IC_TECHNOLOGY_DICT, IC_TYPE_DICT
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    WidgetConfig,
)


class ICDesignElectricInputPanel(RAMSTKFixedPanel):
    """Display IC assessment input attribute data in the RAMSTK Work Book.

    The Integrated Circuit assessment input view displays all the assessment
    inputs for the selected integrated circuit.  This includes, currently,
    inputs for MIL-HDBK-217FN2.  The attributes of an integrated circuit
    assessment input view are:

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

    # Define private class attributes.
    _record_field = "hardware_id"
    _select_msg = "succeed_get_design_electric_attributes"
    _tag = "design_electric"
    _title = _("Integrated Circuit Design Inputs")

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
                    "listen_topic": "mvw_editing_reliability",
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The quality level of the integrated circuit."),
                    "visible": True,
                },
            },
            {
                "widget": self.cmbPackage,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "package_id",
                    "index": 30,
                    "label_text": _("Package:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The type of package housing the integrated circuit."),
                    "visible": True,
                },
            },
            {
                "widget": self.txtArea,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "area",
                    "index": 3,
                    "label_text": _("Die Area:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "The die area (in mil<sup>2</sup>) of the integrated circuit."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtNElements,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "n_elements",
                    "index": 25,
                    "label_text": _("N Elements:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "The number of active elements in the integrated circuit."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtThetaJC,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "theta_jc",
                    "index": 47,
                    "label_text": _("\u0398<sub>JC</sub>:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The junction to case thermal resistance."),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtNActivePins,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "n_active_pins",
                    "index": 22,
                    "label_text": _("Active Pins:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "The number of active pins on the integrated circuit."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.cmbTechnology,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "technology_id",
                    "index": 37,
                    "label_text": _("Technology:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "The technology used to construct the integrated circuit."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.txtYearsInProduction,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 2,
                    "field": "years_in_production",
                    "index": 55,
                    "label_text": _("Years in Production:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "The number of years the generic device type has been in "
                        "production."
                    ),
                    "visible": True,
                    "width": 125,
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
                    "tooltip": _(
                        "The method of construction of the integrated circuit."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.txtNCycles,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "n_cycles",
                    "index": 24,
                    "label_text": _("Programming Cycles:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "The total number of programming cycles over the EEPROM life."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtOperatingLife,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "operating_life",
                    "index": 28,
                    "label_text": _("Operating Life:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The system lifetime operating hours."),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.cmbECC,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "family_id",
                    "index": 15,
                    "label_text": _("Error Correction Code:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The error correction code used by the EEPROM."),
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
                    "tooltip": _("The application of the integrated circuit."),
                    "visible": True,
                },
            },
            {
                "widget": self.cmbType,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "type_id",
                    "index": 48,
                    "label_text": _("Device Type:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The type of GaAs or VLSI device."),
                    "visible": True,
                },
            },
            {
                "widget": self.txtFeatureSize,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "feature_size",
                    "index": 16,
                    "label_text": _("Feature Size:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The feature size (in microns) of the VLSI device."),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.cmbManufacturing,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "manufacturing_id",
                    "index": 20,
                    "label_text": _("Manufacturing Process:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The manufacturing process for the VLSI device."),
                    "visible": True,
                },
            },
            {
                "widget": self.txtVoltageESD,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "voltage_esd",
                    "index": 51,
                    "label_text": _("ESD Threshold Voltage:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "The ESD susceptibility threshold voltage of the VLSI device."
                    ),
                    "visible": True,
                    "width": 125,
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
        self._do_load_construction()
        self._do_load_ecc()
        self._do_load_manufacturing()
        self._do_load_package()
        self._do_load_quality()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "changed_subcategory": self.on_subcategory_change,
                "succeed_get_reliability_attributes": self._set_reliability_attributes,
            }
        )

    # pylint: disable=unused-argument
    def on_subcategory_change(self, subcategory_id: int) -> None:
        """Load the integrated circuit subcategory-specific RAMSTKComboBoxes.

        :param subcategory_id: the subcategory ID of the selected IC. This is unused in
            this method but required because this method is a PyPubSub listener.
        """
        self.subcategory_id = subcategory_id

        self.cmbTechnology.do_load_combo(
            self._get_technology_list(),
        )
        self.cmbType.do_load_combo(
            IC_TYPE_DICT.get(self.subcategory_id, []),
        )

        self._set_sensitive()

    def _do_load_application(self, attributes: Dict[str, Any]) -> None:
        """Load the IC application RAMSTKComboBox.

        :param attributes: the attributes dict for the selected integrated circuit.
        """
        self.cmbApplication.do_load_combo(
            self._get_application_list(attributes["construction_id"]),
        )

    def _do_load_construction(self) -> None:
        """Load the IC construction RAMSTKComboBox."""
        self.cmbConstruction.do_load_combo(
            [
                ["FLOTOX"],
                [_("Textured Poly")],
            ],
        )

    def _do_load_ecc(self) -> None:
        """Load the IC ECC RAMSTKComboBox."""
        self.cmbECC.do_load_combo(
            [
                [_("No on-chip ECC")],
                [_("On-chip Hamming code")],
                [_("Two-Needs-One redundant cell approach")],
            ],
        )

    def _do_load_manufacturing(self) -> None:
        """Load the IC manufacturing RAMSTKComboBox."""
        self.cmbManufacturing.do_load_combo(
            [
                ["QML or QPL"],
                ["Non-QML or non-QPL"],
            ],
        )

    def _do_load_package(self) -> None:
        """Load the IC package RAMSTKComboBox."""
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
        )

    def _do_load_quality(self) -> None:
        """Load the IC quality RAMSTKComboBox."""
        self.cmbQuality.do_load_combo(
            [
                [_("Class S")],
                [_("Class B")],
                [_("Class B-1")],
            ],
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
            return IC_TECHNOLOGY_DICT.get(self.subcategory_id, [])
        except KeyError:
            return []

    def _set_reliability_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        """
        self._hazard_rate_method_id = int(attributes["hazard_rate_method_id"])
        self._quality_id = int(attributes["quality_id"])

        self._set_sensitive()
        super().do_set_widget_sensitivity([self.cmbQuality])
        self.cmbQuality.do_update(
            {"quality_id": self._quality_id},
        )

    def _set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected IC."""
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
        super().do_set_widget_sensitivity(_sensitivity_map.get(self.subcategory_id, []))

        # For Part Stress, add extra sensitivity.
        if self._hazard_rate_method_id == 2:
            super().do_set_widget_sensitivity(
                [
                    self.cmbPackage,
                    self.txtThetaJC,
                    self.txtNElements,
                ]
            )
