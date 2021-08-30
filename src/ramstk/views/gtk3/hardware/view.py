# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.iew.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Hardware Views."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKModuleView

# RAMSTK Local Imports
from . import HardwareTreePanel


class HardwareModuleView(RAMSTKModuleView):
    """Display Hardware attribute data in the RAMSTK Module Book.

    The Hardware Module View displays all the Hardware associated with the
    connected RAMSTK Program in a flat list.  The attributes of a Hardware
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
    _module: str = "hardware"
    _tablabel: str = "Hardware"
    _tabtooltip: str = _(
        "Displays the hardware hierarchy (BoM) for the " "selected Revision."
    )

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Hardware Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_icons["tab"] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + "/32x32/hardware.png"
        )

        # Initialize private list attributes.
        self._lst_callbacks[0] = self._do_request_insert_sibling
        self._lst_callbacks.insert(1, self._do_request_insert_child)
        self._lst_callbacks.insert(2, self._do_request_insert_part)
        self._lst_callbacks.insert(4, self._do_request_calculate_hardware)
        self._lst_callbacks.insert(5, self._do_request_calculate_all_hardware)
        self._lst_icons[0] = "insert_sibling"
        self._lst_icons.insert(1, "insert_child")
        self._lst_icons.insert(2, "insert_part")
        self._lst_icons.insert(4, "calculate")
        self._lst_icons.insert(5, "calculate_all")
        self._lst_mnu_labels: List[str] = [
            _("Add Sibling Assembly"),
            _("Add Child Assembly"),
            _("Add Piece Part"),
            _("Delete Selected"),
            _("Calculate the Selected"),
            _("Calculate the System"),
            _("Save Selected Hardware"),
            _("Save All Hardware"),
        ]
        self._lst_tooltips: List[str] = [
            _(
                "Adds a new hardware assembly at the same "
                "hierarchy level as the selected hardware item "
                "(i.e., a sibling hardware item)."
            ),
            _(
                "Adds a new hardware assembly one level "
                "subordinate to the selected hardware item (i.e., a "
                "child hardware item)."
            ),
            _(
                "Adds a new hardware component/piece-part "
                "to the the selected hardware assembly."
            ),
            _("Remove the currently selected hardware item " "and any children."),
            _("Calculate the selected hardware item and all of it's " "children."),
            _("Calculate the entire system."),
            _("Save changes to the selected hardware item."),
            _("Save changes to the entire system."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = HardwareTreePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, "selected_{0}".format(self._module))

    def _do_request_calculate_hardware(self, __button: Gtk.ToolButton) -> None:
        """Send request to calculate the selected hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage(
            "request_calculate_hardware",
            node_id=self._record_id,
        )

    def _do_request_calculate_all_hardware(self, __button: Gtk.ToolButton) -> None:
        """Send request to iteratively calculate all hardware items.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage(
            "request_calculate_hardware",
            node_id=1,
        )

    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> Any:
        """Request to insert a new child assembly under the selected assembly.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage(
            "request_insert_hardware",
            parent_id=self._record_id,
            part=0,
        )

    def _do_request_insert_part(self, __button: Gtk.ToolButton) -> None:
        """Send request to insert a piece part to the selected Hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage("request_insert_hardware", parent_id=self._record_id, part=1)

    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> Any:
        """Send request to insert a new sibling Hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        print("Insert sibling of {1} for {0}".format(self._parent_id, self._record_id))
        pub.sendMessage("request_insert_hardware", parent_id=self._parent_id, part=0)

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the work stream module's record ID and, if any, parent ID.

        :param attributes: the attributes dict for the selected work stream
            module item.
        :return: None
        :rtype: None
        """
        self._record_id = attributes["hardware_id"]
        self._parent_id = attributes["parent_id"]

    def __make_ui(self) -> None:
        """Build the user interface for the function module view.

        :return: None
        """
        super().make_ui()

        self._pnlPanel.do_set_properties()
        self._pnlPanel.do_set_callbacks()
        self._pnlPanel.do_set_cell_callbacks(
            "mvw_editing_hardware",
            [
                2,
                3,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
                25,
                26,
                27,
                28,
                29,
                30,
                31,
                32,
                33,
            ],
        )
        self._pnlPanel.tvwTreeView.dic_handler_id[
            "button-press"
        ] = self._pnlPanel.tvwTreeView.connect(
            "button_press_event", super().on_button_press
        )
        for _element in ["assembly", "part"]:
            self._pnlPanel.dic_icons[_element] = self._dic_icons[_element]
