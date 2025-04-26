# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.environmental_input_panel.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Design Electric environmental input panel module."""

# Standard Library Imports
from typing import List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    WidgetConfig,
    make_widget_config,
)


class EnvironmentalInputPanel(RAMSTKFixedPanel):
    """Panel to display environmental data about the selected hardware item.

    The widgets of a Design Electric environmental input panel are:

    :ivar cmbActiveEnviron: the RAMSTKComboBox() used to select the active (operating)
        environment for the selected hardware item.  These are the MIL-HDBK-217
        environments.
    :ivar cmbDormantEnviron: the RAMSTKComboBox() used to select the dormant (storage)
        environment for the selected hardware item.  These are the MIL-HDBK-338
        environments.
    :ivar txtActiveTemp: the RAMSTKEntry() used to input and display the active
        (operating) temperature of the selected hardware item.
    :ivar txtDormantTemp: the RAMSTKEntry() used to input and display the dormant
        (storage) temperature of the selected hardware item.
    :ivar txtDutyCycle: the RAMSTKEntry() used to input and display the duty cycle of
        the selected hardware item.
    :ivar txtMissionTime: the RAMSTKEntry() used to input and display the mission
        time of the selected hardware item.
    """

    # Define private class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Hardware Environmental Inputs")

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

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.cmbActiveEnviron,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "active_environment_id",
                    "index": 12,
                    "label_text": _("Active Environment:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                {
                    "editable": True,
                    "tooltip": _("The operating environment for the hardware item."),
                    "visible": True,
                    "width_request": 200,
                },
            ),
            make_widget_config(
                self.txtActiveTemp,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "temperature_active",
                    "index": 37,
                    "label_text": _("Active Temperature (\u00b0C):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The ambient temperature in the operating environment."
                    ),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.cmbDormantEnviron,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "environment_dormant_id",
                    "index": 13,
                    "label_text": _("Dormant Environment:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The storage environment for the hardware item."),
                    "visible": True,
                    "width_request": 200,
                },
            ),
            make_widget_config(
                self.txtDormantTemp,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "temperature_dormant",
                    "index": 39,
                    "label_text": _("Dormant Temperature (\u00b0C):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The ambient temperature in the storage environment."),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtMissionTime,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "mission_time",
                    "index": 14,
                    "label_text": _("Mission Time:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The mission time of the selected hardware item."),
                    "visible": True,
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtDutyCycle,
                {
                    "datatype": "gfloat",
                    "default": 100.0,
                    "field": "duty_cycle",
                    "index": 9,
                    "label_text": _("Duty Cycle:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The duty cycle of the selected hardware item."),
                    "visible": True,
                    "width_request": 125,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_fixed_panel()
        super().do_set_widget_callbacks()

    def do_load_environment_active(self, environments: List[List[str]]) -> None:
        """Load the active environments RAMSTKComboBox().

        :param environments: the list of active environments.
        """
        self.cmbActiveEnviron.do_load_combo(environments)

    def do_load_environment_dormant(self, environments: List[List[str]]) -> None:
        """Load the dormant environments RAMSTKComboBox().

        :param environments: the list of dormant environments.
        """
        self.cmbDormantEnviron.do_load_combo(environments)
