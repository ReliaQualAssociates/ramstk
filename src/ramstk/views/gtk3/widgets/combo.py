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

    def __init__(self, position_idx: int = 0, simple_flag: bool = True) -> None:
        """Create RAMSTK ComboBox widgets.

        :keyword position_idx: the index in the RAMSTKComboBox Gtk.ListView() to
            display.  Default is 0.
        :keyword simple_flag: indicates whether to make a simple (one item) or
            complex (three item) RAMSTKComboBox.  Default is True.
        """
        RAMSTKWidget.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._index: int = position_idx

        _list_obj = Gtk.ListStore()
        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        if not simple_flag:
            _list_obj.set_column_types(
                [GObject.TYPE_STRING, GObject.TYPE_STRING, GObject.TYPE_STRING]
            )
        else:
            _list_obj.set_column_types([GObject.TYPE_STRING])
        self.set_model(_list_obj)

        _cell_obj = Gtk.CellRendererText()
        self.pack_start(_cell_obj, True)
        self.add_attribute(_cell_obj, "text", self._index)

        self.show()

    def do_get_options(self) -> Dict[int, Any]:
        """Retrieve all the options in the RAMSTK Combo.

        :return: _options_dic
        :rtype: dict
        """
        _options_dic = {}

        _model_obj = self.get_model()
        _iter_obj = _model_obj.get_iter_first()

        _option_idx = 0
        while _iter_obj is not None:
            _options_dic[_option_idx] = _model_obj.get_value(_iter_obj, self._index)
            _iter_obj = _model_obj.iter_next(_iter_obj)
            _option_idx += 1

        return _options_dic

    def do_load_combo(
        self,
        entries_lst: List[List[Union[str, int]]],
        signal_str: str = "changed",
        simple_flag: bool = True,
    ) -> None:
        """Load RAMSTK ComboBox widgets.

        :param entries_lst: the information to load into the Gtk.ComboBox().
            This is always a list of lists where each internal list contains
            the information to be displayed and there is one internal list for
            each RAMSTKComboBox line.
        :param signal_str: the name of the signal whose handler ID the
            RAMSTKComboBox() needs to block.
        :param simple_flag: indicates whether this is a simple (one item) or
            complex (three item) RAMSTKComboBox.  A simple (default)
            RAMSTKComboBox contains and displays one field only.  A 'complex'
            RAMSTKComboBox contains three str fields, but only displays the
            first field.  The other two fields are hidden and used to store
            information associated with the items displayed in the
            RAMSTKComboBox.  For example, if the name of an item is displayed,
            the other two fields might contain a code and an index.  These
            could be extracted for use in the RAMSTK Views.
        :return: None
        :rtype: None
        :raise: TypeError if attempting to load other than string values.
        """
        _model_obj = self.get_model()
        _model_obj.clear()

        try:
            _handler_id = self.dic_handler_id[signal_str]
            self.handler_block(_handler_id)
        except KeyError:
            _handler_id = -1

        if not simple_flag:
            _model_obj.append(["", "", ""])
            for _entry_obj in entries_lst:
                _model_obj.append(list(_entry_obj))
        else:
            _model_obj.append([""])
            for _entry_obj in entries_lst:
                _model_obj.append([_entry_obj[self._index]])

        if _handler_id > 0:
            self.handler_unblock(_handler_id)

    def do_update(self, value_int: int, signal_str: str = "") -> None:
        """Update the RAMSTK Combo with a new value.

        :param value_int: the information to update the RAMSTKCombo() to
            display.
        :param signal_str: the name of the signal whose handler ID the
            RAMSTKComboBox() needs to block.
        :return: None
        :rtype: None
        """
        _handler_id = self.dic_handler_id[signal_str]

        _value_int = none_to_default(value_int, 0)  # type: ignore

        self.handler_block(_handler_id)
        self.set_active(_value_int)
        self.handler_unblock(_handler_id)

    def get_value(self, column_idx: int = 0) -> str:
        """Return value in the RAMSTKComboBox() model at the index position.

        :keyword column_idx: the column in the RAMSTKComboBox() model whose
            value is to be retrieved.  Defaults to zero which will always
            read a 'simple' RAMSTKComboBox().
        :return: _value
        :rtype: str
        """
        _model_obj = self.get_model()
        _row_obj = self.get_active_iter()

        return _model_obj.get_value(_row_obj, column_idx)
