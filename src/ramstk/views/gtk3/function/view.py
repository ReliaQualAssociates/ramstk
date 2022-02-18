# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.function.view.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Function Views."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKModuleView, RAMSTKPanel, RAMSTKWorkView

# RAMSTK Local Imports
from . import FunctionGeneralDataPanel, FunctionTreePanel


class FunctionModuleView(RAMSTKModuleView):
    """Display Function attribute data in the RAMSTK Module Book.

    The Function Module View displays all the Functions associated with the
    connected RAMSTK Program in a flat list.  The attributes of a Function
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
    _tag: str = "function"
    _tablabel: str = "Function"
    _tabtooltip: str = _("Displays the functional hierarchy for the selected Revision.")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Function Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_icons["tab"] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + "/32x32/function.png"
        )

        # Initialize private list attributes.
        self._lst_callbacks.insert(1, super().do_request_insert_child)
        self._lst_icons[0] = "insert_sibling"
        self._lst_icons.insert(1, "insert_child")
        self._lst_mnu_labels = [
            _("Add Sibling Function"),
            _("Add Child Function"),
            _("Delete Selected Function"),
            _("Save Selected Function"),
            _("Save All Functions"),
        ]
        self._lst_tooltips = [
            _("Add a new sibling function."),
            _("Add a new child function."),
            _("Delete the currently selected function."),
            _("Save changes to the currently selected function."),
            _("Save changes to all functions."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = FunctionTreePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, f"selected_{self._tag}")

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the stakeholder input's record ID.

        :param attributes: the attributes dict for the selected function.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["revision_id"] = attributes["revision_id"]
        self.dic_pkeys["function_id"] = attributes["function_id"]
        self.dic_pkeys["parent_id"] = attributes["parent_id"]
        self.dic_pkeys["record_id"] = attributes["function_id"]

    def __make_ui(self) -> None:
        """Build the user interface for the function module view.

        :return: None
        """
        super().make_ui()

        self._pnlPanel.tvwTreeView.dic_handler_id[
            "button-press"
        ] = self._pnlPanel.tvwTreeView.connect(
            "button_press_event", super().on_button_press
        )


class FunctionWorkView(RAMSTKWorkView):
    """Display general Function attribute data in the RAMSTK Work Book.

    The Function Work View displays all the general data attributes for the
    selected Function. The attributes of a Function General Data Work View are:

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
    _tag: str = "function"
    _tablabel = _("General\nData")
    _tabtooltip = _("Displays general information for the selected Function.")

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Function Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_mnu_labels = [
            _("Save Selected Function"),
            _("Save All Functions"),
        ]
        self._lst_tooltips = [
            _("Save changes to the currently selected function."),
            _("Save changes to all functions."),
        ]

        # Initialize private scalar attributes.
        self._pnlGeneralData: RAMSTKPanel = FunctionGeneralDataPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, "selected_function")

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the stakeholder input's record ID.

        :param attributes: the attributes dict for the selected stakeholder
            input.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["parent_id"] = attributes["parent_id"]
        self.dic_pkeys["record_id"] = attributes["function_id"]

    def __make_ui(self) -> None:
        """Build the user interface for the Function General Data tab.

        :return: None
        :rtype: None
        """
        super().do_make_layout()

        self.pack_end(self._pnlGeneralData, True, True, 0)
        self.show_all()
