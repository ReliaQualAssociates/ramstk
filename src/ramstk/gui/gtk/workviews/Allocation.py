# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.Allocation.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Allocation Work View."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, Gdk, Gtk
from .WorkView import RAMSTKWorkView


class Allocation(RAMSTKWorkView):
    """
    Display Allocation attribute data in the Work Book.

    The WorkView displays all the attributes for the Allocation. The
    attributes of a Allocation Work View are:

    :ivar _lst_handler_id: list containing the ID's of the callback
                           signals for each Gtk.Widget() associated with
                           an editable Allocation attribute.

    +-------+-------------------------------------------+
    | Index | Widget - Signal                           |
    +=======+===========================================+
    |   0   | tvw_allocation `cursor_changed`           |
    +-------+-------------------------------------------+
    |   1   | tvw_allocation `button_press_event`       |
    +-------+-------------------------------------------+
    |   2   | tvw_allocation `edited`                   |
    +-------+-------------------------------------------+
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Allocation.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKWorkView.__init__(self, controller, module='Allocation')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._parent_id = None
        self._allocation_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        _bg_color = '#FFFFFF'
        _fg_color = '#000000'
        _fmt_file = (
            controller.RAMSTK_CONFIGURATION.RAMSTK_CONF_DIR + '/layouts/' +
            controller.RAMSTK_CONFIGURATION.RAMSTK_FORMAT_FILE['allocation'])
        _fmt_path = "/root/tree[@name='Allocation']/column"
        _tooltip = _(u"Displays the Allocation Analysis for the "
                     u"currently selected Hardware item.")

        self.treeview = ramstk.RAMSTKTreeView(
            _fmt_path, 0, _fmt_file, _bg_color, _fg_color, pixbuf=False)
        self._lst_col_order = self.treeview.order
        self.treeview.set_tooltip_text(_tooltip)

        self.cmbAllocationGoal = ramstk.RAMSTKComboBox(
            tooltip=_(
                u"Selects the goal measure for the selected hardware assembly."
            ))
        self.cmbAllocationMethod = ramstk.RAMSTKComboBox(
            tooltip=_(
                u"Selects the method for allocating the reliability goal for "
                u"the selected hardware assembly."))
        self.txtHazardRateGoal = ramstk.RAMSTKEntry(
            width=125,
            tooltip=(
                u"Displays the hazard rate goal for the selected hardware "
                u"item."))
        self.txtMTBFGoal = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(
                u"Displays the MTBF goal for the selected hardware item."))
        self.txtReliabilityGoal = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(
                u"Displays the reliability goal for the selected hardware "
                u"item."))

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_select, 'selectedHardware')
        pub.subscribe(self._do_clear_page, 'closedProgram')

    def __make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the Gtk.ButtonBox() for the Allocation class Work View.

        :return: _buttonbox; the Gtk.ButtonBox() for the Allocation Work View.
        :rtype: :class:`Gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Calculate the currently selected child hardware item.")
        ]

        _callbacks = [self._do_request_calculate]

        _icons = ['calculate']

        _buttonbox = ramstk.do_make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)

        return _buttonbox

    def __make_goalbox(self):
        """
        Make the Allocation methods and goal-setting container.

        :return: a Gtk.Frame() containing the widgets used to select the
                 allocation method and goals.
        :rtype: :class:`Gtk.Frame`
        """
        # Load the method and goal comboboxes.
        self.cmbAllocationGoal.do_load_combo([[_(u"Reliability"), 0],
                                              [_(u"Hazard Rate"), 1],
                                              [_(u"MTBF"), 2]])
        self.cmbAllocationMethod.do_load_combo(
            [[_(u"Equal Apportionment"), 0], [_(u"AGREE Apportionment"), 1],
             [_(u"ARINC Apportionment"), 2],
             [_(u"Feasibility of Objectives"), 3]])

        _fixed = Gtk.Fixed()

        _fixed.put(ramstk.RAMSTKLabel(_(u"Select Allocation Method")), 5, 5)
        _fixed.put(self.cmbAllocationMethod, 5, 30)
        _fixed.put(ramstk.RAMSTKLabel(_(u"Select Goal Metric")), 5, 70)
        _fixed.put(self.cmbAllocationGoal, 5, 95)
        _fixed.put(ramstk.RAMSTKLabel(_(u"R(t) Goal")), 5, 135)
        _fixed.put(self.txtReliabilityGoal, 5, 160)
        _fixed.put(ramstk.RAMSTKLabel(_(u"h(t) Goal")), 5, 200)
        _fixed.put(self.txtHazardRateGoal, 5, 225)
        _fixed.put(ramstk.RAMSTKLabel(_(u"MTBF Goal")), 5, 265)
        _fixed.put(self.txtMTBFGoal, 5, 290)

        _frame = ramstk.RAMSTKFrame(label=_(u"Allocation Goals and Method"))
        _frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        _frame.add(_fixed)

        self.txtHazardRateGoal.props.editable = 0
        self.txtHazardRateGoal.set_sensitive(0)
        self.txtMTBFGoal.props.editable = 0
        self.txtMTBFGoal.set_sensitive(0)
        self.txtReliabilityGoal.props.editable = 0
        self.txtReliabilityGoal.set_sensitive(0)

        return _frame

    def __make_ui(self):
        """
        Make the Allocation RAMSTKTreeview().

        :return: a Gtk.Frame() containing the instance of Gtk.Treeview().
        :rtype: :class:`Gtk.Frame`
        """
        _scrollwindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                 Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.treeview)

        _frame = ramstk.RAMSTKFrame(label=_(u"Allocation Analysis"))
        _frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.treeview.set_grid_lines(Gtk.TREE_VIEW_GRID_LINES_BOTH)

        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._do_change_row))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))
        self._lst_handler_id.append(
            self.cmbAllocationMethod.connect('changed', self._on_combo_changed,
                                             2))
        self._lst_handler_id.append(
            self.cmbAllocationGoal.connect('changed', self._on_combo_changed,
                                           3))
        self._lst_handler_id.append(
            self.txtReliabilityGoal.connect('focus_out_event',
                                            self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.txtHazardRateGoal.connect('focus_out_event',
                                           self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtMTBFGoal.connect('focus_out_event', self._on_focus_out, 6))

        for i in [
                self._lst_col_order[3], self._lst_col_order[5],
                self._lst_col_order[6], self._lst_col_order[7],
                self._lst_col_order[8], self._lst_col_order[9],
                self._lst_col_order[10], self._lst_col_order[11]
        ]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cell_renderers()
            try:
                _cell[0].connect('edited', self._do_edit_cell, i,
                                 self.treeview.get_model())
            except TypeError:
                _cell[0].connect('toggled', self._do_edit_cell, 'new text', i,
                                 self.treeview.get_model())

        _label = ramstk.RAMSTKLabel(
            _(u"Allocation"),
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(u"Displays the Allocation analysis for the selected "
                      u"hardware item."))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.pack_start(self.__make_buttonbox(), False, True)

        _hbox = Gtk.HBox()
        _hbox.pack_start(self.__make_goalbox(), False, True)
        _hbox.pack_end(_frame, True, True)
        self.pack_end(_hbox, True, True)

        self.show_all()

        return None

    def _do_clear_page(self):
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

        self.cmbAllocationMethod.set_active(0)
        self.cmbAllocationGoal.set_active(0)
        self.txtHazardRateGoal.set_text('')
        self.txtMTBFGoal.set_text('')
        self.txtReliabilityGoal.set_text('')

        return None

    def _do_change_row(self, treeview):
        """
        Handle events for the Allocation Tree View RAMSTKTreeView().

        This method is called whenever a Tree View row is activated.

        :param treeview: the Allocation RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeViewRAMSTKTreeView`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()
        try:
            self._allocation_id = _model.get_value(_row, 1)
        except TypeError:
            self._allocation_id = None

        treeview.handler_unblock(self._lst_handler_id[0])

        return _return

    def _do_edit_cell(self, __cell, path, new_text, position, model):
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
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if not self.treeview.do_edit_cell(__cell, path, new_text, position,
                                          model):

            _allocation = self._dtc_data_controller.request_do_select(
                self._allocation_id)

            if position == self._lst_col_order[3]:
                _allocation.included = model[path][self._lst_col_order[3]]
            elif position == self._lst_col_order[4]:
                _allocation.n_sub_elements = int(new_text)
            elif position == self._lst_col_order[5]:
                _allocation.n_sub_elements = int(new_text)
            elif position == self._lst_col_order[6]:
                _allocation.mission_time = float(new_text)
            elif position == self._lst_col_order[7]:
                _allocation.duty_cycle = float(new_text)
            elif position == self._lst_col_order[8]:
                _allocation.int_factor = int(new_text)
            elif position == self._lst_col_order[9]:
                _allocation.soa_factor = int(new_text)
            elif position == self._lst_col_order[10]:
                _allocation.op_time_factor = int(new_text)
            elif position == self._lst_col_order[11]:
                _allocation.env_factor = int(new_text)
        else:
            _return = True

        return _return

    def _do_load_page(self, **kwargs):  # pylint: disable=unused-argument
        """
        Iterate through the tree and load the Allocation RAMSTKTreeView().

        :return: (_error_code, _user_msg, _debug_msg); the error code, message
                 to be displayed to the user, and the message to be written to
                 the debug log.
        :rtype: (int, str, str)
        """
        _error_code = 0
        _user_msg = ""
        _debug_msg = ""

        _data = []

        _model = self.treeview.get_model()
        _model.clear()

        _parent = self._dtc_data_controller.request_do_select(self._parent_id)
        if _parent is not None:
            self.cmbAllocationMethod.set_active(_parent.method_id)
            self.cmbAllocationGoal.set_active(_parent.goal_measure_id)
            self.txtHazardRateGoal.set_text(
                str(self.fmt.format(_parent.hazard_rate_goal)))
            self.txtMTBFGoal.set_text(str(self.fmt.format(_parent.mtbf_goal)))
            self.txtReliabilityGoal.set_text(
                str(self.fmt.format(_parent.reliability_goal)))

        _children = self._dtc_data_controller.request_do_select_children(
            self._parent_id)
        if _children is not None:
            for _child in _children:
                try:
                    _entity = _child.data
                    _node_id = _child.identifier

                    _name = self._dtc_data_controller.dic_hardware_data[
                        _node_id][0]
                    _availability = self._dtc_data_controller.dic_hardware_data[
                        _node_id][1]
                    _hazard_rate = self._dtc_data_controller.dic_hardware_data[
                        _node_id][2]
                    _mtbf = self._dtc_data_controller.dic_hardware_data[
                        _node_id][3]
                    _reliability = self._dtc_data_controller.dic_hardware_data[
                        _node_id][4]
                    _data = [
                        _entity.revision_id, _entity.hardware_id, _name,
                        _entity.included, _entity.n_sub_systems,
                        _entity.n_sub_elements, _entity.mission_time,
                        _entity.duty_cycle, _entity.int_factor,
                        _entity.soa_factor, _entity.op_time_factor,
                        _entity.env_factor, _entity.weight_factor,
                        _entity.percent_weight_factor, _hazard_rate,
                        _entity.hazard_rate_alloc, _mtbf, _entity.mtbf_alloc,
                        _reliability, _entity.reliability_alloc, _availability,
                        _entity.availability_alloc
                    ]

                    try:
                        _model.append(None, _data)
                    except TypeError:
                        _error_code = 1
                        _user_msg = _(u"One or more Allocation line items had "
                                      u"the wrong data type in it's data "
                                      u"package and is not displayed in the "
                                      u"Allocation.")
                        _debug_msg = ("RAMSTK ERROR: Data for Allocation ID "
                                      "{0:s} for Hardware ID {1:s} is the "
                                      "wrong type for one or more "
                                      "columns.".format(
                                          str(_node_id), str(self._parent_id)))
                    except ValueError:
                        _error_code = 1
                        _user_msg = _(u"One or more Allocation line items was "
                                      u"missing some of it's data and is not "
                                      u"displayed in the Allocation.")
                        _debug_msg = ("RAMSTK ERROR: Too few fields for "
                                      "Allocation ID {0:s} for Hardware ID "
                                      "{1:s}.".format(
                                          str(_node_id), str(self._parent_id)))
                except AttributeError:
                    if _node_id != 0:
                        _error_code = 1
                        _user_msg = _(u"One or more Allocation line items was "
                                      u"missing it's data package and is not "
                                      u"displayed in the Allocation.")
                        _debug_msg = ("RAMSTK ERROR: There is no data package "
                                      "for Allocation ID {0:s} for Hardware "
                                      "ID {1:s}.".format(
                                          str(_node_id), str(self._parent_id)))

        return (_error_code, _user_msg, _debug_msg)

    def _do_request_calculate(self, __button):
        """
        Calculate the Allocation RPN or criticality.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        if not self._dtc_data_controller.request_do_calculate(self._parent_id):
            self._do_load_page()

        return None

    def _do_request_calculate_all(self, __button):
        """
        Calculate the Allocation RPN or criticality for all items.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        if not self._dtc_data_controller.request_do_calculate_all():
            self._do_load_page()

        return None

    def _do_request_update(self, __button):
        """
        Request to save the currently selected entity in the Allocation.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        _return = self._dtc_data_controller.request_do_update(self._parent_id)
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

        return _return

    def _do_request_update_all(self, __button):
        """
        Request to save all the entities in the Allocation.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        _return = self._dtc_data_controller.request_do_update_all()
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

        return _return

    def _do_set_visible(self, **kwargs):
        """
        Set the Allocation treeview columns visible, hidden, and/or editable.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self.treeview.do_set_visible_columns(**kwargs)

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Allocation Work View RAMSTKTreeView().

        :param treeview: the Allocation TreeView RAMSTKTreeView().
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
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            _icons = ['calculate', 'save', 'save-all']
            _labels = [_(u"Calculate"), _(u"Save"), _(u"Save All")]
            _callbacks = [
                self._do_request_calculate, self._do_request_update,
                self._do_request_update_all
            ]
            RAMSTKWorkView.on_button_press(
                self,
                event,
                icons=_icons,
                labels=_labels,
                callbacks=_callbacks)

        treeview.handler_unblock(self._lst_handler_id[1])

        return _return

    def _on_combo_changed(self, combo, index):
        """
        Respond to Gtk.ComboBox() 'changed' signals.

        :param Gtk.ComboBox combo: the Gtk.ComboBox() that called this method.
        :param int index: the index in the handler ID list oc the callback
                          signal associated with the Gtk.ComboBox() that
                          called this method.
        :return: None
        :rtype: None
        """
        combo.handler_block(self._lst_handler_id[index])

        _parent = self._dtc_data_controller.request_do_select(self._parent_id)

        if _parent is not None:
            if index == 2:
                _parent.method_id = combo.get_active()
                if _parent.method_id == 1:  # Equal apportionment.
                    _visible = [2, 3, 4, 6, 14, 15, 16, 17, 18, 19]
                    _hidden = [0, 1, 5, 7, 8, 9, 10, 11, 12, 13, 20, 21]
                    _editable = [
                        3,
                        6,
                    ]

                elif _parent.method_id == 2:  # AGREE apportionment.
                    _visible = [2, 3, 4, 5, 6, 7, 12, 14, 15, 16, 17, 18, 19]
                    _hidden = [0, 1, 8, 9, 10, 11, 13, 20, 21]
                    _editable = [3, 5, 6, 7]

                elif _parent.method_id == 3:  # ARINC apportionment.
                    _visible = [2, 3, 12, 14, 15, 16, 17, 18, 19]
                    _hidden = [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 13, 20, 21]
                    _editable = [
                        3,
                    ]

                elif _parent.method_id == 4:  # Feasibility of Objectives.
                    _visible = [
                        2, 3, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
                    ]
                    _hidden = [0, 1, 4, 5, 6, 7, 20, 21]
                    _editable = [3, 8, 9, 10, 11]

                self._do_set_visible(
                    visible=_visible, hidden=_hidden, editable=_editable)

            elif index == 3:
                _parent.goal_measure_id = combo.get_active()
                if combo.get_active() == 0:  # Nothing selected.
                    self.txtReliabilityGoal.props.editable = 0
                    self.txtReliabilityGoal.set_sensitive(0)
                    self.txtMTBFGoal.props.editable = 0
                    self.txtMTBFGoal.set_sensitive(0)
                    self.txtHazardRateGoal.props.editable = 0
                    self.txtHazardRateGoal.set_sensitive(0)
                elif combo.get_active() == 1:  # Expressed as reliability.
                    self.txtReliabilityGoal.props.editable = 1
                    self.txtReliabilityGoal.set_sensitive(1)
                    self.txtReliabilityGoal.set_text(
                        str(self.fmt.format(_parent.reliability_goal)))
                    self.txtMTBFGoal.props.editable = 0
                    self.txtMTBFGoal.set_sensitive(0)
                    self.txtMTBFGoal.set_text(
                        str(self.fmt.format(_parent.mtbf_goal)))
                    self.txtHazardRateGoal.props.editable = 0
                    self.txtHazardRateGoal.set_sensitive(0)
                    self.txtHazardRateGoal.set_text(
                        str(self.fmt.format(_parent.hazard_rate_goal)))
                elif combo.get_active() == 2:  # Expressed as a failure rate.
                    self.txtReliabilityGoal.props.editable = 0
                    self.txtReliabilityGoal.set_sensitive(0)
                    self.txtReliabilityGoal.set_text(
                        str(self.fmt.format(_parent.reliability_goal)))
                    self.txtMTBFGoal.props.editable = 0
                    self.txtMTBFGoal.set_sensitive(0)
                    self.txtMTBFGoal.set_text(
                        str(self.fmt.format(_parent.mtbf_goal)))
                    self.txtHazardRateGoal.props.editable = 1
                    self.txtHazardRateGoal.set_sensitive(1)
                    self.txtHazardRateGoal.set_text(
                        str(self.fmt.format(_parent.hazard_rate_goal)))
                elif combo.get_active() == 3:  # Expressed as an MTBF.
                    self.txtReliabilityGoal.props.editable = 0
                    self.txtReliabilityGoal.set_sensitive(0)
                    self.txtReliabilityGoal.set_text(
                        str(self.fmt.format(_parent.reliability_goal)))
                    self.txtMTBFGoal.props.editable = 1
                    self.txtMTBFGoal.set_sensitive(1)
                    self.txtMTBFGoal.set_text(
                        str(self.fmt.format(_parent.mtbf_goal)))
                    self.txtHazardRateGoal.props.editable = 0
                    self.txtHazardRateGoal.set_sensitive(0)
                    self.txtHazardRateGoal.set_text(
                        str(self.fmt.format(_parent.hazard_rate_goal)))

        combo.handler_unblock(self._lst_handler_id[index])

        return None

    def _on_focus_out(self, entry, __event, index):
        """
        Respond to Gtk.Entry() 'changed' signals.

        :param Gtk.Entry entry: the Gtk.Entry() that called this method.
        :param Gdk.Event __event: the Gdk.Event() that called this
                                      method.
        :param int index: the index in the handler ID list oc the callback
                          signal associated with the Gtk.Entry() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """
        entry.handler_block(self._lst_handler_id[index])

        _parent = self._dtc_data_controller.request_do_select(self._parent_id)
        if _parent is not None:
            if index == 4:  # Reliability goal
                print entry.get_text()
                _parent.reliability_goal = float(entry.get_text())
                _parent.calculate_goals()

                # Set the other two goals.
                self.txtHazardRateGoal.handler_block(self._lst_handler_id[5])
                self.txtMTBFGoal.handler_block(self._lst_handler_id[6])
                self.txtHazardRateGoal.set_text(
                    str(self.fmt.format(_parent.hazard_rate_goal)))
                self.txtMTBFGoal.set_text(
                    str(self.fmt.format(_parent.mtbf_goal)))
                self.txtHazardRateGoal.handler_unblock(self._lst_handler_id[5])
                self.txtMTBFGoal.handler_unblock(self._lst_handler_id[6])
            elif index == 5:  # Hazard rate goal
                _parent.hazard_rate_goal = float(entry.get_text())
                _parent.calculate_goals()

                # Set the other two goals.
                self.txtReliabilityGoal.handler_block(self._lst_handler_id[4])
                self.txtMTBFGoal.handler_block(self._lst_handler_id[6])
                self.txtReliabilityGoal.set_text(
                    str(self.fmt.format(_parent.reliability_goal)))
                self.txtMTBFGoal.set_text(
                    str(self.fmt.format(_parent.mtbf_goal)))
                self.txtReliabilityGoal.handler_unblock(
                    self._lst_handler_id[4])
                self.txtMTBFGoal.handler_unblock(self._lst_handler_id[6])
            elif index == 6:  # MTBF goal
                _parent.mtbf_goal = float(entry.get_text())
                _parent.calculate_goals()

                # Set the other two goals.
                self.txtReliabilityGoal.handler_block(self._lst_handler_id[4])
                self.txtHazardRateGoal.handler_block(self._lst_handler_id[5])
                self.txtReliabilityGoal.set_text(
                    str(self.fmt.format(_parent.reliability_goal)))
                self.txtHazardRateGoal.set_text(
                    str(self.fmt.format(_parent.hazard_rate_goal)))
                self.txtReliabilityGoal.handler_unblock(
                    self._lst_handler_id[4])
                self.txtHazardRateGoal.handler_unblock(self._lst_handler_id[5])

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_select(self, module_id, **kwargs):
        """
        Respond to the `selectedHardware` signal from pypubsub.

        :return: None
        :rtype: None
        """
        self._parent_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKBaseView.__init__
        if self._dtc_data_controller is None:
            self._dtc_data_controller = self._mdcRAMSTK.dic_controllers[
                'allocation']

        (_error_code, _user_msg, _debug_msg) = self._do_load_page(**kwargs)

        RAMSTKWorkView.on_select(
            self,
            title=_(u"Allocating Reliability Requirement for Hardware ID "
                    u"{0:d}").format(self._parent_id),
            error_code=_error_code,
            user_msg=_user_msg,
            debug_msg=_debug_msg)

        return None
