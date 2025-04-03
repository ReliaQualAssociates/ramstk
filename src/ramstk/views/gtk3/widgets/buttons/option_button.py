# pylint: disable=protected-access, non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.buttons.option_button.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKOptionButton module."""

# Standard Library Imports
from datetime import date
from typing import Dict, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk

# RAMSTK Local Imports
from ..widget import WidgetProperties
from . import RAMSTKButton


class RAMSTKOptionButton(Gtk.RadioButton, RAMSTKButton):
    """The RAMSTKOptionButton class."""

    # Define private class attributes.
    _edit_signal = "clicked"

    def __init__(self, group: Gtk.RadioButton = None, label: str = "") -> None:
        """Initialize an instance of the RAMSTKOptionButton widget.

        :param group: the group the RAMSTKOptionButton belongs to, if any. Default is
            None.
        :param label: the text to place in the label on the RAMSTKOptionButton. Default
            is an empty string.
        """
        RAMSTKButton.__init__(self)

        self.dic_properties["label"] = label
        self.dic_properties["group"] = group

        self.set_group(self.dic_properties["group"])
        self.set_label(self.dic_properties["label"])

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKOptionButton.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKOptionButton.
        """
        super().do_set_properties(properties)

        self.dic_properties["group"] = properties.get("group")

        self.set_group(self.dic_properties["group"])

    def do_update(self, package: Dict[str, Union[bool, date, float, int, str]]) -> None:
        """Update the RAMSTKOptionButton with a new value.

        :param package: the date package to use to update the RAMSTKOptionButton.
        """
        _field, _value = next(iter(package.items()))

        if _field != self.field:
            return

        try:
            self.handler_block(self.handler_id)
            self.set_active(_value)
            self.handler_unblock(self.handler_id)
        except KeyError:
            self.set_active(_value)

    def on_changed(self) -> None:
        """Retrieve the data package for the RAMSTKOptionButton on value changes.

        This method also sends a PyPubSub message along with the data package for
        listeners to update with the new value.
        """
        try:
            self.handler_block(self.handler_id)
            _package = {self.field: self.get_active()}
            self.handler_unblock(self.handler_id)
        except KeyError:
            _package = {self.field: self.get_active()}

        pub.sendMessage(self.topic, node_id=self.record_id, package=_package)
