# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Revision Panels."""

# Third Party Imports
from pubsub import pub  # type: ignore

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKEntry,
    RAMSTKFixedPanel,
    RAMSTKTextView,
    RAMSTKTreePanel,
)


class RevisionTreePanel(RAMSTKTreePanel):
    """Panel to display flat list of revisions."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_retrieve_all_revision"
    _tag = "revision"
    _title = _("List of Revisions")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Revision panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self.tvwTreeView.dic_row_loader = {
            "revision": super().do_load_treerow,
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._on_edit_message: str = f"mvw_editing_{self._tag}"

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
            "availability_logistics": [
                1,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Logistics A(t)"),
                "gfloat",
            ],
            "availability_mission": [
                2,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Mission A(t)"),
                "gfloat",
            ],
            "cost": [
                3,
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
                _("Cost"),
                "gfloat",
            ],
            "cost_failure": [
                4,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Cost/Failure"),
                "gfloat",
            ],
            "cost_hour": [
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
                    "visible": False,
                },
                _("Cost/Hour"),
                "gfloat",
            ],
            "hazard_rate_active": [
                6,
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
                _("Active h(t)"),
                "gfloat",
            ],
            "hazard_rate_dormant": [
                7,
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
                _("Dormant h(t)"),
                "gfloat",
            ],
            "hazard_rate_logistics": [
                8,
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
                _("Logistics h(t)"),
                "gfloat",
            ],
            "hazard_rate_mission": [
                9,
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
                _("Mission h(t)"),
                "gfloat",
            ],
            "hazard_rate_software": [
                10,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Software h(t)"),
                "gfloat",
            ],
            "mmt": [
                11,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("MMT"),
                "gfloat",
            ],
            "mcmt": [
                12,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("MCMT"),
                "gfloat",
            ],
            "mpmt": [
                13,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("MPMT"),
                "gfloat",
            ],
            "mtbf_logistics": [
                14,
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
                _("Logistics MTBF"),
                "gfloat",
            ],
            "mtbf_mission": [
                15,
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
                _("Mission MTBF"),
                "gfloat",
            ],
            "mttr": [
                16,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("MTTR"),
                "gfloat",
            ],
            "name": [
                17,
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
                _("Revision Name"),
                "gchararray",
            ],
            "reliability_logistics": [
                18,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Logistics R(t)"),
                "gfloat",
            ],
            "reliability_mission": [
                19,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Mission R(t)"),
                "gfloat",
            ],
            "remarks": [
                20,
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
                _("Remarks"),
                "gchararray",
            ],
            "total_part_count": [
                21,
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
                _("Part Count"),
                "gint",
            ],
            "revision_code": [
                22,
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
                _("Revision Code"),
                "gchararray",
            ],
            "program_time": [
                23,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Program Time"),
                "gfloat",
            ],
            "program_time_sd": [
                24,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Program Time SE"),
                "gfloat",
            ],
            "program_cost": [
                25,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Total Cost"),
                "gfloat",
            ],
            "program_cost_sd": [
                26,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Total Cost SE"),
                "gfloat",
            ],
        }

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_set_properties()
        super().do_make_panel()
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

        if module == self._tag and _row is not None:
            _code = _model.get_value(_row, self.tvwTreeView.position["revision_code"])
            _name = _model.get_value(_row, self.tvwTreeView.position["name"])
            _title = _(f"Analyzing Revision {_code}: {_name}")

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

            pub.sendMessage("selected_revision", attributes=_attributes)
            pub.sendMessage("request_set_title", title=_title)


class RevisionGeneralDataPanel(RAMSTKFixedPanel):
    """The panel to display general data about the selected Revision."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "revision_id"
    _select_msg = "selected_revision"
    _tag = "revision"
    _title = _("General Revision Information")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Revision General Data panel."""
        super().__init__()

        # Initialize widgets.
        self.txtCode: RAMSTKEntry = RAMSTKEntry()
        self.txtName: RAMSTKEntry = RAMSTKEntry()
        self.txtRemarks: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map = {
            "revision_code": [
                22,
                self.txtCode,
                "changed",
                super().on_changed_entry,
                "wvw_editing_revision",
                "",
                {
                    "width": 125,
                    "tooltip": _("A unique code for the selected revision."),
                },
                _("Revision Code:"),
                "gchararray",
            ],
            "name": [
                17,
                self.txtName,
                "changed",
                super().on_changed_entry,
                "wvw_editing_revision",
                "",
                {
                    "width": 800,
                    "tooltip": _("The name of the selected revision."),
                },
                _("Revision Name:"),
                "gchararray",
            ],
            "remarks": [
                20,
                self.txtRemarks,
                "changed",
                super().on_changed_textview,
                "wvw_editing_revision",
                "",
                {
                    "height": 100,
                    "width": 800,
                    "tooltip": _(
                        "Enter any remarks associated with the selected revision."
                    ),
                },
                _("Remarks:"),
                "gchararray",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
