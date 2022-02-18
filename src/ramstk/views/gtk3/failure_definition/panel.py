# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.failure_definition.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Failure Definition Panels."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKTreePanel


class FailureDefinitionTreePanel(RAMSTKTreePanel):
    """Panel to display list of failure definitions."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_retrieve_all_definition"
    _tag = "definition"
    _title = _("Failure Definition List")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the failure definition panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self.tvwTreeView.dic_row_loader = {
            "definition": super().do_load_treerow,
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._filtered_tree = True
        self._on_edit_message: str = f"wvw_editing_{self._tag}"

        # Initialize public dictionary class attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
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
            "definition_id": [
                2,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Definition ID"),
                "gint",
            ],
            "definition": [
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
                _("Definition"),
                "gchararray",
            ],
        }

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.tvwTreeView.set_tooltip_text(
            _("Displays the list of failure definitions for the selected revision.")
        )

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_select_function, "selected_function")

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_filter_tree(
        self, model: Gtk.TreeModel, row: Gtk.TreeIter, data: Any
    ) -> bool:
        """Filter Hazards to show only those associated with the selected Function.

        :param model: the filtered model for the Hazard RAMSTKTreeView.
        :param row: the iter to check against condition(s).
        :param data: unused in this method; required by Gtk.TreeModelFilter() widget.
        :return: True if row should be visible, False else.
        :rtype: bool
        """
        return model[row][1] == self._parent_id

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Read attributes from newly selected RAMSTKTreeView() row.

        This method is called whenever a view's RAMSTKTreeView() row is
        activated/changed.

        :param selection: the Gtk.TreeSelection() for the newly selected row.
        :return: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes["definition_id"]

            pub.sendMessage(
                "selected_failure_definition",
                attributes=_attributes,
            )

    def _on_select_function(self, attributes: Dict[str, Any]) -> None:
        """Filter hazards list when Function is selected.

        :param attributes: the dict of Function attributes for the selected Function.
        :return: None
        :rtype: None
        """
        self._parent_id = attributes["function_id"]
        self.tvwTreeView.filt_model.refilter()
