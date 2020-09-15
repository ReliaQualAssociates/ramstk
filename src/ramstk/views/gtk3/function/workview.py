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
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton, RAMSTKEntry, RAMSTKFrame, RAMSTKTextView, RAMSTKWorkView
)


class GeneralData(RAMSTKWorkView):
    """
    Display general Function attribute data in the RAMSTK Work Book.

    The Function Work View displays all the general data attributes for the
    selected Function. The attributes of a Function General Data Work View are:

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

    # Define private dict class attributes.
    _dic_keys: Dict[int, List[str]] = {
        0: ['function_code', 'string'],
        1: ['name', 'string'],
        2: ['remarks', 'string'],
        3: 'safety_critical'
    }

    # Define private list class attributes.
    _lst_labels: List[str] = [
        _("Function Code:"),
        _("Function Name:"),
        _("Remarks:"), ''
    ]
    _lst_title = [_("General Information"), ""]

    # Define private scalar class attributes.
    _module: str = 'function'
    _tablabel = _("General\nData")
    _tabtooltip = _("Displays general information for the "
                    "selected Function")

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize the Function Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks = [
            self._do_request_update,
            self._do_request_update_all,
        ]
        self._lst_icons = ['save', 'save-all']
        self._lst_tooltips = [
            _("Save changes to the currently selected "
              "Function."),
            _("Save changes to all Functions."),
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.chkSafetyCritical: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Function is safety critical."))
        self.txtCode: RAMSTKEntry = RAMSTKEntry()
        self.txtName: RAMSTKEntry = RAMSTKEntry()
        self.txtRemarks: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        self._dic_switch: Dict[str, Union[object, str]] = {
            'function_code': [self.txtCode.do_update, 'changed'],
            'name': [self.txtName.do_update, 'changed'],
            'remarks': [self.txtRemarks.do_update, 'changed'],
            'safety_critical': [self.chkSafetyCritical.do_update, 'toggled']
        }

        self._lst_widgets = [
            self.txtCode, self.txtName, self.txtRemarks, self.chkSafetyCritical
        ]

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'request_clear_workviews')
        pub.subscribe(self._do_load_page, 'selected_function')

        pub.subscribe(self.on_edit, 'mvw_editing_function')
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_function')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_function')

    def __make_ui(self) -> None:
        """
        Build the user interface for the Function General Data tab.

        :return: None
        :rtype: None
        """
        self.make_tab_label(
            tablabel=self._tablabel,
            tooltip=self._tabtooltip,
        )
        self.make_toolbuttons(
            icons=self._lst_icons,
            tooltips=self._lst_tooltips,
            callbacks=self._lst_callbacks,
        )

        _frame: RAMSTKFrame = super().do_make_panel_fixed(
            start=0,
            end=len(self._lst_labels),
        )
        _frame.do_set_properties(
            bold=True,
            title=self._lst_title[0],
        )
        self.pack_end(_frame, True, True, 0)

        self.show_all()

    def __set_callbacks(self) -> None:
        """
        Set the callback methods and functions.

        :return: None
        :rtype: None
        """
        self.txtCode.dic_handler_id['changed'] = (self.txtCode.connect(
            'focus-out-event', self._on_focus_out, 0))
        self.txtName.dic_handler_id['changed'] = (self.txtName.connect(
            'focus-out-event', self._on_focus_out, 1))
        self.txtRemarks.dic_handler_id['changed'] = (
            self.txtRemarks.do_get_buffer().connect('changed',
                                                    self._on_focus_out, None,
                                                    2))
        self.chkSafetyCritical.dic_handler_id['toggled'] = (
            self.chkSafetyCritical.connect('toggled', self._on_toggled, 3))

    def __set_properties(self) -> None:
        """
        Set the properties of the General Data Work View and widgets.

        :return: None
        :rtype: None
        """
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

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.txtCode.do_update('', signal='changed')
        self.txtName.do_update('', signal='changed')
        self.txtRemarks.do_update('', signal='changed')
        self.chkSafetyCritical.do_update(False, signal='toggled')

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Function General Data page.

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

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save the currently selected Function.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_function', node_id=self._record_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the Functions.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_functions')

    # pylint: disable=unused-argument
    def _on_focus_out(self, entry: Gtk.Entry, __event: Gdk.EventFocus,
                      index: int) -> None:
        """
        Handle changes made in RAMSTKEntry() and RAMSTKTextView() widgets.

        This method is called by:

            * RAMSTKEntry() 'focus-out-event' signal
            * RAMSTKTextView() 'changed' signal

        This method sends the 'wvw_editing_function' message.

        :param entry: the Gtk.Entry() that called the method.
        :type entry: :class:`Gtk.Entry`
        :param __event: the Gdk.EventFocus that triggered the signal.
        :type __event: :class:`Gdk.EventFocus`
        :param int index: the position in the Function class Gtk.TreeModel()
            associated with the data from the calling Gtk.Entry().
        :return: None
        :rtype: None
        """
        super().on_focus_out(entry, index, 'wvw_editing_function')

    def _on_toggled(self, checkbutton: RAMSTKCheckButton, index: int) -> None:
        """
        Handle RAMSTKCheckButton() 'toggle' signals.

        :param checkbutton: the RAMSTKCheckButton() that called this method.
        :type: :class:`ramstk.gui.gtk.ramstk.Button.RAMSTKCheckButton`
        :param int index: the index in the signal handler ID list.
        :return: None
        :rtype: None
        """
        super().on_toggled(checkbutton, index, message='wvw_editing_function')


class HazOps(RAMSTKWorkView):
    """
    Display HazOps attribute data in the Work Book.

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
    _dic_keys: Dict[int, str] = {
        3: 'potential_hazard',
        4: 'potential_cause',
        5: 'assembly_effect',
        6: 'assembly_severity',
        7: 'assembly_probability',
        9: 'assembly_mitigation',
        10: 'assembly_severity_f',
        11: 'assembly_probability_f',
        13: 'system_effect',
        14: 'system_severity',
        15: 'system_probability',
        17: 'system_mitigation',
        18: 'system_severity_f',
        19: 'system_probability_f',
        21: 'remarks'
    }

    # Define private list class attributes.
    _lst_labels: List[str] = []
    _lst_title: List[str] = ["", _("HazOps Analysis")]

    # Define private scalar class attributes.
    _module: str = 'hazard'
    _tablabel: str = _("HazOps")
    _tabtooltip: str = _("Displays the HazOps analysis for the "
                         "selected function.")

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize the Work View for the HazOps.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks: List[object] = [
            self._do_request_insert, self._do_request_delete,
            self._do_request_calculate, self._do_request_update,
            self._do_request_update_all
        ]
        self._lst_icons: List[str] = [
            'add', 'remove', 'calculate', 'save', 'save-all'
        ]
        self._lst_mnu_labels: List[str] = [
            _("Add Hazard"),
            _("Delete Selected"),
            _("Calculate HazOp"),
            _("Save Selected Hazard"),
            _("Save All Hazards")
        ]
        self._lst_tooltips: List[str] = [
            _("Add a new hazard to the HazOps analysis."),
            _("Delete the selected hazard from the selected function."),
            _("Calculate the HazOps analysis."),
            _("Save changes to the selected hazard."),
            _("Save changes to all hazards.")
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__set_properties()
        super().make_ui_with_treeview()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.__do_load_tree, 'succeed_calculate_hazard')
        pub.subscribe(self.__do_load_tree, 'succeed_delete_hazard')
        pub.subscribe(self.__do_load_tree, 'succeed_insert_hazard')
        pub.subscribe(self.__do_set_parent, 'selected_function')
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_load_tree, 'succeed_get_hazards_attributes')

        pub.subscribe(self.do_set_cursor_active, 'succeed_calculate_hazard')
        pub.subscribe(self.do_set_cursor_active, 'succeed_delete_hazard')
        pub.subscribe(self.do_set_cursor_active, 'succeed_insert_hazard')
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_function')
        pub.subscribe(self.do_set_cursor_active_on_fail, 'fail_delete_hazard')
        pub.subscribe(self.do_set_cursor_active_on_fail, 'fail_insert_hazard')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_function')

    # pylint: disable=unused-argument
    def __do_load_tree(self, node_id: int) -> None:
        """
        Wrapper method responds to calculate, delete, insert messages.

        :param int node_id: the hazard ID that was deleted or inserted.
            This argument is broadcast with the PyPubSub message and must
            remain with it's current spelling.
        :return: None
        :rtype: None
        """
        pub.sendMessage('request_get_function_attributes',
                        node_id=self._parent_id,
                        table='hazards')

    def __do_set_parent(self, attributes: Dict[str, Any]) -> None:
        """
        Set the hazard's parent ID when a function is selected.

        :param dict attributes: the function dict for the selected function ID.
        :return: None
        :rtype: None
        """
        try:
            self._revision_id = attributes['revision_id']
            self._parent_id = attributes['function_id']
        except KeyError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

    def __set_callbacks(self) -> None:
        """
        Set the callback functions and methods for the HazOps widgets.

        :return: None
        :rtype: None
        """
        for i in self._lst_col_order[3:]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cells()
            try:
                _cell[0].connect('edited', self._on_cell_edit, i)
            except TypeError:
                _cell[0].connect('toggled', self._on_cell_edit, 'new text', i)

    def __set_properties(self) -> None:
        """
        Set the properties of the HazOps widgets.

        :return: None
        :rtype: None
        """
        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.treeview.set_tooltip_text(
            _("Displays the HazOps Analysis for the currently "
              "selected Hardware item."))

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _columns = self.treeview.get_columns()
        for _column in _columns:
            self.treeview.remove_column(_column)

        _model.clear()

    def _do_load_hazards(self, hazards: Dict[Any, Any]) -> None:
        """
        Load the Gtk.CellRendererCombos() containing hazards.

        :param dict hazards: the dict containing the hazards and hazard types
            to be considered.
        :return: None
        :rtype: None
        """
        _model = self._get_cell_model(3)
        for _key in hazards:
            _hazard = '{0:s}, {1:s}'.format(hazards[_key][0], hazards[_key][1])
            _model.append((_hazard, ))

    def _do_load_probability(self, probability: List[str]) -> None:
        """
        Load the Gtk.CellRendererCombos() containing probabilities.

        :param list probability: the list of hazard probabilities.
        :return: None
        :rtype: None
        """
        for i in [7, 11, 15, 19]:
            _model = self._get_cell_model(i)
            for _item in probability:
                _model.append((_item[0], ))

    def _do_load_severity(self, severity: Dict[Any, Any]) -> None:
        """
        Load the Gtk.CellRendererCombo() containing severities.

        :param dict severity: the dict containing the hazard severity
            categories and values.
        :return: None
        :rtype: None
        """
        for i in [6, 10, 14, 18]:
            _model = self._get_cell_model(i)
            for _key in severity:
                _severity = severity[_key][1]
                _model.append((_severity, ))

    def _do_load_tree(self, attributes: Dict[int, Any]) -> None:
        """
        Load the Hazard Analysis Work View's Gtk.TreeModel.

        :param dict attributes: the hazards dict for the selected function
            ID, if any.
        :return: None
        :rtype: None
        """
        _model: Gtk.ListStore = self.treeview.get_model()
        _model.clear()

        if attributes is not None:
            _hazards = list(attributes.values())
            for _hazard in _hazards:
                _attributes = list(_hazard.get_attributes().values())
                _attributes.append('')
                try:
                    # noinspection PyDeepBugsSwappedArgs
                    _model.append(None, _attributes)
                except ValueError as _error:
                    self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

            super().do_expand_tree()

    def _get_cell_model(self, column: int) -> Gtk.TreeModel:
        """
        Retrieve the Gtk.CellRendererCombo() Gtk.TreeModel().

        :param int column: the column number to retrieve the cell from.
        :return: _model
        :rtype: :class:`Gtk.TreeModel`
        """
        _model: Gtk.TreeModel = None
        _column = self.treeview.get_column(column)

        if _column is not None:
            _cell = _column.get_cells()[0]
            _model = _cell.get_property('model')
            _model.clear()

        return _model

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """
        Request to calculate the HazOps HRI.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_fha', node_id=self._parent_id)

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """
        Request to delete the selected hazard from the HazOps.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_delete_hazard',
                        function_id=self._parent_id,
                        node_id=self._record_id)

    def _do_request_insert(self, __button: Gtk.ToolButton) -> None:
        """
        Request to insert a new hazard for the selected function.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_insert_hazard', function_id=self._parent_id)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save the selected Hazard.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_hazard', node_id=self._parent_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the entities in the HazOps.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_hazops')

    def _on_cell_edit(self, cell: Gtk.CellRenderer, path: str, new_text: str,
                      position: int) -> None:
        """
        Handle edits of the HazOps Work View RAMSTKTreeview().

        :param cell: the Gtk.CellRenderer() that was edited.
        :type cell: :class:`Gtk.CellRenderer`
        :param str path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
                             Gtk.CellRenderer().
        :return: None
        :rtype: None
        """
        try:
            _key = self._dic_keys[self._lst_col_order[position]]
        except KeyError as _error:
            _key = ''
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        if not self.treeview.do_edit_cell(cell, path, new_text, position):
            pub.sendMessage('wvw_editing_hazard',
                            node_id=[self._parent_id, self._record_id, ''],
                            package={_key: new_text})

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """
        Handle events for the HazOps Tree View RAMSTKTreeView().

        This method is called whenever a Tree View row is activated.

        :param selection: the HazOps RAMSTKTreeview Gtk.TreeSelection().
        :type selection: :class:`Gtk.TreeSelection`
        :return: None
        :rtype: None
        """
        selection.handler_block(self.treeview.dic_handler_id['changed'])

        _model, _row = selection.get_selected()
        try:
            self._record_id = _model.get_value(_row, 2)
        except TypeError as _error:
            self._record_id = -1
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        selection.handler_unblock(self.treeview.dic_handler_id['changed'])

    def do_load_combobox(self, hazards: Dict[Any, Any],
                         severity: Dict[Any, Any], probability: List[str]) -> \
            None:
        """
        Load the Gtk.CellRendererCombo() widgets.

        :param dict hazards: the dict containing the hazards and hazard types
            to be considered.
        :param dict severity: the dict containing the hazard severity
            categories and values.
        :param list probability: the list of hazard probabilities.
        :return: None
        :rtype: None
        """
        # Load the potential hazards into the Gtk.CellRendererCombo().
        self._do_load_hazards(hazards)

        # Load the severity classes into the Gtk.CellRendererCombo().
        self._do_load_severity(severity)

        # Load the failure probabilities into the Gtk.CellRendererCombo().
        self._do_load_probability(probability)
