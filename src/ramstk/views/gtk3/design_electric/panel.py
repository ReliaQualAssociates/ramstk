# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Design Electric Panels."""

# Standard Library Imports
from typing import List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    RAMSTKScrolledWindow,
)


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
        self.scwDesignRatings: RAMSTKScrolledWindow = RAMSTKScrolledWindow(None)
        self.txtActiveTemp: RAMSTKEntry = RAMSTKEntry()
        self.txtDormantTemp: RAMSTKEntry = RAMSTKEntry()
        self.txtDutyCycle: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionTime: RAMSTKEntry = RAMSTKEntry()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_index_map = {
            9: ["duty_cycle", "float"],
            12: ["environment_active_id", "integer"],
            13: ["environment_dormant_id", "integer"],
            14: ["mission_time", "float"],
            37: ["temperature_active", "float"],
            39: ["temperature_dormant", "float"],
        }
        self.dic_attribute_widget_map = {
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
