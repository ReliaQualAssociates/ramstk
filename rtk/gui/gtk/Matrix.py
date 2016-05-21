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

<<<<<<< HEAD
# Modules required for the GUI.
=======
# Import modules for the GUI.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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
<<<<<<< HEAD
import Configuration as _conf
import gui.gtk.Widgets as _widg
=======
try:
    import Configuration
except ImportError:
    import rtk.Configuration as Configuration
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2016 Andrew "weibullguy" Rowland'

try:
<<<<<<< HEAD
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
=======
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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
<<<<<<< HEAD
        _fmt = '{0:0.' + str(_conf.PLACES) + 'f}'
=======
        _fmt = '{0:0.' + str(Configuration.PLACES) + 'f}'
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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


<<<<<<< HEAD
class Matrix(gtk.TreeView):
    """
    The List Book view for displaying a Matrix.  The attributes of a matrix
    List Book view are:
=======
class Matrix(gobject.GObject):
    """
    The List Book view for displaying a Matrix.  The attributes of a matrix
    List Book view are:

    :ivar _lst_matrix_icons: list of icons to use in the various Matrix views.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    """

    def __init__(self, model=None):
        """
        Method to initialize an instance of the Matrix widget class.

        :keyword gtk.TreeModel model: the gtk.ListStore() or gtk.TreeStore() to
                                      use as the gtk.TreeModel() for this
                                      Matrix.
        """

<<<<<<< HEAD
        gtk.TreeView.__init__(self)

        self.set_model(model)

    def insert_column(self, heading, position, editable=True,
                      background='white', foreground='black'):
=======
        self.__gobject_init__()

        # Define private dictionary attributes.

        # Define private list attributes.
        _icon = Configuration.ICON_DIR + '32x32/none.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        self._lst_matrix_icons = [_icon]
        _icon = Configuration.ICON_DIR + '32x32/partial.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        self._lst_matrix_icons.append(_icon)
        _icon = Configuration.ICON_DIR + '32x32/complete.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        self._lst_matrix_icons.append(_icon)

        # Define private scalar attributes.

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.n_fixed_columns = 0

        self.treeview = gtk.TreeView(model)

    def add_column(self, heading, position, editable=True, background='white',
                   foreground='black'):
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """
        Method to create and add a column to the Matrix at the end.

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
<<<<<<< HEAD
=======
        _label.set_tooltip_markup("<span weight='bold'>" + heading + "</span>")
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _label.set_use_markup(True)
        _label.show_all()

        _column = gtk.TreeViewColumn()
        _column.set_visible(1)

<<<<<<< HEAD
        if position in [0, 1]:
=======
        if position in [0, 1, 2]:
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            _cell = gtk.CellRendererText()
            _cell.set_property('background', background)
            _cell.set_property('editable', editable)
            _cell.set_property('foreground', foreground)
            _cell.set_property('wrap-width', 250)
            _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            _cell.set_property('yalign', 0.1)
<<<<<<< HEAD
            _cell.connect('edited', self._on_tree_edited, position)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=position)
        else:
            _cell = gtk.CellRendererPixbuf()
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, pixbuf=position)
=======
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=position)
        else:
            # The position in the Matrix that the gtk.CellRendererPixbuf() will
            # display depends on the number of non-x-reference columns at the
            # beginning of the Matrix.  The general function for determining
            # the position for the gtk.CellRendererPixbuf() to display is:
            #
            #    _pixbuf_pos = 2 * position - n_fixed_columns
            #
            # In this case, there are three non-x-reference columns.
            _position = 2 * position - self.n_fixed_columns
            _cell = gtk.CellRendererPixbuf()
            _column.pack_start(_cell, False)
            _column.set_attributes(_cell, pixbuf=_position)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            _cell = gtk.CellRendererCombo()
            _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
            _cellmodel.append([""])
            _cellmodel.append([_(u"Partial")])
            _cellmodel.append([_(u"Complete")])
            _cell.set_property('background', background)
            _cell.set_property('editable', editable)
            _cell.set_property('foreground', foreground)
            _cell.set_property('has-entry', False)
            _cell.set_property('model', _cellmodel)
            _cell.set_property('text-column', 0)
            _cell.set_property('wrap-width', 250)
            _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            _cell.set_property('yalign', 0.1)
<<<<<<< HEAD
            _cell.connect('changed', self._on_combo_changed, position)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=position)

        # Make sure non-editable cells have a light gray background.
        if not editable and col_type != 6:
=======
            _cell.connect('changed', self._on_combo_changed, _position)
            _column.pack_end(_cell, True)

        # Make sure non-editable cells have a light gray background.
        if not editable:
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            _cell.set_property('background', 'light gray')

        _column.set_alignment(0.5)
        _column.set_resizable(True)
        _column.set_widget(_label)

        _column.set_cell_data_func(_cell, _format_cell, position)
        _column.connect('notify::width', _resize_wrap, _cell)

<<<<<<< HEAD
        self.append_column(_column)
=======
        self.treeview.append_column(_column)

        return False

    def remove_column(self, position):
        """
        Method to remove a column from the Matrix.

        :param int position: the position in the Matrix of the column to
                             remove.
        :return: False if succesful or True if an error is encountered.
        :rtype: bool
        """

        _model = self.treeview.get_model()
        _column = _model.get_n_columns()[position]

        self.treeview.remove_column(_column)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

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

<<<<<<< HEAD
            _piter = model.append(prow, _item[2:])
=======
            _data = _item[1:4]

            # Add the proper Pixbuf right before the database index that
            # defines which Pixbuf to use.
            for _index in range(4, len(_item)):
                if _item[_index] == '':
                    _item[_index] = '0'
                _pixbuf = self._lst_matrix_icons[int(_item[_index])]
                _data.extend([_pixbuf, _item[_index]])

            try:
                _piter = model.append(prow, _data)
            except ValueError:
                print model.get_n_columns(), len(_data), _data
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            _parent_id = _item[1]

            # Find the child items of the current parent item.  These will be
            # the new parent items to pass to this method.
            _parents = [_i for _i in items if _i[0] == _parent_id]
            self.load_matrix(_parents, items, model, _piter)

        return False

<<<<<<< HEAD
    def _on_combo_changed(self, cell, path, new_row, position):
        """
=======
    def _on_combo_changed(self, cell, __path, row, column):
        """
        Callback method to respond to changed signals for the
        gtk.CellRendererCombo() in the Matrix.

        :param gkt.CellRendererCombo cell: the gtk.CellRendererCombo() calling
                                           this method.
        :param str __path: the path of the selected row in the Matrix.
        :param gtk.TreeIter row: the gtk.TreeIter() for the
                                 gtk.CellRendererCombo() in the selected row in
                                 the Matrix.
        :param int column: the column position of the gtk.CellRendererCombo()
                           in the Matrix.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        _model = cell.get_property('model')

<<<<<<< HEAD
        if _model.get_value(new_row, 0) == 'P':
            cell.set_property('cell-background', 'pink')
        elif _model.get_value(new_row, 0) == 'C':
            cell.set_property('cell-background', 'green')
        else:
            cell.set_property('cell-background', 'white')

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
=======
        (_matrix_model,
         _matrix_row) = self.treeview.get_selection().get_selected()

        if _model.get_value(row, 0) == 'Partial':
            _value = 1
            _icon = self._lst_matrix_icons[1]
        elif _model.get_value(row, 0) == 'Complete':
            _value = 2
            _icon = self._lst_matrix_icons[2]
        else:
            _value = 0
            _icon = self._lst_matrix_icons[0]

        _matrix_model.set_value(_matrix_row, column, _icon)

        self.emit('changed', self.treeview, _value, column)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        return False


# Register the new widget type.
gobject.type_register(Matrix)
<<<<<<< HEAD
=======
gobject.signal_new('changed', Matrix, gobject.SIGNAL_RUN_FIRST,
                   gobject.TYPE_NONE,
                   (gtk.TreeView(), gobject.TYPE_INT, gobject.TYPE_INT))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
