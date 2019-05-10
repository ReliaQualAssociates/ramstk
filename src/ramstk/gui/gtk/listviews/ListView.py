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

    :ivar list _lst_col_order: list containing the order of the columns in the
                               List View RAMSTKTreeView().
    :ivar str _module: the capitalized name of the RAMSTK module the List View is
                       associated with.
    :ivar hbx_tab_label: the :class:`Gtk.HBox` used for the label in the
                         ListBook.
    :ivar treeview: the :class:`Gtk.TreeView` displaying the list of items
                    in the selected module.
    """

    def __init__(self, controller, **kwargs):
        """
        Initialize the List View.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        _module = kwargs['module']

        GObject.GObject.__init__(self)
        ramstk.RAMSTKBaseView.__init__(self, controller, **kwargs)

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
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _type = GObject.type_name(model.get_column_type(position))
        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        return _return
