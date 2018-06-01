# -*- coding: utf-8 -*-
#
#       gui.gtk.rtk.Matrix.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
RTKBaseMatrix Module
-------------------------------------------------------------------------------

This module contains the base class for all the RTK data matrix views.
"""

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
from rtk.gui.gtk.rtk import RTKLabel
from .Widget import gobject, gtk, pango

_ = gettext.gettext


class RTKBaseMatrix(object):
    """
    The RTK base widget for displaying RTK Matrix views.  The attributes of an
    RTKBaseMatrix are:

    :ivar list _dic_icons: dictionary of icons to use in the various RTKMatrix
                           views.
    :ivar _rtk_matrix: the RTKDataMatrix to display in the Matrix View.
    :ivar int _n_columns: the number of columns in the matrix.
    :ivar int _n_rows: the number rows in the matrix.
    :ivar matrix: the gtk.TreeView() displaying the RTKDataMatrix.
    :type matrix: :py:class:`gtk.TreeView`
    """

    def __init__(self, controller):
        """
        Method to initialize an instance of the RTKMatrix widget class.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        # Initialize private dictionary attributes.
        self._dic_icons = {
            0:
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/none.png',
            1:
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/partial.png',
            2:
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/complete.png',
            'save':
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/save.png',
            'save-all':
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/save-all.png'
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._mdcRTK = controller
        self._rtk_matrix = None
        self._n_columns = 0
        self._n_rows = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.n_fixed_columns = 0
        self.matrix = gtk.TreeView(None)

        try:
            locale.setlocale(locale.LC_ALL,
                             controller.RTK_CONFIGURATION.RTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

    def do_load_matrix(self, matrix, column_headings, row_headings, rows):
        """
        Method to load the RTKMatrix view with the values from the
        RTKDataMatrix that is passed to this method.

        :param matrix: the RTKDataMatrix to display in the RTKMatrix widget.
        :type matrix: :py:class:`rtk.datamodels.RTKDataMatrix.RTKDataMatrix`
        :param dict column_headings: the dicionary containing the headings to
                                     use for the matrix columns.  Keys are the
                                     column <MODULE> IDs; values are a noun
                                     field associated with the key.
        :param dict row_headings: the dictionary containing the headings to
                                  use for the matrix rows.  Keys are the row
                                  <MODULE> IDs; values are a noun field
                                  associated with the key.
        :param str rows: the heading to put in the first column of the matrix.
                         This indicates what information is found in the rows.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        self._rtk_matrix = matrix
        self._n_columns = len(self._rtk_matrix.columns)
        self._n_rows = len(self._rtk_matrix.index)

        _gobject_types = [gobject.TYPE_INT, gobject.TYPE_STRING] + \
                         [gtk.gdk.Pixbuf, gobject.TYPE_STRING] * \
            (self._n_columns) + [gobject.TYPE_STRING]

        _model = gtk.TreeStore(*_gobject_types)

        self.matrix.set_model(_model)

        # The first column will contain the Function ID and Function Code.
        _cell = gtk.CellRendererText()
        _cell.set_property('background', 'light gray')
        _column = self._make_column(
            [
                _cell,
            ], '', visible=False)
        _column.set_attributes(_cell, text=0)
        _cell = gtk.CellRendererText()
        _cell.set_alignment(0.9, 0.5)
        _cell.set_property('background', 'light gray')
        _cell.set_property('editable', False)
        _cell.set_property('foreground', '#000000')
        _cell.set_property('wrap-width', 250)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _column = self._make_column([
            _cell,
        ], rows)
        _column.set_attributes(_cell, markup=1)
        self.matrix.append_column(_column)

        # The remaining columns will be gtk.CellRendererCombo()'s for
        # displaying the interaction between Function and Hardware.
        j = 2
        for i in xrange(self._n_columns):  # pylint: disable=E0602
            _cell = self._make_combo_cell()
            self._do_set_properties(_cell, True, i + j + 1,
                                    self._rtk_matrix.columns[i], _model)

            _pbcell = gtk.CellRendererPixbuf()
            _pbcell.set_property('xalign', 0.5)
            _heading = column_headings[self._rtk_matrix.columns[i]]
            _column = self._make_column([_pbcell, _cell], _heading)
            _column.set_attributes(_pbcell, pixbuf=i + j)
            self.matrix.append_column(_column)

            j += 1

        # Add one more column so the last column will not be extra wide.
        _column = self._make_column([
            gtk.CellRendererText(),
        ], '')

        try:
            # pylint: disable=undefined-loop-variable
            _column.set_attributes(_cell, text=i + j + 1)
        except UnboundLocalError:
            _column.set_visible(False)

        self.matrix.append_column(_column)

        # Now we load the data into the RTK Matrix View.
        for i in list(self._rtk_matrix.index):
            _data = [i, "<span weight='bold'>" + row_headings[i] + "</span>"]
            for j in list(self._rtk_matrix.loc[i]):
                _pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons[j], 22, 22)
                _data.append(_pixbuf)
                _data.append(j)
            _data.append('')

            _model.append(None, _data)

        return _return

    # pylint: disable=too-many-arguments
    def _do_edit_cell(self, cell, path, row, position, col_index, model):
        """
        Callback method to respond to changed signals for the
        gtk.CellRendererCombo() in the RTKMatrix.

        :param cell: the gtk.CellRendererCombo() calling this method.
        :type cell: :py:class:`gtk.CellRendererCombo`
        :param str path: the path of the selected row in the RTKMatrix.
        :param row: the gtk.TreeIter() for the gtk.CellRendererCombo() in the
                    selected row in the RTKMatrix.
        :type row: :py:class:`gtk.TreeIter`
        :param int position: the position of the cell in the RTKMatrix.
        :param int col_index: the column_item_id of the Matrix cell to be
                              edited.
        :param model: the gtk.TreeModel() associated with the RTKMatrix.
        :type model: :py:class:`gtk.TreeModel`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _model = cell.get_property('model')

        _column_item_id = col_index
        _row_item_id = model[path][0]
        if _model.get_value(row, 0) == 'Partial':
            self._rtk_matrix[_column_item_id][_row_item_id] = 1
            _pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                self._dic_icons[1], 22, 22)
        elif _model.get_value(row, 0) == 'Complete':
            self._rtk_matrix[_column_item_id][_row_item_id] = 2
            _pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                self._dic_icons[2], 22, 22)
        else:
            self._rtk_matrix[_column_item_id][_row_item_id] = 0
            _pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                self._dic_icons[0], 22, 22)

        model[path][position - 1] = _pixbuf

        return False

    def _do_set_properties(self, cell, editable, position, col_index, model):
        """
        Method to set common properties of gtk.CellRenderers().

        :param cell: the cell whose properties are to be set.
        :type cell: :py:class:`gtk.CellRenderer`
        :param bool editable: indicates whether or not the cell is editable.
        :param int position: the position in the gtk.TreeModel() that this
                             cell falls.
        :param int col_index: the column_item_id of the Matrix cell to be
                              edited.
        :param model: the `:py:class:gtk.TreeModel` associated with the
                      treeview.
        """

        cell.set_property('background', '#FFFFFF')
        cell.set_property('editable', editable)
        cell.set_property('foreground', '#000000')
        cell.set_property('wrap-width', 250)
        cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        cell.set_property('yalign', 0.1)
        cell.connect('changed', self._do_edit_cell, position, col_index, model)

    # pylint: disable=too-many-arguments
    def _make_buttonbox(self,
                        icons,
                        tooltips,
                        callbacks,
                        orientation='horizontal',
                        height=-1,
                        width=-1):
        """
        Method to create the buttonbox for RTK Matrix Views.  This method
        creates the base buttonbox used by all RTK Matrix Views.  Use a
        buttonbox for an RTK Matrix View if there are only buttons to be added.

        :param list icons: list of icon names to place on the toolbuttons.
                           The items in the list are keys in _dic_icons.
        :return: _buttonbox
        :rtype: :py:class:`gtk.ButtonBox`
        """

        if orientation == 'horizontal':
            _buttonbox = gtk.HButtonBox()
        else:
            _buttonbox = gtk.VButtonBox()

        _buttonbox.set_layout(gtk.BUTTONBOX_START)

        i = 0
        for _icon in icons:
            _image = gtk.Image()
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                self._dic_icons[_icon], height, width)
            _image.set_from_pixbuf(_icon)

            _button = gtk.Button()
            _button.set_image(_image)

            _button.props.width_request = width
            _button.props.height_request = height

            try:
                _button.set_tooltip_markup(tooltips[i])
            except IndexError:
                _button.set_tooltip_markup("")

            try:
                _button.connect('clicked', callbacks[i])
            except IndexError:
                _button.set_sensitive(False)

            _buttonbox.pack_start(_button)

            i += 1

        return _buttonbox

    @staticmethod
    def _make_combo_cell():
        """
        Method to make a gtk.CellRendererCombo().

        :return: _cell
        :rtype: :py:class:`gtk.CellRendererCombo`
        """

        _cell = gtk.CellRendererCombo()
        _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
        _cellmodel.append([""])
        _cellmodel.append([_(u"Partial")])
        _cellmodel.append([_(u"Complete")])
        _cell.set_property('has-entry', False)
        _cell.set_property('model', _cellmodel)
        _cell.set_property('text-column', 0)

        return _cell

    def _make_column(self, cells, heading, visible=True):
        """
        Method to make a gtk.TreeViewColumn()

        :param list cells: list of gtk.CellRenderer()s that are to be packed in
                           the column.
        :param str heading: the column heading text.
        :return: _column
        :rtype: :py:class:`gtk.TreeViewColumn`
        """

        _column = gtk.TreeViewColumn("")

        for _cell in cells:
            if isinstance(_cell, gtk.CellRendererPixbuf):
                _column.pack_start(_cell, False)
            else:
                _column.pack_start(_cell, True)
                _column.connect('notify::width', self._on_resize_wrap, _cell)

        _label = RTKLabel(
            heading, width=-1, height=-1, justify=gtk.JUSTIFY_CENTER)
        _label.set_angle(90)
        _column.set_widget(_label)
        _column.set_resizable(True)
        _column.set_alignment(0.5)
        _column.set_visible(visible)

        return _column

    @staticmethod
    def _on_resize_wrap(column, __param, cell):
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

        cell.set_property('wrap-width', _width)

        return False
