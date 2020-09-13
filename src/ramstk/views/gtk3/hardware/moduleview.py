# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.moduleview.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Hardware GTK3 module view."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (RAMSTKMessageDialog, RAMSTKModuleView,
                                       RAMSTKTreeView)


class ModuleView(RAMSTKModuleView):
    """
    Display Hardware attribute data in the RAMSTK Module Book.

    The Hardware Module View displays all the Hardware associated with the
    connected RAMSTK Program in a flat list.  All attributes of a Hardware
    Module View are inherited.
    """
    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module='hardware') -> None:
        """
        Initialize the Hardware Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger, module)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/hardware.png')
        self._dic_key_index = {
            'revision_id': 0,
            'hardware_id': 1,
            'alt_part_number': 2,
            'cage_code': 3,
            'comp_ref_des': 4,
            'cost': 5,
            'cost_failure': 6,
            'cost_hour': 7,
            'description': 8,
            'duty_cycle': 9,
            'figure_number': 10,
            'lcn': 11,
            'level': 12,
            'manufacturer_id': 13,
            'mission_time': 14,
            'name': 15,
            'nsn': 16,
            'page_number': 17,
            'parent_id': 18,
            'part': 19,
            'part_number': 20,
            'quantity': 21,
            'ref_des': 22,
            'remarks': 23,
            'repairable': 24,
            'specification_number': 25,
            'tagged_part': 26,
            'total_part_count': 27,
            'total_power_dissipation': 28,
            'year_of_manufacture': 29,
            'cost_type_id': 30,
            'attachments': 31,
            'category_id': 32,
            'subcategory_id': 33
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_insert_hardware, 'succeed_insert_hardware')
        pub.subscribe(self._on_module_switch, 'mvwSwitchedPage')

        pub.subscribe(self.do_load_tree, 'succeed_retrieve_hardware')
        pub.subscribe(self.do_refresh_tree, 'wvw_editing_hardware')
        pub.subscribe(self.do_set_cursor_active,
                      'succeed_calculate_hardware_2')
        pub.subscribe(self.do_set_cursor_active, 'succeed_delete_hardware')
        pub.subscribe(self.do_set_cursor_active, 'succeed_insert_hardware')
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_hardware')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_calculate_hardware')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_delete_hardware')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_insert_hardware')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_hardware')
        pub.subscribe(self.on_delete, 'succeed_delete_hardware')

    def __make_ui(self) -> None:
        """
        Build the user interface for the Hardware work stream module.

        :return: None
        :rtype: None
        """
        super().make_ui(icons=[
            'insert_sibling', 'insert_child', 'insert_part', 'remove',
            'calculate', 'calculate_all'
        ],
                        tooltips=[
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
                            _("Calculate the entire system.")
                        ],
                        callbacks=[
                            self._do_request_insert_sibling,
                            self._do_request_insert_child,
                            self._do_request_insert_part,
                            self._do_request_delete,
                            self._do_request_calculate_hardware,
                            self._do_request_calculate_all_hardware
                        ])

    def _do_request_calculate_hardware(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to calculate the selected hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_hardware', node_id=self._record_id)

    def _do_request_calculate_all_hardware(self,
                                           __button: Gtk.ToolButton) -> None:
        """
        Send request to iteratively calculate all hardware items.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_all_hardware')

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to delete selected record from the RAMSTKHardware table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
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

    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> Any:
        """
        Request to insert a new child assembly under the selected assembly.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_insert_hardware',
                        parent_id=self._record_id,
                        part=0)

    def _do_request_insert_part(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to insert a piece part to the selected Hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_insert_hardware',
                        parent_id=self._record_id,
                        part=1)

    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> Any:
        """
        Send request to insert a new sibling Hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_insert_hardware',
                        parent_id=self._parent_id,
                        part=0)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to update the selected record to the RAMSTKHardware table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_hardware', node_id=self._record_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to save all the records to the RAMSTKHardware table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_hardware')

    def _on_button_press(self, treeview: RAMSTKTreeView,
                         event: Gdk.Event) -> None:
        """
        Handle mouse clicks on the Hardware Module View RAMSTKTreeView().

        :param treeview: the Hardware class Gtk.TreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`
        :param event: the Gdk.Event() that called this method (the
            important attribute is which mouse button was clicked).
                * 1 = left
                * 2 = scrollwheel
                * 3 = right
                * 4 = forward
                * 5 = backward
                * 8 =
                * 9 =

        :type event: :class:`Gdk.Event`
        :return: None
        :rtype: None
        """
        treeview.handler_block(treeview.dic_handler_id['button-press'])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            super().on_button_press(
                event,
                icons=[
                    'insert_sibling', 'insert_child', 'insert_part',
                    'calculate', 'calculate_all'
                ],
                labels=[
                    _("Add Sibling Assembly"),
                    _("Add Child Assembly"),
                    _("Add Piece Part"),
                    _("Calculate the Selected Hardware"),
                    _("Calculate the System"),
                    _("Remove Selected Hardware Item"),
                    _("Save Selected Hardware Item"),
                    _("Save All Hardware Items")
                ],
                callbacks=[
                    self._do_request_insert_sibling,
                    self._do_request_insert_child,
                    self._do_request_insert_part,
                    self._do_request_calculate_hardware,
                    self._do_request_calculate_all_hardware,
                    self._do_request_delete, self._do_request_update,
                    self._do_request_update_all
                ])
        treeview.handler_unblock(treeview.dic_handler_id['button-press'])

    def _on_cell_edit(self, __cell: Gtk.CellRenderer, path: str, new_text: str,
                      position: int) -> None:
        """
        Handle edits of Hardware package Module View RAMSTKTreeview().

        This hardware sends a dict with it's message that relates the
        database field and the new data for that field.

            `package` key: `package` value

        corresponds to:

            database field name: new value

        The workview module listens for this message so it can update it's
        widgets.  Other modules may listen as well.

        :param __cell: the Gtk.CellRenderer() that was edited.
        :type __cell: :class:`Gtk.CellRenderer`
        :param str path: the Gtk.TreeView() path of the
            Gtk.CellRenderer() that was edited.
        :param str new_text: the new text in the edited
            Gtk.CellRenderer().
        :param int position: the column position of the edited
            Gtk.CellRenderer().
        :return: None
        :rtype: None
        """
        _dic_keys = {
            2: 'alt_part_number',
            3: 'cage_code',
            4: 'comp_ref_des',
            5: 'cost',
            8: 'description',
            9: 'duty_cycle',
            10: 'figure_number',
            11: 'lcn',
            14: 'mission_time',
            15: 'name',
            16: 'nsn',
            17: 'page_number',
            20: 'part_number',
            21: 'quantity',
            22: 'ref_des',
            23: 'remarks',
            25: 'specification_number',
            29: 'year_of_manufacture'
        }

        try:
            _key = _dic_keys[self._lst_col_order[position]]
        except KeyError:
            _key = ''

        self.treeview.do_edit_cell(__cell, path, new_text, position)

        pub.sendMessage('mvw_editing_hardware',
                        node_id=[self._record_id, -1, ''],
                        package={_key: new_text})

    def _on_insert_hardware(self, node_id: int, tree: treelib.Tree) -> None:
        """
        Add row to module view for newly added hardware.

        :param int node_id: the ID of the newly added hardware.
        :param tree: the treelib Tree() containing the work stream module's
            data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _data = tree.get_node(node_id).data['hardware'].get_attributes()
        self._parent_id = _data['parent_id']
        super().on_insert(_data)

    def _on_module_switch(self, module: str = '') -> None:
        """
        Set the Module Book title when the Hardware module is selected.

        :param str module: the name of the module just selected.
        :return: None
        """
        _model, _row = self.treeview.selection.get_selected()

        if module == 'hardware' and _row is not None:
            _code = _model.get_value(_row, self._lst_col_order[5])
            _name = _model.get_value(_row, self._lst_col_order[15])
            _title = _("Analyzing Hardware {0:s}: {1:s}").format(
                str(_code), str(_name))

            pub.sendMessage('request_set_title', title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """
        Handle events for the Hardware package Module View RAMSTKTreeView().

        This method is called whenever a Hardware Module View RAMSTKTreeView()
        row is activated/changed.

        :param selection: the Hardware class Gtk.TreeSelection().
        :type selection: :class:`Gtk.TreeSelection`
        :return: None
        :rtype: None
        """
        selection.handler_block(self.treeview.dic_handler_id['changed'])

        _attributes: Dict[str, Any] = super().on_row_change(selection)

        if _attributes:
            self._parent_id = _attributes['parent_id']

            _title = _("Analyzing Hardware {0:s}: {1:s}").format(
                str(_attributes['comp_ref_des']), str(_attributes['name']))

            pub.sendMessage('selected_hardware', attributes=_attributes)
            pub.sendMessage('request_get_all_hardware_attributes',
                            node_id=self._record_id)
            pub.sendMessage('request_set_title', title=_title)

        selection.handler_unblock(self.treeview.dic_handler_id['changed'])
