# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.validation.moduleview.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Validation GTK3 module view."""

# Standard Library Imports
from typing import Dict, List

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


class ValidationPanel(RAMSTKPanel):
    """Panel to display flat list of validation tasks."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Validation panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            0: ['description', 'string'],
            1: ['task_type', 'integer'],
            2: ['task_specification', 'string'],
            3: ['measurement_unit', 'integer'],
            4: ['acceptable_minimum', 'float'],
            5: ['acceptable_maximum', 'float'],
            6: ['acceptable_mean', 'float'],
            7: ['acceptable_variance', 'float'],
            8: ['date_start', 'string'],
            9: ['date_end', 'string'],
            10: ['status', 'float'],
            11: ['name', 'string'],
            12: ['time_minimum', 'float'],
            14: ['time_average', 'float'],
            15: ['time_maximum', 'float'],
            16: ['cost_minimum', 'float'],
            17: ['cost_average', 'float'],
            18: ['cost_maximum', 'float'],
        }
        self._dic_attribute_updater = {
            'revision_id': [None, 'edited', 0],
            'validation_id': [None, 'edited', 1],
            'description': [None, 'edited', 2],
            'task_type': [None, 'edited', 3],
            'task_specification': [None, 'edited', 4],
            'measurement_unit': [None, 'edited', 5],
            'acceptable_minimum': [None, 'edited', 6],
            'acceptable_mean': [None, 'edited', 7],
            'acceptable_maximum': [None, 'edited', 8],
            'acceptable_variance': [None, 'edited', 9],
            'date_start': [None, 'edited', 10],
            'date_end': [None, 'edited', 11],
            'status': [None, 'edited', 12],
            'time_minimum': [None, 'edited', 13],
            'time_average': [None, 'edited', 14],
            'time_maximum': [None, 'edited', 15],
            'cost_minimum': [None, 'edited', 18],
            'cost_average': [None, 'edited', 19],
            'cost_maximum': [None, 'edited', 20],
            'confidence': [None, 'edited', 23],
            'time_ll': [None, 'edited', 24],
            'time_mean': [None, 'edited', 25],
            'time_ul': [None, 'edited', 26],
            'time_variance': [None, 'edited', 27],
            'cost_ll': [None, 'edited', 28],
            'cost_mean': [None, 'edited', 29],
            'cost_ul': [None, 'edited', 30],
            'cost_variance': [None, 'edited', 31],
            'name': [None, 'edited', 32],
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._title = _("Verification Task List")

        # Initialize public dictionary class attributes.

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_make_panel_treeview()
        self.__do_set_properties()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_tree, 'succeed_retrieve_validations')
        pub.subscribe(super().do_refresh_tree, 'wvw_editing_validation')
        pub.subscribe(super().on_delete, 'succeed_delete_validation')

        pub.subscribe(self._on_module_switch, 'mvwSwitchedPage')

    def _on_module_switch(self, module: str = '') -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == 'validation' and _row is not None:
            _code = _model.get_value(_row, self._lst_col_order[5])
            _name = _model.get_value(_row, self._lst_col_order[15])
            _title = _("Analyzing Validation {0:s}: {1:s}").format(
                str(_code), str(_name))

            pub.sendMessage('request_set_title', title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Validation Module View RAMSTKTreeView().

        This method is called whenever a Validation Module View
        RAMSTKTreeView() row is activated/changed.

        :param selection: the Validation class Gtk.TreeSelection().
        :return: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes['validation_id']
            self._parent_id = _attributes['parent_id']

            _title = _("Analyzing Validation {0:s}: {1:s}").format(
                str(_attributes['validation_code']), str(_attributes['name']))

            pub.sendMessage('selected_validation', attributes=_attributes)
            pub.sendMessage('request_get_validation_attributes',
                            node_id=self._record_id,
                            table='hazards')
            pub.sendMessage('request_set_title', title=_title)

    def __do_set_callbacks(self) -> None:
        """Set callbacks for the Validation module view.

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
            _("Displays the hierarchical list of validations."))


class ModuleView(RAMSTKModuleView):
    """Display Validation attribute data in the RAMSTK Module Book.

    The Validation Module View displays all the Validations associated with the
    connected RAMSTK Program in a flat list.  The attributes of a Validation
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
    _module: str = 'validation'
    _tablabel: str = 'Verification'
    _tabtooltip: str = _("Displays the list of verification tasks for the "
                         "selected Revision.")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Validation Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/validation.png')

        # Initialize private list attributes.
        self._lst_callbacks = [
            self.do_request_insert_sibling,
            self._do_request_delete,
            self._do_request_update,
            self._do_request_update_all,
        ]
        self._lst_icons = [
            'add',
            'remove',
            'save',
            'save-all',
        ]
        self._lst_mnu_labels = [
            _("Add Task"),
            _("Delete Selected Task"),
            _("Save Selected Task"),
            _("Save All Tasks"),
        ]
        self._lst_tooltips = [
            _("Add a new validation task."),
            _("Remove the currently selected validation task."),
            _("Save changes to the currently selected validation task."),
            _("Save changes to all validation tasks."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = ValidationPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().make_ui()
        self._pnlPanel.do_set_cell_callbacks(
            'mvw_editing_validation',
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_set_cursor_active, 'succeed_delete_validation_2')
        pub.subscribe(self.do_set_cursor_active, 'succeed_insert_validation_2')
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_validation')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_delete_validation')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_insert_validation')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_validation')

        pub.subscribe(self._on_insert_validation, 'succeed_insert_validation')

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete selected record from the RAMSTKValidation table.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent(
        ).get_parent()
        _prompt = _("You are about to delete Validation {0:d} and all "
                    "data associated with it.  Is this really what "
                    "you want to do?").format(self._record_id)
        _dialog: RAMSTKMessageDialog = RAMSTKMessageDialog(parent=_parent)
        _dialog.do_set_message(_prompt)
        _dialog.do_set_message_type('question')

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage('request_delete_validation',
                            node_id=self._record_id)

        _dialog.do_destroy()

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """Request to update the selected record to the RAMSTKValidation table.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_validation', node_id=self._record_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """Request to save all the records to the RAMSTKValidation table.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_validations')

    def _on_insert_validation(self, node_id: int, tree: treelib.Tree) -> None:
        """Add row to module view for newly added validation.

        :param node_id: the ID of the newly added validation.
        :param tree: the treelib Tree() containing the work stream module's
            data.
        :return: None
        """
        _data = tree.get_node(node_id).data['validation'].get_attributes()
        self._pnlPanel.on_insert(_data)
