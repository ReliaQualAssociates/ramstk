# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.function.tree_panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Function tree panel module."""

# Standard Library Imports
from typing import List

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCellRendererText,
    RAMSTKCellRendererToggle,
    RAMSTKTreePanel,
    WidgetConfig,
)


class FunctionTreePanel(RAMSTKTreePanel):
    """Panel to display hierarchy of functions."""

    # Define private class attributes.
    _select_msg = "succeed_retrieve_all_function"
    _tag = "function"
    _title = _("Function Tree")

    def __init__(self) -> None:
        """Initialize an instance of the FunctionTreePanel widget."""
        super().__init__()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "revision_id",
                    "index": 0,
                    "label_text": _("Revision ID"),
                    "listen_topic": f"wvw_editing_{self._tag}",
                },
                "properties": {
                    "background_" "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "function_id",
                    "index": 1,
                    "label_text": _("Function ID"),
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "default": 1.0,
                    "field": "availability_logistics",
                    "index": 2,
                    "label_text": _("Logistics A(t)"),
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "default": 1.00,
                    "field": "availability_mission",
                    "index": 3,
                    "label_text": _("Mission A(t)"),
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "field": "cost",
                    "index": 4,
                    "label_text": _("Cost"),
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "field": "function_code",
                    "index": 5,
                    "label_text": _("Function Code"),
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "index": 6,
                    "label_text": _("Logistics h(t)"),
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "field": "hazard_rate_mission",
                    "index": 7,
                    "label_text": _("Mission h(t)"),
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "field": "level",
                    "index": 8,
                    "label_text": _("Level"),
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "field": "mmt",
                    "index": 9,
                    "label_text": "MMT",
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "field": "mcmt",
                    "index": 10,
                    "label_text": "MCMT",
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "field": "mpmt",
                    "index": 11,
                    "label_text": "MPMT",
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "field": "mtbf_logistics",
                    "index": 12,
                    "label_text": _("Logistics MTBF"),
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "field": "mtbf_mission",
                    "index": 13,
                    "label_text": _("Mission MTBF"),
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "field": "mttr",
                    "index": 14,
                    "label_text": "MTTR",
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "index": 15,
                    "label_text": _("Function Name"),
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "index": 16,
                    "label_text": _("Parent ID"),
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "field": "remarks",
                    "index": 17,
                    "label_text": _("Remarks"),
                    "listen_topic": f"wvw_editing_{self._tag}",
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererToggle(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "safety_critical",
                    "index": 18,
                    "label_text": _("Safety Critical"),
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "field": "total_mode_count",
                    "index": 19,
                    "label_text": _("Mode Count"),
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "field": "total_part_count",
                    "index": 20,
                    "label_text": _("Total Parts"),
                    "listen_topic": f"wvw_editing_{self._tag}",
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
                    "default": "",
                    "field": "type_id",
                    "index": 21,
                    "label_text": _("Function Type"),
                    "listen_topic": f"wvw_editing_{self._tag}",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
        ]
        self._on_edit_message: str = f"mvw_editing_{self._tag}"

        super().do_set_widget_properties()
        super().do_make_panel()
        super().do_set_widget_callbacks()

        self.tvwTreeView.set_tooltip_text(
            _("Displays the hierarchical list of functions.")
        )

    # ----- ----- RAMSTKTreePanel specific methods. ----- ----- #
    def _on_module_switch(self, module: str = "") -> None:
        """Respond to changes in FunctionModuleView tab.

        :param module: the name of the module that was just selected.
        """
        # FIXME: This method needs to use something other than the position dict of
        #  the RAMSTKTreeView class to get the column numbers.
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == self._tag and _row is not None:
            _code = _model.get_value(_row, self.tvwTreeView.position["function_code"])
            _name = _model.get_value(_row, self.tvwTreeView.position["name"])
            _title = _(f"Analyzing Function {_code}: {_name}")
            super().do_set_title(_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the FunctionModuleView RAMSTKTreeView.

        This method is called whenever a FunctionModuleView RAMSTKTreeView row is
        activated/changed.

        :param selection: the FunctionTreePanel RAMSTKTreeView Gtk.TreeSelection.
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            _title = _(
                f"Analyzing Function {_attributes["function_code"]}: "
                f"{_attributes["name"]}"
            )
            super().do_set_title(_title)
