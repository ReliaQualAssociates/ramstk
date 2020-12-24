# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.moduleview.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Requirement GTK3 module view."""

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

# RAMSTK Local Imports
from . import ATTRIBUTE_KEYS


class RequirementPanel(RAMSTKPanel):
    """Panel to display hierarchy of requirements."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Requirement panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = ATTRIBUTE_KEYS
        self._dic_attribute_updater = {
            'requirement_id': [None, 'edited', 1],
            'derived': [None, 'edited', 2],
            'description': [None, 'edited', 3],
            'figure_number': [None, 'edited', 4],
            'owner': [None, 'edited', 5],
            'page_number': [None, 'edited', 6],
            'parent_id': [None, 'edited', 7],
            'priority': [None, 'edited', 8],
            'requirement_code': [None, 'edited', 9],
            'specification': [None, 'edited', 10],
            'requirement_type': [None, 'edited', 11],
            'validated': [None, 'edited', 12],
            'validated_date': [None, 'edited', 13],
            'q_clarity_0': [None, 'edited', 14],
            'q_clarity_1': [None, 'edited', 15],
            'q_clarity_2': [None, 'edited', 16],
            'q_clarity_3': [None, 'edited', 17],
            'q_clarity_4': [None, 'edited', 18],
            'q_clarity_5': [None, 'edited', 19],
            'q_clarity_6': [None, 'edited', 20],
            'q_clarity_7': [None, 'edited', 21],
            'q_clarity_8': [None, 'edited', 22],
            'q_complete_0': [None, 'edited', 23],
            'q_complete_1': [None, 'edited', 24],
            'q_complete_2': [None, 'edited', 25],
            'q_complete_3': [None, 'edited', 26],
            'q_complete_4': [None, 'edited', 27],
            'q_complete_5': [None, 'edited', 28],
            'q_complete_6': [None, 'edited', 29],
            'q_complete_7': [None, 'edited', 30],
            'q_complete_8': [None, 'edited', 31],
            'q_complete_9': [None, 'edited', 32],
            'q_consistent_0': [None, 'edited', 33],
            'q_consistent_1': [None, 'edited', 34],
            'q_consistent_2': [None, 'edited', 35],
            'q_consistent_3': [None, 'edited', 36],
            'q_consistent_4': [None, 'edited', 37],
            'q_consistent_5': [None, 'edited', 38],
            'q_consistent_6': [None, 'edited', 39],
            'q_consistent_7': [None, 'edited', 40],
            'q_consistent_8': [None, 'edited', 41],
            'q_verifiable_0': [None, 'edited', 42],
            'q_verifiable_1': [None, 'edited', 43],
            'q_verifiable_2': [None, 'edited', 44],
            'q_verifiable_3': [None, 'edited', 45],
            'q_verifiable_4': [None, 'edited', 46],
            'q_verifiable_5': [None, 'edited', 47],
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._title = _("Requirement BoM")

        # Initialize public dictionary class attributes.

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_make_panel_treeview()
        self.__do_set_properties()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_tree, 'succeed_retrieve_requirements')
        pub.subscribe(super().do_refresh_tree, 'wvw_editing_requirement')
        pub.subscribe(super().on_delete, 'succeed_delete_requirement')

        pub.subscribe(self._on_module_switch, 'mvwSwitchedPage')

    def do_set_callbacks(self) -> None:
        """Set callbacks for the requirement module view.

        :return: None
        """
        super().do_set_callbacks()
        super().do_set_cell_callbacks('mvw_editing_requirement',
                                      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def _on_module_switch(self, module: str = '') -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == 'requirement' and _row is not None:
            _code = _model.get_value(_row, self._lst_col_order[5])
            _name = _model.get_value(_row, self._lst_col_order[15])
            _title = _("Analyzing Requirement {0:s}: {1:s}").format(
                str(_code), str(_name))

            pub.sendMessage('request_set_title', title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Requirement ModuleView RAMSTKTreeView().

        This method is called whenever a Requirement Module View
        RAMSTKTreeView() row is activated/changed.

        :param selection: the Requirement class Gtk.TreeSelection().
        :return: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes['requirement_id']
            self._parent_id = _attributes['parent_id']

            _title = _("Analyzing Requirement {0:s}: {1:s}").format(
                str(_attributes['requirement_code']),
                str(_attributes['description']))

            pub.sendMessage('selected_requirement', attributes=_attributes)
            pub.sendMessage('request_set_title', title=_title)

    def __do_set_properties(self) -> None:
        """Set common properties of the ModuleView and widgets.

        :return: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        self.tvwTreeView.set_tooltip_text(
            _("Displays the hierarchical list of requirements."))


class ModuleView(RAMSTKModuleView):
    """Display Requirement attribute data in the RAMSTK Module Book.

    The Requirement Module View displays all the Requirements associated with
    the connected RAMSTK Program in a flat list.  The attributes of a
    Requirement Module View are:

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
    _module: str = 'requirement'
    _tablabel: str = 'Requirement'
    _tabtooltip: str = _("Displays the RAMS requirements hierarchy for the "
                         "selected Revision.")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Requirement Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/requirement.png')

        # Initialize private list attributes.
        self._lst_callbacks.insert(1, self.do_request_insert_child)
        self._lst_icons[0] = 'insert_sibling'
        self._lst_icons.insert(1, 'insert_child')
        self._lst_mnu_labels = [
            _("Add Sibling Requirement"),
            _("Add Child Requirement"),
            _("Delete Selected Requirement"),
            _("Save Selected Requirement"),
            _("Save All Requirements"),
        ]
        self._lst_tooltips = [
            _("Add a new sibling requirement."),
            _("Add a new child requirement."),
            _("Remove the currently selected requirement."),
            _("Save changes to the currently selected requirement."),
            _("Save changes to all requirements"),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = RequirementPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().make_ui()
        self._pnlPanel.do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_insert_requirement,
                      'succeed_insert_requirement')

    def do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete selected record from the RAMSTKRequirement table.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent(
        ).get_parent()
        _prompt = _("You are about to delete Requirement {0:d} and all "
                    "data associated with it.  Is this really what "
                    "you want to do?").format(self._record_id)
        _dialog = RAMSTKMessageDialog(parent=_parent)
        _dialog.do_set_message(_prompt)
        _dialog.do_set_message_type('question')

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage('request_delete_requirement',
                            node_id=self._record_id)

        _dialog.do_destroy()

    def _on_insert_requirement(self, node_id: int, tree: treelib.Tree) -> None:
        """Add row to module view for newly added requirement.

        :param node_id: the ID of the newly added requirement.
        :param tree: the treelib Tree() containing the work stream module's
            data.
        :return: None
        """
        _data = tree.get_node(node_id).data['requirement'].get_attributes()
        self._pnlPanel.on_insert(_data)
