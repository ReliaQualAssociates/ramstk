# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.listviews.ListView.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKListView Meta-Class Module."""

# Import other RTK modules.
from rtk.gui.gtk.rtk.Widget import gobject, gtk
from rtk.gui.gtk import rtk


class RTKListView(gtk.HBox, rtk.RTKBaseView):
    """
    Class to display data in the RTK List Book.

    This is the meta class for all RTK List View classes.  Attributes of the
    RTKListView are:

    :ivar list _lst_col_order: list containing the order of the columns in the
                               List View RTKTreeView().
    :ivar str _module: the capitalized name of the RTK module the List View is
                       associated with.
    :ivar hbx_tab_label: the :class:`gtk.HBox` used for the label in the
                         ListBook.
    :ivar treeview: the :class:`gtk.TreeView` displaying the list of items
                    in the selected module.
    """

    def __init__(self, controller, **kwargs):
        """
        Initialize the List View.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        _module = kwargs['module']

        gtk.HBox.__init__(self)
        rtk.RTKBaseView.__init__(self, controller, **kwargs)

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
        Handle edits of the List View RTKTreeView().

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _type = gobject.type_name(model.get_column_type(position))
        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        return _return
