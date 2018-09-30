# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.Combo.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""
Combo Module
-------------------------------------------------------------------------------

This module contains RAMSTK combobox and comboboxentry classes.  These classes are
derived from the applicable pyGTK combobox, but are provided with RAMSTK specific
property values and methods.  This ensures a consistent look and feel to
widgets in the RAMSTK application.
"""

# Import the ramstk.Widget base class.
from .Widget import gobject, gtk  # pylint: disable=E0401


class RAMSTKComboBox(gtk.ComboBox):
    """
    This is the RAMSTK Entry class.
    """

    def __init__(self,
                 width=200,
                 height=30,
                 index=0,
                 simple=True,
                 tooltip='RAMSTK WARNING: Missing tooltip.  '
                 'Please register an Enhancement type bug.'):
        """
        Method to create RAMSTK Combo widgets.

        :keyword int width: width of the gtk.ComboBox() widget.  Default is
                            200.
        :keyword int height: height of the gtk.ComboBox() widget.  Default is
                             30.
        :keyword int index: the index in the RAMSTKComboBox gtk.ListView() to
                            display.  Default = 0.  Only needed with complex
                            RAMSTKComboBox.
        :keyword bool simple: indicates whether this to make a simple (one
                              item) or complex (three item) RAMSTKComboBox.
        :keyword str tooltip: the tooltip text to display for the
        gtk.ComboBox().
        """

        gtk.ComboBox.__init__(self)

        self.props.width_request = width
        self.props.height_request = height

        if not simple:
            _list = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
                                  gobject.TYPE_STRING)
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


class RAMSTKComboBoxEntry(gtk.ComboBoxEntry):
    """
    This is the RAMSTK Entry class.
    """

    def __init__(self,
                 width=200,
                 height=30,
                 tooltip='RAMSTK WARNING: Missing tooltip.  '
                 'Please register an Enhancement type bug.'):
        """
        Method to create RAMSTK Combo widgets.

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
        self.props.height_request = height

        _list = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
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
