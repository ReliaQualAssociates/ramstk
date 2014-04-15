#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to
RTK Program test plans.  This includes the following types of test plans:

    - Highly Accelerated Life Test (HALT)
    - Highly Accelerated Stress Screening (HASS)
    - Accelerated Life Test (ALT)
    - Environmental Stress Screening (ESS)
    - Reliability Growth (RG) Testing
    - Reliability Demonstration/Qualification (RD/RQ) Testing
    - Production Reliability Verification Testing (PRVT)
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__copyright__ = 'Copyright 2013 - 2014, Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       testing.py is part of The RTK Project
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
    import gtk  # @UnusedImport
except ImportError:
    sys.exit(1)
try:
    import gtk.glade  # @UnusedImport
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

from datetime import datetime

import locale
import gettext
_ = gettext.gettext

# Mathematics.
from math import ceil, exp, log, sqrt

import numpy as np
from scipy.stats import chi2, norm              # pylint: disable=E0611

try:
    from rpy2 import robjects
    from rpy2.robjects import r as R
    from rpy2.robjects.packages import importr
    __USE_RPY__ = False
    __USE_RPY2__ = True
except ImportError:
    __USE_RPY__ = False
    __USE_RPY2__ = False

# Plotting.
import matplotlib
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse
matplotlib.use('GTK')

# Other RTK modules.
from _assistants_.adds import AddRGRecord
import calculations as _calc
import configuration as _conf
import utilities as _util
import widgets as _widg

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')


def _close_plot(__window, __event, plot, parent):
    """
    Function to close the plot and return it to its original parent widget.

    :param __window: the gtk.Window() that is being destroyed.
    :type __window: gtk.Window
    :param __event: the gtk.gdk.Event() that called this method.
    :type __event: gtk.gdk.Event
    :param plot: the matplotlib FigureCanvas that was expaneded.
    :type plot: matplotlib.FigureCanvas
    :param parent: the original parent widget for the plot.
    :type parent: gtk.Widget
    """

    plot.reparent(parent)

    return False


# TODO: Create calculator module for small pop-up calculators and move the
# TODO: _mttff_calculator to that module.
def _mttff_calculator(__button):
    """
    Function to launch the mean time to first failure calculator.

    :param __button: the gtk.Button() that called this method.
    :type __button: gtk.Button
    """

    fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

    # Create an assistant for the calculator.
    _dialog_ = _widg.make_dialog(_(u"RTK - Time to First Failure "
                                   u"Calculator"))

    # Add the labels to the assistant.
    _fixed1_ = gtk.Fixed()
    _fixed2_ = gtk.Fixed()

    _dialog_.vbox.pack_start(_fixed1_)  # pylint: disable=E1101
    _dialog_.vbox.pack_end(_fixed2_)    # pylint: disable=E1101

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
    txtMTBFI = _widg.make_entry(width=100)
    txtNItems = _widg.make_entry(width=100)
    txtHrsWkItem = _widg.make_entry(width=100)
    txtA = _widg.make_entry(width=100)
    txtM = _widg.make_entry(width=100)
    txtB = _widg.make_entry(width=100)
    txtConfidence = _widg.make_entry(width=100)

    _fixed1_.put(txtMTBFI, _x_pos_, _y_pos1_[0])
    _fixed1_.put(txtNItems, _x_pos_, _y_pos1_[1])
    _fixed1_.put(txtHrsWkItem, _x_pos_, _y_pos1_[2])
    _fixed1_.put(txtA, _x_pos_, _y_pos1_[3])
    _fixed1_.put(txtM, _x_pos_, _y_pos1_[4])
    _fixed1_.put(txtB, _x_pos_, _y_pos1_[5])
    _fixed1_.put(txtConfidence, _x_pos_, _y_pos1_[6])

    # Add the results widgets to the assistant.
    txtMTTFF = _widg.make_entry(width=100, editable=False)
    txtTTFFLL = _widg.make_entry(width=100, editable=False)
    txtTTFFUL = _widg.make_entry(width=100, editable=False)

    _fixed2_.put(txtMTTFF, _x_pos_, _y_pos2_[0])
    _fixed2_.put(txtTTFFLL, _x_pos_, _y_pos2_[1])
    _fixed2_.put(txtTTFFUL, _x_pos_ + 105, _y_pos2_[1])

    _dialog_.show_all()

    # Run the assistant.
    _response_ = _dialog_.run()
    if _response_ == gtk.RESPONSE_ACCEPT:
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
        _ttffll_ = ((_fix_timell_ + (7.0 * _mtbfi_) /
                     (_n_items_ * _hrs_wk_item_)) *
                    _hrs_wk_item_ * _n_items_) / 7.0
        _ttfful_ = ((_fix_timeul_ + (7.0 * _mtbfi_) /
                     (_n_items_ * _hrs_wk_item_)) *
                    _hrs_wk_item_ * _n_items_) / 7.0

        txtMTTFF.set_text(str(fmt.format(_mttff_)))
        txtTTFFLL.set_text(str(fmt.format(_ttffll_)))
        txtTTFFUL.set_text(str(fmt.format(_ttfful_)))

    else:
        _dialog_.destroy()

    return False


class Testing(object):
    """
    The Testing class is used to represent the reliability test plans
    associated with the system being analyzed.
    """

# TODO: Write code to update Work Book widgets when editing the Module Book.
    def __init__(self, application):
        """
        Initializes the Testing Object.

        :param application: the RTK application.
        """

# Define private TESTING class attributes.
        self._app = application
        self._int_mission_id = -1

# Define private TESTING class dictionary attributes.
        self._dic_assemblies = {}           # List of assemblies.
        self._dic_rg_plan = {}              # RG plan details.

# Define private TESTING class list attributes.
        self._col_order = []

# Define public TESTING class attributes.
        self.assembly_id = 0
        self.test_id = 0
        self.test_name = ''
        self.test_description = ''
        self.test_type = 0
        self.mi = 0.0
        self.mg = 0.0
        self.mgp = 0.0
        self.tr = 0.0
        self.consumer_risk = 0.0
        self.producer_risk = 0.0
        self.rg_plan_model = 0
        self.rg_assess_model = 0
        self.n_phases = 0
        self.attachment = ''
        self.ttt = 0.0
        self.avg_growth = 0.3
        self.avg_ms = 0.75
        self.probability = 0.75
        self.ttff = 0.0
        self.avg_fef = 0.7
        self.grouped = 0
        self.group_interval = 0.0
        self.cum_time = 0.0
        self.cum_failures = 0.0
        self.confidence = 0.75
        self.treeview = None
        self.n_tests = 0

# Create the main TESTING class treeview.
        (self.treeview,
         self._col_order) = _widg.make_treeview('Testing', 11, self._app,
                                                None, _conf.RTK_COLORS[10],
                                                _conf.RTK_COLORS[11])

# Toolbar widgets.
        self.btnAdd = gtk.ToolButton()
        self.btnRemove = gtk.ToolButton()

# Planning Inputs page widgets.
        # Widgets for multiple test types.
        self.cmbAssembly = _widg.make_combo(simple=False)
        self.cmbTestType = _widg.make_combo()

        self.txtName = _widg.make_entry(width=400)
        self.txtDescription = gtk.TextBuffer()
        self.txtAttachment = gtk.TextBuffer()
        self.txtConsumerRisk = _widg.make_entry(width=100)
        self.txtProducerRisk = _widg.make_entry(width=100)

        self.fraPlan = _widg.make_frame(label=_(u""))
        self.fraPlanDetails = _widg.make_frame(label=_(u""))

        # Widgets for reliability growth tests.
        self.btnFindMTBFI = _widg.make_button(height=25,
                                              width=25,
                                              label=u"...",
                                              image=None)
        self.btnFindTTFF = _widg.make_button(height=25,
                                             width=25,
                                             label=u"...",
                                             image=None)

        self.chkFixMTBFI = _widg.make_check_button()
        self.chkFixMTBFG = _widg.make_check_button()
        self.chkFixTTT = _widg.make_check_button()
        self.chkFixAverageGR = _widg.make_check_button()
        self.chkFixProgramMS = _widg.make_check_button()
        self.chkFixProgramProb = _widg.make_check_button()
        self.chkFixTTFF = _widg.make_check_button()

        self.cmbPlanModel = _widg.make_combo()
        self.cmbAssessModel = _widg.make_combo()

        self.fxdRGPlan = gtk.Fixed()

        self.scwRGPlanDetails = gtk.ScrolledWindow()

        self.spnNumPhases = gtk.SpinButton()

        self.tvwRGPlanDetails = gtk.TreeView()

        self.txtMTBFI = _widg.make_entry(width=100)
        self.txtMTBFG = _widg.make_entry(width=100)
        self.txtMTBFGP = _widg.make_entry(width=100)
        self.txtTechReq = _widg.make_entry(width=100)
        self.txtTTT = _widg.make_entry(width=100)
        self.txtAverageGR = _widg.make_entry(width=100)
        self.txtAverageFEF = _widg.make_entry(width=100)
        self.txtProgramMS = _widg.make_entry(width=100)
        self.txtProgramProb = _widg.make_entry(width=100)
        self.txtTTFF = _widg.make_entry(width=100)

# Test Feasibility page widgets.
        height = (self._app.winWorkBook.height * 0.01) / 2.0
        width = (self._app.winWorkBook.width * 0.01) / 2.0

        # Widgets for reliability growth test feasibility.
        self.chkMIMGP = _widg.make_check_button(label=_(u"Acceptable "
                                                        u"MTBF<sub>I</sub> "
                                                        u"/ MTBF<sub>GP"
                                                        u"</sub>."))
        self.chkMIMGP.set_tooltip_text(_(u"Indicates whether or not the "
                                         u"initial MTBF to mature MTBF ratio "
                                         u"is within reasonable limits."))
        self.lblMIMGP = _widg.make_label("", width=150)

        self.chkFEF = _widg.make_check_button(label=_(u"Acceptable average "
                                                      u"fix effectiveness "
                                                      u"factor (FEF)."))
        self.chkFEF.set_tooltip_text(_(u"Indicates whether or not the average "
                                       u"fix effectiveness factor (FEF) is "
                                       u"within reasonable limits."))
        self.lblFEF = _widg.make_label("", width=150)

        self.chkMGMGP = _widg.make_check_button(label=_(u"Acceptable "
                                                        u"MTBF<sub>G</sub> "
                                                        u"/ MTBF<sub>GP"
                                                        u"</sub>."))
        self.chkMGMGP.set_tooltip_text(_(u"Indicates whether or not the goal "
                                         u"MTBF to mature MTBF ratio is "
                                         u"within reasonable limits."))
        self.lblMGMGP = _widg.make_label("", width=150)

        self.chkTRMG = _widg.make_check_button(label=_(u"Acceptable "
                                                       u"MTBF<sub>G</sub> "
                                                       u"/ MTBF<sub>I"
                                                       u"</sub>."))
        self.chkTRMG.set_tooltip_text(_(u"Indicates whether or not the goal "
                                        u"MTBF to initial MTBF ratio is "
                                        u"within reasonable limits."))
        self.lblMGMI = _widg.make_label("", width=150)

        self.figFigureOC = Figure(figsize=(width, height))

        self.fraTestRisk = _widg.make_frame()
        self.fraTestFeasibility = _widg.make_frame()
        self.fraOCCurve = _widg.make_frame()

        self.fxdRGRisk = gtk.Fixed()

        self.pltPlotOC = FigureCanvas(self.figFigureOC)
        self.pltPlotOC.mpl_connect('button_press_event', self._expand_plot)
        self.pltPlotOC.set_tooltip_text(_(u"Displays the Reliability Growth "
                                          u"plan Operating Characteristic "
                                          u"curve."))

        self.axAxisOC = self.figFigureOC.add_subplot(111)

        self.scwTestFeasibility = gtk.ScrolledWindow()

        self.tvwTestFeasibility = gtk.TreeView()

        self.txtMIMGP = _widg.make_entry(width=75)
        self.txtFEF = _widg.make_entry(width=75)
        self.txtMGMGP = _widg.make_entry(width=75)
        self.txtTRMG = _widg.make_entry(width=75)

# Test Assessment page widgets.
        # Widgets to enter and display the observed data.
        self.optIndividual = gtk.RadioButton(label=_(u"Individual Failure "
                                                     u"Time Data"))
        self.optIndividual.set_tooltip_text(_(u"Estimate parameters based on "
                                              u"individual failure times."))
        self.optIndividual.set_name('individual')
        self.optIndividual.set_active(True)

        self.optGrouped = gtk.RadioButton(group=self.optIndividual,
                                          label=_(u"Grouped Failure Time "
                                                  u"Data"))
        self.optGrouped.set_tooltip_text(_(u"Estimate parameters based on "
                                           u"grouped failures times."))
        self.optGrouped.set_name('grouped')

        self.optMTBF = gtk.RadioButton(label=_(u"Display results as MTBF"))
        self.optMTBF.set_tooltip_text(_(u"If selected, test results will be "
                                        u"displayed as MTBF.  This is the "
                                        u"default."))
        self.optMTBF.set_name('mtbf')
        self.optMTBF.set_active(True)
        self.optMTBF.connect('toggled', self._callback_radio)

        self.optFailureIntensity = gtk.RadioButton(group=self.optMTBF,
                                                   label=_(u"Display results "
                                                           u"as failure "
                                                           u"intensity"))
        self.optFailureIntensity.set_tooltip_text(_(u"If selected, test "
                                                    u"results will be "
                                                    u"displayed as failure "
                                                    u"intensity (rate)."))
        self.optFailureIntensity.set_name('failureintensity')
        self.optFailureIntensity.connect('toggled', self._callback_radio)

        self.scwTestAssessment = gtk.ScrolledWindow()

        self.tvwTestAssessment = gtk.TreeView()
        self.tvwTestAssessment.set_tooltip_text(_(u"Displays the incidents "
                                                  u"associated with the "
                                                  u"selected test plan."))

        self.txtGroupInterval = _widg.make_entry(width=75)
        self.txtGroupInterval.set_tooltip_text(_(u"Displays the width of the "
                                                 u"grouping intervals if "
                                                 u"using Option for Grouped "
                                                 u"Data."))

        self.spnConfidence = gtk.SpinButton()
        self.spnConfidence.set_tooltip_text(_(u"Displays the confidence level "
                                              u"to use for failure rate/MTBF "
                                              u"bounds and goodness of fit "
                                              u"tests."))

        # Widgets to display the estimated parameters for the selected model.
        self.txtCumTestTime = _widg.make_entry(width=100, editable=False)
        self.txtCumTestTime.set_tooltip_text(_(u"Displays the cumulative test "
                                               u"time to date for the "
                                               u"selected test."))

        self.txtCumFailures = _widg.make_entry(width=100, editable=False)
        self.txtCumFailures.set_tooltip_text(_(u"Displays the cumulative "
                                               u"number of failures to date "
                                               u"for the selected test."))

        self.txtScale = _widg.make_entry(width=100, editable=False)
        self.txtScale.set_tooltip_text(_(u"Displays the reliability growth "
                                         u"model estimated scale parameter."))

        self.txtShape = _widg.make_entry(width=100, editable=False)
        self.txtShape.set_tooltip_text(_(u"Displays the reliability growth "
                                         u"model estimated shape parameter."))

        self.txtGRActual = _widg.make_entry(width=100, editable=False)
        self.txtGRActual.set_tooltip_text(_(u"Displays the average growth "
                                            u"rate over the reliability "
                                            u"growth program to date."))

        self.txtRhoInst = _widg.make_entry(width=100, editable=False)
        self.txtRhoInst.set_tooltip_text(_(u"Displays the currently assessed "
                                           u"instantaneous failure rate of "
                                           u"the item under test."))

        self.txtRhoC = _widg.make_entry(width=100, editable=False)
        self.txtRhoC.set_tooltip_text(_(u"Displays the currently assessed "
                                        u"cumulative failure rate of the "
                                        u"item under test."))

        self.txtMTBFInst = _widg.make_entry(width=100, editable=False)
        self.txtMTBFInst.set_tooltip_text(_(u"Displays the currently assessed "
                                            u"instantaneous MTBF of the "
                                            u"item under test."))

        self.txtMTBFC = _widg.make_entry(width=100, editable=False)
        self.txtMTBFC.set_tooltip_text(_(u"Displays the currently assessed "
                                         u"cumulative MTBF of the item "
                                         u"under test."))

        self.lblGoFTrend = _widg.make_label("", width=100)
        self.txtGoFTrend = _widg.make_entry(width=100, editable=False)
        self.txtGoFTrend.set_tooltip_text(_(u"Displays the goodness of fit "
                                            u"test statistic for failure "
                                            u"rate/MTBF trend."))

        self.lblGoFModel = _widg.make_label("", width=100)
        self.txtGoFModel = _widg.make_entry(width=100, editable=False)
        self.txtGoFModel.set_tooltip_text(_(u"Displays the goodness of fit "
                                            u"test statistic for assessing "
                                            u"fit to the selected growth "
                                            u"model."))

        self.optLinear = gtk.RadioButton(label=_(u"Use Linear Scales"))
        self.optLinear.set_tooltip_text(_(u"Select this option to use linear "
                                          u"scales on the reliability growth "
                                          u"plot."))
        self.optLinear.set_name('linear')
        self.optLinear.set_active(True)
        self.optLinear.connect('toggled', self._callback_radio)

        self.optLogarithmic = gtk.RadioButton(group=self.optLinear,
                                              label=_(u"Use Logarithmic "
                                                      u"Scales"))
        self.optLogarithmic.set_tooltip_text(_(u"Select this option to use "
                                               u"logarithmic scales on the "
                                               u"reliability growth plot."))
        self.optLogarithmic.set_name('log')
        self.optLogarithmic.connect('toggled', self._callback_radio)

        self.figFigure1 = Figure(figsize=(width, height))

        self.pltPlot1 = FigureCanvas(self.figFigure1)
        self.pltPlot1.mpl_connect('button_press_event', self._expand_plot)
        self.pltPlot1.set_tooltip_text(_(u"Displays the selected test plan "
                                         u"and observed results."))

        self.axAxis1 = self.figFigure1.add_subplot(111)

        self.vbxPlot1 = gtk.VBox()

# Put it all together.
        _toolbar_ = self._create_toolbar()

        self.notebook = self._create_notebook()

        self.vbxTesting = gtk.VBox()
        self.vbxTesting.pack_start(_toolbar_, expand=False)
        self.vbxTesting.pack_start(self.notebook)

        self.notebook.connect('switch-page', self._notebook_page_switched)

    def create_tree(self):
        """
        Creates the TESTING treeview and connects it to callback functions to
        handle editing.  Background and foreground colors can be set using the
        user-defined values in the RTK configuration file.
        """

        self.treeview.set_tooltip_text(_(u"Displays a list of program "
                                         u"reliability tests."))
        self.treeview.set_enable_tree_lines(True)

        self.treeview.set_search_column(0)
        self.treeview.set_reorderable(True)

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None, 0)
        self.treeview.connect('row_activated', self._treeview_row_changed, 0)

        _scrollwindow_ = gtk.ScrolledWindow()
        _scrollwindow_.add(self.treeview)

        return _scrollwindow_

    def _create_toolbar(self):
        """
        Method to create the gtk.ToolBar() for the TESTING class.
        """

        toolbar = gtk.Toolbar()

        # Add button.
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        self.btnAdd.set_icon_widget(_image)
        self.btnAdd.set_name('Add')
        self.btnAdd.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnAdd, 0)

        # Remove button.
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        self.btnRemove.set_icon_widget(_image)
        self.btnRemove.set_name('Remove')
        self.btnRemove.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnRemove, 1)

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
        # button.connect('clicked', AssignResults, self._app)
        button.set_tooltip_text(_(u"Assigns MTBF and hazard rate results to "
                                  u"the selected assembly."))
        toolbar.insert(button, 4)

        toolbar.show()

        return toolbar

    def _create_notebook(self):
        """
        Method to create the TESTING class gtk.Notebook().
        """

        def _create_planning_inputs_tab(self, notebook):
            """
            Function to create the TESTING class gtk.Notebook() page for
            displaying test planning inputs for the selected test.

            :param self: the current instance of a TESTING class.
            :param notebook: the TESTING class gtk.Notebook() widget.
            :type notebook: gtk.Notebook
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hpaned = gtk.HPaned()

            # Populate the left side of the Planning Input page.
            _fixed = gtk.Fixed()

            _frame = _widg.make_frame(label=_(u"Planning Inputs"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_fixed)

            _hpaned.pack1(_frame, True, True)

            _hpaned1 = gtk.HPaned()

            self.fraPlan.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            self.fraPlanDetails.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

            self.scwRGPlanDetails.set_policy(gtk.POLICY_AUTOMATIC,
                                             gtk.POLICY_AUTOMATIC)
            self.scwRGPlanDetails.add(self.tvwRGPlanDetails)

            _hpaned1.pack1(self.fraPlan, True, True)
            _hpaned1.pack2(self.fraPlanDetails, True, True)

            _hpaned.pack2(_hpaned1, True, True)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display test planning inputs.       #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets that are common to all test types.
            _results = [["HALT"], ["HASS"], ["ALT"], ["ESS"],
                        [_(u"Reliability Growth")],
                        [_(u"Reliability Demonstration")], ["PRVT"]]
            _widg.load_combo(self.cmbTestType, _results)

            _results = [["AMSAA-Crow"], ["SPLAN"], ["SSPLAN"]]
            _widg.load_combo(self.cmbPlanModel, _results)

            _results = [[_(u"AMSAA/Crow Continuous")],
                        [_(u"AMSAA/Crow Discrete")],
                        ["SSTRACK"], [_(u"AMSAA/Crow Projection")],
                        [_(u"Crow Extended")]]
            _widg.load_combo(self.cmbAssessModel, _results)

            _labels = [_(u"Assembly:"), _(u"Test Type:"), _(u"Test Title:"),
                       _(u"Test Description:")]
            (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
            _x_pos += 5

            self.cmbAssembly.set_tooltip_text(_(u"Selects and displays the "
                                                u"assembly associated with "
                                                u"the test."))
            _fixed.put(self.cmbAssembly, _x_pos, _y_pos[0])
            self.cmbAssembly.connect('changed', self._callback_combo, 1)

            self.cmbTestType.set_tooltip_text(_(u"Selects and displays the "
                                                u"type of test being "
                                                u"planned."))
            _fixed.put(self.cmbTestType, _x_pos, _y_pos[1])
            self.cmbTestType.connect('changed', self._callback_combo, 5)

            self.txtName.set_tooltip_text(_(u"The title or name of the "
                                            u"selected test."))
            _fixed.put(self.txtName, _x_pos, _y_pos[2])
            self.txtName.connect('focus-out-event',
                                 self._callback_entry, 'text', 3)

            _textview_ = _widg.make_text_view(buffer=self.txtDescription,
                                              width=555)
            _textview_.set_tooltip_text(_(u"Detailed description of the "
                                          u"selected test."))
            _fixed.put(_textview_, 5, _y_pos[3] + 30)
            self.txtDescription.connect('changed',
                                        self._callback_entry, None, 'text', 4)

            # Create a tag named hyperlink if it doesn't already exist.
            _tag = self.txtAttachment.get_tag_table().lookup('hyperlink')
            if _tag is None:
                _tag = self.txtAttachment.create_tag('hyperlink',
                                                     foreground='blue')
            _tag.connect('event', self._hyperlink_handler)

            _label = _widg.make_label(_(u"Attachments:"), 150, 25)
            _fixed.put(_label, 5, _y_pos[3] + 135)
            _textview = _widg.make_text_view(buffer=self.txtAttachment,
                                             width=555)
            _textview.set_tooltip_text(_(u"Displays the URLs to any "
                                         u"attached documents associated "
                                         u"with the selected test."))
            _fixed.put(_textview, 5, _y_pos[3] + 170)
            self.txtAttachment.connect('changed',
                                       self._callback_entry, None, 'text', 15)

            _fixed.show_all()

            # Place the reliability growth plan widgets on the reliability
            # growth gtk.Fixed().
            _labels = [_(u"RG Planning Model:"), _(u"RG Assessment Model:"),
                       _(u"Initial Program MTBF (MTBF<sub>I</sub>):"),
                       _(u"Program Required MTBF (MTBF<sub>TR</sub>):"),
                       _(u"Program Goal MTBF (MTBF<sub>G</sub>):"),
                       _(u"Potential Mature MTBF (MTBF<sub>GP</sub>):"),
                       _(u"Number of Phases:"),
                       _(u"Time to First Fix (t<sub>1</sub>):"),
                       _(u"Total Test Time:"), _(u"Average Growth Rate:"),
                       _(u"Average FEF:"), _(u"Program MS:"),
                       _(u"Program Probability:"), _(u"Producer Risk:"),
                       _(u"Consumer Risk:")]
            (_x_pos,
             _y_pos) = _widg.make_labels(_labels, self.fxdRGPlan, 5, 5)
            _x_pos += 20

            _label = _widg.make_label(_(u"Fix\nValue"), 150, 50)
            self.fxdRGPlan.put(_label, _x_pos + 230, _y_pos[0])

            self.cmbPlanModel.set_tooltip_text(_(u"Selects and displays the "
                                                 u"reliability growth "
                                                 u"planning model to be "
                                                 u"used."))
            self.fxdRGPlan.put(self.cmbPlanModel, _x_pos, _y_pos[0])
            self.cmbPlanModel.connect('changed', self._callback_combo, 12)

            self.cmbAssessModel.set_tooltip_text(_(u"Selects and displays the "
                                                   u"reliability growth "
                                                   u"assessment model to be "
                                                   u"used."))
            self.fxdRGPlan.put(self.cmbAssessModel, _x_pos, _y_pos[1])
            self.cmbAssessModel.connect('changed', self._callback_combo, 13)

            self.btnFindMTBFI.set_tooltip_text(_(u"Launches the initial MTBF "
                                                 u"calculator."))
            # self.fxdRGPlan.put(self.btnFindMTBFI, _x_pos + 125, _y_pos[2])

            self.btnFindTTFF.set_tooltip_text(_(u"Launches the time to first "
                                                u"fix calculator."))
            self.fxdRGPlan.put(self.btnFindTTFF, _x_pos + 125, _y_pos[7])
            self.btnFindTTFF.connect('released', self._mttff_calculator)

            self.txtMTBFI.set_tooltip_text(_(u"The initial MTBF for the "
                                             u"selected reliability growth "
                                             u"plan."))
            self.fxdRGPlan.put(self.txtMTBFI, _x_pos, _y_pos[2])
            self.txtMTBFI.connect('focus-out-event',
                                  self._callback_entry, 'float', 6)

            self.chkFixMTBFI.set_tooltip_text(_(u"Fixes the value of the "
                                                u"initial MTBF when "
                                                u"creating the selected "
                                                u"reliability growth plan."))
            self.fxdRGPlan.put(self.chkFixMTBFI, _x_pos + 240, _y_pos[2])
            self.chkFixMTBFI.set_active(True)

            self.txtMTBFG.set_tooltip_text(_(u"The goal MTBF for the "
                                             u"selected reliability growth "
                                             u"plan."))
            self.fxdRGPlan.put(self.txtMTBFG, _x_pos, _y_pos[4])
            self.txtMTBFG.connect('focus-out-event',
                                  self._callback_entry, 'float', 7)

            self.chkFixMTBFG.set_tooltip_text(_(u"Fixes the value of the "
                                                u"program goal MTBF when "
                                                u"creating the selected "
                                                u"reliability growth plan."))
            self.fxdRGPlan.put(self.chkFixMTBFG, _x_pos + 240, _y_pos[4])
            self.chkFixMTBFG.set_active(True)

            self.txtMTBFGP.set_tooltip_text(_(u"The potential MTBF at "
                                              u"maturity for the assembly "
                                              u"associated with the selected "
                                              u"reliability growth plan."))
            self.fxdRGPlan.put(self.txtMTBFGP, _x_pos, _y_pos[5])
            self.txtMTBFGP.connect('focus-out-event',
                                   self._callback_entry, 'float', 8)

            self.txtTechReq.set_tooltip_text(_(u"The MTBF require by the "
                                               u"developmental program "
                                               u"associated with the selected "
                                               u"reliability growth plan."))
            self.fxdRGPlan.put(self.txtTechReq, _x_pos, _y_pos[3])
            self.txtTechReq.connect('focus-out-event',
                                    self._callback_entry, 'float', 9)

            self.spnNumPhases.set_adjustment(gtk.Adjustment(0, 0, 100, 1, 1))
            self.spnNumPhases.set_tooltip_text(_(u"The number of reliability "
                                                 u"growth phases."))
            self.fxdRGPlan.put(self.spnNumPhases, _x_pos, _y_pos[6])
            self.spnNumPhases.connect('focus-out-event',
                                      self._callback_entry, 'float', 14)
            self.spnNumPhases.connect('value-changed',
                                      self._callback_spin, 14)

            self.txtTTFF.set_tooltip_text(_(u"The estimated time to the first "
                                            u"fix during the reliability "
                                            u"growth program."))
            self.fxdRGPlan.put(self.txtTTFF, _x_pos, _y_pos[7])
            self.txtTTFF.connect('focus-out-event',
                                 self._callback_entry, 'float', 20)

            self.chkFixTTFF.set_tooltip_text(_(u"Fixes the value of the time "
                                               u"to first fix when "
                                               u"calculating the selected "
                                               u"reliability growth plan."))
            self.fxdRGPlan.put(self.chkFixTTFF, _x_pos + 240, _y_pos[7])
            self.chkFixTTFF.set_active(True)

            self.txtTTT.set_tooltip_text(_(u"The total test time."))
            self.fxdRGPlan.put(self.txtTTT, _x_pos, _y_pos[8])
            self.txtTTT.connect('focus-out-event',
                                self._callback_entry, 'float', 16)

            self.chkFixTTT.set_tooltip_text(_(u"Fixes the value of the total "
                                              u"program test time when "
                                              u"calculating the selected "
                                              u"reliability growth plan."))
            self.fxdRGPlan.put(self.chkFixTTT, _x_pos + 240, _y_pos[8])
            self.chkFixTTT.set_active(True)

            self.txtAverageGR.set_tooltip_text(_(u"The average growth rate "
                                                 u"over the entire "
                                                 u"reliability growth "
                                                 u"program."))
            self.fxdRGPlan.put(self.txtAverageGR, _x_pos, _y_pos[9])
            self.txtAverageGR.connect('focus-out-event',
                                      self._callback_entry, 'float', 17)

            self.chkFixAverageGR.set_tooltip_text(_(u"Fixes the value of the "
                                                    u"average growth rate "
                                                    u"when calculating the "
                                                    u"selected reliability "
                                                    u"growth plan."))
            self.fxdRGPlan.put(self.chkFixAverageGR, _x_pos + 240, _y_pos[9])
            self.chkFixAverageGR.set_active(True)

            self.txtAverageFEF.set_tooltip_text(_(u"The average fix "
                                                  u"effectiveness factor "
                                                  u"(FEF) over the entire "
                                                  u"reliability growth "
                                                  u"program."))
            self.fxdRGPlan.put(self.txtAverageFEF, _x_pos, _y_pos[10])
            # self.fxdRGPlan.put(self.chkFixAverageFEF, _x_pos + 240,
            #                   _y_pos[10])
            self.txtAverageFEF.connect('focus-out-event',
                                       self._callback_entry, 'float', 21)

            self.txtProgramMS.set_tooltip_text(_(u"The percentage of failure "
                                                 u"that will be addressed by "
                                                 u"corrective action over the "
                                                 u"entire reliability growth "
                                                 u"program."))
            self.fxdRGPlan.put(self.txtProgramMS, _x_pos, _y_pos[11])
            self.txtProgramMS.connect('focus-out-event',
                                      self._callback_entry, 'float', 18)

            self.chkFixProgramMS.set_tooltip_text(_(u"Fixes the value of the "
                                                    u"management strategy "
                                                    u"when creating the "
                                                    u"selected reliability "
                                                    u"growth plan."))
            self.fxdRGPlan.put(self.chkFixProgramMS, _x_pos + 240,
                               _y_pos[11])
            self.chkFixProgramMS.set_active(True)

            self.txtProgramProb.set_tooltip_text(_(u"The probability of "
                                                   u"seeing a failure in any "
                                                   u"phase of the reliability "
                                                   u"growth program."))
            self.fxdRGPlan.put(self.txtProgramProb, _x_pos, _y_pos[12])
            self.txtProgramProb.connect('focus-out-event',
                                        self._callback_entry, 'float', 19)

            self.chkFixProgramProb.set_tooltip_text(_(u"Fixes the value of "
                                                      u"the probability of "
                                                      u"seeing a failure when "
                                                      u"creating the selected "
                                                      u"reliability growth "
                                                      u"plan."))
            self.fxdRGPlan.put(self.chkFixProgramProb, _x_pos + 240,
                               _y_pos[12])
            self.chkFixProgramProb.set_active(True)

            self.txtProducerRisk.set_tooltip_text(_(u"The producer (Type I) "
                                                    u"risk.  This is the risk "
                                                    u"of accepting a system "
                                                    u"when the true "
                                                    u"reliability is below "
                                                    u"the technical "
                                                    u"requirement."))
            self.fxdRGPlan.put(self.txtProducerRisk, _x_pos, _y_pos[13])
            self.txtProducerRisk.connect('focus-out-event',
                                         self._callback_entry, 'float', 11)

            self.txtConsumerRisk.set_tooltip_text(_(u"The consumer (Type II) "
                                                    u"risk.  This is the risk "
                                                    u"of rejecting a system "
                                                    u"when the true "
                                                    u"reliability is at least "
                                                    u"the goal reliability."))
            self.fxdRGPlan.put(self.txtConsumerRisk, _x_pos, _y_pos[14])
            self.txtConsumerRisk.connect('focus-out-event',
                                         self._callback_entry, 'float', 10)

            self.fxdRGPlan.show_all()

            # Place the reliability growth phase widgets on the reliability
            # growth phase gtk.TreeView().
            # =============================================================== #
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
            # =============================================================== #
            _labels = [_(u"Phase"), _(u"Test\nArticles"), _(u"Start Date"),
                       _(u"End Date"), _(u"Total Time"), _(u"Growth Rate"),
                       _(u"Initial MTBF"), _(u"Final MTBF"),
                       _(u"Average MTBF")]
            _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_INT,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT)
            self.tvwRGPlanDetails.set_model(_model)

            for i in range(9):
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('background', 'white')
                _cell.connect('edited', self._rg_plan_edit, i)

                _column = gtk.TreeViewColumn()
                label = _widg.make_column_heading(_labels[i])
                _column.set_widget(label)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i)
                _column.set_resizable(True)
                if i < 2:
                    _datatype = (i, 'gint')
                elif i == 2 or i == 3:
                    _datatype = (i, 'gchararray')
                else:
                    _datatype = (i, 'gfloat')
                _column.set_cell_data_func(_cell, _widg.format_cell,
                                           (i, _datatype))
                _column.connect('notify::width', _widg.resize_wrap, _cell)

                self.tvwRGPlanDetails.append_column(_column)

            self.tvwRGPlanDetails.connect('button_press_event',
                                          self._treeview_clicked, 1)

            # Insert the tab.
            _label = gtk.Label()
            _label.set_markup("<span weight='bold'>" +
                              _(u"Planning\nInputs") + "</span>")
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.show_all()
            _label.set_tooltip_text(_(u"Displays planning inputs for the "
                                      u"selected test."))

            notebook.insert_page(_hpaned,
                                 tab_label=_label,
                                 position=-1)

        def _create_feasibility_tab(self, notebook):
            """
            Function to create the TESTING class gtk.Notebook() page for
            displaying test feasibility results for the selected test.

            Keyword Arguments:
            self     -- the current instance of a TESTING class.
            notebook -- the TESTING class gtk.Notebook() widget.
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hpaned_ = gtk.HPaned()
            _hpaned2_ = gtk.HPaned()

            _fixed_ = gtk.Fixed()

            self.fraTestRisk.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            self.fraTestFeasibility.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            self.fraOCCurve.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

            _hpaned_.pack1(self.fraTestRisk)
            _hpaned_.pack2(_hpaned2_)

            _hpaned2_.pack1(self.fraTestFeasibility)
            _hpaned2_.pack2(self.fraOCCurve)

            self.scwTestFeasibility.set_policy(gtk.POLICY_AUTOMATIC,
                                               gtk.POLICY_AUTOMATIC)
            self.scwTestFeasibility.add(self.tvwTestFeasibility)

            self.fraOCCurve.add(self.pltPlotOC)
            self.fraOCCurve.hide()

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display test planning inputs.       #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Create the gtk.Fixed() for displaying reliability growth plan
            # feasibility.
            _labels_ = [_(u"MTBF<sub>I</sub> / MTBF<sub>GP</sub> should fall "
                          u"in the range of 0.15 - 0.47.  On average this "
                          u"ratio is 0.30."),
                        _(u"Program MTBF<sub>I</sub> / MTBF<sub>GP</sub>:"),
                        "", "",
                        _(u"MTBF<sub>G</sub> / MTBF<sub>GP</sub> should fall "
                          u"in the range of 0.60 - 0.80."),
                        _(u"Program MTBF<sub>G</sub> / MTBF<sub>GP</sub>:"),
                        "", "",
                        _(u"MTBF<sub>G</sub> / MTBF<sub>I</sub> should fall "
                          u"in the range of 2 - 3."),
                        _(u"Program MTBF<sub>G</sub> / MTBF<sub>TR</sub>:"),
                        "", "",
                        _(u"The Fix Effectiveness Factor should fall in the "
                          u"range of 0.55 - 0.85.  On average the FEF is "
                          u"0.70."),
                        _(u"Program average FEF:"), "", ""]
            (_x_pos_, _y_pos_) = _widg.make_labels(_labels_,
                                                   self.fxdRGRisk, 5, 5)

            self.fxdRGRisk.put(self.txtMIMGP, _x_pos_, _y_pos_[1])
            self.fxdRGRisk.put(self.lblMIMGP, _x_pos_, _y_pos_[2])
            self.fxdRGRisk.put(self.chkMIMGP, 5, _y_pos_[3])

            self.fxdRGRisk.put(self.txtMGMGP, _x_pos_, _y_pos_[5])
            self.fxdRGRisk.put(self.lblMGMGP, _x_pos_, _y_pos_[6])
            self.fxdRGRisk.put(self.chkMGMGP, 5, _y_pos_[7])

            self.fxdRGRisk.put(self.txtTRMG, _x_pos_, _y_pos_[9])
            self.fxdRGRisk.put(self.lblMGMI, _x_pos_, _y_pos_[10])
            self.fxdRGRisk.put(self.chkTRMG, 5, _y_pos_[11])

            self.fxdRGRisk.put(self.txtFEF, _x_pos_, _y_pos_[13])
            self.fxdRGRisk.put(self.lblFEF, _x_pos_, _y_pos_[14])
            self.fxdRGRisk.put(self.chkFEF, 5, _y_pos_[15])

            self.fxdRGRisk.show_all()

            # Populate the center of the Test Feasibility tab.
            _labels_ = [_(u"Phase"), _(u"Number of\nTest\nArticles"),
                        _(u"Start Date"), _(u"End Date"),
                        _(u"Expected\nNumber\nof\nFailures"),
                        _(u"Required\nManagement\nStrategy"),
                        _(u"Average\nFEF"), _(u"Test Time\nper Unit"),
                        _(u"Test Time\nper Unit\nper Week")]
            _model_ = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_INT,
                                    gobject.TYPE_STRING, gobject.TYPE_STRING,
                                    gobject.TYPE_INT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT)
            self.tvwTestFeasibility.set_model(_model_)

            for i in range(9):
                cell = gtk.CellRendererText()
                if i == 1 or i == 2 or i == 3:
                    cell.set_property('editable', 1)
                    cell.set_property('background', 'white')
                    cell.connect('edited', self._rg_feasibility_edit, i)
                else:
                    cell.set_property('editable', 0)
                    cell.set_property('background', 'grey')

                column = gtk.TreeViewColumn()
                label = _widg.make_column_heading(_labels_[i])
                column.set_widget(label)
                column.pack_start(cell, True)
                column.set_attributes(cell, text=i)
                column.set_resizable(True)
                if i > 3:
                    _datatype_ = (i, 'gfloat')
                else:
                    _datatype_ = (i, 'gint')
                column.set_cell_data_func(cell, _widg.format_cell,
                                          (i, _datatype_))
                column.connect('notify::width', _widg.resize_wrap, cell)
                self.tvwTestFeasibility.append_column(column)

            self.tvwTestFeasibility.connect('button_press_event',
                                            self._treeview_clicked, 2)

            # Insert the tab.
            _label_ = gtk.Label()
            _heading_ = _(u"Test\nFeasibility")
            _label_.set_markup("<span weight='bold'>" + _heading_ + "</span>")
            _label_.set_alignment(xalign=0.5, yalign=0.5)
            _label_.set_justify(gtk.JUSTIFY_CENTER)
            _label_.show_all()
            _label_.set_tooltip_text(_(u"Assessment of the feasibility of the "
                                       u"selected test."))

            notebook.insert_page(_hpaned_,
                                 tab_label=_label_,
                                 position=-1)

            return False

        def _create_assessment_tab(self, notebook):
            """
            Function to create the TESTING class gtk.Notebook() page for
            displaying test assessment results for the selected test.

            :param self: the current instance of a TESTING class.
            :param notebook: the TESTING class gtk.Notebook() widget.
            :type notebook: gtk.Notebook
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hpaned = gtk.HPaned()
            _hpaned2 = gtk.HPaned()

            _vbox = gtk.VBox()
            _hpaned.pack1(_vbox)
            _hpaned.pack2(_hpaned2)

            _fxdDataSet_ = gtk.Fixed()

            _frame = _widg.make_frame(label=_(u""))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_fxdDataSet_)
            _frame.show_all()

            _vbox.pack_start(_frame, expand=False)

            self.scwTestAssessment.set_policy(gtk.POLICY_AUTOMATIC,
                                              gtk.POLICY_AUTOMATIC)
            self.scwTestAssessment.add(self.tvwTestAssessment)

            _frame = _widg.make_frame(label=_(u"Reliability Test Data"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(self.scwTestAssessment)
            _frame.show_all()

            _vbox.pack_end(_frame)

            _fxdNumericalResults_ = gtk.Fixed()

            _frame = _widg.make_frame(label=_(u"Estimated Parameters"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_fxdNumericalResults_)
            _frame.show_all()

            _hpaned2.pack1(_frame)

            _vbox = gtk.VBox()
            _hpaned2.pack2(_vbox)

            _fxdGraphicalResults_ = gtk.Fixed()

            _vbox.pack_start(_fxdGraphicalResults_, expand=False)

            _frame = _widg.make_frame(label=_(u"Reliability Test Plot"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(self.pltPlot1)
            _frame.show_all()

            _vbox.pack_end(_frame)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display test assessment results.    #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to describe the format of the dataset.
            _y_pos = 5
            _fxdDataSet_.put(self.optIndividual, 5, _y_pos)
            self.optIndividual.connect('toggled', self._callback_check, 22)
            _y_pos += 30

            _fxdDataSet_.put(self.optGrouped, 5, _y_pos)
            _fxdDataSet_.put(self.txtGroupInterval, 230, _y_pos)
            self.optGrouped.connect('toggled', self._callback_check, 22)
            self.txtGroupInterval.connect('focus-out-event',
                                          self._callback_entry, 'float', 23)
            _y_pos += 25

            _adjustment_ = gtk.Adjustment(0, 0, 100, 0.5, 1)
            self.spnConfidence.set_adjustment(_adjustment_)

            _label = _widg.make_label(_(u"Confidence:"))
            _fxdDataSet_.put(_label, 5, _y_pos)
            _fxdDataSet_.put(self.spnConfidence, 230, _y_pos)
            self.spnConfidence.connect('focus-out-event',
                                       self._callback_entry, 'float', 26)
            self.spnConfidence.connect('value-changed',
                                       self._callback_spin, 26)
            _y_pos += 25

            _label = _widg.make_label(u"")
            _fxdDataSet_.put(_label, 5, _y_pos)

            # Place the gtk.TreeView() that will display the reliability test
            # data.
            _labels = [_(u"Record\nNumber"), _(u"Date"),
                       _(u"Interval\nStart"), _(u"Interval\nEnd"),
                       _(u"Number\nof\nFailures")]
            _model_ = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_INT)
            self.tvwTestAssessment.set_model(_model_)

            for i in range(5):
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('background', 'white')
                _cell.connect('edited', _widg.edit_tree, i, _model_)

                _column = gtk.TreeViewColumn()
                _column.set_widget(_widg.make_column_heading(_labels[i]))
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i)
                _column.set_resizable(True)
                if i == 1 or i == 2:
                    _datatype = (i, 'gfloat')
                else:
                    _datatype = (i, 'gint')
                _column.set_celldata_func(_cell, _widg.format_cell,
                                          (i, _datatype))
                _column.connect('notify::width', _widg.resize_wrap, _cell)

                self.tvwTestAssessment.append_column(_column)

            # Place the widgets use to display the numerical results of the
            # test data assessment.
            _labels = [_(u"Cum. Test Time:"), _(u"Cum. Failures:"),
                       _(u"Lambda:"), _(u"Beta:"), _(u"Observed Growth Rate:"),
                       _(u"Instantaneous Failure Rate:"),
                       _(u"Cumulative Failure Rate:"),
                       _(u"Instantaneous MTBF:"), _(u"Cumulative MTBF:"),
                       _(u"GoF for Trend:"), _(u"GoF for Model:")]
            (_x_pos, _y_pos) = _widg.make_labels(_labels,
                                                 _fxdNumericalResults_, 5, 5)
            _x_pos += 20

            _fxdNumericalResults_.put(self.txtCumTestTime, _x_pos, _y_pos[0])
            _fxdNumericalResults_.put(self.txtCumFailures, _x_pos, _y_pos[1])
            _fxdNumericalResults_.put(self.txtScale, _x_pos, _y_pos[2])
            _fxdNumericalResults_.put(self.txtShape, _x_pos, _y_pos[3])
            _fxdNumericalResults_.put(self.txtGRActual, _x_pos, _y_pos[4])
            _fxdNumericalResults_.put(self.txtRhoInst, _x_pos, _y_pos[5])
            _fxdNumericalResults_.put(self.txtRhoC, _x_pos, _y_pos[6])
            _fxdNumericalResults_.put(self.txtMTBFInst, _x_pos, _y_pos[7])
            _fxdNumericalResults_.put(self.txtMTBFC, _x_pos, _y_pos[8])
            _fxdNumericalResults_.put(self.txtGoFTrend, _x_pos, _y_pos[9])
            _fxdNumericalResults_.put(self.lblGoFTrend, _x_pos + 105,
                                      _y_pos[9])
            _fxdNumericalResults_.put(self.txtGoFModel, _x_pos, _y_pos[10])
            _fxdNumericalResults_.put(self.lblGoFModel, _x_pos + 105,
                                      _y_pos[10])

            # Place the widgets use to display the graphical results of the
            # test data assessment.
            _fxdGraphicalResults_.put(self.optLinear, 5, 5)
            _fxdGraphicalResults_.put(self.optMTBF, 205, 5)
            _fxdGraphicalResults_.put(self.optLogarithmic, 5, 40)
            _fxdGraphicalResults_.put(self.optFailureIntensity, 205, 40)

            _label = _widg.make_label(u"")
            _fxdGraphicalResults_.put(_label, 5, 75)

            # Insert the tab.
            _label = gtk.Label()
            _label.set_markup("<span weight='bold'>" +
                              _(u"Test\nAssessment") + "</span>")
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.show_all()
            _label.set_tooltip_text(_(u"Displays reliability test results."))
            notebook.insert_page(_hpaned,
                                 tab_label=_label,
                                 position=-1)

        _notebook_ = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if _conf.TABPOS[2] == 'left':
            _notebook_.set_tab_pos(gtk.POS_LEFT)
        elif _conf.TABPOS[2] == 'right':
            _notebook_.set_tab_pos(gtk.POS_RIGHT)
        elif _conf.TABPOS[2] == 'top':
            _notebook_.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook_.set_tab_pos(gtk.POS_BOTTOM)

        _create_planning_inputs_tab(self, _notebook_)
        _create_feasibility_tab(self, _notebook_)
        _create_assessment_tab(self, _notebook_)

        return _notebook_

    def load_tree(self):
        """
        Method to load the TESTING class gtk.TreeModel() from the RTK program
        database.

        :rtype : bool
        """

        _query_ = "SELECT * FROM tbl_tests \
                   WHERE fld_revision_id=%d" % self._app.REVISION.revision_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)
        try:
            self.n_tests = len(_results_)
        except TypeError:
            self.n_tests = 0

        _model_ = self.treeview.get_model()
        _model_.clear()

# Load the model with the returned results.
        for i in range(self.n_tests):
            _model_.append(None, _results_[i])

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        root = _model_.get_iter_root()
        if root is not None:
            path = _model_.get_path(root)
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
        Method to load the TESTING class gtk.Notebook.
        """

        def _load_planning_tab(self):
            """
            Function to load the widgets on the Test Planning page.

            :param self: the current instance of an TESTING class.
            """

            fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

            (_model_, _row_) = self.treeview.get_selection().get_selected()

            self.test_id = _model_.get_value(_row_, 2)

            _assembly_id = _model_.get_value(_row_,
                                             self._col_order[1])
            try:
                _index_ = self._dic_assemblies[_assembly_id]
            except KeyError:
                _index_ = 0
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
            self.txtMTBFI.set_text(
                str(fmt.format(_model_.get_value(_row_, self._col_order[6]))))
            self.txtMTBFG.set_text(
                str(fmt.format(_model_.get_value(_row_, self._col_order[7]))))
            self.txtMTBFGP.set_text(
                str(fmt.format(_model_.get_value(_row_, self._col_order[8]))))
            self.txtTechReq.set_text(
                str(fmt.format(_model_.get_value(_row_, self._col_order[9]))))
            self.txtConsumerRisk.set_text(
                str(fmt.format(_model_.get_value(_row_, self._col_order[10]))))
            self.txtProducerRisk.set_text(
                str(fmt.format(_model_.get_value(_row_, self._col_order[11]))))
            self.spnNumPhases.set_value(
                _model_.get_value(_row_, self._col_order[14]))
            self.txtAttachment.set_text(
                str(_model_.get_value(_row_, self._col_order[15])))
            self._load_hyperlinks()
            self.txtTTT.set_text(
                str(fmt.format(_model_.get_value(_row_, self._col_order[16]))))
            self.txtAverageGR.set_text(
                str(fmt.format(_model_.get_value(_row_, self._col_order[17]))))
            self.txtProgramMS.set_text(
                str(fmt.format(_model_.get_value(_row_, self._col_order[18]))))
            self.txtProgramProb.set_text(
                str(fmt.format(_model_.get_value(_row_, self._col_order[19]))))
            self.txtTTFF.set_text(
                str(fmt.format(_model_.get_value(_row_, self._col_order[20]))))
            self.txtAverageFEF.set_text(
                str(fmt.format(_model_.get_value(_row_, self._col_order[21]))))

            if _test_type == 5:                 # Reliability growth
                self._rg_plan_details(1)
                self._rg_plan_details(2)

            return False

        def _load_assessment_tab(self):
            """
            Function to load the widgets on the Test Assessment page.

            Keyword Arguments:
            self -- the current instance of an TESTING class.
            """

            (_model_, _row_) = self.treeview.get_selection().get_selected()

            _grouped_ = _model_.get_value(_row_, 22)
            if _grouped_ == 1:
                self.optGrouped.set_active(True)
            else:
                self.optIndividual.set_active(True)

            self.spnConfidence.set_value(_model_.get_value(_row_, 26))

            self.txtGroupInterval.set_text(str(_model_.get_value(_row_, 23)))
            self.txtCumTestTime.set_text(str(_model_.get_value(_row_, 24)))
            self.txtCumFailures.set_text(str(_model_.get_value(_row_, 25)))

            return False

        def _load_test_assessment_tree(self):
            """
            Function to load the TESTING class test data gtk.TreeView().

            Keyword Arguments:
            self -- the current instance of an TESTING class.
            """

            _query_ = "SELECT fld_record_id, fld_request_date, \
                              fld_left_interval, fld_right_interval, \
                              fld_quantity \
                       FROM tbl_survival_data \
                       WHERE fld_dataset_id=%d" % self.test_id
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)
            try:
                _n_records_ = len(_results_)
            except TypeError:
                _n_records_ = 0

            _model_ = self.tvwTestAssessment.get_model()
            _model_.clear()
            for i in range(_n_records_):
                _date = str(datetime.fromordinal(
                    int(_results_[i][1])).strftime('%Y-%m-%d'))
                _model_.append([_results_[i][0], _date, _results_[i][2],
                                _results_[i][3], _results_[i][4]])

            self.tvwTestAssessment.set_cursor('0', None, False)
            _root_ = _model_.get_iter_root()
            if _root_ is not None:
                _path_ = _model_.get_path(_root_)
                _col_ = self.tvwRGPlanDetails.get_column(0)
                self.tvwRGPlanDetails.row_activated(_path_, _col_)

            return False

        (_model_, _row_) = self.treeview.get_selection().get_selected()
        if _row_ is not None:
            _load_planning_tab(self)
            _load_assessment_tab(self)
            _load_test_assessment_tree(self)

        if self._app.winWorkBook.get_child() is not None:
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxTesting)
        self._app.winWorkBook.show_all()

        _title = _(u"RTK Work Book: Program Reliability Testing "
                   u"(%d Tests)") % self.n_tests
        self._app.winWorkBook.set_title(_title)

        self.notebook.set_current_page(0)

        return False

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

        if event.button == 3:              # Right click.
            window = gtk.Window()
            window.set_skip_pager_hint(True)
            window.set_skip_taskbar_hint(True)
            window.set_default_size(width, height)
            window.set_border_width(5)
            window.set_position(gtk.WIN_POS_NONE)
            window.set_title(_(u"RTK Plot"))

            window.connect('delete_event', _close_plot, plot, parent)

            plot.reparent(window)

            window.show_all()

        return False

    def _load_rg_plot(self, TPT, MTBFA, _obs_, _N_):    # pylint: disable=C0103
        """
        Loads the Reliability Growth plot.

        :param list TPT: a list of the planned test times for each test phase.
        :param list MTBFA: a list of planned average MTBF values for each test
                           phase.
        :param list _obs_: a list of observed values for each test phase.
        :param list _N_: a list of the number of failures in each interval.
        :return: False or True
        :rtype : boolean
        """

        def _load_idealized(self):
            """
            Function to load the idealized growth curve.

            :param self:
            :rtype: list
            """

            (_model_, _row_) = self.treeview.get_selection().get_selected()

            # Read overall program inputs.
            _MTBFI_ = _model_.get_value(_row_, 6)
            _TTT_ = _model_.get_value(_row_, 16)
            _AvgGR_ = _model_.get_value(_row_, 17)
            _ti_ = _model_.get_value(_row_, 20)

            _times_ = list(xrange(int(_TTT_)))
            _ideal_ = []
            if self.optMTBF.get_active():
                for i in range(len(_times_)):
                    if _times_[i] < int(_ti_):
                        _ideal_.append(_MTBFI_)
                    elif _times_[i] == int(_ti_):
                        _ideal_.append(np.nan)  # pylint: disable=E1101
                    else:
                        _ideal_.append(
                            (_MTBFI_ * (_times_[i] / _ti_) ** _AvgGR_) /
                            (1.0 - _AvgGR_))

            elif self.optFailureIntensity.get_active():
                for i in range(len(_times_)):
                    if _times_[i] < int(_ti_):
                        _ideal_.append(1.0 / _MTBFI_)
                    elif _times_[i] == int(_ti_):
                        _ideal_.append(np.nan)  # pylint: disable=E1101
                    else:
                        _ideal_.append((1.0 - _AvgGR_) /
                                       (_MTBFI_ *
                                        (_times_[i] / _ti_) ** _AvgGR_))

            return _ideal_

        def _load_plan(self, MTBFA, TPT):   # pylint: disable=C0103
            """
            Funciton to load the planned growth curve.

            :param list MTBFA: a list of planned average MTBF values for each
                               test phase.
            :param list TPT: a list of the planned test times for each test
                             phase.
            :return: _plan
            :rtype: list
            """

            (_model_, _row_) = self.treeview.get_selection().get_selected()

            # Read overall program inputs.
            _TTT_ = _model_.get_value(_row_, 16)

            _times_ = list(xrange(int(_TTT_)))
            _plan_ = []
            j = 0
            if self.optMTBF.get_active():
                _ylabel_ = _(u"MTBF")
                for i in range(len(_times_)):
                    _T0_ = int(sum(TPT[:j]))
                    _T1_ = int(sum(TPT[:j + 1]))
                    if int(_times_[i]) >= _T0_ and int(_times_[i]) < _T1_:
                        _plan_.append(MTBFA[j])
                    else:
                        _plan_.append(np.nan)   # pylint: disable=E1101
                        j += 1
            elif self.optFailureIntensity.get_active():
                _ylabel_ = _(u"Failure Intensity")
                for i in range(len(_times_)):
                    _T0_ = int(sum(TPT[:j]))
                    _T1_ = int(sum(TPT[:j + 1]))
                    if int(_times_[i] >= _T0_ and int(_times_[i]) < _T1_):
                        _plan_.append(1.0 / MTBFA[j])
                    else:
                        _plan_.append(np.nan)   # pylint: disable=E1101
                        j += 1

            return _plan_

        def _load_observed(self, obs, N):       # pylint: disable=C0103
            """
            Method to load the observed MTBF values.

            :param list obs: a list of observed values for each test phase.
            :param list N: a list of the number of failures in each interval.
            """

            (_model_, _row_) = self.treeview.get_selection().get_selected()

            # Read overall program inputs.
            _TTT_ = _model_.get_value(_row_, 16)
            _AvgGR_ = _model_.get_value(_row_, 17)
            _ti_ = _model_.get_value(_row_, 20)

            _interval_ = float(self.txtGroupInterval.get_text())
            _alpha_ = float(self.spnConfidence.get_value()) / 100.0

            # Update the left interval time using the previous record's right
            # interval value if the data is grouped.  Create a list of observed
            # cumulative failure times to use when plotting the results.
            i = 0
            _f_time_ = 0.0
            _obs_times_ = [0.5 * _interval_]
            _model_ = self.tvwTestAssessment.get_model()
            _row_ = _model_.get_iter_root()
            while _row_ is not None:
                if self.optGrouped.get_active():
                    _obs_times_.append(_obs_times_[i] + _interval_)
                    _model_.set_value(_row_, 2, _f_time_)
                    _f_time_ = _model_.get_value(_row_, 3)
                    i += 1
                else:
                    _obs_times_.append(_f_time_)
                    _f_time_ = _model_.get_value(_row_, 3)
                    _model_.set_value(_row_, 2, _f_time_)

                _row_ = _model_.iter_next(_row_)

            # The last observation time is the minimum of the last entered
            # time or the last interval time.
            _obs_times_[-1] = min(_TTT_, _obs_times_[-1])
            _obs_times_ = np.array(             # pylint: disable=E1101
                _obs_times_[:len(obs)])

            # Calculate the bounds at each observation point.
            _obsll_ = np.array([], float)       # pylint: disable=E1101
            _obsul_ = np.array([], float)       # pylint: disable=E1101
            for i in range(len(_obs_)):
                _Cll_ = (1.0 - (norm.ppf(0.5 + (_alpha_ / 2.0)) / sqrt(
                    2.0 * sum(N[:i + 1])))) ** -2.0  # @IgnorePep8
                _Cul_ = (1.0 + (norm.ppf(0.5 + (_alpha_ / 2.0)) / sqrt(
                    2.0 * sum(N[:i + 1])))) ** -2.0  # @IgnorePep8
                _obsll_ = np.append(            # pylint: disable=E1101
                    _obsll_, obs[i] * _Cll_)
                _obsul_ = np.append(            # pylint: disable=E1101
                    _obsul_, obs[i] * _Cul_)

            (_new_obs_times_, _obsll_) = _calc.smooth_curve(_obs_times_,
                                                            _obsll_,
                                                            50 * len(obs))
            (_new_obs_times_, _obsul_) = _calc.smooth_curve(_obs_times_,
                                                            _obsul_,
                                                            50 * len(obs))
            _obs_times_ = _obs_times_.tolist()

            return (_obs_times_, _new_obs_times_, _obsll_, _obsul_)

        (_model_, _row_) = self.treeview.get_selection().get_selected()
        TTT = _model_.get_value(_row_, 16)
        ti = _model_.get_value(_row_, 20)
        _interval_ = float(self.txtGroupInterval.get_text())
        _alpha_ = float(self.spnConfidence.get_value()) / 100.0
        if self.optMTBF.get_active():
            _targets_ = [_model_.get_value(_row_, 9)]
            _targets_.append(_model_.get_value(_row_, 7))
            _targets_.append(_model_.get_value(_row_, 8))
        elif self.optFailureIntensity.get_active():
            _targets_ = [1.0 / _model_.get_value(_row_, 9)]
            _targets_.append(1.0 / _model_.get_value(_row_, 7))
            _targets_.append(1.0 / _model_.get_value(_row_, 8))

        _times_ = list(xrange(int(TTT)))
        _ideal_ = _load_idealized(self)
        _plan_ = _load_plan(self, MTBFA, TPT)
        if self.optMTBF.get_active():
            _ylabel_ = _(u"MTBF")
        elif self.optFailureIntensity.get_active():
            _ylabel_ = _(u"Failure Intensity")
        _legend_ = [u"Idealized Growth Curve", u"Planned Growth Curve"]
        _widg.load_plot(self.axAxis1, self.pltPlot1,
                        x=_times_, y1=_ideal_, y2=_plan_,
                        _title_=_(u""),
                        _xlab_=_(u"Test Time (t)"),
                        _ylab_=_ylabel_,
                        _type_=[2, 2, 2],
                        _marker_=['b-', 'r-'])
        if len(_obs_) > 0:
            (_obs_times_, _new_obs_times_,
             _obsll_, _obsul_) = _load_observed(self, _obs_, _N_)

            line = matplotlib.lines.Line2D(_obs_times_, _obs_, lw=0.0,
                                           color='k',
                                           marker='o', markersize=6)
            self.axAxis1.add_line(line)

            line = matplotlib.lines.Line2D(_new_obs_times_, _obsll_, lw=1.5,
                                           color='k',
                                           ls='-.')
            self.axAxis1.add_line(line)

            line = matplotlib.lines.Line2D(_new_obs_times_, _obsul_, lw=1.5,
                                           color='k',
                                           ls='-.')
            self.axAxis1.add_line(line)

            _legend_.append(u"Observed")
            _legend_.append(u"{0:.1f}% Bounds".format(_alpha_ * 100.0))

        for i in range(len(_targets_)):
            self.axAxis1.axhline(y=_targets_[i], xmin=0, color='m',
                                 linewidth=2.5, linestyle=':')
        if self.optLogarithmic.get_active():
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
                                  arrowprops=dict(
                                      arrowstyle="wedge,tail_width=1.",
                                      fc='#E5E5E5', ec='None',
                                      alpha=0.5,
                                      patchA=None,
                                      patchB=Ellipse((2, -1), 0.5, 0.5),
                                      relpos=(0.5, 0.5)))

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
        Method for creating hyperlinks in the Attachment gtk.TextBuffer().

        :rtype : boolean
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        _text_ = str(_model_.get_value(_row_, self._col_order[14]))

        _start_ = self.txtAttachment.get_start_iter()
        _end_ = self.txtAttachment.get_end_iter()

        self.txtAttachment.delete(_start_, _end_)
        if _text_ != 'None':
            self.txtAttachment.insert_with_tags_by_name(_start_, _text_ + '\n',
                                                        'hyperlink')

        return False

    def _hyperlink_handler(self, __tag, __widget, event, row):
        """
        Method for retrieving the line (hyperlink) that was clicked in the
        Attachment gtk.TextBuffer and opening the link in the default
        application.

        :param __tag: the gtk.TextTag() that called this method.
        :param __widget: the gtk.TextView() that contains the tag calling this
                         method.
        :param event: the mouse button event calling this method.
        :param row: the gtk.TextIter that called this method.
        """

        import magic

        line_number = row.get_line()
        _start_ = self.txtAttachment.get_iter_at_line(line_number)
        _end_ = self.txtAttachment.get_iter_at_line(line_number + 1)

        _text_ = self.txtAttachment.get_text(_start_, _end_,
                                             include_hidden_chars=False)

        if len(_text_) > 1 and event.type == gtk.gdk.BUTTON_RELEASE:
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

# Find the largest test plan ID already in the RTK Program database and
# increment it by one.
        _query_ = "SELECT MAX(fld_test_id) \
                   FROM tbl_tests"
        _max_id_ = self._app.DB.execute_query(_query_,
                                              None,
                                              self._app.ProgCnx)[0][0]
        if _max_id_ is None or not _max_id_ or _max_id_ == '':
            _max_id_ = 1001
        else:
            _max_id_ = _max_id_ + 1

# Insert the number of test plans the user has requested.
        _n_test_plans_ = _util.add_items(_title_, _prompt_)
        for i in range(_n_test_plans_):         # pylint: disable=W0612
            _query = "INSERT INTO tbl_tests \
                      (fld_revision_id, fld_test_id, fld_test_name) \
                      VALUES(%d, %d, 'Test Plan')" % \
                     (self._app.REVISION.revision_id, _max_id_)
            _results_ = self._app.DB.execute_query(_query,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)
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

        _label_ = _widg.make_label(_(u"Are you sure you want to delete the "
                                     u"selected test plan(s)."), 600, 250)
        _fixed_.put(_label_, 5, y_pos)

        _fixed_.show_all()

        _dialog_.vbox.pack_start(_fixed_)   # pylint: disable=E1101

        response = _dialog_.run()

        if response == gtk.RESPONSE_ACCEPT:
            for i in range(len(_records_)):
                _query_ = "DELETE FROM tbl_tests \
                           WHERE fld_test_id=%d" % _records_[i]
                _results_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx,
                                                       commit=True)

        _dialog_.destroy()

        self.load_tree()

        return False

    def _calculate(self, __button):
        """
        Method to perform calculations for the TESTING Object.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: gtk.ToolButton
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
        Prob = _model_.get_value(_row_, 19)
        AvgFEF = _model_.get_value(_row_, 21)
        _alpha_ = self.spnConfidence.get_value() / 100.0

# The following is used to optimize the
        if self.chkFixProgramProb.get_active():
            _fix_[0] = True

        if self.chkFixProgramMS.get_active():
            _fix_[1] = True

        if self.chkFixTTFF.get_active():
            _fix_[2] = True

        if not self.chkFixTTT.get_active():
            TTT = ceil(exp(log(t1) + (1.0 / AvgGR) *
                           (log(MTBFF / MTBFI) + log(1.0 - AvgGR))))
            _fix_[3] = False

        if self.chkFixMTBFI.get_active():
            _fix_[4] = True

        if self.chkFixMTBFG.get_active():
            _fix_[5] = True

        if not self.chkFixAverageGR.get_active():
            AvgGR = -log(TTT / t1) - 1.0 + sqrt((1.0 + log(TTT / t1))**2.0 +
                                                2.0 * log(MTBFF / MTBFI))
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

        # Cumulative failures.
        # Cumulative failures per phase,
        # Total test time for each phase.
        # Average planned MTBF.
        N0 = 0.0
        N = [0]                             # pylint: disable=C0103
        TTTi = []
        MTBFAP = []
        while row is not None:
            _T1_ = model.get_value(row, 4)
            MTBFi = model.get_value(row, 6)
            MTBFf = model.get_value(row, 7)
            MTBFa = model.get_value(row, 8)
            (GR, T,                             # pylint: disable=C0103
             MTBFi, MTBFf) = _calc.calculate_rg_phase(_T1_, MTBFi, MTBFf,
                                                      MTBFa, AvgGR, AvgMS,
                                                      AvgFEF, Prob, t1, _fix_)

            # Update the Tree Book.
            model.set_value(row, 4, T)
            model.set_value(row, 5, GR)
            model.set_value(row, 6, MTBFi)
            model.set_value(row, 7, MTBFf)

            # Calculate the expected number of failures for the phase and the
            # average MTBF for the phase.
            TTTi.append(T)
            try:
                Ni = ((t1 / MTBFI) *            # pylint: disable=C0103
                      (sum(TTTi) / t1)**(1.0 - GR)) - sum(N)
                M = T / Ni                      # pylint: disable=C0103
            except ZeroDivisionError:
                Ni = 0
                M = 0.0                         # pylint: disable=C0103

            MTBFAP.append(M)
            N.append(Ni)

            model.set_value(row, 8, M)
            row = model.iter_next(row)

# =========================================================================== #
# Reliability growth assessment calculations.
# =========================================================================== #
        # Create lists of the cumulative failure times and number of failures.
        # X = list of cumulative failure times
        # F = list of number of failures per interval
        X = []                                  # pylint: disable=C0103
        F = []                                  # pylint: disable=C0103
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
        if len(X) > 0 and len(F) > 0:
            if not self.optGrouped.get_active():
                (_beta_hat, _lambda_hat,
                 _rho, _mu, _N_,
                 _chi_square_, _Cm_) = _calc.calculate_rgtmc(F, X, 0, False)

            elif self.optGrouped.get_active():
                _interval = float(self.txtGroupInterval.get_text())
                (_beta_hat, _lambda_hat,
                 _rho, _mu, _N_,
                 _chi_square_,
                 _Cm_) = _calc.calculate_rgtmc(F, X, _interval, True)

                _crit_vals_.append(chi2.ppf(_alpha_, (TTT / _interval) - 1))
                _crit_vals_.append(chi2.ppf(_alpha_, sum(F) - 2))

            _gr = 1.0 - _beta_hat[-1]
            _rhoi = _lambda_hat[-1] * _beta_hat[-1] * \
                max(TTTi)**(_beta_hat[-1] - 1)
            _rhoc = _rho[-1]
            _mtbfi = 1.0 / _rhoi
            _mtbfc = _mu[-1]

# Load the results.
            _model_.set_value(_row_, 24, max(X))
            _model_.set_value(_row_, 25, sum(F))
            self.txtScale.set_text(str(fmt.format(_lambda_hat[-1])))
            self.txtShape.set_text(str(fmt.format(_beta_hat[-1])))
            self.txtGRActual.set_text(str(fmt.format(_gr)))
            self.txtRhoInst.set_text(str(fmt.format(_rhoi)))
            self.txtRhoC.set_text(str(fmt.format(_rhoc)))
            self.txtMTBFInst.set_text(str(fmt.format(_mtbfi)))
            self.txtMTBFC.set_text(str(fmt.format(_mtbfc)))
            self.txtGoFTrend.set_text(str(fmt.format(_chi_square_)))
            self.txtGoFModel.set_text(str(fmt.format(_Cm_)))

            if _chi_square_ > _crit_vals_[0]:
                self.lblGoFTrend.set_markup(_(u"<span foreground='green'>"
                                              u"Trend</span>"))
            else:
                self.lblGoFTrend.set_markup(_(u"<span foreground='red'>"
                                              u"No Trend</span>"))

            if _Cm_ < _crit_vals_[1]:
                self.lblGoFModel.set_markup(_(u"<span foreground='green'>"
                                              u"Good Fit</span>"))
            else:
                self.lblGoFModel.set_markup(_(u"<span foreground='red'>"
                                              u"Poor Fit</span>"))

        else:
            _rho = []
            _mu = []

        self._assess_plan_feasibility(TTTi, N)
        self.load_notebook._load_assessment_tab()
        if self.optMTBF.get_active():
            self._load_rg_plot(TTTi, MTBFAP, _mu, _N_)
        elif self.optFailureIntensity.get_active():
            self._load_rg_plot(TTTi, MTBFAP, _rho, _N_)

        return False

    def _assess_plan_feasibility(self, TTT, N):     # pylint: disable=C0103
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
        if _test_type_ == 5:
            MTBFI = float(self.txtMTBFI.get_text())
            MTBFG = float(self.txtMTBFG.get_text())
            MTBFGP = float(self.txtMTBFGP.get_text())
            FEF = float(self.txtAverageFEF.get_text())

# Initial MTBF to growth potential MTBF ratio is high enough.  Too low means
# growth testing is being started too early.
            self.txtMIMGP.set_text(str(fmt.format(MTBFI / MTBFGP)))
            if MTBFI / MTBFGP >= 0.15 and MTBFI / MTBFGP <= 0.47:
                self.chkMIMGP.set_active(True)
            else:
                self.chkMIMGP.set_active(False)

            if MTBFI / MTBFGP >= 0.35:
                _text = "<span foreground='#00CC00'>Low Risk</span>"
            elif MTBFI / MTBFGP < 0.35 and MTBFI / MTBFGP >= 0.2:
                _text = "<span foreground='yellow'>Medium Risk</span>"
            else:
                _text = "<span foreground='red'>High Risk</span>"
            self.lblMIMGP.set_markup(_text)

            self.txtMGMGP.set_text(str(fmt.format(MTBFG / MTBFGP)))
            if MTBFG / MTBFGP >= 0.6 and MTBFG / MTBFGP <= 0.8:
                self.chkMGMGP.set_active(True)
            else:
                self.chkMGMGP.set_active(False)

            if MTBFG / MTBFGP <= 0.7:
                _text = "<span foreground='#00CC00'>Low Risk</span>"
            elif MTBFG / MTBFGP > 0.7 and MTBFG / MTBFGP <= 0.8:
                _text = "<span foreground='yellow'>Medium Risk</span>"
            else:
                _text = "<span foreground='red'>High Risk</span>"
            self.lblMGMGP.set_markup(_text)

            self.txtTRMG.set_text(str(fmt.format(MTBFG / MTBFI)))
            if MTBFG / MTBFI >= 2.0 and MTBFG / MTBFI <= 3.0:
                self.chkTRMG.set_active(True)
            else:
                self.chkTRMG.set_active(False)

            if MTBFG / MTBFI <= 2.0:
                _text = "<span foreground='#00CC00'>Low Risk</span>"
            elif MTBFG / MTBFI > 2.0 and MTBFG / MTBFI <= 3.0:
                _text = "<span foreground='yellow'>Medium Risk</span>"
            else:
                _text = "<span foreground='red'>High Risk</span>"
            self.lblMGMI.set_markup(_text)

            self.txtFEF.set_text(str(fmt.format(FEF)))
            if FEF >= 0.55 and FEF <= 0.85:
                self.chkFEF.set_active(True)
            else:
                self.chkFEF.set_active(False)

            if FEF <= 0.7:
                _text = "<span foreground='#00CC00'>Low Risk</span>"
            elif FEF > 0.7 and FEF <= 0.8:
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
                _dt_start = datetime.strptime(model.get_value(row, 2),
                                              "%Y-%m-%d").toordinal()
                _dt_end = datetime.strptime(model.get_value(row, 3),
                                            "%Y-%m-%d").toordinal()
                _weeks = (_dt_end - _dt_start) / 7.0
                _tpupw = _tpu / _weeks

                model.set_value(row, 4, ceil(N[i + 1] - N[i]))
                model.set_value(row, 7, _tpu)
                model.set_value(row, 8, _tpupw)

                i += 1
                row = model.iter_next(row)

            if i >= 6:
                _text = "<span foreground='#00CC00'>Low Risk</span>"
            elif i < 6 and i >= 4:
                _text = "<span foreground='yellow'>Medium Risk</span>"
            else:
                _text = "<span foreground='red'>High Risk</span>"

        return False

    def test_plan_save(self, __button):
        """
        Saves the TESTING class gtk.TreeView() information to the open RTK
        Program database.

        :param __button: the gtk.Button() widget that called this function.4
        :type __button: gtk.Button
        :return: False or True
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

# Find the notebook page that is currently selected.  We only save the
# information associated with the currently selected page.
        _page = self.notebook.get_current_page()

# Find the test type so we can save the contents of any gtk.TreeView
# associated specifically with the selected type of test.
        _test_type = _model.get_value(_row, 5)

        _model.foreach(self._save_line_item)
        if _test_type == 5:                # Reliability growth.
            _model = self.tvwRGPlanDetails.get_model()
            _model.foreach(self._save_rg_phases)

            _model = self.tvwTestFeasibility.get_model()
            _model.foreach(self._save_rg_feasibility)

        if _page == 2:                     # Observed data.
            _model = self.tvwTestAssessment.get_model()
            _model.foreach(self._save_rg_data)

        return False

    def _save_line_item(self, model, __path, row):
        """
        Saves each row in the TESTING Object treeview model to the RTK's
        Program MySQL or SQLite3 database.

        :param model: the TESTING class gtk.TreeModel().
        :type modle: gtk.TreeModel
        :param string __path: the path of the active row in the TESTING
                              gtk.ListStore().
        :param row: the selected row in the TESTING gtk.TreeView().
        :type row: gtk.Iter
        """

        values = (model.get_value(row, self._col_order[1]),
                  model.get_value(row, self._col_order[3]),
                  model.get_value(row, self._col_order[4]),
                  model.get_value(row, self._col_order[5]),
                  model.get_value(row, self._col_order[6]),
                  model.get_value(row, self._col_order[7]),
                  model.get_value(row, self._col_order[8]),
                  model.get_value(row, self._col_order[9]),
                  model.get_value(row, self._col_order[10]),
                  model.get_value(row, self._col_order[11]),
                  model.get_value(row, self._col_order[12]),
                  model.get_value(row, self._col_order[13]),
                  model.get_value(row, self._col_order[14]),
                  model.get_value(row, self._col_order[15]),
                  model.get_value(row, self._col_order[16]),
                  model.get_value(row, self._col_order[17]),
                  model.get_value(row, self._col_order[18]),
                  model.get_value(row, self._col_order[19]),
                  model.get_value(row, self._col_order[20]),
                  model.get_value(row, self._col_order[21]),
                  model.get_value(row, self._col_order[22]),
                  model.get_value(row, self._col_order[23]),
                  model.get_value(row, self._col_order[24]),
                  model.get_value(row, self._col_order[25]),
                  model.get_value(row, self._col_order[26]),
                  model.get_value(row, self._col_order[2]),
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

    def _save_rg_phases(self, model, __path, row):
        """
        Method to save the reliability growth phase information.

        :param model: the TESTING class reliability growth phase
                      gtk.TreeModel().
        :type model: gtk.TreeModel
        :param string __path: the path of the active row in the TESTING class
                              reliability growth phase gtk.TreeModel().
        :param row: the gtk.TreeIter() of the active row in the TESTING class
                    reliability growth phase gtk.TreeView().
        :type row: gtk.TreeIter
        """

        _dt_start = datetime.strptime(model.get_value(row, 2),
                                      "%Y-%m-%d").toordinal()
        _dt_end = datetime.strptime(model.get_value(row, 3),
                                    "%Y-%m-%d").toordinal()
        _values_ = (model.get_value(row, 1), _dt_start, _dt_end,
                    model.get_value(row, 4), model.get_value(row, 5),
                    model.get_value(row, 6), model.get_value(row, 7),
                    model.get_value(row, 8), model.get_value(row, 0),
                    self.test_id)
        _query_ = "UPDATE tbl_rel_growth \
                   SET fld_test_units=%d, fld_start_date='%s', \
                       fld_end_date='%s', fld_test_time=%f, \
                       fld_growth_rate=%f, fld_mi=%f, fld_mf=%f, fld_ma=%f \
                   WHERE fld_phase_id=%d \
                   AND fld_test_id=%d" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("testing.py: Failed to save reliability "
                                      "growth phase information.")
            return True

        return False

    def _save_rg_feasibility(self, model, __path, row):
        """
        Method to save the reliability growth phase feasibility information.

        Keyword Arguments:
        :param model: the TESTING class reliability growth phase feasibility
                      gtk.TreeModel().
        :type model: gtk.TreeModel
        :param string __path: the path of the active row in the TESTING class
                              reliability growth phase feasibility
                              gtk.TreeModel().
        :param row: the gtk.TreeIter() of the active row in the TESTING class
                    reliability growth phase feasibility gtk.TreeView().
        :type row: gtk.TreeIter
        """

        values = (model.get_value(row, 4), model.get_value(row, 5),
                  model.get_value(row, 6), model.get_value(row, 7),
                  model.get_value(row, 8), model.get_value(row, 0),
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
            self._app.debug_log.error("testing.py: Failed to save reliability "
                                      "growth phase feasibility information.")
            return True

        return False

    def _save_rg_data(self, model, __path, row):
        """
        Method to save the reliability growth testing field data.

        :param model: the TESTING class reliability growth field data
                      gtk.TreeModel().
        :type model: gtk.TreeModel
        :param string __path: the path of the active row in the TESTING class
                              reliability growth field data gtk.TreeModel().
        :param row: the gtk.TreeIter() of the active row in the TESTING class
                    reliability growth field data gtk.TreeView().
        :type row: gtk.TreeIter
        """

        _date_ = datetime.strptime(model.get_value(row, 1),
                                   '%Y-%m-%d').toordinal()
        _values_ = (_date_, model.get_value(row, 2),
                    model.get_value(row, 3), model.get_value(row, 4),
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
            self._app.debug_log.error("testing.py: Failed to save reliability "
                                      "growth field data.")
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
        if index == 22:
            if self.optIndividual.get_active():
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
        if _index_ == 1:
            model = combo.get_model()
            row = combo.get_active_iter()
            if row is not None:
                try:
                    _text_ = int(model.get_value(row, 1))
                except ValueError:
                    _text_ = 0
            else:
                _text_ = 0
        else:
            _text_ = combo.get_active()

# If we've selected a new type of test, make sure we display the correct
# detailed planning information.
        if _index_ == 5:
            if _text_ == 1:  # HALT
                _label_ = _(u"Highly Accelerated Life Test Planning Inputs")
            elif _text_ == 2:  # HASS
                _label_ = _(u"Highly Accelerated Stress Screening Planning "
                            u"Inputs")
            elif _text_ == 3:  # ALT
                _label_ = _(u"Accelerated Life Test Planning Inputs")
            elif _text_ == 4:  # ESS
                _label_ = _(u"Environmental Stress Screening Planning Inputs")
            elif _text_ == 5:  # Reliability Growth
                if self.fraPlan.get_child() is not None:
                    self.fraPlan.remove(self.fraPlan.get_child())
                self.fraPlan.add(self.fxdRGPlan)

                if self.fraTestRisk.get_child() is not None:
                    self.fraTestRisk.remove(self.fraTestRisk.get_child())
                self.fraTestRisk.set_label(_(u"Reliability Growth Test Risk"))
                self.fraTestRisk.add(self.fxdRGRisk)

                if self.fraTestFeasibility.get_child() is not None:
                    self.fraTestFeasibility.remove(
                        self.fraTestFeasibility.get_child())
                self.fraTestFeasibility.set_label(_(u"Reliability Growth Test "
                                                    u"Feasibility"))
                self.fraTestFeasibility.add(self.scwTestFeasibility)
                self.fraTestFeasibility.show_all()

                if self.rg_plan_model == 2:
                    self.fraOCCurve.set_label(_(u"Test Operating "
                                                u"Characteristic Curve"))
                    self.fraOCCurve.show_all()
                else:
                    self.fraOCCurve.hide()

                self._rg_plan_details(1)
            elif _text_ == 6:  # Reliability Demonstration
                _label_ = _(u"Reliability Demonstration/Qualification Test "
                            u"Planning Inputs")
            elif _text_ == 7:  # PRVT
                _label_ = _(u"Production Reliability Verification Test "
                            u"Planning Inputs")

# Try to update the gtk.TreeModel.  Just keep going if no row is selected.
        try:
            _model_.set_value(_row_, _index_, _text_)
        except TypeError:
            pass

        return False

    def _callback_entry(self, entry, __event, convert, index):
        """
        Callback function to retrieve and save entry changes.

        Keyword Arguments:
        :param entry: the gtk.Entry() that called this method.
        :type entry: gtk.Entry
        :param  __event: the gtk.gdk.Event() that called this method.
        :type __event gtk.gdk.Event
        :param string convert: the data type to convert the entry contents to.
        :param integer index: the position in the applicable gtk.TreeView()
                              associated with the data from the calling
                              gtk.Entry().
        :return: False or True
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        if convert == 'text':
            if index == self._col_order[4]:
                _bounds = self.txtDescription.get_bounds()
                _text = self.txtDescription.get_text(_bounds[0], _bounds[1])
            elif index == self._col_order[15]:
                _bounds = self.txtAttachment.get_bounds()
                _text = self.txtAttachment.get_text(_bounds[0], _bounds[1])
            else:
                _text = entry.get_text()

        elif convert == 'int':
            try:
                _text = int(entry.get_text())
            except ValueError:
                _text = 0

        elif convert == 'float':
            try:
                _text = float(entry.get_text().replace('$', ''))
            except ValueError:
                _text_ = 0.0

        elif convert == 'date':
            _text = datetime.strptime(entry.get_text(),
                                      '%Y-%m-%d').toordinal()

        # Try to update the gtk.TreeModel.  Just keep going if no row is
        # selected.
        try:
            _model.set_value(_row, index, _text)
        except TypeError:
            pass

        if index == 13:
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

        if button.get_name() == 'linear':
            self.axAxis1.set_xscale('linear')
            self.axAxis1.set_yscale('linear')
            self.pltPlot1.draw()
        elif button.get_name() == 'log':
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

        if _index_ == 14 and self.test_id > 1000:  # Number of RG phases.
            # Find the last number number of existing phases.
            _query = "SELECT MAX(fld_phase_id) \
                      FROM tbl_rel_growth \
                      WHERE fld_test_id=%d" % self.test_id
            _phases = self._app.DB.execute_query(_query,
                                                 None,
                                                 self._app.ProgCnx)

            if not _phases[0][0] or _phases[0][0] is None:
                self.n_phases = 0
            else:
                self.n_phases = int(_phases[0][0])

            # If spinning down, delete the phases starting with the last
            # phase.
            if _value_ < self.n_phases:
                _diff_ = self.n_phases - _value_
                for i in range(_diff_):
                    query = "DELETE FROM tbl_rel_growth \
                             WHERE fld_test_id=%d \
                             AND fld_phase_id=%d" % \
                            (self.test_id, self.n_phases)
                    self._app.DB.execute_query(query, None, self._app.ProgCnx,
                                               commit=True)

            # If spinning up, add phases until the number of phases is equal
            # to the spinner value.
            elif _value_ > self.n_phases:
                _diff_ = _value_ - self.n_phases
                for i in range(_diff_):
                    query = "INSERT INTO tbl_rel_growth \
                             (fld_test_id, fld_phase_id) \
                             VALUES(%d, %d)" % \
                            (self.test_id, i + self.n_phases + 1)
                    self._app.DB.execute_query(query, None, self._app.ProgCnx,
                                               commit=True)

            self._load_rg_plan_tree()
            self._load_rg_feasibility_tree()

# Try to update the gtk.TreeModel.  Just keep going if no row is selected.
        try:
            (_model_, _row_) = self.treeview.get_selection().get_selected()
            _model_.set_value(_row_, _index_, _value_)
        except ValueError:
            pass
        except TypeError:
            pass

        return False

    def _toolbutton_pressed(self, button):
        """
        Method to reacte to the SOFTWARE Object toolbar button clicked events.

        :param button: the gtk.ToolButton() that was pressed.
        :type : gtk.ToolButton
        """

        _page = self.notebook.get_current_page()

        if _page == 0:                     # Planning inputs
            if button.get_name() == 'Add':
                self._test_plan_add()
            elif button.get_name() == 'Remove':
                self._test_plan_remove()
        elif _page == 1:                   # Test feasibility
            if button.get_name() == 'Add':
                self._test_plan_add()
            elif button.get_name() == 'Remove':
                self._test_plan_remove()
        elif _page == 2:                   # Test assessment
            if button.get_name() == 'Add':
                AddRGRecord(self._app)

        return False

    def _notebook_page_switched(self, __notebook, __page, page_num):
        """
        Called whenever the Work Book gtk.Notebook() page is changed.

        :param __notebook: the Work Book gtk.Notebook().
        :param __page: the newly selected page widget.
        :param integer page_num: the newly selected page number.
                                 0 = Planning Inputs
                                 1 = Test Feasibility
                                 2 = Test Assessment
        :return: False
        """

        if page_num == 0:
            self.btnAdd.set_tooltip_text(_(u"Add a new test plan."))
            self.btnRemove.set_tooltip_text(_(u"Delete the selected test "
                                              u"plan."))
        elif page_num == 1:
            self.btnAdd.set_tooltip_text(_(u"Add a new test plan."))
            self.btnRemove.set_tooltip_text(_(u"Delete the selected test "
                                              u"plan."))
        elif page_num == 2:
            self.btnAdd.set_tooltip_text(_(u"Add a new test record."))
            self.btnRemove.set_tooltip_text(_(u"Delete the selected test "
                                              u"record."))

        return False

    def _rg_plan_details(self, index):
        """
        Method to load the reliability growth plan details.

        :param integer index: the index of the
        :return: False
        """
        if index == 1:
            # self.fraPlan.add(self.fxdRGPlan)

            if self.fraPlanDetails.get_child() is not None:
                self.fraPlanDetails.remove(self.fraPlanDetails.get_child())

            self.fraPlanDetails.add(self.scwRGPlanDetails)
            self.fraPlanDetails.show_all()

            label = self.fraPlanDetails.get_label_widget()

        # elif _index_ == 2:
        #    if self.fraPlanDetails2.get_child() is not None:
        #        self.fraPlanDetails2.remove(self.fraPlanDetails2.get_child())

        #    self.fraPlanDetails2.add(self.scwRGPlanDetails)
        #    self.fraPlanDetails2.show_all()

        #    label = self.fraPlanDetails2.get_label_widget()
        #    _label_ = _(u"Reliability Growth Test Phase Inputs")

            label.set_markup("<span weight='bold'>" +
                             _(u"Reliability Growth Test Planning Inputs") +
                             "</span>")
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

        if _pathinfo_ is not None:
            (_path_, _column_, _x_, _y_) = _pathinfo_
            treeview.grab_focus()
            treeview.set_cursor(_path_, _column_, False)

            if idx == 0:
                if event.button == 1:
                    self._treeview_row_changed(treeview, _path_, _column_, idx)

            elif idx == 1:
                if event.button == 3:
                    (_model_, _row_) = treeview.get_selection().get_selected()

                    _phase_id_ = _model_.get_value(_row_, 0)
                    if _column_.get_widget().get_text() == 'Start Date':
                        _date_ = _util.date_select(None)
                        _model_.set_value(_row_, 2, _date_)
                        self._dic_rg_plan[_phase_id_][2] = _date_

                        _model_ = self.tvwTestFeasibility.get_model()
                        _row_ = _model_.get_iter_from_string(
                            self._dic_rg_plan[_phase_id_][9])
                        _model_.set_value(_row_, 2, _date_)
                    elif _column_.get_widget().get_text() == 'End Date':
                        _date_ = _util.date_select(None)
                        _model_.set_value(_row_, 3, _date_)
                        self._dic_rg_plan[_phase_id_][3] = _date_

                        _model_ = self.tvwTestFeasibility.get_model()
                        _row_ = _model_.get_iter_from_string(
                            self._dic_rg_plan[_phase_id_][9])
                        _model_.set_value(_row_, 3, _date_)

            elif idx == 2:
                if event.button == 3:
                    (_model_, _row_) = treeview.get_selection().get_selected()

                    _phase_id_ = _model_.get_value(_row_, 0)
                    if _column_.get_widget().get_text() == 'Start Date':
                        _date_ = _util.date_select(None)
                        _model_.set_value(_row_, 2, _date_)
                        self._dic_rg_plan[_phase_id_][2] = _date_

                        _model_ = self.tvwRGPlanDetails.get_model()
                        _row_ = _model_.get_iter_from_string(
                            self._dic_rg_plan[_phase_id_][8])
                        _model_.set_value(_row_, 2, _date_)
                    elif _column_.get_widget().get_text() == 'End Date':
                        _date_ = _util.date_select(None)
                        _model_.set_value(_row_, 3, _date_)
                        self._dic_rg_plan[_phase_id_][3] = _date_

                        _model_ = self.tvwRGPlanDetails.get_model()
                        _row_ = _model_.get_iter_from_string(
                            self._dic_rg_plan[_phase_id_][8])
                        _model_.set_value(_row_, 3, _date_)

        return False

    def _treeview_row_changed(self, __treeview, __path, __column, __index):
        """
        Callback function to handle events for the TESTING Object
        gtk.Treeview.  It is called whenever the Incident Object treeview is
        clicked or a row is activated.

        Keyword Arguments:
        __treeview -- the Incident Object gtk.TreeView.
        __path     -- the actived row gtk.TreeView path.
        __column   -- the actived gtk.TreeViewColumn.
        __index
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
        if results == '' or not results:
            return True

        self.n_phases = len(results)

        model = self.tvwRGPlanDetails.get_model()
        model.clear()
        for i in range(self.n_phases):
            try:
                _dt_start = str(datetime.fromordinal(
                    int(results[i][2])).strftime('%Y-%m-%d'))
            except TypeError:
                _dt_start = datetime.today().strftime('%Y-%m-%d')
            try:
                _dt_end = str(datetime.fromordinal(
                    int(results[i][3])).strftime('%Y-%m-%d'))
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

        if results == '' or not results:
            return True

        self.n_phases = len(results)

        model = self.tvwTestFeasibility.get_model()
        model.clear()
        for i in range(self.n_phases):
            try:
                _dt_start = str(datetime.fromordinal(
                    int(results[i][2])).strftime('%Y-%m-%d'))
            except TypeError:
                _dt_start = datetime.today().strftime('%Y-%m-%d')
            try:
                _dt_end = str(datetime.fromordinal(
                    int(results[i][3])).strftime('%Y-%m-%d'))
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
