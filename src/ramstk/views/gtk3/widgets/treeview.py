# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.treeview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKTreeView Module."""

# Standard Library Imports
import datetime
from typing import Any, Callable, Dict, List, Tuple

# Third Party Imports
import toml
import treelib

# RAMSTK Package Imports
from ramstk.utilities import deprecated, string_to_boolean
from ramstk.views.gtk3 import Gdk, GdkPixbuf, GObject, Gtk, Pango

# RAMSTK Local Imports
from .label import RAMSTKLabel
from .widget import RAMSTKWidget


def do_make_column(cells: List[object], **kwargs: Dict[str, Any]) -> Gtk.TreeViewColumn:
    """Make a Gtk.TreeViewColumn().

    :param list cells: list of Gtk.CellRenderer()s that are to be packed in
        the column.
    :return: _column
    :rtype: :class:`Gtk.TreeViewColumn`
    """
    _heading = kwargs.get("heading", "")
    _visible = kwargs.get("visible", True)

    _column = Gtk.TreeViewColumn("")

    for _cell in cells:
        if isinstance(_cell, Gtk.CellRendererPixbuf):
            _column.pack_start(_cell, False)
        else:
            _column.pack_start(_cell, True)

    _label = RAMSTKLabel(_heading)  # type: ignore
    _label.do_set_properties(width=-1, height=-1, justify=Gtk.Justification.CENTER)
    _column.set_widget(_label)
    _column.set_resizable(True)
    _column.set_alignment(0.5)
    _column.set_visible(_visible)

    return _column


def do_set_cell_properties(cell: object, properties: Dict[str, Any]) -> None:
    """Set common properties of Gtk.CellRenderers().

    :param cell: the cell whose properties are to be set.
    :param properties: the properties for the cell.
    :return: None
    :rtype: None
    """
    _bg_color = properties.get("bg_color", "#FFFFFF")
    _digits = properties.get("digits", 2)
    _editable = properties.get("editable", False)
    _fg_color = properties.get("fg_color", "#000000")
    _lower = properties.get("lower", 1)
    _step = properties.get("step", 1)
    _upper = properties.get("upper", 10)
    _visible = properties.get("visible", True)
    _weight = properties.get("weight", 400)
    _weight_set = properties.get("weight_set", False)

    if not _editable:
        _color = Gdk.RGBA(255.0, 255.0, 255.0, 1.0)
        _fg_color = "#000000"
        cell.set_property("cell-background-rgba", _color)  # type: ignore

    cell.set_property("visible", _visible)  # type: ignore
    cell.set_property("yalign", 0.1)  # type: ignore

    if isinstance(cell, Gtk.CellRendererCombo):
        _cellmodel = Gtk.ListStore(GObject.TYPE_STRING)
        _cellmodel.append([""])
        cell.set_property("editable", _editable)
        cell.set_property("has-entry", False)
        cell.set_property("model", _cellmodel)
        cell.set_property("text-column", 0)
    elif isinstance(cell, Gtk.CellRendererSpin):
        _adjustment = Gtk.Adjustment(lower=_lower, upper=_upper, step_incr=_step)
        cell.set_property("adjustment", _adjustment)
        cell.set_property("digits", _digits)
        cell.set_property("editable", _editable)
    elif isinstance(cell, Gtk.CellRendererText):
        cell.set_property("background", _bg_color)
        cell.set_property("editable", _editable)
        cell.set_property("foreground", _fg_color)
        cell.set_property("weight", _weight)
        cell.set_property("weight-set", _weight_set)
        cell.set_property("wrap-width", 250)
        cell.set_property("wrap-mode", Pango.WrapMode.WORD)
    elif isinstance(cell, Gtk.CellRendererToggle):
        cell.set_property("activatable", _editable)
        cell.set_property("cell-background", _bg_color)


class RAMSTKTreeView(Gtk.TreeView, RAMSTKWidget):
    """The RAMSTKTreeView class."""

    def __init__(self) -> None:
        """Initialize a RAMSTKTreeView() instance.

        :return: None
        :rtype: None
        """
        # noinspection PyCallByClass,PyTypeChecker
        RAMSTKWidget.__init__(self)
        GObject.GObject.__init__(self)

        # Initialize private dictionary instance attributes:
        self.dic_row_loader: Dict[str, Callable] = {}

        # Initialize private list instance attributes:

        # Initialize private scalar instance attributes.
        self._has_pixbuf: bool = False

        # Initialize public dictionary instance attributes.
        self.cellprops: Dict[str, Any] = {}
        self.datatypes: Dict[str, str] = {}
        self.editable: Dict[str, bool] = {}
        self.headings: Dict[str, str] = {}
        self.position: Dict[str, int] = {}
        self.visible: Dict[str, bool] = {}
        self.widgets: Dict[str, object] = {}

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.filt_model: Gtk.TreeModelFilter = Gtk.TreeModelFilter()
        self.selection = self.get_selection()
        self.unfilt_model = self.get_model()

    def do_change_cell(
        self,
        cell: Gtk.CellRenderer,
        path: str,
        new_row: Gtk.TreeIter,
        position: int,
    ) -> Any:
        """Handle Gtk.CellRenderer() edits.

        :param cell: the Gtk.CellRenderer() that was edited.
        :param path: the Gtk.TreeView() path of the Gtk.CellRenderer() that
            was edited.
        :param new_row: the new Gtk.TreeIter() selected in the
            Gtk.CellRendererCombo().  This is relative to the cell renderer's model,
            not the RAMSTKTreeView() model.
        :param position: the column position of the edited
            Gtk.CellRenderer().
        :return: new_text; the value of the new text converted to the
            correct data type for the attribute being edited.
        """
        _model = self.get_model()
        _cell_model = cell.get_property("model")

        _new_text = _cell_model.get_value(new_row, 0)

        _idx = 0
        _iter = _cell_model.get_iter_first()
        while _iter is not None:
            if _cell_model.get_value(_iter, 0) == _new_text:
                _model[path][position] = _new_text
                break
            _iter = _cell_model.iter_next(_iter)
            _idx += 1

        return _idx

    def do_edit_cell(
        self, cell: Gtk.CellRenderer, path: str, new_text: Any, position: int
    ) -> Any:
        """Handle Gtk.CellRenderer() edits.

        :param cell: the Gtk.CellRenderer() that was edited.
        :param path: the Gtk.TreeView() path of the Gtk.CellRenderer() that
            was edited.
        :param new_text: the new text in the edited Gtk.CellRenderer().
        :param position: the column position of the edited
            Gtk.CellRenderer().
        :return: new_text; the value of the new text converted to the
            correct data type for the attribute being edited.
        :rtype: Any
        """
        _model = self.get_model()
        _convert = GObject.type_name(_model.get_column_type(position))

        if isinstance(cell, Gtk.CellRendererToggle):
            new_text = not cell.get_active()
        elif _convert == "gchararray":
            new_text = str(new_text)
        elif _convert == "gint":
            try:
                new_text = int(new_text)
            except ValueError:
                new_text = int(float(new_text))
        elif _convert == "gfloat":
            new_text = float(new_text)

        _model[path][position] = new_text

        return new_text

    @deprecated
    def do_expand_tree(self) -> None:
        """Expand the RAMSTKTreeView().

        Currently unused.  Determine if it has value.

        :return: None
        :rtype: None
        """
        _model = self.get_model()
        try:
            _row = _model.get_iter_first()
        except AttributeError:
            _row = None

        self.expand_all()
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.get_column(0)
            self.set_cursor(_path, None, False)
            self.row_activated(_path, _column)

    def do_get_row_by_value(self, search_col: int, value: Any) -> Gtk.TreeIter:
        """Find the row in the RAMSTKTreeView() containing the passed value.

        :param search_col: the column number to search for the desired value.
        :param value: the value to match.
        :return: _iter; the Gtk.TreeIter() for the matching row.
        :rtype: :class:`Gtk.TreeIter`
        """
        _row = self.unfilt_model.get_iter_first()

        while _row is not None:
            if self.unfilt_model.get_value(_row, search_col) == value:
                break

            _row = self.unfilt_model.iter_next(_row)

        return _row

    def do_insert_row(self, data: Dict[str, Any], prow: Gtk.TreeIter = None) -> None:
        """Insert a new row in the treeview.

        :param data: the data dictionary for the new row to insert.
        :param prow: the parent row of the row to insert.
        :return: None
        :rtype: None
        """
        _model, _row = self.selection.get_selected()

        _data = [data[_key] for _key in self.position]

        _row = _model.append(prow, _data)

        _path = _model.get_path(_row)
        _column = self.get_column(0)
        self.set_cursor(_path, None, False)
        self.row_activated(_path, _column)

    def do_load_combo_cell(self, index: int, items: List[str]) -> None:
        """Load items into cell with combobox.

        :param index: the index in the RAMSTKTreeView() model of the
            Gtk.CellRendererCombo() to load.
        :param items: the list of entries to load into the Gtk.CellRendererCombo().
        :return: None
        :rtype: None
        """
        _model = self.get_cell_model(index)
        for _item in items:
            _model.append([_item])

    def do_load_tree(self, tree: treelib.Tree, row: Gtk.TreeIter = None) -> None:
        """Load the RAMSTKTreeView with the contents of the tree."""
        _row = None
        _node = tree.get_node(tree.root)

        if _node.data is not None:
            _row = self.dic_row_loader[_node.tag](_node, row)

        for _n in tree.children(_node.identifier):
            self.do_load_tree(tree.subtree(_n.identifier), _row)

    def do_make_columns(self) -> None:
        """Make the columns for the RAMSTKTreeView().

        :return: None
        :rtype: None
        """
        for _key, _position in self.position.items():
            _cell = self.widgets[_key]
            _properties = {
                "editable": self.editable[_key],
                **self.cellprops[_key],
            }
            do_set_cell_properties(
                _cell,
                properties=_properties,
            )
            # If creating a RAMSTKTreeView() that displays icons and this is
            # the first column we're creating, add a Gtk.CellRendererPixbuf()
            # to go along with the data in the first column.
            if self._has_pixbuf and _position == 0:
                _pbcell = Gtk.CellRendererPixbuf()
                _pbcell.set_property("xalign", 0.5)
                _pbcell.set_property("cell-background", _properties["bg_color"])
                _column = do_make_column(
                    [_pbcell, _cell],
                    heading="",  # type: ignore
                    visible=True,  # type: ignore
                )
                _column.set_attributes(_pbcell, pixbuf=len(self.position.values()))
            else:
                _column = do_make_column(
                    [_cell],
                    heading=self.headings[_key],  # type: ignore
                    visible=string_to_boolean(self.visible[_key]),  # type: ignore
                )

            _column.set_cell_data_func(
                _cell, self._do_format_cell, (_position, self.datatypes[_key])
            )

            self._do_set_column_properties(_key, _column)
            self.append_column(_column)

    def do_make_model(self) -> None:
        """Make the RAMSTKTreeView() data model.

        :return: None
        :rtype: None
        """
        _types = [
            GObject.type_from_name(_datatype)
            for __, _datatype in self.datatypes.items()
        ]

        if self._has_pixbuf:
            _types.append(GdkPixbuf.Pixbuf)

        self.unfilt_model = Gtk.TreeStore(*_types)
        self.set_model(self.unfilt_model)

    # noinspection PyTypeChecker
    def do_parse_format(self, fmt_file: str) -> None:
        """Parse the format file for the RAMSTKTreeView().

        :param fmt_file: the absolute path to the format file to read.
        :return: None
        :rtype: None
        """
        _format = toml.load(fmt_file)

        self._has_pixbuf = string_to_boolean(_format["pixbuf"])

        self.position = {}
        _keys = sorted(_format["position"], key=_format["position"].get)
        for _key in _keys:
            self.position[_key] = _format["position"][_key]
            self.editable[_key] = string_to_boolean(_format["editable"][_key])
            self.visible[_key] = string_to_boolean(_format["visible"][_key])

        self.headings = _format["usertitle"]

    def do_set_editable_columns(self, method: object) -> None:
        """Set the treeview columns editable or read-only.

        :param method: the callback method for the cell.
        :return: None
        """
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

    def do_set_visible_columns(self) -> None:
        """Set the treeview columns visible or hidden.

        :return: None
        :rtype: None
        """
        for _key, _visible in self.visible.items():
            _column = self.get_column(self.position[_key])
            _column.set_visible(_visible)

    def get_aggregate_attributes(self, entity: object) -> List[Any]:
        """Get the attributes for aggregate work stream modules.

        :param entity: the RAMSTK Program database table whose attributes
            are to be returned.
        :return: _attributes; a list of the attributes values in the order
            they will be displayed.
        :rtype: list
        """
        _attributes = []
        try:
            for _key in self.position:
                if _key == "dict":
                    _attributes.append(str(entity))
                else:
                    try:
                        if isinstance(entity[_key], datetime.date):  # type: ignore
                            entity[_key] = entity[_key].strftime(  # type: ignore
                                "%Y-%m-%d"
                            )
                        entity[_key] = entity[_key].decode("utf-8")  # type: ignore
                    except (AttributeError, KeyError):
                        pass
                    _attributes.append(entity[_key])  # type: ignore
        except TypeError:
            pass

        return _attributes

    def get_cell_model(self, column: int, clear: bool = True) -> Gtk.TreeModel:
        """Retrieve the Gtk.TreeModel() from a Gtk.CellRendererCombo().

        :param column: the column number to retrieve the cell's model.
        :param clear: whether or not to clear the Gtk.TreeModel().
            Default is True.
        :return: _model
        :rtype: :class:`Gtk.TreeModel`
        """
        _column = self.get_column(column)
        _cell = _column.get_cells()[0]
        _model = _cell.get_property("model")

        if clear:
            _model.clear()

        return _model

    def get_simple_attributes(self, entity: object) -> List[Any]:
        """Get the attributes for simple work stream modules.

        :param entity: the RAMSTK Program database table whose attributes
            are to be returned.
        :return: _attributes; a list of the attributes values in the order
            they will be displayed.
        :rtype: list
        """
        _attributes = []
        _temp = entity.get_attributes()  # type: ignore

        for _key in self.position:
            try:
                if isinstance(_temp[_key], datetime.date):
                    _temp[_key] = _temp[_key].strftime("%Y-%m-%d")
                _temp[_key] = _temp[_key].decode("utf-8")
            except (AttributeError, KeyError):
                pass
            _attributes.append(_temp[_key])

        return _attributes

    @staticmethod
    def _do_format_cell(
        __column: Gtk.TreeViewColumn,
        cell: Gtk.CellRenderer,
        model: Gtk.TreeModel,
        row: Gtk.TreeIter,
        data: Tuple[Any],
    ) -> None:
        """Set the formatting of the Gtk.Treeview() Gtk.CellRenderers().

        :param __column: the Gtk.TreeViewColumn() containing the
            Gtk.CellRenderer() to format.
        :type __column: :class:`Gtk.TreeViewColumn`
        :param cell: the Gtk.CellRenderer() to format.
        :type cell: :class:`Gtk.CellRenderer`
        :param model: the Gtk.TreeModel() containing the Gtk.TreeViewColumn().
        :type model: :class:`Gtk.TreeModel`
        :param row: the Gtk.TreeIter() pointing to the row containing the
            Gtk.CellRenderer() to format.
        :type row: :class:`Gtk.TreeIter`
        :param tuple data: a tuple containing the position and the data type.
        """
        if data[1] == "gfloat":  # type: ignore
            fmt = "{0:0.6g}"
        elif data[1] == "gint":  # type: ignore
            fmt = "{0:0d}"
        else:
            return

        val = model.get_value(row, data[0])
        try:
            cell.set_property("text", fmt.format(val))
        except (TypeError, ValueError):  # It's a Gtk.CellRendererToggle
            pass

    def _do_set_column_properties(self, key: str, column: Gtk.TreeViewColumn) -> None:
        """Set the properties of the RAMSTKTreeView() column.

        :param key: the value of the key in the widgets and position dicts.
        :param column: the Gtk.TreeViewColumn() to set properties.
        :return: None
        :rtype: None
        """
        _cell = column.get_cells()[-1]

        if isinstance(self.widgets[key], Gtk.CellRendererToggle):
            column.set_attributes(_cell, active=self.position[key])
        elif isinstance(
            self.widgets[key],
            (
                Gtk.CellRendererCombo,
                Gtk.CellRendererSpin,
                Gtk.CellRendererText,
            ),
        ):
            column.set_attributes(_cell, text=self.position[key])

        if self.position[key] > 0:
            column.set_reorderable(True)

    @staticmethod
    def _resize_wrap(
        column: Gtk.TreeViewColumn, __param, cell: Gtk.CellRenderer
    ) -> None:
        """Dynamically set wrap-width property for a Gtk.CellRenderer().

        This is called whenever the column width in the Gtk.TreeView() is
        resized.

        :param column: the Gtk.TreeViewColumn() being resized.
        :param GParamInt __param: the triggering parameter.
        :param cell: the Gtk.CellRenderer() that needs to be resized.
        :return: None
        :rtype: None
        """
        _width = column.get_width()

        if _width <= 0:
            _width = 25
        else:
            _width += 10

            try:
                cell.set_property("wrap-width", _width)
            except TypeError:  # This is a Gtk.CellRendererToggle
                cell.set_property("width", _width)


class CellRendererML(Gtk.CellRendererText):
    """Create a multi-line cell renderer."""

    def __init__(self) -> None:
        """Initialize a CellRendererML instance."""
        GObject.GObject.__init__(self)

        self.textedit_window = None
        self.selection = None
        self.treestore = None
        self.treeiter = None

        self.textedit = Gtk.TextView()
        self.textbuffer = self.textedit.get_buffer()

    # pylint: disable=arguments-differ
    def do_get_size(self, widget, cell_area):
        """Get the size of the CellRendererML.

        :param widget:
        :param cell_area:
        """
        return Gtk.CellRendererText.do_get_size(self, widget, cell_area)

    # pylint: disable=arguments-differ,too-many-locals
    def do_start_editing(
        self, __event, treeview, path, __background_area, cell_area, __flags
    ):
        """Handle edits of the CellRendererML.

        :param __event:
        :param treeview:
        :param path:
        :param __background_area:
        :param cell_area:
        :param __flags:
        """
        if not self.get_property("editable"):
            return

        self.selection = treeview.get_selection()
        self.treestore, self.treeiter = self.selection.get_selected()

        self.textedit_window = Gtk.Dialog(parent=treeview.get_toplevel())
        self.textedit_window.action_area.hide()
        self.textedit_window.set_decorated(False)
        self.textedit_window.set_property("skip-taskbar-hint", True)
        self.textedit_window.set_transient_for(None)

        self.textedit.set_editable(True)
        self.textedit.set_property("visible", True)
        self.textbuffer.set_property("text", self.get_property("text"))

        self.textedit_window.connect("key-press-event", self._keyhandler)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC,
        )
        scrolled_window.set_property("visible", True)
        # self.textedit_window.vbox.pack_start(scrolled_window, True, True, 0)

        scrolled_window.add(self.textedit)
        self.textedit_window.vbox.add(scrolled_window)
        self.textedit_window.realize()

        # Position the popup below the edited cell (and try hard to keep the
        # popup within the toplevel window)
        (tree_x, tree_y) = treeview.get_bin_window().get_origin()
        (tree_w, tree_h) = treeview.window.get_geometry()[2:4]
        (t_w, t_h) = self.textedit_window.window.get_geometry()[2:4]
        x_pos = tree_x + min(
            cell_area.x,
            tree_w - t_w + treeview.get_visible_rect().x,
        )
        y_pos = tree_y + min(
            cell_area.y,
            tree_h - t_h + treeview.get_visible_rect().y,
        )
        self.textedit_window.move(x_pos, y_pos)
        self.textedit_window.resize(cell_area.width, cell_area.height)

        # Run the dialog, get response by tracking keypresses
        response = self.textedit_window.run()

        if response == Gtk.ResponseType.OK:
            self.textedit_window.destroy()

            (iter_first, iter_last) = self.textbuffer.get_bounds()
            text = self.textbuffer.get_text(iter_first, iter_last)

            treeview.set_cursor(path, None, False)

            self.emit("edited", path, text)

        elif response == Gtk.ResponseType.CANCEL:
            self.textedit_window.destroy()
        else:
            print(f"response {response} received")
            self.textedit_window.destroy()

    def _keyhandler(self, __widget, event):
        """Handle key-press-events on the Gtk.TextView().

        :param __widget: the Gtk.TextView() that called this method.
        :param event: the Gdk.Event() that called this method.
        """
        _keyname = Gdk.keyval_name(event.keyval)

        if (
            event.get_state()
            & (Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK)
            and _keyname == "Return"
        ):
            self.textedit_window.response(Gtk.ResponseType.OK)


# Register the new widget types.
GObject.type_register(RAMSTKTreeView)
GObject.type_register(CellRendererML)
