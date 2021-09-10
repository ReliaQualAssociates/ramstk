# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Design Electric Panels."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry, RAMSTKFixedPanel


class DesignElectricEnvironmentalInputPanel(RAMSTKFixedPanel):
    """Panel to display environmental data about the selected Hardware item."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "selected_hardware"
    _tag = "design_electric"
    _title = _("Hardware Environmental Inputs")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Environmental Input panel."""
        super().__init__()

        # Initialize widgets.
        self.cmbActiveEnviron: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbDormantEnviron: RAMSTKComboBox = RAMSTKComboBox()
        self.txtActiveTemp: RAMSTKEntry = RAMSTKEntry()
        self.txtDormantTemp: RAMSTKEntry = RAMSTKEntry()
        self.txtDutyCycle: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionTime: RAMSTKEntry = RAMSTKEntry()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_index_map: Dict[int, List[str]] = {
            9: ["duty_cycle", "float"],
            12: ["environment_active_id", "integer"],
            13: ["environment_dormant_id", "integer"],
            14: ["mission_time", "float"],
            37: ["temperature_active", "float"],
            39: ["temperature_dormant", "float"],
        }
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "environment_active_id": [
                12,
                self.cmbActiveEnviron,
                "changed",
                super().on_changed_combo,
                "wvw_editing_hardware",
                0.0,
                {
                    "tooltip": _("The operating environment for the hardware item."),
                    "width": 200,
                },
                _("Active Environment:"),
            ],
            "temperature_active": [
                37,
                self.txtActiveTemp,
                "changed",
                super().on_changed_entry,
                "wvw_editing_hardware",
                0.0,
                {
                    "tooltip": _(
                        "The ambient temperature in the operating environment."
                    ),
                    "width": 125,
                },
                _("Active Temperature (\u00B0C):"),
            ],
            "environment_dormant_id": [
                13,
                self.cmbDormantEnviron,
                "changed",
                super().on_changed_combo,
                "wvw_editing_hardware",
                0.0,
                {
                    "tooltip": _("The storage environment for the hardware item."),
                    "width": 200,
                },
                _("Dormant Environment:"),
            ],
            "temperature_dormant": [
                39,
                self.txtDormantTemp,
                "changed",
                super().on_changed_entry,
                "wvw_editing_hardware",
                0.0,
                {
                    "tooltip": _("The ambient temperature in the storage environment."),
                    "width": 125,
                },
                _("Dormant Temperature (\u00B0C):"),
            ],
            "mission_time": [
                14,
                self.txtMissionTime,
                "changed",
                super().on_changed_entry,
                "wvw_editing_hardware",
                1.0,
                {
                    "tooltip": _("The mission time of the selected hardware item."),
                    "width": 125,
                },
                _("Mission Time:"),
            ],
            "duty_cycle": [
                9,
                self.txtDutyCycle,
                "changed",
                super().on_changed_entry,
                "mvw_editing_hardware",
                100.0,
                {
                    "tooltip": _("The duty cycle of the selected hardware item."),
                    "width": 125,
                },
                _("Duty Cycle:"),
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        # Make a fixed type panel.
        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.

    def do_load_environment_active(self, environments: List[str]) -> None:
        """Load the active environments RAMSTKComboBox().

        :param environments: the list of active environments.
        :return: None
        """
        self.cmbActiveEnviron.do_load_combo(entries=environments)

    def do_load_environment_dormant(self, environments: List[str]) -> None:
        """Load the dormant environments RAMSTKComboBox().

        :param environments: the list of dormant environments.
        :return: None
        """
        self.cmbDormantEnviron.do_load_combo(entries=environments)


class DesignElectricStressInputPanel(RAMSTKFixedPanel):
    """Panel to display environmental data about the selected Hardware item."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "selected_hardware"
    _tag = "design_electric"
    _title = _("Hardware Thermal &amp; Electrical Stress Inputs")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Stress Input panel."""
        super().__init__()

        # Initialize widgets.
        self.txtTemperatureRatedMin: RAMSTKEntry = RAMSTKEntry()
        self.txtTemperatureKnee: RAMSTKEntry = RAMSTKEntry()
        self.txtTemperatureRatedMax: RAMSTKEntry = RAMSTKEntry()
        self.txtCurrentRated: RAMSTKEntry = RAMSTKEntry()
        self.txtCurrentOperating: RAMSTKEntry = RAMSTKEntry()
        self.txtPowerRated: RAMSTKEntry = RAMSTKEntry()
        self.txtPowerOperating: RAMSTKEntry = RAMSTKEntry()
        self.txtVoltageRated: RAMSTKEntry = RAMSTKEntry()
        self.txtVoltageAC: RAMSTKEntry = RAMSTKEntry()
        self.txtVoltageDC: RAMSTKEntry = RAMSTKEntry()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_index_map: Dict[int, List[str]] = {
            10: ["current_operating", "float"],
            11: ["current_rated", "float"],
            31: ["power_operating", "float"],
            32: ["power_rated", "float"],
            43: ["temperature_knee", "float"],
            44: ["temperature_rated_max", "float"],
            45: ["temperature_rated_min", "float"],
            49: ["voltage_ac_operating", "float"],
            50: ["voltage_dc_operating", "float"],
            52: ["voltage_rated", "float"],
        }
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "temperature_rated_min": [
                45,
                self.txtTemperatureRatedMin,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                25.0,
                {
                    "tooltip": _(
                        "The minimum rated temperature (in \u00B0C) of the hardware "
                        "item."
                    ),
                    "width": 125,
                },
                _("Minimum Rated Temperature (\u00B0C):"),
            ],
            "temperature_knee": [
                43,
                self.txtTemperatureKnee,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                25.0,
                {
                    "tooltip": _(
                        "The break temperature (in \u00B0C) of the hardware item "
                        "beyond which it must be derated."
                    ),
                    "width": 125,
                },
                _("Knee Temperature (\u00B0C):"),
            ],
            "temperature_rated_max": [
                44,
                self.txtTemperatureRatedMax,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                25.0,
                {
                    "tooltip": _(
                        "The maximum rated temperature (in \u00B0C) of the hardware "
                        "item."
                    ),
                    "width": 125,
                },
                _("Maximum Rated Temperature (\u00B0C):"),
            ],
            "current_rated": [
                11,
                self.txtCurrentRated,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                0.0,
                {
                    "tooltip": _("The rated current (in A) of the hardware item."),
                    "width": 125,
                },
                _("Rated Current (A):"),
            ],
            "current_operating": [
                10,
                self.txtCurrentOperating,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                0.0,
                {
                    "tooltip": _("The operating current (in A) of the hardware item."),
                    "width": 200,
                },
                _("Operating Current (A):"),
            ],
            "power_rated": [
                32,
                self.txtPowerRated,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                0.0,
                {
                    "tooltip": _("The rated power (in W) of the hardware item."),
                    "width": 125,
                },
                _("Rated Power (W):"),
            ],
            "power_operating": [
                31,
                self.txtPowerOperating,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                0.0,
                {
                    "tooltip": _("The operating power (in W) of the hardware item."),
                    "width": 200,
                },
                _("Operating Power (W):"),
            ],
            "voltage_rated": [
                52,
                self.txtVoltageRated,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                0.0,
                {
                    "tooltip": _("The rated voltage (in V) of the hardware item."),
                    "width": 125,
                },
                _("Rated Voltage (V):"),
            ],
            "voltage_ac_operating": [
                49,
                self.txtVoltageAC,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                0.0,
                {
                    "tooltip": _(
                        "The operating ac voltage (in V) of the hardware item."
                    ),
                    "width": 125,
                },
                _("Operating ac Voltage (V):"),
            ],
            "voltage_dc_operating": [
                50,
                self.txtVoltageDC,
                "changed",
                super().on_changed_entry,
                "wvw_editing_design_electric",
                0.0,
                {
                    "tooltip": _(
                        "The operating DC voltage (in V) of the hardware item."
                    ),
                    "width": 125,
                },
                _("Operating DC Voltage (V):"),
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        # Make a fixed type panel.
        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
