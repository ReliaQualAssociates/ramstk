# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.function.moduleview.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Function GTK3 module view."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKModuleView, RAMSTKPanel

# RAMSTK Local Imports
from . import ATTRIBUTE_KEYS


class FunctionPanel(RAMSTKPanel):
    """Panel to display hierarchy of functions."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module = 'functions'

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Function panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self._dic_attribute_keys = ATTRIBUTE_KEYS
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
        self._dic_row_loader = {
            'function': super()._do_load_treerow,
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._title = _("Function BoM")

        # Initialize public dictionary class attributes.

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_make_panel_treeview()
        self.__do_set_properties()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_panel, 'succeed_retrieve_functions')
        pub.subscribe(super().do_load_panel, 'succeed_insert_function')
        pub.subscribe(super().do_refresh_tree, 'wvw_editing_function')
        pub.subscribe(super().on_delete, 'succeed_delete_function')

        pub.subscribe(self._on_module_switch, 'mvwSwitchedPage')

    def _on_module_switch(self, module: str = '') -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == 'functions' and _row is not None:
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
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes['function_id']
            self._parent_id = _attributes['parent_id']

            _title = _("Analyzing Function {0:s}: {1:s}").format(
                str(_attributes['function_code']), str(_attributes['name']))

            pub.sendMessage(
                'selected_function',
                attributes=_attributes,
            )
            pub.sendMessage(
                'request_set_title',
                title=_title,
            )

    def __do_set_properties(self) -> None:
        """Set common properties of the ModuleView and widgets.

        :return: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        self.tvwTreeView.set_tooltip_text(
            _("Displays the hierarchical list of functions."))


class ModuleView(RAMSTKModuleView):
    """Display Function attribute data in the RAMSTK Module Book.

    The Function Module View displays all the Functions associated with the
    connected RAMSTK Program in a flat list.  The attributes of a Function
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

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/function.png')

        # Initialize private list attributes.
        self._lst_callbacks.insert(1, super().do_request_insert_child)
        self._lst_icons[0] = 'insert_sibling'
        self._lst_icons.insert(1, 'insert_child')
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

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id,
                      'selected_{0}'.format(self._module))

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the stakeholder input's record ID.

        :param attributes: the attributes dict for the selected stakeholder
            input.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['function_id']
        self._parent_id = attributes['parent_id']

    def __make_ui(self) -> None:
        """Build the user interface for the function module view.

        :return: None
        """
        super().make_ui()

        self._pnlPanel.do_set_properties()
        self._pnlPanel.do_set_callbacks()
        self._pnlPanel.do_set_cell_callbacks('mvw_editing_function',
                                             [5, 15, 17])
        self._pnlPanel.tvwTreeView.dic_handler_id[
            'button-press'] = self._pnlPanel.tvwTreeView.connect(
                "button_press_event",
                super().on_button_press)
