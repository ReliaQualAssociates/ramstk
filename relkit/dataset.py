#!/usr/bin/env python
""" This is the Class that is used to represent and hold information related
    to Program survival data sets. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       dataset.py is part of The RelKit Project
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

# Import other RelKit modules.
import calculations as _calc
import configuration as _conf
import imports as _impt
import utilities as _util
import widgets as _widg

#from _assistants_.dataset import *

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


class Dataset:
    """
    The Dataset class is used to represent the survival data sets associated
    with the system being analyzed.
    """

    _ai_tab_labels = [_("Assembly:"), _("Description:"), _("Data Source:"),
                      _("Distribution:"), _("Fit Method:"), _("Confidence:"),
                      _("Confidence Type:"), _("Confidence Method:"),
                      _("Mission Time:"), _("Number of Points:")]

    def __init__(self, application):
        """
        Initializes the Dataset Object.

        Keyword Arguments:
        application -- the RelKit application.
        """

        self._ready = False

        self._app = application

        self.treeview = None
        self.model = None
        self.selected_row = None
        self.dataset_id = 0
        self.n_datasets = 0
        self._col_order = []

# Create the Notebook for the SOFTWARE object.
        self.notebook = gtk.Notebook()
        if(_conf.TABPOS[2] == 'left'):
            self.notebook.set_tab_pos(gtk.POS_LEFT)
        elif(_conf.TABPOS[2] == 'right'):
            self.notebook.set_tab_pos(gtk.POS_RIGHT)
        elif(_conf.TABPOS[2] == 'top'):
            self.notebook.set_tab_pos(gtk.POS_TOP)
        else:
            self.notebook.set_tab_pos(gtk.POS_BOTTOM)

# Create the Analyses Input tab widgets.
        self.cmbAssembly = _widg.make_combo(simple=False)
        self.cmbConfType = _widg.make_combo()
        self.cmbConfMethod = _widg.make_combo()
        self.cmbDistribution = _widg.make_combo()
        self.cmbFitMethod = _widg.make_combo()
        self.cmbSource = _widg.make_combo()

        self.txtConfidence = _widg.make_entry(_width_=100)
        self.txtDescription = _widg.make_entry(_width_=400)
        self.txtRelTime = _widg.make_entry(_width_=100)
        self.txtRelPoints = _widg.make_entry(_width_=100)

        if self._analyses_input_widgets_create():
            self.debug_app._log.error("dataset.py: Failed to create Analysis Input widgets.")
        if self._analyses_input_tab_create():
            self.debug_app._log.error("dataset.py: Failed to create Analysis Input tab.")

# Create the Analyses Results tab widgets.
        self.txtMHB = _widg.make_entry(_width_=150)
        self.txtLP = _widg.make_entry(_width_=150)
        self.txtLR = _widg.make_entry(_width_=150)
        self.txtScale = _widg.make_entry(_width_=150)
        self.txtScaleLL = _widg.make_entry(_width_=150)
        self.txtScaleUL = _widg.make_entry(_width_=150)
        self.txtShape = _widg.make_entry(_width_=150)
        self.txtShapeLL = _widg.make_entry(_width_=150)
        self.txtShapeUL = _widg.make_entry(_width_=150)
        self.txtLocation = _widg.make_entry(_width_=150)
        self.txtLocationLL = _widg.make_entry(_width_=150)
        self.txtLocationUL = _widg.make_entry(_width_=150)
        self.txtCov11 = _widg.make_entry(_width_=150)
        self.txtCov12 = _widg.make_entry(_width_=150)
        self.txtCov13 = _widg.make_entry(_width_=150)
        self.txtCov21 = _widg.make_entry(_width_=150)
        self.txtCov22 = _widg.make_entry(_width_=150)
        self.txtCov23 = _widg.make_entry(_width_=150)
        self.txtCov31 = _widg.make_entry(_width_=150)
        self.txtCov32 = _widg.make_entry(_width_=150)
        self.txtCov33 = _widg.make_entry(_width_=150)
        self.txtAIC = _widg.make_entry(_width_=150)
        self.txtBIC = _widg.make_entry(_width_=150)
        self.txtMLE = _widg.make_entry(_width_=150)
        self.txtNumSuspensions = _widg.make_entry(_width_=100)
        self.txtNumFailures = _widg.make_entry(_width_=100)
        self.txtMTBF = _widg.make_entry(_width_=100)
        self.txtMTBFLL = _widg.make_entry(_width_=100)
        self.txtMTBFUL = _widg.make_entry(_width_=100)

        self.tvwNonParResults = gtk.TreeView()

        if self._analyses_results_widgets_create():
            self.debug_app._log.error("dataset.py: Failed to create Analysis Results widgets.")
        if self._analyses_results_tab_create():
            self.debug_app._log.error("dataset.py: Failed to create Analysis Results tab.")

# Create the Plot tab widgets.
        self.figSurvival = Figure(figsize=(6, 4))
        self.pltSurvival = FigureCanvas(self.figSurvival)
        self.axSurvival = self.figSurvival.add_subplot(111)
        self.figProbability = Figure(figsize=(6, 4))
        self.pltProbability = FigureCanvas(self.figProbability)
        self.axProbability = self.figProbability.add_subplot(111)
        self.figLogHazard = Figure(figsize=(6, 4))
        self.pltLogHazard = FigureCanvas(self.figLogHazard)
        self.axLogHazard = self.figLogHazard.add_subplot(111)
        self.figHazardRate = Figure(figsize=(6, 4))
        self.pltHazardRate = FigureCanvas(self.figHazardRate)
        self.axHazardRate = self.figHazardRate.add_subplot(111)

        if self._plot_widgets_create():
            self.debug_app._log.error("dataset.py: Failed to create Plot widgets.")
        if self._plot_tab_create():
            self.debug_app._log.error("dataset.py: Failed to create Plot tab.")

        self.vbxDataset = gtk.VBox()
        toolbar = self._toolbar_create()

        self.vbxDataset.pack_start(toolbar, expand=False)
        self.vbxDataset.pack_start(self.notebook)

    def _toolbar_create(self):
        """
        Method to create the toolbar for the INCIDENT Object work book.
        """

        toolbar = gtk.Toolbar()

# Add item button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_ADD)
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        button.set_icon_widget(image)
        button.set_name('Add')
        #button.connect('clicked', self._component_add)
        button.set_tooltip_text(_("Adds a record to the selected data set."))
        toolbar.insert(button, 0)

# Calculate button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_NO)
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        button.set_icon_widget(image)
        button.set_name('Calculate')
        button.connect('clicked', self._calculate)
        button.set_tooltip_text(_("Analyzes the selected data set."))
        toolbar.insert(button, 1)

# Save button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_SAVE)
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        button.set_icon_widget(image)
        button.set_name('Save')
        button.connect('clicked', self.dataset_save)
        button.set_tooltip_text(_("Saves the selected data set."))
        toolbar.insert(button, 2)

# Assign results to affected assembly.
        button = gtk.ToolButton(stock_id = gtk.STOCK_NO)
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/import.png')
        button.set_icon_widget(image)
        button.set_name('Assign')
        button.connect('clicked', self._assign_results)
        button.set_tooltip_text(_("Assigns MTBF and hazard rate results to the selected assembly."))
        toolbar.insert(button, 3)

        toolbar.show()

        return(toolbar)

    def _analyses_input_widgets_create(self):
        """ Method to create the Analysis Input widgets. """

        # Quadrant 1 (upper left) widgets.
        self.cmbAssembly.set_tooltip_text(_("Selects and displays the assembly associated with the dataset."))
        self.cmbAssembly.connect('changed', self._callback_combo, 1)

        self.cmbSource.set_tooltip_text(_("Selects and displays the source of the selected data set."))
        results = [["ALT"], ["Reliability Growth"],
                   ["Reliability Demonstration"], ["Field"]]
        _widg.load_combo(self.cmbSource, results)
        self.cmbSource.connect('changed', self._callback_combo, 3)

        self.cmbDistribution.set_tooltip_text(_("Selects and displays the statistical distribution used to fit the data."))
        results = [["MCF"], ["Kaplan-Meier"], ["Gamma"], ["Exponential"],
                   ["Lognormal"], ["Normal"], ["Weibull"], ["WeiBayes"]]
        _widg.load_combo(self.cmbDistribution, results)
        self.cmbDistribution.connect('changed', self._callback_combo, 4)

        self.cmbConfType.set_tooltip_text(_("Selects and displays the confidence bound type."))
        results = [["Lower One-Sided"], ["Upper One-Sided"], ["Two-Sided"]]
        _widg.load_combo(self.cmbConfType, results)
        self.cmbConfType.connect('changed', self._callback_combo, 6)

        self.cmbConfMethod.set_tooltip_text(_("Selects and displays the method for developing confidence bounds."))
        results = [["Fisher Matrix"], ["Likelihood"], ["Bootstrap"]]
        _widg.load_combo(self.cmbConfMethod, results)
        self.cmbConfMethod.connect('changed', self._callback_combo, 7)

        self.cmbFitMethod.set_tooltip_text(_("Selects and displays the method used to fit the data to the selected distribution."))
        results = [["Rank Regression"], ["MLE"]]
        _widg.load_combo(self.cmbFitMethod, results)
        self.cmbFitMethod.connect('changed', self._callback_combo, 8)

        self.txtDescription.set_tooltip_text(_("Description of the selected data set."))
        self.txtDescription.connect('focus-out-event',
                                    self._callback_entry, 'text', 2)

        self.txtConfidence.set_tooltip_text(_("Desired statistical confidence"))
        self.txtConfidence.connect('focus-out-event',
                                   self._callback_entry, 'float', 5)

        self.txtRelTime.set_tooltip_text(_("Time at which to calculate reliability metrics."))
        self.txtRelTime.connect('focus-out-event',
                                self._callback_entry, 'float', 9)

        self.txtRelPoints.set_tooltip_text(_("Number of points at which to calculate reliability metrics."))
        self.txtRelPoints.connect('focus-out-event',
                                  self._callback_entry, 'int', 10)

        return False

    def _analyses_input_tab_create(self):
        """
        Method to create the Analysis Input gtk.Notebook tab and populate it
        with the appropriate widgets for the DATASET object.
        """

        hbox = gtk.HBox()

        # Populate tab.
        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_("Analyses Inputs"))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(fixed)

        y_pos = 5

        label = _widg.make_label(self._ai_tab_labels[0], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbAssembly, 160, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ai_tab_labels[1], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtDescription, 160, y_pos)
        y_pos += 30

        label = _widg.make_label(self._ai_tab_labels[2], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbSource, 160, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ai_tab_labels[3], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbDistribution, 160, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ai_tab_labels[4], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbFitMethod, 160, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ai_tab_labels[5], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtConfidence, 160, y_pos)
        y_pos += 30

        label = _widg.make_label(self._ai_tab_labels[6], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbConfType, 160, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ai_tab_labels[7], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbConfMethod, 160, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ai_tab_labels[8], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtRelTime, 160, y_pos)
        y_pos += 30

        label = _widg.make_label(self._ai_tab_labels[9], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtRelPoints, 160, y_pos)

        fixed.show_all()

        hbox.pack_start(frame, True, True)

        # Insert the tab.
        label = gtk.Label()
        _heading = _("Analysis\nInputs")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays analysis inputs for the selected dataset."))

        self.notebook.insert_page(hbox,
                                  tab_label=label,
                                  position=-1)

        return False

    def _analyses_input_tab_load(self):
        """
        Loads the widgets with analyses input data for the DATASET Object.
        """

        _index_ = 0
        _assembly_id = self.model.get_value(self.selected_row, 1)
        model = self.cmbAssembly.get_model()
        row = model.get_iter_root()
        while row is not None:
            if(model.get_value(row, 1) == str(_assembly_id)):
                break
            else:
                row = model.iter_next(row)
                _index_ += 1

        self.cmbAssembly.set_active(_index_)

        self.cmbSource.set_active(self.model.get_value(self.selected_row, 3))
        self.cmbDistribution.set_active(self.model.get_value(self.selected_row, 4))
        self.cmbConfType.set_active(self.model.get_value(self.selected_row, 6))
        self.cmbConfMethod.set_active(self.model.get_value(self.selected_row, 7))
        self.cmbFitMethod.set_active(self.model.get_value(self.selected_row, 8))

        self.txtDescription.set_text(str(self.model.get_value(self.selected_row, 2)))
        self.txtConfidence.set_text(str(self.model.get_value(self.selected_row, 5)))
        self.txtRelTime.set_text(str(self.model.get_value(self.selected_row, 9)))
        self.txtRelPoints.set_text(str(self.model.get_value(self.selected_row, 10)))

        return False

    def _analyses_results_widgets_create(self):
        """ Method for creating DATASET Class analysis results widgets. """

        self.txtMHB.set_tooltip_text(_(""))
        self.txtLP.set_tooltip_text(_(""))
        self.txtLR.set_tooltip_text(_(""))
        self.txtScale.set_tooltip_text(_(""))
        self.txtScaleLL.set_tooltip_text(_(""))
        self.txtScaleUL.set_tooltip_text(_(""))
        self.txtShape.set_tooltip_text(_(""))
        self.txtShapeLL.set_tooltip_text(_(""))
        self.txtShapeUL.set_tooltip_text(_(""))
        self.txtLocation.set_tooltip_text(_(""))
        self.txtLocationLL.set_tooltip_text(_(""))
        self.txtLocationUL.set_tooltip_text(_(""))
        self.txtCov11.set_tooltip_text(_(""))
        self.txtCov12.set_tooltip_text(_(""))
        self.txtCov13.set_tooltip_text(_(""))
        self.txtCov21.set_tooltip_text(_(""))
        self.txtCov22.set_tooltip_text(_(""))
        self.txtCov23.set_tooltip_text(_(""))
        self.txtCov31.set_tooltip_text(_(""))
        self.txtCov32.set_tooltip_text(_(""))
        self.txtCov33.set_tooltip_text(_(""))
        self.txtAIC.set_tooltip_text(_(""))
        self.txtBIC.set_tooltip_text(_(""))
        self.txtMLE.set_tooltip_text(_(""))
        self.txtNumSuspensions.set_tooltip_text(_(""))
        self.txtNumFailures.set_tooltip_text(_(""))
        self.txtMTBF.set_tooltip_text(_(""))
        self.txtMTBFLL.set_tooltip_text(_(""))
        self.txtMTBFUL.set_tooltip_text(_(""))

        return False

    def _analyses_results_tab_create(self):
        """
        Method to create the Analysis Input gtk.Notebook tab and populate it
        with the appropriate widgets for the DATASET object.
        """

        hbox = gtk.HBox()

        # Populate quadrant 2 (right half).
        vbox = gtk.VBox()

        # Summary results.
        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_("Summary"))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(fixed)

        y_pos = 5
        label = _widg.make_label(_("Number of Suspensions:"), width=200)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtNumSuspensions, 210, y_pos)
        y_pos += 30

        label = _widg.make_label(_("Number of Failures:"), width=200)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtNumFailures, 210, y_pos)
        y_pos += 30

        label = _widg.make_label(_("Estimated MTBF:"), width=200)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtMTBF, 210, y_pos)
        fixed.put(self.txtMTBFLL, 315, y_pos)
        fixed.put(self.txtMTBFUL, 420, y_pos)
        y_pos += 30

        vbox.pack_start(frame, True, True)

        # Non-parametric table of results.
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
        self.tvwNonParResults.set_model(model)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_("Time"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(""))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=1)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(""))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=2)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(""))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=3)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_("S(t)"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=4)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_("Standard\nError"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=5)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_("Lower\nBound"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=6)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_("Upper\nBound"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=7)
        self.tvwNonParResults.append_column(column)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwNonParResults)

        frame = _widg.make_frame(_label_=_("Non-Parametric Estimates"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vbox.pack_start(frame, True, True)

        # Non-parametric goodness of fit statistics.
        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_("Non-Parametric GOF Statistics"))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(fixed)

        y_pos = 5
        label = _widg.make_label(_("MIL Handbook"), width=150)
        fixed.put(label, 155, y_pos)

        label = _widg.make_label(_("Laplace"), width=150)
        fixed.put(label, 310, y_pos)

        label = _widg.make_label(_("Lewis-Robinson"), width=150)
        fixed.put(label, 465, y_pos)
        y_pos += 30

        fixed.put(self.txtMHB, 155, y_pos)
        fixed.put(self.txtLP, 310, y_pos)
        fixed.put(self.txtLR, 465, y_pos)

        vbox.pack_start(frame, True, True)

        hbox.pack_start(vbox, True, True)

        # Parametric estimates.
        vbox = gtk.VBox()

        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_("Parametric Estimates"))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(fixed)

        y_pos = 5
        label = _widg.make_label(_("Scale Parameter"), width=150)
        fixed.put(label, 155, y_pos)

        label = _widg.make_label(_("Shape Parameter"), width=150)
        fixed.put(label, 310, y_pos)

        label = _widg.make_label(_("Location Parameter"), width=150)
        fixed.put(label, 465, y_pos)
        y_pos += 30

        label = _widg.make_label(_("Lower Bound"), width=150)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtScaleLL, 155, y_pos)
        fixed.put(self.txtShapeLL, 310, y_pos)
        fixed.put(self.txtLocationLL, 465, y_pos)
        y_pos += 30

        label = _widg.make_label(_("Point Estimate"), width=150)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtScale, 155, y_pos)
        fixed.put(self.txtShape, 310, y_pos)
        fixed.put(self.txtLocation, 465, y_pos)
        y_pos += 30

        label = _widg.make_label(_("Upper Bound"), width=150)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtScaleUL, 155, y_pos)
        fixed.put(self.txtShapeUL, 310, y_pos)
        fixed.put(self.txtLocationUL, 465, y_pos)

        vbox.pack_start(frame, True, True)

        # Covariance matrix.
        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_("Covariance Matrix"))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(fixed)

        y_pos = 5
        label = _widg.make_label(_("Scale"), width=150)
        fixed.put(label, 155, y_pos)
        label = _widg.make_label(_("Shape"), width=150)
        fixed.put(label, 310, y_pos)
        label = _widg.make_label(_("Location"), width=150)
        fixed.put(label, 465, y_pos)
        y_pos += 30

        label = _widg.make_label(_("Scale"), width=150)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtCov11, 155, y_pos)
        fixed.put(self.txtCov12, 310, y_pos)
        fixed.put(self.txtCov13, 465, y_pos)
        y_pos += 30

        label = _widg.make_label(_("Shape"), width=150)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtCov21, 155, y_pos)
        fixed.put(self.txtCov22, 310, y_pos)
        fixed.put(self.txtCov23, 465, y_pos)
        y_pos += 30

        label = _widg.make_label(_("Location"), width=150)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtCov31, 155, y_pos)
        fixed.put(self.txtCov32, 310, y_pos)
        fixed.put(self.txtCov33, 465, y_pos)

        vbox.pack_start(frame, True, True)

        # Parametric goodness of fit statistics.
        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_("Parametric GOF Statistics"))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(fixed)

        y_pos = 5
        label = _widg.make_label("AIC", width=150)
        fixed.put(label, 155, y_pos)
        label = _widg.make_label("BIC", width=150)
        fixed.put(label, 310, y_pos)
        label = _widg.make_label("MLE", width=150)
        fixed.put(label, 465, y_pos)
        y_pos += 30

        fixed.put(self.txtAIC, 155, y_pos)
        fixed.put(self.txtBIC, 310, y_pos)
        fixed.put(self.txtMLE, 465, y_pos)

        vbox.pack_start(frame, True, True)

        hbox.pack_start(vbox, True, True)

        # Insert the tab.
        label = gtk.Label()
        _heading = _("Analysis\nResults")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays analysis results for the selected dataset."))

        self.notebook.insert_page(hbox,
                                  tab_label=label,
                                  position=-1)

        return False

    def _analyses_results_tab_load(self):
        """
        Loads the widgets with analyses results for the DATASET Object.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        self.txtNumSuspensions.set_text(str(self.model.get_value(self.selected_row, 11)))
        self.txtNumFailures.set_text(str(self.model.get_value(self.selected_row, 12)))
        self.txtScale.set_text(str(fmt.format(self.model.get_value(self.selected_row, 13))))
        self.txtScaleLL.set_text(str(fmt.format(self.model.get_value(self.selected_row, 14))))
        self.txtScaleUL.set_text(str(fmt.format(self.model.get_value(self.selected_row, 15))))
        self.txtShape.set_text(str(fmt.format(self.model.get_value(self.selected_row, 16))))
        self.txtShapeLL.set_text(str(fmt.format(self.model.get_value(self.selected_row, 17))))
        self.txtShapeUL.set_text(str(fmt.format(self.model.get_value(self.selected_row, 18))))
        self.txtLocation.set_text(str(fmt.format(self.model.get_value(self.selected_row, 19))))
        self.txtLocationLL.set_text(str(fmt.format(self.model.get_value(self.selected_row, 20))))
        self.txtLocationUL.set_text(str(fmt.format(self.model.get_value(self.selected_row, 21))))
        self.txtCov11.set_text(str(fmt.format(self.model.get_value(self.selected_row, 22))))        # Scale variance (var 1)
        self.txtCov22.set_text(str(fmt.format(self.model.get_value(self.selected_row, 23))))        # Scale variance (var 2)
        self.txtCov33.set_text(str(fmt.format(self.model.get_value(self.selected_row, 24))))        # Location variance (var 3)
        self.txtCov12.set_text(str(fmt.format(self.model.get_value(self.selected_row, 25))))        # Scale-Shape variance (cov 1)
        self.txtCov21.set_text(str(fmt.format(self.model.get_value(self.selected_row, 25))))        # Scale-Shape variance (cov 1)
        self.txtCov13.set_text(str(fmt.format(self.model.get_value(self.selected_row, 26))))        # Scale-Location variance (cov 2)
        self.txtCov31.set_text(str(fmt.format(self.model.get_value(self.selected_row, 26))))        # Scale-Location variance (cov 2)
        self.txtCov23.set_text(str(fmt.format(self.model.get_value(self.selected_row, 27))))        # Shape-Location variance (cov 3)
        self.txtCov32.set_text(str(fmt.format(self.model.get_value(self.selected_row, 27))))        # Shape-Location variance (cov 3)
        self.txtMHB.set_text(str(fmt.format(self.model.get_value(self.selected_row, 28))))
        self.txtLP.set_text(str(fmt.format(self.model.get_value(self.selected_row, 29))))
        self.txtLR.set_text(str(fmt.format(self.model.get_value(self.selected_row, 30))))
        self.txtAIC.set_text(str(fmt.format(self.model.get_value(self.selected_row, 31))))
        self.txtBIC.set_text(str(fmt.format(self.model.get_value(self.selected_row, 32))))
        self.txtMLE.set_text(str(fmt.format(self.model.get_value(self.selected_row, 33))))

        return False

    def _plot_widgets_create(self):

        return False

    def _plot_tab_create(self):
        """
        Method to create the survival analysis plot gtk.Notebook tab and add
        it to the gtk.Notebook at the correct location.
        """

        hbox = gtk.HBox()

        frame = _widg.make_frame(_label_=_("Survival Analysis Plots"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(hbox)
        frame.show_all()

        vbox = gtk.VBox()
        hbox.pack_start(vbox)

        vbox.pack_start(self.pltSurvival)
        vbox.pack_start(self.pltProbability)

        vbox = gtk.VBox()
        hbox.pack_start(vbox)

        vbox.pack_start(self.pltLogHazard)
        vbox.pack_start(self.pltHazardRate)

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Analysis\nPlots") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays survival analyses plots."))
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _calculate(self, button):
        """
        Method to execute the selected analysis.

        Keyword Arguments:
        button -- the gtk.ToolButton that called this method.
        """

        import operator
        import itertools
        import numpy

        from math import log, sqrt
        from scipy.stats import norm

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _dataset_ = self.model.get_value(self.selected_row, 0)
        _analysis_ = self.model.get_value(self.selected_row, 4)
        _conf_ = self.model.get_value(self.selected_row, 5)
        _type_ = self.model.get_value(self.selected_row, 6)
        _reltime_ = self.model.get_value(self.selected_row, 9)

        if(_analysis_ == 1):                # MCF
            query = "SELECT fld_unit, fld_left_interval, \
                            fld_right_interval, fld_tbf \
                     FROM tbl_survival_data \
                     WHERE fld_dataset_id=%d \
                     AND fld_status=1 \
                     ORDER BY fld_unit ASC, \
                              fld_left_interval ASC" % _dataset_
            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx)

            # Create a list of unique units and then get a count of the
            # total number of unique units.
            _units_ = []
            idx = operator.itemgetter(0)
            y = itertools.imap(idx, results)
            for i in y:
                _units_.append(i)
            _units_ = list(set(_units_))

            # Create a list of unique failures times and then get a counts of
            # the total number of unique failurestimes.
            _times_ = []
            idx = operator.itemgetter(2)
            y = itertools.imap(idx, results)
            for i in y:
                _times_.append(i)
            _times_ = list(set(_times_))
            _times_.sort()

            _calc.mean_cumulative_function(_units_, _times_, results)

        elif(_analysis_ == 2):              # Kaplan-Meier
            query = "SELECT fld_right_interval, fld_status \
                     FROM tbl_survival_data \
                     WHERE fld_dataset_id=%d \
                     ORDER BY fld_right_interval ASC, \
                     fld_status DESC" % _dataset_
            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx)

            # 0 = Event Time (string)
            # 1 = number at risk at beginning of interval i (integer)
            # 2 = number of events in interval [i - 1, 1] (integer)
            # 3 = probability of survival in interval [i - 1, 1] (float)
            # 4 = probability of survival up to time i S(ti) (float)
            # 5 = Standard error of S(ti) (float)
            # 6 = Lower bound on S(ti)
            # 7 = Upper bound on S(ti)
            # 8 = Cumulative hazard function [H(t)]
            # 9 = Estiamte of the mean up to time i
            nonpar = _calc.kaplan_meier(results, _reltime_, _conf_, _type_)

            n_points = len(nonpar)
            times = [x[0] for x in nonpar]
            Shat = [x[4] for x in nonpar]
            Shatll = [x[6] for x in nonpar]
            Shatul = [x[7] for x in nonpar]
            _H_ = [x[8] for x in nonpar]
            muhat = [x[9] for x in nonpar]

            logH = []
            logtimes = []
            zShat = []
            _h_ = []
            for i in range(n_points):
                logH.append(log(_H_[i]))
                logtimes.append(log(times[i]))
                zShat.append(norm.ppf(Shat[i]))
                _h_.append(_H_[i] / times[i])

            model = self.tvwNonParResults.get_model()
            model.clear()

            for i in range(n_points):
                _data_ = [str(nonpar[i][0]), int(nonpar[i][1]),
                          int(nonpar[i][2]), float(nonpar[i][3]),
                          float(nonpar[i][4]), float(nonpar[i][5]),
                          float(nonpar[i][6]), float(nonpar[i][7])]
                model.append(_data_)

            self.txtMTBF.set_text(str(fmt.format(muhat[n_points - 1])))
            #self.txtMTBFLL.set_text(str(fmt.format(muhatll)))
            #self.txtMTBFUL.set_text(str(fmt.format(muhatul)))

            _name = self.model.get_value(self.selected_row, 2)

            # Plot the survival curve.
            self.axSurvival.cla()

            self.axSurvival.grid(True, which='both')
            self.axSurvival.set_title(_("Kaplan-Meier Plot of %s") % _name)
            self.axSurvival.set_xlabel(_("Time"))
            self.axSurvival.set_ylabel(_("Survival Function [S(t)]"))

            lineSurv, = self.axSurvival.step(times, Shat, 'g-', where='mid')
            lineSurv2, = self.axSurvival.step(times, Shatll, 'r-', where='mid')
            lineSurv3, = self.axSurvival.step(times, Shatul, 'b-', where='mid')

            for i in range(n_points):
                lineSurv.set_ydata(Shat)
                lineSurv2.set_ydata(Shatll)
                lineSurv3.set_ydata(Shatul)

            self.pltSurvival.draw()

            labell = "Lower %s%% Bound" % str('{0:0.4g}'.format(_conf_))
            labelu = "Upper %s%% Bound" % str('{0:0.4g}'.format(_conf_))
            self.figSurvival.legend((lineSurv, lineSurv2, lineSurv3),
                                    ("Survival Function", labell,
                                    labelu),
                                    'upper right')

            # Plot the cumulative hazard curve.
            self.axProbability.cla()

            self.axProbability.grid(True, which='both')
            self.axProbability.set_title(_("Cumulative Hazard Plot of %s") % _name)
            self.axProbability.set_xlabel(_("Time"))
            self.axProbability.set_ylabel(_("Cumulative Hazard Function [H(t)]"))

            lineProb, = self.axProbability.step(times, _H_, 'g-', where='mid')
            #lineProb2, = self.axProbability.step(times, _Hll_, 'r-', where='mid')
            #lineProb3, = self.axProbability.step(times, _Hul_, 'b-', where='mid')

            for i in range(n_points):
                lineProb.set_ydata(_H_)
                #lineProb2.set_ydata(_Hll_)
                #lineProb3.set_ydata(_Hul_)

            self.pltProbability.draw()

            labell = "Lower %s%% Bound" % str('{0:0.4g}'.format(_conf_))
            labelu = "Upper %s%% Bound" % str('{0:0.4g}'.format(_conf_))
            #self.figProbability.legend((lineProb, lineProb2, lineProb3),
            #                        ("Cumulative Hazard Function", labell,
            #                        labelu),
            #                        'upper right')

            # Plot the log cumulative hazard curve.
            self.axLogHazard.cla()

            self.axLogHazard.grid(True, which='both')
            self.axLogHazard.set_title(_("Log Hazard Plot of %s") % _name)
            self.axLogHazard.set_xlabel(_("Time"))
            self.axLogHazard.set_ylabel(_("Log Hazard Function [H(t)]"))

            lineLogHaz, = self.axLogHazard.step(logtimes, logH, 'g-', where='mid')
            #lineLogHaz2, = self.axLogHazard.step(log(times), log(_Hll_), 'r-', where='mid')
            #lineLogHaz3, = self.axLogHazard.step(log(times), log(_Hul_), 'b-', where='mid')

            for i in range(n_points):
                lineLogHaz.set_ydata(logH)
                #lineLogHaz2.set_ydata(_Hll_)
                #lineLogHaz3.set_ydata(_Hul_)

            self.pltLogHazard.draw()

            labell = "Lower %s%% Bound" % str('{0:0.4g}'.format(_conf_))
            labelu = "Upper %s%% Bound" % str('{0:0.4g}'.format(_conf_))
            #self.figLogHazard.legend((lineProb, lineProb2, lineProb3),
            #                        ("Log Cumulative Hazard Function", labell,
            #                        labelu),
            #                        'upper right')

            # Plot the hazard rate curve.
            self.axHazardRate.cla()

            self.axHazardRate.grid(True, which='both')
            self.axHazardRate.set_title(_("Z(S) Plot of %s") % _name)
            self.axHazardRate.set_xlabel(_("Time"))
            self.axHazardRate.set_ylabel(_("Z(S(t))"))

            lineHazRate, = self.axHazardRate.step(logtimes, _h_, 'g-', where='mid')
            #lineHazRate2, = self.axHazardRate.step(log(times), log(_Hll_), 'r-', where='mid')
            #lineHazRate3, = self.axHazardRate.step(log(times), log(_Hul_), 'b-', where='mid')

            for i in range(n_points):
                lineHazRate.set_ydata(_h_)
                #lineHazRate2.set_ydata(_Hll_)
                #lineHazRate3.set_ydata(_Hul_)

            self.pltHazardRate.draw()

            labell = "Lower %s%% Bound" % str('{0:0.4g}'.format(_conf_))
            labelu = "Upper %s%% Bound" % str('{0:0.4g}'.format(_conf_))
            #self.figHazardRate.legend((lineProb, lineProb2, lineProb3),
            #                        ("Log Cumulative Hazard Function", labell,
            #                        labelu),
            #                        'upper right')

    def dataset_save(self, button):
        """
        Saves the DATASET Object gtk.TreeView information to the Program's
        MySQL or SQLite3 database.

        Keyword Arguments:
        button -- the gtk.Button widget that called this function.
        """

        self.model.foreach(self._save_line_item)

        return False

    def _save_line_item(self, model, path_, row):
        """
        Saves each row in the DATASET Object treeview model to the RelKit's
        Program MySQL or SQLite3 database.

        Keyword Arguments:
        model -- the DATASET gtk.ListStore.
        path_ -- the path of the active row in the DATASET gtk.ListStore.
        row   -- the selected row in the DATASET gtk.TreeView.
        """

        values = (self.model.get_value(self.selected_row, 1), \
                  self.model.get_value(self.selected_row, 2), \
                  self.model.get_value(self.selected_row, 3), \
                  self.model.get_value(self.selected_row, 4), \
                  self.model.get_value(self.selected_row, 5), \
                  self.model.get_value(self.selected_row, 6), \
                  self.model.get_value(self.selected_row, 7), \
                  self.model.get_value(self.selected_row, 8), \
                  self.model.get_value(self.selected_row, 9), \
                  self.model.get_value(self.selected_row, 10), \
                  self.model.get_value(self.selected_row, 11), \
                  self.model.get_value(self.selected_row, 12), \
                  self.model.get_value(self.selected_row, 13), \
                  self.model.get_value(self.selected_row, 14), \
                  self.model.get_value(self.selected_row, 15), \
                  self.model.get_value(self.selected_row, 16), \
                  self.model.get_value(self.selected_row, 17), \
                  self.model.get_value(self.selected_row, 18), \
                  self.model.get_value(self.selected_row, 19), \
                  self.model.get_value(self.selected_row, 20), \
                  self.model.get_value(self.selected_row, 21), \
                  self.model.get_value(self.selected_row, 22), \
                  self.model.get_value(self.selected_row, 23), \
                  self.model.get_value(self.selected_row, 24), \
                  self.model.get_value(self.selected_row, 25), \
                  self.model.get_value(self.selected_row, 26), \
                  self.model.get_value(self.selected_row, 27), \
                  self.model.get_value(self.selected_row, 28), \
                  self.model.get_value(self.selected_row, 29), \
                  self.model.get_value(self.selected_row, 30), \
                  self.model.get_value(self.selected_row, 31), \
                  self.model.get_value(self.selected_row, 32), \
                  self.model.get_value(self.selected_row, 33), \
                  self.model.get_value(self.selected_row, 0))

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_dataset \
                     SET fld_assembly_id=%d, fld_description='%s', \
                         fld_source=%d, fld_distribution_id=%d, \
                         fld_confidence=%f, fld_confidence_type=%d, \
                         fld_confidence_method=%d, fld_fit_method=%d, \
                         fld_rel_time=%f, fld_num_rel_points=%d, \
                         fld_num_suspension=%d, fld_num_failures=%d, \
                         fld_scale=%f, fld_scale_ll=%f, fld_scale_ul=%f, \
                         fld_shape=%f, fld_shape_ll=%f, fld_shape_ul=%f, \
                         fld_location=%f, fld_location_ll=%f, \
                         fld_location_ul=%f, fld_variance_1=%f, \
                         fld_variance_2=%f, fld_variance_3=%f, \
                         fld_covariance_1=%f, fld_covariance_2=%f, \
                         fld_covariance_3=%f, fld_mhb=%f, fld_lp=%f, \
                         fld_lr=%f, fld_aic=%f, fld_bic=%f, fld_mle=%f \
                     WHERE fld_dataset_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_dataset \
                     SET fld_assembly_id=?, fld_description=?, \
                         fld_source=?, fld_distribution_id=?, \
                         fld_confidence=?, fld_confidence_type=?, \
                         fld_confidence_method=?, fld_fit_method=?, \
                         fld_rel_time=?, fld_num_rel_points=?, \
                         fld_num_suspension=?, fld_num_failures=?, \
                         fld_scale=?, fld_scale_ll=?, fld_scale_ul=?, \
                         fld_shape=?, fld_shape_ll=?, fld_shape_ul=?, \
                         fld_location=?, fld_location_ll=?, \
                         fld_location_ul=?, fld_variance_1=?, \
                         fld_variance_2=?, fld_variance_3=?, \
                         fld_covariance_1=?, fld_covariance_2=?, \
                         fld_covariance_3=?, fld_mhb=?, fld_lp=?, \
                         fld_lr=?, fld_aic=?, fld_bic=?, fld_mle=? \
                     WHERE fld_dataset_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("dataset.py: Failed to save dataset.")
            return True

        return False

    def _assign_results(self, button):
        """
        Assigns the MTBF and hazard rate results to the assembly associated
        with the dataset.  Values are assigned to the specified fields.

        Keyword Arguments:
        button -- the gtk.Button widget that called this function.
        """

        _assembly_id = self.model.get_value(self.selected_row, 1)

        print _assembly_id

        return False

    def _callback_combo(self, combo, _index_):
        """
        Callback function to retrieve and save combobox changes.

        Keyword Arguments:
        combo   -- the combobox that called the function.
        _index_ -- the position in the DATASET Object _attribute list
                   associated with the data from the calling combobox.
        """

        # _index_   Field
        #   1       Assembly ID
        #   3       Source of dataset
        #   4       Statistical distribution ID
        #   6       Confidence type
        #   7       Confidence method
        #   8       Fit method
        if(_index_ == 1):
            model = combo.get_model()
            row = combo.get_active_iter()
            if(row is not None):
                _text_ = int(model.get_value(row, 1))
            else:
                _text_ = 0
        else:
            _text_ = combo.get_active()

        self.model.set_value(self.selected_row, _index_, _text_)

        return False

    def _callback_entry(self, entry, event, convert, _index_):
        """
        Callback function to retrieve and save entry changes.

        Keyword Arguments:
        entry    -- the gtk.Entry that called the function.
        event    -- the gtk.gdk.Event that called the function.
        convert  -- the data type to convert the entry contents to.
        _index_  -- the position in the applicable treeview associated
                    with the data from the calling gtk.Entry.
        """

        from datetime import datetime

        if(convert == 'text'):
            _text_ = entry.get_text()

        elif(convert == 'int'):
            _text_ = int(entry.get_text())

        elif(convert == 'float'):
            _text_ = float(entry.get_text().replace('$', ''))

        elif(convert == 'date'):
            _text_ = datetime.strptime(entry.get_text(), '%Y-%m-%d').toordinal()

        self.model.set_value(self.selected_row, _index_, _text_)

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the Validation Object
        treeview.

        Keyword Arguments:
        treeview -- the Validation Object treeview.
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
        Callback function to handle events for the INCIDENT Object
        gtk.Treeview.  It is called whenever the Incident Object treeview is
        clicked or a row is activated.

        Keyword Arguments:
        treeview -- the Incident Object gtk.TreeView.
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

    def create_tree(self):
        """
        Creates the DATASET treeview and connects it to callback functions to
        handle editting.  Background and foreground colors can be set using the
        user-defined values in the RelKit configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()
        bg_color = _conf.RELIAFREE_COLORS[12]
        fg_color = _conf.RELIAFREE_COLORS[13]
        (self.treeview, self._col_order) = _widg.make_treeview('Dataset', 16,
                                                               self._app,
                                                               None,
                                                               bg_color,
                                                               fg_color)
        self.treeview.set_enable_tree_lines(True)

        self.treeview.set_tooltip_text(_("Displays a list of survival data sets."))

        scrollwindow.add(self.treeview)
        self.model = self.treeview.get_model()

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)

        return(scrollwindow)

    def load_tree(self):
        """
        Loads the Hardware treeview model with system information.  This
        information can be stored either in a MySQL or SQLite3 database.
        """

        if(_conf.RELIAFREE_MODULES[0] == 1):
            values = (self._app.REVISION.revision_id,)
        else:
            values = (0,)

        query = "SELECT * FROM tbl_dataset"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            return True

        self.n_datasets = len(results)

        self.model.clear()

        # Load the model with the returned results.
        for i in range(self.n_datasets):
            self.model.append(None, results[i])

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        root = self.model.get_iter_root()
        if root is not None:
            path = self.model.get_path(root)
            col = self.treeview.get_column(0)
            self.treeview.row_activated(path, col)

        # Load the Assembly combo.
        query = "SELECT fld_description, fld_assembly_id, fld_name \
                 FROM tbl_system"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)
        _widg.load_combo(self.cmbAssembly, results, simple=False)

        return False

    def load_notebook(self):
        """ Method to load the DATASET Object gtk.Notebook. """

        if self.selected_row is not None:
            self._analyses_input_tab_load()
            self._analyses_results_tab_load()
        #    self._load_component_list()

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxDataset)
        self._app.winWorkBook.show_all()

        _title = _("RelKit Work Bench: Program Survival Analyses (%d Datasets)") % \
                   self.n_datasets
        self._app.winWorkBook.set_title(_title)

        self.notebook.set_current_page(0)

        return False
