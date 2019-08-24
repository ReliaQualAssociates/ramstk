# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.matrix.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKBaseMatrix Module."""

# Standard Library Imports
import locale
from typing import Any, Dict, List

# Third Party Imports
import pandas as pd
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.views.gtk3 import GdkPixbuf, GObject, Gtk, Pango, _

# RAMSTK Local Imports
from .button import do_make_buttonbox
from .label import RAMSTKLabel


class RAMSTKBaseMatrix(Gtk.HBox):
    """
    The RAMSTK base widget for displaying RAMSTK Matrix views.

    The attributes of an RAMSTKBaseMatrix are:

    :ivar list _dic_icons: dictionary of icons to use in the various
        RAMSTKMatrix views.
    :ivar _ramstk_matrix: the RAMSTKDataMatrix to display in the Matrix View.
    :ivar int _n_columns: the number of columns in the matrix.
    :ivar int _n_rows: the number rows in the matrix.
    :ivar matrix: the Gtk.TreeView() displaying the RAMSTKDataMatrix.
    :type matrix: :class:`Gtk.TreeView`
    """

    RAMSTK_CONFIGURATION = None

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 test: bool = False,
                 **kwargs: Any) -> None:
        """
        Initialize an instance of the RAMSTKBaseMatrix widget class.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param bool test: indicates whether the RAMSTBaseMatrix is being
            created by a test or not (default).
        """
        self.RAMSTK_USR_CONFIGURATION = configuration

        # Initialize private dictionary attributes.
        self._dic_icons = {
            0:
            self.RAMSTK_USR_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/none.png',
            1:
            self.RAMSTK_USR_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/partial.png',
            2:
            self.RAMSTK_USR_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/complete.png',
            'save':
            self.RAMSTK_USR_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/save.png',
            'save-all':
            self.RAMSTK_USR_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/save-all.png',
            'view-refresh':
            self.RAMSTK_USR_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/view-refresh.png'
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._matrix_type = kwargs['matrix_type']
        self._revision_id = None
        self._ramstk_matrix = None
        self._n_columns = 0
        self._n_rows = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.n_fixed_columns = 0
        self.hbx_tab_label = Gtk.HBox()
        self.matrix = Gtk.TreeView(None)

        try:
            locale.setlocale(locale.LC_ALL,
                             self.RAMSTK_USR_CONFIGURATION.RAMSTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        if not test:
            self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_matrix, 'retrieved_matrix')

    def __make_ui(self) -> None:
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.pack_start(
            do_make_buttonbox(
                self,
                icons=['view-refresh'],
                tooltips=[
                    self._dic_matrix_labels[self._matrix_type][0],
                ],
                callbacks=[self._do_request_create],
                orientation='vertical',
                height=-1,
                width=-1), False, False, 0)

        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.add(self.matrix)

        self.pack_end(_scrolledwindow, True, True, 0)

        _label = Gtk.Label()
        _label.set_markup("<span weight='bold'>"
                          + self._dic_matrix_labels[self._matrix_type][1]
                          + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(Gtk.Justification.CENTER)
        _label.show_all()
        _label.set_tooltip_text(self._dic_matrix_labels[self._matrix_type][2])

        # self.hbx_tab_label.pack_start(_image, True, True, 0)
        self.hbx_tab_label.pack_end(_label, True, True, 0)
        self.hbx_tab_label.show_all()

        self.show_all()

    def _do_set_properties(self, cell: Gtk.CellRenderer, editable: bool,
                           position: int, col_index: int,
                           model: Gtk.TreeModel) -> None:
        """
        Set common properties of Gtk.CellRenderers().

        :param cell: the cell whose properties are to be set.
        :type cell: :class:`Gtk.CellRenderer`
        :param bool editable: indicates whether or not the cell is editable.
        :param int position: the position in the Gtk.TreeModel() that this cell
            falls.
        :param int col_index: the column_item_id of the Matrix cell to be
            edited.
        :param model: the :class:`Gtk.TreeModel` associated with the treeview.
        :return: None
        :rtype: None
        """
        cell.set_property('background', '#FFFFFF')
        cell.set_property('editable', editable)
        cell.set_property('foreground', '#000000')
        cell.set_property('wrap-width', 250)
        cell.set_property('wrap-mode', Pango.WrapMode.WORD_CHAR)
        cell.set_property('yalign', 0.1)
        cell.connect('changed', self._on_cell_edit, position, col_index, model)

    def _make_column(self,
                     cells: List[Gtk.CellRenderer],
                     heading: str,
                     visible: bool = True) -> Gtk.TreeViewColumn:
        """
        Make a Gtk.TreeViewColumn().

        :param list cells: list of Gtk.CellRenderer()s that are to be packed in
            the column.
        :param str heading: the column heading text.
        :return: _column
        :rtype: :class:`Gtk.TreeViewColumn`
        """
        _column = Gtk.TreeViewColumn("")

        for _cell in cells:
            if isinstance(_cell, Gtk.CellRendererPixbuf):
                _column.pack_start(_cell, False)
            else:
                _column.pack_start(_cell, True)
                _column.connect('notify::width', self._on_resize_wrap, _cell)

        _label = RAMSTKLabel(heading)
        _label.do_set_properties(width=-1,
                                 height=-1,
                                 justify=Gtk.Justification.CENTER)
        _label.set_angle(90)
        _column.set_widget(_label)
        _column.set_resizable(True)
        _column.set_alignment(0.5)
        _column.set_visible(visible)

        return _column

    @staticmethod
    def _make_combo_cell() -> Gtk.CellRendererCombo:
        """
        Make a Gtk.CellRendererCombo().

        :return: _cell
        :rtype: :class:`Gtk.CellRendererCombo`
        """
        _cell = Gtk.CellRendererCombo()
        _cellmodel = Gtk.ListStore(GObject.TYPE_STRING)
        _cellmodel.append([""])
        _cellmodel.append([_("Partial")])
        _cellmodel.append([_("Complete")])
        _cell.set_property('has-entry', False)
        _cell.set_property('model', _cellmodel)
        _cell.set_property('text-column', 0)

        return _cell

    # pylint: disable=too-many-arguments
    def _on_cell_edit(self, cell: Gtk.CellRendererCombo, path: str,
                      row: Gtk.TreeIter, position: int, col_index: int,
                      model: Gtk.TreeModel) -> None:
        """
        Respond to `changed` signals for the Gtk.CellRendererCombo()s.

        :param cell: the Gtk.CellRendererCombo() calling this method.
        :type cell: :class:`Gtk.CellRendererCombo`
        :param str path: the path of the selected row in the RAMSTKMatrix.
        :param row: the Gtk.TreeIter() for the Gtk.CellRendererCombo() in the
            selected row in the RAMSTKMatrix.
        :type row: :class:`Gtk.TreeIter`
        :param int position: the position of the cell in the RAMSTKMatrix.
        :param int col_index: the column_item_id of the Matrix cell to be
            edited.
        :param model: the Gtk.TreeModel() associated with the RAMSTKMatrix.
        :type model: :class:`Gtk.TreeModel`
        :return: None
        :rtype: None
        """
        _model = cell.get_property('model')

        _column_item_id = col_index
        _row_item_id = model[path][0]
        if _model.get_value(row, 0) == 'Partial':
            self._ramstk_matrix[_column_item_id][_row_item_id] = 1
            _pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                self._dic_icons[1], 22, 22)
        elif _model.get_value(row, 0) == 'Complete':
            self._ramstk_matrix[_column_item_id][_row_item_id] = 2
            _pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                self._dic_icons[2], 22, 22)
        else:
            self._ramstk_matrix[_column_item_id][_row_item_id] = 0
            _pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                self._dic_icons[0], 22, 22)

        model[path][position - 1] = _pixbuf

    @staticmethod
    def _on_resize_wrap(column: Gtk.TreeViewColumn, __param: Any,
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

    def do_load_matrix(self, matrix: pd.DataFrame,
                       column_headings: Dict[int, str],
                       row_headings: Dict[int, str], rows: str) -> None:
        """
        Load the RAMSTKMatrix view with the values from the RAMSTKDataMatrix.

        :param matrix: the RAMSTKDataMatrix to display in the RAMSTKMatrix
            widget.
        :type matrix: :class:`ramstk.views.gtk3.widgets.matrix.RAMSTKMatrix`
        :param dict column_headings: the dicionary containing the headings to
            use for the matrix columns.  Keys are the column <MODULE> IDs;
            values are a noun field associated with the key.
        :param dict row_headings: the dictionary containing the headings to
            use for the matrix rows.  Keys are the row <MODULE> IDs; values are
            a noun field associated with the key.
        :param str rows: the heading to put in the first column of the matrix.
            This indicates what information is found in the rows.
        :return: None
        :rtype: None
        """
        self._ramstk_matrix = matrix
        self._n_columns = len(self._ramstk_matrix.columns)
        self._n_rows = len(self._ramstk_matrix.index)

        _gobject_types = [GObject.TYPE_INT, GObject.TYPE_STRING] + \
                         [GdkPixbuf.Pixbuf, GObject.TYPE_STRING] * \
            (self._n_columns) + [GObject.TYPE_STRING]

        _model = Gtk.TreeStore(*_gobject_types)

        self.matrix.set_model(_model)

        # The first column will contain the Function ID and Function Code.
        _cell = Gtk.CellRendererText()
        _cell.set_property('background', 'light gray')
        _column = self._make_column([
            _cell,
        ], '', visible=False)
        _column.set_attributes(_cell, text=0)
        _cell = Gtk.CellRendererText()
        _cell.set_alignment(0.9, 0.5)
        _cell.set_property('background', 'light gray')
        _cell.set_property('editable', False)
        _cell.set_property('foreground', '#000000')
        _cell.set_property('wrap-width', 250)
        _cell.set_property('wrap-mode', Pango.WrapMode.WORD_CHAR)
        _column = self._make_column([
            _cell,
        ], rows)
        _column.set_attributes(_cell, markup=1)
        self.matrix.append_column(_column)

        # The remaining columns will be Gtk.CellRendererCombo()'s for
        # displaying the interaction between Function and Hardware.
        j = 2
        for i in range(self._n_columns):  # pylint: disable=E0602
            _cell = self._make_combo_cell()
            self._do_set_properties(_cell, True, i + j + 1,
                                    self._ramstk_matrix.columns[i], _model)

            _pbcell = Gtk.CellRendererPixbuf()
            _pbcell.set_property('xalign', 0.5)
            _heading = column_headings[self._ramstk_matrix.columns[i]]
            _column = self._make_column([_pbcell, _cell], _heading)
            _column.set_attributes(_pbcell, pixbuf=i + j)
            self.matrix.append_column(_column)

            j += 1

        # Add one more column so the last column will not be extra wide.
        _column = self._make_column([
            Gtk.CellRendererText(),
        ], '')

        try:
            # pylint: disable=undefined-loop-variable
            _column.set_attributes(_cell, text=i + j + 1)
        except UnboundLocalError:
            _column.set_visible(False)

        self.matrix.append_column(_column)

        # Now we load the data into the RAMSTK Matrix View.
        for i in list(self._ramstk_matrix.index):
            _data = [i, "<span weight='bold'>" + row_headings[i] + "</span>"]
            for j in list(self._ramstk_matrix.loc[i]):
                _pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self._dic_icons[j], 22, 22)
                _data.append(_pixbuf)
                _data.append(j)
            _data.append('')

            _model.append(None, _data)
