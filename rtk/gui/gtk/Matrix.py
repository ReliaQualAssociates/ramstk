#!/usr/bin/env python
"""
#############
Matrix Module
#############
"""

# -*- coding: utf-8 -*-
#
#       gui.gtk.Matrix.py is part of The RTK Project
#
# All rights reserved.

import sys

# Import modules for localization support.
import gettext
import locale

# Modules required for the GUI.
import pango
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

# Import other RTK modules.
import Configuration as _conf
import gui.gtk.Widgets as _widg

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2016 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _format_cell(__column, cell, model, row, position):
    """
    Method to set the formatting of the gtk.Treeview() gtk.CellRenderers().

    :param gtk.TreeViewColumn __column: the gtk.TreeViewColumn() containing
                                        the gtk.CellRenderer() to format.
    :param gtk.CellRenderer cell: the gtk.CellRenderer() to format.
    :param gtk.TreeModel model: the gtk.TreeModel() containing the
                                gtk.TreeViewColumn().
    :param gtk.TreeIter row: the gtk.TreeIter() pointing to the row
                             containing the gtk.CellRenderer() to format.
    :param int position: the column position in the Matrix.
    :return: False is successful or True if an error is encountered.
    :rtype: bool
    """

    _cell_type = gobject.type_name(model.get_column_type(position))

    if _cell_type == 'gfloat':
        _fmt = '{0:0.' + str(_conf.PLACES) + 'f}'
    elif _cell_type == 'gint':
        _fmt = '{0:0.0f}'
    else:
        return

    _val = model.get_value(row, position)
    try:
        cell.set_property('text', _fmt.format(_val))
    except TypeError:                       # It's a gtk.CellRendererToggle
        pass

    return False


def _resize_wrap(column, __param, cell):
    """
    Method to dynamically set the wrap-width property for a gtk.CellRenderer()
    in the gtk.TreeView() when the column width is resized.

    :param gtk.TreeViewColumn column: the gtk.TreeViewColumn() being resized.
    :param GParamInt __param: the triggering parameter.
    :param gtk.CellRenderer cell: the gtk.CellRenderer() that needs to be
                                  resized.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    _width = column.get_width()

    if _width <= 0:
        return
    else:
        _width += 10

    try:
        cell.set_property('wrap-width', _width)
    except TypeError:                       # This is a gtk.CellRendererToggle
        cell.set_property('width', _width)

    return False


class Matrix(gtk.TreeView):
    """
    The List Book view for displaying a Matrix.  The attributes of a matrix
    List Book view are:
    """

    def __init__(self, model=None):
        """
        Method to initialize an instance of the Matrix widget class.

        :keyword gtk.TreeModel model: the gtk.ListStore() or gtk.TreeStore() to
                                      use as the gtk.TreeModel() for this
                                      Matrix.
        """

        gtk.TreeView.__init__(self)

        self.set_model(model)

    def insert_column(self, col_type, heading, position, editable=True,
                      background='white', foreground='black'):
        """
        Method to create and add a column to the Matrix at the end.

        :param int col_type: the type of gtk.CellRenderer() to place in the
                             column.
        :param str heading: the string to use as the column heading.
        :param int position: the position of the column in the gtk.TreeView().
        :keyword bool editable: indicates whether or not the gtk.CellRenderer()
                                in the column is editable.
        :keyword str background: the background color of the gtk.CellRenderer()
                                 in the column.
        :keyword str foreground: the foreground color of the gtk.CellRenderer()
                                 in the column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _label = gtk.Label()
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_angle(90)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_markup("<span weight='bold'>" + heading + "</span>")
        _label.set_use_markup(True)
        _label.show_all()

        _column = gtk.TreeViewColumn()
        _column.set_visible(1)

        if col_type == 0:
            _cell = gtk.CellRendererAccel()
            _column.pack_start(_cell, True)
        elif col_type == 1:
            _cell = gtk.CellRendererCombo()
            _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
            _cellmodel.append([""])
            _cell.set_property('background', background)
            _cell.set_property('editable', editable)
            _cell.set_property('foreground', foreground)
            _cell.set_property('has-entry', False)
            _cell.set_property('model', _cellmodel)
            _cell.set_property('text-column', 0)
            _cell.set_property('wrap-width', 250)
            _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            _cell.set_property('yalign', 0.1)
            _cell.connect('edited', self._on_tree_edited, position)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=position)
        elif col_type == 2:
            _cell = gtk.CellRendererPixbuf()
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, pixbuf=position)
        elif col_type == 3:
            _cell = gtk.CellRendererProgress()
            _column.pack_start(_cell, True)
        elif col_type == 4:
            _cell = gtk.CellRendererSpin()
            _adjustment = gtk.Adjustment(upper=5.0, step_incr=0.05)
            _cell.set_property('adjustment', _adjustment)
            _cell.set_property('background', background)
            _cell.set_property('digits', 2)
            _cell.set_property('editable', editable)
            _cell.set_property('foreground', foreground)
            _cell.set_property('yalign', 0.1)
            _cell.connect('edited', self._on_tree_edited, position)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=position)
        elif col_type == 5:
            _cell = gtk.CellRendererSpinner()
            _column.pack_start(_cell, True)
        elif col_type == 6:
            _cell = gtk.CellRendererToggle()
            _cell.set_property('activatable', editable)
            _cell.connect('edited', self._on_tree_edited, position)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, active=position)
        else:
            _cell = gtk.CellRendererText()
            _cell.set_property('background', background)
            _cell.set_property('editable', editable)
            _cell.set_property('foreground', foreground)
            _cell.set_property('wrap-width', 250)
            _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            _cell.set_property('yalign', 0.1)
            _cell.connect('edited', self._on_tree_edited, position)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=position)

        # Make sure non-editable cells have a light gray background.
        if not editable and col_type != 6:
            _cell.set_property('background', 'light gray')

        _column.set_alignment(0.5)
        _column.set_resizable(True)
        _column.set_widget(_label)

        _column.set_cell_data_func(_cell, _format_cell, position)
        _column.connect('notify::width', _resize_wrap, _cell)

        self.append_column(_column)

        return False

    def load_matrix(self, parents, items, model, prow=None):
        """
        Method to load data into the Matrix view.

        :param list parents: the list of top-level items to load.
        :param list items: the complete list of items to use for finding the
                           child items for each parent.  Each list in the list
                           of items must have the following fields:
                           [Parent ID, Item ID, Col 1 Val, ... Col m Val]
        :param gtk.TreeModel model: the Matrix List View gtk.TreeModel().
        :keyword gtk.TreeIter prow: the parent gtk.TreeIter().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Iterate through the list of parent items and load them into the
        # matrix.
        for _item in parents:
            if _item[0] == -1:              # Indicates a top-level item.
                prow = None

            _piter = model.append(prow, _item[2:])
            _parent_id = _item[1]

            # Find the child items of the current parent item.  These will be
            # the new parent items to pass to this method.
            _parents = [_i for _i in items if _i[0] == _parent_id]
            self.load_matrix(_parents, items, model, _piter)

        return False

    def _on_tree_edited(self, cell, path, new_text, position):
        """
        Callback method whenever a gtk.TreeView() gtk.CellRenderer() is edited.

        :param gtk.CellRenderer cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer() that
                         was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _model = self.get_model()
        _convert = gobject.type_name(_model.get_column_type(position))

        if new_text is None:
            _model[path][position] = not cell.get_active()
        elif _convert == 'gchararray':
            _model[path][position] = str(new_text)
        elif _convert == 'gint':
            _model[path][position] = int(new_text)
        elif _convert == 'gfloat':
            _model[path][position] = float(new_text)

        return False


# Register the new widget type.
gobject.type_register(Matrix)
