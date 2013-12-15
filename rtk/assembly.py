#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to the
hardware assemblies of the Program.
"""

__author__ = 'Andrew Rowland <andrew.rowland@reliaqual.com>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       assembly.py is part of The RTK Project
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

from datetime import datetime

# Import other RTK modules.
import calculations as _calc
import configuration as _conf
import imports as _impt
import utilities as _util
import widgets as _widg

from _assistants_.imports import ImportHardware
from _assistants_.exports import ExportHardware

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, "")

import gettext
_ = gettext.gettext


class Assembly:
    """
    The ASSEMBLY Class is used to represent a piece of hardware in a system
    being analyzed.  It is a meta-class for the COMPONENT Class.
    """

    # TODO: Add tooltips to all widgets.
    _gd_tab_labels = [[_(u"Assembly Name:"), _(u"Part Number:"),
                       _(u"Alternate Part #:"), "", "",
                       _(u"Ref Designator:"), _(u"Composite Ref Des:"),
                       _(u"Quantity:"), _(u"Description:")],
                      [_(u"Specification:"), _(u"Page Number:"),
                       _(u"Figure Number:"), _(u"Image File:"),
                       _(u"Attachments:"), _(u"Mission Time:")],
                      [_(u"Manufacturer:"), _(u"CAGE Code:"), _(u"LCN:"),
                       _(u"NSN:"), _(u"Manufacture Year:")],
                      [_(u"Revision ID:"), _(u"Repairable?"), _(u"Tagged?"),
                       _(u"Remarks:")]]
    _al_tab_labels = [_("Measure:"), _("Reliability:"), _("MTTF/MTBF:"),
                      _("Failure Rate:"), _("Allocation Type:"),
                      _("Elements:"), _("Operating Time:")]
    _ai_tab_labels = [[_("h(t) Type:"), _("Calculation Model:"),
                       _("Specified h(t):"), _("Specified MTBF:"),
                       _("Software h(t):"), _("Additive Adj:"),
                       _("Multiplicative Adj:"),
                       _("Allocation Weight:"),
                       _("Failure Distribution:"), _("Scale:"), _("Shape:"),
                       _("Location:"), _("Active Environ:"),
                       _("Active Temp:"), _("Dormant Environ:"),
                       _("Dormant Temp:"), _("Duty Cycle:"),
                       _("Humidity:"), _("Vibration:"), _("RPM:"),
                       _("Weibull File:")],
                      [_("MTTR Type:"), _("Specified MTTR:"),
                       _("Additive Adj:"),
                       _("Multiplicative Adj:"),
                       _("Repair Distribution:"), _("Scale:"), _("Shape:")],
                      [],
                      [_("Cost Type:"), _("Unit Cost:")]]
    _ar_tab_labels = [[_("Active h(t):"), _("Dormant h(t):"),
                       _("Software h(t):"), _("Predicted h(t):"),
                       _("Mission h(t):"), _("h(t) Percent:"),
                       _("MTBF:"), _("Mission MTBF:"), _("Reliability:"),
                       _("Mission R(t):")],
                      [_("MPMT:"), _("MCMT:"), _("MTTR:"), _("MMT:"),
                       _("Availability:"), _("Mission A(t):")],
                      [],
                      [_("Total Cost:"), _("Cost/Failure:"), _("Cost/Hour:"),
                       _("Assembly Criticality:"), _("Total Part Count:"),
                       _("Total Power Used:")]]

    _al_header_labels = [_("Revision ID"), _("Assembly ID"),
                         _("Description"), _("Included?"),
                         _("Number of\nSub-Systems"),
                         _("Number of\nSub-Elements"),
                         _("Operating\nTime"), _("Duty Cycle"),
                         _("Intricacy\n(1-10)"), _("State of\nthe Art\n(1-10)"),
                         _("Operating\nTime (1-10)"), _("Environment\n(1-10)"),
                         _("Weighting\nFactor"), _("Percent\nWeighting\nFactor"),
                         _("Current\nFailure\nRate"),
                         _("Allocated\nFailure\nRate"),
                         _("Current\nMTBF"), _("Allocated\nMTBF"),
                         _("Current\nReliability"), _("Allocated\nReliability"),
                         _("Current\nAvailability"), _("Allocated\nAvailability")]

    _ft_tab_labels = [[_("Incident ID:"), _("Incident Date:"),
                       _("Reported By:"), _("Category:"),
                       _("Problem Type:"), _("Description:"),
                       _("Details:"), _("Criticality:"),
                       _("Method of Detection:"), _("Remarks:"),
                       _("Product Life Cycle:"), _("Incident Status:")],
                      [_("Test Procedure:"), _("Test Case:"),
                       _("Execution Time:"), _("Effect of Problem:"),
                       _("Recommended Solution:")],
                      [_("This failure occurred on equipment or a component part that is production intent."),
                       _("This failure is independent of any other failure."),
                       _("This failure is due to design deficiencies or poor workmanship of the equipment or component part."),
                       _("This failure is due to a defective component part."),
                       _("This failure is due to a component part that wore out prior to it's stipulated life."),
                       _("This failure is the first occurrence of an intermittent failure on this equipment."),
                       _("This failure is a malfunction (including false alarm) of the built-in test features."),
                       _("This failure is due to misadjustment of operator controls AND the information necessary to properly adjust these controls is not available from indicators which are integral to the equipment under test."),
                       _("This failure is dependent on another, relevent, failure."),
                       _("This failure is directly attributable to improper test setup."),
                       _("This failure is the failure of test insrumentation or monitoring equipment (other than built-in test equipment)."),
                       _("This failure is the result of test operator error."),
                       _("This failure is attributable to an error in the test procedure."),
                       _("This failure is the second or subsequent intermittent failure on this equipment."),
                       _("This failure occurred during burn-in, troubleshooting, repair verification, or setup."),
                       _("This failure is clearly attributable to an overstress condition in excess of the design requirements."),
                       _("This failure is within the responsibility of this organization.")],
                      [_("Prescribed Action:"), _("Action Taken:"),
                       _("Owner:"), _("Due Date:"), _("Status:"),
                       _("Approved"), _("Approved By:"), _("Approval Date:"),
                       _("Closed"), _("Closed By:"), _("Closure Date:")],
                      [_("Reviewed"), _("Reviewed By:"), _("Reviewed Date:"),
                       _("Approved"), _("Approved By:"), _("Approved Date:"),
                       _("Closed"), _("Closed By:"), _("Closure Date:")]]

    _mp_tab_labels = [[_(u"This item is a major load carrying element."),
                       _(u"The loss of this item's function results in an adverse effect on operating safety or aborts the mission."),
                       _(u"The actual or predicted failure rate and consumption of resources is high."),
                       _(u"The item, or a like item on similar equipment, has existing scheduled maintenance requirements."),
                       _(u"This item is Structurally Significant"),
                       _(u"This item is Functionally Significant")],
                      [_(u"This failure mode is evident to the operating crew\nwhile performing normal duties."),
                       _(u"This failure mode causes a functional loss or secondary\ndamage that could have a direct, adverse effect\non operating safety."),
                       _(u"This hidden failure mode by itself or in combination\nwith another failure has an adverse effect on\noperating safety."),
                       _(u"Safety Hidden"), _(u"Safety Evident"),
                       _(u"Non-Safety Hidden"), _(u"Economic/Operational")]]

    def __init__(self, application):
        """
        Initializes the Assembly Object.

        Keyword Arguments:
        application -- the RTK application.
        """

        self._ready = False

        self._app = application

        self.system_model = self._app.HARDWARE.model
        self.system_selected_row = self._app.HARDWARE.selected_row

# Define local dictionary variables.
        self._mission = {}
        self._mission_phase = {}
        self._assembly_risks_ = {}          # Carries risk matrix values for the assembly.
        self._system_risks_ = {}            # Carries risk matrix values for the system.
        self._hrmodel = {}
        self._fmeca = {}
        self._mechanisms = {}
        self._fmeca_controls = {}
        self._fmeca_actions = {}
        self._CA = {}                       # Carries MIL-STD-1629A values.
        self._ItemCA = {}                   # Carries MIL-STD-1629A values.
        self._rpnsev = {}                   # Carries RPN severity values.
        self._RPN = {}                      # Carries RPN and new RPN values.

# Define local list variables.
        self._risk_col_order = []
        self._sia_col_order = []

# Define global scalar variables.
        self.assembly_id = 0

# Define local scalar variables.
        self._category = 0
        self._subcategory = 0
        self._mode_id = 0

# Create the Notebook for the ASSEMBLY object.
        self.notebook = gtk.Notebook()
        if(_conf.TABPOS[2] == 'left'):
            self.notebook.set_tab_pos(gtk.POS_LEFT)
        elif(_conf.TABPOS[2] == 'right'):
            self.notebook.set_tab_pos(gtk.POS_RIGHT)
        elif(_conf.TABPOS[2] == 'top'):
            self.notebook.set_tab_pos(gtk.POS_TOP)
        else:
            self.notebook.set_tab_pos(gtk.POS_BOTTOM)

        self.notebook.connect('switch-page', self._notebook_page_switched)

# Create generic toolbar action buttons.  These will call different
# methods or functions depending on the ASSEMBLY Object notebook tab
# that is selected.
        self.btnAddItem = gtk.ToolButton()
        self.btnFMECAAdd = gtk.MenuToolButton(None, label = "")
        self.btnRemoveItem = gtk.ToolButton()
        self.btnAnalyze = gtk.ToolButton()
        self.btnSaveResults = gtk.ToolButton()
        self.btnRollup = gtk.ToolButton()
        self.btnEdit = gtk.ToolButton()

# Create the General Data tab widgets for the ASSEMBLY object.
        self.fxdGenDataQuad1 = gtk.Fixed()
        self.txtName = _widg.make_entry()
        self.txtPartNum = _widg.make_entry()
        self.txtAltPartNum = _widg.make_entry()
        self.txtRefDes = _widg.make_entry()
        self.txtCompRefDes = _widg.make_entry()
        self.txtQuantity = _widg.make_entry()
        self.txtDescription = _widg.make_entry(_width_=700)
        self.fxdGenDataQuad2 = gtk.Fixed()
        self.cmbManufacturer = _widg.make_combo(simple=False)
        self.txtCAGECode = _widg.make_entry()
        self.txtLCN = _widg.make_entry()
        self.txtNSN = _widg.make_entry()
        self.txtYearMade = _widg.make_entry()
        self.fxdGenDataQuad3 = gtk.Fixed()
        self.txtSpecification = _widg.make_entry()
        self.txtPageNum = _widg.make_entry()
        self.txtFigNum = _widg.make_entry()
        self.txtImageFile = _widg.make_entry()
        self.txtAttachments = _widg.make_entry()
        self.txtMissionTime = _widg.make_entry()
        self.fxdGenDataQuad4 = gtk.Fixed()
        self.txtRevisionID = _widg.make_entry(_width_=50, editable=False)
        self.chkRepairable = _widg.make_check_button()
        self.chkTagged = _widg.make_check_button()
        self.txtRemarks = _widg.make_text_view(width=400)
        if self._general_data_widgets_create():
            self._app.debug_log.error("assembly.py: Failed to create General Data tab widgets.")
        if self._general_data_tab_create():
            self._app.debug_log.error("assembly.py: Failed to create General Data tab.")

# Create the Diagrams tab widgets for the ASSEMBLY object.
        # TODO: Implement Diagram Worksheet for ASSEMBLY.

# Create the Allocation tab widgets for the ASSEMBLY object.
        self.tvwAllocation = gtk.TreeView()
        self.cmbRqmtType = _widg.make_combo(_width_=125)
        self.txtReliabilityGoal = _widg.make_entry(_width_=125)
        self.txtMTBFGoal = _widg.make_entry(_width_=125)
        self.txtFailureRateGoal = _widg.make_entry(_width_=125)
        self.cmbAllocationType = _widg.make_combo(_width_=125)
        self.txtNumElements = _widg.make_entry(_width_=125,
                                               editable=False,
                                               bold=True)
        self.txtOperTime = _widg.make_entry(_width_=125)
        self.chkApplyResults = _widg.make_check_button(_(u"Apply results to hardware"))
        if self._allocation_widgets_create():
            self._app.debug_log.error("assembly.py: Failed to create Allocation tab widgets.")
        if self._allocation_tab_create():
            self._app.debug_log.error("assembly.py: Failed to create Allocation tab.")

# Create the Risk Analysis tab widgets for the ASSEMBLY object.
        self.fraRiskAnalysis = _widg.make_frame()
        self.tvwRisk = gtk.TreeView()
        self.tvwRiskMap = gtk.TreeView()
        if self._risk_analysis_widgets_create():
            self._app.debug_log.error("assembly.py: Failed to create Risk Analysis widgets.")
        if self._risk_analysis_tab_create():
            self._app.debug_log.error("assembly.py: Failed to create Risk Analysis tab.")

# Create the Similar Items Analysis tab widgets for the ASSEMBLY object.
        self.tvwSIA = gtk.TreeView()
        if self._similar_item_widgets_create():
            self._app.debug_log.error("assembly.py: Failed to create Similar Item widgets.")
        if self._similar_item_tab_create():
            self._app.debug_log.error("assembly.py: Failed to create Similar Item tab.")

# Create the Assessment Input tab widgets for the ASSEMBLY object.
        self.fxdRelInputQuad1 = gtk.Fixed()
        self.cmbHRType = _widg.make_combo()
        self.cmbCalcModel = _widg.make_combo()
        self.txtSpecifiedHt = _widg.make_entry()
        self.txtSpecifiedMTBF = _widg.make_entry()
        self.txtSoftwareHt = _widg.make_entry()
        self.txtAddAdj = _widg.make_entry()
        self.txtMultAdj = _widg.make_entry()
        self.txtAllocationWF = _widg.make_entry()
        self.cmbFailDist = _widg.make_combo()
        self.txtFailScale = _widg.make_entry()
        self.txtFailShape = _widg.make_entry()
        self.txtFailLoc = _widg.make_entry()
        self.cmbActEnviron = _widg.make_combo()
        self.txtActTemp = _widg.make_entry()
        self.cmbDormantEnviron = _widg.make_combo()
        self.txtDormantTemp = _widg.make_entry()
        self.txtDutyCycle = _widg.make_entry()
        self.txtHumidity = _widg.make_entry()
        self.txtVibration = _widg.make_entry()
        self.txtRPM = _widg.make_entry()
        self.txtWeibullFile = _widg.make_entry()
        self.fxdRelInputQuad2 = gtk.Fixed()
        self.cmbMTTRType = _widg.make_combo()
        self.txtSpecifiedMTTR = _widg.make_entry()
        self.txtMTTRAddAdj = _widg.make_entry()
        self.txtMTTRMultAdj = _widg.make_entry()
        self.cmbRepairDist = _widg.make_combo()
        self.txtRepairScale = _widg.make_entry()
        self.txtRepairShape = _widg.make_entry()
        self.fxdRelInputQuad4 = gtk.Fixed()
        self.cmbCostType = _widg.make_combo(200, 30)
        self.txtCost = _widg.make_entry()
        if self._assessment_inputs_widgets_create():
            self._app.debug_log.error("assembly.py: Failed to create Assessment Inputs tab widgets.")
        if self._assessment_inputs_tab_create():
            self._app.debug_log.error("assembly.py: Failed to create Assessment Inputs tab.")

# Create the Assessment Results tab widgets for the ASSEMBLY object.
        self.fxdCalcResultsQuad1 = gtk.Fixed()
        self.txtActiveHt = _widg.make_entry(editable=False, bold=True)
        self.txtDormantHt = _widg.make_entry(editable=False, bold=True)
        self.txtSoftwareHt2 = _widg.make_entry(editable=False, bold=True)
        self.txtPredictedHt = _widg.make_entry(editable=False, bold=True)
        self.txtMissionHt = _widg.make_entry(editable=False, bold=True)
        self.txtHtPerCent = _widg.make_entry(editable=False, bold=True)
        self.txtMTBF = _widg.make_entry(editable=False, bold=True)
        self.txtMissionMTBF = _widg.make_entry(editable=False, bold=True)
        self.txtReliability = _widg.make_entry(editable=False, bold=True)
        self.txtMissionRt = _widg.make_entry(editable=False, bold=True)
        self.fxdCalcResultsQuad2 = gtk.Fixed()
        self.txtMPMT = _widg.make_entry(editable=False, bold=True)
        self.txtMCMT = _widg.make_entry(editable=False, bold=True)
        self.txtMTTR = _widg.make_entry(editable=False, bold=True)
        self.txtMMT = _widg.make_entry(editable=False, bold=True)
        self.txtAvailability = _widg.make_entry(editable=False, bold=True)
        self.txtMissionAt = _widg.make_entry(editable=False, bold=True)
        self.fxdCalcResultsQuad4 = gtk.Fixed()
        self.txtTotalCost = _widg.make_entry(editable=False, bold=True)
        self.txtCostFailure = _widg.make_entry(editable=False, bold=True)
        self.txtCostHour = _widg.make_entry(editable=False, bold=True)
        self.txtAssemblyCrit = _widg.make_entry(editable=False, bold=True)
        self.txtPartCount = _widg.make_entry(editable=False, bold=True)
        self.txtTotalPwr = _widg.make_entry(editable=False, bold=True)
        if self._assessment_results_widgets_create():
            self._app.debug_log.error("assembly.py: Failed to create Assessment Results tab widgets.")
        if self._assessment_results_tab_create():
            self._app.debug_log.error("assembly.py: Failed to create Assessment Results tab.")

# Create the FMEA/FMECA tab widgets for the ASSEMBLY object.
        bg_color = _conf.RTK_COLORS[6]
        fg_color = _conf.RTK_COLORS[7]
        (self.tvwFMECA,
         self._FMECA_col_order) = _widg.make_treeview('FMECA', 9,
                                                      self._app,
                                                      None,
                                                      bg_color,
                                                      fg_color)

        # Add background color and editable attributes so failure mechanisms,
        # controls, and actions will not be editable in the FMECA worksheet.
        cols = len(self._FMECA_col_order)
        _column = self.tvwFMECA.get_columns()
        for i in range(len(_column)):
            _cell = _column[i].get_cell_renderers()

            # Always allow editting of the first column since this is the
            # description column.
            if(i == 1):
                _cell[0].set_property('background', '#FFFFFF')
                _cell[0].set_property('editable', True)
            else:
                try:
                    if(_cell[0].get_property('editable')):
                        _column[i].add_attribute(_cell[0], 'background', cols + 1)
                        _column[i].add_attribute(_cell[0], 'editable', cols + 2)
                except TypeError:
                    pass

        self.fraFMECADetails = _widg.make_frame(_label_=_(u"Failure Mechanism Details"))

        # Create the widgets to display the failure mode details.
        self.fxdMode = gtk.Fixed()
        self.chkFCQ1 = _widg.make_check_button(_label_=self._mp_tab_labels[1][0])
        self.chkFCQ1.connect('toggled', self._callback_check, 90)
        self.chkFCQ2 = _widg.make_check_button(_label_=self._mp_tab_labels[1][1])
        self.chkFCQ2.connect('toggled', self._callback_check, 90)
        self.chkFCQ3 = _widg.make_check_button(_label_=self._mp_tab_labels[1][2])
        self.chkFCQ3.connect('toggled', self._callback_check, 90)

        buffer = gtk.TextBuffer()
        self.txtFCQ1 = _widg.make_text_view(buffer_=buffer, width=400, height=75)
        buffer = gtk.TextBuffer()
        self.txtFCQ2 = _widg.make_text_view(buffer_=buffer, width=400, height=75)
        buffer = gtk.TextBuffer()
        self.txtFCQ3 = _widg.make_text_view(buffer_=buffer, width=400, height=75)

        self.optHS = _widg.make_option_button(_label_=self._mp_tab_labels[1][3])
        self.optES = _widg.make_option_button(_group_=self.optHS,
                                              _label_=self._mp_tab_labels[1][4])
        self.optNSH = _widg.make_option_button(_group_=self.optHS,
                                               _label_=self._mp_tab_labels[1][5])
        self.optEO = _widg.make_option_button(_group_=self.optHS,
                                              _label_=self._mp_tab_labels[1][6])

        # Create the widgets to display the failure mechanism/cause details.
        self.fxdMechanism = gtk.Fixed()
        self.cmbOccurenceI = _widg.make_combo()
        self.cmbDetectionI = _widg.make_combo()
        self.cmbOccurrenceN = _widg.make_combo()
        self.cmbDetectionN = _widg.make_combo()
        self.txtMechanismID = _widg.make_entry(_width_=50, editable=False)
        self.txtMechanismDescription = _widg.make_entry()
        self.txtRPNI = _widg.make_entry(_width_=50, editable=False)
        self.txtRPNN = _widg.make_entry(_width_=50, editable=False)

        # Create the widgets to display the current controls details.
        self.fxdControl = gtk.Fixed()
        self.cmbControlType = _widg.make_combo()
        self.txtControlID = _widg.make_entry(_width_=50, editable=False)
        self.txtControlDescription = _widg.make_entry()

        # Create the widgets to display the recommended action details.
        self.fxdAction = gtk.Fixed()
        self.cmbActionCategory = _widg.make_combo()
        self.cmbActionStatus = _widg.make_combo()
        self.cmbActionResponsible = _widg.make_combo()
        self.cmbActionApproved = _widg.make_combo()
        self.cmbActionClosed = _widg.make_combo()
        self.txtActionID = _widg.make_entry(_width_=50, editable=False)
        self.txtActionDueDate = _widg.make_entry(_width_=100)
        self.txtActionApproveDate = _widg.make_entry(_width_=100)
        self.txtActionCloseDate = _widg.make_entry(_width_=100)
        self.txtActionRecommended = _widg.make_text_view(width=375, height=75)
        self.txtActionTaken = _widg.make_text_view(width=375, height=75)

        if self._fmeca_tab_create():
            self._app.debug_log.error("assembly.py: Failed to create FMECA tab.")

# Create the Maintenance Planning tab widgets for the ASSEMBLY object.
        # Create the widgets for determing SSI and FSI status.
        self.chkFSIQ1 = _widg.make_check_button(_label_=self._mp_tab_labels[0][0])
        self.chkFSIQ2 = _widg.make_check_button(_label_=self._mp_tab_labels[0][1])
        self.chkFSIQ3 = _widg.make_check_button(_label_=self._mp_tab_labels[0][2])
        self.chkFSIQ4 = _widg.make_check_button(_label_=self._mp_tab_labels[0][3])

        buffer = gtk.TextBuffer()
        self.txtFSIQ1 = _widg.make_text_view(buffer_=buffer, width=800,
                                             height=75)
        buffer = gtk.TextBuffer()
        self.txtFSIQ2 = _widg.make_text_view(buffer_=buffer, width=800,
                                             height=75)
        buffer = gtk.TextBuffer()
        self.txtFSIQ3 = _widg.make_text_view(buffer_=buffer, width=800,
                                             height=75)
        buffer = gtk.TextBuffer()
        self.txtFSIQ4 = _widg.make_text_view(buffer_=buffer, width=800,
                                             height=75)

        self.chkSSI = _widg.make_check_button(_label_=self._mp_tab_labels[0][4])
        self.chkFSI = _widg.make_check_button(_label_=self._mp_tab_labels[0][5])

        self._safety_significance_widgets_create()
        self._safety_significance_tab_create()

        #self._maintenance_planning_tab_create()

        self.vbxAssembly = gtk.VBox()
        toolbar = self._toolbar_create()

        self.vbxAssembly.pack_start(toolbar, expand=False)
        self.vbxAssembly.pack_start(self.notebook)

        self._selected_tab = 0

        self._ready = True

    def _toolbar_create(self):
        """ Method to create the toolbar for the Assembly Object work book. """

        toolbar = gtk.Toolbar()

        _pos = 0

# Add sibling assembly button.
        button = gtk.ToolButton()
        button.set_tooltip_text(_(u"Adds a new assembly at the same indenture level as the selected assembly to the RTK Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.assembly_add, 0)
        toolbar.insert(button, _pos)
        _pos += 1

# Add child assembly button.
        button = gtk.ToolButton()
        button.set_tooltip_text(_(u"Adds a new assembly one indenture level subordinate to the selected assembly to the RTK Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_child.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.assembly_add, 1)
        toolbar.insert(button, _pos)
        _pos += 1

# Delete assembly button
        button = gtk.ToolButton()
        button.set_tooltip_text(_(u"Removes the currently selected assembly from the RTK Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.assembly_delete)
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

# Add item button.  Depending on the notebook page selected will determine
# what type of item is added.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        self.btnAddItem.set_icon_widget(image)
        self.btnAddItem.set_name('Add')
        self.btnAddItem.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnAddItem, _pos)
        _pos += 1

        self.btnFMECAAdd.set_tooltip_text(_(u"Add items to the active FMEA/FMECA."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        self.btnFMECAAdd.set_icon_widget(image)
        menu = gtk.Menu()
        menu_item = gtk.MenuItem(label=_(u"Mode"))
        menu_item.set_tooltip_text(_("Add a new failure mode to the currently selected assembly."))
        menu_item.connect('activate', self._toolbutton_pressed)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_(u"Mechanism"))
        menu_item.set_tooltip_text(_(u"Add a new failure mechanism to the currently selected failure mode."))
        menu_item.connect('activate', self._toolbutton_pressed)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_(u"Control"))
        menu_item.set_tooltip_text(_(u"Add a new control to the currently selected failure mechanism."))
        menu_item.connect('activate', self._toolbutton_pressed)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_(u"Action"))
        menu_item.set_tooltip_text(_("Add a new acion to the currently selected failure mechanism."))
        menu_item.connect('activate', self._toolbutton_pressed)
        menu.add(menu_item)
        self.btnFMECAAdd.set_menu(menu)
        menu.show_all()
        self.btnFMECAAdd.show()
        toolbar.insert(self.btnFMECAAdd, _pos)
        _pos += 1

# Remove item button.  Depending on the notebook page selected will determine
# what type of item is removed.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        self.btnRemoveItem.set_icon_widget(image)
        self.btnRemoveItem.set_name('Remove')
        self.btnRemoveItem.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnRemoveItem, _pos)
        _pos += 1

# Perform analysis button.  Depending on the notebook page selected will
# determine which analysis is executed.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        self.btnAnalyze.set_icon_widget(image)
        self.btnAnalyze.set_name('Analyze')
        self.btnAnalyze.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnAnalyze, _pos)
        _pos += 1

# Save results button.  Depending on the notebook page selected will determine
# which results are saved.
# TODO: Add 'SAVE' button for saving the currently selected Assembly.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        self.btnSaveResults.set_icon_widget(image)
        self.btnSaveResults.set_name('Save')
        self.btnSaveResults.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnSaveResults, _pos)
        _pos += 1

        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/rollup.png')
        self.btnRollup.set_icon_widget(image)
        self.btnRollup.set_name('Rollup')
        self.btnRollup.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnRollup, _pos)
        _pos += 1

        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/edit.png')
        self.btnEdit.set_icon_widget(image)
        self.btnEdit.set_name('Edit')
        self.btnEdit.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnEdit, _pos)
        _pos += 1

# Create an import button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/db-import.png')
        button.set_icon_widget(image)
        button.set_name('Import')
        button.connect('clicked', ImportHardware, self._app)
        button.set_tooltip_text(_(u"Launches the hardware import assistant."))
        toolbar.insert(button, _pos)
        _pos += 1

# Create an export button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/db-export.png')
        button.set_icon_widget(image)
        button.set_name('Export')
        button.connect('clicked', ExportHardware, self._app)
        button.set_tooltip_text(_(u"Launches the hardware export assistant."))
        toolbar.insert(button, _pos)

        toolbar.show()

# Hide the toolbar buttons associated with specific analyses.
        self.btnAddItem.hide()
        self.btnFMECAAdd.hide()
        self.btnRemoveItem.hide()
        self.btnAnalyze.hide()
        self.btnSaveResults.hide()
        self.btnRollup.hide()
        self.btnEdit.hide()

        return(toolbar)

    def _general_data_widgets_create(self):
        """ Method to create General Data widgets. """

# Create the labels for the upper-left and lower-left quadrants.
        y_pos = 5
        _max1_ = 0
        _max2_ = 0
        _max1_ = _widg.make_labels(self._gd_tab_labels[0],
                                   self.fxdGenDataQuad1,
                                   y_pos)
        _max2_ = _widg.make_labels(self._gd_tab_labels[2],
                                   self.fxdGenDataQuad2,
                                   y_pos)

        _x_pos_ = max(_max1_, _max2_) + 20

# Quadrant 1 (upper left) widgets.  These widgets are used to display general
# information about the selected assembly.
        self.txtName.set_tooltip_text(_("Enter the name of the selected assembly."))
        self.txtName.connect('focus-out-event',
                             self._callback_entry, 'text', 58)

        self.txtPartNum.set_tooltip_text(_("Enter the part number of the selected assembly."))
        self.txtPartNum.connect('focus-out-event',
                                self._callback_entry, 'text', 64)

        self.txtAltPartNum.set_tooltip_text(_("Enter an alternative part number for the selected assembly."))
        self.txtAltPartNum.connect('focus-out-event',
                                   self._callback_entry, 'text', 4)

        self.txtRefDes.set_tooltip_text(_("Enter the reference designator of the selected assembly."))
        self.txtRefDes.connect('focus-out-event',
                               self._callback_entry, 'text', 68)

        self.txtCompRefDes.set_tooltip_text(_("Enter the composite reference designator of the selected assembly."))
        self.txtCompRefDes.connect('focus-out-event',
                                   self._callback_entry, 'text', 12)

        self.txtQuantity.set_tooltip_text(_("Enter the quantity of the selected assembly."))
        self.txtQuantity.connect('focus-out-event',
                                 self._callback_entry, 'int', 67)

        self.txtDescription.set_tooltip_text(_("Enter a description for the selected assembly."))
        self.txtDescription.connect('focus-out-event',
                                    self._callback_entry, 'text', 17)

        # Place the widgets.
        self.fxdGenDataQuad1.put(self.txtName, _x_pos_, y_pos)
        y_pos += 30
        self.fxdGenDataQuad1.put(self.txtPartNum, _x_pos_, y_pos)
        y_pos += 30
        self.fxdGenDataQuad1.put(self.txtAltPartNum, _x_pos_, y_pos)
        y_pos += 90
        self.fxdGenDataQuad1.put(self.txtRefDes, _x_pos_, y_pos)
        y_pos += 30
        self.fxdGenDataQuad1.put(self.txtCompRefDes, _x_pos_, y_pos)
        y_pos += 30
        self.fxdGenDataQuad1.put(self.txtQuantity, _x_pos_, y_pos)
        y_pos += 30
        self.fxdGenDataQuad1.put(self.txtDescription, _x_pos_, y_pos)

        self.fxdGenDataQuad1.show_all()

# Quadrant 2 (upper right) widgets.  These widgets are used to display
# logistics information about the selected assembly.
        self.cmbManufacturer.set_tooltip_text(_("Select the manufacturer of the selected assembly."))
        self.cmbManufacturer.connect('changed',
                                     self._callback_combo, 43)

        query = "SELECT fld_manufacturers_noun, fld_location, fld_cage_code \
                 FROM tbl_manufacturers \
                 ORDER BY fld_manufacturers_noun ASC"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbManufacturer, results, False)

        self.txtCAGECode.set_tooltip_text(_("Enter the Commercial and Government Entity (CAGE) code of the selected assembly."))
        self.txtCAGECode.connect('focus-out-event',
                                 self._callback_entry, 'text', 9)

        self.txtLCN.set_tooltip_text(_("Enter the logistics control number (LCN) of the selected assembly."))
        self.txtLCN.connect('focus-out-event',
                            self._callback_entry, 'text', 41)

        self.txtNSN.set_tooltip_text(_("Enter the national stock number (NSN) of the selected assembly."))
        self.txtNSN.connect('focus-out-event',
                            self._callback_entry, 'text', 59)

        self.txtYearMade.set_tooltip_text(_("Enter the year the selected assembly was manufactured."))
        self.txtYearMade.connect('focus-out-event',
                                 self._callback_entry, 'int', 87)

        # Place the widgets.
        y_pos = 5
        self.fxdGenDataQuad2.put(self.cmbManufacturer, _x_pos_, y_pos)
        y_pos += 30
        self.fxdGenDataQuad2.put(self.txtCAGECode, _x_pos_, y_pos)
        y_pos += 30
        self.fxdGenDataQuad2.put(self.txtLCN, _x_pos_, y_pos)
        y_pos += 30
        self.fxdGenDataQuad2.put(self.txtNSN, _x_pos_, y_pos)
        y_pos += 30
        self.fxdGenDataQuad2.put(self.txtYearMade, _x_pos_, y_pos)

        self.fxdGenDataQuad2.show_all()

# Create the labels for the upper-right and lower-right quadrants.
        y_pos = 5
        _max1_ = 0
        _max2_ = 0
        _max1_ = _widg.make_labels(self._gd_tab_labels[1],
                                   self.fxdGenDataQuad3,
                                   y_pos)
        _max2_ = _widg.make_labels(self._gd_tab_labels[3],
                                   self.fxdGenDataQuad4,
                                   y_pos)

        _x_pos_ = max(_max1_, _max2_) + 20

# Quadrant 3 (lower left) widgets.  These widget are used to display
# requirements information about the selected assembly.
        self.txtSpecification.set_tooltip_text(_("Enter the governing specification for the selected assembly, if any."))
        self.txtSpecification.connect('focus-out-event',
                                      self._callback_entry, 'text', 77)

        self.txtPageNum.set_tooltip_text(_("Enter the governing specification page number for the selected assembly."))
        self.txtPageNum.connect('focus-out-event',
                                self._callback_entry, 'text', 61)

        self.txtFigNum.set_tooltip_text(_("Enter the governing specification figure number for the selected assembly."))
        self.txtFigNum.connect('focus-out-event',
                               self._callback_entry, 'text', 36)

        self.txtImageFile.set_tooltip_text(_("Enter the URL to an image of the selected assembly."))
        self.txtImageFile.connect('focus-out-event',
                                  self._callback_entry, 'text', 38)

        self.txtAttachments.set_tooltip_text(_("Enter the URL to an attachment associated with the selected assembly."))
        self.txtAttachments.connect('focus-out-event',
                                    self._callback_entry, 'text', 6)

        self.txtMissionTime.set_tooltip_text(_("Enter the mission time for the selected assembly."))
        self.txtMissionTime.connect('focus-out-event',
                                    self._callback_entry, 'float', 45)

        # Place the widgets.
        self.fxdGenDataQuad3.put(self.txtSpecification, _x_pos_, y_pos)
        y_pos += 30
        self.fxdGenDataQuad3.put(self.txtPageNum, _x_pos_, y_pos)
        y_pos += 30
        self.fxdGenDataQuad3.put(self.txtFigNum, _x_pos_, y_pos)
        y_pos += 30
        self.fxdGenDataQuad3.put(self.txtImageFile, _x_pos_, y_pos)
        y_pos += 30
        self.fxdGenDataQuad3.put(self.txtAttachments, _x_pos_, y_pos)
        y_pos += 30
        self.fxdGenDataQuad3.put(self.txtMissionTime, _x_pos_, y_pos)

        self.fxdGenDataQuad3.show_all()

# Quadrant 4 (lower right) widgets.  These widgets are used to display
# miscellaneous information about the selected assembly.
        self.txtRevisionID.set_tooltip_text(_("Displays the currently selected revision."))

        self.chkRepairable.set_tooltip_text(_("Indicates whether or not the selected assembly is repairable."))
        self.chkRepairable.connect('toggled', self._callback_check, 75)

        self.chkTagged.set_tooltip_text(_("Indicates whether or not the selected assembly is tagged."))
        self.chkTagged.connect('toggled', self._callback_check, 79)

        # Place the widgets.
        y_pos = 5
        self.fxdGenDataQuad4.put(self.txtRevisionID, _x_pos_, y_pos)
        y_pos += 30
        self.fxdGenDataQuad4.put(self.chkRepairable, _x_pos_, y_pos)
        y_pos += 30
        self.fxdGenDataQuad4.put(self.chkTagged, _x_pos_, y_pos)
        y_pos += 30

        self.txtRemarks.set_tooltip_text(_(u"Enter any remarks associated with the selected assembly."))
        self.txtRemarks.get_child().get_child().connect('focus-out-event',
                                                        self._callback_entry,
                                                        'text', 71)
        self.fxdGenDataQuad4.put(self.txtRemarks, _x_pos_, y_pos)

        self.fxdGenDataQuad4.show_all()

        return False

    def _general_data_tab_create(self):
        """
        Method to create the General Data gtk.Notebook tab and populate it
        with the appropriate widgets for the ASSEMVBLY object.
        """

        hbox = gtk.HBox()

# Populate quadrant 1 (upper left).
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.fxdGenDataQuad1)

        frame = _widg.make_frame(_label_=_(u"General Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned = gtk.VPaned()

        vpaned.pack1(frame, True, True)

# Populate quadrant 2 (lower left).
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.fxdGenDataQuad2)

        frame = _widg.make_frame(_label_=_(u"Manufacturer Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned.pack2(frame, True, True)

        hbox.pack_start(vpaned)

# Populate quadrant 3 (upper right).
        vpaned = gtk.VPaned()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.fxdGenDataQuad3)

        frame = _widg.make_frame(_label_=_(u"Specification Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned.pack1(frame, True, True)

# Populate quadrant 4 (lower right).
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.fxdGenDataQuad4)

        frame = _widg.make_frame(_label_=_(u"Miscellaneous Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned.pack2(frame, True, True)

        hbox.pack_start(vpaned)

# Insert the tab.
        label = gtk.Label()
        _heading = _(u"General\nData")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Displays general information about the selected assembly."))

        self.notebook.insert_page(hbox,
                                  tab_label=label,
                                  position=-1)

        return False

    def _general_data_tab_load(self):
        """
        Loads the widgets with general information about the ASSEMBLY Object.
        """

        treemodel = self._app.HARDWARE.model
        row = self._app.HARDWARE.selected_row

        self.txtRevisionID.set_text(str(treemodel.get_value(row, 0)))
        self.txtAltPartNum.set_text(treemodel.get_value(row, 4))
        self.txtAttachments.set_text(treemodel.get_value(row, 6))
        self.txtCAGECode.set_text(treemodel.get_value(row, 9))
        self.txtCompRefDes.set_text(treemodel.get_value(row, 12))
        self.txtDescription.set_text(treemodel.get_value(row, 17))
        self.txtFigNum.set_text(treemodel.get_value(row, 36))
        self.txtImageFile.set_text(treemodel.get_value(row, 38))
        self.txtLCN.set_text(treemodel.get_value(row, 41))
        self.cmbManufacturer.set_active(treemodel.get_value(row, 43))
        self.txtName.set_text(treemodel.get_value(row, 58))
        self.txtNSN.set_text(treemodel.get_value(row, 59))
        self.txtPageNum.set_text(treemodel.get_value(row, 61))
        self.txtPartNum.set_text(treemodel.get_value(row, 64))
        self.txtQuantity.set_text(str(treemodel.get_value(row, 67)))
        self.txtRefDes.set_text(treemodel.get_value(row, 68))
        _text_ = _util.none_to_string(treemodel.get_value(row, 71))
        textbuffer = self.txtRemarks.get_child().get_child().get_buffer()
        textbuffer.set_text(_text_)
        self.chkRepairable.set_active(treemodel.get_value(row, 75))
        self.txtSpecification.set_text(treemodel.get_value(row, 77))
        self.chkTagged.set_active(treemodel.get_value(row, 79))
        self.txtYearMade.set_text(str(treemodel.get_value(row, 87)))

        return False


    def _allocation_widgets_create(self):
        """ Method to create the Allocation widgets. """

        import pango

        # Widgets to display allocation results.
        model = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_STRING, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
        self.tvwAllocation.set_model(model)
        self.tvwAllocation.set_tooltip_text(_("Displays the list of immediate child assemblies that may be included in the allocation."))

        cols = int(len(self._al_header_labels))
        for i in range(cols):
            if(i == 3):
                cell = gtk.CellRendererToggle()
                cell.set_property('activatable', 1)
                cell.connect('toggled', self._allocation_tree_edit, None, i,
                             model)
            else:
                cell = gtk.CellRendererText()
                cell.set_property('editable', 1)
                cell.set_property('wrap-width', 250)
                cell.set_property('wrap-mode', pango.WRAP_WORD)
                cell.set_property('background', 'white')
                cell.set_property('foreground', 'black')
                cell.connect('edited', self._allocation_tree_edit, i, model)

            column = gtk.TreeViewColumn()
            column.pack_start(cell, True)
            if(i == 3):
                column.set_attributes(cell, active=i)
            else:
                column.set_attributes(cell, text=i)

            column.set_visible(0)

            label = gtk.Label(column.get_title())
            label.set_line_wrap(True)
            text = "<span weight='bold'>%s</span>" % self._al_header_labels[i]
            label.set_markup(text)
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.show_all()
            column.set_widget(label)

            self.tvwAllocation.append_column(column)

        self.tvwAllocation.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

# Widgets to display allocation inputs and methods.
        types = [[_("Reliability"), 0], [_("MTTF/MTBF"), 1],
                 [_("Failure Intensity"), 2]]
        _widg.load_combo(self.cmbRqmtType, types)
        self.cmbRqmtType.connect('changed', self._callback_combo, 500)
        self.cmbRqmtType.set_tooltip_text(_("Selects the reliability goal measure for the active revision."))

        self.txtReliabilityGoal.props.editable = 0
        self.txtReliabilityGoal.set_sensitive(0)
        self.txtReliabilityGoal.connect('focus-out-event', self._callback_entry,
                                        'float', 500)
        self.txtReliabilityGoal.set_tooltip_text(_("Displays the reliability goal value for the active revision.  Editable if reliability goal measure is Reliability."))

        self.txtMTBFGoal.props.editable = 0
        self.txtMTBFGoal.set_sensitive(0)
        self.txtMTBFGoal.connect('focus-out-event', self._callback_entry,
                                 'float', 501)
        self.txtMTBFGoal.set_tooltip_text(_("Displays the MTBF goal for the active revision.  Editable if reliability goal measure is MTBF."))

        self.txtFailureRateGoal.props.editable = 0
        self.txtFailureRateGoal.set_sensitive(0)
        self.txtFailureRateGoal.connect('focus-out-event', self._callback_entry,
                                        'float', 502)
        self.txtFailureRateGoal.set_tooltip_text(_("Displays the failure intensity goal for the active revision.  Editable if reliability goal measure is Failure Intensity."))

        methods = [[_("Equal Apportionment"), 0],
                   [_("AGREE Apportionment"), 1],
                   [_("ARINC Apportionment"), 2],
                   [_("Feasibility of Objectives"), 3]]
        _widg.load_combo(self.cmbAllocationType, methods)
        self.cmbAllocationType.connect('changed', self._callback_combo, 501)
        self.cmbAllocationType.set_tooltip_text(_("Select the reliability allocation method for the selected assembly."))

        self.txtNumElements.set_tooltip_text(_("Display the total number of sub-systems included in the allocation analysis."))

        self.txtOperTime.set_tooltip_text(_("Enter the operating time over which the allocation is calculated."))

        self.chkApplyResults.set_tooltip_text(_("Sets the hardware's specified failure intensity to use the allocation results."))

        return False

    def _allocation_tab_create(self):
        """
        Method to create the Allocation gtk.Notebook tab and populate it with
        the appropriate widgets.
        """

        hbox = gtk.HBox()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add(self.tvwAllocation)

        frame = _widg.make_frame(_label_=_("Allocation Inputs"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hbox.pack_start(frame)

        fixed = gtk.Fixed()
        #fixed.props.width_request = 250

        frame = _widg.make_frame(_label_=_("Calculations"))
        frame.add(fixed)

        hbox.pack_start(frame, expand=False)

        _lbl_width = 200
        y_pos = 5

        label = _widg.make_label(self._al_tab_labels[0], _lbl_width, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbRqmtType, _lbl_width + 5, y_pos)
        y_pos += 35

        label = _widg.make_label(self._al_tab_labels[1], _lbl_width, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtReliabilityGoal, _lbl_width + 5, y_pos)
        y_pos += 30

        label = _widg.make_label(self._al_tab_labels[2], _lbl_width, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtMTBFGoal, _lbl_width + 5, y_pos)
        y_pos += 30

        label = _widg.make_label(self._al_tab_labels[3], _lbl_width, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtFailureRateGoal, _lbl_width + 5, y_pos)
        y_pos += 30

        label = _widg.make_label(self._al_tab_labels[4], _lbl_width, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbAllocationType, _lbl_width + 5, y_pos)
        y_pos += 35

        label = _widg.make_label(self._al_tab_labels[5], _lbl_width, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtNumElements, _lbl_width + 5, y_pos)
        y_pos += 30

        label = _widg.make_label(self._al_tab_labels[6], _lbl_width, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtOperTime, _lbl_width + 5, y_pos)
        y_pos += 30

        fixed.put(self.chkApplyResults, 5, y_pos)
        y_pos += 45

        fixed.show_all()

# Insert the tab.
        label = gtk.Label()
        _heading = _("Allocation")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays reliability allocation calculations for the selected Assembly."))

        self.notebook.insert_page(hbox,
                                  tab_label=label,
                                  position=-1)

        return False

    def _allocation_tab_load(self):
        """
        Loads the widgets with allocation information about the ASSEMBLY
        Object.
        """

        model = self._app.HARDWARE.model
        row = self._app.HARDWARE.selected_row

        if(_conf.RTK_MODULES[0] == 1):
            _values = (model.get_string_from_iter(row),
                      self._app.REVISION.revision_id)
        else:
            _values = (model.get_string_from_iter(row), 0)

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        # Get mission time from the HARDWARE gtk.TreeView
        self.cmbAllocationType.set_active(model.get_value(row, 3))
        self.txtOperTime.set_text(str('{0:0.2f}'.format(model.get_value(row, 45))))

        _query = "SELECT t1.fld_revision_id, t1.fld_assembly_id, \
                         t2.fld_name, t1.fld_included, \
                         t1.fld_n_sub_systems, t1.fld_n_sub_elements, \
                         t2.fld_mission_time, t2.fld_duty_cycle, \
                         t1.fld_int_factor, t1.fld_soa_factor, \
                         t1.fld_op_time_factor, t1.fld_env_factor, \
                         t1.fld_weight_factor, t1.fld_percent_wt_factor, \
                         t2.fld_failure_rate_predicted, \
                         t1.fld_failure_rate_alloc, \
                         t2.fld_mtbf_predicted, \
                         t1.fld_mtbf_alloc, \
                         t2.fld_reliability_predicted, \
                         t1.fld_reliability_alloc, \
                         t2.fld_availability, \
                         t1.fld_availability_alloc \
                 FROM tbl_allocation AS t1 \
                 INNER JOIN tbl_system AS t2 \
                 ON t1.fld_revision_id=t2.fld_revision_id \
                 AND t1.fld_assembly_id=t2.fld_assembly_id \
                 WHERE t2.fld_parent_assembly='%s' \
                 AND t1.fld_revision_id=%d" % _values
        results = self._app.DB.execute_query(_query,
                                             None,
                                             self._app.ProgCnx)

        if(_conf.RTK_MODULES[0] == 1):
            _values = (self.assembly_id, self._app.REVISION.revision_id)
        else:
            _values = (self.assembly_id, 0)

        _query = "SELECT fld_reliability_goal_measure, \
                         fld_reliability_goal \
                  FROM tbl_system \
                  WHERE fld_assembly_id=%d \
                  AND fld_revision_id=%d" % _values
        goal = self._app.DB.execute_query(_query,
                                          None,
                                          self._app.ProgCnx)

        if(results == ''):
            return True

        n_records = len(results)

        # Load the allocation gtk.TreeView
        model = self.tvwAllocation.get_model()
        model.clear()
        for i in range(n_records):
            row = model.append(None, results[i])

        root = model.get_iter_root()
        if root is not None:
            path = model.get_path(root)
            self.tvwAllocation.expand_all()
            self.tvwAllocation.set_cursor('0', None, False)
            col = self.tvwAllocation.get_column(0)
            self.tvwAllocation.row_activated(path, col)

        # Set the reliability requirement widgets.
        self.cmbRqmtType.set_active(goal[0][0])
        if(goal[0][0] == 1):                # Reliability goal
            self.txtReliabilityGoal.set_text(str(fmt.format(goal[0][1])))

            (MTBF, FR) = self._calculate_goals(500)

            self.txtMTBFGoal.set_text(str(fmt.format(MTBF)))
            self.txtFailureRateGoal.set_text(str(fmt.format(FR)))

        elif(goal[0][0] == 2):              # MTBF goal
            self.txtMTBFGoal.set_text(str(fmt.format(goal[0][1])))

            (Reliability, FR) = self._calculate_goals(501)

            self.txtReliabilityGoal.set_text(str(fmt.format(Reliability)))
            self.txtFailureRateGoal.set_text(str(fmt.format(FR)))

        elif(goal[0][0] == 3):              # Failure rate goal
            self.txtFailureRateGoal.set_text(str(fmt.format(goal[0][1])))

            (Reliability, MTBF) = self._calculate_goals(502)

            self.txtReliabilityGoal.set_text(str(fmt.format(Reliability)))
            self.txtMTBFGoal.set_text(str(fmt.format(MTBF)))

        return False

    def _risk_analysis_widgets_create(self):
        """ Method to create the Risk Analysis widgets. """

        import pango
        from lxml import etree

# Retrieve the user-defined column heading text from the format file.
        path = "/root/tree[@name='Risk']/column/usertitle"
        heading = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(path)

# Retrieve the column datatype from the format file.
        path = "/root/tree[@name='Risk']/column/datatype"
        datatype = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(path)

# Retrieve the cellrenderer type from the format file.
        path = "/root/tree[@name='Risk']/column/widget"
        widget = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(path)

# Retrieve the column position from the format file.
        path = "/root/tree[@name='Risk']/column/position"
        position = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(path)

# Retrieve whether or not the column is editable from the format file.
        path = "/root/tree[@name='Risk']/column/editable"
        editable = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(path)

# Retrieve whether or not the column is visible from the format file.
        path = "/root/tree[@name='Risk']/column/visible"
        visible = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(path)

# Create a list of GObject datatypes to pass to the model.
        types = []
        for i in range(len(position)):
            types.append(datatype[i].text)

        gobject_types = []
        gobject_types = [gobject.type_from_name(types[ix])
            for ix in range(len(types))]

# Retrieve the list of hazards to include in the risk analysis worksheet.
        query = "SELECT fld_category, \
                        fld_subcategory \
                 FROM tbl_hazards"
        _hazard_ = self._app.COMDB.execute_query(query,
                                                 None,
                                                 self._app.ComCnx)

# Retrieve the list of hazard severities to include in the risk analysis
# worksheet.
        _query_ = "SELECT fld_criticality_name, fld_criticality_value \
                   FROM tbl_criticality \
                   ORDER BY fld_criticality_value DESC"
        _severity_ = self._app.COMDB.execute_query(_query_,
                                                   None,
                                                   self._app.ComCnx)

# Retrieve the list of hazard probabilities to include in the risk analysis
# worksheet.
        _query_ = "SELECT fld_probability_name, fld_probability_value \
                   FROM tbl_failure_probability"
        _probability_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)

        bg_color = _conf.RTK_COLORS[6]
        fg_color = _conf.RTK_COLORS[7]

# Create the model and treeview for the risk analysis worksheet.
        model = gtk.TreeStore(*gobject_types)
        self.tvwRisk.set_model(model)

        cols = int(len(heading))
        _visible = False
        for i in range(cols):
            self._risk_col_order.append(int(position[i].text))

            if(widget[i].text == 'combo'):
                cell = gtk.CellRendererCombo()
                cellmodel = gtk.ListStore(gobject.TYPE_STRING)

                cellmodel.append([""])
                if(i == 3):
                    for j in range(len(_hazard_)):
                        cellmodel.append([_hazard_[j][0] + ", " + _hazard_[j][1]])
                elif(i == 6 or i == 10 or i == 14 or i == 18):
                    for j in range(len(_severity_)):
                        cellmodel.append([_severity_[j][0]])
                elif(i == 7 or i == 11 or i == 15 or i == 19):
                    for j in range(len(_probability_)):
                        cellmodel.append([_probability_[j][0]])

                cell.set_property('has-entry', False)   # Prevent users from adding new values.
                cell.set_property('model', cellmodel)
                cell.set_property('text-column', 0)
                cell.connect('changed', self._callback_combo_cell,
                             int(position[i].text), model, cols)
            elif(widget[i].text == 'spin'):
                cell = gtk.CellRendererSpin()
                adjustment = gtk.Adjustment(upper=5.0, step_incr=0.05)
                cell.set_property('adjustment', adjustment)
                cell.set_property('digits', 2)
            else:
                cell = gtk.CellRendererText()

            cell.set_property('editable', int(editable[i].text))
            if(int(editable[i].text) == 0):
                cell.set_property('background', 'light gray')
            else:
                cell.set_property('background', bg_color)
                cell.set_property('foreground', fg_color)
                cell.set_property('wrap-width', 250)
                cell.set_property('wrap-mode', pango.WRAP_WORD)
                cell.connect('edited', _widg.edit_tree, int(position[i].text),
                             model)

            label = gtk.Label()
            label.set_line_wrap(True)
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            _text = heading[i].text.replace("  ", "\n")
            label.set_markup("<span weight='bold'>" + _text + "</span>")
            label.set_use_markup(True)
            label.show_all()

            column = gtk.TreeViewColumn()
            column.set_visible(int(visible[i].text))
            column.pack_start(cell, True)
            column.set_attributes(cell, text=int(position[i].text))

            column.set_widget(label)

            column.set_cell_data_func(cell, _widg.format_cell,
                                      (int(position[i].text),
                                      datatype[i].text))
            column.set_resizable(True)
            column.connect('notify::width', _widg.resize_wrap, cell)

            if(i > 0):
                column.set_reorderable(True)

            self.tvwRisk.append_column(column)

        self.tvwRisk.set_tooltip_text(_(u"Displays the risk analysis for the selected Assembly."))
        self.tvwRisk.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

# Create the gtk.TreeModel() and gtk.TreeView() for the risk matrix.
#
# Index     Information
#   0       Criticality category
#   1       Criticality value
#   2       Count of probability 1      (index 5, 8, 11, etc.)
#   3       Value of probability 1      (index 6, 9, 12, etc.)
#   4       Cell background color code  (index 7, 10, 13, etc.)
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_STRING,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_STRING,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_STRING,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_STRING,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_STRING)
        self.tvwRiskMap.set_model(model)

        label = gtk.Label()
        label.set_line_wrap(True)
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_LEFT)
        _text_ = u"\t\tProbability\nSeverity"
        label.set_markup("<span weight='bold'>" + _text_ + "</span>")
        label.set_use_markup(True)
        label.show_all()

        column = gtk.TreeViewColumn()
        column.set_widget(label)
        column.set_visible(True)
        cell = gtk.CellRendererText()       # Severity noun name.
        cell.set_property('visible', True)
        cell.set_property('editable', False)
        cell.set_property('background', 'light gray')
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        cell = gtk.CellRendererText()       # Severity multiplier.
        cell.set_property('visible', False)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=1)
        self.tvwRiskMap.append_column(column)

        _width_ = int(column.get_property('width'))

        j = 2
        _prob_ = []
        for i in range(len(_probability_)):
            label = gtk.Label()
            label.set_line_wrap(True)
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            _text_ = _probability_[i][0]
            _text_ = _text_.replace(" ", "\n")
            label.set_markup("<span weight='bold'>" + _text_ + "</span>")
            label.set_use_markup(True)
            label.show_all()

            column = gtk.TreeViewColumn()
            column.set_widget(label)
            column.set_visible(True)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
            cell = gtk.CellRendererText()       # Quantity of hazards in cell.
            cell.set_property('visible', True)
            cell.set_property('xalign', 0.5)
            cell.set_property('yalign', 0.5)
            column.pack_start(cell, True)
            column.set_attributes(cell, text=j, background=j+2)
            cell = gtk.CellRendererText()       # Frequency multiplier.
            cell.set_property('visible', False)
            column.pack_start(cell, True)
            column.set_attributes(cell, text=j+1)
            cell = gtk.CellRendererText()       # Cell background color.
            cell.set_property('visible', False)
            column.pack_start(cell, True)
            column.set_attributes(cell, text=j+2)
            self.tvwRiskMap.append_column(column)

            j += 3

        column = gtk.TreeViewColumn()
        column.set_visible(True)
        self.tvwRiskMap.append_column(column)

        for i in range(len(_severity_)):
            self._assembly_risks_[_severity_[i][0]] = [_severity_[i][1]]
            self._system_risks_[_severity_[i][0]] = [_severity_[i][1]]
            _data_ = [_severity_[i][0], self._assembly_risks_[_severity_[i][0]][0]]
            _prob_ = {}
            for j in range(len(_probability_)):
                _risk_ = _severity_[i][1] * _probability_[j][1]
                if(_risk_ <= _conf.RTK_RISK_POINTS[0]):
                    _color_ = '#90EE90'     # Green
                elif(_risk_ > _conf.RTK_RISK_POINTS[0] and
                     _risk_ <= _conf.RTK_RISK_POINTS[1]):
                    _color_ = '#FFFF79'     # Yellow
                else:
                    _color_ = '#FFC0CB'     # Red

                _prob_[_probability_[j][0]] = [0, _probability_[j][1], _color_]
                _data_.append(0)
                _data_.append(_probability_[j][1])
                _data_.append(_color_)

            self._assembly_risks_[_severity_[i][0]].append(_prob_)
            self._system_risks_[_severity_[i][0]].append(_prob_)
            model.append(_data_)

        self.tvwRiskMap.set_size_request(575, -1)
        self.tvwRiskMap.set_tooltip_text(_(u"Displays the risk matrix for the selected Assembly."))
        self.tvwRiskMap.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        return False

    def _risk_analysis_tab_create(self):
        """
        Method to create the Risk Analysis gtk.Notebook tab and
        populate it with the appropriate widgets.
        """

        hpaned = gtk.HPaned()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add(self.tvwRisk)

        frame = _widg.make_frame()
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hpaned.pack1(frame, resize=True, shrink=False)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add(self.tvwRiskMap)

        frame = _widg.make_frame()
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hpaned.pack2(frame, resize=False, shrink=True)

        label = gtk.Label()
        _heading = _(u"Hazard\nAnalysis")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Displays the hazards analysis for the selected Assembly."))

        self.notebook.insert_page(hpaned,
                                  tab_label=label,
                                  position=-1)

        return False

    def _risk_analysis_tab_load(self):
        """
        Loads the similar items analysis worksheet with information for the
        selected assembly's children.
        """

        if self._app.HARDWARE.selected_row is not None:
            _model_ = self._app.HARDWARE.model
            _row_ = self._app.HARDWARE.selected_row
            _path_ = _model_.get_string_from_iter(_row_)

        if(_conf.RTK_MODULES[0] == 1):
            _values_ = (self._app.REVISION.revision_id, _path_)
        else:
            _values_ = (0, _path_)

        _query_ = "SELECT t1.fld_risk_id, \
                          t2.fld_name, \
                          t2.fld_failure_rate_predicted, \
                          t1.fld_potential_hazard, \
                          t1.fld_potential_cause, \
                          t1.fld_assembly_effect, \
                          t1.fld_assembly_severity, \
                          t1.fld_assembly_probability, \
                          t1.fld_assembly_hri, \
                          t1.fld_assembly_mitigation, \
                          t1.fld_assembly_severity_f, \
                          t1.fld_assembly_probability_f, \
                          t1.fld_assembly_hri_f, \
                          t1.fld_system_effect, \
                          t1.fld_system_severity, \
                          t1.fld_system_probability, \
                          t1.fld_system_hri, \
                          t1.fld_system_mitigation, \
                          t1.fld_system_severity_f, \
                          t1.fld_system_probability_f, \
                          t1.fld_system_hri_f, \
                          t1.fld_remarks, \
                          t1.fld_function_1, \
                          t1.fld_function_2, \
                          t1.fld_function_3, \
                          t1.fld_function_4, \
                          t1.fld_function_5, \
                          t1.fld_result_1, \
                          t1.fld_result_2, \
                          t1.fld_result_3, \
                          t1.fld_result_4, \
                          t1.fld_result_5, \
                          t1.fld_user_blob_1, \
                          t1.fld_user_blob_2, \
                          t1.fld_user_blob_3, \
                          t1.fld_user_float_1, \
                          t1.fld_user_float_2, \
                          t1.fld_user_float_3, \
                          t1.fld_user_int_1, \
                          t1.fld_user_int_2, \
                          t1.fld_user_int_3 \
                   FROM tbl_risk_analysis AS t1 \
                   INNER JOIN tbl_system AS t2 \
                   ON t2.fld_assembly_id=t1.fld_assembly_id \
                   WHERE t1.fld_revision_id=%d \
                   AND t2.fld_parent_assembly='%s'" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if(not _results_ or len(_results_) == 0):
            _query_ = "SELECT t1.fld_risk_id, \
                              t2.fld_name, \
                              t2.fld_failure_rate_predicted, \
                              t1.fld_potential_hazard, \
                              t1.fld_potential_cause, \
                              t1.fld_assembly_effect, \
                              t1.fld_assembly_severity, \
                              t1.fld_assembly_probability, \
                              t1.fld_assembly_hri, \
                              t1.fld_assembly_mitigation, \
                              t1.fld_assembly_severity_f, \
                              t1.fld_assembly_probability_f, \
                              t1.fld_assembly_hri_f, \
                              t1.fld_system_effect, \
                              t1.fld_system_severity, \
                              t1.fld_system_probability, \
                              t1.fld_system_hri, \
                              t1.fld_system_mitigation, \
                              t1.fld_system_severity_f, \
                              t1.fld_system_probability_f, \
                              t1.fld_system_hri_f, \
                              t1.fld_remarks, \
                              t1.fld_function_1, \
                              t1.fld_function_2, \
                              t1.fld_function_3, \
                              t1.fld_function_4, \
                              t1.fld_function_5, \
                              t1.fld_result_1, \
                              t1.fld_result_2, \
                              t1.fld_result_3, \
                              t1.fld_result_4, \
                              t1.fld_result_5, \
                              t1.fld_user_blob_1, \
                              t1.fld_user_blob_2, \
                              t1.fld_user_blob_3, \
                              t1.fld_user_float_1, \
                              t1.fld_user_float_2, \
                              t1.fld_user_float_3, \
                              t1.fld_user_int_1, \
                              t1.fld_user_int_2, \
                              t1.fld_user_int_3 \
                       FROM tbl_risk_analysis AS t1 \
                       INNER JOIN tbl_system AS t2 \
                       ON t2.fld_assembly_id=t1.fld_assembly_id \
                       WHERE t1.fld_revision_id=%d \
                       AND t1.fld_assembly_id=%d" % \
                       (self._app.REVISION.revision_id, self.assembly_id)
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

        if(not _results_ or len(_results_) == 0):
            return True

        _model_ = self.tvwRisk.get_model()
        _model_.clear()

        _n_assemblies_ = len(_results_)
        for i in range(_n_assemblies_):
            try:
                _model_.append(None, _results_[i])
            except TypeError:
                pass

# Load the risk matrix.
        _query_ = "SELECT fld_severity_id, fld_probability_id, \
                          fld_hazard_count \
                   FROM tbl_risk_matrix \
                   WHERE fld_revision_id=%d \
                   AND fld_assembly_id=%d" % \
                   (self._app.REVISION.revision_id, self.assembly_id)
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        _model_ = self.tvwRiskMap.get_model()
        #for i in range(len(_results_)):
         #   model.set(row, _results_[i][2])

        return False

    def _similar_item_widgets_create(self):
        """ Method to create the Similar Item Analysis widgets. """

        import pango
        from lxml import etree

        # Create the gtk.TreeView.
        # Retrieve the column heading text from the format file.
        path = "/root/tree[@name='SIA']/column/usertitle"
        heading = etree.parse(_conf.RTK_FORMAT_FILE[8]).xpath(path)

        # Retrieve the column datatype from the format file.
        path = "/root/tree[@name='SIA']/column/datatype"
        datatype = etree.parse(_conf.RTK_FORMAT_FILE[8]).xpath(path)

        # Retrieve the cellrenderer type from the format file.
        path = "/root/tree[@name='SIA']/column/widget"
        widget = etree.parse(_conf.RTK_FORMAT_FILE[8]).xpath(path)

        # Retrieve the column position from the format file.
        path = "/root/tree[@name='SIA']/column/position"
        position = etree.parse(_conf.RTK_FORMAT_FILE[8]).xpath(path)

        # Retrieve whether or not the column is editable from the format file.
        path = "/root/tree[@name='SIA']/column/editable"
        editable = etree.parse(_conf.RTK_FORMAT_FILE[8]).xpath(path)

        # Retrieve whether or not the column is visible from the format file.
        path = "/root/tree[@name='SIA']/column/visible"
        visible = etree.parse(_conf.RTK_FORMAT_FILE[8]).xpath(path)

        # Create a list of GObject datatypes to pass to the model.
        types = []
        for i in range(len(position)):
            types.append(datatype[i].text)

        gobject_types = []
        gobject_types = [gobject.type_from_name(types[ix])
            for ix in range(len(types))]

        bg_color = _conf.RTK_COLORS[6]
        fg_color = _conf.RTK_COLORS[7]

        # Create the model and treeview.
        model = gtk.TreeStore(*gobject_types)
        self.tvwSIA.set_model(model)

        cols = int(len(heading))
        _visible = False
        for i in range(cols):
            self._sia_col_order.append(int(position[i].text))

            if(widget[i].text == 'combo'):
                cell = gtk.CellRendererCombo()
                cellmodel = gtk.ListStore(gobject.TYPE_STRING,
                                          gobject.TYPE_INT)

                for j in range(len(risk_category)):
                    cellmodel.append(risk_category[j])

                cell.set_property('has-entry', False)
                cell.set_property('model', cellmodel)
                cell.set_property('text-column', 0)
                cell.connect('changed', self._callback_combo_cell,
                             int(position[i].text), model, cols)
            elif(widget[i].text == 'spin'):
                cell = gtk.CellRendererSpin()
                adjustment = gtk.Adjustment(upper=5.0, step_incr=0.05)
                cell.set_property('adjustment', adjustment)
                cell.set_property('digits', 2)
            elif(widget[i].text == 'blob'):
                cell = _widg.CellRendererML()
            else:
                cell = gtk.CellRendererText()

            cell.set_property('editable', int(editable[i].text))
            if(int(editable[i].text) == 0):
                cell.set_property('background', 'light gray')
            else:
                cell.set_property('background', bg_color)
                cell.set_property('foreground', fg_color)
                cell.set_property('wrap-width', 250)
                cell.set_property('wrap-mode', pango.WRAP_WORD)
                cell.connect('edited', _widg.edit_tree, int(position[i].text),
                             model)

            label = gtk.Label()
            label.set_line_wrap(True)
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            _text = heading[i].text.replace("  ", "\n")
            label.set_markup("<span weight='bold'>" + _text + "</span>")
            label.set_use_markup(True)
            label.show_all()

            column = gtk.TreeViewColumn()
            column.set_visible(int(visible[i].text))
            column.pack_start(cell, True)
            column.set_attributes(cell, text=int(position[i].text))

            column.set_widget(label)

            column.set_cell_data_func(cell, _widg.format_cell,
                                      (int(position[i].text),
                                      datatype[i].text))
            column.set_resizable(True)
            column.connect('notify::width', _widg.resize_wrap, cell)

            if(i > 0):
                column.set_reorderable(True)

            self.tvwSIA.append_column(column)

        self.tvwSIA.set_tooltip_text(_("Displays the similar items analysis for the selected Assembly."))
        self.tvwSIA.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        return False

    def _similar_item_tab_create(self):
        """
        Method to create the Similar Item Analysis gtk.Notebook tab and
        populate it with the appropriate widgets.
        """

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add(self.tvwSIA)

        frame = _widg.make_frame()
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        label = gtk.Label()
        _heading = _("Similar Item\nAnalysis")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays the similar item analysis for the selected Assembly."))

        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _similar_item_tab_load(self):
        """
        Loads the similar items analysis worksheet with information for the
        selected assembly's children.
        """

        if self._app.HARDWARE.selected_row is not None:
            model = self._app.HARDWARE.model
            row = self._app.HARDWARE.selected_row
            path_ = model.get_string_from_iter(row)

        if(_conf.RTK_MODULES[0] == 1):
            values = (self._app.REVISION.revision_id, path_)
        else:
            values = (0, path_)

        query = "SELECT t1.fld_sia_id, t2.fld_name, \
                        t2.fld_failure_rate_predicted, \
                        t1.fld_change_desc_1, t1.fld_change_factor_1, \
                        t1.fld_change_desc_2, t1.fld_change_factor_2, \
                        t1.fld_change_desc_3, t1.fld_change_factor_3, \
                        t1.fld_change_desc_4, t1.fld_change_factor_4, \
                        t1.fld_change_desc_5, t1.fld_change_factor_5, \
                        t1.fld_change_desc_6, t1.fld_change_factor_6, \
                        t1.fld_change_desc_7, t1.fld_change_factor_7, \
                        t1.fld_change_desc_8, t1.fld_change_factor_8, \
                        t1.fld_function_1, t1.fld_function_2, \
                        t1.fld_function_3, t1.fld_function_4, \
                        t1.fld_function_5, \
                        t1.fld_result_1, t1.fld_result_2, t1.fld_result_3, \
                        t1.fld_result_4, t1.fld_result_5, \
                        t1.fld_user_blob_1, t1.fld_user_blob_2, \
                        t1.fld_user_blob_3, t1.fld_user_float_1, \
                        t1.fld_user_float_2, t1.fld_user_float_3, \
                        t1.fld_user_int_1, t1.fld_user_int_2, \
                        t1.fld_user_int_3 \
                 FROM tbl_similar_item AS t1 \
                 INNER JOIN tbl_system AS t2 \
                 ON t2.fld_assembly_id=t1.fld_assembly_id \
                 WHERE t1.fld_revision_id=%d \
                 AND t2.fld_parent_assembly='%s'" % values
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

        model = self.tvwSIA.get_model()
        model.clear()

        if not results:
            return True

        n_assemblies = len(results)

        for i in range(n_assemblies):
            try:
                row = model.append(None, results[i])
            except TypeError:
                pass

        return False

    def _assessment_inputs_widgets_create(self):
        """ Method to create the Assessment Inputs widgets. """

# Create the left side labels.
        y_pos = 5
        _max1_ = 0
        _max2_ = 0
        _max1_ = _widg.make_labels(self._ai_tab_labels[0],
                                   self.fxdRelInputQuad1,
                                   y_pos)

        _x_pos_ = max(_max1_, _max2_) + 20

# Quadrant 1 (upper left) widgets.  These widgets are used to display
# reliability assessment inputs.
        self.cmbHRType.set_tooltip_text(_(u"Select the method of assessing the failure intensity for the selected assembly."))
        _query_ = "SELECT fld_hr_type_noun FROM tbl_hr_type"
        _results_ = self._app.COMDB.execute_query(_query_,
                                                  None,
                                                  self._app.ComCnx)
        _widg.load_combo(self.cmbHRType, _results_)
        self.cmbHRType.connect('changed', self._callback_combo, 35)

        self.cmbCalcModel.set_tooltip_text(_(u"Select the reliability prediction model for the selected assembly."))
        _query_ = "SELECT fld_model_noun FROM tbl_calculation_model"
        _results_ = self._app.COMDB.execute_query(_query_,
                                                  None,
                                                  self._app.ComCnx)
        _widg.load_combo(self.cmbCalcModel, _results_)
        self.cmbCalcModel.connect('changed', self._callback_combo, 10)

        self.txtSpecifiedHt.set_tooltip_text(_(u"Enter the specified failure intensity for the selected assembly."))
        self.txtSpecifiedHt.connect('focus-out-event',
                                    self._callback_entry, 'float', 34)

        self.txtSpecifiedMTBF.set_tooltip_text(_(u"Enter the specified mean time between failure (MTBF) for the selected assembly."))
        self.txtSpecifiedMTBF.connect('focus-out-event',
                                      self._callback_entry, 'float', 51)

        self.txtSoftwareHt.set_tooltip_text(_(u"Enter the software failure rate for the selected assembly."))
        self.txtSoftwareHt.connect('focus-out-event',
                                   self._callback_entry, 'float', 33)

        self.txtAddAdj.set_tooltip_text(_(u"Enter any reliability assessment additive adjustment factor for the selected assembly."))
        self.txtAddAdj.connect('focus-out-event',
                               self._callback_entry, 'float', 2)

        self.txtMultAdj.set_tooltip_text(_(u"Enter any reliability assessment multiplicative adjustment factor for the selected assembly."))
        self.txtMultAdj.connect('focus-out-event',
                                self._callback_entry, 'float', 57)

        self.txtAllocationWF.set_tooltip_text(_(u"Enter the reliability allocation weighting factor for the selected assembly."))
        self.txtAllocationWF.connect('focus-out-event',
                                     self._callback_entry, 'float', 3)

        self.cmbFailDist.set_tooltip_text(_(u"Select the distribution of times to failure for the selected assembly."))
        _query_ = "SELECT fld_distribution_noun FROM tbl_distributions"
        _results_ = self._app.COMDB.execute_query(_query_,
                                                  None,
                                                  self._app.ComCnx)
        _widg.load_combo(self.cmbFailDist, _results_)
        self.cmbFailDist.connect('changed', self._callback_combo, 24)

        self.txtFailScale.set_tooltip_text(_(u"Enter the time to failure distribution scale factor."))
        self.txtFailScale.connect('focus-out-event',
                                  self._callback_entry, 'float', 25)

        self.txtFailShape.set_tooltip_text(_(u"Enter the time to failure distribution shape factor."))
        self.txtFailShape.connect('focus-out-event',
                                  self._callback_entry, 'float', 26)

        self.txtFailLoc.set_tooltip_text(_(u"Enter the time to failure distribution location factor."))
        self.txtFailLoc.connect('focus-out-event',
                                self._callback_entry, 'float', 27)

        self.cmbActEnviron.set_tooltip_text(_(u"Select the active operating environment for the selected assembly."))
        self.cmbActEnviron.connect('changed', self._callback_combo, 22)
        _query_ = "SELECT fld_active_environ_code, fld_active_environ_noun \
                   FROM tbl_active_environs"
        _results_ = self._app.COMDB.execute_query(_query_,
                                                  None,
                                                  self._app.ComCnx)
        model = self.cmbActEnviron.get_model()
        model.clear()
        self.cmbActEnviron.append_text('')
        for i in range(len(_results_)):
            self.cmbActEnviron.append_text(_results_[i][0] + ' - ' +
                                           _results_[i][1])

        self.txtActTemp.set_tooltip_text(_(u"Enter the active environment operating temperature for the selected assembly."))
        self.txtActTemp.connect('focus-out-event',
                                self._callback_entry, 'float', 80)

        self.cmbDormantEnviron.set_tooltip_text(_(u"Select the dormant environment for the selected assembly."))
        _query_ = "SELECT fld_dormant_environ_noun \
                   FROM tbl_dormant_environs"
        _results_ = self._app.COMDB.execute_query(_query_,
                                                  None,
                                                  self._app.ComCnx)
        _widg.load_combo(self.cmbDormantEnviron, _results_)
        self.cmbDormantEnviron.connect('changed', self._callback_combo, 23)

        self.txtDormantTemp.set_tooltip_text(_(u"Enter the dormant environment temperature for the selected assembly."))
        self.txtDormantTemp.connect('focus-out-event',
                                    self._callback_entry, 'float', 81)

        self.txtDutyCycle.set_tooltip_text(_(u"Enter the operating duty cycle for the selected assembly."))
        self.txtDutyCycle.connect('focus-out-event',
                                  self._callback_entry, 'float', 20)

        self.txtHumidity.set_tooltip_text(_(u"Enter the active environment operating humidity for the selected assembly."))
        self.txtHumidity.connect('focus-out-event',
                                 self._callback_entry, 'float', 37)

        self.txtVibration.set_tooltip_text(_(u"Enter the active environment operating vibration level for the selected assembly."))
        self.txtVibration.connect('focus-out-event',
                                  self._callback_entry, 'float', 84)

        self.txtRPM.set_tooltip_text(_(u"Enter the active environment operating RPM for the selected assembly."))
        self.txtRPM.connect('focus-out-event',
                            self._callback_entry, 'float', 76)

        self.txtWeibullFile.set_tooltip_text(_(u"Enter the URL to a survival analysis file for the selected assembly."))
        self.txtWeibullFile.connect('focus-out-event',
                                    self._callback_entry, 'text', 86)

        # Place the widgets.
        self.fxdRelInputQuad1.put(self.cmbHRType, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.cmbCalcModel, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtSpecifiedHt, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtSpecifiedMTBF, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtSoftwareHt, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtAddAdj, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtMultAdj, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtAllocationWF, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.cmbFailDist, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtFailScale, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtFailShape, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtFailLoc, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.cmbActEnviron, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtActTemp, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.cmbDormantEnviron, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtDormantTemp, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtDutyCycle, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtHumidity, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtVibration, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtRPM, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtWeibullFile, _x_pos_, y_pos)

        self.fxdRelInputQuad1.show_all()

# Create the right side labels.
        y_pos = 5
        _max1_ = 0
        _max2_ = 0
        _max1_ = _widg.make_labels(self._ai_tab_labels[1],
                                   self.fxdRelInputQuad2,
                                   y_pos)
        _max2_ = _widg.make_labels(self._ai_tab_labels[3],
                                   self.fxdRelInputQuad4,
                                   y_pos)

        _x_pos_ = max(_max1_, _max2_) + 20

# Create quadrant 2 (upper right) widgets.
        self.cmbMTTRType.set_tooltip_text(_(u"Select the method of assessing the mean time to repair (MTTR) for the selected assembly."))
        _query_ = "SELECT fld_mttr_type_noun FROM tbl_mttr_type"
        _results_ = self._app.COMDB.execute_query(_query_,
                                                  None,
                                                  self._app.ComCnx)

        _widg.load_combo(self.cmbMTTRType, _results_)
        self.cmbMTTRType.connect('changed', self._callback_combo, 56)

        self.txtSpecifiedMTTR.set_tooltip_text(_(u"Enter the specified mean time to repair (MTTR) for the selected assembly."))
        self.txtSpecifiedMTTR.connect('focus-out-event',
                                      self._callback_entry, 'float', 55)

        self.txtMTTRAddAdj.set_tooltip_text(_(u"Enter any mean time to repair (MTTR) assessment additive adjustment factor for the selected assembly."))
        self.txtMTTRAddAdj.connect('focus-out-event',
                                   self._callback_entry, 'float', 53)

        self.txtMTTRMultAdj.set_tooltip_text(_(u"Enter any mean time to repair (MTTR) assessment multaplicative adjustment factor for the selected assembly."))
        self.txtMTTRMultAdj.connect('focus-out-event',
                                    self._callback_entry, 'float', 54)

        self.cmbRepairDist.set_tooltip_text(_(u"Select the time to repair distribution for the selected assembly."))
        _query_ = "SELECT fld_distribution_noun FROM tbl_distributions"
        _results_ = self._app.COMDB.execute_query(_query_,
                                                  None,
                                                  self._app.ComCnx)
        _widg.load_combo(self.cmbRepairDist, _results_)
        self.cmbRepairDist.connect('changed', self._callback_combo, 72)

        self.txtRepairScale.set_tooltip_text(_(u"Enter the time to repair distribution scale parameter."))
        self.txtRepairScale.connect('focus-out-event',
                                    self._callback_entry, 'float', 73)

        self.txtRepairShape.set_tooltip_text(_(u"Enter the time to repair distribution shape parameter."))
        self.txtRepairShape.connect('focus-out-event',
                                    self._callback_entry, 'float', 74)

        # Place the widgets.
        self.fxdRelInputQuad2.put(self.cmbMTTRType, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad2.put(self.txtSpecifiedMTTR, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad2.put(self.txtMTTRAddAdj, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad2.put(self.txtMTTRMultAdj, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad2.put(self.cmbRepairDist, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad2.put(self.txtRepairScale, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad2.put(self.txtRepairShape, _x_pos_, y_pos)

        self.fxdRelInputQuad2.show_all()

# Create quadrant 4 (lower right) widgets.
        self.cmbCostType.set_tooltip_text(_(u"Select the method for assessing the cost of the selected assembly."))
        _query_ = "SELECT fld_cost_type_noun FROM tbl_cost_type"
        _results_ = self._app.COMDB.execute_query(_query_,
                                                  None,
                                                  self._app.ComCnx)
        _widg.load_combo(self.cmbCostType, _results_)
        self.cmbCostType.connect('changed', self._callback_combo, 16)

        self.txtCost.set_tooltip_text(_(u"Enter the cost of the selected assembly."))
        self.txtCost.connect('focus-out-event',
                             self._callback_entry, 'float', 13)

        # Place teh widgets.
        y_pos = 5
        self.fxdRelInputQuad4.put(self.cmbCostType, _x_pos_, y_pos)
        y_pos += 30
        self.fxdRelInputQuad4.put(self.txtCost, _x_pos_, y_pos)

        self.fxdRelInputQuad4.show_all()

        return False

    def _assessment_inputs_tab_create(self):
        """
        Method to create the Calculation Inputs gtk.Notebook tab and populate
        it with the appropriate widgets.
        """

        hbox = gtk.HBox()

# Populate quadrant 1 (upper left).
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.fxdRelInputQuad1)

        frame = _widg.make_frame(_label_=_(u"Reliability Inputs"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hbox.pack_start(frame)

# Populate quadrant 2 (upper right).
        vbox = gtk.VBox()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.fxdRelInputQuad2)

        frame = _widg.make_frame(_label_=_(u"Maintainability Inputs"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vbox.pack_start(frame)

# Populate quadrant 4 (lower right)
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.fxdRelInputQuad4)

        frame = _widg.make_frame(_label_=_(u"Miscellaneous Inputs"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vbox.pack_start(frame)

        hbox.pack_start(vbox)

        label = gtk.Label()
        _heading = _(u"Assessment\nInputs")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Allows entering reliability, maintainability, and other assessment inputs for the selected assembly."))

        self.notebook.insert_page(hbox,
                                  tab_label=label,
                                  position=-1)

        return False

    def _assessment_inputs_tab_load(self):
        """
        Loads the widgets with calculation input data for the ASSEMBLY Object.
        """

        sys_tree_model = self._app.HARDWARE.model
        sys_tree_row = self._app.HARDWARE.selected_row

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        self.cmbHRType.set_active(int(sys_tree_model.get_value(sys_tree_row, 35)))
        self.cmbCalcModel.set_active(int(sys_tree_model.get_value(sys_tree_row, 10)))
        self.txtSpecifiedHt.set_text(str(fmt.format(sys_tree_model.get_value(sys_tree_row, 34))))
        self.txtSpecifiedMTBF.set_text(str(sys_tree_model.get_value(sys_tree_row, 51)))
        self.txtSoftwareHt.set_text(str(fmt.format(sys_tree_model.get_value(sys_tree_row, 33))))
        self.txtAddAdj.set_text(str(sys_tree_model.get_value(sys_tree_row, 2)))
        self.txtMultAdj.set_text(str(sys_tree_model.get_value(sys_tree_row, 57)))
        self.txtAllocationWF.set_text(str(sys_tree_model.get_value(sys_tree_row, 3)))
        self.cmbFailDist.set_active(int(sys_tree_model.get_value(sys_tree_row, 24)))
        self.txtFailScale.set_text(str(sys_tree_model.get_value(sys_tree_row, 25)))
        self.txtFailShape.set_text(str(sys_tree_model.get_value(sys_tree_row, 26)))
        self.txtFailLoc.set_text(str(sys_tree_model.get_value(sys_tree_row, 27)))
        self.cmbActEnviron.set_active(int(sys_tree_model.get_value(sys_tree_row, 22)))
        self.txtActTemp.set_text(str(sys_tree_model.get_value(sys_tree_row, 80)))
        self.cmbDormantEnviron.set_active(int(sys_tree_model.get_value(sys_tree_row, 23)))
        self.txtDormantTemp.set_text(str(sys_tree_model.get_value(sys_tree_row, 81)))
        self.txtDutyCycle.set_text(str(sys_tree_model.get_value(sys_tree_row, 20)))
        self.txtHumidity.set_text(str(sys_tree_model.get_value(sys_tree_row, 37)))
        self.txtVibration.set_text(str(sys_tree_model.get_value(sys_tree_row, 84)))
        self.txtRPM.set_text(str(sys_tree_model.get_value(sys_tree_row, 76)))
        self.txtWeibullFile.set_text(str(sys_tree_model.get_value(sys_tree_row, 86)))
        self.cmbMTTRType.set_active(int(sys_tree_model.get_value(sys_tree_row, 56)))
        self.txtSpecifiedMTTR.set_text(str(sys_tree_model.get_value(sys_tree_row, 55)))
        self.txtMTTRAddAdj.set_text(str(sys_tree_model.get_value(sys_tree_row, 53)))
        self.txtMTTRMultAdj.set_text(str(sys_tree_model.get_value(sys_tree_row, 54)))
        self.cmbRepairDist.set_active(int(sys_tree_model.get_value(sys_tree_row, 72)))
        self.txtRepairScale.set_text(str(sys_tree_model.get_value(sys_tree_row, 73)))
        self.txtRepairShape.set_text(str(sys_tree_model.get_value(sys_tree_row, 74)))
        self.txtMissionTime.set_text(str('{0:0.2f}'.format(sys_tree_model.get_value(sys_tree_row, 45))))
        self.cmbCostType.set_active(int(sys_tree_model.get_value(sys_tree_row, 16)))
        self.txtCost.set_text(str(locale.currency(sys_tree_model.get_value(sys_tree_row, 13))))

        return False

    def _assessment_results_widgets_create(self):
        """ Method to create the Assessment Results widgets. """

# Create the left side labels.
        y_pos = 5
        _max1_ = 0
        _max2_ = 0
        _max1_ = _widg.make_labels(self._ar_tab_labels[0],
                                   self.fxdCalcResultsQuad1,
                                   y_pos)

        _x_pos_ = max(_max1_, _max2_) + 20

# Create the quadrant 1 (upper left) widgets.
        self.txtActiveHt.set_tooltip_text(_(u"Displays the active failure intensity for the selected assembly."))
        self.txtDormantHt.set_tooltip_text(_(u"Displays the dormant failure intensity for the selected assembly."))
        self.txtSoftwareHt2.set_tooltip_text(_(u"Displays the software failure intensity for the selected assembly."))
        self.txtPredictedHt.set_tooltip_text(_(u"Displays the predicted failure intensity for the selected assembly.  This is the sum of the active, dormant, and software failure intensities."))
        self.txtMissionHt.set_tooltip_text(_(u"Displays the mission failure intensity for the selected assembly."))
        self.txtHtPerCent.set_tooltip_text(_(u"Displays the percent of the total system failure intensity attributable to the selected assembly."))
        self.txtMTBF.set_tooltip_text(_(u"Displays the limiting mean time between failure (MTBF) for the selected assembly."))
        self.txtMissionMTBF.set_tooltip_text(_(u"Displays the mission mean time between failure (MTBF) for the selected assembly."))
        self.txtReliability.set_tooltip_text(_(u"Displays the limiting reliability for the selected assembly."))
        self.txtMissionRt.set_tooltip_text(_(u"Displays the mission reliability for the selected assembly."))

        self.fxdCalcResultsQuad1.put(self.txtActiveHt, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtDormantHt, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtSoftwareHt2, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtPredictedHt, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtMissionHt, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtHtPerCent, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtMTBF, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtMissionMTBF, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtReliability, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtMissionRt, _x_pos_, y_pos)

        self.fxdCalcResultsQuad1.show_all()

# Create the right side labels.
        y_pos = 5
        _max1_ = 0
        _max2_ = 0
        _max1_ = _widg.make_labels(self._ar_tab_labels[1],
                                   self.fxdCalcResultsQuad2,
                                   y_pos)
        _max2_ = _widg.make_labels(self._ar_tab_labels[3],
                                   self.fxdCalcResultsQuad4,
                                   y_pos)

        _x_pos_ = max(_max1_, _max2_) + 20

# Create the quadrant 2 (upper right) widgets.
        self.txtMPMT.set_tooltip_text(_(u"Displays the mean preventive maintenance time (MPMT) for the selected assembly."))
        self.txtMCMT.set_tooltip_text(_(u"Displays the mean corrective maintenance time (MCMT) for the selected assembly."))
        self.txtMTTR.set_tooltip_text(_(u"Displays the mean time to repair (MTTR) for the selected assembly."))
        self.txtMMT.set_tooltip_text(_(u"Displays the mean maintenance time (MMT) for the selected assembly."))
        self.txtAvailability.set_tooltip_text(_(u"Displays the limiting availability for the selected assembly."))
        self.txtMissionAt.set_tooltip_text(_(u"Displays the mission availability for the selected assembly."))

        self.fxdCalcResultsQuad2.put(self.txtMPMT, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad2.put(self.txtMCMT, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad2.put(self.txtMTTR, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad2.put(self.txtMMT, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad2.put(self.txtAvailability, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad2.put(self.txtMissionAt, _x_pos_, y_pos)

        self.fxdCalcResultsQuad2.show_all()

# Create the quadrant 4 (lower right) widgets.
        self.txtTotalCost.set_tooltip_text(_(u"Displays the total cost of the selected assembly."))
        self.txtCostFailure.set_tooltip_text(_(u"Displays the cost per failure of the selected assembly."))
        self.txtCostHour.set_tooltip_text(_(u"Displays the cost per mission hour of the selected assembly."))
        self.txtAssemblyCrit.set_tooltip_text(_(u"Displays the criticality of the selected assembly.  This is calculated by the FMEA."))
        self.txtPartCount.set_tooltip_text(_(u"Displays the total number of components used to construct the selected assembly."))
        self.txtTotalPwr.set_tooltip_text(_(u"Displays the total power of the selected assembly."))

        y_pos = 5
        self.fxdCalcResultsQuad4.put(self.txtTotalCost, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad4.put(self.txtCostFailure, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad4.put(self.txtCostHour, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad4.put(self.txtAssemblyCrit, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad4.put(self.txtPartCount, _x_pos_, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad4.put(self.txtTotalPwr, _x_pos_, y_pos)

        self.fxdCalcResultsQuad4.show_all()

        return False

    def _assessment_results_tab_create(self):
        """
        Method to create the Assessment Results gtk.Notebook tab and
        populate it with the appropriate widgets.
        """

        hbox = gtk.HBox()

# Create quadrant 1 (upper left).
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.fxdCalcResultsQuad1)

        frame = _widg.make_frame(_label_=_(u"Reliability Results"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hbox.pack_start(frame)

# Create quadrant 2 (upper right).
        vbox = gtk.VBox()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.fxdCalcResultsQuad2)

        frame = _widg.make_frame(_label_=_(u"Maintainability Results"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vbox.pack_start(frame)

# Create quadrant 4 (lower right).
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.fxdCalcResultsQuad4)

        frame = _widg.make_frame(_label_=_(u"Miscellaneous Results"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vbox.pack_start(frame)

        hbox.pack_start(vbox)

        label = gtk.Label()
        _heading = _(u"Assessment\nResults")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Displays the results the reliability, maintainability, and other assessments for the selected assembly."))

        self.notebook.insert_page(hbox,
                                  tab_label=label,
                                  position=-1)

        return False

    def assessment_results_tab_load(self):
        """
        Loads the widgets with calculation results for the ASSEMBLY Object.
        """

        sys_tree_model = self._app.HARDWARE.model
        sys_tree_row = self._app.HARDWARE.selected_row

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        self.txtCompRefDes.set_text(sys_tree_model.get_value(sys_tree_row, 12))

        self.txtActiveHt.set_text(str(fmt.format(sys_tree_model.get_value(sys_tree_row, 28))))
        self.txtDormantHt.set_text(str(fmt.format(sys_tree_model.get_value(sys_tree_row, 29))))
        self.txtSoftwareHt2.set_text(str(fmt.format(sys_tree_model.get_value(sys_tree_row, 33))))
        self.txtPredictedHt.set_text(str(fmt.format(sys_tree_model.get_value(sys_tree_row, 32))))
        self.txtMissionHt.set_text(str(fmt.format(sys_tree_model.get_value(sys_tree_row, 30))))
        self.txtHtPerCent.set_text(str(fmt.format(sys_tree_model.get_value(sys_tree_row, 31))))

        self.txtMTBF.set_text(str('{0:0.2f}'.format(sys_tree_model.get_value(sys_tree_row, 50))))
        self.txtMissionMTBF.set_text(str('{0:0.2f}'.format(sys_tree_model.get_value(sys_tree_row, 49))))

        self.txtReliability.set_text(str(fmt.format(sys_tree_model.get_value(sys_tree_row, 70))))
        self.txtMissionRt.set_text(str(fmt.format(sys_tree_model.get_value(sys_tree_row, 69))))

        self.txtMPMT.set_text(str('{0:0.2f}'.format(sys_tree_model.get_value(sys_tree_row, 48))))
        self.txtMCMT.set_text(str('{0:0.2f}'.format(sys_tree_model.get_value(sys_tree_row, 44))))
        self.txtMTTR.set_text(str('{0:0.2f}'.format(sys_tree_model.get_value(sys_tree_row, 52))))
        self.txtMMT.set_text(str('{0:0.2f}'.format(sys_tree_model.get_value(sys_tree_row, 46))))

        self.txtAvailability.set_text(str(fmt.format(sys_tree_model.get_value(sys_tree_row, 7))))
        self.txtMissionAt.set_text(str(fmt.format(sys_tree_model.get_value(sys_tree_row, 8))))

        self.txtTotalCost.set_text(str(locale.currency(sys_tree_model.get_value(sys_tree_row, 13))))
        self.txtCostFailure.set_text(str(locale.currency(sys_tree_model.get_value(sys_tree_row, 14))))
        self.txtCostHour.set_text(str('${0:0.4g}'.format(sys_tree_model.get_value(sys_tree_row, 15))))

        self.txtAssemblyCrit.set_text(str(sys_tree_model.get_value(sys_tree_row, 5)))
        self.txtPartCount.set_text(str(fmt.format(sys_tree_model.get_value(sys_tree_row, 82))))
        self.txtTotalPwr.set_text(str(fmt.format(sys_tree_model.get_value(sys_tree_row, 83))))

        return False

    def _fmeca_tab_create(self):
        """
        Method to create the FMECA gtk.Notebook tab and populate it with the
        appropriate widgets.
        """

        self.tvwFMECA.set_tooltip_text(_(u"Displays the failure mode, effects, and criticality analysis (FMECA) for the selected assembly."))
        self.tvwFMECA.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

# Load the severity classification gtk.CellRendererCombo.
        column = self.tvwFMECA.get_column(self._FMECA_col_order[11])
        cell = column.get_cell_renderers()
        cellmodel = cell[0].get_property('model')
        cellmodel.clear()
        query = "SELECT fld_criticality_id, fld_criticality_name, \
                        fld_criticality_cat \
                 FROM tbl_criticality"
        _results = self._app.COMDB.execute_query(query,
                                              None,
                                              self._app.ComCnx)

        if(_results == '' or not _results or _results is None):
            _util.application_error(_(u"There was a problem loading the failure criticality list in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
        else:
            _phases = len(_results)
            cellmodel.append([""])
            for i in range(_phases):
                cellmodel.append([_results[i][2] + " - " + _results[i][1]])

# Load the qualitative failure probability gtk.CellRendererCombo.
        column = self.tvwFMECA.get_column(self._FMECA_col_order[13])
        cell = column.get_cell_renderers()
        cellmodel = cell[0].get_property('model')
        cellmodel.clear()
        query = "SELECT * FROM tbl_failure_probability"
        _results = self._app.COMDB.execute_query(query,
                                                 None,
                                                 self._app.ComCnx)

        if(_results == '' or not _results or _results is None):
            _util.application_error(_(u"There was a problem loading the failure probability list in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
        else:
            _probs = len(_results)
            cellmodel.append([""])
            for i in range(_probs):
                cellmodel.append([_results[i][1]])

        self.tvwFMECA.connect('cursor_changed',
                              self._fmeca_treeview_row_changed, None, None)
        self.tvwFMECA.connect('row_activated',
                              self._fmeca_treeview_row_changed)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwFMECA)

        frame = _widg.make_frame(_label_=_(u"Failure Mode, Effects, and Criticality Analysis"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hpane = gtk.HPaned()
        hpane.pack1(frame, resize=True, shrink=False)

# Load the RPN severity and RPN severity new gtk.CellRendererCombo.
        column = self.tvwFMECA.get_column(self._FMECA_col_order[20])
        cell = column.get_cell_renderers()
        cellmodel1 = cell[0].get_property('model')
        cellmodel1.clear()
        column = self.tvwFMECA.get_column(self._FMECA_col_order[21])
        cell = column.get_cell_renderers()
        cellmodel2 = cell[0].get_property('model')
        cellmodel2.clear()
        query = "SELECT fld_severity_name \
                 FROM tbl_rpn_severity \
                 WHERE fld_fmeca_type=0"
        _results = self._app.COMDB.execute_query(query,
                                                 None,
                                                 self._app.ComCnx)

        if(_results == '' or not _results or _results is None):
            _util.application_error(_(u"There was a problem loading the RPN Severity list in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
        else:
            _probs = len(_results)
            cellmodel1.append([""])
            cellmodel2.append([""])
            for i in range(_probs):
                self._rpnsev[_results[i][0]] = i
                cellmodel1.append([_results[i][0]])
                cellmodel2.append([_results[i][0]])

# Load the RPN occurrence and RPN ocurrence new gtk.Combo.
        cellmodel1 = self.cmbOccurenceI.get_model()
        cellmodel2 = self.cmbOccurrenceN.get_model()
        cellmodel1.clear()
        cellmodel2.clear()
        query = "SELECT fld_occurrence_name \
                 FROM tbl_rpn_occurrence \
                 WHERE fld_fmeca_type=0"
        _results = self._app.COMDB.execute_query(query,
                                                 None,
                                                 self._app.ComCnx)

        if(_results == '' or not _results or _results is None):
            _util.application_error(_(u"There was a problem loading the RPN Occurrence list in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
        else:
            _probs = len(_results)
            cellmodel1.append([""])
            cellmodel2.append([""])
            for i in range(_probs):
                cellmodel1.append([_results[i][0]])
                cellmodel2.append([_results[i][0]])

# Load the RPN detection and RPN detection new gtk.Combo.
        cellmodel1 = self.cmbDetectionI.get_model()
        cellmodel2 = self.cmbDetectionN.get_model()
        cellmodel1.clear()
        cellmodel2.clear()
        query = "SELECT fld_detection_name \
                 FROM tbl_rpn_detection \
                 WHERE fld_fmeca_type=0"
        _results = self._app.COMDB.execute_query(query,
                                                 None,
                                                 self._app.ComCnx)

        if(_results == '' or not _results or _results is None):
            _util.application_error(_(u"There was a problem loading the RPN Detection list in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
        else:
            _probs = len(_results)
            cellmodel1.append([""])
            cellmodel2.append([""])
            for i in range(_probs):
                cellmodel1.append([_results[i][0]])
                cellmodel2.append([_results[i][0]])

# Load the FMECA control type gtk.Combo.
        self.cmbControlType.append_text("")
        self.cmbControlType.append_text(_(u"Prevention"))
        self.cmbControlType.append_text(_(u"Detection"))

# Load the FMECA action type gtk.Combo.
        query = "SELECT fld_action_name \
                 FROM tbl_action_category"
        _results = self._app.COMDB.execute_query(query,
                                                 None,
                                                 self._app.ComCnx)

        if(_results == '' or not _results or _results is None):
            _util.application_error(_(u"There was a problem loading the action category list in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
        else:
            _actions = len(_results)
            self.cmbActionCategory.append_text("")
            for i in range(_actions):
                self.cmbActionCategory.append_text(_results[i][0])

# Load the FMECA action status gtk.Combo.
        query = "SELECT fld_status_name \
                 FROM tbl_status"
        _results = self._app.COMDB.execute_query(query,
                                                 None,
                                                 self._app.ComCnx)

        if(_results == '' or not _results or _results is None):
            _util.application_error(_(u"There was a problem loading the action status list in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
        else:
            _actions = len(_results)
            self.cmbActionStatus.append_text("")
            for i in range(_actions):
                self.cmbActionStatus.append_text(_results[i][0])

# Load the FMECA user list gtk.Combos.
        query = "SELECT fld_user_lname, fld_user_fname \
                 FROM tbl_users"
        _results = self._app.COMDB.execute_query(query,
                                                 None,
                                                 self._app.ComCnx)

        if(_results == '' or not _results or _results is None):
            _util.application_error(_(u"There was a problem loading the user lists in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
        else:
            _actions = len(_results)
            self.cmbActionResponsible.append_text("")
            self.cmbActionApproved.append_text("")
            self.cmbActionClosed.append_text("")
            for i in range(_actions):
                _user = _results[i][0] + ", " + _results[i][1]
                self.cmbActionResponsible.append_text(_user)
                self.cmbActionApproved.append_text(_user)
                self.cmbActionClosed.append_text(_user)

# Create the detailed information gtk.Fixed widget for failure mode.
        self.chkFCQ2.set_sensitive(False)
        self.chkFCQ3.set_sensitive(True)
        self.optHS.set_active(True)

        y_pos = 5

        self.fxdMode.put(self.chkFCQ1, 5, y_pos)
        y_pos += 60

        self.fxdMode.put(self.txtFCQ1, 5, y_pos)
        y_pos += 80

        self.fxdMode.put(self.chkFCQ2, 5, y_pos)
        y_pos += 60

        self.fxdMode.put(self.txtFCQ2, 5, y_pos)
        y_pos += 80

        self.fxdMode.put(self.chkFCQ3, 5, y_pos)
        y_pos += 60

        self.fxdMode.put(self.txtFCQ3, 5, y_pos)
        y_pos += 80

        self.fxdMode.put(self.optHS, 5, y_pos)
        self.fxdMode.put(self.optES, 205, y_pos)
        y_pos += 30

        self.fxdMode.put(self.optNSH, 5, y_pos)
        self.fxdMode.put(self.optEO, 205, y_pos)

# Create the detailed information gtk.Fixed widget for failure mechanisms.
        _lbl_width = 200
        y_pos = 5

        label = _widg.make_label(_(u"Mechanism ID:"), _lbl_width, 25)
        self.fxdMechanism.put(label, 5, y_pos)
        self.fxdMechanism.put(self.txtMechanismID, _lbl_width + 5, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"Mechanism:"), _lbl_width, 25)
        self.fxdMechanism.put(label, 5, y_pos)
        self.fxdMechanism.put(self.txtMechanismDescription, _lbl_width + 5,
                              y_pos)
        self.txtMechanismDescription.connect('focus-out-event',
                                             self._callback_entry, 'text',
                                             1000)
        y_pos += 55

        label = _widg.make_label(_(u"Occurence:"), _lbl_width, 25)
        self.fxdMechanism.put(label, 5, y_pos)
        self.fxdMechanism.put(self.cmbOccurenceI, _lbl_width + 5, y_pos)
        self.cmbOccurenceI.connect('changed', self._callback_combo, 1001)
        y_pos += 35

        label = _widg.make_label(_(u"Detection:"), _lbl_width, 25)
        self.fxdMechanism.put(label, 5, y_pos)
        self.fxdMechanism.put(self.cmbDetectionI, _lbl_width + 5, y_pos)
        self.cmbDetectionI.connect('changed', self._callback_combo, 1002)
        y_pos += 35

        label = _widg.make_label(_(u"RPN:"), _lbl_width, 25)
        self.fxdMechanism.put(label, 5, y_pos)
        self.fxdMechanism.put(self.txtRPNI, _lbl_width + 5, y_pos)
        y_pos += 55

        label = _widg.make_label(_(u"New Occurence:"), _lbl_width, 25)
        self.fxdMechanism.put(label, 5, y_pos)
        self.fxdMechanism.put(self.cmbOccurrenceN, _lbl_width + 5, y_pos)
        self.cmbOccurrenceN.connect('changed', self._callback_combo, 1004)
        y_pos += 35

        label = _widg.make_label(_(u"New Detection:"), _lbl_width, 25)
        self.fxdMechanism.put(label, 5, y_pos)
        self.fxdMechanism.put(self.cmbDetectionN, _lbl_width + 5, y_pos)
        self.cmbDetectionN.connect('changed', self._callback_combo, 1005)
        y_pos += 35

        label = _widg.make_label(_(u"New RPN:"), _lbl_width + 5, 25)
        self.fxdMechanism.put(label, 5, y_pos)
        self.fxdMechanism.put(self.txtRPNN, _lbl_width + 5, y_pos)

# Create the detailed information gtk.Fixed widget for current controls.
        y_pos = 5

        label = _widg.make_label(_(u"Control ID:"), _lbl_width, 25)
        self.fxdControl.put(label, 5, y_pos)
        self.fxdControl.put(self.txtControlID, _lbl_width + 5, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"Control:"), _lbl_width, 25)
        self.fxdControl.put(label, 5, y_pos)
        self.fxdControl.put(self.txtControlDescription, _lbl_width + 5, y_pos)
        self.txtControlDescription.connect('focus-out-event',
                                           self._callback_entry, 'text',
                                           1000)
        y_pos += 30

        label = _widg.make_label(_(u"Control Type:"), _lbl_width, 25)
        self.fxdControl.put(label, 5, y_pos)
        self.fxdControl.put(self.cmbControlType, _lbl_width + 5, y_pos)
        self.cmbControlType.connect('changed', self._callback_combo, 1001)

# Create the detailed information gtk.Fixed widget for recommended actions.
        y_pos = 5

        label = _widg.make_label(_(u"Action ID:"), 200, 25)
        self.fxdAction.put(label, 5, y_pos)
        self.fxdAction.put(self.txtActionID, 205, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"Recommended Action:"), 200, 25)
        self.fxdAction.put(label, 5, y_pos)
        y_pos += 30
        self.fxdAction.put(self.txtActionRecommended, 5, y_pos)
        self.txtActionRecommended.connect('focus-out-event',
                                          self._callback_entry, 'text', 1000)
        y_pos += 80

        label = _widg.make_label(_(u"Action Category:"), 150, 25)
        self.fxdAction.put(label, 5, y_pos)
        self.fxdAction.put(self.cmbActionCategory, 180, y_pos)
        self.cmbActionCategory.connect('changed', self._callback_combo, 1001)
        y_pos += 35

        label = _widg.make_label(_(u"Action Owner:"), 150, 25)
        self.fxdAction.put(label, 5, y_pos)
        self.fxdAction.put(self.cmbActionResponsible, 180, y_pos)
        self.cmbActionResponsible.connect('changed', self._callback_combo, 1002)
        label = _widg.make_label(_(u"Due Date:"), 125, 25)
        self.fxdAction.put(label, 385, y_pos)
        self.fxdAction.put(self.txtActionDueDate, 515, y_pos)
        self.txtActionDueDate.connect('focus-out-event',
                                      self._callback_entry, 'date', 1003)
        y_pos += 35

        label = _widg.make_label(_(u"Status:"), 150, 25)
        self.fxdAction.put(label, 5, y_pos)
        self.fxdAction.put(self.cmbActionStatus, 180, y_pos)
        self.cmbActionStatus.connect('changed', self._callback_combo, 1004)
        y_pos += 60

        label = _widg.make_label(_(u"Action Taken:"), 150, 25)
        self.fxdAction.put(label, 5, y_pos)
        y_pos += 30

        self.fxdAction.put(self.txtActionTaken, 5, y_pos)
        self.txtActionTaken.connect('focus-out-event',
                                    self._callback_entry, 'text',
                                    1005)
        y_pos += 80

        label = _widg.make_label(_(u"Approved By:"), 150, 25)
        self.fxdAction.put(label, 5, y_pos)
        self.fxdAction.put(self.cmbActionApproved, 180, y_pos)
        self.cmbActionApproved.connect('changed', self._callback_combo, 1006)
        label = _widg.make_label(_(u"Approval Date:"), 125, 25)
        self.fxdAction.put(label, 385, y_pos)
        self.fxdAction.put(self.txtActionApproveDate, 515, y_pos)
        self.txtActionApproveDate.connect('focus-out-event',
                                          self._callback_entry, 'date', 1007)
        y_pos += 35

        label = _widg.make_label(_(u"Closed By:"), 150, 25)
        self.fxdAction.put(label, 5, y_pos)
        self.fxdAction.put(self.cmbActionClosed, 180, y_pos)
        self.cmbActionClosed.connect('changed', self._callback_combo, 1008)
        label = _widg.make_label(_(u"Closure Date:"), 125, 25)
        self.fxdAction.put(label, 385, y_pos)
        self.fxdAction.put(self.txtActionCloseDate, 515,y_pos)
        self.txtActionCloseDate.connect('focus-out-event',
                                        self._callback_entry, 'date', 1009)

        self.fraFMECADetails.set_shadow_type(gtk.SHADOW_ETCHED_IN)

        hpane.pack2(self.fraFMECADetails, resize=False, shrink=False)

        label = gtk.Label()
        _heading = _(u"FMEA/FMECA\nWorksheet")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Failure mode, effects, and criticality analysis (FMECA) for the selected assembly."))

        self.notebook.insert_page(hpane,
                                  tab_label=label,
                                  position=-1)

        return False

    def _fmeca_tab_load(self):
        """ Method to load the FMECA tab information. """

        _bg_color = '#D3D3D3'
        _editable = False

        self._ItemCA = {}

        model = self.tvwFMECA.get_model()
        model.clear()

# Load the mission phase gtk.CellRendererCombo.
        column = self.tvwFMECA.get_column(self._FMECA_col_order[2])
        cell = column.get_cell_renderers()
        cellmodel = cell[0].get_property('model')
        cellmodel.clear()

        query = "SELECT fld_phase_id, fld_phase_name, fld_phase_start, \
                        fld_phase_end \
                 FROM tbl_mission_phase \
                 WHERE fld_mission_id=%d" % 0
        _results = self._app.DB.execute_query(query,
                                              None,
                                              self._app.ProgCnx)

        if(not _results or _results == '' or _results is None):
            _util.application_error(_(u"There was a problem loading the mission phase list in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK program database is corrupt."))
        else:
            _phases = len(_results)
            cellmodel.append([""])
            for i in range(_phases):
                self._mission_phase[_results[i][0]] = float(_results[i][3]) - float(_results[i][2])
                cellmodel.append([_results[i][1]])

# Load the failure modes to the gtk.TreeView.
        query = "SELECT t1.fld_mode_id, t1.fld_mode_description, \
                        t1.fld_mission_phase, t1.fld_local_effect, \
                        t1.fld_next_effect, t1.fld_end_effect, \
                        t1.fld_detection_method, t1.fld_other_indications, \
                        t1.fld_isolation_method, t1.fld_design_provisions, \
                        t1.fld_operator_actions, t1.fld_severity_class, \
                        t1.fld_hazard_rate_source, t1.fld_failure_probability, \
                        t1.fld_effect_probability, t1.fld_mode_ratio, \
                        t1.fld_mode_failure_rate, t1.fld_mode_op_time, \
                        t1.fld_mode_criticality, t1.fld_rpn_severity, \
                        t1.fld_rpn_severity_new, t1.fld_critical_item, \
                        t1.fld_single_point, t1.fld_remarks, \
                        t2.fld_failure_rate_active, t2.fld_assembly_criticality \
                 FROM tbl_fmeca AS t1 \
                 INNER JOIN tbl_system AS t2 \
                 ON t2.fld_assembly_id=t1.fld_assembly_id \
                 WHERE t1.fld_assembly_id=%d \
                 AND t1.fld_function_id=0" % self.assembly_id
        _results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

        if(not _results or _results == ''):
            return True

        _n_modes = len(_results)
        icon = _conf.ICON_DIR + '32x32/mode.png'
        icon = gtk.gdk.pixbuf_new_from_file_at_size(icon, 16, 16)
        for i in range(_n_modes):
            self._CA[_results[i][0]] = [_results[i][14], _results[i][15],
                                        _results[i][24], _results[i][17],
                                        _results[i][11], 0.0, 0.0]
            try:
                self._ItemCA[self.assembly_id].append([_results[i][0],
                                                       _results[i][11], ''])
            except KeyError:
                self._ItemCA[self.assembly_id] = [[_results[i][0],
                                                   _results[i][11], '']]

            data = [_results[i][self._FMECA_col_order[0]],
                    _util.none_to_string(_results[i][self._FMECA_col_order[1]]),
                    _util.none_to_string(_results[i][self._FMECA_col_order[2]]),
                    _util.none_to_string(_results[i][self._FMECA_col_order[3]]),
                    _util.none_to_string(_results[i][self._FMECA_col_order[4]]),
                    _util.none_to_string(_results[i][self._FMECA_col_order[5]]),
                    _util.none_to_string(_results[i][self._FMECA_col_order[6]]),
                    _util.none_to_string(_results[i][self._FMECA_col_order[7]]),
                    _util.none_to_string(_results[i][self._FMECA_col_order[8]]),
                    _util.none_to_string(_results[i][self._FMECA_col_order[9]]),
                    _util.none_to_string(_results[i][self._FMECA_col_order[10]]),
                    _util.none_to_string(_results[i][self._FMECA_col_order[11]]),
                    _util.none_to_string(_results[i][self._FMECA_col_order[12]]),
                    _util.none_to_string(_results[i][self._FMECA_col_order[13]]),
                    _util.none_to_string(_results[i][self._FMECA_col_order[14]]),
                    str(_results[i][self._FMECA_col_order[15]]),
                    str(_results[i][self._FMECA_col_order[16]]),
                    str(_results[i][self._FMECA_col_order[17]]),
                    str(_results[i][self._FMECA_col_order[18]]),
                    _util.none_to_string(_results[i][25]),
                    str(_results[i][self._FMECA_col_order[19]]),
                    str(_results[i][self._FMECA_col_order[20]]),
                    _results[i][self._FMECA_col_order[21]],
                    _results[i][self._FMECA_col_order[22]],
                    _util.none_to_string(_results[i][self._FMECA_col_order[23]]),
                    0, '#FFFFFF', True, icon]

            # Load the FMECA gtk.TreeView with the data.
            try:
                model.append(None, data)
            except TypeError:
                _util.application_error(_(u"Failed to load FMEA/FMECA failure mode %d" % _results[i][2]))
                pass

            # Load the FMECA dictionary with the data.
            self._fmeca[_results[i][self._FMECA_col_order[0]]] = data[1:25]

# Load the failure consequences to the FMECA dictionary.
        query = "SELECT * FROM tbl_failure_consequences \
                 WHERE fld_assembly_id=%d" % self.assembly_id
        _results = self._app.DB.execute_query(query,
                                              None,
                                              self._app.ProgCnx)

        _n_modes = len(_results)
        for i in range(_n_modes):
            self._fmeca[_results[i][1]].append(_results[i][2])
            self._fmeca[_results[i][1]].append(_results[i][3])
            self._fmeca[_results[i][1]].append(_results[i][4])
            self._fmeca[_results[i][1]].append(_results[i][5])
            self._fmeca[_results[i][1]].append(_results[i][6])
            self._fmeca[_results[i][1]].append(_results[i][7])
            self._fmeca[_results[i][1]].append(_results[i][8])
            self._fmeca[_results[i][1]].append(_results[i][9])
            self._fmeca[_results[i][1]].append(_results[i][10])

# Load the failure mechanisms to the gtk.TreeView.
        query = "SELECT t1.fld_assembly_id, t1.fld_mode_id, \
                        t1.fld_mechanism_id, t1.fld_mechanism_description, \
                        t1.fld_rpn_occurrence, t1.fld_rpn_detection, \
                        t1.fld_rpn, t1.fld_rpn_occurrence_new, \
                        t1.fld_rpn_detection_new, t1.fld_rpn_new, \
                        t1.fld_parent, t2.fld_rpn_severity, \
                        t2.fld_rpn_severity_new \
                 FROM tbl_fmeca_mechanisms AS t1 \
                 INNER JOIN tbl_fmeca AS t2 ON t2.fld_mode_id=t1.fld_mode_id \
                 WHERE t1.fld_assembly_id=%d" % self.assembly_id
        _results = self._app.DB.execute_query(query,
                                              None,
                                              self._app.ProgCnx)

        if(not _results or _results == '' or _results is None):
            return True

        _n_mechanisms = len(_results)
        icon = _conf.ICON_DIR + '32x32/mechanism.png'
        icon = gtk.gdk.pixbuf_new_from_file_at_size(icon, 16, 16)
        for i in range(_n_mechanisms):
            _piter = model.get_iter_from_string(_results[i][10])
            self._mechanisms[_results[i][2]] = [_results[i][3], _results[i][4],
                                                _results[i][5], _results[i][6],
                                                _results[i][7], _results[i][8],
                                                _results[i][9], _results[i][10]]
            self._RPN[_results[i][2]] = [self._rpnsev[_results[i][11]],
                                         _results[i][4],
                                         _results[i][5], _results[i][6],
                                         self._rpnsev[_results[i][12]],
                                         _results[i][7],
                                         _results[i][8], _results[i][9]]
            _data = [_results[i][2], _util.none_to_string(_results[i][3]),
                     "", "", "", "", "", "", "", "", "", "", "", "", "",
                     "", "", "", "", "", "", "", 0, 0, "", 1, _bg_color,
                     _editable, icon]

            try:
                model.insert(_piter, i, _data)
            except TypeError:
                _util.application_error(_(u"Failed to load FMEA/FMECA failure mechanism %d" % _results[i][2]))
                pass

# Load the actions to the gtk.TreeView.
        query = "SELECT * FROM tbl_fmeca_actions \
                 WHERE fld_assembly_id=%d" % self.assembly_id

        _results = self._app.DB.execute_query(query,
                                              None,
                                              self._app.ProgCnx)

        if(not _results or _results == '' or _results is None):
            pass
        else:
            _n_actions = len(_results)
            icon = _conf.ICON_DIR + '32x32/action.png'
            icon = gtk.gdk.pixbuf_new_from_file_at_size(icon, 16, 16)
            for i in range(_n_actions):
                _piter = model.get_iter_from_string(_results[i][14])
                self._fmeca_actions[_results[i][3]] = [_results[i][4],
                                                       _results[i][5],
                                                       _results[i][6],
                                                       _results[i][7],
                                                       _results[i][8],
                                                       _results[i][9],
                                                       _results[i][10],
                                                       _results[i][11],
                                                       _results[i][12],
                                                       _results[i][13],
                                                       _results[i][14]]
                _data = [_results[i][3], _util.none_to_string(_results[i][4]),
                         "", "", "", "", "", "", "", "", "", "", "", "", "",
                         "", "", "", "", "", "", "", 0, 0, "", 3, _bg_color,
                         _editable, icon]

                try:
                    model.insert(_piter, i, _data)
                except TypeError:
                    _util.application_error(_(u"Failed to load FMEA/FMECA action %d" % _results[i][3]))
                    pass

# Load the controls to the gtk.TreeView.
        query = "SELECT * FROM tbl_fmeca_controls \
                 WHERE fld_assembly_id=%d" % self.assembly_id

        _results = self._app.DB.execute_query(query,
                                              None,
                                              self._app.ProgCnx)

        if(not _results or _results == '' or _results is None):
            return True
        else:
            _n_controls = len(_results)
            icon = _conf.ICON_DIR + '32x32/control.png'
            icon = gtk.gdk.pixbuf_new_from_file_at_size(icon, 16, 16)
            for i in range(_n_controls):
                try:
                    _piter = model.get_iter_from_string(_results[i][6])
                except ValueError:
                    _piter = None
                self._fmeca_controls[_results[i][3]] = [_results[i][4],
                                                        _results[i][5],
                                                        _results[i][6]]
                _data = [_results[i][3], _util.none_to_string(_results[i][4]),
                         "", "", "", "", "", "", "", "", "", "", "", "", "",
                         "", "", "", "", "", "", "", 0, 0, "", 2, _bg_color,
                         _editable, icon]

                try:
                    model.insert(_piter, i, _data)
                except TypeError:
                    _util.application_error(_(u"Failed to load FMEA/FMECA control %d" % _results[i][3]))
                    pass

# Fully expand the FMECA gtk.TreeView.
        root = model.get_iter_root()
        if root is not None:
            path = model.get_path(root)
            self.tvwFMECA.expand_all()
            col = self.tvwFMECA.get_column(1)
            self.tvwFMECA.set_cursor(path, col, False)
            self.tvwFMECA.row_activated(path, col)

        return False

    def _fmeca_treeview_row_changed(self, treeview, path, column):
        """
        Method to load the correct gtk.Fixed when changing rows in the FMECA
        gtk.TreeView.

        Keyword Arguments:
        treeview -- the ASSEMBLY Object FMECA gtk.TreeView.
        path     -- the actived row gtk.TreeView path.
        column   -- the actived gtk.TreeViewColumn.
        """

# Remove the existing gtk.Fixed widget.
        if(self.fraFMECADetails.get_child() is not None):
            self.fraFMECADetails.remove(self.fraFMECADetails.get_child())

        selection = self.tvwFMECA.get_selection()
        (model, row) = selection.get_selected()

        _fmeca_len = len(self._FMECA_col_order)
        _type = model.get_value(row, _fmeca_len)

        if(_type == 0):                     # Failure mode.
            self.fraFMECADetails.add(self.fxdMode)

            _label = self.fraFMECADetails.get_label_widget()
            _label.set_markup("<span weight='bold'>Failure Mode Consequence</span>")

        elif(_type == 1):                   # Failure mechanism.
            _id = model.get_value(row, 0)
            self.txtMechanismID.set_text(str(_id))
            self.txtMechanismDescription.set_text(model.get_value(row, 1))
            self.cmbOccurenceI.set_active(self._mechanisms[_id][1])
            self.cmbDetectionI.set_active(self._mechanisms[_id][2])
            self.txtRPNI.set_text(str(self._mechanisms[_id][3]))
            self.cmbOccurrenceN.set_active(self._mechanisms[_id][4])
            self.cmbDetectionN.set_active(self._mechanisms[_id][5])
            self.txtRPNN.set_text(str(self._mechanisms[_id][6]))

            self.fraFMECADetails.add(self.fxdMechanism)
            _label = self.fraFMECADetails.get_label_widget()
            _label.set_markup("<span weight='bold'>Failure Mechanism/Cause</span>")

        elif(_type == 2):                   # Control
            _id = model.get_value(row, 0)
            self.txtControlID.set_text(str(_id))
            self.txtControlDescription.set_text(
            _util.none_to_string(self._fmeca_controls[_id][0]))
            self.cmbControlType.set_active(self._fmeca_controls[_id][1])

            self.fraFMECADetails.add(self.fxdControl)
            _label = self.fraFMECADetails.get_label_widget()
            _label.set_markup("<span weight='bold'>Failure Mechanism/Cause Control</span>")

        elif(_type == 3):                   # Action
            _id = model.get_value(row, 0)
            self.txtActionID.set_text(str(_id))
            _buffer = self.txtActionRecommended.get_children()[0].get_children()[0].get_buffer()
            _buffer.set_text(_util.none_to_string(self._fmeca_actions[_id][0]))
            self.cmbActionCategory.set_active(int(self._fmeca_actions[_id][1]))
            self.cmbActionResponsible.set_active(int(self._fmeca_actions[_id][2]))
            _dte = str(datetime.fromordinal(int(self._fmeca_actions[_id][3])).strftime('%Y-%m-%d'))
            self.txtActionDueDate.set_text(_dte)
            self.cmbActionStatus.set_active(int(self._fmeca_actions[_id][4]))
            _buffer = self.txtActionTaken.get_children()[0].get_children()[0].get_buffer()
            _buffer.set_text(_util.none_to_string(self._fmeca_actions[_id][5]))
            self.cmbActionApproved.set_active(int(self._fmeca_actions[_id][6]))
            _dte = str(datetime.fromordinal(int(self._fmeca_actions[_id][7])).strftime('%Y-%m-%d'))
            self.txtActionApproveDate.set_text(_dte)
            self.cmbActionClosed.set_active(int(self._fmeca_actions[_id][8]))
            _dte = str(datetime.fromordinal(int(self._fmeca_actions[_id][9])).strftime('%Y-%m-%d'))
            self.txtActionCloseDate.set_text(_dte)

            self.fraFMECADetails.add(self.fxdAction)
            _label = self.fraFMECADetails.get_label_widget()
            _label.set_markup("<span weight='bold'>Failure Mechanism/Cause Action Details</span>")

        self.fraFMECADetails.show_all()

        return False

    def _safety_significance_widgets_create(self):
        """
        Method to create Safety Significance and Failure Consequence widgets.
        """

        self.chkFSIQ1.set_tooltip_text(_(u""))
        self.chkFSIQ2.set_tooltip_text(_(u""))
        self.chkFSIQ3.set_tooltip_text(_(u""))
        self.chkFSIQ4.set_tooltip_text(_(u""))

        self.txtFSIQ1.set_tooltip_text(_(u"Justification for the answer to safety significance question 1."))
        self.txtFSIQ2.set_tooltip_text(_(u"Justification for the answer to safety significance question 2."))
        self.txtFSIQ3.set_tooltip_text(_(u"Justification for the answer to safety significance question 3."))
        self.txtFSIQ4.set_tooltip_text(_(u"Justification for the answer to safety significance question 4."))

        self.chkFCQ1.set_tooltip_text(_(u""))
        self.chkFCQ2.set_tooltip_text(_(u""))
        self.chkFCQ3.set_tooltip_text(_(u""))

        self.txtFCQ1.set_tooltip_text(_(u"To help determine if the failure is evident, refer to the item description, failure detection method, and compensating provisions on the FMECA worksheet.  The FMECA identifies design features, instruments, or warning lights which make a failure evident to the operator."))
        self.txtFCQ2.set_tooltip_text(_(u"Direct means the failure mode must achieve its effect by itself and not in combination with other failure modes.  Adverse effect means the direct consequences of the failure mode are extremely serious or possibly catastrophic.  The failure mode must impact a function that is not protected by redundancy or protective devices."))
        self.txtFCQ3.set_tooltip_text(_(u"First, analyze the failure mode by itself to determine if it has an adverse effect on operating safety.  Second, if the hidden failure by itself does not have an advese effect on safety, look for a combination of failures that will.  If a combination of failures is identified, list the additional failure in the justification."))

        return False

    def _safety_significance_tab_create(self):
        """
        Method to create the Safety Significance and Failure Consequnce
        gtk.Notebook tab and populate it with the appropriate widgets.
        """

        fixed = gtk.Fixed()

        y_pos = 5

        fixed.put(self.chkFSIQ1, 5, y_pos)
        y_pos += 25

        fixed.put(self.txtFSIQ1, 5, y_pos)
        y_pos += 80

        fixed.put(self.chkSSI, 5, y_pos)

        y_pos = 5

        fixed.put(self.chkFSIQ2, 1015, y_pos)
        y_pos += 25

        fixed.put(self.txtFSIQ2, 1015, y_pos)
        y_pos += 80

        fixed.put(self.chkFSIQ3, 1015, y_pos)
        y_pos += 25

        fixed.put(self.txtFSIQ3, 1015, y_pos)
        y_pos += 80

        fixed.put(self.chkFSIQ4, 1015, y_pos)
        y_pos += 25

        fixed.put(self.txtFSIQ4, 1015, y_pos)
        y_pos += 90

        fixed.put(self.chkFSI, 1015, y_pos)

        frame = _widg.make_frame(_label_=_(u"Safety Significance Determination"))
        frame.add(fixed)

        label = gtk.Label()
        _heading = _(u"Assembly\nSignificance")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Significance determination for the selected assembly."))

        self.notebook.insert_page(frame, tab_label=label, position=-1)

        return False

    def _maintenance_planning_widgets_create(self):
        """ Method to create Maintenance Planning widgets. """

        return False

    def _maintenance_planning_tab_create(self):
        """
        Method to create the Maintenance Planning gtk.Notebook tab and populate
        it with the appropriate widgets.
        """

        hbox = gtk.HBox()

        label = gtk.Label()
        _heading = _(u"Maintenance\nTask Analysis")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Maintenance task analysis for the selected assembly."))

        self.notebook.insert_page(hbox, tab_label=label, position=-1)

        return False

    def assembly_add(self, widget, type_):
        """
        Adds a new Assembly to the Program's database.

        Keyword Arguments:
        widget -- the widget that called this function.
        type_  -- the type of Assembly to add; 0 = sibling, 1 = child.
        """

        if self._app.HARDWARE.ispart:
            _util.application_error(_(u"An assembly can not be added as a child of a component.  Please select an assembly to create a child assembly."))
            return True
        else:
            if(type_ == 0):
                _iter = self._app.HARDWARE.model.iter_parent(self._app.HARDWARE.selected_row)
                try:
                    _parent = self._app.HARDWARE.model.get_string_from_iter(_iter)
                except TypeError:
                    _util.application_error(_(u"An sibling assembly can not be added to the top-level assembly."))
                    return True
                n_new_assembly = _util.add_items(_(u"Sibling Assembly"))
            if(type_ == 1):
                _parent = self._app.HARDWARE.model.get_string_from_iter(self._app.HARDWARE.selected_row)
                n_new_assembly = _util.add_items(_(u"Child Assembly"))

        for i in range(n_new_assembly):

# Create the default description of the assembly.
            _descrip = str(_conf.RTK_PREFIX[4]) + ' ' + \
                       str(_conf.RTK_PREFIX[5])

# Increment the assembly index.
            _conf.RTK_PREFIX[5] = _conf.RTK_PREFIX[5] + 1

# Find the revision ID.
            if(_conf.RTK_MODULES[0] == 1):
                _values = (self._app.REVISION.revision_id,
                           str(_conf.RTK_PROG_INFO[3]),
                           _parent, _descrip)
            else:
                _values = (0, str(_conf.RTK_PROG_INFO[3]),
                           _parent, _descrip)

# First we add the assembly to the system table.  Next we find the the ID of
# the newly inserted assembly.  Finally, we add this new assembly to the
# allocation table, risk analysis table, similar item table, and functional
# matrix table.
            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_system \
                         (fld_revision_id, fld_entered_by, \
                          fld_parent_assembly, fld_description) \
                         VALUES (%d, '%s', '%s', '%s')" % _values
            elif(_conf.BACKEND == 'sqlite3'):
                query = "SELECT MAX(fld_assembly_id) FROM tbl_system"
                assembly_id = self._app.DB.execute_query(query,
                                                         None,
                                                         self._app.ProgCnx)
                assembly_id = assembly_id[0][0] + 1

                _values = _values + (assembly_id,)
                query = "INSERT INTO tbl_system \
                         (fld_revision_id, fld_entered_by, \
                          fld_parent_assembly, fld_description, \
                          fld_assembly_id) \
                         VALUES (%d, '%s', '%s', '%s', %d)" % _values

            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("assembly.py: Failed to add new assembly to system table.")
                return True

            if(_conf.BACKEND == 'mysql'):
                query = "SELECT LAST_INSERT_ID()"
                assembly_id = self._app.DB.execute_query(query,
                                                         None,
                                                         self._app.ProgCnx)
                assembly_id = assembly_id[0][0]

            if(assembly_id == ''):
                self._app.debug_log.error("assembly.py: Failed to retrieve new assembly ID.")
                return True

            if(_conf.RTK_MODULES[0] == 1):
                _values = (self._app.REVISION.revision_id,
                           assembly_id)
            else:
                _values = (0, assembly_id)

            query = "INSERT INTO tbl_allocation \
                     (fld_revision_id, fld_assembly_id) \
                     VALUES (%d, %d)" % _values
            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("assembly.py: Failed to add new assembly to allocation table.")
                return True

            query = "INSERT INTO tbl_risk_analysis \
                     (fld_revision_id, fld_assembly_id) \
                     VALUES (%d, %d)" % _values
            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("assembly.py: Failed to add new assembly to risk analysis table.")
                return True

            _query_ = "INSERT INTO tbl_risk_matrix \
                       (fld_revision_id, fld_assembly_id) \
                       VALUES(%d, %d)" % _values
            results = self._app.DB.execute_query(_query_,
                                                 None,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("assembly.py: Failed to add new assembly to risk matrix table.")
                return True

            query = "INSERT INTO tbl_similar_item \
                     (fld_revision_id, fld_assembly_id) \
                     VALUES (%d, %d)" % _values
            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("assembly.py: Failed to add new assembly to similar items table.")
                return True

            query = "INSERT INTO tbl_functional_matrix \
                     (fld_revision_id, fld_assembly_id) \
                     VALUES(%d, %d)" % _values
            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("assembly.py: Failed to add new assembly to functional matrix table.")
                return True

        self._app.REVISION.load_tree()
        #TODO: Need to find and select the previously selected revision before loading the hardware tree.
        self._app.HARDWARE.load_tree()

        return False

    def assembly_delete(self, menuitem):
        """
        Deletes the currently selected Assembly from the Program's MySQL or
        SQLite3 database.

        Keyword Arguments:
        menuitem -- the gtk.MenuItem that called this function.
        """

        if self._app.HARDWARE.ispart:
            return True

        model = self._app.HARDWARE.model
        row = self._app.HARDWARE.selected_row

        _values = (model.get_string_from_iter(row),)

# First delete all of the children from the system table.
        query = "DELETE FROM tbl_system \
                 WHERE fld_parent_assembly='%s'" % _values
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("assembly.py: Failed to delete assembly from system table.")
            return True

        if(_conf.RTK_MODULES[0] == 1):
            _values = (self._app.REVISION.revision_id, model.get_value(row, 1))
        else:
            _values = (0, model.get_value(row, 1))

# Second delete the parent from the system table, then from the allocation
# table, risk analysis table, similar item table, and functional matrix.
        query = "DELETE FROM tbl_system \
                 WHERE fld_revision_id=%d \
                 AND fld_assembly_id=%d" % _values
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("assembly.py: Failed to delete assembly from system table.")
            return True

        query = "DELETE FROM tbl_allocation \
                 WHERE fld_revision_id=%d \
                 AND fld_assembly_id=%d" % _values
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("assembly.py: Failed to delete assembly from allocation table.")
            return True

        query = "DELETE FROM tbl_risk_analysis \
                 WHERE fld_revision_id=%d \
                 AND fld_assembly_id=%d" % _values
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("assembly.py: Failed to delete assembly from risk analysis table.")
            return True

        _query_ = "DELETE FROM tbl_risk_matrix \
                   WHERE fld_revision_id=%d \
                   AND fld_assembly_id=%d" % _values
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("assembly.py: Failed to delete assembly from risk matrix table.")
            return True

        query = "DELETE FROM tbl_similar_item \
                 WHERE fld_revision_id=%d \
                 AND fld_assembly_id=%d" % _values
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("assembly.py: Failed to delete assembly from similar item table.")
            return True

        query = "DELETE FROM tbl_functional_matrix \
                 WHERE fld_revision_id=%d \
                 AND fld_assembly_id=%d" % _values
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("assembly.py: Failed to delete assembly from functional matrix table.")
            return True

        self._app.REVISION.load_tree()
        #TODO: Need to find and select the previously selected revision before loading the hardware tree.
        self._app.HARDWARE.load_tree()

        return False

    def load_notebook(self):
        """ Method to load the Assembly Object gtk.Notebook. """

        self.system_model = self._app.HARDWARE.model
        self.system_selected_row = self._app.HARDWARE.selected_row

        self.assembly_id = self.system_model.get_value(self.system_selected_row, 1)

        if(self.system_model.get_value(self.system_selected_row, 63) == 1):
            try:
                self._hrmodel = dict(self.system_model.get_value(self.system_selected_row, 88))
            except:
                self._app.user_log.error(_(u"No model dictionary for part %s") % \
                                         self.system_model.get_value(self.system_selected_row, 68))
                self._hrmodel = {}

        self._general_data_tab_load()
        self._allocation_tab_load()
        self._risk_analysis_tab_load()
        self._similar_item_tab_load()
        self._assessment_inputs_tab_load()
        self.assessment_results_tab_load()
        self._fmeca_tab_load()
        #self._maintenance_planning_tab_load()

        if(_conf.METHOD == 'LRM'):
            self._risk_analysis_tab_load()

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxAssembly)

        _title_ = _(u"RTK Work Book: Analyzing %s") % \
                  self._app.HARDWARE.model.get_value(self._app.HARDWARE.selected_row, 58)
        self._app.winWorkBook.set_title(_title_)

        self.notebook.set_current_page(self._selected_tab)
        self._app.winWorkBook.show_all()

        return False

    def _allocate(self):
        """
        Method to allocate reliability of selected assembly to lower level
        assemblies.  Only allocates one indenture level down.
        """

        from math import exp, log

        model = self.tvwAllocation.get_model()
        row = model.get_iter_root()

# Read the requirement inputs.
        Ts = float(self.txtOperTime.get_text())
        Rs = float(self.txtReliabilityGoal.get_text())
        MTBFs = float(self.txtMTBFGoal.get_text())
        lambdas = float(self.txtFailureRateGoal.get_text())

        num_included = 0
        while row is not None:
            if model.get_value(row, 3):
                num_included += 1
            row = model.iter_next(row)

        i = self.cmbAllocationType.get_active()
        if(i == 1):                         # Equal apportionment
            Wi = 1.0 / float(num_included)
            Ri = Rs**Wi
            FRi = -1.0 * log(Ri) / Ts
            try:
                MTBFi = 1.0 / FRi
            except ZeroDivisionError:
                MTBFi = 0.0

            row = model.get_iter_root()
            while row is not None:
                if model.get_value(row, 3):
                    model.set_value(row, 12, Wi)
                    model.set_value(row, 15, FRi)
                    model.set_value(row, 17, MTBFi)
                    model.set_value(row, 19, Ri)

                row = model.iter_next(row)

        elif(i == 2):                       # AGREE apportionment
            row = model.get_iter_root()
            while row is not None:
                if model.get_value(row, 3):
                    DC = float(model.get_value(row, 7))
                    ti = Ts * DC / 100.0
                    wi = float(model.get_value(row, 12))
                    ni = float(model.get_value(row, 5))
                    MTBFi = (num_included * wi * ti) / (-1.0 * ni * log(Rs))
                    FRi = 1.0 / MTBFi
                    Ri = exp(-1.0 * FRi * Ts)
                    model.set_value(row, 6, ti)
                    model.set_value(row, 15, FRi)
                    model.set_value(row, 17, MTBFi)
                    model.set_value(row, 19, Ri)

                row = model.iter_next(row)

        elif(i == 3):                       # ARINC apportionment
# Calculate the current system failure rate.
            FRs = 0.0
            row = model.get_iter_root()
            while row is not None:
                FRs += float(model.get_value(row, 14))
                row = model.iter_next(row)

# Now calculate the allocated values for each sub-system.
            row = model.get_iter_root()
            while row is not None:
                if model.get_value(row, 3):
                    FRi = float(model.get_value(row, 14))
                    try:
                        Wi = FRi / FRs
                    except ZeroDivisionError:
                        Wi = 0.0
                    FRi = Wi * lambdas
                    try:
                        MTBFi = 1.0 / FRi
                    except ZeroDivisionError:
                        MTBFi = 0.0

                Ri = exp(-1.0 * FRi * Ts)
                model.set_value(row, 12, Wi)
                model.set_value(row, 15, FRi)
                model.set_value(row, 17, MTBFi)
                model.set_value(row, 19, Ri)
                row = model.iter_next(row)

        elif(i == 4):                       # Feasibility of Objectives
# First calculate the system falure rate and weighting factor for each
# sub-system.
            Wght = 0.0
            row = model.get_iter_root()
            while row is not None:
                if model.get_value(row, 3):
                    ri1 = model.get_value(row, 8)
                    ri2 = model.get_value(row, 9)
                    ri3 = model.get_value(row, 10)
                    ri4 = model.get_value(row, 11)
                    Wi = ri1 * ri2 * ri3 * ri4
                    Wght += Wi
                    model.set_value(row, 12, Wi)

                row = model.iter_next(row)

            row = model.get_iter_root()
            while row is not None:
                if model.get_value(row, 3):
                    Wi = model.get_value(row, 12)
                    Ci = Wi / Wght
                    FRi = Ci * lambdas
                    try:
                        MTBFi = 1.0 / FRi
                    except ZeroDivisionError:
                        MTBFi = 0.0
                    Ri = exp(-1.0 * FRi * Ts)

                    model.set_value(row, 13, Ci)
                    model.set_value(row, 15, FRi)
                    model.set_value(row, 17, MTBFi)
                    model.set_value(row, 19, Ri)

                row = model.iter_next(row)

        self.txtNumElements.set_text(str(num_included))

        return False

    def _calculate_goals(self, measure=500):
        """
        Calculates the other two reliability metrics from the ASSEMBLY Object
        similar item analysis goal provided.

        Keyword Arguments:
        measure -- the reliability goal measurement:
                   1. Reliability
                   2. MTBF
                   3. Hazard Rate
        """

        from math import exp, log

        op_time = float(self.txtOperTime.get_text())

        if(measure == 500):
            Rg = float(self.txtReliabilityGoal.get_text())
            try:
                MTBFg = -1.0 * op_time / log(Rg)
            except ZeroDivisionError:
                MTBFg = 0.0
            try:
                FRg = 1.0 / MTBFg
            except ZeroDivisionError:
                FRg = 0.0

            return(MTBFg, FRg)

        elif(measure == 501):
            MTBFg = float(self.txtMTBFGoal.get_text())
            try:
                FRg = 1.0 / MTBFg
            except ZeroDivisionError:
                FRg = 0.0
            try:
                Rg = exp(-1.0 * op_time / MTBFg)
            except ZeroDivisionError:
                Rg = 1.0

            return(Rg, FRg)

        elif(measure == 502):
            FRg = float(self.txtFailureRateGoal.get_text())
            try:
                MTBFg = 1.0 / FRg
            except ZeroDivisionError:
                MTBFg = 0.0
            try:
                Rg = exp(-1.0 * op_time / MTBFg)
            except ZeroDivisionError:
                Rg = 1.0

            return(Rg, MTBFg)

    def _calculate_risk(self):
        """ Calculates the Assembly Object risk analysis. """

# Get the list of failure probability names then create a dictionary using
# these probability names as the keys.  The values for each key are a list
# where the list contains:
#
#   Index       Information
#     0         Count of assembly-level combinations before mitigation.
#     1         Count of system-level combinations before mitigation.
#     2         Count of assembly-level combinations after mitigation.
#     3         Count of system-level combinations after mitigation.
#     4         Index in the gtk.TreeView() risk map for the first count.
# {'Probability Name': [Assembly Count, System Count, Assembly Count, System Count, Index]}
        _columns_ = self.tvwRiskMap.get_columns()
        _probs_ = {}
        j = 2
        for i in range(1, len(_columns_)):
            try:
                _text_ = _columns_[i].get_widget().get_text()
                _text_ = _text_.replace('\t', '')
                _text_ = _text_.replace('\n', ' ')
                _probs_[_text_] = [0, 0, 0, 0, j]
                j += 3
            except AttributeError:
                pass

# Get the count of hazard criticality and hazard probability combinations for
# assembly level effects and system level effects.
        _model_ = self.tvwRisk.get_model()
        _row_ = _model_.get_iter_first()
        _keys_ = _probs_.keys()
        while _row_ is not None:
            _assembly_crit_ = _model_.get_value(_row_, 6)
            _assembly_prob_ = _model_.get_value(_row_, 7)
            _assembly_crit_f_ = _model_.get_value(_row_, 10)
            _assembly_prob_f_ = _model_.get_value(_row_, 11)
            _system_crit_ = _model_.get_value(_row_, 14)
            _system_prob_ = _model_.get_value(_row_, 15)
            _system_crit_f_ = _model_.get_value(_row_, 18)
            _system_prob_f_ = _model_.get_value(_row_, 19)

#{'Severity Name': [Severity Value, {'Probability Name': [Count, P Value, Cell Color]}
            # Increment the count of assembly and system severity/probability
            # combinations.
            try:
                _probs_[_assembly_prob_][0] += 1
                _probs_[_system_prob_][1] += 1
            except KeyError:
                pass

            try:
                _c_ = self._assembly_risks_[_assembly_crit_][0]
                _p_ = self._assembly_risks_[_assembly_crit_][1][_assembly_prob_][1]
                _assembly_hri_ = _c_ * _p_
                _c_ = self._assembly_risks_[_assembly_crit_f_][0]
                _p_ = self._assembly_risks_[_assembly_crit_f_][1][_assembly_prob_f_][1]
                _assembly_hri_f_ = _c_ * _p_
            except KeyError:
                _assembly_hri_ = 0
                _assembly_hri_f_ = 0

            try:
                _c_ = self._system_risks_[_system_crit_][0]
                _p_ = self._system_risks_[_system_crit_][1][_system_prob_][1]
                _system_hri_ = _c_ * _p_
                _c_ = self._system_risks_[_system_crit_f_][0]
                _p_ = self._system_risks_[_system_crit_f_][1][_system_prob_f_][1]
                _system_hri_f_ = _c_ * _p_
            except KeyError:
                _system_hri_ = 0
                _system_hri_f_ = 0

            _model_.set_value(_row_, 8, _assembly_hri_)
            _model_.set_value(_row_, 12, _assembly_hri_f_)
            _model_.set_value(_row_, 16, _system_hri_)
            _model_.set_value(_row_, 20, _system_hri_f_)

# Update the count of severity/probability interactions and calculate the
# hazard risk index (HRI) for the assembly and the system.
            for i in range(len(_keys_)):
                try:
                    self._assembly_risks_[_assembly_crit_][1][_keys_[i]][0] = _probs_[_keys_[i]][0]
                except KeyError:
                    pass

                try:
                    self._system_risks_[_system_crit_][1][_keys_[i]][0] = _probs_[_keys_[i]][1]
                except KeyError:
                    pass

            _row_ = _model_.iter_next(_row_)

# Update the counts in the risk matrix gtk.TreeView().
        _model_ = self.tvwRiskMap.get_model()
        _row_ = _model_.get_iter_first()
        while _row_ is not None:
            _crit_ = _model_.get_value(_row_, 0)
            for i in range(len(_keys_)):
                try:
                    _count_ = self._assembly_risks_[_crit_][1][_keys_[i]][0]
                    _idx_ = _probs_[_keys_[i]][4]
                    _model_.set_value(_row_, _idx_, _count_)
                except KeyError:
                    pass

            _row_ = _model_.iter_next(_row_)

# Perform user-defined calculations.
        model = self.tvwRisk.get_model()
        row = model.get_iter_first()
        _calculations_ = {}
        while row is not None:
            #_calculations_['hr_sys'] = model.get_value(row, 2)

# Get the assembly failure intensity.
            _calculations_['hr'] = model.get_value(row, 2)

# Get the user-defined float and integer values.
            _calculations_['uf1'] = float(model.get_value(row, 35))
            _calculations_['uf2'] = float(model.get_value(row, 36))
            _calculations_['uf3'] = float(model.get_value(row, 37))
            _calculations_['ui1'] = float(model.get_value(row, 38))
            _calculations_['ui2'] = float(model.get_value(row, 39))
            _calculations_['ui3'] = float(model.get_value(row, 40))

# Get the user-defined functions.
            _calculations_['equation1'] = model.get_value(row, 22)
            _calculations_['equation2'] = model.get_value(row, 23)
            _calculations_['equation3'] = model.get_value(row, 24)
            _calculations_['equation4'] = model.get_value(row, 25)
            _calculations_['equation5'] = model.get_value(row, 26)

# Get the existing results.  This allows the use of the results fields to be
# manually set to a float values by the user.  Essentially creating five more
# user-defined float values.
            _calculations_['res1'] = model.get_value(row, 27)
            _calculations_['res2'] = model.get_value(row, 28)
            _calculations_['res3'] = model.get_value(row, 29)
            _calculations_['res4'] = model.get_value(row, 30)
            _calculations_['res5'] = model.get_value(row, 31)

            keys = _calculations_.keys()
            values = _calculations_.values()

            for i in range(len(keys)):
                vars()[keys[i]] = values[i]

# If the system failure intensity is greater than zero, perform the remaining
# risk calculations.  If not, notify the user and exit this function.
            #if(_calculations_['hr_sys'] <= 0.0):
            #    _util.application_error(_(u"The System failure intensity is 0.  This will likely cause erroneous results if used in calculations.  You should specify or calculate the System failure intensity before executing risk analysis calculations."))
            #    return True

            try:
                results1 = eval(_calculations_['equation1'])
            except SyntaxError:
                results1 = _calculations_['res1']

            try:
                results2 = eval(_calculations_['equation2'])
            except SyntaxError:
                results2 = _calculations_['res2']

            try:
                results3 = eval(_calculations_['equation3'])
            except SyntaxError:
                results3 = _calculations_['res3']

            try:
                results4 = eval(_calculations_['equation4'])
            except SyntaxError:
                results4 = _calculations_['res4']

            try:
                results5 = eval(_calculations_['equation5'])
            except SyntaxError:
                results5 = _calculations_['res5']

            model.set_value(row, 22, results1)
            model.set_value(row, 23, results2)
            model.set_value(row, 24, results3)
            model.set_value(row, 25, results4)
            model.set_value(row, 26, results5)

            row = model.iter_next(row)

        return False

    def _calculate_sia(self):
        """ Calculates the Assembly Object similar item analysis. """

        model = self.tvwSIA.get_model()
        row = model.get_iter_first()

        while row is not None:
            sia = {}

# Get the assembly failure intensity.
            sia['hr'] = float(model.get_value(row, 2))

# Get the change factor values.
            sia['pi1'] = float(model.get_value(row, 4))
            sia['pi2'] = float(model.get_value(row, 6))
            sia['pi3'] = float(model.get_value(row, 8))
            sia['pi4'] = float(model.get_value(row, 10))
            sia['pi5'] = float(model.get_value(row, 12))
            sia['pi6'] = float(model.get_value(row, 14))
            sia['pi7'] = float(model.get_value(row, 16))
            sia['pi8'] = float(model.get_value(row, 18))

# Get the user-defined float and integer values.
            sia['uf1'] = float(model.get_value(row, 32))
            sia['uf2'] = float(model.get_value(row, 33))
            sia['uf3'] = float(model.get_value(row, 34))
            sia['ui1'] = float(model.get_value(row, 35))
            sia['ui2'] = float(model.get_value(row, 36))
            sia['ui3'] = float(model.get_value(row, 37))

# Get the user-defined functions.
            sia['equation1'] = model.get_value(row, 19)
            sia['equation2'] = model.get_value(row, 20)
            sia['equation3'] = model.get_value(row, 21)
            sia['equation4'] = model.get_value(row, 22)
            sia['equation5'] = model.get_value(row, 23)

# Get the existing results.  This allows the use of the results fields to be
# manually set to a float values by the user.  Essentially creating five more
# user-defined float values.
            sia['res1'] = model.get_value(row, 24)
            sia['res2'] = model.get_value(row, 25)
            sia['res3'] = model.get_value(row, 26)
            sia['res4'] = model.get_value(row, 27)
            sia['res5'] = model.get_value(row, 28)

            keys = sia.keys()
            values = sia.values()

            for i in range(len(keys)):
                vars()[keys[i]] = values[i]

            try:
                results1 = eval(sia['equation1'])
            except SyntaxError:
                results1 = model.get_value(row, 24)

            try:
                results2 = eval(sia['equation2'])
            except SyntaxError:
                results2 = model.get_value(row, 25)

            try:
                results3 = eval(sia['equation3'])
            except SyntaxError:
                results3 = model.get_value(row, 26)

            try:
                results4 = eval(sia['equation4'])
            except SyntaxError:
                results4 = model.get_value(row, 27)

            try:
                results5 = eval(sia['equation5'])
            except SyntaxError:
                results5 = model.get_value(row, 28)

            model.set_value(row, 24, results1)
            model.set_value(row, 25, results2)
            model.set_value(row, 26, results3)
            model.set_value(row, 27, results4)
            model.set_value(row, 28, results5)

            row = model.iter_next(row)

        return False

    def _allocation_save(self):
        """
        Saves the Assembly Object allocation analysis gtkTreeView information
        to the Program's MySQL or SQLite3 database.
        """

# Update the HARDWARE gtk.TreeView with the reliability goals.
        measure = self.cmbRqmtType.get_active()
        if(measure == 1):
            value = float(self.txtReliabilityGoal.get_text())
        elif(measure == 2):
            value = float(self.txtMTBFGoal.get_text())
        elif(measure == 3):
            value = float(self.txtFailureRateGoal.get_text())
        else:
            value = 1.0

# Update the allocation method.
        i = self.cmbAllocationType.get_active()
        model = self._app.HARDWARE.model
        row = self._app.HARDWARE.selected_row
        model.set_value(row, 3, i)
        model.set_value(row, 89, measure)
        model.set_value(row, 90, value)

# Save the results.
        self._app.HARDWARE.hardware_save()

# Save each of the lines in the allocation analysis table.
        model = self.tvwAllocation.get_model()
        model.foreach(self._allocation_save_line_item)

        if(self.chkApplyResults.get_active()):
            self._app.HARDWARE.load_tree()

        return False

    def _allocation_save_line_item(self, model, path_, row):
        """
        Saves each row in the Assembly Object allocation treeview model to the
        MySQL or SQLite3 database.

        Keyword Arguments:
        model -- the Assembly Object allocation gtk.TreeModel.
        path_ -- the path of the active row in the Assembly Object
                 allocation gtk.TreeModel.
        row   -- the selected row in the Assembly Object allocation
                 gtk.TreeView.
        """

        _values = (model.get_value(row, 3), model.get_value(row, 4), \
                   model.get_value(row, 5), model.get_value(row, 12), \
                   model.get_value(row, 13), model.get_value(row, 8), \
                   model.get_value(row, 9), model.get_value(row, 10), \
                   model.get_value(row, 11), model.get_value(row, 21), \
                   model.get_value(row, 19), model.get_value(row, 15), \
                   model.get_value(row, 17), model.get_value(row, 0), \
                   model.get_value(row, 1))

        query = "UPDATE tbl_allocation \
                 SET fld_included=%d, fld_n_sub_systems=%d, \
                     fld_n_sub_elements=%d, fld_weight_factor=%f, \
                     fld_percent_wt_factor=%f, fld_int_factor=%d, \
                     fld_soa_factor=%d, fld_op_time_factor=%d, \
                     fld_env_factor=%d, fld_availability_alloc=%f, \
                     fld_reliability_alloc=%f, fld_failure_rate_alloc=%f, \
                     fld_mtbf_alloc=%f \
                 WHERE fld_revision_id=%d \
                 AND fld_assembly_id=%d" % _values
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

# Trickle down the reliability goals.
        if(self.chkApplyResults.get_active()):

            measure = self.cmbRqmtType.get_active()
            if(measure == 1):           # Expressed as reliability.
                value = model.get_value(row, 19)
            elif(measure == 2):         # Expressed as an MTBF.
                value = model.get_value(row, 17)
            elif(measure == 3):         # Expressed as a failure rate.
                value = model.get_value(row, 15)
            else:
                value = 1.0

            _values = (model.get_value(row, 15), model.get_value(row, 17), 3, \
                       measure, value, model.get_value(row, 0), \
                       model.get_value(row, 1))

            query = "UPDATE tbl_system \
                     SET fld_failure_rate_specified=%f, \
                         fld_mtbf_specified=%f, \
                         fld_failure_rate_type=%d, \
                         fld_reliability_goal_measure=%d, \
                         fld_reliability_goal=%f \
                     WHERE fld_revision_id=%d \
                     AND fld_assembly_id=%d" % _values
            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx,
                                                 commit=True)

        if not results:
            self._app.debug_log.error("assembly.py: Failed to update system table with allocation results.")
            return True

        return False

    def _function_edit(self, _index_):
        """
        Method to edit the Similar Item Analysis functions.

        Keyword Arguments:
        _index_ -- the index indicating whether to edit risk analysis or
                   similar item analysis functions.
                   0 = risk analysis
                   1 = similar item analysis
        """

        if(_index_ == 0):
            selection = self.tvwRisk.get_selection()
            (model, row) = selection.get_selected()
        elif(_index_ == 1):
            selection = self.tvwSIA.get_selection()
            (model, row) = selection.get_selected()

        dialog = _widg.make_dialog(_(u"RTK - Edit Risk Analysis or Similar Item Functions"),
                                   self._app.winWorkBook)

        fixed = gtk.Fixed()

        y_pos = 10

        label = _widg.make_label(_(u"You can define up to five functions using the Risk Analysis or Similar Item data.  You can use the selected assembly hazard rate, change category index, the change factor, the change cost, the user float, the user integer values, and results of other functions.\n\n \
System hazard rate is hr_sys\n \
Assembly hazard rate is hr\n \
Risk category index is cat[1-8]\n \
Change factor is pi[1-8]\n \
Change cost is cost[1-8]\n \
User float is uf[1-3]\n \
User integer is ui[1-3]\n \
Function result is res[1-5]\n\n \
For example, pi1*pi2+pi3, multiplies the first change factors and adds the value to the third change factor."), 600, 350)
        fixed.put(label, 5, y_pos)
        y_pos += 360

        label = _widg.make_label(_(u"User function 1:"))
        txtFunction1 = _widg.make_entry()
        if(_index_ == 0):
            txtFunction1.set_text(model.get_value(row, 35))
        elif(_index_ == 1):
            txtFunction1.set_text(model.get_value(row, 19))

        fixed.put(label, 5, y_pos)
        fixed.put(txtFunction1, 195, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"User function 2:"))
        txtFunction2 = _widg.make_entry()
        if(_index_ == 0):
            txtFunction2.set_text(model.get_value(row, 36))
        elif(_index_ == 1):
            txtFunction2.set_text(model.get_value(row, 20))
        fixed.put(label, 5, y_pos)
        fixed.put(txtFunction2, 195, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"User function 3:"))
        txtFunction3 = _widg.make_entry()
        if(_index_ == 0):
            txtFunction3.set_text(model.get_value(row, 37))
        elif(_index_ == 1):
            txtFunction3.set_text(model.get_value(row, 21))
        fixed.put(label, 5, y_pos)
        fixed.put(txtFunction3, 195, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"User function 4:"))
        txtFunction4 = _widg.make_entry()
        if(_index_ == 0):
            txtFunction4.set_text(model.get_value(row, 38))
        elif(_index_ == 1):
            txtFunction4.set_text(model.get_value(row, 22))
        fixed.put(label, 5, y_pos)
        fixed.put(txtFunction4, 195, y_pos)
        y_pos += 30

        label = _widg.make_label(_(u"User function 5:"))
        txtFunction5 = _widg.make_entry()
        if(_index_ == 0):
            txtFunction5.set_text(model.get_value(row, 39))
        elif(_index_ == 1):
            txtFunction5.set_text(model.get_value(row, 23))
        fixed.put(label, 5, y_pos)
        fixed.put(txtFunction5, 195, y_pos)
        y_pos += 30

        chkApplyAll = gtk.CheckButton(label=_(u"Apply to all assemblies."))
        fixed.put(chkApplyAll, 5, y_pos)

        fixed.show_all()

        dialog.vbox.pack_start(fixed)

        response = dialog.run()

        if(response == gtk.RESPONSE_ACCEPT):
            _func1 = txtFunction1.get_text()
            _func2 = txtFunction2.get_text()
            _func3 = txtFunction3.get_text()
            _func4 = txtFunction4.get_text()
            _func5 = txtFunction5.get_text()
            if(_index_ == 0):
                _cols = [35, 36, 37, 38, 39]
            elif(_index_ == 1):
                _cols = [19, 20, 21, 22, 23]

            if(chkApplyAll.get_active()):
                while row is not None:
                    model.set_value(row, _cols[0], _func1)
                    model.set_value(row, _cols[1], _func2)
                    model.set_value(row, _cols[2], _func3)
                    model.set_value(row, _cols[3], _func4)
                    model.set_value(row, _cols[4], _func5)
                    row = model.iter_next(row)
            else:
                model.set_value(row, _cols[0], _func1)
                model.set_value(row, _cols[1], _func2)
                model.set_value(row, _cols[2], _func3)
                model.set_value(row, _cols[3], _func4)
                model.set_value(row, _cols[4], _func5)

        dialog.destroy()

        return False

    def _sia_rollup(self):
        """
        Rolls-up the lower level similar item analysis change descriptions to
        the selected Assembly Object.
        """

        model = self._app.HARDWARE.model
        row = self._app.HARDWARE.selected_row
        _values = model.get_string_from_iter(row)

# Select all of the lower level element change descriptions for the selected
# assembly.
        query = "SELECT t2.fld_name, t1.fld_change_desc_1, \
                        t1.fld_change_desc_2, t1.fld_change_desc_3, \
                        t1.fld_change_desc_4, t1.fld_change_desc_5, \
                        t1.fld_change_desc_6, t1.fld_change_desc_7, \
                        t1.fld_change_desc_8 \
                 FROM tbl_similar_item AS t1 \
                 INNER JOIN tbl_system AS t2 \
                 ON t1.fld_assembly_id=t2.fld_assembly_id \
                 WHERE t2.fld_parent_assembly='%s'" % _values
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

# Combine the changes descriptions into a single change description for each
# change category.
        summary = ["", "", "", "", "", "", "", ""]
        for i in range(len(results)):
            system = results[i][0]
            for j in range(8):
                if(results[i][j+1] != '' and results[i][j+1] is not None):
                    summary[j] = summary[j] + system + ":\n" + \
                                 results[i][j+1] + "\n"

# Update the selected assembly's change descriptions with the combined change
# description.
        if(_conf.RTK_MODULES[0] == 1):
            _values = (summary[0], summary[1], summary[2], summary[3], \
                       summary[4], summary[5], summary[6], summary[7], \
                       self._app.REVISION.revision_id, self.assembly_id)
        else:
            _values = (summary[0], summary[1], summary[2], summary[3], \
                       summary[4], summary[5], summary[6], summary[7], \
                       0, self.assembly_id)

# Update the database.
        query = "UPDATE tbl_similar_item \
                 SET fld_change_desc_1='%s', fld_change_desc_2='%s', \
                     fld_change_desc_3='%s', fld_change_desc_4='%s', \
                     fld_change_desc_5='%s', fld_change_desc_6='%s', \
                     fld_change_desc_7='%s', fld_change_desc_8='%s' \
                 WHERE fld_revision_id=%d AND fld_assembly_id=%d" % _values
        self._app.DB.execute_query(query,
                                   None,
                                   self._app.ProgCnx,
                                   commit=True)

        return False

    def _risk_rollup(self):
        """
        Rolls-up the lower level risk analysis change descriptions to the
        selected Assembly Object.
        """

        model = self._app.HARDWARE.model
        row = self._app.HARDWARE.selected_row
        _values = model.get_string_from_iter(row)

# Select all of the lower level element change descriptions for the selected
# assembly.
        query = "SELECT t2.fld_name, t1.fld_change_desc_1, \
                        t1.fld_change_desc_2, t1.fld_change_desc_3, \
                        t1.fld_change_desc_4, t1.fld_change_desc_5, \
                        t1.fld_change_desc_6, t1.fld_change_desc_7, \
                        t1.fld_change_desc_8 \
                 FROM tbl_risk_analysis AS t1 \
                 INNER JOIN tbl_system AS t2 \
                 ON t1.fld_assembly_id=t2.fld_assembly_id \
                 WHERE t2.fld_parent_assembly='%s'" % _values
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

# Combine the changes descriptions into a single change description for each
# change category.
        summary = ["", "", "", "", "", "", "", ""]
        for i in range(len(results)):
            system = results[i][0]
            for j in range(8):
                if(results[i][j+1] != '' and results[i][j+1] is not None):
                    summary[j] = summary[j] + system + ":\n" + \
                                 results[i][j+1] + "\n"

# Now find the sums of the five result fields.
        query = "SELECT SUM(t1.fld_result_1), SUM(t1.fld_result_2), \
                        SUM(t1.fld_result_3), SUM(t1.fld_result_4), \
                        SUM(t1.fld_result_5) \
                 FROM tbl_risk_analysis AS t1 \
                 INNER JOIN tbl_system AS t2 \
                 ON t1.fld_assembly_id=t2.fld_assembly_id \
                 WHERE t2.fld_parent_assembly='%s'" % _values
        sums = self._app.DB.execute_query(query,
                                          None,
                                          self._app.ProgCnx)

# Update the selected assembly's change descriptions with the combined change
# description.
        if(_conf.RTK_MODULES[0] == 1):
            _values = (summary[0], summary[1], summary[2], summary[3], \
                       summary[4], summary[5], summary[6], summary[7], \
                       sums[0][0], sums[0][1], sums[0][2], sums[0][3], \
                       sums[0][4], \
                       self._app.REVISION.revision_id, self.assembly_id)
        else:
            _values = (summary[0], summary[1], summary[2], summary[3], \
                       summary[4], summary[5], summary[6], summary[7], \
                       sums[0][0], sums[0][1], sums[0][2], sums[0][3], \
                       sums[0][4], 0, self.assembly_id)

# Update the database.
        query = "UPDATE tbl_risk_analysis \
                 SET fld_change_desc_1='%s', fld_change_desc_2='%s', \
                     fld_change_desc_3='%s', fld_change_desc_4='%s', \
                     fld_change_desc_5='%s', fld_change_desc_6='%s', \
                     fld_change_desc_7='%s', fld_change_desc_8='%s', \
                     fld_result_1=%d, fld_result_2=%d, \
                     fld_result_3=%d, fld_result_4=%d, \
                     fld_result_5=%d \
                 WHERE fld_revision_id=%d AND fld_assembly_id=%d" % _values
        self._app.DB.execute_query(query,
                                   None,
                                   self._app.ProgCnx,
                                   commit=True)

        return False

    def _risk_save(self):
        """
        Saves the Assembly Object risk analysis gtk.TreeView
        information to the Program's MySQL or SQLite3 database.
        """

# First save the risk analysis worksheet to tbl_risk_analysis.
        _model_ = self.tvwRisk.get_model()
        _model_.foreach(self._risk_save_line_item)

# Then save the risk matrix.
        _model_ = self.tvwRiskMap.get_model()
        _model_.foreach(self._risk_map_save_line_item)

        return False

    def _risk_save_line_item(self, model, path_, row):
        """
        Saves each row in the Assembly Object risk analysis treeview
        model to the database.

        Keyword Arguments:
        model -- the Assembly Object similar item analysis gtk.TreeModel.
        path_ -- the path of the active row in the Assembly Object
                 similar item analysis gtk.TreeModel.
        row   -- the selected row in the Assembly Object similar item
                 analysis gtk.TreeView.
        """

        if(_conf.BACKEND == 'mysql'):
            equation1 = self._app.ProgCnx.escape_string(model.get_value(row, self._risk_col_order[22]))
            equation2 = self._app.ProgCnx.escape_string(model.get_value(row, self._risk_col_order[23]))
            equation3 = self._app.ProgCnx.escape_string(model.get_value(row, self._risk_col_order[24]))
            equation4 = self._app.ProgCnx.escape_string(model.get_value(row, self._risk_col_order[25]))
            equation5 = self._app.ProgCnx.escape_string(model.get_value(row, self._risk_col_order[26]))
        elif(_conf.BACKEND == 'sqlite3'):
            equation1 = model.get_value(row, self._risk_col_order[22])
            equation2 = model.get_value(row, self._risk_col_order[23])
            equation3 = model.get_value(row, self._risk_col_order[24])
            equation4 = model.get_value(row, self._risk_col_order[25])
            equation5 = model.get_value(row, self._risk_col_order[26])

        _values = (model.get_value(row, self._risk_col_order[3]), \
                   model.get_value(row, self._risk_col_order[4]), \
                   model.get_value(row, self._risk_col_order[5]), \
                   model.get_value(row, self._risk_col_order[6]), \
                   model.get_value(row, self._risk_col_order[7]), \
                   model.get_value(row, self._risk_col_order[8]), \
                   model.get_value(row, self._risk_col_order[9]), \
                   model.get_value(row, self._risk_col_order[10]), \
                   model.get_value(row, self._risk_col_order[11]), \
                   model.get_value(row, self._risk_col_order[12]), \
                   model.get_value(row, self._risk_col_order[13]), \
                   model.get_value(row, self._risk_col_order[14]), \
                   model.get_value(row, self._risk_col_order[15]), \
                   model.get_value(row, self._risk_col_order[16]), \
                   model.get_value(row, self._risk_col_order[17]), \
                   model.get_value(row, self._risk_col_order[18]), \
                   model.get_value(row, self._risk_col_order[19]), \
                   model.get_value(row, self._risk_col_order[20]), \
                   model.get_value(row, self._risk_col_order[21]), \
                   equation1, \
                   equation2, \
                   equation3, \
                   equation4, \
                   equation5, \
                   model.get_value(row, self._risk_col_order[27]), \
                   model.get_value(row, self._risk_col_order[28]), \
                   model.get_value(row, self._risk_col_order[29]), \
                   model.get_value(row, self._risk_col_order[30]), \
                   model.get_value(row, self._risk_col_order[31]), \
                   model.get_value(row, self._risk_col_order[32]), \
                   model.get_value(row, self._risk_col_order[33]), \
                   model.get_value(row, self._risk_col_order[34]), \
                   model.get_value(row, self._risk_col_order[35]), \
                   model.get_value(row, self._risk_col_order[36]), \
                   model.get_value(row, self._risk_col_order[37]), \
                   model.get_value(row, self._risk_col_order[38]), \
                   model.get_value(row, self._risk_col_order[39]), \
                   model.get_value(row, self._risk_col_order[40]), \
                   self._app.REVISION.revision_id, \
                   model.get_value(row, self._risk_col_order[0]))

        query = "UPDATE tbl_risk_analysis \
                 SET fld_potential_hazard='%s', \
                     fld_potential_cause='%s', \
                     fld_assembly_effect='%s', \
                     fld_assembly_severity='%s', \
                     fld_assembly_probability='%s', \
                     fld_assembly_hri=%d, \
                     fld_assembly_mitigation='%s', \
                     fld_assembly_severity_f='%s', \
                     fld_assembly_probability_f='%s', \
                     fld_assembly_hri_f=%d, \
                     fld_system_effect='%s', \
                     fld_system_severity='%s', \
                     fld_system_probability='%s', \
                     fld_system_hri=%d, \
                     fld_system_mitigation='%s', \
                     fld_system_severity_f='%s', \
                     fld_system_probability_f='%s', \
                     fld_system_hri_f=%d, \
                     fld_remarks='%s', \
                     fld_function_1='%s', \
                     fld_function_2='%s', \
                     fld_function_3='%s', \
                     fld_function_4='%s', \
                     fld_function_5='%s', \
                     fld_result_1=%f, fld_result_2=%f, fld_result_3=%f, \
                     fld_result_4=%f, fld_result_5=%f, \
                     fld_user_blob_1='%s', fld_user_blob_2='%s', \
                     fld_user_blob_3='%s', fld_user_float_1=%f, \
                     fld_user_float_2=%f, fld_user_float_3=%f, \
                     fld_user_int_1=%d, fld_user_int_2=%d, \
                     fld_user_int_3=%d \
                 WHERE fld_revision_id=%d \
                 AND fld_risk_id=%d" % _values
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("assembly.py: Failed to save assembly to risk analysis table.")
            return True

    def _risk_map_save_line_item(self, model, path_, row):
        """
        Saves each row in the Assembly Object risk map gtk.TreeView() model to
        the database.

        Keyword Arguments:
        model -- the Assembly Object risk matrix gtk.TreeModel().
        path_ -- the path of the active row in the Assembly Object risk matrix
                 gtk.TreeModel().
        row   -- the selected row in the Assembly Object risk matrix
                 gtk.TreeView().
        """

        _crit_ = model.get_value(row, 1)

        for j in (2, 5, 8, 11, 14):
            _count_ = model.get_value(row, j)
            _prob_ = model.get_value(row, j + 1)
            _values_ = (_count_, self._app.REVISION.revision_id,
                        self.assembly_id, _crit_, _prob_)
            _query_ = "UPDATE tbl_risk_matrix \
                       SET fld_hazard_count=%d \
                       WHERE fld_revision_id=%d \
                       AND fld_assembly_id=%d \
                       AND fld_severity_id=%d \
                       AND fld_probability_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

# The combination of revision, assembly, severity, and probability doesn't
# already exist so add it.
            if _results_:
                _query_ = "INSERT INTO tbl_risk_matrix \
                           (fld_hazard_count, fld_revision_id, \
                            fld_assembly_id, fld_severity_id, \
                            fld_probability_id) \
                           VALUES(%d, %d, %d, %d, %d)" % _values_
                _results_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx,
                                                       commit=True)

        return False

    def _sia_save(self):
        """
        Saves the Assembly Object similar item analysis gtk.TreeView
        information to the Program's MySQL or SQLite3 database.
        """

        model = self.tvwSIA.get_model()
        model.foreach(self._sia_save_line_item)

        return False

    def _sia_save_line_item(self, model, path_, row):
        """
        Saves each row in the Assembly Object similar item analysis treeview
        model to the database.

        Keyword Arguments:
        model -- the Assembly Object similar item analysis gtk.TreeModel.
        path_ -- the path of the active row in the Assembly Object
                 similar item analysis gtk.TreeModel.
        row   -- the selected row in the Assembly Object similar item
                 analysis gtk.TreeView.
        """

        if(_conf.BACKEND == 'mysql'):
            equation1 = self._app.ProgCnx.escape_string(
                                model.get_value(row, self._sia_col_order[19]))
            equation2 = self._app.ProgCnx.escape_string(
                                model.get_value(row, self._sia_col_order[20]))
            equation3 = self._app.ProgCnx.escape_string(
                                model.get_value(row, self._sia_col_order[21]))
            equation4 = self._app.ProgCnx.escape_string(
                                model.get_value(row, self._sia_col_order[22]))
            equation5 = self._app.ProgCnx.escape_string(
                                model.get_value(row, self._sia_col_order[23]))

        elif(_conf.BACKEND == 'sqlite3'):
            equation1 = model.get_value(row, self._sia_col_order[19])
            equation2 = model.get_value(row, self._sia_col_order[20])
            equation3 = model.get_value(row, self._sia_col_order[21])
            equation4 = model.get_value(row, self._sia_col_order[22])
            equation5 = model.get_value(row, self._sia_col_order[23])

        _values_ = (model.get_value(row, self._sia_col_order[3]), \
                    model.get_value(row, self._sia_col_order[4]), \
                    model.get_value(row, self._sia_col_order[5]), \
                    model.get_value(row, self._sia_col_order[6]), \
                    model.get_value(row, self._sia_col_order[7]), \
                    model.get_value(row, self._sia_col_order[8]), \
                    model.get_value(row, self._sia_col_order[9]), \
                    model.get_value(row, self._sia_col_order[10]), \
                    model.get_value(row, self._sia_col_order[11]), \
                    model.get_value(row, self._sia_col_order[12]), \
                    model.get_value(row, self._sia_col_order[13]), \
                    model.get_value(row, self._sia_col_order[14]), \
                    model.get_value(row, self._sia_col_order[15]), \
                    model.get_value(row, self._sia_col_order[16]), \
                    model.get_value(row, self._sia_col_order[17]), \
                    model.get_value(row, self._sia_col_order[18]), \
                    equation1, \
                    equation2, \
                    equation3, \
                    equation4, \
                    equation5, \
                    model.get_value(row, self._sia_col_order[24]), \
                    model.get_value(row, self._sia_col_order[25]), \
                    model.get_value(row, self._sia_col_order[26]), \
                    model.get_value(row, self._sia_col_order[27]), \
                    model.get_value(row, self._sia_col_order[28]), \
                    model.get_value(row, self._sia_col_order[29]), \
                    model.get_value(row, self._sia_col_order[30]), \
                    model.get_value(row, self._sia_col_order[31]), \
                    model.get_value(row, self._sia_col_order[32]), \
                    model.get_value(row, self._sia_col_order[33]), \
                    model.get_value(row, self._sia_col_order[34]), \
                    model.get_value(row, self._sia_col_order[35]), \
                    model.get_value(row, self._sia_col_order[36]), \
                    model.get_value(row, self._sia_col_order[37]), \
                    self._app.REVISION.revision_id, \
                    model.get_value(row, self._sia_col_order[0]))

        _query_ = "UPDATE tbl_similar_item \
                   SET fld_change_desc_1='%s', fld_change_factor_1=%f, \
                       fld_change_desc_2='%s', fld_change_factor_2=%f, \
                       fld_change_desc_3='%s', fld_change_factor_3=%f, \
                       fld_change_desc_4='%s', fld_change_factor_4=%f, \
                       fld_change_desc_5='%s', fld_change_factor_5=%f, \
                       fld_change_desc_6='%s', fld_change_factor_6=%f, \
                       fld_change_desc_7='%s', fld_change_factor_7=%f, \
                       fld_change_desc_8='%s', fld_change_factor_8=%f, \
                       fld_function_1='%s', fld_function_2='%s', \
                       fld_function_3='%s', fld_function_4='%s', \
                       fld_function_5='%s', \
                       fld_result_1=%f, fld_result_2=%f, fld_result_3=%f, \
                       fld_result_4=%f, fld_result_5=%f, \
                       fld_user_blob_1='%s', fld_user_blob_2='%s', \
                       fld_user_blob_3='%s', fld_user_float_1=%f, \
                       fld_user_float_2=%f, fld_user_float_3=%f, \
                       fld_user_int_1=%d, fld_user_int_2=%d, \
                       fld_user_int_3=%d \
                   WHERE fld_revision_id=%d \
                   AND fld_sia_id=%d" % _values_

        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("assembly.py: Failed to save assembly to similar item table.")
            return True

        return False

    def _fmeca_save(self):
        """
        Saves the ASSEMBLY Object FMECA gtk.TreeView information to the
        Program's MySQL or SQLite3 database.
        """

        model = self.tvwFMECA.get_model()
        model.foreach(self._fmeca_save_line_item)

        return False

    def _fmeca_save_line_item(self, model, path, row):
        """
        Saves each row in the Assembly Object FMEA/FMECA treeview model to the
        open RTK database.

        Keyword Arguments:
        model -- the Assembly Object similar item analysis gtk.TreeModel.
        path  -- the path of the active row in the Assembly Object
                 similar item analysis gtk.TreeModel.
        row   -- the selected row in the Assembly Object similar item
                 analysis gtk.TreeView.
        """

# Find the type of information in the row.
#   0 = failure mode
#   1 = failure mechanism
#   2 = design control
#   3 = action
        _type_ = model.get_value(row, len(self._FMECA_col_order))

        if(_type_ == 0):                     # Failure mode.
# Update the FMECA table.
            _values_ = (model.get_value(row, self._FMECA_col_order[1]), \
                        model.get_value(row, self._FMECA_col_order[2]), \
                        model.get_value(row, self._FMECA_col_order[3]), \
                        model.get_value(row, self._FMECA_col_order[4]), \
                        model.get_value(row, self._FMECA_col_order[5]), \
                        model.get_value(row, self._FMECA_col_order[6]), \
                        model.get_value(row, self._FMECA_col_order[7]), \
                        model.get_value(row, self._FMECA_col_order[8]), \
                        model.get_value(row, self._FMECA_col_order[9]), \
                        model.get_value(row, self._FMECA_col_order[10]), \
                        model.get_value(row, self._FMECA_col_order[11]), \
                        model.get_value(row, self._FMECA_col_order[12]), \
                        model.get_value(row, self._FMECA_col_order[13]), \
                        float(model.get_value(row, self._FMECA_col_order[14])), \
                        float(model.get_value(row, self._FMECA_col_order[15])), \
                        float(model.get_value(row, self._FMECA_col_order[16])), \
                        float(model.get_value(row, self._FMECA_col_order[17])), \
                        float(model.get_value(row, self._FMECA_col_order[18])), \
                        model.get_value(row, self._FMECA_col_order[20]), \
                        model.get_value(row, self._FMECA_col_order[21]),
                        int(model.get_value(row, self._FMECA_col_order[22])), \
                        int(model.get_value(row, self._FMECA_col_order[23])), \
                        model.get_value(row, self._FMECA_col_order[24]), \
                        int(model.get_value(row, self._FMECA_col_order[0])))

            _query_ = "UPDATE tbl_fmeca \
                       SET fld_mode_description='%s', fld_mission_phase='%s', \
                           fld_local_effect='%s', fld_next_effect='%s', \
                           fld_end_effect='%s', fld_detection_method='%s', \
                           fld_other_indications='%s', \
                           fld_isolation_method='%s', \
                           fld_design_provisions='%s', \
                           fld_operator_actions='%s', \
                           fld_severity_class='%s', \
                           fld_hazard_rate_source='%s', \
                           fld_failure_probability='%s', \
                           fld_effect_probability=%f, \
                           fld_mode_ratio=%f, fld_mode_failure_rate=%f, \
                           fld_mode_op_time=%f, fld_mode_criticality=%f, \
                           fld_rpn_severity='%s', fld_rpn_severity_new='%s', \
                           fld_critical_item=%d, fld_single_point=%d, \
                           fld_remarks='%s' \
                       WHERE fld_mode_id=%d" % _values_

        elif(_type_ == 1):                  # Failure mechanism.
            _parent_ = model.get_string_from_iter(model.iter_parent(row))
            _values_ = (model.get_value(row, 1), \
                        self._mechanisms[model.get_value(row, 0)][1], \
                        self._mechanisms[model.get_value(row, 0)][2], \
                        self._mechanisms[model.get_value(row, 0)][3], \
                        self._mechanisms[model.get_value(row, 0)][4], \
                        self._mechanisms[model.get_value(row, 0)][5], \
                        self._mechanisms[model.get_value(row, 0)][6], \
                        _parent_, model.get_value(row, 0))

            _query_ = "UPDATE tbl_fmeca_mechanisms \
                       SET fld_mechanism_description='%s', \
                           fld_rpn_occurrence=%d, fld_rpn_detection=%d, \
                           fld_rpn=%d, fld_rpn_occurrence_new=%d, \
                           fld_rpn_detection_new=%d, fld_rpn_new=%d, \
                           fld_parent='%s' \
                       WHERE fld_mechanism_id=%d" % _values_

        elif(_type_ == 2):                  # Control.
            _parent_ = model.get_string_from_iter(model.iter_parent(row))
            _values_ = (model.get_value(row, 1), \
                        self._fmeca_controls[model.get_value(row, 0)][1], \
                        _parent_, model.get_value(row, 0))

            _query_ = "UPDATE tbl_fmeca_controls \
                       SET fld_control_description='%s', \
                           fld_control_type=%d, fld_parent='%s' \
                       WHERE fld_control_id=%d" % _values_

        elif(_type_ == 3):                  # Action.
            _parent_ = model.get_string_from_iter(model.iter_parent(row))
            _values_ = (model.get_value(row, 1), \
                        self._fmeca_actions[model.get_value(row, 0)][1], \
                        self._fmeca_actions[model.get_value(row, 0)][2], \
                        self._fmeca_actions[model.get_value(row, 0)][3], \
                        self._fmeca_actions[model.get_value(row, 0)][4], \
                        self._fmeca_actions[model.get_value(row, 0)][5], \
                        self._fmeca_actions[model.get_value(row, 0)][6], \
                        self._fmeca_actions[model.get_value(row, 0)][7], \
                        self._fmeca_actions[model.get_value(row, 0)][8], \
                        self._fmeca_actions[model.get_value(row, 0)][9], \
                        _parent_, model.get_value(row, 0))

            _query_ = "UPDATE tbl_fmeca_actions \
                       SET fld_action_recommended='%s', \
                           fld_action_category='%s', fld_action_owner='%s', \
                           fld_action_due_date=%d, fld_action_status='%s', \
                           fld_action_taken='%s', fld_action_approved='%s', \
                           fld_action_approve_date=%d, fld_action_closed='%s', \
                           fld_action_close_date=%d, fld_parent='%s' \
                       WHERE fld_action_id=%d" % _values_

        self._app.DB.execute_query(_query_,
                                   None,
                                   self._app.ProgCnx,
                                   commit=True)

        return False

    def _allocation_tree_edit(self, cell, path, new_text, position, model):
        """
        Called whenever a TreeView CellRenderer is edited.

        Keyword Arguments:
        cell     -- the CellRenderer that was edited.
        path     -- the TreeView path of the CellRenderer that was edited.
        new_text -- the new text in the edited CellRenderer.
        position -- the column position of the edited CellRenderer.
        model    -- the TreeModel the CellRenderer belongs to.
        """

        convert = gobject.type_name(model.get_column_type(position))

        if(position == 3):
            model[path][position] = not cell.get_active()
        elif(convert == 'gchararray'):
            model[path][position] = str(new_text)
        elif(convert == 'gint'):
            model[path][position] = int(new_text)
        elif(convert == 'gfloat'):
            model[path][position] = float(new_text)

        return False

    def _callback_combo_cell(self, cell, path, row, position, treemodel,
                             lastcol):
        """
        Called whenever a TreeView CellRendererCombo changes.

        Keyword Arguments:
        cell      -- the gtk.CellRendererCombo that called this function
        path      -- the path in the gtk.TreeView containing the
                     gtk.CellRendererCombo that called this function.
        row       -- the new gtk.TreeIter in the gtk.CellRendererCombo that
                     called this function.
        position  -- the position of in the gtk.TreeView of the
                     gtk.CellRendererCombo that called this function.
        treemodel -- the gtk.TreeModel for the gtk.TreeView.
        lastcol   -- the index of the last visible column in the
                     gtk.TreeView.
        """

        model = cell.get_property('model')
        val = model.get_value(row, 0)

        treerow = treemodel.get_iter(path)
        treemodel.set_value(treerow, position, val)

        return False

    def _callback_combo(self, combo, index_):
        """
        Callback function to retrieve and save combobox changes.

        Keyword Arguments:
        combo   -- the gtk.Combo that called the function.
        _index_ -- the position in the applicable treeview associated with the
                   data from the calling gtk.Combo.
        """

        i = combo.get_active()

        if(index_ < 200):                   # Hardware information.
            # Get the Hardware Tree model/selected row and update the
            # Hardware TreeView.
            model = self._app.HARDWARE.model
            row = self._app.HARDWARE.selected_row
            model.set_value(row, index_, int(combo.get_active()))

            if(index_ == 10):               # Calculation model
                self._trickledown(model, row, index_, int(combo.get_active()))
                if(int(combo.get_active()) > 2):
                    _title_ = _("RTK Information")

                    dialog = _widg.make_dialog(_title_,
                             _flags_=(gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT),
                             _buttons_=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

                    _text_ = _("%s model not yet implemented.  Contact weibullguy@gmail.com if you would like to help." % combo.get_active_text())
                    label = _widg.make_label(_text_,
                                             width=250, height=75)
                    dialog.vbox.pack_start(label)
                    label.show()

                    dialog.run()
                    dialog.destroy()

            elif(index_ == 22):             # Active Environment
                self._trickledown(model, row, index_, int(combo.get_active()))

            elif(index_ == 23):             # Dormant environment
                self._trickledown(model, row, index_, int(combo.get_active()))

            elif(index_ == 35):             # Hazard rate type
                # If selected type is hazard rate specified or MTBF specified,
                # set active and predicted values equal to specified values.
                if(combo.get_active() == 2):    # Specified hazard rate.
                    ht = model.get_value(row, 34)
                    try:
                        mtbf = 1.0 / ht
                    except ZeroDivisionError:
                        mtbf = 0.0
                    model.set_value(row, 28, ht)
                    model.set_value(row, 32, ht)
                    model.set_value(row, 50, mtbf)
                    model.set_value(row, 51, mtbf)
                elif(combo.get_active() == 3):  # Specified MTBF.
                    mtbf = model.get_value(row, 51)
                    try:
                        ht = 1.0 / mtbf
                    except ZeroDivisionError:
                        ht = 0.0
                    model.set_value(row, 28, ht)
                    model.set_value(row, 32, ht)
                    model.set_value(row, 34, ht)
                    model.set_value(row, 50, mtbf)

            elif(index_ == 43):             # Manufacturer
                cmbmodel = combo.get_model()
                cmbrow = combo.get_active_iter()

                try:
                    self.txtCAGECode.set_text(str(cmbmodel.get_value(cmbrow, 2)))
                    model.set_value(row, 9, str(cmbmodel.get_value(cmbrow, 2)))
                except TypeError:           # No row is selected
                    pass

        elif(index_ > 199 and
             index_ < 300):                # Incident report entries
            _index_ = index_ - 200
            selection = self.tvwIncidentList.get_selection()
            (model, row) = selection.get_selected()
            if(row is not None):
                model.set_value(row, _index_, i)

        elif(index_ > 299 and
             index_ < 400):                 # Incident action entries
            _index_ = index_ - 300
            selection = self.tvwActionList.get_selection()
            (model, row) = selection.get_selected()
            if(row is not None):
                model.set_value(row, _index_, i)

# Reliability requirement measure combo box called this function.
        elif(index_ == 500):
            i = int(combo.get_active())
            if(i == 0):                     # Nothing selected.
                self.txtReliabilityGoal.props.editable = 0
                self.txtReliabilityGoal.set_sensitive(0)
                self.txtMTBFGoal.props.editable = 0
                self.txtMTBFGoal.set_sensitive(0)
                self.txtFailureRateGoal.props.editable = 0
                self.txtFailureRateGoal.set_sensitive(0)
            elif(i == 1):                   # Expressed as reliability.
                self.txtReliabilityGoal.props.editable = 1
                self.txtReliabilityGoal.set_sensitive(1)
                self.txtMTBFGoal.props.editable = 0
                self.txtMTBFGoal.set_sensitive(0)
                self.txtFailureRateGoal.props.editable = 0
                self.txtFailureRateGoal.set_sensitive(0)
            elif(i == 2):                   # Expressed as an MTBF.
                self.txtReliabilityGoal.props.editable = 0
                self.txtReliabilityGoal.set_sensitive(0)
                self.txtMTBFGoal.props.editable = 1
                self.txtMTBFGoal.set_sensitive(1)
                self.txtFailureRateGoal.props.editable = 0
                self.txtFailureRateGoal.set_sensitive(0)
            elif(i == 3):                   # Expressed as a failure rate.
                self.txtReliabilityGoal.props.editable = 0
                self.txtReliabilityGoal.set_sensitive(0)
                self.txtMTBFGoal.props.editable = 0
                self.txtMTBFGoal.set_sensitive(0)
                self.txtFailureRateGoal.props.editable = 1
                self.txtFailureRateGoal.set_sensitive(1)

# Reliability allocation method combo box called this function.  Hide/show the
# appropriate columns in the Allocation gtk.TreeView.
        elif(index_ == 501):
            i = int(combo.get_active())
            _heading_ = _("Weighting Factor")
            if(i == 1):                     # Equal apportionment selected.
                for col in 0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 13, 19, 20, 21:
                    self.tvwAllocation.get_column(col).set_visible(0)
                for col in 2, 12, 14, 15, 16, 17, 18, 19:
                    self.tvwAllocation.get_column(col).set_visible(1)
                    column = self.tvwAllocation.get_column(col)
                    cells = column.get_cell_renderers()
                    for i in range(len(cells)):
                        cells[i].set_property('background', 'light gray')
                        cells[i].set_property('editable', 0)

            elif(i == 2):                   # AGREE apportionment selected.
                for col in 0, 1, 4, 8, 9, 10, 11, 13, 19, 20, 21:
                    self.tvwAllocation.get_column(col).set_visible(0)
                for col in 2, 6, 12, 14, 15, 16, 17, 18, 19:
                    self.tvwAllocation.get_column(col).set_visible(1)
                    column = self.tvwAllocation.get_column(col)
                    cells = column.get_cell_renderers()
                    for i in range(len(cells)):
                        cells[i].set_property('background', 'light gray')
                        cells[i].set_property('editable', 0)
                for col in 5, 7, 12:
                    self.tvwAllocation.get_column(col).set_visible(1)
                    column = self.tvwAllocation.get_column(col)
                    cells = column.get_cell_renderers()
                    for i in range(len(cells)):
                        cells[i].set_property('background', 'white')
                        cells[i].set_property('editable', 1)

                _heading_ = _("Importance Measure")

            elif(i == 3):                   # ARINC apportionment selected.
                for col in 0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 13, 20, 21:
                    self.tvwAllocation.get_column(col).set_visible(0)
                for col in 2, 12, 14, 15, 16, 17, 18, 19:
                    self.tvwAllocation.get_column(col).set_visible(1)
                    column = self.tvwAllocation.get_column(col)
                    cells = column.get_cell_renderers()
                    for i in range(len(cells)):
                        cells[i].set_property('background', 'light gray')
                        cells[i].set_property('editable', 0)

            elif(i == 4):                   # Feasibility of Objectives selected.
                for col in 0, 1, 4, 5, 6, 7, 19, 20, 21:
                    self.tvwAllocation.get_column(col).set_visible(0)
                for col in 2, 12, 13, 14, 15, 16, 17, 18, 19:
                    self.tvwAllocation.get_column(col).set_visible(1)
                    column = self.tvwAllocation.get_column(col)
                    cells = column.get_cell_renderers()
                    for i in range(len(cells)):
                        cells[i].set_property('background', 'light gray')
                        cells[i].set_property('editable', 0)
                for col in 8, 9, 10, 11:
                    self.tvwAllocation.get_column(col).set_visible(1)
                    column = self.tvwAllocation.get_column(col)
                    cells = column.get_cell_renderers()
                    for i in range(len(cells)):
                        cells[i].set_property('background', 'white')
                        cells[i].set_property('editable', 1)

            elif(i == 5):                   # Repairable System apportionment selected.
                for col in 0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19:
                    self.tvwAllocation.get_column(col).set_visible(0)
                for col in 2, 12, 14, 15, 16, 17, 18, 19, 20, 21:
                    self.tvwAllocation.get_column(col).set_visible(1)
                    column = self.tvwAllocation.get_column(col)
                    cells = column.get_cell_renderers()
                    for i in range(len(cells)):
                        cells[i].set_property('background', 'light gray')
                        cells[i].set_property('editable', 0)

            self.tvwAllocation.get_column(3).set_visible(1)
            column = self.tvwAllocation.get_column(12)
            _label_ = column.get_widget()
            _text_ = "<span weight='bold'>%s</span>" % _heading_
            _label_.set_markup(_text_)
            column.set_widget(_label_)

        elif(index_ >= 1000):
            selection = self.tvwFMECA.get_selection()
            (model, row) = selection.get_selected()
            _id = model.get_value(row, 0)
            _type = model.get_value(row, len(self._FMECA_col_order))

            _index_ = index_ - 1000

            if(_type == 1):                 # Failure mechanism
                self._mechanisms[_id][_index_] = i
            elif(_type == 2):               # Control
                self._fmeca_controls[_id][_index_] = i
            elif(_type == 3):               # Action
                self._fmeca_actions[_id][_index_] = i

        return False

    def _callback_entry(self, entry, event, convert, index_):
        """
        Callback function to retrieve and save entry changes.

        Keyword Arguments:
        entry    -- the gtk.Entry that called the function.
        event    -- the gtk.gdk.Event that called the function.
        convert  -- the data type to convert the entry contents to.
        _index_  -- the position in the applicable treeview associated
                    with the data from the calling gtk.Entry.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        if(convert == 'text'):
            if(index_ == 71):
                textbuffer = self.txtRemarks.get_child().get_child().get_buffer()
                _text_ = textbuffer.get_text(*textbuffer.get_bounds())
            else:
                _text_ = entry.get_text()

        elif(convert == 'int'):
            _text_ = int(entry.get_text())

        elif(convert == 'float'):
            _text_ = float(entry.get_text().replace('$', ''))

        elif(convert == 'date'):
            _text_ = datetime.strptime(entry.get_text(), '%Y-%m-%d').toordinal()

        if(index_ < 200):                   # Hardware information.
            # Get the Hardware Tree model and selected row.
            model = self._app.HARDWARE.model
            row = self._app.HARDWARE.selected_row

            # Update the Hardware Tree.
            model.set_value(row, index_, _text_)

            if(index_ == 20 or index_ == 37 or
               index_ == 45 or index_ == 81 or
               index_ == 84):
                # Trickle down values to children assemblies and components if
                # change is made to duty cycle, humidity, mission time, dormant
                # temperature, or vibration
                self._trickledown(model, row, index_, _text_)

            elif(index_ == 34):             # Specified hazard rate
                # Set predicted failure rate to specified value if the
                # hazard rate type is selected as allocated or hazard rate
                # specified.
                _hr_ = model.get_value(row, 34)
                if(model.get_value(row, 35) == 2):
                    try:
                        _mtbf_ = 1.0 / float(_hr_)
                    except ZeroDivisionError:
                        _mtbf_ = 0.0

                    model.set_value(row, 28, _text_)
                    model.set_value(row, 32, _text_)
                    model.set_value(row, 50, _mtbf_)

            elif(index_ == 51):             # Specified MTBF
                # Set predicted MTBF to specified value if the hazard rate type
                # is selected as allocated or MTBFspecified.
                if(model.get_value(row, 35) == 3):
                    try:
                        _ht_ = 1.0 / _text_
                    except ZeroDivisionError:
                        _ht_ = 0.0

                    model.set_value(row, 28, _ht_)
                    model.set_value(row, 32, _ht_)
                    model.set_value(row, 50, _text_)

            elif(index_ == 80):             # Active Temperature
                # Number of children.
                n_children = model.iter_n_children(row)

                # Update the ambient temperature for each of the child
                # components.
                for i in range(n_children):
                    chrow = model.iter_nth_child(row, i)
                    model.set_value(chrow, index_, _text_)

                    # Now update the Parts List treeview.
                    partmodel = self._app.COMPONENT.model
                    partrow = self._app.COMPONENT.selected_row
                    partmodel.set_value(partrow, 103, _text_)

        elif(index_ > 199 and
             index_ < 300):                # Incident report entries
            _index_ = index_ - 200
            if(_index_ == 4):
                _text_ = self.txtLongDescription.get_text(*self.txtLongDescription.get_bounds())
            elif(_index_ == 7):
                _text_ = self.txtIncidentRemarks.get_text(*self.txtIncidentRemarks.get_bounds())
            elif(_index_ == 12):
                _text_ = self.txtEffect.get_text(*self.txtEffect.get_bounds())
            elif(_index_ == 13):
                _text_ = self.txtRecommendedSolution.get_text(*self.txtRecommendedSolution.get_bounds())

            selection = self.tvwIncidentList.get_selection()
            (model, row) = selection.get_selected()
            model.set_value(row, _index_, _text_)

        elif(index_ > 299 and
             index_ < 400):                 # Action entries
            _index_ = index_ - 300
            if(_index_ == 1):
                _text_ = self.txtActionPrescribed.get_text(*self.txtActionPrescribed.get_bounds())
            elif(_index_ == 5):
                _text_ = self.txtActionTaken.get_text(*self.txtActionTaken.get_bounds())

            selection = self.tvwActionList.get_selection()
            (model, row) = selection.get_selected()
            model.set_value(row, _index_, _text_)

        elif(index_ >= 500 and
             index_ < 1000):                # Allocation goals.
            if(index_ == 500):
                (MTBFg, FRg) = self._calculate_goals(500)

                self.txtMTBFGoal.set_text(str(fmt.format(MTBFg)))
                self.txtFailureRateGoal.set_text(str(fmt.format(FRg)))

            elif(index_ == 501):
                (Rg, FRg) = self._calculate_goals(501)

                self.txtReliabilityGoal.set_text(str(fmt.format(Rg)))
                self.txtFailureRateGoal.set_text(str(fmt.format(FRg)))

            elif(index_ == 502):
                (Rg, MTBFg) = self._calculate_goals(502)

                self.txtReliabilityGoal.set_text(str(fmt.format(Rg)))
                self.txtMTBFGoal.set_text(str(fmt.format(MTBFg)))

        elif(index_ >= 1000):               # FMECA information.
            selection = self.tvwFMECA.get_selection()
            (model, row) = selection.get_selected()
            _id = model.get_value(row, 0)
            _type = model.get_value(row, len(self._FMECA_col_order))

            _index_ = index_ - 1000

            if(_type == 1):                 # Failure mechanism
                self._mechanisms[_id][_index_] = _text_
            elif(_type == 2):               # Control
                self._fmeca_controls[_id][_index_] = _text_
            elif(_type == 3):               # Action
                if(_index_ == 0):
                    textbuffer = self.txtActionRecommended.get_child().get_child().get_buffer()
                    _text_ = textbuffer.get_text(*textbuffer.get_bounds())
                elif(_index_ == 5):
                    textbuffer = self.txtActionTaken.get_child().get_child().get_buffer()
                    _text_ = textbuffer.get_text(*textbuffer.get_bounds())

                self._fmeca_actions[_id][_index_] = _text_

        return False

    def _callback_check(self, check, index_):
        """
        Callback function to retrieve and save checkbutton changes.

        Keyword Arguments:
        check  -- the checkbutton that called the function.
        index_ -- the position in the Assembly Object _attribute list
                  associated with the data from the calling checkbutton.
        """

        if(index_ > 87):
# Determine the failure consequences.
            if(self.chkFCQ1.get_active() and not self.chkFCQ2.get_active()):
                self.optEO.set_active(True)
            elif(not self.chkFCQ1.get_active() and not self.chkFCQ3.get_active()):
                self.optNSH.set_active(True)
            elif(self.chkFCQ1.get_active() and self.chkFCQ2.get_active()):
                self.optES.set_active(True)
            else:
                self.optHS.set_active(True)

# Make the correct question available depending on the answer to question 1.
            if(self.chkFCQ1.get_active()):
                self.chkFCQ2.set_sensitive(True)
                self.chkFCQ3.set_sensitive(False)
            else:
                self.chkFCQ2.set_sensitive(False)
                self.chkFCQ3.set_sensitive(True)

        else:
# Get the Hardware Tree model and selected row.
            model = self._app.HARDWARE.model
            row = self._app.HARDWARE.selected_row

# Update the Hardware Tree.
            model.set_value(row, index_, check.get_active())

        return False

    def _trickledown(self, model, row, _index_, _value_):
        """
        Updates child assemblies and components when certain information is
        changed in the parent assembly.

        Keyword Arguments:
        model   -- the HARDWARE Object treemodel.
        row     -- the selected row in the HARDWARE Object treemodel.
        _index_ -- the position in the ASSEMBLY Object _attribute list
                   associated with the data to be trickled down.
        _value_ -- the value to update the children with.
        """

        n_children = model.iter_n_children(row)

        for i in range(n_children):
            chrow = model.iter_nth_child(row, i)
            if(model.iter_has_child(chrow)):
                self._trickledown(model, chrow, _index_, _value_)
            model.set_value(chrow, _index_, _value_)
            if(model.get_value(chrow, 63) == 1):
                self._category = model.get_value(chrow, 11)
                self._subcategory = model.get_value(chrow, 78)

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
                    3 = Similar Items Analysis
                    4 = Assessment Inputs
                    5 = Assessment Results
                    6 = FMEA
                    7 = Maintenance Planning
                    8 = Reliability Growth Planning
        """

        self._selected_tab = page_num

        if(page_num == 0):                  # General data tab.
            self.btnAddItem.show()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.hide()
            self.btnSaveResults.hide()
            self.btnRollup.hide()
            self.btnEdit.hide()
            self.btnAddItem.set_tooltip_text(_(u"Add components to the currently selected assembly."))
        elif(page_num == 1):                # Allocation tab
            self.btnAddItem.hide()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.hide()
            self.btnEdit.hide()
            self.btnAddItem.set_tooltip_text(_(u"Add components to the currently selected assembly."))
            self.btnAnalyze.set_tooltip_text(_(u"Allocates the reliability to the child assemblies/parts."))
            self.btnSaveResults.set_tooltip_text(_(u"Saves the allocation results for the selected assembly."))
        elif(page_num == 2):                # Hazard analysis tab
            self.btnAddItem.show()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.show()
            self.btnEdit.show()
            self.btnAddItem.set_tooltip_text(_(u"Adds a hazard to the selected assembly."))
            self.btnAnalyze.set_tooltip_text(_(u"Performs a risk analysis of changes to the selected assembly."))
            self.btnSaveResults.set_tooltip_text(_(u"Saves the risk analysis results for the selected assembly."))
            self.btnRollup.set_tooltip_text(_(u"Summarizes the lower level risk analyses."))
            self.btnEdit.set_tooltip_text(_(u"Create/edit current risk analysis functions."))
        elif(page_num == 3):                # Similar items tab
            self.btnAddItem.hide()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.show()
            self.btnEdit.show()
            self.btnAnalyze.set_tooltip_text(_("Performs the similar item analysis."))
            self.btnSaveResults.set_tooltip_text(_("Saves the similar item analysis results for the selected assembly."))
            self.btnRollup.set_tooltip_text(_("Summarizes the lower level similar item analyses."))
            self.btnEdit.set_tooltip_text(_("Create/edit current similar item analysis functions."))
        elif(page_num == 4):                # Assessment inputs tab
            self.btnAddItem.show()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.show()
            self.btnSaveResults.hide()
            self.btnRollup.hide()
            self.btnEdit.hide()
            self.btnAnalyze.set_tooltip_text(_("Calculate the hardware metrics in the open RTK Program Database."))
        elif(page_num == 5):                # Assessment results tab
            self.btnAddItem.show()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.hide()
            self.btnSaveResults.hide()
            self.btnRollup.hide()
            self.btnEdit.hide()
        elif(page_num == 6):                # FMEA/FMECA tab
            self.btnAddItem.hide()
            self.btnFMECAAdd.show()
            self.btnRemoveItem.show()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.show()
            self.btnEdit.hide()
            self.btnAddItem.set_tooltip_text(_("Add a new failure mode."))
            self.btnRemoveItem.set_tooltip_text(_("Remove the currently selected failure mode."))
            self.btnAnalyze.set_tooltip_text(_("Calculates the mode and item criticality for the selected allocation method."))
            self.btnSaveResults.set_tooltip_text(_("Saves the FMEA/FMECA for the selected assembly."))
            self.btnRollup.set_tooltip_text(_("Summarizes the lower level FMEA/FMECA results."))
        elif(page_num == 7):                # Maintenance planning tab
            self.btnAddItem.hide()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.show()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.hide()
            self.btnEdit.hide()
            self.btnAddItem.set_tooltip_text(_("Add a new maintenance activity."))
            self.btnRemoveItem.set_tooltip_text(_("Remove the currently selected maintenance activity."))
            #self.btnAnalyze.set_tooltip_text(_("Calculates the selected allocation method."))
            #self.btnSaveResults.set_tooltip_text(_("Saves the allocation results for the selected assembly."))
        elif(page_num == 8):                # RG planning tab
            self.btnAddItem.hide()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.show()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.hide()
            self.btnEdit.hide()
            self.btnAddItem.set_tooltip_text(_("Add a new reliability growth plan."))
            self.btnRemoveItem.set_tooltip_text(_("Remove the currently selected reliability growth plan."))
            #self.btnAnalyze.set_tooltip_text(_("Calculates the selected allocation method."))
            #self.btnSaveResults.set_tooltip_text(_("Saves the allocation results for the selected assembly."))
        elif(page_num == 9):                # RG tracking tab
            self.btnAddItem.show()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.show()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.hide()
            self.btnEdit.hide()
            self.btnAddItem.set_tooltip_text(_("Add a new relibility growth incident."))
            #self.btnAnalyze.set_tooltip_text(_("Calculates the selected allocation method."))
            #self.btnSaveResults.set_tooltip_text(_("Saves the allocation results for the selected assembly."))
        else:
            self.btnAddItem.hide()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.hide()
            self.btnSaveResults.hide()
            self.btnRollup.hide()
            self.btnEdit.hide()

        return False

    def _toolbutton_pressed(self, widget):
        """
        Method to reacte to the ASSEMBLY Object toolbar button clicked events.

        Keyword Arguments:
        widget -- the toolbar button that was pressed.
        """

        # FMEA roll-up lower level FMEA.
        # FMEA calculate criticality.
        # V&V add new task
        # V&V assign existing task
        # Maintenance planning
        # Maintenance planning save changes to selected maintenance policy
        _button_ = widget.get_name()
        _page_ = self.notebook.get_current_page()

        if(_page_ == 0):                    # General data tab.
            if(_button_ == 'Add'):
                self._app.COMPONENT.component_add(widget, None)
            elif(_button_ == 'Analyze'):
                _calc.calculate_project(widget, self._app, 3)
        elif(_page_ == 1):                  # Allocation tab.
            if(_button_ == 'Analyze'):
                self._allocate()
            elif(_button_ == 'Save'):
                self._allocation_save()
        elif(_page_ == 2):                  # Risk analysis tab.
            if(_button_ == 'Add'):
                _query_ = "INSERT INTO tbl_risk_analysis \
                           (fld_revision_id, fld_assembly_id) \
                           VALUES (%d, %d)" % \
                           (self._app.REVISION.revision_id, self.assembly_id)
                _results_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx,
                                                       commit=True)
                self._risk_analysis_tab_load()
            elif(_button_ == 'Analyze'):
                self._calculate_risk()
            elif(_button_ == 'Save'):
                self._risk_save()
            elif(_button_ == 'Rollup'):
                self._risk_rollup()
            elif(_button_ == 'Edit'):
                self._function_edit(_index_=0)
        elif(_page_ == 3):                  # Similar item analysis tab.
            if(_button_ == 'Analyze'):
                self._calculate_sia()
            elif(_button_ == 'Save'):
                self._sia_save()
            elif(_button_ == 'Rollup'):
                self._sia_rollup()
            elif(_button_ == 'Edit'):
                self._function_edit(_index_=1)
        elif(_page_ == 4):                  # Assessment inputs tab.
            if(_button_ == 'Add'):
                self._app.COMPONENT.component_add(widget, None)
            elif(_button_ == 'Analyze'):
                _calc.calculate_project(widget, self._app, 3)
        elif(_page_ == 5):                  # Assessment results tab.
            if(_button == 'Add'):
                self._app.COMPONENT.component_add(widget, None)
            elif(_button_ == 'Analyze'):
                _calc.calculate_project(widget, self._app, 3)
        elif(_page_ == 6):                  # FMEA/FMECA tab.
            if(widget.get_label() == 'Mode'):
# Find the id of the next failure mode.
                query = "SELECT seq FROM sqlite_sequence \
                         WHERE name='tbl_fmeca'"
                _last_id = self._app.DB.execute_query(query,
                                                      None,
                                                      self._app.ProgCnx)

                if(not _last_id):
                    _last_id = 0
                else:
                    _last_id = _last_id[0][0] + 1

# Insert the new failure mode.
                query = "INSERT INTO tbl_fmeca \
                         (fld_assembly_id, fld_function_id, fld_mode_id) \
                         VALUES (%d, 0, %d)" % (self.assembly_id, _last_id)
                self._app.DB.execute_query(query,
                                           None,
                                           self._app.ProgCnx,
                                           True)

                # Insert a new line in the failure consequence table.
                query = "INSERT INTO tbl_failure_consequences \
                         (fld_assembly_id, fld_mode_id) \
                         VALUES (%d, %d)" % (self.assembly_id, _last_id)
                self._app.DB.execute_query(query,
                                           None,
                                           self._app.ProgCnx,
                                           True)

                self._fmeca_tab_load()

            elif(widget.get_label() == 'Mechanism'):
# Find the id and gtk.TreeIter of the parent failure mode.
                _selection = self.tvwFMECA.get_selection()
                (model, row) = _selection.get_selected()
                _mode_id = model.get_value(row, 0)
                _parent =  model.get_string_from_iter(row)

                if(_parent.count(':') != 0):
                    _util.application_error(_(u"  A failure mechanism can only be the child of a failure mode, not another failure mechanism, control, or action."))
                    return True

# Find the id of the next failure mechanism.
                query = "SELECT seq FROM sqlite_sequence \
                         WHERE name='tbl_fmeca_mechanisms'"
                _next_id = self._app.DB.execute_query(query,
                                                      None,
                                                      self._app.ProgCnx)

                if(not _next_id):
                    _next_id = 0
                else:
                    _next_id = _next_id[0][0] + 1

# Insert the new failure mechanism.
                query = "INSERT INTO tbl_fmeca_mechanisms \
                         (fld_assembly_id, fld_mode_id, \
                          fld_mechanism_id, fld_parent) \
                         VALUES (%d, %d, %d, '%s')" % (self.assembly_id,
                                                       _mode_id, _next_id,
                                                       _parent)
                self._app.DB.execute_query(query,
                                           None,
                                           self._app.ProgCnx,
                                           True)
                self._fmeca_tab_load()

            elif(widget.get_label() == 'Control'):
# Find the id and gtk.TreeIter of the parent failure mechanism.
                _selection = self.tvwFMECA.get_selection()
                (model, row) = _selection.get_selected()
                _mechanism_id = model.get_value(row, 0)
                _parent =  model.get_string_from_iter(row)

                if(_parent.count(':') != 1):
                    _util.application_error(_(u"A control can only be the child of a failure mechanism, not another control, failure mode, or action."))
                    return True

# Find the id of the grand-parent failure mode.
                row = model.iter_parent(row)
                _mode_id = model.get_value(row, 0)

# Find the id of the next control.
                query = "SELECT seq FROM sqlite_sequence \
                         WHERE name='tbl_fmeca_controls'"
                _next_id = self._app.DB.execute_query(query,
                                                      None,
                                                      self._app.ProgCnx)

                if(not _next_id):
                    _next_id = 0
                else:
                    _next_id = _next_id[0][0] + 1

# Insert the new control.
                query = "INSERT INTO tbl_fmeca_controls \
                         (fld_assembly_id, fld_mode_id, \
                          fld_mechanism_id, fld_control_id, fld_parent) \
                         VALUES (%d, %d, %d, %d, '%s')" % (self.assembly_id,
                                                           _mode_id,
                                                           _mechanism_id,
                                                           _next_id,
                                                           _parent)
                self._app.DB.execute_query(query,
                                           None,
                                           self._app.ProgCnx,
                                           True)
                self._fmeca_tab_load()

            elif(widget.get_label() == 'Action'):
# Find the id and gtk.TreeIter of the parent failure mechanism.
                _selection = self.tvwFMECA.get_selection()
                (model, row) = _selection.get_selected()
                _mechanism_id = model.get_value(row, 0)
                _parent =  model.get_string_from_iter(row)

                if(_parent.count(':') != 1):
                    _util.application_error(_(u"An action can only be the child of a failure mechanism, not another action, failure mode, or control."))
                    return True

# Find the id of the grand-parent failure mode.
                row = model.iter_parent(row)
                _mode_id = model.get_value(row, 0)

# Find the id of the next control.
                query = "SELECT seq FROM sqlite_sequence \
                         WHERE name='tbl_fmeca_actions'"
                _next_id = self._app.DB.execute_query(query,
                                                      None,
                                                      self._app.ProgCnx)

                if(not _next_id):
                    _next_id = 0
                else:
                    _next_id = _next_id[0][0] + 1

# Insert the new action.
                query = "INSERT INTO tbl_fmeca_actions \
                         (fld_assembly_id, fld_mode_id, \
                          fld_mechanism_id, fld_action_id, fld_parent) \
                         VALUES (%d, %d, %d, %d, '%s')" % (self.assembly_id,
                                                           _mode_id,
                                                           _mechanism_id,
                                                           _next_id,
                                                           _parent)
                self._app.DB.execute_query(query,
                                           None,
                                           self._app.ProgCnx,
                                           True)
                self._fmeca_tab_load()

            elif(_button_ == 'Remove'):
                selection = self.tvwFMECA.get_selection()
                (model, row) = selection.get_selected()

                _fmeca_len = len(self._FMECA_col_order)
                _type = model.get_value(row, _fmeca_len)
                _id = model.get_value(row, 0)

                if(_type == 0):
# Delete the failure mode from the FMECA table, then delete associated failure
# mechanisms, controls, and actions.
                    query = "DELETE FROM tbl_fmeca \
                             WHERE fld_mode_id=%d" % _id
                    self._app.DB.execute_query(query,
                                               None,
                                               self._app.ProgCnx,
                                               True)

                    query = "DELETE FROM tbl_fmeca_mechanisms \
                             WHERE fld_mode_id=%d" % _id
                    self._app.DB.execute_query(query,
                                               None,
                                               self._app.ProgCnx,
                                               True)

                    query = "DELETE FROM tbl_fmeca_controls \
                             WHERE fld_mode_id=%d" % _id
                    self._app.DB.execute_query(query,
                                               None,
                                               self._app.ProgCnx,
                                               True)

                    query = "DELETE FROM tbl_fmeca_actions \
                             WHERE fld_mode_id=%d" % _id
                    self._app.DB.execute_query(query,
                                               None,
                                               self._app.ProgCnx,
                                               True)
                elif(_type == 1):
# Delete the failure mechanism from the FMECA mechanisms table, then delete
# associated controls and actions.
                    query = "DELETE FROM tbl_fmeca_mechanisms \
                             WHERE fld_mechanism_id=%d" % _id
                    self._app.DB.execute_query(query,
                                               None,
                                               self._app.ProgCnx,
                                               True)

                    query = "DELETE FROM tbl_fmeca_controls \
                             WHERE fld_mechanism_id=%d" % _id
                    self._app.DB.execute_query(query,
                                               None,
                                               self._app.ProgCnx,
                                               True)

                    query = "DELETE FROM tbl_fmeca_actions \
                             WHERE fld_mechanism_id=%d" % _id
                    self._app.DB.execute_query(query,
                                               None,
                                               self._app.ProgCnx,
                                               True)
                elif(_type == 2):
# Delete the control from the FMECA controls table.
                    query = "DELETE FROM tbl_fmeca_controls \
                             WHERE fld_control_id=%d" % _id
                    self._app.DB.execute_query(query,
                                               None,
                                               self._app.ProgCnx,
                                               True)
                elif(_type == 3):
# Delete the control from the FMECA actions table.
                    query = "DELETE FROM tbl_fmeca_actions \
                             WHERE fld_action_id=%d" % _id
                    self._app.DB.execute_query(query,
                                               None,
                                               self._app.ProgCnx,
                                               True)

                self._fmeca_tab_load()

            elif(_button_ == 'Analyze'):
# Calculate the MIL-STD-1629A and automotive RPN criticalities.
                (self._CA,
                 self._ItemCA,
                 self._RPN) = _calc.criticality_analysis(self._CA,
                                                         self._ItemCA,
                                                         self._RPN)

# Update the RTK program database with the MIL-STD-1629A results.
                _query = "UPDATE tbl_fmeca \
                          SET fld_mode_criticality=%g, \
                              fld_mode_failure_rate=%g \
                          WHERE fld_mode_id=%d"

                _keys = self._CA.keys()
                for i in range(len(_keys)):
                    _values = (self._CA[_keys[i]][4], self._CA[_keys[i]][5],
                               _keys[i])
                    query = _query % _values

                    _results = self._app.DB.execute_query(query,
                                                          None,
                                                          self._app.ProgCnx,
                                                          commit=True)

# Update the RTK program database with the automotive RPN results.
                _query = "UPDATE tbl_fmeca_mechanisms \
                          SET fld_rpn=%d, fld_rpn_new=%d \
                          WHERE fld_mechanism_id=%d"

                _keys = self._RPN.keys()
                for i in range(len(_keys)):
                    _values = (self._RPN[_keys[i]][3], self._RPN[_keys[i]][7],
                               _keys[i])
                    query = _query % _values
                    _results = self._app.DB.execute_query(query,
                                                          None,
                                                          self._app.ProgCnx,
                                                          commit=True)

# Update the RTK program database with the MIL-STD-1629A item criticality.
                _query = "UPDATE tbl_system \
                          SET fld_assembly_criticality='%s' \
                          WHERE fld_assembly_id=%d"

                _keys = self._ItemCA.keys()
                for i in range(len(_keys)):
                    _values = (self._ItemCA[_keys[i]][-1], _keys[i])
                    query = _query % _values
                    _results = self._app.DB.execute_query(query,
                                                          None,
                                                          self._app.ProgCnx,
                                                          commit=True)

                self._fmeca_tab_load()

            elif(_button_ == 'Save'):
                self._fmeca_save()
        elif(_page_ == 7):                  # Maintenance planning tab.
            if(_button_ == 'Add'):
                print "Add maintenance activity"
            elif(_button_ == 'Remove'):
                print "Remove maintenance activity"
            elif(_button_ == 'Analyze'):
                print "Maintenance costs"
            elif(_button_ == 'Save'):
                print "Saving maintenance policy"

        return False
