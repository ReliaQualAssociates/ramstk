# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Combo.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
This module contains functions for creating, populating, destroying, and
interacting with pyGTK widgets.  Import this module in other modules that
create, populate, destroy, or interact with pyGTK widgets in the RTK
application.  This module is specific to RTK combo box widgets.
"""

# Import the rtk.Widget base class.
from Widget import gobject, gtk


class RTKComboBox(gtk.ComboBoxEntry):
    """
    This is the RTK Entry class.
    """

    def __init__(self, width=200, height=30, simple=True, has_entry=False,
                 tooltip='RTK WARNING: Missing tooltip.  '
                         'Please register an Enhancement type bug.'):
        """
        Method to create RTK Combo widgets.

        :keyword int width: width of the gtk.ComboBox() widget.  Default is
                            200.
        :keyword int height: height of the gtk.ComboBox() widget.  Default is
                             30.
        :keyword bool simple: indicates whether the gtk.ComboBox() contains
                              only the display information or if there is
                              additional, hidden, information in columns 1 and
                              2.
        :keyword bool has_entry: indicates whether the ComboBox can have
                                 entries added by the user.
        :keyword str tooltip: the tooltip text to display for the
        gtk.ComboBox().
        :return: _combobox
        :rtype: gtk.ComboBox
        """

        gtk.ComboBoxEntry.__init__(self)

        self.props.width_request = width
        self.props.height_request = height

        if simple:
            _list = gtk.ListStore(gobject.TYPE_STRING)
        else:
            _list = gtk.ListStore(gobject.TYPE_STRING,
                                  gobject.TYPE_STRING,
                                  gobject.TYPE_STRING)

        _cell = gtk.CellRendererText()
        self.pack_start(_cell, True)
        self.set_attributes(_cell, text=0)

        self.set_model(_list)

        if has_entry:
            self.set_text_column(0)

        self.set_tooltip_markup(tooltip)

        self.show()

    def do_load_combo(self, entries, simple=True, index=0):
        """
        Method to load gtk.ComboBox() widgets.

        :param list entries: the information to load into the gtk.ComboBox().
        :keyword bool simple: indicates whether the load is simple (single
                              column) or complex (multiple columns).  For
                              complex gtk.ComboBox(), the displayed value will
                              be in column 0.
        :keyword int index: the index in the list to display.  Only used when
                            doing a simple load.  Default is 0.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _model = self.get_model()
        _model.clear()

        if simple:
            self.append_text("")
            for __, entry in enumerate(entries):
                self.append_text(entry[index])
        else:
            _model.append(None, ["", "", ""])
            for __, entry in enumerate(entries):
                _model.append(None, entry)

        return _return
