#!/usr/bin/env python
"""
#########################################################
Survival Package Kaplan-Meier Distribution Work Book View
#########################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.survival.gui.gtk.Kaplan-Meier.py is part of The RTK Project
#
# All rights reserved.

import sys

# Import modules for localization support.
import gettext
import locale

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
import pkg_resources
pkg_resources.require('matplotlib==1.4.3')
matplotlib.use('GTK')

# Import other RTK modules.
try:
    import configuration as _conf
    import widgets as _widg
except ImportError:
    import rtk.configuration as _conf
    import rtk.widgets as _widg

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Results(gtk.HPaned):
    """
    The Work Book page to display all the attributes for an Kaplan-Meier
    distribution.  The attributes of an Kaplan-Meier Results page are:

    :ivar _model: the Survival :py:class:`rtk.survival.Survival.Model`
                  whose attributes are being displayed.
    :ivar gtk.Entry txtNumFailures:
    :ivar gtk.Entry txtNumSuspensions:
    :ivar gtk.Entry txtMTBFLL:
    :ivar gtk.Entry txtMTBF:
    :ivar gtk.Entry txtMTBFUL:
    :ivar gtk.TreeView tvwResults:
    """

    def __init__(self):
        """
        Initializes the Results page for the Kaplan-Meier distribution.
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
        self.txtNumFailures = _widg.make_entry(width=50, editable=False)
        self.txtNumSuspensions = _widg.make_entry(width=50, editable=False)
        self.txtMTBFLL = _widg.make_entry(width=150, editable=False)
        self.txtMTBF = _widg.make_entry(width=150, editable=False)
        self.txtMTBFUL = _widg.make_entry(width=150, editable=False)

        self.tvwResults = gtk.TreeView()

    def create_results_page(self):
        """
        Method to create the page for displaying numerical results of the
        analysis for the Kaplan-Meier distribution.

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

        _frame = _widg.make_frame(label=_(u"Kaplan-Meier Table"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwResults)
        _frame.add(_scrollwindow)

        self.pack2(_frame, True, False)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display analysis results.           #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        self.txtNumFailures.set_tooltip_markup(_(u"Displays the number of "
                                                 u"failures in the dataset."))
        self.txtNumSuspensions.set_tooltip_markup(_(u"Displays the number of "
                                                    u"suspensions in the "
                                                    u"dataset."))
        self.txtMTBFLL.set_tooltip_markup(_(u"Displays the lower "
                                            u"<span>\u03B1</span>% confidence "
                                            u"bound on the MTBF estimated "
                                            u"from the dataset."))
        self.txtMTBF.set_tooltip_markup(_(u"Displays the point estimate of "
                                          u"the MTBF estimated from the "
                                          u"dataset."))
        self.txtMTBFUL.set_tooltip_markup(_(u"Displays the upper "
                                            u"<span>\u03B1</span>% confidence "
                                            u"bound on the MTBF estimated "
                                            u"from the dataset."))

        # Place the summary of results widgets.
        _labels = [_(u"Number of Failures:"), _(u"Number of Suspensions:")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fxdSummary, 5, 5)
        _x_pos += 35

        _fxdSummary.put(self.txtNumFailures, _x_pos, _y_pos[0])
        _fxdSummary.put(self.txtNumSuspensions, _x_pos, _y_pos[1])

        _label = _widg.make_label(_(u"LCL"), height=-1, width=150,
                                  justify=gtk.JUSTIFY_CENTER)
        _fxdSummary.put(_label, _x_pos, _y_pos[1] + 35)
        _label = _widg.make_label(_(u"Point\nEstimate"), height=-1, width=150,
                                  justify=gtk.JUSTIFY_CENTER)
        _fxdSummary.put(_label, _x_pos + 155, _y_pos[1] + 35)
        _label = _widg.make_label(_(u"UCL"), height=-1, width=150,
                                  justify=gtk.JUSTIFY_CENTER)
        _fxdSummary.put(_label, _x_pos + 310, _y_pos[1] + 35)

        _label = _widg.make_label(_(u"MTBF:"))
        _fxdSummary.put(_label, 5, _y_pos[1] + 75)
        _fxdSummary.put(self.txtMTBFLL, _x_pos, _y_pos[1] + 75)
        _fxdSummary.put(self.txtMTBF, _x_pos + 155, _y_pos[1] + 75)
        _fxdSummary.put(self.txtMTBFUL, _x_pos + 310, _y_pos[1] + 75)

        # Place the reliability table.
        _model = gtk.ListStore(gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
        self.tvwResults.set_model(_model)
        _headings = [_(u"Time\n(t)"), _(u"S(t) Lower\nBound"), _(u"S(t)"),
                     _(u"S(t) Upper\nBound"), _(u"h(t) Lower\nBound"),
                     _(u"Hazard\nRate h(t)"), _(u"h(t) Upper\nBound"),
                     _(u"H(t) Lower\nBound"),
                     _(u"Cumulative\nHazard\nRate H(t)"),
                     _(u"H(t) Upper\nBound")]
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
        self.lblPage.set_markup("<span weight='bold'>" +
                                _(u"Kaplan-Meier\nResults") + "</span>")
        self.lblPage.set_alignment(xalign=0.5, yalign=0.5)
        self.lblPage.set_justify(gtk.JUSTIFY_CENTER)
        self.lblPage.show_all()
        self.lblPage.set_tooltip_text(_(u"Displays Kaplan-Meier analysis "
                                        u"results for the selected dataset."))

        return False

    def load_results_page(self, model):
        """
        Method to load the gtk.Widgets() necessary for displaying the results
        of fitting a dataset to the Kaplan-Meier distribution.

        :param model: the :py:class:`rtk.survival.Survival` data model to
                      display the results for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        self._model = model

        # Load the summary information.
        self.txtNumFailures.set_text(str(self._model.n_failures))
        self.txtNumSuspensions.set_text(str(self._model.n_suspensions))

        self.txtMTBFLL.set_text(str(fmt.format(self._model.scale[0])))
        self.txtMTBF.set_text(str(fmt.format(self._model.scale[1])))
        self.txtMTBFUL.set_text(str(fmt.format(self._model.scale[2])))

        # Load the non-parametric results table.
        _model = self.tvwResults.get_model()
        for _index, _row in enumerate(self._model.km):
            _model.append([_row[0], _row[1], _row[2], _row[3],
                           self._model.hazard[3][_index],
                           self._model.hazard[2][_index],
                           self._model.hazard[1][_index],
                           self._model.hazard[6][_index],
                           self._model.hazard[5][_index],
                           self._model.hazard[4][_index]])

        return False


class Plots(gtk.HBox):
    """
    The Work Book page to display plots for an Kaplan-Meier distribution.  The
    attributes of an Kaplan-Meier Plot page are:

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
        Initializes the Plot page for the Kaplan-Meier distribution.
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
        Method to create the page for displaying plots for the Kaplan-Meier
        distribution.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _vbox = gtk.VBox()
        self.pack_start(_vbox, True, True)

        _frame = _widg.make_frame(_(u"Survival Function"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot1)
        _vbox.pack_start(_frame, True, True)

        _frame = _widg.make_frame(_(u"Hazard Function"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot2)
        _vbox.pack_end(_frame, True, True)

        _vbox = gtk.VBox()
        self.pack_end(_vbox, True, True)

        _frame = _widg.make_frame(_(u"Cumulative Hazard Function"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot3)
        _vbox.pack_start(_frame, True, True)

        _frame = _widg.make_frame(_(u"Log Cumulative Hazard Function"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot4)
        _vbox.pack_end(_frame, True, True)

        # Connect widgets to callback functions.
        self.pltPlot1.mpl_connect('button_press_event', _widg.expand_plot)
        self.pltPlot2.mpl_connect('button_press_event', _widg.expand_plot)
        self.pltPlot3.mpl_connect('button_press_event', _widg.expand_plot)
        self.pltPlot4.mpl_connect('button_press_event', _widg.expand_plot)

        # Insert the page.
        self.lblPage.set_markup("<span weight='bold'>Analysis\nPlots</span>")
        self.lblPage.set_alignment(xalign=0.5, yalign=0.5)
        self.lblPage.set_justify(gtk.JUSTIFY_CENTER)
        self.lblPage.show_all()
        self.lblPage.set_tooltip_text(_(u"Displays survival analyses plots."))

        return False

    def load_plots(self, model):
        """
        Method to load the plots for the Kaplan-Meier distribution.

        :param model: the :py:class:`rtk.survival.Survival` data model to
                      display the plots for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._model = model

        self._load_survival_plot()
        self._load_hazard_plot()
        self._load_cumulative_hazard_plot()
        self._load_log_hazard_plot()

        return False

    def _load_survival_plot(self):
        """
        Method to load plot 1 with the survival function.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.axAxis1.cla()

        if self._model.km != []:
            _plot_title = _(u"Survival Function Plot for {0:s}").format(
                self._model.description)
            _widg.load_plot(self.axAxis1, self.pltPlot1,
                            x=self._model.km[:, 0], y1=self._model.km[:, 1],
                            y2=self._model.km[:, 2], y3=self._model.km[:, 3],
                            _title=_plot_title, _xlab=_(u"Time"),
                            _ylab=_(u"Survival Function [S(t)] "),
                            _marker=['r:', 'g-', 'b:'])
            _text = (u"S(t) LCL", u"Survival Function [S(t)]", u"S(t) UCL")
            _widg.create_legend(self.axAxis1, _text, fontsize='medium',
                                legframeon=True, location='upper right',
                                legshadow=True)

        return False

    def _load_hazard_plot(self):
        """
        Method to load plot 2 with the hazard function.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.axAxis2.cla()

        if self._model.hazard != []:
            _plot_title = (u"Hazard Rate Plot for {0:s}").format(
                self._model.description)
            _widg.load_plot(self.axAxis2, self.pltPlot2,
                            x=self._model.hazard[0],
                            y1=self._model.hazard[1],
                            y2=self._model.hazard[2],
                            y3=self._model.hazard[3],
                            _title=_plot_title, _xlab=_(u"Time"),
                            _ylab=_(u"Hazard Rate [h(t)] "),
                            _marker=['b:', 'g-', 'r:'])
            _text = (u"h(t) UCL", u"Hazard Rate [h(t)]", u"h(t) LCL")
            _widg.create_legend(self.axAxis2, _text, fontsize='medium',
                                legframeon=True, location='upper right',
                                legshadow=True)

        return False

    def _load_cumulative_hazard_plot(self):
        """
        Method to load plot 3 with the cumulative hazard function.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.axAxis3.cla()

        if self._model.hazard != []:
            _plot_title = _(u"Cumulative Hazard Plot for {0:s}").format(
                self._model.description)
            _widg.load_plot(self.axAxis3, self.pltPlot3,
                            x=self._model.hazard[0], y1=self._model.hazard[4],
                            y2=self._model.hazard[5], y3=self._model.hazard[6],
                            _title=_plot_title, _xlab=_("Time"),
                            _ylab=_("Cumulative Hazard Function [H(t)] "),
                            _marker=['b:', 'g-', 'r:'])
            _text = (u"H(t) UCL", u"Cumulative Hazard Function [H(t)]",
                     u"H(t) LCL")
            _widg.create_legend(self.axAxis3, _text, fontsize='medium',
                                legframeon=True, location='upper left',
                                legshadow=True)

        return False

    def _load_log_hazard_plot(self):
        """
        Method to load plot 4 with the logarithm of the cumulative hazard
        function.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.axAxis4.cla()

        if self._model.hazard != []:
            _plot_title = _("Log Cumulative Hazard Plot for {0:s}").format(
                self._model.description)
            _widg.load_plot(self.axAxis4, self.pltPlot4,
                            x=self._model.hazard[0], y1=self._model.hazard[7],
                            y2=self._model.hazard[8], y3=self._model.hazard[9],
                            _title=_plot_title, _xlab=_("log(Time)"),
                            _ylab=_("Log Cum. Hazard Function [log H(t)] "),
                            _marker=['b:', 'g-', 'r:'])
            _text = (u"log H(t) UCL",
                     u"Log Cumulative Hazard Function [log H(t)]",
                     u"log H(t) LCL")
            _widg.create_legend(self.axAxis4, _text, fontsize='medium',
                                legframeon=True, location='upper left',
                                legshadow=True)

        return False
