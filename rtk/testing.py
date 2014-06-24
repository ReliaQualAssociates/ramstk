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
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2013 - 2014, Andrew "weibullguy" Rowland'

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
from scipy.stats import chi2, norm

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
from _calculations_.growth import *
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
    :return: False if successful or True if an error is encountered
    :rtype: boolean
    """

    plot.reparent(parent)

    return False


# TODO: Create calculator module for small pop-up calculators and move the _mttff_calculator to that module.
def _mttff_calculator(__button, __event):
    """
    Function to launch the mean time to first failure calculator.

    :param __button: the gtk.Button() that called this function.
    :type __button: gtk.Button
    :param __event: the gtk.gdk.Event() that called this function.
    :type __event: gtk.gdk.Event
    :return: False if successful or True if an error is encountered.
    :rtype: boolean
    """

    from configuration import PLACES

    fmt = '{0:0.' + str(PLACES) + 'g}'

    # Create an assistant for the calculator.
    _dialog = _widg.make_dialog(_(u"RTK - Time to First Failure "
                                  u"Calculator"))

    # Add the labels to the assistant.
    _fixed1 = gtk.Fixed()
    _fixed2 = gtk.Fixed()

    _dialog.vbox.pack_start(_fixed1)
    _dialog.vbox.pack_end(_fixed2)

    _labels = [_(u"Starting MTBF:"), _(u"No. of Test Articles:"),
               _(u"Average Hours/Week/Article:"),
               _(u"Min. Time to Implement First Fix:"),
               _(u"Likely Time to Implement First Fix:"),
               _(u"Max. Time to Implement First Fix:"),
               _(u"Confidence:")]
    (_x_pos1, _y_pos1) = _widg.make_labels(_labels, _fixed1, 5, 5)
    _x_pos1 += 25

    _labels = [_(u"Expected Time to First Failure:"),
               _(u"Time to First Fix:")]
    (_x_pos2, _y_pos2) = _widg.make_labels(_labels, _fixed2, 5, 5)
    _x_pos2 += 25
    _x_pos = max(_x_pos1, _x_pos2)

    # Add the user input widgets to the assistant.
    txtMTBFI = _widg.make_entry(width=100)
    txtNItems = _widg.make_entry(width=100)
    txtHrsWkItem = _widg.make_entry(width=100)
    txtA = _widg.make_entry(width=100)
    txtM = _widg.make_entry(width=100)
    txtB = _widg.make_entry(width=100)
    txtConfidence = _widg.make_entry(width=100)

    _fixed1.put(txtMTBFI, _x_pos, _y_pos1[0])
    _fixed1.put(txtNItems, _x_pos, _y_pos1[1])
    _fixed1.put(txtHrsWkItem, _x_pos, _y_pos1[2])
    _fixed1.put(txtA, _x_pos, _y_pos1[3])
    _fixed1.put(txtM, _x_pos, _y_pos1[4])
    _fixed1.put(txtB, _x_pos, _y_pos1[5])
    _fixed1.put(txtConfidence, _x_pos, _y_pos1[6])

    # Add the results widgets to the assistant.
    txtMTTFF = _widg.make_entry(width=100, editable=False)
    txtTTFFLL = _widg.make_entry(width=100, editable=False)
    txtTTFFUL = _widg.make_entry(width=100, editable=False)

    _fixed2.put(txtMTTFF, _x_pos, _y_pos2[0])
    _fixed2.put(txtTTFFLL, _x_pos, _y_pos2[1])
    _fixed2.put(txtTTFFUL, _x_pos + 105, _y_pos2[1])

    _dialog.show_all()

    # Run the assistant.
    if _dialog.run() == gtk.RESPONSE_ACCEPT:
        _mtbfi = float(txtMTBFI.get_text())
        _n_items = float(txtNItems.get_text())
        _hrs_wk_item = float(txtHrsWkItem.get_text())
        _a = float(txtA.get_text())
        _m = float(txtM.get_text())
        _b = float(txtB.get_text())
        _confidence = float(txtConfidence.get_text())

        _conf = 1.0 - ((100.0 - _confidence) / 200.0)

        _mean_fix_time = (_a + 4.0 * _m + _b) / 6.0
        _sd_fix_time = (_b - _a) / 6.0
        _fix_timell = _mean_fix_time - norm.ppf(_conf) * _sd_fix_time
        _fix_timeul = _mean_fix_time + norm.ppf(_conf) * _sd_fix_time

        _mttff = _mtbfi / _n_items
        _ttffll = ((_fix_timell + (7.0 * _mtbfi) /
                    (_n_items * _hrs_wk_item)) *
                   _hrs_wk_item * _n_items) / 7.0
        _ttfful = ((_fix_timeul + (7.0 * _mtbfi) /
                    (_n_items * _hrs_wk_item)) *
                   _hrs_wk_item * _n_items) / 7.0

        txtMTTFF.set_text(str(fmt.format(_mttff)))
        txtTTFFLL.set_text(str(fmt.format(_ttffll)))
        txtTTFFUL.set_text(str(fmt.format(_ttfful)))

    else:
        _dialog.destroy()

    return False


class Testing(object):
    """
    The Testing class is used to represent the reliability test plans
    associated with the system being analyzed.
    """

    # These are the Cramer-von Mises critical values for Crow-AMSAA GoF tests.
    _cvm_table = {2: {0.2: 0.138, 0.15: 0.149, 0.1: 0.162, 0.05: 0.175, 0.01: 0.186},
                  3: {0.2: 0.121, 0.15: 0.135, 0.1: 0.154, 0.05: 0.184, 0.01: 0.23},
                  4: {0.2: 0.121, 0.15: 0.134, 0.1: 0.155, 0.05: 0.191, 0.01: 0.28},
                  5: {0.2: 0.121, 0.15: 0.137, 0.1: 0.160, 0.05: 0.199, 0.01: 0.30},
                  6: {0.2: 0.123, 0.15: 0.139, 0.1: 0.162, 0.05: 0.204, 0.01: 0.31},
                  7: {0.2: 0.124, 0.15: 0.140, 0.1: 0.165, 0.05: 0.208, 0.01: 0.32},
                  8: {0.2: 0.124, 0.15: 0.141, 0.1: 0.165, 0.05: 0.210, 0.01: 0.32},
                  9: {0.2: 0.125, 0.15: 0.142, 0.1: 0.167, 0.05: 0.212, 0.01: 0.32},
                  10: {0.2: 0.125, 0.15: 0.142, 0.1: 0.167, 0.05: 0.212, 0.01: 0.32},
                  11: {0.2: 0.126, 0.15: 0.143, 0.1: 0.169, 0.05: 0.214, 0.01: 0.32},
                  12: {0.2: 0.126, 0.15: 0.144, 0.1: 0.169, 0.05: 0.214, 0.01: 0.32},
                  13: {0.2: 0.126, 0.15: 0.144, 0.1: 0.169, 0.05: 0.214, 0.01: 0.33},
                  14: {0.2: 0.126, 0.15: 0.144, 0.1: 0.169, 0.05: 0.214, 0.01: 0.33},
                  15: {0.2: 0.126, 0.15: 0.144, 0.1: 0.169, 0.05: 0.215, 0.01: 0.33},
                  16: {0.2: 0.127, 0.15: 0.145, 0.1: 0.171, 0.05: 0.216, 0.01: 0.33},
                  17: {0.2: 0.127, 0.15: 0.145, 0.1: 0.171, 0.05: 0.217, 0.01: 0.33},
                  18: {0.2: 0.127, 0.15: 0.146, 0.1: 0.171, 0.05: 0.217, 0.01: 0.33},
                  19: {0.2: 0.127, 0.15: 0.146, 0.1: 0.171, 0.05: 0.217, 0.01: 0.33},
                  20: {0.2: 0.128, 0.15: 0.146, 0.1: 0.172, 0.05: 0.217, 0.01: 0.33},
                  30: {0.2: 0.128, 0.15: 0.146, 0.1: 0.172, 0.05: 0.218, 0.01: 0.33},
                  60: {0.2: 0.128, 0.15: 0.147, 0.1: 0.173, 0.05: 0.220, 0.01: 0.33},
                  100: {0.2: 0.129, 0.15: 0.147, 0.1: 0.173, 0.05: 0.220, 0.01: 0.34}}

# TODO: Write code to update Work Book widgets when editing the Module Book.
    def __init__(self, application):
        """
        Initializes the Testing Object.

        :param application: the RTK application.
        """

        # Define private Testing class attributes.
        self._app = application
        self._int_mission_id = -1

        # Define private Testing class dictionary attributes.
        self._dic_assemblies = {}           # List of assemblies.
        self._dic_rg_plan = {}              # RG plan details.

        # Define private Testing class list attributes.

        # Define public Testing class attributes.
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

        self.fraPlan = _widg.make_frame(label=_(u""))
        self.fraPlanDetails = _widg.make_frame(label=_(u""))

        self.txtName = _widg.make_entry(width=400)
        self.txtDescription = gtk.TextBuffer()
        self.txtAttachment = gtk.TextBuffer()
        self.txtConsumerRisk = _widg.make_entry(width=100)
        self.txtProducerRisk = _widg.make_entry(width=100)

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
        _height = (self._app.winWorkBook.height * 0.01) / 2.0
        _width = (self._app.winWorkBook.width * 0.01) / 2.0

        # Widgets for reliability growth test feasibility.
        self.chkMIMGP = _widg.make_check_button(label=_(u"Acceptable "
                                                        u"MTBF<sub>I</sub> "
                                                        u"/ MTBF<sub>GP"
                                                        u"</sub>."))
        self.chkFEF = _widg.make_check_button(label=_(u"Acceptable average "
                                                      u"fix effectiveness "
                                                      u"factor (FEF)."))
        self.chkMGMGP = _widg.make_check_button(label=_(u"Acceptable "
                                                        u"MTBF<sub>G</sub> "
                                                        u"/ MTBF<sub>GP"
                                                        u"</sub>."))
        self.chkTRMG = _widg.make_check_button(label=_(u"Acceptable "
                                                       u"MTBF<sub>G</sub> "
                                                       u"/ MTBF<sub>I"
                                                       u"</sub>."))

        self.figFigureOC = Figure(figsize=(_width, _height))

        self.fraTestRisk = _widg.make_frame()
        self.fraTestFeasibility = _widg.make_frame()
        self.fraOCCurve = _widg.make_frame()

        self.fxdRGRisk = gtk.Fixed()

        self.lblMIMGP = _widg.make_label("", width=150)
        self.lblFEF = _widg.make_label("", width=150)
        self.lblMGMGP = _widg.make_label("", width=150)
        self.lblMGMI = _widg.make_label("", width=150)

        self.pltPlotOC = FigureCanvas(self.figFigureOC)

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

        self.scwTestAssessment = gtk.ScrolledWindow()
        self.spnConfidence = gtk.SpinButton()
        self.tvwTestAssessment = gtk.TreeView()

        # Widgets to display the estimated parameters for the selected model.
        self.txtCumTestTime = _widg.make_entry(width=100, editable=False)
        self.txtCumFailures = _widg.make_entry(width=100, editable=False)
        self.txtScale = _widg.make_entry(width=100, editable=False)
        self.txtScalell = _widg.make_entry(width=100, editable=False)
        self.txtScaleul = _widg.make_entry(width=100, editable=False)
        self.txtShape = _widg.make_entry(width=100, editable=False)
        self.txtShapell = _widg.make_entry(width=100, editable=False)
        self.txtShapeul = _widg.make_entry(width=100, editable=False)
        self.txtGRActual = _widg.make_entry(width=100, editable=False)
        self.txtGRActualll = _widg.make_entry(width=100, editable=False)
        self.txtGRActualul = _widg.make_entry(width=100, editable=False)
        self.txtRhoInst = _widg.make_entry(width=100, editable=False)
        self.txtRhoInstll = _widg.make_entry(width=100, editable=False)
        self.txtRhoInstul = _widg.make_entry(width=100, editable=False)
        self.txtRhoC = _widg.make_entry(width=100, editable=False)
        self.txtRhoCll = _widg.make_entry(width=100, editable=False)
        self.txtRhoCul = _widg.make_entry(width=100, editable=False)
        self.txtMTBFInst = _widg.make_entry(width=100, editable=False)
        self.txtMTBFInstll = _widg.make_entry(width=100, editable=False)
        self.txtMTBFInstul = _widg.make_entry(width=100, editable=False)
        self.txtMTBFC = _widg.make_entry(width=100, editable=False)
        self.txtMTBFCll = _widg.make_entry(width=100, editable=False)
        self.txtMTBFCul = _widg.make_entry(width=100, editable=False)
        self.txtGoFTrend = _widg.make_entry(width=100, editable=False)
        self.lblGoFModel = _widg.make_label("", width=100)
        self.txtGoFModel = _widg.make_entry(width=100, editable=False)
        self.optLinear = gtk.RadioButton(label=_(u"Use Linear Scales"))
        self.optLinear.set_name('linear')
        self.optLinear.set_active(True)
        self.optLogarithmic = gtk.RadioButton(group=self.optLinear,
                                              label=_(u"Use Logarithmic "
                                                      u"Scales"))
        self.optLogarithmic.set_name('log')

        self.figFigure1 = Figure(figsize=(_width, _height))

        self.pltPlot1 = FigureCanvas(self.figFigure1)

        self.axAxis1 = self.figFigure1.add_subplot(111)

        self.vbxPlot1 = gtk.VBox()

        # Put it all together.
        _toolbar = self._create_toolbar()

        self.notebook = self._create_notebook()

        self.vbxTesting = gtk.VBox()
        self.vbxTesting.pack_start(_toolbar, expand=False)
        self.vbxTesting.pack_start(self.notebook)

        self.notebook.connect('switch-page', self._notebook_page_switched)

    def create_tree(self):
        """
        Creates the Testing treeview and connects it to callback functions to
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
        Method to create the Testing class gtk.Notebook().
        """

        def _create_planning_inputs_tab(self, notebook):
            """
            Function to create the Testing class gtk.Notebook() page for
            displaying test planning inputs for the selected test.

            :param self: the current instance of a Testing class.
            :param notebook: the Testing class gtk.Notebook() widget.
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

            _textview_ = _widg.make_text_view(txvbuffer=self.txtDescription,
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
            _textview = _widg.make_text_view(txvbuffer=self.txtAttachment,
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

            # Set the tooltips for the gtk.Widget().
            self.fxdRGPlan.put(_label, _x_pos + 230, _y_pos[0])

            self.cmbPlanModel.set_tooltip_text(_(u"Selects and displays the "
                                                 u"reliability growth "
                                                 u"planning model to be "
                                                 u"used."))
            self.cmbAssessModel.set_tooltip_text(_(u"Selects and displays the "
                                                   u"reliability growth "
                                                   u"assessment model to be "
                                                   u"used."))
            self.btnFindMTBFI.set_tooltip_text(_(u"Launches the initial MTBF "
                                                 u"calculator."))
            self.btnFindTTFF.set_tooltip_text(_(u"Launches the time to first "
                                                u"fix calculator."))
            self.txtMTBFI.set_tooltip_text(_(u"The initial MTBF for the "
                                             u"selected reliability growth "
                                             u"plan."))
            self.chkFixMTBFI.set_tooltip_text(_(u"Fixes the value of the "
                                                u"initial MTBF when "
                                                u"creating the selected "
                                                u"reliability growth plan."))
            self.txtMTBFG.set_tooltip_text(_(u"The goal MTBF for the "
                                             u"selected reliability growth "
                                             u"plan."))
            self.chkFixMTBFG.set_tooltip_text(_(u"Fixes the value of the "
                                                u"program goal MTBF when "
                                                u"creating the selected "
                                                u"reliability growth plan."))
            self.txtMTBFGP.set_tooltip_text(_(u"The potential MTBF at "
                                              u"maturity for the assembly "
                                              u"associated with the selected "
                                              u"reliability growth plan."))
            self.txtTechReq.set_tooltip_text(_(u"The MTBF require by the "
                                               u"developmental program "
                                               u"associated with the selected "
                                               u"reliability growth plan."))
            self.spnNumPhases.set_tooltip_text(_(u"The number of reliability "
                                                 u"growth phases."))
            self.txtTTFF.set_tooltip_text(_(u"The estimated time to the first "
                                            u"fix during the reliability "
                                            u"growth program."))
            self.chkFixTTFF.set_tooltip_text(_(u"Fixes the value of the time "
                                               u"to first fix when "
                                               u"calculating the selected "
                                               u"reliability growth plan."))
            self.txtTTT.set_tooltip_text(_(u"The total test time."))
            self.chkFixTTT.set_tooltip_text(_(u"Fixes the value of the total "
                                              u"program test time when "
                                              u"calculating the selected "
                                              u"reliability growth plan."))
            self.txtAverageGR.set_tooltip_text(_(u"The average growth rate "
                                                 u"over the entire "
                                                 u"reliability growth "
                                                 u"program."))
            self.chkFixAverageGR.set_tooltip_text(_(u"Fixes the value of the "
                                                    u"average growth rate "
                                                    u"when calculating the "
                                                    u"selected reliability "
                                                    u"growth plan."))
            self.txtAverageFEF.set_tooltip_text(_(u"The average fix "
                                                  u"effectiveness factor "
                                                  u"(FEF) over the entire "
                                                  u"reliability growth "
                                                  u"program."))
            self.txtProgramMS.set_tooltip_text(_(u"The percentage of failure "
                                                 u"that will be addressed by "
                                                 u"corrective action over the "
                                                 u"entire reliability growth "
                                                 u"program."))
            self.chkFixProgramMS.set_tooltip_text(_(u"Fixes the value of the "
                                                    u"management strategy "
                                                    u"when creating the "
                                                    u"selected reliability "
                                                    u"growth plan."))
            self.txtProgramProb.set_tooltip_text(_(u"The probability of "
                                                   u"seeing a failure in any "
                                                   u"phase of the reliability "
                                                   u"growth program."))
            self.chkFixProgramProb.set_tooltip_text(_(u"Fixes the value of "
                                                      u"the probability of "
                                                      u"seeing a failure when "
                                                      u"creating the selected "
                                                      u"reliability growth "
                                                      u"plan."))
            self.txtProducerRisk.set_tooltip_text(_(u"The producer (Type I) "
                                                    u"risk.  This is the risk "
                                                    u"of accepting a system "
                                                    u"when the true "
                                                    u"reliability is below "
                                                    u"the technical "
                                                    u"requirement."))
            self.txtConsumerRisk.set_tooltip_text(_(u"The consumer (Type II) "
                                                    u"risk.  This is the risk "
                                                    u"of rejecting a system "
                                                    u"when the true "
                                                    u"reliability is at least "
                                                    u"the goal reliability."))

            # Position the gtk.Widget() on the page.
            self.fxdRGPlan.put(self.cmbPlanModel, _x_pos, _y_pos[0])
            self.fxdRGPlan.put(self.cmbAssessModel, _x_pos, _y_pos[1])
            # self.fxdRGPlan.put(self.btnFindMTBFI, _x_pos + 125, _y_pos[2])
            self.fxdRGPlan.put(self.btnFindTTFF, _x_pos + 125, _y_pos[7])
            self.fxdRGPlan.put(self.txtMTBFI, _x_pos, _y_pos[2])
            self.fxdRGPlan.put(self.chkFixMTBFI, _x_pos + 240, _y_pos[2])
            self.fxdRGPlan.put(self.txtMTBFG, _x_pos, _y_pos[4])
            self.fxdRGPlan.put(self.chkFixMTBFG, _x_pos + 240, _y_pos[4])
            self.fxdRGPlan.put(self.txtMTBFGP, _x_pos, _y_pos[5])
            self.fxdRGPlan.put(self.txtTechReq, _x_pos, _y_pos[3])
            self.fxdRGPlan.put(self.spnNumPhases, _x_pos, _y_pos[6])
            self.fxdRGPlan.put(self.txtTTFF, _x_pos, _y_pos[7])
            self.fxdRGPlan.put(self.chkFixTTFF, _x_pos + 240, _y_pos[7])
            self.fxdRGPlan.put(self.txtTTT, _x_pos, _y_pos[8])
            self.fxdRGPlan.put(self.chkFixTTT, _x_pos + 240, _y_pos[8])
            self.fxdRGPlan.put(self.txtAverageGR, _x_pos, _y_pos[9])
            self.fxdRGPlan.put(self.chkFixAverageGR, _x_pos + 240, _y_pos[9])
            self.fxdRGPlan.put(self.txtAverageFEF, _x_pos, _y_pos[10])
            # self.fxdRGPlan.put(self.chkFixAverageFEF, _x_pos + 240,
            #                   _y_pos[10])
            self.fxdRGPlan.put(self.txtProgramMS, _x_pos, _y_pos[11])
            self.fxdRGPlan.put(self.chkFixProgramMS, _x_pos + 240,
                               _y_pos[11])
            self.fxdRGPlan.put(self.txtProgramProb, _x_pos, _y_pos[12])
            self.fxdRGPlan.put(self.chkFixProgramProb, _x_pos + 240,
                               _y_pos[12])
            self.fxdRGPlan.put(self.txtProducerRisk, _x_pos, _y_pos[13])
            self.fxdRGPlan.put(self.txtConsumerRisk, _x_pos, _y_pos[14])

            # Initialize some values.
            self.chkFixMTBFI.set_active(True)
            self.chkFixMTBFG.set_active(True)
            self.spnNumPhases.set_adjustment(gtk.Adjustment(0, 0, 100, 1, 1))
            self.chkFixTTFF.set_active(True)
            self.chkFixTTT.set_active(True)
            self.chkFixAverageGR.set_active(True)
            self.chkFixProgramMS.set_active(True)
            self.chkFixProgramProb.set_active(True)

            # Connect gtk.Widget() signals to callback functions.
            self.cmbPlanModel.connect('changed', self._callback_combo, 12)
            self.cmbAssessModel.connect('changed', self._callback_combo, 13)
            self.btnFindTTFF.connect('button-release-event', _mttff_calculator)
            self.txtMTBFI.connect('focus-out-event',
                                  self._callback_entry, 'float', 6)
            self.txtMTBFG.connect('focus-out-event',
                                  self._callback_entry, 'float', 7)
            self.txtMTBFGP.connect('focus-out-event',
                                   self._callback_entry, 'float', 8)
            self.txtTechReq.connect('focus-out-event',
                                    self._callback_entry, 'float', 9)
            self.spnNumPhases.connect('focus-out-event',
                                      self._callback_entry, 'float', 14)
            self.spnNumPhases.connect('value-changed',
                                      self._callback_spin, 14)
            self.txtTTFF.connect('focus-out-event',
                                 self._callback_entry, 'float', 20)
            self.txtTTT.connect('focus-out-event',
                                self._callback_entry, 'float', 16)
            self.txtAverageGR.connect('focus-out-event',
                                      self._callback_entry, 'float', 17)
            self.txtAverageFEF.connect('focus-out-event',
                                       self._callback_entry, 'float', 21)
            self.txtProgramMS.connect('focus-out-event',
                                      self._callback_entry, 'float', 18)
            self.txtProgramProb.connect('focus-out-event',
                                        self._callback_entry, 'float', 19)
            self.txtProducerRisk.connect('focus-out-event',
                                         self._callback_entry, 'float', 11)
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
            #   4. Cumulative test time at end of the test phase
            #   5. Growth Rate for the test phase
            #   6. Number of failures during test phase
            #   7. Average MTBF for the test phase
            #   8. Initial MTBF for the test phase (calculated from the model)
            #   9. Final MTBF for the test phase (calculated from the model)
            # =============================================================== #
            self.tvwRGPlanDetails.set_tooltip_markup(_(u"Displays the details "
                                                       u"of the reliability "
                                                       u"growth plan.  Right "
                                                       u"click any date "
                                                       u"field to show the "
                                                       u"calendar."))
            _labels = [_(u"Phase"), _(u"Test\nArticles"), _(u"Start Date"),
                       _(u"End Date"), _(u"Cumulative\nTest Time"),
                       _(u"Growth Rate"), _(u"Number of\nFailures"),
                       _(u"Average\nMTBF"), _(u"Initial\nMTBF"),
                       _(u"Final\nMTBF")]
            _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_INT,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_INT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
            self.tvwRGPlanDetails.set_model(_model)

            for i in range(10):
                if i == 0:
                    _cell = gtk.CellRendererText()
                    _cell.set_property('editable', 0)
                    _cell.set_property('background', 'light gray')
                else:
                    _cell = gtk.CellRendererText()
                    _cell.set_property('editable', 1)
                    _cell.set_property('background', 'white')
                    _cell.connect('edited', self._rg_plan_edit, i)

                _column = gtk.TreeViewColumn()
                _label = _widg.make_column_heading(_labels[i])
                _column.set_widget(_label)
                _column.pack_start(_cell, True)
                _column.set_resizable(True)
                if i in [0, 1, 6]:
                    _datatype = (i, 'gint')
                elif i in [2, 3]:
                    _datatype = (i, 'gchararray')
    # TODO: Unhide the growth rate column after figuring out a good way to calculate test phase specific growth rates.
                elif i == 5:
                    _datatype = (i, 'gfloat')
                    _column.set_visible(False)
                else:
                    _datatype = (i, 'gfloat')
                _column.set_attributes(_cell, text=i)
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

            :param self: the current instance of a TESTING class.
            :param notebook: the TESTING class gtk.Notebook() widget.
            :type notebook: gtk.NoteBook
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
                        _(u"Program MTBF<sub>G</sub> / MTBF<sub>I</sub>:"),
                        "", "",
                        _(u"The Fix Effectiveness Factor should fall in the "
                          u"range of 0.55 - 0.85.  On average the FEF is "
                          u"0.70."),
                        _(u"Program average FEF:"), "", ""]
            (_x_pos_, _y_pos_) = _widg.make_labels(_labels_,
                                                   self.fxdRGRisk, 5, 5)

            self.chkMIMGP.set_tooltip_text(_(u"Indicates whether or not the "
                                             u"initial MTBF to mature MTBF "
                                             u"ratio is within reasonable "
                                             u"limits."))
            self.chkFEF.set_tooltip_text(_(u"Indicates whether or not the "
                                           u"average fix effectiveness factor "
                                           u"(FEF) is within reasonable "
                                           u"limits."))
            self.chkMGMGP.set_tooltip_text(_(u"Indicates whether or not the "
                                             u"goal MTBF to mature MTBF ratio "
                                             u"is within reasonable limits."))
            self.chkTRMG.set_tooltip_text(_(u"Indicates whether or not the "
                                            u"goal MTBF to initial MTBF ratio "
                                            u"is within reasonable limits."))
            self.pltPlotOC.set_tooltip_text(_(u"Displays the Reliability "
                                              u"Growth plan Operating "
                                              u"Characteristic (OC) curve."))

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
            self.tvwTestFeasibility.set_tooltip_markup(_(u"Displays the "
                                                         u"details of the "
                                                         u"reliability growth "
                                                         u"plan.  Right click "
                                                         u"any date field to "
                                                         u"show the "
                                                         u"calendar."))
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
                    _datatype = (i, 'gfloat')
                else:
                    _datatype = (i, 'gint')
                column.set_cell_data_func(cell, _widg.format_cell,
                                          (i, _datatype))
                column.connect('notify::width', _widg.resize_wrap, cell)
                self.tvwTestFeasibility.append_column(column)

            self.pltPlotOC.mpl_connect('button_press_event', self._expand_plot)
            self.tvwTestFeasibility.connect('button_press_event',
                                            self._treeview_clicked, 2)

            # Insert the tab.
            _label = gtk.Label()
            _label.set_markup("<span weight='bold'>" +
                              _(u"Test\nFeasibility") +
                              "</span>")
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.show_all()
            _label.set_tooltip_text(_(u"Assessment of the feasibility of the "
                                      u"selected test."))

            notebook.insert_page(_hpaned_,
                                 tab_label=_label,
                                 position=-1)

            return False

        def _create_assessment_tab(self, notebook):
            """
            Function to create the Testing class gtk.Notebook() page for
            displaying test assessment results for the selected test.

            :param self: the current instance of a Testing class.
            :param notebook: the Testing class gtk.Notebook() widget.
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
            self.optIndividual.set_tooltip_text(_(u"Estimate parameters based "
                                                  u"on individual failure "
                                                  u"times."))
            self.optGrouped.set_tooltip_text(_(u"Estimate parameters based on "
                                               u"grouped failures times."))
            self.spnConfidence.set_tooltip_text(_(u"Displays the confidence "
                                                  u"level to use for failure "
                                                  u"rate/MTBF bounds and "
                                                  u"goodness of fit (GoF) "
                                                  u"tests."))

            # Place the widgets used to describe the format of the dataset.
            _y_pos = 5
            _fxdDataSet_.put(self.optIndividual, 5, _y_pos)
            _y_pos += 30

            _fxdDataSet_.put(self.optGrouped, 5, _y_pos)
            _y_pos += 25

            _adjustment = gtk.Adjustment(75.0, 50.0, 100.0, 0.5, 0, 0)
            self.spnConfidence.set_adjustment(_adjustment)
            self.spnConfidence.set_digits(1)

            _label = _widg.make_label(_(u"Confidence:"))
            _fxdDataSet_.put(_label, 5, _y_pos)
            _fxdDataSet_.put(self.spnConfidence, 230, _y_pos)
            _y_pos += 25

            _label = _widg.make_label(u"")
            _fxdDataSet_.put(_label, 5, _y_pos)

            self.optIndividual.connect('toggled', self._callback_check, 22)
            self.optGrouped.connect('toggled', self._callback_check, 22)
            self.spnConfidence.connect('focus-out-event',
                                       self._callback_entry, 'float', 26)
            self.spnConfidence.connect('value-changed',
                                       self._callback_spin, 26)

            # Place the gtk.TreeView() that will display the reliability test
            # data.
            _labels = [_(u"Record\nNumber"), _(u"Date"),
                       _(u"Interval\nStart"), _(u"Interval\nEnd"),
                       _(u"Number\nof\nFailures")]
            _model_ = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_INT)
            self.tvwTestAssessment.set_model(_model_)
            self.tvwTestAssessment.set_tooltip_text(_(u"Displays the "
                                                      u"incidents associated "
                                                      u"with the selected "
                                                      u"test plan."))

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
                _column.set_cell_data_func(_cell, _widg.format_cell,
                                           (i, _datatype))
                _column.connect('notify::width', _widg.resize_wrap, _cell)

                self.tvwTestAssessment.append_column(_column)

            # Place the widgets use to display the numerical results of the
            # test data assessment.
            _labels = [_(u"Cum. Test Time:"), _(u"Cum. Failures:")]
            (_x_max, _y_pos1) = _widg.make_labels(_labels,
                                                  _fxdNumericalResults_, 5, 5)
            _labels = [_(u"Lambda:"), _(u"Beta:"), _(u"Observed Growth Rate:"),
                       _(u"Instantaneous Failure Rate:"),
                       _(u"Cumulative Failure Rate:"),
                       _(u"Instantaneous MTBF:"), _(u"Cumulative MTBF:"),
                       _(u"GoF for Model:")]
            (_x_pos, _y_pos2) = _widg.make_labels(_labels,
                                                  _fxdNumericalResults_, 5,
                                                  _y_pos1[1] + 70)
            _x_pos = max(_x_max, _x_pos) + 20
            _y_pos = _y_pos1 + _y_pos2

            self.txtCumTestTime.set_tooltip_text(_(u"Displays the cumulative "
                                                   u"test time to date for "
                                                   u"the selected test."))
            self.txtCumFailures.set_tooltip_text(_(u"Displays the cumulative "
                                                   u"number of failures to "
                                                   u"date for the selected "
                                                   u"test."))
            self.txtScale.set_tooltip_text(_(u"Displays the reliability "
                                             u"growth model estimated scale "
                                             u"parameter."))
            self.txtScalell.set_tooltip_text(_(u"Displays the lower bound on "
                                               u"the reliability growth model "
                                               u"scale parameter."))
            self.txtScaleul.set_tooltip_text(_(u"Displays the upper bound on "
                                               u"the reliability growth model "
                                               u"scale parameter."))
            self.txtShape.set_tooltip_text(_(u"Displays the reliability "
                                             u"growth model estimated shape "
                                             u"parameter."))
            self.txtShapell.set_tooltip_text(_(u"Displays the lower bound on "
                                               u"the reliability growth model "
                                               u"shape parameter."))
            self.txtShapeul.set_tooltip_text(_(u"Displays the upper bound on "
                                               u"the reliability growth model "
                                               u"shape parameter."))
            self.txtGRActual.set_tooltip_text(_(u"Displays the average growth "
                                                u"rate over the reliability "
                                                u"growth program to date."))
            self.txtGRActualll.set_tooltip_text(_(u"Displays the lower bound "
                                                  u"on the average growth "
                                                  u"rate over the reliability "
                                                  u"growth program to date."))
            self.txtGRActualul.set_tooltip_text(_(u"Displays the upper bound "
                                                  u"on the average growth "
                                                  u"rate over the reliability "
                                                  u"growth program to date."))
            self.txtRhoInst.set_tooltip_text(_(u"Displays the currently "
                                               u"assessed instantaneous "
                                               u"failure intensity (failure "
                                               u"rate) of the item under "
                                               u"test."))
            self.txtRhoInstll.set_tooltip_text(_(u"Displays the lower bound "
                                                 u"on the instantaneous "
                                                 u"failure intensity (failure "
                                                 u"rate) of the item under "
                                                 u"test."))
            self.txtRhoInstul.set_tooltip_text(_(u"Displays the upper bound "
                                                 u"on the instantaneous "
                                                 u"failure intensity (failure "
                                                 u"rate) of the item under "
                                                 u"test."))
            self.txtRhoC.set_tooltip_text(_(u"Displays the currently assessed "
                                            u"cumulative failure intensity "
                                            u"(failure rate) of the item "
                                            u"under test."))
            self.txtRhoCll.set_tooltip_text(_(u"Displays the lower bound on "
                                              u"the cumulative failure "
                                              u"intensity (failure rate) of "
                                              u"the item under test."))
            self.txtRhoCul.set_tooltip_text(_(u"Displays the upper bound on "
                                              u"the cumulative failure "
                                              u"intensity (failure rate) of "
                                              u"the item under test."))
            self.txtMTBFInst.set_tooltip_text(_(u"Displays the currently "
                                                u"assessed instantaneous MTBF "
                                                u"of the item under test."))
            self.txtMTBFInstll.set_tooltip_text(_(u"Displays the lower bound "
                                                  u"on the instantaneous MTBF "
                                                  u"of the item under test."))
            self.txtMTBFInstul.set_tooltip_text(_(u"Displays the upper bound "
                                                  u"on the instantaneous MTBF "
                                                  u"of the item under test."))
            self.txtMTBFC.set_tooltip_text(_(u"Displays the currently "
                                             u"assessed cumulative MTBF of "
                                             u"the item under test."))
            self.txtMTBFCll.set_tooltip_text(_(u"Displays the lower bound on "
                                               u"the cumulative MTBF of the "
                                               u"item under test."))
            self.txtMTBFCul.set_tooltip_text(_(u"Displays the upper bound on "
                                               u"the cumulative MTBF of the "
                                               u"item under test."))
            self.txtGoFTrend.set_tooltip_text(_(u"Displays the critical value "
                                                u"for testing the hypothesis "
                                                u"of a good fit to the "
                                                u"selected growth model."))
            self.txtGoFModel.set_tooltip_text(_(u"Displays the goodness of "
                                                u"fit test statistic for "
                                                u"assessing fit to the "
                                                u"selected growth model.  If "
                                                u"this value is less than the "
                                                u"critical value, the model "
                                                u"is a good fit to the data."))

            _fxdNumericalResults_.put(self.txtCumTestTime, _x_pos, _y_pos[0])
            _fxdNumericalResults_.put(self.txtCumFailures, _x_pos, _y_pos[1])

            _label = _widg.make_label(_(u"Lower\nBound"), height=-1, wrap=True,
                                      justify=gtk.JUSTIFY_CENTER)
            _fxdNumericalResults_.put(_label, _x_pos + 5, _y_pos[1] + 35)
            _label = _widg.make_label(_(u"\nEstimate"), height=-1, wrap=True,
                                      justify=gtk.JUSTIFY_CENTER)
            _fxdNumericalResults_.put(_label, _x_pos + 105, _y_pos[1] + 35)
            _label = _widg.make_label(_(u"Upper\nBound"), height=-1, wrap=True,
                                      justify=gtk.JUSTIFY_CENTER)
            _fxdNumericalResults_.put(_label, _x_pos + 205, _y_pos[1] + 35)
            _fxdNumericalResults_.put(self.txtScalell, _x_pos, _y_pos[2])
            _fxdNumericalResults_.put(self.txtScale, _x_pos + 100, _y_pos[2])
            _fxdNumericalResults_.put(self.txtScaleul, _x_pos + 200, _y_pos[2])
            _fxdNumericalResults_.put(self.txtShapell, _x_pos, _y_pos[3])
            _fxdNumericalResults_.put(self.txtShape, _x_pos + 100, _y_pos[3])
            _fxdNumericalResults_.put(self.txtShapeul, _x_pos + 200, _y_pos[3])
            _fxdNumericalResults_.put(self.txtGRActualll, _x_pos, _y_pos[4])
            _fxdNumericalResults_.put(self.txtGRActual, _x_pos + 100,
                                      _y_pos[4])
            _fxdNumericalResults_.put(self.txtGRActualul, _x_pos + 200,
                                      _y_pos[4])
            _fxdNumericalResults_.put(self.txtRhoInstll, _x_pos, _y_pos[5])
            _fxdNumericalResults_.put(self.txtRhoInst, _x_pos + 100, _y_pos[5])
            _fxdNumericalResults_.put(self.txtRhoInstul, _x_pos + 200,
                                      _y_pos[5])
            _fxdNumericalResults_.put(self.txtRhoCll, _x_pos, _y_pos[6])
            _fxdNumericalResults_.put(self.txtRhoC, _x_pos + 100, _y_pos[6])
            _fxdNumericalResults_.put(self.txtRhoCul, _x_pos + 200, _y_pos[6])
            _fxdNumericalResults_.put(self.txtMTBFInstll, _x_pos, _y_pos[7])
            _fxdNumericalResults_.put(self.txtMTBFInst, _x_pos + 100,
                                      _y_pos[7])
            _fxdNumericalResults_.put(self.txtMTBFInstul, _x_pos + 200,
                                      _y_pos[7])
            _fxdNumericalResults_.put(self.txtMTBFCll, _x_pos, _y_pos[8])
            _fxdNumericalResults_.put(self.txtMTBFC, _x_pos + 100, _y_pos[8])
            _fxdNumericalResults_.put(self.txtMTBFCul, _x_pos + 200, _y_pos[8])
            _fxdNumericalResults_.put(self.txtGoFTrend, _x_pos, _y_pos[9])
            _fxdNumericalResults_.put(self.txtGoFModel, _x_pos + 100,
                                      _y_pos[9])
            _fxdNumericalResults_.put(self.lblGoFModel, _x_pos + 205,
                                      _y_pos[9])

            # Place the widgets use to display the graphical results of the
            # test data assessment.
            self.optMTBF.set_tooltip_text(_(u"If selected, test results will "
                                            u"be displayed as MTBF.  This is "
                                            u"the default."))
            self.optFailureIntensity.set_tooltip_text(_(u"If selected, test "
                                                        u"results will be "
                                                        u"displayed as "
                                                        u"failure intensity "
                                                        u"(failure rate)."))
            self.optLinear.set_tooltip_text(_(u"Select this option to use "
                                              u"linear scales on the "
                                              u"reliability growth plot."))
            self.optLogarithmic.set_tooltip_text(_(u"Select this option to "
                                                   u"use logarithmic scales "
                                                   u"on the reliability "
                                                   u"growth plot."))
            self.pltPlot1.set_tooltip_text(_(u"Displays the selected test "
                                             u"plan and observed results."))

            _fxdGraphicalResults_.put(self.optLinear, 5, 5)
            _fxdGraphicalResults_.put(self.optMTBF, 205, 5)
            _fxdGraphicalResults_.put(self.optLogarithmic, 5, 40)
            _fxdGraphicalResults_.put(self.optFailureIntensity, 205, 40)

            _label = _widg.make_label(u"")
            _fxdGraphicalResults_.put(_label, 5, 75)

            self.optMTBF.connect('toggled', self._callback_radio)
            self.optFailureIntensity.connect('toggled', self._callback_radio)
            self.optLinear.connect('toggled', self._callback_radio)
            self.optLogarithmic.connect('toggled', self._callback_radio)
            self.pltPlot1.mpl_connect('button_press_event', self._expand_plot)

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

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
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

    def load_test_assessment_tree(self):
        """
        Method to load the Testing class test data gtk.TreeView().
        """

        _query = "SELECT fld_record_id, fld_request_date, \
                         fld_left_interval, fld_right_interval, \
                         fld_quantity \
                  FROM tbl_survival_data \
                  WHERE fld_dataset_id=%d" % self.test_id
        _results = self._app.DB.execute_query(_query,
                                              None,
                                              self._app.ProgCnx)
        try:
            _n_records = len(_results)
        except TypeError:
            _n_records = 0

        _model = self.tvwTestAssessment.get_model()
        _model.clear()
        for i in range(_n_records):
            _date = str(datetime.fromordinal(
                int(_results[i][1])).strftime('%Y-%m-%d'))
            _model.append([_results[i][0], _date, _results[i][2],
                           _results[i][3], _results[i][4]])

        self.tvwTestAssessment.set_cursor('0', None, False)
        _root = _model.get_iter_root()
        if _root is not None:
            _path = _model.get_path(_root)
            _col = self.tvwRGPlanDetails.get_column(0)
            self.tvwRGPlanDetails.row_activated(_path, _col)

        return False

    def load_notebook(self):
        """
        Method to load the TESTING class gtk.Notebook.
        """

        def _load_planning_tab(self):
            """
            Function to load the widgets on the Test Planning page.

            :param self: the current instance of an Testing class.
            """

            fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

            try:
                _index_ = self._dic_assemblies[self.assembly_id]
            except KeyError:
                _index_ = 0
            self.cmbAssembly.set_active(_index_)
            self.cmbTestType.set_active(self.test_type)
            self.cmbPlanModel.set_active(self.rg_plan_model)
            self.cmbAssessModel.set_active(self.rg_assess_model)
            self.txtName.set_text(self.test_name)
            self.txtDescription.set_text(
                _util.none_to_string(self.test_description))
            self.txtMTBFI.set_text(str(fmt.format(self.mi)))
            self.txtMTBFG.set_text(str(fmt.format(self.mg)))
            self.txtMTBFGP.set_text(str(fmt.format(self.mgp)))
            self.txtTechReq.set_text(str(fmt.format(self.tr)))
            self.txtConsumerRisk.set_text(str(fmt.format(self.consumer_risk)))
            self.txtProducerRisk.set_text(str(fmt.format(self.producer_risk)))
            self.spnNumPhases.set_value(self.n_phases)
            self.txtAttachment.set_text(str(self.attachment))
            self._load_hyperlinks()
            self.txtTTT.set_text(str(fmt.format(self.ttt)))
            self.txtAverageGR.set_text(str(fmt.format(self.avg_growth)))
            self.txtProgramMS.set_text(str(fmt.format(self.avg_ms)))
            self.txtProgramProb.set_text(str(fmt.format(self.probability)))
            self.txtTTFF.set_text(str(fmt.format(self.ttff)))
            self.txtAverageFEF.set_text(str(fmt.format(self.avg_fef)))

            if self.test_type == 5:                 # Reliability growth
                self._rg_plan_details(1)
                self._rg_plan_details(2)

            return False

        (_model, _row) = self.treeview.get_selection().get_selected()
        if _row is not None:
            _load_planning_tab(self)
            self.load_assessment_tab()
            self.load_test_assessment_tree()

        if self._app.winWorkBook.get_child() is not None:
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxTesting)
        self._app.winWorkBook.show_all()

        _title = _(u"RTK Work Book: Program Reliability Testing "
                   u"(%d Tests)") % self.n_tests
        self._app.winWorkBook.set_title(_title)

        # only show the OC curve if the RG planning model is SPLAN or SSPLAN.
        if self.rg_plan_model < 2:
            self.fraOCCurve.hide()
        else:
            self.fraOCCurve.show()

        self.notebook.set_current_page(0)

        return False

    def load_assessment_tab(self):
        """
        Method to load the widgets on the Test Assessment page.
        """

        if self.grouped == 1:
            self.optGrouped.set_active(True)
        else:
            self.optIndividual.set_active(True)

        self.spnConfidence.set_value(self.confidence)
        self.txtCumTestTime.set_text(str(self.cum_time))
        self.txtCumFailures.set_text(str(self.cum_failures))

        return False

    def _update_attributes(self):
        """
        Method to update the Testing class attributes.
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        if _row is not None:
            self.assembly_id = _model.get_value(_row, 1)
            self.test_id = _model.get_value(_row, 2)
            self.test_name = _model.get_value(_row, 3)
            self.test_description = _model.get_value(_row, 4)
            self.test_type = _model.get_value(_row, 5)
            self.mi = _model.get_value(_row, 6)
            self.mg = _model.get_value(_row, 7)
            self.mgp = _model.get_value(_row, 8)
            self.tr = _model.get_value(_row, 9)
            self.consumer_risk = _model.get_value(_row, 10)
            self.producer_risk = _model.get_value(_row, 11)
            self.rg_plan_model = _model.get_value(_row, 12)
            self.rg_assess_model = _model.get_value(_row, 13)
            self.n_phases = _model.get_value(_row, 14)
            self.attachment = _model.get_value(_row, 15)
            self.ttt = _model.get_value(_row, 16)
            self.avg_growth = _model.get_value(_row, 17)
            self.avg_ms = _model.get_value(_row, 18)
            self.probability = _model.get_value(_row, 19)
            self.ttff = _model.get_value(_row, 20)
            self.avg_fef = _model.get_value(_row, 21)
            self.grouped = _model.get_value(_row, 22)
            self.group_interval = _model.get_value(_row, 23)
            self.cum_time = _model.get_value(_row, 24)
            self.cum_failures = _model.get_value(_row, 25)
            self.confidence = _model.get_value(_row, 26)

        return False

    def _expand_plot(self, event):
        """
        Method to display a plot in it's own window.

        :param event: the matplotlib MouseEvent that called this method.
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

    def _load_rg_plot(self, times, ideal, plan, obs):
        """
        Loads the Reliability Growth plot.

        :param TPT: a list of the planned test times for each test phase.
        :param MTBFA: a list of planned average MTBF values for each test
                      phase.
        :param obs: a list of lists of observed values for each test phase.
                    The inner lists contain [Lower Bound, Point, Upper Bound]
                    for the instantaneous failure intensity or instantaneous
                    MTBF at each failure time.
        :return: False if successful or True if an error is encountered.
        :rtype : boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = self.treeview.get_selection().get_selected()
        _MTBFI = _model.get_value(_row, 6)
        _ttt = _model.get_value(_row, 16)
        _AvgGR = _model.get_value(_row, 17)
        _ti = _model.get_value(_row, 20)
        _alpha = float(self.spnConfidence.get_value())

        if self.optMTBF.get_active():
            _targets = [_model.get_value(_row, 9)]
            _targets.append(_model.get_value(_row, 7))
            _targets.append(_model.get_value(_row, 8))
        elif self.optFailureIntensity.get_active():
            _targets = [1.0 / _model.get_value(_row, 9)]
            _targets.append(1.0 / _model.get_value(_row, 7))
            _targets.append(1.0 / _model.get_value(_row, 8))

        # Plot all the information.
        self.axAxis1.cla()

        # Plot the observed instantaneous MTBF values and bounds if there are
        # any observed values.
        if len(obs) > 3:

            # Update the left interval time using the previous record's right
            # interval value if the data is grouped.  Create a list of observed
            # cumulative failure times to use when plotting the results.
            _f_time = 0.0
            _obs_times = []
            _model = self.tvwTestAssessment.get_model()
            _row = _model.get_iter_root()
            while _row is not None:
                if self.optGrouped.get_active():
                    _model.set_value(_row, 2, _f_time)
                    _f_time = _model.get_value(_row, 3)
                    _obs_times.append(_f_time)
                else:
                    _f_time = _model.get_value(_row, 3)
                    _model.set_value(_row, 2, _f_time)
                    _obs_times.append(_f_time)

                _row = _model.iter_next(_row)

            _obs_times[-1] = min(_ttt, _obs_times[-1])

            _obsll = np.array([y[1] - y[0] for y in obs])
            _obspt = np.array([y[1] for y in obs])
            _obsul = np.array([y[2] - y[1] for y in obs])

            _obsll[np.isnan(_obsll)] = 0.0
            _obsll[np.isinf(_obsll)] = 0.0
            _obsll[np.where(_obsll) < 0.0] = 0.0
            _obspt[np.isnan(_obspt)] = 0.0
            _obspt[np.isinf(_obspt)] = 0.0
            _obsul[np.isnan(_obsul)] = 0.0
            _obsul[np.isinf(_obsul)] = 0.0

            # Plot the observed values with error bars indicating bounds at
            # each observation.
            self.axAxis1.errorbar(_obs_times, _obspt, yerr=[_obsll, _obsul],
                                  fmt='o', ecolor='k', color='k')

            # Create the legend text.
            _legend = tuple([_(u"Observed w/ {0:0.1f}% Error "
                               u"Bars".format(_alpha)),
                             _(u"Idealized Growth Curve"),
                             _(u"Planned Growth Curve"), _(u"Target Values")])

            # Find the minimum and maximum y-value.
            _y_min = max(0.0, min(_obsll))
            if max([y[2] for y in obs]) > 1.1 * max(_obspt):
                _y_max = max(max(_targets), max(_obspt), max(ideal),
                             max(plan))
            else:
                _y_max = max(max(_targets), max(_obspt),
                             max([y[0] for y in obs]),
                             max([y[2] for y in obs]), max(ideal), max(plan))

        else:
            # Create the legend text.
            _legend = tuple([_(u"Idealized Growth Curve"),
                             _(u"Planned Growth Curve"), _(u"Target Values")])

            # Find the minimum and maximum y-value.
            _y_min = max(0.0, min(_targets), min(ideal), min(plan))
            _y_max = max(max(_targets), max(ideal), max(plan))

        # Add the idealized growth curve.
        _line = matplotlib.lines.Line2D(times, ideal,
                                        lw=1.5, color='b')
        self.axAxis1.add_line(_line)

        # Add the planned growth curve.
        _line = matplotlib.lines.Line2D(times, plan,
                                        lw=1.5, color='r')
        self.axAxis1.add_line(_line)

        # Show the target values on the plot.
        for i in range(len(_targets)):
            self.axAxis1.axhline(y=_targets[i], xmin=0, color='m',
                                 linewidth=2.5, linestyle=':')
        if self.optLogarithmic.get_active():
            self.axAxis1.set_xscale('log')
            self.axAxis1.set_yscale('log')
        else:
            self.axAxis1.set_xscale('linear')
            self.axAxis1.set_yscale('linear')

        for i in range(len(_targets)):
            self.axAxis1.annotate(str(fmt.format(_targets[i])),
                                  xy=(_ttt, _targets[i]),
                                  xycoords='data',
                                  xytext=(25, -25),
                                  textcoords='offset points',
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

        # Create and place the legend.
        _leg = self.axAxis1.legend(_legend, 'upper left', shadow=True)
        for _text in _leg.get_texts():
            _text.set_fontsize('small')
        for _line in _leg.get_lines():
            _line.set_linewidth(0.5)

        # Add labels to the axes and adjust them slightly for readability.
        self.axAxis1.set_xlabel(_(u"Cumulative Test Time"))
        if self.optMTBF.get_active():
            self.axAxis1.set_ylabel(u"MTBF")
        elif self.optFailureIntensity.get_active():
            self.axAxis1.set_ylabel(_(u"Failure Intensity"))
        self.axAxis1.set_xlim(right=1.1 * _ttt)
        self.axAxis1.set_ylim(bottom=_y_min, top=1.05 * _y_max)

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
                _util.rtk_error(_(u"File %s does not exist" % _text_))

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

        (_model, _paths) = self.treeview.get_selection().get_selected_rows()

        _records = []
        for i in range(len(_paths)):
            _row = _model.get_iter(_paths[i])
            _records.append(_model.get_value(_row, 1))

        _title = _(u"RTK: Confirm Delete")
        _dialog = _widg.make_dialog(_title)

        _fixed = gtk.Fixed()

        y_pos = 10

        _label = _widg.make_label(_(u"Are you sure you want to delete the "
                                    u"selected test plan(s)."), 600, 250)
        _fixed.put(_label, 5, y_pos)

        _fixed.show_all()

        _dialog_.vbox.pack_start(_fixed)

        if _dialog.run() == gtk.RESPONSE_ACCEPT:
            for i in range(len(_records)):
                _query = "DELETE FROM tbl_tests \
                          WHERE fld_test_id=%d" % _records[i]
                self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                           commit=True)

        _dialog.destroy()

        self.load_tree()

        return False

    def _calculate(self, __button):
        """
        Method to perform calculations for the Testing class.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: gtk.ToolButton
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = self.treeview.get_selection().get_selected()

        # Initialize variables.
        _plan_inputs = {}

        N = [0]                             # Cumulative failures per phase.
        TTTi = []                           # Total test time for each phase.
        MTBFAP = []                         # Average planned MTBF.
        _plan = []
        _X = []                             # Failure times.
        _F = []                             # Number of failures at each time.
        _plot_mtbfi = []
        _plot_rhoi = []
        _lambda_hat = [0.0, 0.0, 0.0]       # Scale parameter estimates.
        _beta_hat = [0.0, 0.0, 0.0]         # Shape parameter estimates.
        _rho_c = [0.0, 0.0, 0.0]            # Cum. failure intensity
        _rho_i = [0.0, 0.0, 0.0]            # Instantaneous failure intensity
        _mu_c = [0.0, 0.0, 0.0]             # Cumulative MTBF
        _mu_i = [0.0, 0.0, 0.0]             # Instantaneous MTBF
        _gr = [0.0, 0.0, 0.0]               # Growth rate estimates.
        _crit_vals = []                     # Trend and GoF critical values.

        _N = 0

        _util.set_cursor(self._app, gtk.gdk.WATCH)

        # Read test input values.
        _alpha = self.spnConfidence.get_value() / 100.0
        _alpha_half = (1.0 - _alpha) / 2.0
        MTBFI = _model.get_value(_row, 6)
        MTBFF = _model.get_value(_row, 9)
        self.gp = _model.get_value(_row, 8)
        TTT = _model.get_value(_row, 16)
        t1 = _model.get_value(_row, 20)
        AvgMS = _model.get_value(_row, 18)
        AvgGR = _model.get_value(_row, 17)
        Prob = _model.get_value(_row, 19)
        AvgFEF = _model.get_value(_row, 21)

        # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
        # Calculate the idealized growth curve.                             #
        # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
        # Calculate initial MTBF.
        if not self.chkFixMTBFI.get_active():
            MTBFI = initial_mtbf(TTT, t1, MTBFF, AvgGR, AvgMS, Prob)

        # Calculate final MTBF.
        if not self.chkFixMTBFG.get_active():
            MTBFF = final_mtbf(TTT, t1, MTBFI, AvgGR)

        # Calculate total test time.
        if not self.chkFixTTT.get_active():
            TTT = total_time(t1, MTBFI, MTBFF, AvgGR)

        #if not self.chkFixTTFF.get_active():
        #    t1 = minimum_first_phase_time(MTBFI, AvgMS, Prob)

        # Calculate the management strategy.
        if not self.chkFixProgramMS.get_active():
            AvgMS = management_strategy(MTBFI, self.gp, AvgFEF)

        # Calculate the growth rate.
        if not self.chkFixAverageGR.get_active():
            AvgGR = growth_rate(TTT, t1, MTBFI, MTBFF)

        # Calculate the probability of seeing at least one failure.
        if not self.chkFixProgramProb.get_active():
            Prob = prob(t1, MTBFI, AvgMS)

        self.mgp = growth_potential(MTBFI, AvgMS, AvgFEF)
        if not isinstance(self.mgp, (int, long, float)):
            self.mgp = MTBFF

        _model.set_value(_row, 6, MTBFI)
        _model.set_value(_row, 9, MTBFF)
        _model.set_value(_row, 8, self.mgp)
        _model.set_value(_row, 16, TTT)
        _model.set_value(_row, 17, AvgGR)
        _model.set_value(_row, 18, AvgMS)
        _model.set_value(_row, 19, Prob)

        self.txtMTBFI.set_text(str(fmt.format(MTBFI)))
        self.txtTechReq.set_text(str(fmt.format(MTBFF)))
        self.txtMTBFGP.set_text(str(fmt.format(self.mgp)))
        self.txtTTT.set_text(str(fmt.format(TTT)))
        self.txtAverageGR.set_text(str(fmt.format(AvgGR)))
        self.txtProgramMS.set_text(str(fmt.format(AvgMS)))
        self.txtProgramProb.set_text(str(fmt.format(Prob)))

        # Calculate the ideal growth curve from 0 - TTT in steps of one.
        _times = range(int(TTT))
        _ideal = idealized_values(TTT, t1, MTBFI, AvgGR,
                                  self.optMTBF.get_active())

        # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
        # Reliability growth planning phase specific calculations.          #
        # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
        # Calculate the minimum recommended length of the first test phase and
        # compare it to the user-supplied length of the first test phase, if
        # any.
        _t1 = minimum_first_phase_time(TTT, MTBFF, MTBFI, AvgGR)

        __model = self.tvwRGPlanDetails.get_model()
        __row = __model.get_iter_root()
        if __model.get_value(__row, 4) < _t1:
            _response = _util.rtk_question(_(u"The planned length of the "
                                             u"first test phase is less than "
                                             u"the minimum recommended length "
                                             u"of the first test phase.\n\n"
                                             u"Planned length: %f\n"
                                             u"Recommended length: %f\n\n"
                                             u"The probability of observing a "
                                             u"failure during the first test "
                                             u"phase is reduced.  Without a "
                                             u"test failure, there can be no "
                                             u"reliability growth.  Should "
                                             u"RTK set the length of phase 1 "
                                             u"equal to the recommended "
                                             u"minimum value?") %
                                           (__model.get_value(__row, 4), _t1))
            if _response == gtk.RESPONSE_YES:
                __model.set_value(__row, 4, _t1)

        planned_growth_curve(__model, __row, __model.get_value(__row, 4),
                             MTBFI, AvgGR)

        # Create the list of planned MTBF values.
        __row = __model.get_iter_root()
        _ttti = 0
        while __row is not None:
            _tttj = int(__model.get_value(__row, 4)) - _ttti
            _plan += planned_values(_tttj, __model.get_value(__row, 7))
            _ttti = int(__model.get_value(__row, 4))
            __row = __model.iter_next(__row)

        # Assess the feasibility of the plan.
        self._assess_plan_feasibility()

        # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
        # Reliability growth assessment calculations.                       #
        # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
        # Iterate through each of the records in the assessment data.  If
        # there is more than one record available, estimate reliability
        # growth model parameters and create a list of observed failure rates
        # and MTBF values to use for plotting.
        __model = self.tvwTestAssessment.get_model()
        __row = __model.get_iter_root()
        while __row is not None:
            _X.append(__model.get_value(__row, 3))
            _F.append(__model.get_value(__row, 4))

            _M = len(_X)                    # Total number of groups.
            _N = sum(_F)                    # Total number of failures.

# TODO: Add gtk.Entry() for entering termination time for a time terminated test.
            _T_star = _X[-1]                # Test termination time.

            # Estimate model parameters and bounds.
            if _N > 1:
                if not self.optGrouped.get_active():  # Exact failure times.
                    (_lambda_hat[1],
                     _beta_hat[1]) = crow_amsaa_parameters(_F, _X,
                                                           grouped=False)

                elif self.optGrouped.get_active():    # Grouped failure times.
                    (_lambda_hat[1],
                     _beta_hat[1]) = crow_amsaa_parameters(_F, _X,
                                                           grouped=True)
# TODO: Add a gtk.ComboBox() to select confidence bound types for RG assessment.  Default to Crow bounds until then.
            # Calculate the confidence bounds for the model parameters.
            (_lambda_hat[0],
             _lambda_hat[2]) = crow_bounds(_N, _T_star, _lambda_hat[1],
                                           _beta_hat[1], _alpha, 2)
            (_beta_hat[0],
             _beta_hat[2]) = crow_bounds(_N, _T_star, _lambda_hat[1],
                                         _beta_hat[1], _alpha, 1)

            # Calculate MTBF and failure intensity point estimates.
            (_mu_c[1],
             _mu_i[1]) = crow_amsaa_mean(_lambda_hat[1], _beta_hat[1], _T_star)

            _rho_c[1] = 1.0 / _mu_c[1]
            _rho_i[1] = 1.0 / _mu_i[1]

            # Calculate bounds on the MTBF and failure intensities.
            (_rho_c[0],
             _rho_c[2]) = crow_bounds(_N, _T_star, _lambda_hat[1],
                                      _beta_hat[1], _alpha, 3)

            _mu_c[0] = 1.0 / _rho_c[2]
            _mu_c[2] = 1.0 / _rho_c[0]

            _rho_i[0] = _lambda_hat[0] * _beta_hat[0] * \
                _T_star**(_beta_hat[0] - 1.0)
            _rho_i[2] = _lambda_hat[2] * _beta_hat[2] * \
                _T_star**(_beta_hat[2] - 1.0)

            _mu_i[0] = 1.0 / _rho_i[2]
            _mu_i[2] = 1.0 / _rho_i[0]

            # Append calculated MTBF and failure intensity values to the lists
            # passed to the plotting method.
            _plot_mtbfi.append([_mu_i[0], _mu_i[1], _mu_i[2]])
            _plot_rhoi.append([_rho_i[0], _rho_i[1], _rho_i[2]])

            __row = __model.iter_next(__row)

        self.cum_time = _T_star
        self.cum_failures = _N

        # Calculate critical values for GoF tests.
        _chi2_critical_l = chi2.ppf(_alpha_half, 2 * _N)
        _chi2_critical_u = chi2.ppf(_alpha + _alpha_half, 2 * _N)

        _probs = self._cvm_table.get(_M, self._cvm_table[min(self._cvm_table.keys(), key=lambda k: abs(k - _M))])
        _cvm_critical = _probs.get(2.0 * _alpha_half, _probs[min(_probs.keys(), key=lambda k: abs(k - 2.0 * _alpha_half))])

        if not self.optGrouped.get_active():    # Exact failure times.
            # Test the hypothesis that the data fits the Crow-AMSAA model.
            #
            #       Ho: the data fits the Crow-AMSAA model
            #       Ha: the data does not fit the Crow-AMSAA model
            #
            # Reject Ho if _CvM exceeds the critical value.
            _cvm = cramer_von_mises(_X, _beta_hat[1], _T_star, type2=True)
            self.txtGoFTrend.set_text(str(fmt.format(_cvm_critical)))
            self.txtGoFModel.set_text(str(fmt.format(_cvm)))
            if _cvm < _cvm_critical:
                self.lblGoFModel.set_markup(_(u"<span foreground='green'>"
                                              u"Good Fit</span>"))
            else:
                self.lblGoFModel.set_markup(_(u"<span foreground='red'>"
                                              u"Poor Fit</span>"))

        elif self.optGrouped.get_active():      # Grouped failure times.
            # Test the hypothesis that the data fits the Crow-AMSAA model.
            #
            #       Ho: the data fits the Crow-AMSAA model
            #       Ha: the data does not fit the Crow-AMSAA model
            #
            # Reject Ho if _chi2 exceeds the critical values.
            _chi2 = crow_amsaa_chi_square(_F, _X,
                                          _lambda_hat[1], _beta_hat[1])
            self.txtGoFTrend.set_text(str(fmt.format(_chi2_critical_u)))
            self.txtGoFModel.set_text(str(fmt.format(_chi2)))
            if _chi2 > _chi2_critical_l and _chi2 < _chi2_critical_u:
                self.lblGoFModel.set_markup(_(u"<span foreground='green'>"
                                              u"Good Fit</span>"))
            else:
                self.lblGoFModel.set_markup(_(u"<span foreground='red'>"
                                              u"Poor Fit</span>"))

        if _N > 1:
            # Calculate the growth rate and it's bounds.
            _gr[0] = 1.0 - _beta_hat[2]
            _gr[1] = 1.0 - _beta_hat[1]
            _gr[2] = 1.0 - _beta_hat[0]

            # Load the results.
            _model.set_value(_row, 24, _T_star)
            _model.set_value(_row, 25, _N)
            self.txtScalell.set_text(str(fmt.format(_lambda_hat[0])))
            self.txtScale.set_text(str(fmt.format(_lambda_hat[1])))
            self.txtScaleul.set_text(str(fmt.format(_lambda_hat[2])))
            self.txtShapell.set_text(str(fmt.format(_beta_hat[0])))
            self.txtShape.set_text(str(fmt.format(_beta_hat[1])))
            self.txtShapeul.set_text(str(fmt.format(_beta_hat[2])))
            self.txtGRActualll.set_text(str(fmt.format(_gr[0])))
            self.txtGRActual.set_text(str(fmt.format(_gr[1])))
            self.txtGRActualul.set_text(str(fmt.format(_gr[2])))
            self.txtRhoInstll.set_text(str(fmt.format(_rho_i[0])))
            self.txtRhoInst.set_text(str(fmt.format(_rho_i[1])))
            self.txtRhoInstul.set_text(str(fmt.format(_rho_i[2])))
            self.txtRhoCll.set_text(str(fmt.format(_rho_c[0])))
            self.txtRhoC.set_text(str(fmt.format(_rho_c[1])))
            self.txtRhoCul.set_text(str(fmt.format(_rho_c[2])))
            self.txtMTBFInstll.set_text(str(fmt.format(_mu_i[0])))
            self.txtMTBFInst.set_text(str(fmt.format(_mu_i[1])))
            self.txtMTBFInstul.set_text(str(fmt.format(_mu_i[2])))
            self.txtMTBFCll.set_text(str(fmt.format(_mu_c[0])))
            self.txtMTBFC.set_text(str(fmt.format(_mu_c[1])))
            self.txtMTBFCul.set_text(str(fmt.format(_mu_c[2])))

            self.load_assessment_tab()

        # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
        # Plot the ideal curve, planned curve, and actual results (if any). #
        # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
        if self.optMTBF.get_active():
            self._load_rg_plot(_times, _ideal, _plan, _plot_mtbfi)
        elif self.optFailureIntensity.get_active():
            self._load_rg_plot(_times, _ideal, _plan, _plot_rhoi)

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)

        return False

    def _assess_plan_feasibility(self):
        """
        Method to assess the feasibility of a test plan.  The assessment
        criteria come from MIL-HDBK-189C, section 5.1.5 and section 5.1.6.\n\n

        The criteria and acceptable ranges are:\n

        - Initial MTBF / Goal MTBF              0.15 - 0.47\n
        - Goal MTBF / Growth Potential MTBF     0.60 - 0.80\n
        - Growth Rate                           0.23 - 0.64\n
        - Fix Effectiveness Factor              0.55 - 0.85\n

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _test_type = self.cmbTestType.get_active()

        # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
        # Reliability growth planning feasibility assessment.               #
        # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ #
        if _test_type == 5:
            _ttt = []
            _n = []
            _model = self.tvwRGPlanDetails.get_model()
            _row = _model.get_iter_root()
            while _row is not None:
                _ttt.append(_model.get_value(_row, 4))
                _n.append(_model.get_value(_row, 6))

                _row = _model.iter_next(_row)

            _mtbfi = float(self.txtMTBFI.get_text())
            _mtbfg = float(self.txtMTBFG.get_text())
            _mtbfgp = float(self.txtMTBFGP.get_text())
            _fef = float(self.txtAverageFEF.get_text())

            # Initial MTBF to growth potential MTBF ratio is high enough.  Too
            # low means growth testing is probably being started too early.
            try:
                self.txtMIMGP.set_text(str(fmt.format(_mtbfi / _mtbfgp)))
            except ZeroDivisionError:
                self.txtMIMGP.set_text("0.0")

            if _mtbfi / _mtbfgp >= 0.15 and _mtbfi / _mtbfgp <= 0.47:
                self.chkMIMGP.set_active(True)
            else:
                self.chkMIMGP.set_active(False)

            if _mtbfi / _mtbfgp >= 0.35:
                _text = "<span foreground='#00CC00'>Low Risk</span>"
            elif _mtbfi / _mtbfgp < 0.35 and _mtbfi / _mtbfgp >= 0.2:
                _text = "<span foreground='#D5D515'>Medium Risk</span>"
            else:
                _text = "<span foreground='red'>High Risk</span>"
            self.lblMIMGP.set_markup(_text)

            # Goal MTBF to growth potential MTBF ratio is high enough.  Too
            # high means there is a low probability of achieving the goal MTBF.
            # Too low means the system may be over designed.
            self.txtMGMGP.set_text(str(fmt.format(_mtbfg / _mtbfgp)))
            if _mtbfg / _mtbfgp >= 0.6 and _mtbfg / _mtbfgp <= 0.8:
                self.chkMGMGP.set_active(True)
            else:
                self.chkMGMGP.set_active(False)

            if _mtbfg / _mtbfgp <= 0.7:
                _text = "<span foreground='#00CC00'>Low Risk</span>"
            elif _mtbfg / _mtbfgp > 0.7 and _mtbfg / _mtbfgp <= 0.8:
                _text = "<span foreground='#D5D515'>Medium Risk</span>"
            else:
                _text = "<span foreground='red'>High Risk</span>"
            self.lblMGMGP.set_markup(_text)

            # Program average growth rate.
            self.txtTRMG.set_text(str(self.avg_growth))
            if self.avg_growth >= 0.23 and self.avg_growth <= 0.64:
                self.chkTRMG.set_active(True)
            else:
                self.chkTRMG.set_active(False)

            if self.avg_growth < 0.35:
                _text = "<span foreground='#00CC00'>Low Risk</span>"
            elif self.avg_growth >= 0.35 and self.avg_growth <= 0.55:
                _text = "<span foreground='#D5D515'>Medium Risk</span>"
            else:
                _text = "<span foreground='red'>High Risk</span>"
            self.lblMGMI.set_markup(_text)

            # Fix effectiveness factor is low enough, but not too low.  Too low
            # means many failures will not be corrected, too high means it may
            # not be possible to remove enough failures from the system.
            self.txtFEF.set_text(str(fmt.format(_fef)))
            if _fef >= 0.55 and _fef <= 0.85:
                self.chkFEF.set_active(True)
            else:
                self.chkFEF.set_active(False)

            if _fef <= 0.7:
                self.lblFEF.set_markup("<span foreground='#00CC00'>"
                                       "Low Risk</span>")
            elif _fef > 0.7 and _fef <= 0.8:
                self.lblFEF.set_markup("<span foreground='#D5D515'>"
                                       "Medium Risk</span>")
            else:
                self.lblFEF.set_markup("<span foreground='red'>"
                                       "High Risk</span>")

            # Reliability growth planning feasibility per phase.
            i = 0
            _model = self.tvwTestFeasibility.get_model()
            _row = _model.get_iter_root()
            while _row is not None:
                _articles = _model.get_value(_row, 1)
                _dt_start = datetime.strptime(_model.get_value(_row, 2),
                                              "%Y-%m-%d").toordinal()
                _dt_end = datetime.strptime(_model.get_value(_row, 3),
                                            "%Y-%m-%d").toordinal()
                _weeks = (_dt_end - _dt_start) / 7.0

                try:
                    _tpu = _ttt[i] / _articles
                except ZeroDivisionError:
                    _util.rtk_warning(_(u"You have not entered the number of "
                                        u"test units for test phase %d.  "
                                        u"Unable to calculate the average "
                                        u"test time per test unit.  Please "
                                        u"enter the number of test units for "
                                        u"test phase %d and try again.") %
                                      ((i + 1), (i + 1)))
                    _tpu = 0.0

                try:
                    _tpupw = _tpu / _weeks
                except ZeroDivisionError:
                    _util.rtk_warning(_(u"Start date and end date are the "
                                        u"same for test phase %d.  Unable to "
                                        u"calculate the average test time "
                                        u"per week for a test unit.  Please "
                                        u"correct one or both dates and try "
                                        u"again.") % (i + 1))
                    _tpupw = 0.0

                _model.set_value(_row, 4, _n[i])
                _model.set_value(_row, 7, _tpu)
                _model.set_value(_row, 8, _tpupw)

                i += 1
                _row = _model.iter_next(_row)

        return False

    def test_plan_save(self, __button):
        """
        Saves the Testing class gtk.TreeView() information to the open RTK
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

        :param model: the Testing class reliability growth phase
                      gtk.TreeModel().
        :type model: gtk.TreeModel
        :param string __path: the path of the active row in the Testing class
                              reliability growth phase gtk.TreeModel().
        :param row: the gtk.TreeIter() of the active row in the Testing class
                    reliability growth phase gtk.TreeView().
        :type row: gtk.TreeIter
        """

        _dt_start = datetime.strptime(model.get_value(row, 2),
                                      "%Y-%m-%d").toordinal()
        _dt_end = datetime.strptime(model.get_value(row, 3),
                                    "%Y-%m-%d").toordinal()
        _query = "UPDATE tbl_rel_growth \
                  SET fld_test_units=%d, fld_start_date='%s', \
                      fld_end_date='%s', fld_test_time=%f, \
                      fld_growth_rate=%f, fld_num_fails=%d, fld_ma=%f, \
                      fld_mi=%f, fld_mf=%f \
                  WHERE fld_phase_id=%d \
                  AND fld_test_id=%d" % \
                 (model.get_value(row, 1), _dt_start, _dt_end,
                  model.get_value(row, 4), model.get_value(row, 5),
                  model.get_value(row, 6), model.get_value(row, 7),
                  model.get_value(row, 8), model.get_value(row, 9),
                  model.get_value(row, 0), self.test_id)
        if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                          commit=True):
            _util.rtk_error(_(u"Error saving reliability growth phase %d.") %
                            model.get_value(row, 0))
            return True

        return False

    def _save_rg_feasibility(self, model, __path, row):
        """
        Method to save the reliability growth phase feasibility information.

        Keyword Arguments:
        :param model: the TESTING class reliability growth phase feasibility
                      gtk.TreeModel().
        :type model: gtk.TreeModel
        :param __path: the path of the active row in the TESTING class
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
        :param __path: the path of the active row in the TESTING class
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
        Callback function to retrieve and save gtk.CheckButton() changes for
        the Testing class.

        :param check: the gtk.CheckButton() that called the function.
        :type check: gtk.CheckButton
        :param index: the position in the Testing class gtk.TreeModel()
                      associated with the data from the calling checkbutton.
        :type index: integer
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        # Update the Testing Tree.
        if index == 22:
            if self.optIndividual.get_active():
                _model.set_value(_row, index, 0)
            else:
                _model.set_value(_row, index, 1)

        else:
            _model.set_value(_row, index, check.get_active())

        self._update_attributes()

        return False

    def _callback_combo(self, combo, index):
        """
        Callback function to retrieve and save gtk.ComboBox changes for the
        Testing class.

        :param combo: the gtk.ComboBox() that called the function.
        :type combo: gtk.ComboBox
        :param index: the position in the Testing class gtk.TreeModel()
                      associated with the data from the calling combobox.
        :type index: integer
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        _text = combo.get_active()

        # Index     Field
        #    1      Assembly ID
        #    5      Test Type
        #   12      RG Planning Model
        #   13      RG Assessment Model
        if index == 1:
            model = combo.get_model()
            row = combo.get_active_iter()
            if row is not None:
                try:
                    _text = int(model.get_value(row, 1))
                except ValueError:
                    _text = 0
            else:
                _text = 0
        else:
            _text = combo.get_active()

        # If we've selected a new type of test, make sure we display the
        # correct detailed planning information.
        if index == 5:
            if _text == 1:                  # HALT
                _label = _(u"Highly Accelerated Life Test Planning Inputs")
            elif _text == 2:                # HASS
                _label = _(u"Highly Accelerated Stress Screening Planning "
                           u"Inputs")
            elif _text == 3:                # ALT
                _label = _(u"Accelerated Life Test Planning Inputs")
            elif _text == 4:                # ESS
                _label = _(u"Environmental Stress Screening Planning Inputs")
            elif _text == 5:                # Reliability Growth
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
            elif _text == 6:                # Reliability Demonstration
                _label = _(u"Reliability Demonstration/Qualification Test "
                           u"Planning Inputs")
            elif _text == 7:                # PRVT
                _label = _(u"Production Reliability Verification Test "
                           u"Planning Inputs")
        elif index == 12:                   # RG planning model
            if _text < 2:
                self.fraOCCurve.hide()
            else:
                self.fraOCCurve.show()

        # Try to update the Testing class gtk.TreeModel().  Just keep going
        # if no row is selected.
        try:
            _model.set_value(_row, index, _text)
        except TypeError:
            pass

        self._update_attributes()

        return False

    def _callback_entry(self, entry, __event, convert, index):
        """
        Callback function to retrieve and save gtk.Entry() changes for the
        Testing class.

        :param entry: the gtk.Entry() that called this method.
        :type entry: gtk.Entry
        :param  __event: the gtk.gdk.Event() that called this method.
        :type __event: gtk.gdk.Event
        :param convert: the data type to convert the entry contents to.
        :type convert: string
        :param index: the position in the applicable gtk.TreeModel() associated
                      with the data from the calling gtk.Entry().
        :type index: integer
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
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

        self._update_attributes()

        return False

    def _callback_radio(self, button):
        """
        Callback function to retrieve and save gtk.RadioButton() changes for
        the Testing class.

        :param button: the gtk.RadioButton() that called the function.
        :type button: gtk.RadioButton
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if button.get_name() == 'linear':
            self.axAxis1.set_xscale('linear')
            self.axAxis1.set_yscale('linear')
            self.pltPlot1.draw()
        elif button.get_name() == 'log':
            self.axAxis1.set_xscale('log')
            self.axAxis1.set_yscale('log')
            self.pltPlot1.draw()

        self._update_attributes()

        return False

    def _callback_spin(self, spin, index):
        """
        Callback function to retrieve and save gtk.SpinButton() changes for the
        Testing class.

        :param spin: the gtk.SpinButton() that called the function.
        :type spin: gtk.SpinButton
        :param index: the position in the Testing class gtk.TreeModel()
                      associated with the data from the calling
                      gtk.SpinButton().
        :type index: integer
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if index == 14 and self.test_id > 1000:  # Number of RG phases.
            _value = spin.get_value_as_int()

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
            if _value < self.n_phases:
                _diff = self.n_phases - _value
                for i in range(_diff):
                    _query = "DELETE FROM tbl_rel_growth \
                              WHERE fld_test_id=%d \
                              AND fld_phase_id=%d" % \
                             (self.test_id, self.n_phases)
                    self._app.DB.execute_query(_query,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

            # If spinning up, add phases until the number of phases is equal
            # to the spinner value.
            elif _value > self.n_phases:
                _diff = _value - self.n_phases
                for i in range(_diff):
                    _query = "INSERT INTO tbl_rel_growth \
                              (fld_test_id, fld_phase_id) \
                              VALUES(%d, %d)" % \
                             (self.test_id, i + self.n_phases + 1)
                    self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                               commit=True)

            self._load_rg_plan_tree()
            self._load_rg_feasibility_tree()

        else:
            _value = spin.get_value()

        # Try to update the gtk.TreeModel.  Just keep going if no row is
        # selected.
        try:
            (_model, _row) = self.treeview.get_selection().get_selected()
            _model.set_value(_row, index, _value)
        except ValueError:
            pass
        except TypeError:
            pass

        self._update_attributes()

        return False

    def _toolbutton_pressed(self, button):
        """
        Method to react to the Testing class toolbar button clicked events.

        :param button: the gtk.ToolButton() that was pressed.
        :type : gtk.ToolButton
        :return: False if successful or True if an error is encountered.
        :rtype: booelan
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
        :return: False if successful or True if an error is encountered.
        :rtype: booelan
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

        :param index: the index of the
        :type index: integer
        :return: False if successful or True if an error is encountered.
        :rtype: booelan
        """

        if index == 1:
            if self.fraPlanDetails.get_child() is not None:
                self.fraPlanDetails.remove(self.fraPlanDetails.get_child())

            self.fraPlanDetails.add(self.scwRGPlanDetails)
            self.fraPlanDetails.show_all()

            label = self.fraPlanDetails.get_label_widget()

            self._load_rg_plan_tree()
            self._load_rg_feasibility_tree()

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
        Callback function to handle events for the Testing class
        gtk.TreeView().  It is called whenever the Testing class gtk.TreeView()
        is clicked or a row is activated.

        :param __treeview: the Testing class gtk.TreeView().
        :type __treeview: gtk.TreeView
        :param __path: the selected row gtk.TreeView() path.
        :type __path: string
        :param __column: the selected gtk.TreeViewColumn().
        :type __column: gtk.TreeViewColumn
        :param __index:
        :type __index: integer
        """

        (_model, _row) = self.treeview.get_selection().get_selected()
        if _row is not None:
            self._update_attributes()
            self.load_notebook()

            return False
        else:
            return True

    def _rg_plan_edit(self, cell, path, new_text, position):
        """
        Callback function when editing a gtkCellRenderer() in the RG plan
        details gtk.TreeView()
        """

        _model = self.tvwRGPlanDetails.get_model()
        _row = _model.get_iter_from_string(path)

        _widg.edit_tree(cell, path, new_text, position, _model)

        if _row is not None:
            # Update the dictionary containing the RG Plan details.
            _phase_id = _model.get_value(_row, 0)
            self._dic_rg_plan[_phase_id][0] = _model.get_value(_row, 1)
            self._dic_rg_plan[_phase_id][1] = _model.get_value(_row, 2)
            self._dic_rg_plan[_phase_id][2] = _model.get_value(_row, 3)
            self._dic_rg_plan[_phase_id][3] = _model.get_value(_row, 4)
            self._dic_rg_plan[_phase_id][4] = _model.get_value(_row, 5)
            self._dic_rg_plan[_phase_id][5] = _model.get_value(_row, 6)
            self._dic_rg_plan[_phase_id][6] = _model.get_value(_row, 7)

            # Now update the RG plan feasibility gtk.TreeModel().
            _model = self.tvwTestFeasibility.get_model()
            _row = _model.get_iter_from_string(self._dic_rg_plan[_phase_id][8])
            _model.set_value(_row, 1, self._dic_rg_plan[_phase_id][0])
            _model.set_value(_row, 2, self._dic_rg_plan[_phase_id][1])
            _model.set_value(_row, 3, self._dic_rg_plan[_phase_id][2])

        return False

    def _rg_feasibility_edit(self, cell, path, new_text, position):
        """
        Callback function when editing a gtkCellRenderer() in the RG plan
        details gtk.TreeView()
        """

        _model = self.tvwTestFeasibility.get_model()
        _row = _model.get_iter_from_string(path)

        _widg.edit_tree(cell, path, new_text, position, _model)

        # Update the dictionary containing the RG Plan details.
        if _row is not None:
            _phase_id = _model.get_value(_row, 0)
            self._dic_rg_plan[_phase_id][0] = _model.get_value(_row, 1)
            self._dic_rg_plan[_phase_id][1] = _model.get_value(_row, 2)
            self._dic_rg_plan[_phase_id][2] = _model.get_value(_row, 3)

            # Now update the RG plan details gtk.TreeModel().
            _model = self.tvwRGPlanDetails.get_model()
            _row = _model.get_iter_from_string(self._dic_rg_plan[_phase_id][8])
            _model.set_value(_row, 1, self._dic_rg_plan[_phase_id][0])
            _model.set_value(_row, 2, self._dic_rg_plan[_phase_id][1])
            _model.set_value(_row, 3, self._dic_rg_plan[_phase_id][2])

        return False

    def _load_rg_plan_tree(self):
        """
        Method to load the Testing class reliability growth detailed plan
        gtk.TreeView().
        """

        _query = "SELECT fld_phase_id, fld_test_units, fld_start_date, \
                         fld_end_date, fld_test_time, fld_growth_rate, \
                         fld_num_fails, fld_ma, fld_mi, fld_mf \
                  FROM tbl_rel_growth \
                  WHERE fld_test_id=%d" % self.test_id
        _results = self._app.DB.execute_query(_query,
                                              None,
                                              self._app.ProgCnx)
        try:
            self.n_phases = len(_results)
        except TypeError:
            self.n_phases = 0

        _model = self.tvwRGPlanDetails.get_model()
        _model.clear()
        for i in range(self.n_phases):
            try:
                _dt_start = str(datetime.fromordinal(
                    int(_results[i][2])).strftime('%Y-%m-%d'))
            except TypeError:
                _dt_start = datetime.today().strftime('%Y-%m-%d')
            try:
                _dt_end = str(datetime.fromordinal(
                    int(_results[i][3])).strftime('%Y-%m-%d'))
            except TypeError:
                _dt_end = datetime.today().strftime('%Y-%m-%d')
            _data = [_results[i][0], _results[i][1], _dt_start, _dt_end,
                     _results[i][4], _results[i][5], _results[i][6],
                     _results[i][7], _results[i][8], _results[i][9]]
            _row = _model.append(_data)
            _path = _model.get_string_from_iter(_row)
            self._dic_rg_plan[_results[i][0]] = [_results[i][1], _dt_start,
                                                 _dt_end, _results[i][4],
                                                 _results[i][5],
                                                 _results[i][6],
                                                 _results[i][7], _path, '0']

        self.tvwRGPlanDetails.expand_all()
        self.tvwRGPlanDetails.set_cursor('0', None, False)
        if _model.get_iter_root() is not None:
            _path = _model.get_path(_model.get_iter_root())
            _col = self.tvwRGPlanDetails.get_column(0)
            self.tvwRGPlanDetails.row_activated(_path, _col)

        return False

    def _load_rg_feasibility_tree(self):
        """
        Method to load the Testing class reliability growth plan feasibility
        gtk.TreeView().
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
            self._dic_rg_plan[results[i][0]][8] = _path_

        self.tvwTestFeasibility.expand_all()
        self.tvwTestFeasibility.set_cursor('0', None, False)
        root = model.get_iter_root()
        if root is not None:
            path = model.get_path(root)
            col = self.tvwRGPlanDetails.get_column(0)
            self.tvwTestFeasibility.row_activated(path, col)

        return False
