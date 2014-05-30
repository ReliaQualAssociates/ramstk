#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to
Program survival data sets.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       dataset.py is part of The RTK Project
#
# All rights reserved.

import locale
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

# Plotting package.
import matplotlib
matplotlib.use('GTK')
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure

# Import modules for mathematics.
import numpy as np
from math import exp, fabs, log, sqrt
from scipy.stats import chi2, norm          # pylint: disable=E0611

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
import calculations as _calc
import configuration as _conf
import utilities as _util
import widgets as _widg

# Import other RTK classes.
from _assistants_.adds import AddDataset
from _assistants_.updates import AssignMTBFResults

# Import other RTK calculation functions.
from _calculations_.growth import power_law, loglinear
from _calculations_.survival import kaplan_meier, kaplan_meier_hazard, \
    kaplan_meier_mean, mean_cumulative_function, parametric_fit, \
    theoretical_distribution, turnbull

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

import gettext
_ = gettext.gettext


class Dataset(object):
    """
    The Dataset class is used to represent the survival data sets associated
    with the system being analyzed.
    """

    def __init__(self, application):
        """
        Initializes the Dataset class.

        @param application: the current instance of the RTK application.
        """

        # Define private Dataset class scalar attributes.
        self._app = application
        self._nevada_chart = True       # Dataset created from a Nevada chart.

        # Define private Dataset class dictionary attributes.

        # Define private Dataset class list attributes.

        # Define public Dataset class scalar attributes.
        self.dataset_id = 0
        """ ID in the RTK Program database of the currently selected data set.
        """
        self.assembly_id = 0
        self.description = ''
        """ Description of the data set."""
        self.source = 0
        """ Source of the data set."""
        self.distribution_id = 0
        """ ID in the RTK Program database of the statistical distribution to
            fit the data to."""
        self.confidence = 0.75
        """ s-confidence level to use in analyses of the data set. """
        self.confidence_type = 0
        """ s-confidence type (lower one-sided, upper one-sided, or
            two-sided). """
        self.confidence_method = 0
        self.fit_method = 0
        self.rel_time = 100.0
        self.n_rel_points = 0
        self.n_suspensions = 0
        self.n_failures = 0
        self.mhb = 0.0
        self.lp = 0.0
        self.lr = 0.0
        self.aic = 0.0
        self.bic = 0.0
        self.mle = 0.0
        self.start_time = 0.0
        self.end_time = 0.0
        self.start_date = 719163
        self.end_date = 719163
        self.n_datasets = 0

        # Define public Dataset class dictionary attributes.

        # Define public Dataset class list attributes.
        self.scale = [0.0, 0.0, 0.0]
        """ List of scale parameter estimates.\n
        | 0 | Point estimate\n
        | 1 | Lower bound estimate\n
        | 2 | Upper bound estimate"""       # pylint: disable=W0105
        self.shape = [0.0, 0.0, 0.0]
        """ List of shape parameter estimates.\n
        | 0 | Point estimate\n
        | 1 | Lower bound estimate\n
        | 2 | Upper bound estimate"""       # pylint: disable=W0105
        self.location = [0.0, 0.0, 0.0]
        """ List of location parameter estimates.\n
        | 0 | Point estimate\n
        | 1 | Lower bound estimate\n
        | 2 | Upper bound estimate"""       # pylint: disable=W0105
        self.variance = [0.0, 0.0, 0.0]
        """ List of variance estimates.\n
        | 0 | Scale parameter estimate\n
        | 1 | Shape parameter estimate\n
        | 2 | Location parameter estimate"""    # pylint: disable=W0105
        self.covariance = [0.0, 0.0, 0.0]
        """ List of covariance estimates.\n
        | 0 | Scale-Shape estimate\n
        | 1 | Scale-Location estimate\n
        | 2 | Shape-Location estimate"""    # pylint: disable=W0105

        # Create the main Dataset class treeview.
        (self.treeview,
         self._col_order) = _widg.make_treeview('Dataset', 16, self._app, None,
                                                _conf.RTK_COLORS[12],
                                                _conf.RTK_COLORS[13])

        # Dataset class Work Book toolbar widgets.

        # Create the Analyses Input page widgets.
        self.chkGroup = _widg.make_check_button(label=_(u"Decompose results "
                                                        u"to children "
                                                        u"assemblies"))
        self.chkParts = _widg.make_check_button(label=_(u"Decompose results "
                                                        u"to parts"))

        self.cmbAssembly = _widg.make_combo(simple=False)
        self.cmbConfType = _widg.make_combo()
        self.cmbConfMethod = _widg.make_combo()
        self.cmbDistribution = _widg.make_combo()
        self.cmbFitMethod = _widg.make_combo()
        self.cmbSource = _widg.make_combo()

        self.fraDataset = _widg.make_frame(label=_(u"Dataset"))
        self.fraNevadaChart = _widg.make_frame(label=_(u"Nevada Chart"))

        self.lblFitMethod = _widg.make_label(_(u"Fit Method:"), 150, 25)
        self.lblConfMethod = _widg.make_label(_(u"Confidence Method:"),
                                              150, 25)

        self.tvwDataset = gtk.TreeView()
        self.tvwDataset.set_search_column(0)
        self.tvwDataset.set_reorderable(True)

        self.tvwNevadaChart = gtk.TreeView()

        self.txtConfidence = _widg.make_entry(width=100)
        self.txtDescription = _widg.make_entry(width=200)
        self.txtStartTime = _widg.make_entry(width=100)
        self.txtEndTime = _widg.make_entry(width=100)
        self.txtRelPoints = _widg.make_entry(width=100)

        self.txtStartDate = _widg.make_entry(width=100)
        self.txtEndDate = _widg.make_entry(width=100)

        self.btnStartDate = _widg.make_button(height=25, width=25,
                                              label="...", image=None)
        self.btnEndDate = _widg.make_button(height=25, width=25,
                                            label="...", image=None)

        # Create the Analyses Results tab widgets.
        self.fraSummary = _widg.make_frame(label=_(u"Summary of Results"))
        self.fraNonParStats = _widg.make_frame(label=_(u"Non-Parametric "
                                                       u"Statistics"))
        self.fraNonParEst = _widg.make_frame(label=_(u"Parameter Estimates"))
        self.fraParStats = _widg.make_frame(label=_(u"Parameter Estimates"))

        self.hpnAnalysisResults = gtk.HPaned()

        self.vpnAnalysisResults = gtk.VPaned()

        # Upper left quadrant widgets.
        self.lblCumMTBF = _widg.make_label(_(u"Cumulative MTBF:"), width=-1)
        self.lblMTBFi = _widg.make_label(_(u"Instantaneous MTBF:"), width=-1)
        self.lblCumFI = _widg.make_label(_(u"Cumulative Failure Intensity:"),
                                         width=-1)
        self.lblFIi = _widg.make_label(_(u"Instantaneous Failure Intensity:"),
                                       width=-1)

        self.txtNumSuspensions = _widg.make_entry(width=50, editable=False)
        self.txtNumFailures = _widg.make_entry(width=50, editable=False)

        self.txtMTBF = _widg.make_entry(width=100, editable=False)
        self.txtMTBFLL = _widg.make_entry(width=100, editable=False)
        self.txtMTBFUL = _widg.make_entry(width=100, editable=False)
        self.txtMTBFi = _widg.make_entry(width=100, editable=False)
        self.txtMTBFiLL = _widg.make_entry(width=100, editable=False)
        self.txtMTBFiUL = _widg.make_entry(width=100, editable=False)
        self.txtHazardRate = _widg.make_entry(width=100, editable=False)
        self.txtHazardRateLL = _widg.make_entry(width=100, editable=False)
        self.txtHazardRateUL = _widg.make_entry(width=100, editable=False)
        self.txtHazardRatei = _widg.make_entry(width=100, editable=False)
        self.txtHazardRateiLL = _widg.make_entry(width=100, editable=False)
        self.txtHazardRateiUL = _widg.make_entry(width=100, editable=False)

        # Lower left quadrant non-parametric widgets.
        self.lblMHBResult = _widg.make_label(_(u""), width=100)
        self.lblZLPResult = _widg.make_label(_(u""), width=100)
        self.lblZLRResult = _widg.make_label(_(u""), width=100)
        self.lblRhoResult = _widg.make_label(_(u""), width=100)

        self.txtMHB = _widg.make_entry(width=100)
        self.txtChiSq = _widg.make_entry(width=100)
        self.txtMHBPValue = _widg.make_entry(width=100)
        self.txtLP = _widg.make_entry(width=100)
        self.txtZLPNorm = _widg.make_entry(width=100)
        self.txtZLPPValue = _widg.make_entry(width=100)
        self.txtLR = _widg.make_entry(width=100)
        self.txtZLRNorm = _widg.make_entry(width=100)
        self.txtZLRPValue = _widg.make_entry(width=100)
        self.txtRho = _widg.make_entry(width=100)
        self.txtRhoNorm = _widg.make_entry(width=100)
        self.txtRhoPValue = _widg.make_entry(width=100)

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
        self.lblAIC = _widg.make_label("AIC", width=150)
        self.lblBIC = _widg.make_label("BIC", width=150)
        self.lblMLE = _widg.make_label("MLE", width=150)

        self.txtScale = _widg.make_entry(width=100, editable=False)
        self.txtScaleLL = _widg.make_entry(width=100, editable=False)
        self.txtScaleUL = _widg.make_entry(width=100, editable=False)
        self.txtShape = _widg.make_entry(width=100, editable=False)
        self.txtShapeLL = _widg.make_entry(width=100, editable=False)
        self.txtShapeUL = _widg.make_entry(width=100, editable=False)
        self.txtLocation = _widg.make_entry(width=100, editable=False)
        self.txtLocationLL = _widg.make_entry(width=100, editable=False)
        self.txtLocationUL = _widg.make_entry(width=100, editable=False)

        self.txtShapeShape = _widg.make_entry(width=100, editable=False)
        self.txtShapeScale = _widg.make_entry(width=100, editable=False)
        self.txtShapeLocation = _widg.make_entry(width=100, editable=False)
        self.txtScaleShape = _widg.make_entry(width=100, editable=False)
        self.txtScaleScale = _widg.make_entry(width=100, editable=False)
        self.txtScaleLocation = _widg.make_entry(width=100, editable=False)
        self.txtLocationShape = _widg.make_entry(width=100, editable=False)
        self.txtLocationScale = _widg.make_entry(width=100, editable=False)
        self.txtLocationLocation = _widg.make_entry(width=100, editable=False)
        self.txtAIC = _widg.make_entry(width=100, editable=False)
        self.txtBIC = _widg.make_entry(width=100, editable=False)
        self.txtMLE = _widg.make_entry(width=100, editable=False)

        self.tvwNonParResults = gtk.TreeView()

        # Create the Plot tab widgets.
        _height = (self._app.winWorkBook.height * 0.01) / 2.0
        _width = (self._app.winWorkBook.width * 0.01) / 2.0
        self.figFigure1 = Figure(figsize=(_width, _height))
        self.pltPlot1 = FigureCanvas(self.figFigure1)
        self.pltPlot1.mpl_connect('button_press_event', _widg.expand_plot)
        self.axAxis1 = self.figFigure1.add_subplot(111)
        self.figFigure2 = Figure(figsize=(_width, _height))
        self.pltPlot2 = FigureCanvas(self.figFigure2)
        self.pltPlot2.mpl_connect('button_press_event', _widg.expand_plot)
        self.axAxis2 = self.figFigure2.add_subplot(111)
        self.figFigure3 = Figure(figsize=(_width, _height))
        self.pltPlot3 = FigureCanvas(self.figFigure3)
        self.pltPlot3.mpl_connect('button_press_event', _widg.expand_plot)
        self.axAxis3 = self.figFigure3.add_subplot(111)
        self.figFigure4 = Figure(figsize=(_width, _height))
        self.pltPlot4 = FigureCanvas(self.figFigure4)
        self.pltPlot4.mpl_connect('button_press_event', _widg.expand_plot)
        self.axAxis4 = self.figFigure4.add_subplot(111)
        self.vbxPlot1 = gtk.VBox()
        self.vbxPlot2 = gtk.VBox()

        # Create the analysis results breakdown widgets.
        self.fraResultsByChildAssembly = _widg.make_frame(label=_(u"Summary "
                                                                  u"of "
                                                                  u"Results "
                                                                  u"By Child "
                                                                  u"Assembly"))
        self.fraResultsByPart = _widg.make_frame(label=_(u"Summary of Results "
                                                         u"By Part"))

        self.hpnResultsBreakdown = gtk.HPaned()

        self.tvwResultsByChildAssembly = gtk.TreeView()
        self.tvwResultsByPart = gtk.TreeView()

        self.btnAssign = _widg.make_button(width=100, label="Assign",
                                           image=None)
        self.btnCancel = _widg.make_button(width=100, label="Cancel",
                                           image=None)

        # Put it all together.
        _toolbar = self._create_toolbar()

        self.notebook = self._create_notebook()

        self.vbxDataset = gtk.VBox()
        self.vbxDataset.pack_start(_toolbar, expand=False)
        self.vbxDataset.pack_start(self.notebook)

        self.notebook.connect('switch-page', self._notebook_page_switched)

    def create_tree(self):
        """
        Creates the Dataset class gtk.TreeView() and connects it to callback
        functions to handle editing.

        @return _scrollwindow: the gtk.ScrolledWindow() container holding the
                               Dataset class gtk.TreeView().
        @rtype: gtk.ScrolledWindow
        """

        self.treeview.set_tooltip_text(_(u"Displays a list of survival data "
                                         u"sets."))
        self.treeview.set_enable_tree_lines(True)
        self.treeview.set_search_column(0)
        self.treeview.set_reorderable(True)

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)

        return _scrollwindow

    def _create_toolbar(self):
        """
        Method to create the gtk.Toolbar() for the Dataset class Work Book.

        @return: _toolbar
        @rtype: gtk.Toolbar
        """

        _toolbar = gtk.Toolbar()

        _pos = 0

        _button = gtk.MenuToolButton(None, label="")
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        _button.set_icon_widget(_image)
        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"Dataset"))
        _menu_item.set_tooltip_text(_(u"Add a new data set to the open RTK "
                                      u"Program database."))
        _menu_item.connect('activate', AddDataset, self._app)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Records"))
        _menu_item.set_tooltip_text(_(u"Add a record to the selected data "
                                      u"set."))
        _menu_item.connect('activate', self._add_record)
        _menu.add(_menu_item)
        _button.set_menu(_menu)
        _menu.show_all()
        _button.show()
        _toolbar.insert(_button, _pos)
        _pos += 1

        # Remove items button.
        _button = gtk.MenuToolButton(None, label="")
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        _button.set_icon_widget(_image)
        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"Dataset"))
        _menu_item.set_tooltip_text(_(u"Removes the selected data set from "
                                      u"the open RTK Program database."))
        _menu_item.connect('activate', self._delete_data_set)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Records"))
        _menu_item.set_tooltip_text(_(u"Removes the selected record from the "
                                      u"selected data set."))
        _menu_item.connect('activate', self._delete_record)
        _menu.add(_menu_item)
        _button.set_menu(_menu)
        _menu.show_all()
        _button.show()
        _toolbar.insert(_button, _pos)
        _pos += 1

        # Consolidate results.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert-assembly.png')
        _button.set_icon_widget(_image)
        _button.set_name('Assign')
        _button.connect('clicked', self._consolidate_dataset)
        _button.set_tooltip_text(_(u"Consolidates the records in the selected "
                                   u"data set."))
        _toolbar.insert(_button, _pos)
        _pos += 1

        # Calculate button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        _button.set_icon_widget(_image)
        _button.set_name('Calculate')
        _button.connect('clicked', self._calculate)
        _button.set_tooltip_text(_(u"Analyzes the selected data set."))
        _toolbar.insert(_button, _pos)
        _pos += 1

        # Save button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.set_name('Save')
        _button.connect('clicked', self._save_dataset)
        _button.set_tooltip_text(_(u"Saves the selected data set and it's "
                                   u"records."))
        _toolbar.insert(_button, _pos)
        _pos += 1

        # Assign results to affected assembly.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/import.png')
        _button.set_icon_widget(_image)
        _button.set_name('Assign')
        _button.connect('clicked', AssignMTBFResults, self._app)
        _button.set_tooltip_text(_(u"Assigns MTBF and hazard rate results to "
                                   u"the selected assembly."))
        _toolbar.insert(_button, _pos)

        _toolbar.show()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Dataset class gtk.Notebook().

        @return: _notebook
        @rtype: gtk.Notebook
        """

        def _create_analyses_input_page(self, notebook):
            """
            Function to create the Dataset class gtk.Notebook() page for
            displaying assessment inputs for the selected data set.

            @param self: the current instance of a Dataset class.
            @param notebook: the Dataset class gtk.Notebook() widget.
            @type notebook: gtk.Notebook
            @return: False if successful or True if an error is encountered.
            @rtype: boolean
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hbox = gtk.HBox()

            self.tvwDataset.set_rubber_banding(True)
            self.tvwDataset.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add(self.tvwDataset)

            self.fraDataset.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            self.fraDataset.add(_scrollwindow)

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add(self.tvwNevadaChart)

            self.fraNevadaChart.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            self.fraNevadaChart.add(_scrollwindow)

            _hbox.pack_start(self.fraDataset, True, True)

            _fixed = gtk.Fixed()

            _frame = _widg.make_frame(label=_(u"Analyses Inputs"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
            _frame.add(_fixed)

            _hbox.pack_end(_frame, True, True)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display analysis input information. #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Load the gtk.ComboBox() widgets.
            _results = [["ALT"], [_(u"Reliability Growth")],
                        [_(u"Reliability Demonstration")], [_(u"Field")]]
            _widg.load_combo(self.cmbSource, _results)
            _results = [[u"MCF"], [u"Kaplan-Meier"], [_(u"NHPP - Power Law")],
                        [u"NHPP - Loglinear"], [_(u"Exponential")],
                        [_(u"Lognormal")], [_(u"Normal")], [u"Weibull"],
                        ["WeiBayes"]]
            _widg.load_combo(self.cmbDistribution, _results)
            _results = [["Lower One-Sided"], ["Upper One-Sided"],
                        ["Two-Sided"]]
            _widg.load_combo(self.cmbConfType, _results)
            _results = [[_(u"Crow (NHPP Only)")], [_(u"Duane (NHPP Only)")],
                        [_(u"Fisher Matrix")], [_(u"Likelihood")],
                        [_(u"Bootstrap")]]
            _widg.load_combo(self.cmbConfMethod, _results)
            _results = [["MLE"], ["Rank Regression"]]
            _widg.load_combo(self.cmbFitMethod, _results)

            # Create the Dataset treeview on the left side.
            _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_INT, gobject.TYPE_STRING)
            self.tvwDataset.set_model(_model)

            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _cell.set_property('visible', 1)
            _cell.set_property('background', 'gray')
            _column = gtk.TreeViewColumn()
            _label = _widg.make_column_heading(_(u"Record\nID"))
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=0)
            _column.set_visible(1)
            self.tvwDataset.append_column(_column)

            _types = ['text', 'float', 'float', 'int']
            _labels = [_(u"Affected\nUnit"), _(u"Left"), _(u"Right"),
                       _(u"Quantity")]
            for i in range(len(_labels)):
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('background', 'white')
                _cell.connect('edited', self._callback_entry_cell, i+1,
                              _types[i])
                _column = gtk.TreeViewColumn()
                _label = _widg.make_column_heading(_labels[i])
                _column.set_widget(_label)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i+1)
                _column.set_sort_column_id(i+1)
                self.tvwDataset.append_column(_column)

            _cell = gtk.CellRendererCombo()
            _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
            _cellmodel.append([_(u"Event")])
            _cellmodel.append([_(u"Right Censored")])
            _cellmodel.append([_(u"Left Censored")])
            _cellmodel.append([_(u"Interval Censored")])
            _cell.set_property('editable', True)
            _cell.set_property('has-entry', False)
            _cell.set_property('model', _cellmodel)
            _cell.set_property('text-column', 0)
            _cell.connect('changed', self._callback_combo_cell, 5, _model)
            _column = gtk.TreeViewColumn()
            _label = _widg.make_column_heading(_(u"Status"))
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=5)
            _column.set_visible(1)
            self.tvwDataset.append_column(_column)

            # Create the labels for the left half of the right side.
            _labels = [_("Assembly:"), _("Description:"), _("Data Source:"),
                       _("Distribution:"), _(""), _("Confidence:"),
                       _("Confidence Type:"), _("")]
            (_x_pos1, _y_pos1) = _widg.make_labels(_labels, _fixed, 5, 5)
            _x_pos1 += 35

            # Create the labels for the right half of the right side.
            _labels = [_("Start Time:"), _("End Time:"), _("Step Interval:"),
                       _(u"Start Date:"), _(u"End Date:")]
            (_x_pos2,
             _y_pos2) = _widg.make_labels(_labels, _fixed, _x_pos1 + 205, 5)
            _x_pos2 += _x_pos1
            _x_pos2 += 230

            self.cmbAssembly.set_tooltip_text(_(u"Selects and displays the "
                                                u"assembly associated with "
                                                u"the data set."))
            self.txtDescription.set_tooltip_text(_(u"Description of the "
                                                   u"selected data set."))
            self.cmbSource.set_tooltip_text(_(u"Selects and displays the "
                                              u"source of the selected data "
                                              u"set."))
            self.cmbDistribution.set_tooltip_text(_(u"Selects and displays "
                                                    u"the statistical "
                                                    u"distribution used to "
                                                    u"fit the data."))
            self.cmbFitMethod.set_tooltip_text(_(u"Selects and displays the "
                                                 u"method used to fit the "
                                                 u"data to the selected "
                                                 u"distribution."))
            self.txtConfidence.set_tooltip_text(_(u"Desired statistical "
                                                  u"confidence"))
            self.cmbConfType.set_tooltip_text(_(u"Selects and displays the "
                                                u"type of confidence bounds."))
            self.cmbConfMethod.set_tooltip_text(_(u"Selects and displays the "
                                                  u"method for developing "
                                                  u"confidence bounds."))
            self.txtStartTime.set_tooltip_text(_(u"Earliest failure time to "
                                                 u"use for calculating "
                                                 u"reliability metrics."))
            self.txtEndTime.set_tooltip_text(_(u"Latest failure time to use "
                                               u"for calculating reliability "
                                               u"metrics."))
            self.txtRelPoints.set_tooltip_text(_(u"Number of points at which "
                                                 u"to calculate reliability "
                                                 u"metrics."))
            self.txtStartDate.set_tooltip_text(_(u"Earliest failure date to "
                                                 u"use for calculating "
                                                 u"reliability metrics."))
            self.txtEndDate.set_tooltip_text(_(u"Latest failure date to use "
                                               u"for calculating reliability "
                                               u"metrics."))
            self.btnStartDate.set_tooltip_text(_(u"Launches the calendar to "
                                                 u"select the start date."))
            self.btnEndDate.set_tooltip_text(_(u"Launches the calendar to "
                                               u"select the end date."))
            self.chkGroup.set_tooltip_text(_(u"When checked, the MTBF and "
                                             u"failure intensity results will "
                                             u"be distributed to all "
                                             u"next-level child assemblies "
                                             u"according to the percentage of "
                                             u"records each assembly "
                                             u"contributes.  This assumes "
                                             u"failure times are "
                                             u"exponentially distributed."))
            self.chkParts.set_tooltip_text(_(u"When checked, the MTBF and "
                                             u"failure intensity results will "
                                             u"be distributed to all "
                                             u"components according to the "
                                             u"percentage of records each "
                                             u"component contributes.  This "
                                             u"assumes failure times are "
                                             u"exponentially distributed."))

            # Place widgets on the left side.
            _fixed.put(self.cmbAssembly, _x_pos1, _y_pos1[0])
            _fixed.put(self.txtDescription, _x_pos1, _y_pos1[1])
            _fixed.put(self.cmbSource, _x_pos1, _y_pos1[2])
            _fixed.put(self.cmbDistribution, _x_pos1, _y_pos1[3])
            _fixed.put(self.lblFitMethod, 5, _y_pos1[4])
            _fixed.put(self.cmbFitMethod, _x_pos1, _y_pos1[4])
            _fixed.put(self.txtConfidence, _x_pos1, _y_pos1[5])
            _fixed.put(self.cmbConfType, _x_pos1, _y_pos1[6])
            _fixed.put(self.lblConfMethod, 5, _y_pos1[7])
            _fixed.put(self.cmbConfMethod, _x_pos1, _y_pos1[7])

            # Place widgets on the right side.
            _fixed.put(self.txtStartTime, _x_pos2, _y_pos2[0])
            _fixed.put(self.txtEndTime, _x_pos2, _y_pos2[1])
            _fixed.put(self.txtRelPoints, _x_pos2, _y_pos2[2])
            _fixed.put(self.txtStartDate, _x_pos2, _y_pos2[3])
            _fixed.put(self.btnStartDate, _x_pos2 + 105, _y_pos2[3])
            _fixed.put(self.txtEndDate, _x_pos2, _y_pos2[4])
            _fixed.put(self.btnEndDate, _x_pos2 + 105, _y_pos2[4])
            _fixed.put(self.chkGroup, _x_pos2, _y_pos2[4] + 30)
            _fixed.put(self.chkParts, _x_pos2, _y_pos2[4] + 60)

            _fixed.show_all()

            self.cmbAssembly.connect('changed', self._callback_combo, 1)
            self.cmbSource.connect('changed', self._callback_combo, 3)
            self.cmbDistribution.connect('changed', self._callback_combo, 4)
            self.cmbConfType.connect('changed', self._callback_combo, 6)
            self.cmbConfMethod.connect('changed', self._callback_combo, 7)
            self.cmbFitMethod.connect('changed', self._callback_combo, 8)
            self.txtDescription.connect('focus-out-event',
                                        self._callback_entry, 'text', 2)
            self.txtConfidence.connect('focus-out-event',
                                       self._callback_entry, 'float', 5)
            self.txtStartTime.connect('focus-out-event',
                                      self._callback_entry, 'float', 34)
            self.txtEndTime.connect('focus-out-event',
                                    self._callback_entry, 'float', 9)
            self.txtRelPoints.connect('focus-out-event',
                                      self._callback_entry, 'int', 10)
            self.txtStartDate.connect('focus-out-event',
                                      self._callback_entry, 'date', 35)
            self.txtStartDate.connect('changed', self._callback_entry, None,
                                      'date', 35)
            self.txtEndDate.connect('focus-out-event',
                                    self._callback_entry, 'date', 36)
            self.txtEndDate.connect('changed', self._callback_entry, None,
                                    'date', 36)
            self.btnStartDate.connect('released', _util.date_select,
                                      self.txtStartDate)
            self.btnEndDate.connect('released', _util.date_select,
                                    self.txtEndDate)

            self.chkGroup.hide()
            self.chkParts.hide()

            # Insert the tab.
            _label = gtk.Label()
            _label.set_markup("<span weight='bold'>" +
                              _(u"Analysis\nInputs") + "</span>")
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.show_all()
            _label.set_tooltip_text(_(u"Displays analysis inputs for the "
                                      u"selected dataset."))
            notebook.insert_page(_hbox, tab_label=_label, position=-1)

            return False

        def _create_analyses_results_page(self, notebook):
            """
            Function to create the Dataset class gtk.Notebook() page for
            displaying assessment results for the selected data set.

            @param self: the current instance of a Dataset class.
            @param notebook: the Dataset class gtk.Notebook() widget.
            @type notebook: gtk.Notebook
            @return: False if successful or True if an error is encountered.
            @rtype: boolean
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            self.hpnAnalysisResults.pack1(self.vpnAnalysisResults)

            self.fraSummary.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            self.vpnAnalysisResults.pack1(self.fraSummary)

            self.fraNonParStats.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            self.vpnAnalysisResults.pack2(self.fraNonParStats)

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add(self.tvwNonParResults)
            self.fraNonParEst.add(_scrollwindow)
            self.fraNonParEst.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

            self.hpnAnalysisResults.pack2(self.fraNonParEst)

            self.fraParStats.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

            self.lblScale.set_use_markup(True)
            self.lblShape.set_use_markup(True)
            self.lblLocation.set_use_markup(True)
            self.lblMHBResult.set_use_markup(True)
            self.lblZLPResult.set_use_markup(True)
            self.lblZLRResult.set_use_markup(True)
            self.lblRhoResult.set_use_markup(True)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display analysis results.           #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            self.txtMHB.set_tooltip_markup(_(u"Displays the value of the "
                                             u"MIL-HDBK test for trend."))
            self.txtChiSq.set_tooltip_markup(_(u"Displays the chi square "
                                               u"critical value for the "
                                               u"MIL-HDBK test for trend."))
            self.txtMHBPValue.set_tooltip_markup(_(u"Displays the p-value for "
                                                   u"the MIL-HDBK test for "
                                                   u"trend."))
            self.txtLP.set_tooltip_markup(_(u"Displays the value of the "
                                            u"LaPlace test for trend."))
            self.txtZLPNorm.set_tooltip_markup(_(u"Displays the standard "
                                                 u"normal critical value for "
                                                 u"the LaPlace test for "
                                                 u"trend."))
            self.txtZLPPValue.set_tooltip_markup(_(u"Displays the p-value for "
                                                   u"the Laplace test for "
                                                   u"trend."))
            self.txtLR.set_tooltip_markup(_(u"Displays the value of the "
                                            u"Lewis-Robinson test for trend."))
            self.txtZLRNorm.set_tooltip_markup(_(u"Displays the standard "
                                                 u"normal critical value for "
                                                 u"the Lewis-Robinson test "
                                                 u"for trend."))
            self.txtZLRPValue.set_tooltip_markup(_(u"Displays the p-value for "
                                                   u"the Lewis-Robinson test "
                                                   u"for trend."))
            self.txtRho.set_tooltip_markup(_(u"Displays the value of the lag "
                                             u"1 sample serial correlation "
                                             u"coefficient."))
            self.txtRhoNorm.set_tooltip_markup(_(u"Displays the standard "
                                                 u"normal critical value for "
                                                 u"the lag 1 sample serial "
                                                 u"correlation coefficient."))
            self.txtRhoPValue.set_tooltip_markup(_(u"Displays the p-value for "
                                                   u"the lag 1 sample serial "
                                                   u"correlation "
                                                   u"coefficient."))
            self.txtScale.set_tooltip_markup(_(u"Displays the point estimate "
                                               u"of the scale parameter."))
            self.txtScaleLL.set_tooltip_markup(_(u"Displays the lower "
                                                 u"<span>\u03B1</span>% bound "
                                                 u"on the scale parameter."))
            self.txtScaleUL.set_tooltip_markup(_(u"Displays the upper "
                                                 u"<span>\u03B1</span>% bound "
                                                 u"on the scale parameter."))
            self.txtShape.set_tooltip_markup(_(u"Displays the point estimate "
                                               u"of the shape parameter."))
            self.txtShapeLL.set_tooltip_markup(_(u"Displays the lower "
                                                 u"<span>\u03B1</span>% bound "
                                                 u"on the shape parameter."))
            self.txtShapeUL.set_tooltip_markup(_(u"Displays the upper "
                                                 u"<span>\u03B1</span>% bound "
                                                 u"on the shape parameter."))
            self.txtLocation.set_tooltip_markup(_(u"Displays the point "
                                                  u"estimate of the location "
                                                  u"parameter."))
            self.txtLocationLL.set_tooltip_markup(_(u"Displays the lower "
                                                    u"<span>\u03B1</span>% "
                                                    u"bound on the location "
                                                    u"parameter."))
            self.txtLocationUL.set_tooltip_markup(_(u"Displays the upper "
                                                    u"<span>\u03B1</span>% "
                                                    u"bound on the location "
                                                    u"parameter."))
            self.txtShapeShape.set_tooltip_markup(_(u"Displays the variance "
                                                    u"of the shape "
                                                    u"parameter."))
            self.txtShapeScale.set_tooltip_markup(_(u"Displays the covariance "
                                                    u"of the shape and scale "
                                                    u"parameters."))
            self.txtShapeLocation.set_tooltip_markup(_(u"Displays the "
                                                       u"covariance of the "
                                                       u"shape and location"
                                                       u" parameters."))
            self.txtScaleShape.set_tooltip_markup(_(u"Displays the covariance "
                                                    u"of the scale and shape "
                                                    u"parameters."))
            self.txtScaleScale.set_tooltip_markup(_(u"Displays the variance "
                                                    u"of the scale "
                                                    u"parameter."))
            self.txtScaleLocation.set_tooltip_markup(_(u"Displays the "
                                                       u"covariance of the "
                                                       u"scale and location "
                                                       u"parameters."))
            self.txtLocationShape.set_tooltip_markup(_(u"Displays the "
                                                       u"covariance of the "
                                                       u"location and shape "
                                                       u"parameters."))
            self.txtLocationScale.set_tooltip_markup(_(u"Displays the "
                                                       u"covariance of the "
                                                       u"location and scale "
                                                       u"parameters."))
            self.txtLocationLocation.set_tooltip_markup(_(u"Displays the "
                                                          u"variance of the "
                                                          u"location "
                                                          u"parameter."))
            self.txtAIC.set_tooltip_markup(_(u"Displays the value of Aikike's "
                                             u"information criterion."))
            self.txtBIC.set_tooltip_markup(_(u"Displays the value of Bayes' "
                                             u"information criterion."))
            self.txtMLE.set_tooltip_markup(_(u"Displays the likelihood "
                                             u"value."))
            self.txtNumSuspensions.set_tooltip_markup(_(u"Displays the number "
                                                        u"of suspensions in "
                                                        u"the data set."))
            self.txtNumFailures.set_tooltip_markup(_(u"Displays the number of "
                                                     u"failures in the dat "
                                                     u"set."))
            self.txtMTBF.set_tooltip_markup(_(u"Displays the point estimate "
                                              u"of the MTBF."))
            self.txtMTBFLL.set_tooltip_markup(_(u"Displays the lower "
                                                u"<span>\u03B1</span>% bound "
                                                u"on the MTBF."))
            self.txtMTBFUL.set_tooltip_markup(_(u"Displays the upper "
                                                u"<span>\u03B1</span>% bound "
                                                u"on the MTBF."))
            self.txtHazardRate.set_tooltip_markup(_(u"Displays the point "
                                                    u"estimate of the hazard "
                                                    u"rate."))
            self.txtHazardRateLL.set_tooltip_markup(_(u"Displays the lower "
                                                      u"<span>\u03B1</span>% "
                                                      u"bound on the hazard "
                                                      u"rate."))
            self.txtHazardRateUL.set_tooltip_markup(_(u"Displays the upper "
                                                      u"<span>\u03B1</span>% "
                                                      u"bound on the hazard "
                                                      u"rate."))
            self.txtMTBFi.set_tooltip_markup(_(u"Displays the point estimate "
                                               u"of the instantaneous MTBF."))
            self.txtMTBFiLL.set_tooltip_markup(_(u"Displays the lower "
                                                 u"<span>\u03B1</span>% bound "
                                                 u"on the instantaneous "
                                                 u"MTBF."))
            self.txtMTBFiUL.set_tooltip_markup(_(u"Displays the upper "
                                                 u"<span>\u03B1</span>% bound "
                                                 u"on the instantaneous "
                                                 u"MTBF."))
            self.txtHazardRatei.set_tooltip_markup(_(u"Displays the point "
                                                     u"estimate the "
                                                     u"instantaneous failure "
                                                     u"intensity."))
            self.txtHazardRateiLL.set_tooltip_markup(_(u"Displays the lower "
                                                       u"<span>\u03B1</span>% "
                                                       u"bound on the "
                                                       u"instantaneous "
                                                       u"failure intensity."))
            self.txtHazardRateiUL.set_tooltip_markup(_(u"Displays the upper "
                                                       u"<span>\u03B1</span>% "
                                                       u"bound on the "
                                                       u"instantaneous "
                                                       u"failure intensity."))

            # Build the summary of results container.  The summary is used for
            # all analyses.
            _fixed = gtk.Fixed()
            _labels = [_(u"Number of Suspensions:"), _(u"Number of Failures:"),
                       _(u"LCL"), _(u"Estimate"), _(u"UCL")]
            (_x_pos, _y_pos) = _widg.make_labels(_labels[0:2], _fixed, 5, 5)
            _x_pos = max(_x_pos, self.lblCumMTBF.size_request()[0])
            _x_pos = max(_x_pos, self.lblMTBFi.size_request()[0])
            _x_pos = max(_x_pos, self.lblCumFI.size_request()[0])
            _x_pos = max(_x_pos, self.lblFIi.size_request()[0])
            _x_pos += 25

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fixed)
            self.fraSummary.add(_scrollwindow)

            _fixed.put(self.txtNumSuspensions, _x_pos, _y_pos[0])
            _fixed.put(self.txtNumFailures, _x_pos, _y_pos[1])

            _label = _widg.make_label(_labels[2], width=150)
            _fixed.put(_label, _x_pos, _y_pos[1] + 30)
            _label = _widg.make_label(_labels[3], width=150)
            _fixed.put(_label, _x_pos + 105, _y_pos[1] + 30)
            _label = _widg.make_label(_labels[4], width=150)
            _fixed.put(_label, _x_pos + 210, _y_pos[1] + 30)

            _fixed.put(self.lblCumMTBF, 5, _y_pos[1] + 60)
            _fixed.put(self.txtMTBFLL, _x_pos, _y_pos[1] + 60)
            _fixed.put(self.txtMTBF, _x_pos + 105, _y_pos[1] + 60)
            _fixed.put(self.txtMTBFUL, _x_pos + 210, _y_pos[1] + 60)
            _fixed.put(self.lblModel, _x_pos + 315, _y_pos[1] + 60)

            _fixed.put(self.lblMTBFi, 5, _y_pos[1] + 90)
            _fixed.put(self.txtMTBFiLL, _x_pos, _y_pos[1] + 90)
            _fixed.put(self.txtMTBFi, _x_pos + 105, _y_pos[1] + 90)
            _fixed.put(self.txtMTBFiUL, _x_pos + 210, _y_pos[1] + 90)

            _fixed.put(self.lblCumFI, 5, _y_pos[1] + 120)
            _fixed.put(self.txtHazardRateUL, _x_pos, _y_pos[1] + 120)
            _fixed.put(self.txtHazardRate, _x_pos + 105, _y_pos[1] + 120)
            _fixed.put(self.txtHazardRateLL, _x_pos + 210, _y_pos[1] + 120)

            _fixed.put(self.lblFIi, 5, _y_pos[1] + 150)
            _fixed.put(self.txtHazardRateiLL, _x_pos, _y_pos[1] + 150)
            _fixed.put(self.txtHazardRatei, _x_pos + 105, _y_pos[1] + 150)
            _fixed.put(self.txtHazardRateiUL, _x_pos + 210, _y_pos[1] + 150)

            # Build the non-parametric goodness of fit statistics container.
            _fixed = gtk.Fixed()
            _labels = [_(u"MIL\nHandbook"), _(u"Laplace"),
                       _(u"Lewis\nRobinson"),
                       _(u"Serial\nCorrelation\nCoefficient")]
            (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 30)
            _x_pos += 20

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fixed)
            self.fraNonParStats.add(_scrollwindow)

            _label = _widg.make_label(_(u"Test Statistic"), width=150)
            _fixed.put(_label, _x_pos + 5, 5)
            _fixed.put(self.txtMHB, _x_pos + 5, _y_pos[0])
            _fixed.put(self.txtLP, _x_pos + 5, _y_pos[1])
            _fixed.put(self.txtLR, _x_pos + 5, _y_pos[2])
            _fixed.put(self.txtRho, _x_pos + 5, _y_pos[3])

            _label = _widg.make_label(_(u"Critical Value"), width=150)
            _fixed.put(_label, _x_pos + 105, 5)
            _fixed.put(self.txtChiSq, _x_pos + 105, _y_pos[0])
            _fixed.put(self.txtZLPNorm, _x_pos + 105, _y_pos[1])
            _fixed.put(self.txtZLRNorm, _x_pos + 105, _y_pos[2])
            _fixed.put(self.txtRhoNorm, _x_pos + 105, _y_pos[3])

            _label = _widg.make_label(_(u"p-Value"), width=150)
            _fixed.put(_label, _x_pos + 210, 5)
            _fixed.put(self.txtMHBPValue, _x_pos + 210, _y_pos[0])
            _fixed.put(self.txtZLPPValue, _x_pos + 210, _y_pos[1])
            _fixed.put(self.txtZLRPValue, _x_pos + 210, _y_pos[2])
            _fixed.put(self.txtRhoPValue, _x_pos + 210, _y_pos[3])

            _fixed.put(self.lblMHBResult, _x_pos + 315, _y_pos[0])
            _fixed.put(self.lblZLPResult, _x_pos + 315, _y_pos[1])
            _fixed.put(self.lblZLRResult, _x_pos + 315, _y_pos[2])
            _fixed.put(self.lblRhoResult, _x_pos + 315, _y_pos[3])

            # Build the parametric statistics container.
            _fixed = gtk.Fixed()
            _x_pos = max(self.lblScale.size_request()[0],
                         self.lblShape.size_request()[0])
            _x_pos = max(_x_pos, self.lblLocation.size_request()[0])
            _x_pos = max(_x_pos, self.lblRowScale.size_request()[0])
            _x_pos = max(_x_pos, self.lblRowShape.size_request()[0])
            _x_pos = max(_x_pos, self.lblRowLocation.size_request()[0])
            _x_pos += 20

            _y_inc = max(self.lblScale.size_request()[1], 25) + 5
            _y_pos = [_y_inc]
            _y_inc += max(self.lblShape.size_request()[1], 25) + 5
            _y_pos.append(_y_inc)
            _y_inc += max(self.lblLocation.size_request()[1], 25) + 5
            _y_pos.append(_y_inc)
            _y_inc += max(self.lblRowScale.size_request()[1], 55) + 5
            _y_pos.append(_y_inc)
            _y_inc += max(self.lblRowShape.size_request()[1], 25) + 5
            _y_pos.append(_y_inc)
            _y_inc += max(self.lblRowLocation.size_request()[1], 25) + 5
            _y_pos.append(_y_inc)

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fixed)
            self.fraParStats.add(_scrollwindow)

            # Place the parameter estimates widgets.
            _label = _widg.make_label(_(u"LCL"), width=150)
            _fixed.put(_label, _x_pos, 5)
            _label = _widg.make_label(_(u"Estimate"), width=150)
            _fixed.put(_label, _x_pos + 105, 5)
            _label = _widg.make_label(_(u"UCL"), width=150)
            _fixed.put(_label, _x_pos + 210, 5)

            _fixed.put(self.lblScale, 5, _y_pos[0])
            _fixed.put(self.txtScaleLL, _x_pos, _y_pos[0])
            _fixed.put(self.txtScale, _x_pos + 105, _y_pos[0])
            _fixed.put(self.txtScaleUL, _x_pos + 210, _y_pos[0])

            _fixed.put(self.lblShape, 5, _y_pos[1])
            _fixed.put(self.txtShapeLL, _x_pos, _y_pos[1])
            _fixed.put(self.txtShape, _x_pos + 105, _y_pos[1])
            _fixed.put(self.txtShapeUL, _x_pos + 210, _y_pos[1])

            _fixed.put(self.lblLocation, 5, _y_pos[2])
            _fixed.put(self.txtLocationLL, _x_pos, _y_pos[2])
            _fixed.put(self.txtLocation, _x_pos + 105, _y_pos[2])
            _fixed.put(self.txtLocationUL, _x_pos + 210, _y_pos[2])

            # Place the variance-covariance matrix.
            _fixed.put(self.lblColScale, _x_pos, _y_pos[2] + 30)
            _fixed.put(self.lblColShape, _x_pos + 105, _y_pos[2] + 30)
            _fixed.put(self.lblColLocation, _x_pos + 210, _y_pos[2] + 30)

            _fixed.put(self.lblRowScale, 5, _y_pos[3])
            _fixed.put(self.txtScaleScale, _x_pos, _y_pos[3])
            _fixed.put(self.txtScaleShape, _x_pos + 105, _y_pos[3])
            _fixed.put(self.txtScaleLocation, _x_pos + 210, _y_pos[3])

            _fixed.put(self.lblRowShape, 5, _y_pos[4])
            _fixed.put(self.txtShapeScale, _x_pos, _y_pos[4])
            _fixed.put(self.txtShapeShape, _x_pos + 105, _y_pos[4])
            _fixed.put(self.txtShapeLocation, _x_pos + 210, _y_pos[4])

            _fixed.put(self.lblRowLocation, 5, _y_pos[5])
            _fixed.put(self.txtLocationScale, _x_pos, _y_pos[5])
            _fixed.put(self.txtLocationShape, _x_pos + 105, _y_pos[5])
            _fixed.put(self.txtLocationLocation, _x_pos + 210, _y_pos[5])

            # Place the parametric goodness of fit statistics.
            _fixed.put(self.lblAIC, 5, _y_pos[5] + 30)
            _fixed.put(self.lblBIC, 5, _y_pos[5] + 60)
            _fixed.put(self.lblMLE, 5, _y_pos[5] + 90)
            _fixed.put(self.txtAIC, _x_pos, _y_pos[5] + 30)
            _fixed.put(self.txtBIC, _x_pos, _y_pos[5] + 60)
            _fixed.put(self.txtMLE, _x_pos, _y_pos[5] + 90)

            _fixed.show_all()

            self.lblModel.hide()

            # Insert the tab.
            _label = gtk.Label()
            _label.set_markup("<span weight='bold'>" +
                              _(u"Analysis\nResults") + "</span>")
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.show_all()
            _label.set_tooltip_text(_(u"Displays analysis results for the "
                                      u"selected dataset."))
            notebook.insert_page(self.hpnAnalysisResults, tab_label=_label,
                                 position=-1)

            return False

        def _create_plot_page(self, notebook):
            """
            Function to create the Dataset class gtk.Notebook() page for
            displaying plots for the selected data set.

            @param self: the current instance of a Dataset class.
            @param notebook: the Dataset class gtk.Notebook() widget.
            @type notebook: gtk.Notebook
            @return: False if successful or True if an error is encountered.
            @rtype: boolean
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hbox = gtk.HBox()

            _frame = _widg.make_frame(label=_(u"Survival Analysis Plots"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_hbox)
            _frame.show_all()

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display general information.        #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hbox.pack_start(self.vbxPlot1)

            self.vbxPlot1.pack_start(self.pltPlot1)
            self.vbxPlot1.pack_start(self.pltPlot3)

            _hbox.pack_start(self.vbxPlot2)

            self.vbxPlot2.pack_start(self.pltPlot2)
            self.vbxPlot2.pack_start(self.pltPlot4)

            # Insert the page.
            _label = gtk.Label()
            _label.set_markup("<span weight='bold'>Analysis\nPlots</span>")
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.show_all()
            _label.set_tooltip_text(_(u"Displays survival analyses plots."))
            notebook.insert_page(_frame, tab_label=_label, position=-1)

            return False

        def _create_results_breakdown_page(self, notebook):
            """
            Function to create the Dataset class gtk.Notebook() page for
            displaying results decomposed to child assemblies and/or components
            for the selected data set.

            @param self: the current instance of a Dataset class.
            @param notebook: the Dataset class gtk.Notebook() widget.
            @type notebook: gtk.Notebook
            @return: False if successful or True if an error is encountered.
            @rtype: boolean
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hpaned = gtk.HPaned()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add(self.tvwResultsByChildAssembly)

            self.fraResultsByChildAssembly.add(_scrollwindow)

            _hpaned.pack1(self.fraResultsByChildAssembly, True, True)

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add(self.tvwResultsByPart)

            self.fraResultsByPart.add(_scrollwindow)

            _hpaned.pack2(self.fraResultsByPart, True, True)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display general information.        #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Table of results allocated to each assembly.
            _model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                                   gobject.TYPE_INT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_STRING)
            self.tvwResultsByChildAssembly.set_model(_model)

            _labels = [_(u"Hardware\nItem"), _(u"Number of\nFailures"), _(u""),
                       _(u"MTBF\nLower Bound"), _(u"MTBF"),
                       _(u"MTBF\nUpper Bound"),
                       _(u"Failure Intensity\nLower Bound"),
                       _(u"Failure\nIntensity"),
                       _(u"Failure Intensity\nUpper Bound")]
            for i in range(len(_labels)):
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _column = gtk.TreeViewColumn()
                _label = _widg.make_column_heading(_labels[i])
                _column.set_widget(_label)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i, background=9)
                _column.set_clickable(True)
                _column.set_resizable(True)
                _column.set_sort_column_id(i)
                self.tvwResultsByChildAssembly.append_column(_column)

            # Table of results allocated to each part.
            _model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_STRING)
            self.tvwResultsByPart.set_model(_model)

            self.tvwResultsByPart.columns_autosize()
            self.tvwResultsByPart.set_headers_clickable(True)
            self.tvwResultsByPart.set_reorderable(True)

            _labels = [_(u"Part\nNumber"), _(u"Number of\nFailures"), _(u""),
                       _(u"MTBF\nLower Bound"), _(u"MTBF"),
                       _(u"MTBF\nUpper Bound"),
                       _(u"Failure Intensity\nLower Bound"),
                       _(u"Failure\nIntensity"),
                       _(u"Failure Intensity\nUpper Bound")]
            for i in range(len(_labels)):
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _column = gtk.TreeViewColumn()
                _label = _widg.make_column_heading(_labels[i])
                _column.set_widget(_label)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i, background=8)
                _column.set_clickable(True)
                _column.set_sort_column_id(i)
                self.tvwResultsByPart.append_column(_column)

            # Insert the tab.
            _label = gtk.Label()
            _label.set_markup("<span weight='bold'>" +
                              _(u"Results\nBreakdowns") + "</span>")
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.show_all()
            _label.set_tooltip_text(_(u"Displays analysis results for the "
                                      u"selected data set broken down by "
                                      u"child assembly and part number."))
            notebook.insert_page(_hpaned, tab_label=_label, position=-1)

            return False

        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if _conf.TABPOS[2] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif _conf.TABPOS[2] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif _conf.TABPOS[2] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        _create_analyses_input_page(self, _notebook)
        _create_analyses_results_page(self, _notebook)
        _create_plot_page(self, _notebook)
        _create_results_breakdown_page(self, _notebook)

        return _notebook

    def load_tree(self):
        """
        Loads the Dataset class gtk.TreeModel().

        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

# TODO: Add revision information to data sets.
        _query = "SELECT * FROM tbl_dataset"
        _results = self._app.DB.execute_query(_query, None, self._app.ProgCnx)
        try:
            self.n_datasets = len(_results)
        except TypeError:
            self.n_datasets = 0

        # Load the model with the returned results.
        _model.clear()
        for i in range(self.n_datasets):
            _model.append(None, _results[i])

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        if _model.get_iter_root() is not None:
            _path = _model.get_path(_model.get_iter_root())
            _col = self.treeview.get_column(0)
            self.treeview.row_activated(_path, _col)

        # Load the Assembly combo.
        _query = "SELECT fld_name, fld_assembly_id, fld_description \
                  FROM tbl_system"
        _results = self._app.DB.execute_query(_query, None, self._app.ProgCnx)
        _widg.load_combo(self.cmbAssembly, _results, simple=False)

        return False

    def load_notebook(self):
        """
        Method to load the Dataset class gtk.Notebook().

        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        def _load_analyses_input_page(self):
            """
            Loads the widgets with analyses input data for the Dataset class.
            """

            # Load the affected assembly gtk.ComboBox()
            _index = 0
            _model = self.cmbAssembly.get_model()
            _row = _model.get_iter_root()
            while _row is not None:
                if _model.get_value(_row, 1) == str(self.assembly_id):
                    break
                else:
                    _row = _model.iter_next(_row)
                    _index += 1

            self.cmbAssembly.set_active(_index)
            if _index in [1, 2, 3]:
                self.chkGroup.show()
                self.chkParts.show()
            else:
                self.chkGroup.hide()
                self.chkParts.hide()

            self.cmbSource.set_active(self.source)
            self.cmbDistribution.set_active(self.distribution_id)
            self.cmbConfType.set_active(self.confidence_type)
            self.cmbConfMethod.set_active(self.confidence_method)
            self.cmbFitMethod.set_active(self.fit_method)

            self.txtDescription.set_text(self.description)
            self.txtConfidence.set_text(str(self.confidence))
            self.txtStartTime.set_text(str(self.start_time))
            self.txtEndTime.set_text(str(self.end_time))
            self.txtRelPoints.set_text(str(self.n_rel_points))

            _start_date = _util.ordinal_to_date(self.start_date)
            _end_date = _util.ordinal_to_date(self.end_date)
            self.txtStartDate.set_text(str(_start_date))
            self.txtEndDate.set_text(str(_end_date))

            self._load_dataset_tree()

            if self._nevada_chart != 0:
                self._load_nevada_chart()

            return False

        (_model, _row) = self.treeview.get_selection().get_selected()

        if _row is not None:
            _load_analyses_input_page(self)
            self.load_analyses_results_page()
            #self._load_component_list()

        if self._app.winWorkBook.get_child() is not None:
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxDataset)
        self._app.winWorkBook.show_all()

        if self._nevada_chart:
            self.fraNevadaChart.show_all()
        else:
            self.fraNevadaChart.hide_all()

        _title = _(u"RTK Work Book: Program Survival Analyses "
                   u"(%d Datasets)") % self.n_datasets
        self._app.winWorkBook.set_title(_title)

        self.notebook.set_current_page(0)

        return False

    def load_analyses_results_page(self):
        """
        Loads the gtk.Widgets() with analyses results for the Dataset class.

        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        # Clear the page.
        for _child in self.hpnAnalysisResults.get_children():
            self.hpnAnalysisResults.remove(_child)
        for _child in self.vpnAnalysisResults.get_children():
            self.vpnAnalysisResults.remove(_child)

        # Hide widgets that are not used for all analyses.  These will be
        # show as appropriate for the analysis results being loaded.
        self.lblMTBFi.hide()
        self.lblFIi.hide()
        self.lblRhoResult.hide()
        self.txtMTBFiLL.hide()
        self.txtMTBFi.hide()
        self.txtMTBFiUL.hide()
        self.txtHazardRateiLL.hide()
        self.txtHazardRatei.hide()
        self.txtHazardRateiUL.hide()
        self.lblModel.hide()

        # Hide the parameter estimate widgets.
        self.lblLocation.hide()
        self.txtLocation.hide()
        self.txtLocationLL.hide()
        self.txtLocationUL.hide()

        # Hide the variance-covariance matrix widgets.
        self.lblRowScale.hide()
        self.lblRowShape.hide()
        self.lblRowLocation.hide()
        self.lblColScale.hide()
        self.lblColShape.hide()
        self.lblColLocation.hide()
        self.txtScaleScale.hide()
        self.txtShapeShape.hide()
        self.txtLocationLocation.hide()
        self.txtShapeScale.hide()
        self.txtScaleShape.hide()
        self.txtScaleLocation.hide()
        self.txtLocationScale.hide()
        self.txtShapeLocation.hide()
        self.txtLocationShape.hide()

        # Hide the non-parametric GoF statistic widgets.
        self.lblRhoResult.hide()
        self.txtRho.hide()
        self.txtRhoNorm.hide()
        self.txtRhoPValue.hide()

        # Hide the parametric GoF statistic widgets.
        self.lblAIC.hide()
        self.lblBIC.hide()
        self.lblMLE.hide()
        self.txtAIC.hide()
        self.txtBIC.hide()
        self.txtMLE.hide()

        self.hpnAnalysisResults.pack1(self.vpnAnalysisResults, True, True)
        self.vpnAnalysisResults.pack1(self.fraSummary, True, True)

        # Update summary information.
        self.txtNumSuspensions.set_text(str(self.n_suspensions))
        self.txtNumFailures.set_text(str(self.n_failures))

        # Update mean cumulative function information.
        if self.distribution_id == 1:
            self.hpnAnalysisResults.pack2(self.fraNonParEst, True, True)
            self.vpnAnalysisResults.pack2(self.fraNonParStats, True, True)

            self.txtMHB.set_text(str(fmt.format(self.mhb)))
            self.txtLP.set_text(str(fmt.format(self.lp)))
            self.txtLR.set_text(str(fmt.format(self.lr)))

            self.lblCumMTBF.set_markup(_(u"<span>MTBF:</span>"))
            self.lblCumFI.set_markup(_(u"<span>Failure Intensity:</span>"))

            # Show widgets specific to MCF.
            self.lblRhoResult.show()
            self.txtRho.show()
            self.txtRhoNorm.show()
            self.txtRhoPValue.show()

        # Update Kaplan-Meier analysis information.
        elif self.distribution_id == 2:
            self.hpnAnalysisResults.pack2(self.fraNonParEst, True, True)
            self.vpnAnalysisResults.pack2(self.fraNonParStats, True, True)

            self.lblCumMTBF.set_markup(_(u"<span>MTBF</span>"))
            self.lblCumFI.set_markup(_(u"<span>Failure\nIntensity</span>"))

        # Update NHPP Power Law analysis information.
        elif self.distribution_id == 3:
            self.hpnAnalysisResults.pack2(self.fraNonParEst, True, True)
            self.vpnAnalysisResults.pack2(self.fraParStats, True, True)

            _b_hat = str(fmt.format(self.scale[0]))
            _alpha_hat = str(fmt.format(self.shape[0]))
            self.lblModel.set_markup(_(u"<span>MTBF<sub>C</sub> = "
                                       u"%s T<sup>%s</sup></span>") %
                                     (_b_hat, _alpha_hat))

            self.txtScale.set_text(str(fmt.format(self.scale[0])))
            self.txtScaleLL.set_text(str(fmt.format(self.scale[1])))
            self.txtScaleUL.set_text(str(fmt.format(self.scale[2])))
            self.txtShape.set_text(str(fmt.format(self.shape[0])))
            self.txtShapeLL.set_text(str(fmt.format(self.shape[1])))
            self.txtShapeUL.set_text(str(fmt.format(self.shape[2])))

            self.lblCumMTBF.set_markup(_(u"<span>Cumulative MTBF:</span>"))
            self.lblMTBFi.set_markup(_(u"<span>Instantaneous MTBF:</span>"))
            self.lblCumFI.set_markup(_(u"<span>Cumulative Failure Intensity:"
                                       u"</span>"))
            self.lblFIi.set_markup(_(u"<span>Instantaneous Failure Intensity:"
                                     u"</span>"))
            self.lblScale.set_markup(_(u"b"))
            self.lblShape.set_markup(_(u"\u03B1"))

            # Show widgets necessary for NHPP Power Law results.
            self.lblMTBFi.show()
            self.txtMTBFiLL.show()
            self.txtMTBFi.show()
            self.txtMTBFiUL.show()
            self.lblFIi.show()
            self.txtHazardRateiLL.show()
            self.txtHazardRatei.show()
            self.txtHazardRateiUL.show()
            self.lblModel.show()

        # Update parametric analysis information.
        else:
            self.vpnAnalysisResults.pack2(self.fraParStats, True, True)

            self.txtScale.set_text(str(fmt.format(self.scale[0])))
            self.txtScaleLL.set_text(str(fmt.format(self.scale[1])))
            self.txtScaleUL.set_text(str(fmt.format(self.scale[2])))
            self.txtShape.set_text(str(fmt.format(self.shape[0])))
            self.txtShapeLL.set_text(str(fmt.format(self.shape[1])))
            self.txtShapeUL.set_text(str(fmt.format(self.shape[2])))
            self.txtLocation.set_text(str(fmt.format(self.location[0])))
            self.txtLocationLL.set_text(str(fmt.format(self.location[1])))
            self.txtLocationUL.set_text(str(fmt.format(self.location[2])))
            # Scale variance.
            self.txtScaleScale.set_text(str(fmt.format(self.variance[0])))
            # Shape variance.
            self.txtShapeShape.set_text(str(fmt.format(self.variance[1])))
            # Location variance.
            self.txtLocationLocation.set_text(
                str(fmt.format(self.variance[2])))
            # Shape-scale covariance.
            self.txtShapeScale.set_text(str(fmt.format(self.covariance[0])))
            # Scale-shape covariance.
            self.txtScaleShape.set_text(str(fmt.format(self.covariance[0])))
            # Scale-location covariance.
            self.txtScaleLocation.set_text(str(fmt.format(self.covariance[1])))
            # Location-scale covariance.
            self.txtLocationScale.set_text(str(fmt.format(self.covariance[1])))
            # Shape-location covariance.
            self.txtShapeLocation.set_text(str(fmt.format(self.covariance[2])))
            # Location-shape covariance.
            self.txtLocationShape.set_text(str(fmt.format(self.covariance[2])))
            self.txtAIC.set_text(str(fmt.format(self.aic)))
            self.txtBIC.set_text(str(fmt.format(self.bic)))
            self.txtMLE.set_text(str(fmt.format(self.mle)))

            self.lblScale.set_markup(_(u"<span>Scale</span>"))
            self.lblShape.set_markup(_(u"<span>Shape</span>"))
            self.lblLocation.show()

        return False

    def _load_dataset_tree(self):
        """
        Method used to load the survival data set in the gtk.TreeView().

        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        # Load the gtk.TreeView() containing the list of failure/censoring
        # times.
        _query = "SELECT fld_record_id, fld_unit, fld_left_interval, \
                         fld_right_interval, fld_quantity, fld_status \
                  FROM tbl_survival_data \
                  WHERE fld_dataset_id=%s \
                  ORDER BY fld_unit ASC, \
                           fld_left_interval ASC" % self.dataset_id
        _results = self._app.DB.execute_query(_query, None, self._app.ProgCnx)

        try:
            _n_events = len(_results)
        except TypeError:
            _n_events = 0

        _model = self.tvwDataset.get_model()
        _model.clear()
        for i in range(_n_events):
            _model.append([_results[i][0], _results[i][1], _results[i][2],
                           _results[i][3], _results[i][4], _results[i][5]])

        return False

    def _load_nevada_chart(self):
        """
        Method to load the Nevada chart if one is associated with the selected
        data set.

        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        import pango
        from datetime import date, datetime

        _nevada = {}

        _query = "SELECT DISTINCT(fld_ship_date), fld_number_shipped \
                  FROM tbl_nevada_chart \
                  WHERE fld_dataset_id=%d \
                  ORDER BY fld_ship_date" % self.dataset_id
        _results = self._app.DB.execute_query(_query, None, self._app.ProgCnx)

        _query = "SELECT fld_ship_date, fld_return_date, fld_number_returned \
                  FROM tbl_nevada_chart \
                  WHERE fld_dataset_id=%d \
                  ORDER BY fld_ship_date, fld_return_date" % self.dataset_id
        _returns = self._app.DB.execute_query(_query, None, self._app.ProgCnx)

        try:
            _n_periods = len(_results)
        except TypeError:
            _n_periods = 0

        try:
            _n_returns = len(_returns)
        except TypeError:
            _n_returns = 0

        # Create a dictionary with the following:
        #
        #     Key = shipment date (month-year).
        #   Value = list with each position containing:
        #       0 = the number of units shipped.
        #       1 = dictionary of returned units where the key is the return
        #           date and the value is the number of units returned.
        #
        #   {u'Jan-08': [32, {u'Mar-08': 0, u'Feb-08': 0}]}
        #
        # Create a list of GObject types to use for creating the gtkListStore()
        # used to display the Nevada chart.
        _gobject_types = [gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_INT, gobject.TYPE_STRING]
        for i in range(_n_periods):
            _date_ship = datetime.strftime(
                date.fromordinal(_results[i][0]), '%b-%y')
            _nevada[_date_ship] = [_results[i][1], {}]

        _n_cols = 2
        _headings = [_(u"Ship Date"), _(u"Number\nShipped")]
        for i in range(_n_returns):
            _date_ship = datetime.strftime(
                date.fromordinal(_returns[i][0]), '%b-%y')
            _date_return = datetime.strftime(
                date.fromordinal(_returns[i][1]), '%b-%y')
            _nevada[_date_ship][1][_date_return] = _returns[i][2]
            _n_cols = max(_n_cols, len(_nevada[_date_ship][1]) + 2)
            if _date_return not in _headings:
                _headings.append(_date_return)
                _gobject_types.append(gobject.TYPE_INT)
                _gobject_types.append(gobject.TYPE_STRING)

        # Create the gtk.ListStore() and columns for the Nevada chart
        # gtk.TreeView().
        j = 0
        _model = gtk.ListStore(*_gobject_types)
        for i in range(_n_cols):
            _cell = gtk.CellRendererText()       # Value to be displayed.
            _cell.set_property('editable', 0)
            _cell.set_property('wrap-width', 250)
            _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            _cell.set_property('xalign', 0.5)
            _cell.set_property('yalign', 0.1)

            _column = gtk.TreeViewColumn("")
            _label = gtk.Label(_column.get_title())
            _label.set_line_wrap(True)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_markup("<span weight='bold'>" +
                              _headings[i] + "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=j, background=j+1)
            _column.set_resizable(True)
            _column.set_alignment(0.5)

            _cell = gtk.CellRendererText()       # Cell background color.
            _cell.set_property('visible', False)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=j+1)

            self.tvwNevadaChart.append_column(_column)

            j += 2

        self.tvwNevadaChart.set_model(_model)

        # Load the Nevada chart gtk.ListStore() with the data.
        _date_ship = _nevada.keys()
        _date_return = _headings[2:]
        for i in range(len(_date_ship)):
            _returns = _nevada[_date_ship[i]][1].keys()
            _data = [_date_ship[i], 'light gray',
                     _nevada[_date_ship[i]][0], 'light gray']
            for j in range(len(_date_return)):
                if _date_return[j] not in _returns:
                    _data.append(0)
                    _data.append('light gray')
                else:
                    _data.append(_nevada[_date_ship[i]][1][_date_return[j]])
                    _data.append('#FFFFFF')
            _model.append(_data)

        return False

    def _load_nonparametric_tree(self, model, data, index, col_headings):
        """"
        Method to load the gtk.TreeView() with the results of non-parametric
        analyses.  This includes the MCF, Kaplan-Meier, and NHPP - Power Law
        analyses.

        @param model: the nonparametric estimates gtk.TreeModel().
        @type: model gtk.TreeModel
        @param data: a dictionary containing the data to load into the
                     gtk.TreeModel().
        @type data: dictionary
        @param index: a list containing the order of the
        @type: index: list of integers
        @param col_headings: a list containing the the text for the
                             gtk.TreeColumn() headers.
        @type col_headings: list of strings
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        # Remove the existing model from the gtk.TreeView.
        self.tvwNonParResults.set_model(None)

        # Remove all the existing columns from the gtk.TreeView.
        for _col in self.tvwNonParResults.get_columns():
            self.tvwNonParResults.remove_column(_col)

        # Load the model with the data.
        for i in range(len(data)):
            _lineitem = []
            for j in range(len(index)):
                _lineitem.append(data[i][index[j]])

            model.append(_lineitem)

        # Add columns to display the data.
        for i in range(len(col_headings)):
            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _cell.set_property('background', 'light gray')
            _column = gtk.TreeViewColumn()
            _label = _widg.make_column_heading(col_headings[i])
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=i)
            self.tvwNonParResults.append_column(_column)

        self.tvwNonParResults.set_model(model)

        return False

    def _update_tree(self):
        """
        Method to update the Dataset class gtk.TreeModel().

        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        _model.set_value(_row, self._col_order[11], self.n_suspensions)
        _model.set_value(_row, self._col_order[12], self.n_failures)
        _model.set_value(_row, self._col_order[13], self.scale[0])
        _model.set_value(_row, self._col_order[14], self.scale[1])
        _model.set_value(_row, self._col_order[15], self.scale[2])
        _model.set_value(_row, self._col_order[16], self.shape[0])
        _model.set_value(_row, self._col_order[17], self.shape[1])
        _model.set_value(_row, self._col_order[18], self.shape[2])
        _model.set_value(_row, self._col_order[19], self.location[0])
        _model.set_value(_row, self._col_order[20], self.location[1])
        _model.set_value(_row, self._col_order[21], self.location[2])
        _model.set_value(_row, self._col_order[22], self.variance[0])
        _model.set_value(_row, self._col_order[23], self.variance[1])
        _model.set_value(_row, self._col_order[24], self.variance[2])
        _model.set_value(_row, self._col_order[25], self.covariance[0])
        _model.set_value(_row, self._col_order[26], self.covariance[1])
        _model.set_value(_row, self._col_order[27], self.covariance[2])
        _model.set_value(_row, self._col_order[28], self.mhb)
        _model.set_value(_row, self._col_order[29], self.lp)
        _model.set_value(_row, self._col_order[30], self.lr)
        _model.set_value(_row, self._col_order[31], self.aic)
        _model.set_value(_row, self._col_order[32], self.bic)
        _model.set_value(_row, self._col_order[33], self.mle)

        return False

    def _update_attributes(self):
        """
        Method to update the Dataset class attributes.

        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        self.dataset_id = _model.get_value(_row, self._col_order[0])
        self.assembly_id = _model.get_value(_row, self._col_order[1])
        self.description = _model.get_value(_row, self._col_order[2])
        self.source = _model.get_value(_row, self._col_order[3])
        self.distribution_id = _model.get_value(_row, self._col_order[4])
        self.confidence = _model.get_value(_row, self._col_order[5])
        self.confidence_type = _model.get_value(_row, self._col_order[6])
        self.confidence_method = _model.get_value(_row, self._col_order[7])
        self.fit_method = _model.get_value(_row, self._col_order[8])
        self.rel_time = _model.get_value(_row, self._col_order[9])
        self.n_rel_points = _model.get_value(_row, self._col_order[10])
        self.n_suspensions = _model.get_value(_row, self._col_order[11])
        self.n_failures = _model.get_value(_row, self._col_order[12])

        self.scale[0] = _model.get_value(_row, self._col_order[13])
        self.scale[1] = _model.get_value(_row, self._col_order[14])
        self.scale[2] = _model.get_value(_row, self._col_order[15])
        self.shape[0] = _model.get_value(_row, self._col_order[16])
        self.shape[1] = _model.get_value(_row, self._col_order[17])
        self.shape[2] = _model.get_value(_row, self._col_order[18])
        self.location[0] = _model.get_value(_row, self._col_order[19])
        self.location[1] = _model.get_value(_row, self._col_order[20])
        self.location[2] = _model.get_value(_row, self._col_order[21])
        self.variance[0] = _model.get_value(_row, self._col_order[22])
        self.variance[1] = _model.get_value(_row, self._col_order[23])
        self.variance[2] = _model.get_value(_row, self._col_order[24])
        self.covariance[0] = _model.get_value(_row, self._col_order[25])
        self.covariance[1] = _model.get_value(_row, self._col_order[26])
        self.covariance[2] = _model.get_value(_row, self._col_order[27])

        self.mhb = _model.get_value(_row, self._col_order[28])
        self.lp = _model.get_value(_row, self._col_order[29])
        self.lr = _model.get_value(_row, self._col_order[30])
        self.aic = _model.get_value(_row, self._col_order[31])
        self.bic = _model.get_value(_row, self._col_order[32])
        self.mle = _model.get_value(_row, self._col_order[33])
        self.start_time = _model.get_value(_row, self._col_order[34])
# TODO: Add end time attribute.
        #self.end_time = _model.get_value(_row, self._col_order[35])
        self.start_date = _model.get_value(_row, self._col_order[35])
        self.end_date = _model.get_value(_row, self._col_order[36])
        self._nevada_chart = _model.get_value(_row, self._col_order[37])

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Method for handling mouse clicks on the Dataset class gtk.TreeView().

        @param treeview: the Dataset class gtk.TreeView().
        @type treeview: gtk.TreeView
        @param event: a gtk.gdk.Event() that called this function (the
                      important attribute is which mouse button was clicked).
                      1 = left
                      2 = scrollwheel
                      3 = right
                      4 = forward
                      5 = backward
                      8 =
                      9 =
        @type event: gtk.gdk.Event
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        if event.button == 1:
            self._treeview_row_changed(treeview, None, 0)
        elif event.button == 3:
            print "Pop-up a menu!"

        return False

    def _treeview_row_changed(self, __treeview, __path, __column):
        """
        Callback function to handle events for the Dataset class
        gtk.Treeview().  It is called whenever the Dataset class
        gtk.TreeView() is clicked or a row is activated.

        @param __treeview: the Dataset class gtk.TreeView().
        @type __treeview: gtk.TreeView
        @param __path: the activated gtk.TreeIter() path.
        @type __path: string
        @param __column: the activated gtk.TreeViewColumn().
        @type __column: integer
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        if _row is not None:
            self._update_attributes()
            self.load_notebook()

            if self.distribution_id == 1 or self.distribution_id == 2:
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

    def _add_record(self, __button):
        """
        Method to add one or more record to the selected survival analysis
        data set.

        @param __button: the gtk.ToolButton() that called this method.
        @type __button: gtk.ToolButton
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        _n_new_records = _util.add_items(_(u"RTK - Add Data Set Records"),
                                         _(u"How many records to add?"))

        _util.set_cursor(self._app, gtk.gdk.WATCH)

        # Find the maximum record ID for the selected data set.
        _query = "SELECT MAX(fld_record_id) \
                  FROM tbl_survival_data \
                  WHERE fld_dataset_id=%d" % self.dataset_id
        _next_record = self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx)
        try:
            _next_record = _next_record[0][0] + 1
        except TypeError:
            _next_record = 0

        # Add the records.
        _error = False
        for i in range(_n_new_records):
            _query = "INSERT INTO tbl_survival_data \
                      (fld_record_id, fld_dataset_id, fld_assembly_id) \
                      VALUES (%d, %d, %d)" % \
                     (_next_record, self.dataset_id, self.assembly_id)
            if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=True):
                _error = True

            _next_record += 1

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)

        if _error:
            _util.rtk_error(_(u"Error adding one ore more survival records."))
            return True

        self._load_dataset_tree()

        return False

    def _delete_data_set(self, __button):
        """
        Method to remove the selected data set from the open RTK Program
        database.

        @param __button: the gtk.Button() that called this method.
        @type __button: gtk.Button
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        _util.set_cursor(self._app, gtk.gdk.WATCH)
        print "Fuck it"
        _query = "DELETE FROM tbl_dataset \
                  WHERE fld_dataset_id=%d" % self.dataset_id
        if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                          commit=True):
            _util.rtk_error(_(u"Error deleting data set."))
            return True

        self.load_tree()

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)

        return False

    def _delete_record(self, __button):
        """
        Method to remove the selected record from the survival analysis
        data set.

        @param __button: the gtk.ToolButton() that called this method.
        @type __button: gtk.ToolButton
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        _util.set_cursor(self._app, gtk.gdk.WATCH)

        (_model, _paths) = self.tvwDataset.get_selection().get_selected_rows()

        _records = []
        for i in range(len(_paths)):
            _row = _model.get_iter(_paths[i])
            _records.append(_model.get_value(_row, 0))

        _dialog = _widg.make_dialog(_(u"RTK: Confirm Delete"))

        _fixed = gtk.Fixed()

        _y_pos = 10

        _label = _widg.make_label(_(u"Are you sure you want to delete the "
                                    u"selected survival data record(s)."),
                                  width=600, height=250, wrap=True)
        _fixed.put(_label, 5, _y_pos)

        _fixed.show_all()

        _dialog.vbox.pack_start(_fixed)     # pylint: disable=E1101

        if _dialog.run() == gtk.RESPONSE_ACCEPT:
            for i in range(len(_records)):
                _query = "DELETE FROM tbl_survival_data \
                          WHERE fld_record_id=%d" % _records[i]
                if not self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx,
                                                  commit=True):
# TODO: Log each record that can't be deleted to the RTK_error.log.
                    _util.rtk_error(_(u"Error deleting survival record."))

        _dialog.destroy()

        self._load_dataset_tree()

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)

        return False

    def _save_dataset(self, __button):
        """
        Method to save the Dataset class gtk.TreeView() information to the open
        RTK Program database.

        @param __button: the gtk.Button() widget that called this method.
        @type __button: gtk.Button
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        def _save_line_item(model, __path, row, self):
            """
            Method to save each row in the Dataset class gtk.TreeModel to the
            open RTK Program database.

            @param model: the Dataset class gtk.TreeModel().
            @type model: gtk.TreeModel
            @param __path: the path of the active gtk.TreeIter() in the Dataset
                           class gtk.TreeModel().
            @type __path: string
            @param row: the selected gtk.TreeIter() in the Dataset class
                        gtk.TreeModel().
            @type row: gtk.TreeIter
            @return: False if successful or True if an error is encountered.
            @rtype: boolean
            """

            _values = (model.get_value(row, 1), model.get_value(row, 2),
                       model.get_value(row, 3), model.get_value(row, 4),
                       model.get_value(row, 5), model.get_value(row, 6),
                       model.get_value(row, 7), model.get_value(row, 8),
                       model.get_value(row, 9), model.get_value(row, 10),
                       model.get_value(row, 11), model.get_value(row, 12),
                       model.get_value(row, 13), model.get_value(row, 14),
                       model.get_value(row, 15), model.get_value(row, 16),
                       model.get_value(row, 17), model.get_value(row, 18),
                       model.get_value(row, 19), model.get_value(row, 20),
                       model.get_value(row, 21), model.get_value(row, 22),
                       model.get_value(row, 23), model.get_value(row, 24),
                       model.get_value(row, 25), model.get_value(row, 26),
                       model.get_value(row, 27), model.get_value(row, 28),
                       model.get_value(row, 29), model.get_value(row, 30),
                       model.get_value(row, 31), model.get_value(row, 32),
                       model.get_value(row, 33), model.get_value(row, 34),
                       model.get_value(row, 35), model.get_value(row, 36),
                       model.get_value(row, 0))

            _query = "UPDATE tbl_dataset \
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
                          fld_start_time=%d, fld_start_date=%d, \
                          fld_end_date=%d \
                      WHERE fld_dataset_id=%d" % _values
            if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=True):
                _util.rtk_error(_(u"Error saving data set %d.") %
                                model.get_value(row, 0))
                return True

            return False

        def _save_survival_record(model, __path, row, self):
            """
            Function to save each of the survival data records that comprise
            the selected Dataset to the open RTK Program database.

            @param model: the Dataset class records gtk.TreeModel().
            @type model: gtk.TreeModel
            @param __path: the path of the active gtk.TreeIter() in the Dataset
                           class records gtk.TreeModel().
            @type __Path: string
            @param row: the selected gtk.TreeIter() in the Dataset records
                        gtk.TreeModel().
            @type row: gtk.TreeIter
            @return: False if successful or True if an error is encountered.
            @rtype: boolean
            """

            _query = "UPDATE tbl_survival_data \
                      SET fld_unit='%s', fld_left_interval=%f, \
                          fld_right_interval=%f, fld_quantity=%d, \
                          fld_status='%s' \
                      WHERE fld_record_id=%d" % \
                     (model.get_value(row, 1), model.get_value(row, 2),
                      model.get_value(row, 3), model.get_value(row, 4),
                      model.get_value(row, 5), model.get_value(row, 0))
            if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=True):
                _util.rtk_error(_(u"Error saving data set record %d.") %
                                model.get_value(row, 0))

            return False

        _util.set_cursor(self._app, gtk.gdk.WATCH)

        _model = self.treeview.get_model()
        _model.foreach(_save_line_item, self)

        _model = self.tvwDataset.get_model()
        _model.foreach(_save_survival_record, self)

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)

        return False

    def _callback_combo(self, combo, index):
        """
        Callback function to retrieve and save gtk.ComboBox() changes.

        @param combo: the gtk.ComboBox() that called this method.
        @type combo: gtk.ComboBox
        @param index: the position in the Dataset class gtk.TreeView()
                      associated with the data from the calling gtk.ComboBox().
                      1 = Assembly ID
                      3 = Source of dataset
                      4 = Statistical distribution ID
                      6 = Confidence type
                      7 = Confidence method
                      8 = Fit method
        @type index: integer
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        if index == 1:
            _model = combo.get_model()
            _row = combo.get_active_iter()
            if _row is not None:
                try:
                    _text = int(_model.get_value(_row, 1))
                except ValueError:
                    _text = 0
            else:
                _text = 0
        else:
            _text = combo.get_active()

        if index == 4:                      # Statistical distribution.
            self.distribution_id = _text

            try:
                self.hpnAnalysisResults.remove(
                    self.hpnAnalysisResults.get_child2())
            except TypeError:
                pass

            try:
                self.vpnAnalysisResults.remove(
                    self.vpnAnalysisResults.get_child2())
            except TypeError:
                pass

            if self.distribution_id in [1, 2]:  # MCF or Kaplan-Meier
                self.chkGroup.show()
                self.chkParts.show()
                self.cmbFitMethod.hide()
                self.cmbConfMethod.hide()
                self.lblFitMethod.hide()
                self.lblConfMethod.hide()
                self.hpnAnalysisResults.pack2(self.fraNonParEst)
                self.vpnAnalysisResults.pack2(self.fraNonParStats)
            else:
                self.chkGroup.hide()
                self.chkParts.hide()
                self.cmbFitMethod.show()
                self.cmbConfMethod.show()
                self.lblFitMethod.show()
                self.lblConfMethod.show()
                self.vpnAnalysisResults.pack2(self.fraParStats)

            if _text == 7:                  # WeiBayes
                dialog = _widg.make_dialog(_(u"RTK Information"),
                                           dlgbuttons=(gtk.STOCK_OK,
                                                       gtk.RESPONSE_ACCEPT))

                fixed = gtk.Fixed()

                y_pos = 10
                label = _widg.make_label(_(u"WeiBayes is not yet implemented "
                                           u"in RTK."), width=300, height=100)
                fixed.put(label, 5, y_pos)

                fixed.show_all()

                dialog.vbox.pack_start(fixed)   # pylint: disable=E1101
                dialog.run()

                dialog.destroy()

        elif index == 7:                    # Confidence method
            self.confidence_method = _text

        (_model, _row) = self.treeview.get_selection().get_selected()
        _model.set_value(_row, index, _text)

        return False

    def _callback_entry(self, entry, __event, convert, index):
        """
        Callback function to retrieve and save gtk.Entry() changes.

        @param entry: the gtk.Entry() that called the function.
        @type entry: gtk.Entry
        @param __event: the gtk.gdk.Event() that called the function.
        @type __event: gtk.gdk.Event
        @param convert: the data type to convert the gtk.Entry() contents to.
        @type convert: string
        @param index: the position in the applicable gtk.TreeModel() associated
                      with the data from the calling gtk.Entry().
        @type index: integer
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        from datetime import datetime

        if convert == 'text':
            _text = entry.get_text()

        elif convert == 'int':
            _text = int(entry.get_text())

        elif convert == 'float':
            _text = float(entry.get_text().replace('$', ''))

        elif convert == 'date':
            _text = datetime.strptime(entry.get_text(), '%Y-%m-%d').toordinal()

        (_model, _row) = self.treeview.get_selection().get_selected()
        _model.set_value(_row, index, _text)

        return False

    def _callback_combo_cell(self, cell, path, row, col, treemodel):
        """
        Called whenever a gtk.TreeView() gtk.CellRendererCombo() changes.

        @param cell: the gtk.CellRendererCombo)_ that called this method.
        @type cell: gtk.CellRendererCombo
        @param path: the path in the gtk.TreeView() containing the
                     gtk.CellRendererCombo() that called this function.
        @type path: string
        @param row: the new gtk.TreeIter() in the gtk.CellRendererCombo() that
                    called this function.
        @type row: gtk.TreeIter
        @param col: the index of the column in the gtk.TreeView() containing
                    the gtk.CellRendererCombo().
        @type col: integer
        @param treemodel: the gtk.TreeModel() for the gtk.TreeView().
        @type treemodel: gtk.TreeModel
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        model = cell.get_property('model')
        val = model.get_value(row, 0)

        row = treemodel.get_iter(path)
        treemodel.set_value(row, col, val)

        return False

    def _callback_entry_cell(self, __cell, path, new_text, index, convert):
        """
        Called whenever a gtk.TreeView() gtk.CellRendererText() changes.

        @param __cell: the gtk.CellRendererText() that called this method.
        @type __cell: gtk.CellRendererText
        @param path: the path in the gtk.TreeView() containing the
                     gtk.CellRendererText() that called this method.
        @type path: string
        @param new_text: the new text in the gtk.CellRendererText() that called
                         this method.
        @type new_text: string
        @param index: the index (column) in the gtk.TreeView() containing the
                      gtk.CellRendererText() that is being edited.
        @type index: integer
        @param convert: the data type to convert new_text to for the
                        gtk.CellRendererText().
        @type convert: string
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        from datetime import datetime

        model = self.tvwDataset.get_model()
        row = model.get_iter(path)

        if convert == 'int':
            new_text = int(new_text)
        elif convert == 'float':
            new_text = float(new_text)
        elif convert == 'date':
            new_text = datetime.strptime(new_text, '%Y-%m-%d').toordinal()

        model.set_value(row, index, new_text)

        return False

    def _notebook_page_switched(self, __notebook, __page, __page_num):
        """
        Called whenever the Dataset class Work Book gtk.Notebook() page is
        changed.

        @param __notebook: the Dataset class gtk.Notebook().
        @type __notebook: gtk.Notebook
        @param __page: the newly selected page's gtk.Widget().
        @type __page: gtk.Widget
        @param __page_num: the newly selected page number.
                           0 = Analysis Inputs
                           1 = Analysis Results (numeric)
                           2 = Plots
                           3 = Results Breakdown
        @type __page_num: integer
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        return False

    def _calculate(self, __button):
        """
        Method to execute the selected analysis.

        @param __button: the gtk.ToolButton() that called this method.
        @type __button: gtk.ToolButton
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _util.set_cursor(self._app, gtk.gdk.WATCH)

        _RELTIME_ = False

        if self.confidence_type == 3:       # Two-sided bounds.
            _confidence = (100.0 + self.confidence) / 200.0
        else:                               # One-sided bounds.
            _confidence = self.confidence / 100.0

        # Set maximum time to some very large value if the user has not set
        # this themselves.  Keeping it at zero results in nothing being
        # returned from the SQL queries to follow.
        if self.rel_time == 0.0:
            self.rel_time = 1000000.0
            _RELTIME_ = True

        if self.n_rel_points == 0:
            self.n_rel_points = 1

        # Determine the confidence bound z-value.
        _z_norm = norm.ppf(_confidence)

        # Get the entire dataset.
        _query = "SELECT fld_unit, fld_left_interval, fld_right_interval, \
                         fld_tbf, fld_status, fld_quantity, fld_request_date \
                  FROM tbl_survival_data \
                  WHERE fld_dataset_id=%d \
                  AND fld_right_interval <= %f AND fld_right_interval > %f \
                  AND fld_request_date >= %d AND fld_request_date < %d \
                  ORDER BY fld_request_date ASC, \
                           fld_unit ASC, \
                           fld_left_interval ASC" % (self.dataset_id,
                                                     self.rel_time,
                                                     self.start_time,
                                                     self.start_date,
                                                     self.end_date)
        _results = self._app.DB.execute_query(_query, None, self._app.ProgCnx)

        _censdata = []
        for i in range(len(_results)):
            _censdata.append([_results[i][1], _results[i][2]])

        # Initialize variables.
        self.n_failures = 0
        self.n_suspensions = 0
        MTBF = 0.0
        MTBFLL = 0.0
        MTBFUL = 0.0
        self.scale[0] = 0.0
        self.scale[1] = 0.0
        self.scale[2] = 0.0
        self.shape[0] = 0.0
        self.shape[1] = 0.0
        self.shape[2] = 0.0
        self.location[0] = 0.0
        self.location[1] = 0.0
        self.location[2] = 0.0
        self.variance[0] = 0.0
        self.variance[1] = 0.0
        self.variance[2] = 0.0
        self.covariance[0] = 0.0
        self.covariance[1] = 0.0
        self.covariance[2] = 0.0
        self.mhb = 0.0
        self.lp = 0.0
        self.lr = 0.0
        self.mle = 0.0
        self.aic = 0.0
        self.bic = 0.0

        # Initialize some lists.
        _p_value = [1.0, 1.0, 1.0, 1.0]
        _text = [u"", u"", u""]

        # ================================================================= #
        # Perform Nelson's mean cumulative function analysis.               #
        # ================================================================= #
        if self.distribution_id == 1:                 # MCF
            # Create a list of unique units.
            _query = "SELECT DISTINCT(fld_unit) \
                      FROM tbl_survival_data \
                      WHERE fld_dataset_id=%d \
                      AND fld_right_interval <= %f \
                      AND fld_right_interval > %f" % \
                     (self.dataset_id, self.rel_time, self.start_time)
            _results = self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx)
            try:
                _n_units = len(_results)
            except TypeError:
                _n_units = 0

            _units = []
            for i in range(_n_units):
                _units.append(_results[i][0])

            # Create a list of unique failure times.
            _query = "SELECT DISTINCT(fld_right_interval) \
                      FROM tbl_survival_data \
                      WHERE fld_dataset_id=%d \
                      AND fld_right_interval >= %f \
                      AND fld_right_interval <= %f \
                      ORDER BY fld_right_interval ASC" % \
                     (self.dataset_id, self.start_time, self.rel_time)
            _results = self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx)

            try:
                _n_times = len(_results)
            except TypeError:
                _n_times = 0

            _times = []
            for i in range(_n_times):
                _times.append(_results[i][0])

            # Get the entire dataset.
            # Example of a record returned from the following query:
            #     (u'HT36103', 0.0, 12.0, 12.0)
            _query = "SELECT fld_unit, fld_left_interval, \
                             fld_right_interval, fld_tbf, fld_quantity \
                      FROM tbl_survival_data \
                      WHERE fld_dataset_id=%d \
                      AND fld_right_interval >= %f \
                      AND fld_right_interval <= %f \
                      ORDER BY fld_unit ASC, \
                               fld_left_interval ASC" % \
                     (self.dataset_id, self.start_time, self.rel_time)
            _results = self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx)

            # ============================================================== #
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
            # =============================================================== #
            _nonpar = mean_cumulative_function(_units, _times, _results,
                                               _confidence)

            # Load the non-parametric results gtk.TreeView
            _model = gtk.ListStore(gobject.TYPE_FLOAT, gobject.TYPE_INT,
                                   gobject.TYPE_INT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
            _index = [0, 3, 4, 5, 6, 7, 9, 8, 11, 10, 12, 14, 13, 15]
            _col_headings = [_(u"Event\nTime"),
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
            self._load_nonparametric_tree(_model, _nonpar, _index,
                                          _col_headings)
            # Get:
            #   Total number of failures.
            #   List of unique failures times.
            #   List of MCF at each unique failure time.
            #   List of MCF lower bound at each unique failure time.
            #   List of MCF upper bound at each unique failure time.
            #   Maximum observed time.
            _n_records = len(_nonpar)
            _failures = [x[4] for x in _nonpar]
            self.n_failures = int(sum(_failures))
            times = [x[0] for x in _nonpar]
            muhat = [x[9] for x in _nonpar]
            muhatll = [x[7] for x in _nonpar]
            muhatul = [x[8] for x in _nonpar]
            ta = max(times)

            # Calculate the MIL-HDBK-189, Laplace, and Lewis-Robinson test
            # statistics.  Find the chi-square critical value.  These
            # statistics are used to test for HPP vs. NHPP in the data.
            _query = "SELECT t1.fld_unit, t2.fld_tbf, t1.fld_request_date \
                      FROM tbl_incident AS t1 \
                      INNER JOIN tbl_survival_data AS t2 \
                      WHERE t2.fld_record_id=t1.fld_incident_id \
                      AND t2.fld_dataset_id=%d \
                      AND t2.fld_right_interval >= %f \
                      AND t2.fld_right_interval <= %f \
                      AND t1.fld_request_date >= %d \
                      AND t1.fld_request_date < %d \
                      ORDER BY t1.fld_request_date ASC" % \
                     (self.dataset_id, self.start_time, self.rel_time,
                      self.start_date, self.end_date)
            _results = self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx)

            _tbf = []
            _failnum = []
            _dates = []
            _denominator = 0.0
            for i in range(_n_records):
                try:
                    self.mhb += log(times[i] / ta)
                    _denominator += log(ta / times[i])
                except ValueError or ZeroDivisionError:
                    print i, times[i], ta


                self.lp += times[i] / ta
                _tbf.append(_results[i][1])
                _failnum.append(i)
                _dates.append(_results[i][2])

            self.mhb = -2.0 * self.mhb
            self.lp = (self.lp - (self.n_failures / 2.0)) / \
                      sqrt(self.n_failures / 12.0)
            tau = np.mean(_tbf)             # pylint: disable=E1101
            S = np.std(_tbf)                # pylint: disable=E1101
            self.lr = self.lp * tau / S

            _chisq = chi2.ppf(1.0 - _confidence, 2 * self.n_failures)

            _beta = self.n_failures / _denominator
            _eta = ta / self.n_failures**(1.0 / _beta)

            # Calculate the sample serial correlation coefficient.
            _cov = 0.0
            _var1 = 0.0
            _var2 = 0.0
            _tau_bar = np.mean(_tbf)        # pylint: disable=E1101
            for i in range(len(_tbf) - 1):
                _cov += (_tbf[i] - _tau_bar) * (_tbf[i + 1] - _tau_bar)
                _var1 += (_tbf[i] - _tau_bar)**2.0
                _var2 += (_tbf[i + 1] - _tau_bar)**2.0
            _rho = sqrt(self.n_failures - 1) * (_cov / sqrt(_var1 * _var2))

            _p_value[0] = chi2.cdf(self.mhb, 2 * self.n_failures)
            _p_value[1] = norm.cdf(abs(self.lp))
            _p_value[2] = norm.cdf(abs(self.lr))
            _p_value[3] = norm.cdf(_rho)

            # Plot the mean cumulative function with confidence bounds.
            _widg.load_plot(self.axAxis1, self.pltPlot1, x=times,
                            y1=muhat, y2=muhatll, y3=muhatul,
                            _title_=_(u"MCF Plot for %s") % self.description,
                            _xlab_=_(u"Time"),
                            _ylab_=_(u"Mean Cumulative Function [mu(t)]"),
                            _marker_=['g-', 'r-', 'b-'])
            _text = (u"MCF", u"MCF LCL", u"MCF UCL")
            _widg.create_legend(self.axAxis1, _text, fontsize='medium',
                                legframeon=True, location='lower right',
                                legshadow=True)

            for plot in self.vbxPlot1.get_children():
                self.vbxPlot1.remove(plot)

            self.vbxPlot1.pack_start(self.pltPlot1)

            # Plot the run sequence plot.
            _widg.load_plot(self.axAxis2, self.pltPlot2,
                            x=_dates, y1=_tbf,
                            _title_=_(u"Run Sequence Plot for %s") %
                            self.description,
                            _xlab_=_(u"Date"),
                            _ylab_=_(u"Time Between Failure"),
                            _type_=[4], _marker_=['g-'])

            # Create a lag plot.
            _zero_line = []
            for i in range(len(_tbf) - 1):
                _zero_line.append(_tbf[i])

            _widg.load_plot(self.axAxis4, self.pltPlot4,
                            x=_tbf[0:len(_tbf)-1], y1=_tbf[1:len(_tbf)],
                            y2=_zero_line,
                            _title_=_(u"Lag Plot for %s") % self.description,
                            _xlab_=_(u"Lagged Time Between Failure"),
                            _ylab_=_(u"Time Between Failure"),
                            _type_=[2, 2], _marker_=['go', 'k-'])

            for plot in self.vbxPlot2.get_children():
                self.vbxPlot2.remove(plot)

            self.vbxPlot2.pack_start(self.pltPlot2)
            self.vbxPlot2.pack_start(self.pltPlot4)

            # Assign the cumulative MTBF for display.
            MTBF = _nonpar[_n_records - 1][10]
            MTBFLL = _nonpar[_n_records - 1][11]
            MTBFUL = _nonpar[_n_records - 1][12]

            self.txtChiSq.set_text(str(fmt.format(_chisq)))
            self.txtRho.set_text(str(fmt.format(_rho)))
            self.txtZLPNorm.set_text(str(fmt.format(_z_norm)))
            self.txtZLRNorm.set_text(str(fmt.format(_z_norm)))
            self.txtRhoNorm.set_text(str(fmt.format(_z_norm)))

            if self.mhb > _chisq:
                self.lblMHBResult.set_markup(
                    _(u"<span foreground='red'>Nonconstant</span>"))
            else:
                self.lblMHBResult.set_markup(
                    _(u"<span foreground='green'>Constant</span>"))
            if fabs(self.lp) > _z_norm:
                self.lblZLPResult.set_markup(
                    _(u"<span foreground='red'>Nonconstant</span>"))
            else:
                self.lblZLPResult.set_markup(
                    _(u"<span foreground='green'>Constant</span>"))
            if fabs(self.lr) > _z_norm:
                self.lblZLRResult.set_markup(
                    _(u"<span foreground='red'>Nonconstant</span>"))
            else:
                self.lblZLRResult.set_markup(
                    _(u"<span foreground='green'>Constant</span>"))

        # =================================================================== #
        # Perform a Kaplan-Meier analysis.
        # =================================================================== #
        elif self.distribution_id == 2:     # Kaplan-Meier
# TODO: Revise tbl_dataset to include a field for the hardware id.
# TODO: Revise the following query to include the hardware id field that will be added.
            _query = "SELECT fld_left_interval, fld_right_interval, \
                             fld_status, fld_quantity, fld_unit \
                      FROM tbl_survival_data \
                      WHERE fld_dataset_id=%d \
                      AND fld_right_interval >= %f \
                      AND fld_right_interval <= %f \
                      ORDER BY fld_right_interval ASC, \
                      fld_status DESC" % (self.dataset_id, self.start_time,
                                          self.rel_time)
            _results = self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx)

            # Make a list with the rank of the records that are failures.
            r = []
            for i in range(len(_results)):
                if(_results[i][2] == 'Event' or
                   _results[i][2] == 'Interval Censored'):
                    r.append(i + 1)

            # The Kaplan-Meier function will retun a list of lists where the
            # index of each list is:
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
            _nonpar = kaplan_meier(_results, self.rel_time, _confidence)
            turnbull(_results, self.rel_time, _confidence)

            n_points = _nonpar[0][0]
            _times = _nonpar[1]
            _Shat = _nonpar[5]
            _Shatll = _nonpar[8]
            _Shatul = _nonpar[9]

            _kaplan_meier = []
            for i in range(len(_times)):
                _kaplan_meier.append([_nonpar[1][i], _nonpar[2][i],
                                      _nonpar[3][i], _nonpar[7][i],
                                      _nonpar[9][i], _nonpar[5][i],
                                      _nonpar[8][i]])
                self.n_failures += _nonpar[3][i]

            # Calculate the MTBF, the variance on the MTBF, and the limits on
            # the MTBF.
            _mtbf = kaplan_meier_mean(_kaplan_meier, _confidence)

            MTBF = _mtbf[len(_mtbf) - 1][0]
            MTBFLL = _mtbf[len(_mtbf) - 1][1]
            MTBFUL = _mtbf[len(_mtbf) - 1][2]

            # Load the non-parametric results gtk.TreeView
            _model = gtk.ListStore(gobject.TYPE_FLOAT, gobject.TYPE_INT,
                                   gobject.TYPE_INT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT)
            _index = [0, 1, 2, 3, 4, 5, 6]
            _col_headings = [_(u"Time"), _(u"Number\nat Risk"),
                             _(u"Number\nFailing"), _(u"se S(t)"),
                             _(u"S(t) Lower\nBound"), _(u"S(t)"),
                             _(u"S(t) Upper\nBound")]
            self._load_nonparametric_tree(_model, _kaplan_meier,
                                          _index, _col_headings)

            _logtimes = [log(i) for i in _times]

            (_h_, _hll_, _hul_,
             _H_, _Hll_, _Hul_,
             _logH_, _logHll_, _logHul_) = kaplan_meier_hazard(_kaplan_meier)

            # Calculate the number of failures and suspensions in the dataset.
            self.n_suspensions = n_points - self.n_failures

            # Plot the survival curve with confidence bounds.
            _widg.load_plot(self.axAxis1, self.pltPlot1,
                            x=_times, y1=_Shat,
                            y2=_Shatll, y3=_Shatul,
                            _title_=_(u"Kaplan-Meier Plot for %s") %
                            self.description,
                            _xlab_=_(u"Time"),
                            _ylab_=_(u"Survival Function [S(t)] "),
                            _marker_=['g-', 'r-', 'b-'])
            _text = (u"Survival Function [S(t)]", u"S(t) LCL", u"S(t) UCL")
            _widg.create_legend(self.axAxis1, _text, fontsize='medium',
                                legframeon=True, location='upper right',
                                legshadow=True)

            # Plot the hazard rate curve with confidence bounds.
            _widg.load_plot(self.axAxis3, self.pltPlot3,
                            x=_times[1:], y1=_h_[1:],
                            y2=_hll_[1:], y3=_hul_[1:],
                            _title_=_(u"Hazard Rate Plot for %s") %
                            self.description,
                            _xlab_=_(u"Time"),
                            _ylab_=_(u"Hazard Rate [h(t)] "),
                            _marker_=['g-', 'r-', 'b-'])
            _text = (u"Hazard Rate [h(t)]", u"h(t) LCL", u"h(t) UCL")
            _widg.create_legend(self.axAxis3, _text, fontsize='medium',
                                legframeon=True, location='upper right',
                                legshadow=True)

            for plot in self.vbxPlot1.get_children():
                self.vbxPlot1.remove(plot)

            self.vbxPlot1.pack_start(self.pltPlot1)
            self.vbxPlot1.pack_start(self.pltPlot3)

            # Plot the cumulative hazard curve with confidence bounds.
            _widg.load_plot(self.axAxis2, self.pltPlot2,
                            x=_times, y1=_H_,
                            y2=_Hll_, y3=_Hul_,
                            _title_=_("Cumulative Hazard Plot for %s") %
                            self.description,
                            _xlab_=_("Time"),
                            _ylab_=_("Cumulative Hazard Function [H(t)] "),
                            _marker_=['g-', 'r-', 'b-'])
            _text = (u"Cumulative Hazard Function [H(t)]",
                     u"H(t) LCL", u"H(t) UCL")
            _widg.create_legend(self.axAxis2, _text, fontsize='medium',
                                legframeon=True, location='upper left',
                                legshadow=True)

            # Plot the log cumulative hazard curve with confidence bounds.
            _widg.load_plot(self.axAxis4, self.pltPlot4,
                            x=_logtimes, y1=_logH_[:len(_logtimes)],
                            y2=_logHll_, y3=_logHul_,
                            _title_=_("Log Cum. Hazard Plot for %s") %
                            self.description,
                            _xlab_=_("log(Time)"),
                            _ylab_=_("Log Cum. Hazard Function [log H(t)] "),
                            _marker_=['g-', 'r-', 'b-'])
            _text = (u"Log Cumulative Hazard Function [log H(t)]",
                     u"log H(t) LCL", u"log H(t) UCL")
            _widg.create_legend(self.axAxis4, _text, fontsize='medium',
                                legframeon=True, location='upper left',
                                legshadow=True)

            for plot in self.vbxPlot2.get_children():
                self.vbxPlot2.remove(plot)

            self.vbxPlot2.pack_start(self.pltPlot2)
            self.vbxPlot2.pack_start(self.pltPlot4)

        # =================================================================== #
        # Fit the data to a power law (Duane) model and estimate it's
        # parameters.
        # =================================================================== #
        elif self.distribution_id == 3:     # NHPP - Power Law

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
            for i in range(len(_results)):
                _F_.append(_results[i][5])
                _X_.append(_results[i][2])
                _dates_.append(_results[i][6])

            _T_ = float(self.txtEndTime.get_text())

            # The power_law function will return a list of lists where each
            # list contains:
            #   Index       Value
            #    0          Cumulative test time
            #    1          Cumulative number of failures
            #    2          Calculated cumulative MTBF
            #    3          Lower bound on alpha
            #    4          Point estimate of alpha
            #    5          Upper bound on alpha
            #    6          Lower bound on b
            #    7          Point estimate of b
            #    8          Upper bound on b
            #    9          Lower bound on model estimate of cumulative MTBF
            #   10          Model point estimate of cumulative MTBF
            #   11          Upper bound on model estimate of cumulative MTBF
            #   12          Lower bound on model estimate of instantaneous MTBF
            #   13          Model point estimate of instantaneous MTBF
            #   14          Upper bound on model estimate of instantaneous MTBF
            #   15          Lower bound on model estimate of cumulative failure
            #               intensity
            #   16          Model point estimate of cumulative failure
            #               intensity
            #   17          Upper bound on model estimate of cumulative failure
            #               intensity
            #   18          Lower bound on model estimate of instantaneous
            #               failure intensity
            #   19          Model point estimate of instantaneous failure
            #               intensity
            #   20          Upper bound on model estimate of instantaneous
            #               failure intensity
            _power_law = power_law(_F_, _X_, self.confidence_method,
                                   self.fit_method, self.confidence_type,
                                   _confidence, _T_)
            if len(_power_law) == 0:
                _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)
                return True

            # Load the non-parametric results gtk.TreeView
            _model = gtk.ListStore(gobject.TYPE_FLOAT, gobject.TYPE_INT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
            _index = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 16, 17]
            _col_headings = [_(u"Cumulative\nTime"),
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
            self._load_nonparametric_tree(_model, _power_law,
                                          _index, _col_headings)

            self.shape[1] = _power_law[len(_power_law) - 1][3]
            self.shape[0] = _power_law[len(_power_law) - 1][4]
            self.shape[2] = _power_law[len(_power_law) - 1][5]

            self.scale[1] = _power_law[len(_power_law) - 1][6]
            self.scale[0] = _power_law[len(_power_law) - 1][7]
            self.scale[2] = _power_law[len(_power_law) - 1][8]

            MTBFLL = _power_law[len(_power_law) - 1][9]
            MTBF = _power_law[len(_power_law) - 1][10]
            MTBFUL = _power_law[len(_power_law) - 1][11]

            MTBFiLL = _power_law[len(_power_law) - 1][12]
            MTBFi = _power_law[len(_power_law) - 1][13]
            MTBFiUL = _power_law[len(_power_law) - 1][14]

            _start = int(0.1 * len(_power_law))
            _end = len(_power_law) - 1
            _shape = sum([z[4] for z in _power_law[_start:_end]]) / \
                     (_end - _start)
            _scale = sum([z[7] for z in _power_law[_start:_end]]) / \
                     (_end - _start)

            # Calculate the bounds at each observation point.
            _mtbf_c_plot_ll_ = np.array([], float)  # pylint: disable=E1101
            _mtbf_c_plot_ul_ = np.array([], float)  # pylint: disable=E1101
            _fi_c_plot_ll_ = np.array([], float)    # pylint: disable=E1101
            _fi_c_plot_ul_ = np.array([], float)    # pylint: disable=E1101
            for i in range(len(_power_law)):
                _times_.append(_power_law[i][0])
                _mtbf_model_.append(_scale * _power_law[i][0]**_shape)
                _fi_model_.append((1.0 / _scale) * _power_law[i][0]**-_shape)
                _mtbf_c_plot_ll_ = np.append(_mtbf_c_plot_ll_,  # pylint: disable=E1101
                                             _power_law[i][9])
                _mtbf_c_plot_.append(_power_law[i][10])    # pylint: disable=E1101
                _mtbf_c_plot_ul_ = np.append(_mtbf_c_plot_ul_,  # pylint: disable=E1101
                                             _power_law[i][11])
                _fi_c_plot_ll_ = np.append(_fi_c_plot_ll_, _power_law[i][15])  # pylint: disable=E1101
                _fi_c_plot_.append(_power_law[i][16])  # pylint: disable=E1101
                _fi_c_plot_ul_ = np.append(_fi_c_plot_ul_, _power_law[i][17])  # pylint: disable=E1101

            _times_ = np.array(_times_[:len(_mtbf_c_plot_ll_)]) # pylint: disable=E1101

            (_new_times_,
             _mtbf_c_plot_ll_,
             _error) = _calc.smooth_curve(_times_, _mtbf_c_plot_ll_,
                                          50 * len(_mtbf_c_plot_ll_))
            _mtbf_c_plot_ul_ = _calc.smooth_curve(_times_, _mtbf_c_plot_ul_,
                                                  50 * len(_mtbf_c_plot_ul_))[1]
            _fi_c_plot_ll_ = _calc.smooth_curve(_times_, _fi_c_plot_ll_,
                                                50 * len(_fi_c_plot_ll_))[1]
            _fi_c_plot_ul_ = _calc.smooth_curve(_times_, _fi_c_plot_ul_,
                                                50 * len(_fi_c_plot_ul_))[1]
            _times_ = _times_.tolist()

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
                            y1=_mtbf_c_plot_, y2=_mtbf_model_,
                            _title_=_(u"Duane Plot of %s Cumulative MTBF") %
                            self.description,
                            _xlab_=_(u"Cumulative Time [hours]"),
                            _ylab_=_(u"Cumulative MTBF [m(t)] "),
                            _marker_=['go', 'k--'],
                            _type_=[2, 2])

            # Plot the smoothed confidence bounds.
            line = matplotlib.lines.Line2D(_new_times_[10:],
                                           _mtbf_c_plot_ll_[10:], lw=1.5,
                                           color='r', ls='-.')
            self.axAxis1.add_line(line)
            line = matplotlib.lines.Line2D(_new_times_[10:],
                                           _mtbf_c_plot_ul_[10:], lw=1.5,
                                           color='b', ls='-.')
            self.axAxis1.add_line(line)

            self.axAxis1.set_xscale('log')
            self.axAxis1.set_yscale('log')

            _text = (_(u"Cumulative MTBF"), _(u"Cum. MTBF LCL"),
                     _(u"Cum. MTBF UCL"), _(u"Fitted Model"))
            _widg.create_legend(self.axAxis1, _text, fontsize='medium',
                                legframeon=True, location='lower right',
                                legshadow=True)

            _widg.load_plot(self.axAxis2, self.pltPlot2, x=_dates_,
                            y1=_mtbf_c_plot_, y2=_mtbf_model_,
                            _title_=_(u"Duane Plot of %s Cumulative MTBF Over "
                                      u"Calendar Time") % self.description,
                            _xlab_=_(u"Calendar Time"),
                            _ylab_=_(u"Cumulative MTBF [m(t)] "),
                            _marker_=['go', 'k--'],
                            _type_=[4, 4])

            _text = (_(u"Cumulative MTBF"), _(u"Cum. MTBF LCL"),
                     _(u"Cum. MTBF UCL"), _(u"Fitted Model"))
            _widg.create_legend(self.axAxis2, _text, fontsize='medium',
                                legframeon=True, location='lower right',
                                legshadow=True)

            # Load the failure intensity versus cumulative operating time.
            _widg.load_plot(self.axAxis3, self.pltPlot3, x=_times_,
                            y1=_fi_c_plot_, y2=_fi_model_,
                            _title_=_(u"Duane Plot of %s Cumulative Failure "
                                      u"Intesity") % self.description,
                            _xlab_=_(u"Cumulative Time [hours]"),
                            _ylab_=_(u"Cumulative Failure Intensity "),
                            _marker_=['go', 'k--'],
                            _type_=[2, 2])

            # Plot the smoothed confidence bounds.
            line = matplotlib.lines.Line2D(_new_times_, _fi_c_plot_ll_,
                                           lw=1.5, color='r', ls='-.')
            self.axAxis3.add_line(line)

            line = matplotlib.lines.Line2D(_new_times_, _fi_c_plot_ul_,
                                           lw=1.5, color='b', ls='-.')
            self.axAxis3.add_line(line)

            self.axAxis3.set_xscale('log')
            self.axAxis3.set_yscale('log')

            _text = (_(u"Cumulative Failure Intensity"), _(u"Cum. FI LCL"),
                     _(u"Cum. FI UCL"), _(u"Fitted Model"))
            _widg.create_legend(self.axAxis3, _text, fontsize='medium',
                                legframeon=True, location='upper right',
                                legshadow=True)

            # Load the failure intensity versus calendar time plot.
            _widg.load_plot(self.axAxis4, self.pltPlot4, x=_dates_[3:],
                            y1=_fi_c_plot_[3:], y2=_fi_model_[3:],
                            _title_=_(u"Duane Plot of %s Cumulative Failure "
                                      u"Intensity Over Calendar Time") %
                            self.description,
                            _xlab_=_(u"Calendar Time"),
                            _ylab_=_(u"Cumulative Failure Intensity "),
                            _marker_=['go', 'k--'],
                            _type_=[4, 4])

            _text = (_(u"Cumulative Failure Intensity"), _(u"Cum. FI LCL"),
                     _(u"Cum. FI UCL"), _(u"Fitted Model"))
            _widg.create_legend(self.axAxis4, _text, fontsize='medium',
                                legframeon=True, location='upper right',
                                legshadow=True)

            for plot in self.vbxPlot1.get_children():
                self.vbxPlot1.remove(plot)

            self.vbxPlot1.pack_start(self.pltPlot1)
            self.vbxPlot1.pack_start(self.pltPlot3)

            for plot in self.vbxPlot2.get_children():
                self.vbxPlot2.remove(plot)

            self.vbxPlot2.pack_start(self.pltPlot2)
            self.vbxPlot2.pack_start(self.pltPlot4)

            self.pltPlot1.draw()

        elif self.distribution_id == 4:     # NHPP - Loglinear

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
            for i in range(len(_results)):
                _F_.append(_results[i][5])
                _X_.append(_results[i][3])
                _dates_.append(_results[i][6])

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
#   18          Lower bound on model estimate of instantaneous failure
#               intensity
#   19          Model point estimate of instantaneous failure intensity
#   20          Upper bound on model estimate of instantaneous failure
#               intensity
            _log_linear = loglinear(_F_, _X_, self.fit_method,
                                    self.confidence_type, _confidence, _T_)

# =========================================================================== #
# Fit the data to an exponential distribution and estimate it's parameters.
# =========================================================================== #
        elif self.distribution_id == 5:
            fit = parametric_fit(_results, self.start_time, self.rel_time,
                                 self.fit_method, 'exponential')

            if self.fit_method == 1:        # MLE
                self.scale[0] = fit[0][0]
                self.scale[1] = fit[0][0] - _z_norm * fit[1][0]
                self.scale[2] = fit[0][0] + _z_norm * fit[1][0]
                self.variance[0] = fit[1][0]**2.0
                self.mle = fit[3][0]
                self.aic = fit[4][0]
                self.bic = fit[5][0]

            elif self.fit_method == 2:      # Rank regression.
                self.scale[0] = 1.0 / exp(fit[0][0])
                self.scale[1] = 1.0 / (exp(fit[0][0] + _z_norm * fit[2][0]))
                self.scale[2] = 1.0 / (exp(fit[0][0] - _z_norm * fit[2][0]))
                self.variance[0] = fit[2][0]
                self.mle = fit[3][0]

            MTBF = 1.0 / self.scale[0]
            MTBFLL = 1.0 / self.scale[1]
            MTBFUL = 1.0 / self.scale[2]

            para = R.list(rate=self.scale[0])
            _theop_ = theoretical_distribution(_censdata, 'exp', para)

            times = [float(i[3]) for i in _results if i[2] <= self.rel_time]
            Rtimes = robjects.FloatVector(times)
            Rtimes = R.sort(Rtimes)
            _qqplot_ = R.qqplot(R.qexp(R.ppoints(Rtimes), rate=self.scale[0]),
                                Rtimes, False)

# =========================================================================== #
# Fit the data to a lognormal and estimate it's parameters.
# =========================================================================== #
        elif self.distribution_id == 6:
            fit = parametric_fit(_results, self.start_time, self.rel_time,
                                 self.fit_method, 'lognormal')

            if self.fit_method == 1:        # MLE
                self.scale[0] = fit[0][0]
                self.scale[1] = self.scale[0] - _z_norm * fit[1][0]
                self.scale[2] = self.scale[0] + _z_norm * fit[1][0]
                self.shape[0] = fit[0][1]
                self.shape[1] = self.shape[0] - _z_norm * fit[1][1]
                self.shape[2] = self.shape[0] + _z_norm * fit[1][1]
                self.variance[0] = fit[2][0]**2
                self.covariance[0] = fit[2][1]**2
                self.variance[0] = fit[2][2]**2
                self.covariance[1] = fit[2][3]**2
                self.mle = fit[3][0]
                self.aic = fit[4][0]
                self.bic = fit[5][0]

            elif self.fit_method == 2:      # Rank regression.
                self.scale[0] = fit[1][0]
                self.shape[0] = fit[1][1]
                self.variance[0] = fit[2][0]
                self.covariance[0] = fit[2][1]
                self.covariance[1] = fit[2][2]
                self.variance[1] = fit[2][3]
                self.scale[1] = self.scale[0] - _z_norm * \
                                sqrt(self.variance[0])
                self.scale[2] = self.scale[0] + _z_norm * \
                                sqrt(self.variance[0])
                self.shape[1] = self.shape[0] - _z_norm * \
                                sqrt(self.variance[1])
                self.shape[2] = self.shape[0] + _z_norm * \
                                sqrt(self.variance[1])

            MTBF = exp(self.scale[0] + 0.5 * self.shape[0]**2.0)
            MTBFLL = exp(self.scale[1] + 0.5 * self.shape[1]**2.0)
            MTBFUL = exp(self.scale[2] + 0.5 * self.shape[2]**2.0)

            para = R.list(sdlog=self.shape[0], meanlog=self.scale[0])
            _theop_ = theoretical_distribution(_censdata, 'lnorm', para)

            times = [float(i[3]) for i in _results if i[2] <= self.rel_time]
            Rtimes = robjects.FloatVector(times)
            Rtimes = R.sort(Rtimes)
            _qqplot_ = R.qqplot(R.qlnorm(R.ppoints(Rtimes),
                                         meanlog=self.scale[0],
                                         sdlog=self.shape[0]), Rtimes, False)

# =========================================================================== #
# Fit the data to a normal distibution and estimate it's parameters.
# =========================================================================== #
        elif self.distribution_id == 7:
            fit = parametric_fit(_results, self.start_time, self.rel_time,
                                 self.fit_method, 'normal')

            if self.fit_method == 1:        # MLE
                self.scale[0] = fit[0][0]
                self.scale[1] = self.scale[0] - _z_norm * fit[1][0]
                self.scale[2] = self.scale[0] + _z_norm * fit[1][0]
                self.shape[0] = fit[0][1]
                self.shape[1] = self.shape[0] - _z_norm * fit[1][1]
                self.shape[2] = self.shape[0] + _z_norm * fit[1][1]
                self.variance[0] = fit[1][0]**2
                self.variance[1] = fit[1][1]**2
                self.mle = fit[3][0]
                self.aic = fit[4][0]
                self.bic = fit[5][0]
            elif self.fit_method == 2:      # Rank regression.
                self.scale[0] = fit[1][0]
                self.shape[0] = exp(fit[1][1])
                self.variance[0] = fit[2][0]
                self.covariance[0] = fit[2][1]
                self.variance[0] = fit[2][2]
                self.variance[1] = fit[2][3]
                self.scale[1] = self.scale[0] - _z_norm * \
                                sqrt(self.variance[0])
                self.scale[2] = self.scale[0] + _z_norm * \
                                sqrt(self.variance[0])
                self.shape[1] = self.shape[0] - _z_norm * \
                                sqrt(self.variance[1])
                self.shape[2] = self.shape[0] + _z_norm * \
                                sqrt(self.variance[1])

            MTBF = self.scale[0]
            MTBFLL = self.scale[1]
            MTBFUL = self.scale[2]

            para = R.list(sd=self.shape[0], mean=self.scale[0])
            _theop_ = theoretical_distribution(_censdata, 'norm', para)

            times = [float(i[3]) for i in _results if i[2] <= self.rel_time]
            Rtimes = robjects.FloatVector(times)
            Rtimes = R.sort(Rtimes)
            _qqplot_ = R.qqplot(R.qnorm(R.ppoints(Rtimes), mean=self.scale[0],
                                        sd=self.shape[0]), Rtimes, False)

# =========================================================================== #
# Fit the data to a Weibull distribution and estimate it's parameters.
# =========================================================================== #
        elif self.distribution_id == 8:
            fit = parametric_fit(_results, self.start_time, self.rel_time,
                                 self.fit_method, 'weibull')

            if self.fit_method == 1:        # MLE
                self.scale[0] = fit[0][1]
                self.scale[1] = self.scale[0] / exp(_z_norm * fit[1][1] /
                                                    self.scale[0])
                self.scale[2] = self.scale[0] * exp(_z_norm * fit[1][1] /
                                                    self.scale[0])
                self.shape[0] = fit[0][0]
                self.shape[1] = self.shape[0] / exp(_z_norm * fit[1][0] /
                                                    self.shape[0])
                self.shape[2] = self.shape[0] * exp(_z_norm * fit[1][0] /
                                                    self.shape[0])
                self.variance[1] = fit[1][0]**2
                self.variance[0] = fit[1][1]**2
                self.mle = fit[3][0]
                self.aic = fit[4][0]
                self.bic = fit[5][0]

                if __USE_RPY2__:
                    MTBF = self.scale[0] * \
                           R.gamma(1.0 + (1.0 / self.shape[0]))[0]
                    MTBFLL = self.scale[1] * \
                             R.gamma(1.0 + (1.0 / self.shape[2]))[0]
                    MTBFUL = self.scale[2] * \
                             R.gamma(1.0 + (1.0 / self.shape[1]))[0]

            elif self.fit_method == 2:      # Regression
                self.scale[0] = exp(fit[1][0])
                self.shape[0] = exp(fit[1][1])
                self.variance[0] = fit[2][0]
                self.covariance[0] = fit[2][1]
                self.variance[1] = fit[2][3]
                self.scale[1] = self.scale[0] - _z_norm * \
                                sqrt(self.variance[0])
                self.scale[2] = self.scale[0] + _z_norm * \
                                sqrt(self.variance[0])
                self.shape[1] = self.shape[0] - _z_norm * \
                                sqrt(self.variance[1])
                self.shape[2] = self.shape[0] + _z_norm * \
                                sqrt(self.variance[1])

                if __USE_RPY2__:
                    MTBF = self.scale[0] * \
                           R.gamma(1.0 + (1.0 / self.shape[0]))[0]
                    MTBFLL = self.scale[1] * \
                             R.gamma(1.0 + (1.0 / self.shape[2]))[0]
                    MTBFUL = self.scale[2] * \
                             R.gamma(1.0 + (1.0 / self.shape[1]))[0]

            para = R.list(shape=self.shape[0], scale=self.scale[0])
            _theop_ = theoretical_distribution(_censdata, 'weibull', para)

            times = [float(i[3]) for i in _results if i[2] <= self.rel_time]
            Rtimes = robjects.FloatVector(times)
            Rtimes = R.sort(Rtimes)
            _qqplot_ = R.qqplot(R.qweibull(R.ppoints(Rtimes),
                                           shape=self.shape[0],
                                           scale=self.scale[0]), Rtimes, False)

        #elif self.distribution_id == 9:     # Fit to a WeiBayes.

# Find the percent of records belonging to each sub-assembly and then allocate
# this percent of the overall failure rate to each sub-assembly.
        if self.chkGroup.get_active():
            _query = "SELECT t2.fld_name, SUM(t1.fld_quantity), \
                             t2.fld_assembly_id \
                      FROM tbl_survival_data AS t1 \
                      INNER JOIN tbl_system AS t2 \
                      ON t1.fld_assembly_id=t2.fld_assembly_id \
                      WHERE t1.fld_dataset_id=%d \
                      AND t1.fld_right_interval <= %f \
                      AND t1.fld_right_interval > %f \
                      AND t1.fld_request_date >= %d \
                      AND t1.fld_request_date < %d \
                      GROUP BY t2.fld_name" % (self.dataset_id, self.rel_time,
                                               self.start_time,
                                               self.start_date, self.end_date)
            _results = self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx)

            _model = self.tvwResultsByChildAssembly.get_model()
            _model.clear()
            _total = float(sum(x[1] for x in _results))
            for i in range(len(_results)):
                if _results[i][1] / _total >= 0.1:
                    _color = 'red'
                elif(_results[i][1] / _total < 0.1 and
                     _results[i][1] / _total >= 0.05):
                    _color = 'yellow'
                elif(_results[i][1] / _total < 0.05 and
                     _results[i][1] / _total >= 0.01):
                    _color = 'white'
                else:
                    _color = 'light gray'

                _values = (_results[i][0], _results[i][1], _results[i][2],
                           (MTBFLL * _total) / float(_results[i][1]),
                           (MTBF * _total) / float(_results[i][1]),
                           (MTBFUL * _total) / float(_results[i][1]),
                           float(_results[i][1]) / (MTBFUL * _total),
                           float(_results[i][1]) / (MTBF * _total),
                           float(_results[i][1]) / (MTBFLL * _total),
                           _color)
                _model.append(_values)

            self.fraResultsByChildAssembly.show_all()

        # Find the percent of records belonging to each component and then
        # allocate this percent of the overall failure rate to each component.
        if self.chkParts.get_active():
            _query = "SELECT t1.fld_part_num, COUNT(t1.fld_part_num) \
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
                      (self._app.REVISION.revision_id, self.rel_time,
                       self.start_time, self.start_date, self.end_date)
            _results = self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx)

            _model = self.tvwResultsByPart.get_model()
            _model.clear()
            _total = float(sum(x[1] for x in _results))
            for i in range(len(_results)):
                if _results[i][1] / _total >= 0.01:
                    _color = 'red'
                elif(_results[i][1] / _total < 0.01 and
                     _results[i][1] / _total >= 0.005):
                    _color = 'yellow'
                elif(_results[i][1] / _total < 0.005 and
                     _results[i][1] / _total >= 0.001):
                    _color = 'white'
                else:
                    _color = 'light gray'

                _values = (_results[i][0], _results[i][1],
                           (MTBFLL * _total) / float(_results[i][1]),
                           (MTBF * _total) / float(_results[i][1]),
                           (MTBFUL * _total) / float(_results[i][1]),
                           float(_results[i][1]) / (MTBFUL * _total),
                           float(_results[i][1]) / (MTBF * _total),
                           float(_results[i][1]) / (MTBFLL * _total),
                           _color)
                _model.append(_values)

# =========================================================================== #
# Create and display parametric plots.
# =========================================================================== #
        if self.distribution_id > 4:
            # Plot a histogram of interarrival times.
            hist = R.hist(Rtimes, plot='False')
            _bins = list(hist[0])
            # counts = list(hist[1])

            __title__ = _(u"Histogram of Interarrival Times for %s") % \
                        self.description
            _widg.load_plot(self.axAxis1, self.pltPlot1,
                            x=Rtimes, y1=_bins,
                            _title_=__title__,
                            _xlab_=_(u"Interarrival Times"),
                            _ylab_=_(u"Count "),
                            _type_=[3],
                            _marker_=['g'])

            # Plot an ECDF of interarrival times.
            Rstats = importr('stats')
            Fn = Rstats.ecdf(Rtimes)        # pylint: disable=E1101
            _ecdf = Fn(Rtimes)

            __title__ = _(u"Empirical CDF of Interarrival Times for %s") % \
                        self.description
            _widg.load_plot(self.axAxis3, self.pltPlot3,
                            x=Rtimes, y1=_ecdf, y2=_theop_[1:],
                            _title_=__title__,
                            _xlab_=_(u"t"),
                            _ylab_=_(u"F(t) "),
                            _type_=[1, 2],
                            _marker_=['b-', 'r:'])

            # Plot the probability plot of interarrival times.
            __title__ = _(u"Probability Plot of Interarrival Times for "
                          u"%s ") % self.description
            _widg.load_plot(self.axAxis4, self.pltPlot4,
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

        if _RELTIME_:
            self.rel_time = 0.0

        # Update results widgets.
        self._update_tree()
        self.load_analyses_results_page()

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

        self.txtMHBPValue.set_text(str(fmt.format(_p_value[0])))
        self.txtZLPPValue.set_text(str(fmt.format(_p_value[1])))
        self.txtZLRPValue.set_text(str(fmt.format(_p_value[2])))
        self.txtRhoPValue.set_text(str(fmt.format(_p_value[3])))

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)

        return False

    def _consolidate_dataset(self, __button):
        """
        Consolidates the data set so there are only unique failure times,
        suspension times, and intervals with a quantity value rather than a
        single record for each failure.

        @param __button: the gtk.Button() that called this function.
        @type __button: gtk.Button
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        _query = "SELECT fld_record_id, fld_unit, fld_left_interval, \
                         fld_right_interval, fld_status, fld_quantity \
                  FROM tbl_survival_data \
                  WHERE fld_dataset_id=%d \
                  ORDER BY fld_unit ASC, \
                           fld_left_interval ASC, \
                           fld_right_interval ASC, \
                           fld_status ASC" % self.dataset_id
        _results = self._app.DB.execute_query(_query, None, self._app.ProgCnx)

        try:
            _n_records = len(_results)
        except TypeError:
            _n_records = 0

        _del_id = []
        _keep_id = []
        _quantity = _results[0][5]
        for i in range(1, _n_records):
        # If the units are the same, the left intervals are the same, the right
        # intervals are the same, and the type are the same, increment the
        # count of records with the same failure times and add the previous
        # record id to the list of records to delete.
            if(_results[i][1] == _results[i - 1][1] and
               _results[i][2] == _results[i - 1][2] and
               _results[i][3] == _results[i - 1][3] and
               _results[i][4] == _results[i - 1][4]):
                _quantity += _results[i][5]
                _del_id.append(_results[i - 1][0])
            else:
                _keep_id.append([_results[i - 1][0], _quantity])
                _quantity = _results[i][5]

        # Keep the last record.
        _keep_id.append([_results[-1][0], _quantity])

        # Update the quantity of the records to be kept.
        _n_keep = len(_keep_id)
        for i in range(_n_keep):
            _query = "UPDATE tbl_survival_data \
                      SET fld_quantity=%d \
                      WHERE fld_record_id=%d" % (_keep_id[i][1],
                                                 _keep_id[i][0])
            self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                       commit=True)

        # Delete the records that are "duplicates."
        _n_del = len(_del_id)
        for i in range(_n_del):
            _query = "DELETE FROM tbl_survival_data \
                      WHERE fld_record_id=%d" % _del_id[i]
            self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                       commit=True)

        # Reload the dataset tree.
        self.load_tree()

        return False
