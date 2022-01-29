# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.view.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Revision Views."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub  # type: ignore

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKMessageDialog,
    RAMSTKModuleView,
    RAMSTKPanel,
    RAMSTKWorkView,
)

# RAMSTK Local Imports
from . import RevisionGeneralDataPanel, RevisionTreePanel


class RevisionModuleView(RAMSTKModuleView):
    """Display Revision attribute data in the RAMSTK Module Book.

    The Revision Module View displays all the Revisions associated with the
    connected RAMSTK Program in a flat list.  The attributes of a Revision
    Module View are:

    :cvar _tag: the name of the module.

    :ivar _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag: str = "revision"
    _tablabel: str = "Revision"
    _tabtooltip: str = _("Displays the list of Revisions for the open RAMSTK Project.")

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
        self.dic_pkeys["record_id"] = attributes["revision_id"]

    def __make_ui(self) -> None:
        """Build the user interface for the revision module view.

        :return: None
        """
        super().make_ui()

        self._pnlPanel.tvwTreeView.dic_handler_id[
            "button-press"
        ] = self._pnlPanel.tvwTreeView.connect(
            "button_press_event", super().on_button_press
        )


class RevisionWorkView(RAMSTKWorkView):
    """Display general Revision attribute data in the RAMSTK Work Book.

    The Revision Work View displays all the general data attributes for the
    selected Revision. The attributes of a Revision General Data Work View are:

    :cvar str _tag: the name of the module.
    :cvar str _tablabel: the text to display on the tab's label.
    :cvar str _tabtooltip: the text to display as the tab's tooltip.

    :ivar list _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar list _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar list _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar list _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag: str = "revision"
    _tablabel = _("General\nData")
    _tabtooltip = _("Displays general information for the selected Revision")

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Revision Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_tooltips: List[str] = [
            _("Save changes to the currently selected Revision."),
            _("Save changes to all Revisions."),
        ]

        # Initialize private scalar attributes.
        self._pnlGeneralData: RAMSTKPanel = RevisionGeneralDataPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, "selected_revision")

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the Revision's record ID.

        :param attributes: the attribute dict for the selected Revision.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["record_id"] = attributes["revision_id"]

    def __make_ui(self) -> None:
        """Build the user interface for the Revision General Data tab.

        :return: None
        :rtype: None
        """
        super().do_make_layout()

        self.pack_start(self._pnlGeneralData, True, True, 0)

        self.show_all()
