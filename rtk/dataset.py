#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to
Program survival data sets.
"""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2012 - 2013 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       dataset.py is part of The RTK Project
#
# All rights reserved.

import sys
from os import name

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

import numpy

# Import R library.
try:
    from rpy2 import robjects
    from rpy2.robjects import r as R
    from rpy2.robjects.packages import importr
    __USE_RPY__ = False
    __USE_RPY2__ = True
except ImportError:
    __USE_RPY__ = False
    __USE_RPY2__ = False

# Import other RTK modules.
import configuration as _conf
import imports as _impt
import utilities as _util
import widgets as _widg

# Import other RTK classes.
from _assistants_.adds import AddDatasetRecord
from _assistants_.updates import AssignMTBFResults

# Import other RTK calculation functions.
from _calculations_.survival import *
from _calculations_.growth import power_law, loglinear, crow_amsaa_continuous

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
                      _("Start Time:"), _("End Time"), _("Step Interval:"),
                      _(u"Start Date:"), _(u"End Date:")]

    def __init__(self, application):
        """
        Initializes the Dataset Object.

        Keyword Arguments:
        application -- the RTK application.
        """

        self._ready = False
        self._nevada_chart_ = True         # Dataset created from a Nevada chart.

        self._app = application

        self.treeview = None
        self.model = None
        self.selected_row = None
        self.dataset_id = 0
        self.n_datasets = 0
        self._col_order = []

# Create the Notebook for the DATASET object.
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
        self.chkGroup = _widg.make_check_button(_label_=_(u"Decompose results to children assemblies"))
        self.chkParts = _widg.make_check_button(_label_=_(u"Decompose results to parts"))

        self.cmbAssembly = _widg.make_combo(simple=False)
        self.cmbConfType = _widg.make_combo()
        self.cmbConfMethod = _widg.make_combo()
        self.cmbDistribution = _widg.make_combo()
        self.cmbFitMethod = _widg.make_combo()
        self.cmbSource = _widg.make_combo()

        self.fraNevadaChart = _widg.make_frame(_label_=_(u"Nevada Chart"))

        self.lblFitMethod = _widg.make_label(self._ai_tab_labels[4], 150, 25)
        self.lblConfMethod = _widg.make_label(self._ai_tab_labels[7], 150, 25)

        self.tvwDataset = gtk.TreeView()
        self.tvwDataset.set_search_column(0)
        self.tvwDataset.set_reorderable(True)

        self.tvwNevadaChart = gtk.TreeView()

        self.txtConfidence = _widg.make_entry(_width_=100)
        self.txtDescription = _widg.make_entry(_width_=200)
        self.txtStartTime = _widg.make_entry(_width_=100)
        self.txtEndTime = _widg.make_entry(_width_=100)
        self.txtRelPoints = _widg.make_entry(_width_=100)

        self.txtStartDate = _widg.make_entry(_width_=100)
        self.txtEndDate = _widg.make_entry(_width_=100)

        self.btnStartDate = _widg.make_button(_height_=25, _width_=25,
                                              _label_="...", _image_=None)
        self.btnEndDate = _widg.make_button(_height_=25, _width_=25,
                                            _label_="...", _image_=None)

        if self._analyses_input_widgets_create():
            self._app.debug_log.error("dataset.py: Failed to create Analysis Input widgets.")
        if self._analyses_input_tab_create():
            self._app.debug_log.error("dataset.py: Failed to create Analysis Input tab.")

# Create the Analyses Results tab widgets.
        self.fraSummary = _widg.make_frame(_label_=_(u"Summary"))
        self.fraNonParEst = _widg.make_frame(_label_=_(u"Non-Parametric Estimates"))
        self.fraNonParStats = _widg.make_frame(_label_=_(u"Non-Parametric Statistics"))
        self.fraParEst = _widg.make_frame(_label_=_(u"Parametric Estimates"))
        self.fraVarCov = _widg.make_frame(_label_=_(u"Covariance Matrix"))
        self.fraParGOF = _widg.make_frame(_label_=_(u"Parametric GOF Statistics"))

        self.hpnAnalysisResults = gtk.HPaned()
        self.vbxAnalysisResults1 = gtk.VBox()
        self.vbxAnalysisResults2 = gtk.VBox()

        self.hpnAnalysisResults = gtk.HPaned()

        self.hpnAnalysisResults.pack1(self.vbxAnalysisResults1, True, True)

        # Upper left quadrant widgets.
        self.lblCumMTBF = _widg.make_label(_(u"Cumulative\nMTBF"), width=125,
                                           height=50)
        self.lblCumFI = _widg.make_label(_(u"Cumulative\nHazard\nRate"),
                                         width=125, height=50)
        self.lblMTBFi = _widg.make_label("", width=125, height=50)
        self.lblFIi = _widg.make_label("", width=125, height=50)

        self.txtNumSuspensions = _widg.make_entry(_width_=100)
        self.txtNumFailures = _widg.make_entry(_width_=100)

        self.txtMTBF = _widg.make_entry(_width_=125)
        self.txtMTBFLL = _widg.make_entry(_width_=125)
        self.txtMTBFUL = _widg.make_entry(_width_=125)
        self.txtHazardRate = _widg.make_entry(_width_=125)
        self.txtHazardRateLL = _widg.make_entry(_width_=125)
        self.txtHazardRateUL = _widg.make_entry(_width_=125)
        self.txtMTBFi = _widg.make_entry(_width_=125)
        self.txtMTBFiLL = _widg.make_entry(_width_=125)
        self.txtMTBFiUL = _widg.make_entry(_width_=125)
        self.txtHazardRatei = _widg.make_entry(_width_=125)
        self.txtHazardRateiLL = _widg.make_entry(_width_=125)
        self.txtHazardRateiUL = _widg.make_entry(_width_=125)

        # Lower left quadrant non-parametric widgets.
        self.lblMHBResult = _widg.make_label(_(u""), width=100)
        self.lblZLPResult = _widg.make_label(_(u""), width=100)
        self.lblZLRResult = _widg.make_label(_(u""), width=100)
        self.lblRhoResult = _widg.make_label(_(u""), width=100)

        self.txtMHB = _widg.make_entry(_width_=100)
        self.txtChiSq = _widg.make_entry(_width_=100)
        self.txtMHBPValue = _widg.make_entry(_width_=100)
        self.txtLP = _widg.make_entry(_width_=100)
        self.txtZLPNorm = _widg.make_entry(_width_=100)
        self.txtZLPPValue = _widg.make_entry(_width_=100)
        self.txtLR = _widg.make_entry(_width_=100)
        self.txtZLRNorm = _widg.make_entry(_width_=100)
        self.txtZLRPValue = _widg.make_entry(_width_=100)
        self.txtRho = _widg.make_entry(_width_=100)
        self.txtRhoNorm = _widg.make_entry(_width_=100)
        self.txtRhoPValue = _widg.make_entry(_width_=100)

        # Lower left quadrant parametric widgets.
        self.lblScale = _widg.make_label(_(u"Scale"), width=150)
        self.lblShape = _widg.make_label(_(u"Shape"), width=150)
        self.lblLocation = _widg.make_label(_(u"Location"), width=150)
        self.lblRowScale = _widg.make_label(_(u"Scale"), width=150)
        self.lblRowShape = _widg.make_label(_(u"Shape"), width=150)
        self.lblRowLocation = _widg.make_label(_(u"Location"), width=150)
        self.lblColScale = _widg.make_label(_(u"Scale"), width=150)
        self.lblColShape = _widg.make_label(_(u"Shape"), width=150)
        self.lblColLocation = _widg.make_label(_(u"Location"), width=150)
        self.lblModel = _widg.make_label("", width=350)

        self.txtScale = _widg.make_entry(_width_=150)
        self.txtScaleLL = _widg.make_entry(_width_=150)
        self.txtScaleUL = _widg.make_entry(_width_=150)
        self.txtShape = _widg.make_entry(_width_=150)
        self.txtShapeLL = _widg.make_entry(_width_=150)
        self.txtShapeUL = _widg.make_entry(_width_=150)
        self.txtLocation = _widg.make_entry(_width_=150)
        self.txtLocationLL = _widg.make_entry(_width_=150)
        self.txtLocationUL = _widg.make_entry(_width_=150)

        self.txtShapeShape = _widg.make_entry(_width_=150)
        self.txtShapeScale = _widg.make_entry(_width_=150)
        self.txtShapeLocation = _widg.make_entry(_width_=150)
        self.txtScaleShape = _widg.make_entry(_width_=150)
        self.txtScaleScale = _widg.make_entry(_width_=150)
        self.txtScaleLocation = _widg.make_entry(_width_=150)
        self.txtLocationShape = _widg.make_entry(_width_=150)
        self.txtLocationScale = _widg.make_entry(_width_=150)
        self.txtLocationLocation = _widg.make_entry(_width_=150)
        self.txtAIC = _widg.make_entry(_width_=150)
        self.txtBIC = _widg.make_entry(_width_=150)
        self.txtMLE = _widg.make_entry(_width_=150)

        self.tvwNonParResults = gtk.TreeView()

        if self._analyses_results_widgets_create():
            self._app.debug_log.error("dataset.py: Failed to create Analysis Results widgets.")
        if self._analyses_results_tab_create():
            self._app.debug_log.error("dataset.py: Failed to create Analysis Results tab.")

# Create the Plot tab widgets.
        height = (self._app.winWorkBook.height * 0.01) / 2.0
        width = (self._app.winWorkBook.width * 0.01) / 2.0
        self.figFigure1 = Figure(figsize=(width, height))
        self.pltPlot1 = FigureCanvas(self.figFigure1)
        self.pltPlot1.mpl_connect('button_press_event', self._expand_plot)
        self.axAxis1 = self.figFigure1.add_subplot(111)
        self.figFigure2 = Figure(figsize=(width, height))
        self.pltPlot2 = FigureCanvas(self.figFigure2)
        self.pltPlot2.mpl_connect('button_press_event', self._expand_plot)
        self.axAxis2 = self.figFigure2.add_subplot(111)
        self.figFigure3 = Figure(figsize=(width, height))
        self.pltPlot3 = FigureCanvas(self.figFigure3)
        self.pltPlot3.mpl_connect('button_press_event', self._expand_plot)
        self.axAxis3 = self.figFigure3.add_subplot(111)
        self.figFigure4 = Figure(figsize=(width, height))
        self.pltPlot4 = FigureCanvas(self.figFigure4)
        self.pltPlot4.mpl_connect('button_press_event', self._expand_plot)
        self.axAxis4 = self.figFigure4.add_subplot(111)
        self.vbxPlot1 = gtk.VBox()
        self.vbxPlot2 = gtk.VBox()

        if self._plot_tab_create():
            self._app.debug_log.error("dataset.py: Failed to create Plot tab.")

# Create the analysis results breakdown widgets.
        self.fraResultsByChildAssembly = _widg.make_frame(_label_=_(u"Summary of Results By Child Assembly"))
        self.fraResultsByPart = _widg.make_frame(_label_=_(u"Summary of Results By Part"))

        self.hpnResultsBreakdown = gtk.HPaned()

        self.tvwResultsByChildAssembly = gtk.TreeView()
        self.tvwResultsByPart = gtk.TreeView()

        if self._results_breakdown_tab_create():
            self._app.debug_log.error("dataset.py: Failed to create Results Breakdown tab.")

        self.btnAssign = _widg.make_button(_width_=100, _label_="Assign",
                                           _image_=None)
        self.btnCancel = _widg.make_button(_width_=100, _label_="Cancel",
                                           _image_=None)

        self.vbxDataset = gtk.VBox()
        toolbar = self._toolbar_create()

        self.vbxDataset.pack_start(toolbar, expand=False)
        self.vbxDataset.pack_start(self.notebook)

    def _expand_plot(self, event):
        """
        Method to display a plot in it's own window.

        Keyword Arguments:
        event -- the matplotlib MouseEvent that called this method.
        """

        plot = event.canvas
        parent = plot.get_parent()

        height = int(self._app.winWorkBook.height)
        width = int(self._app.winWorkBook.width / 2.0)

        if(event.button == 3):              # Right click.
            window = gtk.Window()
            window.set_skip_pager_hint(True)
            window.set_skip_taskbar_hint(True)
            window.set_default_size(width, height)
            window.set_border_width(5)
            window.set_position(gtk.WIN_POS_NONE)
            window.set_title(_(u"RTK Plot"))

            window.connect('delete_event', self._close_plot, plot, parent)

            plot.reparent(window)

            window.show_all()

        return False

    def _close_plot(self, window, event, plot, parent):
        """ Method to close the plot.

            window -- the gtk.Window that is being destroyed.
            event  -- the gtk.gdk.Event that called this method.
            plot   -- the matplotlib FigureCanvas that was expaneded.
            parent -- the origirnal parent widget for the plot.
        """

        plot.reparent(parent)

        return False

    def _toolbar_create(self):
        """
        Method to create the toolbar for the INCIDENT Object work book.
        """

        toolbar = gtk.Toolbar()

        _pos = 0

# Add record button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        button.set_icon_widget(image)
        button.set_name('Add')
        button.connect('clicked', self._record_add)
        button.set_tooltip_text(_(u"Adds a record to the selected data set."))
        toolbar.insert(button, _pos)
        _pos += 1

# Remove record button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        button.set_icon_widget(image)
        button.set_name('Remove')
        button.connect('clicked', self._record_remove)
        button.set_tooltip_text(_(u"Removes the selected record from the data set."))
        toolbar.insert(button, _pos)
        _pos += 1

# Consolidate results.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert-assembly.png')
        button.set_icon_widget(image)
        button.set_name('Assign')
        button.connect('clicked', self._consolidate_dataset)
        button.set_tooltip_text(_(u"Consolidates the records in the selected data set."))
        toolbar.insert(button, _pos)
        _pos += 1

# Calculate button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        button.set_icon_widget(image)
        button.set_name('Calculate')
        button.connect('clicked', self._calculate)
        button.set_tooltip_text(_(u"Analyzes the selected data set."))
        toolbar.insert(button, _pos)
        _pos += 1

# Save button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        button.set_icon_widget(image)
        button.set_name('Save')
        button.connect('clicked', self._dataset_save)
        button.set_tooltip_text(_(u"Saves the selected data set records."))
        toolbar.insert(button, _pos)
        _pos += 1

# Assign results to affected assembly.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/import.png')
        button.set_icon_widget(image)
        button.set_name('Assign')
        button.connect('clicked', AssignMTBFResults, self._app)
        button.set_tooltip_text(_(u"Assigns MTBF and hazard rate results to the selected assembly."))
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.show()

        return(toolbar)

    def _analyses_input_widgets_create(self):
        """ Method to create the Analysis Input widgets. """

# Quadrant 1 (upper left) widgets.
        self.cmbAssembly.set_tooltip_text(_(u"Selects and displays the assembly associated with the dataset."))
        self.cmbAssembly.connect('changed', self._callback_combo, 1)

        self.cmbSource.set_tooltip_text(_(u"Selects and displays the source of the selected data set."))
        results = [["ALT"], [_(u"Reliability Growth")],
                   [_(u"Reliability Demonstration")], [_(u"Field")]]
        _widg.load_combo(self.cmbSource, results)
        self.cmbSource.connect('changed', self._callback_combo, 3)

        self.cmbDistribution.set_tooltip_text(_(u"Selects and displays the statistical distribution used to fit the data."))
        results = [[u"MCF"], [u"Kaplan-Meier"], [_(u"NHPP - Power Law")], [u"NHPP - Loglinear"],
                   [_(u"Exponential")], [_(u"Lognormal")], [_(u"Normal")],
                   [u"Weibull"], ["WeiBayes"]]
        _widg.load_combo(self.cmbDistribution, results)
        self.cmbDistribution.connect('changed', self._callback_combo, 4)

        self.cmbConfType.set_tooltip_text(_(u"Selects and displays the confidence bound type."))
        results = [["Lower One-Sided"], ["Upper One-Sided"], ["Two-Sided"]]
        _widg.load_combo(self.cmbConfType, results)
        self.cmbConfType.connect('changed', self._callback_combo, 6)

        self.cmbConfMethod.set_tooltip_text(_(u"Selects and displays the method for developing confidence bounds."))
        results = [["Fisher Matrix"], ["Likelihood"], ["Bootstrap"]]
        _widg.load_combo(self.cmbConfMethod, results)
        self.cmbConfMethod.connect('changed', self._callback_combo, 7)

        self.cmbFitMethod.set_tooltip_text(_(u"Selects and displays the method used to fit the data to the selected distribution."))
        results = [["MLE"], ["Rank Regression"]]
        _widg.load_combo(self.cmbFitMethod, results)
        self.cmbFitMethod.connect('changed', self._callback_combo, 8)

        self.txtDescription.set_tooltip_text(_(u"Description of the selected data set."))
        self.txtDescription.connect('focus-out-event',
                                    self._callback_entry, 'text', 2)

        self.txtConfidence.set_tooltip_text(_(u"Desired statistical confidence"))
        self.txtConfidence.connect('focus-out-event',
                                   self._callback_entry, 'float', 5)

        self.txtStartTime.set_tooltip_text(_(u"Earliest time to use for calculating reliability metrics."))
        self.txtStartTime.connect('focus-out-event',
                                  self._callback_entry, 'float', 34)

        self.txtEndTime.set_tooltip_text(_(u"Latest time to use for calculating reliability metrics."))
        self.txtEndTime.connect('focus-out-event',
                                self._callback_entry, 'float', 9)

        self.txtRelPoints.set_tooltip_text(_(u"Number of points at which to calculate reliability metrics."))
        self.txtRelPoints.connect('focus-out-event',
                                  self._callback_entry, 'int', 10)

        self.txtStartDate.set_tooltip_text(_(u"Earliest date to use for calculating reliability metrics."))
        self.txtStartDate.connect('focus-out-event',
                                  self._callback_entry, 'date', 35)
        self.txtStartDate.connect('changed', self._callback_entry, None,
                                  'date', 35)

        self.txtEndDate.set_tooltip_text(_(u"Latest date to use for calculating reliability metrics."))
        self.txtEndDate.connect('focus-out-event',
                                self._callback_entry, 'date', 36)
        self.txtEndDate.connect('changed', self._callback_entry, None,
                                'date', 36)

        self.btnStartDate.set_tooltip_text(_(u"Launches the calendar to select the start date."))
        self.btnStartDate.connect('released', _util.date_select,
                                  self.txtStartDate)

        self.btnEndDate.set_tooltip_text(_(u"Launches the calendar to select the end date."))
        self.btnEndDate.connect('released', _util.date_select,
                                self.txtEndDate)

        self.chkGroup.set_tooltip_text(_(u"When checked, the MTBF and failure intensity results will be distributed to all next-level child assemblies according to the percentage of records each assembly contributes.  This assumes failure times are exponentially distributed."))

        self.chkParts.set_tooltip_text(_(u"When checked, the MTBF and failure intensity results will be distributed to all components according to the percentage of records each component contributes.  This assumes failure times are exponentially distributed."))

# Create the Dataset treeview.
        model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_INT, gobject.TYPE_STRING)
        self.tvwDataset.set_model(model)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('visible', 1)
        cell.set_property('background', 'gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Record\nID"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        column.set_visible(1)
        self.tvwDataset.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 1)
        cell.set_property('background', 'white')
        cell.connect('edited', self._callback_entry_cell, 1, 'text')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Affected\nUnit"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=1)
        column.set_sort_column_id(1)
        self.tvwDataset.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 1)
        cell.set_property('background', 'white')
        cell.connect('edited', self._callback_entry_cell, 2, 'float')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Left"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=2)
        column.set_sort_column_id(2)
        self.tvwDataset.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 1)
        cell.set_property('background', 'white')
        cell.connect('edited', self._callback_entry_cell, 3, 'float')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Right"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=3)
        column.set_sort_column_id(3)
        self.tvwDataset.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 1)
        cell.set_property('background', 'white')
        cell.connect('edited', self._callback_entry_cell, 4, 'int')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Quantity"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=4)
        column.set_sort_column_id(4)
        self.tvwDataset.append_column(column)

        cell = gtk.CellRendererCombo()
        cellmodel = gtk.ListStore(gobject.TYPE_STRING)
        cellmodel.append([_(u"Event")])
        cellmodel.append([_(u"Right Censored")])
        cellmodel.append([_(u"Left Censored")])
        cellmodel.append([_(u"Interval Censored")])
        cell.set_property('editable', True)
        cell.set_property('has-entry', False)
        cell.set_property('model', cellmodel)
        cell.set_property('text-column', 0)
        cell.connect('changed', self._callback_combo_cell, 5, model)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Status"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=5)
        column.set_visible(1)
        self.tvwDataset.append_column(column)

        return False

    def _analyses_input_tab_create(self):
        """
        Method to create the Analysis Input gtk.Notebook tab and populate it
        with the appropriate widgets for the DATASET object.
        """

        hbox = gtk.HBox()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add(self.tvwDataset)

        frame = _widg.make_frame(_label_=_(u"Dataset"))
        frame.add(scrollwindow)

        hbox.pack_start(frame, True, True)

# Populate tab.
        vpaned = gtk.VPaned()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add(self.tvwNevadaChart)

        self.fraNevadaChart.add(scrollwindow)

        vpaned.pack1(self.fraNevadaChart)

        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_(u"Analyses Inputs"))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(fixed)

        y_pos = 5

        label = _widg.make_label(self._ai_tab_labels[0], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbAssembly, 205, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ai_tab_labels[1], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtDescription, 205, y_pos)
        y_pos += 30

        label = _widg.make_label(self._ai_tab_labels[2], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbSource, 205, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ai_tab_labels[3], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbDistribution, 205, y_pos)
        y_pos += 35

        fixed.put(self.lblFitMethod, 5, y_pos)
        fixed.put(self.cmbFitMethod, 205, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ai_tab_labels[5], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtConfidence, 205, y_pos)
        y_pos += 30

        label = _widg.make_label(self._ai_tab_labels[6], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbConfType, 205, y_pos)
        y_pos += 35

        fixed.put(self.lblConfMethod, 5, y_pos)
        fixed.put(self.cmbConfMethod, 205, y_pos)

        y_pos = 5

        label = _widg.make_label(self._ai_tab_labels[8], 200, 25)
        fixed.put(label, 420, y_pos)
        fixed.put(self.txtStartTime, 725, y_pos)
        y_pos += 30

        label = _widg.make_label(self._ai_tab_labels[9], 200, 25)
        fixed.put(label, 420, y_pos)
        fixed.put(self.txtEndTime, 725, y_pos)
        y_pos += 30

        label = _widg.make_label(self._ai_tab_labels[10], 200, 25)
        fixed.put(label, 420, y_pos)
        fixed.put(self.txtRelPoints, 725, y_pos)
        y_pos += 30

        label = _widg.make_label(self._ai_tab_labels[11], 200, 25)
        fixed.put(label, 420, y_pos)
        fixed.put(self.txtStartDate, 725, y_pos)
        fixed.put(self.btnStartDate, 830, y_pos)
        y_pos += 30

        label = _widg.make_label(self._ai_tab_labels[12], 200, 25)
        fixed.put(label, 420, y_pos)
        fixed.put(self.txtEndDate, 725, y_pos)
        fixed.put(self.btnEndDate, 830, y_pos)
        y_pos += 30

        fixed.put(self.chkGroup, 420, y_pos)
        y_pos += 30

        fixed.put(self.chkParts, 420, y_pos)

        fixed.show_all()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(frame)

        vpaned.pack2(scrollwindow)

        hbox.pack_start(vpaned, True, True)

        self.chkGroup.hide()
        self.chkParts.hide()

# Insert the tab.
        label = gtk.Label()
        _heading = _(u"Analysis\nInputs")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Displays analysis inputs for the selected dataset."))

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
        if(_index_ == 1 or _index_ == 2 or _index_ == 3):
            self.chkGroup.show()
            self.chkParts.show()
        else:
            self.chkGroup.hide()
            self.chkParts.hide()

        self.cmbSource.set_active(self.model.get_value(self.selected_row, 3))
        self.cmbDistribution.set_active(
            self.model.get_value(self.selected_row, 4))
        self.cmbConfType.set_active(self.model.get_value(self.selected_row, 6))
        self.cmbConfMethod.set_active(
            self.model.get_value(self.selected_row, 7))
        self.cmbFitMethod.set_active(
            self.model.get_value(self.selected_row, 8))

        self.txtDescription.set_text(
            str(self.model.get_value(self.selected_row, 2)))
        self.txtConfidence.set_text(
            str(self.model.get_value(self.selected_row, 5)))
        self.txtEndTime.set_text(
            str(self.model.get_value(self.selected_row, 9)))
        self.txtRelPoints.set_text(
            str(self.model.get_value(self.selected_row, 10)))
        self.txtStartTime.set_text(
            str(self.model.get_value(self.selected_row, 34)))

        _start_date_ = _util.ordinal_to_date(self.model.get_value(self.selected_row, 35))
        _end_date_ = _util.ordinal_to_date(self.model.get_value(self.selected_row, 36))
        self.txtStartDate.set_text(str(_start_date_))
        self.txtEndDate.set_text(str(_end_date_))

        self._nevada_chart_ = self.model.get_value(self.selected_row, 37)

        self._load_dataset_tree()

        if(self._nevada_chart_ != 0):
            self._load_nevada_chart()

        return False

    def _load_dataset_tree(self):
        """ Method used to load the survival dataset in the gtk.TreeView. """

# Load the gtk.TreeView containing the list of failure/censoring times.
        query = "SELECT fld_record_id, fld_unit, fld_left_interval, \
                        fld_right_interval, fld_quantity, fld_status \
                 FROM tbl_survival_data \
                 WHERE fld_dataset_id=%s \
                 ORDER BY fld_unit ASC, \
                          fld_left_interval ASC" % self.dataset_id
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

        if not results:
            return True

        n_events = len(results)

        model = self.tvwDataset.get_model()
        model.clear()

        for i in range(n_events):
            _data_ = [results[i][0], results[i][1], results[i][2],
                      results[i][3], results[i][4], results[i][5]]
            model.append(_data_)

        return False

    def _load_nevada_chart(self):
        """
        Method to load the Nevada chart if one is associated with the selevcted
        dataset.
        """

        import pango
        from datetime import date, datetime

        _nevada_ = {}

        _query_ = "SELECT DISTINCT(fld_ship_date), fld_number_shipped \
                   FROM tbl_nevada_chart \
                   WHERE fld_dataset_id=%d \
                   ORDER BY fld_ship_date" % self.dataset_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        _query_ = "SELECT fld_ship_date, fld_return_date, fld_number_returned \
                   FROM tbl_nevada_chart \
                   WHERE fld_dataset_id=%d \
                   ORDER BY fld_ship_date, fld_return_date" % self.dataset_id
        _returns_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if not _results_ or not _returns_:
            return True

        _n_periods_ = len(_results_)
        _n_returns_ = len(_returns_)

# Create a dictionary with the following:
#
#     Key -- shipment date (month-year).
#   Value -- list with each position containing:
#       0 = the number of units shipped.
#       1 = dictionary of returned units where the key is the return date and
#           the value is the number of units returned.
#
#   {u'Jan-08': [32, {u'Mar-08': 0, u'Feb-08': 0}]}
#
# Create a list of GObject types to use for creating the gtkListStore() used
# to display the Nevada chart.
        _gobject_types_ = [gobject.TYPE_STRING, gobject.TYPE_STRING,
                           gobject.TYPE_INT, gobject.TYPE_STRING]
        for i in range(_n_periods_):
            _date_ship_ = datetime.strftime(
                          date.fromordinal(_results_[i][0]), '%b-%y')
            _nevada_[_date_ship_] = [_results_[i][1], {}]

        _n_cols_ = 2
        _headings_ = [_(u"Ship Date"), _(u"Number\nShipped")]
        for i in range(_n_returns_):
            _date_ship_ = datetime.strftime(
                          date.fromordinal(_returns_[i][0]), '%b-%y')
            _date_return_ = datetime.strftime(
                            date.fromordinal(_returns_[i][1]), '%b-%y')
            _nevada_[_date_ship_][1][_date_return_] = _returns_[i][2]
            _n_cols_ = max(_n_cols_, len(_nevada_[_date_ship_][1]) + 2)
            if(_date_return_ not in _headings_):
                _headings_.append(_date_return_)
                _gobject_types_.append(gobject.TYPE_INT)
                _gobject_types_.append(gobject.TYPE_STRING)

# Create the gtk.ListStore() and columns for the Nevada chart gtk.TreeView().
        j = 0
        model = gtk.ListStore(*_gobject_types_)
        for i in range(_n_cols_):
            cell = gtk.CellRendererText()       # Value to be displayed.
            cell.set_property('editable', 0)
            cell.set_property('wrap-width', 250)
            cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            cell.set_property('xalign', 0.5)
            cell.set_property('yalign', 0.1)

            column = gtk.TreeViewColumn("")
            label = gtk.Label(column.get_title())
            label.set_line_wrap(True)
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.set_markup("<span weight='bold'>" + _headings_[i] + "</span>")
            label.set_use_markup(True)
            label.show_all()
            column.set_widget(label)
            column.pack_start(cell, True)
            column.set_attributes(cell, text=j, background=j+1)
            column.set_resizable(True)
            column.set_alignment(0.5)

            cell = gtk.CellRendererText()       # Cell background color.
            cell.set_property('visible', False)
            column.pack_start(cell, True)
            column.set_attributes(cell, text=j+1)

            self.tvwNevadaChart.append_column(column)

            j += 2

        self.tvwNevadaChart.set_model(model)

# Load the Nevada chart gtk.ListStore() with the data.
        _date_ship_ = _nevada_.keys()
        _date_return_ = _headings_[2:]
        for i in range(len(_date_ship_)):
            _returns_ = _nevada_[_date_ship_[i]][1].keys()
            _data_ = [_date_ship_[i], 'light gray',
                      _nevada_[_date_ship_[i]][0], 'light gray']
            for j in range(len(_date_return_)):
                if(_date_return_[j] not in _returns_):
                    _data_.append(0)
                    _data_.append('light gray')
                else:
                    _data_.append(_nevada_[_date_ship_[i]][1][_date_return_[j]])
                    _data_.append('#FFFFFF')
            model.append(_data_)

        return False

    def _load_nonparametric_tree(self, _model_, _data_, _index_, _col_headings_):
        """"
        Method to load the gtk.TreeView with the results of non-parametric
        analyses.  This includes the MCF, Kaplan-Meier, and NHPP - Power Law
        analyses.

        Keyword Arguments:
        _model_
        _data_
        _index_
        _col_headings_
        """

# Remove the existing model from the gtk.TreeView.
        self.tvwNonParResults.set_model(None)

# Remove all the existing columns from the gtk.TreeView.
        _col_ = self.tvwNonParResults.get_columns()
        for i in range(len(_col_)):
            self.tvwNonParResults.remove_column(_col_[i])

# Load the model with the data.
        for i in range(len(_data_)):
            _lineitem_ = []
            for j in range(len(_index_)):
                _lineitem_.append(_data_[i][_index_[j]])

            _model_.append(_lineitem_)

# Add columns to display the data.
        for i in range(len(_col_headings_)):
            cell = gtk.CellRendererText()
            cell.set_property('editable', 0)
            cell.set_property('background', 'light gray')
            column = gtk.TreeViewColumn()
            label = _widg.make_column_heading(_col_headings_[i])
            column.set_widget(label)
            column.pack_start(cell, True)
            column.set_attributes(cell, text=i)
            self.tvwNonParResults.append_column(column)

        self.tvwNonParResults.set_model(_model_)

        return False

    def _analyses_results_widgets_create(self):
        """ Method for creating DATASET Class analysis results widgets. """

        self.fraSummary.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.fraNonParEst.set_shadow_type(gtk.SHADOW_NONE)
        self.fraNonParStats.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.fraParEst.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.fraVarCov.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.fraParGOF.set_shadow_type(gtk.SHADOW_ETCHED_IN)

        self.tvwDataset.set_rubber_banding(True)
        selection = self.tvwDataset.get_selection()
        selection.set_mode(gtk.SELECTION_MULTIPLE)

        self.lblScale.set_use_markup(True)
        self.lblShape.set_use_markup(True)
        self.lblLocation.set_use_markup(True)
        self.lblMHBResult.set_use_markup(True)
        self.lblZLPResult.set_use_markup(True)
        self.lblZLRResult.set_use_markup(True)
        self.lblRhoResult.set_use_markup(True)

        self.txtMHB.set_tooltip_markup(_(u"Displays the value of the MIL-HDBK test for trend."))
        self.txtChiSq.set_tooltip_markup(_(u"Displays the chi square critical value for the MIL-HDBK test for trend."))
        self.txtMHBPValue.set_tooltip_markup(_(u"Displays the p-value for the MIL-HDBK test for trend."))
        self.txtLP.set_tooltip_markup(_(u"Displays the value of the LaPlace test for trend."))
        self.txtZLPNorm.set_tooltip_markup(_(u"Displays the standard normal critical value for the LaPlace test for trend."))
        self.txtZLPPValue.set_tooltip_markup(_(u"Displays the p-value for the Laplace test for trend."))
        self.txtLR.set_tooltip_markup(_(u"Displays the value of the Lewis-Robinson test for trend."))
        self.txtZLRNorm.set_tooltip_markup(_(u"Displays the standard normal critical value for the Lewis-Robinson test for trend."))
        self.txtZLRPValue.set_tooltip_markup(_(u"Displays the p-value for the Lewis-Robinson test for trend."))
        self.txtRho.set_tooltip_markup(_(u"Displays the value of the lag 1 sample serial correlation coefficient."))
        self.txtRhoNorm.set_tooltip_markup(_(u"Displays the standard normal critical value for the lag 1 sample serial correlation coefficient."))
        self.txtRhoPValue.set_tooltip_markup(_(u"Displays the p-value for the lag 1 sample serial correlation coefficient."))
        self.txtScale.set_tooltip_markup(_(u"Displays the point estimate of the scale parameter."))
        self.txtScaleLL.set_tooltip_markup(_(u"Displays the lower <span>\u03B1</span>% bound on the scale parameter."))
        self.txtScaleUL.set_tooltip_markup(_(u"Displays the upper <span>\u03B1</span>% bound on the scale parameter."))
        self.txtShape.set_tooltip_markup(_(u"Displays the point estimate of the shape parameter."))
        self.txtShapeLL.set_tooltip_markup(_(u"Displays the lower <span>\u03B1</span>% bound on the shape parameter."))
        self.txtShapeUL.set_tooltip_markup(_(u"Displays the upper <span>\u03B1</span>% bound on the shape parameter."))
        self.txtLocation.set_tooltip_markup(_(u"Displays the point estimate of the location parameter."))
        self.txtLocationLL.set_tooltip_markup(_(u"Displays the lower <span>\u03B1</span>% bound on the location parameter."))
        self.txtLocationUL.set_tooltip_markup(_(u"Displays the upper <span>\u03B1</span>% bound on the location parameter."))
        self.txtShapeShape.set_tooltip_markup(_(u"Dispalys the variance of the shape parameter."))
        self.txtShapeScale.set_tooltip_markup(_(u"Displays the covariance of the shape and scale parameters."))
        self.txtShapeLocation.set_tooltip_markup(_(u"Displays the covariance of the shape and location parameters."))
        self.txtScaleShape.set_tooltip_markup(_(u"Displays the covariance of the scale and shape parameters."))
        self.txtScaleScale.set_tooltip_markup(_(u"Displays the variance of the scale parameter."))
        self.txtScaleLocation.set_tooltip_markup(_(u"Displays the covariance of the scale and location parameters."))
        self.txtLocationShape.set_tooltip_markup(_(u"Displays the covariance of the location and shape parameters."))
        self.txtLocationScale.set_tooltip_markup(_(u"Displays the covariance of the location and scale parameters."))
        self.txtLocationLocation.set_tooltip_markup(_(u"Displays the variance of the location parameter."))
        self.txtAIC.set_tooltip_markup(_(u"Displays the value of Aikike's information criterion."))
        self.txtBIC.set_tooltip_markup(_(u"Displays the value of Bayes' information criterion."))
        self.txtMLE.set_tooltip_markup(_(u"Displays the likelihood value."))
        self.txtNumSuspensions.set_tooltip_markup(_(u"Displays the number of suspensions in the data set."))
        self.txtNumFailures.set_tooltip_markup(_(u"Displays the number of failures in the dat set."))
        self.txtMTBF.set_tooltip_markup(_(u"Displays the point estimate of the MTBF."))
        self.txtMTBFLL.set_tooltip_markup(_(u"Displays the lower <span>\u03B1</span>% bound on the MTBF."))
        self.txtMTBFUL.set_tooltip_markup(_(u"Displays the upper <span>\u03B1</span>% bound on the MTBF."))
        self.txtHazardRate.set_tooltip_markup(_(u"Displays the point estimate of the hazard rate."))
        self.txtHazardRateLL.set_tooltip_markup(_(u"Displays the lower <span>\u03B1</span>% bound on the hazard rate."))
        self.txtHazardRateUL.set_tooltip_markup(_(u"Displays the upper <span>\u03B1</span>% bound on the hazard rate."))

        self.txtMTBFi.set_tooltip_markup(_(u"Displays the point estimate of the instantaneous MTBF."))
        self.txtMTBFiLL.set_tooltip_markup(_(u"Displays the lower <span>\u03B1</span>% bound on the instantaneous MTBF."))
        self.txtMTBFiUL.set_tooltip_markup(_(u"Displays the upper <span>\u03B1</span>% bound on the instantaneous MTBF."))
        self.txtHazardRatei.set_tooltip_markup(_(u"Displays the point estimate the instantaneous failure intensity."))
        self.txtHazardRateiLL.set_tooltip_markup(_(u"Displays the lower <span>\u03B1</span>% bound on the instantaneous failure intensity."))
        self.txtHazardRateiUL.set_tooltip_markup(_(u"Displays the upper <span>\u03B1</span>% bound on the instantaneous failure intensity."))

        return False

    def _analyses_results_tab_create(self):
        """
        Method to create the Analysis Input gtk.Notebook tab and populate it
        with the appropriate widgets for the DATASET object.
        """

# Summary of results.
        fixed = gtk.Fixed()
        self.fraSummary.add(fixed)

        y_pos = 5
        label = _widg.make_label(_(u"Number of Suspensions:"), width=200)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtNumSuspensions, 210, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"Number of Failures:"), width=200)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtNumFailures, 210, y_pos)
        y_pos += 40

        fixed.put(self.lblCumMTBF, 210, y_pos)
        fixed.put(self.lblCumFI, 340, y_pos)
        fixed.put(self.lblMTBFi, 470, y_pos)
        fixed.put(self.lblFIi, 600, y_pos)
        y_pos += 55

        label = _widg.make_label(_(u"Lower Bound"), width=150)
        fixed.put(label, 10, y_pos)
        fixed.put(self.txtMTBFLL, 210, y_pos)
        fixed.put(self.txtHazardRateLL, 340, y_pos)
        fixed.put(self.txtMTBFiLL, 470, y_pos)
        fixed.put(self.txtHazardRateiLL, 600, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"Point Estimate"), width=150)
        fixed.put(label, 10, y_pos)
        fixed.put(self.txtMTBF, 210, y_pos)
        fixed.put(self.txtHazardRate, 340, y_pos)
        fixed.put(self.txtMTBFi, 470, y_pos)
        fixed.put(self.txtHazardRatei, 600, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"Upper Bound"), width=150)
        fixed.put(label, 10, y_pos)
        fixed.put(self.txtMTBFUL, 210, y_pos)
        fixed.put(self.txtHazardRateUL, 340, y_pos)
        fixed.put(self.txtMTBFiUL, 470, y_pos)
        fixed.put(self.txtHazardRateiUL, 600, y_pos)
        y_pos += 30

        self.txtMTBFiLL.hide()
        self.txtHazardRateiLL.hide()
        self.txtMTBFi.hide()
        self.txtHazardRatei.hide()
        self.txtMTBFiUL.hide()
        self.txtHazardRateiUL.hide()

# Non-parametric table of results.
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add(self.tvwNonParResults)

        self.fraNonParEst.add(scrollwindow)

# Non-parametric statistics.
        fixed = gtk.Fixed()
        self.fraNonParStats.add(fixed)

        y_pos = 5
        label = _widg.make_label(_(u"MIL\nHandbook"), height=50, width=100)
        fixed.put(label, 210, y_pos)

        label = _widg.make_label(_(u"Laplace"), height=50, width=100)
        fixed.put(label, 315, y_pos)

        label = _widg.make_label(_(u"Lewis\nRobinson"), height=50, width=100)
        fixed.put(label, 420, y_pos)

        label = _widg.make_label(_(u"Serial\nCorrelation\nCoefficient"), height=50, width=100)
        fixed.put(label, 525, y_pos)
        y_pos += 55

        label = _widg.make_label(_(u"Test Statistic"), width=150)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtMHB, 210, y_pos)
        fixed.put(self.txtLP, 315, y_pos)
        fixed.put(self.txtLR, 420, y_pos)
        fixed.put(self.txtRho, 525, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"Critical Value"), width=150)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtChiSq, 210, y_pos)
        fixed.put(self.txtZLPNorm, 315, y_pos)
        fixed.put(self.txtZLRNorm, 420, y_pos)
        fixed.put(self.txtRhoNorm, 525, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"p-Value"), width=150)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtMHBPValue, 210, y_pos)
        fixed.put(self.txtZLPPValue, 315, y_pos)
        fixed.put(self.txtZLRPValue, 420, y_pos)
        fixed.put(self.txtRhoPValue, 525, y_pos)
        y_pos += 30

        fixed.put(self.lblMHBResult, 210, y_pos)
        fixed.put(self.lblZLPResult, 315, y_pos)
        fixed.put(self.lblZLRResult, 420, y_pos)
        fixed.put(self.lblRhoResult, 525, y_pos)

# Parametric estimates.
        fixed = gtk.Fixed()
        self.fraParEst.add(fixed)

        y_pos = 5
        fixed.put(self.lblScale, 155, y_pos)
        fixed.put(self.lblShape, 305, y_pos)
        fixed.put(self.lblLocation, 455, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"Lower Bound"), width=150)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtScaleLL, 155, y_pos)
        fixed.put(self.txtShapeLL, 305, y_pos)
        fixed.put(self.txtLocationLL, 455, y_pos)
        y_pos += 25

        label = _widg.make_label(_(u"Point Estimate"), width=150)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtScale, 155, y_pos)
        fixed.put(self.txtShape, 305, y_pos)
        fixed.put(self.txtLocation, 455, y_pos)
        fixed.put(self.lblModel, 605, y_pos)
        y_pos += 25

        label = _widg.make_label(_(u"Upper Bound"), width=150)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtScaleUL, 155, y_pos)
        fixed.put(self.txtShapeUL, 305, y_pos)
        fixed.put(self.txtLocationUL, 455, y_pos)

# Variance-Covariance matrix.
        fixed = gtk.Fixed()
        self.fraVarCov.add(fixed)

        y_pos = 5
        fixed.put(self.lblRowScale, 155, y_pos)
        fixed.put(self.lblRowShape, 305, y_pos)
        fixed.put(self.lblRowLocation, 455, y_pos)
        y_pos += 30

        fixed.put(self.lblColScale, 5, y_pos)
        fixed.put(self.txtScaleScale, 155, y_pos)
        fixed.put(self.txtScaleShape, 305, y_pos)
        fixed.put(self.txtScaleLocation, 455, y_pos)
        y_pos += 25

        fixed.put(self.lblColShape, 5, y_pos)
        fixed.put(self.txtShapeScale, 155, y_pos)
        fixed.put(self.txtShapeShape, 305, y_pos)
        fixed.put(self.txtShapeLocation, 455, y_pos)
        y_pos += 25

        fixed.put(self.lblColLocation, 5, y_pos)
        fixed.put(self.txtLocationScale, 155, y_pos)
        fixed.put(self.txtLocationShape, 305, y_pos)
        fixed.put(self.txtLocationLocation, 455, y_pos)

# Parametric goodness of fit statistics.
        fixed = gtk.Fixed()
        self.fraParGOF.add(fixed)

        y_pos = 5
        label = _widg.make_label("AIC", width=150)
        fixed.put(label, 155, y_pos)
        label = _widg.make_label("BIC", width=150)
        fixed.put(label, 305, y_pos)
        label = _widg.make_label("MLE", width=150)
        fixed.put(label, 455, y_pos)
        y_pos += 30

        fixed.put(self.txtAIC, 155, y_pos)
        fixed.put(self.txtBIC, 305, y_pos)
        fixed.put(self.txtMLE, 455, y_pos)

# Insert the tab.
        label = gtk.Label()
        _heading = _(u"Analysis\nResults")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Displays analysis results for the selected dataset."))
        self.notebook.insert_page(self.hpnAnalysisResults,
                                  tab_label=label,
                                  position=-1)

        return False

    def _analyses_results_tab_load(self):
        """
        Loads the widgets with analyses results for the DATASET Object.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

# Get the distribtion ID.
        _analysis_ = self.cmbDistribution.get_active()

# Clear the tab.
        for child in self.hpnAnalysisResults.get_children():
            self.hpnAnalysisResults.remove(child)
        for child in self.vbxAnalysisResults1.get_children():
            self.vbxAnalysisResults1.remove(child)
        for child in self.vbxAnalysisResults2.get_children():
            self.vbxAnalysisResults2.remove(child)

        self.lblMTBFi.hide()
        self.lblFIi.hide()
        self.lblRhoResult.hide()
        self.txtMTBFiLL.hide()
        self.txtHazardRateiLL.hide()
        self.txtMTBFi.hide()
        self.txtHazardRatei.hide()
        self.txtMTBFiUL.hide()
        self.txtHazardRateiUL.hide()
        self.txtRho.hide()
        self.txtRhoNorm.hide()
        self.txtRhoPValue.hide()

# Update summary information.  This is always shown regardless of the type of
# analysis performed.
        self.vbxAnalysisResults1.pack_start(self.fraSummary, True, True)
        self.txtNumSuspensions.set_text(
            str(self.model.get_value(self.selected_row, 11)))
        self.txtNumFailures.set_text(
            str(self.model.get_value(self.selected_row, 12)))

# Update mean cumulative function information.
        if(_analysis_ == 1):
            self.hpnAnalysisResults.pack1(self.vbxAnalysisResults1, True, True)
            self.hpnAnalysisResults.pack2(self.fraNonParEst, True, True)
            self.vbxAnalysisResults1.pack_start(self.fraNonParStats, True, True)
            self.txtMHB.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 28))))
            self.txtLP.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 29))))
            self.txtLR.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 30))))

            self.lblCumMTBF.set_markup(_(u"<span>MTBF</span>"))
            self.lblCumFI.set_markup(_(u"<span>Failure\nIntensity</span>"))

            self.lblRhoResult.show()
            self.txtRho.show()
            self.txtRhoNorm.show()
            self.txtRhoPValue.show()

# Update Kaplan-Meier analysis information.
        elif(_analysis_ == 2):
            self.hpnAnalysisResults.pack1(self.vbxAnalysisResults1, True, True)
            self.hpnAnalysisResults.pack2(self.fraNonParEst, True, True)

            self.lblCumMTBF.set_markup(_(u"<span>MTBF</span>"))
            self.lblCumFI.set_markup(_(u"<span>Failure\nIntensity</span>"))

# Update NHPP Power Law analysis information.
        elif(_analysis_ == 3):
            self.hpnAnalysisResults.pack1(self.vbxAnalysisResults1, True, True)
            self.hpnAnalysisResults.pack2(self.fraNonParEst, True, True)
            self.vbxAnalysisResults1.pack_start(self.fraParEst, True, True)

            _b_hat_ = str(fmt.format(self.model.get_value(self.selected_row, 13)))
            _alpha_hat_ = str(fmt.format(self.model.get_value(self.selected_row, 16)))
            self.lblModel.set_markup(_(u"<span>MTBF<sub>C</sub> = %s T<sup>%s</sup></span>") % (_b_hat_, _alpha_hat_))

            self.txtScale.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 13))))
            self.txtScaleLL.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 14))))
            self.txtScaleUL.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 15))))
            self.txtShape.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 16))))
            self.txtShapeLL.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 17))))
            self.txtShapeUL.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 18))))

            self.lblCumMTBF.set_markup(_(u"<span>Cumulative\nMTBF</span>"))
            self.lblCumFI.set_markup(_(u"<span>Cumulative\nFailure\nIntensity</span>"))
            self.lblMTBFi.set_markup(_(u"<span>Instantaneous\nMTBF</span>"))
            self.lblFIi.set_markup(_(u"<span>Instantaneous\nFailure\nIntensity</span>"))
            self.lblScale.set_markup(_(u"b"))
            self.lblShape.set_markup(_(u"\u03B1"))

            # Show widgets.
            self.chkGroup.show()
            self.chkParts.show()
            self.lblMTBFi.show()
            self.lblFIi.show()
            self.txtMTBFiLL.show()
            self.txtHazardRateiLL.show()
            self.txtMTBFi.show()
            self.txtHazardRatei.show()
            self.txtMTBFiUL.show()
            self.txtHazardRateiUL.show()

            # Hide widgets.
            self.lblLocation.hide()
            self.txtLocation.hide()
            self.txtLocationLL.hide()
            self.txtLocationUL.hide()

# Update parametric analysis information.
        else:
            self.hpnAnalysisResults.pack1(self.vbxAnalysisResults1, True, True)
            self.hpnAnalysisResults.pack1(self.vbxAnalysisResults2, True, True)
            self.vbxAnalysisResults1.pack_start(self.fraParEst, True, True)
            self.vbxAnalysisResults2.pack_start(self.fraVarCov, True, True)
            self.vbxAnalysisResults2.pack_start(self.fraParGOF, True, True)

            self.txtScale.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 13))))
            self.txtScaleLL.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 14))))
            self.txtScaleUL.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 15))))
            self.txtShape.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 16))))
            self.txtShapeLL.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 17))))
            self.txtShapeUL.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 18))))
            self.txtLocation.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 19))))
            self.txtLocationLL.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 20))))
            self.txtLocationUL.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 21))))
# Scale variance.
            self.txtScaleScale.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 22))))
# Shape variance.
            self.txtShapeShape.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 23))))
# Location variance.
            self.txtLocationLocation.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 24))))
# Shape-scale covariance.
            self.txtShapeScale.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 25))))
# Scale-shape covariance.
            self.txtScaleShape.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 25))))
# Scale-location covariance.
            self.txtScaleLocation.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 26))))
# Location-scale covariance.
            self.txtLocationScale.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 26))))
# Shape-location covariance.
            self.txtShapeLocation.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 27))))
# Location-shape covariance.
            self.txtLocationShape.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 27))))
            self.txtAIC.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 31))))
            self.txtBIC.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 32))))
            self.txtMLE.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 33))))

            self.lblScale.set_markup(_(u"<span>Scale</span>"))
            self.lblShape.set_markup(_(u"<span>Shape</span>"))
            self.lblLocation.show()

        return False

    def _plot_tab_create(self):
        """
        Method to create the survival analysis plot gtk.Notebook tab and add
        it to the gtk.Notebook at the correct location.
        """

        hbox = gtk.HBox()

        frame = _widg.make_frame(_label_=_(u"Survival Analysis Plots"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(hbox)
        frame.show_all()

        hbox.pack_start(self.vbxPlot1)

        self.vbxPlot1.pack_start(self.pltPlot1)
        self.vbxPlot1.pack_start(self.pltPlot3)

        hbox.pack_start(self.vbxPlot2)

        self.vbxPlot2.pack_start(self.pltPlot2)
        self.vbxPlot2.pack_start(self.pltPlot4)

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>Analysis\nPlots</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Displays survival analyses plots."))
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _load_plot(self, axis, plot, x, y1=None, y2=None, y3=None,
                   _title_="", _xlab_="", _ylab_="", _type_=[1, 1, 1],
                   _marker_=['g-', 'r-', 'b-']):
        """ Method to load the matplotlib plots.

            Keyword Arguments:
            axis     -- the matplotlib axis object.
            plot     -- the matplotlib plot object.
            x        -- the x values to plot.
            y1       -- the first data set y values to plot.
            y2       -- the second data set y values to plot.
            y3       -- the third data set y values to plot.
            _title_  -- the title for the plot.
            _xlab_   -- the x asis label for the plot.
            _ylab_   -- the y axis label for the plot.
            _type_   -- the type of line to plot (1=step, 2=plot, 3=histogram).
            _marker_ -- the marker to use on the plot.
        """

        from scipy.interpolate import spline

        n_points = len(x)

        axis.cla()

        axis.grid(True, which='both')

        if(y1 is not None):
            if(_type_[0] == 1):
                line, = axis.step(x, y1, _marker_[0], where='mid')
                for i in range(n_points):
                    line.set_ydata(y1)
            elif(_type_[0] == 2):
                line, = axis.plot(x, y1, _marker_[0], linewidth=2)
                for i in range(n_points):
                    line.set_ydata(y1)
            elif(_type_[0] == 3):
                axis.grid(False, which='both')
                n, bins, patches = axis.hist(x, bins=y1, color=_marker_[0])
            elif(_type_[0] == 4):
                line, = axis.plot_date(x, y1, _marker_[0],
                                       xdate=True, linewidth=2)

        if(y2 is not None):
            if(_type_[1] == 1):
                line2, = axis.step(x, y2, _marker_[1], where='mid')
                for i in range(n_points):
                    line2.set_ydata(y2)
            elif(_type_[1] == 2):
                line2, = axis.plot(x, y2, _marker_[1], linewidth=2)
                for i in range(n_points):
                    line2.set_ydata(y2)
            elif(_type_[1] == 3):
                axis.grid(False, which='both')
                n, bins, patches = axis.hist(x, bins=y2, color=_marker_[1])
                line2, = axis.plot(bins, y2)
            elif(_type_[1] == 4):
                line2, = axis.plot_date(x, y2, _marker_[1],
                                        xdate=True, linewidth=2)

        if(y3 is not None):
            if(_type_[2] == 1):
                line3, = axis.step(x, y3, _marker_[2], where='mid')
                for i in range(n_points):
                    line3.set_ydata(y3)
            elif(_type_[2] == 2):
                line3, = axis.plot(x, y3, _marker_[2], linewidth=2)
                for i in range(n_points):
                    line3.set_ydata(y3)
            elif(_type_[2] == 3):
                axis.grid(False, which='both')
                n, bins, patches = axis.hist(x, bins=y3, color=_marker_[2])
                line3, = axis.plot(bins, y3)
            elif(_type_[2] == 4):
                line3, = axis.plot_date(x, y3, _marker_[2],
                                        xdate=True, linewidth=2)

        axis.set_title(_title_)
        axis.set_xlabel(_xlab_)
        axis.set_ylabel(_ylab_)

        plot.draw()

        return False

    def _results_breakdown_tab_create(self):
        """
        Method to create gtk.Notebook() tab for displaying results broken
        down by child assembly and/or components.
        """

# Table of results allocated to each assembly.
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_STRING)
        self.tvwResultsByChildAssembly.set_model(model)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Hardware\nItem"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0, background=9)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_sort_column_id(0)
        self.tvwResultsByChildAssembly.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Number of\nFailures"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=1, background=9)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_sort_column_id(1)
        self.tvwResultsByChildAssembly.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u""))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=2, background=9)
        column.set_resizable(True)
        column.set_visible(False)
        self.tvwResultsByChildAssembly.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"MTBF\nLower Bound"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=3, background=9)
        column.set_resizable(True)
        self.tvwResultsByChildAssembly.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"MTBF"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=4, background=9)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_sort_column_id(3)
        self.tvwResultsByChildAssembly.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"MTBF\nUpper Bound"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=5, background=9)
        column.set_resizable(True)
        self.tvwResultsByChildAssembly.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Failure Intensity\nLower Bound"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=6, background=9)
        column.set_resizable(True)
        self.tvwResultsByChildAssembly.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Failure\nIntensity"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=7, background=9)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_sort_column_id(6)
        self.tvwResultsByChildAssembly.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Failure Intensity\nUpper Bound"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=8, background=9)
        column.set_resizable(True)
        self.tvwResultsByChildAssembly.append_column(column)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add(self.tvwResultsByChildAssembly)

        self.fraResultsByChildAssembly.add(scrollwindow)

        self.hpnResultsBreakdown.pack1(self.fraResultsByChildAssembly, True, True)

# Table of results allocated to each part.
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_STRING)
        self.tvwResultsByPart.set_model(model)

        self.tvwResultsByPart.columns_autosize()
        self.tvwResultsByPart.set_headers_clickable(True)
        self.tvwResultsByPart.set_reorderable(True)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Part\nNumber"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0, background=8)
        column.set_clickable(True)
        column.set_sort_column_id(0)
        self.tvwResultsByPart.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Number of\nFailures"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=1, background=8)
        column.set_clickable(True)
        column.set_sort_column_id(1)
        self.tvwResultsByPart.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"MTBF\nLower Bound"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=2, background=8)
        self.tvwResultsByPart.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"MTBF"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=3, background=8)
        column.set_clickable(True)
        column.set_sort_column_id(3)
        self.tvwResultsByPart.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"MTBF\nUpper Bound"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=4, background=8)
        self.tvwResultsByPart.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Hazard Rate\nLower Bound"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=5, background=8)
        self.tvwResultsByPart.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Hazard\nRate"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=6, background=8)
        column.set_clickable(True)
        column.set_sort_column_id(6)
        self.tvwResultsByPart.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Hazard Rate\nUpper Bound"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=7, background=8)
        self.tvwResultsByPart.append_column(column)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add(self.tvwResultsByPart)

        self.fraResultsByPart.add(scrollwindow)

        self.hpnResultsBreakdown.pack2(self.fraResultsByPart, True, True)

# Insert the tab.
        label = gtk.Label()
        _heading = _(u"Results\nBreakdowns")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Displays analysis results for the selected dataset broken down by child assembly and part number."))
        self.notebook.insert_page(self.hpnResultsBreakdown,
                                  tab_label=label,
                                  position=-1)

        return False

    def _record_add(self, button):
        """
        Method to add a record to the selected survival analysis dataset.

        Keyword Arguments:
        button -- the gtk.ToolButton that called this method.
        """

        model = self.tvwDataset.get_model()
        model.append()

# Find the assembly the dataset is associated with.
        _assembly_id = self.model.get_value(self.selected_row, 1)

# Find the maximum record ID for the selected dataset.
        _query = "SELECT MAX(fld_record_id) \
                  FROM tbl_survival_data \
                  WHERE fld_dataset_id=%d" % self.dataset_id
        _results = self._app.DB.execute_query(_query,
                                              None,
                                              self._app.ProgCnx,
                                              False)

        _values = (_results[0][0] + 1, self.dataset_id, _assembly_id)
        _query = "INSERT INTO tbl_survival_data \
                  (fld_record_id, fld_dataset_id, fld_assembly_id) \
                  VALUES (%d, %d, %d)" % _values
        _results = self._app.DB.execute_query(_query,
                                              None,
                                              self._app.ProgCnx,
                                              True)

        return False

    def _record_remove(self, button):
        """
        Method to remove the selected record from the survival analysis
        dataset.

        Keyword Arguments:
        button -- the gtk.ToolButton that called this method.
        """

        selection = self.tvwDataset.get_selection()
        (model, paths) = selection.get_selected_rows()

        _records = []
        for i in range(len(paths)):
            row = model.get_iter(paths[i])
            _records.append(model.get_value(row, 0))

        _title_ = _(u"RTK: Confirm Delete")
        _dialog = _widg.make_dialog(_title_)

        fixed = gtk.Fixed()

        y_pos = 10

        label = _widg.make_label(_(u"Are you sure you want to delete the selected survival data record(s)."), 600, 250)
        fixed.put(label, 5, y_pos)

        fixed.show_all()

        _dialog.vbox.pack_start(fixed)

        response = _dialog.run()

        if(response == gtk.RESPONSE_ACCEPT):
            for i in range(len(_records)):
                query = "DELETE FROM tbl_survival_data \
                         WHERE fld_record_id=%d" % _records[i]
                results = self._app.DB.execute_query(query,
                                                     None,
                                                     self._app.ProgCnx,
                                                     True)

        _dialog.destroy()

        self._load_dataset_tree()

        return False

    def _calculate(self, button):
        """
        Method to execute the selected analysis.

        Keyword Arguments:
        button -- the gtk.ToolButton that called this method.
        """

        from math import exp, fabs, floor, log, sqrt
        from scipy.stats import chi2, norm

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _RELTIME_ = False
        _dataset_ = self.model.get_value(self.selected_row, 0)  # Dataset ID.
        _name = self.model.get_value(self.selected_row, 2)      # Dataset name.
        _analysis_ = self.cmbDistribution.get_active()          # Distribution ID.
        _conf_ = float(self.txtConfidence.get_text())           # Confidence.
        _type_ = self.cmbConfType.get_active()                  # Confidence type.
        _fitmeth_ = self.cmbFitMethod.get_active()              # Fit method.
        _starttime_ = float(self.txtStartTime.get_text())       # Minimum time.
        _reltime_ = float(self.txtEndTime.get_text())           # Maximum time.
        _step_ = int(self.txtRelPoints.get_text())
        _startdate_ = _util.date_to_ordinal(self.txtStartDate.get_text())
        _enddate_ = _util.date_to_ordinal(self.txtEndDate.get_text())

        if(_type_ == 3):                    # Two-sided bounds.
            _conf_ = (100.0 + _conf_) / 200.0
        else:                               # One-sided bounds.
            _conf_ = _conf_ / 100.0

 # Set maximum time to some very large value if the user has not set this
 # themselves.  Keeping it at zero results in nothing being returned from the
 # SQL queries to follow.
        if(_reltime_ == 0.0):
            _reltime_ = 1000000.0
            _RELTIME_ = True

        if(_step_ == 0):
            _step_ = 1

# Determine the confidence bound z-value.
        _z_norm_ = norm.ppf(_conf_)

# Get the entire dataset.
        _query_ = "SELECT fld_unit, fld_left_interval, fld_right_interval, \
                          fld_tbf, fld_status, fld_quantity, fld_request_date \
                   FROM tbl_survival_data \
                   WHERE fld_dataset_id=%d \
                   AND fld_right_interval <= %f AND fld_right_interval > %f \
                   AND fld_request_date >= %d AND fld_request_date < %d \
                   ORDER BY fld_request_date ASC, \
                            fld_unit ASC, \
                            fld_left_interval ASC" % (_dataset_, _reltime_,
                                                      _starttime_, _startdate_,
                                                      _enddate_)
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        censdata = []
        for i in range(len(_results_)):
            censdata.append([_results_[i][1], _results_[i][2]])

# Initialize variables.
        n_suspensions = 0
        n_failures = 0
        MTBF = 0.0
        MTBFLL = 0.0
        MTBFUL = 0.0
        scale = 0.0
        scalell = 0.0
        scaleul = 0.0
        shape = 0.0
        shapell = 0.0
        shapeul = 0.0
        location = 0.0
        locationll = 0.0
        locationul = 0.0
        shapeshape = 0.0
        shapescale = 0.0
        shapelocation = 0.0
        scaleshape = 0.0
        scalescale = 0.0
        scalelocation = 0.0
        locationlocation = 0.0
        mhb = 0.0
        zlp = 0.0
        zlr = 0.0
        mle = 0.0
        aic = 0.0
        bic = 0.0

# Initialize some lists.
        p_value = [1.0, 1.0, 1.0, 1.0]
        _text = [u"", u"", u""]

# =========================================================================== #
# Perform Nelson's mean cumulative function analysis.
# =========================================================================== #
        if(_analysis_ == 1):                # MCF
# Create a list of unique units.
            _query_ = "SELECT DISTINCT(fld_unit) \
                       FROM tbl_survival_data \
                       WHERE fld_dataset_id=%d \
                       AND fld_right_interval <= %f \
                       AND fld_right_interval > %f" % \
                       (_dataset_, _reltime_, _starttime_)
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

            _units_ = []
            for i in range(len(_results_)):
                _units_.append(_results_[i][0])

# Create a list of unique failure times.
            _query_ = "SELECT DISTINCT(fld_right_interval) \
                       FROM tbl_survival_data \
                       WHERE fld_dataset_id=%d \
                       AND fld_right_interval >= %f \
                       AND fld_right_interval <= %f \
                       ORDER BY fld_right_interval ASC" % \
                       (_dataset_, _starttime_, _reltime_)
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

            _times_ = []
            for i in range(len(_results_)):
                _times_.append(_results_[i][0])

# Get the entire dataset.
# Example of a record returned from the following query:
#     (u'HT36103', 0.0, 12.0, 12.0)
            _query_ = "SELECT fld_unit, fld_left_interval, \
                              fld_right_interval, fld_tbf, fld_quantity \
                       FROM tbl_survival_data \
                       WHERE fld_dataset_id=%d \
                       AND fld_right_interval >= %f \
                       AND fld_right_interval <= %f \
                       ORDER BY fld_unit ASC, \
                                fld_left_interval ASC" % \
                       (_dataset_, _starttime_, _reltime_)
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

# =========================================================================== #
#  0 = Event Time ti. (string)
#  1 = Delta array at time ti. (array of integers)
#  2 = d array at time ti. (array of integers)
#  3 = Sum of delta at time ti. (integer)
#  4 = Sum of d at time ti. (integer)
#  5 = d bar at time ti. (float)
#  6 = Variance of MCF at time ti. (float)
#  7 = Lower bound on mean cumulative function at time ti. (float)
#  8 = Upper bound on mean cumulative fucntion at time ti. (float)
#  9 = Mean cumulative function at time ti. (float)
# 10 = Cumulative MTBF at time ti. (float)
# 11 = Lower bound on cumulative MTBF at time ti. (float)
# 12 = Upper bound on cumulative MTBF at time ti. (float)
# 13 = Instantaneous MTBF at time ti. (float)
# 14 = Lower bound on instantaneous MTBF at time ti. (float)
# 15 = Upper bound on instantaneous MTBF at time ti. (float)
# =========================================================================== #
            _nonpar_ = mean_cumulative_function(_units_, _times_,
                                                _results_, _conf_)

# Load the non-parametric results gtk.TreeView
            _model_ = gtk.ListStore(gobject.TYPE_FLOAT, gobject.TYPE_INT,
                                    gobject.TYPE_INT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
            _index_ = [0, 3, 4, 5, 6, 7, 9, 8, 11, 10, 12, 14, 13, 15]
            _col_headings_ = [_(u"Event\nTime"),
                              _(u"\u03B4."), _(u"d."), _(u"d bar"),
                              _(u"\u03C3<sup>2</sup><sub>MCF</sub>"),
                              _(u"MCF Lower\nBound"), _(u"MCF"),
                              _(u"MCF Upper\nBound"),
                              _(u"Cumulative MTBF\nLower Bound"),
                              _(u"Cumulative\nMTBF"),
                              _(u"Cumulative\nMTBF\nUpper Bound"),
                              _(u"Instantaneous\nMTBF\nLower Bound"),
                              _(u"Instantaneous\nMTBF"),
                              _(u"Instantaneous\nMTBF\nUpper Bound")]
            self._load_nonparametric_tree(_model_, _nonpar_,
                                          _index_, _col_headings_)
# Get:
#   Total number of failures.
#   List of unique failures times.
#   List of MCF at each unique failure time.
#   List of MCF lower bound at each unique failure time.
#   List of MCF upper bound at each unique failure time.
#   Maximum observed time.
            _n_records_ = len(_nonpar_)
            _failures_ = [x[4] for x in _nonpar_]
            n_failures = int(sum(_failures_))
            times = [x[0] for x in _nonpar_]
            muhat = [x[9] for x in _nonpar_]
            muhatll = [x[7] for x in _nonpar_]
            muhatul = [x[8] for x in _nonpar_]
            ta = max(times)

# Calculate the MIL-HDBK-189, Laplace, and Lewis-Robinson test statistics.
# Find the chi-square critical value.  These statistics are used to test for
# HPP vs. NHPP in the data.
            _query_ = "SELECT t1.fld_unit, t2.fld_tbf, t1.fld_request_date \
                       FROM tbl_incident AS t1 \
                       INNER JOIN tbl_survival_data AS t2 \
                       WHERE t2.fld_record_id=t1.fld_incident_id \
                       AND t2.fld_dataset_id=%d \
                       AND t2.fld_right_interval >= %f \
                       AND t2.fld_right_interval <= %f \
                       AND t1.fld_request_date >= %d \
                       AND t1.fld_request_date < %d \
                       ORDER BY t1.fld_request_date ASC" % \
                       (_dataset_, _starttime_, _reltime_, _startdate_,
                        _enddate_)
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

            _tbf_ = []
            _failnum_ = []
            _dates_ = []
            _denominator_ = 0.0
            for i in range(_n_records_):
                mhb += log(times[i] / ta)
                _denominator_ += log(ta / times[i])
                zlp += times[i] / ta
                _tbf_.append(_results_[i][1])
                _failnum_.append(i)
                _dates_.append(_results_[i][2])

            mhb = -2.0 * mhb
            zlp = (zlp - (n_failures / 2.0)) / sqrt(n_failures / 12.0)
            tau = numpy.mean(_tbf_)
            S = numpy.std(_tbf_)
            zlr = zlp * tau / S

            _chisq_ = chi2.ppf(1.0 - _conf_, 2 * n_failures)

            _beta_ = n_failures / _denominator_
            _eta_ = ta / n_failures**(1.0 / _beta_)

# Calculate the sample serial correlation coefficient.
            _cov_ = 0.0
            _var1_ = 0.0
            _var2_ = 0.0
            _tau_bar_ = numpy.mean(_tbf_)
            for i in range(len(_tbf_) - 1):
                _cov_ += (_tbf_[i] - _tau_bar_) * (_tbf_[i + 1] - _tau_bar_)
                _var1_ += (_tbf_[i] - _tau_bar_)**2.0
                _var2_ += (_tbf_[i + 1] - _tau_bar_)**2.0
            _rho_ = sqrt(n_failures - 1) * (_cov_ / sqrt(_var1_ * _var2_))

            p_value[0] = chi2.cdf(mhb, 2 * n_failures)
            p_value[1] = norm.cdf(abs(zlp))
            p_value[2] = norm.cdf(abs(zlr))
            p_value[3] = norm.cdf(_rho_)

# Plot the mean cumulative function with confidence bounds.
            _widg.load_plot(self.axAxis1, self.pltPlot1, x=times,
                            y1=muhat, y2=muhatll, y3=muhatul,
                            _title_=_(u"MCF Plot of %s") % _name,
                            _xlab_=_(u"Time"),
                            _ylab_=_(u"Mean Cumulative Function [mu(t)]"),
                            _marker_=['g-', 'r-', 'b-'])
            _text_ = (u"MCF", u"MCF LCL", u"MCF UCL")
            _widg.create_legend(self.axAxis1, _text_, _fontsize_='medium',
                                _frameon_=True, _location_='lower right',
                                _shadow_=True)

            for plot in self.vbxPlot1.get_children():
                self.vbxPlot1.remove(plot)

            self.vbxPlot1.pack_start(self.pltPlot1)

# Plot the run sequence plot.
            _widg.load_plot(self.axAxis2, self.pltPlot2,
                            x=_dates_, y1=_tbf_,
                            _title_=_(u"Run Sequence Plot of %s") % _name,
                            _xlab_=_(u"Date"),
                            _ylab_=_(u"Time Between Failure"),
                            _type_=[4], _marker_=['g-'])

# Create a lag plot.
            _zero_line_ = []
            for i in range(len(_tbf_) - 1):
                _zero_line_.append(_tbf_[i])

            _widg.load_plot(self.axAxis4, self.pltPlot4,
                            x=_tbf_[0:len(_tbf_)-1], y1=_tbf_[1:len(_tbf_)],
                            y2=_zero_line_,
                            _title_=_(u"Lag Plot of %s") % _name,
                            _xlab_=_(u"Lagged Time Between Failure"),
                            _ylab_=_(u"Time Between Failure"),
                            _type_=[2, 2], _marker_=['go', 'k-'])

            for plot in self.vbxPlot2.get_children():
                self.vbxPlot2.remove(plot)

            self.vbxPlot2.pack_start(self.pltPlot2)
            self.vbxPlot2.pack_start(self.pltPlot4)

# Assign the cumulative MTBF for display.
            MTBF = _nonpar_[_n_records_ - 1][10]
            MTBFLL = _nonpar_[_n_records_ - 1][11]
            MTBFUL = _nonpar_[_n_records_ - 1][12]

            self.txtChiSq.set_text(str(fmt.format(_chisq_)))
            self.txtRho.set_text(str(fmt.format(_rho_)))
            self.txtZLPNorm.set_text(str(fmt.format(_z_norm_)))
            self.txtZLRNorm.set_text(str(fmt.format(_z_norm_)))
            self.txtRhoNorm.set_text(str(fmt.format(_z_norm_)))

            if(mhb > _chisq_):
                _text[0] = _(u"<span foreground='red'>Nonconstant</span>")
            else:
                _text[0] = _(u"<span foreground='green'>Constant</span>")
            if(fabs(zlp) > _z_norm_):
                _text[1] = _(u"<span foreground='red'>Nonconstant</span>")
            else:
                _text[1] = _(u"<span foreground='green'>Constant</span>")
            if(fabs(zlr) > _z_norm_):
                _text[2] = _(u"<span foreground='red'>Nonconstant</span>")
            else:
                _text[2] = _(u"<span foreground='green'>Constant</span>")

# =========================================================================== #
# Perform a Kaplan-Meier analysis.
# =========================================================================== #
        elif(_analysis_ == 2):              # Kaplan-Meier
# TODO: Revise tbl_dataset to include a field for the hardware id.
# TODO: Revise the following query to include the hardware id field that will be added.
            _query_ = "SELECT fld_left_interval, fld_right_interval, \
                              fld_status, fld_quantity, fld_unit \
                       FROM tbl_survival_data \
                       WHERE fld_dataset_id=%d \
                       AND fld_right_interval >= %f \
                       AND fld_right_interval <= %f \
                       ORDER BY fld_right_interval ASC, \
                       fld_status DESC" % (_dataset_, _starttime_, _reltime_)
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

# Make a list with the rank of the records that are failures.
            r = []
            for i in range(len(_results_)):
                if(_results_[i][2] == 'Event' or
                   _results_[i][2] == 'Interval Censored'):
                    r.append(i + 1)

# The Kaplan-Meier function will retun a list of lists where the index of each
# list is:
#    0 = total number of subjects in each curve.
#    1 = the time points at which the curve has a step.
#    2 = the number of subjects at risk at t.
#    3 = the number of events that occur at time t.
#    4 = the number of subjects that enter at time t (counting
#        process data only).
#    5 = the estimate of survival at time t+0. This may be a vector
#        or a matrix.
#    6 = type of survival censoring.
#    7 = the standard error of the cumulative hazard or
#        -log(survival).
#    8 = upper confidence limit for the survival curve.
#    9 = lower confidence limit for the survival curve.
#   10 = the approximation used to compute the confidence limits.
#   11 = the level of the confidence limits, e.g. 90 or 95%.
#   12 = the returned value from the na.action function, if any.
#        It will be used in the printout of the curve, e.g., the
#        number of observations deleted due to missing values.
            _nonpar_ = kaplan_meier(_results_, _reltime_, _conf_)
            turnbull(_results_, _reltime_, _conf_)

            n_points = _nonpar_[0][0]
            _times_ = _nonpar_[1]
            _Shat_ = _nonpar_[5]
            _Shatll_ = _nonpar_[8]
            _Shatul_ = _nonpar_[9]

            n_failures = 0
            _kaplan_meier_ = []
            for i in range(len(_times_)):
                _kaplan_meier_.append([_nonpar_[1][i], _nonpar_[2][i],
                                       _nonpar_[3][i], _nonpar_[7][i],
                                       _nonpar_[9][i], _nonpar_[5][i],
                                       _nonpar_[8][i]])
                n_failures += _nonpar_[3][i]

# Calculate the MTBF, the variance on the MTBF, and the limits on the MTBF.
            _mtbf_ = kaplan_meier_mean(_kaplan_meier_, _conf_)

            MTBF = _mtbf_[len(_mtbf_) - 1][0]
            MTBFLL = _mtbf_[len(_mtbf_) - 1][1]
            MTBFUL = _mtbf_[len(_mtbf_) - 1][2]

# Load the non-parametric results gtk.TreeView
            _model_ = gtk.ListStore(gobject.TYPE_FLOAT, gobject.TYPE_INT,
                                    gobject.TYPE_INT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT)
            _index_ = [0, 1, 2, 3, 4, 5, 6]
            _col_headings_ = [_(u"Time"), _(u"Number\nat Risk"),
                              _(u"Number\nFailing"), _(u"se S(t)"),
                              _(u"S(t) Lower\nBound"), _(u"S(t)"),
                              _(u"S(t) Upper\nBound")]
            self._load_nonparametric_tree(_model_, _kaplan_meier_,
                                          _index_, _col_headings_)

            _logtimes_ = [log(i) for i in _times_]

            (_h_, _hll_, _hul_,
             _H_, _Hll_, _Hul_,
             _logH_, _logHll_, _logHul_) = kaplan_meier_hazard(_kaplan_meier_)

# Calculate the number of failures and suspensions in the dataset.
            n_suspensions = n_points - n_failures

# Plot the survival curve with confidence bounds.
            self._load_plot(self.axAxis1, self.pltPlot1,
                            x=_times_, y1=_Shat_,
                            y2=_Shatll_, y3=_Shatul_,
                            _title_=_(u"Kaplan-Meier Plot of %s") % _name,
                            _xlab_=_(u"Time"),
                            _ylab_=_(u"Survival Function [S(t)] "),
                            _marker_=['g-', 'r-', 'b-'])
            _text_ = (u"Survival Function [S(t)]", u"S(t) LCL", u"S(t) UCL")
            _widg.create_legend(self.axAxis1, _text_, _fontsize_='medium',
                                _frameon_=True, _location_='upper right',
                                _shadow_=True)

# Plot the hazard rate curve with confidence bounds.
            self._load_plot(self.axAxis3, self.pltPlot3,
                            x=_times_[1:], y1=_h_[1:],
                            y2=_hll_[1:], y3=_hul_[1:],
                            _title_=_(u"Hazard Rate Plot of %s") % _name,
                            _xlab_=_(u"Time"),
                            _ylab_=_(u"Hazard Rate [h(t)] "),
                            _marker_=['g-', 'r-', 'b-'])
            _text_ = (u"Hazard Rate [h(t)]", u"h(t) LCL", u"h(t) UCL")
            _widg.create_legend(self.axAxis3, _text_, _fontsize_='medium',
                                _frameon_=True, _location_='upper right',
                                _shadow_=True)

            for plot in self.vbxPlot1.get_children():
                self.vbxPlot1.remove(plot)

            self.vbxPlot1.pack_start(self.pltPlot1)
            self.vbxPlot1.pack_start(self.pltPlot3)

# Plot the cumulative hazard curve with confidence bounds.
            self._load_plot(self.axAxis2, self.pltPlot2,
                            x=_times_, y1=_H_,
                            y2=_Hll_, y3=_Hul_,
                            _title_=_("Cumulative Hazard Plot of %s") % _name,
                            _xlab_=_("Time"),
                            _ylab_=_("Cumulative Hazard Function [H(t)] "),
                            _marker_=['g-', 'r-', 'b-'])
            _text_ = (u"Cumulative Hazard Function [H(t)]",
                      u"H(t) LCL", u"H(t) UCL")
            _widg.create_legend(self.axAxis2, _text_, _fontsize_='medium',
                                _frameon_=True, _location_='upper left',
                                _shadow_=True)

# Plot the log cumulative hazard curve with confidence bounds.
            self._load_plot(self.axAxis4, self.pltPlot4,
                            x=_logtimes_, y1=_logH_[:len(_logtimes_)],
                            y2=_logHll_, y3=_logHul_,
                            _title_=_("Log Cum. Hazard Plot of %s") % _name,
                            _xlab_=_("log(Time)"),
                            _ylab_=_("Log Cum. Hazard Function [log H(t)] "),
                            _marker_=['g-', 'r-', 'b-'])
            _text_ = (u"Log Cumulative Hazard Function [log H(t)]",
                      u"log H(t) LCL", u"log H(t) UCL")
            _widg.create_legend(self.axAxis4, _text_, _fontsize_='medium',
                                _frameon_=True, _location_='upper left',
                                _shadow_=True)

            for plot in self.vbxPlot2.get_children():
                self.vbxPlot2.remove(plot)

            self.vbxPlot2.pack_start(self.pltPlot2)
            self.vbxPlot2.pack_start(self.pltPlot4)

# =========================================================================== #
# Fit the data to a power law (Duane) model and estimate it's parameters.
# =========================================================================== #
        elif(_analysis_ == 3):              # NHPP - Power Law

            _F_ = []
            _X_ = []
            _dates_ = []
            _times_ = []
            _mtbf_model_ = []
            _fi_model_ = []
            _mtbf_c_plot_ll_ = []
            _mtbf_c_plot_ = []
            _mtbf_c_plot_ul_ = []
            _fi_c_plot_ll_ = []
            _fi_c_plot_ = []
            _fi_c_plot_ul_ = []

# Create lists of the failure times and number of failures.
            for i in range(len(_results_)):
                _F_.append(_results_[i][5])
                _X_.append(_results_[i][3])
                _dates_.append(_results_[i][6])

            _T_ = float(self.txtEndTime.get_text())

# The power_law function will return a list of lists where each list contains:
#   Index       Value
#    0          Cumulative test time
#    1          Cumulative number of failures
#    2          Calculated cumulative MTBF
#    3          Lower bound on alpha
#    4          Point estimate of alpha
#    5          Upper bounf on alpha
#    6          Lower bound on b
#    7          Point estimate of b
#    8          Upper bound on b
#    9          Lower bound on model estimate of cumulative MTBF
#   10          Model point estimate of cumulative MTBF
#   11          Upper bound on model estimate of cumulative MTBF
#   12          Lower bound on model estimate of instantaneous MTBF
#   13          Model point estimate of instantaneous MTBF
#   14          Upper bound on model estimate of instantaneous MTBF
#   15          Lower bound on model estimate of cumulative failure intensity
#   16          Model point estimate of cumulative failure intensity
#   17          Upper bound on model estimate of cumulative failure intensity
#   18          Lower bound on model estimate of instantaneous failure intensity
#   19          Model point estimate of instantaneous failure intensity
#   20          Upper bound on model estimate of instantaneous failure intensity
            _power_law_ = power_law(_F_, _X_, _fitmeth_, _type_, _conf_, _T_)

# Load the non-parametric results gtk.TreeView
            _model_ = gtk.ListStore(gobject.TYPE_FLOAT, gobject.TYPE_INT,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
            _index_ = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 16, 17]
            _col_headings_ = [_(u"Cumulative\nTime"),
                              _(u"Cumulative\nNumber\nof Failures"),
                              _(u"\u03B1\nLower Bound"), _(u"\u03B1"),
                              _(u"\u03B1\nLower Bound"), _(u"b\nLower Bound"),
                              _(u"b"), _(u"b\nUpper Bound"),
                              _(u"Cumulative MTBF\nLower Bound"),
                              _(u"Cumulative\nMTBF"),
                              _(u"Cumulative\nMTBF\nUpper Bound"),
                              _(u"Cumulative\nFailure Intensity\nUpper Bound"),
                              _(u"Cumulative\nFailure\nIntensity"),
                              _(u"Cumulative\nFailure Intensity\nUpper Bound")]
            self._load_nonparametric_tree(_model_, _power_law_,
                                          _index_, _col_headings_)

            shapell = _power_law_[len(_power_law_) - 1][3]
            shape = _power_law_[len(_power_law_) - 1][4]
            shapeul = _power_law_[len(_power_law_) - 1][5]

            scalell = _power_law_[len(_power_law_) - 1][6]
            scale = _power_law_[len(_power_law_) - 1][7]
            scaleul = _power_law_[len(_power_law_) - 1][8]

            MTBFLL = _power_law_[len(_power_law_) - 1][9]
            MTBF = _power_law_[len(_power_law_) - 1][10]
            MTBFUL = _power_law_[len(_power_law_) - 1][11]

            MTBFiLL = _power_law_[len(_power_law_) - 1][12]
            MTBFi = _power_law_[len(_power_law_) - 1][13]
            MTBFiUL = _power_law_[len(_power_law_) - 1][14]

            for i in range(len(_power_law_)):
                _times_.append(_power_law_[i][0])
                _mtbf_model_.append(scale * _power_law_[i][0]**shape)
                _fi_model_.append((1.0 / scale) * _power_law_[i][0]**-shape)
                _mtbf_c_plot_ll_.append(_power_law_[i][9])
                _mtbf_c_plot_.append(_power_law_[i][10])
                _mtbf_c_plot_ul_.append(_power_law_[i][11])
                _fi_c_plot_ll_.append(_power_law_[i][15])
                _fi_c_plot_.append(_power_law_[i][16])
                _fi_c_plot_ul_.append(_power_law_[i][17])

# Display the NHPP Power Law specific results.
            self.txtMTBFi.set_text(str(fmt.format(MTBFi)))
            self.txtMTBFiLL.set_text(str(fmt.format(MTBFiLL)))
            self.txtMTBFiUL.set_text(str(fmt.format(MTBFiUL)))

            try:
                self.txtHazardRatei.set_text(str(fmt.format(1.0 / MTBFi)))
            except ZeroDivisionError:
                self.txtHazardRatei.set_text("0.0")

            try:
                self.txtHazardRateiLL.set_text(str(fmt.format(1.0 / MTBFiUL)))
            except ZeroDivisionError:
                self.txtHazardRateiLL.set_text("0.0")

            try:
                self.txtHazardRateiUL.set_text(str(fmt.format(1.0 / MTBFiLL)))
            except ZeroDivisionError:
                self.txtHazardRateiUL.set_text("0.0")

# Plot the MTBF curve with confidence bounds.
            _widg.load_plot(self.axAxis1, self.pltPlot1, x=_times_,
                            y1=_mtbf_c_plot_, y2=_mtbf_c_plot_ll_,
                            y3=_mtbf_c_plot_ul_, y4=_mtbf_model_,
                            _title_=_(u"Duane Plot of %s Cumulative MTBF") % _name,
                            _xlab_=_(u"Cumulative Time [hours]"),
                            _ylab_=_(u"Cumulative MTBF [m(t)] "),
                            _marker_=['go', 'r-', 'b-', 'k--'],
                            _type_=[2, 2, 2, 2])
            _text_ = (_(u"Cumulative MTBF"), _(u"Cum. MTBF LCL"),
                      _(u"Cum. MTBF UCL"), _(u"Fitted Model"))
            _widg.create_legend(self.axAxis1, _text_, _fontsize_='medium',
                                _frameon_=True, _location_='lower right',
                                _shadow_=True)

            self.axAxis1.set_xscale('log')
            self.axAxis1.set_yscale('log')

            _widg.load_plot(self.axAxis2, self.pltPlot2, x=_dates_,
                            y1=_mtbf_c_plot_, y2=_mtbf_c_plot_ll_,
                            y3=_mtbf_c_plot_ul_, y4=_mtbf_model_,
                            _title_=_(u"Duane Plot of %s Cumulative MTBF Over Calendar Time") % _name,
                            _xlab_=_(u"Calendar Time"),
                            _ylab_=_(u"Cumulative MTBF [m(t)] "),
                            _marker_=['go', 'r-', 'b-', 'k--'],
                            _type_=[4, 4, 4, 4])
            _text_ = (_(u"Cumulative MTBF"), _(u"Cum. MTBF LCL"),
                      _(u"Cum. MTBF UCL"), _(u"Fitted Model"))
            _widg.create_legend(self.axAxis2, _text_, _fontsize_='medium',
                                _frameon_=True, _location_='lower right',
                                _shadow_=True)

            _widg.load_plot(self.axAxis3, self.pltPlot3, x=_times_,
                            y1=_fi_c_plot_, y2=_fi_c_plot_ll_,
                            y3=_fi_c_plot_ul_, y4=_fi_model_,
                            _title_=_(u"Duane Plot of %s Cumulative Failure Intesity") % _name,
                            _xlab_=_(u"Cumulative Time [hours]"),
                            _ylab_=_(u"Cumulative Failure Intensity "),
                            _marker_=['go', 'r-', 'b-', 'k--'],
                            _type_=[2, 2, 2, 2])
            _text_ = (_(u"Cumulative Failure Intensity"), _(u"Cum. FI LCL"),
                      _(u"Cum. FI UCL"), _(u"Fitted Model"))
            _widg.create_legend(self.axAxis3, _text_,  _fontsize_='medium',
                                _frameon_=True, _location_='upper right',
                                _shadow_=True)

            self.axAxis3.set_xscale('log')
            self.axAxis3.set_yscale('log')

            _widg.load_plot(self.axAxis4, self.pltPlot4, x=_dates_[3:],
                            y1=_fi_c_plot_[3:], y2=_fi_c_plot_ll_[3:],
                            y3=_fi_c_plot_ul_[3:], y4=_fi_model_[3:],
                            _title_=_(u"Duane Plot of %s Cumulative Failure Intesity Over Calendar Time") % _name,
                            _xlab_=_(u"Calendar Time"),
                            _ylab_=_(u"Cumulative Failure Intensity "),
                            _marker_=['go', 'r-', 'b-', 'k--'],
                            _type_=[4, 4, 4, 4])
            _text_ = (_(u"Cumulative Failure Intensity"), _(u"Cum. FI LCL"),
                      _(u"Cum. FI UCL"), _(u"Fitted Model"))
            _widg.create_legend(self.axAxis4, _text_,  _fontsize_='medium',
                                _frameon_=True, _location_='upper right',
                                _shadow_=True)

            for plot in self.vbxPlot1.get_children():
                self.vbxPlot1.remove(plot)

            self.vbxPlot1.pack_start(self.pltPlot1)
            self.vbxPlot1.pack_start(self.pltPlot3)

            for plot in self.vbxPlot2.get_children():
                self.vbxPlot2.remove(plot)

            self.vbxPlot2.pack_start(self.pltPlot2)
            self.vbxPlot2.pack_start(self.pltPlot4)

        elif(_analysis_ == 4):              # NHPP - Loglinear

            _F_ = []
            _X_ = []
            _dates_ = []
            _times_ = []
            _mtbf_model_ = []
            _fi_model_ = []
            _mtbf_c_plot_ll_ = []
            _mtbf_c_plot_ = []
            _mtbf_c_plot_ul_ = []
            _fi_c_plot_ll_ = []
            _fi_c_plot_ = []
            _fi_c_plot_ul_ = []

# Create lists of the failure times and number of failures.
            for i in range(len(_results_)):
                _F_.append(_results_[i][5])
                _X_.append(_results_[i][3])
                _dates_.append(_results_[i][6])

            _T_ = float(self.txtEndTime.get_text())

# The power_law function will return a list of lists where each list contains:
#   Index       Value
#    0          Cumulative test time
#    1          Cumulative number of failures
#    2          Calculated cumulative MTBF
#    3          Lower bound on alpha
#    4          Point estimate of alpha
#    5          Upper bounf on alpha
#    6          Lower bound on b
#    7          Point estimate of b
#    8          Upper bound on b
#    9          Lower bound on model estimate of cumulative MTBF
#   10          Model point estimate of cumulative MTBF
#   11          Upper bound on model estimate of cumulative MTBF
#   12          Lower bound on model estimate of instantaneous MTBF
#   13          Model point estimate of instantaneous MTBF
#   14          Upper bound on model estimate of instantaneous MTBF
#   15          Lower bound on model estimate of cumulative failure intensity
#   16          Model point estimate of cumulative failure intensity
#   17          Upper bound on model estimate of cumulative failure intensity
#   18          Lower bound on model estimate of instantaneous failure intensity
#   19          Model point estimate of instantaneous failure intensity
#   20          Upper bound on model estimate of instantaneous failure intensity
            _log_linear_ = loglinear(_F_, _X_, _fitmeth_, _type_, _conf_, _T_)

# =========================================================================== #
# Fit the data to an exponential distribution and estimate it's parameters.
# =========================================================================== #
        elif(_analysis_ == 5):
            fit = parametric_fit(results, _starttime_, _reltime_,
                                 _fitmeth_, 'exponential')

            if(_fitmeth_ == 1):             # MLE
                scale = fit[0][0]
                scalell = fit[0][0] - _z_norm_ * fit[1][0]
                scaleul = fit[0][0] + _z_norm_ * fit[1][0]
                scalescale = fit[1][0]**2.0
                mle = fit[3][0]
                aic = fit[4][0]
                bic = fit[5][0]

            elif(_fitmeth_ == 2):           # Rank regression.
                scale = 1.0 / exp(fit[0][0])
                scalell = 1.0 / (exp(fit[0][0] + _z_norm_ * fit[2][0]))
                scaleul = 1.0 / (exp(fit[0][0] - _z_norm_ * fit[2][0]))
                scalescale = fit[2][0]
                mle = fit[3][0]

            MTBF = 1.0 / scale
            MTBFLL = 1.0 / scaleul
            MTBFUL = 1.0 / scalell

            para = R.list(rate=scale)
            _theop_ = theoretical_distribution(censdata, 'exp', para)

            times = [float(i[3]) for i in results if i[2] <= _reltime_]
            Rtimes = robjects.FloatVector(times)
            Rtimes = R.sort(Rtimes)
            _qqplot_ = R.qqplot(R.qexp(R.ppoints(Rtimes), rate=scale),
                                Rtimes, False)

# Display the widgets we need.
            self.txtScaleScale.show()

# Hide widgets we don't need.
            self.lblRowShape.hide()
            self.lblColShape.hide()
            self.lblRowLocation.hide()
            self.lblColLocation.hide()
            self.txtShapeShape.hide()
            self.txtShapeScale.hide()
            self.txtShapeLocation.hide()
            self.txtScaleShape.hide()
            self.txtScaleLocation.hide()
            self.txtLocationShape.hide()
            self.txtLocationScale.hide()
            self.txtLocationLocation.hide()

# =========================================================================== #
# Fit the data to a lognormal and estimate it's parameters.
# =========================================================================== #
        elif(_analysis_ == 6):
            fit = parametric_fit(results, _starttime_, _reltime_,
                                 _fitmeth_, 'lognormal')

            if(_fitmeth_ == 1):             # MLE
                scale = fit[0][0]
                scalell = scale - _z_norm_ * fit[1][0]
                scaleul = scale + _z_norm_ * fit[1][0]
                shape = fit[0][1]
                shapell = shape - _z_norm_ * fit[1][1]
                shapeul = shape + _z_norm_ * fit[1][1]
                scalescale = fit[2][0]**2
                scaleshape = fit[2][1]**2
                shapeshape = fit[2][2]**2
                shapescale = fit[2][3]**2
                mle = fit[3][0]
                aic = fit[4][0]
                bic = fit[5][0]

            elif(_fitmeth_ == 2):           # Rank regression.
                scale = fit[1][0]
                shape = fit[1][1]
                scalescale = fit[2][0]
                scaleshape = fit[2][1]
                shapescale = fit[2][2]
                shapeshape = fit[2][3]
                scalell = scale - _z_norm_ * sqrt(scalescale)
                scaleul = scale + _z_norm_ * sqrt(scalescale)
                shapell = shape - _z_norm_ * sqrt(shapeshape)
                shapeul = shape + _z_norm_ * sqrt(shapeshape)

            MTBF = exp(scale + 0.5 * shape**2.0)
            MTBFLL = exp(scalell + 0.5 * shapell**2.0)
            MTBFUL = exp(scaleul + 0.5 * shapeul**2.0)

            para = R.list(sdlog=shape, meanlog=scale)
            _theop_ = theoretical_distribution(censdata, 'lnorm', para)

            times = [float(i[3]) for i in results if i[2] <= _reltime_]
            Rtimes = robjects.FloatVector(times)
            Rtimes = R.sort(Rtimes)
            _qqplot_ = R.qqplot(R.qlnorm(R.ppoints(Rtimes), meanlog=scale,
                                sdlog=shape), Rtimes, False)

# Display the widgets we need.
            self.lblRowShape.show()
            self.lblColShape.show()
            self.lblRowScale.show()
            self.lblColScale.show()
            self.txtShapeShape.show()
            self.txtShapeScale.show()
            self.txtScaleShape.show()
            self.txtScaleScale.show()

# Hide widgets we don't need.
            self.lblRowLocation.hide()
            self.lblColLocation.hide()
            self.txtShapeLocation.hide()
            self.txtScaleLocation.hide()
            self.txtLocationShape.hide()
            self.txtLocationScale.hide()
            self.txtLocationLocation.hide()

# =========================================================================== #
# Fit the data to a normal distibution and estimate it's parameters.
# =========================================================================== #
        elif(_analysis_ == 7):
            fit = parametric_fit(results, _starttime_, _reltime_,
                                 _fitmeth_, 'normal')

            if(_fitmeth_ == 1):             # MLE
                scale = fit[0][0]
                scalell = scale - _z_norm_ * fit[1][0]
                scaleul = scale + _z_norm_ * fit[1][0]
                shape = fit[0][1]
                shapell = shape - _z_norm_ * fit[1][1]
                shapeul = shape + _z_norm_ * fit[1][1]
                scalescale = fit[1][0]**2
                shapeshape = fit[1][1]**2
                mle = fit[3][0]
                aic = fit[4][0]
                bic = fit[5][0]
            elif(_fitmeth_ == 2):           # Rank regression.
                scale = fit[1][0]
                shape = exp(fit[1][1])
                scalescale = fit[2][0]
                scaleshape = fit[2][1]
                shapescale = fit[2][2]
                shapeshape = fit[2][3]
                scalell = scale - _z_norm_ * sqrt(scalescale)
                scaleul = scale + _z_norm_ * sqrt(scalescale)
                shapell = shape - _z_norm_ * sqrt(shapeshape)
                shapeul = shape + _z_norm_ * sqrt(shapeshape)

            MTBF = scale
            MTBFLL = scalell
            MTBFUL = scaleul

            para = R.list(sd=shape, mean=scale)
            _theop_ = theoretical_distribution(censdata, 'norm', para)

            times = [float(i[3]) for i in results if i[2] <= _reltime_]
            Rtimes = robjects.FloatVector(times)
            Rtimes = R.sort(Rtimes)
            _qqplot_ = R.qqplot(R.qnorm(R.ppoints(Rtimes), mean=scale,
                                sd=shape), Rtimes, False)

# Display the widgets we need.
            self.lblRowShape.show()
            self.lblColShape.show()
            self.lblRowScale.show()
            self.lblColScale.show()
            self.txtShapeShape.show()
            self.txtShapeScale.show()
            self.txtScaleShape.show()
            self.txtScaleScale.show()

# Hide widgets we don't need.
            self.lblRowLocation.hide()
            self.lblColLocation.hide()
            self.txtShapeLocation.hide()
            self.txtScaleLocation.hide()
            self.txtLocationShape.hide()
            self.txtLocationScale.hide()
            self.txtLocationLocation.hide()

# =========================================================================== #
# Fit the data to a Weibull distribution and estimate it's parameters.
# =========================================================================== #
        elif(_analysis_ == 8):
            fit = parametric_fit(results, _starttime_, _reltime_,
                                 _fitmeth_, 'weibull')

            if(_fitmeth_ == 1):             # MLE
                scale = fit[0][1]
                scalell = scale / exp(_z_norm_ * fit[1][1] / scale)
                scaleul = scale * exp(_z_norm_ * fit[1][1] / scale)
                shape = fit[0][0]
                shapell = shape / exp(_z_norm_ * fit[1][0] / shape)
                shapeul = shape * exp(_z_norm_ * fit[1][0] / shape)
                shapeshape = fit[1][0]**2
                scalescale = fit[1][1]**2
                mle = fit[3][0]
                aic = fit[4][0]
                bic = fit[5][0]

                if(__USE_RPY2__):
                    MTBF = scale * R.gamma(1.0 + (1.0 / shape))[0]
                    MTBFLL = scalell * R.gamma(1.0 + (1.0 / shapell))[0]
                    MTBFUL = scaleul * R.gamma(1.0 + (1.0 / shapeul))[0]

            elif(_fitmeth_ == 2):           # Regression
                scale = exp(fit[1][0])
                shape = exp(fit[1][1])
                scalescale = fit[2][0]
                scaleshape = fit[2][1]
                shapescale = fit[2][2]
                shapeshape = fit[2][3]
                scalell = scale - _z_norm_ * sqrt(scalescale)
                scaleul = scale + _z_norm_ * sqrt(scalescale)
                shapell = shape - _z_norm_ * sqrt(shapeshape)
                shapeul = shape + _z_norm_ * sqrt(shapeshape)

                if(__USE_RPY2__):
                    MTBF = scale * R.gamma(1.0 + (1.0 / shape))[0]
                    MTBFLL = scalell * R.gamma(1.0 + (1.0 / shapeul))[0]
                    MTBFUL = scaleul * R.gamma(1.0 + (1.0 / shapell))[0]

            para = R.list(shape=shape, scale=scale)
            _theop_ = theoretical_distribution(censdata, 'weibull', para)

            times = [float(i[3]) for i in results if i[2] <= _reltime_]
            Rtimes = robjects.FloatVector(times)
            Rtimes = R.sort(Rtimes)
            _qqplot_ = R.qqplot(R.qweibull(R.ppoints(Rtimes), shape=shape,
                                scale=scale), Rtimes, False)

# Display the widgets we need.
            self.lblRowShape.show()
            self.lblColShape.show()
            self.lblRowScale.show()
            self.lblColScale.show()
            self.txtShapeShape.show()
            self.txtShapeScale.show()
            self.txtScaleShape.show()
            self.txtScaleScale.show()

# Hide widgets we don't need.
            self.lblRowLocation.hide()
            self.lblColLocation.hide()
            self.txtShapeLocation.hide()
            self.txtScaleLocation.hide()
            self.txtLocationShape.hide()
            self.txtLocationScale.hide()
            self.txtLocationLocation.hide()

        #elif(_analysis_ == 9):              # Fit to a WeiBayes.

# Find the percent of records belonging to each sub-assembly and then allocate
# this percent of the overall failure rate to each sub-assembly.
        if(self.chkGroup.get_active()):
            _query_ = "SELECT t2.fld_name, SUM(t1.fld_quantity), \
                              t2.fld_assembly_id \
                       FROM tbl_survival_data AS t1 \
                       INNER JOIN tbl_system AS t2 \
                       ON t1.fld_assembly_id=t2.fld_assembly_id \
                       WHERE t1.fld_dataset_id=%d \
                       AND t1.fld_right_interval <= %f \
                       AND t1.fld_right_interval > %f \
                       AND t1.fld_request_date >= %d \
                       AND t1.fld_request_date < %d \
                       GROUP BY t2.fld_name" % (_dataset_, _reltime_,
                                                _starttime_, _startdate_,
                                                _enddate_)
            _results_ = self._app.DB.execute_query(_query_,
                                                  None,
                                                  self._app.ProgCnx)

            _model_ = self.tvwResultsByChildAssembly.get_model()
            _model_.clear()
            _total_ = float(sum(x[1] for x in _results_))
            for i in range(len(_results_)):
                if(_results_[i][1] / _total_ >= 0.1):
                    _color_ = 'red'
                elif(_results_[i][1] / _total_ < 0.1 and
                     _results_[i][1] / _total_ >= 0.05):
                    _color_ = 'yellow'
                elif(_results_[i][1] / _total_ < 0.05 and
                     _results_[i][1] / _total_ >= 0.01):
                    _color_ = 'white'
                else:
                    _color_ = 'light gray'

                _values_ = (_results_[i][0], _results_[i][1], _results_[i][2],
                           (MTBFLL * _total_) / float(_results_[i][1]),
                           (MTBF * _total_) / float(_results_[i][1]),
                           (MTBFUL * _total_) / float(_results_[i][1]),
                           float(_results_[i][1]) / (MTBFUL * _total_),
                           float(_results_[i][1]) / (MTBF * _total_),
                           float(_results_[i][1]) / (MTBFLL * _total_),
                           _color_)
                _model_.append(_values_)

# Find the percent of records belonging to each component and then allocate
# this percent of the overall failure rate to each component.
        if(self.chkParts.get_active()):
            _query_ = "SELECT t1.fld_part_num, COUNT(t1.fld_part_num) \
                       FROM tbl_incident_detail AS t1 \
                       INNER JOIN tbl_incident AS t2 ON \
                                  t1.fld_incident_id=t2.fld_incident_id \
                       WHERE t2.fld_revision_id=%d \
                       AND t1.fld_age_at_incident <= %f \
                       AND t1.fld_age_at_incident > %f \
                       AND t2.fld_request_date >= %d \
                       AND t2.fld_request_date < %d \
                       GROUP BY t1.fld_part_num \
                       ORDER BY COUNT(t1.fld_part_num) DESC" % \
                       (self._app.REVISION.revision_id, _reltime_,
                        _starttime_, _startdate_, _enddate_)
            _results_ = self._app.DB.execute_query(_query_,
                                                  None,
                                                  self._app.ProgCnx)

            _model_ = self.tvwResultsByPart.get_model()
            _model_.clear()
            _total_ = float(sum(x[1] for x in _results_))
            for i in range(len(_results_)):
                if(_results_[i][1] / _total_ >= 0.01):
                    _color_ = 'red'
                elif(_results_[i][1] / _total_ < 0.01 and
                     _results_[i][1] / _total_ >= 0.005):
                    _color_ = 'yellow'
                elif(_results_[i][1] / _total_ < 0.005 and
                     _results_[i][1] / _total_ >= 0.001):
                    _color_ = 'white'
                else:
                    _color_ = 'light gray'

                _values_ = (_results_[i][0], _results_[i][1],
                            (MTBFLL * _total_) / float(_results_[i][1]),
                            (MTBF * _total_) / float(_results_[i][1]),
                            (MTBFUL * _total_) / float(_results_[i][1]),
                            float(_results_[i][1]) / (MTBFUL * _total_),
                            float(_results_[i][1]) / (MTBF * _total_),
                            float(_results_[i][1]) / (MTBFLL * _total_),
                            _color_)
                _model_.append(_values_)

# =========================================================================== #
# Create and display parametric plots.
# =========================================================================== #
        if(_analysis_ > 4):
# Plot a histogram of interarrival times.
            hist = R.hist(Rtimes, plot='False')
            bins = list(hist[0])
            counts = list(hist[1])

            __title__ = _(u"Histogram of Interarrival Times for %s") % _name
            self._load_plot(self.axAxis1, self.pltPlot1,
                            x=Rtimes, y1=bins,
                            _title_=__title__,
                            _xlab_=_(u"Interarrival Times"),
                            _ylab_=_(u"Count "),
                            _type_=[3],
                            _marker_=['g'])

# Plot an ECDF of interarrival times.
            Rstats = importr('stats')
            Fn = Rstats.ecdf(Rtimes)
            ecdf = Fn(Rtimes)

            __title__ = _(u"Empirical CDF of Interarrival Times for %s") \
                % _name
            self._load_plot(self.axAxis3, self.pltPlot3,
                            x=Rtimes, y1=ecdf, y2=_theop_[1:],
                            _title_=__title__,
                            _xlab_=_(u"t"),
                            _ylab_=_(u"F(t) "),
                            _type_=[1, 2],
                            _marker_=['b-', 'r:'])

# Plot the probability plot of interarrival times.
            __title__ = _(u"Probability Plot of Interarrival Times for %s ") \
                % _name
            self._load_plot(self.axAxis4, self.pltPlot4,
                            x=_qqplot_[0], y1=_qqplot_[1],
                            _title_=__title__,
                            _xlab_=_(u"Theoretical"),
                            _ylab_=_(u"Observed"),
                            _type_=[2],
                            _marker_=['o'])

            for plot in self.vbxPlot1.get_children():
                self.vbxPlot1.remove(plot)

            self.vbxPlot1.pack_start(self.pltPlot1)
            self.vbxPlot1.pack_start(self.pltPlot3)

            for plot in self.vbxPlot2.get_children():
                self.vbxPlot2.remove(plot)

            #self.vbxPlot2.pack_start(self.pltPlot2)
            self.vbxPlot2.pack_start(self.pltPlot4)

        if(_RELTIME_):
            _reltime_ = 0.0

# Update gtk.TreeView with results.
        self.model.set_value(self.selected_row, 4, _analysis_)
        self.model.set_value(self.selected_row, 6, _type_)
        self.model.set_value(self.selected_row, 8, _fitmeth_)
        self.model.set_value(self.selected_row, 9, _reltime_)
        self.model.set_value(self.selected_row, 11, n_suspensions)
        self.model.set_value(self.selected_row, 12, n_failures)
        self.model.set_value(self.selected_row, 13, scale)
        self.model.set_value(self.selected_row, 14, scalell)
        self.model.set_value(self.selected_row, 15, scaleul)
        self.model.set_value(self.selected_row, 16, shape)
        self.model.set_value(self.selected_row, 17, shapell)
        self.model.set_value(self.selected_row, 18, shapeul)
        self.model.set_value(self.selected_row, 19, location)
        self.model.set_value(self.selected_row, 20, locationll)
        self.model.set_value(self.selected_row, 21, locationul)
        self.model.set_value(self.selected_row, 22, scalescale)
        self.model.set_value(self.selected_row, 23, shapeshape)
        self.model.set_value(self.selected_row, 24, locationlocation)
        self.model.set_value(self.selected_row, 25, scaleshape)
        self.model.set_value(self.selected_row, 26, scalelocation)
        self.model.set_value(self.selected_row, 27, shapelocation)
        self.model.set_value(self.selected_row, 28, mhb)
        self.model.set_value(self.selected_row, 29, zlp)
        self.model.set_value(self.selected_row, 30, zlr)
        self.model.set_value(self.selected_row, 31, aic)
        self.model.set_value(self.selected_row, 32, bic)
        self.model.set_value(self.selected_row, 33, mle)

# Update results widgets.
        self._analyses_results_tab_load()

        self.txtMTBF.set_text(str(fmt.format(MTBF)))
        self.txtMTBFLL.set_text(str(fmt.format(MTBFLL)))
        self.txtMTBFUL.set_text(str(fmt.format(MTBFUL)))

        try:
            self.txtHazardRate.set_text(str(fmt.format(1.0 / MTBF)))
        except ZeroDivisionError:
            self.txtHazardRate.set_text("0.0")

        try:
            self.txtHazardRateLL.set_text(str(fmt.format(1.0 / MTBFUL)))
        except ZeroDivisionError:
            self.txtHazardRateLL.set_text("0.0")

        try:
            self.txtHazardRateUL.set_text(str(fmt.format(1.0 / MTBFLL)))
        except ZeroDivisionError:
            self.txtHazardRateUL.set_text("0.0")

        self.txtMHBPValue.set_text(str(fmt.format(p_value[0])))
        self.txtZLPPValue.set_text(str(fmt.format(p_value[1])))
        self.txtZLRPValue.set_text(str(fmt.format(p_value[2])))
        self.txtRhoPValue.set_text(str(fmt.format(p_value[3])))

        self.lblMHBResult.set_markup(_text[0])
        self.lblZLPResult.set_markup(_text[1])
        self.lblZLRResult.set_markup(_text[2])

        return False

    def _consolidate_dataset(self, _button_):
        """
        Consolidates the dataset so there are only unique failure times,
        suspension times, and intervals with a quantity value rather than a
        single record for each failure.

        Keyword Arguments:
        _button_ -- the gtk.Button that called this function.
        """

        _query_ = "SELECT fld_record_id, fld_unit, fld_left_interval, \
                          fld_right_interval, fld_status, fld_quantity \
                   FROM tbl_survival_data \
                   WHERE fld_dataset_id=%d \
                   ORDER BY fld_unit ASC, \
                            fld_left_interval ASC, \
                            fld_right_interval ASC, \
                            fld_status ASC" % self.dataset_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        _n_records_ = len(_results_)

        _del_id_ = []
        _keep_id_ = []
        _quantity_ = _results_[0][5]
        for i in range(1, _n_records_):
# If the units are the same, the left intervals are the same, the right
# intervals are the same, and the type are the same, increment the count of
# records with the same failure times and add the previous record id to the
# list of records to delete.
            if(_results_[i][1] == _results_[i - 1][1] and
               _results_[i][2] == _results_[i - 1][2] and
               _results_[i][3] == _results_[i - 1][3] and
               _results_[i][4] == _results_[i - 1][4]):
                _quantity_ += _results_[i][5]
                _del_id_.append(_results_[i - 1][0])
            else:
                _keep_id_.append([_results_[i - 1][0], _quantity_])
                _quantity_ = _results_[i][5]

# Keep the last record.
        _keep_id_.append([_results_[-1][0], _quantity_])

# Update the quantity of the records to be kept.
        _n_keep_ = len(_keep_id_)
        for i in range(_n_keep_):
            _query_ = "UPDATE tbl_survival_data \
                       SET fld_quantity=%d \
                       WHERE fld_record_id=%d" % (_keep_id_[i][1],
                                                  _keep_id_[i][0])
            self._app.DB.execute_query(_query_,
                                       None,
                                       self._app.ProgCnx,
                                       commit=True)

# Delete the records that are "duplicates."
        _n_del_ = len(_del_id_)
        for i in range(_n_del_):
            _query_ = "DELETE FROM tbl_survival_data \
                       WHERE fld_record_id=%d" % _del_id_[i]
            self._app.DB.execute_query(_query_,
                                       None,
                                       self._app.ProgCnx,
                                       commit=True)

# Reload the dataset tree.
        self.load_tree()

        return False

    def _dataset_save(self, button):
        """
        Saves the DATASET Object gtk.TreeView information to the Program's
        MySQL or SQLite3 database.

        Keyword Arguments:
        button -- the gtk.Button widget that called this function.
        """

        self.model.foreach(self._save_line_item)

        return False

    def _survival_data_save(self, button):
        """
        Method to save the Dataset records gtk.TreeView information to the
        Program's MySQL or SQLite3 database.

        Keyword Arguments:
        button -- the gtk.Button widget that called this function.
        """

        model = self.tvwDataset.get_model()
        model.foreach(self._save_survival_record)

        return False

    def _save_line_item(self, model, path_, row):
        """
        Saves each row in the DATASET Object treeview model to the RTK's
        Program MySQL or SQLite3 database.

        Keyword Arguments:
        model -- the DATASET gtk.ListStore.
        path_ -- the path of the active row in the DATASET gtk.ListStore.
        row   -- the selected row in the DATASET gtk.TreeView.
        """

        _values_ = (self.model.get_value(self.selected_row, 1), \
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
                    self.model.get_value(self.selected_row, 34), \
                    self.model.get_value(self.selected_row, 35), \
                    self.model.get_value(self.selected_row, 36), \
                    self.model.get_value(self.selected_row, 0))

        _query_ = "UPDATE tbl_dataset \
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
                       fld_lr=%f, fld_aic=%f, fld_bic=%f, fld_mle=%f, \
                       fld_start_time=%d, fld_start_date=%d, fld_end_date=%d \
                   WHERE fld_dataset_id=%d" % _values_

        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("dataset.py: Failed to save dataset.")
            return True

        return False

    def _save_survival_record(self, model, path, row):
        """
        Saves each of the survival data records that comprise the selected
        DATASET to the RTK Program MySQL or SQLite3 database.

        Keyword Arguments:
        model -- the DATASET tvwDataset gtk.ListStore.
        path  -- the path of the active row in the DATASET gtk.ListStore.
        row   -- the selected row in the DATASET gtk.TreeView.
        """

        _values_ = (model.get_value(row, 1), model.get_value(row, 2),
                    model.get_value(row, 3), model.get_value(row, 4),
                    model.get_value(row, 0))

        _query_ = "UPDATE tbl_survival_data \
                   SET fld_unit='%s', fld_left_interval=%f, \
                       fld_right_interval=%f, fld_status='%s' \
                   WHERE fld_record_id=%d" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

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

        if(_index_ == 4):
            if(_text_ == 1 or _text_ == 2 or _index_ == 3): # MCF, Kaplan-Meier, or NHPP - Power Law
                self.chkGroup.show()
                self.chkParts.show()
                self.cmbFitMethod.hide()
                self.cmbConfMethod.hide()
                self.lblFitMethod.hide()
                self.lblConfMethod.hide()
            else:
                self.chkGroup.hide()
                self.chkParts.hide()
                self.cmbFitMethod.show()
                self.cmbConfMethod.show()
                self.lblFitMethod.show()
                self.lblConfMethod.show()

            if(_text_ == 7):                # WeiBayes
                dialog = _widg.make_dialog(_(u"RTK Information"),
                            _buttons_=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

                fixed = gtk.Fixed()

                y_pos = 10
                label = _widg.make_label(_(u"WeiBayes is not yet implemented in RTK."), width=300, height=100)
                fixed.put(label, 5, y_pos)

                fixed.show_all()

                dialog.vbox.pack_start(fixed)
                dialog.run()

                dialog.destroy()

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

    def _callback_combo_cell(self, cell, path, row, col, treemodel):
        """
        Called whenever a TreeView CellRendererCombo changes.

        Keyword Arguments:
        cell      -- the gtk.CellRendererCombo that called this function
        path      -- the path in the gtk.TreeView containing the
                     gtk.CellRendererCombo that called this function.
        row       -- the new gtk.TreeIter in the gtk.CellRendererCombo that
                     called this function.
        col       -- the index of the column in the gtk.TreeView containing
                     the gtk.CellRendererCombo.
        treemodel -- the gtk.TreeModel for the gtk.TreeView.
        """

        model = cell.get_property('model')
        val = model.get_value(row, 0)

        row = treemodel.get_iter(path)
        treemodel.set_value(row, col, val)

        return False

    def _callback_entry_cell(self, cell, path, new_text, _index_, _convert_):
        """
        Called whenever a TreeView CellRendererCombo changes.

        Keyword Arguments:
        cell      -- the gtk.CellRendererCombo that called this function
        path      -- the path in the gtk.TreeView containing the
                     gtk.CellRendererCombo that called this function.
        new_text  -- the new text in the gtk.CellRendererText that called this
                     method.
        _index_   -- the index (column) in the gtk.TreeView containing the
                     gtk.CellRendererText that is being edited.
        _convert_ -- the data type to convert new_text to for the
                     gtk.CellRendererText.
        """

        model = self.tvwDataset.get_model()
        row = model.get_iter(path)

        if(_convert_ == 'int'):
            new_text = int(new_text)
        elif(_convert_ == 'float'):
            new_text = float(new_text)
        elif(_convert_ == 'date'):
            new_text = datetime.strptime(new_text, '%Y-%m-%d').toordinal()

        model.set_value(row, _index_, new_text)

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
            self.dataset_id = self.model.get_value(self.selected_row, 0)
            self.load_notebook()

            if(self.model.get_value(self.selected_row, 4) == 1 or
               self.model.get_value(self.selected_row, 4) == 2):
                self.lblFitMethod.hide()
                self.lblConfMethod.hide()
                self.cmbFitMethod.hide()
                self.cmbConfMethod.hide()
            else:
                self.lblFitMethod.show()
                self.lblConfMethod.show()
                self.cmbFitMethod.show()
                self.cmbConfMethod.show()

            return False
        else:
            return True

    def create_tree(self):
        """
        Creates the DATASET treeview and connects it to callback functions to
        handle editting.  Background and foreground colors can be set using the
        user-defined values in the RTK configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()
        bg_color = _conf.RTK_COLORS[12]
        fg_color = _conf.RTK_COLORS[13]
        (self.treeview, self._col_order) = _widg.make_treeview('Dataset', 16,
                                                               self._app,
                                                               None,
                                                               bg_color,
                                                               fg_color)
        self.treeview.set_enable_tree_lines(True)

        self.treeview.set_tooltip_text(_(u"Displays a list of survival data sets."))

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

        if(_conf.RTK_MODULES[0] == 1):
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
        query = "SELECT fld_name, fld_assembly_id, fld_description \
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
            #self._load_component_list()

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxDataset)
        self._app.winWorkBook.show_all()

        if(self._nevada_chart_):
            self.fraNevadaChart.show_all()
        else:
            self.fraNevadaChart.hide_all()

        _title = _(u"RTK Work Book: Program Survival Analyses (%d Datasets)") % \
                   self.n_datasets
        self._app.winWorkBook.set_title(_title)

        self.notebook.set_current_page(0)

        return False
