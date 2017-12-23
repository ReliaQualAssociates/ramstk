#!/usr/bin/env python
"""
###########################################################################
Survival Package Mean Cumulative Function (MCF) Distribution Work Book View
###########################################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.survival.gui.gtk.MCF.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys

# Import modules for localization support.
import gettext
import locale

# Import modules for mathematics support.
from math import fabs
import numpy as np
from scipy.stats import chi2, norm  # pylint: disable=E0611

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
    import Configuration as _conf
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.gui.gtk.Widgets as _widg

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext

matplotlib.use('GTK')


class Results(gtk.HPaned):
    """
    The Work Book page to display all the attributes for an MCF
    distribution.  The attributes of an MCF Results page are:

    :ivar _model: the :py:class:`rtk.survival.Survival.Model` whose attributes
                  are being displayed.
    :ivar gtk.Label lblMHBResult:
    :ivar gtk.Label lblZLPResult:
    :ivar gtk.Label lblZLRResult:
    :ivar gtk.Label lblRhoResult:
    :ivar gtk.TreeView tvwResults:
    :ivar gtk.Entry txtNumFailures:
    :ivar gtk.Entry txtMHB:
    :ivar gtk.Entry txtChiSq:
    :ivar gtk.Entry txtMHBPValue:
    :ivar gtk.Entry txtLP:
    :ivar gtk.Entry txtZLPNorm:
    :ivar gtk.Entry txtZLPPValue:
    :ivar gtk.Entry txtLR:
    :ivar gtk.Entry txtZLRNorm:
    :ivar gtk.Entry txtZLRPValue:
    :ivar gtk.Entry txtRho:
    :ivar gtk.Entry txtRhoNorm:
    :ivar gtk.Entry txtRhoPValue:
    """

    def __init__(self):
        """
        Initializes the Results page for the MCF distribution.
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
        self.lblMHBResult = _widg.make_label(_(u""), width=150)
        self.lblZLPResult = _widg.make_label(_(u""), width=150)
        self.lblZLRResult = _widg.make_label(_(u""), width=150)
        self.lblRhoResult = _widg.make_label(_(u""), width=150)

        self.txtNumFailures = _widg.make_entry(width=50, editable=False)
        self.txtMHB = _widg.make_entry(width=100, editable=False)
        self.txtChiSq = _widg.make_entry(width=100, editable=False)
        self.txtMHBPValue = _widg.make_entry(width=100, editable=False)
        self.txtLP = _widg.make_entry(width=100, editable=False)
        self.txtZLPNorm = _widg.make_entry(width=100, editable=False)
        self.txtZLPPValue = _widg.make_entry(width=100, editable=False)
        self.txtLR = _widg.make_entry(width=100, editable=False)
        self.txtZLRNorm = _widg.make_entry(width=100, editable=False)
        self.txtZLRPValue = _widg.make_entry(width=100, editable=False)
        self.txtRho = _widg.make_entry(width=100, editable=False)
        self.txtRhoNorm = _widg.make_entry(width=100, editable=False)
        self.txtRhoPValue = _widg.make_entry(width=100, editable=False)

        self.tvwResults = gtk.TreeView()

    def create_results_page(self):
        """
        Method to create the page for displaying numerical results of the
        analysis for the MCF distribution.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _frame = _widg.make_frame(label=_(u"Summary of Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        _fxdSummary = gtk.Fixed()
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdSummary)
        _frame.add(_scrollwindow)

        self.pack1(_frame, True, True)

        _frame = _widg.make_frame(label=_(u"Mean Cumulative Function Table"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwResults)
        _frame.add(_scrollwindow)

        self.pack2(_frame, True, False)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display analysis results.           #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        self.txtNumFailures.set_tooltip_markup(
            _(u"Displays the number of "
              u"failures in the dataset."))
        self.txtMHB.set_tooltip_markup(
            _(u"Displays the value of the MIL-HDBK "
              u"test for trend."))
        self.txtChiSq.set_tooltip_markup(
            _(u"Displays the \u03C7<sup>2</sup> "
              u"critical value for the MIL-HDBK "
              u"test for trend."))
        self.txtMHBPValue.set_tooltip_markup(
            _(u"Displays the p-value for the "
              u"MIL-HDBK test for trend."))
        self.txtLP.set_tooltip_markup(
            _(u"Displays the value of the LaPlace "
              u"test for trend."))
        self.txtZLPNorm.set_tooltip_markup(
            _(u"Displays the standard normal "
              u"critical value for the LaPlace "
              u"test for trend."))
        self.txtZLPPValue.set_tooltip_markup(
            _(u"Displays the p-value for the "
              u"LaPlace test for trend."))
        self.txtLR.set_tooltip_markup(
            _(u"Displays the value of the "
              u"Lewis-Robinson test for trend."))
        self.txtZLRNorm.set_tooltip_markup(
            _(u"Displays the standard normal "
              u"critical value for the "
              u"Lewis-Robinson test for "
              u"trend."))
        self.txtZLRPValue.set_tooltip_markup(
            _(u"Displays the p-value for the "
              u"Lewis-Robinson test for "
              u"trend."))
        self.txtRho.set_tooltip_markup(
            _(u"Displays the value of the lag 1 "
              u"sample serial correlation "
              u"coefficient."))
        self.txtRhoNorm.set_tooltip_markup(
            _(u"Displays the standard normal "
              u"critical value for the lag 1 "
              u"sample serial correlation "
              u"coefficient."))
        self.txtRhoPValue.set_tooltip_markup(
            _(u"Displays the p-value for the "
              u"lag 1 sample serial "
              u"correlation coefficient."))

        # Place the summary of results widgets.
        _labels = [_(u"Number of Failures:")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fxdSummary, 5, 5)
        _x_pos += 35

        _fxdSummary.put(self.txtNumFailures, _x_pos, _y_pos[0])

        # Place the non-parametric goodness of fit statistics.
        _label = _widg.make_label(
            _(u"<u>Goodness of Fit Statistics</u>"),
            width=-1,
            justify=gtk.JUSTIFY_CENTER)
        _fxdSummary.put(_label, 275, 35)

        _label = _widg.make_label(
            _(u"Test\nStatistic"),
            height=-1,
            width=150,
            justify=gtk.JUSTIFY_CENTER)
        _fxdSummary.put(_label, 130, 65)
        _label = _widg.make_label(
            _(u"Critical Value"),
            height=-1,
            width=150,
            justify=gtk.JUSTIFY_CENTER)
        _fxdSummary.put(_label, 280, 65)
        _label = _widg.make_label(
            _(u"p-Value"), height=-1, width=150, justify=gtk.JUSTIFY_CENTER)
        _fxdSummary.put(_label, 430, 65)

        _label = _widg.make_label(_(u"MIL-HDBK:"))
        _fxdSummary.put(_label, 5, 95)
        _fxdSummary.put(self.txtMHB, 155, 95)
        _fxdSummary.put(self.txtChiSq, 305, 95)
        _fxdSummary.put(self.txtMHBPValue, 455, 95)
        _fxdSummary.put(self.lblMHBResult, 605, 95)

        _label = _widg.make_label(_(u"LaPlace:"))
        _fxdSummary.put(_label, 5, 125)
        _fxdSummary.put(self.txtLP, 155, 125)
        _fxdSummary.put(self.txtZLPNorm, 305, 125)
        _fxdSummary.put(self.txtZLPPValue, 455, 125)
        _fxdSummary.put(self.lblZLPResult, 605, 125)

        _label = _widg.make_label(_(u"Lewis-Robinson:"))
        _fxdSummary.put(_label, 5, 155)
        _fxdSummary.put(self.txtLR, 155, 155)
        _fxdSummary.put(self.txtZLRNorm, 305, 155)
        _fxdSummary.put(self.txtZLRPValue, 455, 155)
        _fxdSummary.put(self.lblZLRResult, 605, 155)

        _label = _widg.make_label(
            _(u"Serial\nCorrelation\nCoefficient:"), height=-1)
        _fxdSummary.put(_label, 5, 185)
        _fxdSummary.put(self.txtRho, 155, 185)
        _fxdSummary.put(self.txtRhoNorm, 305, 185)
        _fxdSummary.put(self.txtRhoPValue, 455, 185)
        _fxdSummary.put(self.lblRhoResult, 605, 185)

        # Place the reliability table.
        _model = gtk.ListStore(gobject.TYPE_FLOAT, gobject.TYPE_INT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT)
        self.tvwResults.set_model(_model)
        _headings = [
            _(u"Time\n(t)"),
            _(u"Number of\nFailures"),
            _(u"MCF\nLower\nLimit"),
            _(u"MCF\nPoint\nEstimate"),
            _(u"MCF\nUpper\nLimit")
        ]
        for _index, _heading in enumerate(_headings):
            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _column = gtk.TreeViewColumn()
            _label = _widg.make_column_heading(_heading)
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=_index)
            _column.set_clickable(True)
            _column.set_resizable(True)
            _column.set_sort_column_id(_index)
            self.tvwResults.append_column(_column)

        # Insert the tab.
        self.lblPage.set_markup(
            "<span weight='bold'>" + _(u"MCF\nResults") + "</span>")
        self.lblPage.set_alignment(xalign=0.5, yalign=0.5)
        self.lblPage.set_justify(gtk.JUSTIFY_CENTER)
        self.lblPage.show_all()
        self.lblPage.set_tooltip_text(
            _(u"Displays Mean Cumulative Function "
              u"analysis results for the selected "
              u"dataset."))

        return False

    def load_results_page(self, model):
        """
        Method to load the gtk.Widgets() necessary for displaying the results
        of fitting a dataset to the MCF distribution.

        :param model: the :py:class:`rtk.survival.Survival` data model to
                      display the results for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'
        _p_value = [0.0, 0.0, 0.0, 0.0]

        self._model = model

        # Load the summary information.
        self.txtNumFailures.set_text(str(self._model.n_failures))

        # Load the GoF statistics.
        _chisq = chi2.ppf(1.0 - self._model.confidence,
                          2 * self._model.n_failures)
        _z_norm = norm.ppf(self._model.confidence)

        _p_value[0] = float(
            chi2.cdf(self._model.mhb, 2 * self._model.n_failures))
        _p_value[1] = float(norm.cdf(self._model.lp))
        _p_value[2] = float(norm.cdf(self._model.lr))
        _p_value[3] = norm.cdf(self._model.rho)

        self.txtMHB.set_text(str(fmt.format(self._model.mhb)))
        self.txtLP.set_text(str(fmt.format(self._model.lp)))
        self.txtLR.set_text(str(fmt.format(self._model.lr)))
        self.txtRho.set_text(str(fmt.format(self._model.rho)))

        self.txtChiSq.set_text(str(fmt.format(_chisq)))
        self.txtZLPNorm.set_text(str(fmt.format(_z_norm)))
        self.txtZLRNorm.set_text(str(fmt.format(_z_norm)))
        self.txtRhoNorm.set_text(str(fmt.format(_z_norm)))

        self.txtMHBPValue.set_text(str(fmt.format(_p_value[0])))
        self.txtZLPPValue.set_text(str(fmt.format(_p_value[1])))
        self.txtZLRPValue.set_text(str(fmt.format(_p_value[2])))
        self.txtRhoPValue.set_text(str(fmt.format(_p_value[3])))

        if self._model.mhb > _chisq:
            self.lblMHBResult.set_markup(
                _(u"<span foreground='red'>Nonconstant</span>"))
        else:
            self.lblMHBResult.set_markup(
                _(u"<span foreground='green'>Constant</span>"))
        if fabs(self._model.lp) > _z_norm:
            self.lblZLPResult.set_markup(
                _(u"<span foreground='red'>Nonconstant</span>"))
        else:
            self.lblZLPResult.set_markup(
                _(u"<span foreground='green'>Constant</span>"))
        if fabs(self._model.lr) > _z_norm:
            self.lblZLRResult.set_markup(
                _(u"<span foreground='red'>Nonconstant</span>"))
        else:
            self.lblZLRResult.set_markup(
                _(u"<span foreground='green'>Constant</span>"))

        # Load the non-parametric results table.
        _model = self.tvwResults.get_model()
        try:
            _times = self._model.mcf[:, 0]
        except IndexError:
            _times = []

        for i in range(len(_times)):
            _model.append([
                float(_times[i, 0]),
                int(self._model.mcf[i, 1]),
                float(self._model.mcf[i, 2]),
                float(self._model.mcf[i, 3]),
                float(self._model.mcf[i, 4])
            ])

        return False


class Plots(gtk.HBox):
    """
    The Work Book page to display plots for an MCF distribution.  The
    attributes of an MCF Plot page are:

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
        Initializes the Plot page for the MCF distribution.
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

    def create_plot_page(self):
        """
        Method to create the page for displaying plots for the MCF
        distribution.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _vbox = gtk.VBox()
        self.pack_start(_vbox, True, True)

        _frame = _widg.make_frame(_(u"Run Sequence Plot"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot1)
        _vbox.pack_start(_frame, True, True)

        _frame = _widg.make_frame(_(u"Lag Plot"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot2)
        _vbox.pack_start(_frame, True, True)

        _vbox = gtk.VBox()
        self.pack_end(_vbox, True, True)

        _frame = _widg.make_frame(_(u"Mean Cumulative Function"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot3)
        _vbox.pack_start(_frame, True, True)

        # Connect widgets to callback functions.
        self.pltPlot1.mpl_connect('button_press_event', _widg.expand_plot)
        self.pltPlot2.mpl_connect('button_press_event', _widg.expand_plot)
        self.pltPlot3.mpl_connect('button_press_event', _widg.expand_plot)

        # Insert the page.
        self.lblPage.set_markup("<span weight='bold'>Analysis\nPlots</span>")
        self.lblPage.set_alignment(xalign=0.5, yalign=0.5)
        self.lblPage.set_justify(gtk.JUSTIFY_CENTER)
        self.lblPage.show_all()
        self.lblPage.set_tooltip_text(_(u"Displays survival analyses plots."))

        return False

    def load_plots(self, model):
        """
        Method to load the plots for the MCF distribution.

        :param model: the :py:class:`rtk.survival.Survival` data model to
                      display the plots for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._model = model

        self._load_run_sequence_plot()
        self._load_lag_plot()
        self._load_mcf_plot()

        return False

    def _load_run_sequence_plot(self):
        """
        Method to load plot 1 with the run-sequence plot.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.axAxis1.cla()

        # Create a list of failure dates.
        _dates = [
            x.failure_date for x in self._model.dicRecords.values()
            if x.interarrival_time != np.inf
        ]

        # Create a list of interarrival times.
        _tbf = [
            x.interarrival_time for x in self._model.dicRecords.values()
            if x.interarrival_time != np.inf
        ]

        if len(_dates) > 0 and len(_tbf) > 0:
            _plot_title = _(u"Run Sequence Plot for {0:s}").format(
                self._model.description)
            _widg.load_plot(
                self.axAxis1,
                self.pltPlot1,
                _dates,
                y1=_tbf,
                title=_plot_title,
                xlab=_(u"Date"),
                ylab=_(u"Time Between Failure"),
                ltype=[4],
                marker=['g-'])

        return False

    def _load_lag_plot(self):
        """
        Method to load plot 2 with a lag 1 plot.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.axAxis2.cla()

        # Create a list of interarrival times.
        _tbf = sorted([
            x.interarrival_time for x in self._model.dicRecords.values()
            if x.interarrival_time != np.inf
        ])

        if len(_tbf) > 0:
            _zero_line = _tbf[:-1]
            _plot_title = _(u"Lag Plot for {0:s}").format(
                self._model.description)
            _widg.load_plot(
                self.axAxis2,
                self.pltPlot2,
                _tbf[0:len(_tbf) - 1],
                y1=_tbf[1:len(_tbf)],
                y2=_zero_line,
                title=_plot_title,
                xlab=_(u"Lagged Time Between Failure"),
                ylab=_(u"Time Between Failure"),
                ltype=[2, 2],
                marker=['go', 'k-'])

        return False

    def _load_mcf_plot(self):
        """
        Method to load plot 3 with the mean cumulative function.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.axAxis3.cla()

        # Get the list of unique failure times and mcf.
        if self._model.mcf != []:
            _times = self._model.mcf[:, 0]
            _muhatll = self._model.mcf[:, 2]
            _muhat = self._model.mcf[:, 3]
            _muhatul = self._model.mcf[:, 4]

            # Plot the mean cumulative function with confidence bounds.
            _plot_title = _(u"MCF Plot for {0:s}").format(
                self._model.description)
            _widg.load_plot(
                self.axAxis3,
                self.pltPlot3,
                _times,
                y1=_muhatll,
                y2=_muhat,
                y3=_muhatul,
                title=_plot_title,
                xlab=_(u"Time"),
                ylab=_(u"Mean Cumulative Function [mu(t)]"),
                marker=['r:', 'g-', 'b:'])
            _text = (u"MCF LCL", u"MCF", u"MCF UCL")
            _widg.create_legend(
                self.axAxis3,
                _text,
                fontsize='medium',
                legframeon=True,
                location='lower right',
                legshadow=True)

        return False
