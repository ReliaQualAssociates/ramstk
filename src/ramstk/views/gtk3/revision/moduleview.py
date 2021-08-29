# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.moduleview.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Revision GTK3 module view."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKMessageDialog, RAMSTKModuleView

# RAMSTK Local Imports
from . import RevisionTreePanel


class RevisionModuleView(RAMSTKModuleView):
    """Display Revision attribute data in the RAMSTK Module Book.

    The Revision Module View displays all the Revisions associated with the
    connected RAMSTK Program in a flat list.  The attributes of a Revision
    Module View are:

    :cvar _module: the name of the module.

    :ivar _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = "revision"
    _tablabel: str = "Revision"
    _tabtooltip: str = _(
        "Displays the list of Revisions for the open RAMSTK " "Project."
    )

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Revision Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_icons["tab"] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + "/32x32/revision.png"
        )

        # Initialize private list attributes.
        self._lst_mnu_labels = [
            _("Add Revision"),
            _("Delete Selected Revision"),
            _("Save Selected Revision"),
            _("Save All Revisions"),
        ]
        self._lst_tooltips = [
            _("Add a new revision."),
            _("Remove the currently selected revision."),
            _("Save changes to the currently selected revision."),
            _("Save changes to all revisions."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = RevisionTreePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, "selected_revision")
        pub.subscribe(self._on_insert_revision, "succeed_insert_revision")

    def do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete selected record from the RAMSTKRevision table.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent().get_parent()
        _prompt = _(
            "You are about to delete Revision {0:d} and all "
            "data associated with it.  Is this really what "
            "you want to do?"
        ).format(self._revision_id)
        _dialog = RAMSTKMessageDialog(parent=_parent)
        _dialog.do_set_message(_prompt)
        _dialog.do_set_message_type("question")

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage("request_delete_revision", node_id=self._revision_id)

        _dialog.do_destroy()

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the Revision's record ID.

        :param attributes: the attributes dict for the selected Revision.
        :return: None
        :rtype: None
        """
        self._record_id = attributes["revision_id"]

    def _on_insert_revision(self, node_id: int = 0, tree: treelib.Tree = "") -> None:
        """Add row to module view for newly added revision.

        :param node_id: the ID of the newly added revision.
        :param tree: the treelib Tree() containing the work stream module's
            data.
        :return: None
        """
        _data = tree.get_node(node_id).data["revision"].get_attributes()
        self._pnlPanel.on_insert(_data)

    def __make_ui(self) -> None:
        """Build the user interface for the revision module view.

        :return: None
        """
        super().make_ui()

        self._pnlPanel.do_set_properties()
        self._pnlPanel.do_set_callbacks()
        self._pnlPanel.tvwTreeView.dic_handler_id[
            "button-press"
        ] = self._pnlPanel.tvwTreeView.connect(
            "button_press_event", super().on_button_press
        )
