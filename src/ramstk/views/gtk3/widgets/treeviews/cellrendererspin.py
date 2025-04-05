# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.treeviews.cellrendererspin.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKCellRendererSpin module."""

# Standard Library Imports
from typing import Optional

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk

# RAMSTK Local Imports
from ..widget import WidgetProperties
from . import RAMSTKCellRendererText


class RAMSTKCellRendererSpin(Gtk.CellRendererSpin, RAMSTKCellRendererText):
    """The RAMSTKCellRendererSpin class."""

    # Define private scalar class attributes.
    _default_height = 25
    _default_width = 25
    _edit_signal = "edited"

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKCellRendererSpin widget."""
        RAMSTKCellRendererText.__init__(self)

        # Initialize public attributes.
        self.tree_model: Optional[Gtk.TreeStore] = None
        self.tree_row: Optional[Gtk.TreeIter] = None

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKCellRendererSpin.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKCellRendererSpin.
        """
        super().do_set_properties(properties)

        self.dic_properties["adjustment"] = properties.get(
            "adjustment", Gtk.Adjustment()
        )
        self.dic_properties["climb_rate"] = properties.get("climb_rate", 0.0)
        self.dic_properties["digits"] = properties.get("digits", 0)

        self.set_property("adjustment", self.dic_properties["adjustment"])
        self.set_property("climb_rate", self.dic_properties["climb_rate"])
        self.set_property("digits", self.dic_properties["digits"])
