#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.TreeView.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This module contains functions for creating, populating, destroying, and
interacting with pyGTK widgets.  Import this module in other modules that
create, populate, destroy, or interact with pyGTK widgets in the RTK
application.  This module is specific to treeview and related widgets.
"""

import gettext
import sys

import defusedxml.lxml as lxml

# Modules required for the GUI.
import pango
try:
    from pygtk import require
    require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

from .Label import RTKLabel

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class RTKTreeView(gtk.TreeView):
    """
    This is the RTK TreeView class.
    """

    def __init__(self, fmt_path, fmt_idx, fmt_file, bg_col='white',
                 fg_col='black', pixbuf=False):
        """
        Method to create RTK TreeView widgets.

        :param str fmt_path: the base XML path in the format file to read.
        :param int fmt_idx: the index of the format file to use when creating
                            the gtk.TreeView().
        :keyword str bg_col: the background color to use for each row.
                             Defaults to white.
        :keyword str fg_col: the foreground (text) color to use for each row.
                             Defaults to black.
        :keyword bool pixbuf: indicates whether or not to append a PixBuf
                              column to the gtk.TreeModel().
        """

        gtk.TreeView.__init__(self)

        # Initialize private dictionary instance attributes:

        # Initialize private list instance attributes:

        # Initialize private scalar instance attributes.

        # Initialize public dictionary instance attributes.

        # Initialize public list instance attributes.
        self.order = []

        # Initialize public scalar instance attributes.

        # Retrieve the column heading text from the format file.
        _headings = lxml.parse(fmt_file).xpath(fmt_path + "/usertitle")

        # Retrieve the column datatype from the format file.
        _datatypes = lxml.parse(fmt_file).xpath(fmt_path + "/datatype")

        # Retrieve the column position from the format file.
        position = lxml.parse(fmt_file).xpath(fmt_path + "/position")

        # Retrieve the cell renderer type from the format file.
        _widgets = lxml.parse(fmt_file).xpath(fmt_path + "/widget")

        # Retrieve whether or not the column is editable from the format file.
        editable = lxml.parse(fmt_file).xpath(fmt_path + "/editable")

        # Retrieve whether or not the column is visible from the format file.
        visible = lxml.parse(fmt_file).xpath(fmt_path + "/visible")

        # Create a list of GObject datatypes to pass to the model.
        _types = []
        for _datatype in _datatypes:
            _types.append(gobject.type_from_name(_datatype.text))

        if pixbuf:
            _types.append(gtk.gdk.Pixbuf)
        # FIXME: What is this for?  It'll become obvious later.
        elif fmt_idx in [15, 16]:
            _types.append(gobject.TYPE_INT)
            _types.append(gobject.TYPE_STRING)
            _types.append(gobject.TYPE_BOOLEAN)
            _types.append(gtk.gdk.Pixbuf)

        # Create the model.
        _model = gtk.TreeStore(*_types)

        _n_cols = int(len(_types))
        for i in range(_n_cols):
            self.order.append(int(position[i].text))

            _visible = int(visible[i].text)
            _heading = _headings[i].text.replace("  ", "\n")

            if pixbuf and i == 0:
                _cell = gtk.CellRendererPixbuf()
                _visible = 0
                _heading = ''
            elif _widgets[i].text == 'combo':
                _cell = self._do_make_combo_cell(bg_col, fg_col,
                                                 int(editable[i].text),
                                                 int(position[i].text))
            elif _widgets[i].text == 'spin':
                _cell = self._do_make_spin_cell(bg_col, fg_col,
                                                int(editable[i].text),
                                                int(position[i].text),
                                                _model)
            elif _widgets[i].text == 'toggle':
                _cell = self._do_make_toggle_cell(int(editable[i].text),
                                                  int(position[i].text),
                                                  _model)
            elif _widgets[i].text == 'blob':
                _cell = self._do_make_text_cell(bg_col, fg_col,
                                                int(editable[i].text),
                                                int(position[i].text),
                                                _model, True)
            else:
                _cell = self._do_make_text_cell(bg_col, fg_col,
                                                int(editable[i].text),
                                                int(position[i].text),
                                                _model)

            _column = self._do_make_column([_cell, ], _visible, _heading)
            _column.set_cell_data_func(_cell, self._format_cell,
                                       (int(position[i].text),
                                        _datatypes[i].text))

            if pixbuf and i == 0:
                _column.set_attributes(_cell, pixbuf=_n_cols)
            elif _widgets[i].text == 'toggle':
                _column.set_attributes(_cell, active=int(position[i].text))
            else:
                _column.set_attributes(_cell, text=int(position[i].text))

            if i > 0:
                _column.set_reorderable(True)

            self.append_column(_column)

        # FIXME: What is this for?  It'll become obvious later.
        if fmt_idx == 9:
            column = gtk.TreeViewColumn("")
            column.set_visible(0)
            cell = gtk.CellRendererText()
            column.pack_start(cell, True)
            column.set_attributes(cell, text=_n_cols)
            self.append_column(column)

        self.set_model(_model)

    def _do_make_column(self, cells, visible, heading):
        """
        Method to make a gtk.TreeViewColumn()

        :param list cells: list of gtk.CellRenderer()s that are to be packed in
                           the column
        :param int visible: indicates whether the column will be visible.
        :param str heading: the column heading text.
        :return: _column
        :rtype: :py:class:`gtk.TreeViewColumn`
        """

        _column = gtk.TreeViewColumn("")

        _column.set_visible(visible)

        for _cell in cells:
            _column.pack_start(_cell, True)
            _column.connect('notify::width', self._resize_wrap, _cell)

        _label = RTKLabel(heading, width=-1, height=-1,
                          justify=gtk.JUSTIFY_CENTER)
        _column.set_widget(_label)
        _column.set_resizable(True)
        _column.set_alignment(0.5)

        return _column

    def _do_make_combo_cell(self, bg_color, fg_color, editable, position):
        """
        Method to make a gtk.CellRendererCombo().

        :param str bg_color: the cell background color.
        :param str fg_color: the cell foreground color.
        :param int editable: indicates whether the cell is editable.
        :param int position: the position in the gtk.TreeModel() that this
                             cell falls.
        :return: _cell
        :rtype: :py:class:`gtk.CellRendererCombo`
        """

        _cell = gtk.CellRendererCombo()
        _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
        _cellmodel.append([""])
        _cell.set_property('background', bg_color)
        _cell.set_property('editable', editable)
        _cell.set_property('foreground', fg_color)
        _cell.set_property('has-entry', False)
        _cell.set_property('model', _cellmodel)
        _cell.set_property('text-column', 0)
        _cell.set_property('wrap-width', 250)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _cell.connect('edited', self._on_edit_tree, position, _model)

        if editable == 0:
            _cell.set_property('background', 'light gray')

        return _cell

    def _do_make_spin_cell(self, bg_color, fg_color, editable, position,
                           model):
        """
        Method to make a gtk.CellRendererCombo().

        :param str bg_color: the cell background color.
        :param str fg_color: the cell foreground color.
        :param int editable: indicates whether the cell is editable.
        :param int position: the position in the gtk.TreeModel() that this
                             cell falls.
        :param model: the gtk.TreeModel() the cell belongs to.
        :type model: :py:class:`gtk.TreeModel`
        :return: _cell
        :rtype: :py:class:`gtk.CellRendererCombo`
        """

        _cell = gtk.CellRendererSpin()
        _adjustment = gtk.Adjustment(upper=5.0, step_incr=0.05)
        _cell.set_property('adjustment', _adjustment)
        _cell.set_property('background', bg_color)
        _cell.set_property('digits', 2)
        _cell.set_property('editable', editable)
        _cell.set_property('foreground', fg_color)
        _cell.set_property('yalign', 0.1)
        _cell.connect('edited', self._on_edit_tree, position, model)

        if editable == 0:
            _cell.set_property('background', 'light gray')

        return _cell

    def _do_make_text_cell(self, bg_color, fg_color, editable, position,
                           model, blob=False):
        """
        Method to make a gtk.CellRendererCombo().

        :param str bg_color: the cell background color.
        :param str fg_color: the cell foreground color.
        :param int editable: indicates whether the cell is editable.
        :param int position: the position in the gtk.TreeModel() that this
                             cell falls.
        :param model: the gtk.TreeModel() the cell belongs to.
        :param bool blob: indicates whether the cell will be displaying a BLOB
                          field.
        :type model: :py:class:`gtk.TreeModel`
        :return: _cell
        :rtype: :py:class:`gtk.CellRendererCombo`
        """

        if not blob:
            _cell = gtk.CellRendererText()
        else:
            _cell = CellRendererML()

        _cell.set_property('background', bg_color)
        _cell.set_property('editable', editable)
        _cell.set_property('foreground', fg_color)
        _cell.set_property('wrap-width', 250)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _cell.connect('edited', self._on_edit_tree, position, model)

        if editable == 0:
            _cell.set_property('background', 'light gray')

        return _cell

    def _do_make_toggle_cell(self, editable, position, model):
        """
        Method to make a gtk.CellRendererCombo().

        :param int editable: indicates whether the cell is editable.
        :param int position: the position in the gtk.TreeModel() that this
                             cell falls.
        :param model: the gtk.TreeModel() the cell belongs to.
        :type model: :py:class:`gtk.TreeModel`
        :return: _cell
        :rtype: :py:class:`gtk.CellRendererCombo`
        """

        _cell = gtk.CellRendererToggle()
        _cell.set_property('activatable', editable)
        _cell.connect('toggled', self._on_cell_toggled, position, model)

        return _cell

    @staticmethod
    def _on_cell_toggled(cell, path, position, model):
        """
        Method called when a gtk.TreeView() gtk.CellRendererToggle() is edited.

        :param gtk.CellRendererToggle cell: the gtk.CellRendererToggle() that
                                            was edited.
        :param str path: the gtk.TreeView() path of the
                         gtk.CellRendererToggle() that was edited.
        :param int position: the column position of the edited
                             gtk.CellRendererToggle().
        :param gtk.TreeModel model: the gtk.TreeModel() the
                                    gtk.CellRendererToggle() belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        model[path][position] = not cell.get_active()

        return False

    @staticmethod
    def _on_edit_tree(cell, path, new_text, position, model):
        """
        Method called when a gtk.TreeView() gtk.CellRenderer() is edited.

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

        _convert = gobject.type_name(model.get_column_type(position))

        if new_text is None:
            model[path][position] = not cell.get_active()
        elif _convert == 'gchararray':
            model[path][position] = str(new_text)
        elif _convert == 'gint':
            model[path][position] = int(new_text)
        elif _convert == 'gfloat':
            model[path][position] = float(new_text)

        return False

    @staticmethod
    def _format_cell(__column, cell, model, row, data):
        """
        Method to set the formatting of the gtk.Treeview() gtk.CellRenderers().

        :param __column: the gtk.TreeViewColumn() containing the
                         gtk.CellRenderer() to format.
        :type __column: :py:class:`gtk.TreeViewColumn`
        :param cell: the gtk.CellRenderer() to format.
        :type cell: :py:class:`gtk.CellRenderer`
        :param model: the gtk.TreeModel() containing the gtk.TreeViewColumn().
        :type model: :py:class:`gtk.TreeModel`
        :param row: the gtk.TreeIter() pointing to the row containing the
                    gtk.CellRenderer() to format.
        :type row: :py:class:`gtk.TreeIter`
        :param tuple data: a tuple containing the position and the data type.
        """

        if data[1] == 'gfloat':
            # fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'
            fmt = '{0:0.6g}'
        elif data[1] == 'gint':
            fmt = '{0:0.0f}'
        else:
            return

        val = model.get_value(row, data[0])
        try:
            cell.set_property('text', fmt.format(val))
        except TypeError:  # It's a gtk.CellRendererToggle
            pass

        return

    @staticmethod
    def _resize_wrap(column, __param, cell):
        """
        Method to dynamically set the wrap-width property for a
        gtk.CellRenderer() in the gtk.TreeView() when the column width is
        resized.

        :param column: the gtk.TreeViewColumn() being resized.
        :type column: :py:class:`gtk.TreeViewColumn`
        :param GParamInt __param: the triggering parameter.
        :param cell: the gtk.CellRenderer() that needs to be resized.
        :type cell: :py:class:`gtk.CellRenderer`
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
        except TypeError:  # This is a gtk.CellRendererToggle
            cell.set_property('width', _width)

        return False


class CellRendererML(gtk.CellRendererText):
    """
    Class to create a multi-line cell renderer.  It is based on the base class
    gtk.CellRendererText().
    """

    def __init__(self):

        gtk.CellRendererText.__init__(self)

        self.textedit_window = None
        self.selection = None
        self.treestore = None
        self.treeiter = None

        self.textedit = gtk.TextView()
        self.textbuffer = self.textedit.get_buffer()

    def do_get_size(self, widget, cell_area):
        """
        Method to get the size of the CellRendererML.
        """

        size_tuple = gtk.CellRendererText.do_get_size(self, widget, cell_area)

        return size_tuple

    def do_start_editing(self, __event, treeview, path, __background_area,
                         cell_area, __flags):
        """


        :param __event:
        :param treeview:
        :param path:
        :param __background_area:
        :param cell_area:
        :param __flags:
        """

        if not self.get_property('editable'):
            return

        self.selection = treeview.get_selection()
        self.treestore, self.treeiter = self.selection.get_selected()

        self.textedit_window = gtk.Dialog(parent=treeview.get_toplevel())
        self.textedit_window.action_area.hide()
        self.textedit_window.set_decorated(False)
        self.textedit_window.set_property('skip-taskbar-hint', True)
        self.textedit_window.set_transient_for(None)

        self.textedit.set_editable(True)
        self.textedit.set_property('visible', True)
        self.textbuffer.set_property('text', self.get_property('text'))

        self.textedit_window.connect('key-press-event', self._keyhandler)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.set_property('visible', True)
        # self.textedit_window.vbox.pack_start(scrolled_window)

        scrolled_window.add(self.textedit)
        self.textedit_window.vbox.add(scrolled_window)
        self.textedit_window.realize()

        # Position the popup below the edited cell (and try hard to keep the
        # popup within the toplevel window)
        (tree_x, tree_y) = treeview.get_bin_window().get_origin()
        (tree_w, tree_h) = treeview.window.get_geometry()[2:4]
        (t_w, t_h) = self.textedit_window.window.get_geometry()[2:4]
        x_pos = tree_x + min(cell_area.x,
                             tree_w - t_w + treeview.get_visible_rect().x)
        y_pos = tree_y + min(cell_area.y,
                             tree_h - t_h + treeview.get_visible_rect().y)
        self.textedit_window.move(x_pos, y_pos)
        self.textedit_window.resize(cell_area.width, cell_area.height)

        # Run the dialog, get response by tracking keypresses
        response = self.textedit_window.run()

        if response == gtk.RESPONSE_OK:
            self.textedit_window.destroy()

            (iter_first, iter_last) = self.textbuffer.get_bounds()
            text = self.textbuffer.get_text(iter_first, iter_last)

            # self.treestore[path][2] = text

            treeview.set_cursor(path, None, False)

            self.emit('edited', path, text)

        elif response == gtk.RESPONSE_CANCEL:
            self.textedit_window.destroy()
        else:
            print "response %i received" % response
            self.textedit_window.destroy()

    def _keyhandler(self, __widget, event):
        """


        :param __widget:
        :param event:
        """

        _keyname = gtk.gdk.keyval_name(event.keyval)
        if event.state & (gtk.gdk.SHIFT_MASK | gtk.gdk.CONTROL_MASK) and \
                _keyname == 'Return':
            self.textedit_window.response(gtk.RESPONSE_OK)

# Register the new widget types.
gobject.type_register(CellRendererML)
