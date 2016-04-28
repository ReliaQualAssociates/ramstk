#!/usr/bin/env python
"""
################################################
Reliability Growth Testing Module Work Book View
################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.testing.gui.gtk.Growth.py is part of The RTK Project
#
# All rights reserved.

import sys

# Import modules for localization support.
import gettext
import locale

import numpy as np

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

# Modules used for plotting.
import matplotlib
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse
matplotlib.use('GTK')

# Import other RTK modules.
try:
    import Configuration
    import Utilities
    import gui.gtk.Widgets as Widgets
    import analyses.statistics.growth.CrowAMSAA as CrowAMSAA
    import analyses.statistics.growth.SPLAN as SPLAN
    from testing.Assistants import MTBFICalculator
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    import rtk.gui.gtk.Widgets as Widgets
    import rtk.analyses.statistics.growth.CrowAMSAA as CrowAMSAA
    import rtk.analyses.statistics.growth.SPLAN as SPLAN
    from rtk.testing.Assistants import MTBFICalculator

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _expand_plot(event):
    """
    Function to display a plot in it's own window.

    :param event: the matplotlib MouseEvent that called this function.
    :return: False if successful or True if an error is encountered.
    :rtype: boolean
    """

    _plot = event.canvas
    _parent = _plot.get_parent()

    if event.button == 3:               # Right click.
        _window = gtk.Window()
        _window.set_skip_pager_hint(True)
        _window.set_skip_taskbar_hint(True)
        _window.set_default_size(1000, 700)
        _window.set_border_width(5)
        _window.set_position(gtk.WIN_POS_NONE)
        _window.set_title(_(u"RTK Plot"))

        _window.connect('delete_event', _close_plot, _plot, _parent)

        _plot.reparent(_window)

        _window.show_all()

    return False


def _close_plot(__window, __event, plot, parent):
    """
    Function to close the plot and return it to its original parent widget.

    :param gtk.Window __window: the gtk.Window() that is being destroyed.
    :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                  function.
    :param matplotlib.FigureCanvas plot: the matplotlib FigureCanvas that was
                                         expanded.
    :param gtk.Widget parent: the original parent widget for the plot.
    :return: False if successful or True if an error is encountered
    :rtype: boolean
    """

    plot.reparent(parent)

    return False


def _plot_ideal(axis1, plot, x_vals, y_vals, x_max, y_max, xlabel, ylabel,
                log=False):
    """
    Function to plot the Reliability Growth ideal and planned curves.

    :param axis1: the matplotlib Axis() to plot against.
    :param plot: the matplotlib FigureCanvas() to draw the plot on.
    :param list x_vals: the list of x values for the plot.
    :param list y_vals: a list of y value lists for the plot.
    :param float x_max: the maximum x value for the x-axis.
    :param float y_max: the maximum y value for the y-axis.
    :param str xlabel: the label for the x-axis.
    :param str ylabel: the label for the y-axis.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    _lines = []
    _cols = ['b', 'r']

    # Clear the plot of any existing data.
    axis1.cla()

    if log:
        axis1.set_xscale('log')
        axis1.set_yscale('log')
    else:
        axis1.set_xscale('linear')
        axis1.set_yscale('linear')

    # Add each line to the plot if the x and y values are of the same length.
    for _index, _y_val in enumerate(y_vals):
        if len(x_vals) == len(_y_val):
            _line = matplotlib.lines.Line2D(x_vals, _y_val, lw=1.5,
                                            color=_cols[_index])
            axis1.add_line(_line)
            _lines.append(_line)

    # Add labels to the axes and adjust them slightly for readability.
    axis1.set_xlabel(xlabel)
    axis1.set_ylabel(ylabel)
    axis1.set_xlim(right=1.1 * x_max)
    axis1.set_ylim(bottom=0.0, top=1.05 * y_max)
    plot.draw()

    return _lines


def _plot_assessed(axis1, x_vals, y_vals, index=0):
    """
    Function to plot the assessed values with error bars.

    :param axis1: the matplotlib Axis() to plot against.
    :param list x_vals: the list of x-values for the plot.
    :param list y_vals: a list of y-value lists for the plot.  This list
                        consists of [[lower limit values], [point estimates],
                                     [upper limit values]]
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    _cols = ['g', 'k']
    _markers = ['o', 's']

    _l_bar = y_vals[1] - y_vals[0]
    _u_bar = y_vals[2] - y_vals[1]
    # axis1.errorbar(x_vals, y_vals[1], yerr=[_l_bar, _u_bar], fmt='o',
    #                ecolor=_cols[index], color=_cols[index])

    _line = matplotlib.lines.Line2D(x_vals, y_vals[1], ls='None',
                                    marker=_markers[index], color=_cols[index])
    axis1.add_line(_line)

    return _line


def _add_targets(axis1, targets, x_max):
    """
    Function to add target lines and bubbles to a plot.

    :param list targets: list of target values.
    :param float x_max: the maximum x value displayed on the plot.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'

    # Add each target line and annotation bubble.
    for __, _target in enumerate(targets):
        _line = axis1.axhline(y=_target, xmin=0, color='m',
                              linewidth=2.5, linestyle=':')

        axis1.annotate(str(fmt.format(_target)), xy=(x_max, _target),
                       xycoords='data', xytext=(25, -25),
                       textcoords='offset points', size=12, va="center",
                       bbox=dict(boxstyle="round", fc='#E5E5E5',
                                 ec='None', alpha=0.5),
                       arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                       fc='#E5E5E5', ec='None',
                                       alpha=0.5, patchA=None,
                                       patchB=Ellipse((2, -1), 0.5, 0.5),
                                       relpos=(0.5, 0.5)))

    return _line


def _add_legend(axis1, lines, legend):
    """
    Function to add a legend to a Reliability Growth plot.

    :param list lines: the list of lines to add to the legend.
    :param tuple legend: tuple of legend text.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    # Create and place the legend.
    _leg = axis1.legend(lines, legend, loc='best', shadow=True)
    for _text in _leg.get_texts():
        _text.set_fontsize('small')
    for _line in _leg.get_lines():
        _line.set_linewidth(0.5)

    return False


class Planning(gtk.HPaned):                 # pylint: disable=R0902, R0904
    """
    The Work Book view displays all the attributes for the selected Reliability
    Growth Test Plan.  The attributes of a Reliability Growth Test Planning
    Work Book view are:

    :ivar list _lst_handler_id: the list containing gtk.Widget() signal handler
                                IDs.
    :ivar _testing_model: the :py:class:`rtk.testing.growth.Growth.Model` whose
                          attributes are being displayed.
    :ivar gtk.Button btnFindMTBFI: the gtk.Button()
    :ivar gtk.Button btnFindMTBFGP: the gtk.Button()
    :ivar gtk.Button btnFindt1: the gtk.Button()
    :ivar gtk.Button btnFindTTT: the gtk.Button()
    :ivar gtk.Button btnFindAlpha: the gtk.Button()
    :ivar gtk.Button btnFindFEF: the gtk.Button()
    :ivar gtk.Button btnFindMS: the gtk.Button()
    :ivar gtk.Button btnFindProb: the gtk.Button()
    :ivar gtk.Button btnCalculate: the gtk.Button() used to call the data
                                   controller 'request_calculate' method.
    :ivar gtk.Button btnSave: the gtk.Button() used to call the data controller
                              'request_save' method.
    :ivar gtk.ComboBox cmbPlanModel: the gtk.ComboBox() to select and display
                                     the planning model.
    :ivar gtk.ComboBox cmbAssessModel: the gtk.ComboBox() to select and display
                                       the assessment/projection model.
    :ivar dtcGrowth: the :py:class:`rtk.testing.growth.Growth.Growth` data
                     controller.
    :ivar gtk.SpinButton spnNumPhases: the gtk.SpinButton() to enter and
                                       display the number of test phases.
    :ivar gtk.TreeView tvwRGTestPlan: the gtk.TreeView() to edit and display
                                      the test phase details.
    :ivar gtk.Entry txtTechReq: the gtk.Entry() to enter and display the
                                program technical requirement MTBF.
    :ivar gtk.Entry txtMTBFG: the gtk.Entry() to enter and display the program
                              goal MTBF.
    :ivar gtk.Entry txtMTBFGP: the gtk.Entry() to enter and display the growth
                               potential MTBF.
    :ivar gtk.Entry txtMTBFI: the gtk.Entry() to enter and display the average
                              MTBF over the first test phase.
    :ivar gtk.Entry txtTTT: the gtk.Entry() to enter and display the program
                            total time on test.
    :ivar gtk.Entry txtAverageGR: the gtk.Entry() to enter and display the
                                  program average growth rate.
    :ivar gtk.Entry txtProgramMS: the gtk.Entry() to enter and display the
                                  program average management strategy.
    :ivar gtk.Entry txtAverageFEF: the gtk.Entry() to enter and display the
                                   program average fix effectiveness factor.
    :ivar gtk.Entry txtProgramProb: the gtk.Entry() to enter and display the
                                    average program probability of observing
                                    a failure.
    :ivar gtk.Entry txtTTFF: the gtk.Entry() to enter and display the length of
                             the first test phase.
    """

    def __init__(self, controller, listbook):
        """
        Method to initialize the Work Book view for the Reliability Growth Test
        Planning.

        :param controller: the :py:class:`rtk.testing.growth.Growth.Growth`
                           data controller.
        :param listbook: the :py:class:`rtk.testing.ListBook.ListView`
                         associated with the WorkBook this is embedded in.
        """

        gtk.HPaned.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self.dtcGrowth = controller
        self._listview = listbook
        self._testing_model = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.btnFindMTBFI = Widgets.make_button(height=25, width=25,
                                                image='calculate')
        self.btnFindMTBFGP = Widgets.make_button(height=25, width=25,
                                                 image='calculate')
        self.btnFindt1 = Widgets.make_button(height=25, width=25,
                                             image='calculate')
        self.btnFindTTT = Widgets.make_button(height=25, width=25,
                                              image='calculate')
        self.btnFindAlpha = Widgets.make_button(height=25, width=25,
                                                image='calculate')
        self.btnFindFEF = Widgets.make_button(height=25, width=25,
                                              image='calculate')
        self.btnFindMS = Widgets.make_button(height=25, width=25,
                                             image='calculate')
        self.btnFindProb = Widgets.make_button(height=25, width=25,
                                               image='calculate')
        self.btnCalculate = Widgets.make_button(width=35, image='calculate')
        self.btnSave = Widgets.make_button(width=35, image='save')

        self.cmbPlanModel = Widgets.make_combo()
        self.cmbAssessModel = Widgets.make_combo()

        self.figFigure1 = Figure()
        self.pltPlot1 = FigureCanvas(self.figFigure1)
        self.axAxis1 = self.figFigure1.add_subplot(111)

        self.optMTBF = gtk.RadioButton(label=_(u"Display results as MTBF"))

        self.optMTBF.set_name('mtbf')
        self.optMTBF.set_active(True)

        self.optFailureIntensity = gtk.RadioButton(group=self.optMTBF,
                                                   label=_(u"Display results "
                                                           u"as failure "
                                                           u"intensity"))
        self.optFailureIntensity.set_name('failureintensity')

        self.optLinear = gtk.RadioButton(label=_(u"Use Linear Scales"))
        self.optLinear.set_name('linear')
        self.optLinear.set_active(True)
        self.optLogarithmic = gtk.RadioButton(group=self.optLinear,
                                              label=_(u"Use Logarithmic "
                                                      u"Scales"))
        self.optLogarithmic.set_name('log')

        self.spnNumPhases = gtk.SpinButton()

        self.spnNumPhases.set_digits(0)
        self.spnNumPhases.set_increments(1, 5)
        self.spnNumPhases.set_range(0, 100)

        self.txtTechReq = Widgets.make_entry(width=100)
        self.txtMTBFG = Widgets.make_entry(width=100)
        self.txtMTBFGP = Widgets.make_entry(width=100)
        self.txtMTBFI = Widgets.make_entry(width=100)
        self.txtTTT = Widgets.make_entry(width=100)
        self.txtAverageGR = Widgets.make_entry(width=100)
        self.txtProgramMS = Widgets.make_entry(width=100)
        self.txtAverageFEF = Widgets.make_entry(width=100)
        self.txtProgramProb = Widgets.make_entry(width=100)
        self.txtt1 = Widgets.make_entry(width=100)

        # Set gtk.Widget() tooltip text.
        self.btnFindMTBFI.set_tooltip_text(_(u"Launches the initial MTBF "
                                             u"calculator."))
        self.btnFindMTBFGP.set_tooltip_text(_(u"Calculates the program growth "
                                              u"potential MTBF."))
        self.btnFindt1.set_tooltip_text(_(u"Calculates the minimum required "
                                          u"length of the first test phase."))
        self.btnFindTTT.set_tooltip_text(_(u"Calculates the minimum required "
                                           u"time for the test program to "
                                           u"achieve the goal MTBF."))
        self.btnFindAlpha.set_tooltip_text(_(u"Calculates the minimum "
                                             u"required growth rate to "
                                             u"sustain over the test program "
                                             u"to achieve the goal MTBF."))
        self.btnFindFEF.set_tooltip_text(_(u"Calculates the average required "
                                           u"fix effectiveness factor (FEF) "
                                           u"to sustain over the test program "
                                           u"to achieve the goal MTBF."))
        self.btnFindMS.set_tooltip_text(_(u"Calculates the average required "
                                          u"management strategy (MS) to "
                                          u"sustain over the test program to "
                                          u"achieve the goal MTBF."))
        self.btnFindProb.set_tooltip_text(_(u"Calculates the probability of "
                                            u"observing a failure during the "
                                            u"first phase of the test "
                                            u"program."))
        self.btnCalculate.set_tooltip_text(_(u"Calculate the missing test "
                                             u"planning inputs."))
        self.btnSave.set_tooltip_text(_(u"Saves changes to the test planning "
                                        u"inputs."))

        self.cmbPlanModel.set_tooltip_text(_(u"Selects and displays the "
                                             u"reliability growth planning "
                                             u"model to be used."))
        self.cmbAssessModel.set_tooltip_text(_(u"Selects and displays the "
                                               u"reliability growth "
                                               u"assessment model to be "
                                               u"used."))

        self.optMTBF.set_tooltip_text(_(u"If selected, test results will be "
                                        u"displayed as MTBF.  This is the "
                                        u"default."))
        self.optFailureIntensity.set_tooltip_text(_(u"If selected, test "
                                                    u"results will be "
                                                    u"displayed as failure "
                                                    u"intensity (failure "
                                                    u"rate)."))
        self.optLinear.set_tooltip_text(_(u"Select this option to use linear "
                                          u"scales on the reliability growth "
                                          u"plot."))
        self.optLogarithmic.set_tooltip_text(_(u"Select this option to use "
                                               u"logarithmic scales on the "
                                               u"reliability growth plot."))

        self.pltPlot1.set_tooltip_text(_(u"Displays the selected test plan "
                                         u"and observed results."))

        self.spnNumPhases.set_tooltip_text(_(u"Sets the number of test phases "
                                             u"for the selected test."))
        self.spnNumPhases.set_tooltip_text(_(u"The number of reliability "
                                             u"growth phases."))

        self.txtMTBFI.set_tooltip_text(_(u"The average MTBF of the first test "
                                         u"phase for the seleceted "
                                         u"reliability growth plan."))
        self.txtMTBFG.set_tooltip_text(_(u"The goal MTBF for the selected "
                                         u"reliability growth plan."))
        self.txtMTBFGP.set_tooltip_text(_(u"The potential MTBF at maturity "
                                          u"for the assembly associated with "
                                          u"the selected reliability growth "
                                          u"plan."))
        self.txtTechReq.set_tooltip_text(_(u"The MTBF require by the "
                                           u"developmental program associated "
                                           u"with the selected reliability "
                                           u"growth plan."))
        self.txtt1.set_tooltip_text(_(u"The estimated time to the first fix "
                                      u"during the reliability growth "
                                      u"program."))
        self.txtTTT.set_tooltip_text(_(u"The total test time."))
        self.txtAverageGR.set_tooltip_text(_(u"The average growth rate over "
                                             u"the entire reliability growth "
                                             u"program."))
        self.txtAverageFEF.set_tooltip_text(_(u"The average fix effectiveness "
                                              u"factor (FEF) over the entire "
                                              u"reliability growth program."))
        self.txtProgramMS.set_tooltip_text(_(u"The percentage of failures "
                                             u"that will be addressed by "
                                             u"corrective action over the "
                                             u"entire reliability growth "
                                             u"program."))
        self.txtProgramProb.set_tooltip_text(_(u"The probability of seeing a "
                                               u"failure during the first "
                                               u"phase of the reliability "
                                               u"growth program."))

        # Connect gtk.Widget() signals to callback methods.
        self._lst_handler_id.append(
            self.btnFindMTBFI.connect('button-release-event',
                                      self._on_button_clicked, 0))
        self._lst_handler_id.append(
            self.btnFindMTBFGP.connect('button-release-event',
                                       self._on_button_clicked, 1))
        self._lst_handler_id.append(
            self.btnFindt1.connect('button-release-event',
                                   self._on_button_clicked, 2))
        self._lst_handler_id.append(
            self.btnFindTTT.connect('button-release-event',
                                    self._on_button_clicked, 3))
        self._lst_handler_id.append(
            self.btnFindAlpha.connect('button-release-event',
                                      self._on_button_clicked, 4))
        self._lst_handler_id.append(
            self.btnFindFEF.connect('button-release-event',
                                    self._on_button_clicked, 5))
        self._lst_handler_id.append(
            self.btnFindMS.connect('button-release-event',
                                   self._on_button_clicked, 6))
        self._lst_handler_id.append(
            self.btnFindProb.connect('button-release-event',
                                     self._on_button_clicked, 7))
        self._lst_handler_id.append(
            self.btnCalculate.connect('button-release-event',
                                      self._on_button_clicked, 8))
        self._lst_handler_id.append(
            self.btnSave.connect('button-release-event',
                                 self._on_button_clicked, 9))

        self._lst_handler_id.append(
            self.cmbPlanModel.connect('changed', self._on_combo_changed, 10))
        self._lst_handler_id.append(
            self.cmbAssessModel.connect('changed', self._on_combo_changed, 11))

        self.optMTBF.connect('toggled', self._load_plot)
        self.optFailureIntensity.connect('toggled', self._load_plot)
        self.optLinear.connect('toggled', self._load_plot)
        self.optLogarithmic.connect('toggled', self._load_plot)

        self._lst_handler_id.append(
            self.spnNumPhases.connect('focus-out-event',
                                      self._on_focus_out, 12))
        self._lst_handler_id.append(
            self.spnNumPhases.connect('value-changed',
                                      self._on_spin_value_changed, 13))

        self._lst_handler_id.append(
            self.txtMTBFI.connect('focus-out-event', self._on_focus_out, 14))
        self._lst_handler_id.append(
            self.txtMTBFG.connect('focus-out-event', self._on_focus_out, 15))
        self._lst_handler_id.append(
            self.txtTechReq.connect('focus-out-event', self._on_focus_out, 16))
        self._lst_handler_id.append(
            self.txtMTBFGP.connect('focus-out-event', self._on_focus_out, 17))
        self._lst_handler_id.append(
            self.txtt1.connect('focus-out-event', self._on_focus_out, 18))
        self._lst_handler_id.append(
            self.txtTTT.connect('focus-out-event', self._on_focus_out, 19))
        self._lst_handler_id.append(
            self.txtAverageGR.connect('focus-out-event',
                                      self._on_focus_out, 20))
        self._lst_handler_id.append(
            self.txtAverageFEF.connect('focus-out-event',
                                       self._on_focus_out, 21))
        self._lst_handler_id.append(
            self.txtProgramMS.connect('focus-out-event',
                                      self._on_focus_out, 22))
        self._lst_handler_id.append(
            self.txtProgramProb.connect('focus-out-event',
                                        self._on_focus_out, 23))

        self.pltPlot1.mpl_connect('button_press_event', _expand_plot)

        self.show_all()

    def create_page(self):
        """
        Method to create the page for displaying the Reliability Growth Test
        Phase details for the selected Growth Test.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HBox()
        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        _hbox.pack_start(_bbox, False, True)

        _bbox.pack_start(self.btnCalculate, False, False)
        _bbox.pack_start(self.btnSave, False, False)

        _fixed = gtk.Fixed()

        _frame = Widgets.make_frame(_(u"Program Planning Inputs"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_fixed)

        _hbox.pack_end(_frame)

        self.pack1(_hbox, False, True)

        # Load the gtk.ComboBox()
        _results = [["AMSAA-Crow"], ["SPLAN"], ["SSPLAN"]]
        Widgets.load_combo(self.cmbPlanModel, _results)

        _results = [[_(u"AMSAA/Crow Continuous")], [_(u"AMSAA/Crow Discrete")],
                    ["SSTRACK"], [_(u"AMSAA/Crow Projection")],
                    [_(u"Crow Extended")]]
        Widgets.load_combo(self.cmbAssessModel, _results)

        # Create the labels.
        _labels = [_(u"RG Planning Model:"), _(u"RG Assessment Model:"),
                   _(u"Phase 1 Average MTBF (MTBF<sub>I</sub>):"),
                   _(u"Program Required MTBF (MTBF<sub>TR</sub>):"),
                   _(u"Program Goal MTBF (MTBF<sub>G</sub>):"),
                   _(u"Potential Mature MTBF (MTBF<sub>GP</sub>):"),
                   _(u"Number of Phases:"),
                   _(u"Time to First Fix (t<sub>1</sub>):"),
                   _(u"Total Test Time:"), _(u"Average Program Growth Rate:"),
                   _(u"Average Program FEF:"), _(u"Average Program MS:"),
                   _(u"Average Program Probability:")]

        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5, 30)
        _x_pos += 50

        # Position the gtk.Widget() on the page.
        _fixed.put(self.cmbPlanModel, _x_pos, _y_pos[0])
        _fixed.put(self.cmbAssessModel, _x_pos, _y_pos[1])
        _fixed.put(self.txtMTBFI, _x_pos, _y_pos[2])
        _fixed.put(self.btnFindMTBFI, _x_pos + 125, _y_pos[2])
        _fixed.put(self.txtTechReq, _x_pos, _y_pos[3])
        _fixed.put(self.txtMTBFG, _x_pos, _y_pos[4])
        _fixed.put(self.txtMTBFGP, _x_pos, _y_pos[5])
        _fixed.put(self.btnFindMTBFGP, _x_pos + 125, _y_pos[5])
        _fixed.put(self.spnNumPhases, _x_pos, _y_pos[6])
        _fixed.put(self.txtt1, _x_pos, _y_pos[7])
        _fixed.put(self.btnFindt1, _x_pos + 125, _y_pos[7])
        _fixed.put(self.txtTTT, _x_pos, _y_pos[8])
        _fixed.put(self.btnFindTTT, _x_pos + 125, _y_pos[8])
        _fixed.put(self.txtAverageGR, _x_pos, _y_pos[9])
        _fixed.put(self.btnFindAlpha, _x_pos + 125, _y_pos[9])
        _fixed.put(self.txtAverageFEF, _x_pos, _y_pos[10])
        _fixed.put(self.btnFindFEF, _x_pos + 125, _y_pos[10])
        _fixed.put(self.txtProgramMS, _x_pos, _y_pos[11])
        _fixed.put(self.btnFindMS, _x_pos + 125, _y_pos[11])
        _fixed.put(self.txtProgramProb, _x_pos, _y_pos[12])
        _fixed.put(self.btnFindProb, _x_pos + 125, _y_pos[12])

        # Create the Reliability Growth Plot (right half of page).
        _vbox = gtk.VBox()

        _fixed = gtk.Fixed()
        _vbox.pack_start(_fixed, False, True)

        _frame = Widgets.make_frame(label=_(u"Program Planning Curves"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot1)
        _frame.show_all()

        _vbox.pack_start(_frame, True, True)

        self.pack2(_vbox, True, False)

        _y_pos = 5
        _fixed.put(self.optMTBF, 5, _y_pos)
        _fixed.put(self.optFailureIntensity, 205, _y_pos)
        _y_pos += 30
        _fixed.put(self.optLinear, 5, _y_pos)
        _fixed.put(self.optLogarithmic, 205, _y_pos)

        return False

    def load_page(self, model):
        """
        Method to load the Reliability Growth Test Plan gtk.Notebook() page.

        :param model: the :py:class:`rtk.testing.Testing.Model` to load.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._testing_model = model

        fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'

        # Load the individual widgets.
        self.cmbPlanModel.set_active(model.rg_plan_model)
        self.cmbAssessModel.set_active(model.rg_assess_model)
        self.txtMTBFI.set_text(str(fmt.format(model.lst_i_mtbfa[0])))
        self.txtMTBFG.set_text(str(fmt.format(model.mtbfg)))
        self.txtTechReq.set_text(str(fmt.format(model.tr)))
        self.txtMTBFGP.set_text(str(fmt.format(model.mtbfgp)))
        self.spnNumPhases.set_value(model.n_phases)
        self.txtTTT.set_text(str(fmt.format(model.ttt)))
        self.txtAverageGR.set_text(str(fmt.format(model.avg_growth)))
        self.txtAverageFEF.set_text(str(fmt.format(model.avg_fef)))
        self.txtProgramMS.set_text(str(fmt.format(model.avg_ms)))
        self.txtProgramProb.set_text(str(fmt.format(model.probability)))
        self.txtt1.set_text(str(fmt.format(model.lst_p_test_time[0])))

        # Load the Reliability Growth Plan plot.
        self._load_plot()

        # (Re-)load the List Book.
        self._listview.load(self._testing_model)

        return False

    def _load_plot(self, __button=None, ideal=None, plan=None):    # pylint: disable=R0914
        """
        Method to load the Reliability Growth planning plot.

        :keyword gtk.RadioButton __button: the gtk.RadioButton() that called
                                           this method when it is called by a
                                           gtk.RadioButton().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# TODO: Re-write Planning._load_plot; current McCabe Complexity metric=12.
        _log = False

        if(self._testing_model.ttt <= 0.0 and
           len(self._testing_model.dic_test_data.values()) > 0):
            self._testing_model.ttt = [x[3] for x in
                                       self._testing_model.dic_test_data.values()][-1]

        _times = [_t for _t in range(int(self._testing_model.ttt))]

        # If the ideal curve hasn't been calculated, then calculate it's
        # values.
        if ideal is None or ideal == []:
            ideal = self._testing_model.calculate_idealized_growth_curve()

        # If the planned curves haven't been calculated, then calculate their
        # values.
        if plan is None or plan == []:
            plan = self._testing_model.create_planned_values()

        _xlabel = _(u"Cumulative Test Time")
        if self.optMTBF.get_active():
            _targets = self._testing_model.lst_p_mtbfa
            _ylabel = u"MTBF"

        elif self.optFailureIntensity.get_active():
            ideal = [1.0 / _mtbf for _mtbf in ideal]
            plan = [1.0 / _mtbf for _mtbf in plan]
            _targets = [1.0 / _mtbfa
                        for _mtbfa in self._testing_model.lst_p_mtbfa]
            _ylabel = _(u"Failure Intensity")

        # Find the maximum y-value.
        try:
            _y_max = max(max(ideal), max(plan), max(_targets))
        except ValueError:
            _y_max = 0.0

        if self.optLogarithmic.get_active():
            _log = True

        _lines = _plot_ideal(self.axAxis1, self.pltPlot1, _times,
                             [ideal, plan], self._testing_model.ttt, _y_max,
                             _xlabel, _ylabel, _log)

        # Add the target values to the plot.
        _l = _add_targets(self.axAxis1, _targets, self._testing_model.ttt)
        _lines.append(_l)

        # Add the legend to the plot.
        _legend = (_(u"Idealized Growth Curve"),
                   _(u"Planned Average Values"), _(u"Target Values"))
        _add_legend(self.axAxis1, _lines, _legend)

        self.pltPlot1.draw()

        return False

    def _on_button_clicked(self, button, __event, index):
        """
        Method to respond to gtk.Button() 'clicked' signals and call the
        correct function or method, passing any parameters as needed.

        :param gtk.Button button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# TODO: Re-write Planning._on_button_clicked; current McCabe Complexity metric=23.
        fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'

        button.handler_block(self._lst_handler_id[index])

        if index == 0:
            MTBFICalculator(self.txtMTBFI, self._testing_model)
        elif index == 1:
            _mtbfa = self._testing_model.lst_i_mtbfa[0]
            _ms = self._testing_model.avg_ms
            _fef = self._testing_model.avg_fef
            if _mtbfa > 0.0 and _ms > 0.0 and _fef > 0.0:
                _mtbfgp = SPLAN.calculate_growth_potential(_mtbfa, _ms, _fef)
                self._testing_model.mtbfgp = _mtbfgp
                self.txtMTBFGP.set_text(str(fmt.format(_mtbfgp)))
            else:
                Utilities.rtk_error(_(u"To calculate the growth potential "
                                      u"MTBF, you must provide the following "
                                      u"inputs with values greater than "
                                      u"zero:\n\n"
                                      u"1. Average MTBF over the first test "
                                      u"phase (MI): {0:f}\n"
                                      u"2. Management Strategy (MS): {1:f}\n"
                                      u"3. Fix Effectiveness Factor "
                                      u"(FEF): {2:f}\n\n").format(_mtbfa,
                                                                  _ms, _fef))
        elif index == 2:
            _alpha = self._testing_model.avg_growth
            _mtbfa = self._testing_model.lst_i_mtbfa[0]
            _mtbfg = self._testing_model.mtbfg
            _ttt = self._testing_model.ttt
            if _alpha > 0.0 and _mtbfa > 0.0 and _mtbfg > 0.0 and _ttt > 0.0:
                _t1 = CrowAMSAA.calculate_t1(_alpha, _mtbfa, _mtbfg, _ttt)
            else:
                Utilities.rtk_error(_(u"To calculate the minimum length of "
                                      u"the first phase, you must provide the "
                                      u"following inputs with values greater "
                                      u"than zero:\n\n"
                                      u"1. Average growth rate (GR): {0:f}\n"
                                      u"2. Average MTBF over the first "
                                      u"phase (MI): {1:f}\n"
                                      u"3. Final (goal) MTBF (MF): {2:f}\n"
                                      u"4. Total time on test "
                                      u"(TTT): {3:f}\n\n").format(_alpha,
                                                                  _mtbfa,
                                                                  _mtbfg,
                                                                  _ttt))
        elif index == 3:
            _alpha = self._testing_model.avg_growth
            _mtbfa = self._testing_model.lst_i_mtbfa[0]
            _mtbfg = self._testing_model.mtbfg
            _t1 = self._testing_model.lst_i_test_time[0]
            if _alpha > 0.0 and _mtbfa > 0.0 and _mtbfg > 0.0 and _t1 > 0.0:
                _ttt = CrowAMSAA.calculate_total_time(_alpha, _mtbfa, _mtbfg,
                                                      _t1)
            else:
                Utilities.rtk_error(_(u"To calculate the minimum total test "
                                      u"time required to achieve the goal "
                                      u"MTBF, you must provide the following "
                                      u"inputs with values greater than "
                                      u"zero:\n\n"
                                      u"1. Average growth rate (GR): {0:f}\n"
                                      u"2. Average MTBF of the first "
                                      u"phase (MI): {1:f}\n"
                                      u"3. Final (goal) MTBF (MF): {2:f}\n"
                                      u"4. Length of first test phase "
                                      u"(t1): {3:f}\n\n").format(_alpha,
                                                                 _mtbfa,
                                                                 _mtbfg, _t1))
        elif index == 4:
            _mtbfa = self._testing_model.lst_i_mtbfa[0]
            _mtbfg = self._testing_model.mtbfg
            _ttt = self._testing_model.ttt
            _t1 = self._testing_model.lst_i_test_time[0]
            if _mtbfa > 0.0 and _mtbfg > 0.0 and _ttt > 0.0 and _t1 > 0.0:
                _alpha = CrowAMSAA.calculate_growth_rate(_mtbfa, _mtbfg, _ttt,
                                                         _t1)
            else:
                Utilities.rtk_error(_(u"To calculate the minimum required "
                                      u"growth rate to achieve the goal MTBF, "
                                      u"you must provide the following inputs "
                                      u"with values greater than zero:\n\n"
                                      u"1. Average MTBF over the first test "
                                      u"phase (MI): {0:f}\n"
                                      u"2. Final (goal) MTBF (MF): {1:f}\n"
                                      u"3. Total time on test (TTT): {2:f}\n"
                                      u"4. Length of the first test phase "
                                      u"(t1): {3:f}\n\n").format(_mtbfa,
                                                                 _mtbfg,
                                                                 _ttt, _t1))
        # elif index == 5:
            # _fef = SPLAN.calculate_fef(_mtbfa, _ms, _fef)
        elif index == 6:
            _fef = self._testing_model.avg_fef
            _mtbfa = self._testing_model.lst_i_mtbfa[0]
            _mtbfgp = self._testing_model.mtbfgp
            if _fef > 0.0 and _mtbfa > 0.0 and _mtbfgp > 0.0:
                _ms = SPLAN.calculate_management_strategy(_fef, _mtbfa,
                                                          _mtbfgp)
            else:
                Utilities.rtk_error(_(u"To calculate the minimum required "
                                      u"management strategy to achiave the "
                                      u"goal MTBF, you must provide the "
                                      u"following inputs with values greater "
                                      u"than zero:\n\n"
                                      u"1. Fix Effectiveness Factor "
                                      u"(FEF): {0:f}\n"
                                      u"2. Average MTBF over the first test "
                                      u"phase (MI): {1:f}\n"
                                      u"3. Growth Potential MTBF "
                                      u"(MGP): {2:f}\n\n").format(_fef, _mtbfa,
                                                                  _mtbfgp))
        elif index == 7:
            _ttt = self._testing_model.ttt
            _ms = self._testing_model.avg_ms
            _mtbfa = self._testing_model.lst_i_mtbfa[0]
            if _ttt > 0.0 and _ms > 0.0 and _mtbfa > 0.0:
                _prob = SPLAN.calculate_probability(_ttt, _ms, _mtbfa)
            else:
                Utilities.rtk_error(_(u"To calculate the probability of "
                                      u"observing a failure during the first "
                                      u"test phase, you must provide the "
                                      u"following inputs with values greater "
                                      u"than zero:\n\n"
                                      u"1. Total time on test (TTT): {0:f}\n"
                                      u"2. Management strategy (MS): {1:f}\n"
                                      u"3. Average MTBF over the first test "
                                      u"phase (MI): {3:f}\n\n").format(_ttt,
                                                                       _ms,
                                                                       _mtbfa))
        elif index == 8:
            _test_id = self._testing_model.test_id
            _mtbf = self.optMTBF.get_active()
            (_ideal, _plan) = self.dtcGrowth.request_calculate(_test_id, _mtbf)
            self._load_plot(None, _ideal, _plan)

            # Update the RG plan details.
            _model = self._listview.tvwRGTestPlan.get_model()
            _row = _model.get_iter_root()
            while _row is not None:
                _phase = _model.get_value(_row, 0)
                _mtbfi = self._testing_model.lst_p_mtbfi[_phase - 1]
                _mtbfa = self._testing_model.lst_p_mtbfa[_phase - 1]
                _mtbff = self._testing_model.lst_p_mtbff[_phase - 1]

                _model.set_value(_row, 10, _mtbfi)
                _model.set_value(_row, 11, _mtbfa)
                _model.set_value(_row, 12, _mtbff)
                _row = _model.iter_next(_row)
        elif index == 9:
            self.dtcGrowth.save_test(self._testing_model.test_id)

        button.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_combo_changed(self, combo, index):
        """
        Method to respond to gtk.ComboBox() 'changed' signals.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called the function.
        :param int index: the position in the Testing class gtk.TreeModel()
                          associated with the data from the calling combobox.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        combo.handler_block(self._lst_handler_id[index])

        if index == 10:                      # Planning Model
            self._testing_model.rg_plan_model = combo.get_active()
        elif index == 11:                    # Assessment Model
            self._testing_model.rg_assess_model = combo.get_active()

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):     # pylint: disable=R0912
        """
        Method to respond to gtk.Entry() 'focus_out' signals and call the
        correct function or method, passing any parameters as needed.

        :param gtk.Entry entry: the gtk.Entry() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Entry() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """
# TODO: Re-write Planning._on_focus_out; current McCabe Complexity metric=12.
        entry.handler_block(self._lst_handler_id[index])

        # Get the gtk.TreeModel() of the RG plan details and the root (first
        # phase) gtk.TreeIter().
        _model = self._listview.tvwRGTestPlan.get_model()
        _row = _model.get_iter_root()

        if index == 12:                     # Number of phases
            self._testing_model.num_phases = float(entry.get_text())
        elif index == 14:                   # Initial average MTBF
            _mtbfa = float(entry.get_text())
            self._testing_model.lst_i_mtbfa[0] = _mtbfa
            _model.set_value(_row, 6, _mtbfa)
        elif index == 15:                   # Goal MTBF
            _n_phases = self._testing_model.n_phases
            _mtbfg = float(entry.get_text())
            self._testing_model.mtbfg = _mtbfg
            self._testing_model.lst_i_mtbff[_n_phases - 1] = _mtbfg
        elif index == 16:                   # Technical requirement
            self._testing_model.tr = float(entry.get_text())
        elif index == 17:                   # Growth potential MTBF
            self._testing_model.mtbfgp = float(entry.get_text())
        elif index == 18:                   # Length of first test phase
            _t1 = float(entry.get_text())
            self._testing_model.lst_p_test_time[0] = _t1
            _model.set_value(_row, 3, _t1)
        elif index == 19:                   # Total time on test
            self._testing_model.ttt = float(entry.get_text())
        elif index == 10:                   # Average program growth rate
            self._testing_model.avg_growth = float(entry.get_text())
        elif index == 21:                   # Average program FEF
            self._testing_model.avg_fef = float(entry.get_text())
        elif index == 22:                   # Average program management strategy
            self._testing_model.avg_ms = float(entry.get_text())
        elif index == 23:                   # Program probability
            self._testing_model.probability = float(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_spin_value_changed(self, button, index):
        """
        Method to respond to the gtk.SpinButton() 'value-changed' signals.

        :param gtk.SpinButton button: the gtk.SpinButton() that called this
                                      method
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.SpinButton() that
                          called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        button.handler_block(self._lst_handler_id[index])

        _n_phases = int(self.spnNumPhases.get_value())
        _new_phases = _n_phases - self._testing_model.n_phases
        if _new_phases > 0:
            for i in range(_new_phases):
                _phase_id = self._testing_model.n_phases + i
                self.dtcGrowth.add_test_phase(self._testing_model.test_id,
                                              _phase_id)
                self._testing_model.lst_i_mtbfi.append(0.0)
                self._testing_model.lst_i_mtbff.append(0.0)
                self._testing_model.lst_i_mtbfa.append(0.0)
                self._testing_model.lst_i_n_failures.append(0)
                self._testing_model.lst_p_growth_rate.append(0.0)
                self._testing_model.lst_p_ms.append(0.0)
                self._testing_model.lst_p_fef.append(0.0)
                self._testing_model.lst_p_prob.append(0.0)
                self._testing_model.lst_p_mtbfi.append(0.0)
                self._testing_model.lst_p_mtbff.append(0.0)
                self._testing_model.lst_p_mtbfa.append(0.0)
                self._testing_model.lst_p_test_time.append(0.0)
                self._testing_model.lst_p_n_failures.append(0)
                self._testing_model.lst_p_start_date.append(0)
                self._testing_model.lst_p_end_date.append(0)
                self._testing_model.lst_p_weeks.append(0.0)
                self._testing_model.lst_p_n_test_units.append(0)
                self._testing_model.lst_p_tpu.append(0.0)
                self._testing_model.lst_p_tpupw.append(0.0)
                self._testing_model.lst_o_growth_rate.append(0.0)
                self._testing_model.lst_o_ms.append(0.0)
                self._testing_model.lst_o_fef.append(0.0)
                self._testing_model.lst_o_mtbfi.append(0.0)
                self._testing_model.lst_o_mtbff.append(0.0)
                self._testing_model.lst_o_mtbfa.append(0.0)
                self._testing_model.lst_o_test_time.append(0.0)
                self._testing_model.lst_o_n_failures.append(0)

                self._listview.add_test_phase(_phase_id + 1)

        elif _new_phases < 0:
            for i in range(abs(_new_phases)):
                _phase_id = self._testing_model.n_phases - (i + 1)
                self.dtcGrowth.delete_test_phase(self._testing_model.test_id,
                                                 _phase_id)
                self._testing_model.lst_i_mtbfi.pop(_phase_id)
                self._testing_model.lst_i_mtbff.pop(_phase_id)
                self._testing_model.lst_i_mtbfa.pop(_phase_id)
                self._testing_model.lst_i_n_failures.pop(_phase_id)
                self._testing_model.lst_p_growth_rate.pop(_phase_id)
                self._testing_model.lst_p_ms.pop(_phase_id)
                self._testing_model.lst_p_fef.pop(_phase_id)
                self._testing_model.lst_p_prob.pop(_phase_id)
                self._testing_model.lst_p_mtbfi.pop(_phase_id)
                self._testing_model.lst_p_mtbff.pop(_phase_id)
                self._testing_model.lst_p_mtbfa.pop(_phase_id)
                self._testing_model.lst_p_test_time.pop(_phase_id)
                self._testing_model.lst_p_n_failures.pop(_phase_id)
                self._testing_model.lst_p_start_date.pop(_phase_id)
                self._testing_model.lst_p_end_date.pop(_phase_id)
                self._testing_model.lst_p_weeks.pop(_phase_id)
                self._testing_model.lst_p_n_test_units.pop(_phase_id)
                self._testing_model.lst_p_tpu.pop(_phase_id)
                self._testing_model.lst_p_tpupw.pop(_phase_id)
                self._testing_model.lst_o_growth_rate.pop(_phase_id)
                self._testing_model.lst_o_ms.pop(_phase_id)
                self._testing_model.lst_o_fef.pop(_phase_id)
                self._testing_model.lst_o_mtbfi.pop(_phase_id)
                self._testing_model.lst_o_mtbff.pop(_phase_id)
                self._testing_model.lst_o_mtbfa.pop(_phase_id)
                self._testing_model.lst_o_test_time.pop(_phase_id)
                self._testing_model.lst_o_n_failures.pop(_phase_id)

                self._listview.delete_test_phase(_phase_id + 1)

        self._testing_model.n_phases = _n_phases

        button.handler_unblock(self._lst_handler_id[index])

        return False


class Feasibility(gtk.HPaned):              # pylint: disable=R0902, R0904
    """
    The Work Book view displays all the attributes for the selected Reliability
    Growth Test Plan feasibility.  The attributes of a Reliability Growth Test
    Feasibility Work Book view are:

    :ivar list _lst_handler_id: default value: []

    :ivar _testing_model: the :py:class:`rtk.testing.growth.Growth.Model`
    :ivar dtcGrowth: the :py:class:`rtk.testing.growth.Growth.Growth`
    :ivar axAxisOC:
    :ivar gtk.CheckButton chkMIMGP:
    :ivar gtk.CheckButton chkFEF:
    :ivar gtk.CheckButton chkMGMGP:
    :ivar gtk.CheckButton chkGR:
    :ivar figFigureOC:
    :ivar gtk.Frame fraTestRisk:
    :ivar gtk.Frame fraTestFeasibility:
    :ivar gtk.Frame fraOCCurve:
    :ivar gtk.Label lblMIMGP:
    :ivar gtk.Label lblFEF:
    :ivar gtk.Label lblMGMGP:
    :ivar gtk.Label lblGR:
    :ivar pltPlotOC:
    :ivar gtk.ScrolledWindow scwTestFeasibility:
    :ivar gtk.TreeView tvwTestFeasibility:
    :ivar gtk.Entry txtMIMGP:
    :ivar gtk.Entry txtFEF:
    :ivar gtk.Entry txtMGMGP:
    :ivar gtk.Entry txtGR:
    """

    def __init__(self, controller, listbook):
        """
        Method to initialize the Work Book view for the Reliability Growth Test
        Feasibility.

        :param controller: the :py:class:`rtk.testing.growth.Growth.Growth`
                           data controller.
        :param listbook: the :py:class:`rtk.testing.ListBook` associated with
                         this view.
        """

        gtk.HPaned.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._feasibility = [0.0, 0.0, -1, -1]
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self.dtcGrowth = controller
        self._listview = listbook
        self._testing_model = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.btnCalculate = Widgets.make_button(width=35, image='calculate')
        self.btnSave = Widgets.make_button(width=35, image='save')

        self.chkMIMGP = Widgets.make_check_button(label=_(u"Acceptable "
                                                          u"MTBF<sub>I</sub> "
                                                          u"/ MTBF<sub>GP"
                                                          u"</sub>."))
        self.chkFEF = Widgets.make_check_button(label=_(u"Acceptable average "
                                                        u"fix effectiveness "
                                                        u"factor (FEF)."))
        self.chkMGMGP = Widgets.make_check_button(label=_(u"Acceptable "
                                                          u"MTBF<sub>G</sub> "
                                                          u"/ MTBF<sub>GP"
                                                          u"</sub>."))
        self.chkGR = Widgets.make_check_button(label=_(u"Acceptable "
                                                       u"average growth "
                                                       u"rate."))

        self.figFigureOC = Figure()

        self.lblMIMGP = Widgets.make_label("", width=150)
        self.lblFEF = Widgets.make_label("", width=150)
        self.lblMGMGP = Widgets.make_label("", width=150)
        self.lblGR = Widgets.make_label("", width=150)

        self.pltPlotOC = FigureCanvas(self.figFigureOC)

        self.axAxisOC = self.figFigureOC.add_subplot(111)

        self.txtMIMGP = Widgets.make_entry(width=75)
        self.txtFEF = Widgets.make_entry(width=75)
        self.txtMGMGP = Widgets.make_entry(width=75)
        self.txtGR = Widgets.make_entry(width=75)

        # Set tooltips for gtk.Widgets().
        self.btnCalculate.set_tooltip_text(_(u"Calculate the feasibility of "
                                             u"the planned test."))
        self.btnSave.set_tooltip_text(_(u"Saves changes to the test "
                                        u"feasibility assessment."))

        # Connect gtk.Widget() signals to callback methods.
        self._lst_handler_id.append(
            self.btnCalculate.connect('button-release-event',
                                      self._on_button_clicked, 0))
        self._lst_handler_id.append(
            self.btnSave.connect('button-release-event',
                                 self._on_button_clicked, 1))

        self.show_all()

    def create_page(self):
        """
        Method to create the page for displaying the Reliability Growth Test
        Phase details for the selected Growth Test.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HBox()
        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        _hbox.pack_start(_bbox, False, True)

        _bbox.pack_start(self.btnCalculate, False, False)
        _bbox.pack_start(self.btnSave, False, False)

        _fixed = gtk.Fixed()

        _frame = Widgets.make_frame(_(u"Program Planning Inputs"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_fixed)

        _hbox.pack_end(_frame)

        self.pack1(_hbox, False, True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the labels.
        _labels = [_(u"MTBF<sub>I</sub> / MTBF<sub>G</sub> should fall in "
                     u"the range of 0.15 - 0.47.  On average this ratio is "
                     u"0.30."),
                   _(u"Program MTBF<sub>I</sub> / MTBF<sub>G</sub>:"), "", "",
                   _(u"MTBF<sub>G</sub> / MTBF<sub>G</sub> should fall in "
                     u"the range of 0.60 - 0.80."),
                   _(u"Program MTBF<sub>G</sub> / MTBF<sub>GP</sub>:"), "", "",
                   _(u"Average growth rate should fall in the range of "
                     u"0.23 - 0.64."),
                   _(u"Program average growth rate:"), "", "",
                   _(u"The Fix Effectiveness Factor should fall in the range "
                     u"of 0.55 - 0.85.  On average the FEF is 0.70."),
                   _(u"Program average FEF:"), "", ""]

        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5, 30)
        _x_pos += 40

        # Set the tooltips for the gtk.Widget().
        self.chkMIMGP.set_tooltip_text(_(u"Indicates whether or not the "
                                         u"initial MTBF to goal MTBF ratio "
                                         u"is within reasonable limits."))
        self.chkFEF.set_tooltip_text(_(u"Indicates whether or not the average "
                                       u"fix effectiveness factor (FEF) is "
                                       u"within reasonable limits."))
        self.chkMGMGP.set_tooltip_text(_(u"Indicates whether or not the goal "
                                         u"MTBF to mature MTBF ratio is "
                                         u"within reasonable limits."))
        self.chkGR.set_tooltip_text(_(u"Indicates whether or not the average "
                                      u"growth rate is within reasonable "
                                      u"limits."))
        self.pltPlotOC.set_tooltip_text(_(u"Displays the Reliability Growth "
                                          u"Plan Operating Characteristic "
                                          u"(OC) curve."))

        # Position the gtk.Widget() on the page.
        _fixed.put(self.txtMIMGP, _x_pos, _y_pos[1])
        _fixed.put(self.lblMIMGP, _x_pos, _y_pos[2])
        _fixed.put(self.chkMIMGP, 5, _y_pos[3])

        _fixed.put(self.txtMGMGP, _x_pos, _y_pos[5])
        _fixed.put(self.lblMGMGP, _x_pos, _y_pos[6])
        _fixed.put(self.chkMGMGP, 5, _y_pos[7])

        _fixed.put(self.txtGR, _x_pos, _y_pos[9])
        _fixed.put(self.lblGR, _x_pos, _y_pos[10])
        _fixed.put(self.chkGR, 5, _y_pos[11])

        _fixed.put(self.txtFEF, _x_pos, _y_pos[13])
        _fixed.put(self.lblFEF, _x_pos, _y_pos[14])
        _fixed.put(self.chkFEF, 5, _y_pos[15])

        _vbox = gtk.VBox()

        _fixed = gtk.Fixed()
        _vbox.pack_start(_fixed, False, True)

        # _frame = Widgets.make_frame(label=_(u"Program Planning Curves"))
        # _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        # _frame.add(self.pltPlotOC)
        # _frame.show_all()

        # _vbox.pack_start(_frame, True, True)

        self.pack2(_vbox, True, False)

        # Connect gtk.Widget() signals to callback functions.
        self.pltPlotOC.mpl_connect('button_press_event', _expand_plot)

        return False

    def load_page(self, model):
        """
        Method to load the Reliability Growth Test Feasibility gtk.Notebook()
        page.

        :param model: the :py:class:`rtk.testing.Testing.Model` to load.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """
# TODO: Re-write Feasibility._load_page; current McCabe Complexity metric=21.
        self._testing_model = model

        fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'

        _low = u"<span foreground='#00CC00'>Low Risk</span>"
        _medium = u"<span foreground='#E6E639'>Medium Risk</span>"
        _high = u"<span foreground='red'>High Risk</span>"

        # Load the individual widgets.
        self.txtMIMGP.set_text(str(fmt.format(self._feasibility[0])))

        if self._feasibility[0] >= 0.15 and self._feasibility[0] <= 0.47:
            self.chkMIMGP.set_active(True)
        else:
            self.chkMIMGP.set_active(False)

        if self._feasibility[0] >= 0.35:
            self.lblMIMGP.set_markup(_low)
        elif self._feasibility[0] < 0.35 and self._feasibility[0] >= 0.2:
            self.lblMIMGP.set_markup(_medium)
        else:
            self.lblMIMGP.set_markup(_high)

        self.txtMGMGP.set_text(str(fmt.format(self._feasibility[1])))
        if self._feasibility[1] >= 0.6 and self._feasibility[1] <= 0.8:
            self.chkMGMGP.set_active(True)
        else:
            self.chkMGMGP.set_active(False)

        if self._feasibility[1] <= 0.7:
            self.lblMGMGP.set_markup(_low)
        elif self._feasibility[1] > 0.7 and self._feasibility[1] <= 0.8:
            self.lblMGMGP.set_markup(_medium)
        else:
            self.lblMGMGP.set_markup(_high)

        # Program average growth rate.
        self.txtGR.set_text(str(model.avg_growth))
        if model.avg_growth >= 0.23 and model.avg_growth <= 0.64:
            self.chkGR.set_active(True)
        else:
            self.chkGR.set_active(False)

        if model.avg_growth < 0.35:
            self.lblGR.set_markup(_low)
        elif model.avg_growth >= 0.35 and model.avg_growth <= 0.55:
            self.lblGR.set_markup(_medium)
        else:
            self.lblGR.set_markup(_high)

        # Program average fix effectiveness factor.
        self.txtFEF.set_text(str(fmt.format(model.avg_fef)))
        if model.avg_fef >= 0.55 and model.avg_fef <= 0.85:
            self.chkFEF.set_active(True)
        else:
            self.chkFEF.set_active(False)

        if model.avg_fef <= 0.7:
            self.lblFEF.set_markup(_low)
        elif model.avg_fef > 0.7 and model.avg_fef <= 0.8:
            self.lblFEF.set_markup(_medium)
        else:
            self.lblFEF.set_markup(_high)

        # (Re-)load the List Book.
        self._listview.load(self._testing_model)

        return False

    def _on_button_clicked(self, button, __event, index):
        """
        Method to respond to gtk.Button() 'clicked' signals and call the
        correct function or method, passing any parameters as needed.

        :param gtk.Button button: the gtk.Button() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() raised by the
                                      gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        button.handler_block(self._lst_handler_id[index])

        if index == 0:
            self._feasibility = self._testing_model.assess_plan_feasibility()

            if self._feasibility[2] > -1:
                Utilities.rtk_warning(_(u"You have not entered the number of "
                                        u"test units for test phase {0:d}.  "
                                        u"Unable to calculate the average "
                                        u"test time per test unit.  Please "
                                        u"enter the number of test units for "
                                        u"test phase {1:d} and try "
                                        u"again.").format(self._feasibility[2],
                                                          self._feasibility[2]))
            if self._feasibility[3] > -1:
                Utilities.rtk_warning(_(u"Start date and end date are the "
                                        u"same for test phase {0:d}.  Unable "
                                        u"to calculate the average test time "
                                        u"per week for a test unit.  Please "
                                        u"correct one or both dates and try "
                                        u"again.").format(self._feasibility[3]))

            self.load_page(self._testing_model)

        elif index == 1:
            self.dtcGrowth.save_test(self._testing_model.test_id)

        button.handler_unblock(self._lst_handler_id[index])

        return False


class Assessment(gtk.HPaned):               # pylint: disable=R0902, R0904
    """
    The Work Book view displays all the attributes for the selected Reliability
    Growth Test Plan assessment.  The attributes of a Reliability Growth Test
    Assessment Work Book view are:

    :ivar list _lst_handler_id: default value: []

    :ivar :py:class:`rtk.testing.growth.Model` _testing_model: default value: None
    :ivar float _cvm_critical: default value: 0.0
    :ivar :py:class:`rtk.testing.growth.Growth` dtcGrowth:

    """

    def __init__(self, controller, listbook):
        """
        Method to initialize the Work Book view for the Reliability Growth Test
        Assessment.

        :param controller: the :py:class:`rtk.testing.growth.Growth.Growth`
                           data controller.
        :param listbook: the :py:class:`rtk.testing.ListBook` associated with
                         this view.
        """

        gtk.HPaned.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self.dtcGrowth = controller
        self._listview = listbook
        self._testing_model = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.btnAssess = Widgets.make_button(width=35, image='calculate')
        self.btnSave = Widgets.make_button(width=35, image='save')

        self.lblTrend = Widgets.make_label("", width=-1)
        self.lblGoF = Widgets.make_label("", width=-1)

        self.optIndividual = gtk.RadioButton(label=_(u"Individual Failure "
                                                     u"Time Data"))
        self.optIndividual.set_name('individual')
        self.optIndividual.set_active(True)

        self.optGrouped = gtk.RadioButton(group=self.optIndividual,
                                          label=_(u"Grouped Failure Time "
                                                  u"Data"))
        self.optGrouped.set_name('grouped')

        self.optMTBF = gtk.RadioButton(label=_(u"Display results as MTBF"))

        self.optMTBF.set_name('mtbf')
        self.optMTBF.set_active(True)

        self.optFailureIntensity = gtk.RadioButton(group=self.optMTBF,
                                                   label=_(u"Display results "
                                                           u"as failure "
                                                           u"intensity"))
        self.optFailureIntensity.set_name('failureintensity')

        self.optLinear = gtk.RadioButton(label=_(u"Use Linear Scales"))
        self.optLinear.set_name('linear')
        self.optLinear.set_active(True)
        self.optLogarithmic = gtk.RadioButton(group=self.optLinear,
                                              label=_(u"Use Logarithmic "
                                                      u"Scales"))
        self.optLogarithmic.set_name('log')

        self.spnConfidence = gtk.SpinButton()

        self.txtCumTestTime = Widgets.make_entry(width=100, editable=False)
        self.txtCumFailures = Widgets.make_entry(width=100, editable=False)
        self.txtScale = Widgets.make_entry(width=100, editable=False)
        self.txtScalell = Widgets.make_entry(width=100, editable=False)
        self.txtScaleul = Widgets.make_entry(width=100, editable=False)
        self.txtShape = Widgets.make_entry(width=100, editable=False)
        self.txtShapell = Widgets.make_entry(width=100, editable=False)
        self.txtShapeul = Widgets.make_entry(width=100, editable=False)
        self.txtGRActual = Widgets.make_entry(width=100, editable=False)
        self.txtGRActualll = Widgets.make_entry(width=100, editable=False)
        self.txtGRActualul = Widgets.make_entry(width=100, editable=False)
        self.txtRhoInst = Widgets.make_entry(width=100, editable=False)
        self.txtRhoInstll = Widgets.make_entry(width=100, editable=False)
        self.txtRhoInstul = Widgets.make_entry(width=100, editable=False)
        self.txtRhoC = Widgets.make_entry(width=100, editable=False)
        self.txtRhoCll = Widgets.make_entry(width=100, editable=False)
        self.txtRhoCul = Widgets.make_entry(width=100, editable=False)
        self.txtMTBFInst = Widgets.make_entry(width=100, editable=False)
        self.txtMTBFInstll = Widgets.make_entry(width=100, editable=False)
        self.txtMTBFInstul = Widgets.make_entry(width=100, editable=False)
        self.txtMTBFC = Widgets.make_entry(width=100, editable=False)
        self.txtMTBFCll = Widgets.make_entry(width=100, editable=False)
        self.txtMTBFCul = Widgets.make_entry(width=100, editable=False)
        self.txtTrendCV = Widgets.make_entry(width=100, editable=False)
        self.txtTrendModel = Widgets.make_entry(width=100, editable=False)
        self.txtGoFCV = Widgets.make_entry(width=100, editable=False)
        self.txtGoFModel = Widgets.make_entry(width=100, editable=False)
        self.txtTestTermTime = Widgets.make_entry(width=100)

        self.figFigure1 = Figure()
        self.pltPlot1 = FigureCanvas(self.figFigure1)
        self.axAxis1 = self.figFigure1.add_subplot(111)

        # Set gtk.Widget() tooltip text.
        self.btnAssess.set_tooltip_text(_(u"Assesses the current reliability "
                                          u"of the system under test."))
        self.optIndividual.set_tooltip_text(_(u"Estimate parameters based on "
                                              u"individual failure times."))
        self.optGrouped.set_tooltip_text(_(u"Estimate parameters based on "
                                           u"grouped failures times."))
        self.spnConfidence.set_tooltip_text(_(u"Displays the confidence level "
                                              u"level to use for failure "
                                              u"rate/MTBF bounds and goodness "
                                              u"of fit (GoF) tests."))
        self.txtTestTermTime.set_tooltip_text(_(u"For time terminated "
                                                u"(Type II) tests, enter the "
                                                u"test termination time."))
        self.txtCumTestTime.set_tooltip_text(_(u"Displays the cumulative test "
                                               u"time to date for the "
                                               u"selected test."))
        self.txtCumFailures.set_tooltip_text(_(u"Displays the cumulative "
                                               u"number of failures to date "
                                               u"for the selected test."))
        self.txtScale.set_tooltip_text(_(u"Displays the reliability growth "
                                         u"model estimated scale parameter."))
        self.txtScalell.set_tooltip_text(_(u"Displays the lower bound on the "
                                           u"reliability growth model scale "
                                           u"parameter."))
        self.txtScaleul.set_tooltip_text(_(u"Displays the upper bound on the "
                                           u"reliability growth model scale "
                                           u"parameter."))
        self.txtShape.set_tooltip_text(_(u"Displays the reliability growth "
                                         u"model estimated shape parameter."))
        self.txtShapell.set_tooltip_text(_(u"Displays the lower bound on the "
                                           u"reliability growth model shape "
                                           u"parameter."))
        self.txtShapeul.set_tooltip_text(_(u"Displays the upper bound on the "
                                           u"reliability growth model shape "
                                           u"parameter."))
        self.txtGRActual.set_tooltip_text(_(u"Displays the average growth "
                                            u"rate over the reliability "
                                            u"growth program to date."))
        self.txtGRActualll.set_tooltip_text(_(u"Displays the lower bound "
                                              u"on the average growth "
                                              u"rate over the reliability "
                                              u"growth program to date."))
        self.txtGRActualul.set_tooltip_text(_(u"Displays the upper bound on "
                                              u"the average growth rate over "
                                              u"the reliability growth "
                                              u"program to date."))
        self.txtRhoInst.set_tooltip_text(_(u"Displays the currently assessed "
                                           u"instantaneous failure intensity "
                                           u"(failure rate) of the item under "
                                           u"test."))
        self.txtRhoInstll.set_tooltip_text(_(u"Displays the lower bound on "
                                             u"the instantaneous failure "
                                             u"intensity (failure rate) of "
                                             u"the item under test."))
        self.txtRhoInstul.set_tooltip_text(_(u"Displays the upper bound on "
                                             u"the instantaneous failure "
                                             u"intensity (failure rate) of "
                                             u"the item under test."))
        self.txtRhoC.set_tooltip_text(_(u"Displays the currently assessed "
                                        u"cumulative failure intensity "
                                        u"(failure rate) of the item under "
                                        u"test."))
        self.txtRhoCll.set_tooltip_text(_(u"Displays the lower bound on the "
                                          u"cumulative failure intensity "
                                          u"(failure rate) of the item under "
                                          u"test."))
        self.txtRhoCul.set_tooltip_text(_(u"Displays the upper bound on the "
                                          u"cumulative failure intensity "
                                          u"(failure rate) of the item under "
                                          u"test."))
        self.txtMTBFInst.set_tooltip_text(_(u"Displays the currently assessed "
                                            u"instantaneous MTBF of the item "
                                            u"under test."))
        self.txtMTBFInstll.set_tooltip_text(_(u"Displays the lower bound on "
                                              u"the instantaneous MTBF of the "
                                              u"item under test."))
        self.txtMTBFInstul.set_tooltip_text(_(u"Displays the upper bound on "
                                              u"the instantaneous MTBF of the "
                                              u"item under test."))
        self.txtMTBFC.set_tooltip_text(_(u"Displays the currently assessed "
                                         u"cumulative MTBF of the item under "
                                         u"test."))
        self.txtMTBFCll.set_tooltip_text(_(u"Displays the lower bound on the "
                                           u"cumulative MTBF of the item "
                                           u"under test."))
        self.txtMTBFCul.set_tooltip_text(_(u"Displays the upper bound on the "
                                           u"cumulative MTBF of the item "
                                           u"under test."))
        self.txtTrendCV.set_tooltip_text(_(u"Displays the critical value for "
                                           u"testing the hypothesis of "
                                           u"exponentially distributed "
                                           u"failure times (i.e., no "
                                           u"growth)."))
        self.txtTrendModel.set_tooltip_text(_(u"Displays the test statistic "
                                              u"for assessing exponentially "
                                              u"distributed failure times "
                                              u"(i.e., no growth).  If this "
                                              u"value is greater than the "
                                              u"critical value, the data "
                                              u"suggests failure times are "
                                              u"exponentially distributed "
                                              u"(i.e., there is growth)."))
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

        self.optMTBF.set_tooltip_text(_(u"If selected, test results will be "
                                        u"displayed as MTBF.  This is the "
                                        u"default."))
        self.optFailureIntensity.set_tooltip_text(_(u"If selected, test "
                                                    u"results will be "
                                                    u"displayed as failure "
                                                    u"intensity (failure "
                                                    u"rate)."))
        self.optLinear.set_tooltip_text(_(u"Select this option to use linear "
                                          u"scales on the reliability growth "
                                          u"plot."))
        self.optLogarithmic.set_tooltip_text(_(u"Select this option to use "
                                               u"logarithmic scales on the "
                                               u"reliability growth plot."))
        self.pltPlot1.set_tooltip_text(_(u"Displays the selected test plan "
                                         u"and observed results."))

        # Connect gtk.Widget() signals to callback methods and functions.
        self._lst_handler_id.append(
            self.btnAssess.connect('button-release-event',
                                   self._on_button_clicked, 0))
        self._lst_handler_id.append(
            self.btnSave.connect('button-release-event',
                                 self._on_button_clicked, 1))
        self._lst_handler_id.append(
            self.spnConfidence.connect('focus-out-event',
                                       self._on_focus_out, 2))
        self._lst_handler_id.append(
            self.txtTestTermTime.connect('focus-out-event',
                                         self._on_focus_out, 3))
        self._lst_handler_id.append(
            self.optIndividual.connect('toggled', self._on_toggled, 4))
        self._lst_handler_id.append(
            self.optGrouped.connect('toggled', self._on_toggled, 5))

        self.optMTBF.connect('toggled', self._load_plot)
        self.optFailureIntensity.connect('toggled', self._load_plot)
        self.optLinear.connect('toggled', self._load_plot)
        self.optLogarithmic.connect('toggled', self._load_plot)

        self._lst_handler_id.append(
            self.spnConfidence.connect('value-changed',
                                       self._on_spin_value_changed, 6))

        self.pltPlot1.mpl_connect('button_press_event', _expand_plot)

        self.show_all()

    def create_page(self):                  # pylint: disable=R0914
        """
        Method to create the page for displaying the Reliability Growth Test
        assessment results for the selected Growth Test.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        _hbox.pack_start(_bbox, False, True)

        _bbox.pack_start(self.btnAssess, False, False)
        _bbox.pack_start(self.btnSave, False, False)

        _fixed = gtk.Fixed()

        _frame = Widgets.make_frame(_(u"Estimated Parameters"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_fixed)

        _hbox.pack_end(_frame)

        self.pack1(_hbox, False, True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the labels.
        _labels = [_(u"Cum. Test Time:"), _(u"Cum. Failures:"),
                   _(u"Confidence:"), _(u"Test Termination Time:")]
        (_x_max, _y_pos1) = Widgets.make_labels(_labels, _fixed, 5, 55)
        _labels = [_(u"Lambda:"), _(u"Beta:"), _(u"Observed Growth Rate:"),
                   _(u"Instantaneous Failure Rate:"),
                   _(u"Cumulative Failure Rate:"), _(u"Instantaneous MTBF:"),
                   _(u"Cumulative MTBF:")]
        (_x_pos, _y_pos2) = Widgets.make_labels(_labels, _fixed, 5,
                                                _y_pos1[1] + 140)
        _x_pos = max(_x_max, _x_pos) + 40
        _y_pos = _y_pos1 + _y_pos2

        # Position the gtk.Widget() on the page.
        # Place the widgets used to describe the format of the dataset.
        _fixed.put(self.optIndividual, 5, 5)
        _fixed.put(self.optGrouped, 305, 5)

        _adjustment = gtk.Adjustment(75.0, 50.0, 100.0, 0.5, 0, 0)
        self.spnConfidence.set_adjustment(_adjustment)
        self.spnConfidence.set_digits(int(Configuration.PLACES))

        # Place the widgets use to display the numerical results of the test
        # data assessment.
        _fixed.put(self.txtCumTestTime, _x_pos, _y_pos[0])
        _fixed.put(self.txtCumFailures, _x_pos, _y_pos[1])
        _fixed.put(self.spnConfidence, _x_pos, _y_pos[2])
        _fixed.put(self.txtTestTermTime, _x_pos, _y_pos[3])

        _label = Widgets.make_label(_(u"Lower\nBound"), height=-1, wrap=True,
                                    justify=gtk.JUSTIFY_CENTER)
        _fixed.put(_label, _x_pos + 5, _y_pos[3] + 35)
        _label = Widgets.make_label(_(u"\nEstimate"), height=-1, wrap=True,
                                    justify=gtk.JUSTIFY_CENTER)
        _fixed.put(_label, _x_pos + 105, _y_pos[3] + 35)
        _label = Widgets.make_label(_(u"Upper\nBound"), height=-1, wrap=True,
                                    justify=gtk.JUSTIFY_CENTER)
        _fixed.put(_label, _x_pos + 205, _y_pos[3] + 35)
        _fixed.put(self.txtScalell, _x_pos, _y_pos[4])
        _fixed.put(self.txtScale, _x_pos + 100, _y_pos[4])
        _fixed.put(self.txtScaleul, _x_pos + 200, _y_pos[4])
        _fixed.put(self.txtShapell, _x_pos, _y_pos[5])
        _fixed.put(self.txtShape, _x_pos + 100, _y_pos[5])
        _fixed.put(self.txtShapeul, _x_pos + 200, _y_pos[5])
        _fixed.put(self.txtGRActualll, _x_pos, _y_pos[6])
        _fixed.put(self.txtGRActual, _x_pos + 100, _y_pos[6])
        _fixed.put(self.txtGRActualul, _x_pos + 200, _y_pos[6])
        _fixed.put(self.txtRhoInstll, _x_pos, _y_pos[7])
        _fixed.put(self.txtRhoInst, _x_pos + 100, _y_pos[7])
        _fixed.put(self.txtRhoInstul, _x_pos + 200, _y_pos[7])
        _fixed.put(self.txtRhoCll, _x_pos, _y_pos[8])
        _fixed.put(self.txtRhoC, _x_pos + 100, _y_pos[8])
        _fixed.put(self.txtRhoCul, _x_pos + 200, _y_pos[8])
        _fixed.put(self.txtMTBFInstll, _x_pos, _y_pos[9])
        _fixed.put(self.txtMTBFInst, _x_pos + 100, _y_pos[9])
        _fixed.put(self.txtMTBFInstul, _x_pos + 200, _y_pos[9])
        _fixed.put(self.txtMTBFCll, _x_pos, _y_pos[10])
        _fixed.put(self.txtMTBFC, _x_pos + 100, _y_pos[10])
        _fixed.put(self.txtMTBFCul, _x_pos + 200, _y_pos[10])

        _label = Widgets.make_label(_(u"Statistical Test for Trend"))
        _fixed.put(_label, 5, _y_pos[10] + 40)
        self.lblTrend.set_markup(_(u"H<sub>o</sub>: Exponential Failure "
                                   u"Times (No Growth)"))
        _fixed.put(self.lblTrend, 5, _y_pos[10] + 75)
        _label = Widgets.make_label(_(u"Critical Value:"))
        _fixed.put(_label, 5, _y_pos[10] + 110)
        _fixed.put(self.txtTrendCV, _x_pos, _y_pos[10] + 110)
        _label = Widgets.make_label(_(u"Test Statistic:"))
        _fixed.put(_label, 5, _y_pos[10] + 140)
        _fixed.put(self.txtTrendModel, _x_pos, _y_pos[10] + 140)

        _label = Widgets.make_label(_(u"Statistical Test for Goodness of Fit"),
                                    width=-1)
        _fixed.put(_label, _x_pos + 205, _y_pos[10] + 40)
        self.lblGoF.set_markup(_(u"H<sub>o</sub>: Data Follows AMSAA Model"))
        _fixed.put(self.lblGoF, _x_pos + 205, _y_pos[10] + 75)
        _fixed.put(self.txtGoFCV, _x_pos + 205, _y_pos[10] + 110)
        _fixed.put(self.txtGoFModel, _x_pos + 205, _y_pos[10] + 140)

        # Place the widgets use to display the graphical results of the test
        # data assessment.
        _vbox = gtk.VBox()

        _fixed = gtk.Fixed()

        _vbox.pack_start(_fixed, False, True)

        _frame = Widgets.make_frame(label=_(u"Reliability Test Plot"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot1)
        _frame.show_all()

        _vbox.pack_start(_frame, True, True)

        self.pack2(_vbox, True, False)

        _fixed.put(self.optMTBF, 5, 5)
        _fixed.put(self.optFailureIntensity, 205, 5)
        _fixed.put(self.optLinear, 5, 40)
        _fixed.put(self.optLogarithmic, 205, 40)

        return False

    def load_page(self, model):
        """
        Method to load the Reliability Growth Test Assessment gtk.Notebook()
        page.

        :param model: the :py:class:`rtk.testing.Testing.Model` to load.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        self._testing_model = model

        fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'

        # If this is the initial load of the assessment, assess the test data.
        if len(self._testing_model.cum_mean) <= 1:
            self.dtcGrowth.request_assessment(self._testing_model.test_id)

        # Load the individual widgets.
        if model.grouped == 1:
            self.optGrouped.set_active(True)

        else:
            self.optIndividual.set_active(True)

        self.spnConfidence.set_value(float(model.confidence * 100.0))
        self.txtCumTestTime.set_text(str(model.cum_time))
        self.txtCumFailures.set_text(str(model.cum_failures))
        self.txtTestTermTime.set_text(str(model.test_termination_time))

        self.txtScalell.set_text(str(fmt.format(model.alpha_hat[0])))
        self.txtScale.set_text(str(fmt.format(model.alpha_hat[1])))
        self.txtScaleul.set_text(str(fmt.format(model.alpha_hat[2])))
        self.txtShapell.set_text(str(fmt.format(model.beta_hat[0])))
        self.txtShape.set_text(str(fmt.format(model.beta_hat[1])))
        self.txtShapeul.set_text(str(fmt.format(model.beta_hat[2])))
        self.txtGRActualll.set_text(str(fmt.format(
            model.lst_o_growth_rate[0])))
        self.txtGRActual.set_text(str(fmt.format(model.lst_o_growth_rate[1])))
        self.txtGRActualul.set_text(str(fmt.format(
            model.lst_o_growth_rate[2])))
        self.txtMTBFInstll.set_text(str(fmt.format(
            model.instantaneous_mean[-1][0])))
        self.txtMTBFInst.set_text(str(fmt.format(
            model.instantaneous_mean[-1][1])))
        self.txtMTBFInstul.set_text(str(fmt.format(
            model.instantaneous_mean[-1][2])))
        self.txtMTBFCll.set_text(str(fmt.format(model.cum_mean[-1][0])))
        self.txtMTBFC.set_text(str(fmt.format(model.cum_mean[-1][1])))
        self.txtMTBFCul.set_text(str(fmt.format(model.cum_mean[-1][2])))

        try:
            self.txtRhoInstll.set_text(str(
                fmt.format(1.0 / model.instantaneous_mean[-1][2])))
        except ZeroDivisionError:
            self.txtRhoInstll.set_text("0.0")

        try:
            self.txtRhoInst.set_text(str(
                fmt.format(1.0 / model.instantaneous_mean[-1][1])))
        except ZeroDivisionError:
            self.txtRhoInst.set_text("0.0")

        try:
            self.txtRhoInstul.set_text(str(
                fmt.format(1.0 / model.instantaneous_mean[-1][0])))
        except ZeroDivisionError:
            self.txtRhoInstul.set_text("0.0")

        try:
            self.txtRhoCll.set_text(str(
                fmt.format(1.0 / model.cum_mean[-1][2])))
        except ZeroDivisionError:
            self.txtRhoCll.set_text("0.0")

        try:
            self.txtRhoC.set_text(str(
                fmt.format(1.0 / model.cum_mean[-1][1])))
        except ZeroDivisionError:
            self.txtRhoC.set_text("0.0")

        try:
            self.txtRhoCul.set_text(str(
                fmt.format(1.0 / model.cum_mean[-1][0])))
        except ZeroDivisionError:
            self.txtRhoCul.set_text("0.0")

        self.txtTrendCV.set_text(str(fmt.format(model.chi2_critical_value[1])))
        self.txtTrendModel.set_text(str(fmt.format(model.chi_square)))
        if(self._testing_model.chi_square >
           self._testing_model.chi2_critical_value[1]):
            self.lblTrend.set_markup(_(u"H<sub>o</sub>: Exponential Failure "
                                       u"Times (No Growth)     "
                                       u"<span foreground='green'>"
                                       u"Reject</span>"))
        else:
            self.lblTrend.set_markup(_(u"H<sub>o</sub>: Exponential Failure "
                                       u"Times (No Growth)     "
                                       u"<span foreground='red'>"
                                       u"Fail to Reject</span>"))

        self.txtGoFCV.set_text(str(fmt.format(model.cvm_critical_value)))
        self.txtGoFModel.set_text(str(fmt.format(model.cramer_vonmises)))
        if(self._testing_model.cramer_vonmises <
           self._testing_model.cvm_critical_value):
            self.lblGoF.set_markup(_(u"H<sub>o</sub>: Data Follows AMSAA "
                                     u"Model     <span foreground='green'>"
                                     u"Fail to Reject</span>"))
        else:
            self.lblGoF.set_markup(_(u"H<sub>o</sub>: Data Follows AMSAA "
                                     u"Model     <span foreground='red'>"
                                     u"Reject</span>"))

        # Load the RG Assessment plot.
        self._load_plot()

        # (Re-)load the List Book.
        self._listview.load(self._testing_model)

        return False

    def _load_plot(self, __button=None, ideal=None, plan=None):    # pylint: disable=R0914
        """
        Method to load the Reliability Growth assessment plot.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# TODO: Re-write Assessment._load_plot; current McCabe Complexity metric=13.
        _log = False

        if(self._testing_model.ttt <= 0.0 and
           len(self._testing_model.dic_test_data.values()) > 0):
            self._testing_model.ttt = [x[3] for x in
                                       self._testing_model.dic_test_data.values()][-1]

        _times = [_t for _t in range(int(self._testing_model.ttt))]

        # If the ideal curve hasn't been calculated, then calculate it's
        # values.
        if ideal is None or ideal == []:
            ideal = self._testing_model.calculate_idealized_growth_curve()

        # If the planned curves haven't been calculated, then calculate their
        # values.
        if plan is None or plan == []:
            plan = self._testing_model.create_planned_values()

        _xlabel = _(u"Cumulative Test Time")
        if self.optMTBF.get_active():
            _targets = self._testing_model.lst_p_mtbfa
            _ylabel = _(u"Cumulative MTBF")

        elif self.optFailureIntensity.get_active():
            ideal = [1.0 / _mtbf for _mtbf in ideal]
            plan = [1.0 / _mtbf for _mtbf in plan]
            _targets = [1.0 / _mtbfa
                        for _mtbfa in self._testing_model.lst_p_mtbfa]
            _ylabel = _(u"Cumulative Failure Intensity")

        if self.optLogarithmic.get_active():
            _log = True

        # Retrieve the observed cumulative and instantaneous MTBF or failure
        # intensity values and bounds if there are any observed values.
        (_obs_times,
         _cumll,
         _cumpt,
         _cumul) = self._get_observed_values(self._testing_model.cum_mean)
        (_obs_times,
         _insll,
         _inspt,
         _insul) = self._get_observed_values(self._testing_model.instantaneous_mean)

        # Find the minimum and maximum y-value.
        try:
            #_y_max = max(max(_targets), max(_cumll), max(_cumpt), max(_cumul),
            #             max(_insll), max(_inspt), max(_insul), max(ideal),
            #             max(plan))
            _y_max = max(max(_targets), max(_cumpt), max(_inspt), max(ideal),
                         max(plan))
        except ValueError:
            _y_max = 0.0

        _lines = _plot_ideal(self.axAxis1, self.pltPlot1, _times,
                             [ideal, plan], self._testing_model.ttt, _y_max,
                             _xlabel, _ylabel, _log)

        # Add the target values to the plot.
        _l = _add_targets(self.axAxis1, _targets, self._testing_model.ttt)
        _lines.append(_l)

        _legend = [_(u"Idealized Growth Curve"), _(u"Planned Growth Curve"),
                   _(u"Target Values")]

        # Plot the observed cumulative values.
        if len(_obs_times) == len(_cumpt):
            _l = _plot_assessed(self.axAxis1, _obs_times,
                                [_cumll, _cumpt, _cumul])
            _legend.append(_(u"Observed Cumulative Values"))
            _lines.append(_l)

        if len(_obs_times) == len(_inspt):
            _l = _plot_assessed(self.axAxis1, _obs_times,
                                [_insll, _inspt, _insul], index=1)
            _legend.append(_(u"Observed Instantaneous Values"))
            _lines.append(_l)

        # Add the legend to the plot.
        _legend = tuple(_legend)
        _add_legend(self.axAxis1, _lines, _legend)

        self.pltPlot1.draw()

        return False

    def _get_observed_values(self, means):
        """
        Method to create lists of the point estimate of observed values, the
        alpha lower limit and alpha upper limit on observed values.

        :param list means: a list of the mean values to correct and split into
                           three lists.
        :return: (_obs_times, _obsll, _obspt, _obsul)
        :rtype: tuple of lists of floats
        """
# TODO: Re-write Assessment._get_observed_values; current McCabe Complexity metric=12.
        _obs_times = []

        # First update the left interval time using the previous record's right
        # interval value if the data is grouped.  Then create a list of
        # observed cumulative failure times to use when plotting the results.
        _f_time = 0.0
        _model = self._listview.tvwRGTestAssessment.get_model()
        _row = _model.get_iter_root()
        while _row is not None:
            _key = _model.get_value(_row, 0) - 1
            if self.optGrouped.get_active():
                self._testing_model.dic_test_data[_key][2] = _f_time
                _model.set_value(_row, 2, _f_time)
                _f_time = _model.get_value(_row, 3)
            else:
                _f_time = _model.get_value(_row, 3)
                _model.set_value(_row, 2, _f_time)
                self._testing_model.dic_test_data[_key][2] = _f_time

            _obs_times.append(_f_time)

            _row = _model.iter_next(_row)

        if self.optMTBF.get_active():
            _obsll = np.array([y[0] for y in means])
            _obspt = np.array([y[1] for y in means])
            _obsul = np.array([y[2] for y in means])
        elif self.optFailureIntensity.get_active():
            _obsll = np.array([1.0 / y[2] for y in means])
            _obspt = np.array([1.0 / y[1] for y in means])
            _obsul = np.array([1.0 / y[0] for y in means])

        _obsll[np.isnan(_obsll)] = 0.0
        _obsll[np.isinf(_obsll)] = 0.0
        _obsll[np.where(_obsll) < 0.0] = 0.0
        _obspt[np.isnan(_obspt)] = 0.0
        _obspt[np.isinf(_obspt)] = 0.0
        _obsul[np.isnan(_obsul)] = 0.0
        _obsul[np.isinf(_obsul)] = 0.0

        return(_obs_times, _obsll, _obspt, _obsul)

    def _on_button_clicked(self, button, __event, index):
        """
        Method to respond to gtk.Button() 'clicked' signals and call the
        correct function or method, passing any parameters as needed.

        :param gtk.Button button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        button.handler_block(self._lst_handler_id[index])

        if index == 0:
            self.dtcGrowth.request_assessment(self._testing_model.test_id)
            self.load_page(self._testing_model)

        elif index == 1:
            self.dtcGrowth.save_test(self._testing_model.test_id)

        button.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):     # pylint: disable=R0912
        """
        Method to respond to gtk.Entry() 'focus_out' signals and call the
        correct function or method, passing any parameters as needed.

        :param gtk.Entry entry: the gtk.Entry() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Entry() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        entry.handler_block(self._lst_handler_id[index])

        if index == 2:                      # Statistical confidence
            self._testing_model.confidence = float(entry.get_text()) / 100.0
        elif index == 3:
            self._testing_model.test_termination_time = float(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_toggled(self, button, index):   # pylint: disable=R0912
        """
        Method to respond to gtk.ToggleButton() 'toggled' signals and call
        the correct function or method, passing any parameters as needed.

        :param gtk.ToggleButton button: the gtk.ToggleButton() that called this
                                        method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.SpinButton() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        button.handler_block(self._lst_handler_id[index])

        if index == 4:
            self._testing_model.grouped = 0
        elif index == 5:
            self._testing_model.grouped = 1
        elif index == 6:
            print "MTBF"
        elif index == 7:
            print "Failure intensity"
        elif index == 8:
            print "Linear"
        elif index == 9:
            print "Logarithmic"

        button.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_spin_value_changed(self, button, index):   # pylint: disable=R0912
        """
        Method to respond to gtk.SpinButton() 'value_changed' signals and call
        the correct function or method, passing any parameters as needed.

        :param gtk.SpinButton button: the gtk.SpinButton() that called this
                                      method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        button.handler_block(self._lst_handler_id[index])

        if self._testing_model is not None:
            self._testing_model.confidence = button.get_value() / 100.0

        button.handler_unblock(self._lst_handler_id[index])

        return False
