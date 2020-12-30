# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.moduleview.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Requirement GTK3 module view."""

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


class RequirementPanel(RAMSTKPanel):
    """Panel to display hierarchy of requirements."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module = 'requirements'

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
        self._dic_row_loader = {
            'requirement': self.__do_load_requirement,
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._title = _("Requirements")

        # Initialize public dictionary class attributes.

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_make_panel_treeview()
        self.__do_set_properties()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_panel, 'succeed_retrieve_requirements')
        pub.subscribe(super().do_load_panel, 'succeed_insert_requirement')
        pub.subscribe(super().do_refresh_tree, 'wvw_editing_requirement')
        pub.subscribe(super().on_delete, 'succeed_delete_requirement')

        pub.subscribe(self._on_module_switch, 'mvwSwitchedPage')

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

    def __do_load_requirement(self, node: treelib.Node,
                              row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a requirement into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the requirement
            tree.
        :return: _new_row; the row that was just populated with requirement
            data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        _attributes = [
            _entity.revision_id, _entity.requirement_id, _entity.derived,
            _entity.description, _entity.figure_number, _entity.owner,
            _entity.page_number, _entity.parent_id, _entity.priority,
            _entity.requirement_code, _entity.specification,
            _entity.requirement_type, _entity.validated,
            str(_entity.validated_date), _entity.q_clarity_0,
            _entity.q_clarity_1, _entity.q_clarity_2, _entity.q_clarity_3,
            _entity.q_clarity_4, _entity.q_clarity_5, _entity.q_clarity_6,
            _entity.q_clarity_7, _entity.q_clarity_8, _entity.q_complete_0,
            _entity.q_complete_1, _entity.q_complete_2, _entity.q_complete_3,
            _entity.q_complete_4, _entity.q_complete_5, _entity.q_complete_6,
            _entity.q_complete_7, _entity.q_complete_8, _entity.q_complete_9,
            _entity.q_consistent_0, _entity.q_consistent_1,
            _entity.q_consistent_2, _entity.q_consistent_3,
            _entity.q_consistent_4, _entity.q_consistent_5,
            _entity.q_consistent_6, _entity.q_consistent_7,
            _entity.q_consistent_8, _entity.q_verifiable_0,
            _entity.q_verifiable_1, _entity.q_verifiable_2,
            _entity.q_verifiable_3, _entity.q_verifiable_4,
            _entity.q_verifiable_5
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading requirement {0} in the "
                "requirement tree.  This might indicate it was missing it's "
                "data package, some of the data in the package was missing, "
                "or some of the data was the wrong type.  Row data was: "
                "{1}").format(str(node.identifier), _attributes)
            pub.sendMessage('do_log_warning_msg',
                            logger_name='WARNING',
                            message=_message)

        return _new_row

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

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id,
                      'selected_{0}'.format(self._module))

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

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the Requirement's record and parent ID.

        :param attributes: the attributes dict for the selected Requirement.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['requirement_id']
        self._parent_id = attributes['parent_id']

    def __make_ui(self) -> None:
        """Build the user interface for the requirement module view.

        :return: None
        """
        super().make_ui()

        self._pnlPanel.do_set_properties()
        self._pnlPanel.do_set_callbacks()
        self._pnlPanel.do_set_cell_callbacks('mvw_editing_requirement',
                                             [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self._pnlPanel.tvwTreeView.dic_handler_id[
            'button-press'] = self._pnlPanel.tvwTreeView.connect(
                "button_press_event",
                super().on_button_press)
