# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.treeviews.cellrenderercombo.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKCellRendererCombo module."""

# Standard Library Imports
from datetime import date
from typing import Dict, List, Optional, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk

# RAMSTK Local Imports
from ..widget import RAMSTKBaseWidget, WidgetProperties


class RAMSTKCellRendererCombo(Gtk.CellRendererCombo, RAMSTKBaseWidget):
    """The RAMSTKCellRendererCombo class."""

    # Define private scalar class attributes.
    _default_height = 25
    _default_width = 25
    _edit_signal = "changed"

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKCellRendererCombo widget."""
        RAMSTKBaseWidget.__init__(self)

        # Initialize public attributes.
        self.tree_model: Optional[Gtk.TreeStore] = None
        self.tree_row: Optional[Gtk.TreeIter] = None

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKCellRendererCombo.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKCellRendererCombo.
        """
        super().do_set_properties(properties)

        self.dic_properties["editable"] = properties.get("editable", True)
        self.dic_properties["has_entry"] = properties.get("has_entry", False)
        self.dic_properties["model"] = properties.get("model", Gtk.ListStore(str))
        self.dic_properties["text_column"] = properties.get("text_column", 0)

        self.set_property("editable", self.dic_properties["editable"])
        self.set_property("has-entry", self.dic_properties["has_entry"])
        self.set_property("model", self.dic_properties["model"])
        self.set_property("text-column", self.dic_properties["text_column"])

    def do_update(self, package: Dict[str, Union[bool, date, float, int, str]]) -> None:
        """Update the RAMSTKCellRendererCombo with a new value.

        :param package: the date package to use to update the RAMSTKCellRendererCombo.
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
        new_iter: Gtk.TreeIter,
    ):
        """Retrieve the data package for the RAMSTKCellRendererCombo on value changes.

        This method also sends a PyPubSub message along with the data package for
        listeners to update with the new value.

        :param __cellrender: the RAMSTKCellRendererCombo that just changed.
        :param path: the RAMSTKTreeView path to the RAMSTKCellRendererCombo that just
            changed.
        :param new_iter: the Gtk.TreeIter of the newly selected value in the
            RAMSTKCellRendererCombo.
        """
        _package = {}
        _model = self.get_property("model")

        _iter = _model.get_iter_first()
        while _iter is not None:
            if _model.get_value(_iter, 0) == new_iter:
                self.tree_model[  # type: ignore[index] # noqa # pylint: disable=unsubscriptable-object
                    path
                ][
                    self.index
                ] = new_iter
                _package = {self.field: new_iter}
                break
            _iter = _model.iter_next(_iter)

        pub.sendMessage(self.send_topic, node_id=self.record_id, package=_package)

    # ----- ----- RAMSTKCellRendererCombo specific methods. ----- ----- #
    def do_load_combo(self, items: List[str]) -> None:
        """Load items into the RAMSTKCellRendererCombo.

        :param items: the list of entries to load into the RAMSTKCellRendererCombo.
        """
        _model = self.get_property("model")
        for _item in items:
            _model.append([str(_item)])
