# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.pof.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Physics of Failure tree panel module."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple, Union

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import GdkPixbuf, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCellRendererCombo,
    RAMSTKCellRendererSpin,
    RAMSTKCellRendererText,
    RAMSTKTreePanel,
    WidgetConfig,
)


class PoFTreePanel(RAMSTKTreePanel):
    """Panel to display Physics if Failure analysis worksheet."""

    # Define private class attributes.
    _dic_visible_mask: Dict[str, List[bool]] = {
        "mode": [
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            True,
        ],
        "mechanism": [
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ],
        "opload": [
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
        ],
        "opstress": [
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            True,
            True,
            False,
            False,
            True,
        ],
        "test_method": [
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            True,
        ],
    }
    _select_msg = "succeed_retrieve_pof"
    _tag = "pof"
    _title = _("Physics of Failure (PoF) Analysis")

    def __init__(self) -> None:
        """Initialize an instance of the PoF analysis worksheet."""
        super().__init__()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "hardware_id",
                    "index": 0,
                    "label_text": _("Hardware ID"),
                    "listen_topic": "wvw_editing_allocation",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "mode_id",
                    "index": 1,
                    "label_text": _("Mode ID"),
                    "listen_topic": "wvw_editing_allocation",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "mechanism_id",
                    "index": 2,
                    "label_text": _("Mechanism ID"),
                    "listen_topic": "wvw_editing_allocation",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "opload_id",
                    "index": 3,
                    "label_text": _("Load ID"),
                    "listen_topic": "wvw_editing_allocation",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "opstress_id",
                    "index": 4,
                    "label_text": _("Stress ID"),
                    "listen_topic": "wvw_editing_allocation",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "test_method_id",
                    "index": 5,
                    "label_text": _("Test ID"),
                    "listen_topic": "wvw_editing_allocation",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "description",
                    "index": 6,
                    "label_text": _("Description"),
                    "listen_topic": "wvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "effect_end",
                    "index": 7,
                    "label_text": _("End Effect"),
                    "listen_topic": "wvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "severity_class",
                    "index": 8,
                    "label_text": _("Severity"),
                    "listen_topic": "wvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "mode_probability",
                    "index": 9,
                    "label_text": _("Mode Probability"),
                    "listen_topic": "wvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "damage_model",
                    "index": 10,
                    "label_text": _("Damage Model"),
                    "listen_topic": "wvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "measurable_parameter",
                    "index": 11,
                    "label_text": _("Measurable Parameter"),
                    "listen_topic": "wvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "load_history",
                    "index": 12,
                    "label_text": _("Load History Method"),
                    "listen_topic": "wvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "boundary_conditions",
                    "index": 13,
                    "label_text": _("Boundary Conditions"),
                    "listen_topic": "wvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererSpin(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "priority_id",
                    "index": 14,
                    "label_text": _("Priority"),
                    "listen_topic": "wvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "remarks",
                    "index": 15,
                    "label_text": _("Remarks"),
                    "listen_topic": "wvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
        ]
        self._filtered_tree = True
        self._on_edit_message: str = f"wvw_editing_{self._tag}"

        # Initialize public instance attributes.
        self.dic_icons: Dict[str, str] = {}
        self.lst_damage_models: List[str] = []
        self.lst_load_history: List[str] = []
        self.lst_measurable_parameters: List[str] = []

        super().do_set_widget_properties()
        super().do_make_panel()
        super().do_set_widget_callbacks()
        self._do_load_priorities()

        # FIXME: Do we need this line?
        self.tvwTreeView.dic_row_loader = {
            "mode": self.__do_load_mode,
            "mechanism": self.__do_load_mechanism,
            "opload": self.__do_load_opload,
            "opstress": self.__do_load_opstress,
            "test_method": self.__do_load_test_method,
        }
        self.tvwTreeView.set_tooltip_text(
            _(
                "Displays the Physics of Failure (PoF) Analysis for the currently "
                "selected hardware item."
            )
        )

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "succeed_retrieve_pof": super().do_load_panel,
                "selected_hardware": self._on_select_hardware,
            }
        )

    # ----- ----- RAMSTKTreePanel specific methods. ----- ----- #
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the PoF Work View RAMSTKTreeView().

        This method is called whenever a RAMSTKTreeView() row is activated.

        :param selection: the TreeSelection() of the currently selected row in the PoF
            RAMSTKTreeView().
        :return: None
        """
        _attributes = super().on_row_change(selection)
        _model, _row = selection.get_selected()

        if _row is not None:
            self.do_get_pof_level(_model, _row)
            super().do_set_visible_columns()
            self._record_id = _attributes[f"{self.level}_id"]

    # ----- ----- - PoFTreePanel specific methods. - ----- ----- #
    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_filter_tree(
        self, model: Gtk.TreeModel, row: Gtk.TreeIter, data: Any
    ) -> bool:
        """Filter PoF to show only those rows associated with the selected Hardware.

        :param model: the filtered model for the PoF RAMSTKTreeView.
        :param row: the iter to check against condition(s).
        :param data: unused in this method; required by Gtk.TreeModelFilter() widget.
        :return: True if row should be visible, False else.
        :rtype: bool
        """
        # FIXME: This method should be moved to the RAMSTKTreeView class.
        return model[row][0] == self._parent_id

    def do_get_pof_level(self, model: Gtk.TreeModel, row: Gtk.TreeIter) -> None:
        """Determine the PoF level of the selected PoF row.

        :param model: the PoF Gtk.TreeModel.
        :param row: the selected Gtk.TreeIter in the PoF.
        """
        _cid = ""

        for _col in [1, 2, 3, 4, 5]:
            _cid = f"{_cid}{int(bool(model.get_value(row, _col)))}"

        self.level = {
            "10000": "mode",
            "11000": "mechanism",
            "11100": "opload",
            "11110": "opstress",
            "11101": "test_method",
        }[_cid]

    def do_load_damage_models(self, models: Dict[int, Tuple[str]]) -> None:
        """Load the RAMSTKTreeView damage model CellRendererCombo.

        :param models: the dict with damage models to load.
        """
        for _model in models:
            self.lst_damage_models.append(models[_model][0])

        self.tvwTreeView.do_load_cellrenderercombo(
            "damage_model",
            self.lst_damage_models,
        )

    def do_load_load_history(self, histories: Dict[int, Tuple[str]]) -> None:
        """Load the RAMSTKTreeView operating load history CellRendererCombo.

        :param histories: the dict with load histories to load.
        """
        for _history in histories:
            self.lst_load_history.append(histories[_history][0])

        self.tvwTreeView.do_load_cellrenderercombo(
            "load_history",
            self.lst_load_history,
        )

    def do_load_measurable_parameters(
        self, parameters: Dict[int, Tuple[str, str]]
    ) -> None:
        """Load the RAMSTKTreeView measurable parameters CellRendererCombo.

        :param parameters: the dict with measurable parameters to load.
        """
        for _parameter in parameters:
            self.lst_measurable_parameters.append(parameters[_parameter][1])

        self.tvwTreeView.do_load_cellrenderercombo(
            "measurable_parameter",
            self.lst_measurable_parameters,
        )

    def _do_load_priorities(self) -> None:
        """Load the priority RAMSTKCellRendererSpin."""
        # Set the priority Gtk.CellRendererSpin()'s adjustment limits and
        # step increments.
        _cell = self.tvwTreeView.get_column(
            self.tvwTreeView.position["priority_id"]
        ).get_cells()[0]
        _adjustment = _cell.get_property("adjustment")
        _adjustment.configure(5, 1, 5, -1, 0, 0)

    def _on_cell_edit(
        self,
        cell: Gtk.CellRenderer,
        path: str,
        new_text: str,
        key: str,
        message: str,
    ) -> None:
        """Handle edits of description column to ensure proper level is updated.

        :param cell: the Gtk.CellRenderer() that was edited.
        :param path: the RAMSTKTreeView() path of the Gtk.CellRenderer() that was
            edited.
        :param new_text: the new text in the edited Gtk.CellRenderer().
        :param key: the column key of the edited Gtk.CellRenderer().
        :param message: the PyPubSub message to publish.
        """
        super().on_cell_edit(
            cell,
            path,
            new_text,
            key,
            f"wvw_editing_{self.level}",
        )

    def _on_select_hardware(
        self, attributes: Dict[str, Union[int, float, str]]
    ) -> None:
        """Filter FMEA when Hardware is selected.

        :param attributes: the dict of attributes for the selected Hardware.
        """
        self._parent_id = attributes["hardware_id"]
        self.tvwTreeView.filt_model.refilter()

    def __do_load_mechanism(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter:
        """Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :param row: the parent row of the mechanism to load into the FMEA form.
        :return: _new_row; the row that was just populated with mechanism data.
        """
        # TODO: Can we simplify these __do_load methods and remove the duplication?
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons["mechanism"], 22, 22
        )

        _attributes = [
            _entity.hardware_id,
            _entity.mode_id,
            _entity.mechanism_id,
            0,
            0,
            0,
            _entity.description,
            "",
            "",
            0.0,
            "",
            "",
            "",
            "",
            0,
            "",
            _icon,
        ]

        try:
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                f"An error occurred when loading failure mechanism {node.identifier} "
                f"in the physics of failure analysis.  This might indicate it was "
                f"missing it's data package, some of the data in the package was "
                f"missing, or some of the data was the wrong type.  Row data "
                f"was: {_attributes}"
            )
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row

    def __do_load_mode(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure mode record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the FMEA form.
        :return: _new_row; the row that was just populated with mode data.
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.dic_icons["mode"], 22, 22)

        _attributes = [
            _entity.hardware_id,
            _entity.mode_id,
            0,
            0,
            0,
            0,
            _entity.description,
            _entity.effect_end,
            _entity.severity_class,
            _entity.mode_ratio,
            "",
            "",
            "",
            "",
            0,
            "",
            _icon,
        ]

        try:
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                f"An error occurred when loading failure mode {node.identifier} in the "
                f"physics of failure analysis.  This might indicate it was missing "
                f"its data package, some of the data in the package was missing, or "
                f"some of the data was the wrong type.  Row data was: {_attributes}"
            )
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row

    def __do_load_opload(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :param row: the parent row of the mechanism to load into the FMEA form.
        :return: _new_row; the row that was just populated with mechanism data.
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.dic_icons["opload"], 22, 22)

        _attributes = [
            _entity.hardware_id,
            _entity.mode_id,
            _entity.mechanism_id,
            _entity.opload_id,
            0,
            0,
            _entity.description,
            "",
            "",
            0.0,
            _entity.damage_model,
            "",
            "",
            "",
            _entity.priority_id,
            "",
            _icon,
        ]

        try:
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                f"An error occurred when loading operating load {node.identifier} in "
                f"the physics of failure analysis.  This might indicate it was "
                f"missing its data package, some of the data in the package was "
                f"missing, or some of the data was the wrong type.  Row data "
                f"was: {_attributes}"
            )
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row

    def __do_load_opstress(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :param row: the parent row of the mechanism to load into the FMEA form.
        :return: _new_row; the row that was just populated with mechanism data.
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons["opstress"], 22, 22
        )

        _attributes = [
            _entity.hardware_id,
            _entity.mode_id,
            _entity.mechanism_id,
            _entity.opload_id,
            _entity.opstress_id,
            0,
            _entity.description,
            "",
            "",
            0.0,
            "",
            _entity.measurable_parameter,
            _entity.load_history,
            "",
            0,
            _entity.remarks,
            _icon,
        ]

        try:
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                f"An error occurred when loading operating stress {node.identifier} in "
                f"the physics of failure analysis.  This might indicate it was "
                f"missing its data package, some of the data in the package was "
                f"missing, or some of the data was the wrong type.  Row data "
                f"was: {_attributes}"
            )
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row

    def __do_load_test_method(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter:
        """Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :param row: the parent row of the mechanism to load into the FMEA form.
        :return: _new_row; the row that was just populated with mechanism data.
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons["test_method"], 22, 22
        )

        _attributes = [
            _entity.hardware_id,
            _entity.mode_id,
            _entity.mechanism_id,
            _entity.opload_id,
            0,
            _entity.test_method_id,
            _entity.description,
            "",
            "",
            0.0,
            "",
            "",
            "",
            _entity.boundary_conditions,
            0,
            _entity.remarks,
            _icon,
        ]

        try:
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                f"An error occurred when loading test method {node.identifier} in the "
                f"physics of failure analysis.  This might indicate it was missing its "
                f"data package, some of the data in the package was missing, or some "
                f"of the data was the wrong type.  Row data was: {_attributes}"
            )
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row
