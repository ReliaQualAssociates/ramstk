# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.function.moduleview.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Function GTK3 module view."""

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


class FunctionPanel(RAMSTKPanel):
    """Panel to display hierarchy of functions."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Function panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self._dic_attribute_updater = {
            'revision_id': [None, 'edited', 0],
            'function_id': [None, 'edited', 1],
            'availability_logistics': [None, 'edited', 2],
            'availability_mission': [None, 'edited', 3],
            'cost': [None, 'edited', 4],
            'function_code': [None, 'edited', 5],
            'failure_rate_logistics': [None, 'edited', 6],
            'failure_rate_mission': [None, 'edited', 7],
            'level': [None, 'edited', 8],
            'mmt': [None, 'edited', 9],
            'mcmt': [None, 'edited', 10],
            'mpmt': [None, 'edited', 11],
            'mtbf_logistics': [None, 'edited', 12],
            'mtbf_mission': [None, 'edited', 13],
            'mttr': [None, 'edited', 14],
            'name': [None, 'edited', 15],
            'parent_id': [None, 'edited', 16],
            'remarks': [None, 'edited', 17],
            'safety_critical': [None, 'toggled', 18],
            'total_mode_count': [None, 'edited', 19],
            'total_part_count': [None, 'edited', 20],
            'type': [None, 'edited', 21],
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._title = _("Function BoM")

        # Initialize public dictionary class attributes.

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_make_panel_treeview()
        self.__do_set_properties()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_tree, 'succeed_retrieve_functions')
        pub.subscribe(super().do_refresh_tree, 'wvw_editing_function')
        pub.subscribe(super().on_delete, 'succeed_delete_function')

        pub.subscribe(self._on_module_switch, 'mvwSwitchedPage')

    def _on_module_switch(self, module: str = '') -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == 'function' and _row is not None:
            _code = _model.get_value(_row, self._lst_col_order[5])
            _name = _model.get_value(_row, self._lst_col_order[15])
            _title = _("Analyzing Function {0:s}: {1:s}").format(
                str(_code), str(_name))

            pub.sendMessage('request_set_title', title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Function package Module View RAMSTKTreeView().

        This method is called whenever a Function Module View RAMSTKTreeView()
        row is activated/changed.

        :param selection: the Function class Gtk.TreeSelection().
        :return: None
        """
        selection.handler_block(self.tvwTreeView.dic_handler_id['changed'])

        _attributes: Dict[str, Any] = {}

        _model, _row = selection.get_selected()
        if _row is not None:
            for _key in self._dic_attribute_updater:
                _attributes[_key] = _model.get_value(
                    _row,
                    self._lst_col_order[self._dic_attribute_updater[_key][2]])

        if _attributes:
            self._record_id = _attributes['function_id']
            self._parent_id = _attributes['parent_id']

            _title = _("Analyzing Function {0:s}: {1:s}").format(
                str(_attributes['function_code']), str(_attributes['name']))

            pub.sendMessage('selected_function', attributes=_attributes)
            pub.sendMessage('request_get_function_attributes',
                            node_id=self._record_id,
                            table='hazards')
            pub.sendMessage('request_set_title', title=_title)

        selection.handler_unblock(self.tvwTreeView.dic_handler_id['changed'])

    def __do_set_callbacks(self) -> None:
        """Set callbacks for the Function module view.

        :return: None
        """
        self.tvwTreeView.dic_handler_id[
            'changed'] = self.tvwTreeView.selection.connect(
                'changed', self._on_row_change)

    def __do_set_properties(self) -> None:
        """Set common properties of the ModuleView and widgets.

        :return: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        self.tvwTreeView.set_enable_tree_lines(True)
        self.tvwTreeView.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.tvwTreeView.set_level_indentation(2)
        self.tvwTreeView.set_rubber_banding(True)
        self.tvwTreeView.set_tooltip_text(
            _("Displays the hierarchical list of functions."))


class ModuleView(RAMSTKModuleView):
    """Display Function attribute data in the RAMSTK Module Book.

    The Function Module View displays all the Functions associated with the
    connected RAMSTK Program in a flat list.  The attributes of a Function
    Module View are:

    :cvar _module: the name of the module.

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

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'function'
    _tablabel: str = 'Function'
    _tabtooltip: str = _("Displays the functional hierarchy for the selected "
                         "Revision.")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Function Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            5: ['function_code', 'text'],
            15: ['name', 'text'],
            17: ['remarks', 'text'],
        }
        self._dic_icons['tab'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/function.png')

        # Initialize private list attributes.
        self._lst_callbacks = [
            self.do_request_insert_sibling,
            self.do_request_insert_child,
            self._do_request_delete,
            self._do_request_update,
            self._do_request_update_all,
        ]
        self._lst_icons = [
            'insert_sibling',
            'insert_child',
            'remove',
            'save',
            'save-all',
        ]
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
        self._pnlPanel = FunctionPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_set_cursor_active, 'succeed_delete_function')
        pub.subscribe(self.do_set_cursor_active, 'succeed_insert_function')
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_function')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_delete_function')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_insert_function')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_function')

        pub.subscribe(self._on_insert_function, 'succeed_insert_function')

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete selected record from the RAMSTKFunction table.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent(
        ).get_parent()
        _prompt = _("You are about to delete Function {0:d} and all "
                    "data associated with it.  Is this really what "
                    "you want to do?").format(self._record_id)
        _dialog = RAMSTKMessageDialog(parent=_parent)
        _dialog.do_set_message(_prompt)
        _dialog.do_set_message_type('question')

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage('request_delete_function', node_id=self._record_id)

        _dialog.do_destroy()

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """Request to update the selected record to the RAMSTKFunction table.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_function', node_id=self._record_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """Request to save all the records to the RAMSTKFunction table.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_functions')

    def _on_insert_function(self, node_id: int, tree: treelib.Tree) -> None:
        """Add row to module view for newly added function.

        :param node_id: the ID of the newly added function.
        :param tree: the treelib Tree() containing the work stream module's
            data.
        :return: None
        """
        _data = tree.get_node(node_id).data['function'].get_attributes()
        self._pnlPanel.on_insert(_data)
