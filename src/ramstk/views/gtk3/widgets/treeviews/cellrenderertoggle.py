# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.treeviews.cellrenderertoggle.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKCellRendererToggle module."""

# Standard Library Imports
from datetime import date
from typing import Dict, Optional, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.utilities import boolean_to_integer
from ramstk.views.gtk3 import Gdk, Gtk

# RAMSTK Local Imports
from ..widget import RAMSTKBaseWidget, WidgetProperties


class RAMSTKCellRendererToggle(Gtk.CellRendererToggle, RAMSTKBaseWidget):
    """The RAMSTKCellRendererToggle class."""

    # Define private scalar class attributes.
    _default_height = 25
    _default_width = 25
    _edit_signal = "toggled"

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKCellRendererToggle widget."""
        RAMSTKBaseWidget.__init__(self)

        # Initialize public attributes.
        self.tree_model: Optional[Gtk.TreeStore] = None
        self.tree_row: Optional[Gtk.TreeIter] = None

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKCellRendererToggle.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKCellRendererToggle.
        """
        super().do_set_properties(properties)

        self.dic_properties["cell_background_rgba"] = properties.get(
            "background_rgba", Gdk.RGBA(255.0, 255.0, 255.0, 1.0)
        )

        self.set_property(
            "cell-background-rgba", self.dic_properties["cell_background_rgba"]
        )

    def do_update(self, package: Dict[str, Union[bool, date, float, int, str]]) -> None:
        """Update the RAMSTKCellRendererToggle with a new value.

        :param package: the date package to use to update the RAMSTKCellRendererToggle.
        """
        if not package:
            return

        _key, _value = next(iter(package.items()))

        if self.tree_row is not None:
            self.tree_model.set_value(  # type: ignore[union-attr]
                self.tree_row,
                self.index,
                _value,
            )

    def on_changed(
        self,
        __cellrender: Gtk.CellRenderer,
        path: str,
    ):
        """Retrieve the data package for the RAMSTKCellRendererToggle on value changes.

        This method also sends a PyPubSub message along with the data package for
        listeners to update with the new value.

        :param __cellrender: the RAMSTKCellRendererToggle that just changed.
        :param path: the RAMSTKTreeView path to the RAMSTKCellRendererToggle that just
            changed.
        """
        _new_value = boolean_to_integer(self.get_active())

        self.tree_model[  # type: ignore[index] # pylint: disable=unsubscriptable-object
            path
        ][self.index] = _new_value
        _package = {self.field: _new_value}

        pub.sendMessage(self.send_topic, node_id=self.record_id, package=_package)
