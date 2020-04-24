# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.matrix.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKBaseMatrix Module."""

# Standard Library Imports
from typing import Any

# Third Party Imports
# noinspection PyPackageRequirements
import pandas as pd

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf, GObject, Gtk, _

# RAMSTK Local Imports
from . import treeview


# noinspection PyUnresolvedReferences
class RAMSTKMatrixView(Gtk.TreeView):
    """
    The RAMSTK base widget for displaying RAMSTK Matrix views.

    The attributes of an RAMSTKBaseMatrix are:

    :ivar int _n_columns: the number of columns in the matrix.
    :ivar int _n_rows: the number rows in the matrix.
    :ivar list dic_icons: dictionary of icons to use in the various
        RAMSTKMatrix views.
    :ivar matrix: the RAMSTKDataMatrix to display in the Matrix View.
    :ivar matrixview: the Gtk.TreeView() displaying the RAMSTKDataMatrix.
    :type matrixview: :class:`Gtk.TreeView`
    """

    # noinspection PyMissingConstructor
    def __init__(self, module: str) -> None:
        """
        Initialize a RAMSTKMatrixView() instance.

        :return: None
        :rtype: None
        """
        GObject.GObject.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._matrix_type = module
        self._n_columns = 0
        self._n_rows = 0
        self._revision_id = None

        # Initialize public dictionary attributes.
        self.dic_icons = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.matrix = None
        self.n_fixed_columns = 0

        # Subscribe to PyPubSub messages.

    @staticmethod
    def _do_make_combo_cell() -> Gtk.CellRendererCombo:
        """
        Make a Gtk.CellRendererCombo().

        :return: _cell
        :rtype: :class:`Gtk.CellRendererCombo`
        """
        _cell = Gtk.CellRendererCombo()
        _cellmodel = Gtk.ListStore()
        _cellmodel.set_column_types([GObject.TYPE_STRING])
        _cellmodel.append([""])
        _cellmodel.append([_("Partial")])
        _cellmodel.append([_("Complete")])
        _cell.set_property('has-entry', False)
        _cell.set_property('model', _cellmodel)
        _cell.set_property('text-column', 0)

        return _cell

    @staticmethod
    def _resize_wrap(column: Gtk.TreeViewColumn, __param: Any,
                     cell: Gtk.CellRenderer) -> None:
        """
        Dynamically set the wrap-width property for a Gtk.CellRenderer().

        This method is called when the column width is resized.

        :param column: the Gtk.TreeViewColumn() being resized.
        :type column: :class:`Gtk.TreeViewColumn`
        :param GParamInt __param: the triggering parameter.
        :param cell: the Gtk.CellRenderer() that needs to be resized.
        :type cell: :class:`Gtk.CellRenderer`
        :return: None
        :rtype: None
        """
        _width = column.get_width()

        if _width > 0:
            _width += 10

        cell.set_property('wrap-width', _width)

    # pylint: disable=too-many-arguments
    def do_edit_cell(self,
                     cell: Gtk.CellRenderer,
                     path: str,
                     row: Gtk.TreeIter,
                     position: int,
                     idx_column: str) -> None:
        """
        Respond to `changed` signals for the Gtk.CellRendererCombo()s.

        :param cell: the Gtk.CellRendererCombo() calling this method.
        :type cell: :class:`Gtk.CellRendererCombo`
        :param str path: the path of the selected row in the RAMSTKMatrix.
        :param row: the Gtk.TreeIter() for the Gtk.CellRendererCombo() in the
            selected row in the RAMSTKMatrix.
        :type row: :class:`Gtk.TreeIter`
        :param int position: the position of the cell in the RAMSTKMatrix.
        :param int idx_column: the column_item_id of the Matrix cell to be
            edited.
        :return: None
        :rtype: None
        """
        _model = cell.get_property('model')
        _treemodel = self.get_model()

        _idx_row = int(path) + 1
        if _model.get_value(row, 0) == 'Partial':
            self.matrix.loc[_idx_row, idx_column] = 1
            _pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                self.dic_icons['partial'], 22, 22)
        elif _model.get_value(row, 0) == 'Complete':
            self.matrix.loc[_idx_row, idx_column] = 2
            _pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                self.dic_icons['complete'], 22, 22)
        else:
            self.matrix.loc[_idx_row, idx_column] = 0
            _pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                self.dic_icons['none'], 22, 22)

        _treemodel[path][position - 1] = _pixbuf

    def do_load_matrix(self, matrix: pd.DataFrame) -> None:
        """
        Load the RAMSTKMatrixView with the values from the data matrix.

        :param matrix: the data to display in the RAMSTKMatrixView() widget.
        :type matrix: :class:`pandas.DataFrame`
        :return: None
        :rtype: None
        """
        self.matrix = matrix
        self._n_columns = len(self.matrix.columns)
        self._n_rows = len(self.matrix.index) - 1

        _model = self.get_model()
        try:
            _model.clear()
        except AttributeError:
            _model = Gtk.ListStore()
        _model.set_column_types([GObject.TYPE_INT, GObject.TYPE_STRING]
                                + [GdkPixbuf.Pixbuf, GObject.TYPE_STRING]
                                * (self._n_columns - 2)
                                + [GObject.TYPE_STRING])
        self.set_model(_model)

        # The first column will contain a cell for the record ID and record
        # code.  The record ID will not be visible, but can be used for
        # program control.
        _id_cell = Gtk.CellRendererText()
        treeview.do_set_cell_properties(_id_cell,
                                        bg_color='light gray',
                                        visible=False)

        _code_cell = Gtk.CellRendererText()
        treeview.do_set_cell_properties(_code_cell, bg_color='light gray')
        _code_cell.set_alignment(0.9, 0.5)

        _column = treeview.do_make_column([_id_cell, _code_cell])
        _column.set_attributes(_id_cell, text=0)
        # noinspection PyArgumentList
        _column.set_attributes(_code_cell, markup=1)
        self.append_column(_column)

        # The remaining columns will be Gtk.CellRendererCombo()'s for
        # displaying the interaction between the row module and the column
        # module.
        i = 0
        j = 2
        for i in range(self._n_columns - 2):
            _heading = self.matrix.columns[i + 2]

            _cell = self._do_make_combo_cell()
            treeview.do_set_cell_properties(_cell, editable=True)

            _cell.connect('changed', self.do_edit_cell, i + j + 1, _heading)

            _pbcell = Gtk.CellRendererPixbuf()
            _pbcell.set_property('xalign', 0.5)

            _column = treeview.do_make_column([_pbcell, _cell],
                                              heading=_heading)
            _label = _column.get_widget()
            _label.set_angle(90.0)
            _column.set_widget(_label)
            # noinspection PyArgumentList
            _column.set_attributes(_pbcell, pixbuf=i + j)
            self.append_column(_column)

            j += 1

        # Add one more column so the last column will not be extra wide.
        _cell = Gtk.CellRendererText()
        _column = treeview.do_make_column([_cell])
        _column.set_attributes(_cell, text=i + j + 2)
        self.append_column(_column)

        # Now we load the data into the RAMSTK Matrix View.
        for i in list(self.matrix.index)[1:]:
            _data = [
                self.matrix.loc[i, 'id'], "<span weight='bold'>"
                + self.matrix.loc[i, 'display_name'] + "</span>"
            ]
            for j in list(self.matrix.loc[i][2:]):
                _pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self.dic_icons[['none', 'partial', 'complete'][j]], 22, 22)
                _data.append(_pixbuf)
                _data.append(['', 'Partial', 'Complete'][j])
            _data.append('')

            _model.append(_data)
