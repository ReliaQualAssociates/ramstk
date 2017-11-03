#!/usr/bin/env python
"""
###############################
Software Package Work Book View
###############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.software.WorkBook.py is part of The RTK Project
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

# Import other RTK modules.
try:
    import Configuration
    import Utilities
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    import rtk.gui.gtk.Widgets as Widgets
import __gui.gtk.DevelopmentEnvironment as DevEnv
import __gui.gtk.SRR as SRR
import __gui.gtk.PDR as PDR
import __gui.gtk.CDR as CDR
import __gui.gtk.TRR as TRR
# from Assistants import AddSoftware

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class WorkView(gtk.VBox):                   # pylint: disable=R0902, R0904
    """
    The Work Book view displays all the attributes for the selected
    Software item.  The attributes of a Work Book view are:

    :ivar list _lst_obj_risk_analyses: list containing a pointer to each of the
                                       risk analysis page gtk.Widget().
    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable Software attribute.

    +----------+--------------------------------------------+
    | Position | Widget - Signal                            |
    +==========+============================================+
    |     0    | txtDescription - 'focus-out-event'         |
    +----------+--------------------------------------------+
    |     1    | cmbLevel - 'changed'                       |
    +----------+--------------------------------------------+
    |     2    | cmbApplication - 'changed'                 |
    +----------+--------------------------------------------+
    |     3    | cmbPhase - 'changed'                       |
    +----------+--------------------------------------------+
    |     4    | cmbTCL - 'changed'                         |
    +----------+--------------------------------------------+
    |     5    | cmbTestPath - 'changed'                    |
    +----------+--------------------------------------------+
    |     6    | cmbTestEffort - 'changed'                  |
    +----------+--------------------------------------------+
    |     7    | cmbTestApproach - 'changed'                |
    +----------+--------------------------------------------+
    |     8    | txtLaborTest - 'focus-out-event'           |
    +----------+--------------------------------------------+
    |     9    | txtLaborDev - 'focus-out-event'            |
    +----------+--------------------------------------------+
    |    10    | txtBudgetTest - 'focus-out-event'          |
    +----------+--------------------------------------------+
    |    11    | txtBudgetDev - 'focus-out-event'           |
    +----------+--------------------------------------------+
    |    12    | txtScheduleTest - 'focus-out-event'        |
    +----------+--------------------------------------------+
    |    13    | txtScheduleDev - 'focus-out-event'         |
    +----------+--------------------------------------------+
    |    14    | txtBranches - 'focus-out-event'            |
    +----------+--------------------------------------------+
    |    15    | txtBranchesTest - 'focus-out-event'        |
    +----------+--------------------------------------------+
    |    16    | txtInputs - 'focus-out-event'              |
    +----------+--------------------------------------------+
    |    17    | txtInputsTest - 'focus-out-event'          |
    +----------+--------------------------------------------+
    |    18    | txtUnits - 'focus-out-event'               |
    +----------+--------------------------------------------+
    |    19    | txtUnitsTest - 'focus-out-event'           |
    +----------+--------------------------------------------+
    |    20    | txtInterfaces - 'focus-out-event'          |
    +----------+--------------------------------------------+
    |    21    | txtInterfacesTest - 'focus-out-event'      |
    +----------+--------------------------------------------+

    :ivar _workview: the :py:class:`rtk.gui.gtk.mwi.WorkView` container
                     associated with this Work Book.
    :ivar _modulebook: the :py:class:`rtk.software.ModuleBook` to associate
                       with this Work Book.
    :ivar _software_model: the :py:class:`rtk.software.Software.Model` data
                           model to display.
    :ivar dtcBoM: the :py:class:`rtk.software.Software.Software` data
                  controller used to interface with the RTK Project database.
    :ivar gtk.Button btnEstimate: the gtk.Button() used to request the Software
                                  reliability estimation.
    :ivar gtk.Button btnSave: the gtk.Button() used to request the Software be
                              saved.
    :ivar gtk.Button btnTestCalculate: the gtk.Button() used to request the
                                       Software test plan risk reduction be
                                       calculated.
    :ivar gtk.Button btnTestSave: the gtk.Button() used to request the Software
                                  test plan be saved.
    :ivar gtk.ComboBox cmbApplication: the gtk.ComboBox() to select and display
                                       the Software module application type.
    :ivar gtk.ComboBox cmbLevel: the gtk.ComboBox() to select and display the
                                 Software module level.
                                 * 0 - System
                                 * 1 - CSCI
                                 * 2 - Unit
    :ivar gtk.ComboBox cmbPhase: the gtk.ComboBox() to select and display the
                                 Software module development phase.
    :ivar gtk.ComboBox cmbTCL: the gtk.ComboBox() to select and display the
                               test confidence level for the selected Software
                               module.
    :ivar gtk.ComboBox cmbTestPath: the gtk.ComboBox() to select and display
                                    the test path for the selected Software
                                    module.
    :ivar gtk.ComboBox cmbTestEffort: the gtk.ComboBox() to select and display
                                      the test effort type for the selected
                                      Software module.
    :ivar gtk.ComboBox cmbTestApproach: the gtk.ComboBox() to select and
                                        display the test approach for the
                                        selected Software module.
    :ivar gtk.Notebook nbkRiskAnalysis: the gtk.Notebook() to contain each of
                                        the development phase risk analysis
                                        questions for the selected Software
                                        module.
    :ivar gtk.Entry txtDescription: the gtk.Entry() to enter and display the
                                    description of the Software module.
    :ivar gtk.Entry txtLaborTest: the gtk.Entry() to enter and display the
                                  number of labor hours dedicated to testing
                                  the selected Software module.
    :ivar gtk.Entry txtLaborDev: the gtk.Entry() to enter and display the total
                                 number of labor hours dedicated to developing
                                 the selected Software module.
    :ivar gtk.Entry txtBudgetTest: the gtk.Entry() to enter and display the
                                   money budgeted for testing the selected
                                   Software module.
    :ivar gtk.Entry txtBudgetDev: the gtk.Entry() to enter and display the
                                  total money budgeted for developing the
                                  selected Software module.
    :ivar gtk.Entry txtScheduleTest: the gtk.Entry() to enter and display the
                                     calendar time dedicated to testing the
                                     selected Software module.
    :ivar gtk.Entry txtScheduleDev: the gtk.Entry() to enter and display the
                                    total calendar time dedicated to developing
                                    the selected Software module.
    :ivar gtk.Entry txtBranches: the gtk.Entry() to enter and display the total
                                 number of branches in the selected Software
                                 module.
    :ivar gtk.Entry txtBranchesTest: the gtk.Entry() to enter and display the
                                     number of branches that will be tested in
                                     the selected Software module.
    :ivar gtk.Entry txtInputs: the gtk.Entry() to enter and display the total
                               number of input variables in the selected
                               Software module.
    :ivar gtk.Entry txtInputsTest: the gtk.Entry() to enter and display the
                                   number of input variables that will be
                                   tested in the selected Software module.
    :ivar gtk.Entry txtUnits: the gtk.Entry() to enter and display the total
                              number of Software units comprising the selected
                              Software CSCI.
    :ivar gtk.Entry txtUnitsTest: the gtk.Entry() to enter and display the
                                  number of Software units that will be tested
                                  in the selected Software CSCI.
    :ivar gtk.Entry txtInterfaces: the gtk.Entry() to enter and display the
                                   total number of interfaces to other Software
                                   modules.
    :ivar gtk.Entry txtInterfacesTest: the gtk.Entry() to enter and display the
                                       number of interfaces to other Software
                                       modules that will be tested.
    :ivar gtk.Entry txtEC: the gtk.Entry() to enter and display the number of
                           exception conditions (EC) in the selected Software
                           module.
    :ivar gtk.Entry txtET: the gtk.Entry() to display the execution time (ET)
                           of the selected Software module.
    :ivar gtk.Entry txtOS: the gtk.Entry() to display the operating system (OS)
                           overhead time.
    :ivar gtk.Entry txtDRTest: the gtk.Entry() to enter and display the number
                               of discrepency reports (DR) generated to date
                               during the test.
    :ivar gtk.Entry txtTestTime: the gtk.Entry() to enter and display the total
                                 test time to date.
    :ivar gtk.Entry txtDREOT: the gtk.Entry() to display the number of
                              discrepency reports generated during the entire
                              test.
    :ivar gtk.Entry txtTestTimeEOT: the gtk.Entry() to enter and display the
                                    total test time at the end of test.
    :ivar gtk.Entry txtTE: the gtk.Entry() to display the test effort (TE)
                           factor.
    :ivar gtk.Entry txtTM: the gtk.Entry() to display the test methodology (TM)
                           factor.
    :ivar gtk.Entry txtTC: the gtk.Entry() to display the test coverage (TC)
                           factor.
    :ivar gtk.Entry txtFT1: the gtk.Entry() to display the average failure rate
                            during test.
    :ivar gtk.Entry txtFT2: the gtk.Entry() to display the failure rate at the
                            end of test.
    :ivar gtk.Entry txtRENAVG: the gtk.Entry() to display the average
                               reliability estimation number (REN) during test.
    :ivar gtk.Entry txtRENEOT: the gtk.Entry() to display the REN at the end of
                               testing.
    :ivar gtk.Entry txtEV: the gtk.Entry() to display the input variability
                           factor.
    :ivar gtk.Entry txtEW: the gtk.Entry() to display the workload factor.
    :ivar gtk.Entry txtE: the gtk.Entry() to display the operating environment
                          factor.
    :ivar gtk.Entry txtF: the gtk.Entry() to display the estimated failure rate
                          of the selected Software module.
    """

    def __init__(self, workview, modulebook):
        """
        Method to initialize the Work Book view for the Software package.

        :param workview: the :py:class:`rtk.gui.gtk.mwi.WorkView` container to
                         insert this Work Book into.
        :param modulebook: the :py:class:`rtk.software.ModuleBook` to associate
                           with this Work Book.
        """

        gtk.VBox.__init__(self)

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_handler_id = []
        self._lst_obj_risk_analyses = [None, None, None, None, None, None,
                                       None]

        # Define private scalar attributes.
        self._workview = workview
        self._modulebook = modulebook
        self._software_model = None

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.dtcBoM = modulebook.mdcRTK.dtcSoftwareBoM

        # General Data page widgets.
        self.cmbApplication = Widgets.make_combo(simple=False)
        self.cmbLevel = Widgets.make_combo(simple=False)
        self.cmbPhase = Widgets.make_combo(simple=False)
        self.txtDescription = Widgets.make_text_view(width=400)

        # Risk Analysis page widgets.
        self.btnSave = Widgets.make_button(width=35, image='save')

        self.nbkRiskAnalysis = gtk.Notebook()

        # Test Planning page widgets.
        self.btnTestCalculate = Widgets.make_button(width=35,
                                                    image='calculate')
        self.btnTestSave = Widgets.make_button(width=35, image='save')

        self.cmbTCL = Widgets.make_combo(simple=True)
        self.cmbTestPath = Widgets.make_combo(simple=True)
        self.cmbTestEffort = Widgets.make_combo(simple=True)
        self.cmbTestApproach = Widgets.make_combo(simple=True)

        self.txtLaborTest = Widgets.make_entry(width=75)
        self.txtLaborDev = Widgets.make_entry(width=75)
        self.txtBudgetTest = Widgets.make_entry(width=75)
        self.txtBudgetDev = Widgets.make_entry(width=75)
        self.txtScheduleTest = Widgets.make_entry(width=75)
        self.txtScheduleDev = Widgets.make_entry(width=75)
        self.txtBranches = Widgets.make_entry(width=75)
        self.txtBranchesTest = Widgets.make_entry(width=75)
        self.txtInputs = Widgets.make_entry(width=75)
        self.txtInputsTest = Widgets.make_entry(width=75)
        self.txtUnits = Widgets.make_entry(width=75)
        self.txtUnitsTest = Widgets.make_entry(width=75)
        self.txtInterfaces = Widgets.make_entry(width=75)
        self.txtInterfacesTest = Widgets.make_entry(width=75)

        # Reliability Estimation page widgets.
        self.btnEstimate = Widgets.make_button(width=35, image='calculate')

        self.txtEC = Widgets.make_entry(width=75)
        self.txtET = Widgets.make_entry(width=75)
        self.txtOS = Widgets.make_entry(width=75)
        self.txtDRTest = Widgets.make_entry(width=75)
        self.txtTestTime = Widgets.make_entry(width=75)
        self.txtDREOT = Widgets.make_entry(width=75)
        self.txtTestTimeEOT = Widgets.make_entry(width=75)
        self.txtTE = Widgets.make_entry(width=75, editable=False)
        self.txtTM = Widgets.make_entry(width=75, editable=False)
        self.txtTC = Widgets.make_entry(width=75, editable=False)
        self.txtFT1 = Widgets.make_entry(width=75, editable=False)
        self.txtFT2 = Widgets.make_entry(width=75, editable=False)
        self.txtRENAVG = Widgets.make_entry(width=75, editable=False)
        self.txtRENEOT = Widgets.make_entry(width=75, editable=False)
        self.txtEV = Widgets.make_entry(width=75, editable=False)
        self.txtEW = Widgets.make_entry(width=75, editable=False)
        self.txtE = Widgets.make_entry(width=75, editable=False)
        self.txtF = Widgets.make_entry(width=75, editable=False)

        # Set tooltips for gtk.Widgets().
        self.btnSave.set_tooltip_text(_(u"Saves the reliability risk "
                                        u"assessment."))
        self.btnTestCalculate.set_tooltip_text(_(u"Calculate the test plan "
                                                 u"risk reduction."))
        self.btnTestSave.set_tooltip_text(_(u"Saves the test plan risk "
                                            u"reduction assessment."))
        self.btnEstimate.set_tooltip_text(_(u"Estimate the software failure "
                                            u"rates."))
        self.cmbLevel.set_tooltip_text(_(u"Select the application level "
                                         u"of the selected software "
                                         u"module."))
        self.cmbApplication.set_tooltip_text(_(u"Select the application "
                                               u"type of the selected "
                                               u"software module."))
        self.cmbPhase.set_tooltip_text(_(u"Select the development phase "
                                         u"for the selected software "
                                         u"module."))
        self.cmbTCL.set_tooltip_text(_(u"Select the desired software test "
                                       u"confidence level."))
        self.cmbTestPath.set_tooltip_text(_(u"Select the path for determining "
                                            u"software testing techniques."))
        self.cmbTestEffort.set_tooltip_text(_(u"Select the software test "
                                              u"effort alternative."))
        self.cmbTestApproach.set_tooltip_text(_(u"Select the software test "
                                                u"approach."))
        self.txtLaborTest.set_tooltip_text(_(u"Total number of labor "
                                             u"hours for software "
                                             u"testing."))
        self.txtLaborDev.set_tooltip_text(_(u"Total number of labor hours "
                                            u"for entire software development "
                                            u"effort."))
        self.txtBudgetTest.set_tooltip_text(_(u"Total budget for software "
                                              u"testing."))
        self.txtBudgetDev.set_tooltip_text(_(u"Total budget for entire "
                                             u"for software development "
                                             u"effort."))
        self.txtScheduleTest.set_tooltip_text(_(u"Working days scheduled "
                                                u"for software testing."))
        self.txtScheduleDev.set_tooltip_text(_(u"Working days scheduled "
                                               u"for entire development "
                                               u"effort."))
        self.txtBranches.set_tooltip_text(_(u"The total number of "
                                            u"execution branches in the "
                                            u"selected unit."))
        self.txtBranchesTest.set_tooltip_text(_(u"The total number of "
                                                u"execution branches "
                                                u"actually tested in the "
                                                u"selected unit."))
        self.txtInputs.set_tooltip_text(_(u"The total number of inputs to "
                                          u"the selected unit."))
        self.txtInputsTest.set_tooltip_text(_(u"The total number of "
                                              u"inputs to the selected "
                                              u"unit actually tested."))
        self.txtUnits.set_tooltip_text(_(u"The total number of units in "
                                         u"the selected CSCI."))
        self.txtUnitsTest.set_tooltip_text(_(u"The total number of units "
                                             u"in the selected CSCI "
                                             u"actually tested."))
        self.txtInterfaces.set_tooltip_text(_(u"The total number of "
                                              u"interfaces to the "
                                              u"selected CSCI."))
        self.txtInterfacesTest.set_tooltip_text(_(u"The total number of "
                                                  u"interfaces in the "
                                                  u"selected CSCI "
                                                  u"actually tested."))
        self.txtDescription.set_tooltip_text(_(u"Enter a description of "
                                               u"the selected software "
                                               u"module."))
        self.txtEC.set_tooltip_text(_(u"Displays the number of exception "
                                      u"conditions for the selected "
                                      u"software module."))
        self.txtET.set_tooltip_text(_(u"Displays the total execution time "
                                      u"for the selected software "
                                      u"module."))
        self.txtOS.set_tooltip_text(_(u"Displays the operating system "
                                      u"overhead time for the selected "
                                      u"software module."))
        self.txtDRTest.set_tooltip_text(_(u"Displays the total number of "
                                          u"discrepancy reports recorded "
                                          u"during testing for the selected "
                                          u"software module."))
        self.txtTestTime.set_tooltip_text(_(u"Displays the total test time "
                                            u"for the selected software "
                                            u"module."))
        self.txtDREOT.set_tooltip_text(_(u"Displays the total number of "
                                         u"discrepancy reports recorded "
                                         u"during the last three test periods "
                                         u"for the selected software module."))
        self.txtTestTimeEOT.set_tooltip_text(_(u"Displays the total test time "
                                               u"during the last three test "
                                               u"periods for the selected "
                                               u"software module."))
        self.txtTE.set_tooltip_text(_(u"Displays the reduction in risk due to "
                                      u"the percent of the development "
                                      u"program assigned to testing for the "
                                      u"selected software module."))
        self.txtTM.set_tooltip_text(_(u"Displays the reduction in risk due to "
                                      u"the number of recommended tests that "
                                      u"are actually performed for the "
                                      u"selected software module."))
        self.txtTC.set_tooltip_text(_(u"Displays the reduction in risk due to "
                                      u"percent test coverage of the tests "
                                      u"performed for the selected software "
                                      u"module."))
        self.txtFT1.set_tooltip_text(_(u"Displays the average failure "
                                       u"rate during test for the "
                                       u"selected software module."))
        self.txtFT2.set_tooltip_text(_(u"Displays the failure rate at the "
                                       u"end of test for the selected "
                                       u"software module."))
        self.txtRENAVG.set_tooltip_text(_(u"Displays the average "
                                          u"Reliability Estimation Number "
                                          u"(REN) for the selected "
                                          u"software module."))
        self.txtRENEOT.set_tooltip_text(_(u"Displays the end of test "
                                          u"Reliability Estimation Number "
                                          u"(REN) for the selected "
                                          u"software module."))
        self.txtEV.set_tooltip_text(_(u"Displays the variability of input "
                                      u"for the selected software "
                                      u"module."))
        self.txtEW.set_tooltip_text(_(u"Displays the workload for the "
                                      u"selected software module."))
        self.txtE.set_tooltip_text(_(u"Displays the operating environment "
                                     u"factor for the selected software "
                                     u"module."))
        self.txtF.set_tooltip_text(_(u"Displays the estimated failure "
                                     u"rate for the selected software "
                                     u"module."))

        # Connect gtk.Widget() signals to callback methods.
        _textview = self.txtDescription.get_child().get_child()
        self._lst_handler_id.append(
            _textview.connect('focus-out-event', self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.cmbLevel.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbPhase.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbTCL.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.cmbTestPath.connect('changed', self._on_combo_changed, 5))
        self._lst_handler_id.append(
            self.cmbTestEffort.connect('changed', self._on_combo_changed, 6))
        self._lst_handler_id.append(
            self.cmbTestApproach.connect('changed', self._on_combo_changed, 7))
        self._lst_handler_id.append(
            self.txtLaborTest.connect('focus-out-event',
                                      self._on_focus_out, 8))
        self._lst_handler_id.append(
            self.txtLaborDev.connect('focus-out-event', self._on_focus_out, 9))
        self._lst_handler_id.append(
            self.txtBudgetTest.connect('focus-out-event',
                                       self._on_focus_out, 10))
        self._lst_handler_id.append(
            self.txtBudgetDev.connect('focus-out-event',
                                      self._on_focus_out, 11))
        self._lst_handler_id.append(
            self.txtScheduleTest.connect('focus-out-event',
                                         self._on_focus_out, 12))
        self._lst_handler_id.append(
            self.txtScheduleDev.connect('focus-out-event',
                                        self._on_focus_out, 13))
        self._lst_handler_id.append(
            self.txtBranches.connect('focus-out-event',
                                     self._on_focus_out, 14))
        self._lst_handler_id.append(
            self.txtBranchesTest.connect('focus-out-event',
                                         self._on_focus_out, 15))
        self._lst_handler_id.append(
            self.txtInputs.connect('focus-out-event', self._on_focus_out, 16))
        self._lst_handler_id.append(
            self.txtInputsTest.connect('focus-out-event',
                                       self._on_focus_out, 17))
        self._lst_handler_id.append(
            self.txtUnits.connect('focus-out-event', self._on_focus_out, 18))
        self._lst_handler_id.append(
            self.txtUnitsTest.connect('focus-out-event',
                                      self._on_focus_out, 19))
        self._lst_handler_id.append(
            self.txtInterfaces.connect('focus-out-event',
                                       self._on_focus_out, 20))
        self._lst_handler_id.append(
            self.txtInterfacesTest.connect('focus-out-event',
                                           self._on_focus_out, 21))

        self.btnSave.connect('clicked', self._on_button_clicked, 51)
        self.btnTestCalculate.connect('clicked', self._on_button_clicked, 52)
        self.btnTestSave.connect('clicked', self._on_button_clicked, 53)
        self.btnEstimate.connect('clicked', self._on_button_clicked, 54)

        # Put it all together.
        _toolbar = self._create_toolbar()
        self.pack_start(_toolbar, expand=False)

        _notebook = self._create_notebook()
        self.pack_start(_notebook)

        self.show_all()

    def _create_toolbar(self):
        """
        Method to create the toolbar for the Software class Work Book.

        :return: _toolbar
        :rtype: gtk.Toolbar
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        # Add sibling module button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Adds a new software module at the same "
                                   u"indenture level as the selected software "
                                   u"module."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR +
                             '32x32/insert_sibling.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 0)
        _toolbar.insert(_button, 0)
        _position += 1

        # Add child module button.
        _button = gtk.MenuToolButton(None, label="")
        _button.set_tooltip_text(_(u"Adds a new software CSCI or unit to "
                                   u"the RTK Project that is one level "
                                   u"subordinate to the selected assembly."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/insert_child.png')
        _button.set_icon_widget(_image)
        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"CSCI"))
        _menu_item.set_tooltip_text(_(u"Adds one or more subordinate "
                                      u"CSCI to the currently selected "
                                      u"software item."))
        _menu_item.connect('activate', self._on_button_clicked, 1)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Unit"))
        _menu_item.set_tooltip_text(_(u"Adds one or more units to the "
                                      u"currently selected software item."))
        _menu_item.connect('activate', self._on_button_clicked, 2)
        _menu.add(_menu_item)
        _button.set_menu(_menu)
        _menu.show_all()
        _button.show()
        _toolbar.insert(_button, _position)
        _position += 1

        # Delete module button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Removes the currently selected software "
                                   u"item from the RTK Program Database."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/remove.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 3)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save results button.  Depending on the notebook page selected will
        # determine which results are saved.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 4)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)

        _toolbar.show()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Software class gtk.Notebook().

        :return: _notebook
        :rtype: gtk.Notebook
        """

        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook() tab position.
        if Configuration.TABPOS[2] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif Configuration.TABPOS[2] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif Configuration.TABPOS[2] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        self._create_general_data_page(_notebook)
        self._create_risk_analysis_page(_notebook)
        self._create_test_planning_page(_notebook)
        self._create_assessment_results_page(_notebook)

        return _notebook

    def _create_general_data_page(self, notebook):
        """
        Method to create the Software class gtk.Notebook() page for
        displaying general data about the selected Software.

        :param gtk.Notebook notebook: the Software class gtk.Notebook() widget.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                 gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = Widgets.make_frame(label=_(u"General Information"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.ComboBox() widgets.
        _model = self.cmbLevel.get_model()
        _model.clear()
        _model.append(None, ['', 0, ''])
        for _level in Configuration.RTK_SW_LEVELS:
            _model.append(None, [_level, 0, ''])

        _model = self.cmbApplication.get_model()
        _model.clear()
        _model.append(None, ['', 0, ''])
        for _app in Configuration.RTK_SW_APPLICATION:
            _model.append(None, [_app, 0, ''])

        _model = self.cmbPhase.get_model()
        _model.clear()
        _model.append(None, ['', 0, ''])
        for _phase in Configuration.RTK_SW_DEV_PHASES:
            _model.append(None, [_phase, 0, ''])

        # Create the labels.
        _labels = [_(u"Module Description:"), _(u"Application Level:"),
                   _(u"Application Type:"), _(u"Development Phase:")]

        (_x_pos, _y_pos) = Widgets.make_labels(_labels[1:], _fixed, 5, 110)
        _x_pos += 25

        _label = Widgets.make_label(_labels[0])
        _fixed.put(_label, 5, 5)
        _fixed.put(self.txtDescription, _x_pos, 5)
        _fixed.put(self.cmbLevel, _x_pos, _y_pos[0])
        _fixed.put(self.cmbApplication, _x_pos, _y_pos[1])
        _fixed.put(self.cmbPhase, _x_pos, _y_pos[2])

        _fixed.show_all()

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"General\nData") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays general information about "
                                  u"the selected software module."))
        notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _create_risk_analysis_page(self, notebook):
        """
        Method to create the Software class gtk.Notebook() page for displaying
        the risk analysis for the selected Software.

        :param gtk.Notebook notebook: the Software class gtk.Notebook() widget.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        _hbox = gtk.HBox()
        _hbox.pack_start(_bbox, False, True)
        _hbox.pack_end(self.nbkRiskAnalysis, True, True)

        _bbox.pack_start(self.btnSave, False, False)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display risk analysis information.  #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Add the gtk.Notebook() that guides the risk analysis.
        self._lst_obj_risk_analyses[0] = DevEnv.RiskAnalysis()
        self._lst_obj_risk_analyses[0].create_risk_analysis_page(self.nbkRiskAnalysis)
        self._lst_obj_risk_analyses[1] = SRR.RiskAnalysis()
        self._lst_obj_risk_analyses[1].create_risk_analysis_page(self.nbkRiskAnalysis)
        self._lst_obj_risk_analyses[2] = PDR.RiskAnalysis()
        self._lst_obj_risk_analyses[2].create_risk_analysis_page(self.nbkRiskAnalysis)
        self._lst_obj_risk_analyses[3] = CDR.CSCIRiskAnalysis()
        self._lst_obj_risk_analyses[3].create_risk_analysis_page(self.nbkRiskAnalysis)
        self._lst_obj_risk_analyses[4] = CDR.UnitRiskAnalysis()
        self._lst_obj_risk_analyses[4].create_risk_analysis_page(self.nbkRiskAnalysis)
        self._lst_obj_risk_analyses[5] = TRR.CSCIRiskAnalysis()
        self._lst_obj_risk_analyses[5].create_risk_analysis_page(self.nbkRiskAnalysis)
        self._lst_obj_risk_analyses[6] = TRR.UnitRiskAnalysis()
        self._lst_obj_risk_analyses[6].create_risk_analysis_page(self.nbkRiskAnalysis)

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Risk\nAnalysis") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Allows assessment of the reliability "
                                  u"risk."))
        notebook.insert_page(_hbox,
                             tab_label=_label,
                             position=-1)

        return False

    def _create_test_planning_page(self, notebook):
        """
        Method to create the Software class gtk.Notebook() page for displaying
        the risk analysis for the selected Software.

        :param gtk.Notebook notebook: the Software class gtk.Notebook() widget.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        _hbox = gtk.HBox()
        _hbox.pack_start(_bbox, False, True)

        _hpaned = gtk.HPaned()

        _hbox.pack_end(_hpaned, True, True)

        _bbox.pack_start(self.btnTestCalculate, False, False)
        _bbox.pack_start(self.btnTestSave, False, False)

        _vpaned = gtk.VPaned()

        # Add the test planning widgets to the upper left half.
        _fxdtopleft = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdtopleft)

        _frame = Widgets.make_frame(label=_(u"Test Planning"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)
        _frame.show_all()

        _vpaned.pack1(_frame, resize=True, shrink=True)

        # Add the test effort widgets to the lower left half.
        _fxdbottomleft = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdbottomleft)

        _frame = Widgets.make_frame(label=_(u"Test Effort &amp; Coverage"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack2(_frame, resize=True, shrink=True)

        _hpaned.pack1(_vpaned, resize=True, shrink=True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display risk analysis information.  #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.Combo()
        _list = [["Low"], ["Medium"], ["High"], ["Very High"]]
        Widgets.load_combo(self.cmbTCL, _list, True)

        _list = [[_(u"Choose techniques based on software category")],
                 [_(u"Choose techniques based on types of software errors")]]
        Widgets.load_combo(self.cmbTestPath, _list, True)

        _list = [[_(u"Alternative 1, Labor Hours")],
                 [_(u"Alternative 2, Budget")],
                 [_(u"Alternative 3, Schedule")]]
        Widgets.load_combo(self.cmbTestEffort, _list, True)

        _list = [[_(u"Test Until Method is Exhausted")],
                 [_(u"Stopping Rules")]]
        Widgets.load_combo(self.cmbTestApproach, _list, True)

        # Place the labels in the upper left pane.
        _labels = [_(u"Test Confidence Level:"), _(u"Test Path:"),
                   _(u"Test Effort:"), _(u"Test Approach:")]
        _max1 = 0
        (_max1, _y_pos1) = Widgets.make_labels(_labels, _fxdtopleft,
                                               5, 5, y_inc=30)

        # Place the labels in the lower left pane.  There are two columns
        # of information in the lower left pane.  First we place the left
        # hand column of labels and then the right hand column.  This gives
        # us two _x_pos values for placing the display widgets.
        _labels = [_(u"Labor Hours for Testing:"),
                   _(u"Labor Hours for Development:"),
                   _(u"Budget for Testing:"),
                   _(u"Budget for Development:"),
                   _(u"Working Days for Testing:"),
                   _(u"Working Days for Development:")]
        (_x_pos_left, _y_pos2) = Widgets.make_labels(_labels, _fxdbottomleft,
                                                     5, 5, y_inc=25)
        _x_pos_left = max(_max1, _x_pos_left)
        _x_pos_left += 45

        _labels = [_(u"Number of Branches:"),
                   _(u"Number of Branches Tested:"), _(u"Number of Inputs:"),
                   _(u"Number of Inputs Tested:"), _(u"Number of Units:"),
                   _(u"Number of Units Tested:"), _(u"Number of Interfaces:"),
                   _(u"Number of Interfaces Tested:")]
#                   _(u"Number of Requirements:"),
#                   _(u"Number of Requirements Tested:")]
        (_x_pos_right,
         _y_pos) = Widgets.make_labels(_labels, _fxdbottomleft,
                                       _x_pos_left + 105, 5)
        _x_pos_right += _x_pos_left + 150

        # Place the widgets in the upper left pane.
        _fxdtopleft.put(self.cmbTCL, _x_pos_left, _y_pos1[0])
        _fxdtopleft.put(self.cmbTestPath, _x_pos_left, _y_pos1[1])
        _fxdtopleft.put(self.cmbTestEffort, _x_pos_left, _y_pos1[2])
        _fxdtopleft.put(self.cmbTestApproach, _x_pos_left, _y_pos1[3])

        _fxdtopleft.show_all()

        # Place the widgets in the lower left pane.
        _fxdbottomleft.put(self.txtLaborTest, _x_pos_left, _y_pos2[0])
        _fxdbottomleft.put(self.txtLaborDev, _x_pos_left, _y_pos2[1])
        _fxdbottomleft.put(self.txtBudgetTest, _x_pos_left, _y_pos2[2])
        _fxdbottomleft.put(self.txtBudgetDev, _x_pos_left, _y_pos2[3])
        _fxdbottomleft.put(self.txtScheduleTest, _x_pos_left, _y_pos2[4])
        _fxdbottomleft.put(self.txtScheduleDev, _x_pos_left, _y_pos2[5])

        _fxdbottomleft.put(self.txtBranches, _x_pos_right, _y_pos[0])
        _fxdbottomleft.put(self.txtBranchesTest, _x_pos_right, _y_pos[1])
        _fxdbottomleft.put(self.txtInputs, _x_pos_right, _y_pos[2])
        _fxdbottomleft.put(self.txtInputsTest, _x_pos_right, _y_pos[3])
        _fxdbottomleft.put(self.txtUnits, _x_pos_right, _y_pos[4])
        _fxdbottomleft.put(self.txtUnitsTest, _x_pos_right, _y_pos[5])
        _fxdbottomleft.put(self.txtInterfaces, _x_pos_right, _y_pos[6])
        _fxdbottomleft.put(self.txtInterfacesTest, _x_pos_right, _y_pos[7])

        _fxdbottomleft.show_all()

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Test\nPlanning") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Assists in planning of the software test "
                                  u"program."))
        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_assessment_results_page(self, notebook):
        """
        Method to create the Software class gtk.Notebook() page for
        displaying reliability estimates for the selected Software.

        :param gtk.Notebook notebook: the Software class gtk.Notebook() widget.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        _hbox = gtk.HBox()
        _hbox.pack_start(_bbox, False, True)

        _hpaned = gtk.HPaned()

        _hbox.pack_end(_hpaned, True, True)

        _bbox.pack_start(self.btnEstimate, False, False)

        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = Widgets.make_frame(label=_(u"Reliability Estimation Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hpaned.pack1(_frame, resize=True, shrink=True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _labels = [_(u"Number of Exception Conditions:"),
                   _(u"Total Execution Time:"), _(u"OS Overhead Time:"),
                   _(u"Number of Discrepancy Reports During Test"),
                   _(u"Total Test Time"),
                   _(u"Number of Discrepancy Reports During Last Three Test Periods:"),
                   _(u"Total Test Time During Last Three Test Periods:"),
                   _(u"Risk Reduction Due to Test Effort:"),
                   _(u"Risk Reduction Due to Test Methods:"),
                   _(u"Risk Reduction Due to Test Coverage:"),
                   _(u"Average FR During Test:"), _(u"Failure Rate at EOT:"),
                   _(u"Average REN:"), _(u"EOT REN:"),
                   _(u"Input Variability:"), _(u"Workload:"),
                   _(u"Operating Environment Factor:"),
                   _(u"Estimated Failure Rate:")]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5)
        _x_pos += 45

        _fixed.put(self.txtEC, _x_pos, _y_pos[0])
        _fixed.put(self.txtET, _x_pos, _y_pos[1])
        _fixed.put(self.txtOS, _x_pos, _y_pos[2])
        _fixed.put(self.txtDRTest, _x_pos, _y_pos[3])
        _fixed.put(self.txtTestTime, _x_pos, _y_pos[4])
        _fixed.put(self.txtDREOT, _x_pos, _y_pos[5])
        _fixed.put(self.txtTestTimeEOT, _x_pos, _y_pos[6])
        _fixed.put(self.txtTE, _x_pos, _y_pos[7])
        _fixed.put(self.txtTM, _x_pos, _y_pos[8])
        _fixed.put(self.txtTC, _x_pos, _y_pos[9])
        _fixed.put(self.txtFT1, _x_pos, _y_pos[10])
        _fixed.put(self.txtFT2, _x_pos, _y_pos[11])
        _fixed.put(self.txtRENAVG, _x_pos, _y_pos[12])
        _fixed.put(self.txtRENEOT, _x_pos, _y_pos[13])
        _fixed.put(self.txtEV, _x_pos, _y_pos[14])
        _fixed.put(self.txtEW, _x_pos, _y_pos[15])
        _fixed.put(self.txtE, _x_pos, _y_pos[16])
        _fixed.put(self.txtF, _x_pos, _y_pos[17])

        self._lst_handler_id.append(
            self.txtEC.connect('focus-out-event', self._on_focus_out, 22))
        self._lst_handler_id.append(
            self.txtET.connect('focus-out-event', self._on_focus_out, 23))
        self._lst_handler_id.append(
            self.txtOS.connect('focus-out-event', self._on_focus_out, 24))
        self._lst_handler_id.append(
            self.txtDRTest.connect('focus-out-event', self._on_focus_out, 25))
        self._lst_handler_id.append(
            self.txtTestTime.connect('focus-out-event',
                                     self._on_focus_out, 26))
        self._lst_handler_id.append(
            self.txtDREOT.connect('focus-out-event', self._on_focus_out, 27))
        self._lst_handler_id.append(
            self.txtTestTimeEOT.connect('focus-out-event',
                                        self._on_focus_out, 28))

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Reliability\nEstimation") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays software reliability estimation "
                                  u"results."))
        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Software class gtk.Notebook().

        :param model: the :py:class:`rtk.software.Software.Model` to load.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        self._software_model = model

        # --------------------------------------------------------------#
        # Load the General Data information.                            #
        # --------------------------------------------------------------#
        self.cmbApplication.set_active(model.application_id)
        self.cmbLevel.set_active(model.level_id)
        self.cmbPhase.set_active(model.phase_id)
        _textview = self.txtDescription.get_children()[0].get_children()[0].get_buffer()
        _textview.set_text(model.description)

        # --------------------------------------------------------------#
        # Load the Risk Analysis information.                           #
        # --------------------------------------------------------------#
        self._load_risk_analysis_page()

        # --------------------------------------------------------------#
        # Load the Test Selection Matrix.                               #
        # --------------------------------------------------------------#
        if model.level_id == 2:             # CSCI
            self.txtBranches.props.editable = False
            self.txtBranches.set_sensitive(False)
            self.txtBranchesTest.props.editable = False
            self.txtBranchesTest.set_sensitive(False)
            self.txtInputs.props.editable = False
            self.txtInputs.set_sensitive(False)
            self.txtInputsTest.props.editable = False
            self.txtInputsTest.set_sensitive(False)
            self.txtUnits.props.editable = True
            self.txtUnits.set_sensitive(True)
            self.txtUnitsTest.props.editable = True
            self.txtUnitsTest.set_sensitive(True)
            self.txtInterfaces.props.editable = True
            self.txtInterfaces.set_sensitive(True)
            self.txtInterfacesTest.props.editable = True
            self.txtInterfacesTest.set_sensitive(True)
        elif model.level_id == 3:           # Unit
            self.txtBranches.props.editable = True
            self.txtBranches.set_sensitive(True)
            self.txtBranchesTest.props.editable = True
            self.txtBranchesTest.set_sensitive(True)
            self.txtInputs.props.editable = True
            self.txtInputs.set_sensitive(True)
            self.txtInputsTest.props.editable = True
            self.txtInputsTest.set_sensitive(True)
            self.txtUnits.props.editable = False
            self.txtUnits.set_sensitive(False)
            self.txtUnitsTest.props.editable = False
            self.txtUnitsTest.set_sensitive(False)
            self.txtInterfaces.props.editable = False
            self.txtInterfaces.set_sensitive(False)
            self.txtInterfacesTest.props.editable = False
            self.txtInterfacesTest.set_sensitive(False)
        else:                               # System or unassigned
            self.txtBranches.props.editable = False
            self.txtBranches.set_sensitive(False)
            self.txtBranchesTest.props.editable = False
            self.txtBranchesTest.set_sensitive(False)
            self.txtInputs.props.editable = False
            self.txtInputs.set_sensitive(False)
            self.txtInputsTest.props.editable = False
            self.txtInputsTest.set_sensitive(False)
            self.txtUnits.props.editable = False
            self.txtUnits.set_sensitive(False)
            self.txtUnitsTest.props.editable = False
            self.txtUnitsTest.set_sensitive(False)
            self.txtInterfaces.props.editable = False
            self.txtInterfaces.set_sensitive(False)
            self.txtInterfacesTest.props.editable = False
            self.txtInterfacesTest.set_sensitive(False)

        self.cmbTCL.set_active(int(model.tcl))
        self.cmbTestPath.set_active(int(model.test_path))
        self.cmbTestEffort.set_active(int(model.test_effort))
        self.cmbTestApproach.set_active(int(model.test_approach))
        self.txtLaborTest.set_text(str(model.labor_hours_test))
        self.txtLaborDev.set_text(str(model.labor_hours_dev))
        self.txtBudgetTest.set_text(str(model.budget_test))
        self.txtBudgetDev.set_text(str(model.budget_dev))
        self.txtScheduleTest.set_text(str(model.schedule_test))
        self.txtScheduleDev.set_text(str(model.schedule_dev))
        self.txtBranches.set_text(str(model.branches))
        self.txtBranchesTest.set_text(str(model.branches_test))
        self.txtInputs.set_text(str(model.inputs))
        self.txtInputsTest.set_text(str(model.inputs_test))
        self.txtUnits.set_text(str(model.nm))
        self.txtUnitsTest.set_text(str(model.nm_test))
        self.txtInterfaces.set_text(str(model.interfaces))
        self.txtInterfacesTest.set_text(str(model.interfaces_test))

        # --------------------------------------------------------------#
        # Load the Assessment Results Page.                             #
        # --------------------------------------------------------------#
        self._load_assessment_results_page()

        self.get_children()[1].set_current_page(0)

        return False

    def _load_risk_analysis_page(self):
        """
        Method to load the Software class gtk.Notebook() risk analysis page.
        Show the pages according to the following:

        +------------------------------+--------+----+-----+-----+-----+-----+
        |             Phase            | Level  | DE | SRR | PDR | CDR | TRR |
        +------------------------------+--------+----+-----+-----+-----+-----+
        | Any                          | System | X  |     |     |     |     |
        +------------------------------+--------+----+-----+-----+-----+-----+
        | Concept/Planning             | Module | X  |     |     |     |     |
        +------------------------------+--------+----+-----+-----+-----+-----+
        | Software Requirements Review | Module | X  |  X  |     |     |     |
        +------------------------------+--------+----+-----+-----+-----+-----+
        | Preliminary Design Review    | Module | X  |  X  |  X  |     |     |
        +------------------------------+--------+----+-----+-----+-----+-----+
        | Critical Design Review       | Module | X  |  X  |  X  |  X  |     |
        +------------------------------+--------+----+-----+-----+-----+-----+
        | Test Readiness Review        | Module | X  |  X  |  X  |  X  |  X  |
        +------------------------------+--------+----+-----+-----+-----+-----+
        | Concept/Planning             | Unit   | X  |     |     |     |     |
        +------------------------------+--------+----+-----+-----+-----+-----+
        | Software Requirements Review | Unit   | X  |     |     |     |     |
        +------------------------------+--------+----+-----+-----+-----+-----+
        | Preliminary Design Review    | Unit   | X  |     |     |     |     |
        +------------------------------+--------+----+-----+-----+-----+-----+
        | Critical Design Review       | Unit   | X  |     |     |  X  |     |
        +------------------------------+--------+----+-----+-----+-----+-----+
        | Test Readiness Review        | Unit   | X  |     |     |  X  |  X  |
        +------------------------------+--------+----+-----+-----+-----+-----+

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """
# WARNING: Refactor _load_risk_analysis_page; current McCabe Complexity metric = 21.
        if self._software_model.level_id == 1:             # System
            _lst_show = [0]
            _lst_hide = [1, 2, 3, 4, 5, 6]

        if self._software_model.phase_id == 1:             # Concept/planning
            _lst_show = [0]
            _lst_hide = [1, 2, 3, 4, 5, 6]
        elif self._software_model.phase_id == 2:           # SRR
            if self._software_model.level_id == 2:         # CSCI
                _lst_show = [0, 1]
                _lst_hide = [2, 3, 4, 5, 6]
            elif self._software_model.level_id == 3:       # Unit
                _lst_show = [0]
                _lst_hide = [1, 2, 3, 4, 5, 6]
        elif self._software_model.phase_id == 3:           # PDR
            if self._software_model.level_id == 2:         # CSCI
                _lst_show = [0, 1, 2]
                _lst_hide = [3, 4, 5, 6]
            elif self._software_model.level_id == 3:       # Unit
                _lst_show = [0]
                _lst_hide = [1, 2, 3, 4, 5, 6]
        elif self._software_model.phase_id == 4:           # CDR
            if self._software_model.level_id == 2:         # CSCI
                _lst_show = [0, 1, 2, 3]
                _lst_hide = [4, 5, 6]
            elif self._software_model.level_id == 3:       # Unit
                _lst_show = [0, 4]
                _lst_hide = [1, 2, 3, 5, 6]
        elif self._software_model.phase_id == 5:           # TRR

            if self._software_model.level_id == 2:         # CSCI
                _lst_show = [0, 1, 2, 3, 5]
                _lst_hide = [4, 6]
            elif self._software_model.level_id == 3:       # Unit
                _lst_show = [0, 4, 6]
                _lst_hide = [1, 2, 3, 5]
        else:
            _lst_show = [0]
            _lst_hide = [1, 2, 3, 4, 5, 6]

        for i in _lst_show:
            self.nbkRiskAnalysis.get_nth_page(i).show()
        for i in _lst_hide:
            self.nbkRiskAnalysis.get_nth_page(i).hide()

        for i in range(3):
            self._lst_obj_risk_analyses[i].load(self._software_model)
        if self._software_model.level_id == 2:
            self._lst_obj_risk_analyses[3].load(self._software_model)
            self._lst_obj_risk_analyses[5].load(self._software_model)
        elif self._software_model.level_id == 3:
            self._lst_obj_risk_analyses[4].load(self._software_model)
            self._lst_obj_risk_analyses[6].load(self._software_model)

        return False

    def _load_assessment_results_page(self):
        """
        Method to load the Software class gtk.Notebook() risk assessment page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'

        self.txtEC.set_text(str(fmt.format(self._software_model.ec)))
        self.txtET.set_text(str(fmt.format(self._software_model.et)))
        self.txtOS.set_text(str(fmt.format(self._software_model.os)))
        self.txtDRTest.set_text(str(fmt.format(self._software_model.dr_test)))
        self.txtTestTime.set_text(
            str(fmt.format(self._software_model.test_time)))
        self.txtDREOT.set_text(str(fmt.format(self._software_model.dr_eot)))
        self.txtTestTimeEOT.set_text(
            str(fmt.format(self._software_model.test_time_eot)))

        self.txtFT1.set_text(str(fmt.format(self._software_model.ft1)))
        self.txtFT2.set_text(str(fmt.format(self._software_model.ft2)))
        self.txtTE.set_text(str(fmt.format(self._software_model.te)))
        self.txtTM.set_text(str(fmt.format(self._software_model.tm)))
        self.txtTC.set_text(str(fmt.format(self._software_model.tc)))
        self.txtRENAVG.set_text(str(fmt.format(self._software_model.ren_avg)))
        self.txtRENEOT.set_text(str(fmt.format(self._software_model.ren_eot)))
        self.txtEV.set_text(str(fmt.format(self._software_model.ev)))
        self.txtEW.set_text(str(fmt.format(self._software_model.ew)))
        self.txtE.set_text(str(fmt.format(self._software_model.e_risk)))
        self.txtF.set_text(str(fmt.format(self._software_model.failure_rate)))

        return False

    def _request_add_software(self, software_type, model, parent, software_id):
        """
        Method to call the BoM data controller function 'add_software' and
        then update the Software Work Book gtk.TreeView() with the newly added
        software item.

        :param int software_type: the type of Software item to add.
                                  * 1 = CSCI
                                  * 2 = Unit
        :param gtk.TreeModel model: the gtk.TreeModel() displaying the Software
                                    hierarchy.
        :param gtk.TreeIter parent: the gtk.TreeIter() that will be the parent
                                    of the newly added software item.
        :param int software_id: the software ID of the parent Software module.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Add the new software item to the database and dtcBoM dictionary.
        (_software, _error_code) = self.dtcBoM.add_software(
            self._software_model.revision_id, software_type, software_id)

        if software_type == 1:
            _icon = Configuration.ICON_DIR + '32x32/csci.png'
        elif software_type == 2:
            _icon = Configuration.ICON_DIR + '32x32/unit.png'

        # Update the module book view to show the new assembly.
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _data = list(_software.get_attributes()) + [_icon]

        model.append(parent, _data)
        self._modulebook.treeview.expand_all()

        return False

    def _request_delete_software(self):
        """
        Method to call the BoM data controller function 'delete_software' and
        then update the Software Work Book gtk.TreeView() with the newly added
        software item.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Find the selected software item.
        _selection = self._modulebook.treeview.get_selection()
        (_model, _row) = _selection.get_selected()

        # Delete the selected software item from the database and the
        # Software data controller dictionary.
        self.dtcBoM.delete_software(self._software_model.software_id)

        # Refresh the Software gtkTreeView().
        if _row is not None:
            _path = _model.get_path(_row)
            _model.remove(_row)
            _selection.select_path(_path)

        return False

    def _on_button_clicked(self, __button, index):
        """
        Responds to gtk.Button() clicked signals and calls the correct function
        or method, passing any parameters as needed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# WARNING: Refactor _on_button_clicked; current McCabe Complexity metric = 17.
        _return = False

        if index == 0:
            # Find the selected software item indenture level.
            (_model,
             _row) = self._modulebook.treeview.get_selection().get_selected()
            _level_id = _model.get_value(_row,
                                         self._modulebook._lst_col_order[2])

            # Find the parent software item.
            _row = _model.iter_parent(_row)
            _software_id = _model.get_value(_row, 1)
            if _level_id == 1:
                Widgets.rtk_information(_(u"Can not add a sibling to the "
                                            u"System Software."))

            elif _level_id == 2:
                self._request_add_software(1, _model, _row, _software_id)
            elif _level_id == 3:
                self._request_add_software(2, _model, _row, _software_id)

        elif index == 1:
            # Find the parent software item.
            (_model,
             _row) = self._modulebook.treeview.get_selection().get_selected()

            self._request_add_software(1, _model, _row,
                                       self._software_model.software_id)

        elif index == 2:
            # Find the parent software item.
            (_model,
             _row) = self._modulebook.treeview.get_selection().get_selected()

            self._request_add_software(2, _model, _row,
                                       self._software_model.software_id)

        elif index == 3:
            self._request_delete_software()

        elif index == 4:
            self.dtcBoM.save_software_item(self._software_model.software_id)

        elif index == 51:
            self.dtcBoM.save_development_risk(self._software_model.software_id)

            if self._software_model.phase_id in [2, 3, 4, 5]:
                self.dtcBoM.save_srr_risk(self._software_model.software_id)
            if self._software_model.phase_id in [3, 4, 5]:
                self.dtcBoM.save_pdr_risk(self._software_model.software_id)
            if self._software_model.phase_id in [4, 5]:
                self.dtcBoM.save_cdr_risk(self._software_model.software_id)
            if self._software_model.phase_id == 5:
                self.dtcBoM.save_trr_risk(self._software_model.software_id)

        elif index == 52:
            self.dtcBoM.request_calculate()

            for __, _key in enumerate(self.dtcBoM.dicSoftware[0].dicErrors):
                if sum(self.dtcBoM.dicSoftware[0].dicErrors[_key]) != 0:
                    _error = self.dtcBoM.dicSoftware[0].dicErrors[_key][0]
                    if _error != 0:
                        _content = "rtk.software.WorkBook._on_button_clicked: " \
                                   "Received error {0:d} while attempting " \
                                   "to calculate anomaly management factor " \
                                   "for {1:d}.".format(_error, _key)
                        self._modulebook.mdcRTK.debug_log.error(_content)

                    _error = self.dtcBoM.dicSoftware[0].dicErrors[_key][1]
                    if _error != 0:
                        _content = "rtk.software.WorkBook._on_button_clicked: " \
                                   "Received error {0:d} while attempting " \
                                   "to calculate software quality factor " \
                                   "for {1:d}.".format(_error, _key)
                        self._modulebook.mdcRTK.debug_log.error(_content)

                    _error = self.dtcBoM.dicSoftware[0].dicErrors[_key][2]
                    if _error != 0:
                        _content = "rtk.software.WorkBook._on_button_clicked: " \
                                   "Received error {0:d} while attempting " \
                                   "to calculate language type factor " \
                                   "for {1:d}.".format(_error, _key)
                        self._modulebook.mdcRTK.debug_log.error(_content)

                    _error = self.dtcBoM.dicSoftware[0].dicErrors[_key][3]
                    if _error != 0:
                        _content = "rtk.software.WorkBook._on_button_clicked: " \
                                   "Received error {0:d} while attempting " \
                                   "to calculate the risk reduction for " \
                                   "{1:d}.".format(_error, _key)
                        self._modulebook.mdcRTK.debug_log.error(_content)

                    _error = self.dtcBoM.dicSoftware[0].dicErrors[_key][4]
                    if _error != 0:
                        _content = "rtk.software.WorkBook._on_button_clicked: " \
                                   "Received error {0:d} while attempting " \
                                   "to calculate the reliability estimation " \
                                   "number for {1:d}.".format(_error, _key)
                        self._modulebook.mdcRTK.debug_log.error(_content)

            _prompt = _(u"One or more errors occurred while attempting to "
                        u"calculate software reliability.")
            Widgets.rtk_error(_prompt)

            _return = True

        elif index == 53:
            self.dtcBoM.save_test_selections(self._software_model.software_id)

        elif index == 54:
            self.dtcBoM.request_calculate()

            for __, _key in enumerate(self.dtcBoM.dicSoftware[0].dicErrors):
                if sum(self.dtcBoM.dicSoftware[0].dicErrors[_key]) != 0:
                    _error = self.dtcBoM.dicSoftware[0].dicErrors[_key][0]
                    if _error != 0:
                        _content = "rtk.software.WorkBook._on_button_clicked: " \
                                   "Received error {0:d} while attempting " \
                                   "to calculate anomaly management factor " \
                                   "for {1:d}.".format(_error, _key)
                        self._modulebook.mdcRTK.debug_log.error(_content)

                    _error = self.dtcBoM.dicSoftware[0].dicErrors[_key][1]
                    if _error != 0:
                        _content = "rtk.software.WorkBook._on_button_clicked: " \
                                   "Received error {0:d} while attempting " \
                                   "to calculate software quality factor " \
                                   "for {1:d}.".format(_error, _key)
                        self._modulebook.mdcRTK.debug_log.error(_content)

                    _error = self.dtcBoM.dicSoftware[0].dicErrors[_key][2]
                    if _error != 0:
                        _content = "rtk.software.WorkBook._on_button_clicked: " \
                                   "Received error {0:d} while attempting " \
                                   "to calculate language type factor " \
                                   "for {1:d}.".format(_error, _key)
                        self._modulebook.mdcRTK.debug_log.error(_content)

                    _error = self.dtcBoM.dicSoftware[0].dicErrors[_key][3]
                    if _error != 0:
                        _content = "rtk.software.WorkBook._on_button_clicked: " \
                                   "Received error {0:d} while attempting " \
                                   "to calculate the risk reduction for " \
                                   "{1:d}.".format(_error, _key)
                        self._modulebook.mdcRTK.debug_log.error(_content)

                    _error = self.dtcBoM.dicSoftware[0].dicErrors[_key][4]
                    if _error != 0:
                        _content = "rtk.software.WorkBook._on_button_clicked: " \
                                   "Received error {0:d} while attempting " \
                                   "to calculate the reliability estimation " \
                                   "number for {1:d}.".format(_error, _key)
                        self._modulebook.mdcRTK.debug_log.error(_content)

            _prompt = _(u"One or more errors occurred while attempting to "
                        u"calculate software reliability.")
            Widgets.rtk_error(_prompt)

            _return = True

        return _return


    def _on_combo_changed(self, combo, index):
        """
        Responds to gtk.ComboBox() changed signals and calls the correct
        function or method, passing any parameters as needed.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called this method.
        :param int index: the index in the handler ID list oc the callback
                          signal associated with the gtk.ComboBox() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        combo.handler_block(self._lst_handler_id[index])

        if index == 1:                      # Software level
            self._software_model.level_id = combo.get_active()
            self._modulebook.update(2, self._software_model.level_id)
        elif index == 2:                    # Software application
            self._software_model.application_id = combo.get_active()
            self._modulebook.update(4, self._software_model.application_id)
        elif index == 3:                    # Development phase
            self._software_model.phase_id = combo.get_active()
            self._modulebook.update(5, self._software_model.phase_id)
            self._load_risk_analysis_page()
        elif index == 4:                    # Test confidence level
            self._software_model.tcl = combo.get_active()
            self._modulebook.update(37, self._software_model.tcl)
        elif index == 5:
            self._software_model.test_path = combo.get_active()
            self._modulebook.update(38, self._software_model.test_path)
        elif index == 6:
            self._software_model.test_effort = combo.get_active()
            self._modulebook.update(40, self._software_model.test_effort)
        elif index == 7:
            self._software_model.test_approach = combo.get_active()
            self._modulebook.update(41, self._software_model.test_approach)

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):     # pylint: disable=R0912
        """
        Responds to gtk.Entry() focus_out signals and calls the correct
        function or method, passing any parameters as needed.

        :param gtk.Entry entry: the gtk.Entry() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Entry() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """
# WARNING: Refactor _on_focus_out; current McCabe Complexity metric = 22.
        entry.handler_block(self._lst_handler_id[index])

        if index == 0:
            _textbuffer = entry.get_buffer()
            self._software_model.description = _textbuffer.get_text(*_textbuffer.get_bounds())
            self._modulebook.update(3, self._software_model.description)
        elif index == 8:
            self._software_model.labor_hours_test = float(entry.get_text())
            self._modulebook.update(42, self._software_model.labor_hours_test)
        elif index == 9:
            self._software_model.labor_hours_dev = float(entry.get_text())
            self._modulebook.update(43, self._software_model.labor_hours_dev)
        elif index == 10:
            self._software_model.budget_test = float(entry.get_text())
            self._modulebook.update(44, self._software_model.budget_test)
        elif index == 11:
            self._software_model.budget_dev = float(entry.get_text())
            self._modulebook.update(45, self._software_model.budget_dev)
        elif index == 12:
            self._software_model.schedule_test = float(entry.get_text())
            self._modulebook.update(46, self._software_model.schedule_test)
        elif index == 13:
            self._software_model.schedule_dev = float(entry.get_text())
            self._modulebook.update(47, self._software_model.schedule_dev)
        elif index == 14:
            self._software_model.branches = int(entry.get_text())
            self._modulebook.update(48, self._software_model.branches)
        elif index == 15:
            self._software_model.branches_test = int(entry.get_text())
            self._modulebook.update(49, self._software_model.branches_test)
        elif index == 16:
            self._software_model.inputs = int(entry.get_text())
            self._modulebook.update(50, self._software_model.inputs)
        elif index == 17:
            self._software_model.inputs_test = int(entry.get_text())
            self._modulebook.update(51, self._software_model.inputs_test)
        elif index == 19:
            self._software_model.nm_test = int(entry.get_text())
            self._modulebook.update(52, self._software_model.nm_test)
        elif index == 20:
            self._software_model.interfaces = int(entry.get_text())
            self._modulebook.update(53, self._software_model.interfaces)
        elif index == 21:
            self._software_model.interfaces_test = int(entry.get_text())
            self._modulebook.update(54, self._software_model.interfaces_test)
        elif index == 22:
            self._software_model.ec = float(entry.get_text())
            self._modulebook.update(63, self._software_model.ec)
        elif index == 23:
            self._software_model.et = float(entry.get_text())
            self._modulebook.update(65, self._software_model.et)
        elif index == 24:
            self._software_model.os = float(entry.get_text())
            self._modulebook.update(66, self._software_model.os)
        elif index == 25:
            self._software_model.dr_test = int(entry.get_text())
            self._modulebook.update(72, self._software_model.dr_test)
        elif index == 26:
            self._software_model.test_time = float(entry.get_text())
            self._modulebook.update(73, self._software_model.test_time)
        elif index == 27:
            self._software_model.dr_eot = int(entry.get_text())
            self._modulebook.update(74, self._software_model.dr_eot)
        elif index == 28:
            self._software_model.test_time_eot = float(entry.get_text())
            self._modulebook.update(75, self._software_model.test_time_eot)

        entry.handler_unblock(self._lst_handler_id[index])

        return False
