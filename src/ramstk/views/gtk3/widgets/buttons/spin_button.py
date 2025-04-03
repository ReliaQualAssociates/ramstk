# pylint: disable=protected-access, non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.buttons.spin_button.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKSpinButton module."""

# Standard Library Imports
from datetime import date
from typing import Dict, List, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk

# RAMSTK Local Imports
from ..widget import RAMSTKBaseWidget, WidgetProperties


class RAMSTKSpinButton(Gtk.SpinButton, RAMSTKBaseWidget):
    """The RAMSTKSpinButton class."""

    # Define private class scalar attributes.
    _default_height = 30
    _default_width = 200
    _edit_signal = "value_changed"

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKSpinButton widget."""
        RAMSTKBaseWidget.__init__(self)

        self.show_all()

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKSpinButton.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKSpinButton.
        """
        super().do_set_properties(properties)

        self.dic_properties["lower"] = properties.get("lower", 0.0)
        self.dic_properties["numeric"] = properties.get("numeric", True)
        self.dic_properties["page_increment"] = properties.get("page_increment", 0.1)
        self.dic_properties["page_size"] = properties.get("page_size", 1.0)
        self.dic_properties["step_increment"] = properties.get("step_increment", 1.0)
        self.dic_properties["snap_to_ticks"] = properties.get("snap_to_ticks", True)
        self.dic_properties["upper"] = properties.get("upper", 100.0)

        _limits: List[float] = properties.get("limits", [0.0, 0.0, 100.0, 1.0, 0.1])  # type: ignore[assignment] # noqa

        self.set_adjustment(
            Gtk.Adjustment(_limits[0], _limits[1], _limits[2], _limits[3], _limits[4])
        )
        self.set_numeric(self.dic_properties["numeric"])
        self.set_snap_to_ticks(self.dic_properties["snap_to_ticks"])
        self.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)

    def do_update(self, package: Dict[str, Union[bool, date, float, int, str]]) -> None:
        """Update the RAMSTKSpinButton with a new value.

        :param package: the date package to use to update the RAMSTKSpinButton.
        """
        _field, _value = next(iter(package.items()))

        if _field != self.field:
            return

        try:
            self.handler_block(self.handler_id)
            self.set_value(_value)
            self.handler_unblock(self.handler_id)
        except KeyError:
            self.set_value(_value)

    def on_changed(self) -> None:
        """Retrieve the data package for the RAMSTKSpinButton on value changes.

        This method also sends a PyPubSub message along with the data package for
        listeners to update with the new value.
        """
        try:
            self.handler_block(self.handler_id)
            _package = {self.field: self.get_value()}
            self.handler_unblock(self.handler_id)
        except KeyError:
            _package = {self.field: self.get_value()}

        pub.sendMessage(self.topic, node_id=self.record_id, package=_package)
