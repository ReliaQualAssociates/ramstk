# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.stakeholder.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Stakeholder Panels."""

# Standard Library Imports
from typing import Dict, Tuple

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKTreePanel


class StakeholderTreePanel(RAMSTKTreePanel):
    """Panel to display list of stakeholder inputs."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_retrieve_all_stakeholder"
    _tag = "stakeholder"
    _title = _("Stakeholder Input List")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the stakeholder input panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self.tvwTreeView.dic_row_loader = {
            "stakeholder": super().do_load_treerow,
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._on_edit_message: str = f"lvw_editing_{self._tag}"

        # Initialize public dictionary class attributes.
        self.dic_attribute_widget_map = {
            "revision_id": [
                0,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Revision ID"),
                "gint",
            ],
            "stakeholder_id": [
                1,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Stakeholder ID"),
                "gint",
            ],
            "customer_rank": [
                2,
                Gtk.CellRendererSpin(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "digits": 0,
                    "editable": True,
                    "fg_color": "#000000",
                    "lower": 1,
                    "step": 1,
                    "upper": 5,
                    "visible": True,
                },
                _("Customer Ranking"),
                "gint",
            ],
            "description": [
                3,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Description"),
                "gchararray",
            ],
            "group": [
                4,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Affinity Group"),
                "gchararray",
            ],
            "improvement": [
                5,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Improvement Factor"),
                "gfloat",
            ],
            "overall_weight": [
                6,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Overall Weighting"),
                "gfloat",
            ],
            "planned_rank": [
                7,
                Gtk.CellRendererSpin(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1,
                {
                    "bg_color": "#FFFFFF",
                    "digits": 0,
                    "editable": True,
                    "fg_color": "#000000",
                    "lower": 1,
                    "step": 1,
                    "upper": 5,
                    "visible": True,
                },
                _("Planned Satisfaction Rating"),
                "gint",
            ],
            "priority": [
                8,
                Gtk.CellRendererSpin(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "digits": 0,
                    "editable": True,
                    "fg_color": "#000000",
                    "lower": 1,
                    "step": 1,
                    "upper": 5,
                    "visible": True,
                },
                _("Priority"),
                "gint",
            ],
            "requirement_id": [
                9,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Associated Requirement"),
                "gint",
            ],
            "stakeholder": [
                10,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Stakeholder"),
                "gchararray",
            ],
            "user_float_1": [
                11,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("User Float 1"),
                "gfloat",
            ],
            "user_float_2": [
                12,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("User Float 2"),
                "gfloat",
            ],
            "user_float_3": [
                13,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("User Float 3"),
                "gfloat",
            ],
            "user_float_4": [
                14,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("User Float 4"),
                "gfloat",
            ],
            "user_float_5": [
                15,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("User Float 5"),
                "gfloat",
            ],
        }

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.tvwTreeView.set_tooltip_text(_("Displays the list of stakeholders."))

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_panel, "succeed_calculate_stakeholder")
        pub.subscribe(self._do_load_requirements, "succeed_retrieve_all_requirement")

    def do_load_affinity_groups(self, affinities: Dict[int, Tuple[str, str]]) -> None:
        """Load the affinity group list.

        :param affinities: the dict containing the affinity groups and the
            group type (affinity in all cases).
        :return: None
        """
        _cell = self.tvwTreeView.get_column(
            self.tvwTreeView.position["group"]
        ).get_cells()[0]
        _cell.set_property("has-entry", True)
        _cellmodel = _cell.get_property("model")
        _cellmodel.clear()
        _cellmodel.append([""])

        # pylint: disable=unused-variable
        for _key, _group in affinities.items():
            _cellmodel.append([_group[0]])

    def do_load_stakeholders(self, stakeholders: Dict[int, str]) -> None:
        """Load the stakeholder list.

        :param stakeholders: the dict containing the names of the stakeholders.
        :return: None
        """
        _cell = self.tvwTreeView.get_column(
            self.tvwTreeView.position["stakeholder"]
        ).get_cells()[0]
        _cell.set_property("has-entry", True)
        _cellmodel = _cell.get_property("model")
        _cellmodel.clear()
        _cellmodel.append([""])

        # pylint: disable=unused-variable
        for _key, _group in stakeholders.items():
            _cellmodel.append([_group])

    def _do_load_requirements(self, tree: treelib.Tree) -> None:
        """Load the requirement ID list when Requirements are retrieved.

        :param tree: the treelib Tree() containing the Stakeholder data
            records.
        :return: None
        """
        _cell = self.tvwTreeView.get_column(
            self.tvwTreeView.position["requirement_id"]
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

        The do_set_cursor_active() method responds to the same message,
        but one less argument in it's call.  This results in a PyPubSub
        error and is the reason this wrapper method is needed.

        :param tree: the module's treelib Tree().
        :return: None
        """
        super().do_load_panel(tree)

    def _on_module_switch(self, module: str = "") -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == self._tag and _row is not None:
            _code = _model.get_value(_row, self.tvwTreeView.position["stakeholder_id"])
            _name = _model.get_value(_row, self.tvwTreeView.position["description"])
            _title = _(f"Analyzing Stakeholder {_code}: {_name}")

            pub.sendMessage("request_set_title", title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the List View RAMSTKTreeView().

        This method is called whenever a Stakeholder List View
        RAMSTKTreeView() row is activated/changed.

        :param selection: the Stakeholder class Gtk.TreeSelection().
        :return: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes["stakeholder_id"]
            self._parent_id = _attributes["requirement_id"]

            pub.sendMessage("selected_stakeholder", attributes=_attributes)
