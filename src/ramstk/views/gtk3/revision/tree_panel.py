# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.tree_panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Revision tree panel module."""

# Standard Library Imports
from typing import List

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCellRendererText,
    RAMSTKTreePanel,
    WidgetConfig,
)


class RevisionTreePanel(RAMSTKTreePanel):
    """Panel to display flat list of revisions."""

    # Define private class attributes.
    _select_msg = "succeed_retrieve_all_revision"
    _tag = "revision"
    _title = _("List of Revisions")

    def __init__(self) -> None:
        """Initialize an instance of the Revision tree panel widget."""
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
                    "index": 1,
                    "label_text": _("Logistics A(t)"),
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
                    "field": "availability_mission",
                    "index": 2,
                    "label_text": _("Mission A(t)"),
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
                    "field": "cost",
                    "index": 3,
                    "label_text": _("Cost"),
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
                    "field": "cost_failure",
                    "index": 4,
                    "label_text": _("Cost/Failure"),
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
                    "field": "cost_hour",
                    "index": 5,
                    "label_text": _("Cost/Hour"),
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
                    "field": "hazard_rate_active",
                    "index": 6,
                    "label_text": _("Active h(t)"),
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
                    "field": "hazard_rate_dormant",
                    "index": 7,
                    "label_text": _("Dormant h(t)"),
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
                    "index": 8,
                    "label_text": _("Logistics h(t)"),
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
                    "index": 9,
                    "label_text": _("Mission h(t)"),
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
                    "field": "hazard_rate_software",
                    "index": 10,
                    "label_text": _("Software h(t)"),
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
                    "field": "mmt",
                    "index": 11,
                    "label_text": _("MMT"),
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
                    "field": "mcmt",
                    "index": 12,
                    "label_text": "MCMT",
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
                    "field": "mpmt",
                    "index": 13,
                    "label_text": "MPMT",
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
                    "index": 14,
                    "label_text": _("Logistics MTBF"),
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
                    "index": 15,
                    "label_text": _("Mission MTBF"),
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
                    "index": 16,
                    "label_text": "MTTR",
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
                    "field": "name",
                    "index": 17,
                    "label_text": _("Revision Name"),
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
                    "field": "reliability_logistics",
                    "index": 18,
                    "label_text": _("Logistics R(t)"),
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
                    "field": "reliability_mission",
                    "index": 19,
                    "label_text": _("Mission R(t)"),
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
                    "field": "remarks",
                    "index": 20,
                    "label_text": _("Remarks"),
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
                    "default": 0,
                    "field": "total_part_count",
                    "index": 21,
                    "label_text": _("Part Count"),
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
                    "field": "revision_code",
                    "index": 22,
                    "label_text": _("Cost"),
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
                    "field": "program_time",
                    "index": 23,
                    "label_text": _("Program Time"),
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
                    "field": "program_time_sd",
                    "index": 24,
                    "label_text": _("Program Time SE"),
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
                    "field": "program_cost",
                    "index": 25,
                    "label_text": _("Total Cost"),
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
                    "field": "program_cost_sd",
                    "index": 26,
                    "label_text": _("Total Cost SE"),
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
        ]
        self._on_edit_message: str = f"mvw_editing_{self._tag}"

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_tree_panel()
        super().do_set_widget_callbacks()

        self.tvwTreeView.set_tooltip_text(_("Displays the list of revisions."))

    # ----- ----- RAMSTKTreePanel specific methods. ----- ----- #
    def _on_module_switch(self, module: str = "") -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == self._tag and _row is not None:
            _code = _model.get_value(_row, self.tvwTreeView.position["revision_code"])
            _name = _model.get_value(_row, self.tvwTreeView.position["name"])
            _title = _(f"Analyzing Revision {_code}: {_name}")
            super().do_set_title(_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Revision package Module View RAMSTKTreeView.

        This method is called whenever a Revision Module View RAMSTKTreeView row is
        activated/changed.

        :param selection: the Revision class Gtk.TreeSelection.
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            _title = _(
                f"Analyzing Revision {_attributes["revision_code"]}: "
                f"{_attributes["name"]}"
            )
            super().do_set_title(_title)
