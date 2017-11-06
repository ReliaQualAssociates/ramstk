# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Combo.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
Combo Module
-------------------------------------------------------------------------------

This module contains RTK combobox and comboboxentry classes.  These classes are
derived from the applicable pyGTK combobox, but are provided with RTK specific
property values and methods.  This ensures a consistent look and feel to
widgets in the RTK application.
"""

# Import the rtk.Widget base class.
from .Widget import gobject, gtk                    # pylint: disable=E0401


class RTKComboBox(gtk.ComboBox):
    """
    This is the RTK Entry class.
    """

    def __init__(self, width=200, height=30, index=0, simple=True,
                 tooltip='RTK WARNING: Missing tooltip.  '
                         'Please register an Enhancement type bug.'):
        """
        Method to create RTK Combo widgets.

        :keyword int width: width of the gtk.ComboBox() widget.  Default is
                            200.
        :keyword int height: height of the gtk.ComboBox() widget.  Default is
                             30.
        :keyword int index: the index in the RTKComboBox gtk.ListView() to
                            display.  Default = 0.  Only needed with complex
                            RTKComboBox.
        :keyword bool simple: indicates whether this to make a simple (one
                              item) or complex (three item) RTKComboBox.
        :keyword str tooltip: the tooltip text to display for the
        gtk.ComboBox().
        """

        gtk.ComboBox.__init__(self)

        self.props.width_request = width
        self.props.height_request = height

        """
        A simple (default) RTKComboBox contains and displays one field only.
        A 'complex' RTKComboBox contains three str filed, but only displays the
        first field.  The other two fields are hiddent and used to store
        information associated with the items displayed in the RTKComboBox.
        For example, if the name of an item is displayed, the other two fields
        might contain a code and an index.  These could be extracted for use
        in the RTK Views.
        """
        if not simple:
            _list = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING)
        else:
            _list = gtk.ListStore(gobject.TYPE_STRING)

        _cell = gtk.CellRendererText()
        self.pack_start(_cell, True)
        self.add_attribute(_cell, 'text', index)

        self.set_model(_list)
        self.set_tooltip_markup(tooltip)

        self.show()

    def do_load_combo(self, entries, index=0, simple=True):
        """
        Method to load gtk.ComboBox() widgets.

        :param list entries: the information to load into the gtk.ComboBox().
                             This is always a list of lists where each internal
                             list contains the information to be displayed and
                             there is one internal list for each RTKComboBox
                             line.
        :keyword int index: the index in the internal list to display.  Only
                            used when doing a simple load.  Default is 0.
        :keyword bool simple: indicates whether this is a simple (one item) or
                              complex (three item) RTKComboBox.
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


class RTKComboBoxEntry(gtk.ComboBoxEntry):
    """
    This is the RTK Entry class.
    """

    def __init__(self, width=200, height=30,
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
        """

        gtk.ComboBoxEntry.__init__(self)

        self.props.width_request = width

        _list = gtk.ListStore(gobject.TYPE_STRING,
                              gobject.TYPE_STRING,
                              gobject.TYPE_STRING)

        self.set_model(_list)
        self.set_text_column(0)
        self.set_tooltip_markup(tooltip)

        self.show()

    def do_load_combo(self, entries):
        """
        Method to load gtk.ComboBox() widgets.

        :param list entries: the information to load into the gtk.ComboBox().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _model = self.get_model()
        _model.clear()

        _model.append(None, ["", "", ""])
        for __, entry in enumerate(entries):
            _model.append(None, entry)

        return _return
