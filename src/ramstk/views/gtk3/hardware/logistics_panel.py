# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.logistics_panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The HardwareLogisticsPanel module."""

# Standard Library Imports
from datetime import date
from typing import Dict, List, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    WidgetConfig,
    make_widget_config,
)


class HardwareLogisticsPanel(RAMSTKFixedPanel):
    """Panel to display general data about the selected Hardware task."""

    # Define private class attributes.
    _record_field = "hardware_id"
    _select_msg = "selected_hardware"
    _tag = "hardware"
    _title = _("Hardware Logistics Information")

    def __init__(self) -> None:
        """Initialize an instance of the Hardware Task Description panel."""
        super().__init__()

        # Initialize widgets.
        self.cmbCostType: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbManufacturer: RAMSTKComboBox = RAMSTKComboBox(
            simple=False,
            n_items=3,
        )
        self.txtCAGECode: RAMSTKEntry = RAMSTKEntry()
        self.txtCost: RAMSTKEntry = RAMSTKEntry()
        self.txtNSN: RAMSTKEntry = RAMSTKEntry()
        self.txtQuantity: RAMSTKEntry = RAMSTKEntry()
        self.txtYearMade: RAMSTKEntry = RAMSTKEntry()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.cmbManufacturer,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "manufacturer_id",
                    "index": 13,
                    "label_text": _("Manufacturer:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _("The manufacturer of the selected hardware item."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtCAGECode,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "cage_code",
                    "index": 3,
                    "label_text": _("CAGE Code:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The Commercial and Government Entity (CAGE) Code of the "
                        "selected hardware item."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtNSN,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "nsn",
                    "index": 3,
                    "label_text": _("NSN:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The National Stock Number (NSN) of the selected hardware item."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtYearMade,
                {
                    "datatype": "gchararray",
                    "default": date.today().year - 2,
                    "field": "year_of_manufacture",
                    "index": 29,
                    "label_text": _("Year Introduced:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The year the selected hardware item was introduced to "
                        "the market."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtQuantity,
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "quantity",
                    "index": 21,
                    "label_text": _("Quantity:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The number of the selected hardware items in the design."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtCost,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost",
                    "index": 5,
                    "label_text": _("Unit Cost:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _("The unit cost of the selected hardware item."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbCostType,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "cost_type_id",
                    "index": 30,
                    "label_text": _("Cost Method:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The method for calculating total cost of the selected "
                        "hardware item."
                    ),
                    "visible": True,
                },
            ),
        ]

        super().do_set_widget_properties()
        super().do_make_panel()
        super().do_set_widget_callbacks()

        self.cmbManufacturer.connect("changed", self._do_load_cage_code)

    # ----- ----- HardwareLogisticsPanel specific methods. ----- ----- #
    def do_load_cost_types(self) -> None:
        """Load the category RAMSTKComboBox."""
        self.cmbCostType.do_load_combo([["Assessed"], ["Specified"]])

    def do_load_manufacturers(
        self, manufacturers: Dict[int, List[List[Union[str, int]]]]
    ) -> None:
        """Load the manufacturer RAMSTKComboBox.

        :param manufacturers: the dictionary with manufacturer information.
            The key is the index from the database table.  The value is a tuple
            with the manufacturer's name, office location, and CAGE code.  An
            example might be:

            ('Sprague', 'New Hampshire', '13606')
        """
        _manufacturer = list(manufacturers.values())
        self.cmbManufacturer.do_load_combo(
            entries=_manufacturer,
            simple=False,
        )

    def _do_load_cage_code(self, combo: RAMSTKComboBox) -> None:
        """Load the CAGE code whenever the manufacturer is changed.

        :param combo: the RAMSTKComboBox that called this method.
        """
        _model = combo.get_model()
        _row = combo.get_active_iter()

        try:
            _cage_code = str(_model.get(_row, 2)[0])
        except TypeError:
            _cage_code = ""

        _package = {"cage_code": _cage_code}

        self.txtCAGECode.do_update(_package)
        pub.sendMessage(
            f"wvw_editing_{self._tag}",
            node_id=self._record_id,
            package=_package,
        )
