# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Revision Panels."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKPanel


class RevisionTreePanel(RAMSTKPanel):
    """Panel to display flat list of revisions."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg: str = "succeed_retrieve_revisions"
    _tag: str = "revision"
    _title: str = _("Revision List")
    _type: str = "tree"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Revision panel."""
        super().__init__()

        # Initialize private dictionary class attributes.

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.

        # Initialize public dictionary class attributes.
        self.dic_attribute_index_map = {
            17: ["name", "string"],
            20: ["remarks", "string"],
            22: ["revision_code", "string"],
        }
        self.dic_attribute_widget_map = {
            "revision_id": [
                0,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
            ],
            "availability_logistics": [
                1,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                1.0,
            ],
            "availability_mission": [
                2,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                1.0,
            ],
            "cost": [
                3,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "cost_per_failure": [
                4,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "cost_per_hour": [
                5,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "hazard_rate_active": [
                6,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "hazard_rate_dormant": [
                7,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "hazard_rate_logistics": [
                8,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "hazard_rate_mission": [
                9,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "hazard_rate_software": [
                10,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "mmt": [
                11,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "mcmt": [
                12,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "mpmt": [
                13,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "mtbf_logistics": [
                14,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "mtbf_mission": [
                15,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "mttr": [
                16,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "name": [
                17,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_revision",
                "",
            ],
            "reliability_logistics": [
                18,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                1.0,
            ],
            "reliability_mission": [
                19,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                1.0,
            ],
            "remarks": [
                20,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_revision",
                "",
            ],
            "n_parts": [
                21,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0,
            ],
            "revision_code": [
                22,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_revision",
                "",
            ],
            "program_time": [
                23,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "program_time_sd": [
                24,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "program_cost": [
                25,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
            "program_cost_sd": [
                26,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_revision",
                0.0,
            ],
        }

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_make_tree_panel()
        super().do_set_properties()
        super().do_set_callbacks()

        self.tvwTreeView.set_tooltip_text(_("Displays the list of revisions."))

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_module_switch, "mvwSwitchedPage")

    def _on_module_switch(self, module: str = "") -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == "revision" and _row is not None:
            _code = _model.get_value(_row, self._lst_col_order[5])
            _name = _model.get_value(_row, self._lst_col_order[15])
            _title = _("Analyzing Revision {0:s}: {1:s}").format(str(_code), str(_name))

            pub.sendMessage("request_set_title", title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Revision package Module View RAMSTKTreeView().

        This method is called whenever a Revision Module View RAMSTKTreeView()
        row is activated/changed.

        :param selection: the Revision class Gtk.TreeSelection().
        :return: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes["revision_id"]

            _title = _("Analyzing Revision {0:s}: {1:s}").format(
                str(_attributes["revision_code"]), str(_attributes["name"])
            )

            # pub.sendMessage("selected_revision", attributes=_attributes)
            pub.sendMessage("request_set_title", title=_title)
