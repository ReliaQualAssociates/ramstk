# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.stakeholder.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Stakeholder panel module."""

# Standard Library Imports
from typing import Dict, List, Tuple

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCellRendererCombo,
    RAMSTKCellRendererSpin,
    RAMSTKCellRendererText,
    RAMSTKTreePanel,
    WidgetConfig,
    make_widget_config,
)


class StakeholderTreePanel(RAMSTKTreePanel):
    """Panel to display a list of stakeholder inputs."""

    # Define private class attributes.
    _select_msg = "succeed_retrieve_all_stakeholder"
    _tag = "stakeholder"
    _title = _("Stakeholder Input List")

    def __init__(self) -> None:
        """Initialize an instance of the stakeholder input panel."""
        super().__init__()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "revision_id",
                    "index": 0,
                    "label_text": _("Revision ID"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_stakeholder",
                },
                {
                    "editable": False,
                    "tooltip": "",
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "stakeholder_id",
                    "index": 1,
                    "label_text": _("Stakeholder ID"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_stakeholder",
                },
                {
                    "editable": False,
                    "tooltip": "",
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererSpin(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "customer_rank",
                    "index": 2,
                    "label_text": _("Customer Ranking"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_stakeholder",
                },
                {
                    "editable": True,
                    "tooltip": "",
                    "visible": True,
                    "digits": 0,
                    "lower": 1,
                    "step_increment": 1,
                    "upper": 5,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "description",
                    "index": 3,
                    "label_text": _("Description"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_stakeholder",
                },
                {
                    "editable": True,
                    "tooltip": "",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "group",
                    "index": 4,
                    "label_text": _("Affinity Group"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_stakeholder",
                },
                {
                    "editable": True,
                    "tooltip": "",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "improvement",
                    "index": 5,
                    "label_text": _("Improvement Factor"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_stakeholder",
                },
                {
                    "editable": False,
                    "tooltip": "",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": "",
                    "field": "overall_weight",
                    "index": 6,
                    "label_text": _("Overall Weighting"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_stakeholder",
                },
                {
                    "editable": False,
                    "tooltip": "",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererSpin(),
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "planned_rank",
                    "index": 7,
                    "label_text": _("Planned Satisfaction Rating"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_stakeholder",
                },
                {
                    "editable": True,
                    "tooltip": "",
                    "visible": True,
                    "digits": 0,
                    "lower": 1,
                    "step_increment": 1,
                    "upper": 5,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererSpin(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "priority",
                    "index": 8,
                    "label_text": _("Priority"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_stakeholder",
                },
                {
                    "editable": True,
                    "tooltip": "",
                    "visible": True,
                    "digits": 0,
                    "lower": 1,
                    "step_increment": 1,
                    "upper": 5,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gint",
                    "default": "",
                    "field": "requirement_id",
                    "index": 9,
                    "label_text": _("Associated Requirement"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_stakeholder",
                },
                {
                    "editable": True,
                    "tooltip": "",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "stakeholder",
                    "index": 10,
                    "label_text": _("Stakeholder"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_stakeholder",
                },
                {
                    "editable": True,
                    "tooltip": "",
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": "",
                    "field": "user_float_1",
                    "index": 11,
                    "label_text": _("User Float 1"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_stakeholder",
                },
                {
                    "editable": True,
                    "tooltip": "",
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "user_float_2",
                    "index": 12,
                    "label_text": _("User Float 2"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_stakeholder",
                },
                {
                    "editable": True,
                    "tooltip": "",
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "user_float_3",
                    "index": 13,
                    "label_text": _("User Float 3"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_stakeholder",
                },
                {
                    "editable": True,
                    "tooltip": "",
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0,
                    "field": "user_float_4",
                    "index": 14,
                    "label_text": _("User Float 4"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_stakeholder",
                },
                {
                    "editable": True,
                    "tooltip": "",
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0,
                    "field": "user_float_5",
                    "index": 15,
                    "label_text": _("User Float 5"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_stakeholder",
                },
                {
                    "editable": True,
                    "tooltip": "",
                    "visible": False,
                },
            ),
        ]
        self._lst_groups: List[str] = []
        self._lst_stakeholders: List[str] = []
        self._on_edit_message: str = f"wvw_editing_{self._tag}"

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_tree_panel()
        super().do_set_widget_callbacks()

        # FIXME: Is this line needed?
        # self.tvwTreeView.dic_row_loader = {
        #    "stakeholder": super().do_load_treerow,
        # }
        self.tvwTreeView.set_tooltip_text(_("Displays the list of stakeholders."))

        do_subscribe_to_messages(
            {
                "succeed_calculate_stakeholder": super().do_load_tree_panel,
                "succeed_retrieve_all_requirement": self._do_load_requirements,
            }
        )

    def do_load_affinity_groups(self, affinities: Dict[int, Tuple[str, str]]) -> None:
        """Load the affinity group list.

        :param affinities: the dict containing the affinity groups and the group type
            (affinity in all cases).
        """
        for _group in affinities:
            self._lst_groups.append(affinities[_group][0])

        self.tvwTreeView.do_load_cellrenderercombo("group", self._lst_groups)

    def do_load_stakeholders(self, stakeholders: Dict[int, str]) -> None:
        """Load the stakeholder list.

        :param stakeholders: the dict containing the names of the stakeholders.
        """
        for _stakeholder in stakeholders:
            self._lst_stakeholders.append(stakeholders[_stakeholder][0])

        self.tvwTreeView.do_load_cellrenderercombo(
            "stakeholder",
            self._lst_stakeholders,
        )

    def _do_load_requirements(self, tree: treelib.Tree) -> None:
        """Load the requirement ID list when Requirements are retrieved.

        :param tree: the treelib.Tree containing the Stakeholder data records.
        """
        _cell = self.tvwTreeView.get_column(
            self.tvwTreeView.dic_field_position_map["requirement_id"]
        ).get_cells()[0]
        _model = _cell.get_property("model")
        _model.clear()

        for _node in tree.nodes:
            if _node != 0:
                _model.append(
                    [str(tree.nodes[_node].data["requirement"].requirement_id)]
                )

    def _on_insert(self, tree: treelib.Tree) -> None:
        """Wrap the do_load_panel() method when an element is inserted.

        The do_set_cursor_active() method responds to the same message, but one less
        argument in its call.  This results in a PyPubSub error and is the reason this
        wrapper method is needed.

        :param tree: the module's treelib.Tree.
        """
        super().do_load_panel(tree)

    def _on_module_switch(self, module: str = "") -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == self._tag and _row is not None:
            _code = _model.get_value(
                _row, self.tvwTreeView.dic_field_position_map["stakeholder_id"]
            )
            _name = _model.get_value(
                _row, self.tvwTreeView.dic_field_position_map["description"]
            )
            _title = _(f"Analyzing Stakeholder {_code}: {_name}")

            pub.sendMessage("request_set_title", title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the List View RAMSTKTreeView().

        This method is called whenever a Stakeholder List View RAMSTKTreeView() row is
        activated/changed.

        :param selection: the Stakeholder class Gtk.TreeSelection().
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes["stakeholder_id"]
            self._parent_id = _attributes["requirement_id"]

            pub.sendMessage("selected_stakeholder", attributes=_attributes)
