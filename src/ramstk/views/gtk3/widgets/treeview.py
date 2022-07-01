# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.treeview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKTreeView Module."""


# Standard Library Imports
import contextlib
from typing import Any, Callable, Dict, List, Tuple, Union

# Third Party Imports
# noinspection PyPackageRequirements
import toml
import treelib

# RAMSTK Package Imports
from ramstk.utilities import string_to_boolean
from ramstk.views.gtk3 import Gdk, GdkPixbuf, GObject, Gtk, Pango, _

# RAMSTK Local Imports
from .label import RAMSTKLabel
from .widget import RAMSTKWidget


def do_make_column(
    cells_lst: List[Gtk.CellRenderer],
    **kwargs,
) -> Gtk.TreeViewColumn:
    """Make a Gtk.TreeViewColumn().

    :param list cells_lst: list of Gtk.CellRenderer()s that are to be packed in the
        column.
    :return: _column_obj
    :rtype: :class:`Gtk.TreeViewColumn`
    """
    _header_str = kwargs.get("heading", "")
    _tooltip_str = kwargs.get(
        "tooltip",
        _("Missing tooltip, please file a type:style issue to have one added."),
    )
    _visible_flag = kwargs.get("visible", True)

    _column_obj: Gtk.TreeViewColumn = Gtk.TreeViewColumn("")

    for _cell_obj in cells_lst:
        if isinstance(_cell_obj, Gtk.CellRendererPixbuf):
            _column_obj.pack_start(_cell_obj, False)
        else:
            _column_obj.pack_start(_cell_obj, True)

    _label_obj = RAMSTKLabel(_header_str)
    _label_obj.do_set_properties(
        height=-1,
        justify=Gtk.Justification.CENTER,
        tooltip=_tooltip_str,
        width=-1,
    )
    _column_obj.set_widget(_label_obj)
    _column_obj.set_resizable(True)
    _column_obj.set_alignment(0.5)
    _column_obj.set_visible(_visible_flag)

    return _column_obj


def do_set_cell_properties(
    cell_obj: Union[
        Gtk.CellRendererCombo,
        Gtk.CellRendererSpin,
        Gtk.CellRendererText,
        Gtk.CellRendererToggle,
    ],
    property_dic: Dict[str, Union[bool, float, int, str]],
) -> None:
    """Set common properties of Gtk.CellRenderers().

    :param cell_obj: the Gtk.CellRenderer() object whose properties are to be set.
    :param property_dic: the dictionary of properties for the cell.
    :return: None
    :rtype: None
    """
    _bg_color_str = property_dic.get("bg_color", "#FFFFFF")
    _visible_digits_int = property_dic.get("digits", 2)
    _editable_flag = property_dic.get("editable", False)
    _fg_color_str = property_dic.get("fg_color", "#000000")
    _lower_limit_int = property_dic.get("lower", 1)
    _step_int = property_dic.get("step", 1)
    _upper_limit_int = property_dic.get("upper", 10)
    _visible_flag = property_dic.get("visible", True)
    _font_weight_int = property_dic.get("weight", 400)
    _weight_set_flag = property_dic.get("weight_set", False)

    if not _editable_flag:
        _color_obj = Gdk.RGBA(255.0, 255.0, 255.0, 1.0)
        _fg_color_str = "#000000"
        cell_obj.set_property("cell-background-rgba", _color_obj)  # type: ignore

    cell_obj.set_property("visible", _visible_flag)  # type: ignore
    cell_obj.set_property("yalign", 0.1)  # type: ignore

    if isinstance(cell_obj, Gtk.CellRendererCombo):
        _cellmodel_obj = Gtk.ListStore(GObject.TYPE_STRING)
        _cellmodel_obj.append([""])
        cell_obj.set_property("editable", _editable_flag)
        cell_obj.set_property("has-entry", False)
        cell_obj.set_property("model", _cellmodel_obj)
        cell_obj.set_property("text-column", 0)
    elif isinstance(cell_obj, Gtk.CellRendererSpin):
        _adjustment_obj = Gtk.Adjustment(
            lower=_lower_limit_int,
            upper=_upper_limit_int,
            step_incr=_step_int,
        )
        cell_obj.set_property("adjustment", _adjustment_obj)
        cell_obj.set_property("digits", _visible_digits_int)
        cell_obj.set_property("editable", _editable_flag)
    elif isinstance(cell_obj, Gtk.CellRendererText):
        cell_obj.set_property("background", _bg_color_str)
        cell_obj.set_property("editable", _editable_flag)
        cell_obj.set_property("foreground", _fg_color_str)
        cell_obj.set_property("weight", _font_weight_int)
        cell_obj.set_property("weight-set", _weight_set_flag)
        cell_obj.set_property("wrap-width", 250)
        cell_obj.set_property("wrap-mode", Pango.WrapMode.WORD)
    elif isinstance(cell_obj, Gtk.CellRendererToggle):
        cell_obj.set_property("activatable", _editable_flag)
        cell_obj.set_property("cell-background", _bg_color_str)


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
        cell_obj: Gtk.CellRendererCombo,
        path_str: str,
        new_row_obj: Gtk.TreeIter,
        position_int: int,
    ) -> int:
        """Handle Gtk.CellRendererCombo() edits.

        :param cell_obj: the Gtk.CellRendererCombo() that was edited.
        :param path_str: the Gtk.TreeView() path of the Gtk.CellRendererCombo() that
            was edited.
        :param new_row_obj: the new Gtk.TreeIter() selected in the
            Gtk.CellRendererCombo().  This is relative to the cell renderer's model,
            not the RAMSTKTreeView() model.
        :param position_int: the column position of the edited Gtk.CellRendererCombo().
        :return: _position_idx; the position in the Gtk.CellRenderCombo() list that
            was selected.
        """
        _model_obj: Gtk.TreeModel = self.get_model()
        _cell_model_obj: Gtk.TreeModel = cell_obj.get_property("model")

        _new_text_obj: GObject.Value = _cell_model_obj.get_value(new_row_obj, 0)
        _iter_obj: Gtk.TreeIter = _cell_model_obj.get_iter_first()

        _selected_pos_idx: int = 0
        while _iter_obj is not None:
            if _cell_model_obj.get_value(_iter_obj, 0) == _new_text_obj:
                _model_obj[path_str][position_int] = _new_text_obj
                break
            _iter_obj = _cell_model_obj.iter_next(_iter_obj)
            _selected_pos_idx += 1

        return _selected_pos_idx

    def do_edit_cell(
        self,
        cell_obj: Gtk.CellRenderer,
        path_str: str,
        new_text_obj: Union[bool, float, int, str],
        position_int: int,
    ) -> Union[bool, float, int, str]:
        """Handle Gtk.CellRenderer() edits.

        :param cell_obj: the Gtk.CellRenderer() that was edited.
        :param path_str: the Gtk.TreeView() path of the Gtk.CellRenderer() that was
            edited.
        :param new_text_obj: the new text in the edited Gtk.CellRenderer().
        :param position_int: the column position of the edited Gtk.CellRenderer().
        :return: new_text_obj; the value of the new text converted to the correct data
            type for the attribute being edited.
        :rtype: Any
        """
        _model_obj: Gtk.TreeModel = self.get_model()
        _col_data_type_str: str = GObject.type_name(
            _model_obj.get_column_type(position_int)
        )

        if isinstance(cell_obj, Gtk.CellRendererToggle):
            new_text_obj = not cell_obj.get_active()
        elif _col_data_type_str == "gchararray":
            new_text_obj = str(new_text_obj)
        elif _col_data_type_str == "gint":
            try:
                new_text_obj = int(new_text_obj)
            except ValueError:
                new_text_obj = int(float(new_text_obj))
        elif _col_data_type_str == "gfloat":
            new_text_obj = float(new_text_obj)

        _model_obj[path_str][position_int] = new_text_obj

        return new_text_obj

    def do_get_row_by_value(self, search_col_int: int, value_obj: Any) -> Gtk.TreeIter:
        """Find the row in the RAMSTKTreeView() containing the passed value.

        :param search_col_int: the column number to search for the desired value.
        :param value_obj: the value to match.
        :return: _row_obj; the Gtk.TreeIter() for the matching row.
        :rtype: :class:`Gtk.TreeIter`
        """
        _row_obj = self.unfilt_model.get_iter_first()

        while (
            _row_obj is not None
            and self.unfilt_model.get_value(_row_obj, search_col_int) != value_obj
        ):
            _row_obj = self.unfilt_model.iter_next(_row_obj)

        return _row_obj

    def do_insert_row(
        self, data_dic: Dict[str, Any], prow_obj: Gtk.TreeIter = None
    ) -> None:
        """Insert a new row in the treeview.

        :param data_dic: the data dictionary for the new row to insert.
        :param prow_obj: the parent row of the row to insert.
        :return: None
        :rtype: None
        """
        _model_obj, _row_obj = self.selection.get_selected()

        _data_obj = [data_dic[_position_idx] for _position_idx in self.position]

        _row_obj = _model_obj.append(prow_obj, _data_obj)

        _path_str = _model_obj.get_path(_row_obj)
        _column_obj = self.get_column(0)
        self.set_cursor(_path_str, None, False)
        self.row_activated(_path_str, _column_obj)

    def do_load_combo_cell(self, column_idx: int, item_lst: List[str]) -> None:
        """Load items into cell with combobox.

        :param column_idx: the index in the RAMSTKTreeView() model of the
            Gtk.CellRendererCombo() to load.
        :param item_lst: the list of entries to load into the Gtk.CellRendererCombo().
        :return: None
        :rtype: None
        """
        _model_obj = self.get_cell_model(column_idx)
        for _item_str in item_lst:
            _model_obj.append([_item_str])

    def do_load_tree(
        self, tree_obj: treelib.Tree, row_obj: Gtk.TreeIter = None
    ) -> None:
        """Load the RAMSTKTreeView() with the contents of the treelib Tree().

        :param tree_obj: the treelib.Tree() to load into the RAMSTKTreeView.
        :param row_obj: the current row to load.
        :return: None
        :rtype: None
        """
        _row_obj = None
        _node_obj = tree_obj.get_node(tree_obj.root)

        if _node_obj.data is not None:
            _row_obj = self.dic_row_loader[_node_obj.tag](_node_obj, row_obj)

        for _child_node_obj in tree_obj.children(_node_obj.identifier):
            self.do_load_tree(tree_obj.subtree(_child_node_obj.identifier), _row_obj)

    def do_make_columns(self) -> None:
        """Make the columns for the RAMSTKTreeView().

        :return: None
        :rtype: None
        """
        for _column_name_str, _position_int in self.position.items():
            _cell_obj = self.widgets[_column_name_str]
            _property_dic: Dict[str, Union[bool, float, int, str]] = {
                "editable": self.editable[_column_name_str],
                **self.cellprops[_column_name_str],
            }

            do_set_cell_properties(
                _cell_obj,
                property_dic=_property_dic,
            )

            # If creating a RAMSTKTreeView() that displays icons and this is
            # the first column we're creating, add a Gtk.CellRendererPixbuf()
            # to go along with the data in the first column.
            if self._has_pixbuf and _position_int == 0:
                _pbcell_obj = Gtk.CellRendererPixbuf()
                _pbcell_obj.set_property("xalign", 0.5)
                _pbcell_obj.set_property("cell-background", _property_dic["bg_color"])
                _column_obj: Gtk.TreeViewColumn = do_make_column(
                    [_pbcell_obj, _cell_obj],
                    heading="",  # type: ignore
                    visible=True,  # type: ignore
                )
                _column_obj.set_attributes(
                    _pbcell_obj, pixbuf=len(self.position.values())
                )
            else:
                # noinspection PyTypeChecker
                _column_obj = do_make_column(
                    [_cell_obj],
                    heading=self.headings[_column_name_str],  # type: ignore
                    visible=string_to_boolean(  # type: ignore
                        self.visible[_column_name_str],
                    ),
                )

            _column_obj.set_cell_data_func(
                _cell_obj,
                self._do_format_cell,
                (_position_int, self.datatypes[_column_name_str]),
            )

            self._do_set_column_properties(_column_name_str, _column_obj)
            self.append_column(_column_obj)

    def do_make_model(self) -> None:
        """Make the RAMSTKTreeView() data model.

        :return: None
        :rtype: None
        """
        _data_type_lst = [
            GObject.type_from_name(_datatype_str)
            for __, _datatype_str in self.datatypes.items()
        ]

        if self._has_pixbuf:
            _data_type_lst.append(GdkPixbuf.Pixbuf)

        self.unfilt_model = Gtk.TreeStore(*_data_type_lst)
        self.set_model(self.unfilt_model)

    # noinspection PyTypeChecker
    def do_parse_format(self, fmt_file_path_str: str) -> None:
        """Parse the format file for the RAMSTKTreeView().

        :param fmt_file_path_str: the absolute path to the format file to read.
        :return: None
        :rtype: None
        """
        _format_dic = toml.load(fmt_file_path_str)

        self._has_pixbuf = string_to_boolean(_format_dic["pixbuf"])

        self.position = {}
        _column_name_lst = sorted(
            _format_dic["position"], key=_format_dic["position"].get
        )
        for _column_name_str in _column_name_lst:
            self.position[_column_name_str] = _format_dic["position"][_column_name_str]
            self.editable[_column_name_str] = string_to_boolean(
                _format_dic["editable"][_column_name_str]
            )
            self.visible[_column_name_str] = string_to_boolean(
                _format_dic["visible"][_column_name_str]
            )

        self.headings = _format_dic["usertitle"]

    def do_set_editable_columns(self, edit_method_obj: object) -> None:
        """Set the treeview columns editable or read-only.

        :param edit_method_obj: the callback method for the cell.
        :return: None
        """
        for _column_name_str in self.editable:
            _column_obj = self.get_column(self.position[_column_name_str])

            # Get the last cell so those columns containing a
            # Gtk.CellRendererPixBuf() will return the Gtk.CellRendererText()
            # that is packed with it.  If there is only one cell renderer,
            # that is the one that will be returned.
            _cell_obj = _column_obj.get_cells()[-1]

            if isinstance(self.widgets[_column_name_str], Gtk.CellRendererToggle):
                _cell_obj.connect(
                    "toggled",
                    edit_method_obj,
                    None,
                    self.position[_column_name_str],
                )
            elif isinstance(
                self.widgets[_column_name_str],
                (Gtk.CellRendererSpin, Gtk.CellRendererText),
            ):
                _cell_obj.connect(
                    "edited",
                    edit_method_obj,
                    self.position[_column_name_str],
                )

    def do_set_visible_columns(self) -> None:
        """Set the treeview columns visible or hidden.

        :return: None
        :rtype: None
        """
        for _column_name_str, _visible_flag in self.visible.items():
            _column_obj = self.get_column(self.position[_column_name_str])
            _column_obj.set_visible(_visible_flag)

    def get_cell_model(self, column_obj: int, clear_flag: bool = True) -> Gtk.TreeModel:
        """Retrieve the Gtk.TreeModel() from a Gtk.CellRendererCombo().

        :param column_obj: the column number to retrieve the cell's model.
        :param clear_flag: whether to clear the Gtk.TreeModel().  Default is True.
        :return: _model_obj
        :rtype: :class:`Gtk.TreeModel`
        """
        _column_obj = self.get_column(column_obj)
        _cell_obj = _column_obj.get_cells()[0]
        _model_obj = _cell_obj.get_property("model")

        if clear_flag:
            _model_obj.clear()

        return _model_obj

    @staticmethod
    def _do_format_cell(
        __column_obj: Gtk.TreeViewColumn,
        cell_obj: Gtk.CellRenderer,
        model_obj: Gtk.TreeModel,
        row_obj: Gtk.TreeIter,
        data_tpl: Tuple[Any],
    ) -> None:
        """Set the formatting of the Gtk.Treeview() Gtk.CellRenderers().

        :param __column_obj: the Gtk.TreeViewColumn() containing the
            Gtk.CellRenderer() to format.  Unused in this method.
        :type __column_obj: :class:`Gtk.TreeViewColumn`
        :param cell_obj: the Gtk.CellRenderer() to format.
        :type cell_obj: :class:`Gtk.CellRenderer`
        :param model_obj: the Gtk.TreeModel() containing the Gtk.TreeViewColumn().
        :type model_obj: :class:`Gtk.TreeModel`
        :param row_obj: the Gtk.TreeIter() pointing to the row containing the
            Gtk.CellRenderer() to format.
        :type row_obj: :class:`Gtk.TreeIter`
        :param data_tpl: a tuple containing the position and the data type.
        :return: None
        :rtype: None
        """
        if data_tpl[1] == "gfloat":  # type: ignore
            fmt_str = "{0:0.6g}"
        elif data_tpl[1] == "gint":  # type: ignore
            fmt_str = "{0:0d}"
        else:
            return

        _value_flt = model_obj.get_value(row_obj, data_tpl[0])
        with contextlib.suppress(TypeError, ValueError):
            cell_obj.set_property("text", fmt_str.format(_value_flt))

    def _do_set_column_properties(
        self,
        column_name_str: str,
        column_obj: Gtk.TreeViewColumn,
    ) -> None:
        """Set the properties of the RAMSTKTreeView() column.

        :param column_name_str: the value of the key in the widgets and position dicts.
        :param column_obj: the Gtk.TreeViewColumn() to set properties.
        :return: None
        :rtype: None
        """
        _cell_obj = column_obj.get_cells()[-1]

        if isinstance(self.widgets[column_name_str], Gtk.CellRendererToggle):
            column_obj.set_attributes(_cell_obj, active=self.position[column_name_str])
        elif isinstance(
            self.widgets[column_name_str],
            (
                Gtk.CellRendererCombo,
                Gtk.CellRendererSpin,
                Gtk.CellRendererText,
            ),
        ):
            column_obj.set_attributes(_cell_obj, text=self.position[column_name_str])

        if self.position[column_name_str] > 0:
            column_obj.set_reorderable(True)

    @staticmethod
    def _resize_wrap(
        column_obj: Gtk.TreeViewColumn,
        __param_obj,
        cell_obj: Gtk.CellRenderer,
    ) -> None:
        """Dynamically set wrap-width property for a Gtk.CellRenderer().

        This is called whenever the column width in the Gtk.TreeView() is
        resized.

        :param column_obj: the Gtk.TreeViewColumn() being resized.
        :param GParamInt __param_obj: the triggering parameter.  Unused in this method.
        :param cell_obj: the Gtk.CellRenderer() that needs to be resized.
        :return: None
        :rtype: None
        """
        _width_int = column_obj.get_width()

        if _width_int <= 0:
            _width_int = 25
        else:
            _width_int += 10

        if isinstance(cell_obj, Gtk.CellRendererToggle):
            cell_obj.set_property("width", _width_int)
        else:
            cell_obj.set_property("wrap-width", _width_int)


# Register the new widget types.
GObject.type_register(RAMSTKTreeView)
