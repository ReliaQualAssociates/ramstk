# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.Allocation.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Allocation Work View."""

from sortedcontainers import SortedDict
from pubsub import pub

# Import other RTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _, gtk
from .WorkView import RTKWorkView


class Allocation(RTKWorkView):
    """
    Display Allocation attribute data in the Work Book.

    The WorkView displays all the attributes for the Failure Mode and Effects
    Analysis (Allocation). The attributes of a Allocation Work View are:

    :ivar _lst_handler_id: list containing the ID's of the callback signals for
                           each gtk.Widget() associated with an editable
                           Functional Allocation attribute.

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

    def __init__(self, controller):
        """
        Initialize the Work View for the Allocation.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKWorkView.__init__(self, controller, module='Allocation')

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
        _fmt_file = controller.RTK_CONFIGURATION.RTK_CONF_DIR + \
            '/' + controller.RTK_CONFIGURATION.RTK_FORMAT_FILE['allocation']
        _fmt_path = "/root/tree[@name='Allocation']/column"
        _tooltip = _(u"Displays the Allocation Analysis for the currently "
                     u"selected Hardware item.")

        self.treeview = rtk.RTKTreeView(
            _fmt_path, 0, _fmt_file, _bg_color, _fg_color, pixbuf=False)
        self._lst_col_order = self.treeview.order
        self.treeview.set_tooltip_text(_tooltip)

        self.cmbAllocationGoal = rtk.RTKComboBox(
            tooltip=_(
                u"Selects the goal measure for the selected hardware assembly."
            ))
        self.cmbAllocationMethod = rtk.RTKComboBox(
            tooltip=_(
                u"Selects the method for allocating the reliability goal for "
                u"the selected hardware assembly."))
        self.txtHazardRateGoal = rtk.RTKEntry(
            width=125,
            tooltip=(
                u"Displays the hazard rate goal for the selected hardware "
                u"item."))
        self.txtMTBFGoal = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"Displays the MTBF goal for the selected hardware item."))
        self.txtReliabilityGoal = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"Displays the reliability goal for the selected hardware "
                u"item."))

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
            self.txtReliabilityGoal.connect('focus-out-event',
                                            self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.txtHazardRateGoal.connect('focus-out-event',
                                           self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtMTBFGoal.connect('focus-out-event', self._on_focus_out, 6))

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

        _label = rtk.RTKLabel(
            _(u"Allocation"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays the Allocation analysis for the selected "
                      u"hardware item."))
        self.hbx_tab_label.pack_start(_label)

        self.pack_start(self._make_buttonbox(), False, True)
        _hbox = gtk.HBox()
        _hbox.pack_start(self._make_goalbox(), False, True)
        _hbox.pack_end(self._make_treeview(), True, True)
        self.pack_end(_hbox, True, True)
        self.show_all()

        pub.subscribe(self._do_refresh_view, 'calculatedAllocation')
        pub.subscribe(self._on_select_revision, 'selectedRevision')
        pub.subscribe(self._on_select, 'selectedHardware')

    def _do_change_row(self, treeview):
        """
        Handle events for the Allocation Tree View RTKTreeView().

        This method is called whenever a Tree View row is activated.

        :param treeview: the Allocation RTKTreeView().
        :type treeview: :class:`rtk.gui.gtk.rtk.TreeViewRTKTreeView`
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
        Handle edits of the Allocation Work View RTKTreeview().

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str path: the RTKTreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if not self.treeview.do_edit_cell(__cell, path, new_text, position,
                                          model):

            _allocation = self._dtc_data_controller.request_select(
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

    def _do_load_tree(self, tree):
        """
        Iterate through the tree and load the Allocation RTKTreeView().

        :param tree: the treelib Tree() holding the (partial) Allocation to
                     load.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _data = []
        _model = self.treeview.get_model()

        i = 1
        for _node in tree.children(SortedDict(tree.nodes).keys()[0]):
            _entity = _node.data
            _node_id = _node.identifier

            _name = self._dtc_data_controller.lst_name[i - 1]
            _availability = self._dtc_data_controller.lst_availability[i]
            _hazard_rate = self._dtc_data_controller.lst_hazard_rates[i]
            _mtbf = self._dtc_data_controller.lst_mtbf[i]
            _reliability = self._dtc_data_controller.lst_reliability[i]
            _data = [
                _entity.revision_id, _entity.hardware_id, _name,
                _entity.included, _entity.n_sub_systems,
                _entity.n_sub_elements, _entity.mission_time,
                _entity.duty_cycle, _entity.int_factor, _entity.soa_factor,
                _entity.op_time_factor, _entity.env_factor,
                _entity.weight_factor, _entity.percent_weight_factor,
                _hazard_rate, _entity.hazard_rate_alloc, _mtbf,
                _entity.mtbf_alloc, _reliability, _entity.reliability_alloc,
                _availability, _entity.availability_alloc
            ]

            try:
                _row = _model.append(None, _data)
            except TypeError:
                print "FIXME: Handle TypeError in " \
                      "gtk.gui.workviews.Allocation.Allocation._do_load_tree."
                _return = True
            except ValueError:
                print "FIXME: Handle ValueError in " \
                      "gtk.gui.workviews.Allocation.Allocation._do_load_tree."
                _return = True
            except AttributeError:
                print "FIXME: Handle AttributeError in " \
                      "gtk.gui.workviews.Allocation.Allocation._do_load_tree."
                _return = True

            i += 1

        return _return

    def _do_refresh_view(self):
        """
        Refresh the Allocation Work View after a successful calculation.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model = self.treeview.get_model()
        _model.clear()

        _parent = self._dtc_data_controller.request_select(self._parent_id)

        if _parent is not None:
            self.cmbAllocationMethod.set_active(_parent.method_id)
            self.cmbAllocationGoal.set_active(_parent.goal_measure_id)
            self.txtHazardRateGoal.set_text(
                str(self.fmt.format(_parent.hazard_rate_goal)))
            self.txtMTBFGoal.set_text(str(self.fmt.format(_parent.mtbf_goal)))
            self.txtReliabilityGoal.set_text(
                str(self.fmt.format(_parent.reliability_goal)))

            _tree = self._dtc_data_controller.request_children(self._parent_id)
            self._do_load_tree(_tree)
        else:
            _return = True

        return _return

    def _do_request_calculate(self, __button):
        """
        Calculate the Allocation RPN or criticality.

        :param __button: the gtk.ToolButton() that called this method.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_calculate(self._parent_id)

    def _do_request_update_all(self, __button):
        """
        Request to save all the entities in the Allocation.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_update_all()

    def _do_set_visible(self, visible, hidden, editable):
        """
        Set the Allocation treeview columns visible and hidden.

        :param list visible: a list of integers indicating the columns to set
                             visible.
        :param list hidden: a list of integers indicating the columns to set
                            hidden.
        :param list editable: a list of integers indicating the columns to set
                              editable.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        for _col in hidden:
            self.treeview.get_column(_col).set_visible(0)
        for _col in visible:
            self.treeview.get_column(_col).set_visible(1)
            _column = self.treeview.get_column(_col)
            _cells = _column.get_cell_renderers()
            for __, _cell in enumerate(_cells):
                try:
                    _cell.set_property('background', 'light gray')
                    _cell.set_property('editable', 0)
                except TypeError:
                    _cell.set_property('cell-background', 'light gray')

        for _col in editable:
            _column = self.treeview.get_column(_col)
            _cells = _column.get_cell_renderers()
            for __, _cell in enumerate(_cells):
                try:
                    _cell.set_property('background', 'white')
                    _cell.set_property('editable', 1)
                except TypeError:
                    _cell.set_property('cell-background', 'white')

        return _return

    def _make_buttonbox(self):
        """
        Make the gtk.ButtonBox() for the Allocation class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the Allocation Work View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Calculate the Allocation."),
            _(u"Save the Allocation to the open RTK Program database.")
        ]
        _callbacks = [self._do_request_calculate, self._do_request_update_all]
        _icons = ['calculate', 'save']

        _buttonbox = RTKWorkView._make_buttonbox(self, _icons, _tooltips,
                                                 _callbacks, 'vertical')

        return _buttonbox

    def _make_goalbox(self):
        """
        Make the Allocation methods and goal-setting container.

        :return: a gtk.Frame() containing the widgets used to select the
                 allocation method and goals.
        :rtype: :class:`gtk.Frame`
        """
        # Load the method and goal comboboxes.
        self.cmbAllocationGoal.do_load_combo(
            [[_(u"Reliability"), 0], [_(u"Hazard Rate"), 1], [_(u"MTBF"), 2]])
        self.cmbAllocationMethod.do_load_combo(
            [[_(u"Equal Apportionment"), 0], [_(u"AGREE Apportionment"), 1],
             [_(u"ARINC Apportionment"),
              2], [_(u"Feasibility of Objectives"), 3]])

        _fixed = gtk.Fixed()

        _fixed.put(rtk.RTKLabel(_(u"Select Allocation Method")), 5, 5)
        _fixed.put(self.cmbAllocationMethod, 5, 30)
        _fixed.put(rtk.RTKLabel(_(u"Select Goal Metric")), 5, 70)
        _fixed.put(self.cmbAllocationGoal, 5, 95)
        _fixed.put(rtk.RTKLabel(_(u"R(t) Goal")), 5, 135)
        _fixed.put(self.txtReliabilityGoal, 5, 160)
        _fixed.put(rtk.RTKLabel(_(u"h(t) Goal")), 5, 200)
        _fixed.put(self.txtHazardRateGoal, 5, 225)
        _fixed.put(rtk.RTKLabel(_(u"MTBF Goal")), 5, 265)
        _fixed.put(self.txtMTBFGoal, 5, 290)

        _frame = rtk.RTKFrame(label=_(u"Allocation Goals and Method"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_fixed)

        self.txtHazardRateGoal.props.editable = 0
        self.txtHazardRateGoal.set_sensitive(0)
        self.txtMTBFGoal.props.editable = 0
        self.txtMTBFGoal.set_sensitive(0)
        self.txtReliabilityGoal.props.editable = 0
        self.txtReliabilityGoal.set_sensitive(0)

        return _frame

    def _make_treeview(self):
        """
        Make the Allocation RTKTreeview().

        :return: a gtk.Frame() containing the instance of gtk.Treeview().
        :rtype: :class:`gtk.Frame`
        """
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.treeview)

        _frame = rtk.RTKFrame(label=_(u"Allocation Analysis"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        return _frame

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Allocation Work View RTKTreeView().

        :param treeview: the Allocation TreeView RTKTreeView().
        :type treeview: :class:`rtk.gui.gtk.rtk.TreeView.RTKTreeView`.
        :param event: the gtk.gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backwards
                      * 8 =
                      * 9 =

        :type event: :class:`gtk.gdk.Event`.
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
            print "FIXME: Rick clicking should launch a pop-up menu with " \
                  "options to insert sibling, insert child, delete " \
                  "(selected), save (selected), and save all in " \
                  "rtk.gui.gtk.workviews.Allocation._on_button_press()."

        treeview.handler_unblock(self._lst_handler_id[1])

        return _return

    def _on_combo_changed(self, combo, index):
        """
        Respond to gtk.ComboBox() 'changed' signals.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called this method.
        :param int index: the index in the handler ID list oc the callback
                          signal associated with the gtk.ComboBox() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """
        _return = False

        combo.handler_block(self._lst_handler_id[index])

        _parent = self._dtc_data_controller.request_select(self._parent_id)

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

                _return = self._do_set_visible(_visible, _hidden, _editable)

            elif index == 3:
                _parent.goal_measure_id = combo.get_active()
                #_parent.calculate_goals()
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

        return False

    def _on_focus_out(self, entry, __event, index):
        """
        Respond to gtk.Entry() 'focus_out' signals.

        :param gtk.Entry entry: the gtk.Entry() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param int index: the index in the handler ID list oc the callback
                          signal associated with the gtk.Entry() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """
        entry.handler_block(self._lst_handler_id[index])

        _parent = self._dtc_data_controller.request_select(self._parent_id)
        if _parent is not None:
            if index == 4:  # Reliability goal
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

    def _on_select(self, module_id):
        """
        Respond to the `selectedHardware` signal from pypubsub.

        :param int module_id: the ID of the Hardware that was selected.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._parent_id = module_id

        return self._do_refresh_view()

    def _on_select_revision(self, module_id):
        """
        Respond to the `selectedRevision` signal from pypubsub.

        This method is called whenever a new Revision is selected in the RTK
        Module View.  It selects all the Allocations for the Revision ID passed
        and builds the treelib Tree() to hold them all for use.

        :param int module_id: the Revision ID to select the Allocations for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = \
            self._mdcRTK.dic_controllers['allocation']
        self._dtc_data_controller.request_select_all(module_id)

        return _return
