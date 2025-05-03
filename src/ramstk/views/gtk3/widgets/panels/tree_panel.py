# pylint: disable=non-parent-init-called, too-many-public-methods, cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.panels.tree_panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Tree Panel Class."""


# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
import toml

# pylint: disable=ungrouped-imports
# noinspection PyPackageValidations
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages, string_to_boolean
from ramstk.views.gtk3 import GdkPixbuf, GObject, Gtk, _

# RAMSTK Local Imports
from ..label import RAMSTKLabel
from ..treeviews import RAMSTKTreeView
from . import RAMSTKBasePanel, do_log_message


def do_get_selected_row_attributes(
    selection: Gtk.TreeSelection, dic_attribute_widget_map: dict, position: dict
) -> dict:
    """Get the attributes of the selected RAMSTKTreeView row."""
    # FIXME: This function needs to use the _lst_widget_configuration instead of the
    #  dic_attribute_widget_map.
    _attributes: dict = {}
    _model, _row = selection.get_selected()

    if _row is None:
        return _attributes

    for _key in dic_attribute_widget_map:
        _attributes[_key] = _model.get_value(_row, position[_key])

    return _attributes


class RAMSTKTreePanel(RAMSTKBasePanel):
    """The RAMSTKTreePanel class.

    The attributes of a RAMSTKTreePanel are:

    :ivar tvwTreeView: a RAMSTKTreeView() for the panels that embed a treeview.
    :ivar _filtered_tree: boolean indicating whether to display the filtered
        RAMSTKTreeView() or the full RAMSTKTreeView().
    """

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKTreePanel."""
        super().__init__()

        # Initialize widgets.
        self.tvwTreeView: RAMSTKTreeView = RAMSTKTreeView()

        # Initialize private instance attributes.
        self._filtered_tree: bool = False

        # Initialize public instance attributes.
        self.level: str = ""

        self.tvwTreeView.dic_row_loader = {
            self._tag: self.tvwTreeView.do_load_tree,
        }

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "request_clear_views": self.do_clear_tree_panel,
                f"succeed_insert_{self._tag}": self.do_load_tree_panel,
                f"succeed_delete_{self._tag}": self.on_delete_row,
            }
        )
        if self._select_msg is not None:
            do_subscribe_to_messages(
                {
                    self._select_msg: self.do_load_tree_panel,
                }
            )

        if hasattr(self, "_on_module_switch"):
            do_subscribe_to_messages(
                {
                    "mvwSwitchedPage": self._on_module_switch,
                }
            )

        if hasattr(self, "_on_workview_edit"):
            do_subscribe_to_messages(
                {
                    f"wvw_editing_{self._tag}": self._on_workview_edit,
                }
            )

    # ----- ----- Standard panel methods. ----- ----- #
    def do_set_widget_properties(self) -> None:
        """Set properties of the RAMSTKTreePanel widgets."""
        super().do_set_widget_properties()

        self.tvwTreeView.do_set_properties(
            {
                "enable_grid_lines": True,
                "enable_tree_lines": True,
                "level_indentation": 2,
                "rubber_banding": True,
            }
        )

    # ----- ----- RAMSTKTreePanel specific methods. ----- ----- #
    def do_clear_tree_panel(self) -> None:
        """Clear the contents of the RAMSTKTreePanel."""
        try:
            self.tvwTreeView.get_model().clear()
        except AttributeError:
            self.tvwTreeView.get_model().get_model().clear()

    def do_load_tree_panel(self, tree: treelib.Tree) -> None:
        """Load data into the RAMSTKTreePanel.

        :param tree: the treelib Tree containing the module to load.
        """
        try:
            self.tvwTreeView.unfiltered_model.clear()
        except AttributeError:
            pass

        try:
            self.tvwTreeView.do_load_tree(tree, row=None)
            self.tvwTreeView.expand_all()

            if (_row := self.tvwTreeView.unfiltered_model.get_iter_first()) is not None:
                self.tvwTreeView.selection.select_iter(_row)
                self.show_all()
        except (AttributeError, TypeError, ValueError) as error:
            _frame = inspect.currentframe()
            _method_name = _frame.f_code.co_name if _frame else "unknown_method"
            do_log_message(
                _method_name,
                "do_log_warning_msg",
                "WARNING",
                _(
                    f"An error occurred when loading {self._tag} tree.  This might "
                    f"indicate one of it's nodes was missing it's data package, some "
                    f"of the data in the package was missing, or some of the data was "
                    f"the wrong type.  Error was: {error}."
                ),
            )

        pub.sendMessage("request_set_cursor_active")

    def do_make_tree_panel(self) -> None:
        """Create a panel with a RAMSTKTreeView."""
        for _widget in self._lst_widget_configuration:
            self.tvwTreeView.do_make_column(
                _widget,
                len(self._lst_widget_configuration),
            )

        # Create a scrollable window and add the tree view
        _scrollwindow: Gtk.ScrolledWindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.tvwTreeView)

        self.add(_scrollwindow)
        self.show_all()

    def do_make_treeview(self, format_file: str) -> None:
        """Make the RAMSTKTreeView instance for this panel.

        :param format_file: the absolute path to the format file containing the
            attribute information to update.
        """
        _format = toml.load(format_file)

        # Update RAMSTKCellRenderer widget attributes and properties with
        # user-defined values from the format file.
        _fields = sorted(_format["position"], key=_format["position"].get)
        for _field in _fields:
            for _widget in self._lst_widget_configuration:
                if _widget["attributes"]["field"] == _field:
                    _widget["attributes"]["label_text"] = _format["usertitle"][_field]
                    _widget["attributes"]["index"] = _format["position"][_field]
                    _widget["widget"].set_property(
                        "visible", string_to_boolean(_format["visible"][_field])
                    )
                    try:
                        _widget["widget"].set_property(
                            "editable", string_to_boolean(_format["editable"][_field])
                        )
                    except TypeError:
                        pass

        _column_types = [
            GObject.type_from_name(_widget["attributes"]["datatype"])
            for _widget in self._lst_widget_configuration
        ]
        _column_types.append(GdkPixbuf.Pixbuf)

        self.tvwTreeView.do_make_model(_column_types)

        if self._filtered_tree:
            self.tvwTreeView.filtered_model = (
                self.tvwTreeView.unfiltered_model.filter_new()
            )
            self.tvwTreeView.filtered_model.set_visible_func(self.do_filter_tree)
            self.tvwTreeView.set_model(self.tvwTreeView.filtered_model)

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def on_delete_row(self, tree: treelib.Tree) -> None:
        """Update the RAMSTKTreeView after deleting a line item.

        :param tree: the treelib Tree() containing the workflow module data.
        """
        self.tvwTreeView.do_delete_row(self._filtered_tree)

        pub.sendMessage("request_set_cursor_active")

    def on_row_change(self, selection: Gtk.TreeSelection) -> Dict[str, Any]:
        """Get the attributes for the newly selected row.

        :param selection: the Gtk.TreeSelection for the new row.
        :return: the dict of attributes and value for the item in the selected row. The
            key is the attribute name, the value is the attribute value. Pulling them
            from the RAMSTKTreeView ensures uncommitted changes are always selected.
        """
        _attributes: dict = {}
        _model, _row = selection.get_selected()

        if _row is None:
            return _attributes

        for _widget in self._lst_widget_configuration:
            _field = _widget["widget"].field
            _position = _widget["widget"].index
            _attributes[_field] = _model.get_value(_row, _position)

        _widget["widget"].record_id = _attributes[f"{self._tag}_id"]
        _widget["widget"].parent_id = _attributes.get("parent_id", -1)

        pub.sendMessage(
            f"selected_{self._tag}",
            attributes=_attributes,
        )

        return _attributes

    # ----- ----- Methods to be moved or deleted. ----- -----
    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_refresh_tree(self, node_id: int, package: Dict[str, Any]) -> None:
        """Update the module view RAMSTKTreeView() with attribute changes.

        This method is used to update a RAMSTKPanel() containing a
        RAMSTKTreeView() [generally the module view] whenever a work view
        widget is edited.  It is used to keep the data displayed in-sync.

        A dict 'package' is sent when a workview widget is edited/changed.

            `package` key: `package` value

        corresponds to:

            database field name: database field new value

        The key in the 'package' is used to find the value in
        _dic_attribute_updater corresponding to the data being changed.
        Position 2 of the _dic_attribute_updater value list is the nominal
        position in the RAMSTKTreeView containing the same attribute data
        as the one being changed.

        :param node_id: unused in this method.
        :param package: the key:value for the data being updated.
        """
        # FIXME: Is this method needed or can this refresh be pushed to the
        #  RAMSTKTreeView and/or the RAMSTKCellRenderer widgets?
        if not package:
            return

        _key, _value = next(iter(package.items()))
        try:
            _col_position = self.tvwTreeView.position
            _model, _row = self.tvwTreeView.get_selection().get_selected()

            if _row is not None:
                _model.set_value(_row, _col_position, _value)
        except (KeyError, StopIteration):
            _frame = inspect.currentframe()
            _method_name = _frame.f_code.co_name if _frame else "unknown_method"
            do_log_message(
                _method_name,
                "do_log_debug_msg",
                "DEBUG",
                _(
                    f"Failed to refresh {self._tag} data for record ID "
                    f"{self._record_id}. Key "
                    f"'{_key if ' _key' in locals() else 'UNKNOWN'}' not found in "
                    f"attribute dictionary."
                ),
            )
        except TypeError:
            _frame = inspect.currentframe()
            _method_name = _frame.f_code.co_name if _frame else "unknown_method"
            do_log_message(
                _method_name,
                "do_log_debug_msg",
                "DEBUG",
                _(
                    f"Failed to refresh {self._tag} data for record ID "
                    f"{self._record_id}. Data "
                    f"'{_value if '_value' in locals() else 'UNKNOWN'}' for key "
                    f"'{_key if '_key' in locals() else 'UNKNOWN'}' is of the wrong "
                    f"type."
                ),
            )

    def do_set_headings(self) -> None:
        """Set the treeview headings depending on the selected row.

        It's used when the tree displays an aggregation of models such as the FMEA or
        PoF.  This method applies the appropriate headings when a row is selected.
        """
        # FIXME: Need to use the self._lst_widget_configuration to get the heading
        #  text and visibility status.  This method is not called by anything and may
        #  be unneeded.
        _columns = self.tvwTreeView.get_columns()
        _headings = self.tvwTreeView.headings
        _visible = self.tvwTreeView.visible

        for _idx, _key in enumerate(_headings):
            _label = RAMSTKLabel(f"<span weight='bold'>{_headings[_key]}</span>")
            _label.do_set_properties(
                {
                    "height_request": -1,
                    "justify": Gtk.Justification.CENTER,
                    "wrap": True,
                }
            )
            _label.show_all()

            _column = _columns[_idx]
            _column.set_widget(_label)
            _column.set_visible(_visible.get(_key, True))

    # noinspection PyUnusedLocal
    def do_set_visible_columns(self) -> None:
        """Set visible columns in the RAMSTKTreeView depending on the selected level."""
        # FIXME: this method is intended to dynamically change the columns that are
        #  visible for certain analyses depending on the methodology selected.
        #  Currently the _dic_visible_mask is used to determine which columns are
        #  visible for each method.  This may continue to be the best way to do this,
        #  but there may be a more elegant way that sets that value in the attributes
        #  dict of the RAMSTKCellRenderer.
        for _widget in self._lst_widget_configuration:
            _column = self.tvwTreeView.get_column(_widget["attributes"]["index"])
            _column.set_visible(_widget["properties"]["visible"])
