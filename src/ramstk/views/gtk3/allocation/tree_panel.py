# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.allocation.tree_panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Allocation tree panel module."""

# Standard Library Imports
from typing import Any, Dict, List, Union

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCellRendererText,
    RAMSTKCellRendererToggle,
    RAMSTKTreePanel,
    WidgetConfig,
)


class AllocationTreePanel(RAMSTKTreePanel):
    """Panel to display reliability Allocation worksheet."""

    # Define private class attributes.
    _select_msg = "succeed_retrieve_all_allocation"
    _tag = "allocation"
    _title = _("Allocation Analysis")

    def __init__(self):
        """Initialize an instance of the Allocation worksheet panel."""
        super().__init__()

        # Initialize private instance attributes.
        self._dic_visible_mask: Dict[int, Dict[str, str]] = {
            0: {
                "revision_id": False,
                "hardware_id": False,
                "name": True,
                "included": False,
                "n_sub_systems": False,
                "n_sub_elements": False,
                "mission_time": False,
                "duty_cycle": False,
                "int_factor": False,
                "soa_factor": False,
                "op_time_factor": False,
                "env_factor": False,
                "weight_factor": False,
                "percent_weight_factor": False,
                "hazard_rate_logistics": True,
                "hazard_rate_alloc": False,
                "mtbf_logistics": True,
                "mtbf_alloc": False,
                "reliability_logistics": True,
                "reliability_alloc": False,
                "availability_logistics": True,
                "availability_alloc": False,
                "parent_id": False,
            },
            1: {
                "revision_id": False,
                "hardware_id": False,
                "name": True,
                "included": True,
                "n_sub_systems": True,
                "n_sub_elements": False,
                "mission_time": True,
                "duty_cycle": False,
                "int_factor": False,
                "soa_factor": False,
                "op_time_factor": False,
                "env_factor": False,
                "weight_factor": False,
                "percent_weight_factor": False,
                "hazard_rate_logistics": True,
                "hazard_rate_alloc": True,
                "mtbf_logistics": True,
                "mtbf_alloc": True,
                "reliability_logistics": True,
                "reliability_alloc": True,
                "availability_logistics": True,
                "availability_alloc": True,
                "parent_id": False,
            },
            2: {
                "revision_id": False,
                "hardware_id": False,
                "name": True,
                "included": True,
                "n_sub_systems": True,
                "n_sub_elements": True,
                "mission_time": True,
                "duty_cycle": True,
                "int_factor": False,
                "soa_factor": False,
                "op_time_factor": False,
                "env_factor": False,
                "weight_factor": True,
                "percent_weight_factor": True,
                "hazard_rate_logistics": True,
                "hazard_rate_alloc": True,
                "mtbf_logistics": True,
                "mtbf_alloc": True,
                "reliability_logistics": True,
                "reliability_alloc": True,
                "availability_logistics": True,
                "availability_alloc": True,
                "parent_id": False,
            },
            3: {
                "revision_id": False,
                "hardware_id": False,
                "name": True,
                "included": True,
                "n_sub_systems": False,
                "n_sub_elements": False,
                "mission_time": False,
                "duty_cycle": False,
                "int_factor": False,
                "soa_factor": False,
                "op_time_factor": False,
                "env_factor": False,
                "weight_factor": True,
                "percent_weight_factor": False,
                "hazard_rate_logistics": True,
                "hazard_rate_alloc": True,
                "mtbf_logistics": True,
                "mtbf_alloc": True,
                "reliability_logistics": True,
                "reliability_alloc": True,
                "availability_logistics": True,
                "availability_alloc": True,
                "parent_id": False,
            },
            4: {
                "revision_id": False,
                "hardware_id": False,
                "name": True,
                "included": True,
                "n_sub_systems": False,
                "n_sub_elements": False,
                "mission_time": False,
                "duty_cycle": False,
                "int_factor": True,
                "soa_factor": True,
                "op_time_factor": True,
                "env_factor": True,
                "weight_factor": True,
                "percent_weight_factor": False,
                "hazard_rate_logistics": True,
                "hazard_rate_alloc": True,
                "mtbf_logistics": True,
                "mtbf_alloc": True,
                "reliability_logistics": True,
                "reliability_alloc": True,
                "availability_logistics": True,
                "availability_alloc": True,
                "parent_id": False,
            },
        }
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "revision_id",
                    "index": 0,
                    "label_text": _("Revision ID"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
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
                    "field": "hardware_id",
                    "index": 1,
                    "label_text": _("Hardware ID"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
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
                    "field": "name",
                    "index": 2,
                    "label_text": _("Assembly"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererToggle(),
                "attributes": {
                    "datatype": "gint",
                    "default": 1,
                    "field": "included",
                    "index": 3,
                    "label_text": _("Included?"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 1,
                    "field": "n_sub_systems",
                    "index": 4,
                    "label_text": _("Number of Sub-Systems"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 1,
                    "field": "n_sub_elements",
                    "index": 5,
                    "label_text": _("Number of Sub-Elements"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
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
                    "default": 1,
                    "field": "mission_time",
                    "index": 6,
                    "label_text": _("Operating Time"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
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
                    "default": 1,
                    "field": "duty_cycle",
                    "index": 7,
                    "label_text": _("Duty Cycle"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 1,
                    "field": "int_factor",
                    "index": 8,
                    "label_text": _("Intricacy (1-10)"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 1,
                    "field": "soa_factor",
                    "index": 9,
                    "label_text": _("State of the Art (1-10)"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 1,
                    "field": "op_time_factor",
                    "index": 10,
                    "label_text": _("Operating Time (1-10)"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 1,
                    "field": "env_factor",
                    "index": 11,
                    "label_text": _("Environment (1-10)"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
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
                    "default": 1,
                    "field": "weight_factor",
                    "index": 12,
                    "label_text": _("Weighting Factor"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
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
                    "default": 1,
                    "field": "percent_weight_factor",
                    "index": 13,
                    "label_text": _("Percent Weighting Factor"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
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
                    "field": "hazard_rate_logistics",
                    "index": 14,
                    "label_text": _("Current Hazard Rate"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
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
                    "field": "hazard_rate_alloc",
                    "index": 15,
                    "label_text": _("Allocated Hazard Rate"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
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
                    "field": "mtbf_logistics",
                    "index": 16,
                    "label_text": _("Current MTBF"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
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
                    "field": "mtbf_alloc",
                    "index": 17,
                    "label_text": _("Allocated MTBF"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
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
                    "default": 1.0,
                    "field": "reliability_logistics",
                    "index": 18,
                    "label_text": _("Current Reliability"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
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
                    "default": 1.0,
                    "field": "reliability_alloc",
                    "index": 19,
                    "label_text": _("Allocated Reliability"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
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
                    "default": 1.0,
                    "field": "availability_logistics",
                    "index": 20,
                    "label_text": _("Current Availability"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
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
                    "default": 1.0,
                    "field": "availability_alloc",
                    "index": 21,
                    "label_text": _("Allocated Availability"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "parent_id",
                    "index": 22,
                    "label_text": _("Parent ID"),
                    "listen_topic": "wvw_editing_allocation",
                    "send_topic": "mvw_editing_allocation",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
        ]
        self._filtered_tree = True
        self._goal_id: int = 0
        self._method_id: int = 0
        self._on_edit_message: str = f"wvw_editing_{self._tag}"

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()
        super().do_set_widget_callbacks()

        # FIXME: Is this line needed?
        self.tvwTreeView.dic_row_loader = {
            "allocation": self.__do_load_allocation,
        }
        self.tvwTreeView.set_tooltip_text(
            _(
                "Displays the Allocation Analysis for the currently selected "
                "Hardware item."
            )
        )

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_panel, "succeed_calculate_allocation")
        pub.subscribe(self._do_set_hardware_attributes, "succeed_get_hardware_tree")
        pub.subscribe(
            self._do_set_reliability_attributes, "succeed_get_reliability_tree"
        )
        pub.subscribe(self._on_method_changed, "succeed_change_allocation_method")
        pub.subscribe(self._on_select_hardware, "selected_hardware")

    # ----- ----- RAMSTKTreePanel specific methods. ----- ----- #
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Allocation RAMSTKTreeView().

        This method is called whenever an Allocation RAMSTKTreeView() row is
        activated/changed.

        :param selection: the Allocation Gtk.TreeSelection().
        """
        _attributes = super().on_row_change(selection)

        # FIXME: Can we move setting the record ID to the super class?
        if _attributes:
            self._record_id = _attributes["hardware_id"]

            pub.sendMessage(
                "selected_allocation",
                attributes=_attributes,
            )

    # ----- -- AllocationTreePanel specific methods. --- ----- #
    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_filter_tree(
        self, model: Gtk.TreeModel, row: Gtk.TreeIter, data: Any
    ) -> bool:
        """Filter Allocations to show only those associated with the selected Hardware.

        :param model: the filtered model for the Allocation RAMSTKTreeView.
        :param row: the iter to check against condition(s).
        :param data: unused in this method; required by Gtk.TreeModelFilter widget.
        :return: True if row should be visible, False else.
        :rtype: bool
        """
        # FIXME: There are several places where this method is used.  We need to move
        #  this to the RAMSTKTreePanel class.
        return model[row][22] == self._parent_id

    def _do_set_columns_visible(self) -> None:
        """Set editable columns based on the Allocation method selected."""
        self.tvwTreeView.visible = self._dic_visible_mask[self._method_id]
        self.tvwTreeView.do_set_visible_columns()

    def _do_set_hardware_attributes(self, tree: treelib.Tree) -> None:
        """Set the attributes when the hardware tree is retrieved.

        :param tree: the hardware treelib.Tree.
        """
        for _node in tree.all_nodes()[1:]:
            _hardware = _node.data["hardware"]
            _row = self.tvwTreeView.do_get_row_by_value(1, _hardware.hardware_id)
            if _row is not None:
                self.tvwTreeView.unfilt_model.set_value(
                    _row,
                    2,
                    _hardware.name,
                )

    def _do_set_reliability_attributes(self, tree: treelib.Tree) -> None:
        """Set the attributes when the reliability tree is retrieved.

        :param tree: the reliability treelib.Tree.
        """
        for _node in tree.all_nodes()[1:]:
            _reliability = _node.data["reliability"]
            _row = self.tvwTreeView.do_get_row_by_value(1, _reliability.hardware_id)
            if _row is not None:
                self.tvwTreeView.unfilt_model.set_value(
                    _row,
                    14,
                    _reliability.hazard_rate_logistics,
                )
                self.tvwTreeView.unfilt_model.set_value(
                    _row,
                    16,
                    _reliability.mtbf_logistics,
                )
                self.tvwTreeView.unfilt_model.set_value(
                    _row,
                    18,
                    _reliability.reliability_logistics,
                )
                self.tvwTreeView.unfilt_model.set_value(
                    _row,
                    20,
                    _reliability.availability_logistics,
                )

    def _on_method_changed(self, method_id: int) -> None:
        """Set method ID attributes when user changes the selection.

        :param method_id: the newly selected allocation method.
        """
        self._method_id = method_id
        self._do_set_columns_visible()

    def _on_select_hardware(
        self, attributes: Dict[str, Union[int, float, str]]
    ) -> None:
        """Filter allocation list when Hardware is selected.

        :param attributes: the dict of attributes for the selected Hardware.
        """
        self._parent_id = attributes["hardware_id"]
        self.tvwTreeView.filt_model.refilter()
        pub.sendMessage("request_get_allocation_attributes", node_id=self._parent_id)

    def __do_load_allocation(self, node: Any = "", row: Gtk.TreeIter = None) -> None:
        """Load the allocation RAMSTKTreeView.

        :param node: the treelib Node with the mode data to load.
        :param row: the parent row of the mode to load into the hardware tree.
        """
        # FIXME: This method needs to accept a treelib.Tree object with all the
        #  allocation and then pass that tree to the treeview method do_load_tree.
        #  This method should handle all exceptions and return None.
        _entity = node.data["allocation"]

        if _entity.parent_id != 0:
            _attributes = [
                _entity.revision_id,
                _entity.hardware_id,
                "",
                _entity.included,
                _entity.n_sub_systems,
                _entity.n_sub_elements,
                _entity.mission_time,
                _entity.duty_cycle,
                _entity.int_factor,
                _entity.soa_factor,
                _entity.op_time_factor,
                _entity.env_factor,
                _entity.weight_factor,
                _entity.percent_weight_factor,
                0.0,
                _entity.hazard_rate_alloc,
                0.0,
                _entity.mtbf_alloc,
                0.0,
                _entity.reliability_alloc,
                0.0,
                _entity.availability_alloc,
                _entity.parent_id,
            ]

            try:
                self.tvwTreeView.unfilt_model.append(row, _attributes)
                pub.sendMessage("request_get_hardware_tree")
                pub.sendMessage("request_get_reliability_tree")
            except (AttributeError, TypeError, ValueError):
                _message = _(
                    f"An error occurred when loading allocation record "
                    f"{node.identifier} into the allocation list.  This might indicate "
                    f"it was missing it's data package, some of the data in the "
                    f"package was missing, or some of the data was the wrong type.  "
                    f"Row data was: {_attributes}"
                )

                pub.sendMessage(
                    "do_log_warning_msg",
                    logger_name="WARNING",
                    message=_message,
                )
