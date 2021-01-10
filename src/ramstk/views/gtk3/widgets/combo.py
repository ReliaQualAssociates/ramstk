# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.combo.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK GTK3 Combo Module."""

# Standard Library Imports
from typing import Any, Dict, List, Union

# RAMSTK Package Imports
from ramstk.utilities import none_to_default
from ramstk.views.gtk3 import GObject, Gtk

# RAMSTK Local Imports
from .widget import RAMSTKWidget


class RAMSTKComboBox(Gtk.ComboBox, RAMSTKWidget):
    """The RAMSTK ComboBox class."""

    # Define private class scalar attributes.
    _default_height = 30
    _default_width = 200

    def __init__(self, index: int = 0, simple: bool = True) -> None:
        """Create RAMSTK ComboBox widgets.

        :keyword int index: the index in the RAMSTKComboBox Gtk.ListView() to
            display.  Default is 0.
        :keyword bool simple: indicates whether to make a simple (one item) or
            complex (three item) RAMSTKComboBox.  Default is True.
        """
        RAMSTKWidget.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._index: int = index

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        if not simple:
            _list = Gtk.ListStore()
            _list.set_column_types([
                GObject.TYPE_STRING, GObject.TYPE_STRING, GObject.TYPE_STRING
            ])
        else:
            _list = Gtk.ListStore()
            _list.set_column_types([GObject.TYPE_STRING])
        self.set_model(_list)

        _cell = Gtk.CellRendererText()
        self.pack_start(_cell, True)
        self.add_attribute(_cell, 'text', self._index)

        self.show()

    def do_get_options(self) -> Dict[int, Any]:
        """Retrieve all the options in the RAMSTK Combo.

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

    # noinspection PyIncorrectDocstring
    def do_load_combo(self,
                      entries: List[List[Union[str, int]]],
                      signal: str = '',
                      simple: bool = True) -> None:
        """Load RAMSTK ComboBox widgets.

        :param entries: the information to load into the Gtk.ComboBox().
            This is always a list of lists where each internal list contains
            the information to be displayed and there is one internal list for
            each RAMSTKComboBox line.
        :param signal: the name of the signal whose handler ID the
            RAMSTKComboBox() needs to block.
        :param simple: indicates whether this is a simple (one item) or
            complex (three item) RAMSTKComboBox.  A simple (default)
            RAMSTKComboBox contains and displays one field only.  A 'complex'
            RAMSTKComboBox contains three str fields, but only displays the
            first field.  The other two fields are hidden and used to store
            information associated with the items displayed in the
            RAMSTKComboBox.  For example, if the name of an item is displayed,
            the other two fields might contain a code and an index.  These
            could be extracted for use in the RAMSTK Views.
        :return: None
        :raise: TypeError if attempting to load other than string values.
        """
        _model = self.get_model()
        _model.clear()

        try:
            _handler_id = self.dic_handler_id[signal]
            self.handler_block(_handler_id)
        except KeyError:
            _handler_id = -1

        if not simple:
            _model.append(["", "", ""])
            # pylint: disable=unused-variable
            for __, _entry in enumerate(entries):
                _model.append(list(_entry))
        else:
            _model.append([""])
            # pylint: disable=unused-variable
            for __, _entry in enumerate(entries):
                _model.append([_entry[self._index]])

        if _handler_id > 0:
            self.handler_unblock(_handler_id)

    def do_update(self, value: int, signal: str = '') -> None:
        """Update the RAMSTK Combo with a new value.

        :param value: the information to update the RAMSTKCombo() to
            display.
        :param str signal: the name of the signal whose handler ID the
            RAMSTKComboBox() needs to block.
        :return: None
        :rtype: None
        """
        _handler_id = self.dic_handler_id[signal]

        _value = none_to_default(value, 0)

        self.handler_block(_handler_id)
        self.set_active(_value)
        self.handler_unblock(_handler_id)

    def get_value(self, index: int = 0) -> str:
        """Return value in the RAMSTKComboBox() model at the index position.

        :keyword int index: the column in the RAMSTKComboBox() model whose
            value is to be retrieved.  Defaults to zero which will always
            read a 'simple' RAMSTKComboBox().
        :return: _value
        :rtype: str
        """
        _model = self.get_model()
        _row = self.get_active_iter()

        _value: str = _model.get_value(_row, index)

        return _value
