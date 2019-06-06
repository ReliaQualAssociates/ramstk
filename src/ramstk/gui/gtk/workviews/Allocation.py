# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.Allocation.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Allocation Work View."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import (
    RAMSTKComboBox, RAMSTKEntry, RAMSTKFrame, RAMSTKLabel, RAMSTKTreeView,
)
from ramstk.gui.gtk.ramstk.Widget import Gdk, Gtk, _

# RAMSTK Local Imports
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

    :ivar int _allocation_id: the ID of the selected Allocation.
    :ivar float _hazard_rate_goal: the reliability goal expressed as a hazard
    rate.
    :ivar int _measure_id: the ID of the reliability goal measure (reliability,
    hazard rate, or MTBF).
    :ivar int _method_id: the ID of the apportionment method used (equal,
    AGREE, ARINC, or Feasibility of Objectives).
    :ivar float _mtbf_goal: the reliability goal expressed as an MTBF.
    :ivar float _reliability_goal: the reliability goal expressed as a
    probability.
    """

    def __init__(self, configuration, **kwargs):
        """
        Initialize the Work View for the Allocation.

        :param configuration: the instance of the RAMSTK Configuration() class.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKWorkView.__init__(
            self,
            configuration,
            module='Allocation',
            **kwargs,
        )

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._allocation_id = None
        self._hazard_rate_goal = 0.0
        self._measure_id = 0
        self._method_id = 0
        self._mtbf_goal = 0.0
        self._reliability_goal = 0.0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        _fmt_file = (
            self.RAMSTK_CONFIGURATION.RAMSTK_CONF_DIR + '/layouts/' +
            self.RAMSTK_CONFIGURATION.RAMSTK_FORMAT_FILE['allocation']
        )
        _fmt_path = "/root/tree[@name='Allocation']/column"

        self.treeview = RAMSTKTreeView(
            _fmt_path,
            0,
            _fmt_file,
            "#FFFFFF",
            "#000000",
            pixbuf=False,
        )
        self._lst_col_order = self.treeview.order

        self.cmbAllocationGoal = RAMSTKComboBox()
        self.cmbAllocationMethod = RAMSTKComboBox()
        self.txtHazardRateGoal = RAMSTKEntry()
        self.txtMTBFGoal = RAMSTKEntry()
        self.txtReliabilityGoal = RAMSTKEntry()

        self.__set_properties()
        self.__make_ui()
        self.__load_combobox()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_load_page, 'selected_hardware')
        pub.subscribe(self.do_load_tree, 'retrieved_allocations')

    def __load_combobox(self):
        """
        Load the RAMSTKComboBox() widgets.

        :return: None
        :rtype: None
        """
        self.cmbAllocationGoal.do_load_combo([
            [_("Reliability"), 0],
            [_("Hazard Rate"), 1],
            [_("MTBF"), 2],
        ])
        self.cmbAllocationMethod.do_load_combo(
            [
                [_("Equal Apportionment"), 0],
                [_("AGREE Apportionment"), 1],
                [_("ARINC Apportionment"), 2],
                [_("Feasibility of Objectives"), 3],
            ], )

    def __make_ui(self):
        """
        Make the Allocation RAMSTKTreeview().

        :return: a Gtk.Frame() containing the instance of Gtk.Treeview().
        :rtype: :class:`Gtk.Frame`
        """
        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC,
        )
        _scrolledwindow.add_with_viewport(
            RAMSTKWorkView._make_buttonbox(
                self,
                icons=['calculate'],
                tooltips=[
                    _("Calculate the currently selected child hardware item."),
                ],
                callbacks=[self._do_request_calculate],
            ), )
        self.pack_start(_scrolledwindow, False, False, 0)

        _hbox = Gtk.HBox()

        _fixed = Gtk.Fixed()
        _fixed.put(RAMSTKLabel(_("Select Allocation Method")), 5, 5)
        _fixed.put(self.cmbAllocationMethod, 5, 30)
        _fixed.put(RAMSTKLabel(_("Select Goal Metric")), 5, 70)
        _fixed.put(self.cmbAllocationGoal, 5, 95)
        _fixed.put(RAMSTKLabel(_("R(t) Goal")), 5, 135)
        _fixed.put(self.txtReliabilityGoal, 5, 160)
        _fixed.put(RAMSTKLabel(_("h(t) Goal")), 5, 200)
        _fixed.put(self.txtHazardRateGoal, 5, 225)
        _fixed.put(RAMSTKLabel(_("MTBF Goal")), 5, 265)
        _fixed.put(self.txtMTBFGoal, 5, 290)

        _frame = RAMSTKFrame(label=_("Allocation Goals and Method"))
        _frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        _frame.add(_fixed)

        _hbox.pack_start(_frame, False, True, 0)

        _scrollwindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC,
        )
        _scrollwindow.add(self.treeview)

        _frame = RAMSTKFrame(label=_("Allocation Analysis"))
        _frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True, 0)
        self.pack_end(_hbox, True, True, 0)

        _label = RAMSTKLabel(
            _("Allocation"),
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(
                "Displays the Allocation analysis for the selected "
                "hardware item.", ),
        )
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self):
        """
        Set the callback functions and methods for the Allocation widgets.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._do_change_row), )
        self._lst_handler_id.append(
            self.treeview.connect(
                'button_press_event',
                self._on_button_press,
            ), )

        for i in [
                self._lst_col_order[3],
                self._lst_col_order[5],
                self._lst_col_order[6],
                self._lst_col_order[7],
                self._lst_col_order[8],
                self._lst_col_order[9],
                self._lst_col_order[10],
                self._lst_col_order[11],
        ]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i], ).get_cells()
            try:
                _cell[0].connect(
                    'edited',
                    self._on_cell_edit,
                    i,
                    self.treeview.get_model(),
                )
            except TypeError:
                _cell[0].connect(
                    'toggled',
                    self._on_cell_edit,
                    'new text',
                    i,
                    self.treeview.get_model(),
                )

        self._lst_handler_id.append(
            self.cmbAllocationMethod.connect(
                'changed',
                self._on_combo_changed,
                2,
            ), )
        self._lst_handler_id.append(
            self.cmbAllocationGoal.connect(
                'changed',
                self._on_combo_changed,
                3,
            ), )

        self._lst_handler_id.append(
            self.txtReliabilityGoal.connect(
                'focus_out_event',
                self._on_focus_out,
                4,
            ), )
        self._lst_handler_id.append(
            self.txtHazardRateGoal.connect(
                'focus_out_event',
                self._on_focus_out,
                5,
            ), )
        self._lst_handler_id.append(
            self.txtMTBFGoal.connect(
                'focus_out_event', self._on_focus_out,
                6,
            ), )

    def __set_properties(self):
        """
        Set the properties of the Allocation widgets.

        :return: None
        :rtype: None
        """
        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.treeview.set_tooltip_text(
            _(
                "Displays the Allocation Analysis for the currently selected "
                "Hardware item.", ), )

        self.cmbAllocationGoal.do_set_properties(
            tooltip=_(
                "Selects the goal measure for the selected hardware assembly.", ),
        )
        self.cmbAllocationMethod.do_set_properties(
            tooltip=_(
                "Selects the method for allocating the reliability goal for "
                "the selected hardware assembly.", ), )
        self.txtHazardRateGoal.do_set_properties(
            width=125,
            tooltip=(
                "Displays the hazard rate goal for the selected hardware "
                "item."
            ),
        )
        self.txtMTBFGoal.do_set_properties(
            width=125,
            tooltip=_(
                "Displays the MTBF goal for the selected hardware item.", ),
        )
        self.txtReliabilityGoal.do_set_properties(
            width=125,
            tooltip=_(
                "Displays the reliability goal for the selected hardware "
                "item.", ),
        )

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

    def _do_change_row(self, treeview):
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
            self._allocation_id = _model.get_value(_row, 1)
        except TypeError:
            self._allocation_id = None

        treeview.handler_unblock(self._lst_handler_id[0])

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
        self.txtHazardRateGoal.do_update("", self._lst_handler_id[4])
        self.txtMTBFGoal.do_update("", self._lst_handler_id[5])
        self.txtReliabilityGoal.do_update("", self._lst_handler_id[6])

    def _do_load_page(self, attributes):
        """
        Load the Hardware item information for the Allocation.

        :param dict attributes: a dict of attribute key:value pairs for the
        displayed Hardware item's Allocation.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes["revision_id"]
        self._parent_id = attributes["hardware_id"]
        self._method_id = attributes["method_id"]
        self._measure_id = attributes["goal_measure_id"]
        self._hazard_rate_goal = attributes["hazard_rate_goal"]
        self._mtbf_goal = attributes["mtbf_goal"]
        self._reliability_goal = attributes["reliability_goal"]

        RAMSTKWorkView.on_select(
            self,
            title=_(
                "Allocating Reliability Requirement for Hardware ID "
                "{0:d}", ).format(self._parent_id),
        )

        self.cmbAllocationMethod.set_active(self._method_id)
        self.cmbAllocationGoal.set_active(self._measure_id)
        self.txtReliabilityGoal.do_update(
            str(self.fmt.format(self._reliability_goal)),
            self._lst_handler_id[4],
        )
        self.txtHazardRateGoal.do_update(
            str(self.fmt.format(self._hazard_rate_goal)),
            self._lst_handler_id[5],
        )
        self.txtMTBFGoal.do_update(
            str(self.fmt.format(self._mtbf_goal)),
            self._lst_handler_id[6],
        )

    def _do_request_calculate(self, __button):
        """
        Calculate the Allocation reliability metrics.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            "request_calculate_allocation",
            node_id=self._parent_id,
        )
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_calculate_all(self, __button):
        """
        Calculate the Allocation for all items.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage("request_calculate_all_allocations")
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update(self, __button):
        """
        Request to save the currently selected entity in the Allocation.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            "request_update_allocation",
            node_id=self._allocation_id,
        )
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button):
        """
        Request to save all the entities in the Allocation.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage("request_update_all_allocations")
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

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
        :return: None
        :rtype: None
        """
        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            _icons = ['calculate', 'save', 'save-all']
            _labels = [_("Calculate"), _("Save"), _("Save All")]
            _callbacks = [
                self._do_request_calculate,
                self._do_request_update,
                self._do_request_update_all,
            ]
            RAMSTKWorkView.on_button_press(
                self,
                event,
                icons=_icons,
                labels=_labels,
                callbacks=_callbacks,
            )

        treeview.handler_unblock(self._lst_handler_id[1])

    def _on_cell_edit(self, __cell, path, new_text, position, model):
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
            11: "env_factor",
        }

        if not self.treeview.do_edit_cell(
                __cell,
                path,
                new_text,
                position,
                model,
        ):

            try:
                _key = _dic_keys[self._lst_col_order[position]]
            except KeyError:
                _key = None

            pub.sendMessage(
                "mvw_editing_allocation",
                module_id=self._allocation_id,
                key=_key,
                value=new_text,
            )

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
        _dic_keys = {
            2: 'method_id',
            3: 'goal_measure_id',
        }

        # Key is the allocation method ID:
        #   1: Equal apportionment
        #   2: AGREE apportionment
        #   3: ARINC apportionment
        #   4: Feasibility of Objectives
        _dic_visible = {
            1: [
                2,
                3,
                4,
                6,
                14,
                15,
                16,
                17,
                18,
                19,
            ],
            2: [
                2,
                3,
                4,
                5,
                6,
                7,
                12,
                14,
                15,
                16,
                17,
                18,
                19,
            ],
            3: [
                2,
                3,
                12,
                14,
                15,
                16,
                17,
                18,
                19,
            ],
            4: [
                2,
                3,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
            ],
        }
        _dic_editable = {
            1: [
                3,
                6,
            ],
            2: [
                3,
                5,
                6,
                7,
            ],
            3: [
                3,
            ],
            4: [
                3,
                8,
                9,
                10,
                11,
            ],
        }
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        combo.handler_block(self._lst_handler_id[index])

        _new_text = int(combo.get_active())
        if index == 2:
            self._method_id = combo.get_active()
        elif index == 3:
            self._measure_id = combo.get_active()

        try:
            _visible = _dic_visible[self._method_id]
        except KeyError:
            _visible = []
        try:
            _editable = _dic_editable[self._method_id]
        except KeyError:
            _editable = []

        self._do_set_visible(visible=_visible, editable=_editable)
        self.__set_properties()

        pub.sendMessage(
            'wvw_editing_allocation',
            module_id=self._parent_id,
            key=_key,
            value=_new_text,
        )

        combo.handler_unblock(self._lst_handler_id[index])

    def _on_focus_out(self, entry, __event, index):
        """
        Respond to Gtk.Entry() 'changed' signals.

        :param Gtk.Entry entry: the Gtk.Entry() that called this method.
        :param Gdk.Event __event: the Gdk.Event() that called this
                                      method.
        :param int index: the index in the handler ID list oc the callback
                          signal associated with the Gtk.Entry() that
                          called this method.
        :return: None
        :rtype: None
        """
        _dic_keys = {
            4: "reliability_goal",
            5: "hazard_rate_goal",
            6: "mtbf_goal",
        }
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        entry.handler_block(self._lst_handler_id[index])

        try:
            _new_text = float(entry.get_text())
        except ValueError:
            _new_text = ''

        if index == 4:
            self._reliability_goal = _new_text
        elif index == 5:
            self._hazard_rate_goal = _new_text
        elif index == 6:
            self._mtbf_goal = _new_text

        pub.sendMessage(
            'wvw_editing_allocation',
            module_id=self._parent_id,
            key=_key,
            value=_new_text,
        )
        pub.sendMessage(
            'request_calculate_allocation',
            node_id=self._parent_id,
        )

        entry.handler_unblock(self._lst_handler_id[index])
