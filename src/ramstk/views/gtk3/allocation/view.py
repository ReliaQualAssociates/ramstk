# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.allocation.view.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Allocation Views."""

# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKPanel, RAMSTKWorkView

# RAMSTK Local Imports
from . import AllocationGoalMethodPanel, AllocationTreePanel


class AllocationWorkView(RAMSTKWorkView):
    """Display Allocation attribute data in the RAMSTK Work Book.

    The Allocation Work View displays all the allocation data attributes for
    the selected hardware item. The attributes of an Allocation General Data
    Work View are:

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

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag: str = "allocation"
    _tablabel: str = _("Allocation")
    _tabtooltip: str = _(
        "Displays the Allocation analysis for the selected hardware item."
    )

    # Define public dictionary class attributes.

    # Define public dictionary list attributes.

    # Define public dictionary scalar attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Allocation Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks.insert(0, self._do_request_calculate)
        self._lst_icons.insert(0, "calculate")
        self._lst_mnu_labels.insert(0, _("Calculate"))
        self._lst_tooltips = [
            _("Calculate the currently selected Allocation line item."),
            _("Save changes to the currently selected Allocation line item."),
            _("Save changes to all Allocation line items."),
        ]

        # Initialize private scalar attributes.
        self._pnlGoalMethods: RAMSTKPanel = AllocationGoalMethodPanel()
        self._pnlPanel: RAMSTKPanel = AllocationTreePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, "selected_hardware")

    def _do_set_record_id(self, attributes: Dict[str, Union[float, int, str]]) -> None:
        """Set the allocation's record ID.

        :param attributes: the attribute dict for the selected allocation
            record.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["parent_id"] = attributes["parent_id"]
        self.dic_pkeys["record_id"] = attributes["hardware_id"]

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Calculate the Allocation reliability metrics.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        if self._pnlGoalMethods.method_id == 1:  # Equal
            pub.sendMessage(
                "request_calculate_equal_allocation",
                node_id=self.dic_pkeys["record_id"],
            )
        elif self._pnlGoalMethods.method_id == 2:  # AGREE
            pub.sendMessage(
                "request_calculate_agree_allocation",
                node_id=self.dic_pkeys["record_id"],
            )
        elif self._pnlGoalMethods.method_id == 3:  # ARINC
            pub.sendMessage(
                "request_calculate_arinc_allocation",
                node_id=self.dic_pkeys["record_id"],
            )
        elif self._pnlGoalMethods.method_id == 4:  # FOO
            pub.sendMessage(
                "request_calculate_foo_allocation",
                node_id=self.dic_pkeys["record_id"],
            )

    def __make_ui(self) -> None:
        """Build the user interface for the allocation tab.

        :return: None
        :rtype: None
        """
        _hpaned: Gtk.HPaned = super().do_make_layout_lr()

        self._pnlGoalMethods.fmt = self.fmt
        self._pnlGoalMethods.do_load_comboboxes()

        super().do_embed_treeview_panel()

        self.remove(self.get_children()[-1])
        _hpaned.pack1(self._pnlGoalMethods, True, True)
        _hpaned.pack2(self._pnlPanel, True, True)

        self.show_all()
