# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.treeviews.treeview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKTreeView module."""

# Standard Library Imports
from typing import Any, Dict, List, Optional

# Third Party Imports
# noinspection PyPackageRequirements
import treelib

# RAMSTK Package Imports
from ramstk.utilities import sort_dict
from ramstk.views.gtk3 import GdkPixbuf, GObject, Gtk

# RAMSTK Local Imports
from ..label import RAMSTKLabel
from ..widget import RAMSTKBaseWidget, WidgetProperties
from . import (
    RAMSTKCellRendererCombo,
    RAMSTKCellRendererSpin,
    RAMSTKCellRendererText,
    RAMSTKCellRendererToggle,
)


def do_make_column(
    cells: List[object], heading: str, visible: bool
) -> Gtk.TreeViewColumn:
    """Make a Gtk.TreeViewColumn.

    :param cells: list of Gtk.CellRenderers that are to be packed in
        the column.
    :param heading: the text for the column heading.
    :param visible: whether the column will be visible.
    :return: _column
    :rtype: :class:`Gtk.TreeViewColumn`
    """
    _column = Gtk.TreeViewColumn("")

    for _cell in cells:
        if isinstance(_cell, Gtk.CellRendererPixbuf):
            _column.pack_start(_cell, False)
        else:
            _column.pack_start(_cell, True)

    _label = RAMSTKLabel(heading)  # type: ignore
    _label.do_set_properties(
        {
            "height_request": -1,
            "justify": Gtk.Justification.CENTER,
            "width_request": -1,
        }
    )
    _column.set_widget(_label)
    _column.set_resizable(True)
    _column.set_alignment(0.5)
    _column.set_visible(visible)

    return _column


class RAMSTKTreeView(Gtk.TreeView, RAMSTKBaseWidget):
    """The RAMSTKTreeView class."""

    # Define private class attributes.
    _default_height: int = -1
    _default_width: int = -1
    _edit_signal: str = "changed"

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKTreeView widget."""
        RAMSTKBaseWidget.__init__(self)
        GObject.GObject.__init__(self)

        # Initialize public instance attributes.
        self.dic_field_position_map: Dict[str, int] = {}
        self.filtered_model: Gtk.TreeModelFilter = Gtk.TreeModelFilter()
        self.icon = GdkPixbuf.Pixbuf()
        self.selection = self.get_selection()
        self.unfiltered_model = self.get_model()

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKTreeView.

        The properties of the RAMSTKCellRenderers associated with the RAMSTKTreeView
        will be set by the RAMSTKTreePanel.do_set_widget_properties method.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKTreeView.
        """
        super().do_set_properties(properties)

        self.dic_properties["enable_grid_lines"] = properties.get(
            "enable_grid_lines", Gtk.TreeViewGridLines.BOTH
        )
        self.dic_properties["enable_tree_lines"] = properties.get(
            "enable_tree_lines", True
        )
        self.dic_properties["level_indentation"] = properties.get(
            "level_indentation", 2
        )
        self.dic_properties["rubber_banding"] = properties.get("rubber_banding", True)
        self.dic_properties["tooltip_column"] = properties.get("tooltip_column", 0)

        self.set_enable_tree_lines(self.dic_properties["enable_tree_lines"])
        self.set_grid_lines(self.dic_properties["enable_grid_lines"])
        self.set_tooltip_column(self.dic_properties["tooltip_column"])

    # def do_update(self,
    # package: Dict[str, Union[bool, date, float, int, str]]) -> None:
    # TODO: THIS MAY NOT BE NEEDED FOR THE RAMSTKTreeView or the RAMSTKTreeView METHOD
    #     would call the individual cell renderer do_update methods.

    # def on_changed(self) -> None:
    # TODO: THIS MAY NOT BE NEEDED FOR THE RAMSTKTreeView or the RAMSTKTreeView method
    #     would call the individual cell renderer on_changed methods.

    # ----- ----- RAMSTKTreeView specific methods. ----- ----- #
    def do_delete_row(self, filtered: bool) -> None:
        """Update the RAMSTKTreeView after deleting a row.

        :param filtered: whether to update the RAMSTKTreeView filtered model or the
            unfiltered model.
        """
        _model, _row = self.selection.get_selected()

        if not _row:
            return

        if filtered:
            _row = self.filtered_model.convert_iter_to_child_iter(_row)
            self.unfiltered_model.remove(_row)
            self.filtered_model.refilter()
        else:
            self.unfiltered_model.remove(_row)
            _row = _model.get_iter_first()
            if _row:
                self.selection.select_iter(_row)
                self.show_all()

    def do_insert_row(self, data: Dict[str, Any], prow: Gtk.TreeIter = None) -> None:
        """Insert a new row in the RAMSTKTreeView.

        :param data: the data dictionary for the new row to insert.
        :param prow: the parent row of the row to insert.
        """
        _model, _row = self.selection.get_selected()

        # FIXME: Move this to the tree panel classes and use the
        #  _lst_widget_configuration dict to determine position.  Then pass the clean
        #  data dict to this method.
        _data = [data[_key] for _key in self.position]

        _row = _model.append(prow, data)

        _path = _model.get_path(_row)
        _column = self.get_column(0)
        self.set_cursor(_path, None, False)
        self.row_activated(_path, _column)

    def do_load_cellrenderercombo(
        self,
        column: str,
        entries: List[str],
        clear: bool = True,
    ) -> None:
        """Retrieve the Gtk.TreeModel from a Gtk.CellRendererCombo.

        :param column: the column number to retrieve the cell's model.
        :param entries: the list of entries to load into the Gtk.CellRendererCombo.
        :param clear: whether to clear the Gtk.TreeModel().  Default is True.
        """
        _index = self.dic_field_position_map[column]
        _column = self.get_column(_index)
        _cell = _column.get_cells()[0]
        _cell.do_load_combo(entries)

        # TODO: Add method to RAMSTKCellRendererCombo to clear the model if needed.
        if clear:
            pass
        #    _cell.clear()

    def do_load_tree(
        self,
        tree: treelib.Tree,
        row: Optional[Gtk.TreeIter] = None,
        nid: Optional[int] = None,
    ) -> None:
        """Load the RAMSTKTreeView with the contents of the tree.

        :param tree: the Treelib tree containing the data packages to load into the
            RAMSTKTreeView.
        :param row: the parent Gtk.TreeIter.
        :param nid: the node identifier for the node whose data package is being added
            to the RAMSTKTreeView model.
        """
        _node = None
        _row = None

        for _node in tree.all_nodes():
            if _node.data is not None:
                [[__, _entity]] = _node.data.items()
                _attributes = _entity.get_attributes()
                _data = [
                    _attributes.get(_key, None) for _key in self.dic_field_position_map
                ]
                # FIXME: This is a hack to get the icon to display in the first
                #  column.  We need to add the icon to the data dict in the tree maybe?
                _data.append(self.icon)
                _row = self.unfiltered_model.append(row, _data)

            for _n in tree.children(_node.identifier):
                self.do_load_tree(tree.subtree(_n.identifier), _row, _n.identifier)

    def do_make_column(self, cellrenderer: Gtk.CellRenderer, n_fields: int) -> None:
        """Make a column for the RAMSTKTreeView.

        :param cellrenderer: the RAMSTKCellRenderer to associate with the column.
        :param n_fields: the total number of database fields this RAMSTKTreeView will
            ultimately display.
        """
        _cellrenderer = cellrenderer["widget"]

        # Add a Gtk.CellRendererPixbuf to the first column so the RAMSTKTreeView can
        # display an icon if needed.
        if _cellrenderer.index == 0:
            _pbcell = Gtk.CellRendererPixbuf()
            _pbcell.set_property("xalign", 0.5)
            _column = do_make_column(
                [_pbcell, _cellrenderer],
                heading=_cellrenderer.label_text,
                visible=cellrenderer["properties"]["visible"],
            )
            _column.set_attributes(_pbcell, pixbuf=n_fields)
        else:
            _column = do_make_column(
                [_cellrenderer],
                heading=_cellrenderer.label_text,
                visible=cellrenderer["properties"]["visible"],
            )

        _column.set_cell_data_func(
            _cellrenderer,
            self._do_format_cell,
        )

        self._do_set_column_properties(_cellrenderer, _column)
        self.append_column(_column)
        self.dic_field_position_map[cellrenderer["attributes"]["field"]] = cellrenderer[
            "attributes"
        ]["index"]

    def do_make_model(self, column_types: List[str], store_type: str = "tree") -> None:
        """Make the RAMSTKTreeView data model.

        :param column_types: the list of data types for the RAMSTKTreeView model to
            display.
        :param store_type: the type of store for the RAMSTKTreeView to display. Default
            is 'tree', other option is 'list'.
        """
        if store_type == "tree":
            self.unfiltered_model = Gtk.TreeStore(*column_types)
        else:
            self.unfiltered_model = Gtk.ListStore(*column_types)
        self.set_model(self.unfiltered_model)

        # Sort the field-position map dict by position in ascending order.
        self.dic_field_position_map = sort_dict(self.dic_field_position_map)

    def do_set_visible_columns(self) -> None:
        """Set the treeview columns visible or hidden."""
        # FIXME: Only the allocation, FMEA, and preferences dialog tree panel call this
        #  method at this time.  The usage profile and similar item tree
        #  panels should also use this method to set the visibility of their columns.
        #  Also re-write this method to take a dict of column visibility as an
        #  argument where the key is the field name and the value is a True/False.
        for _key, _visible in self.visible.items():
            _column = self.get_column(self.position[_key])
            _column.set_visible(_visible)

    @staticmethod
    def _do_format_cell(
        __column: Gtk.TreeViewColumn,
        cellrenderer: Gtk.CellRenderer,
        model: Gtk.TreeModel,
        row: Gtk.TreeIter,
        data: Optional[object],
    ) -> None:
        """Set the formatting of the RAMSTKTreeView RAMSTKCellRenderer.

        :param __column: the Gtk.TreeViewColumn containing the RAMSTKCellRenderer to
            format.
        :param cellrenderer: the RAMSTKCellRenderer to format.
        :param model: the Gtk.TreeModel containing the Gtk.TreeViewColumn.
        :param row: the Gtk.TreeIter pointing to the row containing the
            RAMSTKCellRenderer to format.
        :param data: user data.
        """
        cellrenderer.tree_model = model
        cellrenderer.tree_row = row
        if cellrenderer.datatype not in ["gfloat", "gint"] or isinstance(
            cellrenderer, Gtk.CellRendererToggle
        ):
            return

        cellrenderer.set_property("text", cellrenderer.format.format(data))

    @staticmethod
    def _do_set_column_properties(
        cellrenderer: Gtk.CellRenderer, column: Gtk.TreeViewColumn
    ) -> None:
        """Set the properties of the RAMSTKTreeView column.

        :param cellrenderer: the widget configuration dict for the RAMSTKCellRenderer
            associated with this column.
        :param column: the Gtk.TreeViewColumn whose properties are to be set.
        """
        if isinstance(cellrenderer, RAMSTKCellRendererToggle):
            column.set_attributes(cellrenderer, active=cellrenderer.index)
        elif isinstance(
            cellrenderer,
            (
                RAMSTKCellRendererCombo,
                RAMSTKCellRendererSpin,
                RAMSTKCellRendererText,
            ),
        ):
            column.set_attributes(cellrenderer, text=cellrenderer.index)

        if cellrenderer.index > 0:
            column.set_reorderable(True)

    # ----- ----- Methods that are of unknown use at this time.
    def do_get_row_by_value(self, search_col: int, value: Any) -> Gtk.TreeIter:
        """Find the row in the RAMSTKTreeView containing the passed value.

        :param search_col: the column number to search for the desired value.
        :param value: the value to match.
        :return: _iter; the Gtk.TreeIter for the matching row.
        :rtype: :class:`Gtk.TreeIter`
        """
        # FIXME: This method is called by the Allocation and Similar Item panels in
        #  their _do_set_<>_attributes methods to get the row of the RAMSTKTreeView
        #  corresponding to a particular attribute to update in the RAMSTKTreeView.
        #  There is likely a better way to update the RAMSTKTreeView than that and
        #  this method is probably not needed.
        _row = self.unfiltered_model.get_iter_first()

        while (
            _row is not None
            and self.unfiltered_model.get_value(_row, search_col) != value
        ):
            _row = self.unfiltered_model.iter_next(_row)

        return _row

    def do_set_editable_columns(self, method: object) -> None:
        """Set the treeview columns editable or read-only.

        :param method: the callback method for the cell.
        """
        # FIXME: Only the preferences dialog tree panel calls this method.  It is
        #  unlikely this method will be needed after re-writing that class.
        for _key in self.editable:
            _column = self.get_column(self.position[_key])

            # Get the last cell so those columns containing a
            # Gtk.CellRendererPixBuf() will return the Gtk.CellRendererText()
            # that is packed with it.  If there is only one cell renderer,
            # that is the one that will be returned.
            _cell = _column.get_cells()[-1]

            if isinstance(self.widgets[_key], Gtk.CellRendererToggle):
                _cell.connect("toggled", method, None, self.position[_key])
            elif isinstance(
                self.widgets[_key],
                (Gtk.CellRendererSpin, Gtk.CellRendererText),
            ):
                _cell.connect("edited", method, self.position[_key])

    @staticmethod
    def _resize_wrap(
        column: Gtk.TreeViewColumn, __param, cell: Gtk.CellRenderer
    ) -> None:
        """Dynamically set wrap-width property for a Gtk.CellRenderer().

        This is called whenever the column width in the Gtk.TreeView() is resized.

        :param column: the Gtk.TreeViewColumn() being resized.
        :param GParamInt __param: the triggering parameter.
        :param cell: the Gtk.CellRenderer() that needs to be resized.
        """
        # FIXME: This method is unused, but could be useful.
        _width = column.get_width()

        if _width <= 0:
            _width = 25
        else:
            _width += 10

            try:
                cell.set_property("wrap-width", _width)
            except TypeError:  # This is a Gtk.CellRendererToggle
                cell.set_property("width", _width)
