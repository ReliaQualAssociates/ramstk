# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.moduleview.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Revision GTK3 module view."""

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
    Display Revision attribute data in the RAMSTK Module Book.

    The Revision Module View displays all the Revisions associated with the
    connected RAMSTK Program in a flat list.  The attributes of a Revision
    Module View are:

    :cvar str _module: the name of the module.
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

    # Define private scalar class attributes.
    _module: str = 'revision'
    _tablabel: str = 'Revision'
    _tabtooltip: str = _("Displays the list of Revisions for the open RAMSTK "
                         "Project.")

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize the Revision Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/revision.png')

        self._dic_key_index = {
            'revision_id': 0,
            'availability_logistics': 1,
            'availability_mission': 2,
            'cost': 3,
            'cost_per_failure': 4,
            'cost_per_hour': 5,
            'hazard_rate_active': 6,
            'hazard_rate_dormant': 7,
            'hazard_rate_logistics': 8,
            'hazard_rate_mission': 9,
            'hazard_rate_software': 10,
            'mmt': 11,
            'mcmt': 12,
            'mpmt': 13,
            'mtbf_logistics': 14,
            'mtbf_mission': 15,
            'mttr': 16,
            'name': 17,
            'reliability_logistics': 18,
            'reliability_mission': 19,
            'remarks': 20,
            'n_parts': 21,
            'revision_code': 22,
            'program_time': 23,
            'program_time_sd': 24,
            'program_cost': 25,
            'program_cost_sd': 26
        }

        # Initialize private list attributes.
        self._lst_callbacks = [
            self.do_request_insert_sibling, self._do_request_delete,
            self._do_request_update, self._do_request_update_all
        ]
        self._lst_icons = ['add', 'remove', 'save', 'save-all']
        self._lst_mnu_labels = [
            _("Add Revision"),
            _("Delete Selected Revision"),
            _("Save Selected Revision"),
            _("Save All Revisions")
        ]
        self._lst_tooltips = [
            _("Add a new revision."),
            _("Remove the currently selected revision."),
            _("Save changes to the currently selected revision."),
            _("Save changes to all revisions.")
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_insert, 'succeed_insert_revision')
        pub.subscribe(self._on_module_switch, 'mvwSwitchedPage')

        pub.subscribe(self.do_load_tree, 'succeed_retrieve_revisions')
        pub.subscribe(self.do_refresh_tree, 'wvw_editing_revision')
        pub.subscribe(self.do_set_cursor_active, 'succeed_delete_revision')
        pub.subscribe(self.do_set_cursor_active, 'succeed_insert_revision')
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_revision')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_delete_revision')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_insert_revision')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_revision')
        #pub.subscribe(self.on_delete, 'succeed_delete_revision')

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to delete selected record from the RAMSTKRevision table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent(
        ).get_parent()
        _prompt = _("You are about to delete Revision {0:d} and all "
                    "data associated with it.  Is this really what "
                    "you want to do?").format(self._revision_id)
        _dialog = RAMSTKMessageDialog(parent=_parent)
        _dialog.do_set_message(_prompt)
        _dialog.do_set_message_type('question')

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage('request_delete_revision',
                            node_id=self._revision_id)

        _dialog.do_destroy()

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to update the selected record to the RAMSTKRevision table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_revision', node_id=self._revision_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to save all the records to the RAMSTKRevision table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_revisions')

    def _on_cell_edit(self, __cell: Gtk.CellRenderer, path: str, new_text: str,
                      position: int) -> None:
        """
        Handle edits of Revision package Module View RAMSTKTreeview().

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
        _dic_keys = {17: 'name', 20: 'remarks', 22: 'revision_code'}
        try:
            _key = _dic_keys[self._lst_col_order[position]]
        except KeyError:
            _key = ''

        self.treeview.do_edit_cell(__cell, path, new_text, position)

        pub.sendMessage('mvw_editing_revision',
                        node_id=[self._revision_id, -1, ''],
                        package={_key: new_text})

    def _on_insert(self, node_id: int, tree: treelib.Tree) -> None:
        """
        Add row to module view for newly added revision.

        :param int node_id: the ID of the newly added revision.
        :param tree: the treelib Tree() containing the work stream module's
            data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        super().on_insert(
            tree.get_node(node_id).data['revision'].get_attributes())

    def _on_module_switch(self, module: str = '') -> None:
        """

        :param module:
        :return:
        """
        _model, _row = self.treeview.selection.get_selected()

        if module == 'revision':
            _code = _model.get_value(_row, self._lst_col_order[22])
            _name = _model.get_value(_row, self._lst_col_order[17])
            _title = _("Analyzing Revision {0:s}: {1:s}").format(
                str(_code), str(_name))

            pub.sendMessage('request_set_title', title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """
        Handle events for the Revision package Module View RAMSTKTreeView().

        This method is called whenever a Revision Module View RAMSTKTreeView()
        row is activated/changed.

        :param selection: the Revision class Gtk.TreeSelection().
        :type selection: :class:`Gtk.TreeSelection`
        :return: None
        :rtype: None
        """
        selection.handler_block(self.treeview.dic_handler_id['changed'])

        _attributes: Dict[str, Any] = super().on_row_change(selection)

        if _attributes:
            self._revision_id = _attributes['revision_id']

            _title = _("Analyzing Revision {0:s}: {1:s}").format(
                str(_attributes['revision_code']), str(_attributes['name']))

            pub.sendMessage('request_clear_workviews')
            pub.sendMessage('selected_revision', attributes=_attributes)
            pub.sendMessage('request_get_revision_attributes',
                            node_id=self._revision_id,
                            table='failure_definitions')
            pub.sendMessage('request_get_revision_attributes',
                            node_id=self._revision_id,
                            table='usage_profile')
            pub.sendMessage('request_set_title', title=_title)

        selection.handler_unblock(self.treeview.dic_handler_id['changed'])
