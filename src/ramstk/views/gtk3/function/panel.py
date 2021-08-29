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
    RAMSTKPanel,
    RAMSTKTextView,
)


class FunctionTreePanel(RAMSTKPanel):
    """Panel to display hierarchy of functions."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_retrieve_functions"
    _tag = "function"
    _title = _("Function Tree")
    _type = "tree"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Function panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self._dic_row_loader = {
            "function": super()._do_load_treerow,
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.

        # Initialize public dictionary class attributes.
        self.dic_attribute_index_map = {
            5: ["function_code", "string"],
            15: ["name", "string"],
            17: ["remarks", "string"],
            18: ["safety_critical", "bool"],
        }
        self.dic_attribute_widget_map = {
            "revision_id": [
                0,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
            ],
            "function_id": [
                1,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
            ],
            "availability_logistics": [
                2,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
                1.0,
            ],
            "availability_mission": [
                3,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
                1.0,
            ],
            "cost": [
                4,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
                0.0,
            ],
            "function_code": [
                5,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_function",
                "",
            ],
            "failure_rate_logistics": [
                6,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
                0.0,
            ],
            "failure_rate_mission": [
                7,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
                0.0,
            ],
            "level": [
                8,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
                0,
            ],
            "mmt": [
                9,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
                0.0,
            ],
            "mcmt": [
                10,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
                0.0,
            ],
            "mpmt": [
                11,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
                0.0,
            ],
            "mtbf_logistics": [
                12,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
                0.0,
            ],
            "mtbf_mission": [
                13,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
                0.0,
            ],
            "mttr": [
                14,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
                0.0,
            ],
            "name": [
                15,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_function",
                "",
            ],
            "parent_id": [
                16,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
                0,
            ],
            "remarks": [
                17,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_function",
                "",
            ],
            "safety_critical": [
                18,
                Gtk.CellRendererToggle(),
                "toggled",
                super().on_cell_toggled,
                "mvw_editing_function",
                1,
            ],
            "total_mode_count": [
                19,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
                0,
            ],
            "total_part_count": [
                20,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
                0,
            ],
            "type": [
                21,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_function",
                0,
            ],
        }

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_make_tree_panel()
        super().do_set_properties()
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

        if module == "functions" and _row is not None:
            _code = _model.get_value(_row, self._lst_col_order[5])
            _name = _model.get_value(_row, self._lst_col_order[15])
            _title = _("Analyzing Function {0:s}: {1:s}").format(str(_code), str(_name))

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


class FunctionGeneralDataPanel(RAMSTKPanel):
    """The panel to display general data about the selected Function."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "function_id"
    _select_msg = "selected_function"
    _tag = "function"
    _title = _("General Function Information")
    _type = "fixed"

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
        self.dic_attribute_index_map = {
            5: ["function_code", "string"],
            15: ["name", "string"],
            17: ["remarks", "string"],
            18: ["safety_critical", "bool"],
        }
        self.dic_attribute_widget_map = {
            "function_code": [
                5,
                self.txtCode,
                "changed",
                super().on_changed_entry,
                "wvw_editing_function",
                "",
                {
                    "width": 125,
                    "tooltip": _("A unique code for the selected function."),
                },
                _("Function Code:"),
            ],
            "name": [
                15,
                self.txtName,
                "changed",
                super().on_changed_entry,
                "wvw_editing_function",
                "",
                {
                    "width": 800,
                    "tooltip": _("The name of the selected function."),
                },
                _("Function Description:"),
            ],
            "remarks": [
                17,
                self.txtRemarks,
                "changed",
                super().on_changed_textview,
                "mvw_editing_function",
                "",
                {
                    "height": 100,
                    "width": 800,
                    "tooltip": _(
                        "Enter any remarks associated with the selected function."
                    ),
                },
                _("Remarks:"),
            ],
            "safety_critical": [
                18,
                self.chkSafetyCritical,
                "toggled",
                super().on_toggled,
                "mvw_editing_function",
                0,
                {
                    "tooltip": _(
                        "Indicates whether or not the selected function is safety "
                        "critical."
                    )
                },
                "",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        # Make a fixed type panel.
        super().do_set_properties()
        super().do_make_fixed_panel()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
