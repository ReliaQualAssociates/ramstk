# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.moduleview.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Requirement GTK3 module view."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKMessageDialog, RAMSTKModuleView, RAMSTKTreeView
)


class ModuleView(RAMSTKModuleView):
    """
    Display Requirement attribute data in the RAMSTK Module Book.

    The Requirement Module View displays all the Requirements associated with
    the connected RAMSTK Program in a flat list.  All attributes of a
    Requirement Module View are inherited.
    """
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager, module='requirement') -> None:
        """
        Initialize the Requirement Module View.

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
            + '/32x32/requirement.png')
        self._dic_key_index = {
            'requirement_id': 1,
            'derived': 2,
            'description': 3,
            'figure_number': 4,
            'owner': 5,
            'page_number': 6,
            'parent_id': 7,
            'priority': 8,
            'requirement_code': 9,
            'specification': 10,
            'requirement_type': 11,
            'validated': 12,
            'validated_date': 13,
            'q_clarity_0': 14,
            'q_clarity_1': 15,
            'q_clarity_2': 16,
            'q_clarity_3': 17,
            'q_clarity_4': 18,
            'q_clarity_5': 19,
            'q_clarity_6': 20,
            'q_clarity_7': 21,
            'q_clarity_8': 22,
            'q_complete_0': 23,
            'q_complete_1': 24,
            'q_complete_2': 25,
            'q_complete_3': 26,
            'q_complete_4': 27,
            'q_complete_5': 28,
            'q_complete_6': 29,
            'q_complete_7': 30,
            'q_complete_8': 31,
            'q_complete_9': 32,
            'q_consistent_0': 33,
            'q_consistent_1': 34,
            'q_consistent_2': 35,
            'q_consistent_3': 36,
            'q_consistent_4': 37,
            'q_consistent_5': 38,
            'q_consistent_6': 39,
            'q_consistent_7': 40,
            'q_consistent_8': 41,
            'q_verifiable_0': 42,
            'q_verifiable_1': 43,
            'q_verifiable_2': 44,
            'q_verifiable_3': 45,
            'q_verifiable_4': 46,
            'q_verifiable_5': 47
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_delete, 'succeed_delete_requirement')
        pub.subscribe(self._on_insert, 'succeed_insert_requirement')
        pub.subscribe(self.do_load_tree, 'succeed_retrieve_requirements')
        pub.subscribe(self._do_refresh_tree, 'wvw_editing_requirement')
        pub.subscribe(self._on_module_switch, 'mvwSwitchedPage')

    def __make_ui(self) -> None:
        """
        Build the user interface for the Requirement work stream module.

        :return: None
        :rtype: None
        """
        super().make_ui(icons=['insert_sibling', 'insert_child', 'remove'],
                        tooltips=[
                            _("Add a new sibling requirement."),
                            _("Add a new child requirement."),
                            _("Remove the currently selected requirement.")
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

        This method is called by other views when the Requirement data model
        attributes are edited via their gtk.Widgets().

        :param list node_id: unused in this method.
        :param dict package: the key:value for the data being updated.
        :return: None
        :rtype: None
        """
        self.do_refresh_tree(package, self._dic_key_index)

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """
        Request to delete selected record from the RAMSTKRequirement table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent(
        ).get_parent()
        _prompt = _("You are about to delete Requirement {0:d} and all "
                    "data associated with it.  Is this really what "
                    "you want to do?").format(self._record_id)
        _dialog = RAMSTKMessageDialog(_prompt,
                                      self._dic_icons['question'],
                                      'question',
                                      parent=_parent)
        _response = _dialog.do_run()

        if _response == Gtk.ResponseType.YES:
            pub.sendMessage('request_delete_requirement',
                            node_id=self._record_id)

        _dialog.do_destroy()

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to update the selected record to the RAMSTKRequirement table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_requirement',
                        node_id=self._record_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to save all the records to the RAMSTKRequirement table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_requirements')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _on_button_press(self, treeview: RAMSTKTreeView,
                         event: Gdk.Event) -> None:
        """
        Handle mouse clicks on the Requirement Module View RAMSTKTreeView().

        :param treeview: the Requirement class Gtk.TreeView().
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
        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            super().on_button_press(event,
                                    icons=['insert_sibling', 'insert_child'],
                                    labels=[
                                        _("Add Sibling Requirement"),
                                        _("Add Child Requirement"),
                                        _("Remove Selected Requirement"),
                                        _("Save Selected Requirement"),
                                        _("Save All Requirements")
                                    ],
                                    callbacks=[
                                        self.do_request_insert_sibling,
                                        self.do_request_insert_child
                                    ])

        treeview.handler_unblock(self._lst_handler_id[1])

    def _on_cell_edit(self, __cell: Gtk.CellRenderer, path: str, new_text: str,
                      position: int) -> None:
        """
        Handle edits of Requirement package Module View RAMSTKTreeview().

        This requirement sends a dict with it's message that relates the
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
        _dic_keys = {5: 'requirement_code', 15: 'name', 17: 'remarks'}
        try:
            _key = _dic_keys[self._lst_col_order[position]]
        except KeyError:
            _key = ''

        self.treeview.do_edit_cell(__cell, path, new_text, position)

        pub.sendMessage('mvw_editing_requirement',
                        node_id=[self._record_id, -1, ''],
                        package={_key: new_text})

    def _on_insert(self, node_id: int, tree: treelib.Tree) -> None:
        """
        Add row to module view for newly added requirement.

        :param int node_id: the ID of the newly added requirement.
        :param tree: the treelib Tree() containing the work stream module's
            data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _data = tree.get_node(node_id).data['requirement'].get_attributes()
        super().on_insert(_data)

    def _on_module_switch(self, module: str = '') -> None:
        """

        :param module:
        :return:
        """
        _model, _row = self.treeview.selection.get_selected()

        if module == 'requirement' and _row is not None:
            _code = _model.get_value(_row, self._lst_col_order[5])
            _name = _model.get_value(_row, self._lst_col_order[15])
            _title = _("Analyzing Requirement {0:s}: {1:s}").format(
                str(_code), str(_name))

            pub.sendMessage('request_set_title', title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """
        Handle events for the Requirement package Module View RAMSTKTreeView().

        This method is called whenever a Requirement Module View
        RAMSTKTreeView() row is activated/changed.

        :param selection: the Requirement class Gtk.TreeSelection().
        :type selection: :class:`Gtk.TreeSelection`
        :return: None
        :rtype: None
        """
        _model, _row = selection.get_selected()
        _attributes: Dict[str, Any] = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes['requirement_id']
            self._parent_id = _attributes['parent_id']

            _prow = _model.iter_parent(_row)
            if _prow is not None:
                self._parent_id = self._record_id
            else:
                self._parent_id = 0

            _title = _("Analyzing {0:s} Requirement: {1:s}").format(
                str(_attributes['requirement_type']),
                str(_attributes['requirement_code']))

            pub.sendMessage('selected_requirement', attributes=_attributes)
            pub.sendMessage('request_get_requirement_attributes',
                            node_id=self._record_id,
                            table='requirement')
            pub.sendMessage('request_set_title', title=_title)

        selection.handler_unblock(self._lst_handler_id[0])
