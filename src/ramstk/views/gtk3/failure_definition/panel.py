# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.failure_definition.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Failure Definition tree panel module."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCellRendererText,
    RAMSTKTreePanel,
    WidgetConfig,
    make_widget_config,
)


class FailureDefinitionTreePanel(RAMSTKTreePanel):
    """Panel to display list of failure definitions."""

    # Define private class attributes.
    _select_msg = "succeed_retrieve_all_definition"
    _tag = "definition"
    _title = _("Failure Definition List")

    def __init__(self) -> None:
        """Initialize an instance of the failure definition panel."""
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
                    "listen_topic": "wvw_editing_definition",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "function_id",
                    "index": 1,
                    "label_text": _("Function ID"),
                    "listen_topic": "wvw_editing_definition",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "definition_id",
                    "index": 2,
                    "label_text": _("Definition ID"),
                    "listen_topic": "wvw_editing_definition",
                },
                {
                    "editable": False,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "definition",
                    "index": 3,
                    "label_text": _("Definition"),
                    "listen_topic": "wvw_editing_definition",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
        ]
        self._filtered_tree = True
        self._on_edit_message: str = f"wvw_editing_{self._tag}"

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_tree_panel()
        super().do_set_widget_callbacks()

        # FIXME: Is this line needed?
        # self.tvwTreeView.dic_row_loader = {
        #    "definition": super().do_load_treerow,
        # }
        self.tvwTreeView.set_tooltip_text(
            _("Displays the list of failure definitions for the selected revision.")
        )

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "selected_function": self._on_select_function,
            }
        )

    # ----- ----- RAMSTKTreePanel specific methods. ----- ----- #
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Read attributes from newly selected RAMSTKTreeView row.

        This method is called whenever a view's RAMSTKTreeView row is activated/changed.

        :param selection: the Gtk.TreeSelection() for the newly selected row.
        """
        _attributes = super().on_row_change(selection)

        # FIXME: Can we move setting the record ID to the super class?
        if _attributes:
            self._record_id = _attributes["definition_id"]

            pub.sendMessage(
                "selected_failure_definition",
                attributes=_attributes,
            )

    # ----- -- FailureDefinitionTreePanel specific methods. --- ----- #
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

    def _on_select_function(self, attributes: Dict[str, Any]) -> None:
        """Filter hazards list when Function is selected.

        :param attributes: the dict of Function attributes for the selected Function.
        """
        self._parent_id = attributes["function_id"]
        self.tvwTreeView.filt_model.refilter()
