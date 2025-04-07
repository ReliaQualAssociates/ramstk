# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.validation.tree_panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Validation tree panel module."""

# Standard Library Imports
from datetime import date
from typing import Dict, List, Tuple, Union

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCellRendererCombo,
    RAMSTKCellRendererText,
    RAMSTKTreePanel,
    WidgetConfig,
)


class ValidationTreePanel(RAMSTKTreePanel):
    """Panel to display flat list of validation tasks."""

    # Define private class attributes.
    _record_field = "validation_id"
    _select_msg = "succeed_retrieve_all_validation"
    _tag = "validation"
    _title = _("Verification Task List")

    def __init__(self) -> None:
        """Initialize an instance of the Validation panel."""
        super().__init__()

        # Initialize private attributes.
        self._lst_measurement_units: List[str] = []
        self._lst_verification_types: List[str] = []
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "revision_id",
                    "index": 0,
                    "label_text": _("Revision ID"),
                    "listen_topic": "wvw_editing_validation",
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
                    "field": "validation_id",
                    "index": 1,
                    "label_text": _("Validation ID"),
                    "listen_topic": "wvw_editing_validation",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "acceptable_maximum",
                    "format": "{0.0.2g}",
                    "index": 2,
                    "label_text": _("Acceptable Max."),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "acceptable_mean",
                    "format": "{0.0.2g}",
                    "index": 3,
                    "label_text": _("Acceptable Mean"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "acceptable_minimum",
                    "format": "{0.0.2g}",
                    "index": 4,
                    "label_text": _("Acceptable Min."),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "acceptable_variance",
                    "format": "{0.0.4g}",
                    "index": 5,
                    "label_text": _("Acceptable Variance"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 95.0,
                    "field": "confidence",
                    "format": "{0.0.3g}",
                    "index": 6,
                    "label_text": _("Confidence"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost_average",
                    "format": "{0.0.2g}",
                    "index": 7,
                    "label_text": _("Expected Cost"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost_ll",
                    "format": "{0.0.2g}",
                    "index": 8,
                    "label_text": _("Cost _LCL"),
                    "listen_topic": "wvw_editing_validation",
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost_maximum",
                    "format": "{0.0.2g}",
                    "index": 9,
                    "label_text": _("Maximum Cost"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost_mean",
                    "format": "{0.0.2g}",
                    "index": 10,
                    "label_text": _("Mean Cost"),
                    "listen_topic": "wvw_editing_validation",
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost_minimum",
                    "format": "{0.0.2g}",
                    "index": 11,
                    "label_text": _("Minimum Cost"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost_ul",
                    "format": "{0.0.2g}",
                    "index": 12,
                    "label_text": _("Cost UCL"),
                    "listen_topic": "wvw_editing_validation",
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost_variance",
                    "format": "{0.0.4g}",
                    "index": 13,
                    "label_text": _("Cost Variance"),
                    "listen_topic": "wvw_editing_validation",
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": date.today(),
                    "field": "date_end",
                    "index": 14,
                    "label_text": _("End Date"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": date.today(),
                    "field": "date_start",
                    "index": 15,
                    "label_text": _("Start Date"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "description",
                    "index": 16,
                    "label_text": _("Task Description"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "measurement_unit",
                    "index": 17,
                    "label_text": _("Unit of Measure"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "name",
                    "index": 18,
                    "label_text": _("Task Code"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "status",
                    "format": "{0.0.1f}",
                    "index": 19,
                    "label_text": _("% Complete"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "task_specification",
                    "index": 20,
                    "label_text": _("Task Specification"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "task_type",
                    "index": 21,
                    "label_text": _("Task Type"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "time_average",
                    "format": "{0.0.2g}",
                    "index": 22,
                    "label_text": _("Expected Task Time"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "time_ll",
                    "format": "{0.0.2g}",
                    "index": 23,
                    "label_text": _("Acceptable Max."),
                    "listen_topic": "wvw_editing_validation",
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "time_maximum",
                    "format": "{0.0.2g}",
                    "index": 24,
                    "label_text": _("Max. Task Time"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "time_mean",
                    "format": "{0.0.2g}",
                    "index": 25,
                    "label_text": _("Mean Task Time"),
                    "listen_topic": "wvw_editing_validation",
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "time_minimum",
                    "format": "{0.0.2g}",
                    "index": 26,
                    "label_text": _("Min. Task Time"),
                    "listen_topic": "wvw_editing_validation",
                    "send_topic": "mvw_editing_validation",
                },
                "properties": {
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "time_ul",
                    "format": "{0.0.2g}",
                    "index": 27,
                    "label_text": _("Task Time UCL"),
                    "listen_topic": "wvw_editing_validation",
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "time_variance",
                    "format": "{0.0.4g}",
                    "index": 28,
                    "label_text": _("Task Time Variance"),
                    "listen_topic": "wvw_editing_validation",
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
        ]

        # Set up the panel.
        super().do_set_widget_properties()
        super().do_make_panel()
        super().do_set_widget_callbacks()

        # FIXME: Is this line necessary?
        self.tvwTreeView.dic_row_loader = {
            "validation": self.__do_load_validation,
        }
        self.tvwTreeView.set_tooltip_text(
            _("Displays the hierarchical list of verification tasks.")
        )

        # Subscribe to PyPubSub messages.
        self._do_subscribe_to_messages()

    # ----- ----- RAMSTKTreePanel specific methods. ----- ----- #
    def _on_module_switch(self, module: str = "") -> None:
        """Respond to change in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == self._tag and _row is not None:
            _code = _model.get_value(_row, self.tvwTreeView.position["validation_id"])
            _name = _model.get_value(_row, self.tvwTreeView.position["name"])
            _title = _(f"Analyzing Validation Task {_code}: {_name}")

            pub.sendMessage("request_set_title", title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Validation Module View RAMSTKTreeView.

        This method is called whenever a Validation Module View RAMSTKTreeView row is
        activated/changed.

        :param selection: the Validation class Gtk.TreeSelection.
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes["validation_id"]

            _attributes["measurement_unit"] = self._lst_measurement_units.index(
                _attributes["measurement_unit"]
            )
            _attributes["task_type"] = self._lst_verification_types.index(
                _attributes["task_type"]
            )

            _title = _(f"Analyzing Verification Task {_attributes['name']}")

            pub.sendMessage(
                "selected_validation",
                attributes=_attributes,
            )
            pub.sendMessage(
                "request_set_title",
                title=_title,
            )

    # ----- --- ValidationTreePanel specific methods. --- ----- #
    def do_load_measurement_units(
        self, measurement_unit: Dict[int, Tuple[str, str]]
    ) -> None:
        """Load the verification task measurement unit list.

        :param measurement_unit: the dict containing the units of measure.
        """
        for _unit in measurement_unit:
            self._lst_measurement_units.append(measurement_unit[_unit][1])

        self.tvwTreeView.do_load_cellrenderercombo(
            "measurement_unit", self._lst_measurement_units
        )

    def do_load_verification_types(
        self, verification_type: Dict[int, Tuple[str, str]]
    ) -> None:
        """Load the verification task type list.

        :param verification_type: the dict containing the verification task types.
        """
        for _type in verification_type:
            self._lst_verification_types.append(verification_type[_type][1])

        self.tvwTreeView.do_load_cellrenderercombo(
            "task_type", self._lst_verification_types
        )

    def _do_subscribe_to_messages(self) -> None:
        """Subscribe to PyPubSub messages."""
        pub.subscribe(
            super().do_load_panel,
            "succeed_calculate_all_validation_tasks",
        )

    def _on_workview_edit(
        self, node_id: int, package: Dict[str, Union[bool, float, int, str]]
    ) -> None:
        """Update the module view RAMSTKTreeView with attribute changes.

        This is a wrapper for the metaclass method do_refresh_tree.  It is necessary to
        handle RAMSTKComboBox changes because the package value will be an integer and
        the Gtk.CellRendererCombo needs a string input to update.

        :param node_id: the ID of the validation task being edited.
        :param package: the key: value for the data being updated.
        """
        for _key, _value in package.items():
            # FIXME: We can't use the RAMSTKTreeView position attribute.  We need to use
            #  the RAMSTKTreeView's dic_field_position_map.  Fix this in every
            #  TreePanel.
            _column = self.tvwTreeView.get_column(self.tvwTreeView.position[_key])
            _cell = _column.get_cells()[-1]

            if isinstance(_cell, Gtk.CellRendererCombo) and isinstance(_value, int):
                if _key == "measurement_unit":
                    package[_key] = self._lst_measurement_units[_value]
                elif _key == "task_type":
                    package[_key] = self._lst_verification_types[_value]

            super().do_refresh_tree(node_id, package)

    def __do_load_validation(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter:
        """Load a verification task into the RAMSTKTreeView.

        :param node: the treelib.Node with the mode data to load.
        :param row: the parent row of the task to load into the validation tree.
        :return: _new_row; the row that was just populated with validation data.
        :rtype: :class:`Gtk.TreeIter`
        """
        # FIXME: This method needs to accept a treelib.Tree object with all the
        #  requirements and then pass that tree to the treeview method do_load_tree.
        #  This method should handle all exceptions and return None.
        _new_row = None
        _date_format = "%Y-%m-%d"

        # pylint: disable=unused-variable
        _entity = node.data["validation"]

        _attributes = [
            _entity.revision_id,
            _entity.validation_id,
            _entity.acceptable_maximum,
            _entity.acceptable_mean,
            _entity.acceptable_minimum,
            _entity.acceptable_variance,
            _entity.confidence,
            _entity.cost_average,
            _entity.cost_ll,
            _entity.cost_maximum,
            _entity.cost_mean,
            _entity.cost_minimum,
            _entity.cost_ul,
            _entity.cost_variance,
            _entity.date_end.strftime(_date_format),
            _entity.date_start.strftime(_date_format),
            _entity.description,
            self._lst_measurement_units[_entity.measurement_unit],
            _entity.name,
            _entity.status,
            _entity.task_specification,
            self._lst_verification_types[_entity.task_type],
            _entity.time_average,
            _entity.time_ll,
            _entity.time_maximum,
            _entity.time_mean,
            _entity.time_minimum,
            _entity.time_ul,
            _entity.time_variance,
        ]

        try:
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _message = _(
                f"An error occurred when loading verification task {node.identifier} "
                f"into the verification tree.  This might indicate it was missing it's "
                f"data package, some of the data in the package was missing, or "
                f"some of the data was the wrong type.  Row data was: "
                f"{_attributes}"
            )
            pub.sendMessage(
                "do_log_warning_msg",
                logger_name="WARNING",
                message=_message,
            )

        return _new_row
