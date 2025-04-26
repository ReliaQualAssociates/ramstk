# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.fmea.method_panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The FMEA method panel module."""

# Standard Library Imports
from typing import Dict, List

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton,
    RAMSTKFixedPanel,
    RAMSTKLabel,
    RAMSTKTextView,
    WidgetConfig,
    make_widget_config,
)


class FMEAMethodPanel(RAMSTKFixedPanel):
    """Panel to display FMEA criticality methods."""

    # Define private class attributes.
    _record_field = "mode_id"
    _select_msg = "succeed_retrieve_all_mode"
    _tag = "fmeca"
    _title = _("FMEA Risk Analysis Method")

    def __init__(self):
        """Initialize an instance of the FMEA methods panel."""
        super().__init__()

        # Initialize widgets.
        self.chkCriticality: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Calculate Criticality")
        )
        self.chkRPN: RAMSTKCheckButton = RAMSTKCheckButton(label=_("Calculate RPNs"))
        self.txtItemCriticality: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.chkCriticality,
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "type_id",
                    "index": 27,
                    "label_text": _("Calculate Criticality"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "tooltip": _(
                        "Select this option to calculate the MIL-STD-1629, Task 102 "
                        "criticality analysis."
                    ),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkRPN,
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "rpn",
                    "index": 27,
                    "label_text": _("Calculate RPN"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "tooltip": _(
                        "Select this option to calculate the Risk Priority Number "
                        "(RPN)."
                    ),
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtItemCriticality,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "item_criticality",
                    "index": 28,
                    "label_text": _("Item Criticality:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_fmeca",
                },
                {
                    "tooltip": _(
                        "Displays the MIL-STD-1629A, Task 102 item criticality for "
                        "the selected hardware item."
                    ),
                    "bold": True,
                    "editable": False,
                    "height_request": 125,
                    "visible": True,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_fixed_panel()
        super().do_set_widget_callbacks()

        # Move the item criticality RAMSTKTextView() below it's label.
        _fixed: Gtk.Fixed = self.get_children()[0].get_children()[0].get_child()
        _label: RAMSTKLabel = _fixed.get_children()[-2]
        _x_pos: int = _fixed.child_get_property(_label, "x")
        _y_pos: int = _fixed.child_get_property(_label, "y") + 25
        _fixed.move(self.txtItemCriticality.scrollwindow, _x_pos, _y_pos)

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "succeed_calculate_mode_criticality": self._do_load_item_criticality,
            }
        )

    def _do_load_item_criticality(self, item_criticality: Dict[str, float]) -> None:
        """Update the item criticality RAMSTKTextView() with the results.

        :param item_criticality: the item criticality for the selected hardware item.
        """
        _item_criticality = ""
        for _key, _value in item_criticality.items():
            _item_criticality = _item_criticality + _key + ": " + str(_value) + "\n"

        self.txtItemCriticality.do_update({"item_criticality": _item_criticality})
