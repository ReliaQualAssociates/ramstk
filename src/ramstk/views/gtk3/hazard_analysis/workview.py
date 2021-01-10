# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hazard_analysis.workview.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Function Work View."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKPanel, RAMSTKWorkView


class HazOpsPanel(RAMSTKPanel):
    """The panel to display the hazards analysis for the selected Function."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module = 'hazards'

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Function Hazard Analysis panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys = {
            3: ['potential_hazard', 'string'],
            4: ['potential_cause', 'string'],
            5: ['assembly_effect', 'string'],
            6: ['assembly_severity', 'string'],
            7: ['assembly_probability', 'string'],
            9: ['assembly_mitigation', 'string'],
            10: ['assembly_severity_f', 'string'],
            11: ['assembly_probability_f', 'string'],
            13: ['system_effect', 'string'],
            14: ['system_severity', 'string'],
            15: ['system_probability', 'string'],
            17: ['system_mitigation', 'string'],
            18: ['system_severity_f', 'string'],
            19: ['system_probability_f', 'string'],
            21: ['remarks', 'string'],
        }
        self._dic_attribute_updater = {
            'revision_id': [None, 'edited', 0],
            'function_id': [None, 'edited', 1],
            'hazard_id': [None, 'edited', 2],
            'potential_hazard': [None, 'edited', 3],
            'potential_cause': [None, 'edited', 4],
            'assembly_effect': [None, 'edited', 5],
            'assembly_severity': [None, 'edited', 6],
            'assembly_probability': [None, 'edited', 7],
            'assembly_hri': [None, 'edited', 8],
            'assembly_mitigation': [None, 'edited', 9],
            'assembly_severity_f': [None, 'edited', 10],
            'assembly_probability_f': [None, 'edited', 11],
            'assembly_hri_f': [None, 'edited', 12],
            'system_effect': [None, 'edited', 13],
            'system_severity': [None, 'edited', 14],
            'system_probability': [None, 'edited', 15],
            'system_hri': [None, 'edited', 16],
            'system_mitigation': [None, 'edited', 17],
            'system_severity_f': [None, 'edited', 18],
            'system_probability_f': [None, 'edited', 19],
            'system_hri_f': [None, 'edited', 20],
            'remarks': [None, 'edited', 21],
            'function_1': [None, 'edited', 22],
            'function_2': [None, 'edited', 23],
            'function_3': [None, 'edited', 24],
            'function_4': [None, 'edited', 25],
            'function_5': [None, 'edited', 26],
            'result_1': [None, 'edited', 27],
            'result_2': [None, 'edited', 28],
            'result_3': [None, 'edited', 29],
            'result_4': [None, 'edited', 30],
            'result_5': [None, 'edited', 31],
            'user_blob_1': [None, 'edited', 32],
            'user_blob_2': [None, 'edited', 33],
            'user_blob_3': [None, 'edited', 34],
            'user_float_1': [None, 'edited', 35],
            'user_float_2': [None, 'edited', 36],
            'user_float_3': [None, 'edited', 37],
            'user_int_1': [None, 'edited', 38],
            'user_int_2': [None, 'edited', 39],
            'user_int_3': [None, 'edited', 40],
        }
        self._dic_row_loader = {
            'hazard': super()._do_load_treerow,
        }

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.
        self._title: str = _("Hazards Analysis")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        # Make a fixed type panel.

        super().do_make_panel_treeview()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_panel, 'succeed_retrieve_hazards')
        pub.subscribe(super().do_load_panel, 'succeed_get_hazard_tree')
        pub.subscribe(super().do_load_panel, 'succeed_insert_hazard')
        pub.subscribe(super().on_delete, 'succeed_delete_hazard')

        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')

    def do_load_severity(
            self, criticalities: Dict[int, Tuple[str, str, int]]) -> None:
        """Load the Gtk.CellRendererCombo() containing severities.

        :param criticalities: the dict containing the hazard severity
            categories and values.
        :return: None
        :rtype: None
        """
        for i in [6, 10, 14, 18]:
            _model = self.tvwTreeView.get_cell_model(i)
            for _key in criticalities:
                _model.append((criticalities[_key][1], ))

    def do_load_hazards(self, hazards: Dict[Any, Any]) -> None:
        """Load the Gtk.CellRendererCombos() containing hazards.

        :param hazards: the dict containing the hazards and hazard types
            to be considered.
        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_cell_model(3)
        for _key in hazards:
            _hazard = '{0}, {1}'.format(hazards[_key][0], hazards[_key][1])
            _model.append((_hazard, ))

    def do_load_probability(self, probabilities: List[str]) -> None:
        """Load the Gtk.CellRendererCombos() containing probabilities.

        :param probabilities: the list of hazard probabilities.
        :return: None
        :rtype: None
        """
        for i in [7, 11, 15, 19]:
            _model = self.tvwTreeView.get_cell_model(i)
            for _probability in probabilities:
                _model.append((_probability[0], ))

    def do_set_callbacks(self) -> None:
        """Set the callback methods and functions for the panel widgets.

        :return: None
        :rtype: None
        """
        _lst_col_order: List[int] = list(self.tvwTreeView.position.values())

        self.tvwTreeView.dic_handler_id[
            'changed'] = self.tvwTreeView.selection.connect(
                'changed', self._on_row_change)

        for i in _lst_col_order[3:]:
            _cell = self.tvwTreeView.get_column(_lst_col_order[i]).get_cells()
            try:
                _cell[0].connect('edited',
                                 super().on_cell_edit, i, 'wvw_editing_hazard')
            except TypeError:
                _cell[0].connect('toggled',
                                 super().on_cell_toggled, 'new text', i,
                                 'wvw_editing_hazard')

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_model()
        _model.clear()

    def _on_insert(self, tree: Tree) -> None:
        """Wrap the do_load_panel() method when an element is inserted.

        The do_set_cursor_active() method responds to the same message,
        but one less argument in it's call.  This results in a PyPubSub
        error and is the reason this wrapper method is needed.

        :param tree: the module's treelib Tree().
        :return: None
        """
        super().do_load_panel(tree)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the HazOps Tree View RAMSTKTreeView().

        This method is called whenever a Tree View row is activated.

        :param selection: the HazOps RAMSTKTreeview Gtk.TreeSelection().
        :return: None
        :rtype: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._parent_id = _attributes['function_id']
            self._record_id = _attributes['hazard_id']

            pub.sendMessage(
                'selected_hazard',
                attributes=_attributes,
            )

    def __do_set_properties(self) -> None:
        """Set the properties of the panel widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        self.tvwTreeView.set_tooltip_text(
            _("Displays the Hazards Analysis for the currently selected "
              "Function."))


class HazOps(RAMSTKWorkView):
    """Display HazOps attribute data in the Work Book.

    The WorkView displays all the attributes for the Hazards Analysis (HazOps).
    The attributes of a HazOps Work View are:

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
    :ivar int _hazard_id: the ID of the currently selected hazard.
    """
    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'hazard'
    _tablabel: str = _("HazOps")
    _tabtooltip: str = _("Displays the HazOps analysis for the selected "
                         "Function.")

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Work View for the HazOps.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks.insert(0, super().do_request_insert_sibling)
        self._lst_callbacks.insert(1, self.do_request_delete)
        self._lst_callbacks.insert(2, self._do_request_calculate)
        self._lst_icons.insert(0, 'add')
        self._lst_icons.insert(1, 'remove')
        self._lst_icons.insert(2, 'calculate')
        self._lst_mnu_labels = [
            _("Add Hazard"),
            _("Delete Selected Hazard"),
            _("Calculate HazOp"),
            _("Save Selected Hazard"),
            _("Save All Hazards"),
        ]
        self._lst_tooltips = [
            _("Add a new hazard to the HazOps analysis."),
            _("Delete the selected hazard from the selected function."),
            _("Calculate the HazOps analysis."),
            _("Save changes to the selected hazard."),
            _("Save changes to all hazards."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel: RAMSTKPanel = HazOpsPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, 'selected_hazard')
        pub.subscribe(self._on_select_function, 'selected_function')

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Request to calculate the HazOps HRI.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_fha', node_id=self._record_id)

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the record ID when a hazard is selected.

        :param attributes: the hazard dict for the selected hazard ID.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hazard_id']

    def _on_select_function(self, attributes: Dict[str, Any]) -> None:
        """Set the parent ID when a function is selected.

        :param attributes: the function dict for the selected function ID.
        :return: None
        :rtype: None
        """
        self._parent_id = attributes['function_id']

    def __make_ui(self) -> None:
        """Build the user interface for the Function Hazard Analysis tab.

        :return: None
        :rtype: None
        """
        super().do_make_layout()
        super().do_embed_treeview_panel()

        self._pnlPanel.do_set_callbacks()

        self._pnlPanel.do_load_severity(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_SEVERITY)
        self._pnlPanel.do_load_hazards(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_HAZARDS)
        self._pnlPanel.do_load_probability(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_FAILURE_PROBABILITY)

        self.show_all()
