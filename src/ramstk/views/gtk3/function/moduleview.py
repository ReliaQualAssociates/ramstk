# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.function.moduleview.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Function GTK3 module view."""

# Standard Library Imports
from typing import Any, Dict, List

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
    Display Function attribute data in the RAMSTK Module Book.

    The Function Module View displays all the Functions associated with the
    connected RAMSTK Program in a flat list.  All attributes of a Function
    Module View are inherited.
    """
    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module='function') -> None:
        """
        Initialize the Function Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
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
            + '/32x32/function.png')
        self._dic_key_index = {
            'revision_id': 0,
            'function_id': 1,
            'availability_logistics': 2,
            'availability_mission': 3,
            'cost': 4,
            'function_code': 5,
            'failure_rate_logistics': 6,
            'failure_rate_mission': 7,
            'level': 8,
            'mmt': 9,
            'mcmt': 10,
            'mpmt': 11,
            'mtbf_logistics': 12,
            'mtbf_mission': 13,
            'mttr': 14,
            'name': 15,
            'parent_id': 16,
            'remarks': 17,
            'safety_critical': 18,
            'total_mode_count': 19,
            'total_part_count': 20,
            'type': 21
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_delete, 'succeed_delete_function')
        pub.subscribe(self._on_insert, 'succeed_insert_function')
        pub.subscribe(self.do_load_tree, 'succeed_retrieve_functions')
        pub.subscribe(self._do_refresh_tree, 'wvw_editing_function')
        pub.subscribe(self._on_module_switch, 'mvwSwitchedPage')

    def __make_ui(self) -> None:
        """
        Build the user interface for the Function work stream module.

        :return: None
        :rtype: None
        """
        super().make_ui(icons=['insert_sibling', 'insert_child', 'remove'],
                        tooltips=[
                            _("Add a new sibling function."),
                            _("Add a new child function."),
                            _("Remove the currently selected function.")
                        ],
                        callbacks=[
                            self.do_request_insert_sibling,
                            self.do_request_insert_child,
                            self._do_request_delete
                        ])

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _do_refresh_tree(self, node_id: List, package: Dict) -> None:
        """
        Update the module view RAMSTKTreeView() with attribute changes.

        This method is called by other views when the Function data model
        attributes are edited via their gtk.Widgets().

        :param list node_id: unused in this method.
        :param dict package: the key:value for the data being updated.
        :return: None
        :rtype: None
        """
        self.do_refresh_tree(package, {
            'function_code': 5,
            'name': 15,
            'remarks': 17,
            'safety_critical': 18
        })

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to delete selected record from the RAMSTKFunction table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent(
        ).get_parent()
        _prompt = _("You are about to delete Function {0:d} and all "
                    "data associated with it.  Is this really what "
                    "you want to do?").format(self._record_id)
        _dialog = RAMSTKMessageDialog(_prompt,
                                      self._dic_icons['question'],
                                      'question',
                                      parent=_parent)
        _response = _dialog.do_run()

        if _response == Gtk.ResponseType.YES:
            pub.sendMessage('request_delete_function', node_id=self._record_id)

        _dialog.do_destroy()

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to update the selected record to the RAMSTKFunction table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_function', node_id=self._record_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to save all the records to the RAMSTKFunction table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_functions')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _on_button_press(self, treeview: RAMSTKTreeView,
                         event: Gdk.Event) -> None:
        """
        Handle mouse clicks on the Function Module View RAMSTKTreeView().

        :param treeview: the Function class Gtk.TreeView().
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
            super().on_button_press(event,
                                    icons=['insert_sibling', 'insert_child'],
                                    labels=[
                                        _("Add Sibling Function"),
                                        _("Add Child Function"),
                                        _("Remove Selected Function"),
                                        _("Save Selected Function"),
                                        _("Save All Functions")
                                    ],
                                    callbacks=[
                                        self.do_request_insert_sibling,
                                        self.do_request_insert_child
                                    ])

        treeview.handler_unblock(treeview.dic_handler_id['button-press'])

    def _on_cell_edit(self, __cell: Gtk.CellRenderer, path: str, new_text: str,
                      position: int) -> None:
        """
        Handle edits of Function package Module View RAMSTKTreeview().

        This function sends a dict with it's message that relates the
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
        _dic_keys = {5: 'function_code', 15: 'name', 17: 'remarks'}
        try:
            _key = _dic_keys[self._lst_col_order[position]]
        except KeyError:
            _key = ''

        self.treeview.do_edit_cell(__cell, path, new_text, position)

        pub.sendMessage('mvw_editing_function',
                        node_id=[self._record_id, -1, ''],
                        package={_key: new_text})

    def _on_insert(self, node_id: int, tree: treelib.Tree) -> None:
        """
        Add row to module view for newly added function.

        :param int node_id: the ID of the newly added function.
        :param tree: the treelib Tree() containing the work stream module's
            data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _data = tree.get_node(node_id).data['function'].get_attributes()
        super().on_insert(_data)

    def _on_module_switch(self, module: str = '') -> None:
        """

        :param module:
        :return:
        """
        _model, _row = self.treeview.selection.get_selected()

        if module == 'function' and _row is not None:
            _code = _model.get_value(_row, self._lst_col_order[5])
            _name = _model.get_value(_row, self._lst_col_order[15])
            _title = _("Analyzing Function {0:s}: {1:s}").format(
                str(_code), str(_name))

            pub.sendMessage('request_set_title', title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """
        Handle events for the Function package Module View RAMSTKTreeView().

        This method is called whenever a Function Module View RAMSTKTreeView()
        row is activated/changed.

        :param selection: the Function class Gtk.TreeSelection().
        :type selection: :class:`Gtk.TreeSelection`
        :return: None
        :rtype: None
        """
        _model, _row = selection.get_selected()
        _attributes: Dict[str, Any] = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes['function_id']
            self._parent_id = _attributes['parent_id']

            _prow = _model.iter_parent(_row)
            if _prow is not None:
                self._parent_id = self._record_id
            else:
                self._parent_id = 0

            _title = _("Analyzing Function {0:s}: {1:s}").format(
                str(_attributes['function_code']), str(_attributes['name']))

            pub.sendMessage('selected_function', attributes=_attributes)
            pub.sendMessage('request_get_function_attributes',
                            node_id=self._record_id,
                            table='hazards')
            pub.sendMessage('request_set_title', title=_title)

        selection.handler_unblock(self._lst_handler_id[0])
