# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.function.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Function Work View."""

# Standard Library Imports
from typing import Any, Dict, List, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton, RAMSTKEntry, RAMSTKPanel,
    RAMSTKTextView, RAMSTKWorkView
)


class GeneralDataPanel(RAMSTKPanel):
    """The panel to display general data about the selected Function."""
    def __init__(self) -> None:
        """Initialize an instance of the Function General Data panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            0: ['function_code', 'string'],
            1: ['name', 'string'],
            2: ['remarks', 'string'],
            3: ['safety_critical', 'integer'],
        }

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
            _("Function Code:"),
            _("Function Name:"),
            _("Remarks:"),
            '',
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("General Information")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.chkSafetyCritical: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Function is safety critical."))
        self.txtCode: RAMSTKEntry = RAMSTKEntry()
        self.txtName: RAMSTKEntry = RAMSTKEntry()
        self.txtRemarks: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        self._dic_attribute_updater: Dict[str, Union[object, str]] = {
            'function_code': [self.txtCode.do_update, 'changed'],
            'name': [self.txtName.do_update, 'changed'],
            'remarks': [self.txtRemarks.do_update, 'changed'],
            'safety_critical': [self.chkSafetyCritical.do_update, 'toggled']
        }

        self._lst_widgets = [
            self.txtCode,
            self.txtName,
            self.txtRemarks,
            self.chkSafetyCritical,
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_edit, 'mvw_editing_function')

        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel, 'selected_function')

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        self.txtCode.do_update('', signal='changed')
        self.txtName.do_update('', signal='changed')
        self.txtRemarks.do_update('', signal='changed')
        self.chkSafetyCritical.do_update(False, signal='toggled')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load data into the Function General Data page widgets.

        :param dict attributes: the Function attributes to load into the Work
            View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['function_id']

        self.txtCode.do_update(str(attributes['function_code']),
                               signal='changed')
        self.txtName.do_update(str(attributes['name']), signal='changed')
        self.txtRemarks.do_update(str(attributes['remarks']), signal='changed')
        self.chkSafetyCritical.do_update(int(attributes['safety_critical']),
                                         signal='toggled')

    def __do_set_callbacks(self) -> None:
        """Set the callback methods and functions for the panel widgets.

        :return: None
        :rtype: None
        """
        self.txtCode.dic_handler_id['changed'] = (self.txtCode.connect(
            'changed',
            super().on_changed_text, 0, 'wvw_editing_function'))
        self.txtName.dic_handler_id['changed'] = (self.txtName.connect(
            'changed',
            super().on_changed_text, 1, 'wvw_editing_function'))
        self.txtRemarks.dic_handler_id['changed'] = (self.txtRemarks.connect(
            'focus-out-event',
            super().on_focus_out, 2, 'wvw_editing_function'))
        self.chkSafetyCritical.dic_handler_id['toggled'] = (
            self.chkSafetyCritical.connect('toggled',
                                           super().on_toggled, 3,
                                           'wvw_editing_function'))

    def __do_set_properties(self) -> None:
        """Set the properties of the panel widgets.

        :return: None
        :rtype: None
        """
        self.do_set_properties(bold=True, title=self._title)

        # ----- BUTTONS
        self.chkSafetyCritical.do_set_properties(
            tooltip=_("Indicates whether or not the selected function is "
                      "safety critical."))

        # ----- ENTRIES
        self.txtCode.do_set_properties(
            width=125, tooltip=_("A unique code for the selected function."))
        self.txtName.do_set_properties(
            width=800, tooltip=_("The name of the selected function."))
        self.txtRemarks.do_set_properties(
            height=100,
            width=800,
            tooltip=_("Enter any remarks associated with the "
                      "selected function."))


class HazOpsPanel(RAMSTKPanel):
    """The panel to display the hazards analysis for the selected Function."""
    def __init__(self) -> None:
        """Initialize an instance of the Function Hazard Analysis panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
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

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.
        self._parent_id: int = -1
        self._title: str = _("Hazards Analysis")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        # Make a fixed type panel.

        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel, 'succeed_get_hazards_attributes')

        pub.subscribe(self.__do_load_panel, 'succeed_calculate_hazard')
        pub.subscribe(self.__do_load_panel, 'succeed_delete_hazard')
        pub.subscribe(self.__do_load_panel, 'succeed_insert_hazard')

    def do_load_criticality(self, criticalities: List[List[str]]) -> None:
        """Load the Gtk.CellRendererCombo() containing severities.

        :param dict criticalities: the dict containing the hazard severity
            categories and values.
        :return: None
        :rtype: None
        """
        for i in [6, 10, 14, 18]:
            _model = self.tvwTreeView.get_cell_model(i)
            for _criticality in criticalities:
                _model.append((_criticality[0], ))

    def do_load_hazards(self, hazards: Dict[Any, Any]) -> None:
        """Load the Gtk.CellRendererCombos() containing hazards.

        :param dict hazards: the dict containing the hazards and hazard types
            to be considered.
        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_cell_model(3)
        for _key in hazards:
            _hazard = '{0:s}, {1:s}'.format(hazards[_key][0], hazards[_key][1])
            _model.append((_hazard, ))

    def do_load_probability(self, probabilities: List[str]) -> None:
        """Load the Gtk.CellRendererCombos() containing probabilities.

        :param list probabilities: the list of hazard probabilities.
        :return: None
        :rtype: None
        """
        for i in [7, 11, 15, 19]:
            _model = self.tvwTreeView.get_cell_model(i)
            for _probability in probabilities:
                _model.append((_probability[0], ))

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_model()
        _model.clear()

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load data into the Hazard Analysis page widgets.

        :param dict attributes: the Hazard attributes to load.
        :return: None
        :rtype: None
        """
        _model: Gtk.ListStore = self.tvwTreeView.get_model()
        _model.clear()

        if attributes is not None:
            _hazards = list(attributes.values())
            for _hazard in _hazards:
                _attributes = list(_hazard.get_attributes().values())
                _attributes.append('')
                try:
                    # noinspection PyDeepBugsSwappedArgs
                    _model.append(None, _attributes)
                except ValueError:
                    pass
            self._parent_id = _attributes[1]

            self.tvwTreeView.do_expand_tree()

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the HazOps Tree View RAMSTKTreeView().

        This method is called whenever a Tree View row is activated.

        :param selection: the HazOps RAMSTKTreeview Gtk.TreeSelection().
        :type selection: :class:`Gtk.TreeSelection`
        :return: None
        :rtype: None
        """
        selection.handler_block(self.tvwTreeView.dic_handler_id['changed'])

        _model, _row = selection.get_selected()
        try:
            self._parent_id = _model.get_value(_row, 1)
            self._record_id = _model.get_value(_row, 2)
        except TypeError:
            self._parent_id = -1
            self._record_id = -1

        selection.handler_unblock(self.tvwTreeView.dic_handler_id['changed'])

    def __do_set_callbacks(self) -> None:
        """Set the callback methods and functions for the panel widgets.

        :return: None
        :rtype: None
        """
        _lst_column_order: List[int] = list(self.tvwTreeView.position.values())

        self.tvwTreeView.dic_handler_id[
            'changed'] = self.tvwTreeView.selection.connect(
                'changed', self._on_row_change)

        for i in _lst_column_order[3:]:
            _cell = self.tvwTreeView.get_column(
                _lst_column_order[i]).get_cells()
            try:
                _cell[0].connect('edited', self.on_cell_edit, i,
                                 'wvw_editing_hazard')
            except TypeError:
                _cell[0].connect('toggled', self.on_cell_edit, 'new text', i,
                                 'wvw_editing_hazard')

    def __do_set_properties(self) -> None:
        """Set the properties of the panel widgets.

        :return: None
        :rtype: None
        """
        self.do_set_properties(bold=True, title=self._title)

        self.tvwTreeView.set_enable_tree_lines(True)
        self.tvwTreeView.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.tvwTreeView.set_level_indentation(2)
        self.tvwTreeView.set_tooltip_text(
            _("Displays the Hazards Analysis for the currently selected "
              "Function."))

    # pylint: disable=unused-argument
    def __do_load_panel(self, node_id: int) -> None:
        """Wrap method responds to calculate, delete, insert messages.

        This is necessary for now because the Hazards are carried around in
        the Function tree.  This method simply calls another method that
        delivers the attributes dict for the Hazards to the actual method
        that loads them into the RAMSTKTreeView().  Once the Hazards are
        split out from the Function tree, this method is not longer needed.

        :param int node_id: the hazard ID that was deleted or inserted.
            This argument is broadcast with the PyPubSub message and must
            remain with it's current spelling.
        :return: None
        :rtype: None
        """
        pub.sendMessage('request_get_function_attributes',
                        node_id=self._parent_id,
                        table='hazards')


class GeneralData(RAMSTKWorkView):
    """Display general Function attribute data in the RAMSTK Work Book.

    The Function Work View displays all the general data attributes for the
    selected Function. The attributes of a Function General Data Work View are:

    :cvar str _module: the name of the module.
    :cvar str _tablabel: the text to display on the tab's label.
    :cvar str _tabtooltip: the text to display as the tab's tooltip.

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

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'function'
    _tablabel = _("General\nData")
    _tabtooltip = _("Displays general information for the "
                    "selected Function")

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Function Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration:
            :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks = [
            self._do_request_update,
            self._do_request_update_all,
        ]
        self._lst_icons = ['save', 'save-all']
        self._lst_mnu_labels: List[str] = [
            _("Save"),
            _("Save All"),
        ]
        self._lst_tooltips = [
            _("Save changes to the currently selected Function."),
            _("Save changes to all Functions."),
        ]

        # Initialize private scalar attributes.
        self._pnlGeneralData: RAMSTKPanel = GeneralDataPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_function')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_function')

    def __make_ui(self) -> None:
        """Build the user interface for the Function General Data tab.

        :return: None
        :rtype: None
        """
        super().make_tab_label(tablabel=self._tablabel,
                               tooltip=self._tabtooltip)
        super().make_toolbuttons(icons=self._lst_icons,
                                 tooltips=self._lst_tooltips,
                                 callbacks=self._lst_callbacks)

        self.pack_end(self._pnlGeneralData, True, True, 0)
        self.show_all()

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """Request to save the currently selected Function.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_function', node_id=self._record_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """Request to save all the Functions.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_functions')


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
        :type configuration:
            :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks: List[object] = [
            self._do_request_insert,
            self._do_request_delete,
            self._do_request_calculate,
            self._do_request_update,
            self._do_request_update_all,
        ]
        self._lst_icons: List[str] = [
            'add', 'remove', 'calculate', 'save', 'save-all'
        ]
        self._lst_mnu_labels: List[str] = [
            _("Add Hazard"),
            _("Delete Selected"),
            _("Calculate HazOp"),
            _("Save Selected Hazard"),
            _("Save All Hazards"),
        ]
        self._lst_tooltips: List[str] = [
            _("Add a new hazard to the HazOps analysis."),
            _("Delete the selected hazard from the selected function."),
            _("Calculate the HazOps analysis."),
            _("Save changes to the selected hazard."),
            _("Save changes to all hazards."),
        ]

        # Initialize private scalar attributes.
        self._pnlHazOps: RAMSTKPanel = HazOpsPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.__do_set_parent, 'selected_function')

        pub.subscribe(self.do_set_cursor_active, 'succeed_calculate_hazard')
        pub.subscribe(self.do_set_cursor_active, 'succeed_delete_hazard')
        pub.subscribe(self.do_set_cursor_active, 'succeed_insert_hazard')
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_function')
        pub.subscribe(self.do_set_cursor_active_on_fail, 'fail_delete_hazard')
        pub.subscribe(self.do_set_cursor_active_on_fail, 'fail_insert_hazard')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_function')

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Request to calculate the HazOps HRI.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_fha', node_id=self._parent_id)

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete the selected hazard from the HazOps.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_delete_hazard',
                        function_id=self._parent_id,
                        node_id=self._pnlHazOps._record_id)  # pylint: disable=protected-access

    def _do_request_insert(self, __button: Gtk.ToolButton) -> None:
        """Request to insert a new hazard for the selected function.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_insert_hazard', function_id=self._parent_id)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """Request to save the selected Hazard.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_hazard', node_id=self._parent_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """Request to save all the entities in the HazOps.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_hazops')

    def __do_set_parent(self, attributes: Dict[str, Any]) -> None:
        """Set the hazard's parent ID when a function is selected.

        :param dict attributes: the function dict for the selected function ID.
        :return: None
        :rtype: None
        """
        try:
            self._revision_id = attributes['revision_id']
            self._parent_id = attributes['function_id']
        except KeyError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

    def __make_ui(self) -> None:
        """Build the user interface for the Function Hazard Analysis tab.

        :return: None
        :rtype: None
        """
        super().make_tab_label(
            tablabel=self._tablabel,
            tooltip=self._tabtooltip,
        )
        super().make_toolbuttons(
            icons=self._lst_icons,
            tooltips=self._lst_tooltips,
            callbacks=self._lst_callbacks,
        )
        super().do_build_treeview(self._pnlHazOps.tvwTreeView)

        self._pnlHazOps.do_make_panel_treeview()
        self._pnlHazOps.do_load_criticality(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_CRITICALITY)
        self._pnlHazOps.do_load_hazards(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_HAZARDS)
        self._pnlHazOps.do_load_probability(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_FAILURE_PROBABILITY)

        self.pack_end(self._pnlHazOps, True, True, 0)
        self.show_all()
