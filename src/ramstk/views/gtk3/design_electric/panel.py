# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Design Electric Panels."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton,
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    RAMSTKPlot,
    RAMSTKScrolledWindow,
    RAMSTKTextView,
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
        self.txtActiveTemp: RAMSTKEntry = RAMSTKEntry()
        self.txtDormantTemp: RAMSTKEntry = RAMSTKEntry()
        self.txtDutyCycle: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionTime: RAMSTKEntry = RAMSTKEntry()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
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
                "gint",
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
                "gfloat",
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
                "gint",
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
                "gfloat",
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
                "gfloat",
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
                "gfloat",
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
                "gfloat",
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
                "gfloat",
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
                "gfloat",
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
                "gfloat",
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
                "gfloat",
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
                "gfloat",
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
                "gfloat",
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
                "gfloat",
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
                "gfloat",
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
                "gfloat",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        # Make a fixed type panel.
        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.


class DesignElectricStressResultPanel(RAMSTKFixedPanel):
    """Display Hardware stress results attribute data in the RAMSTK Work Book.

    The Hardware stress result view displays all the stress results for the
    selected hardware item.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and part stress methods.  The attributes of a
    Hardware stress result view are:

    :cvar list _lst_labels: the text to use for the stress results widget
        labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
        displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the hardware item
        currently being displayed.

    :ivar str fmt: the format string for displaying numbers.

    :ivar chkOverstressed: display whether or not the selected hardware item is
        overstressed.
    :ivar pltDerate: displays the derating curves and the design operating
        point relative to those curves.
    :ivar txtCurrentRatio: display the ratio of operating current to rated
        current.
    :ivar txtPowerRatio: display the ratio of operating power to rated power.
    :ivar txtVoltageRatio: display the ratio of operating voltage (ac + DC) to
        rated voltage.
    :ivar txtReason: display the reason(s) the hardware item is overstressed.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "selected_hardware"
    _tag = "design_electric"
    _title = _("Hardware Thermal &amp; Electrical Stress Summary")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Hardware stress result view."""
        super().__init__()

        # Initialize widgets.
        self.chkOverstress: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Overstressed")
        )
        self.pltPlot: RAMSTKPlot = RAMSTKPlot()
        self.txtCurrentRatio: RAMSTKEntry = RAMSTKEntry()
        self.txtPowerRatio: RAMSTKEntry = RAMSTKEntry()
        self.txtVoltageRatio: RAMSTKEntry = RAMSTKEntry()
        self.txtReason: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_derate_criteria: List[List[float]] = [
            [0.6, 0.6, 0.0],
            [0.9, 0.9, 0.0],
        ]

        # Initialize private scalar attributes.
        self._category_id: int = 0
        self._part_number: str = ""
        self._ref_des: str = ""

        # Initialize public dictionary attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "current_ratio": [
                12,
                self.txtCurrentRatio,
                "",
                None,
                "",
                0.5,
                {
                    "bold": True,
                    "editable": False,
                    "tooltip": _(
                        "The ratio of operating current to rated current for the "
                        "hardware item."
                    ),
                    "width": 125,
                },
                _("Current Ratio:"),
                "gfloat",
            ],
            "power_ratio": [
                33,
                self.txtPowerRatio,
                "",
                None,
                "",
                0.5,
                {
                    "bold": True,
                    "editable": False,
                    "tooltip": _(
                        "The ratio of operating power to rated power for the "
                        "hardware item."
                    ),
                    "width": 125,
                },
                _("Power Ratio:"),
                "gfloat",
            ],
            "voltage_ratio": [
                53,
                self.txtVoltageRatio,
                "",
                None,
                "",
                0.5,
                {
                    "bold": True,
                    "editable": False,
                    "tooltip": _(
                        "The ratio of operating voltage to rated voltage for the "
                        "hardware item."
                    ),
                    "width": 125,
                },
                _("Voltage Ratio:"),
                "gfloat",
            ],
            "overstressed": [
                29,
                self.chkOverstress,
                "",
                None,
                "",
                0,
                {
                    "tooltip": _(
                        "Indicates whether or not the selected hardware item is "
                        "overstressed."
                    ),
                    "width": 125,
                },
                "",
                "gint",
            ],
            "reason": [
                34,
                self.txtReason,
                "",
                None,
                "",
                "",
                {
                    "bold": True,
                    "editable": False,
                    "tooltip": _(
                        "The reason(s) the selected hardware item is overstressed."
                    ),
                    "width": 350,
                },
                _("Overstress Reason:"),
                "gchararray",
            ],
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().do_set_properties()
        super().do_make_panel()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self._do_set_hardware_attributes,
            "succeed_get_hardware_attributes",
        )

    def _do_load_derating_curve(
        self, attributes: Dict[str, Any], stress: str = "voltage"
    ) -> None:
        """Load the benign and harsh environment derating curves.

        :return: None
        :rtype: None
        """
        self.pltPlot.axis.cla()

        _x = [
            float(attributes["temperature_rated_min"]),
            float(attributes["temperature_knee"]),
            float(attributes["temperature_rated_max"]),
        ]

        self.pltPlot.axis.grid(True, which="both")

        self.pltPlot.do_load_plot(
            x_values=_x, y_values=self._lst_derate_criteria[0], marker="r.-"
        )

        self.pltPlot.do_load_plot(
            x_values=_x, y_values=self._lst_derate_criteria[1], marker="b.-"
        )

        self.pltPlot.do_load_plot(
            x_values=[attributes["temperature_active"]],
            y_values=[attributes["{}_ratio".format(stress)]],
            marker="go",
        )

        self.pltPlot.do_make_title(
            _("{2} Derating Curve for {0} at {1}").format(
                self._part_number, self._ref_des, stress.title()
            ),
            fontsize=12,
        )

        self.pltPlot.do_make_legend(
            (
                _("Harsh Environment"),
                _("Mild Environment"),
                _("{} Operating Point").format(stress.title()),
            )
        )

        self.pltPlot.do_make_labels(
            _("Temperature (\u2070C)"), x_pos=0, y_pos=-0.2, fontsize=10
        )
        self.pltPlot.do_make_labels(
            _("{} Ratio").format(stress.title()),
            x_pos=-1,
            y_pos=0,
            set_x=False,
            fontsize=10,
        )

        self.pltPlot.figure.canvas.draw()

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load the stress results page widgets.

        :param attributes: the attributes dict for the selected Hardware.
        :return: None
        :rtype: None
        """
        self.txtCurrentRatio.do_update(
            str(self.fmt.format(attributes["current_ratio"]))
        )
        self.txtPowerRatio.do_update(str(self.fmt.format(attributes["power_ratio"])))
        self.txtVoltageRatio.do_update(
            str(self.fmt.format(attributes["voltage_ratio"]))
        )
        self.chkOverstress.set_active(attributes["overstress"])
        self.txtReason.do_update(attributes["reason"])

        if self._category_id in [2, 4]:
            self._do_load_derating_curve(attributes, stress="voltage")
        elif self._category_id == 3:
            self._do_load_derating_curve(attributes, stress="power")
        elif self._category_id in [6, 7]:
            self._do_load_derating_curve(attributes, stress="current")

    def _do_set_hardware_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        :return: None
        :rtype: None
        """
        if attributes["hardware_id"] == self._record_id:
            self._category_id = attributes["category_id"]
            self._part_number = attributes["part_number"]
            self._ref_des = attributes["ref_des"]

    def __make_ui(self) -> None:
        """Make the Hardware stress results page.

        :return: None
        :rtype: None
        """
        _scrollwindow: RAMSTKScrolledWindow = self.get_child()
        self.remove(self.get_child())

        _hpaned: Gtk.HPaned = Gtk.HPaned()
        self.add(_hpaned)

        _hpaned.pack1(_scrollwindow, False, False)

        _scrollwindow = RAMSTKScrolledWindow(self.pltPlot.canvas)
        _hpaned.pack2(_scrollwindow, False, False)

        self.show_all()
