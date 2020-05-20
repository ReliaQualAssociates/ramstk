# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.allocation.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Function Work View."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox, RAMSTKEntry, RAMSTKFrame, RAMSTKLabel,
    RAMSTKTreeView, RAMSTKWorkView)


class Allocation(RAMSTKWorkView):
    """
    Display general Function attribute data in the RAMSTK Work Book.

    The Function Work View displays all the general data attributes for the
    selected Function. The attributes of a Function General Data Work View are:

    Callbacks signals in _lst_handler_id:

    +-------+-------------------------------------+
    | Index | Widget - Signal                     |
    +=======+=====================================+
    |   0   | tvw_allocation `cursor_changed`     |
    +-------+-------------------------------------+
    |   1   | tvw_allocation `button_press_event` |
    +-------+-------------------------------------+
    |   2   | tvw_allocation `edited`             |
    +-------+-------------------------------------+
    """
    # Define private class dict attributes.
    _dic_keys = {
        0: 'allocation_method_id',
        1: 'goal_measure_id',
        2: 'reliability_goal',
        3: 'hazard_rate_goal',
        4: 'mtbf_goal'
    }

    # Define private class list attributes.
    _lst_labels = [
        _("Select Allocation Method"),
        _("Select Goal Metric"),
        _("R(t) Goal"),
        _("h(t) Goal"),
        _("MTBF Goal")
    ]

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'allocation') -> None:
        """
        Initialize the Allocation Work View general data page.

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
        self._allocation_tree: treelib.Tree = treelib.Tree()
        self._system_hazard_rate: float = 0.0
        self._hazard_rate_goal: float = 0.0
        self._measure_id: int = 0
        self._method_id: int = 0
        self._mtbf_goal: float = 0.0
        self._reliability_goal: float = 0.0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbAllocationGoal: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbAllocationMethod: RAMSTKComboBox = RAMSTKComboBox()
        self.txtHazardRateGoal: RAMSTKEntry = RAMSTKEntry()
        self.txtMTBFGoal: RAMSTKEntry = RAMSTKEntry()
        self.txtReliabilityGoal: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.cmbAllocationMethod, self.cmbAllocationGoal,
            self.txtReliabilityGoal, self.txtHazardRateGoal, self.txtMTBFGoal
        ]

        self.__set_properties()
        self.__make_ui()
        self.__load_combobox()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')
        pub.subscribe(self._do_set_tree, 'succeed_get_hardware_tree')
        pub.subscribe(self._do_load_row, 'succeed_get_all_hardware_attributes')

    def __load_combobox(self):
        """
        Load the RAMSTKComboBox() widgets.

        :return: None
        :rtype: None
        """
        self.cmbAllocationGoal.do_load_combo([[_("Reliability"), 0],
                                              [_("Hazard Rate"), 1],
                                              [_("MTBF"), 2]])
        self.cmbAllocationMethod.do_load_combo(
            [[_("Equal Apportionment"), 0], [_("AGREE Apportionment"), 1],
             [_("ARINC Apportionment"), 2],
             [_("Feasibility of Objectives"), 3]])

    def __make_ui(self) -> None:
        """
        Create the Function Work View general data page.

        :return: None
        :rtype: None
        """
        # This page has the following layout:
        # +-----+---------------------------------------+
        # |  B  |                                       |
        # |  U  |                                       |
        # |  T  |             SPREAD SHEET              |
        # |  T  |                                       |
        # |  O  |                                       |
        # |  N  |                                       |
        # |  S  |                                       |
        # +-----+---------------------------------------+
        #                                      buttons -----+--> self
        #                                                   |
        #     Gtk.Fixed --->RAMSTKFrame ---+-->Gtk.HBox ----+
        #                                  |
        #  Scrollwindow --->RAMSTKFrame ---+
        #  w/ self.treeview
        # Make the buttons.
        super().make_toolbuttons(
            icons=['calculate'],
            tooltips=[
                _("Calculate the currently selected child hardware item.")
            ],
            callbacks=[self._do_request_calculate])

        _hbox = Gtk.HBox()

        _fixed = Gtk.Fixed()
        _y_pos = 5
        for _idx, _label in enumerate(self._lst_labels):
            _fixed.put(RAMSTKLabel(_label), 5, _y_pos)
            _fixed.put(self._lst_widgets[_idx], 5, _y_pos + 25)

            _y_pos += 65

        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("Allocation Goals and Method"))
        _frame.add(_fixed)

        _hbox.pack_start(_frame, False, True, 0)

        _scrollwindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                 Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.treeview)

        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("Allocation Analysis"))
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True, 0)
        self.pack_end(_hbox, True, True, 0)

        _label = RAMSTKLabel(_("Allocation"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_("Displays the Allocation analysis for the selected "
                      "hardware item."))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self) -> None:
        """
        Set the callback methods and functions.

        :return: None
        :rtype: None
        """
        for i in [
                self._lst_col_order[3], self._lst_col_order[5],
                self._lst_col_order[6], self._lst_col_order[7],
                self._lst_col_order[8], self._lst_col_order[9],
                self._lst_col_order[10], self._lst_col_order[11]
        ]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cells()
            try:
                _cell[0].connect('edited', self._on_cell_edit, i,
                                 self.treeview.get_model())
            except TypeError:
                _cell[0].connect('toggled', self._on_cell_edit, 'new text', i,
                                 self.treeview.get_model())

        self.cmbAllocationMethod.dic_handler_id[
            'changed'] = self.cmbAllocationMethod.connect(
                'changed', self._on_combo_changed, 0)
        self.cmbAllocationGoal.dic_handler_id[
            'changed'] = self.cmbAllocationGoal.connect(
                'changed', self._on_combo_changed, 1)
        self.txtReliabilityGoal.dic_handler_id[
            'changed'] = self.txtReliabilityGoal.connect(
                'focus_out_event', self._on_focus_out, 2)
        self.txtHazardRateGoal.dic_handler_id[
            'changed'] = self.txtHazardRateGoal.connect(
                'focus_out_event', self._on_focus_out, 3)
        self.txtMTBFGoal.dic_handler_id['changed'] = self.txtMTBFGoal.connect(
            'focus_out_event', self._on_focus_out, 4)

    def __set_properties(self) -> None:
        """
        Set the properties of the General Data Work View and widgets.

        :return: None
        :rtype: None
        """
        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.treeview.set_tooltip_text(
            _("Displays the Allocation Analysis for the currently selected "
              "Hardware item."))
        self.cmbAllocationGoal.do_set_properties(tooltip=_(
            "Selects the goal measure for the selected hardware assembly."))
        self.cmbAllocationMethod.do_set_properties(tooltip=_(
            "Selects the method for allocating the reliability goal for "
            "the selected hardware assembly."))
        self.txtHazardRateGoal.do_set_properties(
            width=125,
            tooltip=("Displays the hazard rate goal for the selected hardware "
                     "item."))
        self.txtMTBFGoal.do_set_properties(
            width=125,
            tooltip=_(
                "Displays the MTBF goal for the selected hardware item."))
        self.txtReliabilityGoal.do_set_properties(
            width=125,
            tooltip=_(
                "Displays the reliability goal for the selected hardware "
                "item."))

    def _do_change_row(self, treeview: RAMSTKTreeView) -> None:
        """
        Handle events for the Allocation Tree View RAMSTKTreeView().

        This method is called whenever a Tree View row is activated.

        :param treeview: the Allocation RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.RAMSTKTreeView`
        :return: None
        :rtype: None
        """
        treeview.handler_block(self._lst_handler_id[0])

        (_model, _row) = treeview.get_selection().get_selected()
        try:
            self._record_id = _model.get_value(_row, 1)
        except TypeError:
            self._record_id = -1

        treeview.handler_unblock(self._lst_handler_id[0])

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

        self.cmbAllocationMethod.do_update(0)
        self.cmbAllocationGoal.do_update(0)
        self.txtHazardRateGoal.do_update("")
        self.txtMTBFGoal.do_update("")
        self.txtReliabilityGoal.do_update("")

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Allocation page.

        :param dict attributes: the attributes dict for the selected
            Hardware item.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._measure_id = attributes['goal_measure_id']
        self._method_id = attributes['allocation_method_id']
        self._hazard_rate_goal = attributes['hazard_rate_goal']
        self._mtbf_goal = attributes['mtbf_goal']
        self._reliability_goal = attributes['reliability_goal']
        self._system_hazard_rate = attributes['hazard_rate_logistics']

        self.cmbAllocationMethod.do_update(self._method_id)
        self.cmbAllocationGoal.do_update(self._measure_id)
        self.txtReliabilityGoal.do_update(
            str(self.fmt.format(self._reliability_goal)))
        self.txtHazardRateGoal.do_update(
            str(self.fmt.format(self._hazard_rate_goal)))
        self.txtMTBFGoal.do_update(str(self.fmt.format(self._mtbf_goal)))

        self._do_set_sensitive()

        if self._record_id > 0:
            self._do_load_tree()

    # noinspection PyDeepBugsSwappedArgs
    def _do_load_row(self, attributes: Dict[str, Any]) -> None:
        """
        Load the data into a row.

        :param dict attributes:
        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()

        _data = []
        for _key in self.treeview.korder:
            if _key == 'dict':
                _data.append(str(attributes))
            else:
                _data.append(attributes[_key])

        # Only load Hardware items that are immediate children of the
        # selected Hardware item and prevent loading the selected Hardware item
        # in the Allocation worksheet.  This method will respond to any
        # successful grabs of all the hardware attributes even when
        # requested by other modules.
        if _data[0] == self._record_id and not _data[1] == self._record_id:
            _model.append(None, _data)

    def _do_load_tree(self) -> None:
        """
        Load the Allocation RAMSTKTreeView() with allocation data.

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _model.clear()

        for _node in self._allocation_tree.children(self._record_id):
            _node_id = _node.data['hardware'].get_attributes()['hardware_id']
            pub.sendMessage('request_get_all_hardware_attributes',
                            node_id=_node_id)

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """
        Calculate the Allocation reliability metrics.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        self.do_set_cursor_busy()
        pub.sendMessage('request_allocate_reliability',
                        node_id=self._record_id)
        self.do_set_cursor_active(node_id=self._record_id)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save the currently selected Function.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor_busy()
        pub.sendMessage('request_update_hardware', node_id=self._record_id)
        self.do_set_cursor_active(node_id=self._record_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the Functions.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.do_set_cursor_busy()
        pub.sendMessage('request_update_all_hardware')
        self.do_set_cursor_active(node_id=self._record_id)

    def _do_set_sensitive(self) -> None:
        """
        Set widget sensitivity as needed for the selected R(t) goal.

        :return: None
        :rtype: None
        """
        if self._measure_id == 0:  # Nothing selected.
            self.txtReliabilityGoal.props.editable = 0
            self.txtReliabilityGoal.set_sensitive(0)
            self.txtMTBFGoal.props.editable = 0
            self.txtMTBFGoal.set_sensitive(0)
            self.txtHazardRateGoal.props.editable = 0
            self.txtHazardRateGoal.set_sensitive(0)
        elif self._measure_id == 1:  # Expressed as reliability.
            self.txtReliabilityGoal.props.editable = 1
            self.txtReliabilityGoal.set_sensitive(1)
            self.txtReliabilityGoal.set_text(
                str(self.fmt.format(self._reliability_goal)), )
            self.txtMTBFGoal.props.editable = 0
            self.txtMTBFGoal.set_sensitive(0)
            self.txtMTBFGoal.set_text(str(self.fmt.format(self._mtbf_goal)))
            self.txtHazardRateGoal.props.editable = 0
            self.txtHazardRateGoal.set_sensitive(0)
            self.txtHazardRateGoal.set_text(
                str(self.fmt.format(self._hazard_rate_goal)), )
        elif self._measure_id == 2:  # Expressed as a hazard rate.
            self.txtReliabilityGoal.props.editable = 0
            self.txtReliabilityGoal.set_sensitive(0)
            self.txtReliabilityGoal.set_text(
                str(self.fmt.format(self._reliability_goal)), )
            self.txtMTBFGoal.props.editable = 0
            self.txtMTBFGoal.set_sensitive(0)
            self.txtMTBFGoal.set_text(str(self.fmt.format(self._mtbf_goal)))
            self.txtHazardRateGoal.props.editable = 1
            self.txtHazardRateGoal.set_sensitive(1)
            self.txtHazardRateGoal.set_text(
                str(self.fmt.format(self._hazard_rate_goal)), )
        elif self._measure_id == 3:  # Expressed as an MTBF.
            self.txtReliabilityGoal.props.editable = 0
            self.txtReliabilityGoal.set_sensitive(0)
            self.txtReliabilityGoal.set_text(
                str(self.fmt.format(self._reliability_goal)), )
            self.txtMTBFGoal.props.editable = 1
            self.txtMTBFGoal.set_sensitive(1)
            self.txtMTBFGoal.set_text(str(self.fmt.format(self._mtbf_goal)))
            self.txtHazardRateGoal.props.editable = 0
            self.txtHazardRateGoal.set_sensitive(0)
            self.txtHazardRateGoal.set_text(
                str(self.fmt.format(self._hazard_rate_goal)), )

    def _do_set_tree(self, dmtree: treelib.Tree) -> None:
        """
        Sets the _allocation_tree equal to the datamanger Hardware tree.

        :param dmtree: the Hardware datamanger treelib.Tree() of data.
        :type dmtree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self._allocation_tree = dmtree

    # pylint: disable=unused-argument
    def _on_button_press(self, __treeview: RAMSTKTreeView,
                         event: Gdk.Event) -> None:
        """
        Handle mouse clicks on the Allocation Work View RAMSTKTreeView().

        :param __treeview: the Allocation TreeView RAMSTKTreeView().
        :type __treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`.
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
        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            RAMSTKWorkView.on_button_press(
                self,
                event,
                icons=['calculate'],
                labels=[_("Calculate")],
                callbacks=[self._do_request_calculate])

    def _on_cell_edit(self, __cell: Gtk.CellRenderer, path: str, new_text: str,
                      position: int, model: Gtk.TreeModel) -> None:
        """
        Handle edits of the Allocation Work View RAMSTKTreeview().

        :param Gtk.CellRenderer __cell: the Gtk.CellRenderer() that was edited.
        :param str path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
                             Gtk.CellRenderer().
        :param Gtk.TreeModel model: the Gtk.TreeModel() the Gtk.CellRenderer()
                                    belongs to.
        :return: None
        :rtype: None
        """
        _dic_keys = {
            3: "included",
            4: "n_sub_systems",
            5: "n_sub_elements",
            6: "mission_time",
            7: "duty_cycle",
            8: "int_factor",
            9: "soa_factor",
            10: "op_time_factor",
            11: "env_factor"
        }
        try:
            _key = _dic_keys[self._lst_col_order[position]]
        except KeyError:
            _key = ''

        if not self.treeview.do_edit_cell(__cell, path, new_text, position,
                                          model):
            pub.sendMessage("mvw_editing_allocation",
                            node_id=[self._record_id, 1],
                            package={_key: new_text})

    def _on_combo_changed(self, combo: RAMSTKComboBox, index: int) -> None:
        """
        Respond to Gtk.ComboBox() 'changed' signals.

        :param Gtk.ComboBox combo: the Gtk.ComboBox() that called this method.
        :param int index: the index in the handler ID list oc the callback
            signal associated with the Gtk.ComboBox() that called this method.
        :return: None
        :rtype: None
        """
        # TODO: See issue #310.
        _package = super().on_combo_changed(combo, index,
                                            'wvw_editing_hardware')
        _new_text = list(_package.values())[0]

        # Key is the allocation method ID:
        #   1: Equal apportionment
        #   2: AGREE apportionment
        #   3: ARINC apportionment
        #   4: Feasibility of Objectives
        # Value is the list of columns that should be made visible and/or
        # editable for the selected method.
        _dic_visible = {
            1: [2, 3, 4, 6, 14, 15, 16, 17, 18, 19],
            2: [2, 3, 4, 5, 6, 7, 12, 14, 15, 16, 17, 18, 19],
            3: [2, 3, 12, 14, 15, 16, 17, 18, 19],
            4: [2, 3, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        }
        _dic_editable = {
            1: [3, 6],
            2: [3, 5, 6, 7],
            3: [3],
            4: [3, 8, 9, 10, 11]
        }

        if index == 0:
            self._method_id = _new_text
        elif index == 1:
            self._measure_id = _new_text

        try:
            _visible = _dic_visible[self._method_id]
        except KeyError:
            _visible = []
        try:
            _editable = _dic_editable[self._method_id]
        except KeyError:
            _editable = []

        self.treeview.do_set_visible_columns(visible=_visible)
        # self.treeview.do_set_editable_columns(editable=_editable)

        self._do_set_sensitive()

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
        # TODO: See issues #310.
        _package = super().on_focus_out(entry, index, 'wvw_editing_hardware')

        _new_text = list(_package.values())[0]

        if index == 2:
            self._reliability_goal = _new_text
        elif index == 3:
            self._hazard_rate_goal = _new_text
        elif index == 4:
            self._mtbf_goal = _new_text

        pub.sendMessage('request_calculate_allocation_goals')
