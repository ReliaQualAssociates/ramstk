# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.stakeholder.view.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Stakeholder Views."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKWorkView

# RAMSTK Local Imports
from . import StakeholderTreePanel


class StakeholderWorkView(RAMSTKWorkView):
    """Display Stakeholder Inputs associated with the selected Revision.

    The Stakeholder List View displays all the stakeholder inputs associated
    with the selected Requirement.  The attributes of the Stakeholder List
    View are:

    :cvar _tag: the name of the module.

    :ivar _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag = "stakeholder"
    _tablabel = "<span weight='bold'>" + _("Stakeholder\nInputs") + "</span>"
    _tabtooltip = _("Displays stakeholder inputs for the selected revision.")
    _view_type = "list"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the List View for the Requirement package.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks.insert(0, super().do_request_insert_sibling)
        self._lst_callbacks.insert(1, self._do_request_delete)
        self._lst_callbacks.insert(2, self._do_request_calculate)
        self._lst_icons.insert(0, "add")
        self._lst_icons.insert(1, "remove")
        self._lst_icons.insert(2, "calculate")
        self._lst_mnu_labels.insert(0, _("Add New Input"))
        self._lst_mnu_labels.insert(1, _("Delete Selected Input"))
        self._lst_mnu_labels.insert(2, _("Calculate Inputs"))
        self._lst_tooltips.insert(0, _("Add a new stakeholder input."))
        self._lst_tooltips.insert(
            1, _("Remove the currently selected stakeholder input.")
        )
        self._lst_tooltips.insert(
            2, _("Calculate the stakeholder improvement factors.")
        )
        self._lst_tooltips.insert(
            3, _("Update the currently selected stakeholder input.")
        )
        self._lst_tooltips.insert(4, _("Update all stakeholder inputs."))

        # Initialize private scalar attributes.
        self._pnlPanel = StakeholderTreePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, "selected_stakeholder")

    def _do_add_to_affinity_group(self, new_text: str) -> None:
        """Add an entry to the RAMSTK_AFFINITY_GROUP dictionary.

        :param new_text: the name of the new group to add to the
            RAMSTK_AFFINITY_GROUP dictionary.
        :return: None
        """
        try:
            _new_key = (
                max(self.RAMSTK_USER_CONFIGURATION.RAMSTK_AFFINITY_GROUPS.keys()) + 1
            )
        except ValueError:
            _new_key = 1
        self.RAMSTK_USER_CONFIGURATION.RAMSTK_AFFINITY_GROUPS[_new_key] = str(new_text)

    # pylint: disable=unused-argument
    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Request to calculate the selected Stakeholder input.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage(
            "request_calculate_stakeholder",
            node_id=self.dic_pkeys["record_id"],
        )
        super().do_set_cursor_active()

    # pylint: disable=unused-argument
    def _do_request_calculate_all(self, __button: Gtk.ToolButton) -> None:
        """Request to calculate all Stakeholder inputs.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage("request_calculate_all_stakeholders")
        super().do_set_cursor_active()

    # pylint: disable=unused-argument
    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete the selected Stakeholder.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent().get_parent()
        _dialog = super().do_raise_dialog(parent=_parent)
        _dialog.do_set_message(
            message=_(
                "You are about to delete Stakeholder input {0:d} and "
                "all data associated with it.  Is this really what you "
                "want to do?"
            ).format(self.dic_pkeys["record_id"])
        )
        _dialog.do_set_message_type(message_type="question")

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage(
                "request_delete_stakeholder",
                node_id=self.dic_pkeys["record_id"],
            )

        _dialog.do_destroy()

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the stakeholder input's record ID.

        :param attributes: the attribute dict for the selected stakeholder
            input.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["revision_id"] = attributes["revision_id"]
        self.dic_pkeys["parent_id"] = 0
        self.dic_pkeys["stakeholder_id"] = attributes["requirement_id"]
        self.dic_pkeys["record_id"] = attributes["stakeholder_id"]

    def __make_ui(self) -> None:
        """Build the user interface for the stakeholder input list view.

        :return: None
        """
        super().do_make_layout()
        super().do_embed_treeview_panel()

        self._pnlPanel.do_load_affinity_groups(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_AFFINITY_GROUPS
        )
        self._pnlPanel.do_load_stakeholders(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_STAKEHOLDERS
        )

        self._pnlPanel.tvwTreeView.dic_handler_id[
            "button-press"
        ] = self._pnlPanel.tvwTreeView.connect(
            "button_press_event", super().on_button_press
        )
