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
from .widget import RAMSTKBaseWidget, WidgetAttributes, WidgetProperties


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

        # Initialize public attributes.
        self.column_types: List[GObject.GType] = [GObject.TYPE_STRING]

        _cell = Gtk.CellRendererText()
        self.pack_start(_cell, True)
        self.add_attribute(_cell, "text", self._index)

        self.show()

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_attributes(self, attributes: WidgetAttributes) -> None:
        """Set the attributes of the RAMSTKComboBox.

        :param attributes: the WidgetAttributes dict with the attribute values to set
            for the RAMSTKComboBox.
        """
        super().do_set_attributes(attributes)

        self.column_types = attributes.get("column_types", [GObject.TYPE_STRING])

    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKComboBox.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKComboBox.
        """
        super().do_set_properties(properties)

        self.dic_properties["model"] = properties.get("model", Gtk.ListStore())
        if self.dic_properties["model"]:
            self.dic_properties["model"].set_column_types(  # type: ignore[union-attr] # noqa
                self.column_types
            )
            self.set_model(self.dic_properties["model"])

        self.set_property(
            "tooltip-markup",
            self.dic_properties["tooltip"],
        )

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
            self.handler_block(self.dic_handler_id[self._edit_signal])
            self.set_active(_value)
            self.handler_unblock(self.dic_handler_id[self._edit_signal])
        except KeyError:
            self.set_active(_value)

    def on_changed(self, __combo) -> None:
        """Retrieve the data package for the RAMSTKComboBox on value changes.

        This method also sends a PyPubSub message along with the data package for
        listeners to update with the new value.

        :param __combo: the RAMSTKComboBox that was changed. Unused but required to
            satisfy the Gtk.ComboBox() callback method structure.
        """
        try:
            self.handler_block(self.dic_handler_id[self._edit_signal])
            _package = {self.field: self.get_value()}
            self.handler_unblock(self.dic_handler_id[self._edit_signal])
        except KeyError:
            _package = {self.field: self.get_value()}

        pub.sendMessage(self.send_topic, node_id=self.record_id, package=_package)

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
    ) -> None:
        """Load the RAMSTKComboBox widget.

        :param entries: the information to load into the Gtk.ComboBox(). This is always
            a list of lists where each internal list contains the information to be
            displayed, and there is one internal list for each RAMSTKComboBox line.
        :raises: TypeError if attempting to load other than string values.
        """
        _model = self.get_model()
        _model.clear()

        self.handler_block(self.dic_handler_id[self._edit_signal])

        if not self._simple:
            _model.append([None] * self._n_items)
            for _entry in entries:
                _model.append(list(_entry))
        else:
            _model.append([None])
            for _entry in entries:
                _model.append([_entry[self._index]])

        self.handler_unblock(self.dic_handler_id[self._edit_signal])

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
