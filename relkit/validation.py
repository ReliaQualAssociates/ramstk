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
    _gd_tab_labels = [[_(u"Task ID:"), _(u"Task Effectiveness:"),
                       _(u"Task Description:"), _(u"Task Type:"),
                       _(u"Specification:"), _(u"Measurement Unit:"),
                       _(u"Min. Acceptable:"), _(u"Max. Acceptable:"),
                       _(u"Mean Acceptable:"), _(u"Variance:"),
                       _(u"Start Date:"), _(u"End Date:"), _(u"% Complete:")],
                      [], [], []]

    _ta_tab_labels = [_(u"Are the results of this activity reflected when the new content is introduced into the reliability growth test?"),
                      _(u"Historically has this been an area of expertise using established tools and processes?"),
                      _(u"Is this activity conducted with a cross-functional team?"),
                      _(u"How much of the new content is included in this activity?"),
                      _(u"Does this activity directly impact reliability?"),
                      _(u"Does the analysis lead design with system level models defining requirements for subsystems and components?"),
                      _(u"Is a 3-D system level model used in this activity?"),
                      _(u"Are validated models with well understood loading conditions used in this activity?"),
                      _(u"Are there corrective actions implemented on high risk items?"),
                      _(u"Is this activity conducted at the concept stage and result in significant part reduction and simplification of the design?"),
                      _(u"Is analysis of process variability, process capability, and design tolerances reflected in the design?"),
                      _(u"Are the tests statistically designed with understanding of the defined load(s) and required sample size?")]

    n_attributes = 13

    def __init__(self, application):
        """
        Initializes the Validation Object.

        Keyword Arguments:
        application -- the RTK application.
        """

        self._ready = False

        self._app = application

        self.treeview = None
        self.model = None
        self.selected_row = None
        self.validation_id = 0
        self._col_order = []

# Create the Notebook for the VALIDATION object.
        self.notebook = gtk.Notebook()
        if(_conf.TABPOS[2] == 'left'):
            self.notebook.set_tab_pos(gtk.POS_LEFT)
        elif(_conf.TABPOS[2] == 'right'):
            self.notebook.set_tab_pos(gtk.POS_RIGHT)
        elif(_conf.TABPOS[2] == 'top'):
            self.notebook.set_tab_pos(gtk.POS_TOP)
        else:
            self.notebook.set_tab_pos(gtk.POS_BOTTOM)

        # Calculate the width of the gtk.Entry widgets based on the number
        # of decimal places the user has specified.
        entry_width = int((int(_conf.PLACES) + 5) * 8)

# Create the General Data tab for the VALIDATION Object.
        self.txtID = _widg.make_entry(_width_=50)
        self.txtTask = _widg.make_text_view(width=400)
        self.cmbTaskType = _widg.make_combo(simple=False)
        self.txtSpecification = _widg.make_entry()
        self.cmbMeasurementUnit = _widg.make_combo()
        self.txtMinAcceptable = _widg.make_entry(_width_=entry_width)
        self.txtMaxAcceptable = _widg.make_entry(_width_=entry_width)
        self.txtMeanAcceptable = _widg.make_entry(_width_=entry_width)
        self.txtVarAcceptable = _widg.make_entry(_width_=entry_width)
        self.txtStartDate = _widg.make_entry(_width_=100)
        self.txtEndDate = _widg.make_entry(_width_=100)
        self.txtStatus = gtk.SpinButton()
        self.txtEffectiveness = _widg.make_entry(_width_=50)
        if self._general_data_widgets_create():
            self._app.debug_log.error("validation.py: Failed to create General Data widgets.")
        if self._general_data_tab_create():
            self._app.debug_log.error("validation.py: Failed to create General Data tab.")

# Create the Task Assessment tab for the VALIDATION Object.
        self.optQ11 = gtk.RadioButton(label=_(u"Yes"))
        self.optQ12 = gtk.RadioButton(group=self.optQ11, label=_(u"No"))
        self.optQ13 = gtk.RadioButton(group=self.optQ11, label=_(u"Partially"))
        self.optQ21 = gtk.RadioButton(label=_(u"Yes"))
        self.optQ22 = gtk.RadioButton(group=self.optQ21, label=_(u"No"))
        self.optQ23 = gtk.RadioButton(group=self.optQ21, label=_(u"Partially"))
        self.optQ31 = gtk.RadioButton(label=_(u"Yes"))
        self.optQ32 = gtk.RadioButton(group=self.optQ31, label=_(u"No"))
        self.optQ33 = gtk.RadioButton(group=self.optQ31, label=_(u"Partially"))
        self.optQ41 = gtk.RadioButton(label=_(u">75%"))
        self.optQ42 = gtk.RadioButton(group=self.optQ41, label=_(u"25% - 75%"))
        self.optQ43 = gtk.RadioButton(group=self.optQ41, label=_(u"<25%"))
        self.optQ51 = gtk.RadioButton(label=_(u"Yes"))
        self.optQ52 = gtk.RadioButton(group=self.optQ51, label=_(u"No"))
        self.optQ53 = gtk.RadioButton(group=self.optQ51, label=_(u"Partially"))
        self.optQ61 = gtk.RadioButton(label=_(u"Yes"))
        self.optQ62 = gtk.RadioButton(group=self.optQ61, label=_(u"No"))
        self.optQ63 = gtk.RadioButton(group=self.optQ61, label=_(u"Partially"))
        self.optQ64 = gtk.RadioButton(group=self.optQ61, label=_(u"Not Applicable"))
        self.optQ71 = gtk.RadioButton(label=_(u"Yes"))
        self.optQ72 = gtk.RadioButton(group=self.optQ71, label=_(u"No"))
        self.optQ73 = gtk.RadioButton(group=self.optQ71, label=_(u"Partially"))
        self.optQ74 = gtk.RadioButton(group=self.optQ71, label=_(u"Not Applicable"))
        self.optQ81 = gtk.RadioButton(label=_(u"Yes"))
        self.optQ82 = gtk.RadioButton(group=self.optQ81, label=_(u"No"))
        self.optQ83 = gtk.RadioButton(group=self.optQ81, label=_(u"Partially"))
        self.optQ84 = gtk.RadioButton(group=self.optQ81, label=_(u"Not Applicable"))
        self.optQ91 = gtk.RadioButton(label=_(u"Yes"))
        self.optQ92 = gtk.RadioButton(group=self.optQ91, label=_(u"No"))
        self.optQ93 = gtk.RadioButton(group=self.optQ91, label=_(u"Partially"))
        self.optQ101 = gtk.RadioButton(label=_(u"Yes"))
        self.optQ102 = gtk.RadioButton(group=self.optQ101, label=_(u"No"))
        self.optQ103 = gtk.RadioButton(group=self.optQ101, label=_(u"Partially"))
        self.optQ111 = gtk.RadioButton(label=_(u"Yes"))
        self.optQ112 = gtk.RadioButton(group=self.optQ111, label=_(u"No"))
        self.optQ113 = gtk.RadioButton(group=self.optQ111, label=_(u"Partially"))
        self.optQ114 = gtk.RadioButton(group=self.optQ111, label=_(u"Not Applicable"))
        self.optQ121 = gtk.RadioButton(label=_(u"Yes"))
        self.optQ122 = gtk.RadioButton(group=self.optQ121, label=_(u"No"))
        self.optQ123 = gtk.RadioButton(group=self.optQ121, label=_(u"Partially"))
        self.optQ124 = gtk.RadioButton(group=self.optQ121, label=_(u"Not Applicable"))
        if self._task_assessment_widgets_create():
            self._app.debug_log.error("validation.py: Failed to create Task Assessment widgets.")
        if self._task_assessment_tab_create():
            self._app.debug_log.error("validation.py: Failed to create Task Assessment tab.")

# Put it all together.
        self.vbxValidation = gtk.VBox()
        toolbar = self._toolbar_create()

        self.vbxValidation.pack_start(toolbar, expand=False)
        self.vbxValidation.pack_start(self.notebook)

        #self.notebook.connect('switch-page', self._notebook_page_switched)

        self._ready = True

    def _toolbar_create(self):
        """ Method to create the toolbar for the VALIDATAION Object work
            book.
        """

        toolbar = gtk.Toolbar()

        # Add item button.  Depending on the notebook page selected will
        # determine what type of item is added.
        button = gtk.ToolButton(stock_id = gtk.STOCK_ADD)
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        button.set_icon_widget(image)
        button.set_name('Add')
        button.connect('clicked', self.vandv_task_add)
        button.set_tooltip_text(_("Adds a new V&V activity."))
        toolbar.insert(button, 0)

        # Remove item button.  Depending on the notebook page selected will
        # determine what type of item is removed.
        button = gtk.ToolButton(stock_id = gtk.STOCK_REMOVE)
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        button.set_icon_widget(image)
        button.set_name('Remove')
        button.connect('clicked', self._vandv_task_delete)
        button.set_tooltip_text(_("Deletes the selected V&V activity."))
        toolbar.insert(button, 1)

        # Save results button.  Depending on the notebook page selected will
        # determine which results are saved.
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

    def _general_data_widgets_create(self):
        """ Method to create the General Data widgets. """

        self.txtID.set_tooltip_text(_("Displays the unique code for the selected V&V activity."))

        self.cmbTaskType.set_tooltip_text(_("Selects and displays the type of task for the selected V&V activity."))
        query = "SELECT fld_validation_type_desc, \
                        fld_validation_type_code, \
                        fld_validation_type_id \
                 FROM tbl_validation_type"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbTaskType, results, False)
        self.cmbTaskType.connect('changed', self._callback_combo, 3)

        self.txtSpecification.set_tooltip_text(_("Displays the internal or industry specification or procedure governing the selected V&V activity."))
        self.txtSpecification.connect('focus-out-event',
                                      self._callback_entry, 'text', 4)

        self.cmbMeasurementUnit.set_tooltip_text(_("Selects and displays the measurement unit for the selected V&V activity acceptance parameter."))
        query = "SELECT fld_measurement_code \
                 FROM tbl_measurement_units"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbMeasurementUnit, results)
        self.cmbMeasurementUnit.connect('changed',
                                        self._callback_combo, 5)

        self.txtMinAcceptable.set_tooltip_text(_("Displays the minimum acceptable value for the selected V&V activity."))
        self.txtMinAcceptable.connect('focus-out-event',
                                      self._callback_entry, 'float', 6)

        self.txtMaxAcceptable.set_tooltip_text(_("Displays the maximum acceptable value for the selected V&V activity."))
        self.txtMaxAcceptable.connect('focus-out-event',
                                      self._callback_entry, 'float', 8)

        self.txtMeanAcceptable.set_tooltip_text(_("Displays the mean acceptable value for the selected V&V activity."))
        self.txtMeanAcceptable.connect('focus-out-event',
                                       self._callback_entry, 'float', 7)

        self.txtVarAcceptable.set_tooltip_text(_("Displays the acceptable variance for the selected V&V activity."))
        self.txtVarAcceptable.connect('focus-out-event',
                                      self._callback_entry, 'float', 9)

        self.txtStartDate.set_tooltip_text(_("Displays the date the selected V&V activity is scheduled to start."))
        self.txtStartDate.connect('focus-out-event',
                                  self._callback_entry, 'text', 10)

        self.txtEndDate.set_tooltip_text(_("Displays the date the selected V&V activity is scheduled to end."))
        self.txtEndDate.connect('focus-out-event',
                                self._callback_entry, 'text', 11)

        adjustment = gtk.Adjustment(0, 0, 100, 1, 0.1)
        self.txtStatus.set_tooltip_text(_("Displays % complete of the selected V&V activity."))
        self.txtStatus.set_adjustment(adjustment)
        self.txtStatus.connect('focus-out-event',
                               self._callback_entry, 'float', 12)

        self.txtEffectiveness.set_tooltip_text(_("Displays the effectiveness of the selected V&V activity as a percent improvement in system MTBF."))
        self.txtEffectiveness.connect('focus-out-event',
                                      self._callback_entry, 'float', 13)

        return False

    def _general_data_tab_create(self):
        """
        Method to create the General Data gtk.Notebook tab and populate it with
        the appropriate widgets.
        """

        # Place the quadrant 1 (upper left) widgets.
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("General Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        y_pos = 5

        label = _widg.make_label(self._gd_tab_labels[0][0], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtID, 155, y_pos)

        label = _widg.make_label(self._gd_tab_labels[0][1], 150, 25)
        fixed.put(label, 350, y_pos)
        fixed.put(self.txtEffectiveness, 505, y_pos)
        y_pos += 30

        label = _widg.make_label(self._gd_tab_labels[0][2], 150, 25)
        self.txtTask.set_tooltip_text(_("Displays the description of the selected V&V activity."))
        self.txtTask.get_child().get_child().connect('focus-out-event',
                                                     self._callback_entry,
                                                     'text', 2)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtTask, 155, y_pos)
        y_pos += 105

        label = _widg.make_label(self._gd_tab_labels[0][3], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbTaskType, 155, y_pos)
        y_pos += 35

        label = _widg.make_label(self._gd_tab_labels[0][4],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtSpecification, 155, y_pos)
        y_pos += 30

        label = _widg.make_label(self._gd_tab_labels[0][5],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbMeasurementUnit, 155, y_pos)
        y_pos += 35

        label = _widg.make_label(self._gd_tab_labels[0][6],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtMinAcceptable, 155, y_pos)

        label = _widg.make_label(self._gd_tab_labels[0][8],
                                 150, 25)
        fixed.put(label, 300, y_pos)
        fixed.put(self.txtMaxAcceptable, 455, y_pos)
        y_pos += 30

        label = _widg.make_label(self._gd_tab_labels[0][7],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtMeanAcceptable, 155, y_pos)

        label = _widg.make_label(self._gd_tab_labels[0][9],
                                 150, 25)
        fixed.put(label, 300, y_pos)
        fixed.put(self.txtVarAcceptable, 455, y_pos)
        y_pos += 30

        label = _widg.make_label(self._gd_tab_labels[0][10],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtStartDate, 155, y_pos)

        label = _widg.make_label(self._gd_tab_labels[0][11],
                                 150, 25)
        fixed.put(label, 300, y_pos)
        fixed.put(self.txtEndDate, 455, y_pos)
        y_pos += 30

        label = _widg.make_label(self._gd_tab_labels[0][12],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtStatus, 155, y_pos)
        y_pos += 60

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

        try:
            self.txtID.set_text(str(self.model.get_value(self.selected_row, 1)))
            textbuffer = self.txtTask.get_child().get_child().get_buffer()
            textbuffer.set_text(self.model.get_value(self.selected_row, 2))
            self.cmbTaskType.set_active(int(self.model.get_value(self.selected_row, 3)))
            self.txtSpecification.set_text(str(self.model.get_value(self.selected_row, 4)))
            self.cmbMeasurementUnit.set_active(int(self.model.get_value(self.selected_row, 5)))
            self.txtMinAcceptable.set_text(str(self.model.get_value(self.selected_row, 6)))
            self.txtMeanAcceptable.set_text(str(self.model.get_value(self.selected_row, 7)))
            self.txtMaxAcceptable.set_text(str(self.model.get_value(self.selected_row, 8)))
            self.txtVarAcceptable.set_text(str(self.model.get_value(self.selected_row, 9)))
            self.txtStartDate.set_text(str(self.model.get_value(self.selected_row, 10)))
            self.txtEndDate.set_text(str(self.model.get_value(self.selected_row, 11)))
            self.txtStatus.set_value(self.model.get_value(self.selected_row, 12))
            self.txtEffectiveness.set_text(str(self.model.get_value(self.selected_row, 13)))
        except IndexError:                  # There are no V&V tasks.
            pass

        return False

    def _task_assessment_widgets_create(self):
        """ Method to create the Task Assessment widgets. """

        self.optQ11.connect('toggled', self._callback_radio)
        self.optQ12.connect('toggled', self._callback_radio)
        self.optQ13.connect('toggled', self._callback_radio)
        self.optQ21.connect('toggled', self._callback_radio)
        self.optQ22.connect('toggled', self._callback_radio)
        self.optQ23.connect('toggled', self._callback_radio)
        self.optQ31.connect('toggled', self._callback_radio)
        self.optQ32.connect('toggled', self._callback_radio)
        self.optQ33.connect('toggled', self._callback_radio)
        self.optQ41.connect('toggled', self._callback_radio)
        self.optQ42.connect('toggled', self._callback_radio)
        self.optQ43.connect('toggled', self._callback_radio)
        self.optQ51.connect('toggled', self._callback_radio)
        self.optQ52.connect('toggled', self._callback_radio)
        self.optQ53.connect('toggled', self._callback_radio)
        self.optQ61.connect('toggled', self._callback_radio)
        self.optQ62.connect('toggled', self._callback_radio)
        self.optQ63.connect('toggled', self._callback_radio)
        self.optQ64.connect('toggled', self._callback_radio)
        self.optQ71.connect('toggled', self._callback_radio)
        self.optQ72.connect('toggled', self._callback_radio)
        self.optQ73.connect('toggled', self._callback_radio)
        self.optQ74.connect('toggled', self._callback_radio)
        self.optQ81.connect('toggled', self._callback_radio)
        self.optQ82.connect('toggled', self._callback_radio)
        self.optQ83.connect('toggled', self._callback_radio)
        self.optQ84.connect('toggled', self._callback_radio)
        self.optQ91.connect('toggled', self._callback_radio)
        self.optQ92.connect('toggled', self._callback_radio)
        self.optQ93.connect('toggled', self._callback_radio)
        self.optQ101.connect('toggled', self._callback_radio)
        self.optQ102.connect('toggled', self._callback_radio)
        self.optQ103.connect('toggled', self._callback_radio)
        self.optQ111.connect('toggled', self._callback_radio)
        self.optQ112.connect('toggled', self._callback_radio)
        self.optQ113.connect('toggled', self._callback_radio)
        self.optQ114.connect('toggled', self._callback_radio)
        self.optQ121.connect('toggled', self._callback_radio)
        self.optQ122.connect('toggled', self._callback_radio)
        self.optQ123.connect('toggled', self._callback_radio)
        self.optQ124.connect('toggled', self._callback_radio)

        return False

    def _task_assessment_tab_create(self):
        """
        Method to create the Task Assessment gtk.Notebook tab and populate it
        with the appropriate widgets.
        """

        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_(u"Select the best answer to the following questions when assessing the selected V &amp; V task."))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        _lbl_width = 1200
        y_pos = 5
        for i in range(len(self._ta_tab_labels)):
            label = _widg.make_label(self._ta_tab_labels[i], _lbl_width, 25)
            fixed.put(label, 5, y_pos)
            y_pos += 30

        y_pos = 5

        fixed.put(self.optQ11, _lbl_width + 5, y_pos)
        fixed.put(self.optQ12, _lbl_width + 105, y_pos)
        fixed.put(self.optQ13, _lbl_width + 205, y_pos)
        y_pos += 30

        fixed.put(self.optQ21, _lbl_width + 5, y_pos)
        fixed.put(self.optQ22, _lbl_width + 105, y_pos)
        fixed.put(self.optQ23, _lbl_width + 205, y_pos)
        y_pos += 30

        fixed.put(self.optQ31, _lbl_width + 5, y_pos)
        fixed.put(self.optQ32, _lbl_width + 105, y_pos)
        fixed.put(self.optQ33, _lbl_width + 205, y_pos)
        y_pos += 30

        fixed.put(self.optQ41, _lbl_width + 5, y_pos)
        fixed.put(self.optQ42, _lbl_width + 105, y_pos)
        fixed.put(self.optQ43, _lbl_width + 205, y_pos)
        y_pos += 30

        fixed.put(self.optQ51, _lbl_width + 5, y_pos)
        fixed.put(self.optQ52, _lbl_width + 105, y_pos)
        fixed.put(self.optQ53, _lbl_width + 205, y_pos)
        y_pos += 30

        fixed.put(self.optQ61, _lbl_width + 5, y_pos)
        fixed.put(self.optQ62, _lbl_width + 105, y_pos)
        fixed.put(self.optQ63, _lbl_width + 205, y_pos)
        fixed.put(self.optQ64, _lbl_width + 305, y_pos)
        y_pos += 30

        fixed.put(self.optQ71, _lbl_width + 5, y_pos)
        fixed.put(self.optQ72, _lbl_width + 105, y_pos)
        fixed.put(self.optQ73, _lbl_width + 205, y_pos)
        fixed.put(self.optQ74, _lbl_width + 305, y_pos)
        y_pos += 30

        fixed.put(self.optQ81, _lbl_width + 5, y_pos)
        fixed.put(self.optQ82, _lbl_width + 105, y_pos)
        fixed.put(self.optQ83, _lbl_width + 205, y_pos)
        fixed.put(self.optQ84, _lbl_width + 305, y_pos)
        y_pos += 30

        fixed.put(self.optQ91, _lbl_width + 5, y_pos)
        fixed.put(self.optQ92, _lbl_width + 105, y_pos)
        fixed.put(self.optQ93, _lbl_width + 205, y_pos)
        y_pos += 30

        fixed.put(self.optQ101, _lbl_width + 5, y_pos)
        fixed.put(self.optQ102, _lbl_width + 105, y_pos)
        fixed.put(self.optQ103, _lbl_width + 205, y_pos)
        y_pos += 30

        fixed.put(self.optQ111, _lbl_width + 5, y_pos)
        fixed.put(self.optQ112, _lbl_width + 105, y_pos)
        fixed.put(self.optQ113, _lbl_width + 205, y_pos)
        fixed.put(self.optQ114, _lbl_width + 305, y_pos)
        y_pos += 30

        fixed.put(self.optQ121, _lbl_width + 5, y_pos)
        fixed.put(self.optQ122, _lbl_width + 105, y_pos)
        fixed.put(self.optQ123, _lbl_width + 205, y_pos)
        fixed.put(self.optQ124, _lbl_width + 305, y_pos)
        y_pos += 30

        fixed.show_all()

# Clark's DMS password = p2Hg8q3B

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
            _title_ = _(u"RTK Work Bench: Analyzing %s") % \
                      self.model.get_value(self.selected_row, 2)
        except TypeError:
            _title_ = _(u"RTK Work Bench")
        self._app.winWorkBook.set_title(_title_)

        return False

    def create_tree(self):
        """
        Creates the Validation TreeView and connects it to callback functions
        to handle editting.  Background and foreground colors can be set using
        the user-defined values in the RTK configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()
        bg_color = _conf.RELIAFREE_COLORS[8]
        fg_color = _conf.RELIAFREE_COLORS[9]
        (self.treeview, self._col_order) = _widg.make_treeview('Validation', 4,
                                                               self._app,
                                                               None,
                                                               bg_color,
                                                               fg_color)
        self.treeview.set_enable_tree_lines(True)

        scrollwindow.add(self.treeview)
        self.model = self.treeview.get_model()

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)

        return(scrollwindow)

    def load_tree(self):
        """
        Loads the Validation treeview model with system information.  This
        information can be stored either in a MySQL or SQLite3 database.
        """

        if(_conf.RELIAFREE_MODULES[0] == 1):
            values = (self._app.REVISION.revision_id,)
        else:
            values = (0,)

        # Select everything from the validation table.
        if(_conf.BACKEND == 'mysql'):
            query = "SELECT * FROM tbl_validation \
                     WHERE fld_revision_id=%d \
                     ORDER BY fld_validation_id"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT * FROM tbl_validation \
                     WHERE fld_revision_id=? \
                     ORDER BY fld_validation_id"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            return True

        n_records = len(results)
        self.model.clear()
        for i in range(n_records):
            self.model.append(None, results[i])

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

        model[path][position] = new_text

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
            if(_conf.RELIAFREE_MODULES[0] == 1):
                _revision = self._app.REVISION.revision_id
            else:
                _revision = 0

        n_tasks = _util.add_items(_("V &amp; V Activity"))

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

        selection = self.treeview.get_selection()
        (model, row) = selection.get_selected()

        values = (self._app.REVISION.revision_id, \
                  model.get_value(row, 1))

        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_validation \
                     WHERE fld_revision_id=%d \
                     AND fld_validation_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_validation \
                     WHERE fld_revision_id=? \
                     AND fld_validation_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)
        if not results:
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

        self.model.foreach(self._save_line_item)

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

        values = (model.get_value(row, self._col_order[2]), \
                  model.get_value(row, self._col_order[3]), \
                  model.get_value(row, self._col_order[4]), \
                  model.get_value(row, self._col_order[5]), \
                  model.get_value(row, self._col_order[6]), \
                  model.get_value(row, self._col_order[7]), \
                  model.get_value(row, self._col_order[8]), \
                  model.get_value(row, self._col_order[9]), \
                  model.get_value(row, self._col_order[10]), \
                  model.get_value(row, self._col_order[11]), \
                  model.get_value(row, self._col_order[12]), \
                  model.get_value(row, self._col_order[13]), \
                  self._app.REVISION.revision_id, \
                  model.get_value(row, self._col_order[1]))

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_validation \
                     SET fld_task_desc='%s', fld_task_type=%d, \
                         fld_task_specification='%s', fld_measurement_unit=%d, \
                         fld_min_acceptable=%f, fld_mean_acceptable=%f, \
                         fld_max_acceptable=%f, fld_variance_acceptable=%f, \
                         fld_start_date='%s', fld_end_date='%s', fld_status=%f, \
                         fld_effectiveness=%f \
                     WHERE fld_revision_id=%d \
                     AND fld_validation_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_validation \
                     SET fld_task_desc=?, fld_task_type=?, \
                         fld_task_specification=?, fld_measurement_unit=?, \
                         fld_min_acceptable=?, fld_mean_acceptable=?, \
                         fld_max_acceptable=?, fld_variance_acceptable=?, \
                         fld_start_date=?, fld_end_date=?, fld_status=?, \
                         fld_effectiveness=? \
                     WHERE fld_revision_id=? \
                     AND fld_validation_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("validation.py: Failed to save V&V task.")
            return True

        return False

    def _callback_combo(self, combo, _index_):
        """
        Callback function to retrieve and save combobox changes.

        Keyword Arguments:
        combo  -- the combobox that called the function.
        index_ -- the position in the Validation Object _attribute list
                  associated with the data from the calling combobox.
        """

        # Update the Validation Tree.
        try:
            self.model.set_value(self.selected_row, _index_,
                                 int(combo.get_active()))
        except TypeError:
            print _index_


        return False

    def _callback_entry(self, entry, event, convert, _index_):
        """
        Callback function to retrieve and save entry changes.

        Keyword Arguments:
        entry   -- the entry that called the function.
        event   -- the gtk.gdk.Event that called this function.
        convert -- the data type to convert the entry contents to.
        index_  -- the position in the Validation Object _attribute list
                   associated with the data from the calling entry.
        """

        if(convert == 'text'):
            if(_index_ == 2):
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
        try:
            self.model.set_value(self.selected_row, _index_, _text_)
        except TypeError:
            print _index_

        return False

    def _callback_radio(self, radio):
        """
        Callback function to retrieve and save radio button changes.

        Keyword Arguments:
        radio -- the gtk.RadioButton that called the function.
        """

        print radio

        return False
