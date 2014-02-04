#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to
Program testing plans.
"""

__author__ = 'Andrew Rowland <andrew.rowland@reliaqual.com>'
__copyright__ = 'Copyright 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       testing.py is part of The RTK Project
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

import numpy as np
from scipy.stats import chi2, norm

from datetime import datetime
from math import ceil, exp, floor, log, sqrt

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

from _assistants_.adds import AddRGRecord

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
from matplotlib.patches import Ellipse


class Testing:
    """
    The Testing class is used to represent the reliability test plans
    associated with the system being analyzed.
    """

    _rg_plan_labels = [_(u"Phase"), _(u"Test\nArticles"), _(u"Start Date"),
                       _(u"End Date"), _(u"Total Time"), _(u"Growth Rate"),
                       _(u"Initial MTBF"), _(u"Final MTBF"),
                       _(u"Average MTBF")]

    _test_assess_labels = [_(u"Record\nNumber"), _(u"Date"),
                           _(u"Interval\nStart"), _(u"Interval\nEnd"),
                           _(u"Number\nof\nFailures")]

    _test_feasibility_labels = [_(u"Phase"), _(u"Number of\nTest\nArticles"),
                                _(u"Start Date"), _(u"End Date"),
                                _(u"Expected\nNumber\nof\nFailures"),
                                _(u"Required\nManagement\nStrategy"),
                                _(u"Average\nFEF"),
                                _(u"Test Time\nper Unit"),
                                _(u"Test Time\nper Unit\nper Week")]

    def __init__(self, application):
        """
        Initializes the Testing Object.

        Keyword Arguments:
        application -- the RTK application.
        """

        self._ready = False

        self._app = application

        self.treeview = None

# Define local dictionary variables.
        self._dic_assemblies = {}           # List of assemblies.
        self._dic_rg_plan = {}              # RG plan details.

# Define local list variables.
        self._col_order = []

# Define global integer variables.
        self.test_id = 0
        self.n_tests = 0
        self.n_phases = 0


# Create the Notebook for the TESTING object.
        self.notebook = gtk.Notebook()
        if(_conf.TABPOS[2] == 'left'):
            self.notebook.set_tab_pos(gtk.POS_LEFT)
        elif(_conf.TABPOS[2] == 'right'):
            self.notebook.set_tab_pos(gtk.POS_RIGHT)
        elif(_conf.TABPOS[2] == 'top'):
            self.notebook.set_tab_pos(gtk.POS_TOP)
        else:
            self.notebook.set_tab_pos(gtk.POS_BOTTOM)

# =========================================================================== #
# Create the Test Planning widgets.
# =========================================================================== #
        self.cmbAssembly = _widg.make_combo(simple=False)
        self.cmbTestType = _widg.make_combo()

        self.fraPlanDetails = _widg.make_frame(_label_=_(u""))
        self.fraPlanDetails2 = _widg.make_frame(_label_=_(u""))

        self.txtName = _widg.make_entry(_width_=400)
        self.txtDescription = gtk.TextBuffer()
        self.txtAttachment = gtk.TextBuffer()
        self.txtConsumerRisk = _widg.make_entry(_width_=100)
        self.txtProducerRisk = _widg.make_entry(_width_=100)

# Create widgets for reliability growth planning.
        self.btnFindMTBFI = _widg.make_button(_height_=25, _width_=25,
                                              _label_=u"...", _image_=None)
        self.btnFindTTFF = _widg.make_button(_height_=25, _width_=25,
                                             _label_=u"...", _image_=None)

        self.chkFixMTBFI = _widg.make_check_button()
        self.chkFixMTBFG = _widg.make_check_button()
        self.chkFixTTT = _widg.make_check_button()
        self.chkFixAverageGR = _widg.make_check_button()
        self.chkFixProgramMS = _widg.make_check_button()
        self.chkFixProgramProb = _widg.make_check_button()
        self.chkFixTTFF = _widg.make_check_button()

        self.cmbPlanModel = _widg.make_combo()
        self.cmbAssessModel = _widg.make_combo()

        self.fxdRGPlanDetails = gtk.Fixed()

        self.scwRGPlanDetails = gtk.ScrolledWindow()

        self.spnNumPhases = gtk.SpinButton()

        self.tvwRGPlanDetails = gtk.TreeView()

        self.txtMTBFI = _widg.make_entry(_width_=100)
        self.txtMTBFG = _widg.make_entry(_width_=100)
        self.txtMTBFGP = _widg.make_entry(_width_=100)
        self.txtTechReq = _widg.make_entry(_width_=100)
        self.txtTTT = _widg.make_entry(_width_=100)
        self.txtAverageGR = _widg.make_entry(_width_=100)
        self.txtAverageFEF = _widg.make_entry(_width_=100)
        self.txtProgramMS = _widg.make_entry(_width_=100)
        self.txtProgramProb = _widg.make_entry(_width_=100)
        self.txtTTFF = _widg.make_entry(_width_=100)

        if self._planning_tab_create():
            self._app.debug_log.error("testing.py: Failed to create Planning Input tab.")

# =========================================================================== #
# Create the Test Feasibility widgets.
# =========================================================================== #
        height = (self._app.winWorkBook.height * 0.01) / 2.0
        width = (self._app.winWorkBook.width * 0.01) / 2.0

        self.chkMIMGP = _widg.make_check_button(_label_=_(u"Acceptable MTBF<sub>I</sub> / MTBF<sub>GP</sub>."))
        self.chkMIMGP.set_tooltip_text(_(u"Indicates whether or not the initial MTBF to mature MTBF ratio is within reasonable limits."))
        self.lblMIMGP = _widg.make_label("", width=150)

        self.chkFEF = _widg.make_check_button(_label_=_(u"Acceptable average fix effectiveness factor (FEF)."))
        self.chkFEF.set_tooltip_text(_(u"Indicates whether or not the average fix effectiveness factor (FEF) is within reasonable limits."))
        self.lblFEF = _widg.make_label("", width=150)

        self.chkMGMGP = _widg.make_check_button(_label_=_(u"Acceptable MTBF<sub>G</sub> / MTBF<sub>GP</sub>."))
        self.chkMGMGP.set_tooltip_text(_(u"Indicates whether or not the goal MTBF to mature MTBF ratio is within reasonable limits."))
        self.lblMGMGP = _widg.make_label("", width=150)

        self.chkTRMG = _widg.make_check_button(_label_=_(u"Acceptable MTBF<sub>G</sub> / MTBF<sub>I</sub>."))
        self.chkTRMG.set_tooltip_text(_(u"Indicates whether or not the goal MTBF to initial MTBF ratio is within reasonable limits."))
        self.lblMGMI = _widg.make_label("", width=150)

        self.figFigureOC = Figure(figsize=(width, height))

        self.pltPlotOC = FigureCanvas(self.figFigureOC)
        self.pltPlotOC.mpl_connect('button_press_event', self._expand_plot)
        self.pltPlotOC.set_tooltip_text(_(u"Displays the Reliability Growth plan Operating Characteristic curve."))

        self.axAxisOC = self.figFigureOC.add_subplot(111)

        self.tvwTestFeasibility = gtk.TreeView()

        self.txtMIMGP = _widg.make_entry(_width_=75)
        self.txtFEF = _widg.make_entry(_width_=75)
        self.txtMGMGP = _widg.make_entry(_width_=75)
        self.txtTRMG = _widg.make_entry(_width_=75)

        if self._feasibility_tab_create():
            self._app.debug_log.error("testing.py: Failed to create Test Feasibility tab.")

# =========================================================================== #
# Create the Test Assessment widgets.
# =========================================================================== #
# Widgets to enter and display the observed data.
        self.optIndividual = gtk.RadioButton(label=_(u"Individual Failure Time Data"))
        self.optIndividual.set_tooltip_text(_(u"Estimate parameters based on individual failure times."))
        self.optIndividual.set_name('individual')
        self.optIndividual.set_active(True)

        self.optGrouped = gtk.RadioButton(group=self.optIndividual,
                                          label=_(u"Grouped Failure Time Data"))
        self.optGrouped.set_tooltip_text(_(u"Estimate parameters based on grouped failures times."))
        self.optGrouped.set_name('grouped')

        self.optMTBF = gtk.RadioButton(label=_(u"Display results as MTBF"))
        self.optMTBF.set_tooltip_text(_(u"If selected, test results will be displayed as MTBF.  This is the default."))
        self.optMTBF.set_name('mtbf')
        self.optMTBF.set_active(True)
        self.optMTBF.connect('toggled', self._callback_radio)

        self.optFailureIntensity = gtk.RadioButton(group=self.optMTBF,
                                                   label=_(u"Display results as failure intensity"))
        self.optFailureIntensity.set_tooltip_text(_(u"If selected, test results will be displayed as failure intensity."))
        self.optFailureIntensity.set_name('failureintensity')
        self.optFailureIntensity.connect('toggled', self._callback_radio)

        self.tvwTestAssessment = gtk.TreeView()
        self.tvwTestAssessment.set_tooltip_text(_(u"Displays the incidents associated with the selected test plan."))

        self.txtGroupInterval = _widg.make_entry(_width_=75)
        self.txtGroupInterval.set_tooltip_text(_(u"Displays the width of the grouping intervals if using Option for Grouped Data."))

        self.spnConfidence = gtk.SpinButton()
        self.spnConfidence.set_tooltip_text(_(u"Displays the confidence level to use for failure rate/MTBF bounds and goodness of fit tests."))

# Widgets to display the estimated parameters for the selected model.
        self.txtCumTestTime = _widg.make_entry(_width_=100, editable=False)
        self.txtCumTestTime.set_tooltip_text(_(u"Displays the cumulative test time to date for the selected test."))

        self.txtCumFailures = _widg.make_entry(_width_=100, editable=False)
        self.txtCumFailures.set_tooltip_text(_(u"Displays the cumulative number of failures to date for the selected test."))

        self.txtScale = _widg.make_entry(_width_=100, editable=False)
        self.txtScale.set_tooltip_text(_(u"Displays the reliability growth model estimated scale parameter."))

        self.txtShape = _widg.make_entry(_width_=100, editable=False)
        self.txtShape.set_tooltip_text(_(u"Displays the reliability growth model estimated shape parameter."))

        self.txtGRActual = _widg.make_entry(_width_=100, editable=False)
        self.txtGRActual.set_tooltip_text(_(u"Displays the average growth rate over the reliability growth program to date."))

        self.txtRhoInst = _widg.make_entry(_width_=100, editable=False)
        self.txtRhoInst.set_tooltip_text(_(u"Displays the currently assessed instantaneous failure rate of the system under test."))

        self.txtRhoC = _widg.make_entry(_width_=100, editable=False)
        self.txtRhoC.set_tooltip_text(_(u"Displays the currently assessed cumulative failure rate of the system under test."))

        self.txtMTBFInst = _widg.make_entry(_width_=100, editable=False)
        self.txtMTBFInst.set_tooltip_text(_(u"Displays the currently assessed instantaneous MTBF of the system under test."))

        self.txtMTBFC = _widg.make_entry(_width_=100, editable=False)
        self.txtMTBFC.set_tooltip_text(_(u"Displays the currently assessed cumulative MTBF of the system under test."))

        self.lblGoFTrend = _widg.make_label("", width=100)
        self.txtGoFTrend = _widg.make_entry(_width_=100, editable=False)
        self.txtGoFTrend.set_tooltip_text(_(u"Displays the goodness of fit test statistic for failure rate/MTBF trend."))

        self.lblGoFModel = _widg.make_label("", width=100)
        self.txtGoFModel = _widg.make_entry(_width_=100, editable=False)
        self.txtGoFModel.set_tooltip_text(_(u"Displays the goodness of fit test statistic for assessing fit to the selected growth model."))

# Widgets to display the reliability growth plot.
        self.optLinear = gtk.RadioButton(label=_(u"Use Linear Scales"))
        self.optLinear.set_tooltip_text(_(u"Select this option to use linear scales on the reliability growth plot."))
        self.optLinear.set_name('linear')
        self.optLinear.set_active(True)
        self.optLinear.connect('toggled', self._callback_radio)

        self.optLogarithmic = gtk.RadioButton(group=self.optLinear,
                                              label=_(u"Use Logarithmic Scales"))
        self.optLogarithmic.set_tooltip_text(_(u"Select this option to use logarithmic scales on the reliability growth plot."))
        self.optLogarithmic.set_name('log')
        self.optLogarithmic.connect('toggled', self._callback_radio)

        self.figFigure1 = Figure(figsize=(width, height))

        self.pltPlot1 = FigureCanvas(self.figFigure1)
        self.pltPlot1.mpl_connect('button_press_event', self._expand_plot)
        self.pltPlot1.set_tooltip_text(_(u"Displays the selected test plan and observed results."))

        self.axAxis1 = self.figFigure1.add_subplot(111)

        self.vbxPlot1 = gtk.VBox()

        if self._assessment_tab_create():
            self._app.debug_log.error("testing.py: Failed to create Test Assessment tab.")

        self.vbxTesting = gtk.VBox()
        toolbar = self._toolbar_create()

        self.vbxTesting.pack_start(toolbar, expand=False)
        self.vbxTesting.pack_start(self.notebook)

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
        Method to create the toolbar for the TESTING Object work book.
        """

        toolbar = gtk.Toolbar()

# Add record button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        button.set_icon_widget(image)
        button.set_name('Add')
        button.connect('clicked', self._toolbutton_pressed)
        button.set_tooltip_text(_(u"Adds a new test record."))
        toolbar.insert(button, 0)

# Remove record button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        button.set_icon_widget(image)
        button.set_name('Remove')
        #button.connect('clicked', self._test_record_remove)
        button.set_tooltip_text(_(u"Removes the selected test record."))
        toolbar.insert(button, 1)

# Calculate button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        button.set_icon_widget(image)
        button.set_name('Calculate')
        button.connect('clicked', self._calculate)
        button.set_tooltip_text(_(u"Analyzes the selected test plan."))
        toolbar.insert(button, 2)

# Save button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        button.set_icon_widget(image)
        button.set_name('Save')
        button.connect('clicked', self.test_plan_save)
        button.set_tooltip_text(_(u"Saves changes to the program test plans."))
        toolbar.insert(button, 3)

# Assign results to affected assembly.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/import.png')
        button.set_icon_widget(image)
        button.set_name('Assign')
        #button.connect('clicked', AssignResults, self._app)
        button.set_tooltip_text(_(u"Assigns MTBF and hazard rate results to the selected assembly."))
        toolbar.insert(button, 4)

        toolbar.show()

        return(toolbar)

    def _planning_tab_create(self):
        """
        Method to create the Planing Input gtk.Notebook tab and populate it
        with the appropriate widgets for the TESTING object.
        """

        def _planning_widgets_create(self):
            """
            Method to create the Planning Input widgets.
            """

            self.fraPlanDetails.set_shadow_type(gtk.SHADOW_ETCHED_IN)
            self.fraPlanDetails2.set_shadow_type(gtk.SHADOW_ETCHED_IN)

            self.scwRGPlanDetails.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            self.scwRGPlanDetails.add_with_viewport(self.tvwRGPlanDetails)

    # General test planning input widgets.
            self.cmbAssembly.set_tooltip_text(_(u"Selects and displays the assembly associated with the test."))
            self.cmbAssembly.connect('changed', self._callback_combo, 1)

            self.cmbTestType.set_tooltip_text(_(u"Selects and displays the type of test being planned."))
            results = [["HALT"], ["HASS"], ["ALT"], ["ESS"],
                       [u"Reliability Growth"], [u"Reliability Demonstration"],
                       ["PRVT"]]
            _widg.load_combo(self.cmbTestType, results)
            self.cmbTestType.connect('changed', self._callback_combo, 5)

            self.cmbPlanModel.set_tooltip_text(_(u"Selects and displays the reliability growth planning model to be used."))
            results = [["AMSAA-Crow"], ["SPLAN"], ["SSPLAN"]]
            _widg.load_combo(self.cmbPlanModel, results)
            self.cmbPlanModel.connect('changed', self._callback_combo, 12)

            self.cmbAssessModel.set_tooltip_text(_(u"Selects and displays the reliability growth assessment model to be used."))
            results = [[u"AMSAA/Crow Continuous"], [u"AMSAA/Crow Discrete"],
                       [u"SSTRACK"], [u"AMSAA/Crow Projection"],
                       ["Crow Extended"]]
            _widg.load_combo(self.cmbAssessModel, results)
            self.cmbAssessModel.connect('changed', self._callback_combo, 13)

            self.txtName.set_tooltip_text(_(u"The title or name of the selected test."))
            self.txtName.connect('focus-out-event',
                                 self._callback_entry, 'text', 3)

            self.txtDescription.connect('changed',
                                        self._callback_entry, None, 'text', 4)

    # Create a tag named hyperlink if it doesn't already exist.
            tagtable = self.txtAttachment.get_tag_table()
            tag = tagtable.lookup('hyperlink')
            if(tag is None):
                tag = self.txtAttachment.create_tag('hyperlink', foreground='blue')
            tag.connect('event', self._hyperlink_handler)
            self.txtAttachment.connect('changed',
                                       self._callback_entry, None, 'text', 15)

    # Reliability Growth test planning widgets.
            self.btnFindMTBFI.set_tooltip_text(_(u"Launches the initial MTBF calculator."))
            self.btnFindTTFF.set_tooltip_text(_(u"Launches the time to first fix calculator."))
            self.btnFindTTFF.connect('released', self._mttff_calculator)

            self.txtMTBFI.set_tooltip_text(_(u"The initial MTBF for the selected reliability growth plan."))
            self.txtMTBFI.connect('focus-out-event',
                                  self._callback_entry, 'float', 6)

            self.chkFixMTBFI.set_tooltip_text(_(u"Fixes the value of the initial MTBF when calculating the selected reliability growth plan."))
            self.chkFixMTBFI.set_active(True)

            self.txtMTBFG.set_tooltip_text(_(u"The goal MTBF for the selected reliability growth plan."))
            self.txtMTBFG.connect('focus-out-event',
                                  self._callback_entry, 'float', 7)

            self.chkFixMTBFG.set_tooltip_text(_(u"Fixes the value of the program goal MTBF when calculating the selected reliability growth plan."))
            self.chkFixMTBFG.set_active(True)

            self.txtMTBFGP.set_tooltip_text(_(u"The potential MTBF at maturity for the assembly associated with the selected reliability growth plan."))
            self.txtMTBFGP.connect('focus-out-event',
                                   self._callback_entry, 'float', 8)

            self.txtTechReq.set_tooltip_text(_(u"The MTBF require by the developmental program associated with the selected reliability growth plan."))
            self.txtTechReq.connect('focus-out-event',
                                    self._callback_entry, 'float', 9)

            self.txtProducerRisk.set_tooltip_text(_(u"The producer (Type I) risk.  This is the risk of accepting a system when the true reliability is below the technical requirement."))
            self.txtProducerRisk.connect('focus-out-event',
                                         self._callback_entry, 'float', 11)

            self.txtConsumerRisk.set_tooltip_text(_(u"The consumer (Type II) risk.  This is the risk of rejecting a system when the true reliability is at least the goal reliability."))
            self.txtConsumerRisk.connect('focus-out-event',
                                         self._callback_entry, 'float', 10)

            adjustment = gtk.Adjustment(0, 0, 100, 1, 1)
            self.spnNumPhases.set_adjustment(adjustment)
            self.spnNumPhases.set_tooltip_text(_(u"The number of reliability growth phases."))
            self.spnNumPhases.connect('focus-out-event',
                                      self._callback_entry, 'float', 14)
            self.spnNumPhases.connect('value-changed',
                                      self._callback_spin, 14)

            self.txtTTT.set_tooltip_text(_(u"The total test time."))
            self.txtTTT.connect('focus-out-event',
                                self._callback_entry, 'float', 16)

            self.chkFixTTT.set_tooltip_text(_(u"Fixes the value of the total program test time when calculating the selected reliability growth plan."))
            self.chkFixTTT.set_active(True)

            self.txtAverageGR.set_tooltip_text(_(u"The average growth rate over the entire reliability growth program."))
            self.txtAverageGR.connect('focus-out-event',
                                      self._callback_entry, 'float', 17)

            self.chkFixAverageGR.set_tooltip_text(_(u"Fixes the value of the average growth rate when calculating the selected reliability growth plan."))
            self.chkFixAverageGR.set_active(True)

            self.txtAverageFEF.set_tooltip_text(_(u"The average fix effectiveness factor (FEF) over the entire reliability growth program."))
            self.txtAverageFEF.connect('focus-out-event',
                                      self._callback_entry, 'float', 21)

            self.txtProgramMS.set_tooltip_text(_(u"The percentage of failure that will be addressed by corrective action over the entire reliability growth program."))
            self.txtProgramMS.connect('focus-out-event',
                                      self._callback_entry, 'float', 18)

            self.chkFixProgramMS.set_tooltip_text(_(u"Fixes the value of the management strategy when calculating the selected reliability growth plan."))
            self.chkFixProgramMS.set_active(True)

            self.txtProgramProb.set_tooltip_text(_(u"The probability of seeing a failure in any phase of the reliability growth program."))
            self.txtProgramProb.connect('focus-out-event',
                                        self._callback_entry, 'float', 19)

            self.chkFixProgramProb.set_tooltip_text(_(u"Fixes the value of the probability of seeing a failure when calculating the selected reliability growth plan."))
            self.chkFixProgramProb.set_active(True)

            self.txtTTFF.set_tooltip_text(_(u"The estimated time to the first fix during the reliability growth program."))
            self.txtTTFF.connect('focus-out-event',
                                 self._callback_entry, 'float', 20)

            self.chkFixTTFF.set_tooltip_text(_(u"Fixes the value of the time to first fix when calculating the selected reliability growth plan."))
            self.chkFixTTFF.set_active(True)

    # ======================================================================= #
    # Reliability Growth Testing Detailed Inputs
    #   0. Test Phase
    #   1. Number of Test Articles for the test phase
    #   2. Phase Start Date
    #   3. Phase End Date
    #   4. Test Time for the test phase
    #   5. Growth Rate for the test phase
    #   6. Initial MTBF for the test phase
    #   7. Final MTBF for the test phase
    #   8. Average MTBF for the test phase
    # ======================================================================= #
            _labels_ = [_(u"Phase"), _(u"Test\nArticles"), _(u"Start Date"),
                        _(u"End Date"), _(u"Total Time"), _(u"Growth Rate"),
                        _(u"Initial MTBF"), _(u"Final MTBF"),
                        _(u"Average MTBF")]
            model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_INT,
                                  gobject.TYPE_STRING, gobject.TYPE_STRING,
                                  gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                  gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                  gobject.TYPE_FLOAT)
            self.tvwRGPlanDetails.set_model(model)

            for i in range(9):
                cell = gtk.CellRendererText()
                cell.set_property('editable', 1)
                cell.set_property('background', 'white')
                cell.connect('edited', self._rg_plan_edit, i)

                column = gtk.TreeViewColumn()
                label = _widg.make_column_heading(_labels_[i])
                column.set_widget(label)
                column.pack_start(cell, True)
                column.set_attributes(cell, text=i)
                column.set_resizable(True)
                if(i < 2):
                    _datatype_ = (i, 'gint')
                elif(i == 2 or i == 3):
                    _datatype_ = (i, 'gchararray')
                else:
                    _datatype_ = (i, 'gfloat')
                column.set_cell_data_func(cell, _widg.format_cell,
                                          (i, _datatype_))
                column.connect('notify::width', _widg.resize_wrap, cell)

                self.tvwRGPlanDetails.append_column(column)

            self.tvwRGPlanDetails.connect('button_press_event',
                                          self._treeview_clicked, 1)

            return False

        if _planning_widgets_create(self):
            self._app.debug_log.error("testing.py: Failed to create Planning Input widgets.")

        hpaned = gtk.HPaned()

# Populate the left side of the Planing Input tab.
        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_(u"Planning Inputs"))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(fixed)

        _labels_ = [_(u"Assembly:"), _(u"Test Type:"), _(u"Test Title:"),
                    _(u"Test Description:")]
        (_x_pos_, _y_pos_) = _widg.make_labels(_labels_, fixed, 5, 5)
        _x_pos_ += 5

        fixed.put(self.cmbAssembly, _x_pos_, _y_pos_[0])
        fixed.put(self.cmbTestType, _x_pos_, _y_pos_[1])
        fixed.put(self.txtName, _x_pos_, _y_pos_[2])

        textview = _widg.make_text_view(buffer_=self.txtDescription,
                                        width=555)
        textview.set_tooltip_text(_(u"Detailed description of the selected test."))
        fixed.put(textview, 5, _y_pos_[3] + 30)

        label = _widg.make_label(_(u"Attachments:"), 150, 25)
        fixed.put(label, 5, _y_pos_[3] + 135)
        textview = _widg.make_text_view(buffer_=self.txtAttachment,
                                        width=555)
        textview.set_tooltip_text(_(u"Displays the URLs to any attached documents associated with the selected test."))
        fixed.put(textview, 5, _y_pos_[3] + 170)

        fixed.show_all()

        hpaned.pack1(frame, True, True)

# Populate the gtk.Fixed widgets that will be displayed in the middle of the
# Planning Input tab.  The gtk.Fixed that is displayed depends on the selected
# reliability test type.

# =========================================================================== #
# Reliability Growth Testing Detailed Inputs
# =========================================================================== #

        _labels_ = [_(u"Initial Program MTBF (MTBF<sub>I</sub>):"),
                    _(u"Program Required MTBF (MTBF<sub>TR</sub>):"),
                    _(u"Program Goal MTBF (MTBF<sub>G</sub>):"),
                    _(u"Potential Mature MTBF (MTBF<sub>GP</sub>):"),
                    _(u"Number of Phases:"),
                    _(u"Time to First Fix (t<sub>1</sub>):"),
                    _(u"Total Test Time:"), _(u"Average Growth Rate:"),
                    _(u"Average FEF:"), _(u"Program MS:"),
                    _(u"Program Probability:"), _(u"Producer Risk:"),
                    _(u"Consumer Risk"),]

        (_x_pos_, _y_pos_) = _widg.make_labels(_labels_,
                                               self.fxdRGPlanDetails, 5, 110)
        _x_pos_ += 25

        label = _widg.make_label(_(u"RG Plan Model:"), 150, 50)
        self.fxdRGPlanDetails.put(label, 5, 5)
        self.fxdRGPlanDetails.put(self.cmbPlanModel, _x_pos_, 5)

        label = _widg.make_label(_(u"RG Assessment Model:"), -1, 50)
        self.fxdRGPlanDetails.put(label, 5, 35)
        self.fxdRGPlanDetails.put(self.cmbAssessModel, _x_pos_, 35)

        label = _widg.make_label(_(u"Fix\nValue"), 150, 50)
        self.fxdRGPlanDetails.put(label, _x_pos_ + 135, 65)

        self.fxdRGPlanDetails.put(self.txtMTBFI, _x_pos_, _y_pos_[0])
        #self.fxdRGPlanDetails.put(self.btnFindMTBFI, _x_pos_ + 105, _y_pos_[0])
        self.fxdRGPlanDetails.put(self.chkFixMTBFI, _x_pos_ + 145, _y_pos_[0])
        self.fxdRGPlanDetails.put(self.txtTechReq, _x_pos_, _y_pos_[1])
        self.fxdRGPlanDetails.put(self.txtMTBFG, _x_pos_, _y_pos_[2])
        self.fxdRGPlanDetails.put(self.chkFixMTBFG, _x_pos_ + 145, _y_pos_[2])
        self.fxdRGPlanDetails.put(self.txtMTBFGP, _x_pos_, _y_pos_[3])
        self.fxdRGPlanDetails.put(self.spnNumPhases, _x_pos_, _y_pos_[4])
        self.fxdRGPlanDetails.put(self.txtTTFF, _x_pos_, _y_pos_[5])
        self.fxdRGPlanDetails.put(self.btnFindTTFF, _x_pos_ + 105, _y_pos_[5])
        self.fxdRGPlanDetails.put(self.chkFixTTFF, _x_pos_ + 145, _y_pos_[5])
        self.fxdRGPlanDetails.put(self.txtTTT, _x_pos_, _y_pos_[6])
        self.fxdRGPlanDetails.put(self.chkFixTTT, _x_pos_ + 145, _y_pos_[6])
        self.fxdRGPlanDetails.put(self.txtAverageGR, _x_pos_, _y_pos_[7])
        self.fxdRGPlanDetails.put(self.chkFixAverageGR, _x_pos_ + 145, _y_pos_[7])
        self.fxdRGPlanDetails.put(self.txtAverageFEF, _x_pos_, _y_pos_[8])
        #self.fxdRGPlanDetails.put(self.chkFixAverageFEF, _x_pos_ + 145, _y_pos_[8])
        self.fxdRGPlanDetails.put(self.txtProgramMS, _x_pos_, _y_pos_[9])
        self.fxdRGPlanDetails.put(self.chkFixProgramMS, _x_pos_ + 145, _y_pos_[9])
        self.fxdRGPlanDetails.put(self.txtProgramProb, _x_pos_, _y_pos_[10])
        self.fxdRGPlanDetails.put(self.chkFixProgramProb, _x_pos_ + 145, _y_pos_[10])
        self.fxdRGPlanDetails.put(self.txtProducerRisk, _x_pos_, _y_pos_[11])
        self.fxdRGPlanDetails.put(self.txtConsumerRisk, _x_pos_, _y_pos_[12])

        self.fxdRGPlanDetails.show_all()

        hpaned1 = gtk.HPaned()
        hpaned1.pack1(self.fraPlanDetails)

# Populate the gtk.Fixed widgets that will be displayed on the right of the
# Planning Input tab.  The gtk.Fixed that is displayed depends on the selected
# reliability test type.

        hpaned1.pack2(self.fraPlanDetails2)

        hpaned.pack2(hpaned1, True, True)

# Insert the tab.
        label = gtk.Label()
        _heading = _(u"Planning\nInputs")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Displays planning inputs for the selected test."))

        self.notebook.insert_page(hpaned,
                                  tab_label=label,
                                  position=-1)

        return False

    def _planning_tab_load(self):
        """
        Loads the widgets with test planning input data for the TESTING Object.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        self.test_id = _model_.get_value(_row_, 2)

        _assembly_id = _model_.get_value(_row_,
                                         self._col_order[1])
        _index_ = self._dic_assemblies[_assembly_id]
        self.cmbAssembly.set_active(_index_)

        _test_type = _model_.get_value(_row_, self._col_order[5])
        self.cmbTestType.set_active(_test_type)

        self.cmbPlanModel.set_active(
            _model_.get_value(_row_, self._col_order[12]))
        self.cmbAssessModel.set_active(
            _model_.get_value(_row_, self._col_order[13]))

        self.txtName.set_text(
            str(_model_.get_value(_row_, self._col_order[3])))
        self.txtDescription.set_text(
            str(_model_.get_value(_row_, self._col_order[4])))
        self.txtMTBFI.set_text(str(fmt.format(
            _model_.get_value(_row_, self._col_order[6]))))
        self.txtMTBFG.set_text(str(fmt.format(
            _model_.get_value(_row_, self._col_order[7]))))
        self.txtMTBFGP.set_text(str(fmt.format(
            _model_.get_value(_row_, self._col_order[8]))))
        self.txtTechReq.set_text(str(fmt.format(
            _model_.get_value(_row_, self._col_order[9]))))
        self.txtConsumerRisk.set_text(str(fmt.format(
            _model_.get_value(_row_, self._col_order[10]))))
        self.txtProducerRisk.set_text(str(fmt.format(
            _model_.get_value(_row_, self._col_order[11]))))
        self.spnNumPhases.set_value(
            _model_.get_value(_row_, self._col_order[14]))
        self.txtAttachment.set_text(
            str(_model_.get_value(_row_, self._col_order[15])))
        self._load_hyperlinks()
        self.txtTTT.set_text(str(fmt.format(
            _model_.get_value(_row_, self._col_order[16]))))
        self.txtAverageGR.set_text(str(fmt.format(
            _model_.get_value(_row_, self._col_order[17]))))
        self.txtProgramMS.set_text(str(fmt.format(
            _model_.get_value(_row_, self._col_order[18]))))
        self.txtProgramProb.set_text(str(fmt.format(
            _model_.get_value(_row_, self._col_order[19]))))
        self.txtTTFF.set_text(str(fmt.format(
            _model_.get_value(_row_, self._col_order[20]))))
        self.txtAverageFEF.set_text(str(fmt.format(
            _model_.get_value(_row_, self._col_order[21]))))

        if(_test_type == 5):
            self._rg_plan_details(1)
            self._rg_plan_details(2)

        self.pltPlotOC.hide()

        return False

    def _feasibility_tab_create(self):
        """
        Method to create the Test Feasibility gtk.Notebook tab and populate it
        with the appropriate widgets for the TESTING object.
        """

        hpaned = gtk.HPaned()

# Populate the left side of the Test Feasibility tab.
        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_(u"Test Feasibility"))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(fixed)

        y_pos = 5

        label = _widg.make_label(_(u"MTBF<sub>I</sub> / MTBF<sub>GP</sub> should fall in the range of 0.15 - 0.47.  On average this ratio is 0.30."),
                                 width=400, height=40, bold=False)
        label.set_justify(gtk.JUSTIFY_LEFT)
        fixed.put(label, 5, y_pos)
        y_pos += 45

        label = _widg.make_label(_(u"Program MTBF<sub>I</sub> / MTBF<sub>GP</sub>:"),
                                 width=200, bold=False)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtMIMGP, 205, y_pos)
        fixed.put(self.lblMIMGP, 290, y_pos)
        y_pos += 30

        fixed.put(self.chkMIMGP, 5, y_pos)
        y_pos += 40

        label = _widg.make_label(_(u"MTBF<sub>G</sub> / MTBF<sub>GP</sub> should fall in the range of 0.60 - 0.80."),
                                 width=400, height=40, bold=False)
        label.set_justify(gtk.JUSTIFY_LEFT)
        fixed.put(label, 5, y_pos)
        y_pos += 45

        label = _widg.make_label(_(u"Program MTBF<sub>G</sub> / MTBF<sub>GP</sub>:"),
                                 width=200, bold=False)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtMGMGP, 205, y_pos)
        fixed.put(self.lblMGMGP, 290, y_pos)
        y_pos += 30

        fixed.put(self.chkMGMGP, 5, y_pos)
        y_pos += 40

        label = _widg.make_label(_(u"MTBF<sub>G</sub> / MTBF<sub>I</sub> should fall in the range of 2 - 3."),
                                 width=400, height=40, bold=False)
        label.set_justify(gtk.JUSTIFY_LEFT)
        fixed.put(label, 5, y_pos)
        y_pos += 45

        label = _widg.make_label(_(u"Program MTBF<sub>G</sub> / MTBF<sub>TR</sub>:"),
                                 width=200, bold=False)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtTRMG, 205, y_pos)
        fixed.put(self.lblMGMI, 290, y_pos)
        y_pos += 30

        fixed.put(self.chkTRMG, 5, y_pos)
        y_pos += 40

        label = _widg.make_label(_(u"The Fix Effectiveness Factor should fall in the range of 0.55 - 0.85.  On average the FEF is 0.70."),
                                 width=400, height=40, bold=False)
        label.set_justify(gtk.JUSTIFY_LEFT)
        fixed.put(label, 5, y_pos)
        y_pos += 45

        label = _widg.make_label(_(u"Program average FEF:"),
                                 width=200, bold=False)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtFEF, 205, y_pos)
        fixed.put(self.lblFEF, 290, y_pos)
        y_pos += 30

        fixed.put(self.chkFEF, 5, y_pos)

        fixed.show_all()

        hpaned.pack1(frame)

# Populate the center of the Test Feasibility tab.
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        frame = _widg.make_frame(_label_=_(u"Feasibility By Phase"))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(scrollwindow)
        frame.show_all()

        model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_INT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT)
        self.tvwTestFeasibility.set_model(model)

        for i in range(9):
            cell = gtk.CellRendererText()
            if(i == 1 or i == 2 or i == 3):
                cell.set_property('editable', 1)
                cell.set_property('background', 'white')
                cell.connect('edited', self._rg_feasibility_edit, i)
            else:
                cell.set_property('editable', 0)
                cell.set_property('background', 'grey')

            column = gtk.TreeViewColumn()
            label = _widg.make_column_heading(self._test_feasibility_labels[i])
            column.set_widget(label)
            column.pack_start(cell, True)
            column.set_attributes(cell, text=i)
            column.set_resizable(True)
            if(i > 3):
                _datatype_ = (i, 'gfloat')
            else:
                _datatype_ = (i, 'gint')
            column.set_cell_data_func(cell, _widg.format_cell,
                                      (i, _datatype_))
            column.connect('notify::width', _widg.resize_wrap, cell)

            self.tvwTestFeasibility.append_column(column)

        self.tvwTestFeasibility.connect('button_press_event',
                                        self._treeview_clicked, 2)

        scrollwindow.add_with_viewport(self.tvwTestFeasibility)

        hpaned.pack2(frame)

        hpaned2 = gtk.HPaned()
        hpaned2.pack1(hpaned)

# Populate the right side of the Test Feasibility tab.
        frame = _widg.make_frame(_label_=_(u"Test Operating Characteristic Curve"))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(self.pltPlotOC)
        self.pltPlotOC.hide()

        hpaned2.pack2(frame, resize=False)

# Insert the tab.
        label = gtk.Label()
        _heading = _(u"Test\nFeasibility")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Displays test feasibility for the selected test."))

        self.notebook.insert_page(hpaned2,
                                  tab_label=label,
                                  position=-1)

        return False

    def _assessment_tab_create(self):
        """
        Method to create the Test Assessment gtk.Notebook tab and populate it
        with the appropriate widgets for the TESTING object.
        """

        def _assessment_tab_widgets_create(self):
            """
            Function to create the Assessment tab widgets.
            """

            self.optIndividual.connect('toggled', self._callback_check, 22)
            self.optGrouped.connect('toggled', self._callback_check, 22)

            self.spnConfidence.connect('focus-out-event',
                                       self._callback_entry, 'float', 26)
            self.spnConfidence.connect('value-changed',
                                       self._callback_spin, 26)

            self.txtGroupInterval.connect('focus-out-event',
                                          self._callback_entry, 'float', 23)
            self.txtCumTestTime.connect('focus-out-event',
                                        self._callback_entry, 'float', 24)
            self.txtCumFailures.connect('focus-out-event',
                                        self._callback_entry, 'float', 25)

            return False

        if _assessment_tab_widgets_create(self):
            self._app.debug_log.error("testing.py: Failed to create Assessment Tab widgets.")

        hpaned = gtk.HPaned()

# =========================================================================== #
# Create the left pane to enter/display the observed reliability growth data.
# =========================================================================== #
        vbox = gtk.VBox()

        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_(u""))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(fixed)
        frame.show_all()

        y_pos = 5
        fixed.put(self.optIndividual, 5, y_pos)
        y_pos += 30

        fixed.put(self.optGrouped, 5, y_pos)
        fixed.put(self.txtGroupInterval, 230, y_pos)
        y_pos += 25

        adjustment = gtk.Adjustment(0, 0, 100, 0.5, 1)
        self.spnConfidence.set_adjustment(adjustment)

        label = _widg.make_label(_(u"Confidence:"))
        fixed.put(label, 5, y_pos)
        fixed.put(self.spnConfidence, 230, y_pos)
        y_pos += 25

        label = _widg.make_label(u"")
        fixed.put(label, 5, y_pos)

        vbox.pack_start(frame, expand=False)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        frame = _widg.make_frame(_label_=_(u"Reliability Test Data"))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(scrollwindow)
        frame.show_all()

        model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_INT)
        self.tvwTestAssessment.set_model(model)

        for i in range(5):
            cell = gtk.CellRendererText()
            cell.set_property('editable', 1)
            cell.set_property('background', 'white')
            cell.connect('edited', _widg.edit_tree, i, model)

            column = gtk.TreeViewColumn()
            label = _widg.make_column_heading(self._test_assess_labels[i])
            column.set_widget(label)
            column.pack_start(cell, True)
            column.set_attributes(cell, text=i)
            column.set_resizable(True)
            if(i == 1 or i == 2):
                _datatype_ = (i, 'gfloat')
            else:
                _datatype_ = (i, 'gint')
            column.set_cell_data_func(cell, _widg.format_cell,
                                      (i, _datatype_))
            column.connect('notify::width', _widg.resize_wrap, cell)

            self.tvwTestAssessment.append_column(column)

        scrollwindow.add_with_viewport(self.tvwTestAssessment)

        vbox.pack_start(frame)
        hpaned.pack1(vbox)

# =========================================================================== #
# Create the center pane to display the estimated parameters.
# =========================================================================== #
        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_(u"Estimated Parameters"))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(fixed)
        frame.show_all()

        y_pos = 5
        label = _widg.make_label(_(u"Cum. Test Time:"))
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtCumTestTime, 200, y_pos)
        y_pos += 25

        label = _widg.make_label(_(u"Cum. Failures:"))
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtCumFailures, 200, y_pos)
        y_pos += 25

        label = _widg.make_label(_(u"Lambda:"))
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtScale, 200, y_pos)
        y_pos += 25

        label = _widg.make_label(_(u"Beta:"))
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtShape, 200, y_pos)
        y_pos += 25

        label = _widg.make_label(_(u"Observed Growth Rate:"))
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtGRActual, 200, y_pos)
        y_pos += 40

        label = _widg.make_label(_(u"Instaneous Failure Rate:"))
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtRhoInst, 200, y_pos)
        y_pos += 25

        label = _widg.make_label(_(u"Cumulative Failure Rate:"))
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtRhoC, 200, y_pos)
        y_pos += 25

        label = _widg.make_label(_(u"Instantaneous MTBF:"))
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtMTBFInst, 200, y_pos)
        y_pos += 25

        label = _widg.make_label(_(u"Cumulative MTBF:"))
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtMTBFC, 200, y_pos)
        y_pos += 40

        label = _widg.make_label(_(u"GoF for Trend:"))
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtGoFTrend, 200, y_pos)
        fixed.put(self.lblGoFTrend, 305, y_pos)
        y_pos += 25

        label = _widg.make_label(_(u"GoF for Model:"))
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtGoFModel, 200, y_pos)
        fixed.put(self.lblGoFModel, 305, y_pos)

        hpaned.pack2(frame)

# =========================================================================== #
# Create the right pane to display the reliability growth plot.
# =========================================================================== #
        vbox = gtk.VBox()

        hpaned2 = gtk.HPaned()
        hpaned2.pack1(hpaned)

        fixed = gtk.Fixed()

        y_pos = 5
        fixed.put(self.optLinear, 5, y_pos)
        fixed.put(self.optMTBF, 205, y_pos)
        y_pos += 35

        fixed.put(self.optLogarithmic, 5, y_pos)
        fixed.put(self.optFailureIntensity, 205, y_pos)
        y_pos += 35

        label = _widg.make_label(u"")
        fixed.put(label, 5, y_pos)

        frame = _widg.make_frame(_label_=_(u"Reliability Test Plot"))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(self.pltPlot1)
        frame.show_all()

        vbox.pack_start(fixed, expand=False)
        vbox.pack_start(frame)

        hpaned2.pack2(vbox)

# Insert the tab.
        label = gtk.Label()
        _label_ = _(u"Test\nAssessment")
        label.set_markup("<span weight='bold'>" + _label_ + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Displays reliability test results."))
        self.notebook.insert_page(hpaned2,
                                  tab_label=label,
                                  position=-1)

        return False

    def _assessment_tab_load(self):
        """
        Loads the widgets with test results for the TESTING Object.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        _grouped_ = _model_.get_value(_row_, 22)
        if(_grouped_ == 1):
            self.optGrouped.set_active(True)
        else:
            self.optIndividual.set_active(True)

        self.spnConfidence.set_value(_model_.get_value(_row_, 26))

        self.txtGroupInterval.set_text(str(_model_.get_value(_row_, 23)))
        self.txtCumTestTime.set_text(str(_model_.get_value(_row_, 24)))
        self.txtCumFailures.set_text(str(_model_.get_value(_row_, 25)))

        return False

    def _rg_plot_load(self, TPT, MTBFA, _obs_, _N_):
        """
        Loads the Reliability Growth plot.

        Keyword Arguments:
        TPT   -- a list of the planned test times for each test phase.
        MTBFA -- a list of planned average MTBF values for each test phase.
        obs   -- a list of observed values for each test phase.
        N     -- a list of the number of failures in each interval.
        """

        def _load_idealized(self, MTBFA, TPT):
            """
            Method to load the idealized growth curve.

            Keyword Arguments:
            MTBFA -- a list of planned average MTBF values for each test phase.
            TPT   -- a list of the planned test times for each test phase.
            """

            (_model_, _row_) = self.treeview.get_selection().get_selected()

    # Read overall program inputs.
            MTBFI = _model_.get_value(_row_, 6)
            TTT = _model_.get_value(_row_, 16)
            AvgGR = _model_.get_value(_row_, 17)
            ti = _model_.get_value(_row_, 20)

            times = list(xrange(int(TTT)))
            ideal = []
            plan = []
            j = 0
            if(self.optMTBF.get_active()):
                for i in range(len(times)):
                    if(times[i] < int(ti)):
                        ideal.append(MTBFI)
                    elif(times[i] == int(ti)):
                        ideal.append(np.nan)
                    else:
                        ideal.append((MTBFI * (times[i] / ti)**AvgGR) / (1.0 - AvgGR))

            elif(self.optFailureIntensity.get_active()):
                for i in range(len(times)):
                    if(times[i] < int(ti)):
                        ideal.append(1.0 / MTBFI)
                    elif(times[i] == int(ti)):
                        ideal.append(np.nan)
                    else:
                        ideal.append((1.0 - AvgGR) / (MTBFI * (times[i] / ti)**AvgGR))

            return(ideal)

        def _load_plan(self, MTBFA, TPT):
            """
            Method to load the planned growth curve.

            Keyword Arguments:
            MTBFA -- a list of planned average MTBF values for each test phase.
            TPT   -- a list of the planned test times for each test phase.
            """

            (_model_, _row_) = self.treeview.get_selection().get_selected()

    # Read overall program inputs.
            MTBFI = _model_.get_value(_row_, 6)
            TTT = _model_.get_value(_row_, 16)
            AvgGR = _model_.get_value(_row_, 17)
            ti = _model_.get_value(_row_, 20)

            times = list(xrange(int(TTT)))
            plan = []
            j = 0
            if(self.optMTBF.get_active()):
                _ylabel = _(u"MTBF")
                for i in range(len(times)):
                    T0 = int(sum(TPT[:j]))
                    T1 = int(sum(TPT[:j+1]))
                    if(int(times[i]) >= T0 and int(times[i]) < T1):
                        plan.append(MTBFA[j])
                    else:
                        plan.append(np.nan)
                        j += 1
            elif(self.optFailureIntensity.get_active()):
                _ylabel = _(u"Failure Intensity")
                for i in range(len(times)):
                    T0 = int(sum(TPT[:j]))
                    T1 = int(sum(TPT[:j+1]))
                    if(int(times[i]) >= T0 and int(times[i]) < T1):
                        plan.append(1.0 / MTBFA[j])
                    else:
                        plan.append(np.nan)
                        j += 1

            return(plan)

        def _rg_plot_load_observed(self, obs, N):
            """
            Method to load the observed MTBF values.

            Keyword Arguments:
            obs -- a list of observed values for each test phase.
            N   -- a list of the number of failures in each interval.
            """

            (_model_, _row_) = self.treeview.get_selection().get_selected()

    # Read overall program inputs.
            MTBFI = _model_.get_value(_row_, 6)
            TTT = _model_.get_value(_row_, 16)
            AvgGR = _model_.get_value(_row_, 17)
            ti = _model_.get_value(_row_, 20)

            _interval_ = float(self.txtGroupInterval.get_text())
            _alpha_ = float(self.spnConfidence.get_value()) / 100.0

    # Update the left interval time using the previous record's right interval
    # value if the data is grouped.  Create a list of observed cumulative failure
    # times to use when plotting the results.
            i = 0
            _f_time_ = 0.0
            _obs_times_ = [0.5 * _interval_]
            _model_ = self.tvwTestAssessment.get_model()
            _row_ = _model_.get_iter_root()
            while _row_ is not None:
                if(self.optGrouped.get_active()):
                    _obs_times_.append(_obs_times_[i] + _interval_)
                    _model_.set_value(_row_, 2, _f_time_)
                    _f_time_ = _model_.get_value(_row_, 3)
                    i += 1
                else:
                    _obs_times_.append(_f_time_)
                    _f_time_ = _model_.get_value(_row_, 3)
                    _model_.set_value(_row_, 2, _f_time_)

                _row_ = _model_.iter_next(_row_)

    # The last observation time is the minimum of the last entered time or the last
    # interval time.
            _obs_times_[-1] = min(TTT, _obs_times_[-1])
            _obs_times_ = np.array(_obs_times_[:len(obs)])

    # Calculate the bounds at each observation point.
            _obsll_ = np.array([], float)
            _obsul_ = np.array([], float)
            for i in range(len(_obs_)):
                _Cll_ = (1.0 - (norm.ppf(0.5 + (_alpha_ / 2.0)) / sqrt(2.0 * sum(_N_[:i+1]))))**-2.0
                _Cul_ = (1.0 + (norm.ppf(0.5 + (_alpha_ / 2.0)) / sqrt(2.0 * sum(_N_[:i+1]))))**-2.0
                _obsll_ = np.append(_obsll_, obs[i] * _Cll_)
                _obsul_ = np.append(_obsul_, obs[i] * _Cul_)

            (_new_obs_times_, _obsll_) = _calc.smooth_curve(_obs_times_, _obsll_,
                                                            50 * len(obs))
            _obsul_ = _calc.smooth_curve(_obs_times_, _obsul_, 50 * len(obs))[1]
            _obs_times_ = _obs_times_.tolist()

            return(_obs_times_, _new_obs_times, _obsll_, _obsul_)

        (_model_, _row_) = self.treeview.get_selection().get_selected()

# Read overall program inputs.
        MTBFI = _model_.get_value(_row_, 6)
        TTT = _model_.get_value(_row_, 16)
        AvgGR = _model_.get_value(_row_, 17)
        ti = _model_.get_value(_row_, 20)

        _interval_ = float(self.txtGroupInterval.get_text())
        _alpha_ = float(self.spnConfidence.get_value()) / 100.0

# Create a list of MTBF target values.  These will be plotted as horizontal
# lines on the growth plot.  These MTBF values are the program goal MTBF, the
# growth potential MTBF, and the technical requirements MTBF.
        if(self.optMTBF.get_active()):
            _targets_ = [_model_.get_value(_row_, 9)]
            _targets_.append(_model_.get_value(_row_, 7))
            _targets_.append(_model_.get_value(_row_, 8))
        elif(self.optFailureIntensity.get_active()):
            _targets_ = [1.0 / _model_.get_value(_row_, 9)]
            _targets_.append(1.0 / _model_.get_value(_row_, 7))
            _targets_.append(1.0 / _model_.get_value(_row_, 8))

# Build the idealized growth and planned program curves.
        times = list(xrange(int(TTT)))
        ideal = _load_idealized(self, MTBFA, TPT)
        plan = _load_plan(self, MTBFA, TPT)
        if(self.optMTBF.get_active()):
            _ylabel = _(u"MTBF")
        elif(self.optFailureIntensity.get_active()):
            _ylabel = _(u"Failure Intensity")
        _legend_ = [u"Idealized Growth Curve", u"Planned Growth Curve"]

# Plot the reliability growth program curves.
        _widg.load_plot(self.axAxis1, self.pltPlot1,
                        x=times, y1=ideal, y2=plan,
                        _title_=_(u""),
                        _xlab_=_(u"Test Time (t)"),
                        _ylab_=_ylabel,
                        _type_=[2, 2, 2],
                        _marker_=['b-', 'r-'])

# If there are any observed values, build the observed MTBF curve with bounds.
        if(len(_obs_) > 0):
            (_obs_times_, _new_obs_times, _obsll_, _obsul_) = _load_observed(self, _obs_, _N_)

            line = matplotlib.lines.Line2D(_obs_times_, _obs_, lw=0.0, color='k',
                                           marker='o', markersize=6)
            self.axAxis1.add_line(line)

            line = matplotlib.lines.Line2D(_new_obs_times_, _obsll_, lw=1.5, color='k',
                                           ls='-.')
            self.axAxis1.add_line(line)

            line = matplotlib.lines.Line2D(_new_obs_times_, _obsul_, lw=1.5, color='k',
                                           ls='-.')
            self.axAxis1.add_line(line)

            _legend_.append(u"Observed")
            _legend_.append(u"{0:.1f}% Bounds".format(_alpha_ * 100.0))

# Plot a horizontal line at the technical requirement and the growth potential
# failure rate or MTBF.
        for i in range(len(_targets_)):
            self.axAxis1.axhline(y=_targets_[i], xmin=0, color='m',
                                 linewidth=2.5, linestyle=':')

        if(self.optLogarithmic.get_active()):
            self.axAxis1.set_xscale('log')
            self.axAxis1.set_yscale('log')
        else:
            self.axAxis1.set_xscale('linear')
            self.axAxis1.set_yscale('linear')

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'
        for i in range(len(_targets_)):
            self.axAxis1.annotate(str(fmt.format(_targets_[i])),
                                  xy=(ti, 0.9 * _targets_[i]),
                                  xycoords='data',
                                  xytext=(25, -25), textcoords='offset points',
                                  size=12, va="center",
                                  bbox=dict(boxstyle="round",
                                            fc='#E5E5E5',
                                            ec='None',
                                            alpha=0.5),
                                  arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                                  fc='#E5E5E5', ec='None',
                                                  alpha=0.5,
                                                  patchA=None,
                                                  patchB=Ellipse((2, -1), 0.5, 0.5),
                                                  relpos=(0.5, 0.5))
                                  )

# Create the legend.
        _legend_ = tuple(_legend_)
        leg = self.axAxis1.legend(_legend_, 'lower right', shadow=True)
        for t in leg.get_texts():
            t.set_fontsize('small')
        for l in leg.get_lines():
            l.set_linewidth(0.5)

        self.pltPlot1.draw()

        return False

    def _load_hyperlinks(self):
        """
        Method for creating hyperlinks in the Attachment gtk.TextBuffer.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        _text_ = str(_model_.get_value(_row_, self._col_order[14]))

        iter = self.txtAttachment.get_start_iter()
        iter2 = self.txtAttachment.get_end_iter()

        self.txtAttachment.delete(iter, iter2)
        if(_text_ != 'None'):
            self.txtAttachment.insert_with_tags_by_name(iter, _text_ + '\n',
                                                        'hyperlink')

        return False

    def _hyperlink_handler(self, tag, widget, event, iter):
        """
        Method for retrieving the line (hyperlink) that was clicked in the
        Attachment gtk.TextBuffer and opening the link in the default
        application.

        Keyword Arguments:
        tag    -- the gtk.TextTag that called this method.
        widget -- the gtk.TextView that contains the tag calling this method.
        event  -- the mouse button event calling this method.
        iter   -- the gtk.TextIter that called this method.
        """

        import magic

        line_number = iter.get_line()
        start_iter =  self.txtAttachment.get_iter_at_line(line_number)
        end_iter =  self.txtAttachment.get_iter_at_line(line_number + 1)

        _text_ = self.txtAttachment.get_text(start_iter, end_iter,
                                             include_hidden_chars=False)

        if(len(_text_) > 1 and event.type == gtk.gdk.BUTTON_RELEASE):
            mime = magic.Magic(mime=True)
            try:
                print mime.from_file(_text_)
            except IOError:
                _util.application_error(_(u"File %s does not exist" % _text_))

        return False

    def _test_plan_add(self):
        """
        Method to add a new test plan to the open RTK Program database.
        """

        _title_ = _(u"RTK - Add Test Plans")
        _prompt_ = _(u"How many test plans to add?")

#Find the largest test plan ID already in the RTK Program database and
# increment it by one.
        _query_ = "SELECT MAX(fld_test_id) \
                   FROM tbl_tests"
        _max_id_ = self._app.DB.execute_query(_query_,
                                              None,
                                              self._app.ProgCnx)[0][0]
        if(_max_id_ is None or not _max_id_ or _max_id_ == ''):
            _max_id_ = 1001
        else:
            _max_id_ = _max_id_ + 1

# Insert the number of test plans the user has requested.
        _n_test_plans_ = _util.add_items(_title_, _prompt_)
        for i in range(_n_test_plans_):
            _query_ = "INSERT INTO tbl_tests \
                       (fld_revision_id, fld_test_id, fld_test_name) \
                       VALUES(%d, %d, 'Test Plan')" % \
                       (self._app.REVISION.revision_id, _max_id_)
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   True)
            _max_id_ += 1

        self.load_tree()

        return False

    def _test_plan_remove(self):
        """
        Method to remove the selected test plan from the open RTK Program
        database.
        """

        _selection_ = self.treeview.get_selection()
        (_model_, _paths_) = _selection_.get_selected_rows()

        _records_ = []
        for i in range(len(_paths_)):
            _row_ = _model_.get_iter(_paths_[i])
            _records_.append(_model_.get_value(_row_, 1))

        _title_ = _(u"RTK: Confirm Delete")
        _dialog_ = _widg.make_dialog(_title_)

        _fixed_ = gtk.Fixed()

        y_pos = 10

        _label_ = _widg.make_label(_(u"Are you sure you want to delete the selected test plan(s)."), 600, 250)
        _fixed_.put(_label_, 5, y_pos)

        _fixed_.show_all()

        _dialog_.vbox.pack_start(_fixed_)

        response = _dialog_.run()

        if(response == gtk.RESPONSE_ACCEPT):
            for i in range(len(_records_)):
                _query_ = "DELETE FROM tbl_tests \
                           WHERE fld_test_id=%d" % _records_[i]
                _results_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx,
                                                       True)

        _dialog_.destroy()

        self.load_tree()

        return False

    def _mttff_calculator(self, button):
        """
        Method to launch the mean time to first failure calculator.

        Keyword Arguments:
        button -- the gtk.Button() that called this method.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

# Create an assistant for the calculator.
        _dialog_ = _widg.make_dialog(_(u"RTK - Time to First Failure Calculator"))

# Add the labels to the assistant.
        _fixed1_ = gtk.Fixed()
        _fixed2_ = gtk.Fixed()

        _dialog_.vbox.pack_start(_fixed1_)
        _dialog_.vbox.pack_end(_fixed2_)

        _labels_ = [_(u"Starting MTBF:"), _(u"No. of Test Articles:"),
                    _(u"Average Hours/Week/Article:"),
                    _(u"Min. Time to Implement First Fix:"),
                    _(u"Likely Time to Implement First Fix:"),
                    _(u"Max. Time to Implement First Fix:"),
                    _(u"Confidence:")]
        (_x_pos1_, _y_pos1_) = _widg.make_labels(_labels_, _fixed1_, 5, 5)
        _x_pos1_ += 25

        _labels_ = [_(u"Expected Time to First Failure:"),
                    _(u"Time to First Fix:")]
        (_x_pos2_, _y_pos2_) = _widg.make_labels(_labels_, _fixed2_, 5, 5)
        _x_pos2_ += 25
        _x_pos_ = max(_x_pos1_, _x_pos2_)

# Add the user input widgets to the assistant.
        txtMTBFI = _widg.make_entry(_width_=100)
        txtNItems = _widg.make_entry(_width_=100)
        txtHrsWkItem = _widg.make_entry(_width_=100)
        txtA = _widg.make_entry(_width_=100)
        txtM = _widg.make_entry(_width_=100)
        txtB = _widg.make_entry(_width_=100)
        txtConfidence = _widg.make_entry(_width_=100)

        _fixed1_.put(txtMTBFI, _x_pos_, _y_pos1_[0])
        _fixed1_.put(txtNItems, _x_pos_, _y_pos1_[1])
        _fixed1_.put(txtHrsWkItem, _x_pos_, _y_pos1_[2])
        _fixed1_.put(txtA, _x_pos_, _y_pos1_[3])
        _fixed1_.put(txtM, _x_pos_, _y_pos1_[4])
        _fixed1_.put(txtB, _x_pos_, _y_pos1_[5])
        _fixed1_.put(txtConfidence, _x_pos_, _y_pos1_[6])

# Add the results widgets to the assistant.
        txtMTTFF = _widg.make_entry(_width_=100, editable=False)
        txtTTFFLL = _widg.make_entry(_width_=100, editable=False)
        txtTTFFUL = _widg.make_entry(_width_=100, editable=False)

        _fixed2_.put(txtMTTFF, _x_pos_, _y_pos2_[0])
        _fixed2_.put(txtTTFFLL, _x_pos_, _y_pos2_[1])
        _fixed2_.put(txtTTFFUL, _x_pos_ + 105, _y_pos2_[1])

        _dialog_.show_all()

# Run the assistant.
        _response_ = _dialog_.run()
        if(_response_ == gtk.RESPONSE_ACCEPT):
            _mtbfi_ = float(txtMTBFI.get_text())
            _n_items_ = float(txtNItems.get_text())
            _hrs_wk_item_ = float(txtHrsWkItem.get_text())
            _a_ = float(txtA.get_text())
            _m_ = float(txtM.get_text())
            _b_ = float(txtB.get_text())
            _confidence_ = float(txtConfidence.get_text())

            _conf_ = 1.0 - ((100.0 - _confidence_) / 200.0)

            _mean_fix_time_ = (_a_ + 4.0 * _m_ + _b_) / 6.0
            _sd_fix_time_ = (_b_ - _a_) / 6.0
            _fix_timell_ = _mean_fix_time_ - norm.ppf(_conf_) * _sd_fix_time_
            _fix_timeul_ = _mean_fix_time_ + norm.ppf(_conf_) * _sd_fix_time_

            _mttff_ = _mtbfi_ / _n_items_
            _ttffll_ = ((_fix_timell_ + (7.0 * _mtbfi_) / (_n_items_ * _hrs_wk_item_)) * _hrs_wk_item_ * _n_items_) / 7.0
            _ttfful_ = ((_fix_timeul_ + (7.0 * _mtbfi_) / (_n_items_ * _hrs_wk_item_)) * _hrs_wk_item_ * _n_items_) / 7.0

            txtMTTFF.set_text(str(fmt.format(_mttff_)))
            txtTTFFLL.set_text(str(fmt.format(_ttffll_)))
            txtTTFFUL.set_text(str(fmt.format(_ttfful_)))

        else:
            _dialog_.destroy()

        return False

    def _calculate(self, button):
        """
        Method to perform calculations for the TESTING Object.

        Keyword Arguments:
        button -- the gtk.ToolButton that called this method.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        _fix_ = [True, True, True, True, True, True, True]

# Calculate the idealized growth curve.
        MTBFI = _model_.get_value(_row_, 6)
        MTBFF = _model_.get_value(_row_, 7)
        TTT = _model_.get_value(_row_, 16)
        t1 = _model_.get_value(_row_, 20)
        AvgMS = _model_.get_value(_row_, 18)
        AvgGR = _model_.get_value(_row_, 17)
        Prob = _model_.get_value(_row_, 18)
        AvgFEF = _model_.get_value(_row_, 21)
        _alpha_ = self.spnConfidence.get_value() / 100.0

# The following is used to optimize the
        if(self.chkFixProgramProb.get_active()):
            _fix_[0] = True

        if(self.chkFixProgramMS.get_active()):
            _fix_[1] = True

        if(self.chkFixTTFF.get_active()):
            _fix_[2] = True

        if(not self.chkFixTTT.get_active()):
            TTT = ceil(exp(log(t1) + (1.0 / AvgGR) * (log(MTBFF / MTBFI) + log(1.0 - AvgGR))))
            _fix_[3] = False

        if(self.chkFixMTBFI.get_active()):
            _fix_[4] = True

        if(self.chkFixMTBFG.get_active()):
            _fix_[5] = True

        if(not self.chkFixAverageGR.get_active()):
            AvgGR = -log(TTT / t1) - 1.0 + sqrt((1.0 + log(TTT / t1))**2.0 + 2.0 * log(MTBFF / MTBFI))
            _fix_[6] = False

        _model_.set_value(_row_, 6, MTBFI)
        _model_.set_value(_row_, 7, MTBFF)
        _model_.set_value(_row_, 16, TTT)
        _model_.set_value(_row_, 17, AvgGR)
        _model_.set_value(_row_, 18, AvgMS)
        _model_.set_value(_row_, 19, Prob)
        _model_.set_value(_row_, 20, t1)

        self.txtMTBFI.set_text(str(fmt.format(MTBFI)))
        self.txtMTBFG.set_text(str(fmt.format(MTBFF)))
        self.txtTTT.set_text(str(fmt.format(TTT)))
        self.txtAverageGR.set_text(str(fmt.format(AvgGR)))
        self.txtProgramMS.set_text(str(fmt.format(AvgMS)))
        self.txtProgramProb.set_text(str(fmt.format(Prob)))
        self.txtTTFF.set_text(str(fmt.format(t1)))

# Reliability growth planning phase specific calculations.
        model = self.tvwRGPlanDetails.get_model()
        row = model.get_iter_root()
        N0 = 0.0                            # Cumulative number of failures.
        N = [0]                             # Cumulative number of failures per phase,
        TTTi = []                           # Total test time for each phase.
        MTBFAP = []                         # Average planned MTBF.
        while row is not None:
            _T1_ = model.get_value(row, 4)
            MTBFi = model.get_value(row, 6)
            MTBFf = model.get_value(row, 7)
            MTBFa = model.get_value(row, 8)
            (GR, T, MTBFi, MTBFf) = _calc.calculate_rg_phase(_T1_, MTBFi, MTBFf,
                                                             MTBFa, AvgGR,
                                                             AvgMS, AvgFEF,
                                                             Prob, t1, _fix_)

# Update the Tree Book.
            model.set_value(row, 4, T)
            model.set_value(row, 5, GR)
            model.set_value(row, 6, MTBFi)
            model.set_value(row, 7, MTBFf)

# Calculate the expected number of failures for the phase and the average MTBF
# for the phase.
            TTTi.append(T)

            try:
                Ni = ((t1 / MTBFI) * (sum(TTTi) / t1)**(1.0 - GR)) - sum(N)
                M = T / Ni
            except ZeroDivisionError:
                Ni = 0
                M = 0.0

            MTBFAP.append(M)
            N.append(Ni)

            model.set_value(row, 8, M)
            row = model.iter_next(row)

# =========================================================================== #
# Reliability growth assessment calculations.
# =========================================================================== #
# Create lists of the cumulative failure times and number of failures.
        X = []                              # Cumulative failure times.
        F = []                              # Number of failures per interval.
        model = self.tvwTestAssessment.get_model()
        row = model.get_iter_root()
        while row is not None:
            X.append(model.get_value(row, 3))
            F.append(model.get_value(row, 4))
            row = model.iter_next(row)

# If there is actual test data available, estimate reliability growth model
# parameters and create a list of observed failure rate and MTBF values to use
# for plotting.
        _crit_vals_ = []
        if(len(X) > 0 and len(F) > 0):
            if(not self.optGrouped.get_active()):
                (_beta_hat, _lambda_hat,
                 _rho, _mu, _N_,
                 _chi_square_, _Cm_) = _calc.calculate_rgtmc(F, X, 0, False)

            elif(self.optGrouped.get_active()):
                _interval = float(self.txtGroupInterval.get_text())
                (_beta_hat, _lambda_hat,
                 _rho, _mu, _N_,
                 _chi_square_,
                 _Cm_) = _calc.calculate_rgtmc(F, X, _interval, True)

                _crit_vals_.append(chi2.ppf(_alpha_, (TTT / _interval) - 1))
                _crit_vals_.append(chi2.ppf(_alpha_, sum(F) - 2))

            _gr = 1.0 - _beta_hat[-1]
            _rhoi = _lambda_hat[-1] * _beta_hat[-1] * max(TTTi)**(_beta_hat[-1] - 1)
            _rhoc = _rho[-1]
            _mtbfi = 1.0 / _rhoi
            _mtbfc = _mu[-1]

# Load the results.
            _model_.set_value(_row_, 23, max(X))
            _model_.set_value(_row_, 24, sum(F))
            self.txtScale.set_text(str(fmt.format(_lambda_hat[-1])))
            self.txtShape.set_text(str(fmt.format(_beta_hat[-1])))
            self.txtGRActual.set_text(str(fmt.format(_gr)))
            self.txtRhoInst.set_text(str(fmt.format(_rhoi)))
            self.txtRhoC.set_text(str(fmt.format(_rhoc)))
            self.txtMTBFInst.set_text(str(fmt.format(_mtbfi)))
            self.txtMTBFC.set_text(str(fmt.format(_mtbfc)))
            self.txtGoFTrend.set_text(str(fmt.format(_chi_square_)))
            self.txtGoFModel.set_text(str(fmt.format(_Cm_)))

            if(_chi_square_ > _crit_vals_[0]):
                self.lblGoFTrend.set_markup(_(u"<span foreground='green'>Trend</span>"))
            else:
                self.lblGoFTrend.set_markup(_(u"<span foreground='red'>No Trend</span>"))

            if(_Cm_ < _crit_vals_[1]):
                self.lblGoFModel.set_markup(_(u"<span foreground='green'>Good Fit</span>"))
            else:
                self.lblGoFModel.set_markup(_(u"<span foreground='red'>Poor Fit</span>"))

        else:
            _rho = []
            _mu = []

        self._assess_plan_feasibility(TTTi, N)
        self._assessment_tab_load()
        if(self.optMTBF.get_active()):
            self._rg_plot_load(TTTi, MTBFAP, _mu, N)
        elif(self.optFailureIntensity.get_active()):
            self._rg_plot_load(TTTi, MTBFAP, _rho, N)

        return False

    def _assess_plan_feasibility(self, TTT, N):
        """
        Method to assess the feasibility of a test plan.

        Keyword Arguments:
        TTT -- a list of the test times for each test phase.
        N   -- a list of the number of failures expected in each test phase.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _test_type_ = self.cmbTestType.get_active()

# =========================================================================== #
# Reliability growth planning feasibility assessment.
# The assessment criteria come from MIL-HDBK-189C.
# =========================================================================== #
        if(_test_type_ == 5):
            MTBFI = float(self.txtMTBFI.get_text())
            MTBFG = float(self.txtMTBFG.get_text())
            MTBFGP = float(self.txtMTBFGP.get_text())
            TR = float(self.txtTechReq.get_text())
            GR = float(self.txtAverageGR.get_text())
            FEF = float(self.txtAverageFEF.get_text())
            MS = float(self.txtProgramMS.get_text())

# Initial MTBF to growth potential MTBF ratio is high enough.  Too low means
# growth testing is being started too early.
            self.txtMIMGP.set_text(str(fmt.format(MTBFI/MTBFGP)))
            if(MTBFI/MTBFGP >= 0.15 and MTBFI/MTBFGP <= 0.47):
                self.chkMIMGP.set_active(True)
            else:
                self.chkMIMGP.set_active(False)

            if(MTBFI/MTBFGP >= 0.35):
                _text = "<span foreground='#00CC00'>Low Risk</span>"
            elif(MTBFI/MTBFGP < 0.35 and MTBFI/MTBFGP >= 0.2):
                _text = "<span foreground='yellow'>Medium Risk</span>"
            else:
                _text = "<span foreground='red'>High Risk</span>"
            self.lblMIMGP.set_markup(_text)

            self.txtMGMGP.set_text(str(fmt.format(MTBFG/MTBFGP)))
            if(MTBFG/MTBFGP >= 0.6 and MTBFG/MTBFGP <= 0.8):
                self.chkMGMGP.set_active(True)
            else:
                self.chkMGMGP.set_active(False)

            if(MTBFG/MTBFGP <= 0.7):
                _text = "<span foreground='#00CC00'>Low Risk</span>"
            elif(MTBFG/MTBFGP > 0.7 and MTBFG/MTBFGP <= 0.8):
                _text = "<span foreground='yellow'>Medium Risk</span>"
            else:
                _text = "<span foreground='red'>High Risk</span>"
            self.lblMGMGP.set_markup(_text)

            self.txtTRMG.set_text(str(fmt.format(MTBFG/MTBFI)))
            if(MTBFG/MTBFI >= 2.0 and MTBFG/MTBFI <= 3.0):
                self.chkTRMG.set_active(True)
            else:
                self.chkTRMG.set_active(False)

            if(MTBFG/MTBFI <= 2.0):
                _text = "<span foreground='#00CC00'>Low Risk</span>"
            elif(MTBFG/MTBFI > 2.0 and MTBFG/MTBFI <= 3.0):
                _text = "<span foreground='yellow'>Medium Risk</span>"
            else:
                _text = "<span foreground='red'>High Risk</span>"
            self.lblMGMI.set_markup(_text)

            self.txtFEF.set_text(str(fmt.format(FEF)))
            if(FEF >= 0.55 and FEF <= 0.85):
                self.chkFEF.set_active(True)
            else:
                self.chkFEF.set_active(False)

            if(FEF <= 0.7):
                _text = "<span foreground='#00CC00'>Low Risk</span>"
            elif(FEF > 0.7 and FEF <= 0.8):
                _text = "<span foreground='yellow'>Medium Risk</span>"
            else:
                _text = "<span foreground='red'>High Risk</span>"
            self.lblFEF.set_markup(_text)

# Reliability growth planning feasibility per phase.
            i = 0
            model = self.tvwTestFeasibility.get_model()
            row = model.get_iter_root()
            while row is not None:
                _articles = model.get_value(row, 1)

                _tpu = TTT[i] / _articles
                _dt_start = datetime.strptime(model.get_value(row, 2),"%Y-%m-%d").toordinal()
                _dt_end = datetime.strptime(model.get_value(row, 3),"%Y-%m-%d").toordinal()
                _weeks = (_dt_end - _dt_start) / 7.0
                _tpupw = _tpu / _weeks

                model.set_value(row, 4, ceil(N[i + 1] - N[i]))
                model.set_value(row, 7, _tpu)
                model.set_value(row, 8, _tpupw)

                i += 1
                row = model.iter_next(row)

            if(i >= 6):
                _text = "<span foreground='#00CC00'>Low Risk</span>"
            elif(i < 6 and i >= 4):
                _text = "<span foreground='yellow'>Medium Risk</span>"
            else:
                _text = "<span foreground='red'>High Risk</span>"

        return False

    def test_plan_save(self, button):
        """
        Saves the TESTING Object gtk.TreeView information to the Program's
        MySQL or SQLite3 database.

        Keyword Arguments:
        button -- the gtk.Button widget that called this function.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

# Find the notebook page that is currently selected.  We only save the
# information associated with the currently selected page.
        _page = self.notebook.get_current_page()

# Find the test type so we can save the contents of any gtk.TreeView
# associated specifically with the selected type of test.
        _test_type = _model_.get_value(_row_, 4)

        self.model.foreach(self._save_line_item)
        if(_test_type == 5):                # Reliability growth.
            model = self.tvwRGPlanDetails.get_model()
            model.foreach(self._save_rg_phases)

            model = self.tvwTestFeasibility.get_model()
            model.foreach(self._save_rg_feasibility)

        if(_page == 2):                     # Observed data.
            model = self.tvwTestAssessment.get_model()
            model.foreach(self._save_rg_data)

        return False

    def _save_line_item(self, model, path_, row):
        """
        Saves each row in the TESTING Object treeview model to the RTK's
        Program MySQL or SQLite3 database.

        Keyword Arguments:
        model -- the TESTING gtk.ListStore.
        path_ -- the path of the active row in the TESTING gtk.ListStore.
        row   -- the selected row in the TESTING gtk.TreeView.
        """

        values = (model.get_value(row, self._col_order[1]), \
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
                  model.get_value(row, self._col_order[14]), \
                  model.get_value(row, self._col_order[15]), \
                  model.get_value(row, self._col_order[16]), \
                  model.get_value(row, self._col_order[17]), \
                  model.get_value(row, self._col_order[18]), \
                  model.get_value(row, self._col_order[19]), \
                  model.get_value(row, self._col_order[20]), \
                  model.get_value(row, self._col_order[21]), \
                  model.get_value(row, self._col_order[22]), \
                  model.get_value(row, self._col_order[23]), \
                  model.get_value(row, self._col_order[24]), \
                  model.get_value(row, self._col_order[25]), \
                  model.get_value(row, self._col_order[26]), \
                  model.get_value(row, self._col_order[2]), \
                  model.get_value(row, self._col_order[0]))

        query = "UPDATE tbl_tests \
                 SET fld_assembly_id=%d, fld_test_name='%s', \
                     fld_test_description='%s', fld_test_type=%d, \
                     fld_mi=%f, fld_mg=%f, fld_mgp=%f, fld_tr=%f, \
                     fld_consumer_risk=%f, fld_producer_risk=%f, \
                     fld_rg_plan_model=%d, fld_rg_assess_model=%d, \
                     fld_num_phases=%d, fld_attachment='%s', \
                     fld_ttt=%f, fld_avg_growth=%f, fld_avg_ms=%f, \
                     fld_prob=%f, fld_ttff=%f, fld_avg_fef=%f, \
                     fld_grouped=%d, fld_group_interval=%f, fld_cum_time=%f, \
                     fld_cum_failures=%d, fld_confidence=%f \
                 WHERE fld_test_id=%d \
                 AND fld_revision_id=%d" % values

        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("testing.py: Failed to save test plan.")
            return True

        return False

    def _save_rg_phases(self, model, path_, row):
        """
        Method to save the reliability growth phase information.

        Keyword Arguments:
        model -- the TESTING Object reliability growth phase gtk.ListStore.
        path_ -- the path of the active row in the TESTING Object reliability
                 growth phase gtk.ListStore.
        row   -- the gtk.Iter of the active row in the TESTING Object
                 reliability growth phase gtk.TreeView.
        """

        _dt_start = datetime.strptime(model.get_value(row, 2),"%Y-%m-%d").toordinal()
        _dt_end = datetime.strptime(model.get_value(row, 3),"%Y-%m-%d").toordinal()
        _values_ = (model.get_value(row, 1), _dt_start, _dt_end, \
                    model.get_value(row, 4), model.get_value(row, 5), \
                    model.get_value(row, 6), model.get_value(row, 7), \
                    model.get_value(row, 8), model.get_value(row, 0), \
                    self.test_id)

        _query_ = "UPDATE tbl_rel_growth \
                   SET fld_test_units=%d, fld_start_date='%s', fld_end_date='%s', \
                       fld_test_time=%f, fld_growth_rate=%f, fld_mi=%f, \
                       fld_mf=%f, fld_ma=%f \
                   WHERE fld_phase_id=%d \
                   AND fld_test_id=%d" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("testing.py: Failed to save reliability growth phase information.")
            return True

        return False

    def _save_rg_feasibility(self, model, path_, row):
        """
        Method to save the reliability growth phase feasibility information.

        Keyword Arguments:
        model -- the TESTING Object reliability growth phase feasibility
                 gtk.ListStore.
        path_ -- the path of the active row in the TESTING Object reliability
                 growth phase feasibility gtk.ListStore.
        row   -- the gtk.Iter of the active row in the TESTING Object
                 reliability growth phase feasibility gtk.TreeView.
        """

        values = (model.get_value(row, 4), model.get_value(row, 5), \
                  model.get_value(row, 6), model.get_value(row, 7), \
                  model.get_value(row, 8), model.get_value(row, 0), \
                  self.test_id)

        query = "UPDATE tbl_rel_growth \
                 SET fld_num_fails=%f, fld_ms=%f, fld_fef_avg=%f, fld_tpu=%f, \
                     fld_tpupw=%f \
                 WHERE fld_phase_id=%d \
                 AND fld_test_id=%d" % values

        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("testing.py: Failed to save reliability growth phase feasibility information.")
            return True

        return False

    def _save_rg_data(self, model, path_, row):
        """
        Method to save the reliability growth testing field data.

        Keyword Arguments:
        model -- the TESTING Object reliability growth field data
                 gtk.ListStore.
        path_ -- the path of the active row in the TESTING Object reliability
                 growth field data gtk.ListStore.
        row   -- the gtk.Iter of the active row in the TESTING Object
                 reliability growth field data gtk.TreeView.
        """

        _date_ = datetime.strptime(model.get_value(row, 1), '%Y-%m-%d').toordinal()
        _values_ = (_date_, model.get_value(row, 2), \
                    model.get_value(row, 3), model.get_value(row, 4), \
                    model.get_value(row, 0), self.test_id)

        _query_ = "UPDATE tbl_survival_data \
                   SET fld_request_date=%d, fld_left_interval=%f, \
                       fld_right_interval=%f, fld_quantity=%d \
                   WHERE fld_record_id=%d \
                   AND fld_dataset_id=%d" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("testing.py: Failed to save reliability growth field data.")
            return True

        return False

    def _callback_check(self, check, index):
        """
        Callback function to retrieve and save checkbutton changes.

        Keyword Arguments:
        check  -- the checkbutton that called the function.
        index_ -- the position in the Assembly Object _attribute list
                  associated with the data from the calling checkbutton.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

# Update the Hardware Tree.
        if(index == 22):
            if(self.optIndividual.get_active()):
                _model_.set_value(_row_, index, 0)
            else:
                _model_.set_value(_row_, index, 1)

        else:
            _model_.set_value(_row_, index, check.get_active())

        return False

    def _callback_combo(self, combo, _index_):
        """
        Callback function to retrieve and save combobox changes.

        Keyword Arguments:
        combo   -- the combobox that called the function.
        _index_ -- the position in the DATASET Object _attribute list
                   associated with the data from the calling combobox.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        _text_ = combo.get_active()

        # _index_   Field
        #    1      Assembly ID
        #    5      Test Type
        #   12      RG Planning Model
        #   13      RG Assessment Model
        if(_index_ == 1):
            model = combo.get_model()
            row = combo.get_active_iter()
            if(row is not None):
                _text_ = int(model.get_value(row, 1))
            else:
                _text_ = 0
        else:
            _text_ = combo.get_active()

# If we've selected a new type of test, make sure we display the correct
# detailed planning information.
        if(_index_ == 5):
            if(_text_ == 1):                # HALT
                _label_ = _(u"Highly Accelerated Life Test Planning Inputs")
            elif(_text_ == 2):              # HASS
                _label_ = _(u"Highly Accelerated Stress Screening Planning Inputs")
            elif(_text_ == 3):              # ALT
                _label_ = _(u"Accelerated Life Test Planning Inputs")
            elif(_text_ == 4):              # ESS
                _label_ = _(u"Environmental Stress Screening Planning Inputs")
            elif(_text_ == 5):              # Reliability Growth
                self._rg_plan_details(1)
            elif(_text_ == 6):              # Reliability Demonstration
                _label_ = _(u"Reliability Demonstration/Qualification Test Planning Inputs")
            elif(_text_ == 7):              # PRVT
                _label_ = _(u"Production Reliability Verification Test Planning Inputs")

# Try to update the gtk.TreeModel.  Just keep going if no row is selected.
        try:
            _model_.set_value(_row_, _index_, _text_)
        except TypeError:
            pass

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

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        if(convert == 'text'):
            if(_index_ == self._col_order[4]):
                _bounds = self.txtDescription.get_bounds()
                _text_ = self.txtDescription.get_text(_bounds[0], _bounds[1])
            elif(_index_  == self._col_order[15]):
                _bounds = self.txtAttachment.get_bounds()
                _text_ = self.txtAttachment.get_text(_bounds[0], _bounds[1])
            else:
                _text_ = entry.get_text()

        elif(convert == 'int'):
            try:
                _text_ = int(entry.get_text())
            except ValueError:
                _text_ = 0

        elif(convert == 'float'):
            try:
                _text_ = float(entry.get_text().replace('$', ''))
            except ValueError:
                _text_ = 0.0

        elif(convert == 'date'):
            _text_ = datetime.strptime(entry.get_text(), '%Y-%m-%d').toordinal()

# Try to update the gtk.TreeModel.  Just keep going if no row is selected.
        try:
            _model_.set_value(_row_, _index_, _text_)
        except TypeError:
            pass

        if(_index_ == 13):
            self._rg_plan_details(2)

        return False

    def _callback_radio(self, button):
        """
        Callback function to retrieve and save gtk.RadioButton changes for the
        TESTING Object.

        Keyword Arguments:
        button  -- the gtk.RadioButton that called the function.
        _index_ -- the position in the TESTING Object _attribute list
                   associated with the data from the calling gtk.RadioButton.
        """

        if(button.get_name() == 'linear'):
            self.axAxis1.set_xscale('linear')
            self.axAxis1.set_yscale('linear')
            self.pltPlot1.draw()
        elif(button.get_name() == 'log'):
            self.axAxis1.set_xscale('log')
            self.axAxis1.set_yscale('log')
            self.pltPlot1.draw()

        return False

    def _callback_spin(self, spin, _index_):
        """
        Callback function to retrieve and save gtk.SpinButton changes for the
        TESTING Object.

        Keyword Arguments:
        spin    -- the gtk.SpinButton that called the function.
        _index_ -- the position in the YESTING Object _attribute list
                   associated with the data from the calling gtk.SpinButton.
        """

        _value_ = spin.get_value_as_int()

        if(_index_ == 14 and self.test_id > 1000):  # Number of RG phases.
# Find the last number number of existing phases.
            query = "SELECT MAX(fld_phase_id) \
                     FROM tbl_rel_growth \
                     WHERE fld_test_id=%d" % self.test_id
            _phases = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx)

            if(not _phases[0][0] or _phases[0][0] is None):
                self.n_phases = 0
            else:
                self.n_phases = int(_phases[0][0])

# If spinning down, delete the phases starting with the last phase.
            if(_value_ < self.n_phases):
                _diff_ = self.n_phases - _value_
                for i in range(_diff_):
                    query = "DELETE FROM tbl_rel_growth \
                             WHERE fld_test_id=%d \
                             AND fld_phase_id=%d" % \
                            (self.test_id, self.n_phases)
                    results = self._app.DB.execute_query(query,
                                                         None,
                                                         self._app.ProgCnx,
                                                         commit=True)
# If spinning up, add phases until the number of phases is equal to the
# spinner value.
            elif(_value_ > self.n_phases):
                _diff_ = _value_ - self.n_phases
                for i in range(_diff_):
                    query = "INSERT INTO tbl_rel_growth \
                             (fld_test_id, fld_phase_id) \
                             VALUES(%d, %d)" % \
                            (self.test_id, i + self.n_phases + 1)
                    results = self._app.DB.execute_query(query,
                                                         None,
                                                         self._app.ProgCnx,
                                                         commit=True)

            self._load_rg_plan_tree()
            self._load_rg_feasibility_tree()

# Try to update the gtk.TreeModel.  Just keep going if no row is selected.
        try:
            (_model_, _row_) = self.treeview;get_selection().get_selected()
            _model_.set_value(_row_, _index_, _value_)
        except ValueError:
            pass
        except TypeError:
            pass

        return False

    def _toolbutton_pressed(self, widget):
        """
        Method to reacte to the SOFTWARE Object toolbar button clicked events.

        Keyword Arguments:
        widget -- the toolbar button that was pressed.
        """

        _button_ = widget.get_name()
        _page_ = self.notebook.get_current_page()

        if(_page_ == 0):                    # Planning inputs
            if(_button_ == 'Add'):
                self._test_plan_add()
            elif(_button_ == 'Remove'):
                self._test_plan_remove()
        elif(_page_ == 1):                  # Test feasibility
            if(_button_ == 'Add'):
                self._test_plan_add()
            elif(_button_ == 'Remove'):
                self._test_plan_remove()
        elif(_page_ == 2):                  # Test assessment
            if(_button_ == 'Add'):
                AddRGRecord(self._app)

        return False

    def _notebook_page_switched(self, notebook, page, page_num):
        """
        Called whenever the Tree Book notebook page is changed.

        Keyword Arguments:
        notebook -- the Tree Book notebook widget.
        page     -- the newly selected page widget.
        page_num -- the newly selected page number.
                    0 = General Data
                    1 = Allocation
                    2 = Hazard Analysis
        """

        self._selected_tab = page_num

        #if(page_num == 0):                  # General data tab.

        return False

    def _rg_plan_details(self, _index_):

        if(_index_ == 1):
            if(self.fraPlanDetails.get_child() is not None):
                self.fraPlanDetails.remove(self.fraPlanDetails.get_child())

            self.fraPlanDetails.add(self.fxdRGPlanDetails)
            self.fraPlanDetails.show_all()

            label = self.fraPlanDetails.get_label_widget()
            _label_ = _(u"Reliability Growth Test Planning Inputs")

        elif(_index_ == 2):
            if(self.fraPlanDetails2.get_child() is not None):
                self.fraPlanDetails2.remove(self.fraPlanDetails2.get_child())

            self.fraPlanDetails2.add(self.scwRGPlanDetails)
            self.fraPlanDetails2.show_all()

            label = self.fraPlanDetails2.get_label_widget()
            _label_ = _(u"Reliability Growth Test Phase Inputs")

        label.set_markup("<span weight='bold'>" +
                         _label_ + "</span>")
        label.set_justify(gtk.JUSTIFY_LEFT)
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.show_all()

        return False

    def _treeview_clicked(self, treeview, event, idx):
        """
        Callback function for handling mouse clicks on the Testing Object
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
        idx      -- an index number for the treeview:
                    0 = main treeview
                    1 = detailed RG plan treeview
                    2 = RG plan feasibility treeview
        """

        _x_ = int(event.x)
        _y_ = int(event.y)
        _pathinfo_ = treeview.get_path_at_pos(_x_, _y_)
        if(_pathinfo_ is not None):
            (_path_, _column_, _x_, _y_) = _pathinfo_
            treeview.grab_focus()
            treeview.set_cursor(_path_, _column_, False)

            if(idx == 0):
                if(event.button == 1):
                    self._treeview_row_changed(treeview, _path_, _column_, idx)

            elif(idx == 1):
                if(event.button == 3):
                    (_model_, _row_) = treeview.get_selection().get_selected()

                    _phase_id_ = _model_.get_value(_row_, 0)
                    if(_column_.get_widget().get_text() == 'Start Date'):
                        _date_ = _util.date_select(None)
                        _model_.set_value(_row_, 2, _date_)
                        self._dic_rg_plan[_phase_id_][2] = _date_

                        _model_ = self.tvwTestFeasibility.get_model()
                        _row_ = _model_.get_iter_from_string(
                                        self._dic_rg_plan[_phase_id_][9])
                        _model_.set_value(_row_, 2, _date_)
                    elif(_column_.get_widget().get_text() == 'End Date'):
                        _date_ = _util.date_select(None)
                        _model_.set_value(_row_, 3, _date_)
                        self._dic_rg_plan[_phase_id_][3] = _date_

                        _model_ = self.tvwTestFeasibility.get_model()
                        _row_ = _model_.get_iter_from_string(
                                        self._dic_rg_plan[_phase_id_][9])
                        _model_.set_value(_row_, 3, _date_)

            elif(idx == 2):
                if(event.button == 3):
                    (_model_, _row_) = treeview.get_selection().get_selected()

                    _phase_id_ = _model_.get_value(_row_, 0)
                    if(_column_.get_widget().get_text() == 'Start Date'):
                        _date_ = _util.date_select(None)
                        _model_.set_value(_row_, 2, _date_)
                        self._dic_rg_plan[_phase_id_][2] = _date_

                        _model_ = self.tvwRGPlanDetails.get_model()
                        _row_ = _model_.get_iter_from_string(
                                        self._dic_rg_plan[_phase_id_][8])
                        _model_.set_value(_row_, 2, _date_)
                    elif(_column_.get_widget().get_text() == 'End Date'):
                        _date_ = _util.date_select(None)
                        _model_.set_value(_row_, 3, _date_)
                        self._dic_rg_plan[_phase_id_][3] = _date_

                        _model_ = self.tvwRGPlanDetails.get_model()
                        _row_ = _model_.get_iter_from_string(
                                        self._dic_rg_plan[_phase_id_][8])
                        _model_.set_value(_row_, 3, _date_)

        return False

    def _treeview_row_changed(self, treeview, path, column, idx):
        """
        Callback function to handle events for the TESTING Object
        gtk.Treeview.  It is called whenever the Incident Object treeview is
        clicked or a row is activated.

        Keyword Arguments:
        treeview -- the Incident Object gtk.TreeView.
        path     -- the actived row gtk.TreeView path.
        column   -- the actived gtk.TreeViewColumn.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()
        if _row_ is not None:
            self.test_id = _model_.get_value(_row_, 1)
            self.n_phases = _model_.get_value(_row_, 13)
            self.load_notebook()

            return False
        else:
            return True

    def _rg_plan_edit(self, cell, path, new_text, position):
        """
        Callback function when editing a gtkCellRenderer() in the RG plan
        details gtk.TreeView()
        """

        _model_ = self.tvwRGPlanDetails.get_model()
        _row_ = _model_.get_iter_from_string(path)

        _widg.edit_tree(cell, path, new_text, position, _model_)

# Update the dictionary containing the RG Plan details.
        if _row_ is not None:
            _phase_id_ = _model_.get_value(_row_, 0)
            self._dic_rg_plan[_phase_id_][0] = _model_.get_value(_row_, 1)
            self._dic_rg_plan[_phase_id_][3] = _model_.get_value(_row_, 4)
            self._dic_rg_plan[_phase_id_][4] = _model_.get_value(_row_, 5)
            self._dic_rg_plan[_phase_id_][5] = _model_.get_value(_row_, 6)
            self._dic_rg_plan[_phase_id_][6] = _model_.get_value(_row_, 7)

# Now update the RG plan feasibility gtk.Treeview().
            _model_ = self.tvwTestFeasibility.get_model()
            _path_ = self._dic_rg_plan[_phase_id_][9]
            _row_ = _model_.get_iter_from_string(_path_)
            _model_.set_value(_row_, 1, self._dic_rg_plan[_phase_id_][0])

        return False

    def _rg_feasibility_edit(self, cell, path, new_text, position):
        """
        Callback function when editing a gtkCellRenderer() in the RG plan
        details gtk.TreeView()
        """

        _model_ = self.tvwTestFeasibility.get_model()
        _row_ = _model_.get_iter_from_string(path)

        _widg.edit_tree(cell, path, new_text, position, _model_)

# Update the dictionary containing the RG Plan details.
        if _row_ is not None:
            _phase_id_ = _model_.get_value(_row_, 0)
            self._dic_rg_plan[_phase_id_][0] = _model_.get_value(_row_, 1)

# Now update the RG plan details gtk.Treeview().
            _model_ = self.tvwRGPlanDetails.get_model()
            _path_ = self._dic_rg_plan[_phase_id_][8]
            _row_ = _model_.get_iter_from_string(_path_)
            _model_.set_value(_row_, 1, self._dic_rg_plan[_phase_id_][0])

        return False

    def create_tree(self):
        """
        Creates the TESTING treeview and connects it to callback functions to
        handle editting.  Background and foreground colors can be set using the
        user-defined values in the RTK configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()
        bg_color = _conf.RTK_COLORS[10]
        fg_color = _conf.RTK_COLORS[11]
        (self.treeview, self._col_order) = _widg.make_treeview('Testing', 11,
                                                               self._app,
                                                               None,
                                                               bg_color,
                                                               fg_color)
        self.treeview.set_enable_tree_lines(True)

        self.treeview.set_tooltip_text(_(u"Displays a list of program reliability tests."))

        scrollwindow.add(self.treeview)
        self.model = self.treeview.get_model()

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None, 0)
        self.treeview.connect('row_activated', self._treeview_row_changed, 0)

        return(scrollwindow)

    def _load_rg_plan_tree(self):
        """
        Method to load the TESTING Object reliability growth detailed plan
        gtk.TreeView.
        """

        query = "SELECT fld_phase_id, fld_test_units, fld_start_date, \
                        fld_end_date, fld_test_time, fld_growth_rate, fld_mi, \
                        fld_mf, fld_ma \
                 FROM tbl_rel_growth \
                 WHERE fld_test_id=%d" % self.test_id
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)
        if(results == '' or not results):
            return True

        self.n_phases = len(results)

        model = self.tvwRGPlanDetails.get_model()
        model.clear()
        for i in range(self.n_phases):
            try:
                _dt_start = str(datetime.fromordinal(int(results[i][2])).strftime('%Y-%m-%d'))
            except TypeError:
                _dt_start = datetime.today().strftime('%Y-%m-%d')
            try:
                _dt_end = str(datetime.fromordinal(int(results[i][3])).strftime('%Y-%m-%d'))
            except TypeError:
                _dt_end = datetime.today().strftime('%Y-%m-%d')
            _data = [results[i][0], results[i][1], _dt_start, _dt_end,
                     results[i][4], results[i][5], results[i][6],
                     results[i][7], results[i][8]]
            _row_ = model.append(_data)
            _path_ = model.get_string_from_iter(_row_)
            self._dic_rg_plan[results[i][0]] = [results[i][1], _dt_start,
                                                _dt_end, results[i][4],
                                                results[i][5], results[i][6],
                                                results[i][7], results[i][8],
                                                _path_, '0']

        self.tvwRGPlanDetails.expand_all()
        self.tvwRGPlanDetails.set_cursor('0', None, False)
        root = model.get_iter_root()
        if root is not None:
            path = model.get_path(root)
            col = self.tvwRGPlanDetails.get_column(0)
            self.tvwRGPlanDetails.row_activated(path, col)

        return False

    def _load_rg_feasibility_tree(self):
        """
        Method to load the TESTING Object reliability growth plan feasibility
        gtk.TreeView.
        """

        query = "SELECT fld_phase_id, fld_test_units, fld_start_date, \
                        fld_end_date, fld_num_fails, fld_ms, fld_fef_avg, \
                        fld_tpu, fld_tpupw \
                 FROM tbl_rel_growth \
                 WHERE fld_test_id=%d" % self.test_id
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)
        self.n_phases = len(results)

        if(results == '' or not results):
            return True

        self.n_phases = len(results)

        model = self.tvwTestFeasibility.get_model()
        model.clear()
        for i in range(self.n_phases):
            try:
                _dt_start = str(datetime.fromordinal(int(results[i][2])).strftime('%Y-%m-%d'))
            except TypeError:
                _dt_start = datetime.today().strftime('%Y-%m-%d')
            try:
                _dt_end = str(datetime.fromordinal(int(results[i][3])).strftime('%Y-%m-%d'))
            except TypeError:
                _dt_end = datetime.today().strftime('%Y-%m-%d')
            _data = [results[i][0], results[i][1], _dt_start, _dt_end,
                     results[i][4], results[i][5], results[i][6],
                     results[i][7], results[i][8]]
            _row_ = model.append(_data)
            _path_ = model.get_string_from_iter(_row_)
            self._dic_rg_plan[results[i][0]][9] = _path_

        self.tvwTestFeasibility.expand_all()
        self.tvwTestFeasibility.set_cursor('0', None, False)
        root = model.get_iter_root()
        if root is not None:
            path = model.get_path(root)
            col = self.tvwRGPlanDetails.get_column(0)
            self.tvwTestFeasibility.row_activated(path, col)

        return False

    def _load_test_assessment_tree(self):
        """
        Method to load the TESTING Object test data gtk.TreeView.
        """

        query = "SELECT fld_record_id, fld_request_date, fld_left_interval, \
                        fld_right_interval, fld_quantity \
                 FROM tbl_survival_data \
                 WHERE fld_dataset_id=%d" % self.test_id
        _results = self._app.DB.execute_query(query,
                                              None,
                                              self._app.ProgCnx,
                                              commit=False)

        _n_records = len(_results)

        model = self.tvwTestAssessment.get_model()
        model.clear()
        for i in range(_n_records):
            _date_ = str(datetime.fromordinal(int(_results[i][1])).strftime('%Y-%m-%d'))
            model.append([_results[i][0], _date_, _results[i][2],
                          _results[i][3], _results[i][4]])

        self.tvwTestAssessment.set_cursor('0', None, False)
        root = model.get_iter_root()
        if root is not None:
            path = model.get_path(root)
            col = self.tvwRGPlanDetails.get_column(0)
            self.tvwRGPlanDetails.row_activated(path, col)

        return False

    def load_tree(self):
        """
        Loads the TESTING treeview model with system information.  This
        information can be stored either in a MySQL or SQLite3 database.
        """

        _query_ = "SELECT * FROM tbl_tests \
                   WHERE fld_revision_id=%d" % self._app.REVISION.revision_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)
        if(_results_ is None or _results_ == '' or not _results_):
            return True

        self.n_tests = len(_results_)

        self.model.clear()

# Load the model with the returned results.
        for i in range(self.n_tests):
            self.model.append(None, _results_[i])

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        root = self.model.get_iter_root()
        if root is not None:
            path = self.model.get_path(root)
            col = self.treeview.get_column(0)
            self.treeview.row_activated(path, col)

# Load the Assembly combo.
        _query_ = "SELECT fld_name, fld_assembly_id, fld_description \
                   FROM tbl_system \
                   WHERE fld_revision_id=%d" % self._app.REVISION.revision_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)
        _widg.load_combo(self.cmbAssembly, _results_, simple=False)
        for i in range(len(_results_)):
            self._dic_assemblies[_results_[i][1]] = i + 1

        return False

    def load_notebook(self):
        """
        Method to load the TESTING Object gtk.Notebook.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()
        if(_row_ is not None):
            self._planning_tab_load()
            self._assessment_tab_load()

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxTesting)
        self._app.winWorkBook.show_all()

        _title = _(u"RTK Work Book: Program Reliability Testing (%d Tests)") % \
                   self.n_tests
        self._app.winWorkBook.set_title(_title)

# Load the test assessment tree.
        self._load_test_assessment_tree()

        self.notebook.set_current_page(0)

        return False
