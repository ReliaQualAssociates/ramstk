# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.validation.moduleview.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Validation GTK3 module view."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKMessageDialog, RAMSTKModuleView


class ModuleView(RAMSTKModuleView):
    """
    Display Validation attribute data in the RAMSTK Module Book.

    The Validation Module View displays all the Validations associated with the
    connected RAMSTK Program in a flat list.  All attributes of a Validation
    Module View are inherited.
    """
    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module='validation') -> None:
        """
        Initialize the Validation Module View.

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
            + '/32x32/validation.png')
        self._dic_key_index = {
            'revision_id': 0,
            'validation_id': 1,
            'description': 2,
            'task_type': 3,
            'task_specification': 4,
            'measurement_unit': 5,
            'acceptable_minimum': 6,
            'acceptable_mean': 7,
            'acceptable_maximum': 8,
            'acceptable_variance': 9,
            'date_start': 10,
            'date_end': 11,
            'status': 12,
            'time_minimum': 13,
            'time_average': 14,
            'time_maximum': 15,
            'cost_minimum': 18,
            'cost_average': 19,
            'cost_maximum': 20,
            'confidence': 23,
            'time_ll': 24,
            'time_mean': 25,
            'time_ul': 26,
            'time_variance': 27,
            'cost_ll': 28,
            'cost_mean': 29,
            'cost_ul': 30,
            'cost_variance': 31,
            'name': 32
        }

        # Initialize private list attributes.
        self._lst_callbacks = [
            self.do_request_insert_sibling, self._do_request_delete,
            self._do_request_update, self._do_request_update_all
        ]
        self._lst_icons = ['add', 'remove', 'save', 'save-all']
        self._lst_mnu_labels = [
            _("Add Task"),
            _("Delete Selected Task"),
            _("Save Selected Task"),
            _("Save All Tasks")
        ]
        self._lst_tooltips = [
            _("Add a new validation task."),
            _("Remove the currently selected validation task."),
            _("Save changes to the currently selected validation task."),
            _("Save changes to all validation tasks.")
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_insert, 'succeed_insert_validation')
        pub.subscribe(self._on_module_switch, 'mvwSwitchedPage')

        pub.subscribe(self.do_load_tree, 'succeed_retrieve_validations')
        pub.subscribe(self.do_refresh_tree, 'wvw_editing_validation')
        pub.subscribe(self.do_set_cursor_active, 'succeed_delete_validation_2')
        pub.subscribe(self.do_set_cursor_active, 'succeed_insert_validation_2')
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_validation')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_delete_validation')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_insert_validation')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_validation')
        pub.subscribe(self.on_delete, 'succeed_delete_validation')

    def __make_ui(self) -> None:
        """
        Build the user interface for the Validation work stream module.

        :return: None
        :rtype: None
        """
        super().make_ui(icons=self._lst_icons,
                        tooltips=self._lst_tooltips,
                        callbacks=self._lst_callbacks)

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to delete selected record from the RAMSTKValidation table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent(
        ).get_parent()
        _prompt = _("You are about to delete Validation {0:d} and all "
                    "data associated with it.  Is this really what "
                    "you want to do?").format(self._record_id)
        _dialog = RAMSTKMessageDialog(parent=_parent)
        _dialog.do_set_message(_prompt)
        _dialog.do_set_message_type('question')

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage('request_delete_validation',
                            node_id=self._record_id)

        _dialog.do_destroy()

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to update the selected record to the RAMSTKValidation table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_validation', node_id=self._record_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to save all the records to the RAMSTKValidation table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_validations')

    def _on_cell_edit(self, __cell: Gtk.CellRenderer, path: str, new_text: str,
                      position: int) -> None:
        """
        Handle edits of Validation package Module View RAMSTKTreeview().

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
        _dic_keys = {17: 'name', 20: 'remarks', 22: 'validation_code'}
        try:
            _key = _dic_keys[self._lst_col_order[position]]
        except KeyError:
            _key = ''

        self.treeview.do_edit_cell(__cell, path, new_text, position)

        pub.sendMessage('mvw_editing_validation',
                        node_id=[self._record_id, -1, ''],
                        package={_key: new_text})

    def _on_insert(self, node_id: int, tree: treelib.Tree) -> None:
        """
        Add row to module view for newly added validation.

        :param int node_id: the ID of the newly added validation.
        :param tree: the treelib Tree() containing the work stream module's
            data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        super().on_insert(
            tree.get_node(node_id).data['validation'].get_attributes())

    def _on_module_switch(self, module: str = '') -> None:
        """

        :param module:
        :return:
        """
        _model, _row = self.treeview.selection.get_selected()

        if module == 'validation':
            _code = _model.get_value(_row, self._lst_col_order[22])
            _name = _model.get_value(_row, self._lst_col_order[17])
            _title = _("Analyzing Validation {0:s}: {1:s}").format(
                str(_code), str(_name))

            pub.sendMessage('request_set_title', title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """
        Handle events for the Validation package Module View RAMSTKTreeView().

        This method is called whenever a Validation Module View RAMSTKTreeView()
        row is activated/changed.

        :param selection: the Validation class Gtk.TreeSelection().
        :type selection: :class:`Gtk.TreeSelection`
        :return: None
        :rtype: None
        """
        selection.handler_block(self.treeview.dic_handler_id['changed'])

        _attributes: Dict[str, Any] = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes['validation_id']

            _title = _("Analyzing Validation {0:s}").format(
                str(_attributes['validation_id']))

            pub.sendMessage('selected_validation', attributes=_attributes)
            pub.sendMessage('request_get_validation_attributes',
                            node_id=self._record_id,
                            table='validation')
            pub.sendMessage('request_set_title', title=_title)

        selection.handler_unblock(self.treeview.dic_handler_id['changed'])
