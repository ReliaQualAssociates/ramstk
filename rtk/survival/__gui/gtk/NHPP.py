#!/usr/bin/env python
"""
############################################################################
Survival Package Non-Homogoneous Poisson Process Distribution Work Book View
############################################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.survival.gui.gtk.NHPP.py is part of The RTK Project
#
# All rights reserved.

import sys

# Import modules for localization support.
import gettext
import locale

# Import modules for mathematics.
import numpy as np
from scipy.interpolate import interp1d

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
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
if 'linux' in sys.platform:
    import pkg_resources
    pkg_resources.require('matplotlib==1.4.3')

# Import other RTK modules.
try:
    import Configuration
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.gui.gtk.Widgets as Widgets

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext

matplotlib.use('GTK')


class Results(gtk.HPaned):
    """
    The Work Book page to display all the attributes for a Non-Homogoneous
    Poisson Process .  The attributes of a NHPP Results page are:

    :ivar _model: the Survival :py:class:`rtk.survival.Survival.Model`
                  whose attributes are being displayed.
    :ivar gtk.TreeView tvwResults:
    :ivar gtk.Entry txtNumFailures: the gtk.Entry() to display
    :ivar gtk.Entry txtNumSuspensions: the gtk.Entry() to display
    :ivar gtk.Entry txtMTBFLL: the gtk.Entry() to display
    :ivar gtk.Entry txtMTBF: the gtk.Entry() to display
    :ivar gtk.Entry txtMTBFUL: the gtk.Entry() to display
    :ivar gtk.Entry txtFailureIntensityLL: the gtk.Entry() to display
    :ivar gtk.Entry txtFailureIntensity: the gtk.Entry() to display
    :ivar gtk.Entry txtFailureIntensityUL: the gtk.Entry() to display
    :ivar gtk.Entry txtMTBFiLL: the gtk.Entry() to display
    :ivar gtk.Entry txtMTBFi: the gtk.Entry() to display
    :ivar gtk.Entry txtMTBFiUL: the gtk.Entry() to display
    :ivar gtk.Entry txtFailureIntensityiLL: the gtk.Entry() to display
    :ivar gtk.Entry txtFailureIntensityi: the gtk.Entry() to display
    :ivar gtk.Entry txtFailureIntensityiUL: the gtk.Entry() to display
    :ivar gtk.Entry txtScaleLL: the gtk.Entry() to display
    :ivar gtk.Entry txtScale: the gtk.Entry() to display
    :ivar gtk.Entry txtScaleUL: the gtk.Entry() to display
    :ivar gtk.Entry txtShapeLL: the gtk.Entry() to display
    :ivar gtk.Entry txtShape: the gtk.Entry() to display
    :ivar gtk.Entry txtShapeUL: the gtk.Entry() to display
    """

    def __init__(self):
        """
        Method to initialize the Results page for the NHPP.
        """

        gtk.HPaned.__init__(self)

        # Initialize private dict attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._model = None

        # Initialize public dict attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.lblPage = gtk.Label()
        self.lblModel = Widgets.make_label("", width=-1)
        self.lblModeli = Widgets.make_label("", width=-1)
        self.lblTrend = Widgets.make_label("", width=-1)
        self.lblGoF = Widgets.make_label("", width=-1)

        self.txtNumFailures = Widgets.make_entry(width=50, editable=False)
        self.txtNumSuspensions = Widgets.make_entry(width=50, editable=False)

        self.txtMTBFLL = Widgets.make_entry(width=100, editable=False)
        self.txtMTBF = Widgets.make_entry(width=100, editable=False)
        self.txtMTBFUL = Widgets.make_entry(width=100, editable=False)
        self.txtFailureIntensityLL = Widgets.make_entry(width=100,
                                                        editable=False)
        self.txtFailureIntensity = Widgets.make_entry(width=100,
                                                      editable=False)
        self.txtFailureIntensityUL = Widgets.make_entry(width=100,
                                                        editable=False)

        self.txtMTBFiLL = Widgets.make_entry(width=100, editable=False)
        self.txtMTBFi = Widgets.make_entry(width=100, editable=False)
        self.txtMTBFiUL = Widgets.make_entry(width=100, editable=False)
        self.txtFailureIntensityiLL = Widgets.make_entry(width=100,
                                                         editable=False)
        self.txtFailureIntensityi = Widgets.make_entry(width=100,
                                                       editable=False)
        self.txtFailureIntensityiUL = Widgets.make_entry(width=100,
                                                         editable=False)

        self.txtScaleLL = Widgets.make_entry(width=100, editable=False)
        self.txtScale = Widgets.make_entry(width=100, editable=False)
        self.txtScaleUL = Widgets.make_entry(width=100, editable=False)

        self.txtShapeLL = Widgets.make_entry(width=100, editable=False)
        self.txtShape = Widgets.make_entry(width=100, editable=False)
        self.txtShapeUL = Widgets.make_entry(width=100, editable=False)

        self.txtTrendModel = Widgets.make_entry(width=100, editable=False)
        self.txtTrendCV = Widgets.make_entry(width=100, editable=False)
        self.txtGoFCV = Widgets.make_entry(width=100, editable=False)
        self.txtGoFModel = Widgets.make_entry(width=100, editable=False)

        # Right quadrant widgets.
        self.tvwResults = gtk.TreeView()

        # Set gtk.Widget() tooltip text.
        self.txtNumFailures.set_tooltip_markup(_(u"Displays the number of "
                                                 u"failures in the dataset."))
        self.txtNumSuspensions.set_tooltip_markup(_(u"Displays the number of "
                                                    u"suspensions in the "
                                                    u"dataset."))
        self.txtMTBFLL.set_tooltip_markup(_(u"Displays the lower "
                                            u"<span>\u03B1</span>% confidence "
                                            u"bound on the cumulative MTBF "
                                            u"estimated from the dataset."))
        self.txtMTBF.set_tooltip_markup(_(u"Displays the point estimate of "
                                          u"the cumulative MTBF estimated "
                                          u"from the dataset."))
        self.txtMTBFUL.set_tooltip_markup(_(u"Displays the upper "
                                            u"<span>\u03B1</span>% confidence "
                                            u"bound on the cumulative MTBF "
                                            u"estimated from the dataset."))
        self.txtMTBFiLL.set_tooltip_markup(_(u"Displays the lower "
                                             u"<span>\u03B1</span>% "
                                             u"confidence bound on the "
                                             u"instantaneous MTBF estimated "
                                             u"from the dataset."))
        self.txtMTBFi.set_tooltip_markup(_(u"Displays the point estimate of "
                                           u"the instantaneous MTBF estimated "
                                           u"from the dataset."))
        self.txtMTBFiUL.set_tooltip_markup(_(u"Displays the upper "
                                             u"<span>\u03B1</span>% "
                                             u"confidence bound on the "
                                             u"instantaneous MTBF estimated "
                                             u"from the dataset."))
        self.txtFailureIntensityLL.set_tooltip_markup(_(u"Displays the lower "
                                                        u"<span>\u03B1</span>% "
                                                        u"confidence bound on "
                                                        u"the cumulative "
                                                        u"failure intensity "
                                                        u"estimated from the "
                                                        u"dataset."))
        self.txtFailureIntensity.set_tooltip_markup(_(u"Displays the point "
                                                      u"estimate of the "
                                                      u"cumulative failure "
                                                      u"intensity estimated "
                                                      u"from the "
                                                      u"dataset."))
        self.txtFailureIntensityUL.set_tooltip_markup(_(u"Displays the upper "
                                                        u"<span>\u03B1</span>% "
                                                        u"confidence bound on "
                                                        u"the cumulative "
                                                        u"failure intensity "
                                                        u"estimated from the "
                                                        u"dataset."))
        self.txtFailureIntensityiLL.set_tooltip_markup(_(u"Displays the lower "
                                                         u"<span>\u03B1</span>% "
                                                         u"confidence bound "
                                                         u"on the "
                                                         u"instantaneous "
                                                         u"failure intensity "
                                                         u"estimated from the "
                                                         u"dataset."))
        self.txtFailureIntensityi.set_tooltip_markup(_(u"Displays the point "
                                                       u"estimate of the "
                                                       u"instantaneous "
                                                       u"failure intensity "
                                                       u"estimated from the "
                                                       u"dataset."))
        self.txtFailureIntensityiUL.set_tooltip_markup(_(u"Displays the upper "
                                                         u"<span>\u03B1</span>% "
                                                         u"confidence bound "
                                                         u"on the "
                                                         u"instantaneous "
                                                         u"failure intensity "
                                                         u"estimated from the "
                                                         u"dataset."))
        self.txtScaleLL.set_tooltip_markup(_(u"Displays the lower "
                                             u"<span>\u03B1</span>% "
                                             u"confidence bound on the "
                                             u"scale parameter estimated from "
                                             u"the dataset."))
        self.txtScale.set_tooltip_markup(_(u"Displays the point estimate of "
                                           u"the scale parameter estimated "
                                           u"from the dataset."))
        self.txtScaleUL.set_tooltip_markup(_(u"Displays the upper "
                                             u"<span>\u03B1</span>% "
                                             u"confidence bound on the "
                                             u"scale parameter estimated from "
                                             u"the dataset."))
        self.txtShapeLL.set_tooltip_markup(_(u"Displays the lower "
                                             u"<span>\u03B1</span>% "
                                             u"confidence bound on the "
                                             u"shape parameter estimated from "
                                             u"the dataset."))
        self.txtShape.set_tooltip_markup(_(u"Displays the point estimate of "
                                           u"the shape parameter estimated "
                                           u"from the dataset."))
        self.txtShapeUL.set_tooltip_markup(_(u"Displays the upper "
                                             u"<span>\u03B1</span>% "
                                             u"confidence bound on the "
                                             u"shape parameter estimated from "
                                             u"the dataset."))
        self.txtTrendCV.set_tooltip_text(_(u"Displays the critical value for "
                                           u"testing the hypothesis of "
                                           u"exponentially distributed "
                                           u"failure times."))
        self.txtTrendModel.set_tooltip_text(_(u"Displays the test statistic "
                                              u"for assessing exponentially "
                                              u"distributed failure times. "
                                              u"If this value is greater than "
                                              u"the critical value, the data "
                                              u"suggests failure times are "
                                              u"exponentially distributed."))
        self.txtGoFCV.set_tooltip_text(_(u"Displays the critical value for "
                                         u"testing the hypothesis of a good "
                                         u"fit to the selected growth model."))
        self.txtGoFModel.set_tooltip_text(_(u"Displays the goodness of fit "
                                            u"test statistic for assessing "
                                            u"fit to the selected growth "
                                            u"model.  If this value is less "
                                            u"than the critical value, the "
                                            u"model is a good fit to the "
                                            u"data."))

    def create_results_page(self):
        """
        Method to create the page for displaying numerical results of the
        analysis for the Non-Homogoneous Poisson Process distribution.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _frame = Widgets.make_frame(label=_(u"Summary of Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        _fixed = gtk.Fixed()
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)
        _frame.add(_scrollwindow)

        self.pack1(_frame, resize=True, shrink=False)

        _frame = Widgets.make_frame(label=_(u"Non-Homogoneous Poisson Process "
                                            u"Table"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwResults)
        _frame.add(_scrollwindow)

        self.pack2(_frame, resize=True, shrink=True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display analysis results.           #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _labels = [_(u"Number of Failures:"), _(u"Number of Suspensions:")]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5)
        _x_pos += 35

        _fixed.put(self.txtNumFailures, _x_pos, _y_pos[0])
        _fixed.put(self.txtNumSuspensions, _x_pos, _y_pos[1])

        _label = Widgets.make_label(_(u"LCL"), height=-1, width=100,
                                    justify=gtk.JUSTIFY_CENTER)
        _fixed.put(_label, _x_pos + 50, _y_pos[1] + 35)
        _label = Widgets.make_label(_(u"Point\nEstimate"), height=-1,
                                    width=100, justify=gtk.JUSTIFY_CENTER)
        _fixed.put(_label, _x_pos + 150, _y_pos[1] + 35)
        _label = Widgets.make_label(_(u"UCL"), height=-1, width=100,
                                    justify=gtk.JUSTIFY_CENTER)
        _fixed.put(_label, _x_pos + 265, _y_pos[1] + 35)

        _labels = [_(u"Cumulative MTBF:"), _(u"Instantaneous MTBF:"),
                   _(u"Cumulative Failure Intensity:"),
                   _(u"Instantaneous Failure Intensity:"),
                   _(u"Scale Parameter (\u03BB):"),
                   _(u"Shape Parameter (\u03B2):")]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5,
                                               _y_pos[1] + 65)
        _x_pos += 45

        _fixed.put(self.txtMTBFLL, _x_pos, _y_pos[0])
        _fixed.put(self.txtMTBF, _x_pos + 105, _y_pos[0])
        _fixed.put(self.txtMTBFUL, _x_pos + 210, _y_pos[0])
        _fixed.put(self.lblModel, _x_pos + 315, _y_pos[0])
        _fixed.put(self.txtMTBFiLL, _x_pos, _y_pos[1])
        _fixed.put(self.txtMTBFi, _x_pos + 105, _y_pos[1])
        _fixed.put(self.txtMTBFiUL, _x_pos + 210, _y_pos[1])
        _fixed.put(self.lblModeli, _x_pos + 315, _y_pos[1])
        _fixed.put(self.txtFailureIntensityLL, _x_pos, _y_pos[2])
        _fixed.put(self.txtFailureIntensity, _x_pos + 105, _y_pos[2])
        _fixed.put(self.txtFailureIntensityUL, _x_pos + 210, _y_pos[2])
        _fixed.put(self.txtFailureIntensityiLL, _x_pos, _y_pos[3])
        _fixed.put(self.txtFailureIntensityi, _x_pos + 105, _y_pos[3])
        _fixed.put(self.txtFailureIntensityiUL, _x_pos + 210, _y_pos[3])
        _fixed.put(self.txtScaleLL, _x_pos, _y_pos[4])
        _fixed.put(self.txtScale, _x_pos + 105, _y_pos[4])
        _fixed.put(self.txtScaleUL, _x_pos + 210, _y_pos[4])
        _fixed.put(self.txtShapeLL, _x_pos, _y_pos[5])
        _fixed.put(self.txtShape, _x_pos + 105, _y_pos[5])
        _fixed.put(self.txtShapeUL, _x_pos + 210, _y_pos[5])

        _label = Widgets.make_label(_(u"<u>Statistical Test for Trend</u>"))
        _fixed.put(_label, 5, _y_pos[5] + 40)
        self.lblTrend.set_markup(_(u"H<sub>o</sub>: Exponential Failure "
                                   u"Times"))
        _fixed.put(self.lblTrend, 5, _y_pos[5] + 75)
        _label = Widgets.make_label(_(u"Critical Value:"))
        _fixed.put(_label, 5, _y_pos[5] + 110)
        _fixed.put(self.txtTrendCV, _x_pos, _y_pos[5] + 110)
        _label = Widgets.make_label(_(u"Test Statistic:"))
        _fixed.put(_label, 5, _y_pos[5] + 140)
        _fixed.put(self.txtTrendModel, _x_pos, _y_pos[5] + 140)

        _label = Widgets.make_label(_(u"<u>Statistical Test for Goodness of "
                                      u"Fit</u>"), width=-1)
        _fixed.put(_label, _x_pos + 205, _y_pos[5] + 40)
        self.lblGoF.set_markup(_(u"H<sub>o</sub>: Data Follows NHPP Model"))
        _fixed.put(self.lblGoF, _x_pos + 205, _y_pos[5] + 75)
        _fixed.put(self.txtGoFCV, _x_pos + 205, _y_pos[5] + 110)
        _fixed.put(self.txtGoFModel, _x_pos + 205, _y_pos[5] + 140)

        # Place the reliability table.
        _model = gtk.ListStore(gobject.TYPE_FLOAT, gobject.TYPE_INT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
        self.tvwResults.set_model(_model)
        _headings = [_(u"Time"), _(u"Cumulative\nFailures"),
                     _(u"Scale Parameter\nLower Bound"), _(u"Scale Parameter"),
                     _(u"Scale Parameter\nUpper Bound"),
                     _(u"Shape Parameter\nLower Bound"), _(u"Shape Parameter"),
                     _(u"Shape Parameter\nUpper Bound"),
                     _(u"Cumulative MTBF\nLower Bound"),
                     _(u"Cumulative\nMTBF"),
                     _(u"Cumulative\nMTBF\nUpper Bound"),
                     _(u"Instantaneous MTBF\nLower Bound"),
                     _(u"Instantaneous\nMTBF"),
                     _(u"Instantaneous\nMTBF\nUpper Bound")]
        for _index, _heading in enumerate(_headings):
            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _column = gtk.TreeViewColumn()
            _label = Widgets.make_column_heading(_heading)
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=_index)
            _column.set_clickable(True)
            _column.set_resizable(True)
            _column.set_sort_column_id(_index)
            self.tvwResults.append_column(_column)

        # Insert the tab.
        self.lblPage.set_markup("<span weight='bold'>" +
                                _(u"NHPP\nResults") + "</span>")
        self.lblPage.set_alignment(xalign=0.5, yalign=0.5)
        self.lblPage.set_justify(gtk.JUSTIFY_CENTER)
        self.lblPage.show_all()
        self.lblPage.set_tooltip_text(_(u"Displays Non-Homogoneous Poisson "
                                        u"Process analysis results for the "
                                        u"selected dataset."))

        return False

    def load_results_page(self, model):
        """
        Method to load the gtk.Widgets() necessary for displaying the results
        of fitting a dataset to the Non-Homogoneous Poisson Process
        distribution.

        :param model: the :py:class:`rtk.survival.Survival` data model to
                      display the results for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'

        self._model = model

        # Load the summary information.
        self.txtNumFailures.set_text(str(self._model.n_failures))
        self.txtNumSuspensions.set_text(str(self._model.n_suspensions))

        try:
            self.txtMTBFLL.set_text(
                str(fmt.format(self._model.nhpp[-1][4][0])))
            self.txtMTBF.set_text(str(fmt.format(self._model.nhpp[-1][4][1])))
            self.txtMTBFUL.set_text(
                str(fmt.format(self._model.nhpp[-1][4][2])))
            self.txtFailureIntensityLL.set_text(
                str(fmt.format(1.0 / self._model.nhpp[-1][4][2])))
            self.txtFailureIntensity.set_text(
                str(fmt.format(1.0 / self._model.nhpp[-1][4][1])))
            self.txtFailureIntensityUL.set_text(
                str(fmt.format(1.0 / self._model.nhpp[-1][4][0])))
            self.txtMTBFiLL.set_text(
                str(fmt.format(self._model.nhpp[-1][5][0])))
            self.txtMTBFi.set_text(str(fmt.format(self._model.nhpp[-1][5][1])))
            self.txtMTBFiUL.set_text(
                str(fmt.format(self._model.nhpp[-1][5][2])))
            self.txtFailureIntensityiLL.set_text(
                str(fmt.format(1.0 / self._model.nhpp[-1][5][2])))
            self.txtFailureIntensityi.set_text(
                str(fmt.format(1.0 / self._model.nhpp[-1][5][1])))
            self.txtFailureIntensityiUL.set_text(
                str(fmt.format(1.0 / self._model.nhpp[-1][5][0])))
        except IndexError:
            self.txtMTBFLL.set_text("0.0")
            self.txtMTBF.set_text("0.0")
            self.txtMTBFUL.set_text("0.0")
            self.txtFailureIntensityLL.set_text("0.0")
            self.txtFailureIntensity.set_text("0.0")
            self.txtFailureIntensityUL.set_text("0.0")
            self.txtMTBFiLL.set_text("0.0")
            self.txtMTBFi.set_text("0.0")
            self.txtMTBFiUL.set_text("0.0")
            self.txtFailureIntensityiLL.set_text("0.0")
            self.txtFailureIntensityi.set_text("0.0")
            self.txtFailureIntensityiUL.set_text("0.0")

        self.txtScaleLL.set_text(str(fmt.format(self._model.scale[0])))
        self.txtScale.set_text(str(fmt.format(self._model.scale[1])))
        self.txtScaleUL.set_text(str(fmt.format(self._model.scale[2])))
        self.txtShapeLL.set_text(str(fmt.format(self._model.shape[0])))
        self.txtShape.set_text(str(fmt.format(self._model.shape[1])))
        self.txtShapeUL.set_text(str(fmt.format(self._model.shape[2])))

        self.txtTrendCV.set_text(
            str(fmt.format(self._model.chi2_critical_value[1])))
        self.txtTrendModel.set_text(str(fmt.format(self._model.chi_square)))
        if(self._model.chi_square >
           self._model.chi2_critical_value[1]):
            self.lblTrend.set_markup(_(u"H<sub>o</sub>: Exponential Failure "
                                       u"Times     "
                                       u"<span foreground='green'>"
                                       u"Reject</span>"))
        else:
            self.lblTrend.set_markup(_(u"H<sub>o</sub>: Exponential Failure "
                                       u"Times     "
                                       u"<span foreground='red'>"
                                       u"Fail to Reject</span>"))

        self.txtGoFCV.set_text(str(fmt.format(self._model.cvm_critical_value)))
        self.txtGoFModel.set_text(str(fmt.format(self._model.cramer_vonmises)))
        if(self._model.cramer_vonmises <
           self._model.cvm_critical_value):
            self.lblGoF.set_markup(_(u"H<sub>o</sub>: Data Follows NHPP Model "
                                     u"    <span foreground='green'>Fail to "
                                     u"Reject</span>"))
        else:
            self.lblGoF.set_markup(_(u"H<sub>o</sub>: Data Follows NHPP Model "
                                     u"    <span foreground='red'>"
                                     u"Reject</span>"))

        self.lblModel.set_markup(_(u"<span>MTBF<sub>C</sub> = "
                                   u"{0:0.4f} T<sup>{1:0.4f}</sup>"
                                   u"</span>").format(
                                       1.0 / self._model.scale[1],
                                       1.0 - self._model.shape[1]))

        _beta = self._model.shape[1] - 1.0
        self.lblModeli.set_markup(_(u"<span>MTBF<sub>i</sub> = "
                                    u"1.0 / ({0:0.4f})({1:0.4f})"
                                    u"T<sup>{2:0.4f}"
                                    u"</sup></span>").format(
                                        self._model.scale[1],
                                        self._model.shape[1],
                                        _beta))

        # Load the non-parametric results table.
        self._load_nonparametric_table()

        return False

    def _load_nonparametric_table(self):
        """
        Method to load the non-parametric table with results.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Retrieve and clear the non-parametric results gtk.TreeModel().
        _model = self.tvwResults.get_model()
        _model.clear()

        # Load the non-parametric results gtk.TreeModel().
        for i in range(len(self._model.nhpp)):
            _record = [self._model.nhpp[i][0], self._model.nhpp[i][1],
                       self._model.nhpp[i][2][0], self._model.nhpp[i][2][1],
                       self._model.nhpp[i][2][2], self._model.nhpp[i][3][0],
                       self._model.nhpp[i][3][1], self._model.nhpp[i][3][2],
                       self._model.nhpp[i][4][0], self._model.nhpp[i][4][1],
                       self._model.nhpp[i][4][2], self._model.nhpp[i][5][0],
                       self._model.nhpp[i][5][1], self._model.nhpp[i][5][2]]
            _model.append(_record)

        return False


class Plots(gtk.HBox):
    """
    The Work Book page to display plots for an Non-Homogoneous Poisson Process
    distribution.  The attributes of an Non-Homogoneous Poisson Process Plot
    page are:

    :ivar _model: the :py:class:`rtk.survival.Survival` data model whose
                  results are being displayed.
    :ivar matplotlib.backends.backend_gtkagg.FigureCanvasGTK pltPlot1: the plot
        in the upper left corner.
    :ivar matplotlib.axes.Axes axAxis1: the Axes in the upper left corner plot.
    :ivar matplotlib.backends.backend_gtkagg.FigureCanvasGTK pltPlot2: the plot
        in the lower left corner.
    :ivar matplotlib.axes.Axes axAxis2: the Axes in the lower left corner plot.
    :ivar matplotlib.backends.backend_gtkagg.FigureCanvasGTK pltPlot3: the plot
        in the upper right corner.
    :ivar matplotlib.axes.Axes axAxis3: the Axes in the upper right corner
        plot.
    :ivar matplotlib.backends.backend_gtkagg.FigureCanvasGTK pltPlot4: the plot
        in the lower right corner.
    :ivar matplotlib.axes.Axes axAxis4: the Axes in the lower right corner
        plot.
    """

    def __init__(self):
        """
        Method to initialize the Plot page for the Non-Homogoneous Poisson
        Process distribution.
        """

        gtk.HBox.__init__(self)

        # Initialize private dict attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._model = None

        # Initialize public dict attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.lblPage = gtk.Label()
        _height = 100
        _width = 200
        _figure = Figure(figsize=(_width, _height))
        self.pltPlot1 = FigureCanvas(_figure)
        self.axAxis1 = _figure.add_subplot(111)
        _figure = Figure(figsize=(_width, _height))
        self.pltPlot2 = FigureCanvas(_figure)
        self.axAxis2 = _figure.add_subplot(111)
        _figure = Figure(figsize=(_width, _height))
        self.pltPlot3 = FigureCanvas(_figure)
        self.axAxis3 = _figure.add_subplot(111)
        _figure = Figure(figsize=(_width, _height))
        self.pltPlot4 = FigureCanvas(_figure)
        self.axAxis4 = _figure.add_subplot(111)

        # Connect gtk.Widget() signals to callback functions.
        self.pltPlot1.mpl_connect('button_press_event', Widgets.expand_plot)
        self.pltPlot2.mpl_connect('button_press_event', Widgets.expand_plot)
        self.pltPlot3.mpl_connect('button_press_event', Widgets.expand_plot)
        self.pltPlot4.mpl_connect('button_press_event', Widgets.expand_plot)

    def create_plot_page(self):
        """
        Method to create the page for displaying plots for the Non-Homogoneous
        Poisson Process distribution.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _vbox = gtk.VBox()
        self.pack_start(_vbox, True, True)

        _frame = Widgets.make_frame(_(u"Cumulative MTBF Over Operating Time"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot1)
        _vbox.pack_start(_frame, True, True)

        _frame = Widgets.make_frame(_(u"Cumulative MTBF Over Calendar Time"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot2)
        _vbox.pack_end(_frame, True, True)

        _vbox = gtk.VBox()
        self.pack_end(_vbox, True, True)

        _frame = Widgets.make_frame(_(u"Instantaneous MTBF Over Operating "
                                      u"Time"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot3)
        _vbox.pack_start(_frame, True, True)

        _frame = Widgets.make_frame(_(u"Instantaneous MTBF Over Calendar "
                                      u"Time"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot4)
        _vbox.pack_end(_frame, True, True)

        # Insert the page.
        self.lblPage.set_markup("<span weight='bold'>Analysis\nPlots</span>")
        self.lblPage.set_alignment(xalign=0.5, yalign=0.5)
        self.lblPage.set_justify(gtk.JUSTIFY_CENTER)
        self.lblPage.show_all()
        self.lblPage.set_tooltip_text(_(u"Displays survival analyses plots."))

        return False

    def load_plots(self, model):
        """
        Method to load the plots for the Non-Homogoneous Poisson Process
        distribution.

        :param model: the :py:class:`rtk.survival.Survival` data model to
                      display the plots for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._model = model

        self._load_cumulative_mtbf_plot()
        self._load_cum_mtbf_calendar_plot()
        self._load_instantaneous_mtbf_plot()
        self._load_inst_mtbf_calendar_plot()

        return False

    def _load_cumulative_mtbf_plot(self):
        """
        Method to load plot 1 with the cumulative MTBF versus cumulative time.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.axAxis1.cla()

        if self._model.nhpp != []:
            _times = [x[0] for x in self._model.nhpp]
            _mtbfll = [x[4][0] for x in self._model.nhpp]
            _mtbf = [x[4][1] for x in self._model.nhpp]
            _mtbful = [x[4][2] for x in self._model.nhpp]

            _plot_title = _(u"NHPP - Power Law Plot Cumulative MTBF Over "
                            u"Cumulative Operating Time")
            Widgets.load_plot(self.axAxis1, self.pltPlot1,
                              _times, y1=_mtbf, title=_plot_title,
                              xlab=_(u"Cumulative Operating Time [t]"),
                              ylab=_(u"Cumulative MTBF [MTBF(t)] "), ltype=[2],
                              marker=['go'])

            _x_sm = np.array(_times)
            _x_smooth = np.linspace(_x_sm.min(), _x_sm.max(), 10 * len(_times))

            _smooth = interp1d(_times, _mtbfll)
            _y_smooth = _smooth(_x_smooth)
            _line = matplotlib.lines.Line2D(_x_smooth, _y_smooth, lw=1.5,
                                            color='r', ls='-.')
            self.axAxis1.add_line(_line)

            _smooth = interp1d(_times, _mtbful)
            _y_smooth = _smooth(_x_smooth)
            _line = matplotlib.lines.Line2D(_x_smooth, _y_smooth, lw=1.5,
                                            color='b', ls='-.')
            self.axAxis1.add_line(_line)

            _text = (_(u"Cumulative MTBF"), _(u"Cum. MTBF LCL"),
                     _(u"Cum. MTBF UCL"))
            Widgets.create_legend(self.axAxis1, _text, fontsize='medium',
                                  legframeon=True, location='upper right',
                                  legshadow=True)

            self.axAxis1.set_xscale('log')
            self.axAxis1.set_yscale('log')

        return False

    def _load_cum_mtbf_calendar_plot(self):
        """
        Method to load plot 2 with the cumulative MTBF over calendar time.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.axAxis2.cla()

        if self._model.nhpp != []:
            _dates = [x[6] for x in self._model.nhpp]
            _mtbfll = [x[4][0] for x in self._model.nhpp]
            _mtbf = [x[4][1] for x in self._model.nhpp]
            _mtbful = [x[4][2] for x in self._model.nhpp]

            _plot_title = _(u"NHPP - Power Law Plot Cumulative MTBF Over "
                            u"Calendar Time")
            Widgets.load_plot(self.axAxis2, self.pltPlot2,
                              _dates, y1=_mtbf, title=_plot_title,
                              xlab=_(u"Calendar Time [t]"),
                              ylab=_(u"Cumulative MTBF [MTBF(t)] "), ltype=[4],
                              marker=['go'])

            _x_sm = np.array(_dates)
            _x_smooth = np.linspace(_x_sm.min(), _x_sm.max(), 10 * len(_dates))
            _x_smooth = np.array([int(x) for x in _x_smooth])

            _smooth = interp1d(_dates, _mtbfll)
            _y_smooth = _smooth(_x_smooth)
            _line = matplotlib.lines.Line2D(_x_smooth, _y_smooth, lw=1.5,
                                            color='r', ls='-.')
            self.axAxis2.add_line(_line)

            _smooth = interp1d(_dates, _mtbful)
            _y_smooth = _smooth(_x_smooth)
            _line = matplotlib.lines.Line2D(_x_smooth, _y_smooth, lw=1.5,
                                            color='b', ls='-.')
            self.axAxis2.add_line(_line)

            _text = (_(u"Cumulative MTBF"), _(u"Cum. MTBF LCL"),
                     _(u"Cum. MTBF UCL"))
            Widgets.create_legend(self.axAxis2, _text, fontsize='medium',
                                  legframeon=True, location='upper right',
                                  legshadow=True)

        return False

    def _load_instantaneous_mtbf_plot(self):
        """
        Method to load plot 3 with the instantaneous MTBF over operating time.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.axAxis3.cla()

        if self._model.nhpp != []:
            _times = [x[0] for x in self._model.nhpp]
            _mtbfll = [x[5][0] for x in self._model.nhpp]
            _mtbf = [x[5][1] for x in self._model.nhpp]
            _mtbful = [x[5][2] for x in self._model.nhpp]

            _plot_title = _(u"NHPP - Power Law Plot Instantaneous MTBF Over "
                            u"Cumulative Operating Time")
            Widgets.load_plot(self.axAxis3, self.pltPlot3,
                              _times, y1=_mtbf, title=_plot_title,
                              xlab=_(u"Cumulative Operating Time [t]"),
                              ylab=_(u"Instantaneous MTBF [m(t)] "), ltype=[2],
                              marker=['go'])

            _x_sm = np.array(_times)
            _x_smooth = np.linspace(_x_sm.min(), _x_sm.max(), 10 * len(_times))

            _smooth = interp1d(_times, _mtbfll)
            _y_smooth = _smooth(_x_smooth)
            _line = matplotlib.lines.Line2D(_x_smooth, _y_smooth, lw=1.5,
                                            color='r', ls='-.')
            self.axAxis3.add_line(_line)

            _smooth = interp1d(_times, _mtbful)
            _y_smooth = _smooth(_x_smooth)
            _line = matplotlib.lines.Line2D(_x_smooth, _y_smooth, lw=1.5,
                                            color='b', ls='-.')
            self.axAxis3.add_line(_line)

            _text = (_(u"Instantaneous MTBF"), _(u"Instantaneous MTBF LCL"),
                     _(u"Instantaneous MTBF UCL"))
            Widgets.create_legend(self.axAxis3, _text, fontsize='medium',
                                  legframeon=True, location='upper right',
                                  legshadow=True)

            self.axAxis3.set_xscale('log')
            self.axAxis3.set_yscale('log')

        return False

    def _load_inst_mtbf_calendar_plot(self):
        """
        Method to load plot 4 with the instantaneous MTBF over calendar time.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.axAxis4.cla()

        if self._model.nhpp != []:
            _dates = [x[6] for x in self._model.nhpp]
            _mtbfll = [x[5][0] for x in self._model.nhpp]
            _mtbf = [x[5][1] for x in self._model.nhpp]
            _mtbful = [x[5][2] for x in self._model.nhpp]

            _plot_title = _(u"NHPP - Power Law Plot Instantaneous MTBF Over "
                            u"Calendar Time")
            Widgets.load_plot(self.axAxis4, self.pltPlot4,
                              _dates, y1=_mtbf, title=_plot_title,
                              xlab=_(u"Calendar Time [t]"),
                              ylab=_(u"Instantaneous MTBF [m(t)] "), ltype=[4],
                              marker=['go'])

            _x_sm = np.array(_dates)
            _x_smooth = np.linspace(_x_sm.min(), _x_sm.max(), 10 * len(_dates))
            _x_smooth = np.array([int(x) for x in _x_smooth])

            _smooth = interp1d(_dates, _mtbfll)
            _y_smooth = _smooth(_x_smooth)
            _line = matplotlib.lines.Line2D(_x_smooth, _y_smooth, lw=1.5,
                                            color='r', ls='-.')
            self.axAxis4.add_line(_line)

            _smooth = interp1d(_dates, _mtbful)
            _y_smooth = _smooth(_x_smooth)
            _line = matplotlib.lines.Line2D(_x_smooth, _y_smooth, lw=1.5,
                                            color='b', ls='-.')
            self.axAxis4.add_line(_line)

            _text = (_(u"Instantaneous MTBF"), _(u"Instantaneous MTBF LCL"),
                     _(u"Instantaneous MTBF UCL"))
            Widgets.create_legend(self.axAxis4, _text, fontsize='medium',
                                  legframeon=True, location='upper right',
                                  legshadow=True)

        return False
