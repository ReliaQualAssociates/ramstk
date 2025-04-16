# pylint: disable=protected-access, non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.buttons.color_button.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKColorButton module."""

# Standard Library Imports
from datetime import date
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets.widget import WidgetProperties

# RAMSTK Local Imports
from . import RAMSTKButton


class RAMSTKColorButton(Gtk.ColorButton, RAMSTKButton):
    """The RAMSTKColorButton class."""

    # Define private class attributes.
    _default_height = 30
    _default_width = 60
    _edit_signal = "color-set"

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKColorButton widget."""
        RAMSTKButton.__init__(self)

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKColorButton.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKColorButton.
        """
        super().do_set_properties(properties)

        self.dic_properties["alpha"] = properties.get("alpha", 65535)
        self.dic_properties["rgba"] = properties.get("rgba", (1.0, 1.0, 1.0, 1.0))
        self.dic_properties["title"] = properties.get("title", _("Select a color"))

        self.set_alpha(self.dic_properties["alpha"])
        self.set_rgba(
            Gdk.RGBA(
                red=self.dic_properties["rgba"][0],
                green=self.dic_properties["rgba"][1],
                blue=self.dic_properties["rgba"][2],
                alpha=self.dic_properties["rgba"][3],
            )
        )
        self.set_title(self.dic_properties["title"])

    def do_update(self, package: Dict[str, Union[bool, date, float, int, str]]) -> None:
        """Update the RAMSTKColorButton with a new value.

        :param package: the date package to use to update the RAMSTKColorButton.
        """
        _field, _value = next(iter(package.items()))

        if _field != self.field:
            return

        try:
            self.handler_block(self.handler_id)
            if isinstance(_value, Gdk.RGBA):
                self.set_rgba(_value)
            elif isinstance(_value, int):
                self.set_alpha(_value)
            self.handler_unblock(self.handler_id)
        except KeyError:
            if isinstance(_value, Gdk.RGBA):
                self.set_rgba(_value)
            elif isinstance(_value, int):
                self.set_alpha(_value)
