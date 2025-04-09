# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.combo.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKComboBox module."""

# Standard Library Imports
from datetime import date
from typing import Any, Dict, List, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.utilities import none_to_default
from ramstk.views.gtk3 import GObject, Gtk

# RAMSTK Local Imports
from .widget import RAMSTKBaseWidget, WidgetProperties


class RAMSTKComboBox(Gtk.ComboBox, RAMSTKBaseWidget):
    """The RAMSTKComboBox class."""

    # Define private class scalar attributes.
    _default_height = 30
    _default_width = 200
    _edit_signal = "changed"

    def __init__(
        self,
        index: int = 0,
        simple: bool = True,
        n_items: int = 2,
    ) -> None:
        """Initialize an instance of the RAMSTKComboBox widget.

        :param index: the index in the RAMSTKComboBox Gtk.ListView to display. Default
            is 0.
        :param simple: indicates whether to make a simple (one item) or complex (n_item)
            RAMSTKComboBox. Default is True.
        :param n_items: the number of items (columns) to add for a non-simple
            RAMSTKComboBox.
        """
        RAMSTKBaseWidget.__init__(self)

        # Initialize private attributes.
        self._index: int = index
        self._n_items: int = n_items
        self._simple: bool = simple

        self.set_model(Gtk.ListStore())

        _cell = Gtk.CellRendererText()
        self.pack_start(_cell, True)
        self.add_attribute(_cell, "text", self._index)

        self.show()

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKComboBox.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKComboBox.
        """
        super().do_set_properties(properties)

        self.dic_properties["has_entry"] = properties.get("has_entry", True)
        self.dic_properties["model"] = properties.get("model", Gtk.ListStore())

        if not self._simple:
            self.dic_properties["model"].set_column_types(  # type: ignore[union-attr] # noqa
                [GObject.TYPE_STRING] * self._n_items
            )
        else:
            self.dic_properties["model"].set_column_types([GObject.TYPE_STRING])  # type: ignore[union-attr] # noqa
        self.set_model(self.dic_properties["model"])

        self.set_property("has-entry", self.dic_properties["has_entry"])

    def do_update(
        self, package: Dict[str, Union[bool, date, float, int, str, None]]
    ) -> None:
        """Update the RAMSTKComboBox with a new value.

        :param package: the date package to use to update the RAMSTKComboBox.
        """
        _field, _value = next(iter(package.items()))

        if _field != self.field:
            return

        _value = none_to_default(_value, self.default)

        try:
            self.handler_block(self.handler_id)
            self.set_active(_value)
            self.handler_unblock(self.handler_id)
        except KeyError:
            self.set_active(_value)

    def on_changed(self) -> None:
        """Retrieve the data package for the RAMSTKComboBox on value changes.

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

    # ----- ----- RAMSTKComboBox specific methods. ----- ----- #
    def do_get_options(self) -> Dict[int, Any]:
        """Retrieve all the options in the RAMSTKComboBox.

        :return: _options
        :rtype: dict
        """
        _options = {}

        _model = self.get_model()
        _iter = _model.get_iter_first()

        i = 0
        while _iter is not None:
            _options[i] = _model.get_value(_iter, self._index)
            _iter = _model.iter_next(_iter)
            i += 1

        return _options

    def do_load_combo(
        self,
        entries: List[List[Union[str, int]]],
        simple: bool = True,
    ) -> None:
        """Load the RAMSTKComboBox widget.

        :param entries: the information to load into the Gtk.ComboBox(). This is always
            a list of lists where each internal list contains the information to be
            displayed and there is one internal list for each RAMSTKComboBox line.
        :param simple: indicates whether this is a simple (one item) or complex (three
            item) RAMSTKComboBox. A simple (default) RAMSTKComboBox contains and
            displays one field only. A 'complex' RAMSTKComboBox contains three str
            fields, but only displays the first field. The other two fields are hidden
            and used to store information associated with the items displayed in the
            RAMSTKComboBox. For example, if the name of an item is displayed, the other
            two fields might contain a code and an index. These could be extracted for
            use in the RAMSTK Views.
        :raises: TypeError if attempting to load other than string values.
        """
        _model = self.get_model()
        _model.clear()

        self.handler_block(self.handler_id)

        if not simple:
            _model.append([""] * self._n_items)
            for _entry in entries:
                _model.append(list(_entry))
        else:
            _model.append([""])
            for _entry in entries:
                _model.append([_entry[self._index]])

        self.handler_unblock(self.handler_id)

    def get_value(self, index: int = 0) -> str:
        """Return the value in the RAMSTKComboBox model found at <index> position.

        :param index: the column in the RAMSTKComboBox model whose value is to be
            retrieved. Defaults to zero which will always read a 'simple'
            RAMSTKComboBox.
        :return: _value
        :rtype: str
        """
        _model = self.get_model()
        _row = self.get_active_iter()

        return _model.get_value(_row, index)
