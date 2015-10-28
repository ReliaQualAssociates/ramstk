#!/usr/bin/env python
"""
################################
Allocation Module Work Book View
################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.analyses.allocation.gui.gtk.WorkBook.py is part of The RTK Project
#
# All rights reserved.

import sys

# Modules required for the GUI.
import pango
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
    import widgets as _widg
except ImportError:
    import rtk.configuration as _conf
    import rtk.widgets as _widg

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext

# TODO: Fix all docstrings; copy-paste errors.
class WorkView(gtk.HBox):                   # pylint: disable=R0902, R0904
    """
    The Work Book view displays all the attributes for the selected Allocation.
    The attributes of an Allocation Work Book view are:
    """

    def __init__(self, controller):
        """
        Initializes the Work Book view for the Allocation module.

        :param rtk.analyses.allocation.Allocation controller: the Allocation
                                                              data controller.
        """

        gtk.HBox.__init__(self)

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize public scalar attributes.
        self.dtcAllocation = controller

        self.btnAllocate = _widg.make_button(width=35, image='calculate')
        self.btnSaveAllocation = _widg.make_button(width=35, image='save')
        self.btnTrickledown = _widg.make_button(width=35, image='trickledown')

        self.chkApplyResults = _widg.make_check_button(_(u"Apply results to "
                                                         u"hardware"))

        self.cmbAllocationMethod = _widg.make_combo(width=150)
        self.cmbAllocationGoal = _widg.make_combo(width=150)

        self.tvwAllocation = gtk.TreeView()

        self.txtReliabilityGoal = _widg.make_entry(width=100)
        self.txtMTBFGoal = _widg.make_entry(width=100)
        self.txtHazardRateGoal = _widg.make_entry(width=100)

        self.show_all()

    def create_page(self):
        """
        Creates the page for displaying the reliability allocation analysis for
        the selected Hardware item.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Create the Alloction gtk.TreeView().
        _labels = [_(u""), _(u"Assembly"), _(u"Included?"),
                   _(u"Number of\nSub-Systems"), _(u"Number of\nSub-Elements"),
                   _(u"Operating\nTime"), _(u"Duty Cycle"),
                   _(u"Intricacy\n(1-10)"), _(u"State of\nthe Art\n(1-10)"),
                   _(u"Operating\nTime (1-10)"), _(u"Environment\n(1-10)"),
                   _(u"Weighting\nFactor"), _(u"Percent\nWeighting\nFactor"),
                   _(u"Current\nHazard\nRate"), _(u"Allocated\nHazard\nRate"),
                   _(u"Current\nMTBF"), _(u"Allocated\nMTBF"),
                   _(u"Current\nReliability"), _(u"Allocated\nReliability"),
                   _(u"Current\nAvailability"), _(u"Allocated\nAvailability")]

        _model = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT)
        self.tvwAllocation.set_model(_model)
        self.tvwAllocation.set_tooltip_text(_(u"Displays the list of "
                                              u"immediate child assemblies "
                                              u"that may be included in the "
                                              u"allocation."))

        _columns = int(len(_labels))
        for i in range(_columns):
            _column = gtk.TreeViewColumn()
            if i == 2:
                _cell = gtk.CellRendererToggle()
                _cell.set_property('activatable', 1)
                _cell.connect('toggled', _widg.edit_tree,
                              None, i, _model)
            else:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD)
                _cell.set_property('background', 'white')
                _cell.set_property('foreground', 'black')
                _cell.connect('edited', self._on_cell_edit, i)

            _column.pack_start(_cell, True)
            if i == 2:
                _column.set_attributes(_cell, active=i)
            else:
                _column.set_attributes(_cell, text=i)

            _label = gtk.Label()
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_line_wrap(True)
            _label.set_markup("<span weight='bold'>%s</span>" % _labels[i])
            _label.set_use_markup(True)
            _label.show_all()

            _column.set_widget(_label)

            self.tvwAllocation.append_column(_column)

        self.tvwAllocation.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        self.pack_start(_bbox, False, True)

        _vbox = gtk.VBox()

        self.pack_end(_vbox, True, True)

        _fixed = gtk.Fixed()
        _vbox.pack_start(_fixed, False, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwAllocation)

        _frame = _widg.make_frame(label=_(u"Allocation Inputs"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vbox.pack_end(_frame, True, True)

        _bbox.pack_start(self.btnAllocate, False, False)
        _bbox.pack_start(self.btnSaveAllocation, False, False)
        _bbox.pack_start(self.btnTrickledown, False, False)

        self.btnAllocate.set_tooltip_text(_(u"Performs the selected "
                                            u"alloction."))
        self.btnSaveAllocation.set_tooltip_text(_(u"Saves the selected "
                                                  u"alloction."))
        self.btnTrickledown.set_tooltip_text(_(u"Sets the reliability, hazard "
                                               u"rate and MTBF goal of the "
                                               u"immediately subordinate "
                                               u"hardware items to the "
                                               u"values calculated by the "
                                               u"alloction."))

        # Connect to callback functions.
        self._lst_handler_id.append(
            self.btnAllocate.connect('clicked',
                                     self._on_button_clicked, 0))
        self._lst_handler_id.append(
            self.btnSaveAllocation.connect('clicked',
                                           self._on_button_clicked, 1))
        self._lst_handler_id.append(
            self.btnTrickledown.connect('clicked',
                                        self._on_button_clicked, 2))

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display the allocation analysis.    #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.Combo()
        _results = [[_(u"Equal Apportionment"), 0],
                    [_(u"AGREE Apportionment"), 1],
                    [_(u"ARINC Apportionment"), 2],
                    [_(u"Feasibility of Objectives"), 3]]
        _widg.load_combo(self.cmbAllocationMethod, _results)

        _results = [[_(u"Reliability"), 0],
                    [_(u"Hazard Rate"), 1],
                    [_(u"MTBF"), 2]]
        _widg.load_combo(self.cmbAllocationGoal, _results)

        _labels = [_(u"Allocation Method:"), _(u"Allocation Goal:"),
                   _(u"R(t) Goal:"), _(u"h(t) Goal:"), _(u"MTBF Goal:")]

        # Widgets to display allocation results.
        self.cmbAllocationMethod.set_tooltip_text(_(u"Selects the method for "
                                                    u"allocating the "
                                                    u"reliability goal for "
                                                    u"the selected hardware "
                                                    u"assembly."))
        self.cmbAllocationGoal.set_tooltip_text(_(u"Selects the goal measure "
                                                  u"for the selected hardware "
                                                  u"assembly."))
        self.txtReliabilityGoal.set_tooltip_text(_(u"Displays the reliability "
                                                   u"goal for the selected "
                                                   u"hardware item."))
        self.txtHazardRateGoal.set_tooltip_text(_(u"Displays the hazard rate "
                                                  u"goal for the selected "
                                                  u"hardware item."))
        self.txtMTBFGoal.set_tooltip_text(_(u"Displays the MTBF goal for the "
                                            u"selected hardware item."))

        _x_pos = 5
        _label = _widg.make_label(_labels[0], width=-1)
        _fixed.put(_label, _x_pos, 5)
        _x_pos = _x_pos + _label.size_request()[0] + 25
        _fixed.put(self.cmbAllocationMethod, _x_pos, 5)

        _x_pos = 350
        _label = _widg.make_label(_labels[1], width=-1)
        _fixed.put(_label, _x_pos, 5)
        _x_pos = _x_pos + _label.size_request()[0] + 25
        _fixed.put(self.cmbAllocationGoal, _x_pos, 5)

        _x_pos = 650
        _label = _widg.make_label(_labels[2], width=-1)
        _fixed.put(_label, _x_pos, 5)
        _x_pos = _x_pos + _label.size_request()[0] + 25
        _fixed.put(self.txtReliabilityGoal, _x_pos, 5)
        self.txtReliabilityGoal.props.editable = 0
        self.txtReliabilityGoal.set_sensitive(0)

        _x_pos = 850
        _label = _widg.make_label(_labels[3], width=-1)
        _fixed.put(_label, _x_pos, 5)
        _x_pos = _x_pos + _label.size_request()[0] + 25
        _fixed.put(self.txtHazardRateGoal, _x_pos, 5)
        self.txtHazardRateGoal.props.editable = 0
        self.txtHazardRateGoal.set_sensitive(0)

        _x_pos = 1050
        _label = _widg.make_label(_labels[4], width=-1)
        _fixed.put(_label, _x_pos, 5)
        _x_pos = _x_pos + _label.size_request()[0] + 25
        _fixed.put(self.txtMTBFGoal, _x_pos, 5)
        self.txtMTBFGoal.props.editable = 0
        self.txtMTBFGoal.set_sensitive(0)

        self._lst_handler_id.append(
            self.cmbAllocationMethod.connect('changed',
                                             self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbAllocationGoal.connect('changed',
                                           self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.txtReliabilityGoal.connect('focus-out-event',
                                            self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtHazardRateGoal.connect('focus-out-event',
                                           self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.txtMTBFGoal.connect('focus-out-event',
                                     self._on_focus_out, 7))

        return False

    def load_page(self, controller, hardware_id, parent_row=None):
        """
        Loads the Allocation Module Book gtk.TreeModel() with allocation
        information.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _model = self.tvwAllocation.get_model()

        _parent = self.dtcAllocation.dicAllocation[hardware_id]

        # Find the immediate child assemblies.
        _children = [_a for _a in self.dtcAllocation.dicAllocation.values()
                     if _a.parent_id == hardware_id]

        for _child in _children:
            _hardware = controller.dicHardware[_child.hardware_id]
            _availability = _hardware.availability_logistics
            _hazard_rate = _hardware.hazard_rate_logistics
            _mtbf = _hardware.mtbf_logistics
            _name = _hardware.name
            _reliability = _hardware.reliability_logistics
            _data = [_child.hardware_id, _name, _child.included,
                     _child.n_sub_systems, _child.n_sub_elements,
                     _child._mission_time, _child._duty_cycle,
                     _child.int_factor, _child.soa_factor,
                     _child.op_time_factor, _child.env_factor,
                     _child.weight_factor, _child.percent_wt_factor,
                     _hazard_rate, _child.hazard_rate_alloc,
                     _mtbf, _child.mtbf_alloc, _reliability,
                     _child.reliability_alloc, _availability,
                     _child.availability_alloc]
            _piter = _model.append(parent_row, _data)
            _parent_id = _child.hardware_id

            # Find the child requirements of the current parent requirement.
            # These # will be the new parent requirements to pass to this
            # method.
            self.load_page(controller, _parent_id, _piter)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        self.tvwAllocation.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.tvwAllocation.get_column(0)
            self.tvwAllocation.row_activated(_path, _column)

        # Load the top-bar widgets.
        _allocation = self.dtcAllocation.dicAllocation[hardware_id]
        self.cmbAllocationMethod.set_active(_allocation.method)
        self.cmbAllocationGoal.set_active(_allocation.goal_measure)
        self.txtReliabilityGoal.set_text(
            str(fmt.format(_allocation.reliability_goal)))
        self.txtHazardRateGoal.set_text(
            str(fmt.format(_allocation.hazard_rate_goal)))
        self.txtMTBFGoal.set_text(str(fmt.format(_allocation.mtbf_goal)))

        self._format(hardware_id)

        return False

    def _format(self, hardware_id):
        """
        Formats the Allocation view gtk.TreeView() to show the proper columns
        for the selected allocation method.

        :param int hardware_id: the Hardware ID of the allocation
                                gtk.TreeView() to format.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _allocation = self.dtcAllocation.dicAllocation[hardware_id]

        _heading = _(u"Weighting Factor")
        if _allocation.method == 1:         # Equal apportionment selected.
            for _col in 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 19, 20:
                self.tvwAllocation.get_column(_col).set_visible(0)
            for _col in 1, 13, 14, 15, 16, 17, 18:
                self.tvwAllocation.get_column(_col).set_visible(1)
                _column = self.tvwAllocation.get_column(_col)
                _cells = _column.get_cell_renderers()
                for i in range(len(_cells)):
                    _cells[i].set_property('background', 'light gray')
                    _cells[i].set_property('editable', 0)

        elif _allocation.method == 2:       # AGREE apportionment selected.
            for _col in 0, 2, 3, 7, 8, 9, 10, 12, 19, 20:
                self.tvwAllocation.get_column(_col).set_visible(0)
            for _col in 1, 5, 11, 13, 14, 15, 16, 17, 18:
                self.tvwAllocation.get_column(_col).set_visible(1)
                _column = self.tvwAllocation.get_column(_col)
                _cells = _column.get_cell_renderers()
                for i in range(len(_cells)):
                    _cells[i].set_property('background', 'light gray')
                    _cells[i].set_property('editable', 0)
            for _col in 4, 6:
                self.tvwAllocation.get_column(_col).set_visible(1)
                _column = self.tvwAllocation.get_column(_col)
                _cells = _column.get_cell_renderers()
                for i in range(len(_cells)):
                    _cells[i].set_property('background', 'white')
                    _cells[i].set_property('editable', 1)

            _heading = _(u"Importance Measure")
        elif _allocation.method == 3:   # ARINC apportionment selected.
            for _col in 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 19, 20:
                self.tvwAllocation.get_column(_col).set_visible(0)
            for _col in 1, 11, 13, 14, 15, 16, 17, 18:
                self.tvwAllocation.get_column(_col).set_visible(1)
                _column = self.tvwAllocation.get_column(_col)
                _cells = _column.get_cell_renderers()
                for i in range(len(_cells)):
                    _cells[i].set_property('background', 'light gray')
                    _cells[i].set_property('editable', 0)

        elif _allocation.method == 4:   # Feasibility of Objectives selected.
            for _col in 0, 2, 3, 4, 5, 6, 19, 20:
                self.tvwAllocation.get_column(_col).set_visible(0)
            for _col in 1, 11, 12, 13, 14, 15, 16, 17, 18:
                self.tvwAllocation.get_column(_col).set_visible(1)
                _column = self.tvwAllocation.get_column(_col)
                _cells = _column.get_cell_renderers()
                for i in range(len(_cells)):
                    _cells[i].set_property('background', 'light gray')
                    _cells[i].set_property('editable', 0)
            for _col in 7, 8, 9, 10:
                self.tvwAllocation.get_column(_col).set_visible(1)
                _column = self.tvwAllocation.get_column(_col)
                _cells = _column.get_cell_renderers()
                for i in range(len(_cells)):
                    _cells[i].set_property('background', 'white')
                    _cells[i].set_property('editable', 1)

        return False

    def _on_button_clicked(self, __button, index):
        """
        Responds to gtk.Button() clicked signals and calls the correct function
        or method, passing any parameters as needed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if index == 0:                      # Perform allocation
            self.dtcAllocation.allocate(self._hardware_model.hardware_id)
            _model = self.tvwAllocation.get_model()
            _row = _model.get_iter_root()
            while _row is not None:
                _hardware_id = _model.get_value(_row, 0)
                _allocation = self.dtcAllocation.dicAllocation[_hardware_id]
                _model.set_value(_row, 11, _allocation.weight_factor)
                _model.set_value(_row, 12, _allocation.percent_wt_factor)
                _model.set_value(_row, 14, _allocation.hazard_rate_alloc)
                _model.set_value(_row, 16, _allocation.mtbf_alloc)
                _model.set_value(_row, 18, _allocation.reliability_alloc)
                _row = _model.iter_next(_row)
        elif index == 1:                    # Save allocation
            self.dtcAllocation.save_all_allocation()
        elif index == 2:                    # Trickle down allocation
            self.dtcAllocation.trickle_down(self._hardware_model.hardware_id)

    def _on_cell_edit(self, __cell, path, new_text, index):
        """
        Responds to edited signals from the Allocation gtk.TreeView().

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that called this
                                        method.
        :param str path: the path of the selected gtk.TreeIter().
        :param str new_text: the new text in the gtk.CellRenderer() that called
                             this method.
        :param int index: the position of the gtk.CellRenderer() in the
                          gtk.TreeModel().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _model = self.tvwAllocation.get_model()
        _hardware_id = _model[path][0]
        _allocation = self.dtcAllocation.dicAllocation[_hardware_id]

        _convert = gobject.type_name(_model.get_column_type(index))

        if _convert == 'gchararray':
            _model[path][index] = str(new_text)
        elif _convert == 'gint':
            _model[path][index] = int(new_text)
        elif _convert == 'gfloat':
            _model[path][index] = float(new_text)

        if index == 4:
            _allocation.n_sub_elements = int(new_text)
        elif index == 6:
            _allocation._duty_cycle = float(new_text)
        elif index == 7:
            _allocation.int_factor = int(new_text)
        elif index == 8:
            _allocation.soa_factor = int(new_text)
        elif index == 9:
            _allocation.op_time_factor = int(new_text)
        elif index == 10:
            _allocation.env_factor = int(new_text)

        return False

    def _on_combo_changed(self, combo, index):
        """
        Responds to gtk.ComboBox() changed signals and calls the correct
        function or method, passing any parameters as needed.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called this method.
        :param int index: the index in the handler ID list oc the callback
                          signal associated with the gtk.ComboBox() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = self.tvwAllocation.get_selection().get_selected()
        if _row is None:
            _row = _model.get_iter_root()
        try:
            _hardware_id = _model.get_value(_row, 0)
        except TypeError:
            return True

        combo.handler_block(self._lst_handler_id[index])

        if index == 3:
            _allocation = self.dtcAllocation.dicAllocation[_hardware_id]
            _allocation.method = combo.get_active()
            self._format(_hardware_id)
        elif index == 4:
            _allocation = self.dtcAllocation.dicAllocation[_hardware_id]
            _allocation.goal_measure = combo.get_active()
            _allocation.calculate_goals()
            if combo.get_active() == 0:     # Nothing selected.
                self.txtReliabilityGoal.props.editable = 0
                self.txtReliabilityGoal.set_sensitive(0)
                self.txtMTBFGoal.props.editable = 0
                self.txtMTBFGoal.set_sensitive(0)
                self.txtHazardRateGoal.props.editable = 0
                self.txtHazardRateGoal.set_sensitive(0)
            elif combo.get_active() == 1:   # Expressed as reliability.
                self.txtReliabilityGoal.props.editable = 1
                self.txtReliabilityGoal.set_sensitive(1)
                self.txtReliabilityGoal.set_text(
                    str(fmt.format(_allocation.reliability_goal)))
                self.txtMTBFGoal.props.editable = 0
                self.txtMTBFGoal.set_sensitive(0)
                self.txtMTBFGoal.set_text(
                    str(fmt.format(_allocation.mtbf_goal)))
                self.txtHazardRateGoal.props.editable = 0
                self.txtHazardRateGoal.set_sensitive(0)
                self.txtHazardRateGoal.set_text(
                    str(fmt.format(_allocation.hazard_rate_goal)))
            elif combo.get_active() == 2:   # Expressed as a failure rate.
                self.txtReliabilityGoal.props.editable = 0
                self.txtReliabilityGoal.set_sensitive(0)
                self.txtReliabilityGoal.set_text(
                    str(fmt.format(_allocation.reliability_goal)))
                self.txtMTBFGoal.props.editable = 0
                self.txtMTBFGoal.set_sensitive(0)
                self.txtMTBFGoal.set_text(
                    str(fmt.format(_allocation.mtbf_goal)))
                self.txtHazardRateGoal.props.editable = 1
                self.txtHazardRateGoal.set_sensitive(1)
                self.txtHazardRateGoal.set_text(
                    str(fmt.format(_allocation.hazard_rate_goal)))
            elif combo.get_active() == 3:   # Expressed as an MTBF.
                self.txtReliabilityGoal.props.editable = 0
                self.txtReliabilityGoal.set_sensitive(0)
                self.txtReliabilityGoal.set_text(
                    str(fmt.format(_allocation.reliability_goal)))
                self.txtMTBFGoal.props.editable = 1
                self.txtMTBFGoal.set_sensitive(1)
                self.txtMTBFGoal.set_text(
                    str(fmt.format(_allocation.mtbf_goal)))
                self.txtHazardRateGoal.props.editable = 0
                self.txtHazardRateGoal.set_sensitive(0)
                self.txtHazardRateGoal.set_text(
                    str(fmt.format(_allocation.hazard_rate_goal)))

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):
        """
        Responds to gtk.Entry() focus_out signals and calls the correct
        function or method, passing any parameters as needed.

        :param gtk.Entry entry: the gtk.Entry() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param int index: the index in the handler ID list oc the callback
                          signal associated with the gtk.Entry() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        entry.handler_block(self._lst_handler_id[index])

        if index == 5:                      # Reliability goal
            _hardware_id = self._hardware_model.hardware_id
            _allocation = self.dtcAllocation.dicAllocation[_hardware_id]
            _allocation.reliability_goal = float(entry.get_text())
            _allocation.calculate_goals()

            # Set the other two goals.
            self.txtHazardRateGoal.handler_block(self._lst_handler_id[28])
            self.txtMTBFGoal.handler_block(self._lst_handler_id[29])
            self.txtHazardRateGoal.set_text(
                str(fmt.format(_allocation.hazard_rate_goal)))
            self.txtMTBFGoal.set_text(str(fmt.format(_allocation.mtbf_goal)))
            self.txtHazardRateGoal.handler_unblock(self._lst_handler_id[28])
            self.txtMTBFGoal.handler_unblock(self._lst_handler_id[29])
        elif index == 6:                    # Hazard rate goal
            _hardware_id = self._hardware_model.hardware_id
            _allocation = self.dtcAllocation.dicAllocation[_hardware_id]
            _allocation.hazard_rate_goal = float(entry.get_text())
            _allocation.calculate_goals()

            # Set the other two goals.
            self.txtReliabilityGoal.handler_block(self._lst_handler_id[27])
            self.txtMTBFGoal.handler_block(self._lst_handler_id[29])
            self.txtReliabilityGoal.set_text(
                str(fmt.format(_allocation.reliability_goal)))
            self.txtMTBFGoal.set_text(str(fmt.format(_allocation.mtbf_goal)))
            self.txtReliabilityGoal.handler_unblock(self._lst_handler_id[27])
            self.txtMTBFGoal.handler_unblock(self._lst_handler_id[29])
        elif index == 7:                    # MTBF goal
            _hardware_id = self._hardware_model.hardware_id
            _allocation = self.dtcAllocation.dicAllocation[_hardware_id]
            _allocation.mtbf_goal = float(entry.get_text())
            _allocation.calculate_goals()

            # Set the other two goals.
            self.txtReliabilityGoal.handler_block(self._lst_handler_id[27])
            self.txtHazardRateGoal.handler_block(self._lst_handler_id[28])
            self.txtReliabilityGoal.set_text(
                str(fmt.format(_allocation.reliability_goal)))
            self.txtHazardRateGoal.set_text(
                str(fmt.format(_allocation.hazard_rate_goal)))
            self.txtReliabilityGoal.handler_unblock(self._lst_handler_id[27])
            self.txtHazardRateGoal.handler_unblock(self._lst_handler_id[28])

        entry.handler_unblock(self._lst_handler_id[index])

        return False
