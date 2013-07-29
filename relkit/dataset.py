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
import calculations as _calc
import configuration as _conf
import imports as _impt
import utilities as _util
import widgets as _widg

from _assistants_.updates import AssignMTBFResults

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
                      _("Start Time:"), _("End Time"), _("Step Interval:")]

    _km = [(3.0, 3.0, u'Interval Censored'), (4.0, 4.0, u'Right Censored'), (5.7, 5.7, u'Right Censored'), (6.5, 6.5, u'Interval Censored'), (6.5, 6.5, u'Interval Censored'), (8.4, 8.4, u'Right Censored'), (10.0, 10.0, u'Interval Censored'), (10.0, 10.0, u'Right Censored'), (12.0, 12.0, u'Interval Censored'), (15.0, 15.0, u'Interval Censored')]

    _exp100 = [(u'', 48.146859, 48.146859, 0.0, 1), (u'', 20.564406, 20.564406, 0.0, 1), (u'', 94.072781, 94.072781, 0.0, 1), (u'', 177.992321, 177.992321, 0.0, 1),
               (u'', 89.103398, 89.103398, 0.0, 1), (u'', 350.577920, 350.577920, 0.0, 1), (u'', 82.223220, 82.223220, 0.0, 1),  (u'', 40.360083, 40.360083, 0.0, 1),
               (u'', 39.576065, 39.576065, 0.0, 1), (u'', 53.127178, 53.127178, 0.0, 1), (u'', 159.732430, 159.732430, 0.0, 1), (u'', 48.398973, 48.398973, 0.0, 1),
               (u'', 46.984010, 46.984010, 0.0, 1), (u'', 36.169584, 36.169584, 0.0, 1), (u'', 351.347799, 351.347799, 0.0, 1), (u'', 18.917324, 18.917324, 0.0, 1),
               (u'', 101.977027, 101.977027, 0.0, 1), (u'', 141.988267, 141.988267, 0.0, 1), (u'', 241.044591, 241.044591, 0.0, 1), (u'', 61.993888, 61.993888, 0.0, 1),
               (u'', 171.813927, 171.813927, 0.0, 1), (u'', 78.747517, 78.747517, 0.0, 1), (u'', 54.070510, 54.070510, 0.0, 1), (u'', 87.229221, 87.229221, 0.0, 1),
               (u'', 158.980289, 158.980289, 0.0, 1), (u'', 185.254974, 185.254974, 0.0, 1), (u'', 16.452673, 16.452673, 0.0, 1), (u'', 120.144229, 120.144229, 0.0, 1),
               (u'', 294.418608, 294.418608, 0.0, 1), (u'', 13.640705, 13.640705, 0.0, 1), (u'', 115.532861, 115.532861, 0.0, 1), (u'', 58.595331, 58.595331, 0.0, 1),
               (u'', 7.876539, 7.876539, 0.0, 1), (u'', 10.790563, 10.790563, 0.0, 1), (u'', 67.342074, 67.342074, 0.0, 1), (u'', 14.848170, 14.848170, 0.0, 1),
               (u'', 82.160622, 82.160622, 0.0, 1), (u'', 14.558010, 14.558010, 0.0, 1), (u'', 18.793071, 18.793071, 0.0, 1), (u'', 69.776958, 69.776958, 0.0, 1),
               (u'', 65.542418, 65.542418, 0.0, 1), (u'', 194.039565, 194.039565, 0.0, 1), (u'', 41.559590, 41.559590, 0.0, 1), (u'', 75.549698, 75.549698, 0.0, 1),
               (u'', 14.808375, 14.808375, 0.0, 1), (u'', 184.263190, 184.263190, 0.0, 1), (u'', 2.810047, 2.810047, 0.0, 1), (u'', 13.095068, 13.095068, 0.0, 1),
               (u'', 52.885757, 52.885757, 0.0, 1), (u'', 49.855286, 49.855286, 0.0, 1), (u'', 263.548942, 263.548942, 0.0, 1), (u'', 4.248489, 4.248489, 0.0, 1),
               (u'', 66.864953, 66.864953, 0.0, 1), (u'', 172.663015, 172.663015, 0.0, 1), (u'', 226.918685, 226.918685, 0.0, 1), (u'', 169.175428, 169.175428, 0.0, 1),
               (u'', 148.070217, 148.070217, 0.0, 1), (u'', 3.679958, 3.679958, 0.0, 1), (u'', 28.693005, 28.693005, 0.0, 1), (u'', 34.931869, 34.931869, 0.0, 1),
               (u'', 297.467901, 297.467901, 0.0, 1), (u'', 137.072180, 137.072180, 0.0, 1), (u'', 53.180089, 53.180089, 0.0, 1), (u'', 49.760206, 49.760206, 0.0, 1),
               (u'', 19.664276, 19.664276, 0.0, 1),  (u'', 96.415132, 96.415132, 0.0, 1), (u'', 14.003862, 14.003862, 0.0, 1), (u'', 17.743755, 17.743755, 0.0, 1),
               (u'', 212.279301, 212.279301, 0.0, 1), (u'', 38.951314, 38.951314, 0.0, 1), (u'', 74.057822, 74.057822, 0.0, 1), (u'', 86.769323, 86.769323, 0.0, 1),
               (u'', 37.765341, 37.765341, 0.0, 1), (u'', 5.566417, 5.566417, 0.0, 1), (u'', 71.048013, 71.048013, 0.0, 1), (u'', 5.137094, 5.137094, 0.0, 1),
               (u'', 35.461923, 35.461923, 0.0, 1), (u'', 121.963923, 121.963923, 0.0, 1), (u'', 42.486536, 42.486536, 0.0, 1), (u'', 52.315419, 52.315419, 0.0, 1),
               (u'', 77.095150, 77.095150, 0.0, 1), (u'', 14.259343, 14.259343, 0.0, 1), (u'', 111.147273, 111.147273, 0.0, 1), (u'', 49.364508, 49.364508, 0.0, 1),
               (u'', 1.978637, 1.978637, 0.0, 1), (u'', 163.827122, 163.827122, 0.0, 1), (u'', 66.690012, 66.690012, 0.0, 1), (u'', 80.172196, 80.172196, 0.0, 1),
               (u'', 323.763002, 323.763002, 0.0, 1), (u'', 275.491419, 275.491419, 0.0, 1), (u'', 49.315958, 49.315958, 0.0, 1), (u'', 1.585178, 1.585178, 0.0, 1),
               (u'', 317.922638, 317.922638, 0.0, 1), (u'', 12.398458, 12.398458, 0.0, 1), (u'', 222.930804, 222.930804, 0.0, 1), (u'', 6.328506, 6.328506, 0.0, 1),
               (u'', 143.687402, 143.687402, 0.0, 1), (u'', 134.763300, 134.763300, 0.0, 1), (u'', 88.862705, 88.862705, 0.0, 1), (u'', 143.918067, 143.918067, 0.0, 1)]

    _norm100 = [(u'', 95.37050, 95.37050, 0.0, 1), (u'', 0.0, 114.01126, 0.0, 1), (u'', 0.0, 113.24685, 0.0, 1), (u'', 0.0, 109.16715, 0.0, 1), (u'', 0.0, 104.22744, 0.0, 1),
                (u'', 107.10937, 107.10937, 0.0, 1), (u'', 0.0, 117.43215, 0.0, 1), (u'', 0.0, 94.78554, 0.0, 1), (u'', 0.0, 83.56718, 0.0, 1), (u'', 0.0, 103.50167, 0.0, 1),
                (u'', 89.93169, 89.93169, 0.0, 1), (u'', 0.0, 120.45587, 0.0, 1), (u'', 0.0, 97.08137, 0.0, 1), (u'', 0.0, 96.81358, 0.0, 1), (u'', 0.0, 97.57112, 0.0, 1),
                (u'', 106.75722, 106.75722, 0.0, 1), (u'', 0.0, 99.33548, 0.0, 1), (u'', 0.0, 104.53866, 0.0, 1), (u'', 0.0, 102.02819, 0.0, 1), (u'', 0.0, 90.03242, 0.0, 1),
                (u'', 77.54299, 77.54299, 0.0, 1), (u'', 0.0, 102.76149, 0.0, 1), (u'', 0.0, 82.48589, 0.0, 1), (u'', 0.0, 77.74356, 0.0, 1), (u'', 0.0, 109.97453, 0.0, 1),
                (u'', 94.85149, 94.85149, 0.0, 1), (u'', 0.0, 89.77114, 0.0, 1), (u'', 0.0, 98.19346, 0.0, 1), (u'', 0.0, 102.16592, 0.0, 1), (u'', 0.0, 96.78387, 0.0, 1),
                (u'', 108.86581, 108.86581, 0.0, 1), (u'', 0.0, 120.46225, 0.0, 1), (u'', 0.0, 111.59290, 0.0, 1), (u'', 0.0, 106.14877, 0.0, 1), (u'', 0.0, 102.94616, 0.0, 1),
                (u'', 111.29011, 111.29011, 0.0, 1), (u'', 0.0, 106.00202, 0.0, 1), (u'', 0.0, 114.61717, 0.0, 1), (u'', 0.0, 88.22994, 0.0, 1), (u'', 0.0, 131.36413, 0.0, 1),
                (u'', 86.85545, 86.85545, 0.0, 1), (u'', 0.0, 109.92748, 0.0, 1), (u'', 0.0, 75.11669, 0.0, 1), (u'', 0.0, 100.46514, 0.0, 1), (u'', 0.0, 97.78360, 0.0, 1),
                (u'', 108.16912, 108.16912, 0.0, 1), (u'', 0.0, 98.85145, 0.0, 1), (u'', 0.0, 99.31015, 0.0, 1), (u'', 0.0, 94.58853, 0.0, 1), (u'', 0.0, 98.12350, 0.0, 1),
                (u'', 115.66660, 115.66660, 0.0, 1), (u'', 0.0, 104.49188, 0.0, 1), (u'', 0.0, 93.49034, 0.0, 1), (u'', 0.0, 111.79487, 0.0, 1), (u'', 0.0, 114.32069, 0.0, 1),
                (u'', 106.93861, 106.93861, 0.0, 1), (u'', 0.0, 106.45058, 0.0, 1), (u'', 0.0, 103.10528, 0.0, 1), (u'', 0.0, 107.78179, 0.0, 1), (u'', 0.0, 120.84600, 0.0, 1),
                (u'', 100.10230, 100.10230, 0.0, 1), (u'', 0.0, 92.93094, 0.0, 1), (u'', 0.0, 101.24658, 0.0, 1), (u'', 0.0, 69.51782, 0.0, 1), (u'', 0.0, 106.27645, 0.0, 1),
                (u'', 99.04622, 99.04622, 0.0, 1), (u'', 0.0, 101.30087, 0.0, 1), (u'', 0.0, 98.58876, 0.0, 1), (u'', 0.0, 110.02258, 0.0, 1), (u'', 0.0, 91.25592, 0.0, 1),
                (u'', 106.68794, 106.68794, 0.0, 1), (u'', 0.0, 102.44362, 0.0, 1), (u'', 0.0, 100.34289, 0.0, 1), (u'', 0.0, 96.63522, 0.0, 1), (u'', 0.0, 80.90978, 0.0, 1),
                (u'', 111.08013, 111.08013, 0.0, 1), (u'', 0.0, 107.00581, 0.0, 1), (u'', 0.0, 103.04357, 0.0, 1), (u'', 0.0, 92.66092, 0.0, 1), (u'', 0.0, 81.52659, 0.0, 1),
                (u'', 94.49750, 94.49750, 0.0, 1), (u'', 0.0, 88.79105, 0.0, 1), (u'', 0.0, 97.91323, 0.0, 1), (u'', 0.0, 96.12042, 0.0, 1), (u'', 0.0, 101.23497, 0.0, 1),
                (u'', 95.13220, 95.13220, 0.0, 1), (u'', 0.0, 93.93901, 0.0, 1), (u'', 0.0, 92.30268, 0.0, 1), (u'', 0.0, 96.53697, 0.0, 1), (u'', 0.0, 110.74783, 0.0, 1),
                (u'', 99.88812, 99.88812, 0.0, 1), (u'', 0.0, 92.78015, 0.0, 1), (u'', 0.0, 107.67842, 0.0, 1), (u'', 0.0, 96.18725, 0.0, 1), (u'', 0.0, 87.93806, 0.0, 1),
                (u'', 91.66445, 91.66445, 0.0, 1), (u'', 0.0, 106.14925, 0.0, 1), (u'', 0.0, 104.32056, 0.0, 1), (u'', 0.0, 115.68135, 0.0, 1), (u'', 0.0, 95.92033, 0.0, 1)]

    def __init__(self, application):
        """
        Initializes the Dataset Object.

        Keyword Arguments:
        application -- the RTK application.
        """

        self._ready = False

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
        self.cmbAssembly = _widg.make_combo(simple=False)
        self.cmbConfType = _widg.make_combo()
        self.cmbConfMethod = _widg.make_combo()
        self.cmbDistribution = _widg.make_combo()
        self.cmbFitMethod = _widg.make_combo()
        self.cmbSource = _widg.make_combo()

        self.lblFitMethod = _widg.make_label(self._ai_tab_labels[4], 150, 25)
        self.lblConfMethod = _widg.make_label(self._ai_tab_labels[7], 150, 25)

        self.tvwDataset = gtk.TreeView()
        self.tvwDataset.set_search_column(0)
        self.tvwDataset.set_reorderable(True)

        self.txtConfidence = _widg.make_entry(_width_=100)
        self.txtDescription = _widg.make_entry(_width_=400)
        self.txtStartTime = _widg.make_entry(_width_=100)
        self.txtEndTime = _widg.make_entry(_width_=100)
        self.txtRelPoints = _widg.make_entry(_width_=100)

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

        self.hbxAnalysisResults = gtk.HBox()
        self.vbxAnalysisResults1 = gtk.VBox()
        self.vbxAnalysisResults2 = gtk.VBox()
        self.hbxAnalysisResults.pack_start(self.vbxAnalysisResults1, True, True)
        self.hbxAnalysisResults.pack_start(self.vbxAnalysisResults2, True, True)

        self.txtMHB = _widg.make_entry(_width_=150)
        self.txtChiSq = _widg.make_entry(_width_=150)
        self.txtMHBPValue = _widg.make_entry(_width_=150)
        self.lblMHBResult = _widg.make_label(_(u""), width=150)
        self.txtLP = _widg.make_entry(_width_=150)
        self.txtZLPNorm = _widg.make_entry(_width_=150)
        self.txtZLPPValue = _widg.make_entry(_width_=150)
        self.lblZLPResult = _widg.make_label(_(u""), width=150)
        self.txtLR = _widg.make_entry(_width_=150)
        self.txtZLRNorm = _widg.make_entry(_width_=150)
        self.txtZLRPValue = _widg.make_entry(_width_=150)
        self.lblZLRResult = _widg.make_label(_(u""), width=150)
        self.txtScale = _widg.make_entry(_width_=150)
        self.txtScaleLL = _widg.make_entry(_width_=150)
        self.txtScaleUL = _widg.make_entry(_width_=150)
        self.txtShape = _widg.make_entry(_width_=150)
        self.txtShapeLL = _widg.make_entry(_width_=150)
        self.txtShapeUL = _widg.make_entry(_width_=150)
        self.txtLocation = _widg.make_entry(_width_=150)
        self.txtLocationLL = _widg.make_entry(_width_=150)
        self.txtLocationUL = _widg.make_entry(_width_=150)
        self.lblRowScale = _widg.make_label(_(u"Scale"), width=150)
        self.lblRowShape = _widg.make_label(_(u"Shape"), width=150)
        self.lblRowLocation = _widg.make_label(_(u"Location"), width=150)
        self.lblColScale = _widg.make_label(_(u"Scale"), width=150)
        self.lblColShape = _widg.make_label(_(u"Shape"), width=150)
        self.lblColLocation = _widg.make_label(_(u"Location"), width=150)
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
        self.txtNumSuspensions = _widg.make_entry(_width_=100)
        self.txtNumFailures = _widg.make_entry(_width_=100)
        self.txtMTBF = _widg.make_entry(_width_=150)
        self.txtMTBFLL = _widg.make_entry(_width_=150)
        self.txtMTBFUL = _widg.make_entry(_width_=150)

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

# Add record button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        button.set_icon_widget(image)
        button.set_name('Add')
        button.connect('clicked', self._record_add)
        button.set_tooltip_text(_(u"Adds a record to the selected data set."))
        toolbar.insert(button, 0)

# Remove record button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        button.set_icon_widget(image)
        button.set_name('Remove')
        button.connect('clicked', self._record_remove)
        button.set_tooltip_text(_(u"Removes the selected record from the data set."))
        toolbar.insert(button, 1)

# Calculate button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        button.set_icon_widget(image)
        button.set_name('Calculate')
        button.connect('clicked', self._calculate)
        button.set_tooltip_text(_(u"Analyzes the selected data set."))
        toolbar.insert(button, 2)

# Bathtub search button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/eyes.png')
        button.set_icon_widget(image)
        button.set_name('Bathtub Search')
        button.connect('clicked', self._calculate)
        button.set_tooltip_text(_(u"Searches the selected data set for transition points."))
        toolbar.insert(button, 3)

# Save button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        button.set_icon_widget(image)
        button.set_name('Save')
        button.connect('clicked', self.dataset_save)
        button.set_tooltip_text(_(u"Saves the selected data set."))
        toolbar.insert(button, 4)

# Assign results to affected assembly.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/import.png')
        button.set_icon_widget(image)
        button.set_name('Assign')
        button.connect('clicked', AssignMTBFResults, self._app)
        button.set_tooltip_text(_(u"Assigns MTBF and hazard rate results to the selected assembly."))
        toolbar.insert(button, 5)

        toolbar.show()

        return(toolbar)

    def _analyses_input_widgets_create(self):
        """ Method to create the Analysis Input widgets. """

# Quadrant 1 (upper left) widgets.
        self.cmbAssembly.set_tooltip_text(_(u"Selects and displays the assembly associated with the dataset."))
        self.cmbAssembly.connect('changed', self._callback_combo, 1)

        self.cmbSource.set_tooltip_text(_(u"Selects and displays the source of the selected data set."))
        results = [["ALT"], ["Reliability Growth"],
                   ["Reliability Demonstration"], ["Field"]]
        _widg.load_combo(self.cmbSource, results)
        self.cmbSource.connect('changed', self._callback_combo, 3)

        self.cmbDistribution.set_tooltip_text(_(u"Selects and displays the statistical distribution used to fit the data."))
        results = [["MCF"], ["Kaplan-Meier"], ["Exponential"], ["Lognormal"],
                   ["Normal"], ["Weibull"], ["WeiBayes"]]
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

        model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_STRING)
        self.tvwDataset.set_model(model)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('visible', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Record\nID"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        column.set_visible(0)
        self.tvwDataset.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'white')
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
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Right"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=3)
        column.set_sort_column_id(3)
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
        cell.connect('changed', self._callback_combo_cell, 4, model)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Status"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=4)
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
        scrollwindow.add_with_viewport(self.tvwDataset)

        hbox.pack_start(scrollwindow, True, True)

# Populate tab.
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
        y_pos += 35

        label = _widg.make_label(self._ai_tab_labels[8], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtStartTime, 205, y_pos)
        y_pos += 30

        label = _widg.make_label(self._ai_tab_labels[9], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtEndTime, 205, y_pos)
        y_pos += 30

        label = _widg.make_label(self._ai_tab_labels[10], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtRelPoints, 205, y_pos)
        y_pos += 30

        fixed.show_all()

        hbox.pack_start(frame, True, True)

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

        self._load_dataset_tree()

        return False

    def _load_dataset_tree(self):
        """ Method used to load the survival dataset in the gtk.TreeView. """

# Load the gtk.TreeView containing the list of failure/censoring times.
        query = "SELECT fld_record_id, fld_unit, fld_left_interval, \
                        fld_right_interval, fld_status \
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
            _data = [results[i][0], results[i][1], results[i][2],
                     results[i][3], results[i][4]]
            model.append(_data)

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

        self.txtMHB.set_tooltip_markup(_(u"Displays the value of the MIL-HDBK test for trend."))
        self.txtChiSq.set_tooltip_markup(_(u"Displays the chi square critical value for the MIL-HDBK test for trend."))
        self.txtMHBPValue.set_tooltip_markup(_(u"Displays the p-value for the MIL-HDBK test for trend."))
        self.lblMHBResult.set_use_markup(True)
        self.txtLP.set_tooltip_markup(_(u"Displays the value of the LaPlace test for trend."))
        self.txtZLPNorm.set_tooltip_markup(_(u"Displays the standard normal critical value for the LaPlace test for trend."))
        self.txtZLPPValue.set_tooltip_markup(_(u"Displays the p-value for the Laplace test for trend."))
        self.lblZLPResult.set_use_markup(True)
        self.txtLR.set_tooltip_markup(_(u"Displays the value of the Lewis-Robinson test for trend."))
        self.txtZLRNorm.set_tooltip_markup(_(u"Displays the standard normal critical value for the Lewis-Robinson test for trend."))
        self.txtZLRPValue.set_tooltip_markup(_(u"Displays the p-value for the Lewis-Robinson test for trend."))
        self.lblZLRResult.set_use_markup(True)
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
        label = _widg.make_label(_(u"Estimated MTBF"), width=200)
        fixed.put(label, 415, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"Number of Failures:"), width=200)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtNumFailures, 210, y_pos)
        label = _widg.make_label(_(u"Lower Bound"), width=150)
        fixed.put(label, 415, y_pos)
        label = _widg.make_label(_(u"Point Estimate"), width=150)
        fixed.put(label, 565, y_pos)
        label = _widg.make_label(_(u"Upper Bound"), width=150)
        fixed.put(label, 715, y_pos)
        y_pos += 30

        fixed.put(self.txtMTBFLL, 415, y_pos)
        fixed.put(self.txtMTBF, 565, y_pos)
        fixed.put(self.txtMTBFUL, 715, y_pos)
        y_pos += 30

# Non-parametric table of results.
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
        self.tvwNonParResults.set_model(model)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Time"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u""))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=1)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u""))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=2)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u""))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=3)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"S(t)"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=4)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Standard\nError"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=5)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Lower\nBound"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=6)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Upper\nBound"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=7)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Cumulative\nMTBF"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=8)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Upper\nBound"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=9)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Upper\nBound"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=10)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Instantaneous\nMTBF"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=11)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Upper\nBound"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=12)
        self.tvwNonParResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Upper\nBound"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=13)
        self.tvwNonParResults.append_column(column)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add(self.tvwNonParResults)

        self.fraNonParEst.add(scrollwindow)

# Non-parametric statistics.
        fixed = gtk.Fixed()
        self.fraNonParStats.add(fixed)

        y_pos = 5
        label = _widg.make_label(_(u"MIL Handbook"), width=150)
        fixed.put(label, 155, y_pos)

        label = _widg.make_label(_(u"Laplace"), width=150)
        fixed.put(label, 305, y_pos)

        label = _widg.make_label(_(u"Lewis-Robinson"), width=150)
        fixed.put(label, 455, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"Test Statistic"), width=150)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtMHB, 155, y_pos)
        fixed.put(self.txtLP, 305, y_pos)
        fixed.put(self.txtLR, 455, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"Critical Value"), width=150)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtChiSq, 155, y_pos)
        fixed.put(self.txtZLPNorm, 305, y_pos)
        fixed.put(self.txtZLRNorm, 455, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"p-Value"), width=150)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtMHBPValue, 155, y_pos)
        fixed.put(self.txtZLPPValue, 305, y_pos)
        fixed.put(self.txtZLRPValue, 455, y_pos)
        y_pos += 30

        fixed.put(self.lblMHBResult, 155, y_pos)
        fixed.put(self.lblZLPResult, 305, y_pos)
        fixed.put(self.lblZLRResult, 455, y_pos)

# Parametric estimates.
        fixed = gtk.Fixed()
        self.fraParEst.add(fixed)

        y_pos = 5
        label = _widg.make_label(_(u"Scale"), width=150)
        fixed.put(label, 155, y_pos)

        label = _widg.make_label(_(u"Shape"), width=150)
        fixed.put(label, 305, y_pos)

        label = _widg.make_label(_(u"Location"), width=150)
        fixed.put(label, 455, y_pos)
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
        self.notebook.insert_page(self.hbxAnalysisResults,
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
        for child in self.vbxAnalysisResults1.get_children():
            self.vbxAnalysisResults1.remove(child)
        for child in self.vbxAnalysisResults2.get_children():
            self.vbxAnalysisResults2.remove(child)

# Update summary information.
        self.vbxAnalysisResults1.pack_start(self.fraSummary, True, True)
        self.txtNumSuspensions.set_text(
            str(self.model.get_value(self.selected_row, 11)))
        self.txtNumFailures.set_text(
            str(self.model.get_value(self.selected_row, 12)))

# Update mean cumulative function information.
        if(_analysis_ == 1):
            self.vbxAnalysisResults1.pack_start(self.fraNonParStats, True, True)
            self.vbxAnalysisResults2.pack_start(self.fraNonParEst, True, True)
            #self.hbxAnalysisResults.pack_start(self.vbxAnalysisResults1, True, True)
            #self.hbxAnalysisResults.pack_start(self.vbxAnalysisResults2, True, True)
            self.txtMHB.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 28))))
            self.txtLP.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 29))))
            self.txtLR.set_text(
                str(fmt.format(self.model.get_value(self.selected_row, 30))))

# Update Kaplan-Meier analysis information.
        elif(_analysis_ == 2):
            self.vbxAnalysisResults2.pack_start(self.fraNonParEst, True, True)
            #self.hbxAnalysisResults.pack_start(self.vbxAnalysisResults1, True, True)
            #self.hbxAnalysisResults.pack_start(self.vbxAnalysisResults2, True, True)

# Update parametric analysis information.
        else:
            self.vbxAnalysisResults1.pack_start(self.fraParEst, True, True)
            self.vbxAnalysisResults2.pack_start(self.fraVarCov, True, True)
            self.vbxAnalysisResults2.pack_start(self.fraParGOF, True, True)
            #self.hbxAnalysisResults.pack_start(self.vbxAnalysisResults1, True, True)
            #self.hbxAnalysisResults.pack_start(self.vbxAnalysisResults2, True, True)

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

        axis.set_title(_title_)
        axis.set_xlabel(_xlab_)
        axis.set_ylabel(_ylab_)

        plot.draw()

        return False

    def _record_add(self):

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
        query = "SELECT fld_unit, fld_left_interval, \
                        fld_right_interval, fld_tbf, \
                        fld_status \
                 FROM tbl_survival_data \
                 WHERE fld_dataset_id=%d \
                 AND fld_right_interval <= %f \
                 AND fld_right_interval > 0.0 \
                 ORDER BY fld_unit ASC, \
                          fld_left_interval ASC" % (_dataset_, _reltime_)
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

        censdata = []
        for i in range(len(results)):
            censdata.append([results[i][1], results[i][2]])

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
        p_value = [1.0, 1.0, 1.0]
        _text = [u"", u"", u""]

# =========================================================================== #
# Perform the 'bathtub search.'  This is a search for the minimum and/or
# maximum times at which the values of the Weibull scale and shape parameters
# begin to differ by a given amount.
# =========================================================================== #
        if(button.get_name() == 'Bathtub Search'):
            (scale, deltascale,
             shape, deltashape,
             times) = _calc.bathtub_filter(results, _starttime_,
                                           _reltime_, _step_)

# Plot the estimated eta value versus starting time.
            __title__ = _(u"Percent Change in Eta")
            self._load_plot(self.axAxis1, self.pltPlot1,
                            x=times, y1=deltascale,
                            _title_=__title__,
                            _xlab_=_(u"Start Time (t0)"),
                            _ylab_=_(u"% Change in Eta"),
                            _type_=[2],
                            _marker_=['g-'])

# Plot the estimated beta value versus starting time.
            __title__ = _(u"Percent Change in Beta")
            self._load_plot(self.axAxis2, self.pltPlot2,
                            x=times, y1=deltashape,
                            _title_=__title__,
                            _xlab_=_(u"Start Time (t0)"),
                            _ylab_=_(u"% Change in Beta "),
                            _type_=[2],
                            _marker_=['g-'])

# Plot the change in the Weibull scale parameter (eta) as a function of
# minimum and/or maximum operating times.
            for plot in self.vbxPlot1.get_children():
                self.vbxPlot1.remove(plot)

            self.vbxPlot1.pack_start(self.pltPlot1)

# Plot the change in the Weibull shape parameter (beta) as a function of
# minimum and/or maximum operating times.
            for plot in self.vbxPlot2.get_children():
                self.vbxPlot2.remove(plot)

            self.vbxPlot2.pack_start(self.pltPlot2)

            return False

# =========================================================================== #
# Perform Nelson's mean cumulative function analysis.
# =========================================================================== #
        if(_analysis_ == 1):                # MCF
# Create a list of unique units.
            query = "SELECT DISTINCT(fld_unit) \
                     FROM tbl_survival_data \
                     WHERE fld_dataset_id=%d \
                     AND fld_right_interval <= %f \
                     AND fld_right_interval > %f" % \
                     (_dataset_, _reltime_, _starttime_)
            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx)

            _units_ = []
            for i in range(len(results)):
                _units_.append(results[i][0])

# Create a list of unique failure times.
            query = "SELECT DISTINCT(fld_right_interval) \
                     FROM tbl_survival_data \
                     WHERE fld_dataset_id=%d \
                     AND fld_right_interval >= %f \
                     AND fld_right_interval <= %f \
                     ORDER BY fld_right_interval ASC" % \
                     (_dataset_, _starttime_, _reltime_)
            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx)

            _times_ = []
            for i in range(len(results)):
                _times_.append(results[i][0])

# Get the entire dataset.
# Example of a record returned from the following query:
#     (u'HT36103', 0.0, 12.0, 12.0)
            query = "SELECT fld_unit, fld_left_interval, \
                            fld_right_interval, fld_tbf \
                     FROM tbl_survival_data \
                     WHERE fld_dataset_id=%d \
                     AND fld_right_interval >= %f \
                     AND fld_right_interval <= %f \
                     ORDER BY fld_unit ASC, \
                              fld_left_interval ASC" % \
                     (_dataset_, _starttime_, _reltime_)
            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx)

# =========================================================================== #
#  0 = Event Time ti. (string)
#  1 = Delta array at time ti. (array of integers)
#  2 = d array at time ti. (array of integers)
#  3 = Sum of delta at time ti. (integer)
#  4 = Sum of d at time ti. (integer)
#  5 = d bar at time ti. (float)
#  6 = Variance of d bar at time ti. (float)
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
            nonpar = _calc.mean_cumulative_function(_units_, _times_,
                                                    results, _conf_)

# Get:
#   Total number of failures.
#   List of unique failures times.
#   List of MCF at each unique failure time.
#   List of MCF lower bound at each unique failure time.
#   List of MCF upper bound at each unique failure time.
#   Maximum observed time.
            n_failures = len(nonpar)
            times = [x[0] for x in nonpar]
            muhat = [x[9] for x in nonpar]
            muhatll = [x[7] for x in nonpar]
            muhatul = [x[8] for x in nonpar]
            ta = max(times)

# Calculate the MIL-HDBK-189, Laplace, and Lewis-Robinson test statistics.
# Find the chi-square critical value.  These statistics are used to test for
# HPP vs. NHPP in the data.
            query = "SELECT t1.fld_unit, t2.fld_tbf \
                     FROM tbl_incident AS t1 \
                     INNER JOIN tbl_survival_data AS t2 \
                     WHERE t2.fld_record_id=t1.fld_incident_id \
                     AND fld_dataset_id=%d \
                     AND fld_right_interval >= %f \
                     AND fld_right_interval <= %f \
                     ORDER BY t1.fld_request_date ASC" % \
                     (_dataset_, _starttime_, _reltime_)
            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx)

            tbf = []
            failnum = []
            _denominator_ = 0.0
            for i in range(n_failures):
                mhb += log(times[i] / ta)
                _denominator_ += log(ta / times[i])
                zlp += times[i] / ta
                tbf.append(results[i][1])
                failnum.append(i)

            mhb = -2.0 * mhb
            zlp = (zlp - (n_failures / 2.0)) / sqrt(n_failures / 12.0)
            tau = numpy.mean(tbf)
            S = numpy.std(tbf)
            zlr = zlp * tau / S

            _chisq_ = chi2.ppf(1.0 - _conf_, 2 * n_failures)
            p_value[0] = chi2.cdf(mhb, 2 * n_failures)
            p_value[1] = norm.cdf(abs(zlp))
            p_value[2] = norm.cdf(abs(zlr))

            _beta_ = n_failures / _denominator_
            _eta_ = ta / n_failures**(1.0 / _beta_)

# Find the covariance and variance of the interarrival times.  Use these to
# calculate the sample serial correlation coefficient.
            cov = numpy.cov(tbf[0:n_failures-1], tbf[1:n_failures])
            var = numpy.var(tbf)
            rho = sqrt(n_failures - 1) * cov[0][1] / var

# Load the table with the MCF results.
#   Column      Information
#     1         Time (t_j)
#     2         Delta dot
#     3         d bar
#     4         MCF standard error
#     5         MCF point estimate
#     6         MCF lower bound
#     7         MCF upper bound
#     8         Cumulative MTBF
#     9         Cumulative MTBF lower bound
#    10         Cumulative MTBF upper bound
#    11         Instantaneous MTBF
#    12         Instantaneous MTBF lower bound
#    13         Instantaneous MTBF upper bound
            model = self.tvwNonParResults.get_model()
            model.clear()
            for i in range(n_failures):
                _data_ = [str(nonpar[i][0]), int(nonpar[i][3]),
                          int(nonpar[i][4]), float(nonpar[i][5]),
                          float(nonpar[i][6]), float(nonpar[i][9]),
                          float(nonpar[i][7]), float(nonpar[i][8]),
                          float(nonpar[i][10]), float(nonpar[i][11]),
                          float(nonpar[i][12]), float(nonpar[i][13]),
                          float(nonpar[i][14]), float(nonpar[i][15])]
                model.append(_data_)

            column = self.tvwNonParResults.get_column(1)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>\u03B4.</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(2)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>d.</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(3)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>d bar</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(4)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>se<sub>MCF</sub></span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(5)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>MCF</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(6)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>MCF Lower\nBound</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(7)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>MCF Upper\nBound</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(8)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>Cumulative\nMTBF</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(9)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>Cumulative\nMTBF\nLower Bound</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(10)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>Cumulative\nMTBF\nUpper Bound</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(11)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>Instantaneous\nMTBF</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(12)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>Instantaneous\nMTBF\nLower Bound</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(13)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>Instantaneous\nMTBF\nUpper Bound</span>"))
            column.set_widget(label)

# Plot the mean cumulative function with confidence bounds.
            self._load_plot(self.axAxis1, self.pltPlot1, x=times, y1=muhat,
                            y2=muhatll, y3=muhatul,
                            _title_=_(u"MCF Plot of %s") % _name,
                            _xlab_=_(u"Time"),
                            _ylab_=_(u"Mean Cumulative Function [mu(t)]"),
                            _marker_=['g-', 'r-', 'b-'])

            for plot in self.vbxPlot1.get_children():
                self.vbxPlot1.remove(plot)

            self.vbxPlot1.pack_start(self.pltPlot1)

# Plot the run sequence plot.
            self._load_plot(self.axAxis2, self.pltPlot2,
                            x=failnum, y1=tbf, y2=None, y3=None,
                            _title_=_(u"Run Sequence Plot of %s") % _name,
                            _xlab_=_(u"Failure Number"),
                            _ylab_=_(u"Time Between Failure"),
                            _type_=[2], _marker_=['g-'])

# Create an event plot.
            #query = "SELECT DISTINCT t1.fld_unit, t2.fld_age_at_incident \
            #         FROM tbl_incident AS t1 \
            #         INNER JOIN tbl_incident_detail AS t2 \
            #         WHERE t2.fld_incident_id=t1.fld_incident_id \
            #         ORDER BY t1.fld_unit ASC, \
            #                  t2.fld_age_at_incident ASC"
            #results = self._app.DB.execute_query(query,
            #                                     None,
            #                                     self._app.ProgCnx)
            #self._load_plot(self.axAxis4, self.pltPlot4,
            #                x=tbf[0:n_failures - 1], y1=tbf[1:n_failures],
            #                y2=None, y3=None,
            #                _title_=_(u"Lag 1 Plot of %s") % _name,
            #                _xlab_=_(u"Lagged Time Between Failure"),
            #                _ylab_=_(u"Time Between Failure"),
            #                _type_=[2], _marker_=['go'])

            for plot in self.vbxPlot2.get_children():
                self.vbxPlot2.remove(plot)

            self.vbxPlot2.pack_start(self.pltPlot2)
            #self.vbxPlot2.pack_start(self.pltPlot4)

            self.txtChiSq.set_text(str(fmt.format(_chisq_)))
            self.txtZLPNorm.set_text(str(fmt.format(_z_norm_)))
            self.txtZLRNorm.set_text(str(fmt.format(_z_norm_)))

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
            query = "SELECT fld_left_interval, fld_right_interval, \
                            fld_status, fld_unit \
                     FROM tbl_survival_data \
                     WHERE fld_dataset_id=%d \
                     AND fld_right_interval >= %f \
                     AND fld_right_interval <= %f \
                     ORDER BY fld_right_interval ASC, \
                     fld_status DESC" % (_dataset_, _starttime_, _reltime_)
            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx)

# Make a list with the rank of the records that are failures.
            r = []
            for i in range(len(results)):
                if(results[i][2] == 'Event' or
                   results[i][2] == 'Interval Censored'):
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
            nonpar = _calc.kaplan_meier(results, _reltime_, _conf_)

            n_points = nonpar[0][0]
            times = nonpar[1]
            Shat = nonpar[5]
            Shatll = nonpar[8]
            Shatul = nonpar[9]

# Initialize some list variables.
            logtimes = []
            _H_ = []
            _Hll_ = []
            _Hul_ = []
            logH = []
            logHll = []
            logHul = []
            zShat = []
            _h_ = []
            _hll_ = []
            _hul_ = []
            tr = []
            S = []

# Calculate the cumulative hazard rate, the hazard rate, and the log
# hazard rate.
            for i in range(len(times)):
                logtimes.append(log(times[i]))

                try:
                    _H_.append(-log(Shat[i]))
                    _Hll_.append(-log(Shatul[i]))
                    _Hul_.append(-log(Shatll[i]))
                except ValueError:
                    try:
                        _H_.append(_H_[i - 1])
                        _Hll_.append(_Hll_[i - 1])
                        _Hul_.append(_Hul_[i - 1])
                    except IndexError:
                        _H_.append(0.0)
                        _Hll_.append(0.0)
                        _Hul_.append(0.0)
                except IndexError:
# TODO: Write error handling routine for KM cumulative hazard plots.
                    print i, _H_, _Hll_, _Hul_

                try:
                    logH.append(log(_H_[i]))
                    logHll.append(log(_Hll_[i]))
                    logHul.append(log(_Hul_[i]))
                except ValueError:
                    try:
                        logH.append(logH[i - 1])
                        logHll.append(logHll[i - 1])
                        logHul.append(logHul[i - 1])
                    except IndexError:
                        logH.append(0.0)
                        logHll.append(0.0)
                        logHul.append(0.0)

                zShat.append(norm.ppf(Shat[i]))
                _h_.append(_H_[i] / times[i])
                _hll_.append(_Hll_[i] / times[i])
                _hul_.append(_Hul_[i] / times[i])

# Calculate the mean time between failure.
                if(nonpar[3][i] != 0):      # Event occured at this time.
                    for j in range(int(floor(nonpar[3][i]))):
                        tr.append(nonpar[1][i])
                        S.append(nonpar[5][i])

# Calculate the number of failures and suspensions in the dataset.
            n_failures = len(tr)
            n_suspensions = n_points - n_failures

# Calculate the MTBF and the variance of the MTBF.
            MTBF = tr[0]
            A = []
            for i in range(n_failures - 1):
                MTBF += S[i] * (tr[i + 1] - tr[i])
                A.append(S[i] * (tr[i + 1] - tr[i]))

            for i in range(len(A)):
                try:
                    A[i] = sum(A[i:])**2 / \
                        ((n_points - r[i]) * (n_points - r[i] + 1))
                except ZeroDivisionError:
                    A[i] = A[i - 1]
                except IndexError:
                    A[i] = 0.0

            try:
                var_mu = (n_failures / (n_failures - 1)) * sum(A)
            except ZeroDivisionError:
                var_mu = 0.0

            MTBFLL = MTBF - sqrt(var_mu) * _z_norm_
            MTBFUL = MTBF + sqrt(var_mu) * _z_norm_

# Load the table with the Kaplan-Meier results.
            model = self.tvwNonParResults.get_model()
            model.clear()
            for i in range(len(times)):
                _data_ = [str(nonpar[1][i]), int(nonpar[2][i]),
                          int(nonpar[3][i]), float(nonpar[5][i]),
                          float(nonpar[7][i]), float(nonpar[5][i]),
                          float(nonpar[8][i]), float(nonpar[9][i])]
                model.append(_data_)

            column = self.tvwNonParResults.get_column(1)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>Number at\nRisk</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(2)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>Number\nFailing</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(3)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>p</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(4)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>se S(t)</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(5)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>S(t)</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(6)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>S(t) Lower\nBound</span>"))
            column.set_widget(label)

            column = self.tvwNonParResults.get_column(7)
            label = column.get_widget()
            label.set_markup(_(u"<span weight='bold'>S(t) Upper\nBound</span>"))
            column.set_widget(label)

# Plot the survival curve with confidence bounds.
            self._load_plot(self.axAxis1, self.pltPlot1,
                            x=times, y1=Shat,
                            y2=Shatll, y3=Shatul,
                            _title_=_(u"Kaplan-Meier Plot of %s") % _name,
                            _xlab_=_(u"Time"),
                            _ylab_=_(u"Survival Function [S(t)] "),
                            _marker_=['g-', 'r-', 'b-'])

# Create the legend.
            leg = self.axAxis1.legend((u"Survival Function [S(t)]",
                                       u"Lower CB", u"Upper CB"),
                                      'upper right',
                                      shadow=True)
            for t in leg.get_texts():
                t.set_fontsize('small')
            for l in leg.get_lines():
                l.set_linewidth(0.5)

# Plot the hazard rate curve with confidence bounds.
            self._load_plot(self.axAxis3, self.pltPlot3,
                            x=times[1:], y1=_h_[1:],
                            y2=_hll_[1:], y3=_hul_[1:],
                            _title_=_(u"Hazard Rate Plot of %s") % _name,
                            _xlab_=_(u"Time"),
                            _ylab_=_(u"Hazard Rate [h(t)] "),
                            _marker_=['g-', 'r-', 'b-'])

# Create the legend.
            leg = self.axAxis3.legend((u"Hazard Rate [h(t)]",
                                       u"Lower CB", u"Upper CB"),
                                      'upper right',
                                      shadow=True)
            for t in leg.get_texts():
                t.set_fontsize('small')
            for l in leg.get_lines():
                l.set_linewidth(0.5)

            for plot in self.vbxPlot1.get_children():
                self.vbxPlot1.remove(plot)

            self.vbxPlot1.pack_start(self.pltPlot1)
            self.vbxPlot1.pack_start(self.pltPlot3)

# Plot the cumulative hazard curve with confidence bounds.
            self._load_plot(self.axAxis2, self.pltPlot2,
                            x=times, y1=_H_,
                            y2=_Hll_, y3=_Hul_,
                            _title_=_("Cumulative Hazard Plot of %s") % _name,
                            _xlab_=_("Time"),
                            _ylab_=_("Cumulative Hazard Function [H(t)] "),
                            _marker_=['g-', 'r-', 'b-'])

# Create the legend.
            leg = self.axAxis2.legend(('Cum. Hazard Function [H(t)]',
                                       'Lower CB', 'Upper CB'), 'upper left',
                                       shadow=True)
            for t in leg.get_texts():
                t.set_fontsize('small')
            for l in leg.get_lines():
                l.set_linewidth(0.5)

# Plot the log cumulative hazard curve with confidence bounds.
            self._load_plot(self.axAxis4, self.pltPlot4,
                            x=logtimes, y1=logH[:len(logtimes)],
                            y2=logHll, y3=logHul,
                            _title_=_("Log Cum. Hazard Plot of %s") % _name,
                            _xlab_=_("log(Time)"),
                            _ylab_=_("Log Cum. Hazard Function [log H(t)] "),
                            _marker_=['g-', 'r-', 'b-'])

# Create the legend.
            leg = self.axAxis4.legend(('Log Cum. Hazard Function [log H(t)]',
                                       'Lower CB', 'Upper CB'), 'upper left',
                                       shadow=True)
            for t in leg.get_texts():
                t.set_fontsize('small')
            for l in leg.get_lines():
                l.set_linewidth(0.5)

            for plot in self.vbxPlot2.get_children():
                self.vbxPlot2.remove(plot)

            self.vbxPlot2.pack_start(self.pltPlot2)
            self.vbxPlot2.pack_start(self.pltPlot4)

# =========================================================================== #
# Fit the data to an exponential distribution and estimate it's parameters.
# =========================================================================== #
        elif(_analysis_ == 3):
            fit = _calc.parametric_fit(results, _starttime_, _reltime_,
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
            _theop_ = _calc.theoretical_distribution(censdata, 'exp', para)

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
        elif(_analysis_ == 4):
            fit = _calc.parametric_fit(results, _starttime_, _reltime_,
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
            _theop_ = _calc.theoretical_distribution(censdata, 'lnorm', para)

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
        elif(_analysis_ == 5):
            fit = _calc.parametric_fit(results, _starttime_, _reltime_,
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
            _theop_ = _calc.theoretical_distribution(censdata, 'norm', para)

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
        elif(_analysis_ == 6):
            fit = _calc.parametric_fit(results, _starttime_, _reltime_,
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
            _theop_ = _calc.theoretical_distribution(censdata, 'weibull', para)

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

        #elif(_analysis_ == 7):              # Fit to a WeiBayes.

# =========================================================================== #
# Create and display parametric plots.
# =========================================================================== #
        if(_analysis_ > 2):
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

        self.txtMHBPValue.set_text(str(fmt.format(p_value[0])))
        self.txtZLPPValue.set_text(str(fmt.format(p_value[1])))
        self.txtZLRPValue.set_text(str(fmt.format(p_value[2])))

        self.lblMHBResult.set_markup(_text[0])
        self.lblZLPResult.set_markup(_text[1])
        self.lblZLRResult.set_markup(_text[2])

        return False

    def dataset_save(self, button):
        """
        Saves the DATASET Object gtk.TreeView information to the Program's
        MySQL or SQLite3 database.

        Keyword Arguments:
        button -- the gtk.Button widget that called this function.
        """

        self.model.foreach(self._save_line_item)

        return False

    def _save_survival_record(self, model, path, row):
        """
        Saves each of the survival data records that comprise the selected
        DATASET to the RTK Program MySQL or SQLite3 database.

        Keyword Arguments:
        model -- the DATASET tvwDataset gtk.ListStore.
        path_ -- the path of the active row in the DATASET gtk.ListStore.
        row   -- the selected row in the DATASET gtk.TreeView.
        """

        values = (model.get_value(row, 1), model.get_value(row, 2),
                  model.get_value(row, 3), model.get_value(row, 4),
                  model.get_value(row, 0))

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_survival_data \
                     SET fld_unit='%s', fld_left_interval=%f, \
                         fld_right_interval=%f, fld_status=%d \
                     WHERE fld_record_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_survival_data \
                     SET fld_unit=?, fld_left_interval=?, \
                         fld_right_interval=?, fld_status=? \
                     WHERE fld_record_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

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
                  self.model.get_value(self.selected_row, 34), \
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
                         fld_lr=%f, fld_aic=%f, fld_bic=%f, fld_mle=%f, \
                         fld_start_time=%d \
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
                         fld_lr=?, fld_aic=?, fld_bic=?, fld_mle=?, \
                         fld_start_time=? \
                     WHERE fld_dataset_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("dataset.py: Failed to save dataset.")
            return True

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
            if(_text_ == 1 or _text_ == 2): # MCF or Kaplan-Meier
                self.lblFitMethod.hide()
                self.lblConfMethod.hide()
                self.cmbFitMethod.hide()
                self.cmbConfMethod.hide()
            else:
                self.lblFitMethod.show()
                self.lblConfMethod.show()
                self.cmbFitMethod.show()
                self.cmbConfMethod.show()

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
        bg_color = _conf.RELIAFREE_COLORS[12]
        fg_color = _conf.RELIAFREE_COLORS[13]
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
            #self._load_component_list()

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxDataset)
        self._app.winWorkBook.show_all()

        _title = _(u"RTK Work Bench: Program Survival Analyses (%d Datasets)") % \
                   self.n_datasets
        self._app.winWorkBook.set_title(_title)

        self.notebook.set_current_page(0)

        return False
