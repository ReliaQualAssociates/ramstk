#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to
Program testing plans.
"""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2013 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       testing.py is part of The RelKit Project
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

# Import other RelKit modules.
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


class Testing:
    """
    The Testing class is used to represent the reliability test plans
    associated with the system being analyzed.
    """

    _pi_tab_labels = [_("Assembly:"), _("Test Title:"), _("Test Description:"),
                      _("Test Type:"),
                      _("Initial Program MTBF (MTBF<sub>I</sub>):"),
                      _("Program Goal MTBF (MTBF<sub>G</sub>):"),
                      _("Potential Mature MTBF (MTBF<sub>GP</sub>):"),
                      _("Program Required MTBF (MTBF<sub>TR</sub>):"),
                      _("Producer Risk:"), _("Consumer Risk"),
                      _("RG Plan Model:"), _("RG Assessment Model:"),
                      _("Number of Phases:"), _("Attachments:"),
                      _(u"Total Test Time:"), _(u"Average Growth Rate:"),
                      _(u"Average FEF:"), _(u"Program MS:"),
                      _(u"Program Probability:"),
                      _(u"Time to First Fix (t<sub>1</sub>):")]

    _rg_plan_labels = [_(u"Phase"), _(u"Test\nArticles"), _(u"Start Date"),
                       _(u"End Date"), _(u"Total Time"), _(u"Growth Rate"),
                       _(u"Initial MTBF"), _(u"Final MTBF"),
                       _(u"Average MTBF")]

    _test_assess_labels = [_(u"Record\nNumber"), _(u"Interval\nStart"),
                           _(u"Interval\nEnd"), _(u"Number\nof\nFailures")]

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
        application -- the RelKit application.
        """

        self._ready = False

        self._app = application

        self.treeview = None
        self.model = None
        self.selected_row = None
        self.test_id = 0
        self.n_tests = 0
        self.n_phases = 0
        self._col_order = []

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

        self.spnNumPhases =gtk.SpinButton()

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

        if self._planning_widgets_create():
            self._app.debug_log.error("testing.py: Failed to create Planning Input widgets.")
        if self._planning_tab_create():
            self._app.debug_log.error("testing.py: Failed to create Planning Input tab.")

# =========================================================================== #
# Create the Test Feasibility widgets.
# =========================================================================== #
        height = (self._app.winWorkBook.height * 0.01) / 2.0
        width = (self._app.winWorkBook.width * 0.01) / 2.0

        self.chkMIMGP = _widg.make_check_button(_label_=_(u"Acceptable MTBF<sub>I</sub> / MTBF<sub>GP</sub>."))
        self.chkMIMGP.set_tooltip_text(_(u"Indicates whether or not the initial MTBF to mature MTBF ratio is within historical limits."))

        self.chkFEF = _widg.make_check_button(_label_=_(u"Acceptable average fix effectiveness factor (FEF)."))
        self.chkFEF.set_tooltip_text(_(u"Indicates whether or not the average fix effectiveness factor (FEF) is within historical limits."))

        self.chkMGMGP = _widg.make_check_button(_label_=_(u"Acceptable MTBF<sub>G</sub> / MTBF<sub>GP</sub>."))
        self.chkMGMGP.set_tooltip_text(_(u"Indicates whether or not the goal MTBF to mature MTBF ratio is within historical limits."))

        self.chkTRMG = _widg.make_check_button(_label_=_(u"Acceptable MTBF<sub>G</sub> / MTBF<sub>TR</sub>."))
        self.chkTRMG.set_tooltip_text(_(u"Indicates whether or not the technical requirement MTBF to goal MTBF ratio is within historical limits."))

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
        self.optIndividual.connect('toggled', self._callback_radio)

        self.optGrouped = gtk.RadioButton(group=self.optIndividual,
                                          label=_(u"Grouped Failure Time Data"))
        self.optGrouped.set_tooltip_text(_(u"Estimate parameters based on grouped failures times."))
        self.optGrouped.set_name('grouped')
        self.optGrouped.connect('toggled', self._callback_radio)

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

        self.txtGroupInterval = _widg.make_entry(_width_=100)
        self.txtGroupInterval.set_tooltip_text(_(u"Displays the width of the grouping intervals if using Option for Grouped Data."))

# Widgets to display the estimated parameters for the selected model.
        self.txtScale = _widg.make_entry(_width_=100)
        self.txtScale.set_tooltip_text(_(u"Displays the reliability growth model estimated scale parameter."))

        self.txtShape = _widg.make_entry(_width_=100)
        self.txtShape.set_tooltip_text(_(u"Displays the reliability growth model estimated shape parameter."))

        self.txtGRActual = _widg.make_entry(_width_=100)
        self.txtGRActual.set_tooltip_text(_(u"Displays the average growth rate over the reliability growth program to date."))

        self.txtRhoInst = _widg.make_entry(_width_=100)
        self.txtRhoInst.set_tooltip_text(_(u"Displays the currently assessed instantaneous failure rate of the system under test."))

        self.txtRhoC = _widg.make_entry(_width_=100)
        self.txtRhoC.set_tooltip_text(_(u"Displays the currently assessed cumulative failure rate of the system under test."))

        self.txtMTBFInst = _widg.make_entry(_width_=100)
        self.txtMTBFInst.set_tooltip_text(_(u"Displays the currently assessed instantaneous MTBF of the system under test."))

        self.txtMTBFC = _widg.make_entry(_width_=100)
        self.txtMTBFC.set_tooltip_text(_(u"Displays the currently assessed cumulative MTBF of the system under test."))

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
            window.set_title(_(u"RelKit Plot"))

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
        button.connect('clicked', AddRGRecord, self._app)
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

    def _planning_widgets_create(self):
        """ Method to create the Planning Input widgets. """

        self.fraPlanDetails.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.fraPlanDetails2.set_shadow_type(gtk.SHADOW_ETCHED_IN)

        self.scwRGPlanDetails.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scwRGPlanDetails.add_with_viewport(self.tvwRGPlanDetails)

# General test planning input widgets.
        self.cmbAssembly.set_tooltip_text(_(u"Selects and displays the assembly associated with the test."))
        self.cmbAssembly.connect('changed', self._callback_combo, 0)

        self.cmbTestType.set_tooltip_text(_(u"Selects and displays the type of test being planned."))
        results = [["HALT"], ["HASS"], ["ALT"], ["ESS"],
                   ["Reliability Growth"], ["Reliability Demonstration"],
                   ["PRVT"]]
        _widg.load_combo(self.cmbTestType, results)
        self.cmbTestType.connect('changed', self._callback_combo, 4)

        self.cmbPlanModel.set_tooltip_text(_(u"Selects and displays the reliability growth planning model to be used."))
        results = [["AMSAA-Crow"], ["SPLAN"], ["SSPLAN"]]
        _widg.load_combo(self.cmbPlanModel, results)
        self.cmbPlanModel.connect('changed', self._callback_combo, 11)

        self.cmbAssessModel.set_tooltip_text(_(u"Selects and displays the reliability growth assessment model to be used."))
        results = [["AMSAA/Crow Continuous"], ["AMSAA/Crow Discrete"],
                   ["SSTRACK"], ["AMSAA/Crow Projection"],
                   ["Crow Extended"]]
        _widg.load_combo(self.cmbAssessModel, results)
        self.cmbAssessModel.connect('changed', self._callback_combo, 12)

        self.txtName.set_tooltip_text(_(u"The title or name of the selected test."))
        self.txtName.connect('focus-out-event',
                             self._callback_entry, 'text', 2)

        self.txtDescription.connect('changed',
                                    self._callback_entry, None, 'text', 3)

        self.txtAttachment.connect('changed',
                                   self._callback_entry, None, 'text', 14)

# Reliability Growth test planning widgets.
        self.btnFindMTBFI.set_tooltip_text(_(u"Launches the initial MTBF calculator."))
        self.btnFindTTFF.set_tooltip_text(_(u"Launches the time to first fix calculator."))

        self.txtMTBFI.set_tooltip_text(_(u"The initial MTBF for the selected reliability growth plan."))
        self.txtMTBFI.connect('focus-out-event',
                              self._callback_entry, 'float', 5)

        self.chkFixMTBFI.set_tooltip_text(_(u"Fixes the value of the initial MTBF when calculating the selected reliability growth plan."))
        self.chkFixMTBFI.set_active(True)

        self.txtMTBFG.set_tooltip_text(_(u"The goal MTBF for the selected reliability growth plan."))
        self.txtMTBFG.connect('focus-out-event',
                              self._callback_entry, 'float', 6)

        self.chkFixMTBFG.set_tooltip_text(_(u"Fixes the value of the program goal MTBF when calculating the selected reliability growth plan."))
        self.chkFixMTBFG.set_active(True)

        self.txtMTBFGP.set_tooltip_text(_(u"The potential MTBF at maturity for the assembly associated with the selected reliability growth plan."))
        self.txtMTBFGP.connect('focus-out-event',
                               self._callback_entry, 'float', 7)

        self.txtTechReq.set_tooltip_text(_(u"The MTBF require by the developmental program associated with the selected reliability growth plan."))
        self.txtTechReq.connect('focus-out-event',
                                self._callback_entry, 'float', 8)

        self.txtProducerRisk.set_tooltip_text(_(u"The producer (Type I) risk.  This is the risk of accepting a system when the true reliability is below the technical requirement."))
        self.txtProducerRisk.connect('focus-out-event',
                                     self._callback_entry, 'float', 10)

        self.txtConsumerRisk.set_tooltip_text(_(u"The consumer (Type II) risk.  This is the risk of rejecting a system when the true reliability is at least the goal reliability."))
        self.txtConsumerRisk.connect('focus-out-event',
                                     self._callback_entry, 'float', 9)

        adjustment = gtk.Adjustment(0, 0, 100, 1, 1)
        self.spnNumPhases.set_adjustment(adjustment)
        self.spnNumPhases.set_tooltip_text(_(u"The number of reliability growth phases."))
        self.spnNumPhases.connect('focus-out-event',
                                  self._callback_entry, 'float', 13)
        self.spnNumPhases.connect('value-changed',
                                  self._callback_spin, 13)


        self.txtTTT.set_tooltip_text(_(u"The total test time."))
        self.txtTTT.connect('focus-out-event',
                            self._callback_entry, 'float', 15)

        self.chkFixTTT.set_tooltip_text(_(u"Fixes the value of the total program test time when calculating the selected reliability growth plan."))
        self.chkFixTTT.set_active(True)

        self.txtAverageGR.set_tooltip_text(_(u"The average growth rate over the entire reliability growth program."))
        self.txtAverageGR.connect('focus-out-event',
                                  self._callback_entry, 'float', 16)

        self.chkFixAverageGR.set_tooltip_text(_(u"Fixes the value of the average growth rate when calculating the selected reliability growth plan."))
        self.chkFixAverageGR.set_active(True)

        self.txtAverageFEF.set_tooltip_text(_(u"The average fix effectiveness factor (FEF) over the entire reliability growth program."))
        self.txtAverageFEF.connect('focus-out-event',
                                  self._callback_entry, 'float', 20)

        self.txtProgramMS.set_tooltip_text(_(u"The percentage of failure that will be addressed by corrective action over the entire reliability growth program."))
        self.txtProgramMS.connect('focus-out-event',
                                  self._callback_entry, 'float', 17)

        self.chkFixProgramMS.set_tooltip_text(_(u"Fixes the value of the management strategy when calculating the selected reliability growth plan."))
        self.chkFixProgramMS.set_active(True)

        self.txtProgramProb.set_tooltip_text(_(u"The probability of seeing a failure in any phase of the reliability growth program."))
        self.txtProgramProb.connect('focus-out-event',
                                    self._callback_entry, 'float', 18)

        self.chkFixProgramProb.set_tooltip_text(_(u"Fixes the value of the probability of seeing a failure when calculating the selected reliability growth plan."))
        self.chkFixProgramProb.set_active(True)

        self.txtTTFF.set_tooltip_text(_(u"The estimated time to the first fix during the reliability growth program."))
        self.txtTTFF.connect('focus-out-event',
                             self._callback_entry, 'float', 19)

        self.chkFixTTFF.set_tooltip_text(_(u"Fixes the value of the time to first fix when calculating the selected reliability growth plan."))
        self.chkFixTTFF.set_active(True)

        return False

    def _planning_tab_create(self):
        """
        Method to create the Planing Input gtk.Notebook tab and populate it
        with the appropriate widgets for the TESTING object.
        """

        hpaned = gtk.HPaned()

# Populate the left side of the Planing Input tab.
        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_(u"Planning Inputs"))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(fixed)

        y_pos = 5

        label = _widg.make_label(self._pi_tab_labels[0], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbAssembly, 160, y_pos)
        y_pos += 35

        label = _widg.make_label(self._pi_tab_labels[3], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbTestType, 160, y_pos)
        y_pos += 35

        label = _widg.make_label(self._pi_tab_labels[1], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtName, 160, y_pos)
        y_pos += 30

        label = _widg.make_label(self._pi_tab_labels[2], 150, 25)
        fixed.put(label, 5, y_pos)
        y_pos += 30
        textview = _widg.make_text_view(buffer_=self.txtDescription,
                                        width=555)
        textview.set_tooltip_text(_(u"Detailed description of the selected test."))
        fixed.put(textview, 5, y_pos)
        y_pos += 105

        label = _widg.make_label(self._pi_tab_labels[13], 150, 25)
        fixed.put(label, 5, y_pos)
        y_pos += 30
        textview = _widg.make_text_view(buffer_=self.txtAttachment,
                                        width=555)
        textview.set_tooltip_text(_(u"Displays the URLs to any attached documents associated with the selected test."))
        fixed.put(textview, 5, y_pos)

        fixed.show_all()

        hpaned.pack1(frame, True, True)

# Populate the gtk.Fixed widgets that will be displayed in the middle of the
# Planning Input tab.  The gtk.Fixed that is displayed depends on the selected
# reliability test type.

# =========================================================================== #
# Reliability Growth Testing Detailed Inputs
# =========================================================================== #
        y_pos = 5

        label = _widg.make_label(_(u"Fix\nValue"), 150, 50)
        self.fxdRGPlanDetails.put(label, 445, y_pos)
        y_pos += 55

        label = _widg.make_label(self._pi_tab_labels[4], 300, 25)
        self.fxdRGPlanDetails.put(label, 5, y_pos)
        self.fxdRGPlanDetails.put(self.txtMTBFI, 310, y_pos)
        self.fxdRGPlanDetails.put(self.btnFindMTBFI, 415, y_pos)
        self.fxdRGPlanDetails.put(self.chkFixMTBFI, 455, y_pos)
        y_pos += 30

        label = _widg.make_label(self._pi_tab_labels[5], 300, 25)
        self.fxdRGPlanDetails.put(label, 5, y_pos)
        self.fxdRGPlanDetails.put(self.txtMTBFG, 310, y_pos)
        self.fxdRGPlanDetails.put(self.chkFixMTBFG, 455, y_pos)
        y_pos += 30

        label = _widg.make_label(self._pi_tab_labels[6], 300, 25)
        self.fxdRGPlanDetails.put(label, 5, y_pos)
        self.fxdRGPlanDetails.put(self.txtMTBFGP, 310, y_pos)
        y_pos += 30

        label = _widg.make_label(self._pi_tab_labels[7], 300, 25)
        self.fxdRGPlanDetails.put(label, 5, y_pos)
        self.fxdRGPlanDetails.put(self.txtTechReq, 310, y_pos)
        y_pos += 30

        label = _widg.make_label(self._pi_tab_labels[14], 300, 25)
        self.fxdRGPlanDetails.put(label, 5, y_pos)
        self.fxdRGPlanDetails.put(self.txtTTT, 310, y_pos)
        self.fxdRGPlanDetails.put(self.chkFixTTT, 455, y_pos)
        y_pos += 30

        label = _widg.make_label(self._pi_tab_labels[12], 300, 25)
        self.fxdRGPlanDetails.put(label, 5, y_pos)
        self.fxdRGPlanDetails.put(self.spnNumPhases, 310, y_pos)
        y_pos += 30

        label = _widg.make_label(self._pi_tab_labels[15], 300, 25)
        self.fxdRGPlanDetails.put(label, 5, y_pos)
        self.fxdRGPlanDetails.put(self.txtAverageGR, 310, y_pos)
        self.fxdRGPlanDetails.put(self.chkFixAverageGR, 455, y_pos)
        y_pos += 30

        label = _widg.make_label(self._pi_tab_labels[16], 300, 25)
        self.fxdRGPlanDetails.put(label, 5, y_pos)
        self.fxdRGPlanDetails.put(self.txtAverageFEF, 310, y_pos)
        #self.fxdRGPlanDetails.put(self.chkFixAverageFEF, 455, y_pos)
        y_pos += 30

        label = _widg.make_label(self._pi_tab_labels[17], 300, 25)
        self.fxdRGPlanDetails.put(label, 5, y_pos)
        self.fxdRGPlanDetails.put(self.txtProgramMS, 310, y_pos)
        self.fxdRGPlanDetails.put(self.chkFixProgramMS, 455, y_pos)
        y_pos += 30

        label = _widg.make_label(self._pi_tab_labels[18], 300, 25)
        self.fxdRGPlanDetails.put(label, 5, y_pos)
        self.fxdRGPlanDetails.put(self.txtProgramProb, 310, y_pos)
        self.fxdRGPlanDetails.put(self.chkFixProgramProb, 455, y_pos)
        y_pos += 30

        label = _widg.make_label(self._pi_tab_labels[19], 300, 25)
        self.fxdRGPlanDetails.put(label, 5, y_pos)
        self.fxdRGPlanDetails.put(self.txtTTFF, 310, y_pos)
        self.fxdRGPlanDetails.put(self.btnFindTTFF, 415, y_pos)
        self.fxdRGPlanDetails.put(self.chkFixTTFF, 455, y_pos)
        y_pos += 30

        label = _widg.make_label(self._pi_tab_labels[8], 300, 25)
        self.fxdRGPlanDetails.put(label, 5, y_pos)
        self.fxdRGPlanDetails.put(self.txtProducerRisk, 310, y_pos)
        y_pos += 30

        label = _widg.make_label(self._pi_tab_labels[9], 300, 25)
        self.fxdRGPlanDetails.put(label, 5, y_pos)
        self.fxdRGPlanDetails.put(self.txtConsumerRisk, 310, y_pos)
        y_pos += 30

        label = _widg.make_label(self._pi_tab_labels[10], 300, 25)
        self.fxdRGPlanDetails.put(label, 5, y_pos)
        self.fxdRGPlanDetails.put(self.cmbPlanModel, 310, y_pos)
        y_pos += 30

        label = _widg.make_label(self._pi_tab_labels[11], 300, 25)
        self.fxdRGPlanDetails.put(label, 5, y_pos)
        self.fxdRGPlanDetails.put(self.cmbAssessModel, 310, y_pos)

        self.fxdRGPlanDetails.show_all()

        hpaned1 = gtk.HPaned()
        hpaned1.pack1(self.fraPlanDetails)

# Populate the gtk.Fixed widgets that will be displayed on the right of the
# Planning Input tab.  The gtk.Fixed that is displayed depends on the selected
# reliability test type.

# =========================================================================== #
# Reliability Growth Testing Detailed Inputs
#   0. Test Phase
#   1. Number of Test Articles
#   2. Phase Start Date
#   3. Phase End Date
#   4. Test Time
#   5. Growth Rate
#   6. Initial MTBF
#   7. Final MTBF
#   8. Average MTBF
# =========================================================================== #
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
            cell.connect('edited', _widg.edit_tree, i, model)

            column = gtk.TreeViewColumn()
            label = _widg.make_column_heading(self._rg_plan_labels[i])
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

        _index_ = 0
        _assembly_id = self.model.get_value(self.selected_row,
                                            self._col_order[0])
        model = self.cmbAssembly.get_model()
        row = model.get_iter_root()
        while row is not None:
            if(model.get_value(row, 1) == str(_assembly_id)):
                break
            else:
                row = model.iter_next(row)
                _index_ += 1

        self.cmbAssembly.set_active(_index_)

        _test_type = self.model.get_value(self.selected_row,
                                          self._col_order[4])
        self.cmbTestType.set_active(_test_type)

        self.cmbPlanModel.set_active(
            self.model.get_value(self.selected_row, self._col_order[11]))
        self.cmbAssessModel.set_active(
            self.model.get_value(self.selected_row, self._col_order[12]))

        self.txtName.set_text(
            str(self.model.get_value(self.selected_row, self._col_order[2])))
        self.txtDescription.set_text(
            str(self.model.get_value(self.selected_row, self._col_order[3])))
        self.txtMTBFI.set_text(str(fmt.format(
            self.model.get_value(self.selected_row, self._col_order[5]))))
        self.txtMTBFG.set_text(str(fmt.format(
            self.model.get_value(self.selected_row, self._col_order[6]))))
        self.txtMTBFGP.set_text(str(fmt.format(
            self.model.get_value(self.selected_row, self._col_order[7]))))
        self.txtTechReq.set_text(str(fmt.format(
            self.model.get_value(self.selected_row, self._col_order[8]))))
        self.txtConsumerRisk.set_text(str(fmt.format(
            self.model.get_value(self.selected_row, self._col_order[9]))))
        self.txtProducerRisk.set_text(str(fmt.format(
            self.model.get_value(self.selected_row, self._col_order[10]))))
        self.spnNumPhases.set_value(
            self.model.get_value(self.selected_row, self._col_order[13]))
        self.txtAttachment.set_text(
            str(self.model.get_value(self.selected_row, self._col_order[14])))
        #self._load_hyperlinks()
        self.txtTTT.set_text(str(fmt.format(
            self.model.get_value(self.selected_row, self._col_order[15]))))
        self.txtAverageGR.set_text(str(fmt.format(
            self.model.get_value(self.selected_row, self._col_order[16]))))
        self.txtProgramMS.set_text(str(fmt.format(
            self.model.get_value(self.selected_row, self._col_order[17]))))
        self.txtProgramProb.set_text(str(fmt.format(
            self.model.get_value(self.selected_row, self._col_order[18]))))
        self.txtTTFF.set_text(str(fmt.format(
            self.model.get_value(self.selected_row, self._col_order[19]))))
        self.txtAverageFEF.set_text(str(fmt.format(
            self.model.get_value(self.selected_row, self._col_order[20]))))

        if(_test_type == 5):
            self._rg_plan_details(1)
            self._rg_plan_details(2)

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
        y_pos += 30

        fixed.put(self.chkMGMGP, 5, y_pos)
        y_pos += 40

        label = _widg.make_label(_(u"MTBF<sub>G</sub> / MTBF<sub>TR</sub> should fall in the range of 2 - 3."),
                                 width=400, height=40, bold=False)
        label.set_justify(gtk.JUSTIFY_LEFT)
        fixed.put(label, 5, y_pos)
        y_pos += 45

        label = _widg.make_label(_(u"Program MTBF<sub>G</sub> / MTBF<sub>TR</sub>:"),
                                 width=200, bold=False)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtTRMG, 205, y_pos)
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
        y_pos += 30

        fixed.put(self.chkFEF, 5, y_pos)
        y_pos += 30

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
                cell.connect('edited', _widg.edit_tree, i, model)
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

        scrollwindow.add_with_viewport(self.tvwTestFeasibility)

        hpaned.pack2(frame)

        hpaned2 = gtk.HPaned()
        hpaned2.pack1(hpaned)

# Populate the right side of the Test Feasibility tab.
        frame = _widg.make_frame(_label_=_(u"Test Operating Characteristic Curve"))
        frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        frame.add(self.pltPlotOC)

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

        hbox = gtk.HBox()

# =========================================================================== #
# Create the left pane to enter/display the observed reliability growth data.
# =========================================================================== #
        vbox = gtk.VBox()

        fixed = gtk.Fixed()

        y_pos = 5
        fixed.put(self.optIndividual, 5, y_pos)
        y_pos += 30

        fixed.put(self.optGrouped, 5, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"Grouping Interval:"))
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtGroupInterval, 195, y_pos)
        y_pos += 25

        label = _widg.make_label(u"")
        fixed.put(label, 5, y_pos)

        vbox.pack_start(fixed, expand=False)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        frame = _widg.make_frame(_label_=_(u"Reliability Test Data"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)
        frame.show_all()

        model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_INT)
        self.tvwTestAssessment.set_model(model)

        for i in range(4):
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
        hbox.pack_start(vbox, expand=False)

# =========================================================================== #
# Create the center pane to display the estimated parameters.
# =========================================================================== #
        fixed = gtk.Fixed()

        y_pos = 5
        label = _widg.make_label(_(u"Lambda:"))
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtScale, 200, y_pos)
        y_pos += 25

        label = _widg.make_label(_(u"Beta:"))
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtShape, 200, y_pos)
        y_pos += 40

        label = _widg.make_label(_(u"Observed Growth Rate:"))
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtGRActual, 200, y_pos)
        y_pos += 25

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
        y_pos += 25

        frame = _widg.make_frame(_label_=_(u"Estimated Parameters"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(fixed)
        frame.show_all()

        hbox.pack_start(frame, expand=False)

# =========================================================================== #
# Create the right pane to display the reliability growth plot.
# =========================================================================== #
        vbox = gtk.VBox()

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
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(self.pltPlot1)
        frame.show_all()

        vbox.pack_start(fixed, expand=False)
        vbox.pack_start(frame)
        hbox.pack_start(vbox)

# Insert the tab.
        label = gtk.Label()
        _label_ = _(u"Test\nAssessment")
        label.set_markup("<span weight='bold'>" + _label_ + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Displays reliability test results."))
        self.notebook.insert_page(hbox,
                                  tab_label=label,
                                  position=-1)

        return False

    def _assessment_tab_load(self, TPT, MTBFA, mtbfo):
        """
        Loads the widgets with test results for the TESTING Object.

        Keyword Arguments:
        TPT   -- a list of the planned test times for each test phase.
        MTBFA -- a list of planned, average MTBF values for each test phase.
        mtbfo -- a list of observed, MTBF values for each test phase.
        """

# Read overall program inputs.
# MTBFI -- initial MTBF.
# MTBFF -- program goal MTBF.
# TTT   -- total time on test over entire reliability growth plan.
# AvgGR -- average growth rate over entire reliability growth plan.
# AvgMS -- average management strategy over entire reliability growth plan.
# Prob  -- the probability of seeing one failure during a period of time.
# ti    -- the estimated time the first fix will be implemented.
        MTBFI = self.model.get_value(self.selected_row, 5)
        MTBFF = self.model.get_value(self.selected_row, 6)
        TTT = self.model.get_value(self.selected_row, 15)
        AvgGR = self.model.get_value(self.selected_row, 16)
        AvgMS = self.model.get_value(self.selected_row, 17)
        Prob = self.model.get_value(self.selected_row, 18)
        ti = self.model.get_value(self.selected_row, 19)

# Build the idealized growth and planned program curves.
        times = list(xrange(int(TTT)))
        mtbfs = []
        mtbfa = []
        j = 0
        for i in range(len(times)):
            # Build the idealized curve.
            if(times[i] < int(ti)):
                mtbfs.append(MTBFI)
            elif(times[i] == int(ti)):
                mtbfs.append(np.nan)
            else:
                mtbfs.append((MTBFI * (times[i] / ti)**AvgGR) / (1.0 - AvgGR))

            # Build the planned curve.
            T0 = int(sum(TPT[:j]))
            T1 = int(sum(TPT[:j+1]))
            if(int(times[i]) >= T0 and int(times[i]) < T1):
                mtbfa.append(MTBFA[j])
            else:
                mtbfa.append(np.nan)
                j += 1

# Pad the observed values with non-plotting values when the actual total test
# is less than the planned total test time.
        while(len(mtbfo) < len(mtbfa)):
            mtbfo.append(np.nan)

# Plot the reliability growth program curves.
        __title__ = _(u"")
        if(not self.optGrouped.get_active()):
            _widg.load_plot(self.axAxis1, self.pltPlot1,
                            x=times, y1=mtbfs, y2=mtbfa, y3=mtbfo,
                            _title_=__title__,
                            _xlab_=_(u"Test Time (t)"),
                            _ylab_=_(u"MTBF"),
                            _type_=[2, 2, 2],
                            _marker_=['k-', 'r-', 'bD'])
        else:
            _widg.load_plot(self.axAxis1, self.pltPlot1,
                            x=times, y1=mtbfs, y2=mtbfa, y3=mtbfo,
                            _title_=__title__,
                            _xlab_=_(u"Test Time (t)"),
                            _ylab_=_(u"MTBF"),
                            _type_=[2, 2, 2],
                            _marker_=['k-', 'r-', 'b-'])

        if(self.optLogarithmic):
            self.axAxis1.set_xscale('log')
            self.axAxis1.set_yscale('log')
        else:
            self.axAxis1.set_xscale('linear')
            self.axAxis1.set_yscale('linear')

# Create the legend.
        leg = self.axAxis1.legend((u"Idealized Growth Curve",
                                   u"Planned Growth", u"Observed"),
                                  'upper left',
                                  shadow=True)
        for t in leg.get_texts():
            t.set_fontsize('small')
        for l in leg.get_lines():
            l.set_linewidth(0.5)

        self.axAxis1.set_ybound(lower=-10)

        return False

    def _load_hyperlinks(self):
        """
        Method for creating hyperlinks in the Attachment gtk.TextView.
        """

        _text_ = str(self.model.get_value(self.selected_row, self._col_order[14]))

        def _hyperlink_handler(tag, widget, event, iter):
            line_number = iter.get_line()
            print(line_number)
            if event.type == gtk.gdk.BUTTON_RELEASE:
                print(result[line_number])

        hyperlink = gtk.TextTag()
        hyperlink.connect('event', _hyperlink_handler)

        for line in _text_:
            self.txtAttachment.insert_at_cursor(line + '\n')

        iter1 = self.txtAttachment.get_start_iter()
        iter = self.txtAttachment.get_start_iter()

        flag = iter.forward_to_line_end()

        while(flag != 0) :
            self.txtAttachment.apply_tag(hyperlink, iter, iter1)
            flag = iter.forward_line()
            iter1 = iter.copy()
            iter.forward_to_line_end()

        return False

    def test_plan_remove(self):
        """
        Method to remove the selected test plan from the open RelKit Program.
        """

        selection = self.treeview.get_selection()
        (model, paths) = selection.get_selected_rows()

        _records = []
        for i in range(len(paths)):
            row = model.get_iter(paths[i])
            _records.append(model.get_value(row, 1))

        _title_ = _(u"RelKit: Confirm Delete")
        _dialog = _widg.make_dialog(_title_)

        fixed = gtk.Fixed()

        y_pos = 10

        label = _widg.make_label(_(u"Are you sure you want to delete the selected test plan(s)."), 600, 250)
        fixed.put(label, 5, y_pos)

        fixed.show_all()

        _dialog.vbox.pack_start(fixed)

        response = _dialog.run()

        if(response == gtk.RESPONSE_ACCEPT):
            for i in range(len(_records)):
                query = "DELETE FROM tbl_tests \
                         WHERE fld_test_id=%d" % _records[i]
                results = self._app.DB.execute_query(query,
                                                     None,
                                                     self._app.ProgCnx,
                                                     True)

        _dialog.destroy()

        self.load_tree()

        return False

    def _calculate(self, button):
        """
        Method to perform calculations for the TESTING Object.

        Keyword Arguments:
        button -- the gtk.ToolButton that called this method.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

# =========================================================================== #
# Calculate the idealized growth curve.
# =========================================================================== #
# Read overall program inputs.
        MTBFI = self.model.get_value(self.selected_row, 5)
        MTBFF = self.model.get_value(self.selected_row, 6)
        TTT = self.model.get_value(self.selected_row, 15)
        AvgGR = self.model.get_value(self.selected_row, 16)
        AvgMS = self.model.get_value(self.selected_row, 17)
        Prob = self.model.get_value(self.selected_row, 18)
        t1 = self.model.get_value(self.selected_row, 19)
        AvgFEF = self.model.get_value(self.selected_row, 20)

        MTBFGP = MTBFI / (1.0 - AvgMS * AvgFEF)

# Calculate the probability of seeing at least one failure.
        if(not self.chkFixProgramProb.get_active()):
            try:
                Prob = 1.0 - exp(-1.0 * (t1 * AvgMS / MTBFI))
            except(ValueError, ZeroDivisionError):
                Prob = 0.0
                print "You must provide three of the four inputs: ti, MI, MS, Prob"

# Calculate the management strategy.
        if(not self.chkFixProgramMS.get_active()):
            try:
                AvgMS = log(1.0 - Prob) * MTBFI / (-1.0 * t1)
            except(ValueError, ZeroDivisionError):
                AvgMS = 0.0
                print "You must provide three of the four inputs: ti, MI, MS, Prob"

# Calculate the minimum length of the first test phase.
        if(not self.chkFixTTFF.get_active()):
            try:
                t1 = log(1.0 - Prob) * MTBFI / (-1.0 * AvgMS)
            except(ValueError, ZeroDivisionError):
                t1 = 0.0
                print "You must provide three of the four inputs: ti, MI, MS, Prob"

# Calculate total test time.
        if(not self.chkFixTTT.get_active()):
            try:
                TTT = exp(log(t1) + 1.0 / AvgGR * (log(MTBFF /MTBFI) + log(1.0 - AvgGR)))
            except(ValueError, ZeroDivisionError):
                TTT = 0.0
                print "You must provide four of the five inputs: GR, TI, ti, MI, MF"

# Calculate initial MTBF.
        if(not self.chkFixMTBFI.get_active()):
            try:
                MTBFI = (-1.0 * t1 * AvgMS) / log(1.0 - Prob)
            except (ValueError, ZeroDivisionError):
                try:
                    MTBFI = MTBFF / exp(AvgGR * (0.5 * AvgGR + log(TTT / t1) + 1.0))
                except (ValueError, ZeroDivisionError):
                    MTBFI = 0.0
                    #try:
                    #    MTBFI = (t1 * (TTT / t1)**(1.0 - AvgGR)) / N
                    #except (ValueError, ZeroDivisionError):
                    #    MTBFI = 0.0

# Calculate final MTBF.
        if(not self.chkFixMTBFG.get_active()):
            try:
                MTBFF = MTBFI * exp(AvgGR * (0.5 * AvgGR + log(TTT / t1) + 1.0))
            except(ValueError, ZeroDivisionError):
                MTBFF = 0.0
                print "You must provide four of the five inputs: GR, TI, ti, MI, MF"

# Calculate the growth rate.
        if(not self.chkFixAverageGR.get_active()):
            try:
                AvgGR = -log(TTT / t1) - 1.0 + sqrt((1.0 + log(TTT / t1))**2.0 + 2.0 * log(MTBFF / MTBFI))
            except(ValueError, ZeroDivisionError):
                AvgGR = 0.0
                print "You must provide four of the five inputs: GR, TI, ti, MI, MF"

        self.model.set_value(self.selected_row, 5, MTBFI)
        self.model.set_value(self.selected_row, 6, MTBFF)
        self.model.set_value(self.selected_row, 15, TTT)
        self.model.set_value(self.selected_row, 16, AvgGR)
        self.model.set_value(self.selected_row, 17, AvgMS)
        self.model.set_value(self.selected_row, 18, Prob)
        self.model.set_value(self.selected_row, 19, t1)

        self.txtMTBFI.set_text(str(fmt.format(MTBFI)))
        self.txtMTBFG.set_text(str(fmt.format(MTBFF)))
        self.txtTTT.set_text(str(fmt.format(TTT)))
        self.txtAverageGR.set_text(str(fmt.format(AvgGR)))
        self.txtProgramMS.set_text(str(fmt.format(AvgMS)))
        self.txtProgramProb.set_text(str(fmt.format(Prob)))
        self.txtTTFF.set_text(str(fmt.format(t1)))

# =========================================================================== #
# Reliability growth planning phase specific calculations.
# =========================================================================== #
        model = self.tvwRGPlanDetails.get_model()
        row = model.get_iter_root()
        T1 = model.get_value(row, 4)        # Length of first test phase.
        N0 = 0.0                            # Cumulative number of failures.
        N = [0]                             # Cumulative number of failures per phase,
        TTTi = []                           # Total test time for each phase.
        MTBFAP = []                         # Average planned MTBF.
        while row is not None:
            (GR, T) = _calc.calculate_rg_phase(model, row,
                                               AvgGR, AvgMS, AvgFEF, Prob, t1)

# Calculate the expected number of failures for the phase and the average MTBF
# for the phase.
            TTTi.append(T)

            try:
                Ni = (T1 * (sum(TTTi) / T1)**(1.0 - GR)) / MTBFI
                M = T / (Ni - N0)
            except ZeroDivisionError:
                Ni = 0
                M = 0.0

            MTBFAP.append(M)
            N.append(Ni)
            N0 = Ni

            model.set_value(row, 8, M)
            row = model.iter_next(row)

# =========================================================================== #
# Reliability growth assessment calculations.
# =========================================================================== #
# Create lists of the cumulative failure times and number of failures.
        F = []
        X = []
        model = self.tvwTestAssessment.get_model()
        row = model.get_iter_root()
        while row is not None:
            X.append(model.get_value(row, 2))
            F.append(model.get_value(row, 3))
            row = model.iter_next(row)

# If there is actual test data available, estimate reliability growth model
# parameters and create a list of observed failure rate and MTBF values to use
# for plotting.
        if(len(X) > 0 and len(F) > 0):
            if(not self.optGrouped.get_active()):
                (_beta_hat,
                 _lambda_hat,
                 _rho, _mu) = _calc.calculate_rgtmc(F, X, 0, False)

            elif(self.optGrouped.get_active()):
                _interval = float(self.txtGroupInterval.get_text())
                (_beta_hat,
                 _lambda_hat,
                 _rho, _mu) = _calc.calculate_rgtmc(F, X, _interval, True)

            _gr = 1.0 - _beta_hat
            _rhoi = _lambda_hat * _beta_hat * sum(TTTi)**(_beta_hat - 1)
            _rhoc = _lambda_hat * sum(TTTi)**(_beta_hat - 1)
            _mtbfi = 1.0 / _rhoi
            _mtbfc = 1.0 / _rhoc

# Load the results.
            self.txtScale.set_text(str(fmt.format(_lambda_hat)))
            self.txtShape.set_text(str(fmt.format(_beta_hat)))
            self.txtGRActual.set_text(str(fmt.format(_gr)))
            self.txtRhoInst.set_text(str(fmt.format(_rhoi)))
            self.txtRhoC.set_text(str(fmt.format(_rhoc)))
            self.txtMTBFInst.set_text(str(fmt.format(_mtbfi)))
            self.txtMTBFC.set_text(str(fmt.format(_mtbfc)))
        else:
            _rho = []
            _mu = []

        self._assess_plan_feasibility(TTTi, N)
        self._assessment_tab_load(TTTi, MTBFAP, _mu)

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
# Reliability growth planning feasibility for entire program.
# =========================================================================== #
        if(_test_type_ == 5):
            MTBFI = float(self.txtMTBFI.get_text())
            MTBFG = float(self.txtMTBFG.get_text())
            MTBFGP = float(self.txtMTBFGP.get_text())
            TR = float(self.txtTechReq.get_text())
            GR = float(self.txtAverageGR.get_text())
            FEF = float(self.txtAverageFEF.get_text())
            MS = float(self.txtProgramMS.get_text())

            # The assessment criteria come from MIL-HDBK-189C.
            self.txtMIMGP.set_text(str(fmt.format(MTBFI/MTBFGP)))
            if(MTBFI/MTBFGP >= 0.15 and MTBFI/MTBFGP <= 0.47):
                self.chkMIMGP.set_active(True)
            else:
                self.chkMIMGP.set_active(False)

            self.txtMGMGP.set_text(str(fmt.format(MTBFG/MTBFGP)))
            if(MTBFG/MTBFGP >= 0.6 and MTBFG/MTBFGP <= 0.8):
                self.chkMGMGP.set_active(True)
            else:
                self.chkMGMGP.set_active(False)

            self.txtTRMG.set_text(str(fmt.format(TR/MTBFG)))
            if(TR/MTBFG >= 2.0 and TR/MTBFG <= 3.0):
                self.chkTRMG.set_active(True)
            else:
                self.chkTRMG.set_active(False)

            self.txtFEF.set_text(str(fmt.format(FEF)))
            if(FEF >= 0.55 and FEF <= 0.85):
                self.chkFEF.set_active(True)
            else:
                self.chkFEF.set_active(False)

# =========================================================================== #
# Reliability growth planning feasibility per phase.
# =========================================================================== #
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

        return False

    def test_plan_save(self, button):
        """
        Saves the TESTING Object gtk.TreeView information to the Program's
        MySQL or SQLite3 database.

        Keyword Arguments:
        button -- the gtk.Button widget that called this function.
        """

# Find the notebook page that is currently selected.  We only save the
# information associated with the currently selected page.
        _page = self.notebook.get_current_page()

# Find the test type so we can save the contents of any gtk.TreeView
# associated specifically with the selected type of test.
        _test_type = self.model.get_value(self.selected_row, 4)

        if(_page == 0):                     # Planning data.
            self.model.foreach(self._save_line_item)

            if(_test_type == 5):            # Reliability growth.
                model = self.tvwRGPlanDetails.get_model()
                model.foreach(self._save_rg_phases)

                model = self.tvwTestFeasibility.get_model()
                model.foreach(self._save_rg_feasibility)

        elif(_page == 2):                   # Observed data.
            model = self.tvwTestAssessment.get_model()
            model.foreach(self._save_rg_data)

        return False

    def _save_line_item(self, model, path_, row):
        """
        Saves each row in the TESTING Object treeview model to the RelKit's
        Program MySQL or SQLite3 database.

        Keyword Arguments:
        model -- the TESTING gtk.ListStore.
        path_ -- the path of the active row in the TESTING gtk.ListStore.
        row   -- the selected row in the TESTING gtk.TreeView.
        """

        values = (model.get_value(row, self._col_order[0]), \
                  model.get_value(row, self._col_order[2]), \
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
                  model.get_value(row, self._col_order[1]))

        query = "UPDATE tbl_tests \
                 SET fld_assembly_id=%d, fld_test_name='%s', \
                     fld_test_description='%s', fld_test_type=%d, \
                     fld_mi=%f, fld_mg=%f, fld_mgp=%f, fld_tr=%f, \
                     fld_consumer_risk=%f, fld_producer_risk=%f, \
                     fld_rg_plan_model=%d, fld_rg_assess_model=%d, \
                     fld_num_phases=%d, fld_attachment='%s', \
                     fld_ttt=%f, fld_avg_growth=%f, fld_avg_ms=%f, \
                     fld_prob=%f, fld_ttff=%f \
                 WHERE fld_test_id=%d" % values

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
        values = (model.get_value(row, 1), _dt_start, _dt_end, \
                  model.get_value(row, 4), model.get_value(row, 5), \
                  model.get_value(row, 6), model.get_value(row, 7), \
                  model.get_value(row, 8), model.get_value(row, 0), \
                  self.test_id)

        query = "UPDATE tbl_rel_growth \
                 SET fld_test_units=%d, fld_start_date='%s', fld_end_date='%s', \
                     fld_test_time=%f, fld_growth_rate=%f, fld_mi=%f, \
                     fld_mf=%f, fld_ma=%f \
                 WHERE fld_phase_id=%d \
                 AND fld_test_id=%d" % values

        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
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

        _dt_start = datetime.strptime(model.get_value(row, 2),"%Y-%m-%d").toordinal()
        _dt_end = datetime.strptime(model.get_value(row, 3),"%Y-%m-%d").toordinal()
        values = (model.get_value(row, 1), _dt_start, _dt_end, \
                  model.get_value(row, 4), model.get_value(row, 5), \
                  model.get_value(row, 6), model.get_value(row, 7), \
                  model.get_value(row, 8), model.get_value(row, 0), \
                  self.test_id)

        query = "UPDATE tbl_rel_growth \
                 SET fld_test_units=%d, fld_start_date='%s', fld_end_date='%s', \
                     fld_num_fails=%f, fld_ms=%f, fld_fef_avg=%f, fld_tpu=%f, \
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

        values = (model.get_value(row, 1), model.get_value(row, 2), \
                  model.get_value(row, 3), model.get_value(row, 0), \
                  self.test_id)

        query = "UPDATE tbl_survival_data \
                 SET fld_left_interval=%f, fld_right_interval=%f, \
                     fld_quantity=%d \
                 WHERE fld_record_id=%d \
                 AND fld_dataset_id=%d" % values

        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("testing.py: Failed to save reliability growth field data.")
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

        _text_ = combo.get_active()

        # _index_   Field
        #    0      Assembly ID
        #    4      Test Type
        #   11      RG Planning Model
        #   12      RG Assessment Model
        if(_index_ == 0):
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
        if(_index_ == 4):
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
            self.model.set_value(self.selected_row, _index_, _text_)
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

        if(convert == 'text'):
            if(_index_ == self._col_order[3]):
                _bounds = self.txtDescription.get_bounds()
                _text_ = self.txtDescription.get_text(_bounds[0], _bounds[1])
            elif(_index_  == self._col_order[14]):
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
            self.model.set_value(self.selected_row, _index_, _text_)
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

        if(_index_ == 13):                  # Number of RG phases.
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
            self.model.set_value(self.selected_row, _index_, _value_)
        except TypeError:
            pass

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
            self.test_id = self.model.get_value(self.selected_row, 1)
            self.n_phases = self.model.get_value(self.selected_row, 13)
            self.load_notebook()

            return False
        else:
            return True

    def create_tree(self):
        """
        Creates the TESTING treeview and connects it to callback functions to
        handle editting.  Background and foreground colors can be set using the
        user-defined values in the RelKit configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()
        bg_color = _conf.RELIAFREE_COLORS[10]
        fg_color = _conf.RELIAFREE_COLORS[11]
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
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)

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
        self.n_phases = len(results)

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
            model.append(_data)

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
            model.append(_data)

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

        query = "SELECT fld_record_id, fld_left_interval, fld_right_interval, \
                        fld_quantity \
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
            model.append(_results[i])

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

        query = "SELECT * FROM tbl_tests"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            return True

        self.n_tests = len(results)

        self.model.clear()

# Load the model with the returned results.
        for i in range(self.n_tests):
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
        """
        Method to load the TESTING Object gtk.Notebook.
        """

        if self.selected_row is not None:
            self._planning_tab_load()
            #self._assessment_tab_load()

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxTesting)
        self._app.winWorkBook.show_all()

        _title = _(u"RelKit Work Bench: Program Reliability Testing (%d Tests)") % \
                   self.n_tests
        self._app.winWorkBook.set_title(_title)

# Load the test assessment tree.
        self._load_test_assessment_tree()

        self.notebook.set_current_page(0)

        return False
