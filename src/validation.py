#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to
verification and validation tasks of the Program.
"""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       validation.py is part of The RTK Project
#
# All rights reserved.

import sys

# Modules required for the GUI.
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

# Import other RTK modules.
import configuration as _conf
from utilities import date_select, add_items
from widgets import make_label, make_text_view, make_treeview, create_legend, \
    load_plot, make_labels, make_frame, make_entry, make_button, load_combo, \
    make_combo

from datetime import datetime, date

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

import gettext
_ = gettext.gettext

# Plotting package.
import matplotlib
matplotlib.use('GTK')
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse


# noinspection PyUnresolvedReferences
class Validation(object):
    """
    The VALIDATION class is used to represent the verification and validation
    tasks for the system being analyzed.
    """

    #_ta_tab_labels = [_(u"Does this activity provide quantitative stress information as an output?"),
    #                  _(u"Does this activity provide quantitative strength information as an output?"),
    #                  _(u"Does this activity provide operating environment information as an output?"),
    #                  _(u"Hardware item configuration/architecture"),
    #                  _(u"Hardware item failure modes"),
    #                  _(u"Hardware item failure mechanisms"),
    #                  _(u"Hardware item failure causes"),
    #                  _(u"Hardware item failure times"),
    #                  _(u"Hardware item Part quality"),
    #                  _(u"Hardware item aging/degradation information"),
    #                  _(u"Hardware item design requirements and/or goals"),
    #                  _(u"")]

    def __init__(self, application):
        """
        Initializes the VALIDATION class.

        Keyword Arguments:
        application -- the RTK application.
        """

# Define private VALIDATION class attributes.
        self._app = application

# Define private VALIDATION class dictionary attributes.
        self._dic_types = {}                # Task types.
        self._dic_tasks = {}                # Dictionary containing all the task information.
        self._dic_status = {}

# Define private VALIDATION class list attributes.
        self._lst_col_order = []
        self._lst_handler_id = []

# Define public VALIDATION class attributes.
        self.validation_id = 0
        self.task_description = ''
        self.task_type = ''
        self.task_specification = ''
        self.measurement_unit = 0
        self.min_acceptable = 0.0
        self.mean_acceptable = 0.0
        self.max_acceptable = 0.0
        self.variance_acceptable = 0.0
        self.start_date = 719163
        self.end_date = 719163
        self.status = 0.0
        self.minimum_time = 0.0
        self.average_time = 0.0
        self.maximum_time = 0.0
        self.mean_time = 0.0
        self.time_variance = 0.0
        self.minimum_cost = 0.0
        self.average_cost = 0.0
        self.maximum_cost = 0.0
        self.mean_cost = 0.0
        self.cost_variance = 0.0

# Define public VALIDATION class dictionary attributes.

# Create the main VALIDATION class treeview.
        bg_color = _conf.RTK_COLORS[8]
        fg_color = _conf.RTK_COLORS[9]
        (self.treeview,
         self._lst_col_order) = make_treeview('Validation', 4,
                                              self._app, None,
                                              bg_color, fg_color)

# Toolbar widgets.

# General Data tab widgets.
        self.btnEndDate = make_button(_height_=25, _width_=25, _label_="...",
                                      _image_=None)
        self.btnStartDate = make_button(_height_=25, _width_=25, _label_="...",
                                        _image_=None)

        self.cmbTaskType = make_combo()
        self.cmbMeasurementUnit = make_combo()
        self.spnStatus = gtk.SpinButton()
        self.txtID = make_entry(width=50, editable=False)
        self.txtMaxAcceptable = make_entry(width=100)
        self.txtMeanAcceptable = make_entry(width=100)
        self.txtMinAcceptable = make_entry(width=100)
        self.txtVarAcceptable = make_entry(width=100)
        self.txtSpecification = make_entry()
        self.txtTask = make_text_view(width=400)
        self.txtEndDate = make_entry(width=100)
        self.txtStartDate = make_entry(width=100)
        self.txtMinTime = make_entry(width=100)
        self.txtExpTime = make_entry(width=100)
        self.txtMaxTime = make_entry(width=100)
        self.txtMinCost = make_entry(width=100)
        self.txtExpCost = make_entry(width=100)
        self.txtMaxCost = make_entry(width=100)
        self.txtMeanTimeLL = make_entry(width=100, editable=False)
        self.txtMeanTime = make_entry(width=100, editable=False)
        self.txtMeanTimeUL = make_entry(width=100, editable=False)
        self.txtMeanCostLL = make_entry(width=100, editable=False)
        self.txtMeanCost = make_entry(width=100, editable=False)
        self.txtMeanCostUL = make_entry(width=100, editable=False)

        # These widgets are for the Project Effort.
        self.txtProjectTimeLL = make_entry(width=100, editable=False)
        self.txtProjectTime = make_entry(width=100, editable=False)
        self.txtProjectTimeUL = make_entry(width=100, editable=False)
        self.txtProjectCostLL = make_entry(width=100, editable=False)
        self.txtProjectCost = make_entry(width=100, editable=False)
        self.txtProjectCostUL = make_entry(width=100, editable=False)

# Create the Plot tab widgets.
        _figure_ = Figure()
        self.pltPlot1 = FigureCanvas(_figure_)
        self.axAxis1 = _figure_.add_subplot(111)

# Put it all together.
        _toolbar_ = self._create_toolbar()

        self.notebook = self._create_notebook()

        self.vbxValidation = gtk.VBox()
        self.vbxValidation.pack_start(_toolbar_, expand=False)
        self.vbxValidation.pack_start(self.notebook)

        #self.notebook.connect('switch-page', self._notebook_page_switched)

        self._ready = True

    def create_tree(self):
        """
        Creates the Validation TreeView and connects it to callback functions
        to handle editing.  Background and foreground colors can be set using
        the user-defined values in the RTK configuration file.
        """

        _scrollwindow_ = gtk.ScrolledWindow()

        self.treeview.set_enable_tree_lines(True)

# Connect the cells to the callback function.
        for i in range(2, 23):
            _cell_ = self.treeview.get_column(self._lst_col_order[i]).get_cell_renderers()
            _cell_[0].connect('edited', self._vandv_tree_edit, i,
                              self.treeview.get_model())

        _scrollwindow_.add(self.treeview)

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)

        return _scrollwindow_

    def _create_toolbar(self):
        """
        Method to create the toolbar for the VALIDATAION class Work Book.
        """

        _toolbar_ = gtk.Toolbar()

        _pos_ = 0

# Add item button.  Depending on the notebook page selected will determine what
# type of item is added.
        _button_ = gtk.ToolButton()
        _image_ = gtk.Image()
        _image_.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        _button_.set_icon_widget(_image_)
        _button_.set_name('Add')
        _button_.connect('clicked', self.vandv_task_add)
        _button_.set_tooltip_text(_(u"Adds a new V&V activity."))
        _toolbar_.insert(_button_, _pos_)
        _pos_ += 1

# Remove item button.  Depending on the notebook page selected will determine
# what type of item is removed.
        _button_ = gtk.ToolButton()
        _image_ = gtk.Image()
        _image_.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        _button_.set_icon_widget(_image_)
        _button_.set_name('Remove')
        _button_.connect('clicked', self._vandv_task_delete)
        _button_.set_tooltip_text(_(u"Deletes the selected V&V activity."))
        _toolbar_.insert(_button_, _pos_)
        _pos_ += 1

        _toolbar_.insert(gtk.SeparatorToolItem(), _pos_)
        _pos_ += 1

# Calculate button.
        _button_ = gtk.ToolButton()
        _image_ = gtk.Image()
        _image_.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        _button_.set_icon_widget(_image_)
        _button_.set_name('Analyze')
        _button_.connect('clicked', self._calculate)
        _button_.set_tooltip_text(_(u"Calculates program V&V effort and plots the results."))
        _toolbar_.insert(_button_, _pos_)
        _pos_ += 1

        _toolbar_.insert(gtk.SeparatorToolItem(), _pos_)
        _pos_ += 1

# Save results button.  Depending on the notebook page selected will determine
# which results are saved.
        _button_ = gtk.ToolButton()
        _image_ = gtk.Image()
        _image_.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        _button_.set_icon_widget(_image_)
        _button_.set_name('Save')
        _button_.connect('clicked', self.validation_save)
        _button_.set_tooltip_text(_(u"Saves the selected V&V activity."))
        _toolbar_.insert(_button_, _pos_)

        _toolbar_.show()

        return _toolbar_

    def _create_notebook(self):
        """
        Method to create the VALIDATION class gtk.Notebook().
        """

        def _create_general_data_tab(v, notebook):
            """
            Function to create the VALIDATION class gtk.Notebook() page for
            displaying general data about the selected VALIDATION.

            Keyword Arguments:
            v        -- the current instance of a VALIDATION class.
            notebook -- the VALIDATION class gtk.Notebook() widget.
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hbox_ = gtk.HBox()

            # Build the quadrant 1 (upper left) containers.
            _fxdGenDataQuad1_ = gtk.Fixed()

            _scrollwindow_ = gtk.ScrolledWindow()
            _scrollwindow_.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            _scrollwindow_.add_with_viewport(_fxdGenDataQuad1_)

            _frame_ = make_frame(_label_=_(u"Task Description"))
            _frame_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame_.add(_scrollwindow_)

            _hbox_.pack_start(_frame_, True, True)

            # Build the quadrant 2 (upper right) containers.
            _vpaned_ = gtk.VPaned()

            _fxdGenDataQuad2_ = gtk.Fixed()

            _scrollwindow_ = gtk.ScrolledWindow()
            _scrollwindow_.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            _scrollwindow_.add_with_viewport(_fxdGenDataQuad2_)

            _frame_ = make_frame(_label_=_(u"Task Effort"))
            _frame_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame_.add(_scrollwindow_)

            _vpaned_.pack1(_frame_, True, True)

            # Build the quadrant 4 (lower right) containers.
            _fxdGenDataQuad4_ = gtk.Fixed()

            _scrollwindow_ = gtk.ScrolledWindow()
            _scrollwindow_.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            _scrollwindow_.add_with_viewport(_fxdGenDataQuad4_)

            _frame_ = make_frame(_label_=_(u"Project Effort"))
            _frame_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame_.add(_scrollwindow_)

            _vpaned_.pack2(_frame_, True, True)

            _hbox_.pack_end(_vpaned_)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display general information.        #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Load the gtk.ComboBox() widgets.
            _query_ = "SELECT fld_validation_type_desc \
                       FROM tbl_validation_type"
            _results_ = v._app.COMDB.execute_query(_query_,
                                                   None,
                                                   v._app.ComCnx)
            load_combo(v.cmbTaskType, _results_)

            _query_ = "SELECT fld_measurement_code \
                       FROM tbl_measurement_units"
            _results_ = v._app.COMDB.execute_query(_query_,
                                                   None,
                                                   v._app.ComCnx)
            load_combo(v.cmbMeasurementUnit, _results_)

            # Create the labels for quadrant #1.
            _labels_ = [_(u"Task ID:"), _(u"Task Description:"),
                        _(u"Task Type:"), _(u"Specification:"),
                        _(u"Measurement Unit:"), _(u"Minimum Acceptable:"),
                        _(u"Maximum Acceptable:"), _(u"Mean Acceptable:"),
                        _(u"Variance:")]

            _max1_ = 0
            _max2_ = 0
            (_max1_, _y_pos_) = make_labels(_labels_[2:],
                                            _fxdGenDataQuad1_, 5, 140)

            _label_ = make_label(_labels_[0], -1, 25)
            _fxdGenDataQuad1_.put(_label_, 5, 5)
            _max2_ = _label_.size_request()[0]
            _x_pos_ = max(_max1_, _max2_) + 20

            _label_ = make_label(_labels_[1], 150, 25)
            _fxdGenDataQuad1_.put(_label_, 5, 35)
            _max2_ = _label_.size_request()[0]
            _x_pos_ = max(_x_pos_, _max2_) + 20

            # Place the quadrant #1 widgets.
            v.txtID.set_tooltip_text(_(u"Displays the unique code for the selected V&V activity."))
            _fxdGenDataQuad1_.put(v.txtID, _x_pos_, 5)

            v.txtTask.set_tooltip_text(_(u"Displays the description of the selected V&V activity."))
            _fxdGenDataQuad1_.put(v.txtTask, _x_pos_, 35)
            _buffer_ = v.txtTask.get_child().get_child()
            _id_ = _buffer_.connect('focus-out-event', v._callback_entry,
                                    'text', 2)
            v._lst_handler_id.append(_id_)

            v.cmbTaskType.set_tooltip_text(_(u"Selects and displays the type of task for the selected V&V activity."))
            _fxdGenDataQuad1_.put(v.cmbTaskType, _x_pos_, _y_pos_[0])
            _id_ = v.cmbTaskType.connect('changed', v._callback_combo, 3)
            v._lst_handler_id.append(_id_)

            v.txtSpecification.set_tooltip_text(_(u"Displays the internal or industry specification or procedure governing the selected V&V activity."))
            _fxdGenDataQuad1_.put(v.txtSpecification, _x_pos_, _y_pos_[1])
            _id_ = v.txtSpecification.connect('focus-out-event',
                                              v._callback_entry,
                                              'text', 4)
            v._lst_handler_id.append(_id_)

            v.cmbMeasurementUnit.set_tooltip_text(_(u"Selects and displays the measurement unit for the selected V&V activity acceptance parameter."))
            _fxdGenDataQuad1_.put(v.cmbMeasurementUnit, _x_pos_,
                                  _y_pos_[2] - 3)
            _id_ = v.cmbMeasurementUnit.connect('changed',
                                                v._callback_combo, 5)
            v._lst_handler_id.append(_id_)

            v.txtMinAcceptable.set_tooltip_text(_(u"Displays the minimum acceptable value for the selected V&V activity."))
            _fxdGenDataQuad1_.put(v.txtMinAcceptable, _x_pos_, _y_pos_[3])
            _id_ = v.txtMinAcceptable.connect('focus-out-event',
                                              v._callback_entry,
                                              'float', 6)
            v._lst_handler_id.append(_id_)

            v.txtMeanAcceptable.set_tooltip_text(_(u"Displays the mean acceptable value for the selected V&V activity."))
            _fxdGenDataQuad1_.put(v.txtMaxAcceptable, _x_pos_, _y_pos_[4])
            _id_ = v.txtMeanAcceptable.connect('focus-out-event',
                                               v._callback_entry,
                                               'float', 7)
            v._lst_handler_id.append(_id_)

            v.txtMaxAcceptable.set_tooltip_text(_(u"Displays the maximum acceptable value for the selected V&V activity."))
            _fxdGenDataQuad1_.put(v.txtMeanAcceptable, _x_pos_, _y_pos_[5])
            _id_ = v.txtMaxAcceptable.connect('focus-out-event',
                                              v._callback_entry,
                                              'float', 8)
            v._lst_handler_id.append(_id_)

            v.txtVarAcceptable.set_tooltip_text(_(u"Displays the acceptable variance for the selected V&V activity."))
            _fxdGenDataQuad1_.put(v.txtVarAcceptable, _x_pos_, _y_pos_[6])
            _id_ = v.txtVarAcceptable.connect('focus-out-event',
                                              v._callback_entry,
                                              'float', 9)
            v._lst_handler_id.append(_id_)

            _fxdGenDataQuad1_.show_all()

            # Create the labels for quadrant #2.
            _labels_ = [_(u"Start Date:"), _(u"End Date:"), _(u"% Complete:"),
                        _(u"Minimum Task Time:"), _(u"Most Likely Task Time:"),
                        _(u"Maximum Task Time:"),
                        _(u"Task Time (95% Confidence):"),
                        _(u"Minimum Task Cost:"), _(u"Most Likely Task Cost:"),
                        _(u"Maximum Task Cost:"),
                        _(u"Task Cost (95% Confidence):")]
            (_max1_,
             _y_pos1_) = make_labels(_labels_, _fxdGenDataQuad2_, 5, 5)

            # Create the labels for quadrant #4.
            _labels_ = [_(u"Project Time (95% Confidence):"),
                        _(u"Project Cost (95% Confidence):")]
            (_max2_,
             _y_pos2_) = make_labels(_labels_, _fxdGenDataQuad4_, 5, 5)
            _x_pos_ = max(_max1_, _max2_) + 20

            # Place the quadrant #2 widgets.
            v.btnEndDate.set_tooltip_text(_(u"Launches the calendar to select the date the task was completed."))
            _fxdGenDataQuad2_.put(v.btnEndDate, _x_pos_ + 105, _y_pos1_[1])
            v.btnEndDate.connect('released', date_select,
                                 v.txtEndDate)

            v.btnStartDate.set_tooltip_text(_(u"Launches the calendar to select the date the task was started."))
            _fxdGenDataQuad2_.put(v.btnStartDate, _x_pos_ + 105, _y_pos1_[0])
            v.btnStartDate.connect('released', date_select,
                                   v.txtStartDate)

            v.txtStartDate.set_tooltip_text(_(u"Displays the date the selected V&V activity is scheduled to start."))
            _fxdGenDataQuad2_.put(v.txtStartDate, _x_pos_, _y_pos1_[0])
            v.txtStartDate.connect('changed',
                                   v._callback_entry, None, 'text', 10)
            _id_ = v.txtStartDate.connect('focus-out-event',
                                          v._callback_entry, 'text', 10)
            v._lst_handler_id.append(_id_)

            v.txtEndDate.set_tooltip_text(_(u"Displays the date the selected V&V activity is scheduled to end."))
            _fxdGenDataQuad2_.put(v.txtEndDate, _x_pos_, _y_pos1_[1])
            v.txtEndDate.connect('changed',
                                 v._callback_entry, None, 'text', 11)
            _id_ = v.txtEndDate.connect('focus-out-event',
                                        v._callback_entry, 'text', 11)
            v._lst_handler_id.append(_id_)

            # Set the spin button to be a 0-100 in steps of 0.1 spinner.  Only
            # update if value is numeric and within range.
            v.spnStatus.set_adjustment(gtk.Adjustment(0, 0, 100, 1, 0.1))
            v.spnStatus.set_update_policy(gtk.UPDATE_IF_VALID)
            v.spnStatus.set_numeric(True)
            v.spnStatus.set_snap_to_ticks(True)
            v.spnStatus.set_tooltip_text(
                _(u"Displays % complete of the selected V&V activity."))
            _fxdGenDataQuad2_.put(v.spnStatus, _x_pos_, _y_pos1_[2])
            _id_ = v.spnStatus.connect('value-changed',
                                       v._callback_spin, 'float', 12)
            v._lst_handler_id.append(_id_)

            v.txtMinTime.set_tooltip_text(_(u"Minimum person-time needed to complete the selected task."))
            _fxdGenDataQuad2_.put(v.txtMinTime, _x_pos_, _y_pos1_[3])
            v.txtMinTime.connect('focus-out-event',
                                 v._callback_entry, 'float', 13)
            v._lst_handler_id.append(_id_)

            v.txtExpTime.set_tooltip_text(_(u"Most likely person-time needed to complete the selected task."))
            _fxdGenDataQuad2_.put(v.txtExpTime, _x_pos_, _y_pos1_[4])
            v.txtExpTime.connect('focus-out-event',
                                 v._callback_entry, 'float', 14)
            v._lst_handler_id.append(_id_)

            v.txtMaxTime.set_tooltip_text(_(u"Maximum person-time needed to complete the selected task."))
            _fxdGenDataQuad2_.put(v.txtMaxTime, _x_pos_, _y_pos1_[5])
            v.txtMaxTime.connect('focus-out-event',
                                 v._callback_entry, 'float', 15)
            v._lst_handler_id.append(_id_)

            _fxdGenDataQuad2_.put(v.txtMeanTimeLL, _x_pos_, _y_pos1_[6])
            _fxdGenDataQuad2_.put(v.txtMeanTime, _x_pos_ + 105, _y_pos1_[6])
            _fxdGenDataQuad2_.put(v.txtMeanTimeUL, _x_pos_ + 210, _y_pos1_[6])

            v.txtMinCost.set_tooltip_text(_(u"Minimim cost of the selected task."))
            _fxdGenDataQuad2_.put(v.txtMinCost, _x_pos_, _y_pos1_[7])
            v.txtMinCost.connect('focus-out-event',
                                 v._callback_entry, 'float', 18)
            v._lst_handler_id.append(_id_)

            v.txtExpCost.set_tooltip_text(_(u"Most likely cost of the selected task."))
            v.txtExpCost.connect('focus-out-event',
                                 v._callback_entry, 'float', 19)
            _fxdGenDataQuad2_.put(v.txtExpCost, _x_pos_, _y_pos1_[8])
            v._lst_handler_id.append(_id_)

            v.txtMaxCost.set_tooltip_text(_(u"Maximum cost of the selected task."))
            _fxdGenDataQuad2_.put(v.txtMaxCost, _x_pos_, _y_pos1_[9])
            v.txtMaxCost.connect('focus-out-event',
                                 v._callback_entry, 'float', 20)
            v._lst_handler_id.append(_id_)

            _fxdGenDataQuad2_.put(v.txtMeanCostLL, _x_pos_, _y_pos1_[10])
            _fxdGenDataQuad2_.put(v.txtMeanCost, _x_pos_ + 105, _y_pos1_[10])
            _fxdGenDataQuad2_.put(v.txtMeanCostUL, _x_pos_ + 210, _y_pos1_[10])

            _fxdGenDataQuad2_.show_all()

            # Place the quadrant #4 widgets.
            #v.txtMeanCost.set_tooltip_text(_(u"Average estimated cost to complete the project."))
            #v.txtMeanTime.set_tooltip_text(_(u"Average estimated time needed to complete the project."))
            _fxdGenDataQuad4_.put(v.txtProjectTimeLL, _x_pos_, _y_pos2_[0])
            _fxdGenDataQuad4_.put(v.txtProjectTime, _x_pos_ + 105, _y_pos2_[0])
            _fxdGenDataQuad4_.put(v.txtProjectTimeUL, _x_pos_ + 210, _y_pos2_[0])
            _fxdGenDataQuad4_.put(v.txtProjectCostLL, _x_pos_, _y_pos2_[1])
            _fxdGenDataQuad4_.put(v.txtProjectCost, _x_pos_ + 105, _y_pos2_[1])
            _fxdGenDataQuad4_.put(v.txtProjectCostUL, _x_pos_ + 210, _y_pos2_[1])

            _fxdGenDataQuad4_.show_all()

            # Insert the tab.
            _label_ = gtk.Label()
            _label_.set_markup("<span weight='bold'>" +
                               _(u"General\nData") +
                               "</span>")
            _label_.set_alignment(xalign=0.5, yalign=0.5)
            _label_.set_justify(gtk.JUSTIFY_CENTER)
            _label_.show_all()
            _label_.set_tooltip_text(_(u"Displays general information about the selected V&V task."))
            notebook.insert_page(_hbox_,
                                 tab_label=_label_,
                                 position=-1)

        def _create_plot_tab(self, notebook):
            """
            Method to create the gtk.Notebook() tab and populate it with the
            appropriate widgets for the plot showing the planned and actual
            burndown of V&V tasks.
            """

            _hbox_ = gtk.HBox()

            _frame_ = make_frame(_label_=_(u""))
            _frame_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame_.add(_hbox_)
            _frame_.show_all()

            _hbox_.pack_start(self.pltPlot1)

            # Insert the tab.
            _label_ = gtk.Label()
            _label_.set_markup("<span weight='bold'>" +
                               _(u"Program\nProgress") +
                               "</span>")
            _label_.set_alignment(xalign=0.5, yalign=0.5)
            _label_.set_justify(gtk.JUSTIFY_CENTER)
            _label_.show_all()
            _label_.set_tooltip_text(_(u"Shows a plot of the total expected time to complete all V&amp;V tasks and the current progress."))
            notebook.insert_page(_frame_,
                                 tab_label=_label_,
                                 position=-1)

            return False

        _notebook_ = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if _conf.TABPOS[2] == 'left':
            _notebook_.set_tab_pos(gtk.POS_LEFT)
        elif _conf.TABPOS[2] == 'right':
            _notebook_.set_tab_pos(gtk.POS_RIGHT)
        elif _conf.TABPOS[2] == 'top':
            _notebook_.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook_.set_tab_pos(gtk.POS_BOTTOM)

        _create_general_data_tab(self, _notebook_)
        _create_plot_tab(self, _notebook_)

        return _notebook_

    def load_tree(self):
        """
        Loads the Validation treeview model with information from the RTK
        Program database.
        """

# Load the Requirement Type gtk.CellRendererCombo().
        _query_ = "SELECT fld_validation_type_desc \
                   FROM tbl_validation_type"
        _results_ = self._app.COMDB.execute_query(_query_,
                                                  None,
                                                  self._app.ComCnx)

        if _results_ == '' or not _results_ or _results_ is None:
            pass

        # Load the gtk.CellRendererCombo() and the the local dictionary
        # holding the task types.  The noun name of the task type is the
        # dictionary key and the position in the list is the dictionary value.
        _cell_ = self.treeview.get_column(self._lst_col_order[3]).get_cell_renderers()
        _model_ = _cell_[0].get_property('model')
        _model_.clear()
        _model_.append([""])
        for i in range(len(_results_)):
            _model_.append([_results_[i][0]])
            self._dic_types[_results_[i][0]] = i + 1

# Load the task status dictionary.
        _query_ = "SELECT fld_update_date, fld_time_remaining, \
                          fld_cost_remaining \
                   FROM tbl_validation_status \
                   WHERE fld_revision_id=%d" % self._app.REVISION.revision_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        _n_updates_ = len(_results_)
        for i in range(_n_updates_):
            self._dic_status[_results_[i][0]] = _results_[i][1]

# Select everything from the validation table.
        _query_ = "SELECT * FROM tbl_validation \
                   WHERE fld_revision_id=%d \
                   ORDER BY fld_validation_id" % self._app.REVISION.revision_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if _results_ == '' or not _results_ or _results_ is None:
            return True

# Add all the tasks to the Tree Book and initialize the .
        _n_tasks_ = len(_results_)
        _model_ = self.treeview.get_model()
        _model_.clear()
        for i in range(_n_tasks_):
            _start_ = str(datetime.fromordinal(int(_results_[i][10])).strftime('%Y-%m-%d'))
            _end_ = str(datetime.fromordinal(int(_results_[i][11])).strftime('%Y-%m-%d'))
            _model_.append(None, [_results_[i][0], _results_[i][1],
                                  _results_[i][2], _results_[i][3],
                                  _results_[i][4], _results_[i][5],
                                  _results_[i][6], _results_[i][7],
                                  _results_[i][8], _results_[i][9],
                                  _start_, _end_, _results_[i][12],
                                  _results_[i][13], _results_[i][14],
                                  _results_[i][15], _results_[i][16],
                                  _results_[i][17], _results_[i][18],
                                  _results_[i][19], _results_[i][20],
                                  _results_[i][21], _results_[i][22]])
            self._dic_tasks[_results_[i][1]] = [_results_[i][10],
                                                _results_[i][11],
                                                _results_[i][13],
                                                _results_[i][14],
                                                _results_[i][15],
                                                _results_[i][12],
                                                _results_[i][17],
                                                _results_[i][18],
                                                _results_[i][19],
                                                _results_[i][20],
                                                _results_[i][22]]

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)

        root = _model_.get_iter_root()
        if root is not None:
            path = _model_.get_path(root)
            col = self.treeview.get_column(0)
            self.treeview.row_activated(path, col)

        return False

    def load_notebook(self):
        """
        Method to load the VALIDATION class gtk.Notebook.
        """

        def _load_general_data_tab(self):
            """
            Loads the widgets with general information about the VALIDATION class.
            """

            fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

            (_model_, _row_) = self.treeview.get_selection().get_selected()

            try:
                _index_ = self._dic_types[_model_.get_value(_row_, 3)]
            except KeyError:
                _index_ = 0

            try:
                self.txtID.set_text(str(_model_.get_value(_row_, 1)))
                _textbuffer_ = self.txtTask.get_child().get_child().get_buffer()
                _textbuffer_.set_text(_model_.get_value(_row_, 2))
                self.cmbTaskType.set_active(_index_)
                self.txtSpecification.set_text(str(_model_.get_value(_row_, 4)))
                self.cmbMeasurementUnit.set_active(int(_model_.get_value(_row_, 5)))
                self.txtMinAcceptable.set_text(str(_model_.get_value(_row_, 6)))
                self.txtMeanAcceptable.set_text(str(_model_.get_value(_row_, 7)))
                self.txtMaxAcceptable.set_text(str(_model_.get_value(_row_, 8)))
                self.txtVarAcceptable.set_text(str(_model_.get_value(_row_, 9)))
                self.txtStartDate.set_text(str(_model_.get_value(_row_, 10)))
                self.txtEndDate.set_text(str(_model_.get_value(_row_, 11)))
                self.spnStatus.set_value(_model_.get_value(_row_, 12))
                self.txtMinTime.set_text(str(fmt.format(_model_.get_value(_row_, 13))))
                self.txtExpTime.set_text(str(fmt.format(_model_.get_value(_row_, 14))))
                self.txtMaxTime.set_text(str(fmt.format(_model_.get_value(_row_, 15))))
                self.txtMinCost.set_text(str(fmt.format(_model_.get_value(_row_, 18))))
                self.txtExpCost.set_text(str(fmt.format(_model_.get_value(_row_, 19))))
                self.txtMaxCost.set_text(str(fmt.format(_model_.get_value(_row_, 20))))
            except IndexError:                  # There are no V&V tasks.
                pass

            return False

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        if _row_ is not None:
            _load_general_data_tab(self)
            self._calculate()

        if self._app.winWorkBook.get_child() is not None:
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxValidation)
        self._app.winWorkBook.show_all()

        try:
            _title_ = _(u"RTK Work Book: Analyzing %s") % \
                _model_.get_value(_row_, 2)
        except TypeError:
            _title_ = _(u"RTK Work Book")
        self._app.winWorkBook.set_title(_title_)

        return False

    def _update_tree(self, columns, values):
        """
        Updates the values in the VALIDATION class gtk.Treeview.

        Keyword Arguments:
        columns -- a list of integers representing the column numbers to
                   update.
        values  -- a list of new values for the VALIDATION class
                   TreeView.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()
        for i in columns:
            _model_.set_value(_row_, i, values[i])

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the VALIDATION class
        gtk.Treeview.

        Keyword Arguments:
        treeview -- the VALIDATION class treeview.
        event    -- a gtk.gdk.Event that called this function (the
                    important attribute is which mouse button was clicked).
                    1 = left
                    2 = scrollwheel
                    3 = right
                    4 = forward
                    5 = backward
                    8 =
                    9 =
        """

# TODO: Add a pop-up menu that is launched with a right click.
        if event.button == 1:
            self._treeview_row_changed(treeview, None, 0)
        elif event.button == 3:
            print "Pop-up a menu!"

        return False

    def _treeview_row_changed(self, __treeview, __path, __column):
        """
        Callback function to handle events for the VALIDATION class
        gtk.Treeview.  It is called whenever the VALIDATION class gtk.Treeview
        is clicked or a row is activated.  It will save the previously selected
        row in the VALIDATION class treeview.

        Keyword Arguments:
        __treeview -- the VALIDATION class gtk.TreeView.
        __path     -- the activated row gtk.TreeView path.
        __column   -- the activated gtk.TreeViewColumn.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        if _row_ is not None:
            self.load_notebook()

            return False
        else:
            return True

    def _vandv_tree_edit(self, __cell, path, new_text, position, model):
        """
        Called whenever a VALIDATION class gtk.Treeview() gtk.CellRenderer()
        is edited.

        Keyword Arguments:
        __cell   -- the CellRenderer that was edited.
        path     -- the TreeView path of the CellRenderer that was edited.
        new_text -- the new text in the edited CellRenderer.
        position -- the column position of the edited CellRenderer.
        model    -- the TreeModel the CellRenderer belongs to.
        """

# Update the gtk.TreeModel() with the new value.
        _type_ = gobject.type_name(model.get_column_type(position))

        if _type_ == 'gchararray':
            model[path][position] = str(new_text)
        elif _type_ == 'gint':
            model[path][position] = int(new_text)
        elif _type_ == 'gfloat':
            model[path][position] = float(new_text)

# Now update the associated gtk.Widget() in the Work Book with the new value.
# We block and unblock the signal handlers for the widgets so a race condition
# does not ensue.
        if self._lst_col_order[position] == 2:
            _buffer_ = self.txtTask.get_child().get_child().get_buffer()
            _buffer_.handler_block(self._lst_handler_id[0])
            _buffer_.set_text(str(new_text))
            _buffer_.handler_unblock(self._lst_handler_id[0])
        elif self._lst_col_order[position] == 3:
            try:
                _index_ = self._dic_types[new_text]
            except KeyError:
                _index_ = 0
            self.cmbTaskType.handler_block(self._lst_handler_id[1])
            self.cmbTaskType.set_active(_index_)
            self.cmbTaskType.handler_unblock(self._lst_handler_id[1])
        elif self._lst_col_order[position] == 4:
            self.txtSpecification.handler_block(self._lst_handler_id[2])
            self.txtSpecification.set_text(str(new_text))
            self.txtSpecification.handler_unblock(self._lst_handler_id[2])
        elif self._lst_col_order[position] == 5:
            self.cmbMeasurementUnit.handler_block(self._lst_handler_id[3])
            self.cmbMeasurementUnit.set_active(int(new_text))
            self.cmbMeasurementUnit.handler_unblock(self._lst_handler_id[3])
        elif self._lst_col_order[position] == 6:
            self.txtMinAcceptable.handler_block(self._lst_handler_id[4])
            self.txtMinAcceptable.set_text(str(new_text))
            self.txtMinAcceptable.handler_unblock(self._lst_handler_id[4])
        elif self._lst_col_order[position] == 7:
            self.txtMaxAcceptable.handler_block(self._lst_handler_id[5])
            self.txtMaxAcceptable.set_text(str(new_text))
            self.txtMaxAcceptable.handler_unblock(self._lst_handler_id[5])
        elif self._lst_col_order[position] == 8:
            self.txtMeanAcceptable.handler_block(self._lst_handler_id[6])
            self.txtMeanAcceptable.set_text(str(new_text))
            self.txtMeanAcceptable.handler_unblock(self._lst_handler_id[6])
        elif self._lst_col_order[position] == 9:
            self.txtVarAcceptable.handler_block(self._lst_handler_id[7])
            self.txtVarAcceptable.set_text(str(new_text))
            self.txtVarAcceptable.handler_unblock(self._lst_handler_id[7])
        elif self._lst_col_order[position] == 10:
            self.txtStartDate.handler_block(self._lst_handler_id[8])
            self.txtStartDate.set_text(str(new_text))
            self.txtStartDate.handler_unblock(self._lst_handler_id[8])
        elif self._lst_col_order[position] == 11:
            self.txtEndDate.handler_block(self._lst_handler_id[9])
            self.txtEndDate.set_text(str(new_text))
            self.txtEndDate.handler_unblock(self._lst_handler_id[9])
        elif self._lst_col_order[position] == 12:
            self.spnStatus.handler_block(self._lst_handler_id[10])
            _adjustment_ = self.spnStatus.get_adjustment()
            _adjustment_.set_value(float(new_text))
            self.spnStatus.update()
            self.spnStatus.handler_unblock(self._lst_handler_id[10])

        return False

    def vandv_task_add(self, widget):
        """
        Adds a new Verfication & Validation activity to the RTK Program's
        MySQL or SQLite3 database.

        Keyword Arguments:
        widget -- the widget that called this function.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

# Find the selected revision.
        _revision_ = self._app.REVISION.revision_id

        _n_tasks_ = add_items(title=_(u"RTK - Add V &amp; V Activity"),
                              prompt=_(u"How many V &amp; V activities to add?"))

        for i in range(_n_tasks_):
            _task_name_ = "New V&V Activity " + str(i)

            _query_ = "INSERT INTO tbl_validation \
                       (fld_revision_id, fld_task_desc) \
                       VALUES (%d, '%s')" % \
                      (_revision_, _task_name_)
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if not _results_:
                self._app.user_log.error("validation.py: Failed to add V&V task.")
                return True

        #self._app.REVISION.load_tree()
        self.load_tree

        return False

    def _vandv_task_delete(self, menuitem):
        """
        Deletes the currently selected V&V activity from the RTK Program's
        MySQL or SQLite3 database.

        Keyword Arguments:
        menuitem -- the gtk.MenuItem that called this function.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        _values_ = (self._app.REVISION.revision_id,
                    _model_.get_value(_row_, 1))

        _query_ = "DELETE FROM tbl_validation \
                   WHERE fld_revision_id=%d \
                   AND fld_validation_id=%d" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)
        if not _results_:
            self._app.user_log.error("validation.py: Failed to delete V&V task.")
            return True

        self.load_tree

        return False

    def validation_save(self, widget=None):
        """
        Saves the VALIDATION class gtk.TreeView() information to the open RTK
        Program database.

        Keyword Arguments:
        widget -- the widget that called this function.
        """

        def _save_line_item(model, path_, row, self):
            """
            Function to save each row in the VALIDATION class gtk.TreeModel()
            to the open RTK Program's database.

            Keyword Arguments:
            model -- the VALIDATION class gtk.TreeModel().
            path_ -- the path of the active row in the VALIDATION class
                     gtk.TreeModel().
            row   -- the selected row in the VALIDATION class gtk.TreeView().
            """

            _start_ = datetime.strptime(model.get_value(row, self._lst_col_order[10]), '%Y-%m-%d').toordinal()
            _end_ = datetime.strptime(model.get_value(row, self._lst_col_order[11]), '%Y-%m-%d').toordinal()
            _values_ = (model.get_value(row, self._lst_col_order[2]),
                        model.get_value(row, self._lst_col_order[3]),
                        model.get_value(row, self._lst_col_order[4]),
                        model.get_value(row, self._lst_col_order[5]),
                        model.get_value(row, self._lst_col_order[6]),
                        model.get_value(row, self._lst_col_order[7]),
                        model.get_value(row, self._lst_col_order[8]),
                        model.get_value(row, self._lst_col_order[9]),
                        _start_, _end_,
                        model.get_value(row, self._lst_col_order[12]),
                        model.get_value(row, self._lst_col_order[13]),
                        model.get_value(row, self._lst_col_order[14]),
                        model.get_value(row, self._lst_col_order[15]),
                        model.get_value(row, self._lst_col_order[16]),
                        model.get_value(row, self._lst_col_order[17]),
                        model.get_value(row, self._lst_col_order[18]),
                        model.get_value(row, self._lst_col_order[19]),
                        model.get_value(row, self._lst_col_order[20]),
                        model.get_value(row, self._lst_col_order[21]),
                        model.get_value(row, self._lst_col_order[22]),
                        self._app.REVISION.revision_id,
                        model.get_value(row, self._lst_col_order[1]))

            _query_ = "UPDATE tbl_validation \
                       SET fld_task_desc='%s', fld_task_type='%s', \
                           fld_task_specification='%s', \
                           fld_measurement_unit=%d, fld_min_acceptable=%f, \
                           fld_mean_acceptable=%f, fld_max_acceptable=%f, \
                           fld_variance_acceptable=%f, fld_start_date=%d, \
                           fld_end_date=%d, fld_status=%f, \
                           fld_minimum_time=%f, fld_average_time=%f, \
                           fld_maximum_time=%f, fld_mean_time=%f, \
                           fld_time_variance=%f, fld_minimum_cost=%f, \
                           fld_average_cost=%f, fld_maximum_cost=%f, \
                           fld_mean_cost=%f, fld_cost_variance=%f \
                       WHERE fld_revision_id=%d \
                       AND fld_validation_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if not _results_:
                self._app.debug_log.error("validation.py: Failed to save V&V task.")
                return True

            return False

        _model_ = self.treeview.get_model()
        _model_.foreach(_save_line_item, self)

        for i in range(len(self._dic_status.values())):
            _values_ = (self._dic_status[self._dic_status.keys()[i]],
                        self._dic_status.keys()[i],
                        self._app.REVISION.revision_id)
            _query_ = "UPDATE tbl_validation_status \
                       SET fld_time_remaining=%f \
                       WHERE fld_update_date=%d \
                       AND fld_revision_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)
            if _results_:
                _query_ = "INSERT INTO tbl_validation_status \
                                       (fld_time_remaining, fld_update_date, \
                                        fld_revision_id) \
                           VALUES(%f, %d, %d)" % _values_
                _results_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx,
                                                       commit=True)

        return False

    def _callback_combo(self, combo, index):
        """
        Callback function to retrieve and save combobox changes.

        Keyword Arguments:
        combo -- the combobox that called the function.
        index -- the position in the VALIDATION class _attribute list
                 associated with the data from the calling combobox.
        """

# Update the Validation Tree.
        if index == 3:                      # Task type
            _model_ = combo.get_model()
            _row_ = combo.get_active_iter()
            _data_ = _model_.get_value(_row_, 0)
        else:
            _data_ = int(combo.get_active())

        (_model_, _row_) = self.treeview.get_selection().get_selected()
        _model_.set_value(_row_, index, _data_)

        return False

    def _callback_entry(self, entry, event, convert, index):
        """
        Callback function to retrieve and save entry changes.

        Keyword Arguments:
        entry   -- the entry that called the function.
        event   -- the gtk.gdk.Event() that called this function.
        convert -- the data type to convert the entry contents to.
        index   -- the position in the VALIDATION class _attribute list
                   associated with the data from the calling entry.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        if convert == 'text':
            if index == 2:
                textbuffer = self.txtTask.get_child().get_child().get_buffer()
                _text_ = textbuffer.get_text(*textbuffer.get_bounds())
            else:
                _text_ = entry.get_text()
        elif convert == 'int':
            _text_ = int(entry.get_text())
        elif convert == 'float':
            try:
                _text_ = float(entry.get_text().replace('$', ''))
            except ValueError:
                _text_ = ""

# Update the Validation Tree.
        (_model_, _row_) = self.treeview.get_selection().get_selected()
        try:
            _model_.set_value(_row_, index, _text_)
        except TypeError:
            print index

# Calculate task time estimates.
        if index == 13 or index == 14 or index == 15:
            _a_ = float(_model_.get_value(_row_, 13))
            _m_ = float(_model_.get_value(_row_, 14))
            _b_ = float(_model_.get_value(_row_, 15))

            # Calculate assuming a beta distribution.
            _mean_ = (_a_ + 4.0 * _m_ + _b_) / 6.0
            _sd_ = (_b_ - _a_) / 6.0

            _meanll_ = _mean_ - 1.945 * _sd_
            _meanul_ = _mean_ + 1.945 * _sd_

            self.txtMeanTimeLL.set_text(str(fmt.format(_meanll_)))
            self.txtMeanTime.set_text(str(fmt.format(_mean_)))
            self.txtMeanTimeUL.set_text(str(fmt.format(_meanul_)))

# Calculate task cost estimates.
        if index == 18 or index == 19 or index == 20:
            _a_ = float(_model_.get_value(_row_, 18))
            _m_ = float(_model_.get_value(_row_, 19))
            _b_ = float(_model_.get_value(_row_, 20))

            _mean_ = (_a_ + 4 * _m_ + _b_) / 6.0
            _sd_ = (_b_ - _a_) / 6.0

            _meanll_ = _mean_ - 1.945 * _sd_
            _meanul_ = _mean_ + 1.945 * _sd_

            self.txtMeanCostLL.set_text(str(fmt.format(_meanll_)))
            self.txtMeanCost.set_text(str(fmt.format(_mean_)))
            self.txtMeanCostUL.set_text(str(fmt.format(_meanul_)))

        return False

    def _callback_spin(self, spinbutton, convert, index):
        """
        Callback function to retrieve and save spinbutton changes.

        Keyword Arguments:
        spinbutton -- the gtk.SpinButton() that called this function.
        convert    -- the data type to convert the entry contents to.
        index      -- the position in the VALIDATION class _attribute list
                      associated with the data from the calling entry.
        """

        _text_ = float(spinbutton.get_value())

# Update the Validation Tree.
        (_model_, _row_) = self.treeview.get_selection().get_selected()
        try:
            _model_.set_value(_row_, index, _text_)
        except TypeError:
            print index

        return False

    def _calculate(self, button=None):
        """
        Method to calculate the expected task time, lower limit, and upper
        limit on task time.

        Keyword Arguments:
        button -- the gtk.Button() that called this method.
        """

        from operator import itemgetter

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model_, _row_) = self.treeview.get_selection().get_selected()
        _row_ = _model_.get_iter_root()

        _assess_dates_ = []
        _targets_ = []
        while _row_ is not None:
            _id_ = _model_.get_value(_row_, 1)

# Calculate task time estimates.
            try:
                if _model_.get_value(_row_, 3) == "Reliability, Assessment":
                    _assess_dates_.append(datetime.strptime(_model_.get_value(_row_, 11), '%Y-%m-%d').toordinal())
                    _targets_.append([_model_.get_value(_row_, 6),
                                      _model_.get_value(_row_, 8)])

                _percent_ = float(_model_.get_value(_row_, 12))

                # Calculate mean task time assuming a beta distribution.
                _a_ = float(_model_.get_value(_row_, 13))
                _m_ = float(_model_.get_value(_row_, 14))
                _b_ = float(_model_.get_value(_row_, 15))

                _mean_ = (_a_ + 4.0 * _m_ + _b_) / 6.0
                _sd_ = (_b_ - _a_) / 6.0

                _model_.set_value(_row_, 16, _mean_)
                _model_.set_value(_row_, 17, _sd_)

                self._dic_tasks[_id_][2] = _mean_ - 1.945 * _sd_
                self._dic_tasks[_id_][3] = _mean_
                self._dic_tasks[_id_][4] = _mean_ + 1.945 * _sd_
                self._dic_tasks[_id_][5] = _sd_
                self._dic_tasks[_id_][6] = _percent_

                # Calculate mean task cost assuming a beta distribution.
                _a_ = float(_model_.get_value(_row_, 18))
                _m_ = float(_model_.get_value(_row_, 19))
                _b_ = float(_model_.get_value(_row_, 20))

                _mean_ = (_a_ + 4.0 * _m_ + _b_) / 6.0
                _sd_ = (_b_ - _a_) / 6.0

                _model_.set_value(_row_, 21, _mean_)
                _model_.set_value(_row_, 22, _sd_)

                self._dic_tasks[_id_][7] = _mean_ - 1.945 * _sd_
                self._dic_tasks[_id_][8] = _mean_
                self._dic_tasks[_id_][9] = _mean_ + 1.945 * _sd_
                self._dic_tasks[_id_][10] = _sd_

            except ValueError:
                pass

            _row_ = _model_.iter_next(_row_)

# Get list of task information sorted by end date.
        _tasks_ = sorted(self._dic_tasks.values(),
                         key=itemgetter(1))

# Find the earliest start date, the latest end date, and the total number of
# hours for minimum, most likely, and maximum task time.
        _x_ = [min([_a_[0] for _a_ in _tasks_])]
        _y1_ = [sum([_a_[2] for _a_ in _tasks_])]
        _y2_ = [sum([_m_[3] for _m_ in _tasks_])]
        _y3_ = [sum([_b_[4] for _b_ in _tasks_])]
        _y4_ = [sum([_m_[3] for _m_ in _tasks_])]

# Get a sorted list of unique end dates and then find the total number of hours
# that should be completed on each unique end date.
        _uniq_end_ = sorted(list(set([_a_[1] for _a_ in _tasks_])))
        for i in range(len(_uniq_end_)):
            _sum_time_ = [0.0, 0.0, 0.0, 0.0]
            for j in range(len(_tasks_)):
                if _tasks_[j][1] == _uniq_end_[i]:
                    _sum_time_[0] += _tasks_[j][2]
                    _sum_time_[1] += _tasks_[j][3]
                    _sum_time_[2] += _tasks_[j][4]
                    _sum_time_[3] += _tasks_[j][3] * _tasks_[j][6] / 100.0
            _x_.append(_uniq_end_[i])
            _y1_.append(_y1_[i] - _sum_time_[0])
            _y2_.append(_y2_[i] - _sum_time_[1])
            _y3_.append(_y3_[i] - _sum_time_[2])
            _y4_.append(_y4_[i] - _sum_time_[3])

# Plot the expected time and expected time limits.
        load_plot(self.axAxis1, self.pltPlot1, _x_, _y3_, _y2_, _y1_,
                  None, _title_=_(u"Total Validation Effort"),
                  _xlab_=_(u"Date"),
                  _ylab_=_(u"Total Time for All Tasks "),
                  _marker_=['r--', 'b-', 'g--'],
                  _type_=[4, 4, 4, 4])

# Plot the actual burn-down of total hours.
        self._dic_status[_x_[0]] = _y4_[0]
        self._dic_status[date.today().toordinal()] = _y4_[len(_y4_) - 1]

        _x_ = self._dic_status.keys()
        _y4_ = self._dic_status.values()

        _line_ = matplotlib.lines.Line2D(_x_, _y4_, lw=0.0, color='k',
                                         marker='^', markersize=10)
        self.axAxis1.add_line(_line_)

# Plot a vertical line at the scheduled end-date for each task identified as a
# Reliability Assessment.  Add an annotation box showing the minimum required
# and goal values for each milestone.
        for i in range(len(_assess_dates_)):
            self.axAxis1.axvline(x=_assess_dates_[i], ymin=0, color='m',
                                 linewidth=2.5, linestyle=':')

        for i in range(len(_targets_)):
            self.axAxis1.annotate(str(fmt.format(_targets_[i][0])) + "\n" + str(fmt.format(_targets_[i][1])),
                                  xy=(_assess_dates_[i], 0.95 * max(_y3_)),
                                  xycoords='data',
                                  xytext=(-55, 0), textcoords='offset points',
                                  size=12, va="center",
                                  bbox=dict(boxstyle="round",
                                            fc='#E5E5E5',
                                            ec='None',
                                            alpha=0.5),
                                  arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                                  fc='#E5E5E5', ec='None',
                                                  alpha=0.5,
                                                  patchA=None,
                                                  patchB=Ellipse((2, -1), 0.5, 0.5),
                                                  relpos=(0.2, 0.5))
                                  )

# Create the plot legend.
        _text_ = (_(u"Maximum Expected Time"), _(u"Expected Time"),
                  _(u"Minimum Expected Time"), _(u"Actual Remaining Time"))
        create_legend(self.axAxis1, _text_, _fontsize_='medium',
                      _frameon_=True, _location_='lower left', _shadow_=True)

# Calculate project overall mean values and confidence bounds.
        _mean_ = sum([_m_[3] for _m_ in _tasks_])
        _sd_ = sum([_m_[5] for _m_ in _tasks_])

        self.txtProjectTimeLL.set_text(str(fmt.format(_mean_ - 1.945 * _sd_)))
        self.txtProjectTime.set_text(str(fmt.format(_mean_)))
        self.txtProjectTimeUL.set_text(str(fmt.format(_mean_ + 1.945 * _sd_)))

        _mean_ = sum([_m_[8] for _m_ in _tasks_])
        _sd_ = sum([_m_[10] for _m_ in _tasks_])

        self.txtProjectCostLL.set_text(str(fmt.format(_mean_ - 1.945 * _sd_)))
        self.txtProjectCost.set_text(str(fmt.format(_mean_)))
        self.txtProjectCostUL.set_text(str(fmt.format(_mean_ + 1.945 * _sd_)))

        return False
