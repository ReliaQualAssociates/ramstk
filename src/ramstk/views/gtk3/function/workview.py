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
    RAMSTKCheckButton, RAMSTKEntry, RAMSTKFrame, RAMSTKLabel, RAMSTKTextView,
    RAMSTKTreeView, RAMSTKWorkView, do_make_buttonbox)


class GeneralData(RAMSTKWorkView):
    """
    Display general Function attribute data in the RAMSTK Work Book.

    The Function Work View displays all the general data attributes for the
    selected Function. The attributes of a Function General Data Work View are:
    """

    # Define private dict class attributes.
    _dic_keys = {
        0: 'function_code',
        1: 'name',
        2: 'remarks',
        3: 'safety_critical'
    }

    # Define private list class attributes.
    _lst_labels = [_("Function Code:"), _("Function Name:"), _("Remarks:")]

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'function') -> None:
        """
        Initialize the Function Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger, module)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.chkSafetyCritical = RAMSTKCheckButton(
            label=_("Function is safety critical."))
        self.txtCode = RAMSTKEntry()
        self.txtName = RAMSTKEntry()
        self.txtRemarks = RAMSTKTextView(Gtk.TextBuffer())

        self._dic_switch: Dict[str, Union[object, str]] = {
            'function_code': [self.txtCode.do_update, 'changed'],
            'name': [self.txtName.do_update, 'changed'],
            'remarks': [self.txtRemarks.do_update, 'changed'],
            'safety_critical': [self.chkSafetyCritical.do_update, 'toggled']
        }

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_edit, 'mvw_editing_function')

        pub.subscribe(self._do_clear_page, 'request_clear_workviews')
        pub.subscribe(self._do_load_page, 'selected_function')

    def __make_ui(self) -> None:
        """
        Create the Function Work View general data page.

        :return: None
        :rtype: None
        """
        (_x_pos, _y_pos, _fixed) = super().make_ui(icons=[],
                                                   tooltips=[],
                                                   callbacks=[])

        _fixed.put(self.txtRemarks.scrollwindow, _x_pos, _y_pos[2])
        _fixed.put(self.chkSafetyCritical, 5, _y_pos[2] + 110)

        _label = RAMSTKLabel(_("General\nData"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(
                "Displays general information for the selected Function"))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

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
                                         signal='changed')

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save the currently selected Function.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_function', node_id=self._record_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the Functions.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_functions')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _on_focus_out(
            self,
            entry: Gtk.Entry,
            __event: Gdk.EventFocus,  # pylint: disable=unused-argument
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
        try:
            _key = self._dic_keys[index]
        except KeyError as _error:
            _key = ''
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        entry.handler_block(entry.dic_handler_id['changed'])

        try:
            if index == 2:
                _new_text: str = self.txtRemarks.do_get_text()
            else:
                _new_text = str(entry.get_text())
        except ValueError as _error:
            _new_text = ''
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        pub.sendMessage('wvw_editing_function',
                        node_id=[self._record_id, -1],
                        package={_key: _new_text})

        entry.handler_unblock(entry.dic_handler_id['changed'])

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

    :ivar int _hazard_id: the ID of the currently selected hazard.
    """
    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'hazard') -> None:
        """
        Initialize the Work View for the HazOps.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger, module)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self.__do_set_parent, 'selected_function')
        pub.subscribe(self.__do_load_tree, 'succeed_calculate_hazard')
        pub.subscribe(self.__do_load_tree, 'succeed_delete_hazard')
        pub.subscribe(self._do_load_tree, 'succeed_get_hazards_attributes')
        pub.subscribe(self.__do_load_tree, 'succeed_insert_hazard')

        # These subscriptions cause the cursor to change to/from busy when
        # certain actions are performed.
        pub.subscribe(self.do_set_cursor_active, 'succeed_calculate_hazard')
        pub.subscribe(self.do_set_cursor_active, 'succeed_delete_hazard')
        pub.subscribe(self.do_set_cursor_active, 'succeed_insert_hazard')
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_function')
        pub.subscribe(self._do_set_cursor_active, 'fail_insert_hazard')
        pub.subscribe(self._do_set_cursor_active, 'fail_delete_hazard')
        pub.subscribe(self._do_set_cursor_active, 'fail_update_function')

    # pylint: disable=unused-argument
    def __do_load_tree(self, node_id: int) -> None:
        """
        Wrapper method responds to calculate, delete, insert messages.

        :param int node_id: the hazard ID that was deleted or inserted.
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

    def __make_ui(self) -> None:
        """
        Make the HazOps RAMSTKTreeview().

        :return: None
        :rtype: None
        """
        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        _scrolledwindow.add_with_viewport(
            do_make_buttonbox(
                self,
                icons=['calculate', 'add', 'remove'],
                tooltips=[
                    _("Calculate the HazOps analysis."),
                    _("Add a hazard to the HazOps analysis."),
                    _("Remove the selected hazard and all associated data "
                      "from the HazOps analysis.")
                ],
                callbacks=[
                    self._do_request_calculate, self._do_request_insert,
                    self._do_request_delete
                ]))
        self.pack_start(_scrolledwindow, False, False, 0)

        _scrollwindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                 Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.treeview)

        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("HazOps Analysis"))
        _frame.add(_scrollwindow)

        self.pack_end(_frame, True, True, 0)

        _label = RAMSTKLabel(_("HazOps"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(
                "Displays the HazOps analysis for the selected function."))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

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
                _cell[0].connect('edited', self._on_cell_edit, i,
                                 self.treeview.get_model())
            except TypeError:
                _cell[0].connect('toggled', self._on_cell_edit, 'new text', i,
                                 self.treeview.get_model())

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

            self.do_expand_tree()

    # pylint: disable=unused-argument
    def _do_set_cursor_active(self, error_message: str) -> None:
        """
        Returns the cursor to the active cursor on a fail message.

        The meta-class do_set_active() method expects node_id as the data
        package, but the fail messages carry an error message as the package.
        This method simply calls the meta-class method in response to fail
        messages.

        :param str error_message: the error message associated with the fail
            message.
        :return: None
        :rtype: None
        """
        self.do_set_cursor_active(node_id=self._record_id)

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
        self.do_set_cursor_busy()
        pub.sendMessage('request_calculate_fha', node_id=self._parent_id)

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """
        Request to delete the selected hazard from the HazOps.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.do_set_cursor_busy()
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
        self.do_set_cursor_busy()
        pub.sendMessage('request_insert_hazard', function_id=self._parent_id)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save the selected Hazard.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.do_set_cursor_busy()
        pub.sendMessage('request_update_hazard', node_id=self._parent_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the entities in the HazOps.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.do_set_cursor_busy()
        pub.sendMessage('request_update_all_hazops')

    def _on_button_press(self, treeview: RAMSTKTreeView,
                         event: Gdk.Event) -> None:
        """
        Handle mouse clicks on the HazOps Work View RAMSTKTreeView().

        :param treeview: the HazOps TreeView RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`.
        :param event: the Gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backwards
                      * 8 =
                      * 9 =

        :type event: :class:`Gdk.Event`.
        :return: None
        :rtype: None
        """
        treeview.handler_block(treeview.dic_handler_id['button-press'])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            RAMSTKWorkView.on_button_press(
                self,
                event,
                icons=['add', 'remove', 'calculate'],
                labels=[
                    _("Add Hazard"),
                    _("Remove Selected Hazard"),
                    _("Calculate HazOp"),
                ],
                callbacks=[
                    self._do_request_insert_sibling,
                    self._do_request_delete,
                    self._do_request_calculate,
                ],
            )

        treeview.handler_unblock(treeview.dic_handler_id['button-press'])

    # pylint: disable=unused-argument
    def _on_cell_edit(self, __cell: Gtk.CellRenderer, path: str, new_text: str,
                      position: int, model: Gtk.TreeModel) -> None:
        """
        Handle edits of the HazOps Work View RAMSTKTreeview().

        :param __cell: the Gtk.CellRenderer() that was edited.
        :type __cell: :class:`Gtk.CellRenderer`
        :param str path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
                             Gtk.CellRenderer().
        :param model: the Gtk.TreeModel() the Gtk.CellRenderer() belongs to.
        :type model: :class:`Gtk.TreeModel`
        :return: None
        :rtype: None
        """
        _dic_keys = {
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
        try:
            _key = _dic_keys[self._lst_col_order[position]]
        except KeyError as _error:
            _key = ''
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        if not self.treeview.do_edit_cell(__cell, path, new_text, position):
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
