#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to
verification and validation tasks of the Program.
"""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

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
import utilities as _util
import widgets as _widg

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

import gettext
_ = gettext.gettext


class Validation:
    """
    The Validation class is used to represent the verification and validation
    tasks for the system being analyzed.
    """

    # TODO: Write code to update notebook widgets when editing the Validation treeview.
    # TODO: Add tooltips to all widgets.
    _ta_tab_labels = [_(u"Does this activity provide quantitative stress information as an output?"),
                      _(u"Does this activity provide quantitative strength information as an output?"),
                      _(u"Does this activity provide operating environment information as an output?"),
                      _(u"Hardware item configuration/architecture"),
                      _(u"Hardware item failure modes"),
                      _(u"Hardware item failure mechanisms"),
                      _(u"Hardware item failure causes"),
                      _(u"Hardware item failure times"),
                      _(u"Hardware item Part quality"),
                      _(u"Hardware item aging/degradation information"),
                      _(u"Hardware item design requirements and/or goals"),
                      _(u"")]

    notebook = gtk.Notebook()
    vbxValidation = gtk.VBox()

# Create the General Data tab widgets.
    btnEndDate = _widg.make_button(_height_=25, _width_=25,
                                   _label_="...", _image_=None)
    btnStartDate = _widg.make_button(_height_=25, _width_=25,
                                     _label_="...", _image_=None)

    cmbTaskType = _widg.make_combo()
    cmbMeasurementUnit = _widg.make_combo()

    spnStatus = gtk.SpinButton()

    txtEndDate = _widg.make_entry(_width_=100)
    txtID = _widg.make_entry(_width_=50, editable=False)
    txtMaxAcceptable = _widg.make_entry(_width_=100)
    txtMeanAcceptable = _widg.make_entry(_width_=100)
    txtMinAcceptable = _widg.make_entry(_width_=100)
    txtVarAcceptable = _widg.make_entry(_width_=100)
    txtStartDate = _widg.make_entry(_width_=100)
    txtSpecification = _widg.make_entry()
    txtTask = _widg.make_text_view(width=400)

# Create the Assessment tab widgets.
    scwAssessment = gtk.ScrolledWindow()

    # Create the widgets for assessing the quality of a reliability model.
    fxdModel = gtk.Fixed()

    chkModelQ1 = _widg.make_check_button(_(u"All functional elements are included in the diagram/model."))
    chkModelQ2 = _widg.make_check_button(_(u"All modes of operation are considered in the model."))
    chkModelQ3 = _widg.make_check_button(_(u"The model results show the design achieves the reliability target."))

    # Create the widgets for assessing the quality of a reliability prediction.
    fxdPrediction = gtk.Fixed()

    chkPredictionQ1 = _widg.make_check_button(_(u"The sum of the part failure rates is equal to the module or assembly failure rate."))
    chkPredictionQ2 = _widg.make_check_button(_(u"Environmental conditions and part qualities are representative of the actual design."))
    chkPredictionQ3 = _widg.make_check_button(_(u"Assembly and part temperatures are identified and they realistically represent the thermal approach used."))
    chkPredictionQ4 = _widg.make_check_button(_(u"All system, assembly, subassembly, and part reliability drivers are identified."))
    chkPredictionQ5 = _widg.make_check_button(_(u"All part failure rates are from acceptable sources."))

    # Create the widgets for assessing the quality of a FMEA.
    fxdFMEA = gtk.Fixed()

    chkFMEAQ1 = _widg.make_check_button(_(u"The system definition/description is compatible with the system requirements."))
    chkFMEAQ2 = _widg.make_check_button(_(u"Ground rules and assumptions are clearly stated."))
    chkFMEAQ3 = _widg.make_check_button(_(u"Block diagrams are provided showing functional dependencies at all hardware levels."))
    chkFMEAQ4 = _widg.make_check_button(_(u"The failure effects analysis starts at the lowest hardware level and systematically works to higher levels."))
    chkFMEAQ5 = _widg.make_check_button(_(u"Failure mode data sources are fully described."))
    chkFMEAQ6 = _widg.make_check_button(_(u"Detailed FMEA worksheets clearly track from lower to higher hardware levels."))
    chkFMEAQ7 = _widg.make_check_button(_(u"The FMEA worksheets clearly correspond to the block diagrams."))
    chkFMEAQ8 = _widg.make_check_button(_(u"The FMEA worksheets provide an adequate scope of analysis."))
    chkFMEAQ9 = _widg.make_check_button(_(u"Failure severity classifications are provided."))
    chkFMEAQ10 = _widg.make_check_button(_(u"Specific failure definitions are established."))
    chkFMEAQ11 = _widg.make_check_button(_(u"FMEA results are timely."))
    chkFMEAQ12 = _widg.make_check_button(_(u"FMEA results are clearly summarized and comprehensive recommendations are provided."))
    chkFMEAQ13 = _widg.make_check_button(_(u"FMEA results are being communicated to enhance other program decisions."))

    def __init__(self, application):
        """
        Initializes the Validation Object.

        Keyword Arguments:
        application -- the RTK application.
        """

        self._ready = False

        self._app = application

# Define local dictionary variables.
        self._dic_types = {}                # Dictionary of task types.

# Define local list variables.
        self._lst_col_order = []
        self._lst_handler_id = []

# Define global integer variables.
        self.validation_id = 0

# Create the Notebook for the VALIDATION object.
        if(_conf.TABPOS[2] == 'left'):
            self.notebook.set_tab_pos(gtk.POS_LEFT)
        elif(_conf.TABPOS[2] == 'right'):
            self.notebook.set_tab_pos(gtk.POS_RIGHT)
        elif(_conf.TABPOS[2] == 'top'):
            self.notebook.set_tab_pos(gtk.POS_TOP)
        else:
            self.notebook.set_tab_pos(gtk.POS_BOTTOM)

# Create the General Data tab.
        if self._general_data_tab_create():
            self._app.debug_log.error("validation.py: Failed to create General Data tab.")

# Create the Task Assessment tab.
        #if self._task_assessment_tab_create():
        #    self._app.debug_log.error("validation.py: Failed to create Task Assessment tab.")

# Put it all together.
        toolbar = self._toolbar_create()

        self.vbxValidation.pack_start(toolbar, expand=False)
        self.vbxValidation.pack_start(self.notebook)

        #self.notebook.connect('switch-page', self._notebook_page_switched)

        self._ready = True

    def _toolbar_create(self):
        """
        Method to create the toolbar for the VALIDATAION Object Work Book.
        """

        toolbar = gtk.Toolbar()

# Add item button.  Depending on the notebook page selected will determine what
# type of item is added.
        button = gtk.ToolButton(stock_id = gtk.STOCK_ADD)
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        button.set_icon_widget(image)
        button.set_name('Add')
        button.connect('clicked', self.vandv_task_add)
        button.set_tooltip_text(_("Adds a new V&V activity."))
        toolbar.insert(button, 0)

# Remove item button.  Depending on the notebook page selected will determine
# what type of item is removed.
        button = gtk.ToolButton(stock_id = gtk.STOCK_REMOVE)
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        button.set_icon_widget(image)
        button.set_name('Remove')
        button.connect('clicked', self._vandv_task_delete)
        button.set_tooltip_text(_("Deletes the selected V&V activity."))
        toolbar.insert(button, 1)

# Save results button.  Depending on the notebook page selected will determine
# which results are saved.
        button = gtk.ToolButton(stock_id = gtk.STOCK_SAVE)
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        button.set_icon_widget(image)
        button.set_name('Save')
        button.connect('clicked', self.validation_save)
        button.set_tooltip_text(_("Saves the selected V&V activity."))
        toolbar.insert(button, 2)

        toolbar.show()

        return(toolbar)

    def _general_data_tab_create(self):
        """
        Method to create the General Data gtk.Notebook tab and populate it with
        the appropriate widgets.
        """

        _labels_ = [_(u"Task ID:"), _(u"Task Description:"), _(u"Task Type:"),
                    _(u"Specification:"), _(u"Measurement Unit:"),
                    _(u"Minimum Acceptable:"), _(u"Maximum Acceptable:"),
                    _(u"Mean Acceptable:"), _(u"Variance:"),
                    _(u"Start Date:"), _(u"End Date:"), _(u"% Complete:")]

        def _general_data_widgets_create(self):
            """
            Function to create the General Data widgets.
            """

            self.btnEndDate.set_tooltip_text(_(u"Launches the calendar to select the date the task was completed."))
            self.btnEndDate.connect('released', _util.date_select,
                                    self.txtEndDate)

            self.btnStartDate.set_tooltip_text(_(u"Launches the calendar to select the date the task was started."))
            self.btnStartDate.connect('released', _util.date_select,
                                      self.txtStartDate)

            self.txtID.set_tooltip_text(_(u"Displays the unique code for the selected V&V activity."))

            self.txtTask.set_tooltip_text(_(u"Displays the description of the selected V&V activity."))
            _buffer_ = self.txtTask.get_child().get_child()
            _id_ = _buffer_.connect('focus-out-event', self._callback_entry,
                                    'text', 2)
            self._lst_handler_id.append(_id_)

            self.cmbTaskType.set_tooltip_text(_(u"Selects and displays the type of task for the selected V&V activity."))
            query = "SELECT fld_validation_type_desc \
                     FROM tbl_validation_type"
            results = self._app.COMDB.execute_query(query,
                                                    None,
                                                    self._app.ComCnx)
            _widg.load_combo(self.cmbTaskType, results)
            _id_ = self.cmbTaskType.connect('changed', self._callback_combo, 3)
            self._lst_handler_id.append(_id_)

            self.txtSpecification.set_tooltip_text(_(u"Displays the internal or industry specification or procedure governing the selected V&V activity."))
            _id_ = self.txtSpecification.connect('focus-out-event',
                                                 self._callback_entry,
                                                 'text', 4)
            self._lst_handler_id.append(_id_)

            self.cmbMeasurementUnit.set_tooltip_text(_(u"Selects and displays the measurement unit for the selected V&V activity acceptance parameter."))
            query = "SELECT fld_measurement_code \
                     FROM tbl_measurement_units"
            results = self._app.COMDB.execute_query(query,
                                                    None,
                                                    self._app.ComCnx)
            _widg.load_combo(self.cmbMeasurementUnit, results)
            _id_= self.cmbMeasurementUnit.connect('changed',
                                                  self._callback_combo, 5)
            self._lst_handler_id.append(_id_)

            self.txtMinAcceptable.set_tooltip_text(_(u"Displays the minimum acceptable value for the selected V&V activity."))
            _id_ = self.txtMinAcceptable.connect('focus-out-event',
                                                 self._callback_entry,
                                                 'float', 6)
            self._lst_handler_id.append(_id_)

            self.txtMeanAcceptable.set_tooltip_text(_(u"Displays the mean acceptable value for the selected V&V activity."))
            _id_ = self.txtMeanAcceptable.connect('focus-out-event',
                                                  self._callback_entry,
                                                  'float', 7)
            self._lst_handler_id.append(_id_)

            self.txtMaxAcceptable.set_tooltip_text(_(u"Displays the maximum acceptable value for the selected V&V activity."))
            _id_ = self.txtMaxAcceptable.connect('focus-out-event',
                                                 self._callback_entry,
                                                 'float', 8)
            self._lst_handler_id.append(_id_)

            self.txtVarAcceptable.set_tooltip_text(_(u"Displays the acceptable variance for the selected V&V activity."))
            _id_ = self.txtVarAcceptable.connect('focus-out-event',
                                                 self._callback_entry,
                                                 'float', 9)
            self._lst_handler_id.append(_id_)

            self.txtStartDate.set_tooltip_text(_(u"Displays the date the selected V&V activity is scheduled to start."))
            _id_ = self.txtStartDate.connect('focus-out-event',
                                             self._callback_entry, 'text', 10)
            self._lst_handler_id.append(_id_)

            self.txtEndDate.set_tooltip_text(_(u"Displays the date the selected V&V activity is scheduled to end."))
            _id_ = self.txtEndDate.connect('focus-out-event',
                                           self._callback_entry, 'text', 11)
            self._lst_handler_id.append(_id_)

            # Set the spin button to be a 0-100 in steps of 0.1 spinner.  Only
            # update if value is numeric and within range.
            adjustment = gtk.Adjustment(0, 0, 100, 1, 0.1)
            self.spnStatus.set_adjustment(adjustment)
            self.spnStatus.set_update_policy(gtk.UPDATE_IF_VALID)
            self.spnStatus.set_numeric(True)
            self.spnStatus.set_snap_to_ticks(True)
            self.spnStatus.set_tooltip_text(_(u"Displays % complete of the selected V&V activity."))
            _id_ = self.spnStatus.connect('value-changed',
                                          self._callback_spin, 'float', 12)
            self._lst_handler_id.append(_id_)

            return False

        if _general_data_widgets_create(self):
            self._app.debug_log.error("validation.py: Failed to create General Data widgets.")

# Create the tab.
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_(u"General Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

# Create the labels.  Place labels 2 - 11 first and then 0 and 1 to account for
# The larger gtk.TextView() used for the task description.
        _max1_ = 0
        _max2_ = 0
        (_max1_, _y_pos_) = _widg.make_labels(_labels_[2:], fixed, 5, 140)

        label = _widg.make_label(_labels_[0], -1, 25)
        fixed.put(label, 5, 5)
        _max2_ = label.size_request()[0]
        _x_pos_ = max(_max1_, _max2_) + 20

        label = _widg.make_label(_labels_[1], 150, 25)
        fixed.put(label, 5, 35)
        _max2_ = label.size_request()[0]
        _x_pos_ = max(_x_pos_, _max2_) + 20

        fixed.put(self.txtID, _x_pos_, 5)
        fixed.put(self.txtTask, _x_pos_, 35)

        fixed.put(self.cmbTaskType, _x_pos_, _y_pos_[0])
        fixed.put(self.txtSpecification, _x_pos_, _y_pos_[1])
        fixed.put(self.cmbMeasurementUnit, _x_pos_, _y_pos_[2]-3)
        fixed.put(self.txtMinAcceptable, _x_pos_, _y_pos_[3])
        fixed.put(self.txtMeanAcceptable, _x_pos_, _y_pos_[4])
        fixed.put(self.txtMaxAcceptable, _x_pos_, _y_pos_[5])
        fixed.put(self.txtVarAcceptable, _x_pos_, _y_pos_[6])
        fixed.put(self.txtStartDate, _x_pos_, _y_pos_[7])
        fixed.put(self.btnStartDate, _x_pos_+105, _y_pos_[7])
        fixed.put(self.txtEndDate, _x_pos_, _y_pos_[8])
        fixed.put(self.btnEndDate, _x_pos_+105, _y_pos_[8])
        fixed.put(self.spnStatus, _x_pos_, _y_pos_[9])

        fixed.show_all()

# Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _(u"General\nData") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Displays general information about the selected V&V task."))
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _general_data_tab_load(self):
        """
        Loads the widgets with general information about the VALIDATION Object.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        try:
            _index_ = self._dic_types[_model_.get_value(_row_, 3)]
        except KeyError:
            _index_ = 0

        try:
            self.txtID.set_text(str(_model_.get_value(_row_, 1)))
            textbuffer = self.txtTask.get_child().get_child().get_buffer()
            textbuffer.set_text(_model_.get_value(_row_, 2))
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
        except IndexError:                  # There are no V&V tasks.
            pass

        return False

    def _task_assessment_tab_create(self):
        """
        Method to create the Task Assessment gtk.Notebook tab and populate it
        with the appropriate widgets.
        """

        def _task_assessment_widgets_create(self):
            """
            Function to create the Task Assessment widgets.
            """

            self.scwAssessment.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

            self.chkModelQ1.set_tooltip_text(_(u"Reliability models/diagrams should agree with hardware design drawings/diagrams."))
            self.chkModelQ2.set_tooltip_text(_(u"Duty cycles, alternate paths, degraded conditions, and redundant units should be defined and modeled."))
            self.chkModelQ3.set_tooltip_text(_(u"Unit failure rates and redundancy equations should be used."))

            self.chkPredictionQ1.set_tooltip_text(_(u"Reliability assessments may neglect to include all parts, producing optimistic results."))
            self.chkPredictionQ2.set_tooltip_text(_(u"Optimistic quality levels and favorable environmental conditions are often assumed, causing optimistic results."))
            self.chkPredictionQ3.set_tooltip_text(_(u"Temperature is a significant driver of part failure rates, both electronic and mechanical."))
            self.chkPredictionQ4.set_tooltip_text(_(u"Identification is needed so reliability improvement can be considered."))
            self.chkPredictionQ5.set_tooltip_text(_(u"In the absence of historical operating data (preferred), specific part test data or handbook information are typically acceptable."))

            return False

        if _task_assessment_widgets_create(self):
            self._app.debug_log.error("validation.py: Failed to create Task Assessment widgets.")

# Lay out the Reliability Model questions.
        self.fxdModel.put(self.chkModelQ1, 5, 5)
        self.fxdModel.put(self.chkModelQ2, 5, 35)
        self.fxdModel.put(self.chkModelQ3, 5, 70)

        self.scwAssessment.add_with_viewport(self.fxdModel)

        frame = _widg.make_frame(_label_=_(u"Answer the following questions relative to the selected V &amp; V task."))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(self.scwAssessment)

# Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _(u"Task\nAssessment") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Assesses the effectiveness of the selected V & V task."))
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def load_notebook(self):
        """
        Method to load the VALIDATION Object gtk.Notebook.
        """

        if self.selected_row is not None:
            self._general_data_tab_load()

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxValidation)
        self._app.winWorkBook.show_all()

        try:
            _title_ = _(u"RTK Work Book: Analyzing %s") % \
                      self.model.get_value(self.selected_row, 2)
        except TypeError:
            _title_ = _(u"RTK Work Book")
        self._app.winWorkBook.set_title(_title_)

        return False

    def create_tree(self):
        """
        Creates the Validation TreeView and connects it to callback functions
        to handle editting.  Background and foreground colors can be set using
        the user-defined values in the RTK configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()
        bg_color = _conf.RTK_COLORS[8]
        fg_color = _conf.RTK_COLORS[9]
        (self.treeview, self._lst_col_order) = _widg.make_treeview('Validation', 4,
                                                               self._app,
                                                               None,
                                                               bg_color,
                                                               fg_color)
        self.treeview.set_enable_tree_lines(True)

# Connect the cells to the callback function.
        for i in range(2, 13):
            _cell_ = self.treeview.get_column(self._lst_col_order[i]).get_cell_renderers()
            _cell_[0].connect('edited', self._vandv_tree_edit, i,
                              self.treeview.get_model())

        scrollwindow.add(self.treeview)
        self.model = self.treeview.get_model()

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)

        return(scrollwindow)

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

        if(_results_ == '' or not _results_ or _results_ is None):
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

# Select everything from the validation table.
        _query_ = "SELECT * FROM tbl_validation \
                   WHERE fld_revision_id=%d \
                   ORDER BY fld_validation_id" % self._app.REVISION.revision_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if(_results_ == '' or not _results_ or _results_ is None):
            return True

# Add all the tasks to the Tree Book.
        _n_tasks_ = len(_results_)
        self.model.clear()
        for i in range(_n_tasks_):
            self.model.append(None, _results_[i])

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)

        root = self.model.get_iter_root()
        if root is not None:
            path = self.model.get_path(root)
            col = self.treeview.get_column(0)
            self.treeview.row_activated(path, col)

        return False

    def _update_tree(self, columns, values):
        """
        Updates the values in the VALIDATION Object gtk.Treeview.

        Keyword Arguments:
        columns -- a list of integers representing the column numbers to
                   update.
        values  -- a list of new values for the Validation Object
                   TreeView.
        """

        for i in columns:
            self.model.set_value(self.selected_row, i, values[i])

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the VALIDATION Object
        gtk.Treeview.

        Keyword Arguments:
        treeview -- the VALIDATION Object treeview.
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

        if(event.button == 1):
            self._treeview_row_changed(treeview, None, 0)
        elif(event.button == 3):
            print "Pop-up a menu!"

        return False

    def _treeview_row_changed(self, treeview, path, column):
        """
        Callback function to handle events for the VALIDATION Object
        gtk.Treeview.  It is called whenever the VALIDATION Object gtk.Treeview
        is clicked or a row is activated.  It will save the previously selected
        row in the VALIDATION Object treeview.

        Keyword Arguments:
        treeview -- the Validation Object gtk.TreeView.
        path     -- the actived row gtk.TreeView path.
        column   -- the actived gtk.TreeViewColumn.
        """

        selection = self.treeview.get_selection()
        (self.model, self.selected_row) = selection.get_selected()

        if self.selected_row is not None:
            self.load_notebook()

            return False
        else:
            return True

    def _vandv_tree_edit(self, cell, path, new_text, position, model):
        """
        Called whenever a VALIDATION Object gtk.Treeview CellRenderer is
        edited.

        Keyword Arguments:
        cell     -- the CellRenderer that was edited.
        path     -- the TreeView path of the CellRenderer that was edited.
        new_text -- the new text in the edited CellRenderer.
        position -- the column position of the edited CellRenderer.
        model    -- the TreeModel the CellRenderer belongs to.
        """

# Update the gtk.TreeModel() with the new value.
        type = gobject.type_name(model.get_column_type(position))

        if(type == 'gchararray'):
            model[path][position] = str(new_text)
        elif(type == 'gint'):
            model[path][position] = int(new_text)
        elif(type == 'gfloat'):
            model[path][position] = float(new_text)

# Not update the associated gtk.Widget() in the Work Book with the new value.
# We block and unblock the signal handlers for the widgets so a race condition
# does not ensue.
        if(self._lst_col_order[position] == 2):
            _buffer_ = self.txtTask.get_child().get_child().get_buffer()
            _buffer_.handler_block(self._lst_handler_id[0])
            _buffer_.set_text(str(new_text))
            _buffer_.handler_unblock(self._lst_handler_id[0])
        elif(self._lst_col_order[position] == 3):
            try:
                _index_ = self._dic_types[new_text]
            except KeyError:
                _index_ = 0
            self.cmbTaskType.handler_block(self._lst_handler_id[1])
            self.cmbTaskType.set_active(_index_)
            self.cmbTaskType.handler_unblock(self._lst_handler_id[1])
        elif(self._lst_col_order[position] == 4):
            self.txtSpecification.handler_block(self._lst_handler_id[2])
            self.txtSpecification.set_text(str(new_text))
            self.txtSpecification.handler_unblock(self._lst_handler_id[2])
        elif(self._lst_col_order[position] == 5):
            self.cmbMeasurementUnit.handler_block(self._lst_handler_id[3])
            self.cmbMeasurementUnit.set_active(int(new_text))
            self.cmbMeasurementUnit.handler_unblock(self._lst_handler_id[3])
        elif(self._lst_col_order[position] == 6):
            self.txtMinAcceptable.handler_block(self._lst_handler_id[4])
            self.txtMinAcceptable.set_text(str(new_text))
            self.txtMinAcceptable.handler_unblock(self._lst_handler_id[4])
        elif(self._lst_col_order[position] == 7):
            self.txtMaxAcceptable.handler_block(self._lst_handler_id[5])
            self.txtMaxAcceptable.set_text(str(new_text))
            self.txtMaxAcceptable.handler_unblock(self._lst_handler_id[5])
        elif(self._lst_col_order[position] == 8):
            self.txtMeanAcceptable.handler_block(self._lst_handler_id[6])
            self.txtMeanAcceptable.set_text(str(new_text))
            self.txtMeanAcceptable.handler_unblock(self._lst_handler_id[6])
        elif(self._lst_col_order[position] == 9):
            self.txtVarAcceptable.handler_block(self._lst_handler_id[7])
            self.txtVarAcceptable.set_text(str(new_text))
            self.txtVarAcceptable.handler_unblock(self._lst_handler_id[7])
        elif(self._lst_col_order[position] == 10):
            self.txtStartDate.handler_block(self._lst_handler_id[8])
            self.txtStartDate.set_text(str(new_text))
            self.txtStartDate.handler_unblock(self._lst_handler_id[8])
        elif(self._lst_col_order[position] == 11):
            self.txtEndDate.handler_block(self._lst_handler_id[9])
            self.txtEndDate.set_text(str(new_text))
            self.txtEndDate.handler_unblock(self._lst_handler_id[9])
        elif(self._lst_col_order[position] == 12):
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

# Find the selected revision.
        if self.selected_row is not None:
            _revision = self.model.get_value(self.selected_row, 0)
            _assembly = self.model.get_value(self.selected_row, 2)
        else:
            if(_conf.RTK_MODULES[0] == 1):
                _revision = self._app.REVISION.revision_id
            else:
                _revision = 0

        n_tasks = _util.add_items(title=_(u"RTK - Add V &amp; V Activity"),
                                  prompt=_(u"How many V &amp; V activities to add?"))

        for i in range(n_tasks):

            task_name = "New V&V Activity " + str(i)
            values = (_revision, task_name)

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_validation \
                         (fld_revision_id, fld_task_desc) \
                         VALUES (%d, '%s')"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_validation \
                         (fld_revision_id, fld_task_desc) \
                         VALUES (?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.user_log.error("validation.py: Failed to add V&V task.")
                return True

        #self._app.REVISION.load_tree()
        self.load_tree()

        return False

    def _vandv_task_delete(self, menuitem):
        """
        Deletes the currently selected V&V activity from the RTK Program's
        MySQL or SQLite3 database.

        Keyword Arguments:
        menuitem -- the gtk.MenuItem that called this function.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        _values_ = (self._app.REVISION.revision_id, \
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

        self.load_tree()

        return False

    def validation_save(self, widget=None):
        """
        Saves the VALIDATAION Object treeview information to the RTK
        Program's MySQL or SQLite3 database.

        Keyword Arguments:
        widget -- the widget that called this function.
        """

        _model_ = self.treeview.get_model()
        _model_.foreach(self._save_line_item)

        return False

    def _save_line_item(self, model, path_, row):
        """
        Saves each row in the VALIDATION Object treeview model to the RTK
        Program's MySQL or SQLite3 database.

        Keyword Arguments:
        model -- the Validation Object treemodel.
        path_ -- the path of the active row in the Validation Object
                 treemodel.
        row   -- the selected row in the Validation Object treeview.
        """

        _values = (model.get_value(row, self._lst_col_order[2]), \
                   model.get_value(row, self._lst_col_order[3]), \
                   model.get_value(row, self._lst_col_order[4]), \
                   model.get_value(row, self._lst_col_order[5]), \
                   model.get_value(row, self._lst_col_order[6]), \
                   model.get_value(row, self._lst_col_order[7]), \
                   model.get_value(row, self._lst_col_order[8]), \
                   model.get_value(row, self._lst_col_order[9]), \
                   model.get_value(row, self._lst_col_order[10]), \
                   model.get_value(row, self._lst_col_order[11]), \
                   model.get_value(row, self._lst_col_order[12]), \
                   self._app.REVISION.revision_id, \
                   model.get_value(row, self._lst_col_order[1]))

        query = "UPDATE tbl_validation \
                 SET fld_task_desc='%s', fld_task_type='%s', \
                     fld_task_specification='%s', fld_measurement_unit=%d, \
                     fld_min_acceptable=%f, fld_mean_acceptable=%f, \
                     fld_max_acceptable=%f, fld_variance_acceptable=%f, \
                     fld_start_date='%s', fld_end_date='%s', fld_status=%f \
                 WHERE fld_revision_id=%d \
                 AND fld_validation_id=%d" % _values
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("validation.py: Failed to save V&V task.")
            return True

        return False

    def _callback_combo(self, combo, index):
        """
        Callback function to retrieve and save combobox changes.

        Keyword Arguments:
        combo -- the combobox that called the function.
        index -- the position in the Validation Object _attribute list
                 associated with the data from the calling combobox.
        """

# Update the Validation Tree.
        if(index == 3):                     # Task type
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
        event   -- the gtk.gdk.Event that called this function.
        convert -- the data type to convert the entry contents to.
        index   -- the position in the Validation Object _attribute list
                   associated with the data from the calling entry.
        """

        if(convert == 'text'):
            if(index == 2):
                textbuffer = self.txtTask.get_child().get_child().get_buffer()
                _text_ = textbuffer.get_text(*textbuffer.get_bounds())
            else:
                _text_ = entry.get_text()
        elif(convert == 'int'):
            _text_ = int(entry.get_text())

        elif(convert == 'float'):
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

        return False

    def _callback_spin(self, spinbutton, convert, index):
        """
        Callback function to retrieve and save spinbutton changes.

        Keyword Arguments:
        spinbutton -- the gtk.SpinButton() that called this function.
        convert    -- the data type to convert the entry contents to.
        index      -- the position in the Validation Object _attribute list
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

    def _callback_radio(self, radio):
        """
        Callback function to retrieve and save radio button changes.

        Keyword Arguments:
        radio -- the gtk.RadioButton that called the function.
        """

        print radio

        return False
