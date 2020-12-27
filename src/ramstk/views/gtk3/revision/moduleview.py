# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.moduleview.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Revision GTK3 module view."""

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


class RevisionPanel(RAMSTKPanel):
    """Panel to display flat list of revisions."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module = 'revisions'

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Revision panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = ATTRIBUTE_KEYS
        self._dic_attribute_updater = {
            'revision_id': [None, 'edited', 0],
            'availability_logistics': [None, 'edited', 1],
            'availability_mission': [None, 'edited', 2],
            'cost': [None, 'edited', 3],
            'cost_per_failure': [None, 'edited', 4],
            'cost_per_hour': [None, 'edited', 5],
            'hazard_rate_active': [None, 'edited', 6],
            'hazard_rate_dormant': [None, 'edited', 7],
            'hazard_rate_logistics': [None, 'edited', 8],
            'hazard_rate_mission': [None, 'edited', 9],
            'hazard_rate_software': [None, 'edited', 10],
            'mmt': [None, 'edited', 11],
            'mcmt': [None, 'edited', 12],
            'mpmt': [None, 'edited', 13],
            'mtbf_logistics': [None, 'edited', 14],
            'mtbf_mission': [None, 'edited', 15],
            'mttr': [None, 'edited', 16],
            'name': [None, 'edited', 17],
            'reliability_logistics': [None, 'edited', 18],
            'reliability_mission': [None, 'edited', 19],
            'remarks': [None, 'edited', 20],
            'n_parts': [None, 'edited', 21],
            'revision_code': [None, 'edited', 22],
            'program_time': [None, 'edited', 23],
            'program_time_sd': [None, 'edited', 24],
            'program_cost': [None, 'edited', 25],
            'program_cost_sd': [None, 'edited', 26],
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._title = _("Revision List")

        # Initialize public dictionary class attributes.

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_make_panel_treeview()
        self.__do_set_properties()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_tree, 'succeed_retrieve_revisions')
        pub.subscribe(super().do_refresh_tree, 'wvw_editing_revision')
        pub.subscribe(super().on_delete, 'succeed_delete_revision')

        pub.subscribe(self._on_module_switch, 'mvwSwitchedPage')

    def do_set_callbacks(self) -> None:
        """Set callbacks for the Revision module view.

        :return: None
        """
        super().do_set_callbacks()
        super().do_set_cell_callbacks('mvw_editing_revision', [0, 1, 2])

    def _on_module_switch(self, module: str = '') -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == 'revision' and _row is not None:
            _code = _model.get_value(_row, self._lst_col_order[5])
            _name = _model.get_value(_row, self._lst_col_order[15])
            _title = _("Analyzing Revision {0:s}: {1:s}").format(
                str(_code), str(_name))

            pub.sendMessage('request_set_title', title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Revision package Module View RAMSTKTreeView().

        This method is called whenever a Revision Module View RAMSTKTreeView()
        row is activated/changed.

        :param selection: the Revision class Gtk.TreeSelection().
        :return: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes['revision_id']

            _title = _("Analyzing Revision {0:s}: {1:s}").format(
                str(_attributes['revision_code']), str(_attributes['name']))

            pub.sendMessage('selected_revision', attributes=_attributes)
            pub.sendMessage('request_set_title', title=_title)

    def __do_set_properties(self) -> None:
        """Set common properties of the ModuleView and widgets.

        :return: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        self.tvwTreeView.set_tooltip_text(_("Displays the list of revisions."))


class ModuleView(RAMSTKModuleView):
    """Display Revision attribute data in the RAMSTK Module Book.

    The Revision Module View displays all the Revisions associated with the
    connected RAMSTK Program in a flat list.  The attributes of a Revision
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
    _module: str = 'revision'
    _tablabel: str = 'Revision'
    _tabtooltip: str = _("Displays the list of Revisions for the open RAMSTK "
                         "Project.")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Revision Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/revision.png')

        # Initialize private list attributes.
        self._lst_mnu_labels = [
            _("Add Revision"),
            _("Delete Selected Revision"),
            _("Save Selected Revision"),
            _("Save All Revisions"),
        ]
        self._lst_tooltips = [
            _("Add a new revision."),
            _("Remove the currently selected revision."),
            _("Save changes to the currently selected revision."),
            _("Save changes to all revisions."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = RevisionPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, 'selected_revision')
        pub.subscribe(self._on_insert_revision, 'succeed_insert_revision')

    def do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete selected record from the RAMSTKRevision table.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
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

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the Revision's record ID.

        :param attributes: the attributes dict for the selected Revision.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['revision_id']

    def _on_insert_revision(self,
                            node_id: int = 0,
                            tree: treelib.Tree = '') -> None:
        """Add row to module view for newly added revision.

        :param node_id: the ID of the newly added revision.
        :param tree: the treelib Tree() containing the work stream module's
            data.
        :return: None
        """
        _data = tree.get_node(node_id).data['revision'].get_attributes()
        self._pnlPanel.on_insert(_data)

    def __make_ui(self) -> None:
        """Build the user interface for the revision module view.

        :return: None
        """
        super().make_ui()

        self._pnlPanel.do_set_properties()
        self._pnlPanel.do_set_callbacks()
        self._pnlPanel.tvwTreeView.dic_handler_id[
            'button-press'] = self._pnlPanel.tvwTreeView.connect(
                "button_press_event",
                super().on_button_press)
