# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.stress_results_panel.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Design Electric stress results panel module."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    RAMSTKPlot,
    RAMSTKScrolledWindow,
    RAMSTKTextView,
    WidgetConfig,
    make_widget_config,
)


class StressResultPanel(RAMSTKFixedPanel):
    """Display Hardware stress results attribute data in the RAMSTK Work Book.

    The widgets of a Design Electric electrical stress results panel are:

    :ivar chkOverstress: the RAMSTKCheckButton() used to indicate whether the selected
        hardware item is electrically or thermally overstressed.
    :ivar pltPlot: the RAMSTKPlot() used to display the derating curve and operating
        point of the selected component.
    :ivar txtCurrentRatio: the RAMSTKEntry() used to display the ratio of operating
        to rated current for the selected component.
    :ivar txtPowerRatio: the RAMSTKEntry() used to display the ratio of operating to
        rated power for the selected component.
    :ivar txtVoltageRatio: the RAMSTKEntry() used to display the ratio of operating
        to rated voltage for the selected component.
    :ivar txtReason: the RAMSTKTextView() used to display the reason(s), if any,
        the selected hardware item is overstressed.

    The attributes of a Design Electric electrical stress results panel are:

    :ivar list _lst_derate_criteria: the derating criteria for the selected component.
    :ivar _category_id: the hardware category ID of the selected component.
    :ivar _part_number: the part number of the selected component.
    :ivar _ref_des: the reference designator of the selected component.
    """

    # Define private class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Hardware Thermal &amp; Electrical Stress Summary")

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

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.txtCurrentRatio,
                {
                    "datatype": "gfloat",
                    "default": 0.5,
                    "field": "current_ratio",
                    "index": 12,
                    "label_text": _("Current Ratio:"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "The ratio of operating current to rated current for the "
                        "hardware item."
                    ),
                    "width_request": 125,
                    "editable": False,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPowerRatio,
                {
                    "datatype": "gfloat",
                    "default": 0.5,
                    "field": "power_ratio",
                    "index": 33,
                    "label_text": _("Power Ratio:"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "The ratio of operating power to rated power for the hardware "
                        "item."
                    ),
                    "width_request": 125,
                    "editable": False,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtVoltageRatio,
                {
                    "datatype": "gfloat",
                    "default": 0.5,
                    "field": "voltage_ratio",
                    "index": 53,
                    "label_text": _("Voltage Ratio:"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "The ratio of operating voltage to rated voltage for the "
                        "hardware item."
                    ),
                    "width_request": 125,
                    "editable": False,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkOverstress,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "overstressed",
                    "index": 29,
                    "label_text": "",
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "Indicates whether or not the selected hardware item is "
                        "overstressed."
                    ),
                    "width_request": 125,
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtReason,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "reason",
                    "index": 34,
                    "label_text": _("Overstress Reason:"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                {
                    "tooltip": _(
                        "The reason(s) the selected hardware item is overstressed."
                    ),
                    "width_request": 350,
                    "editable": False,
                    "visible": True,
                },
            ),
        ]
        self._lst_derate_criteria: List[List[float]] = [
            [0.6, 0.6, 0.0],
            [0.9, 0.9, 0.0],
        ]
        self._category_id: int = 0
        self._part_number: str = ""
        self._ref_des: str = ""

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {"selected_hardware": self._do_set_hardware_attributes}
        )

    def _do_load_derating_curve(
        self, attributes: Dict[str, Any], stress: str = "voltage"
    ) -> None:
        """Load the benign and harsh environment derating curves."""
        self.pltPlot.axis.cla()

        _x = [
            float(attributes["temperature_rated_min"]),
            float(attributes["temperature_knee"]),
            float(attributes["temperature_rated_max"]),
        ]

        self.pltPlot.axis.grid(True, which="both")

        self.pltPlot.do_load_plot(
            x_values=_x,
            y_values=self._lst_derate_criteria[0],
            marker="r.-",
            plot_type="step",
        )

        self.pltPlot.do_add_line(
            x_values=_x,
            y_values=self._lst_derate_criteria[1],
            color="b",
            marker=".-",
        )

        self.pltPlot.do_add_line(
            x_values=[attributes["temperature_active"]],
            y_values=[attributes[f"{stress}_ratio"]],
            color="g",
            marker="o",
        )

        self.pltPlot.do_make_title(
            _(
                f"{stress.title()} Derating Curve for {self._part_number} at "
                f"{self._ref_des}"
            ),
            {
                "font_size": 12,
            },
        )

        self.pltPlot.do_make_legend(
            [
                _("Harsh Environment"),
                _("Mild Environment"),
            ],
            _(f"{stress.title()} Operating Point"),
            {},
        )

        self.pltPlot.do_make_labels(
            _("Temperature (\u2070C)"),
            {
                "font_size": 10,
            },
            x_pos=0,
            y_pos=-0.2,
        )
        self.pltPlot.do_make_labels(
            _(f"{stress.title()} Ratio"),
            {
                "font_size": 10,
            },
            set_x=False,
            x_pos=-1,
            y_pos=0,
        )

        self.pltPlot.figure.canvas.draw()

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load the stress results page widgets.

        :param attributes: the attribute dict for the selected Hardware.
        """
        self.txtCurrentRatio.do_update(
            {"current_ratio": str(self.fmt.format(attributes["current_ratio"] or 0.0))}
        )
        self.txtPowerRatio.do_update(
            {"power_ratio": str(self.fmt.format(attributes["power_ratio"] or 0.0))}
        )
        self.txtVoltageRatio.do_update(
            {"voltage_ratio": str(self.fmt.format(attributes["voltage_ratio"] or 0.0))}
        )
        self.chkOverstress.set_active(
            {"overstress": int(attributes["overstress"] or 0)}
        )
        self.txtReason.do_update({"reason": str(attributes["reason"] or "")})

        if self._category_id in [2, 4]:
            self._do_load_derating_curve(attributes, stress="voltage")
        elif self._category_id == 3:
            self._do_load_derating_curve(attributes, stress="power")
        elif self._category_id in [6, 7]:
            self._do_load_derating_curve(attributes, stress="current")
        else:
            self.pltPlot.axis.cla()

    def _do_set_hardware_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        """
        self._category_id = attributes["category_id"]
        self._part_number = attributes["part_number"]
        self._ref_des = attributes["ref_des"]

    def __make_ui(self) -> None:
        """Make the Hardware stress results page."""
        _scrollwindow: RAMSTKScrolledWindow = self.get_child()
        self.remove(self.get_child())

        _hpaned: Gtk.HPaned = Gtk.HPaned()
        self.add(_hpaned)

        _hpaned.pack1(_scrollwindow, False, False)

        _scrollwindow = RAMSTKScrolledWindow(self.pltPlot.canvas)
        _hpaned.pack2(_scrollwindow, False, False)

        self.show_all()
