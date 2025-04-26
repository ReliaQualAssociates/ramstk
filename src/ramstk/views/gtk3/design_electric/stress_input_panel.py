# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.stress_input_panel.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Design Electric stress input panel module."""

# Standard Library Imports
from typing import List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKEntry,
    RAMSTKFixedPanel,
    WidgetConfig,
    make_widget_config,
)


class StressInputPanel(RAMSTKFixedPanel):
    """Panel to display environmental data about the selected Hardware item.

    The widgets of a Design Electric electrical stress input panel are:

    :ivar txtTemperatureRatedMin: the RAMSTKEntry() used to input and display the
        minimum rated temperature of the selected hardware item.
    :ivar txtTemperatureKnee: the RAMSTKEntry() used to input and display the knee
        temperature of the selected hardware item.
    :ivar txtTemperatureRatedMax: the RAMSTKEntry() used to input and display the
        maximum rated temperature of the selected hardware item.
    :ivar txtCurrentRated: the RAMSTKEntry() used to input and display the rated
        current of the selected hardware item.
    :ivar txtCurrentOperating: the RAMSTKEntry() used to input and display the
        operating current of the selected hardware item.
    :ivar txtPowerRated: the RAMSTKEntry() used to input and display the rated power of
        the selected hardware item.
    :ivar txtPowerOperating: the RAMSTKEntry() used to input and display the
        operating power of the selected hardware item.
    :ivar txtVoltageRated: the RAMSTKEntry() used to input and display the rated
        voltage of the selected hardware item.
    :ivar txtVoltageAC: the RAMSTKEntry() used to input and display the operating AC
        voltage of the selected hardware item.
    :ivar txtVoltageDC: the RAMSTKEntry() used to input and display the operating DC
        voltage of the selected hardware item.
    """

    # Define private class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Hardware Thermal &amp; Electrical Stress Inputs")

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

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.txtTemperatureRatedMin,
                {
                    "datatype": "gfloat",
                    "default": 25.0,
                    "field": "temperature_rated_min",
                    "index": 45,
                    "label_text": _("Minimum Rated Temperature (\u00b0C):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "tooltip": _(
                        "The minimum rated temperature (in \u00b0C) of the hardware "
                        "item."
                    ),
                    "width_request": 125,
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtTemperatureKnee,
                {
                    "datatype": "gfloat",
                    "default": 25.0,
                    "field": "temperature_knee",
                    "index": 43,
                    "label_text": _("Knee Temperature (\u00b0C):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "tooltip": _(
                        "The break temperature (in \u00b0C) of the hardware item "
                        "beyond which it must be derated."
                    ),
                    "width_request": 125,
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtTemperatureRatedMax,
                {
                    "datatype": "gfloat",
                    "default": 25.0,
                    "field": "temperature_rated_max",
                    "index": 44,
                    "label_text": _("Maximum Rated Temperature (\u00b0C):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "tooltip": _(
                        "The maximum rated temperature (in \u00b0C) of the hardware "
                        "item."
                    ),
                    "width_request": 125,
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtCurrentRated,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "current_rated",
                    "index": 11,
                    "label_text": _("Rated Current (A):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "tooltip": _("The rated current (in A) of the hardware item."),
                    "width_request": 125,
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtCurrentOperating,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "current_operating",
                    "index": 10,
                    "label_text": _("Operating Current (A):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "tooltip": _("The operating current (in A) of the hardware item."),
                    "width_request": 200,
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPowerRated,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "power_rated",
                    "index": 32,
                    "label_text": _("Rated Power (W):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "tooltip": _("The rated power (in W) of the hardware item."),
                    "width_request": 125,
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPowerOperating,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "power_operating",
                    "index": 31,
                    "label_text": _("Operating Power (W):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "tooltip": _("The operating power (in W) of the hardware item."),
                    "width_request": 200,
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtVoltageRated,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "voltage_rated",
                    "index": 52,
                    "label_text": _("Rated Voltage (V):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "tooltip": _("The rated voltage (in V) of the hardware item."),
                    "width_request": 125,
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtVoltageAC,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "voltage_ac_operating",
                    "index": 49,
                    "label_text": _("Operating ac Voltage (V):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "tooltip": _(
                        "The operating ac voltage (in V) of the hardware item."
                    ),
                    "width_request": 125,
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtVoltageDC,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "voltage_dc_operating",
                    "index": 50,
                    "label_text": _("Operating DC Voltage (V):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "tooltip": _(
                        "The operating DC voltage (in V) of the hardware item."
                    ),
                    "width_request": 125,
                    "editable": True,
                    "visible": True,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_fixed_panel()
        super().do_set_widget_callbacks()
