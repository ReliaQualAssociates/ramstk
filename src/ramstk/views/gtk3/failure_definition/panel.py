# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.failure_definition.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Failure Definition Panels."""

# Standard Library Imports
from typing import Any, Callable, Dict, List

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKTreePanel


class FailureDefinitionTreePanel(RAMSTKTreePanel):
    """Panel to display list of failure definitions."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_retrieve_failure_definitions"
    _tag = "failure_definition"
    _title = _("Failure Definition List")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the failure definition panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self._dic_row_loader: Dict[str, Callable] = {
            "failure_definition": self.__do_load_failure_definition,
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._on_edit_callback: str = "lvw_editing_{}".format(self._tag)

        # Initialize public dictionary class attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "revision_id": [
                0,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_callback,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Revision ID"),
            ],
            "definition_id": [
                1,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_callback,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Definition ID"),
            ],
            "definition": [
                2,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_callback,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Definition"),
            ],
        }

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_make_panel()
        super().do_set_properties()
        super().do_set_callbacks()

        self.tvwTreeView.set_tooltip_text(
            _("Displays the list of failure definitions for the selected revision.")
        )

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_module_switch, "lvwSwitchedPage")

    def _on_module_switch(self, module: str = "") -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == "failure_definition" and _row is not None:
            _code = _model.get_value(_row, self._lst_col_order[1])
            _title = _("Analyzing Failure Definition {0:s}").format(str(_code))

            pub.sendMessage("request_set_title", title=_title)

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

            pub.sendMessage("selected_failure_definition", attributes=_attributes)

    def __do_load_failure_definition(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter:
        """Load a failure definition into the RAMSTKTreeView().

        :param node: the treelib Node() with the definition data to load.
        :param row: the parent row of the definition to load.
        :return: _new_row; the row that was just populated with definition
            data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        _attributes = [_entity.revision_id, _entity.definition_id, _entity.definition]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading failure definition {0:s}.  "
                "This might indicate it was missing it's data package, some "
                "of the data in the package was missing, or some of the data "
                "was the wrong type.  Row data was: {1}"
            ).format(str(node.identifier), _attributes)
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row
