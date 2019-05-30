# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.listviews.ListView.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKListView Meta-Class Module."""

# Import other RAMSTK modules.
from ramstk.gui.gtk.ramstk.Widget import GObject, Gtk
from ramstk.gui.gtk import ramstk


class RAMSTKListView(Gtk.HBox, ramstk.RAMSTKBaseView):
    """
    Class to display data in the RAMSTK List Book.

    This is the meta class for all RAMSTK List View classes.  Attributes of the
    RAMSTKListView are:

    :ivar str _module: the capitalized name of the RAMSTK module the List View
                       is associated with.
    :ivar tab_label: the Gtk.Label() displaying text for the List View tab.
    :type tab_label: :class:`Gtk.Label`
    """

    def __init__(self, configuration, **kwargs):
        """
        Initialize the List View.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        _module = kwargs['module']

        GObject.GObject.__init__(self)
        ramstk.RAMSTKBaseView.__init__(self, configuration, **kwargs)

        self._module = None
        for __, char in enumerate(_module):
            if char.isalpha():
                self._module = _module.capitalize()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.tab_label = Gtk.Label()

    @staticmethod
    def _do_edit_cell(__cell, path, new_text, position, model):
        """
        Handle edits of the List View RAMSTKTreeView().

        :param Gtk.CellRenderer __cell: the Gtk.CellRenderer() that was edited.
        :param str path: the Gtk.TreeView() path of the Gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
                             Gtk.CellRenderer().
        :param Gtk.TreeModel model: the Gtk.TreeModel() the Gtk.CellRenderer()
                                    belongs to.
        :return: None
        :rtype: None
        """
        _type = GObject.type_name(model.get_column_type(position))
        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

    def _make_ui(self):
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.hbx_tab_label.pack_end(self.tab_label, True, True, 0)
        self.hbx_tab_label.show_all()

        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.add(self.treeview)

        self.pack_end(_scrolledwindow, True, True, 0)

        self.show_all()

    def _set_callbacks(self):
        """
        Set common callback methods for the ListView and widgets.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._on_row_change))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

    def _set_properties(self):
        """
        Set common properties of the ListView and widgets.

        :return: None
        :rtype: None
        """
        self.treeview.set_rubber_banding(True)
