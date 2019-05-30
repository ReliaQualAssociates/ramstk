# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.Combo.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Combo Module."""

# Import the ramstk.Widget base class.
from .Widget import GObject, Gtk


class RAMSTKComboBox(Gtk.ComboBox):
    """This is the RAMSTK ComboBox class."""

    def __init__(self, index=0, simple=True, **kwargs):
        r"""
        Create RAMSTK ComboBox widgets.

        :keyword int index: the index in the RAMSTKComboBox Gtk.ListView() to
                            display.  Default is 0.
        :keyword bool simple: indicates whether to make a simple (one item) or
                              complex (three item) RAMSTKComboBox.  Default is
                              True.
        """
        GObject.GObject.__init__(self)

        self._index = index

        if not simple:
            _list = Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_STRING,
                                  GObject.TYPE_STRING)
        else:
            _list = Gtk.ListStore(GObject.TYPE_STRING)
        self.set_model(_list)

        _cell = Gtk.CellRendererText()
        self.pack_start(_cell, True)
        self.add_attribute(_cell, 'text', self._index)

        self.show()

        # TODO: Remove this when all RAMSTK Entrys are refactored.
        self.do_set_properties(**kwargs)

    def do_get_options(self):
        """
        Retrieve all the options in the RAMSTK Combo.

        :return: _options
        :rtype: list
        """
        _options = []

        _model = self.get_model()
        _iter = _model.get_iter_first()

        while _iter is not None:
            _options.append(_model.get_value(_iter, self._index))
            _iter = iter_next(_iter)

        return _options

    def do_load_combo(self, entries, index=0, simple=True):
        """
        Load RAMSTK ComboBox widgets.

        :param list entries: the information to load into the Gtk.ComboBox().
                             This is always a list of lists where each internal
                             list contains the information to be displayed and
                             there is one internal list for each RAMSTKComboBox
                             line.
        :keyword int index: the index in the internal list to display.  Only
                            used when doing a simple load.  Default is 0.
        :keyword bool simple: indicates whether this is a simple (one item) or
                              complex (three item) RAMSTKComboBox.  A
                              simple (default) RAMSTKComboBox contains and
                              displays one field only.  A 'complex' RAMSTKComboBox
                              contains three str fields, but only displays the
                              first field.  The other two fields are hidden and
                              used to store information associated with the
                              items displayed in the RAMSTKComboBox.  For example,
                              if the name of an item is displayed, the other
                              two fields might contain a code and an index.
                              These could be extracted for use in the RAMSTK
                              Views.
        :return: None
        :rtype: None
        """
        _model = self.get_model()
        _model.clear()

        if not simple:
            _model.append(["", "", ""])
            for __, _entry in enumerate(entries):
                _model.append(list(_entry))
        else:
            _model.append([""])
            for __, _entry in enumerate(entries):
                _model.append([_entry[self._index]])

    def do_set_properties(self, **kwargs):
        """
        Set the properties of the RAMSTK combobox.

        :param \**kwargs: See below

        :Keyword Arguments:
            * *height* (int) -- height of the Gtk.ComboBox() widget.
                                Default is 30.
            * *tooltip* (str) -- the tooltip, if any, for the combobox.
                                 Default is an empty string.
            * *width* (int) -- width of the Gtk.ComboBox() widget.
                               Default is 200.
        :return: None
        :rtype: None
        """

        try:
            _height = kwargs['height']
        except KeyError:
            _height = 30
        try:
            _tooltip = kwargs['tooltip']
        except KeyError:
            _tooltip = ''
        try:
            _width = kwargs['width']
        except KeyError:
            _width = 200

        self.props.width_request = _width
        self.props.height_request = _height
        self.set_tooltip_markup(_tooltip)

    def do_update(self, value, handler_id):
        """
        Update the RAMSTK Combo with a new value.

        :param str value: the information to update the RAMSTKCombo() to
                          display.
        :param int handler_id: the handler ID associated with the
                               RAMSTKCombo().
        :return: None
        :rtype: None
        """
        _options = self.do_get_options()

        with self.handler_block(handler_id):
            self.set_active(0)
            for _key, _type in _options.items():
                if _type[self._index] == value:
                    self.set_active(int(_key))
            self.handler_unblock(handler_id)
