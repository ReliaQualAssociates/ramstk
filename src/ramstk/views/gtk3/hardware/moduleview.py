# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.moduleview.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Hardware GTK3 module view."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKMessageDialog, RAMSTKModuleView, RAMSTKPanel
)

# RAMSTK Local Imports
from . import ATTRIBUTE_KEYS


class HardwarePanel(RAMSTKPanel):
    """Panel to display hierarchy of hardware."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Hardware panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = ATTRIBUTE_KEYS
        self._dic_attribute_updater = {
            'revision_id': [None, 'edited', 0, 33],
            'hardware_id': [None, 'edited', 1, 33],
            'alt_part_number': [None, 'edited', 2, 33],
            'cage_code': [None, 'edited', 3, 33],
            'comp_ref_des': [None, 'edited', 4, 33],
            'cost': [None, 'edited', 5, 33],
            'cost_failure': [None, 'edited', 6, 33],
            'cost_hour': [None, 'edited', 7, 33],
            'description': [None, 'edited', 8, 33],
            'duty_cycle': [None, 'edited', 9, 33],
            'figure_number': [None, 'edited', 10, 33],
            'lcn': [None, 'edited', 11, 33],
            'level': [None, 'edited', 12, 33],
            'manufacturer_id': [None, 'edited', 13, 33],
            'mission_time': [None, 'edited', 14, 33],
            'name': [None, 'edited', 15, 33],
            'nsn': [None, 'edited', 16, 33],
            'page_number': [None, 'edited', 17, 33],
            'parent_id': [None, 'edited', 18, 33],
            'part': [None, 'toggled', 19, 33],
            'part_number': [None, 'edited', 20, 33],
            'quantity': [None, 'edited', 21, 33],
            'ref_des': [None, 'edited', 22, 33],
            'remarks': [None, 'edited', 23, 33],
            'repairable': [None, 'toggled', 24, 33],
            'specification_number': [None, 'edited', 25, 33],
            'tagged_part': [None, 'toggled', 26, 33],
            'total_part_count': [None, 'edited', 27, 33],
            'total_power_dissipation': [None, 'edited', 28, 33],
            'year_of_manufacture': [None, 'edited', 29, 33],
            'cost_type_id': [None, 'edited', 30, 33],
            'attachments': [None, 'edited', 31, 33],
            'category_id': [None, 'edited', 32, 33],
            'subcategory_id': [None, 'edited', 33],
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._title = _("Hardware BoM")

        # Initialize public dictionary class attributes.

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_make_panel_treeview()
        self.__do_set_properties()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_tree, 'succeed_retrieve_hardware')
        pub.subscribe(super().do_refresh_tree, 'wvw_editing_hardware')
        pub.subscribe(super().on_delete, 'succeed_delete_hardware')

        pub.subscribe(self._on_module_switch, 'mvwSwitchedPage')

    def _on_module_switch(self, module: str = '') -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == 'hardware' and _row is not None:
            _code = _model.get_value(_row, self._lst_col_order[5])
            _name = _model.get_value(_row, self._lst_col_order[15])
            _title = _("Analyzing Hardware item {0:s}: {1:s}").format(
                str(_code), str(_name))

            pub.sendMessage('request_set_title', title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Hardware package Module View RAMSTKTreeView().

        This method is called whenever a Hardware Module View RAMSTKTreeView()
        row is activated/changed.

        :param selection: the Hardware class Gtk.TreeSelection().
        :return: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes['hardware_id']
            self._parent_id = _attributes['parent_id']

            _title = _("Analyzing Hardware item {0:s}: {1:s}").format(
                str(_attributes['comp_ref_des']), str(_attributes['name']))

            pub.sendMessage('selected_hardware', attributes=_attributes)
            pub.sendMessage('request_get_all_hardware_attributes',
                            node_id=self._record_id)
            pub.sendMessage('request_set_title', title=_title)

    def __do_set_properties(self) -> None:
        """Set common properties of the ModuleView and widgets.

        :return: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        self.tvwTreeView.set_tooltip_text(
            _("Displays the hierarchical list of hardware."))


class ModuleView(RAMSTKModuleView):
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
    _module: str = 'hardware'
    _tablabel: str = 'Hardware'
    _tabtooltip: str = _("Displays the hardware hierarchy (BoM) for the "
                         "selected Revision.")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Hardware Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/hardware.png')

        # Initialize private list attributes.
        self._lst_callbacks.insert(1, self._do_request_insert_child)
        self._lst_callbacks.insert(2, self._do_request_insert_part)
        self._lst_callbacks.insert(4, self._do_request_calculate_hardware)
        self._lst_callbacks.insert(5, self._do_request_calculate_all_hardware)
        self._lst_icons[0] = 'insert_sibling'
        self._lst_icons.insert(1, 'insert_child')
        self._lst_icons.insert(2, 'insert_part')
        self._lst_icons.insert(4, 'calculate')
        self._lst_icons.insert(5, 'calculate_all')
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
            _("Adds a new Hardware assembly at the same "
              "hierarchy level as the selected Hardware "
              "(i.e., a sibling hardware item)."),
            _("Adds a new Hardware assembly one level "
              "subordinate to the selected Hardware (i.e., a "
              "child hardware item)."),
            _("Adds a new hardware component/piece-part "
              "to the the selected hardware assembly."),
            _("Remove the currently selected hardware item "
              "and any children."),
            _("Calculate the selected hardware item."),
            _("Calculate the entire system."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = HardwarePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().make_ui()
        self._pnlPanel.do_set_cell_callbacks('mvw_editing_hardware', [
            2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33
        ])

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_insert_hardware, 'succeed_insert_hardware')

    def do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete selected record from the RAMSTKHardware table.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent(
        ).get_parent()
        _prompt = _("You are about to delete Hardware {0:d} and all "
                    "data associated with it.  Is this really what "
                    "you want to do?").format(self._record_id)
        _dialog = RAMSTKMessageDialog(parent=_parent)
        _dialog.do_set_message(_prompt)
        _dialog.do_set_message_type('question')

        if _dialog.do_run() == Gtk.ResponseType.YES:
            pub.sendMessage('request_delete_hardware', node_id=self._record_id)

        _dialog.do_destroy()

    def _do_request_calculate_hardware(self, __button: Gtk.ToolButton) -> None:
        """Send request to calculate the selected hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_hardware', node_id=self._record_id)

    def _do_request_calculate_all_hardware(self,
                                           __button: Gtk.ToolButton) -> None:
        """Send request to iteratively calculate all hardware items.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_all_hardware')

    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> Any:
        """Request to insert a new child assembly under the selected assembly.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_insert_hardware',
                        parent_id=self._record_id,
                        part=0)

    def _do_request_insert_part(self, __button: Gtk.ToolButton) -> None:
        """Send request to insert a piece part to the selected Hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_insert_hardware',
                        parent_id=self._record_id,
                        part=1)

    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> Any:
        """Send request to insert a new sibling Hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_insert_hardware',
                        parent_id=self._parent_id,
                        part=0)

    def _on_insert_hardware(self, node_id: int, tree: treelib.Tree) -> None:
        """Add row to module view for newly added hardware.

        :param node_id: the ID of the newly added hardware.
        :param tree: the treelib Tree() containing the work stream module's
            data.
        :return: None
        """
        _data = tree.get_node(node_id).data['hardware'].get_attributes()
        self._pnlPanel.on_insert(_data)
