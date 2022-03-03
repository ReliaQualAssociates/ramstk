# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.function.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Function Panels."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    RAMSTKTextView,
    RAMSTKTreePanel,
)


class FunctionTreePanel(RAMSTKTreePanel):
    """Panel to display hierarchy of functions."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_retrieve_all_function"
    _tag = "function"
    _title = _("Function Tree")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Function panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self.tvwTreeView.dic_row_loader = {
            "function": super().do_load_treerow,
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
            "function_id": [
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
                _("Function ID"),
                "gint",
            ],
            "availability_logistics": [
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
                _("Logistics A(t)"),
                "gfloat",
            ],
            "availability_mission": [
                3,
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
                    "visible": True,
                },
                _("Cost"),
                "gfloat",
            ],
            "function_code": [
                5,
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
                _("Function Code"),
                "gchararray",
            ],
            "hazard_rate_logistics": [
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
                _("Logistcs h(t)"),
                "gfloat",
            ],
            "hazard_rate_mission": [
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
                _("Mission h(t)"),
                "gfloat",
            ],
            "level": [
                8,
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
                _("Level"),
                "gint",
            ],
            "mmt": [
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
                    "visible": False,
                },
                _("MMT"),
                "gfloat",
            ],
            "mcmt": [
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
                _("MCMT"),
                "gfloat",
            ],
            "mpmt": [
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
                _("MPMT"),
                "gfloat",
            ],
            "mtbf_logistics": [
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
                    "visible": True,
                },
                _("Logistics MTBF"),
                "gfloat",
            ],
            "mtbf_mission": [
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
                    "visible": True,
                },
                _("Mission MTBF"),
                "gfloat",
            ],
            "mttr": [
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
                    "visible": False,
                },
                _("MTTR"),
                "gfloat",
            ],
            "name": [
                15,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Name"),
                "gchararray",
            ],
            "parent_id": [
                16,
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
                _("Parent ID"),
                "gint",
            ],
            "remarks": [
                17,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Remarks"),
                "gchararray",
            ],
            "safety_critical": [
                18,
                Gtk.CellRendererToggle(),
                "toggled",
                super().on_cell_toggled,
                self._on_edit_message,
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Safety Critical"),
                "gint",
            ],
            "total_mode_count": [
                19,
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
                _("Mode Count"),
                "gint",
            ],
            "total_part_count": [
                20,
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
            "type_id": [
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
                _("Type"),
                "gint",
            ],
        }

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.tvwTreeView.set_tooltip_text(
            _("Displays the hierarchical list of functions.")
        )

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_module_switch, "mvwSwitchedPage")

    def _on_module_switch(self, module: str = "") -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == self._tag and _row is not None:
            _code = _model.get_value(_row, self.tvwTreeView.position["function_code"])
            _name = _model.get_value(_row, self.tvwTreeView.position["name"])
            _title = _(f"Analyzing Function {_code}: {_name}")

            pub.sendMessage("request_set_title", title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Function package Module View RAMSTKTreeView().

        This method is called whenever a Function Module View RAMSTKTreeView()
        row is activated/changed.

        :param selection: the Function class Gtk.TreeSelection().
        :return: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes["function_id"]
            self._parent_id = _attributes["parent_id"]

            _title = _("Analyzing Function {0:s}: {1:s}").format(
                str(_attributes["function_code"]), str(_attributes["name"])
            )

            pub.sendMessage(
                "selected_function",
                attributes=_attributes,
            )
            pub.sendMessage(
                "request_set_title",
                title=_title,
            )


class FunctionGeneralDataPanel(RAMSTKFixedPanel):
    """The panel to display general data about the selected Function."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "function_id"
    _select_msg = "selected_function"
    _tag = "function"
    _title = _("General Function Information")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Function General Data panel."""
        super().__init__()

        # Initialize widgets.
        self.chkSafetyCritical: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Function is safety critical.")
        )
        self.txtCode: RAMSTKEntry = RAMSTKEntry()
        self.txtName: RAMSTKEntry = RAMSTKEntry()
        self.txtRemarks: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map = {
            "function_code": [
                5,
                self.txtCode,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                "",
                {
                    "width": 125,
                    "tooltip": _("A unique code for the selected function."),
                },
                _("Function Code:"),
                "gchararray",
            ],
            "name": [
                15,
                self.txtName,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                "",
                {
                    "width": 800,
                    "tooltip": _("The name of the selected function."),
                },
                _("Function Description:"),
                "gchararray",
            ],
            "remarks": [
                17,
                self.txtRemarks,
                "changed",
                super().on_changed_textview,
                f"wvw_editing_{self._tag}",
                "",
                {
                    "height": 100,
                    "width": 800,
                    "tooltip": _(
                        "Enter any remarks associated with the selected function."
                    ),
                },
                _("Remarks:"),
                "gchararray",
            ],
            "safety_critical": [
                18,
                self.chkSafetyCritical,
                "toggled",
                super().on_toggled,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _(
                        "Indicates whether or not the selected function is safety "
                        "critical."
                    )
                },
                "",
                "gint",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
