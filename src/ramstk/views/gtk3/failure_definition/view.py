# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.failure_definition.view.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Failure Definition Views."""

# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKWorkView

# RAMSTK Local Imports
from . import FailureDefinitionTreePanel


class FailureDefinitionWorkView(RAMSTKWorkView):
    """Display failure definitions associated with the selected revision.

    The attributes of the failure definition list view are:

    :cvar _tag: the name of the module.  Spaces are replaced with single
        underscores if the name is more than one word.
    :cvar _tablabel: the text to display on the view's tab.
    :cvar _tabtooltip: the text to display in the tooltip for the view's tab.

    :ivar _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag: str = "definition"
    _tablabel = "<span weight='bold'>" + _("Failure\nDefinitions") + "</span>"
    _tabtooltip = _("Displays failure definitions for the selected revision.")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the List View for the failure definition package.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks.insert(0, super().do_request_insert_sibling)
        self._lst_callbacks.insert(1, self._do_request_delete)
        self._lst_icons.insert(0, "add")
        self._lst_icons.insert(1, "remove")
        self._lst_mnu_labels = [
            _("Add Definition"),
            _("Delete Selected Definition"),
            _("Save Selected Definition"),
            _("Save All Definitions"),
        ]
        self._lst_tooltips = [
            _("Add a new failure definition."),
            _("Delete the currently selected failure definition."),
            _("Save changes to the currently selected failure definition"),
            _("Save changes to all failure definitions."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel: FailureDefinitionTreePanel = FailureDefinitionTreePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, "selected_failure_definition")
        pub.subscribe(self._on_select_function, "selected_function")

    # pylint: disable=unused-argument
    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete the selected Failure Definition record.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent().get_parent()
        _dialog = super().do_raise_dialog(parent=_parent)
        _dialog.do_set_message(
            message=_(
                f"You are about to delete Failure Definition "
                f"{self.dic_pkeys['record_id']} and all data associated with it.  Is "
                f"this really what you want to do?"
            )
        )
        _dialog.do_set_message_type(message_type="question")

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage(
                "request_delete_definition",
                node_id=self.dic_pkeys["record_id"],
            )

        _dialog.do_destroy()

    def _do_set_record_id(self, attributes: Dict[str, Union[float, int, str]]) -> None:
        """Set the failure definition's record ID.

        :param attributes: the attribute dict for the selected failure
            definition.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["revision_id"] = attributes["revision_id"]
        self.dic_pkeys["definition_id"] = attributes["definition_id"]
        self.dic_pkeys["parent_id"] = 0
        self.dic_pkeys["record_id"] = attributes["definition_id"]

    def _on_select_function(
        self, attributes: Dict[str, Union[float, int, str]]
    ) -> None:
        """Set the parent ID when a function is selected.

        :param attributes: the function dict for the selected function ID.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["parent_id"] = attributes["function_id"]
        self.dic_pkeys["revision_id"] = attributes["revision_id"]
        self.dic_pkeys["function_id"] = attributes["function_id"]

    def __make_ui(self) -> None:
        """Build the user interface for the failure definition list view.

        :return: None
        """
        super().do_make_layout()
        super().do_embed_treeview_panel()

        self._pnlPanel.tvwTreeView.dic_handler_id[
            "button-press"
        ] = self._pnlPanel.tvwTreeView.connect(
            "button_press_event", super().on_button_press
        )
