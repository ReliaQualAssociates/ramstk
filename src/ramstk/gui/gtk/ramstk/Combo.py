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

    def __init__(self, **kwargs):
        r"""
        Create RAMSTK ComboBox widgets.

        :param \**kwargs: See below

        :Keyword Arguments:
            * *height* (int) -- height of the Gtk.ComboBox() widget.
                                Default is 30.
            * *index* (int) -- the index in the RAMSTKComboBox Gtk.ListView()
                               to display.  Only needed with complex
                               RAMSTKComboBox.
                               Default is 0.
            * *simple* (bool) -- indicates whether to make a simple (one item)
                                 or complex (three item) RAMSTKComboBox.
                                 Default is True.
            * *tooltip* (str) -- the tooltip, if any, for the combobox.
                                 Default is an empty string.
            * *width* (int) -- width of the Gtk.ComboBox() widget.
                               Default is 200.
            * *entry* (bool) -- indicates whether to include an entry or not.
                                Default is False.
        """
        GObject.GObject.__init__(self)

        try:
            _height = kwargs['height']
        except KeyError:
            _height = 30
        try:
            _index = kwargs['index']
        except KeyError:
            _index = 0
        try:
            _simple = kwargs['simple']
        except KeyError:
            _simple = True
        try:
            _tooltip = kwargs['tooltip']
        except KeyError:
            _tooltip = ''
        try:
            _width = kwargs['width']
        except KeyError:
            _width = 200
        try:
            _entry = kwargs['entry']
        except KeyError:
            _entry = False

        # Set widget properties.
        self.props.width_request = _width
        self.props.height_request = _height
        self.props.has_entry = _entry

        if not _simple:
            _list = Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_STRING,
                                  GObject.TYPE_STRING)
        else:
            _list = Gtk.ListStore(GObject.TYPE_STRING)

        _cell = Gtk.CellRendererText()
        self.pack_start(_cell, True)
        self.add_attribute(_cell, 'text', _index)

        self.set_model(_list)
        self.set_tooltip_markup(_tooltip)

        self.show()

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
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model = self.get_model()
        _model.clear()

        if not simple:
            _model.append(["", "", ""])
            for __, _entry in enumerate(entries):
                _model.append(list(_entry))
        else:
            self.append_text("")
            for __, _entry in enumerate(entries):
                self.append_text(list(_entry)[index])

        return _return
