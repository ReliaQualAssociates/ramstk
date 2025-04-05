# pylint: disable=protected-access, non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.buttons.check_button.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKCheckButton module."""

# Standard Library Imports
from datetime import date
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.widgets.widget import WidgetProperties

# RAMSTK Local Imports
from . import RAMSTKButton


class RAMSTKCheckButton(Gtk.CheckButton, RAMSTKButton):
    """The RAMSTKCheckButton class."""

    # Define private class scalar attributes.
    _default_height = 40
    _default_width = 200
    _edit_signal = "toggled"

    def __init__(self, label: str = "") -> None:
        """Initialize an instance of the RAMSTKCheckButton widget.

        :param label: the text to display with the Gtk.CheckButton. Default is an empty
            string.
        """
        RAMSTKButton.__init__(self)

        self.dic_properties["label"] = label
        self.set_label(label)

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKCheckButton.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKCheckButton.
        """
        super().do_set_properties(properties)

        self.dic_properties["use_markup"] = properties.get("use_markup", True)
        self.dic_properties["use_underline"] = properties.get("use_underline", True)
        self.dic_properties["wrap"] = properties.get("wrap", True)

        self.set_use_underline(self.dic_properties["use_underline"])
        self.get_child().set_use_markup(self.dic_properties["use_markup"])
        self.get_child().set_line_wrap(self.dic_properties["wrap"])

    def do_update(self, package: Dict[str, Union[bool, date, float, int, str]]) -> None:
        """Update the RAMSTKCheckButton with a new value.

        :param package: the date package to use to update the RAMSTKCheckButton.
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
