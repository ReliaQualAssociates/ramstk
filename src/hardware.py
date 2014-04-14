#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to
the hardware of the Program.
"""

__author__ = 'Andrew Rowland <andrew.rowland@reliaqual.com>'
__copyright__ = 'Copyright 2007 - 2014 Andrew Rowland'

# -*- coding: utf-8 -*-
#
#       hardware.py is part of The RTK Project
#
# All rights reserved.

from datetime import datetime
import gettext
import locale
import sys

from lxml import etree
import matplotlib
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure

# Import other RTK modules.
from _assistants_.exports import ExportHardware
from _assistants_.imports import ImportHardware
import calculations as _calc
import configuration as _conf
import utilities as _util
import widgets as _widg

# Modules required for the GUI.
try:
    import pygtk  # @UnusedImport

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
    import gobject  # @UnusedImport
except ImportError:
    sys.exit(1)
try:
    import pango  # @UnusedImport
except ImportError:
    sys.exit(1)

from math import exp, log

# Modules required for plotting.
matplotlib.use('GTK')

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Hardware(object):
    """
    The HARDWARE
    """

    # TODO: Write code to update Work Book widgets when editing the
    # Module Book.

    def __init__(self, application):
        """
        Initializes the HARDWARE class.

        :param application: the RTK application.
        """

        # Define private HARDWARE class scalar attributes.
        self._app = application
        self._component = None
        self._system_ht = 1.0

        # Define private HARDWARE class dictionary attributes.
        self._treepaths = {}
        self._mission = {}
        self._mission_phase = {}
        self._assembly_risks_ = {}  # Assembly risk matrix values.
        self._system_risks_ = {}  # System risk matrix values.
        self._hrmodel = {}
        self._fmeca = {}
        self._mechanisms = {}
        self._fmeca_controls = {}
        self._fmeca_actions = {}
        self._CA = {}  # Carries MIL-STD-1629A values.
        self._ItemCA = {}  # Carries MIL-STD-1629A values.
        self._rpnsev = {}  # Carries RPN severity values.
        self._RPN = {}  # Carries RPN and new RPN values.

        # Define private HARDWARE class list attributes.
        self._col_order = []
        self._risk_col_order = []
        self._sia_col_order = []

        # Define public HARDWARE class scalar attributes.
        self.revision_id = 0
        self.assembly_id = 0
        self._add_adj_factor = 0.0
        self.allocation_type = 0
        self.alt_part_num = ''
        self.assembly_criticality = ''
        self.attachments = ''
        self.availability = 1.0
        self.availability_mission = 1.0
        self.cage_code = ''
        self.calculation_model = 1
        self.category_id = 0
        self.comp_ref_des = ''
        self.cost = 0.0
        self.cost_per_failure = 0.0
        self.cost_per_hour = 0.0
        self.cost_type = 0
        self.description = ''
        self.detection_fr = 0.0
        self.detection_percent = 100.0
        self.duty_cycle = 100.0
        self.entered_by = ''
        self.environment_active = 0
        self.environment_dormant = 0
        self.failure_dist = 0
        self.failure_parameter_1 = 0.0
        self.failure_parameter_2 = 0.0
        self.failure_parameter_3 = 0.0
        self.failure_rate = 0.0
        self.failure_rate_lcl = 0.0
        self.failure_rate_ucl = 0.0
        self.failure_rate_active = 0.0
        self.failure_rate_dormant = 0.0
        self.failure_rate_mission = 0.0
        self.failure_rate_percent = 0.0
        self.failure_rate_software = 0.0
        self.failure_rate_specified = 0.0
        self.failure_rate_type = 1
        self.figure_number = ''
        self.humidity = 50.0
        self.image_file = ''
        self.isolation_fr = 0.0
        self.isolation_percent = 0.0
        self.lcn = ''
        self.level = 0
        self.manufacturer = 0
        self.mission_time = 100.0
        self.modified_by = ''
        self.mcmt = 0.0
        self.mmt = 0.0
        self.mpmt = 0.0
        self.mtbf = 0.0
        self.mtbf_lcl = 0.0
        self.mtbf_ucl = 0.0
        self.mtbf_mission = 0.0
        self.mtbf_specified = 0.0
        self.mttr = 0.0
        self.mttr_specified = 0.0
        self.mttr_add_adj_factor = 0.0
        self.mttr_mult_adj_factor = 1.0
        self.mttr_type = 1
        self.mult_adj_factor = 1.0
        self.name = ''
        self.nsn = ''
        self.overstress = False
        self.page_number = ''
        self.parent_assembly = '0'
        self.part = False
        self.part_number = ''
        self.percent_isolation_group_ri = 0.0
        self.percent_isolation_single_ri = 0.0
        self.quantity = 1
        self.ref_des = ''
        self.reliability_mission = 1.0
        self.reliability = 1.0
        self.remarks = ''
        self.repair_dist = 0
        self.repair_parameter_1 = 0.0
        self.repair_parameter_2 = 0.0
        self.repairable = False
        self.rpm = 0.0
        self.specification = ''
        self.subcategory_id = 0
        self.tagged = False
        self.temperature_active = 30.0
        self.temperature_dormant = 30.0
        self.n_parts = 0
        self.total_power = 0.0
        self.vibration = 0.0
        self.weibull_data_set = 1
        self.weibull_file = ''
        self.year_of_manufacture = 2002
        self.ht_model = ''
        self.rel_goal_measure = 0
        self.rel_goal = 1.0

        self.assembly = None
        self.system_ht = 0.0

        # Component-specific attributes.
        self.burnin_temp = 0.0
        self.burnin_time = 0.0
        self.lab_devices = 0.0
        self.lab_time = 0.0
        self.lab_temp = 0.0
        self.lab_failures = 0.0
        self.field_time = 0.0
        self.field_failures = 0.0
        self.min_temp = 0.0
        self.knee_temp = 0.0
        self.max_temp = 0.0
        self.rated_current = 0.0
        self.rated_power = 0.0
        self.rated_voltage = 0.0
        self.op_current = 0.0
        self.op_power = 0.0
        self.op_voltage = 0.0
        self.current_ratio = 1.0
        self.voltage_ratio = 1.0
        self.power_ratio = 1.0
        self.theta_jc = 0.0
        self.temp_rise = 0.0
        self.case_temp = 0.0

        # Define public HARDWARE class dictionary attributes.
        #        self.dicHARDWARE = {}

        # Create the main HARDWARE class treeview.
        (self.treeview,
         self._col_order) = _widg.make_treeview('Hardware', 3, self._app,
                                                None, _conf.RTK_COLORS[6],
                                                _conf.RTK_COLORS[7])

        # Toolbar widgets.
        self.btnAddSibling = gtk.ToolButton()
        self.btnAddChild = gtk.ToolButton()
        self.btnRemoveHardware = gtk.ToolButton()
        self.btnAddItem = gtk.ToolButton()
        self.btnFMECAAdd = gtk.MenuToolButton(None, label="")
        self.btnRemoveItem = gtk.ToolButton()
        self.btnAnalyze = gtk.ToolButton()
        self.btnSaveResults = gtk.ToolButton()
        self.btnRollup = gtk.ToolButton()
        self.btnEdit = gtk.ToolButton()

        # General Data page widgets.
        self.chkRepairable = _widg.make_check_button()
        self.chkTagged = _widg.make_check_button()
        self.cmbCategory = _widg.make_combo(simple=False)
        self.cmbManufacturer = _widg.make_combo(simple=False)
        self.cmbSubcategory = _widg.make_combo(simple=False)
        self.lblCategory = _widg.make_label(_(u"Category:"))
        self.lblSubcategory = _widg.make_label(_(u"Subcategory:"))
        self.txtName = _widg.make_entry()
        self.txtPartNum = _widg.make_entry()
        self.txtAltPartNum = _widg.make_entry()
        self.txtRefDes = _widg.make_entry()
        self.txtCompRefDes = _widg.make_entry()
        self.txtQuantity = _widg.make_entry()
        self.txtDescription = _widg.make_entry(width=700)
        self.txtCAGECode = _widg.make_entry()
        self.txtLCN = _widg.make_entry()
        self.txtNSN = _widg.make_entry()
        self.txtYearMade = _widg.make_entry()
        self.txtSpecification = _widg.make_entry()
        self.txtPageNum = _widg.make_entry()
        self.txtFigNum = _widg.make_entry()
        self.txtImageFile = _widg.make_entry()
        self.txtAttachments = _widg.make_entry()
        self.txtMissionTime = _widg.make_entry()
        self.txtRevisionID = _widg.make_entry(width=50, editable=False)
        self.txtRemarks = _widg.make_text_view(width=400)

        # Diagrams page widgets.
        # TODO: Implement Diagram Worksheet for HARDWARE.

        # Allocation page widgets.
        self.chkApplyResults = _widg.make_check_button(_(u"Apply results to "
                                                         u"hardware"))
        self.cmbAllocationType = _widg.make_combo(_width_=125)
        self.cmbRqmtType = _widg.make_combo(_width_=125)
        self.hbxAllocation = gtk.HBox()
        self.lblAllocation = gtk.Label()
        self.tvwAllocation = gtk.TreeView()
        self.txtReliabilityGoal = _widg.make_entry(width=125)
        self.txtMTBFGoal = _widg.make_entry(width=125)
        self.txtFailureRateGoal = _widg.make_entry(width=125)
        self.txtNumElements = _widg.make_entry(width=125,
                                               editable=False,
                                               bold=True)
        self.txtOperTime = _widg.make_entry(width=125)

        # Hazard Analysis page widgets.
        self.hpnHazardAnalysis = gtk.HPaned()
        self.lblHazardAnalysis = gtk.Label()
        self.tvwRisk = gtk.TreeView()
        self.tvwRiskMap = gtk.TreeView()

        # Similar Item Analysis page widgets.
        self.fraSIA = _widg.make_frame()
        self.lblSIA = gtk.Label()
        self.tvwSIA = gtk.TreeView()

        # Assessment Input page widgets.
        self.cmbHRType = _widg.make_combo()
        self.cmbCalcModel = _widg.make_combo()
        self.cmbFailDist = _widg.make_combo()
        self.cmbActEnviron = _widg.make_combo()
        self.cmbDormantEnviron = _widg.make_combo()
        self.cmbMTTRType = _widg.make_combo()
        self.cmbRepairDist = _widg.make_combo()
        self.cmbCostType = _widg.make_combo(200, 30)
        self.lblNoCategory = _widg.make_label(_(u"No category selected for "
                                                u"this part."),
                                              width=400)
        self.lblNoSubCategory = _widg.make_label(_(u"No subcategory selected "
                                                   u"for this part."),
                                                 width=400)
        self.txtSpecifiedHt = _widg.make_entry()
        self.txtSpecifiedMTBF = _widg.make_entry()
        self.txtSoftwareHt = _widg.make_entry()
        self.txtAddAdj = _widg.make_entry(width=100)
        self.txtMultAdj = _widg.make_entry(width=100)
        self.txtAllocationWF = _widg.make_entry(width=100)
        self.txtFailScale = _widg.make_entry(width=100)
        self.txtFailShape = _widg.make_entry(width=100)
        self.txtFailLoc = _widg.make_entry(width=100)
        self.txtActTemp = _widg.make_entry(width=100)
        self.txtDormantTemp = _widg.make_entry(width=100)
        self.txtDutyCycle = _widg.make_entry(width=100)
        self.txtHumidity = _widg.make_entry(width=100)
        self.txtVibration = _widg.make_entry(width=100)
        self.txtRPM = _widg.make_entry(width=100)
        self.txtWeibullFile = _widg.make_entry(width=200)
        self.txtSpecifiedMTTR = _widg.make_entry()
        self.txtMTTRAddAdj = _widg.make_entry(width=100)
        self.txtMTTRMultAdj = _widg.make_entry(width=100)
        self.txtRepairScale = _widg.make_entry(width=100)
        self.txtRepairShape = _widg.make_entry(width=100)
        self.txtCost = _widg.make_entry(width=100)

        # Component-specific input widgets.
        self.fxdRelInputQuad1 = gtk.Fixed()
        self.fxdRelInputQuad4 = gtk.Fixed()
        self.txtBurnInTemp = _widg.make_entry(width=100)
        self.txtBurnInTime = _widg.make_entry(width=100)
        self.txtLabDevices = _widg.make_entry(width=100)
        self.txtLabTime = _widg.make_entry(width=100)
        self.txtLabTemp = _widg.make_entry(width=100)
        self.txtLabFailures = _widg.make_entry(width=100)
        self.txtFieldTime = _widg.make_entry(width=100)
        self.txtFieldFailures = _widg.make_entry(width=100)
        self.txtMinTemp = _widg.make_entry(width=100)
        self.txtKneeTemp = _widg.make_entry(width=100)
        self.txtMaxTemp = _widg.make_entry(width=100)
        self.txtRatedVoltage = _widg.make_entry(width=100)
        self.txtOpVoltage = _widg.make_entry(width=100)
        self.txtRatedCurrent = _widg.make_entry(width=100)
        self.txtOpCurrent = _widg.make_entry(width=100)
        self.txtRatedPower = _widg.make_entry(width=100)
        self.txtOpPower = _widg.make_entry(width=100)
        self.txtThetaJC = _widg.make_entry(width=100)
        self.txtTempRise = _widg.make_entry(width=100)
        self.txtCaseTemp = _widg.make_entry(width=100)

        # Assessment Results page widgets.
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
        self.txtMPMT = _widg.make_entry(editable=False, bold=True)
        self.txtMCMT = _widg.make_entry(editable=False, bold=True)
        self.txtMTTR = _widg.make_entry(editable=False, bold=True)
        self.txtMMT = _widg.make_entry(editable=False, bold=True)
        self.txtAvailability = _widg.make_entry(editable=False, bold=True)
        self.txtMissionAt = _widg.make_entry(editable=False, bold=True)
        self.txtTotalCost = _widg.make_entry(width=100, editable=False,
                                             bold=True)
        self.txtCostFailure = _widg.make_entry(width=100, editable=False,
                                               bold=True)
        self.txtCostHour = _widg.make_entry(width=100, editable=False,
                                            bold=True)
        self.txtAssemblyCrit = _widg.make_entry(width=300, editable=False,
                                                bold=True)
        self.txtPartCount = _widg.make_entry(width=100, editable=False,
                                             bold=True)
        self.txtTotalPwr = _widg.make_entry(width=100, editable=False,
                                            bold=True)

        # Component-specific results widgets.
        self.chkOverstressed = _widg.make_check_button()
        self.figDerate = Figure(figsize=(6, 4))
        self.fraDerate = gtk.Frame()
        self.fxdCalcResultsQuad4 = gtk.Fixed()
        self.pltDerate = FigureCanvas(self.figDerate)
        self.txtAssemblyCrit = _widg.make_entry(editable=False, bold=True)
        self.txtPartCount = _widg.make_entry(width=100, editable=False,
                                             bold=True)
        self.txtTotalPwr = _widg.make_entry(width=100, editable=False,
                                            bold=True)
        self.txtVoltageRatio = _widg.make_entry(width=100, editable=False,
                                                bold=True)
        self.txtCurrentRatio = _widg.make_entry(width=100, editable=False,
                                                bold=True)
        self.txtPwrRatio = _widg.make_entry(width=100, editable=False,
                                            bold=True)
        self.txtOSReason = gtk.TextBuffer()

        # FMEA/FMECA page widgets.
        (self.tvwFMECA,
         self._FMECA_col_order) = _widg.make_treeview('FMECA', 9,
                                                      self._app,
                                                      None,
                                                      _conf.RTK_COLORS[6],
                                                      _conf.RTK_COLORS[7])

        # Add background color and editable attributes so failure mechanisms,
        # controls, and actions will not be editable in the FMECA worksheet.
        _cols_ = len(self._FMECA_col_order)
        _columns_ = self.tvwFMECA.get_columns()
        for i in range(len(_columns_)):
            _cells_ = _columns_[i].get_cell_renderers()

            # Always allow editing of the first column since this is the
            # description column.
            if i == 1:
                _cells_[0].set_property('background', '#FFFFFF')
                _cells_[0].set_property('editable', True)
            else:
                try:
                    if _cells_[0].get_property('editable'):
                        _columns_[i].add_attribute(_cells_[0], 'background',
                                                   _cols_ + 1)
                        _columns_[i].add_attribute(_cells_[0], 'editable',
                                                   _cols_ + 2)
                except TypeError:
                    pass

        self.fraFMECADetails = _widg.make_frame(_label_=_(u"Failure Mechanism "
                                                          u"Details"))

        # Create the widgets to display the failure mode details.
        _labels = [_(u"This failure mode is evident to the operating "
                     u"crew\nwhile performing normal duties."),
                   _(u"This failure mode causes a functional loss or "
                     u"secondary\ndamage that could have a direct, adverse "
                     u"effect\non operating safety."),
                   _(u"This hidden failure mode by itself or in "
                     u"combination\nwith another failure has an adverse "
                     u"effect on\noperating safety."),
                   _(u"Safety Hidden"), _(u"Safety Evident"),
                   _(u"Non-Safety Hidden"), _(u"Economic/Operational")]

        self.fxdMode = gtk.Fixed()
        self.chkFCQ1 = _widg.make_check_button(_label_=_labels[0])
        self.chkFCQ2 = _widg.make_check_button(_label_=_labels[1])
        self.chkFCQ3 = _widg.make_check_button(_label_=_labels[2])
        self.optHS = _widg.make_option_button(_label_=_labels[3])
        self.optES = _widg.make_option_button(_group_=self.optHS,
                                              _label_=_labels[4])
        self.optNSH = _widg.make_option_button(_group_=self.optHS,
                                               _label_=_labels[5])
        self.optEO = _widg.make_option_button(_group_=self.optHS,
                                              _label_=_labels[6])
        self.txtFCQ1 = _widg.make_text_view(buffer_=gtk.TextBuffer(),
                                            width=400, height=75)
        self.txtFCQ2 = _widg.make_text_view(buffer_=gtk.TextBuffer(),
                                            width=400, height=75)
        self.txtFCQ3 = _widg.make_text_view(buffer_=gtk.TextBuffer(),
                                            width=400, height=75)

        # Create the widgets to display the failure mechanism/cause details.
        self.fxdMechanism = gtk.Fixed()
        self.cmbOccurenceI = _widg.make_combo()
        self.cmbDetectionI = _widg.make_combo()
        self.cmbOccurrenceN = _widg.make_combo()
        self.cmbDetectionN = _widg.make_combo()
        self.txtMechanismID = _widg.make_entry(width=50, editable=False)
        self.txtMechanismDescription = _widg.make_entry()
        self.txtRPNI = _widg.make_entry(width=50, editable=False)
        self.txtRPNN = _widg.make_entry(width=50, editable=False)

        # Create the widgets to display the current controls details.
        self.fxdControl = gtk.Fixed()
        self.cmbControlType = _widg.make_combo()
        self.txtControlID = _widg.make_entry(width=50, editable=False)
        self.txtControlDescription = _widg.make_entry()

        # Create the widgets to display the recommended action details.
        self.fxdAction = gtk.Fixed()
        self.cmbActionCategory = _widg.make_combo()
        self.cmbActionStatus = _widg.make_combo()
        self.cmbActionResponsible = _widg.make_combo()
        self.cmbActionApproved = _widg.make_combo()
        self.cmbActionClosed = _widg.make_combo()
        self.txtActionID = _widg.make_entry(width=50, editable=False)
        self.txtActionDueDate = _widg.make_entry(width=100)
        self.txtActionApproveDate = _widg.make_entry(width=100)
        self.txtActionCloseDate = _widg.make_entry(width=100)
        self.txtActionRecommended = _widg.make_text_view(width=375, height=75)
        self.txtActionTaken = _widg.make_text_view(width=375, height=75)

        # Maintenance Planning page widgets.
        # SSI and FSI status widgets.
        _labels = [_(u"This item is a major load carrying element."),
                   _(u"The loss of this item's function results in an "
                     u"adverse effect on operating safety or aborts the "
                     u"mission."),
                   _(u"The actual or predicted failure rate and consumption "
                     u"of resources is high."),
                   _(u"The item, or a like item on similar equipment, has "
                     u"existing scheduled maintenance requirements."),
                   _(u"This item is Structurally Significant"),
                   _(u"This item is Functionally Significant")]

        self.chkFSIQ1 = _widg.make_check_button(_label_=_labels[0])
        self.chkFSIQ2 = _widg.make_check_button(_label_=_labels[1])
        self.chkFSIQ3 = _widg.make_check_button(_label_=_labels[2])
        self.chkFSIQ4 = _widg.make_check_button(_label_=_labels[3])
        self.chkSSI = _widg.make_check_button(_label_=_labels[4])
        self.chkFSI = _widg.make_check_button(_label_=_labels[5])

        self.txtFSIQ1 = _widg.make_text_view(buffer_=gtk.TextBuffer(),
                                             width=400, height=75)
        self.txtFSIQ2 = _widg.make_text_view(buffer_=gtk.TextBuffer(),
                                             width=400, height=75)
        self.txtFSIQ3 = _widg.make_text_view(buffer_=gtk.TextBuffer(),
                                             width=400, height=75)
        self.txtFSIQ4 = _widg.make_text_view(buffer_=gtk.TextBuffer(),
                                             width=400, height=75)

        # Put it all together.
        _toolbar = self._create_toolbar()

        self.notebook = self._create_notebook()

        self.vbxHardware = gtk.VBox()
        self.vbxHardware.pack_start(_toolbar, expand=False)
        self.vbxHardware.pack_end(self.notebook)

        self._selected_tab = 0

        self.notebook.connect('switch-page', self._notebook_page_switched)

    def create_tree(self):
        """
        Creates the HARDWARE class gtk.TreeView() and connects it to callback
        functions to handle editting.  Background and foreground colors can be
        set using the user-defined values in the RTK configuration file.
        """

        self.treeview.set_tooltip_text(_(u"Displays an indentured list (tree) "
                                         u"of hardware."))
        self.treeview.set_enable_tree_lines(True)

        self.treeview.set_search_column(0)
        self.treeview.set_reorderable(True)

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)

        _scrollwindow_ = gtk.ScrolledWindow()
        _scrollwindow_.add(self.treeview)

        return _scrollwindow_

    def _create_toolbar(self):
        """
        Method to create the toolbar for the HARDWARE class work book.
        """

        toolbar = gtk.Toolbar()

        _pos = 0

        # Add sibling assembly button.
        self.btnAddSibling.set_tooltip_text(_(u"Adds a new assembly at the "
                                              u"same indenture level as the "
                                              u"selected assembly to the RTK "
                                              u"Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
        self.btnAddSibling.set_icon_widget(image)
        self.btnAddSibling.connect('clicked', self._add_hardware, 0)
        toolbar.insert(self.btnAddSibling, _pos)
        _pos += 1

        # Add child assembly button.
        self.btnAddChild.set_tooltip_text(_(u"Adds a new assembly one "
                                            u"indenture level subordinate to "
                                            u"the selected assembly to the "
                                            u"RTK Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_child.png')
        self.btnAddChild.set_icon_widget(image)
        self.btnAddChild.connect('clicked', self._add_hardware, 1)
        toolbar.insert(self.btnAddChild, _pos)
        _pos += 1

        # Delete assembly button
        self.btnRemoveHardware.set_tooltip_text(_(u"Removes the currently "
                                                  u"selected assembly from "
                                                  u"the RTK Program "
                                                  u"Database."))
        _image_ = gtk.Image()
        _image_.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        self.btnRemoveHardware.set_icon_widget(_image_)
        self.btnRemoveHardware.connect('clicked', self._delete_hardware)
        toolbar.insert(self.btnRemoveHardware, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

        # Add item button.  Depending on the notebook page selected will
        # determine what type of item is added.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        self.btnAddItem.set_icon_widget(image)
        self.btnAddItem.set_name('Add')
        self.btnAddItem.connect('clicked', self._toolbutton_pressed)
        self.btnAddItem.set_tooltip_text(_(u"Add components to the currently "
                                           u"selected assembly."))
        toolbar.insert(self.btnAddItem, _pos)
        _pos += 1

        self.btnFMECAAdd.set_tooltip_text(_(u"Add items to the active "
                                            u"FMEA/FMECA."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        self.btnFMECAAdd.set_icon_widget(image)
        menu = gtk.Menu()
        menu_item = gtk.MenuItem(label=_(u"Mode"))
        menu_item.set_tooltip_text(_(u"Add a new failure mode to the "
                                     u"currently selected assembly."))
        menu_item.connect('activate', self._toolbutton_pressed)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_(u"Mechanism"))
        menu_item.set_tooltip_text(_(u"Add a new failure mechanism to the "
                                     u"currently selected failure mode."))
        menu_item.connect('activate', self._toolbutton_pressed)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_(u"Control"))
        menu_item.set_tooltip_text(_(u"Add a new control to the currently "
                                     u"selected failure mechanism."))
        menu_item.connect('activate', self._toolbutton_pressed)
        menu.add(menu_item)
        menu_item = gtk.MenuItem(label=_(u"Action"))
        menu_item.set_tooltip_text(_(u"Add a new action to the currently "
                                     u"selected failure mechanism."))
        menu_item.connect('activate', self._toolbutton_pressed)
        menu.add(menu_item)
        self.btnFMECAAdd.set_menu(menu)
        menu.show_all()
        self.btnFMECAAdd.show()
        toolbar.insert(self.btnFMECAAdd, _pos)
        _pos += 1

        # Remove item button.  Depending on the notebook page selected will
        # determine what type of item is removed.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        self.btnRemoveItem.set_icon_widget(image)
        self.btnRemoveItem.set_name('Remove')
        self.btnRemoveItem.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnRemoveItem, _pos)
        _pos += 1

        # Perform analysis button.  Depending on the notebook page selected
        # will determine which analysis is executed.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        self.btnAnalyze.set_icon_widget(image)
        self.btnAnalyze.set_name('Analyze')
        self.btnAnalyze.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnAnalyze, _pos)
        _pos += 1

        # Save results button.  Depending on the notebook page selected will
        # determine which results are saved.
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

        self.btnAddItem.show()
        self.btnFMECAAdd.hide()
        self.btnRemoveItem.hide()
        self.btnAnalyze.hide()
        self.btnSaveResults.hide()
        self.btnRollup.hide()
        self.btnEdit.hide()

        return toolbar

    def _create_notebook(self):
        """
        Method to create the HARDWARE class gtk.Notebook().

        :rtype : gtk.Notebook
        """

        def _create_general_data_tab(self, notebook):
            """
            Function to create the HARDWARE class gtk.Notebook() page for
            displaying general data about the selected HARDWARE.

            :param self: the current instance of a HARDWARE class.
            :type self: Hardware object
            :param notebook: the HARDWARE class gtk.Notebook() widget.
            :type notebook: gtk.Notebook
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hbox_ = gtk.HBox()
            _vpaned = gtk.VPaned()

            # Build the quadrant 1 (upper left) containers.
            _fxdGenDataQuad1_ = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fxdGenDataQuad1_)

            _frame = _widg.make_frame(_label_=_(u"General Information"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            _vpaned.pack1(_frame, True, True)

            # Build the quadrant 3 (lower left) containers.
            _fxdGenDataQuad3_ = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fxdGenDataQuad3_)

            _frame = _widg.make_frame(_label_=_(u"Manufacturer Information"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            _vpaned.pack2(_frame, True, True)

            _hbox_.pack_start(_vpaned)

            # Build the quadrant 2 (upper right) containers.
            _vpaned = gtk.VPaned()

            _fxdGenDataQuad2_ = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fxdGenDataQuad2_)

            _frame = _widg.make_frame(_label_=_(u"Specification Information"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            _vpaned.pack1(_frame, True, True)

            # Build the quadrant 4 (lower right) containers.
            _fxdGenDataQuad4_ = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fxdGenDataQuad4_)

            _frame = _widg.make_frame(_label_=_(u"Miscellaneous Information"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            _vpaned.pack2(_frame, True, True)

            _hbox_.pack_start(_vpaned)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display general information.        #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Load the gtk.ComboBox() widgets.
            _query = "SELECT * FROM tbl_category \
                      ORDER BY fld_category_noun ASC"
            _results = self._app.COMDB.execute_query(_query, None,
                                                     self._app.ComCnx)

            try:
                _n_categories = len(_results)
            except TypeError:
                _n_categories = 0

            _model = self.cmbCategory.get_model()
            _model.clear()
            _model.append(None, ['', 0, ''])
            for i in range(_n_categories):
                _model.append(None, [_results[i][1], _results[i][0], ''])

            _query = "SELECT fld_manufacturers_noun, fld_location, \
                             fld_cage_code \
                      FROM tbl_manufacturers \
                      ORDER BY fld_manufacturers_noun ASC"
            _results = self._app.COMDB.execute_query(_query, None,
                                                     self._app.ComCnx)
            _widg.load_combo(self.cmbManufacturer, _results, False)

            # Create the labels for quadrant #1.
            _labels = [_(u"Assembly Name:"), _(u"Part Number:"),
                       _(u"Alternate Part #:"), "", "",
                       _(u"Ref Designator:"), _(u"Composite Ref Des:"),
                       _(u"Quantity:"), _(u"Description:")]

            _max1 = 0
            _max2 = 0
            (_max1_,
             _y_pos1_) = _widg.make_labels(_labels, _fxdGenDataQuad1_, 5, 5)

            # Create the labels for quadrant #3.
            _labels = [_(u"Manufacturer:"), _(u"CAGE Code:"), _(u"LCN:"),
                       _(u"NSN:"), _(u"Manufacture Year:")]
            (_max2,
             _y_pos2_) = _widg.make_labels(_labels, _fxdGenDataQuad3_, 5, 5)
            _x_pos_ = max(_max1, _max2) + 20

            # Place the quadrant #1 widgets.
            self.txtName.set_tooltip_text(_(u"Displays the name of the "
                                            u"selected assembly."))
            _fxdGenDataQuad1_.put(self.txtName, _x_pos_, _y_pos1_[0])
            self.txtName.connect('focus-out-event',
                                 self._callback_entry, 'text', 58)

            self.txtPartNum.set_tooltip_text(_(u"Displays the part number of "
                                               u"the selected assembly."))
            _fxdGenDataQuad1_.put(self.txtPartNum, _x_pos_, _y_pos1_[1])
            self.txtPartNum.connect('focus-out-event',
                                    self._callback_entry, 'text', 64)

            self.txtAltPartNum.set_tooltip_text(_(u"Displays an alternative "
                                                  u"part number for the "
                                                  u"selected assembly."))
            _fxdGenDataQuad1_.put(self.txtAltPartNum, _x_pos_, _y_pos1_[2])
            self.txtAltPartNum.connect('focus-out-event',
                                       self._callback_entry, 'text', 4)

            self.cmbCategory.set_tooltip_text(_(u"Select the part type for "
                                                u"this component."))
            _fxdGenDataQuad1_.put(self.lblCategory, 5, _y_pos1_[3])
            _fxdGenDataQuad1_.put(self.cmbCategory, _x_pos_, _y_pos1_[3])
            self.cmbCategory.connect('changed', self._callback_combo, 511)

            self.cmbSubcategory.set_tooltip_text(_(u"Select the part sub-type "
                                                   u"for this component."))
            _fxdGenDataQuad1_.put(self.lblSubcategory, 5, _y_pos1_[4])
            _fxdGenDataQuad1_.put(self.cmbSubcategory, _x_pos_, _y_pos1_[4])
            self.cmbSubcategory.connect('changed', self._callback_combo, 578)

            self.txtRefDes.set_tooltip_text(_(u"Displays the reference "
                                              u"designator of the selected "
                                              u"assembly."))
            _fxdGenDataQuad1_.put(self.txtRefDes, _x_pos_, _y_pos1_[5])
            self.txtRefDes.connect('focus-out-event',
                                   self._callback_entry, 'text', 68)

            self.txtCompRefDes.set_tooltip_text(_(u"Displays the composite "
                                                  u"reference designator of "
                                                  u"the selected assembly."))
            _fxdGenDataQuad1_.put(self.txtCompRefDes, _x_pos_, _y_pos1_[6])
            self.txtCompRefDes.connect('focus-out-event',
                                       self._callback_entry, 'text', 12)

            self.txtQuantity.set_tooltip_text(_(u"Displays the quantity of "
                                                u"the selected assembly."))
            _fxdGenDataQuad1_.put(self.txtQuantity, _x_pos_, _y_pos1_[7])
            self.txtQuantity.connect('focus-out-event',
                                     self._callback_entry, 'int', 67)

            self.txtDescription.set_tooltip_text(_(u"Displays the description "
                                                   u"of the selected "
                                                   u"assembly."))
            _fxdGenDataQuad1_.put(self.txtDescription, _x_pos_, _y_pos1_[8])
            self.txtDescription.connect('focus-out-event',
                                        self._callback_entry, 'text', 17)

            _fxdGenDataQuad1_.show_all()

            # Place the quadrant #3 widgets.
            self.cmbManufacturer.set_tooltip_text(_(u"Displays the "
                                                    u"manufacturer of the "
                                                    u"selected assembly."))
            _fxdGenDataQuad3_.put(self.cmbManufacturer, _x_pos_, _y_pos2_[0])
            self.cmbManufacturer.connect('changed',
                                         self._callback_combo, 43)

            self.txtCAGECode.set_tooltip_text(_(u"Displays the Commercial and "
                                                u"Government Entity (CAGE) "
                                                u"code of the selected "
                                                u"assembly."))
            _fxdGenDataQuad3_.put(self.txtCAGECode, _x_pos_, _y_pos2_[1])
            self.txtCAGECode.connect('focus-out-event',
                                     self._callback_entry, 'text', 9)

            self.txtLCN.set_tooltip_text(_(u"Displays the logistics control "
                                           u"number (LCN) of the selected "
                                           u"assembly."))
            _fxdGenDataQuad3_.put(self.txtLCN, _x_pos_, _y_pos2_[2])
            self.txtLCN.connect('focus-out-event',
                                self._callback_entry, 'text', 41)

            self.txtNSN.set_tooltip_text(_(u"Displays the national stock "
                                           u"number (NSN) of the selected "
                                           u"assembly."))
            _fxdGenDataQuad3_.put(self.txtNSN, _x_pos_, _y_pos2_[3])
            self.txtNSN.connect('focus-out-event',
                                self._callback_entry, 'text', 59)

            self.txtYearMade.set_tooltip_text(_(u"Displays the year the "
                                                u"selected assembly was "
                                                u"manufactured."))
            _fxdGenDataQuad3_.put(self.txtYearMade, _x_pos_, _y_pos2_[4])
            self.txtYearMade.connect('focus-out-event',
                                     self._callback_entry, 'int', 87)

            _fxdGenDataQuad3_.show_all()

            # Create the labels for quadrant #2.
            _labels = [_(u"Specification:"), _(u"Page Number:"),
                       _(u"Figure Number:"), _(u"Image File:"),
                       _(u"Attachments:"), _(u"Mission Time:")]

            _max1 = 0
            _max2 = 0
            (_max1,
             _y_pos1_) = _widg.make_labels(_labels, _fxdGenDataQuad2_, 5, 5)

            # Create the labels for quadrant #4.
            _labels = [_(u"Revision ID:"), _(u"Repairable?"), _(u"Tagged?"),
                       _(u"Remarks:")]
            (_max2,
             _y_pos2_) = _widg.make_labels(_labels, _fxdGenDataQuad4_, 5, 5)
            _x_pos_ = max(_max1, _max2) + 20

            # Place the quadrant #2 widgets.
            self.txtSpecification.set_tooltip_text(_(u"Displays the governing "
                                                     u"specification for the "
                                                     u"selected assembly, if "
                                                     u"any."))
            _fxdGenDataQuad2_.put(self.txtSpecification, _x_pos_, _y_pos1_[0])
            self.txtSpecification.connect('focus-out-event',
                                          self._callback_entry, 'text', 77)

            self.txtPageNum.set_tooltip_text(_(u"Displays the governing "
                                               u"specification page number "
                                               u"for the selected assembly."))
            _fxdGenDataQuad2_.put(self.txtPageNum, _x_pos_, _y_pos1_[1])
            self.txtPageNum.connect('focus-out-event',
                                    self._callback_entry, 'text', 61)

            self.txtFigNum.set_tooltip_text(_(u"Displays the governing "
                                              u"specification figure number "
                                              u"for the selected assembly."))
            _fxdGenDataQuad2_.put(self.txtFigNum, _x_pos_, _y_pos1_[2])
            self.txtFigNum.connect('focus-out-event',
                                   self._callback_entry, 'text', 36)

            self.txtImageFile.set_tooltip_text(_(u"Displays the URL to an "
                                                 u"image of the selected "
                                                 u"assembly."))
            _fxdGenDataQuad2_.put(self.txtImageFile, _x_pos_, _y_pos1_[3])
            self.txtImageFile.connect('focus-out-event',
                                      self._callback_entry, 'text', 38)

            self.txtAttachments.set_tooltip_text(_(u"Displays the URL to an "
                                                   u"attachment associated "
                                                   u"with the selected "
                                                   u"assembly."))
            _fxdGenDataQuad2_.put(self.txtAttachments, _x_pos_, _y_pos1_[4])
            self.txtAttachments.connect('focus-out-event',
                                        self._callback_entry, 'text', 6)

            self.txtMissionTime.set_tooltip_text(_(u"Displays the mission "
                                                   u"time for the selected "
                                                   u"assembly."))
            _fxdGenDataQuad2_.put(self.txtMissionTime, _x_pos_, _y_pos1_[5])
            self.txtMissionTime.connect('focus-out-event',
                                        self._callback_entry, 'float', 45)

            _fxdGenDataQuad2_.show_all()

            # Place the quadrant #4 widgets.
            self.txtRevisionID.set_tooltip_text(_(u"Displays the currently "
                                                  u"selected revision."))
            _fxdGenDataQuad4_.put(self.txtRevisionID, _x_pos_, _y_pos2_[0])

            self.chkRepairable.set_tooltip_text(_(u"Indicates whether or not "
                                                  u"the selected assembly is "
                                                  u"repairable."))
            _fxdGenDataQuad4_.put(self.chkRepairable, _x_pos_, _y_pos2_[1])
            self.chkRepairable.connect('toggled', self._callback_check, 75)

            self.chkTagged.set_tooltip_text(_(u"Indicates whether or not the "
                                              u"selected assembly is tagged.  "
                                              u"A tagged assembly has no "
                                              u"specific meaning."))
            _fxdGenDataQuad4_.put(self.chkTagged, _x_pos_, _y_pos2_[2])
            self.chkTagged.connect('toggled', self._callback_check, 79)

            self.txtRemarks.set_tooltip_text(_(u"Enter any remarks associated "
                                               u"with the selected assembly."))
            _fxdGenDataQuad4_.put(self.txtRemarks, _x_pos_, _y_pos2_[3])
            self.txtRemarks.get_child().get_child().connect(
                'focus-out-event', self._callback_entry, 'text', 71)

            _fxdGenDataQuad4_.show_all()

            # Insert the tab.
            _label = gtk.Label()
            _label.set_markup("<span weight='bold'>" +
                              _(u"General\nData") + "</span>")
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.show_all()
            _label.set_tooltip_text(_(u"Displays general information about "
                                      u"the selected assembly."))

            notebook.insert_page(_hbox_,
                                 tab_label=_label,
                                 position=-1)

            return False

        def _create_allocation_tab(self, notebook):
            """
            Function to create the HARDWARE class gtk.Notebook() page for
            displaying the reliability allocation analysis for the selected
            HARDWARE.

            :param self: the current instance of a HARDWARE class.
            :type self: Hardware object
            :param notebook: the HARDWARE class gtk.Notebook() widget.
            :type notebook: gtk.Notebook
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _scrollwindow_ = gtk.ScrolledWindow()
            _scrollwindow_.set_policy(gtk.POLICY_AUTOMATIC,
                                      gtk.POLICY_AUTOMATIC)
            _scrollwindow_.add(self.tvwAllocation)

            _frame_ = _widg.make_frame(_label_=_(u"Allocation Inputs"))
            _frame_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame_.add(_scrollwindow_)

            self.hbxAllocation.pack_start(_frame_)

            _fixed_ = gtk.Fixed()

            _frame_ = _widg.make_frame(_label_=_(u"Calculations"))
            _frame_.add(_fixed_)

            self.hbxAllocation.pack_start(_frame_, expand=False)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display the allocation analysis.    #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _labels_ = [_(u"Measure:"), _(u"Reliability:"), _(u"MTTF/MTBF:"),
                        _(u"Failure Rate:"), _(u"Allocation Type:"),
                        _(u"Elements:"), _(u"Operating Time:")]

            (_x_pos_, _y_pos_) = _widg.make_labels(_labels_, _fixed_, 5, 5)
            _x_pos_ += 30

            # Widgets to display allocation results.
            _labels = [_(u"Revision ID"), _(u"Assembly ID"), _(u"Description"),
                       _(u"Included?"), _(u"Number of\nSub-Systems"),
                       _(u"Number of\nSub-Elements"), _(u"Operating\nTime"),
                       _(u"Duty Cycle"), _(u"Intricacy\n(1-10)"),
                       _(u"State of\nthe Art\n(1-10)"),
                       _(u"Operating\nTime (1-10)"), _(u"Environment\n(1-10)"),
                       _(u"Weighting\nFactor"),
                       _(u"Percent\nWeighting\nFactor"),
                       _(u"Current\nFailure\nRate"),
                       _(u"Allocated\nFailure\nRate"),
                       _(u"Current\nMTBF"), _(u"Allocated\nMTBF"),
                       _(u"Current\nReliability"),
                       _(u"Allocated\nReliability"),
                       _(u"Current\nAvailability"),
                       _(u"Allocated\nAvailability")]

            _model_ = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_INT,
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
            self.tvwAllocation.set_model(_model_)
            self.tvwAllocation.set_tooltip_text(_(u"Displays the list of "
                                                  u"immediate child "
                                                  u"assemblies that may be "
                                                  u"included in the "
                                                  u"allocation."))

            _cols_ = int(len(_labels))
            for i in range(_cols_):
                if i == 3:
                    _cell_ = gtk.CellRendererToggle()
                    _cell_.set_property('activatable', 1)
                    _cell_.connect('toggled', _widg.edit_tree,
                                   None, i, _model_)
                else:
                    _cell_ = gtk.CellRendererText()
                    _cell_.set_property('editable', 1)
                    _cell_.set_property('wrap-width', 250)
                    _cell_.set_property('wrap-mode', pango.WRAP_WORD)
                    _cell_.set_property('background', 'white')
                    _cell_.set_property('foreground', 'black')
                    _cell_.connect('edited', _widg.edit_tree, i,
                                   _model_)

                _column_ = gtk.TreeViewColumn()
                _column_.pack_start(_cell_, True)
                if i == 3:
                    _column_.set_attributes(_cell_, active=i)
                else:
                    _column_.set_attributes(_cell_, text=i)

                # _column_.set_visible(0)

                _label_ = gtk.Label()
                _label_.set_alignment(xalign=0.5, yalign=0.5)
                _label_.set_justify(gtk.JUSTIFY_CENTER)
                _label_.set_line_wrap(True)
                _label_.set_markup("<span weight='bold'>%s</span>" %
                                   _labels[i])
                _label_.set_use_markup(True)
                _label_.show_all()

                _column_.set_widget(_label_)

                self.tvwAllocation.append_column(_column_)

            self.tvwAllocation.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

            self.cmbRqmtType.set_tooltip_text(_(u"Selects the reliability "
                                                u"goal measure for the active "
                                                u"revision."))
            _fixed_.put(self.cmbRqmtType, _x_pos_, _y_pos_[0])
            _results_ = [[_(u"Reliability"), 0], [_(u"MTTF/MTBF"), 1],
                         [_(u"Failure Intensity"), 2]]
            _widg.load_combo(self.cmbRqmtType, _results_)
            self.cmbRqmtType.connect('changed', self._callback_combo, 500)

            self.txtReliabilityGoal.set_tooltip_text(_(u"Displays the "
                                                       u"reliability goal "
                                                       u"value for the active "
                                                       u"revision.  Editable "
                                                       u"if reliability goal "
                                                       u"measure is "
                                                       u"Reliability."))
            _fixed_.put(self.txtReliabilityGoal, _x_pos_, _y_pos_[1])
            self.txtReliabilityGoal.props.editable = 0
            self.txtReliabilityGoal.set_sensitive(0)
            self.txtReliabilityGoal.connect('focus-out-event',
                                            self._callback_entry, 'float', 500)

            self.txtMTBFGoal.set_tooltip_text(_(u"Displays the MTBF goal for "
                                                u"the active revision.  "
                                                u"Editable if reliability "
                                                u"goal measure is MTBF."))
            _fixed_.put(self.txtMTBFGoal, _x_pos_, _y_pos_[2])
            self.txtMTBFGoal.props.editable = 0
            self.txtMTBFGoal.set_sensitive(0)
            self.txtMTBFGoal.connect('focus-out-event', self._callback_entry,
                                     'float', 501)

            self.txtFailureRateGoal.set_tooltip_text(_(u"Displays the failure "
                                                       u"intensity goal for "
                                                       u"the active revision. "
                                                       u"Editable if "
                                                       u"reliability goal "
                                                       u"measure is Failure "
                                                       u"Intensity."))
            _fixed_.put(self.txtFailureRateGoal, _x_pos_, _y_pos_[3])
            self.txtFailureRateGoal.props.editable = 0
            self.txtFailureRateGoal.set_sensitive(0)
            self.txtFailureRateGoal.connect('focus-out-event',
                                            self._callback_entry, 'float', 502)

            self.cmbAllocationType.set_tooltip_text(_(u"Select the reliability"
                                                      u" allocation method for"
                                                      u" the selected "
                                                      u"assembly."))
            _fixed_.put(self.cmbAllocationType, _x_pos_, _y_pos_[4])
            _results_ = [[_(u"Equal Apportionment"), 0],
                         [_(u"AGREE Apportionment"), 1],
                         [_(u"ARINC Apportionment"), 2],
                         [_(u"Feasibility of Objectives"), 3]]
            _widg.load_combo(self.cmbAllocationType, _results_)
            self.cmbAllocationType.connect('changed',
                                           self._callback_combo, 501)

            self.txtNumElements.set_tooltip_text(_(u"Display the total number "
                                                   u"of sub-systems included "
                                                   u"in the allocation "
                                                   u"analysis."))
            _fixed_.put(self.txtNumElements, _x_pos_, _y_pos_[5])

            self.txtOperTime.set_tooltip_text(_(u"Displays the operating time "
                                                u"over which the allocation "
                                                u"is calculated."))
            _fixed_.put(self.txtOperTime, _x_pos_, _y_pos_[6])

            self.chkApplyResults.set_tooltip_text(_(u"Sets the hardware's "
                                                    u"specified failure "
                                                    u"intensity to use the "
                                                    u"allocation results."))
            _fixed_.put(self.chkApplyResults, 5, _y_pos_[6] + 30)

            _fixed_.show_all()

            # Insert the tab.
            self.lblAllocation.set_markup("<span weight='bold'>" +
                                          _(u"Allocation") + "</span>")
            self.lblAllocation.set_alignment(xalign=0.5, yalign=0.5)
            self.lblAllocation.set_justify(gtk.JUSTIFY_CENTER)
            self.lblAllocation.show_all()
            self.lblAllocation.set_tooltip_text(_(u"Displays reliability "
                                                  u"allocation calculations "
                                                  u"for the selected "
                                                  u"assembly."))

            notebook.insert_page(self.hbxAllocation,
                                 tab_label=self.lblAllocation,
                                 position=-1)

            return False

        def _create_hazard_analysis_tab(self, notebook):
            """
            Function to create the HARDWARE class gtk.Notebook() page for
            displaying the hazard analysis for the selected HARDWARE.

            :param self: the current instance of a HARDWARE class.
            :type self: HARDWARE object instance
            :param notebook: the HARDWARE class gtk.Notebook() widget.
            :type notebook: gtk.Notebook
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _scrollwindow_ = gtk.ScrolledWindow()
            _scrollwindow_.set_policy(gtk.POLICY_AUTOMATIC,
                                      gtk.POLICY_AUTOMATIC)
            _scrollwindow_.add(self.tvwRisk)

            _frame_ = _widg.make_frame()
            _frame_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame_.add(_scrollwindow_)

            self.hpnHazardAnalysis.pack1(_frame_, resize=True, shrink=False)

            _scrollwindow_ = gtk.ScrolledWindow()
            _scrollwindow_.set_policy(gtk.POLICY_AUTOMATIC,
                                      gtk.POLICY_AUTOMATIC)
            _scrollwindow_.add(self.tvwRiskMap)

            _frame_ = _widg.make_frame()
            _frame_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame_.add(_scrollwindow_)

            self.hpnHazardAnalysis.pack2(_frame_, resize=False, shrink=True)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display the hazard analysis.        #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _path_ = "/root/tree[@name='Risk']/column/usertitle"
            _heading_ = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(_path_)

            _path_ = "/root/tree[@name='Risk']/column/datatype"
            _datatype_ = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(_path_)

            _path_ = "/root/tree[@name='Risk']/column/widget"
            _widget_ = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(_path_)

            _path_ = "/root/tree[@name='Risk']/column/position"
            _position_ = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(_path_)

            _path_ = "/root/tree[@name='Risk']/column/editable"
            _editable_ = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(_path_)

            _path_ = "/root/tree[@name='Risk']/column/visible"
            _visible_ = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(_path_)

            # Create a list of GObject datatypes to pass to the model.
            _types_ = []
            for i in range(len(_position_)):
                _types_.append(_datatype_[i].text)

            _gobject_types_ = []
            _gobject_types_ = [gobject.type_from_name(_types_[ix])
                               for ix in range(len(_types_))]

            # Retrieve the list of hazards to include in the hazard analysis
            # worksheet.
            _query_ = "SELECT fld_category, \
                              fld_subcategory \
                       FROM tbl_hazards"
            _hazards_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)

            # Retrieve the list of hazard severities to include in the hazard
            # analysis worksheet.
            _query_ = "SELECT fld_criticality_name, fld_criticality_value \
                       FROM tbl_criticality \
                       ORDER BY fld_criticality_value DESC"
            _severity_ = self._app.COMDB.execute_query(_query_,
                                                       None,
                                                       self._app.ComCnx)

            # Retrieve the list of hazard probabilities to include in the
            # hazard analysis worksheet.
            _query_ = "SELECT fld_probability_name, fld_probability_value \
                       FROM tbl_failure_probability"
            _probability_ = self._app.COMDB.execute_query(_query_,
                                                          None,
                                                          self._app.ComCnx)

            bg_color = _conf.RTK_COLORS[6]
            fg_color = _conf.RTK_COLORS[7]

            # Create the model and treeview for the hazard analysis worksheet.
            _model_ = gtk.TreeStore(*_gobject_types_)
            self.tvwRisk.set_model(_model_)

            _cols_ = int(len(_heading_))
            for i in range(_cols_):
                self._risk_col_order.append(int(_position_[i].text))

                if _widget_[i].text == 'combo':
                    _cell_ = gtk.CellRendererCombo()
                    _cellmodel_ = gtk.ListStore(gobject.TYPE_STRING)

                    _cellmodel_.append([""])
                    if i == 3:
                        for j in range(len(_hazards_)):
                            _cellmodel_.append([_hazards_[j][0] +
                                                ", " + _hazards_[j][1]])
                    elif i == 6 or i == 10 or i == 14 or i == 18:
                        for j in range(len(_severity_)):
                            _cellmodel_.append([_severity_[j][0]])
                    elif i == 7 or i == 11 or i == 15 or i == 19:
                        for j in range(len(_probability_)):
                            _cellmodel_.append([_probability_[j][0]])

                    # Prevent users from adding new values.
                    _cell_.set_property('has-entry', False)
                    _cell_.set_property('model', _cellmodel_)
                    _cell_.set_property('text-column', 0)
                    _cell_.connect('changed', _widg.edit_tree,
                                   int(_position_[i].text), _model_)
                elif _widget_[i].text == 'spin':
                    _cell_ = gtk.CellRendererSpin()
                    _adjustment_ = gtk.Adjustment(upper=5.0, step_incr=0.05)
                    _cell_.set_property('adjustment', _adjustment_)
                    _cell_.set_property('digits', 2)
                else:
                    _cell_ = gtk.CellRendererText()

                _cell_.set_property('editable', int(_editable_[i].text))
                if int(_editable_[i].text) == 0:
                    _cell_.set_property('background', 'light gray')
                else:
                    _cell_.set_property('background', bg_color)
                    _cell_.set_property('foreground', fg_color)
                    _cell_.set_property('wrap-width', 250)
                    _cell_.set_property('wrap-mode', pango.WRAP_WORD)
                    _cell_.connect('edited', _widg.edit_tree,
                                   int(_position_[i].text), _model_)

                _label_ = gtk.Label()
                _label_.set_line_wrap(True)
                _label_.set_alignment(xalign=0.5, yalign=0.5)
                _label_.set_justify(gtk.JUSTIFY_CENTER)
                _text_ = _heading_[i].text.replace("  ", "\n")
                _label_.set_markup("<span weight='bold'>" + _text_ + "</span>")
                _label_.set_use_markup(True)
                _label_.show_all()

                _column_ = gtk.TreeViewColumn()
                _column_.set_visible(int(_visible_[i].text))
                _column_.pack_start(_cell_, True)
                _column_.set_attributes(_cell_, text=int(_position_[i].text))

                _column_.set_widget(_label_)

                _column_.set_cell_data_func(_cell_, _widg.format_cell,
                                            (int(_position_[i].text),
                                             _datatype_[i].text))
                _column_.set_resizable(True)
                _column_.connect('notify::width', _widg.resize_wrap, _cell_)

                if i > 0:
                    _column_.set_reorderable(True)

                self.tvwRisk.append_column(_column_)

            self.tvwRisk.set_tooltip_text(_(u"Displays the risk analysis for "
                                            u"the selected assembly."))
            self.tvwRisk.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

            # Create the gtk.TreeModel() and gtk.TreeView() for the risk
            # matrix.
            #
            # Index     Information
            #   0       Criticality category
            #   1       Criticality value
            #   2       Count of probability 1      (index 5, 8, 11, etc.)
            #   3       Value of probability 1      (index 6, 9, 12, etc.)
            #   4       Cell background color code  (index 7, 10, 13, etc.)
            _model_ = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
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
            self.tvwRiskMap.set_model(_model_)

            _label_ = gtk.Label()
            _label_.set_line_wrap(True)
            _label_.set_alignment(xalign=0.5, yalign=0.5)
            _label_.set_justify(gtk.JUSTIFY_LEFT)
            _text_ = u"\t\tProbability\nSeverity"
            _label_.set_markup("<span weight='bold'>" + _text_ + "</span>")
            _label_.set_use_markup(True)
            _label_.show_all()

            _cell_ = gtk.CellRendererText()  # Severity noun name.
            _cell_.set_property('visible', True)
            _cell_.set_property('editable', False)
            _cell_.set_property('background', 'light gray')
            _column_ = gtk.TreeViewColumn()
            _column_.set_widget(_label_)
            _column_.set_visible(True)
            _column_.pack_start(_cell_, True)
            _column_.set_attributes(_cell_, text=0)

            _cell_ = gtk.CellRendererText()  # Severity multiplier.
            _cell_.set_property('visible', False)
            _column_.pack_start(_cell_, True)
            _column_.set_attributes(_cell_, text=1)
            self.tvwRiskMap.append_column(_column_)

            _width_ = int(_column_.get_property('width'))

            j = 2
            for i in range(len(_probability_)):
                _label_ = gtk.Label()
                _label_.set_line_wrap(True)
                _label_.set_alignment(xalign=0.5, yalign=0.5)
                _label_.set_justify(gtk.JUSTIFY_CENTER)
                _text_ = _probability_[i][0]
                _text_ = _text_.replace(" ", "\n")
                _label_.set_markup("<span weight='bold'>" + _text_ + "</span>")
                _label_.set_use_markup(True)
                _label_.show_all()

                _column_ = gtk.TreeViewColumn()
                _column_.set_widget(_label_)
                _column_.set_visible(True)
                _column_.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
                _cell_ = gtk.CellRendererText()  # Quantity of hazards.
                _cell_.set_property('visible', True)
                _cell_.set_property('xalign', 0.5)
                _cell_.set_property('yalign', 0.5)
                _column_.pack_start(_cell_, True)
                _column_.set_attributes(_cell_, text=j, background=j + 2)

                _cell_ = gtk.CellRendererText()  # Frequency multiplier.
                _cell_.set_property('visible', False)
                _column_.pack_start(_cell_, True)
                _column_.set_attributes(_cell_, text=j + 1)

                _cell_ = gtk.CellRendererText()  # Cell background color.
                _cell_.set_property('visible', False)
                _column_.pack_start(_cell_, True)
                _column_.set_attributes(_cell_, text=j + 2)
                self.tvwRiskMap.append_column(_column_)

                j += 3

            _column_ = gtk.TreeViewColumn()
            _column_.set_visible(True)
            self.tvwRiskMap.append_column(_column_)

            for i in range(len(_severity_)):
                self._assembly_risks_[_severity_[i][0]] = [_severity_[i][1]]
                self._system_risks_[_severity_[i][0]] = [_severity_[i][1]]
                _data_ = [_severity_[i][0],
                          self._assembly_risks_[_severity_[i][0]][0]]
                _prob_ = {}
                for j in range(len(_probability_)):
                    _risk = _severity_[i][1] * _probability_[j][1]
                    if _risk <= _conf.RTK_RISK_POINTS[0]:
                        _color_ = '#90EE90'  # Green
                    elif _risk > _conf.RTK_RISK_POINTS[0] and \
                                    _risk <= _conf.RTK_RISK_POINTS[1]:
                        _color_ = '#FFFF79'  # Yellow
                    else:
                        _color_ = '#FFC0CB'  # Red

                    _prob_[_probability_[j][0]] = [0, _probability_[j][1],
                                                   _color_]
                    _data_.append(0)
                    _data_.append(_probability_[j][1])
                    _data_.append(_color_)

                self._assembly_risks_[_severity_[i][0]].append(_prob_)
                self._system_risks_[_severity_[i][0]].append(_prob_)
                _model_.append(_data_)

            self.tvwRiskMap.set_size_request(575, -1)
            self.tvwRiskMap.set_tooltip_text(_(u"Displays the risk matrix for "
                                               u"the selected assembly."))
            self.tvwRiskMap.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

            self.lblHazardAnalysis.set_markup("<span weight='bold'>" +
                                              _(u"Hazard\nAnalysis") +
                                              "</span>")
            self.lblHazardAnalysis.set_alignment(xalign=0.5, yalign=0.5)
            self.lblHazardAnalysis.set_justify(gtk.JUSTIFY_CENTER)
            self.lblHazardAnalysis.show_all()
            self.lblHazardAnalysis.set_tooltip_text(_(u"Displays the hazard "
                                                      u"analysis for the "
                                                      u"selected assembly."))

            notebook.insert_page(self.hpnHazardAnalysis,
                                 tab_label=self.lblHazardAnalysis,
                                 position=-1)

            return False

        def _create_similar_item_tab(self, notebook):
            """
            Function to create the HARDWARE class gtk.Notebook() page for
            displaying the similar item analysis for the selected HARDWARE.

            :param self: the current instance of a HARDWARE class.
            :type self: Hardware object
            :param notebook: the HARDWARE class gtk.Notebook() widget.
            :type notebook: gtk.Notebook
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _scrollwindow_ = gtk.ScrolledWindow()
            _scrollwindow_.set_policy(gtk.POLICY_AUTOMATIC,
                                      gtk.POLICY_AUTOMATIC)
            _scrollwindow_.add(self.tvwSIA)

            self.fraSIA.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            self.fraSIA.add(_scrollwindow_)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display the similar item analysis.  #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _query_ = "SELECT fld_category_noun, fld_category_value \
                       FROM tbl_risk_category"
            _risk_category_ = self._app.COMDB.execute_query(_query_,
                                                            None,
                                                            self._app.ComCnx)

            _path_ = "/root/tree[@name='SIA']/column/usertitle"
            _heading_ = etree.parse(_conf.RTK_FORMAT_FILE[8]).xpath(_path_)

            _path_ = "/root/tree[@name='SIA']/column/datatype"
            _datatype_ = etree.parse(_conf.RTK_FORMAT_FILE[8]).xpath(_path_)

            _path_ = "/root/tree[@name='SIA']/column/widget"
            _widget_ = etree.parse(_conf.RTK_FORMAT_FILE[8]).xpath(_path_)

            _path_ = "/root/tree[@name='SIA']/column/position"
            _position_ = etree.parse(_conf.RTK_FORMAT_FILE[8]).xpath(_path_)

            _path_ = "/root/tree[@name='SIA']/column/editable"
            _editable_ = etree.parse(_conf.RTK_FORMAT_FILE[8]).xpath(_path_)

            _path_ = "/root/tree[@name='SIA']/column/visible"
            _visible_ = etree.parse(_conf.RTK_FORMAT_FILE[8]).xpath(_path_)

            # Create a list of GObject datatypes to pass to the model.
            _types_ = []
            for i in range(len(_position_)):
                _types_.append(_datatype_[i].text)

            _gobject_types_ = []
            _gobject_types_ = [gobject.type_from_name(_types_[ix])
                               # @UndefinedVariable
                               for ix in range(len(_types_))]

            # Create the model and treeview.
            _model_ = gtk.TreeStore(*_gobject_types_)
            self.tvwSIA.set_model(_model_)

            _cols_ = int(len(_heading_))
            for i in range(_cols_):
                self._sia_col_order.append(int(_position_[i].text))

                if _widget_[i].text == 'combo':
                    _cell_ = gtk.CellRendererCombo()
                    _cellmodel_ = gtk.ListStore(gobject.TYPE_STRING,
                                                gobject.TYPE_INT)

                    for j in range(len(_risk_category_)):
                        _cellmodel_.append(_risk_category_[j])

                    _cell_.set_property('has-entry', False)
                    _cell_.set_property('model', _cellmodel_)
                    _cell_.set_property('text-column', 0)
                    _cell_.connect('changed', self._callback_combo_cell,
                                   int(_position_[i].text), _model_, _cols_)
                elif _widget_[i].text == 'spin':
                    _cell_ = gtk.CellRendererSpin()
                    _adjustment_ = gtk.Adjustment(upper=5.0, step_incr=0.05)
                    _cell_.set_property('adjustment', _adjustment_)
                    _cell_.set_property('digits', 2)
                elif _widget_[i].text == 'blob':
                    _cell_ = _widg.CellRendererML()
                else:
                    _cell_ = gtk.CellRendererText()

                _cell_.set_property('editable', int(_editable_[i].text))
                if int(_editable_[i].text) == 0:
                    _cell_.set_property('background', 'light gray')
                else:
                    _cell_.set_property('background', _conf.RTK_COLORS[6])
                    _cell_.set_property('foreground', _conf.RTK_COLORS[7])
                    _cell_.set_property('wrap-width', 250)
                    _cell_.set_property('wrap-mode', pango.WRAP_WORD)
                    _cell_.connect('edited', _widg.edit_tree,
                                   int(_position_[i].text), _model_)

                _label_ = gtk.Label()
                _label_.set_line_wrap(True)
                _label_.set_alignment(xalign=0.5, yalign=0.5)
                _label_.set_justify(gtk.JUSTIFY_CENTER)
                _text_ = _heading_[i].text.replace("  ", "\n")
                _label_.set_markup("<span weight='bold'>" + _text_ + "</span>")
                _label_.set_use_markup(True)
                _label_.show_all()

                _column_ = gtk.TreeViewColumn()
                _column_.set_visible(int(_visible_[i].text))
                _column_.pack_start(_cell_, True)
                _column_.set_attributes(_cell_, text=int(_position_[i].text))

                _column_.set_widget(_label_)

                _column_.set_cell_data_func(_cell_, _widg.format_cell,
                                            (int(_position_[i].text),
                                             _datatype_[i].text))
                _column_.set_resizable(True)
                _column_.connect('notify::width', _widg.resize_wrap, _cell_)

                if i > 0:
                    _column_.set_reorderable(True)

                self.tvwSIA.append_column(_column_)

            self.tvwSIA.set_tooltip_text(_(
                u"Displays the similar items analysis for the selected Assembly."))
            self.tvwSIA.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

            _heading_ = _(u"Similar Item\nAnalysis")
            self.lblSIA.set_markup(
                "<span weight='bold'>" + _heading_ + "</span>")
            self.lblSIA.set_alignment(xalign=0.5, yalign=0.5)
            self.lblSIA.set_justify(gtk.JUSTIFY_CENTER)
            self.lblSIA.show_all()
            self.lblSIA.set_tooltip_text(_(
                u"Displays the similar item analysis for the selected Assembly."))

            notebook.insert_page(self.fraSIA,
                                 tab_label=self.lblSIA,
                                 position=-1)

            return False

        def _create_assessment_inputs_tab(self, notebook):
            """
            Function to create the HARDWARE class gtk.Notebook() page for
            displaying the assessment inputs for the selected HARDWARE.

            Keyword Arguments:
            self     -- the current instance of a HARDWARE class.
            notebook -- the HARDWARE class gtk.Notebook() widget.
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build the quadrant 1 (upper left) containers.
            _fxdRelInputQuad1_ = gtk.Fixed()

            _hbox_ = gtk.HBox()

            _scrollwindow_ = gtk.ScrolledWindow()
            _scrollwindow_.set_policy(gtk.POLICY_AUTOMATIC,
                                      gtk.POLICY_AUTOMATIC)
            _scrollwindow_.add_with_viewport(_hbox_)

            _frame_ = _widg.make_frame(_label_=_(u"Reliability Inputs"))
            _frame_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame_.add(_scrollwindow_)

            _hbox_.pack_start(_fxdRelInputQuad1_, expand=False)
            _hbox_.pack_end(self.fxdRelInputQuad1, expand=False)

            _hbox_ = gtk.HBox()
            _hbox_.pack_start(_frame_)

            # Build the quadrant 2 (upper right) containers.
            _vpaned_ = gtk.VPaned()
            _hbox_.pack_start(_vpaned_)

            _fxdRelInputQuad2_ = gtk.Fixed()

            _frame_ = _widg.make_frame(_label_=_(u"Maintainability Inputs"))
            _frame_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame_.add(_fxdRelInputQuad2_)

            _vpaned_.pack1(_frame_)

            # Build the quadrant 4 (lower right) containers.
            _fxdRelInputQuad4_ = gtk.Fixed()

            _hbox1_ = gtk.HBox()

            _scrollwindow_ = gtk.ScrolledWindow()
            _scrollwindow_.set_policy(gtk.POLICY_AUTOMATIC,
                                      gtk.POLICY_AUTOMATIC)
            _scrollwindow_.add_with_viewport(_hbox1_)

            _frame_ = _widg.make_frame(_label_=_(u"Miscellaneous Inputs"))
            _frame_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame_.add(_scrollwindow_)

            _hbox1_.pack_start(_fxdRelInputQuad4_, expand=False)
            _hbox1_.pack_end(self.fxdRelInputQuad4, expand=False)

            _vpaned_.pack2(_frame_)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display the assessment inputs.      #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Create the labels for quadrant #1.
            _labels_ = [_(u"Failure Rate [h(t)] Type:"),
                        _(u"Calculation Model:"),
                        _(u"Specified h(t):"), _(u"Specified MTBF:"),
                        _(u"Software h(t):"), _(u"Additive Adj:"),
                        _(u"Multiplicative Adj:"), _(u"Allocation Weight:"),
                        _(u"Failure Distribution:"), _(u"Scale:"),
                        _(u"Shape:"),
                        _(u"Location:"), _(u"Active Environ:"),
                        _(u"Active Temp:"), _(u"Dormant Environ:"),
                        _(u"Dormant Temp:"), _(u"Duty Cycle:"),
                        _(u"Humidity:"),
                        _(u"Vibration:"), _(u"RPM:"), _(u"Weibull File:")]

            (_x_pos_,
             _y_pos_) = _widg.make_labels(_labels_, _fxdRelInputQuad1_, 5, 5)
            _x_pos_ += 30

            if not self.part:
                _labels_ = [_(u"Burn-In Temp:"), _(u"Burn-In Time:"),
                            _(u"# of Lab Devices:"), _(u"Lab Test Time:"),
                            _(u"Lab Test Temp:"), _(u"# of Lab Failures:"),
                            _(u"Field Op Time:"), _(u"# of Field Failures:")]
                (_x_pos_r_,
                 _y_pos_r_) = _widg.make_labels(_labels_,
                                                self.fxdRelInputQuad1, 5, 5)
                _x_pos_r_ += 30

            # Place the quadrant #1 widgets.
            self.cmbHRType.set_tooltip_text(_(
                u"Selects the method of assessing the failure intensity for the selected assembly."))
            _fxdRelInputQuad1_.put(self.cmbHRType, _x_pos_, _y_pos_[0])
            _query_ = "SELECT fld_hr_type_noun FROM tbl_hr_type"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)
            _widg.load_combo(self.cmbHRType, _results_)
            self.cmbHRType.connect('changed', self._callback_combo, 35)

            self.cmbCalcModel.set_tooltip_text(_(
                u"Selects the reliability prediction model for the selected assembly."))
            _fxdRelInputQuad1_.put(self.cmbCalcModel, _x_pos_, _y_pos_[1])
            _query_ = "SELECT fld_model_noun FROM tbl_calculation_model"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)
            _widg.load_combo(self.cmbCalcModel, _results_)
            self.cmbCalcModel.connect('changed', self._callback_combo, 10)

            self.txtSpecifiedHt.set_tooltip_text(_(
                u"Displays the specified failure intensity for the selected assembly."))
            _fxdRelInputQuad1_.put(self.txtSpecifiedHt, _x_pos_, _y_pos_[2])
            self.txtSpecifiedHt.connect('focus-out-event',
                                        self._callback_entry, 'float', 34)

            self.txtSpecifiedMTBF.set_tooltip_text(_(
                u"Displays the specified mean time between failure (MTBF) for the selected assembly."))
            _fxdRelInputQuad1_.put(self.txtSpecifiedMTBF, _x_pos_, _y_pos_[3])
            self.txtSpecifiedMTBF.connect('focus-out-event',
                                          self._callback_entry, 'float', 51)

            self.txtSoftwareHt.set_tooltip_text(_(
                u"Displays the software failure rate for the selected assembly."))
            _fxdRelInputQuad1_.put(self.txtSoftwareHt, _x_pos_, _y_pos_[4])
            self.txtSoftwareHt.connect('focus-out-event',
                                       self._callback_entry, 'float', 33)

            self.txtAddAdj.set_tooltip_text(_(
                u"Displays any reliability assessment additive adjustment factor for the selected assembly."))
            _fxdRelInputQuad1_.put(self.txtAddAdj, _x_pos_, _y_pos_[5])
            self.txtAddAdj.connect('focus-out-event',
                                   self._callback_entry, 'float', 2)

            self.txtMultAdj.set_tooltip_text(_(
                u"Displays any reliability assessment multiplicative adjustment factor for the selected assembly."))
            _fxdRelInputQuad1_.put(self.txtMultAdj, _x_pos_, _y_pos_[6])
            self.txtMultAdj.connect('focus-out-event',
                                    self._callback_entry, 'float', 57)

            self.txtAllocationWF.set_tooltip_text(_(
                u"Displays the reliability allocation weighting factor for the selected assembly."))
            _fxdRelInputQuad1_.put(self.txtAllocationWF, _x_pos_, _y_pos_[7])
            self.txtAllocationWF.connect('focus-out-event',
                                         self._callback_entry, 'float', 3)

            self.cmbFailDist.set_tooltip_text(_(
                u"Selects the distribution of times to failure for the selected assembly."))
            _fxdRelInputQuad1_.put(self.cmbFailDist, _x_pos_, _y_pos_[8])
            _query_ = "SELECT fld_distribution_noun FROM tbl_distributions"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)
            _widg.load_combo(self.cmbFailDist, _results_)
            self.cmbFailDist.connect('changed', self._callback_combo, 24)

            self.txtFailScale.set_tooltip_text(
                _(u"Displays the time to failure distribution scale factor."))
            _fxdRelInputQuad1_.put(self.txtFailScale, _x_pos_, _y_pos_[9])
            self.txtFailScale.connect('focus-out-event',
                                      self._callback_entry, 'float', 25)

            self.txtFailShape.set_tooltip_text(
                _(u"Displays the time to failure distribution shape factor."))
            _fxdRelInputQuad1_.put(self.txtFailShape, _x_pos_, _y_pos_[10])
            self.txtFailShape.connect('focus-out-event',
                                      self._callback_entry, 'float', 26)

            self.txtFailLoc.set_tooltip_text(_(
                u"Displays the time to failure distribution location factor."))
            _fxdRelInputQuad1_.put(self.txtFailLoc, _x_pos_, _y_pos_[11])
            self.txtFailLoc.connect('focus-out-event',
                                    self._callback_entry, 'float', 27)

            self.cmbActEnviron.set_tooltip_text(_(
                u"Selects the active operating environment for the selected assembly."))
            _fxdRelInputQuad1_.put(self.cmbActEnviron, _x_pos_, _y_pos_[12])
            self.cmbActEnviron.connect('changed', self._callback_combo, 22)
            _query_ = "SELECT fld_active_environ_code, fld_active_environ_noun \
                       FROM tbl_active_environs"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)
            _model_ = self.cmbActEnviron.get_model()
            _model_.clear()
            self.cmbActEnviron.append_text('')
            for i in range(len(_results_)):
                self.cmbActEnviron.append_text(_results_[i][0] + ' - ' +
                                               _results_[i][1])

            self.txtActTemp.set_tooltip_text(_(
                u"Displays the active environment operating temperature for the selected assembly."))
            _fxdRelInputQuad1_.put(self.txtActTemp, _x_pos_, _y_pos_[13])
            self.txtActTemp.connect('focus-out-event',
                                    self._callback_entry, 'float', 80)

            self.cmbDormantEnviron.set_tooltip_text(_(
                u"Selects the dormant environment for the selected assembly."))
            _fxdRelInputQuad1_.put(self.cmbDormantEnviron, _x_pos_,
                                   _y_pos_[14])
            _query_ = "SELECT fld_dormant_environ_noun \
                       FROM tbl_dormant_environs"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)
            _widg.load_combo(self.cmbDormantEnviron, _results_)
            self.cmbDormantEnviron.connect('changed', self._callback_combo, 23)

            self.txtDormantTemp.set_tooltip_text(_(
                u"Displays the dormant environment temperature for the selected assembly."))
            _fxdRelInputQuad1_.put(self.txtDormantTemp, _x_pos_, _y_pos_[15])
            self.txtDormantTemp.connect('focus-out-event',
                                        self._callback_entry, 'float', 81)

            self.txtDutyCycle.set_tooltip_text(_(
                u"Displays the operating duty cycle for the selected assembly."))
            _fxdRelInputQuad1_.put(self.txtDutyCycle, _x_pos_, _y_pos_[16])
            self.txtDutyCycle.connect('focus-out-event',
                                      self._callback_entry, 'float', 20)

            self.txtHumidity.set_tooltip_text(_(
                u"Displays the active environment operating humidity for the selected assembly."))
            _fxdRelInputQuad1_.put(self.txtHumidity, _x_pos_, _y_pos_[17])
            self.txtHumidity.connect('focus-out-event',
                                     self._callback_entry, 'float', 37)

            self.txtVibration.set_tooltip_text(_(
                u"Displays the active environment operating vibration level for the selected assembly."))
            _fxdRelInputQuad1_.put(self.txtVibration, _x_pos_, _y_pos_[18])
            self.txtVibration.connect('focus-out-event',
                                      self._callback_entry, 'float', 84)

            self.txtRPM.set_tooltip_text(_(
                u"Displays the active environment operating RPM for the selected assembly."))
            _fxdRelInputQuad1_.put(self.txtRPM, _x_pos_, _y_pos_[19])
            self.txtRPM.connect('focus-out-event',
                                self._callback_entry, 'float', 76)

            self.txtWeibullFile.set_tooltip_text(_(
                u"Displays the URL to a survival analysis file for the selected assembly."))
            _fxdRelInputQuad1_.put(self.txtWeibullFile, _x_pos_, _y_pos_[20])
            self.txtWeibullFile.connect('focus-out-event',
                                        self._callback_entry, 'text', 86)

            # Place the right column of widgets.
            self.txtBurnInTemp.set_tooltip_text(_(
                u"Enter the temperature that the selected component will be burned-in."))
            self.fxdRelInputQuad1.put(self.txtBurnInTemp, _x_pos_r_,
                                      _y_pos_r_[0])
            self.txtBurnInTemp.connect('focus-out-event',
                                       self._callback_entry, 'float', 206)

            self.txtBurnInTime.set_tooltip_text(_(
                u"Enter the total time the selected component will be burned-in."))
            self.fxdRelInputQuad1.put(self.txtBurnInTime, _x_pos_r_,
                                      _y_pos_r_[1])
            self.txtBurnInTime.connect('focus-out-event',
                                       self._callback_entry, 'float', 207)

            self.txtLabDevices.set_tooltip_text(_(
                u"The total number of units that will be included in life testing in the laboratory."))
            self.fxdRelInputQuad1.put(self.txtLabDevices, _x_pos_r_,
                                      _y_pos_r_[2])
            self.txtLabDevices.connect('focus-out-event',
                                       self._callback_entry, "int", 220)

            self.txtLabTime.set_tooltip_text(_(
                u"The total time the units will undergo life testing in the laboratory."))
            self.fxdRelInputQuad1.put(self.txtLabTime, _x_pos_r_, _y_pos_r_[3])
            self.txtLabTime.connect('focus-out-event',
                                    self._callback_entry, 'float', 308)

            self.txtLabTemp.set_tooltip_text(_(
                u"The temperature the selected component will be exposed to during life testing in the laboratory."))
            self.fxdRelInputQuad1.put(self.txtLabTemp, _x_pos_r_, _y_pos_r_[4])
            self.txtLabTemp.connect('focus-out-event',
                                    self._callback_entry, 'float', 306)

            self.txtLabFailures.set_tooltip_text(_(
                u"The total number of failure observed during life testing in the laboratory."))
            self.fxdRelInputQuad1.put(self.txtLabFailures, _x_pos_r_,
                                      _y_pos_r_[5])
            self.txtLabFailures.connect('focus-out-event',
                                        self._callback_entry, "int", 227)

            self.txtFieldTime.set_tooltip_text(
                _(u"The total time that selected component has been fielded."))
            self.fxdRelInputQuad1.put(self.txtFieldTime, _x_pos_r_,
                                      _y_pos_r_[6])
            self.txtFieldTime.connect('focus-out-event',
                                      self._callback_entry, 'float', 265)

            self.txtFieldFailures.set_tooltip_text(_(
                u"The total number of failure of the selected component that have been observed in the field."))
            self.fxdRelInputQuad1.put(self.txtFieldFailures, _x_pos_r_,
                                      _y_pos_r_[7])
            self.txtFieldFailures.connect('focus-out-event',
                                          self._callback_entry, "int", 226)

            _fxdRelInputQuad1_.show_all()
            self.fxdRelInputQuad1.show_all()

            # Create the labels for quadrant #2.
            _labels_ = [_(u"MTTR Type:"), _(u"Specified MTTR:"),
                        _(u"Additive Adj:"), _(u"Multiplicative Adj:"),
                        _(u"Repair Distribution:"), _(u"Scale:"), _(u"Shape:")]

            _max1_ = 0
            _max2_ = 0
            (_max1_,
             _y_pos1_) = _widg.make_labels(_labels_, _fxdRelInputQuad2_, 5, 5)

            # Create the labels for quadrant #4.
            _labels_ = [_(u"Cost Type:"), _(u"Unit Cost:")]
            (_max2_,
             _y_pos2_) = _widg.make_labels(_labels_, _fxdRelInputQuad4_, 5, 5)
            _x_pos_ = max(_max1_, _max2_) + 20

            if not self.part:
                _labels_ = [_(u"Min Rated Temp:"), _(u"Knee Temp:"),
                            _(u"Max Rated Temp:"), _(u"Rated Voltage:"),
                            _(u"Operating Voltage:"), _(u"Rated Current:"),
                            _(u"Operating Current:"), _(u"Rated Power:"),
                            _(u"Operating Power:"), _(u"theta JC:"),
                            _(u"Temperature Rise:"), _(u"Case Temperature:")]
                (_x_pos_r_,
                 _y_pos_r_) = _widg.make_labels(_labels_,
                                                self.fxdRelInputQuad4, 5, 5)
                _x_pos_r_ += 30

            # Place the quadrant #2 widgets.
            self.cmbMTTRType.set_tooltip_text(_(
                u"Selects the method of assessing the mean time to repair (MTTR) for the selected assembly."))
            _fxdRelInputQuad2_.put(self.cmbMTTRType, _x_pos_, _y_pos1_[0])
            _query_ = "SELECT fld_mttr_type_noun FROM tbl_mttr_type"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)

            _widg.load_combo(self.cmbMTTRType, _results_)
            self.cmbMTTRType.connect('changed', self._callback_combo, 56)

            self.txtSpecifiedMTTR.set_tooltip_text(_(
                u"Displays the specified mean time to repair (MTTR) for the selected assembly."))
            _fxdRelInputQuad2_.put(self.txtSpecifiedMTTR, _x_pos_, _y_pos1_[1])
            self.txtSpecifiedMTTR.connect('focus-out-event',
                                          self._callback_entry, 'float', 55)

            self.txtMTTRAddAdj.set_tooltip_text(_(
                u"Displays the mean time to repair (MTTR) assessment additive adjustment factor for the selected assembly."))
            _fxdRelInputQuad2_.put(self.txtMTTRAddAdj, _x_pos_, _y_pos1_[2])
            self.txtMTTRAddAdj.connect('focus-out-event',
                                       self._callback_entry, 'float', 53)

            self.txtMTTRMultAdj.set_tooltip_text(_(
                u"Displays the mean time to repair (MTTR) assessment multaplicative adjustment factor for the selected assembly."))
            _fxdRelInputQuad2_.put(self.txtMTTRMultAdj, _x_pos_, _y_pos1_[3])
            self.txtMTTRMultAdj.connect('focus-out-event',
                                        self._callback_entry, 'float', 54)

            self.cmbRepairDist.set_tooltip_text(_(
                u"Selects the time to repair distribution for the selected assembly."))
            _fxdRelInputQuad2_.put(self.cmbRepairDist, _x_pos_, _y_pos1_[4])
            _query_ = "SELECT fld_distribution_noun FROM tbl_distributions"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)
            _widg.load_combo(self.cmbRepairDist, _results_)
            self.cmbRepairDist.connect('changed', self._callback_combo, 72)

            self.txtRepairScale.set_tooltip_text(_(
                u"Displays the time to repair distribution scale parameter."))
            _fxdRelInputQuad2_.put(self.txtRepairScale, _x_pos_, _y_pos1_[5])
            self.txtRepairScale.connect('focus-out-event',
                                        self._callback_entry, 'float', 73)

            self.txtRepairShape.set_tooltip_text(_(
                u"Displays the time to repair distribution shape parameter."))
            _fxdRelInputQuad2_.put(self.txtRepairShape, _x_pos_, _y_pos1_[6])
            self.txtRepairShape.connect('focus-out-event',
                                        self._callback_entry, 'float', 74)

            _fxdRelInputQuad2_.show_all()

            # Place the quadrant #4 widgets.
            self.cmbCostType.set_tooltip_text(_(
                u"Select the method for assessing the cost of the selected assembly."))
            _fxdRelInputQuad4_.put(self.cmbCostType, _x_pos_, _y_pos2_[0])
            _query_ = "SELECT fld_cost_type_noun FROM tbl_cost_type"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)
            _widg.load_combo(self.cmbCostType, _results_)
            self.cmbCostType.connect('changed', self._callback_combo, 16)

            self.txtCost.set_tooltip_text(
                _(u"The cost of the selected hardware item."))
            _fxdRelInputQuad4_.put(self.txtCost, _x_pos_, _y_pos2_[1])
            self.txtCost.connect('focus-out-event',
                                 self._callback_entry, 'float', 13)

            self.txtMinTemp.set_tooltip_text(_(
                u"The minimum design operating temperature for the selected component."))
            self.fxdRelInputQuad4.put(self.txtMinTemp, _x_pos_r_, _y_pos_r_[0])
            self.txtMinTemp.connect('focus-out-event',
                                    self._callback_entry, 'float', 256)

            self.txtKneeTemp.set_tooltip_text(
                _(u"The knee temperature for the selected component."))
            self.fxdRelInputQuad4.put(self.txtKneeTemp, _x_pos_r_,
                                      _y_pos_r_[1])
            self.txtKneeTemp.connect('focus-out-event',
                                     self._callback_entry, 'float', 243)

            self.txtMaxTemp.set_tooltip_text(_(
                u"The maximum design operating temperature for the selected component."))
            self.fxdRelInputQuad4.put(self.txtMaxTemp, _x_pos_r_, _y_pos_r_[2])
            self.txtMaxTemp.connect('focus-out-event',
                                    self._callback_entry, 'float', 255)

            self.txtRatedVoltage.set_tooltip_text(
                _(u"The maximum rated voltage for the selected component."))
            self.fxdRelInputQuad4.put(self.txtRatedVoltage, _x_pos_r_,
                                      _y_pos_r_[3])
            self.txtRatedVoltage.connect('focus-out-event',
                                         self._callback_entry, 'float', 294)

            self.txtOpVoltage.set_tooltip_text(
                _(u"The operating voltage for the selected component."))
            self.fxdRelInputQuad4.put(self.txtOpVoltage, _x_pos_r_,
                                      _y_pos_r_[4])
            self.txtOpVoltage.connect('focus-out-event',
                                      self._callback_entry, 'float', 266)

            self.txtRatedCurrent.set_tooltip_text(
                _(u"The maximum rated current for the selected component."))
            self.fxdRelInputQuad4.put(self.txtRatedCurrent, _x_pos_r_,
                                      _y_pos_r_[5])
            self.txtRatedCurrent.connect('focus-out-event',
                                         self._callback_entry, 'float', 292)

            self.txtOpCurrent.set_tooltip_text(
                _(u"The operating current for the selected component."))
            self.fxdRelInputQuad4.put(self.txtOpCurrent, _x_pos_r_,
                                      _y_pos_r_[6])
            self.txtOpCurrent.connect('focus-out-event',
                                      self._callback_entry, 'float', 262)

            self.txtRatedPower.set_tooltip_text(
                _(u"The maximum rated power for the selected component."))
            self.fxdRelInputQuad4.put(self.txtRatedPower, _x_pos_r_,
                                      _y_pos_r_[7])
            self.txtRatedPower.connect('focus-out-event',
                                       self._callback_entry, 'float', 293)

            self.txtOpPower.set_tooltip_text(
                _(u"The operating power for the selected component."))
            self.fxdRelInputQuad4.put(self.txtOpPower, _x_pos_r_, _y_pos_r_[8])
            self.txtOpPower.connect('focus-out-event',
                                    self._callback_entry, 'float', 264)

            self.txtThetaJC.set_tooltip_text(_(
                u"The junction-to-case thermal resistance for the selected component."))
            self.fxdRelInputQuad4.put(self.txtThetaJC, _x_pos_r_, _y_pos_r_[9])
            self.txtThetaJC.connect('focus-out-event',
                                    self._callback_entry, 'float', 309)

            self.txtTempRise.set_tooltip_text(_(
                u"The ambient to case temperature rise for the selected component."))
            self.fxdRelInputQuad4.put(self.txtTempRise, _x_pos_r_,
                                      _y_pos_r_[10])
            self.txtTempRise.connect('focus-out-event',
                                     self._callback_entry, 'float', 307)

            self.txtCaseTemp.set_tooltip_text(
                _(u"The case temperature for the selected component."))
            self.fxdRelInputQuad4.put(self.txtCaseTemp, _x_pos_r_,
                                      _y_pos_r_[11])
            self.txtCaseTemp.connect('focus-out-event',
                                     self._callback_entry, 'float', 305)

            _fxdRelInputQuad4_.show_all()
            self.fxdRelInputQuad4.show_all()

            _label_ = gtk.Label()
            _heading_ = _(u"Assessment\nInputs")
            _label_.set_markup("<span weight='bold'>" + _heading_ + "</span>")
            _label_.set_alignment(xalign=0.5, yalign=0.5)
            _label_.set_justify(gtk.JUSTIFY_CENTER)
            _label_.show_all()
            _label_.set_tooltip_text(_(
                u"Allows entering reliability, maintainability, and other assessment inputs for the selected assembly."))

            notebook.insert_page(_hbox_,
                                 tab_label=_label_,
                                 position=-1)

            return False

        def _create_assessment_results_tab(self, notebook):
            """
            Function to create the HARDWARE class gtk.Notebook() page for
            displaying the assessment results for the selected HARDWARE.

            :param self: the current instance of a HARDWARE class.
            :type self: RTK application
            :param notebook: the HARDWARE class gtk.Notebook() widget.
            :type notebook: gtk.Notebook
            :return: False or True
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hbox_ = gtk.HBox()

            # Build the quadrant #1 (upper left) containers.
            _fxdCalcResultsQuad1_ = gtk.Fixed()

            _frame = _widg.make_frame(_label_=_(u"Reliability Results"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_fxdCalcResultsQuad1_)

            self.fraDerate.props.height_request = 350
            self.fraDerate.props.width_request = 450

            _hbox_.pack_start(_frame)

            # Build the quadrant #2 (upper right) containers.
            _vbox = gtk.VBox()

            _fxdCalcResultsQuad2_ = gtk.Fixed()

            _frame = _widg.make_frame(_label_=_(u"Maintainability Results"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_fxdCalcResultsQuad2_)

            _vbox.pack_start(_frame)

            # Build the quadrant #4 (lower right) containers.
            _fxdCalcResultsQuad4_ = gtk.Fixed()

            _hbox1_ = gtk.HBox()

            _frame = _widg.make_frame(_label_=_(u"Miscellaneous Results"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_hbox1_)

            _hbox1_.pack_start(_fxdCalcResultsQuad4_)
            _hbox1_.pack_start(self.fxdCalcResultsQuad4)

            _vbox.pack_start(_frame)

            _hbox_.pack_start(_vbox)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display the assessment results.      #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Create the labels for quadrant #1.
            _labels = [_(u"Active h(t):"), _(u"Dormant h(t):"),
                       _(u"Software h(t):"), _(u"Predicted h(t):"),
                       _(u"Mission h(t):"), _(u"h(t) Percent:"),
                       _(u"MTBF:"), _(u"Mission MTBF:"), _(u"Reliability:"),
                       _(u"Mission R(t):")]

            (_x_pos_,
             _y_pos_) = _widg.make_labels(_labels, _fxdCalcResultsQuad1_, 5, 5)
            _x_pos_ += 20

            # Place the quadrant #1 widgets.
            self.txtActiveHt.set_tooltip_text(_(u"Displays the active failure "
                                                u"intensity for the selected "
                                                u"assembly."))
            _fxdCalcResultsQuad1_.put(self.txtActiveHt, _x_pos_, _y_pos_[0])

            self.txtDormantHt.set_tooltip_text(_(u"Displays the dormant "
                                                 u"failure intensity for the "
                                                 u"selected assembly."))
            _fxdCalcResultsQuad1_.put(self.txtDormantHt, _x_pos_, _y_pos_[1])

            self.txtSoftwareHt2.set_tooltip_text(_(u"Displays the software "
                                                   u"failure intensity for "
                                                   u"the selected assembly."))
            _fxdCalcResultsQuad1_.put(self.txtSoftwareHt2, _x_pos_, _y_pos_[2])

            self.txtPredictedHt.set_tooltip_text(_(u"Displays the predicted "
                                                   u"failure intensity for "
                                                   u"the selected assembly.  "
                                                   u"This is the sum of the "
                                                   u"active, dormant, and "
                                                   u"software failure "
                                                   u"intensities."))
            _fxdCalcResultsQuad1_.put(self.txtPredictedHt, _x_pos_, _y_pos_[3])

            self.txtMissionHt.set_tooltip_text(_(u"Displays the mission "
                                                 u"failure intensity for the "
                                                 u"selected assembly."))
            _fxdCalcResultsQuad1_.put(self.txtMissionHt, _x_pos_, _y_pos_[4])

            self.txtHtPerCent.set_tooltip_text(_(u"Displays the percent of "
                                                 u"the total system failure intensity attributable to the selected assembly."))
            _fxdCalcResultsQuad1_.put(self.txtHtPerCent, _x_pos_, _y_pos_[5])

            self.txtMTBF.set_tooltip_text(_(
                u"Displays the limiting mean time between failure (MTBF) for the selected assembly."))
            _fxdCalcResultsQuad1_.put(self.txtMTBF, _x_pos_, _y_pos_[6])

            self.txtMissionMTBF.set_tooltip_text(_(
                u"Displays the mission mean time between failure (MTBF) for the selected assembly."))
            _fxdCalcResultsQuad1_.put(self.txtMissionMTBF, _x_pos_, _y_pos_[7])

            self.txtReliability.set_tooltip_text(_(
                u"Displays the limiting reliability for the selected assembly."))
            _fxdCalcResultsQuad1_.put(self.txtReliability, _x_pos_, _y_pos_[8])

            self.txtMissionRt.set_tooltip_text(_(
                u"Displays the mission reliability for the selected assembly."))
            _fxdCalcResultsQuad1_.put(self.txtMissionRt, _x_pos_, _y_pos_[9])

            self.fraDerate.add(self.pltDerate)
            _fxdCalcResultsQuad1_.put(self.fraDerate, _x_pos_ + 210, 5)

            _fxdCalcResultsQuad1_.show_all()

            # Create the labels for quadrant #2.
            _labels = [_(u"MPMT:"), _(u"MCMT:"), _(u"MTTR:"), _(u"MMT:"),
                       _(u"Availability:"), _(u"Mission A(t):")]

            _max1_ = 0
            _max2_ = 0
            (_max1_, _y_pos1_) = _widg.make_labels(_labels,
                                                   _fxdCalcResultsQuad2_, 5, 5)

            # Create the labels for quadrant #4.
            _labels = [_(u"Total Cost:"), _(u"Cost/Failure:"),
                       _(u"Cost/Hour:"), _(u"Total Part Count:"),
                       _(u"Assembly Criticality:")]
            (_max2_, _y_pos2_) = _widg.make_labels(_labels,
                                                   _fxdCalcResultsQuad4_, 5, 5)
            _x_pos_ = max(_max1_, _max2_) + 20

            if self.part:
                _labels = [_(u"Total Power Used:"), _(u"Voltage Ratio:"),
                           _(u"Current Ratio:"), _(u"Power Ratio:")]
            (_x_pos_r_,
             _y_pos_r_) = _widg.make_labels(_labels,
                                            self.fxdCalcResultsQuad4, 5, 5)
            _x_pos_r_ += 30

            # Place the quadrant #2 widgets.
            self.txtMPMT.set_tooltip_text(_(
                u"Displays the mean preventive maintenance time (MPMT) for the selected assembly."))
            _fxdCalcResultsQuad2_.put(self.txtMPMT, _x_pos_, _y_pos1_[0])

            self.txtMCMT.set_tooltip_text(_(
                u"Displays the mean corrective maintenance time (MCMT) for the selected assembly."))
            _fxdCalcResultsQuad2_.put(self.txtMCMT, _x_pos_, _y_pos1_[1])

            self.txtMTTR.set_tooltip_text(_(
                u"Displays the mean time to repair (MTTR) for the selected assembly."))
            _fxdCalcResultsQuad2_.put(self.txtMTTR, _x_pos_, _y_pos1_[2])

            self.txtMMT.set_tooltip_text(_(
                u"Displays the mean maintenance time (MMT) for the selected assembly."))
            _fxdCalcResultsQuad2_.put(self.txtMMT, _x_pos_, _y_pos1_[3])

            self.txtAvailability.set_tooltip_text(_(
                u"Displays the logistics availability for the selected assembly."))
            _fxdCalcResultsQuad2_.put(self.txtAvailability, _x_pos_,
                                      _y_pos1_[4])

            self.txtMissionAt.set_tooltip_text(_(
                u"Displays the mission availability for the selected assembly."))
            _fxdCalcResultsQuad2_.put(self.txtMissionAt, _x_pos_, _y_pos1_[5])

            _fxdCalcResultsQuad2_.show_all()

            # Place the quadrant #4 widgets.
            self.txtTotalCost.set_tooltip_text(_(u"Displays the total cost of "
                                                 u"the selected assembly."))
            _fxdCalcResultsQuad4_.put(self.txtTotalCost, _x_pos_, _y_pos2_[0])

            self.txtCostFailure.set_tooltip_text(_(u"Displays the cost per "
                                                   u"failure of the selected "
                                                   u"assembly."))
            _fxdCalcResultsQuad4_.put(self.txtCostFailure, _x_pos_,
                                      _y_pos2_[1])

            self.txtCostHour.set_tooltip_text(_(u"Displays the cost per "
                                                u"mission hour of the "
                                                u"selected assembly."))
            _fxdCalcResultsQuad4_.put(self.txtCostHour, _x_pos_, _y_pos2_[2])

            self.txtPartCount.set_tooltip_text(_(u"The total number of "
                                                 u"components used to "
                                                 u"construct the selected "
                                                 u"assembly."))
            _fxdCalcResultsQuad4_.put(self.txtPartCount, _x_pos_, _y_pos2_[3])

            self.txtAssemblyCrit.set_tooltip_text(_(u"The criticality of the "
                                                    u"selected hardware item.  "
                                                    u"This is calculated by "
                                                    u"the FMEA."))
            _fxdCalcResultsQuad4_.put(self.txtAssemblyCrit, _x_pos_,
                                      _y_pos2_[4])

            self.txtTotalPwr.set_tooltip_text(_(u"The total power of the "
                                                u"selected assembly."))
            self.fxdCalcResultsQuad4.put(self.txtTotalPwr, _x_pos_,
                                         _y_pos2_[0])

            self.txtVoltageRatio.set_tooltip_text(_(u"The ratio of operating "
                                                    u"voltage to rated "
                                                    u"voltage for the "
                                                    u"selected component."))
            self.fxdCalcResultsQuad4.put(self.txtVoltageRatio, _x_pos_,
                                         _y_pos2_[1])

            self.txtCurrentRatio.set_tooltip_text(_(u"The ratio of operating "
                                                    u"current to rated "
                                                    u"current for the "
                                                    u"selected component."))
            self.fxdCalcResultsQuad4.put(self.txtCurrentRatio, _x_pos_,
                                         _y_pos2_[2])

            self.txtPwrRatio.set_tooltip_text(_(u"The ratio of operating "
                                                u"power to rated power for "
                                                u"the selected component."))
            self.fxdCalcResultsQuad4.put(self.txtPwrRatio, _x_pos_,
                                         _y_pos2_[3])

            _label_ = _widg.make_label(text=_(u"Overstressed?:"))
            self.chkOverstressed.set_tooltip_text(_(u"Indicates whether the "
                                                    u"selected component is "
                                                    u"overstressed."))
            self.fxdCalcResultsQuad4.put(_label_, _x_pos_ + 210, _y_pos2_[0])
            self.fxdCalcResultsQuad4.put(self.chkOverstressed, _x_pos_ + 360,
                                         _y_pos2_[0])

            _textview_ = _widg.make_text_view(buffer_=self.txtOSReason,
                                              width=250)
            _textview_.set_tooltip_text(_(u"The reason(s) the selected "
                                          u"component is overstressed."))
            self.fxdCalcResultsQuad4.put(_textview_, _x_pos_ + 390, _y_pos_[0])

            _fxdCalcResultsQuad4_.show_all()
            self.fxdCalcResultsQuad4.show_all()

            _label = gtk.Label()
            _label.set_markup(_(u"<span weight='bold'>"
                                u"Assessment\nResults"
                                u"</span>"))
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.show_all()
            _label.set_tooltip_text(_(u"Displays the results the reliability, "
                                      u"maintainability, and other assessments "
                                      u"for the selected assembly."))

            notebook.insert_page(_hbox_,
                                 tab_label=_label,
                                 position=-1)

            return False

        def _create_fmeca_tab(self, notebook):
            """
            Function to create the HARDWARE class gtk.Notebook() page for
            displaying the FMEA/FMECA for the selected HARDWARE.

            Keyword Arguments:
            self     -- the current instance of a HARDWARE class.
            notebook -- the HARDWARE class gtk.Notebook() widget.
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hpaned_ = gtk.HPaned()

            _scrollwindow_ = gtk.ScrolledWindow()
            _scrollwindow_.set_policy(gtk.POLICY_AUTOMATIC,
                                      gtk.POLICY_AUTOMATIC)
            _scrollwindow_.add_with_viewport(self.tvwFMECA)

            _frame_ = _widg.make_frame(
                _label_=_(u"Failure Mode, Effects, and Criticality Analysis"))
            _frame_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame_.add(_scrollwindow_)

            _hpaned_.pack1(_frame_, resize=True, shrink=False)

            self.fraFMECADetails.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

            _hpaned_.pack2(self.fraFMECADetails, resize=False, shrink=False)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display the FMEA/FMECA.             #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            self.tvwFMECA.set_tooltip_text(_(
                u"Displays the failure mode, effects, and criticality analysis (FMECA) for the selected assembly."))
            self.tvwFMECA.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

            # Load the severity classification gtk.CellRendererCombo().
            _column_ = self.tvwFMECA.get_column(self._FMECA_col_order[11])
            _cell_ = _column_.get_cell_renderers()
            _cellmodel_ = _cell_[0].get_property('model')
            _cellmodel_.clear()
            _query_ = "SELECT fld_criticality_id, fld_criticality_name, \
                              fld_criticality_cat \
                       FROM tbl_criticality"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)

            try:
                _n_phases_ = len(_results_)
            except TypeError:
                _util.application_error(_(
                    u"There was a problem loading the failure criticality list in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
                _n_phases_ = 0

            _cellmodel_.append([""])
            for i in range(_n_phases_):
                _cellmodel_.append([_results_[i][2] + " - " + _results_[i][1]])

            # Load the qualitative failure probability gtk.CellRendererCombo().
            _column_ = self.tvwFMECA.get_column(self._FMECA_col_order[13])
            _cell_ = _column_.get_cell_renderers()
            _cellmodel_ = _cell_[0].get_property('model')
            _cellmodel_.clear()
            _query_ = "SELECT * FROM tbl_failure_probability"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)

            try:
                _n_probs_ = len(_results_)
            except TypeError:
                _util.application_error(_(
                    u"There was a problem loading the failure probability list in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
                _n_probs_ = 0

            _cellmodel_.append([""])
            for i in range(_n_probs_):
                _cellmodel_.append([_results_[i][1]])

            self.tvwFMECA.connect('cursor_changed',
                                  self._fmeca_treeview_row_changed, None, None)
            self.tvwFMECA.connect('row_activated',
                                  self._fmeca_treeview_row_changed)

            # Load the RPN severity and RPN severity new gtk.CellRendererCombo.
            _column_ = self.tvwFMECA.get_column(self._FMECA_col_order[20])
            _cell_ = _column_.get_cell_renderers()
            _cellmodel1_ = _cell_[0].get_property('model')
            _cellmodel1_.clear()
            _column_ = self.tvwFMECA.get_column(self._FMECA_col_order[21])
            _cell_ = _column_.get_cell_renderers()
            _cellmodel2_ = _cell_[0].get_property('model')
            _cellmodel2_.clear()
            _query_ = "SELECT fld_severity_name \
                       FROM tbl_rpn_severity \
                       WHERE fld_fmeca_type=0"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)

            try:
                _n_probs = len(_results_)
            except TypeError:
                _util.application_error(_(
                    u"There was a problem loading the RPN Severity list in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
                _n_probs_ = 0

            _cellmodel1_.append([""])
            _cellmodel2_.append([""])
            for i in range(_n_probs_):
                self._rpnsev[_results_[i][0]] = i
                _cellmodel1_.append([_results_[i][0]])
                _cellmodel2_.append([_results_[i][0]])

            # Load the RPN occurrence and RPN ocurrence new gtk.ComboBox().
            _cellmodel1_ = self.cmbOccurenceI.get_model()
            _cellmodel2_ = self.cmbOccurrenceN.get_model()
            _cellmodel1_.clear()
            _cellmodel2_.clear()
            _query_ = "SELECT fld_occurrence_name \
                       FROM tbl_rpn_occurrence \
                       WHERE fld_fmeca_type=0"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)

            try:
                _n_probs = len(_results_)
            except TypeError:
                _util.application_error(_(
                    u"There was a problem loading the RPN Occurrence list in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
                _n_probs_ = 0

            _cellmodel1_.append([""])
            _cellmodel2_.append([""])
            for i in range(_n_probs_):
                _cellmodel1_.append([_results_[i][0]])
                _cellmodel2_.append([_results_[i][0]])

            # Load the RPN detection and RPN detection new gtk.ComboBox().
            _cellmodel1_ = self.cmbDetectionI.get_model()
            _cellmodel2_ = self.cmbDetectionN.get_model()
            _cellmodel1_.clear()
            _cellmodel2_.clear()
            _query_ = "SELECT fld_detection_name \
                       FROM tbl_rpn_detection \
                       WHERE fld_fmeca_type=0"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)

            try:
                _n_probs = len(_results_)
            except TypeError:
                _util.application_error(_(
                    u"There was a problem loading the RPN Detection list in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
                _n_probs_ = 0

            _cellmodel1_.append([""])
            _cellmodel2_.append([""])
            for i in range(_n_probs_):
                _cellmodel1_.append([_results_[i][0]])
                _cellmodel2_.append([_results_[i][0]])

            # Load the FMECA control type gtk.Combo.
            self.cmbControlType.append_text("")
            self.cmbControlType.append_text(_(u"Prevention"))
            self.cmbControlType.append_text(_(u"Detection"))

            # Load the FMECA action type gtk.Combo.
            _query_ = "SELECT fld_action_name \
                       FROM tbl_action_category"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)

            try:
                _n_actions_ = len(_results_)
            except TypeError:
                _util.application_error(_(
                    u"There was a problem loading the action category list in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
                _n_actions_ = 0

            self.cmbActionCategory.append_text("")
            for i in range(_n_actions_):
                self.cmbActionCategory.append_text(_results_[i][0])

            # Load the FMECA action status gtk.Combo.
            _query_ = "SELECT fld_status_name \
                       FROM tbl_status"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)

            try:
                _n_actions_ = len(_results_)
            except TypeError:
                _util.application_error(_(
                    u"There was a problem loading the action status list in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
                _n_actions_ = 0

            self.cmbActionStatus.append_text("")
            for i in range(_n_actions_):
                self.cmbActionStatus.append_text(_results_[i][0])

            # Load the FMECA user list gtk.Combos.
            _query_ = "SELECT fld_user_lname, fld_user_fname \
                       FROM tbl_users"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)

            try:
                _n_actions_ = len(_results_)
            except TypeError:
                _util.application_error(_(
                    u"There was a problem loading the user lists in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
                _n_actions_ = 0

            self.cmbActionResponsible.append_text("")
            self.cmbActionApproved.append_text("")
            self.cmbActionClosed.append_text("")
            for i in range(_n_actions_):
                _user_ = _results_[i][0] + ", " + _results_[i][1]
                self.cmbActionResponsible.append_text(_user_)
                self.cmbActionApproved.append_text(_user_)
                self.cmbActionClosed.append_text(_user_)

            # Create the detailed information gtk.Fixed() widget for failure
            # modes.
            self.chkFCQ2.set_sensitive(False)
            self.chkFCQ3.set_sensitive(True)
            self.optHS.set_active(True)

            self.fxdMode.put(self.chkFCQ1, 5, 5)
            self.chkFCQ1.connect('toggled', self._callback_check, 90)

            self.fxdMode.put(self.txtFCQ1, 5, 65)

            self.fxdMode.put(self.chkFCQ2, 5, 145)
            self.chkFCQ2.connect('toggled', self._callback_check, 90)

            self.fxdMode.put(self.txtFCQ2, 5, 205)

            self.fxdMode.put(self.chkFCQ3, 5, 285)
            self.chkFCQ3.connect('toggled', self._callback_check, 90)

            self.fxdMode.put(self.txtFCQ3, 5, 345)

            self.fxdMode.put(self.optHS, 5, 425)
            self.fxdMode.put(self.optES, 205, 425)
            self.fxdMode.put(self.optNSH, 5, 455)
            self.fxdMode.put(self.optEO, 205, 455)

            # Create the detailed information gtk.Fixed() widget for failure
            # mechanisms.
            _labels_ = [_(u"Mechanism ID:"), _(u"Mechanism:"),
                        _(u"Occurence:"), _(u"Detection:"), _(u"RPN:"),
                        _(u"New Occurence:"), _(u"New Detection:"),
                        _(u"New RPN:")]

            (_x_pos_,
             _y_pos_) = _widg.make_labels(_labels_, self.fxdMechanism, 5, 5)

            self.fxdMechanism.put(self.txtMechanismID, _x_pos_, _y_pos_[0])
            self.fxdMechanism.put(self.txtMechanismDescription, _x_pos_,
                                  _y_pos_[1])
            self.txtMechanismDescription.connect('focus-out-event',
                                                 self._callback_entry, 'text',
                                                 1000)

            self.fxdMechanism.put(self.cmbOccurenceI, _x_pos_, _y_pos_[2])
            self.cmbOccurenceI.connect('changed', self._callback_combo, 1001)

            self.fxdMechanism.put(self.cmbDetectionI, _x_pos_, _y_pos_[3])
            self.cmbDetectionI.connect('changed', self._callback_combo, 1002)

            self.fxdMechanism.put(self.txtRPNI, _x_pos_, _y_pos_[4])

            self.fxdMechanism.put(self.cmbOccurrenceN, _x_pos_, _y_pos_[5])
            self.cmbOccurrenceN.connect('changed', self._callback_combo, 1004)

            self.fxdMechanism.put(self.cmbDetectionN, _x_pos_, _y_pos_[6])
            self.cmbDetectionN.connect('changed', self._callback_combo, 1005)

            self.fxdMechanism.put(self.txtRPNN, _x_pos_, _y_pos_[7])

            # Create the detailed information gtk.Fixed() widget for current
            # controls.
            _labels_ = [_(u"Control ID:"), _(u"Control:"), _(u"Control Type:")]

            (_x_pos_,
             _y_pos_) = _widg.make_labels(_labels_, self.fxdControl, 5, 5)

            self.fxdControl.put(self.txtControlID, _x_pos_, _y_pos_[0])

            self.fxdControl.put(self.txtControlDescription, _x_pos_,
                                _y_pos_[1])
            self.txtControlDescription.connect('focus-out-event',
                                               self._callback_entry, 'text',
                                               1000)

            self.fxdControl.put(self.cmbControlType, _x_pos_, _y_pos_[2])
            self.cmbControlType.connect('changed', self._callback_combo, 1001)

            # Create the detailed information gtk.Fixed widget for recommended
            # actions.
            _labels_ = [_(u"Action ID:"), _(u"Recommended Action:"),
                        _(u"Action Category:"), _(u"Action Owner:"),
                        _(u"Due Date:"), _(u"Status:"), _(u"Action Taken:"),
                        _(u"Approved By:"), _(u"Approval Date:"),
                        _(u"Closed By:"), _(u"Closure Date:")]

            (_x_pos_,
             _y_pos_) = _widg.make_labels(_labels_, self.fxdAction, 5, 5)

            self.fxdAction.put(self.txtActionID, 205, _y_pos_[0])

            self.fxdAction.put(self.txtActionRecommended, _x_pos_, _y_pos_[1])
            self.txtActionRecommended.connect('focus-out-event',
                                              self._callback_entry, 'text',
                                              1000)

            self.fxdAction.put(self.cmbActionCategory, _x_pos_, _y_pos_[2])
            self.cmbActionCategory.connect('changed', self._callback_combo,
                                           1001)

            self.fxdAction.put(self.cmbActionResponsible, _x_pos_, _y_pos_[3])
            self.cmbActionResponsible.connect('changed', self._callback_combo,
                                              1002)

            self.fxdAction.put(self.txtActionDueDate, _x_pos_, _y_pos_[4])
            self.txtActionDueDate.connect('focus-out-event',
                                          self._callback_entry, 'date', 1003)

            self.fxdAction.put(self.cmbActionStatus, _x_pos_, _y_pos_[5])
            self.cmbActionStatus.connect('changed', self._callback_combo, 1004)

            self.fxdAction.put(self.txtActionTaken, _x_pos_, _y_pos_[6])
            self.txtActionTaken.connect('focus-out-event',
                                        self._callback_entry, 'text',
                                        1005)

            self.fxdAction.put(self.cmbActionApproved, _x_pos_, _y_pos_[7])
            self.cmbActionApproved.connect('changed', self._callback_combo,
                                           1006)

            self.fxdAction.put(self.txtActionApproveDate, _x_pos_, _y_pos_[8])
            self.txtActionApproveDate.connect('focus-out-event',
                                              self._callback_entry, 'date',
                                              1007)

            self.fxdAction.put(self.cmbActionClosed, _x_pos_, _y_pos_[9])
            self.cmbActionClosed.connect('changed', self._callback_combo, 1008)

            self.fxdAction.put(self.txtActionCloseDate, _x_pos_, _y_pos_[10])
            self.txtActionCloseDate.connect('focus-out-event',
                                            self._callback_entry, 'date', 1009)

            _label_ = gtk.Label()
            _heading_ = _(u"FMEA/FMECA\nWorksheet")
            _label_.set_markup("<span weight='bold'>" + _heading_ + "</span>")
            _label_.set_alignment(xalign=0.5, yalign=0.5)
            _label_.set_justify(gtk.JUSTIFY_CENTER)
            _label_.show_all()
            _label_.set_tooltip_text(_(
                u"Failure mode, effects, and criticality analysis (FMECA) for the selected assembly."))

            notebook.insert_page(_hpaned_,
                                 tab_label=_label_,
                                 position=-1)

            return False

        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if _conf.TABPOS[2] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif _conf.TABPOS[2] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif _conf.TABPOS[2] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        _create_general_data_tab(self, _notebook)
        _create_allocation_tab(self, _notebook)
        _create_hazard_analysis_tab(self, _notebook)
        _create_similar_item_tab(self, _notebook)
        _create_assessment_inputs_tab(self, _notebook)
        _create_assessment_results_tab(self, _notebook)
        _create_fmeca_tab(self, _notebook)

        return _notebook

    def load_tree(self):
        """
        Method to load the HARDWARE class gtk.TreeView() model with system
        information.
        """

        _query = "SELECT * FROM tbl_system WHERE fld_revision_id=%d" % \
                 self.revision_id
        _results_ = self._app.DB.execute_query(_query,
                                               None,
                                               self._app.ProgCnx)

        try:
            _n_assemblies_ = len(_results_)
        except TypeError:
            _n_assemblies_ = 0

        _pixbuf_ = False
        _cols_ = self.treeview.get_columns()
        for i in range(len(_cols_)):
            if _cols_[i].get_visible() is True and _pixbuf_ is False:
                _viscol_ = i
                _pixbuf_ = True

        _model_ = self.treeview.get_model()
        _model_.clear()

        # Create an empty dictionary to hold the Assembly ID/Hardware Tree
        # gtk.TreeModel() paths.  This is used to keep the Hardware Tree and
        #  the Parts List in sync.
        self._treepaths = {}

        # Load the model with the returned results.
        for i in range(_n_assemblies_):

            if _results_[i][62] == '-':  # Its the top level element.
                _piter_ = None
                self.system_ht = _results_[i][32]
            elif _results_[i][62] != '-':  # Its a child element.
                _piter_ = _model_.get_iter_from_string(_results_[i][62])

            # Select the image to display.  If there is a problem with the part
            # (overstressed, etc.), display the !.  If it is an assembly, display the
            # assembly icon.  If it is a part, display the part icon.
            if _results_[i][60] == 1:
                _icon_ = _conf.ICON_DIR + '32x32/overstress.png'
            elif _results_[i][63] == 0:
                _icon_ = _conf.ICON_DIR + '32x32/assembly.png'
            else:
                _icon_ = _conf.ICON_DIR + '32x32/part.png'

            _icon_ = gtk.gdk.pixbuf_new_from_file_at_size(_icon_, 16,
                                                          16)  # @UndefinedVariable
            _data_ = _results_[i] + (_icon_,)

            _row_ = _model_.append(_piter_, _data_)

            #            self.dicHARDWARE[_results_[i][1]] = _data_ + (_model_.get_string_from_iter(_row_),)
            self._treepaths[_results_[i][68]] = _model_.get_path(_row_)

        _row_ = _model_.get_iter_root()

        _path_ = _model_.get_path(_row_)
        self.treeview.set_cursor(_path_, None, False)
        self.treeview.row_activated(_path_, self.treeview.get_column(0))
        self.treeview.expand_all()

        return False

    def load_notebook(self):
        """
        Method to load the HARDWARE class gtk.Notebook().
        """

        def _load_general_data_tab(self):
            """
            Function to load the widgets on the General Data page.

            Keyword Arguments:
            self -- the current instance of an HARDWARE class.
            """

            self.txtRevisionID.set_text(str(self.revision_id))
            self.txtAltPartNum.set_text(self.alt_part_num)
            self.txtAttachments.set_text(self.attachments)
            self.txtCAGECode.set_text(self.cage_code)
            self.txtCompRefDes.set_text(self.comp_ref_des)
            self.txtDescription.set_text(self.description)
            self.txtFigNum.set_text(self.figure_number)
            self.txtImageFile.set_text(self.image_file)
            self.txtLCN.set_text(self.lcn)
            self.cmbManufacturer.set_active(self.manufacturer)
            self.txtName.set_text(self.name)
            self.txtNSN.set_text(self.nsn)
            self.txtPageNum.set_text(self.page_number)
            self.txtPartNum.set_text(self.part_number)
            self.txtQuantity.set_text(str(self.quantity))
            self.txtRefDes.set_text(self.ref_des)
            _text_ = _util.none_to_string(self.remarks)
            textbuffer = self.txtRemarks.get_child().get_child().get_buffer()
            textbuffer.set_text(_text_)
            self.chkRepairable.set_active(self.repairable)
            self.txtSpecification.set_text(self.specification)
            self.chkTagged.set_active(self.tagged)
            self.txtYearMade.set_text(str(self.year_of_manufacture))

            # Show/hide the assembly-specific or component-specific widgets as
            # appropriate.
            if not self.part:
                self.cmbCategory.hide()
                self.cmbSubcategory.hide()
                self.lblCategory.hide()
                self.lblSubcategory.hide()
            else:
                self.cmbCategory.show()
                self.cmbSubcategory.show()
                self.lblCategory.show()
                self.lblSubcategory.show()

            return False

        def _load_allocation_tab(self, model, row):
            """
            Function to load the widgets on the Allocation page.

            :param self: the current instance of a HARDWARE class.
            :type self: Hardware class object
            :param model: the HARDWARE class gtk.TreeModel()
            :type model: gtk.TreeModel
            :param row: the currently selected row in the HARDWARE class
                        gtk.TreeModel()
            :type row: gtk.Iter
            """

            fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

            _values_ = (model.get_string_from_iter(row), self.revision_id)

            # Get mission time from the HARDWARE gtk.TreeView
            self.cmbAllocationType.set_active(self.allocation_type)
            self.txtOperTime.set_text(str('{0:0.2f}'.format(
                self.mission_time)))

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
                     AND t1.fld_revision_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query,
                                                   None,
                                                   self._app.ProgCnx)

            _values_ = (self.assembly_id, self.revision_id)
            _query_ = "SELECT fld_reliability_goal_measure, \
                              fld_reliability_goal \
                       FROM tbl_system \
                       WHERE fld_assembly_id=%d \
                       AND fld_revision_id=%d" % _values_
            _goal_ = self._app.DB.execute_query(_query_,
                                                None,
                                                self._app.ProgCnx)

            try:
                _n_records_ = len(_results_)
            except TypeError:
                _n_records_ = 0

            # Load the allocation gtk.TreeView
            _model_ = self.tvwAllocation.get_model()
            _model_.clear()
            for i in range(_n_records_):
                _model_.append(None, _results_[i])

            _root_ = _model_.get_iter_root()
            if _root_ is not None:
                _path_ = _model_.get_path(_root_)
                self.tvwAllocation.expand_all()
                self.tvwAllocation.set_cursor('0', None, False)
                _col_ = self.tvwAllocation.get_column(0)
                self.tvwAllocation.row_activated(_path_, _col_)

            # Set the reliability requirement widgets.
            self.cmbRqmtType.set_active(_goal_[0][0])
            if _goal_[0][0] == 1:  # Reliability goal
                self.txtReliabilityGoal.set_text(str(fmt.format(_goal_[0][1])))

                (_mtbf_, _fr_) = self._calculate_goals(500)

                self.txtMTBFGoal.set_text(str(fmt.format(_mtbf_)))
                self.txtFailureRateGoal.set_text(str(fmt.format(_fr_)))

            elif _goal_[0][0] == 2:  # MTBF goal
                self.txtMTBFGoal.set_text(str(fmt.format(_goal_[0][1])))

                (_reliability_, _fr_) = self._calculate_goals(501)

                self.txtReliabilityGoal.set_text(
                    str(fmt.format(_reliability_)))
                self.txtFailureRateGoal.set_text(str(fmt.format(_fr_)))

            elif _goal_[0][0] == 3:  # Failure rate goal
                self.txtFailureRateGoal.set_text(str(fmt.format(_goal_[0][1])))

                (_reliability_, _mtbf_) = self._calculate_goals(502)

                self.txtReliabilityGoal.set_text(
                    str(fmt.format(_reliability_)))
                self.txtMTBFGoal.set_text(str(fmt.format(_mtbf_)))

            return False

        def _load_hazard_analysis_tab(self):
            """
            Function to load the widgets on the Hazard Analysis page.

            :param self: the current instance of an HARDWARE class.
            :return: False
            """

            # Get the hazard analysis for the assembly selected in the
            # Module Book.
            _query = "SELECT t1.fld_risk_id, \
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
                             t1.fld_system_hri_f, t1.fld_remarks, \
                             t1.fld_function_1, t1.fld_function_2, \
                             t1.fld_function_3, t1.fld_function_4, \
                             t1.fld_function_5, t1.fld_result_1, \
                             t1.fld_result_2, t1.fld_result_3, \
                             t1.fld_result_4, t1.fld_result_5, \
                             t1.fld_user_blob_1, t1.fld_user_blob_2, \
                             t1.fld_user_blob_3, t1.fld_user_float_1, \
                             t1.fld_user_float_2, t1.fld_user_float_3, \
                             t1.fld_user_int_1, t1.fld_user_int_2, \
                             t1.fld_user_int_3 \
                      FROM tbl_risk_analysis AS t1 \
                      INNER JOIN tbl_system AS t2 \
                      ON t2.fld_assembly_id=t1.fld_assembly_id \
                      WHERE t1.fld_revision_id={0:d} \
                      AND t1.fld_assembly_id={1:d}" \
                .format(self.revision_id, self.assembly_id)
            _results = self._app.DB.execute_query(_query,
                                                  None,
                                                  self._app.ProgCnx)

            try:
                _n_assemblies = len(_results)
            except TypeError:
                _n_assemblies = 0

            _model = self.tvwRisk.get_model()
            _model.clear()
            for i in range(_n_assemblies):
                try:
                    _model.append(None, _results[i])
                except TypeError:
                    pass

            # If the selected item is the top-level system, hide the assembly
            # level columns and show the system-level columns.  Otherwise
            # hide the system-level columns and show the assembly-level
            # columns.
            if self.parent_assembly == '-':
                _show_cols = [13, 14, 15, 16, 17, 18, 19, 20]
                _hide_cols = [5, 6, 7, 8, 9, 10, 11, 12]
            else:
                _show_cols = [5, 6, 7, 8, 9, 10, 11, 12]
                _hide_cols = [13, 14, 15, 16, 17, 18, 19, 20]

            for i in range(len(_hide_cols)):
                self.tvwRisk.get_column(_hide_cols[i]).set_visible(False)

            for i in range(len(_show_cols)):
                self.tvwRisk.get_column(_show_cols[i]).set_visible(True)

            # Load the risk matrix.
            _query = "SELECT fld_severity_id, fld_probability_id, \
                             fld_hazard_count \
                      FROM tbl_risk_matrix \
                      WHERE fld_revision_id={0:d} \
                      AND fld_assembly_id={1:d}" \
                .format(self._app.REVISION.revision_id, self.assembly_id)
            _results = self._app.DB.execute_query(_query,
                                                  None,
                                                  self._app.ProgCnx)

            # TODO: Load the risk map with saved results.
            _model = self.tvwRiskMap.get_model()
            #for i in range(len(_results)):
            #   model.set(row, _results[i][2])

            return False

        def _load_similar_item_tab(self):
            """
            Function to load the widgets on the Similar Item Analysis page.

            :param self: the current instance of an HARDWARE class.
            :return: False
            """

            (_model_, _row_) = self.treeview.get_selection().get_selected()

            if _row_ is not None:
                _path_ = _model_.get_string_from_iter(_row_)

            _query_ = "SELECT t1.fld_sia_id, t2.fld_name, \
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
                              t1.fld_result_1, t1.fld_result_2, \
                              t1.fld_result_3, t1.fld_result_4, \
                              t1.fld_result_5, t1.fld_user_blob_1, \
                              t1.fld_user_blob_2, t1.fld_user_blob_3, \
                              t1.fld_user_float_1, t1.fld_user_float_2, \
                              t1.fld_user_float_3, t1.fld_user_int_1, \
                              t1.fld_user_int_2, t1.fld_user_int_3 \
                       FROM tbl_similar_item AS t1 \
                       INNER JOIN tbl_system AS t2 \
                       ON t2.fld_assembly_id=t1.fld_assembly_id \
                       WHERE t1.fld_revision_id=%d \
                       AND t2.fld_parent_assembly='%s'" % \
                      (self.revision_id, _path_)
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

            try:
                _n_assemblies_ = len(_results_)
            except TypeError:
                _n_assemblies_ = 0

            _model_ = self.tvwSIA.get_model()
            _model_.clear()
            for i in range(_n_assemblies_):
                try:
                    _model_.append(None, _results_[i])
                except TypeError:
                    pass

            return False

        def _load_assessment_inputs_tab(self):
            """
            Function to load the widgets on the Assessment Inputs page.

            :param self: the current instance of an HARDWARE class.
            :return: False
            """

            fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

            self.cmbHRType.set_active(int(self.failure_rate_type))
            self.cmbCalcModel.set_active(int(self.calculation_model))
            self.txtSpecifiedHt.set_text(
                str(fmt.format(self.failure_rate_specified)))
            self.txtSpecifiedMTBF.set_text(str(self.mtbf_specified))
            self.txtSoftwareHt.set_text(
                str(fmt.format(self.failure_rate_software)))
            self.txtAddAdj.set_text(str(self._add_adj_factor))
            self.txtMultAdj.set_text(str(self.mult_adj_factor))
            self.txtAllocationWF.set_text(str(self.allocation_type))
            self.cmbFailDist.set_active(int(self.failure_dist))
            self.txtFailScale.set_text(str(self.failure_parameter_1))
            self.txtFailShape.set_text(str(self.failure_parameter_2))
            self.txtFailLoc.set_text(str(self.failure_parameter_3))
            self.cmbActEnviron.set_active(int(self.environment_active))
            self.txtActTemp.set_text(str(self.temperature_active))
            self.cmbDormantEnviron.set_active(int(self.environment_dormant))
            self.txtDormantTemp.set_text(str(self.temperature_dormant))
            self.txtDutyCycle.set_text(str(self.duty_cycle))
            self.txtHumidity.set_text(str(self.humidity))
            self.txtVibration.set_text(str(self.vibration))
            self.txtRPM.set_text(str(self.rpm))
            self.txtWeibullFile.set_text(str(self.weibull_file))
            self.cmbMTTRType.set_active(int(self.mttr_type))
            self.txtSpecifiedMTTR.set_text(str(self.mttr_specified))
            self.txtMTTRAddAdj.set_text(str(self.mttr_add_adj_factor))
            self.txtMTTRMultAdj.set_text(str(self.mttr_mult_adj_factor))
            self.cmbRepairDist.set_active(int(self.repair_dist))
            self.txtRepairScale.set_text(str(self.repair_parameter_1))
            self.txtRepairShape.set_text(str(self.repair_parameter_2))
            self.txtMissionTime.set_text(
                str('{0:0.2f}'.format(self.mission_time)))
            self.cmbCostType.set_active(int(self.cost_type))
            self.txtCost.set_text(str(locale.currency(self.cost)))

            self._component = _util.set_part_model(self.category_id,
                                                   self.subcategory_id)

            # Load the component-specific information.
            if self.part:
                self.txtBurnInTemp.set_text(
                    str('{0:0.2g}'.format(self.burnin_temp)))
                self.txtBurnInTime.set_text(
                    str('{0:0.2g}'.format(self.burnin_time)))
                self.txtLabDevices.set_text(
                    str('{0:0.0g}'.format(self.lab_devices)))
                self.txtLabTime.set_text(str('{0:0.2g}'.format(self.lab_time)))
                self.txtLabTemp.set_text(str('{0:0.2g}'.format(self.lab_temp)))
                self.txtLabFailures.set_text(
                    str('{0:0.0g}'.format(self.lab_failures)))
                self.txtFieldTime.set_text(
                    str('{0:0.2g}'.format(self.field_time)))
                self.txtFieldFailures.set_text(
                    str('{0:0.0g}'.format(self.field_failures)))

                self.txtMinTemp.set_text(str('{0:0.2f}'.format(self.min_temp)))
                self.txtKneeTemp.set_text(
                    str('{0:0.2f}'.format(self.knee_temp)))
                self.txtMaxTemp.set_text(str('{0:0.2f}'.format(self.max_temp)))
                self.txtRatedVoltage.set_text(
                    str(fmt.format(self.rated_voltage)))
                self.txtOpVoltage.set_text(str(fmt.format(self.op_voltage)))
                self.txtRatedCurrent.set_text(
                    str(fmt.format(self.rated_current)))
                self.txtOpCurrent.set_text(str(fmt.format(self.op_current)))
                self.txtRatedPower.set_text(str(fmt.format(self.rated_power)))
                self.txtOpPower.set_text(str(fmt.format(self.op_power)))
                self.txtThetaJC.set_text(str(self.theta_jc))
                self.txtTempRise.set_text(str(fmt.format(self.temp_rise)))
                self.txtCaseTemp.set_text(str(fmt.format(self.case_temp)))

                self.fxdRelInputQuad1.show()
                self.fxdRelInputQuad4.show()

                #if self._component is not None:
                #    self.part.assessment_inputs_load(self)

            else:
                self.fxdRelInputQuad1.hide()
                self.fxdRelInputQuad4.hide()

            # Let the user know if the selected part does not have a part
            # category selected.
            if self.category_id < 1:
                self.lblNoCategory.show()
            else:
                self.lblNoCategory.hide()

            # Let the user know if the selected part does not have a part
            # subcategory selected.
            if self.subcategory_id < 1:
                self.lblNoSubCategory.show()
            else:
                self.lblNoSubCategory.hide()

            return False

        (_model, _row) = self.treeview.get_selection().get_selected()

        self.assembly_id = _model.get_value(_row, 1)

        if _model.get_value(_row, 63) == 1:  # Is a component.
            try:
                self.ht_model = dict(_model.get_value(_row, 88))
            except:
                self._app.user_log.error(_(u"No model dictionary for "
                                           u"part %s") %
                                         _model.get_value(_row, 68))
                self.ht_model = {}

        if self._app.winWorkBook.get_child() is not None:
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxHardware)
        self._app.winWorkBook.show_all()

        _load_general_data_tab(self)
        _load_assessment_inputs_tab(self)
        self.load_assessment_results_tab()
        self._load_fmeca_tab()

        # Load and show the assembly-specific pages if the selected hardware
        # item is an assembly.  Otherwise, hide the assembly-specific pages.
        if not self.part:
            _load_allocation_tab(self, _model, _row)
            _load_hazard_analysis_tab(self)
            _load_similar_item_tab(self)
            #_load_maintenance_planning_tab(self)
            if self.notebook.get_nth_page(1) != self.hbxAllocation:
                self.notebook.insert_page(self.hbxAllocation,
                                          tab_label=self.lblAllocation,
                                          position=1)
            if self.notebook.get_nth_page(2) != self.hpnHazardAnalysis:
                self.notebook.insert_page(self.hpnHazardAnalysis,
                                          tab_label=self.lblHazardAnalysis,
                                          position=2)
            if self.notebook.get_nth_page(3) != self.fraSIA:
                self.notebook.insert_page(self.fraSIA,
                                          tab_label=self.lblSIA,
                                          position=3)
        else:
            _page_num_ = self.notebook.page_num(self.hbxAllocation)
            self.notebook.remove_page(_page_num_)
            _page_num_ = self.notebook.page_num(self.hpnHazardAnalysis)
            self.notebook.remove_page(_page_num_)
            _page_num_ = self.notebook.page_num(self.fraSIA)
            self.notebook.remove_page(_page_num_)

        _title_ = _(u"RTK Work Book: Analyzing %s") % self.name
        self._app.winWorkBook.set_title(_title_)

        self.notebook.set_current_page(self._selected_tab)
        self._notebook_page_switched(self.notebook, None, self._selected_tab)

        return False

    def load_assessment_results_tab(self):
        """
        Method to load the widgets on the Assessment Results page.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        self.txtCompRefDes.set_text(self.comp_ref_des)

        self.txtActiveHt.set_text(str(fmt.format(self.failure_rate_active)))
        self.txtDormantHt.set_text(str(fmt.format(self.failure_rate_dormant)))
        self.txtSoftwareHt2.set_text(
            str(fmt.format(self.failure_rate_software)))
        self.txtPredictedHt.set_text(str(fmt.format(self.failure_rate)))
        self.txtMissionHt.set_text(str(fmt.format(self.failure_rate_mission)))
        self.txtHtPerCent.set_text(str(fmt.format(self.failure_rate_percent)))

        self.txtMTBF.set_text(str('{0:0.2f}'.format(self.mtbf)))
        self.txtMissionMTBF.set_text(str('{0:0.2f}'.format(self.mtbf_mission)))

        self.txtReliability.set_text(str(fmt.format(self.reliability)))
        self.txtMissionRt.set_text(str(fmt.format(self.reliability_mission)))

        self.txtMPMT.set_text(str('{0:0.2f}'.format(self.mpmt)))
        self.txtMCMT.set_text(str('{0:0.2f}'.format(self.mcmt)))
        self.txtMTTR.set_text(str('{0:0.2f}'.format(self.mttr)))
        self.txtMMT.set_text(str('{0:0.2f}'.format(self.mmt)))

        self.txtAvailability.set_text(str(fmt.format(self.availability)))
        self.txtMissionAt.set_text(str(fmt.format(self.availability_mission)))

        self.txtTotalCost.set_text(str(locale.currency(self.cost)))
        self.txtCostFailure.set_text(
            str(locale.currency(self.cost_per_failure)))
        self.txtCostHour.set_text(str('${0:0.4g}'.format(self.cost_per_hour)))

        self.txtAssemblyCrit.set_text(str(self.assembly_criticality))
        self.txtPartCount.set_text(str(fmt.format(self.n_parts)))
        self.txtTotalPwr.set_text(str(fmt.format(self.total_power)))

        if self.part:
            self.txtCurrentRatio.set_text(str(fmt.format(self.current_ratio)))
            self.txtPwrRatio.set_text(str(fmt.format(self.power_ratio)))
            self.txtVoltageRatio.set_text(str(fmt.format(self.voltage_ratio)))

            self.chkOverstressed.set_active(self.overstress)

            #self._component.assessment_results_load(self)

            _derate = self.figDerate.add_subplot(111)
            _derate.set_title(_(u"Derating Curve for %s at %s") %
                              (self.txtPartNum.get_text(),
                               self.txtRefDes.get_text()))
            _derate.set_xlabel(_(u"Temperature (\u2070C)"))
            _derate.set_ylabel(_(u"Power (Watts)"))

            # Set up the x, y coordinates for the operating point plot.
            _x_ = []
            _y_ = []
            _x_.append(float(self.min_temp))
            _x_.append(float(self.knee_temp))
            _x_.append(float(self.max_temp))
            _y_.append(float(self.rated_power))
            _y_.append(float(self.rated_power))
            _y_.append(0.0)

            _derate.plot(_x_, _y_, 'r.-', linewidth=2)
            _derate.plot(self.case_temp, self.op_power, 'go')
            if _x_[0] != _x_[2] and _y_[0] != _y_[2]:
                _derate.axis(
                    [0.95 * _x_[0], 1.05 * _x_[2], _y_[2], 1.05 * _y_[0]])
            else:
                _derate.axis([0.95, 1.05, 0.0, 1.05])

            self.chkOverstressed.show()
            self.fraDerate.show()
            self.fxdCalcResultsQuad4.show()
            self.txtCurrentRatio.show()
            self.txtPwrRatio.show()
            self.txtVoltageRatio.show()

        else:
            self.chkOverstressed.hide()
            self.fraDerate.hide()
            self.fxdCalcResultsQuad4.hide()
            self.txtCurrentRatio.hide()
            self.txtPwrRatio.hide()
            self.txtVoltageRatio.hide()

        return False

    def _load_fmeca_tab(self):
        """
        Method to load the widgets on the FMEA/FMECA page.
        """

        self._ItemCA = {}

        _model_ = self.tvwFMECA.get_model()
        _model_.clear()

        # Load the mission phase gtk.CellRendererCombo.
        _column_ = self.tvwFMECA.get_column(self._FMECA_col_order[2])
        _cell_ = _column_.get_cell_renderers()
        _cellmodel_ = _cell_[0].get_property('model')
        _cellmodel_.clear()

        _query_ = "SELECT fld_phase_id, fld_phase_name, fld_phase_start, \
                          fld_phase_end \
                   FROM tbl_mission_phase \
                   WHERE fld_mission_id=%d" % 0
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        try:
            _n_phases_ = len(_results_)
        except TypeError:
            _util.application_error(_(
                u"There was a problem loading the mission phase list in the Assembly Work Book FMEA/FMECA tab.  This may indicate your RTK program database is corrupt."))
            _n_phases_ = 0

        _cellmodel_.append([""])
        for i in range(_n_phases_):
            self._mission_phase[_results_[i][0]] = float(
                _results_[i][3]) - float(_results_[i][2])
            _cellmodel_.append([_results_[i][1]])

        # Load the failure modes to the gtk.TreeView.
        _query_ = "SELECT t1.fld_mode_id, t1.fld_mode_description, \
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
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        try:
            _n_modes_ = len(_results_)
        except TypeError:
            _n_modes_ = 0

        _icon_ = _conf.ICON_DIR + '32x32/mode.png'
        _icon_ = gtk.gdk.pixbuf_new_from_file_at_size(_icon_, 16,
                                                      16)  # @UndefinedVariable
        for i in range(_n_modes_):
            self._CA[_results_[i][0]] = [_results_[i][14],
                                         _results_[i][15],
                                         _results_[i][24],
                                         _results_[i][17],
                                         _results_[i][11], 0.0, 0.0]
            try:
                self._ItemCA[self.assembly_id].append([_results_[i][0],
                                                       _results_[i][11], ''])
            except KeyError:
                self._ItemCA[self.assembly_id] = [[_results_[i][0],
                                                   _results_[i][11], '']]

            _data_ = [_results_[i][self._FMECA_col_order[0]],
                      _util.none_to_string(
                          _results_[i][self._FMECA_col_order[1]]),
                      _util.none_to_string(
                          _results_[i][self._FMECA_col_order[2]]),
                      _util.none_to_string(
                          _results_[i][self._FMECA_col_order[3]]),
                      _util.none_to_string(
                          _results_[i][self._FMECA_col_order[4]]),
                      _util.none_to_string(
                          _results_[i][self._FMECA_col_order[5]]),
                      _util.none_to_string(
                          _results_[i][self._FMECA_col_order[6]]),
                      _util.none_to_string(
                          _results_[i][self._FMECA_col_order[7]]),
                      _util.none_to_string(
                          _results_[i][self._FMECA_col_order[8]]),
                      _util.none_to_string(
                          _results_[i][self._FMECA_col_order[9]]),
                      _util.none_to_string(
                          _results_[i][self._FMECA_col_order[10]]),
                      _util.none_to_string(
                          _results_[i][self._FMECA_col_order[11]]),
                      _util.none_to_string(
                          _results_[i][self._FMECA_col_order[12]]),
                      _util.none_to_string(
                          _results_[i][self._FMECA_col_order[13]]),
                      _util.none_to_string(
                          _results_[i][self._FMECA_col_order[14]]),
                      str(_results_[i][self._FMECA_col_order[15]]),
                      str(_results_[i][self._FMECA_col_order[16]]),
                      str(_results_[i][self._FMECA_col_order[17]]),
                      str(_results_[i][self._FMECA_col_order[18]]),
                      _util.none_to_string(_results_[i][25]),
                      str(_results_[i][self._FMECA_col_order[19]]),
                      str(_results_[i][self._FMECA_col_order[20]]),
                      _results_[i][self._FMECA_col_order[21]],
                      _results_[i][self._FMECA_col_order[22]],
                      _util.none_to_string(
                          _results_[i][self._FMECA_col_order[23]]),
                      0, '#FFFFFF', True, _icon_]

            # Load the FMECA gtk.TreeView with the data.
            try:
                _model_.append(None, _data_)
            except TypeError:
                _util.application_error(_(
                    u"Failed to load FMEA/FMECA failure mode %d" %
                    _results_[i][2]))

            # Load the FMECA dictionary with the data.
            self._fmeca[_results_[i][self._FMECA_col_order[0]]] = _data_[1:25]

        # Load the failure consequences to the FMECA dictionary.
        _query_ = "SELECT * FROM tbl_failure_consequences \
                   WHERE fld_assembly_id=%d" % self.assembly_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        try:
            _n_modes_ = len(_results_)
        except TypeError:
            _n_modes_ = 0

        for i in range(_n_modes_):
            self._fmeca[_results_[i][1]].append(_results_[i][2])
            self._fmeca[_results_[i][1]].append(_results_[i][3])
            self._fmeca[_results_[i][1]].append(_results_[i][4])
            self._fmeca[_results_[i][1]].append(_results_[i][5])
            self._fmeca[_results_[i][1]].append(_results_[i][6])
            self._fmeca[_results_[i][1]].append(_results_[i][7])
            self._fmeca[_results_[i][1]].append(_results_[i][8])
            self._fmeca[_results_[i][1]].append(_results_[i][9])
            self._fmeca[_results_[i][1]].append(_results_[i][10])

        # Load the failure mechanisms to the gtk.TreeView.
        _query_ = "SELECT t1.fld_assembly_id, t1.fld_mode_id, \
                          t1.fld_mechanism_id, t1.fld_mechanism_description, \
                          t1.fld_rpn_occurrence, t1.fld_rpn_detection, \
                          t1.fld_rpn, t1.fld_rpn_occurrence_new, \
                          t1.fld_rpn_detection_new, t1.fld_rpn_new, \
                          t1.fld_parent, t2.fld_rpn_severity, \
                          t2.fld_rpn_severity_new \
                   FROM tbl_fmeca_mechanisms AS t1 \
                   INNER JOIN tbl_fmeca AS t2 ON t2.fld_mode_id=t1.fld_mode_id \
                   WHERE t1.fld_assembly_id=%d" % self.assembly_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        try:
            _n_mechanisms_ = len(_results_)
        except TypeError:
            _n_mechanisms_ = 0

        _icon_ = _conf.ICON_DIR + '32x32/mechanism.png'
        _icon_ = gtk.gdk.pixbuf_new_from_file_at_size(_icon_, 16,
                                                      16)  # @UndefinedVariable
        for i in range(_n_mechanisms_):
            _piter_ = _model_.get_iter_from_string(_results_[i][10])
            self._mechanisms[_results_[i][2]] = [_results_[i][3],
                                                 _results_[i][4],
                                                 _results_[i][5],
                                                 _results_[i][6],
                                                 _results_[i][7],
                                                 _results_[i][8],
                                                 _results_[i][9],
                                                 _results_[i][10]]
            self._RPN[_results_[i][2]] = [self._rpnsev[_results_[i][11]],
                                          _results_[i][4],
                                          _results_[i][5],
                                          _results_[i][6],
                                          self._rpnsev[_results_[i][12]],
                                          _results_[i][7],
                                          _results_[i][8],
                                          _results_[i][9]]
            _data_ = [_results_[i][2],
                      _util.none_to_string(_results_[i][3]), "", "", "",
                      "", "", "", "", "", "", "", "", "", "", "", "", "",
                      "", "", "", "", 0, 0, "", 1, '#D3D3D3', False,
                      _icon_]

            try:
                _model_.insert(_piter_, i, _data_)
            except TypeError:
                _util.application_error(_(
                    u"Failed to load FMEA/FMECA failure mechanism %d" %
                    _results_[i][2]))

        # Load the actions to the gtk.TreeView.
        _query_ = "SELECT * FROM tbl_fmeca_actions \
                   WHERE fld_assembly_id=%d" % self.assembly_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        try:
            _n_actions_ = len(_results_)
        except TypeError:
            _n_actions_ = 0

        _icon_ = _conf.ICON_DIR + '32x32/action.png'
        _icon_ = gtk.gdk.pixbuf_new_from_file_at_size(_icon_, 16,
                                                      16)  # @UndefinedVariable
        for i in range(_n_actions_):
            _piter_ = _model_.get_iter_from_string(_results_[i][14])
            self._fmeca_actions[_results_[i][3]] = [_results_[i][4],
                                                    _results_[i][5],
                                                    _results_[i][6],
                                                    _results_[i][7],
                                                    _results_[i][8],
                                                    _results_[i][9],
                                                    _results_[i][10],
                                                    _results_[i][11],
                                                    _results_[i][12],
                                                    _results_[i][13],
                                                    _results_[i][14]]
            _data_ = [_results_[i][3],
                      _util.none_to_string(_results_[i][4]), "", "", "",
                      "", "", "", "", "", "", "", "", "", "", "", "", "",
                      "", "", "", "", 0, 0, "", 3, '#D3D3D3', False,
                      _icon_]

            try:
                _model_.insert(_piter_, i, _data_)
            except TypeError:
                _util.application_error(_(
                    u"Failed to load FMEA/FMECA action %d" % _results_[i][3]))

        # Load the controls to the gtk.TreeView.
        _query_ = "SELECT * FROM tbl_fmeca_controls \
                   WHERE fld_assembly_id=%d" % self.assembly_id

        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        try:
            _n_controls_ = len(_results_)
        except TypeError:
            _n_controls_ = 0

        _icon_ = _conf.ICON_DIR + '32x32/control.png'
        _icon_ = gtk.gdk.pixbuf_new_from_file_at_size(_icon_, 16,
                                                      16)  # @UndefinedVariable
        for i in range(_n_controls_):
            try:
                _piter_ = _model_.get_iter_from_string(_results_[i][6])
            except ValueError:
                _piter_ = None
            self._fmeca_controls[_results_[i][3]] = [_results_[i][4],
                                                     _results_[i][5],
                                                     _results_[i][6]]
            _data_ = [_results_[i][3],
                      _util.none_to_string(_results_[i][4]), "", "", "",
                      "", "", "", "", "", "", "", "", "", "", "", "", "",
                      "", "", "", "", 0, 0, "", 2, '#D3D3D3', False,
                      _icon_]

            try:
                _model_.insert(_piter_, i, _data_)
            except TypeError:
                _util.application_error(_(
                    u"Failed to load FMEA/FMECA control %d" % _results_[i][3]))

        # Fully expand the FMECA gtk.TreeView.
        _root_ = _model_.get_iter_root()
        if _root_ is not None:
            _path_ = _model_.get_path(_root_)
            self.tvwFMECA.expand_all()
            _col_ = self.tvwFMECA.get_column(1)
            self.tvwFMECA.set_cursor(_path_, _col_, False)
            self.tvwFMECA.row_activated(_path_, _col_)

        return False

    def _update_tree(self, columns, values):
        """
        Updates the values in the HARDWARE class gtk.TreeView().

        Keyword Arguments:
        columns -- a list of integers representing the column numbers to
                   update.
        values  -- a list of new values for the HARDWARE class TreeView().
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        for i in columns:
            _model_.set_value(_row_, i, values[i])

        return False

    def _update_attributes(self):
        """
        Method to update the HARDWARE class attributes.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        self._add_adj_factor = _model_.get_value(_row_, self._col_order[2])
        self.allocation_type = _model_.get_value(_row_, self._col_order[3])
        self.alt_part_num = _model_.get_value(_row_, self._col_order[4])
        self.assembly_criticality = _model_.get_value(_row_,
                                                      self._col_order[5])
        self.attachments = _model_.get_value(_row_, self._col_order[6])
        self.availability = _model_.get_value(_row_, self._col_order[7])
        self.availability_mission = _model_.get_value(_row_,
                                                      self._col_order[8])
        self.cage_code = _model_.get_value(_row_, self._col_order[9])
        self.calculation_model = _model_.get_value(_row_, self._col_order[10])
        self.category_id = _model_.get_value(_row_, self._col_order[11])
        self.comp_ref_des = _model_.get_value(_row_, self._col_order[12])
        self.cost = _model_.get_value(_row_, self._col_order[13])
        self.cost_per_failure = _model_.get_value(_row_, self._col_order[14])
        self.cost_per_hour = _model_.get_value(_row_, self._col_order[15])
        self.cost_type = _model_.get_value(_row_, self._col_order[16])
        self.description = _model_.get_value(_row_, self._col_order[17])
        self.detection_fr = _model_.get_value(_row_, self._col_order[18])
        self.detection_percent = _model_.get_value(_row_, self._col_order[19])
        self.duty_cycle = _model_.get_value(_row_, self._col_order[20])
        self.entered_by = _model_.get_value(_row_, self._col_order[21])
        self.environment_active = _model_.get_value(_row_, self._col_order[22])
        self.environment_dormant = _model_.get_value(_row_,
                                                     self._col_order[23])
        self.failure_dist = _model_.get_value(_row_, self._col_order[24])
        self.failure_parameter_1 = _model_.get_value(_row_,
                                                     self._col_order[25])
        self.failure_parameter_2 = _model_.get_value(_row_,
                                                     self._col_order[26])
        self.failure_parameter_3 = _model_.get_value(_row_,
                                                     self._col_order[27])
        self.failure_rate = _model_.get_value(_row_, self._col_order[32])
        self.failure_rate_lcl = _model_.get_value(_row_, self._col_order[93])
        self.failure_rate_ucl = _model_.get_value(_row_, self._col_order[94])
        self.failure_rate_active = _model_.get_value(_row_,
                                                     self._col_order[28])
        self.failure_rate_dormant = _model_.get_value(_row_,
                                                      self._col_order[29])
        self.failure_rate_mission = _model_.get_value(_row_,
                                                      self._col_order[30])
        self.failure_rate_percent = _model_.get_value(_row_,
                                                      self._col_order[31])
        self.failure_rate_software = _model_.get_value(_row_,
                                                       self._col_order[33])
        self.failure_rate_specified = _model_.get_value(_row_,
                                                        self._col_order[34])
        self.failure_rate_type = _model_.get_value(_row_, self._col_order[35])
        self.figure_number = _model_.get_value(_row_, self._col_order[36])
        self.humidity = _model_.get_value(_row_, self._col_order[37])
        self.image_file = _model_.get_value(_row_, self._col_order[38])
        self.isolation_fr = _model_.get_value(_row_, self._col_order[39])
        self.isolation_percent = _model_.get_value(_row_, self._col_order[40])
        self.lcn = _model_.get_value(_row_, self._col_order[41])
        self.level = _model_.get_value(_row_, self._col_order[42])
        self.manufacturer = _model_.get_value(_row_, self._col_order[43])
        self.mission_time = _model_.get_value(_row_, self._col_order[45])
        self.modified_by = _model_.get_value(_row_, self._col_order[47])
        self.mcmt = _model_.get_value(_row_, self._col_order[44])
        self.mmt = _model_.get_value(_row_, self._col_order[46])
        self.mpmt = _model_.get_value(_row_, self._col_order[48])
        self.mtbf = _model_.get_value(_row_, self._col_order[50])
        self.mtbf_lcl = _model_.get_value(_row_, self._col_order[91])
        self.mtbf_ucl = _model_.get_value(_row_, self._col_order[92])
        self.mtbf_mission = _model_.get_value(_row_, self._col_order[49])
        self.mtbf_specified = _model_.get_value(_row_, self._col_order[51])
        self.mttr = _model_.get_value(_row_, self._col_order[52])
        self.mttr_specified = _model_.get_value(_row_, self._col_order[55])
        self.mttr_add_adj_factor = _model_.get_value(_row_,
                                                     self._col_order[53])
        self.mttr_mult_adj_factor = _model_.get_value(_row_,
                                                      self._col_order[54])
        self.mttr_type = _model_.get_value(_row_, self._col_order[56])
        self.mult_adj_factor = _model_.get_value(_row_, self._col_order[57])
        self.name = _model_.get_value(_row_, self._col_order[58])
        self.nsn = _model_.get_value(_row_, self._col_order[59])
        self.overstress = _model_.get_value(_row_, self._col_order[60])
        self.page_number = _model_.get_value(_row_, self._col_order[61])
        self.parent_assembly = _model_.get_value(_row_, self._col_order[62])
        self.part = _model_.get_value(_row_, self._col_order[63])
        self.part_number = _model_.get_value(_row_, self._col_order[64])
        self.percent_isolation_group_ri = _model_.get_value(_row_,
                                                            self._col_order[
                                                                65])
        self.percent_isolation_single_ri = _model_.get_value(_row_,
                                                             self._col_order[
                                                                 66])
        self.quantity = _model_.get_value(_row_, self._col_order[67])
        self.ref_des = _model_.get_value(_row_, self._col_order[68])
        self.reliability_mission = _model_.get_value(_row_,
                                                     self._col_order[69])
        self.reliability = _model_.get_value(_row_, self._col_order[70])
        self.remarks = _model_.get_value(_row_, self._col_order[71])
        self.repair_dist = _model_.get_value(_row_, self._col_order[72])
        self.repair_parameter_1 = _model_.get_value(_row_, self._col_order[73])
        self.repair_parameter_2 = _model_.get_value(_row_, self._col_order[74])
        self.repairable = _model_.get_value(_row_, self._col_order[75])
        self.rpm = _model_.get_value(_row_, self._col_order[76])
        self.specification = _model_.get_value(_row_, self._col_order[77])
        self.subcategory_id = _model_.get_value(_row_, self._col_order[78])
        self.tagged = _model_.get_value(_row_, self._col_order[79])
        self.temperature_active = _model_.get_value(_row_, self._col_order[80])
        self.temperature_dormant = _model_.get_value(_row_,
                                                     self._col_order[81])
        self.n_parts = _model_.get_value(_row_, self._col_order[82])
        self.total_power = _model_.get_value(_row_, self._col_order[83])
        self.vibration = _model_.get_value(_row_, self._col_order[84])
        self.weibull_data_set = _model_.get_value(_row_, self._col_order[85])
        self.weibull_file = _model_.get_value(_row_, self._col_order[86])
        self.year_of_manufacture = _model_.get_value(_row_,
                                                     self._col_order[87])
        self.ht_model = _model_.get_value(_row_, self._col_order[88])
        self.rel_goal_measure = _model_.get_value(_row_, self._col_order[89])
        self.rel_goal = _model_.get_value(_row_, self._col_order[90])

        if self.part:
            _selection = self._app.winParts.tvwPartsList.get_selection()
            (_model_, _row_) = _selection.get_selected()

            self.burnin_temp = 0.0
            self.burnin_time = 0.0
            self.lab_devices = 0.0
            self.lab_time = 0.0
            self.lab_temp = 0.0
            self.lab_failures = 0.0
            self.field_time = 0.0
            self.field_failures = 0.0
            self.min_temp = 0.0
            self.knee_temp = 0.0
            self.max_temp = 0.0
            self.rated_current = 0.0
            self.rated_power = 0.0
            self.rated_voltage = 0.0
            self.op_current = 0.0
            self.op_power = 0.0
            self.op_voltage = 0.0
            self.current_ratio = 1.0
            self.voltage_ratio = 1.0
            self.power_ratio = 1.0
            self.theta_jc = 0.0
            self.temp_rise = 0.0
            self.case_temp = 0.0

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the HARDWARE class
        gtk.TreeView().

        Keyword Arguments:
        treeview -- the HARDWARE class gtkTreeView().
        event    -- a gtk.gdk.Event() that called this function (the
                    important attribute is which mouse button was clicked).
                    1 = left
                    2 = scrollwheel
                    3 = right
                    4 = forward
                    5 = backward
                    8 =
                    9 =
        """

        if event.button == 1:
            self._treeview_row_changed(treeview, None, 0)
        elif event.button == 3:
            print "Pop-up a menu!"

        return False

    def _treeview_row_changed(self, __treeview, __path, __column):
        """
        Callback function to handle events for the HARDWARE class
        gtk.TreeView().  It is called whenever the HARDWARE class
        gtk.TreeView() is clicked or a row is activated.  It loads the HARDWARE
        class.

        Keyword Arguments:
        __treeview -- the HARDWARE class gtk.TreeView().
        __path     -- the activated row gtk.TreeView() path.
        __column   -- the activated gtk.TreeViewColumn().
        """

        # Save the previously selected row in the Hardware tree.
        #if self.selected_row is not None:
        #_path_ = self.model.get_path(self.selected_row)
        #self._save_line(self.model, _path_, self.selected_row)

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        # Save the previously selected row in the Parts List.
        (_partmodel_,
         _partrow_) = self._app.winParts.tvwPartsList.get_selection().get_selected()

        if _partrow_ is not None and \
                        _row_ is not None and \
                        _model_.get_value(_row_, 63) == 1:
            _path_ = _partmodel_.get_path(_partrow_)
            self._app.winParts.save_line_item(_partmodel_, _path_, _partrow_)

        if _row_ is not None:
            self.revision_id = _model_.get_value(_row_, self._col_order[0])
            self.assembly_id = _model_.get_value(_row_, self._col_order[1])

            self._update_attributes()

        if _model_.get_value(_row_, 63) == 0:  # Is an assembly.
            _path_ = _model_.get_string_from_iter(_row_)
        elif _model_.get_value(_row_, 63) == 1:  # Is a component.
            _row_ = _model_.iter_parent(_row_)
            _path_ = _model_.get_string_from_iter(_row_)

        # Build the queries to select the reliability tests and program
        # incidents associated with the selected HARDWARE item.
        qryParts = "SELECT t1.*, t2.fld_part_number, t2.fld_ref_des \
                    FROM tbl_prediction AS t1 \
                    INNER JOIN tbl_system AS t2 \
                    ON t1.fld_assembly_id=t2.fld_assembly_id \
                    WHERE t2.fld_revision_id=%d \
                    AND t2.fld_parent_assembly='%s'" % \
                   (self._app.REVISION.revision_id, _path_)
        qryIncidents = "SELECT * FROM tbl_incident\
                        WHERE fld_revision_id=%d \
                        AND fld_hardware_id=%d \
                        ORDER BY fld_incident_id" % \
                       (self._app.REVISION.revision_id, self.assembly_id)
        qryDatasets = "SELECT * FROM tbl_dataset \
                       WHERE fld_assembly_id=%d" % self.assembly_id

        self._app.winParts.load_part_tree(qryParts)
        self._app.winParts.load_incident_tree(qryIncidents, None)
        self._app.winParts.load_dataset_tree(qryDatasets, None)

        if _row_ is not None:
            if _model_.get_value(_row_, 63) == 0:  # Is an assembly.
                self.part = False
                self.assembly = _path_

            elif _model_.get_value(_row_, 63) == 1:  # Is a component.
                self.part = True
                self.assembly = _model_.get_value(_row_, 62)
                self._set_parts_list_row()

            self.load_notebook()

            return False
        else:
            return True

    def _fmeca_treeview_row_changed(self, __treeview, __path, __column):
        """
        Method to load the correct gtk.Fixed() when changing rows in the FMECA
        gtk.TreeView().

        Keyword Arguments:
        __treeview -- the HARDWARE class FMECA gtk.TreeView.
        __path     -- the actived row gtk.TreeView path.
        __column   -- the actived gtk.TreeViewColumn.
        """

        # Remove the existing gtk.Fixed() widget.
        if self.fraFMECADetails.get_child() is not None:
            self.fraFMECADetails.remove(self.fraFMECADetails.get_child())

        (_model_, _row_) = self.tvwFMECA.get_selection().get_selected()

        _fmeca_len_ = len(self._FMECA_col_order)
        _type_ = _model_.get_value(_row_, _fmeca_len_)

        if _type_ == 0:  # Failure mode.
            self.fraFMECADetails.add(self.fxdMode)

            _label_ = self.fraFMECADetails.get_label_widget()
            _label_.set_markup(
                "<span weight='bold'>Failure Mode Consequence</span>")

        elif _type_ == 1:  # Failure mechanism.
            _id_ = _model_.get_value(_row_, 0)
            self.txtMechanismID.set_text(str(_id_))
            self.txtMechanismDescription.set_text(_model_.get_value(_row_, 1))
            self.cmbOccurenceI.set_active(self._mechanisms[_id_][1])
            self.cmbDetectionI.set_active(self._mechanisms[_id_][2])
            self.txtRPNI.set_text(str(self._mechanisms[_id_][3]))
            self.cmbOccurrenceN.set_active(self._mechanisms[_id_][4])
            self.cmbDetectionN.set_active(self._mechanisms[_id_][5])
            self.txtRPNN.set_text(str(self._mechanisms[_id_][6]))

            self.fraFMECADetails.add(self.fxdMechanism)
            _label_ = self.fraFMECADetails.get_label_widget()
            _label_.set_markup(
                "<span weight='bold'>Failure Mechanism/Cause</span>")

        elif _type_ == 2:  # Control
            _id_ = _model_.get_value(_row_, 0)
            self.txtControlID.set_text(str(_id_))
            self.txtControlDescription.set_text(
                _util.none_to_string(self._fmeca_controls[_id_][0]))
            self.cmbControlType.set_active(self._fmeca_controls[_id_][1])

            self.fraFMECADetails.add(self.fxdControl)
            _label_ = self.fraFMECADetails.get_label_widget()
            _label_.set_markup(
                "<span weight='bold'>Failure Mechanism/Cause Control</span>")

        elif _type_ == 3:  # Action
            _id_ = _model_.get_value(_row_, 0)
            self.txtActionID.set_text(str(_id_))
            _buffer = \
                self.txtActionRecommended.get_children()[0].get_children()[
                    0].get_buffer()
            _buffer.set_text(
                _util.none_to_string(self._fmeca_actions[_id_][0]))
            self.cmbActionCategory.set_active(
                int(self._fmeca_actions[_id_][1]))
            self.cmbActionResponsible.set_active(
                int(self._fmeca_actions[_id_][2]))
            _date_ = str(datetime.fromordinal(
                int(self._fmeca_actions[_id_][3])).strftime('%Y-%m-%d'))
            self.txtActionDueDate.set_text(_date_)
            self.cmbActionStatus.set_active(int(self._fmeca_actions[_id_][4]))
            _buffer = self.txtActionTaken.get_children()[0].get_children()[
                0].get_buffer()
            _buffer.set_text(
                _util.none_to_string(self._fmeca_actions[_id_][5]))
            self.cmbActionApproved.set_active(
                int(self._fmeca_actions[_id_][6]))
            _date_ = str(datetime.fromordinal(
                int(self._fmeca_actions[_id_][7])).strftime('%Y-%m-%d'))
            self.txtActionApproveDate.set_text(_date_)
            self.cmbActionClosed.set_active(int(self._fmeca_actions[_id_][8]))
            _dte = str(datetime.fromordinal(
                int(self._fmeca_actions[_id_][9])).strftime('%Y-%m-%d'))
            self.txtActionCloseDate.set_text(_date_)

            self.fraFMECADetails.add(self.fxdAction)
            _label_ = self.fraFMECADetails.get_label_widget()
            _label_.set_markup(
                "<span weight='bold'>Failure Mechanism/Cause Action Details</span>")

        self.fraFMECADetails.show_all()

        return False

    def _add_hardware(self, __button, kind):
        """
        Method to add a new hardware item to the open RTK program database.

        :param __button: the gtk.Button() that called this method.
        :type __button: gtk.Button
        :param kind: the kind of Assembly to add.
                      0 = sibling assembly
                      1 = child assembly
                      2 = component
        :type kind: integer
        :return: False or True
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        if self.part and (kind == 0 or kind == 1):
            _util.application_error(_(
                u"An assembly can not be added as a child of a component.  "
                u"Please select an assembly to create a child assembly."))
            return True

        if kind == 0:
            _iter = _model_.iter_parent(_row_)
            try:
                _parent_ = _model_.get_string_from_iter(_iter)
            except TypeError:
                _util.application_error(_(
                    u"A sibling assembly can not be added to the top-level "
                    u"assembly."))
                return True

            _title_ = _(u"RTK - Add Sibling Assemblies")
            _prompt_ = _(u"How many sibling assemblies to add?")

        elif kind == 1:
            _parent_ = _model_.get_string_from_iter(_row_)
            _title_ = _(u"RTK - Add Child Assemblies")
            _prompt_ = _(u"How many child assemblies to add?")

        elif kind == 2:
            _parent_ = _model_.get_string_from_iter(_row_)
            _title_ = _(u"RTK - Add Components")
            _prompt_ = _(u"How many components to add?")

        _n_new_assembly_ = _util.add_items(_title_, _prompt_)
        for i in range(_n_new_assembly_):  # @UnusedVariable
            # Create the default name of the assembly.
            _name_ = str(_conf.RTK_PREFIX[4]) + ' ' + str(_conf.RTK_PREFIX[5])

            # Increment the assembly index.
            _conf.RTK_PREFIX[5] = _conf.RTK_PREFIX[5] + 1

            _values_ = (self.revision_id, str(_conf.RTK_PROG_INFO[3]),
                        _parent_, _name_)

            # First we add the assembly to the system table.  Next we find the
            # # the ID of the newly inserted assembly.  Finally, we add this
            #  new assembly to the allocation table, risk analysis table,
            #  similar item table, and functional matrix table.
            _query_ = "SELECT MAX(fld_assembly_id) FROM tbl_system"
            _assembly_id_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx)
            _assembly_id_ = _assembly_id_[0][0] + 1

            _values_ = _values_ + (_assembly_id_,)
            _query_ = "INSERT INTO tbl_system \
                       (fld_revision_id, fld_entered_by, \
                        fld_parent_assembly, fld_description, \
                        fld_assembly_id) \
                       VALUES (%d, '%s', '%s', '%s', %d)" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if _results_ == '' or not _results_ or _results_ is None:
                self._app.debug_log.error(
                    "assembly.py: Failed to add new assembly to system table.")
                return True

            _values_ = (self.revision_id, _assembly_id_)
            _query_ = "INSERT INTO tbl_allocation \
                       (fld_revision_id, fld_assembly_id) \
                       VALUES (%d, %d)" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if _results_ == '' or not _results_ or _results_ is None:
                self._app.debug_log.error(
                    "assembly.py: Failed to add new assembly to allocation table.")
                return True

            _query = "INSERT INTO tbl_risk_matrix \
                      (fld_revision_id, fld_assembly_id) \
                      VALUES({0:d}, {1:d})".format(self.revision_id,
                                                   _assembly_id_)
            if self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                          commit=True):
                self._app.debug_log.error("assembly.py: Failed to add new "
                                          "assembly to risk matrix table.")
                return True

            _query_ = "INSERT INTO tbl_similar_item \
                       (fld_revision_id, fld_assembly_id) \
                       VALUES (%d, %d)" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if _results_ == '' or not _results_ or _results_ is None:
                self._app.debug_log.error(
                    "assembly.py: Failed to add new assembly to similar items table.")
                return True

            # Retrieve the list of function id's in the open RTK program
            # database.
            _query_ = "SELECT fld_function_id \
                       FROM tbl_functions \
                       WHERE fld_revision_id=%d" % self.revision_id
            _functions_ = self._app.DB.execute_query(_query_,
                                                     None,
                                                     self._app.ProgCnx)

            # Add a record to the functional matrix table for each function
            # that exists in the open RTK program database.
            for j in range(len(_functions_)):
                _values_ = (self.revision_id, _functions_[j][0], _assembly_id_)
                _query_ = "INSERT INTO tbl_functional_matrix \
                           (fld_revision_id, fld_function_id, \
                            fld_assembly_id) \
                           VALUES(%d, %d, %d)" % _values_
                _results_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx,
                                                       commit=True)

                if _results_ == '' or not _results_ or _results_ is None:
                    self._app.debug_log.error(
                        "assembly.py: Failed to add new assembly to functional matrix table.")

            if self.part:
                _values_ = (self.revision_id, _assembly_id_)
                _query_ = "INSERT INTO tbl_prediction \
                           (fld_revision_id, fld_assembly_id) \
                           VALUES (%d, %d)" % _values_
                _results_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx,
                                                       commit=True)

                if _results_ == '' or not _results_ or _results_ is None:
                    self._app.debug_log.error(
                        "hardware.py: Failed to add new component to prediction table.")

        self.load_tree()

        return False

    def _delete_hardware(self, __menuitem):
        """
        Deletes the currently selected hardware item from the open RTK Program
        database.

        Keyword Arguments:
        __menuitem -- the gtk.MenuItem() that called this function.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        # First delete all of the children from the system table.
        _query_ = "DELETE FROM tbl_system \
                   WHERE fld_parent_assembly='%s'" % \
                  _model_.get_string_from_iter(_row_)
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error(
                "assembly.py: Failed to delete assembly %d from system table." % self.assembly_id)
            return True

        # Second delete the parent from the system table, then from the
        # allocation table, hazard analysis table, similar item table, and
        # functional matrix.
        _values_ = (self.revision_id, _model_.get_value(_row_, 1))
        _query_ = "DELETE FROM tbl_system \
                   WHERE fld_revision_id=%d \
                   AND fld_assembly_id=%d" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error(
                "assembly.py: Failed to delete assembly %d from system table." % self.assembly_id)
            return True

        _query_ = "DELETE FROM tbl_allocation \
                   WHERE fld_revision_id=%d \
                   AND fld_assembly_id=%d" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error(
                "assembly.py: Failed to delete assembly %d from allocation table." % self.assembly_id)
            return True

        _query_ = "DELETE FROM tbl_risk_analysis \
                   WHERE fld_revision_id=%d \
                   AND fld_assembly_id=%d" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)
        if not _results_:
            self._app.debug_log.error(
                "assembly.py: Failed to delete assembly %d from risk analysis table." % self.assembly_id)
            return True

        _query_ = "DELETE FROM tbl_risk_matrix \
                   WHERE fld_revision_id=%d \
                   AND fld_assembly_id=%d" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error(
                "assembly.py: Failed to delete assembly %d from risk matrix table." % self.assembly_id)
            return True

        _query_ = "DELETE FROM tbl_similar_item \
                   WHERE fld_revision_id=%d \
                   AND fld_assembly_id=%d" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error(
                "assembly.py: Failed to delete assembly %d from similar item table." % self.assembly_id)
            return True

        _query_ = "DELETE FROM tbl_functional_matrix \
                   WHERE fld_revision_id=%d \
                   AND fld_assembly_id=%d" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error(
                "assembly.py: Failed to delete assembly %d from functional matrix table." % self.assembly_id)
            return True

        if self.part:
            _query_ = "DELETE FROM tbl_prediction \
                       WHERE fld_revision_id=%d \
                       AND fld_assembly_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if _results_ == '' or not _results_ or _results_ is None:
                self._app.debug_log.error(
                    "hardware.py: Failed to delete component from prediction table.")
                return True

        self.load_tree()

        return False

    def _set_parts_list_row(self):
        """
        Sets the corresponding row in the Parts List when a selected row in
        the HARDWARE class gtk.TreeView() is a component.
        """

        _model_ = self._app.winParts.tvwPartsList.get_model()
        _row_ = _model_.get_iter_first()
        while _model_.get_value(_row_, 1) != self.assembly_id:
            _row_ = _model_.iter_next(_row_)

        if _row_ is not None:
            self._app.winParts.selected_row = _row_
            _path_ = _model_.get_path(_row_)
            self._app.winParts.tvwPartsList.set_cursor(_path_)

        return False

    def save_hardware(self):
        """
        Saves the HARDWARE class gtk.TreeView information to the Program's
        MySQL or SQLite3 database.
        """

        def _save_line(model, __path, row, self):
            """
            Saves each row in the HARDWARE class gtk.TreeView() model to the
            RTK Program database.

            Keyword Arguments:
            model  -- the HARDWARE class gtk.Treemodel().
            __path -- the path of the active row in the HARDWARE class
                      gtk.Treemodel().
            row    -- the selected row in the HARDWARE class gtk.TreeView().
            """

            if _conf.BACKEND == 'mysql':
                ht_model = self._app.ProgCnx.escape_string(
                    model.get_value(row, self._col_order[88]))
            elif _conf.BACKEND == 'sqlite3':
                ht_model = model.get_value(row, self._col_order[88])

            _values_ = (model.get_value(row, self._col_order[2]),
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
                        model.get_value(row, self._col_order[27]),
                        model.get_value(row, self._col_order[28]),
                        model.get_value(row, self._col_order[29]),
                        model.get_value(row, self._col_order[30]),
                        model.get_value(row, self._col_order[31]),
                        model.get_value(row, self._col_order[32]),
                        model.get_value(row, self._col_order[33]),
                        model.get_value(row, self._col_order[34]),
                        model.get_value(row, self._col_order[35]),
                        model.get_value(row, self._col_order[36]),
                        model.get_value(row, self._col_order[37]),
                        model.get_value(row, self._col_order[38]),
                        model.get_value(row, self._col_order[39]),
                        model.get_value(row, self._col_order[40]),
                        model.get_value(row, self._col_order[41]),
                        model.get_value(row, self._col_order[42]),
                        model.get_value(row, self._col_order[43]),
                        model.get_value(row, self._col_order[44]),
                        model.get_value(row, self._col_order[45]),
                        model.get_value(row, self._col_order[46]),
                        model.get_value(row, self._col_order[47]),
                        model.get_value(row, self._col_order[48]),
                        model.get_value(row, self._col_order[49]),
                        model.get_value(row, self._col_order[50]),
                        model.get_value(row, self._col_order[51]),
                        model.get_value(row, self._col_order[52]),
                        model.get_value(row, self._col_order[53]),
                        model.get_value(row, self._col_order[54]),
                        model.get_value(row, self._col_order[55]),
                        model.get_value(row, self._col_order[56]),
                        model.get_value(row, self._col_order[57]),
                        model.get_value(row, self._col_order[58]),
                        model.get_value(row, self._col_order[59]),
                        model.get_value(row, self._col_order[60]),
                        model.get_value(row, self._col_order[61]),
                        model.get_value(row, self._col_order[62]),
                        model.get_value(row, self._col_order[63]),
                        model.get_value(row, self._col_order[64]),
                        model.get_value(row, self._col_order[65]),
                        model.get_value(row, self._col_order[66]),
                        model.get_value(row, self._col_order[67]),
                        model.get_value(row, self._col_order[68]),
                        model.get_value(row, self._col_order[69]),
                        model.get_value(row, self._col_order[70]),
                        model.get_value(row, self._col_order[71]),
                        model.get_value(row, self._col_order[72]),
                        model.get_value(row, self._col_order[73]),
                        model.get_value(row, self._col_order[74]),
                        model.get_value(row, self._col_order[75]),
                        model.get_value(row, self._col_order[76]),
                        model.get_value(row, self._col_order[77]),
                        model.get_value(row, self._col_order[78]),
                        model.get_value(row, self._col_order[79]),
                        model.get_value(row, self._col_order[80]),
                        model.get_value(row, self._col_order[81]),
                        model.get_value(row, self._col_order[82]),
                        model.get_value(row, self._col_order[83]),
                        model.get_value(row, self._col_order[84]),
                        model.get_value(row, self._col_order[85]),
                        model.get_value(row, self._col_order[86]),
                        model.get_value(row, self._col_order[87]),
                        ht_model,
                        model.get_value(row, self._col_order[89]),
                        model.get_value(row, self._col_order[90]),
                        self._app.REVISION.revision_id,
                        model.get_value(row, self._col_order[1]))

            _query_ = "UPDATE tbl_system \
                       SET fld_add_adj_factor=%f, fld_allocation_type=%d, \
                           fld_alt_part_number='%s', \
                           fld_assembly_criticality='%s', \
                           fld_attachments='%s', fld_availability=%f, \
                           fld_availability_mission=%f, fld_cage_code='%s', \
                           fld_calculation_model=%d, fld_category_id=%d, \
                           fld_comp_ref_des='%s', fld_cost=%f, \
                           fld_cost_failure=%f, fld_cost_hour=%f, \
                           fld_cost_type=%f, fld_description='%s', \
                           fld_detection_fr=%f, fld_detection_percent=%f, \
                           fld_duty_cycle=%f, fld_entered_by='%s', \
                           fld_environment_active=%d, \
                           fld_environment_dormant=%d, fld_failure_dist=%d, \
                           fld_failure_parameter_1=%f, \
                           fld_failure_parameter_2=%f, \
                           fld_failure_parameter_3=%f, \
                           fld_failure_rate_active=%f, \
                           fld_failure_rate_dormant=%f, \
                           fld_failure_rate_mission=%f, \
                           fld_failure_rate_percent=%f, \
                           fld_failure_rate_predicted=%f, \
                           fld_failure_rate_software=%f, \
                           fld_failure_rate_specified=%f, \
                           fld_failure_rate_type=%d, \
                           fld_figure_number='%s', fld_humidity=%f, \
                           fld_image_file='%s', fld_isolation_fr=%f, \
                           fld_isolation_percent=%f, fld_lcn='%s', \
                           fld_level=%d, fld_manufacturer=%d, \
                           fld_mcmt=%f, fld_mission_time=%f, \
                           fld_mmt=%f, fld_modified_by='%s', \
                           fld_mpmt=%f, fld_mtbf_mission=%f, \
                           fld_mtbf_predicted=%f, fld_mtbf_specified=%f, \
                           fld_mttr=%f, fld_mttr_add_adj_factor=%f, \
                           fld_mttr_mult_adj_factor=%f, \
                           fld_mttr_specified=%f, \
                           fld_mttr_type=%d, fld_mult_adj_factor=%f, \
                           fld_name='%s', fld_nsn='%s', \
                           fld_overstress=%d, fld_page_number='%s', \
                           fld_parent_assembly='%s', fld_part=%d, \
                           fld_part_number='%s', \
                           fld_percent_isolation_group_ri=%f, \
                           fld_percent_isolation_single_ri=%f, \
                           fld_quantity=%d, \
                           fld_ref_des='%s', fld_reliability_mission=%f, \
                           fld_reliability_predicted=%f, fld_remarks='%s', \
                           fld_repair_dist=%d, fld_repair_parameter_1=%f, \
                           fld_repair_parameter_2=%f, fld_repairable=%d, \
                           fld_rpm=%f, fld_specification_number='%s', \
                           fld_subcategory_id=%d, fld_tagged_part=%d, \
                           fld_temperature_active=%f, \
                           fld_temperature_dormant=%f, \
                           fld_total_part_quantity=%d, \
                           fld_total_power_dissipation=%f, \
                           fld_vibration=%f, fld_weibull_data_set=%d, \
                           fld_weibull_file='%s', \
                           fld_year_of_manufacture=%d, \
                           fld_ht_model='%s', \
                           fld_reliability_goal_measure=%d, \
                           fld_reliability_goal=%f \
                   WHERE fld_revision_id=%d AND fld_assembly_id=%d" % _values_

            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if _results_ == '' or not _results_ or _results_ is None:
                self._app.debug_log.error(
                    "hardware.py: Failed to save hardware to system table.")
                return True

            return False

        _model_ = self.treeview.get_model()
        _model_.foreach(_save_line, self)

        return False

    def _save_allocation(self):
        """
        Saves the HARDWARE class allocation analysis information to the open
        RTK Program database.
        """

        def _save_line(model, __path, row, self):
            """
            Saves a single row in the HARDWARE class allocation gtk.TreeModel()
            to the open RTK Program database.

            Keyword Arguments:
            model  -- the HARDWARE class allocation gtk.TreeModel().
            __path -- the path of the selected row in the HARDWARE class
                       allocation gtk.TreeModel().
            row    -- the selected row in the HARDWARE class allocation
                      gtk.TreeView().
            """

            _query = "UPDATE tbl_allocation \
                      SET fld_included={0:d}, \
                          fld_n_sub_systems={1:d}, \
                          fld_n_sub_elements={2:d}, \
                          fld_weight_factor={3:f}, \
                          fld_percent_wt_factor={4:f}, \
                          fld_int_factor={5:d}, \
                          fld_soa_factor={6:d}, \
                          fld_op_time_factor={7:d}, \
                          fld_env_factor={8:d}, \
                          fld_availability_alloc={9:f}, \
                          fld_reliability_alloc={10:f}, \
                          fld_failure_rate_alloc={11:f}, \
                          fld_mtbf_alloc={12:f} \
                      WHERE fld_revision_id={13:d} \
                      AND fld_assembly_id={14:d}".format(
                model.get_value(row, 3), model.get_value(row, 4),
                model.get_value(row, 5), model.get_value(row, 12),
                model.get_value(row, 13), model.get_value(row, 8),
                model.get_value(row, 9), model.get_value(row, 10),
                model.get_value(row, 11), model.get_value(row, 21),
                model.get_value(row, 19), model.get_value(row, 15),
                model.get_value(row, 17), model.get_value(row, 0),
                model.get_value(row, 1))
            _results_ = self._app.DB.execute_query(_query,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            # Trickle down the reliability goals.
            if self.chkApplyResults.get_active():

                _measure_ = self.cmbRqmtType.get_active()
                if _measure_ == 1:  # Expressed as reliability.
                    _value_ = model.get_value(row, 19)
                elif _measure_ == 2:  # Expressed as an MTBF.
                    _value_ = model.get_value(row, 17)
                elif _measure_ == 3:  # Expressed as a failure rate.
                    _value_ = model.get_value(row, 15)
                else:
                    _value_ = 1.0

                _values_ = (model.get_value(row, 15), \
                            model.get_value(row, 17), 3, _measure_, _value_, \
                            model.get_value(row, 0), model.get_value(row, 1))

                _query_ = "UPDATE tbl_system \
                           SET fld_failure_rate_specified=%f, \
                               fld_mtbf_specified=%f, \
                               fld_failure_rate_type=%d, \
                               fld_reliability_goal_measure=%d, \
                               fld_reliability_goal=%f \
                           WHERE fld_revision_id=%d \
                           AND fld_assembly_id=%d" % _values_
                _results_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx,
                                                       commit=True)

            if not _results_:
                self._app.debug_log.error("assembly.py: Failed to update "
                                          "system table with allocation "
                                          "results.")
                return True

            return False

        # Update the HARDWARE class gtk.TreeView() with the reliability goals.
        _measure_ = self.cmbRqmtType.get_active()
        if _measure_ == 1:
            _value_ = float(self.txtReliabilityGoal.get_text())
        elif _measure_ == 2:
            _value_ = float(self.txtMTBFGoal.get_text())
        elif _measure_ == 3:
            _value_ = float(self.txtFailureRateGoal.get_text())
        else:
            _value_ = 1.0

        # Update the allocation method.
        i = self.cmbAllocationType.get_active()
        (_model_, _row_) = self.treeview.get_selection().get_selected()
        _model_.set_value(_row_, 3, i)
        _model_.set_value(_row_, 89, _measure_)
        _model_.set_value(_row_, 90, _value_)

        # Save the results.
        self.save_hardware()

        # Save each of the lines in the allocation analysis table.
        _model_ = self.tvwAllocation.get_model()
        _model_.foreach(_save_line, self)

        if self.chkApplyResults.get_active():
            self.load_tree()

        return False

    def _save_hazard_analysis(self):
        """
        Saves the HARDWARE clss risk analysis information to the open RKT
        Program database.
        """

        def _save_line(model, __path, row, self):
            """
            Saves each row in the HARDWARE class risk analysis gtk.TreeModel
            to the open RTK Program database.

            Keyword Arguments:
            model  -- the HARDWARE class hazard analysis gtk.TreeModel().
            __path -- the path of the selected row in the HARDWARE class hazard
                       analysis gtk.TreeModel().
            row    -- the selected row in the HARDWARE class hazard analysis
                      gtk.TreeView().
            """

            if _conf.BACKEND == 'mysql':
                _equation1_ = self._app.ProgCnx.escape_string(
                    model.get_value(row, self._risk_col_order[22]))
                _equation2_ = self._app.ProgCnx.escape_string(
                    model.get_value(row, self._risk_col_order[23]))
                _equation3_ = self._app.ProgCnx.escape_string(
                    model.get_value(row, self._risk_col_order[24]))
                _equation4_ = self._app.ProgCnx.escape_string(
                    model.get_value(row, self._risk_col_order[25]))
                _equation5_ = self._app.ProgCnx.escape_string(
                    model.get_value(row, self._risk_col_order[26]))
            elif _conf.BACKEND == 'sqlite3':
                _equation1_ = model.get_value(row, self._risk_col_order[22])
                _equation2_ = model.get_value(row, self._risk_col_order[23])
                _equation3_ = model.get_value(row, self._risk_col_order[24])
                _equation4_ = model.get_value(row, self._risk_col_order[25])
                _equation5_ = model.get_value(row, self._risk_col_order[26])

            _values_ = (model.get_value(row, self._risk_col_order[3]), \
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
                        _equation1_, \
                        _equation2_, \
                        _equation3_, \
                        _equation4_, \
                        _equation5_, \
                        model.get_value(row, self._risk_col_order[27]),
                        model.get_value(row, self._risk_col_order[28]),
                        model.get_value(row, self._risk_col_order[29]),
                        model.get_value(row, self._risk_col_order[30]),
                        model.get_value(row, self._risk_col_order[31]),
                        model.get_value(row, self._risk_col_order[32]),
                        model.get_value(row, self._risk_col_order[33]),
                        model.get_value(row, self._risk_col_order[34]),
                        model.get_value(row, self._risk_col_order[35]),
                        model.get_value(row, self._risk_col_order[36]),
                        model.get_value(row, self._risk_col_order[37]),
                        model.get_value(row, self._risk_col_order[38]),
                        model.get_value(row, self._risk_col_order[39]),
                        model.get_value(row, self._risk_col_order[40]),
                        self.revision_id,
                        model.get_value(row, self._risk_col_order[0]))

            _query_ = "UPDATE tbl_risk_analysis \
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
                       AND fld_risk_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if not _results_:
                self._app.debug_log.error("assembly.py: Failed to save "
                                          "assembly to risk analysis table.")
                return True

        def _risk_map_save_line(model, __path, row, self):
            """
            Saves each row in the HARDWARE clas risk map to the open RTK
            Program database.

            Keyword Arguments:
            model  -- the HARDWARE class risk matrix gtk.TreeModel().
            __path -- the path of the selected row in the HARDWARE class risk
                      matrix gtk.TreeModel().
            row    -- the selected row in the HARDWARE class risk matrix
                      gtk.TreeView().
            """

            _crit_ = model.get_value(row, 1)

            for j in (2, 5, 8, 11, 14):
                _count_ = model.get_value(row, j)
                _prob_ = model.get_value(row, j + 1)
                _values_ = (_count_, self.revision_id, self.assembly_id,
                            _crit_, _prob_)
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

                # The combination of revision, assembly, severity, and
                # probability doesn't already exist so add it.
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

        # First save the risk analysis worksheet to tbl_risk_analysis.
        _model_ = self.tvwRisk.get_model()
        _model_.foreach(_save_line, self)

        # Then save the risk matrix.
        _model_ = self.tvwRiskMap.get_model()
        _model_.foreach(_risk_map_save_line, self)

        return False

    def _save_sia(self):
        """
        Saves the Assembly Object similar item analysis gtk.TreeView
        information to the Program's MySQL or SQLite3 database.
        """

        def _save_line(model, __path, row, self):
            """
            Saves a single row in the HARDWARE class similar item analysis
            gtk.TreeModel() to the open RTK Program database.

            Keyword Arguments:
            model  -- the HARDWARE class similar item analysis gtk.TreeModel().
            __path -- the path of the selected row in the HARDWARE class
                      similar item analysis gtk.TreeModel().
            row    -- the selected row in the HARDWARE class similar item
                      analysis gtk.TreeView().
            """

            if _conf.BACKEND == 'mysql':
                _equation1_ = self._app.ProgCnx.escape_string(
                    model.get_value(row, self._sia_col_order[19]))
                _equation2_ = self._app.ProgCnx.escape_string(
                    model.get_value(row, self._sia_col_order[20]))
                _equation3_ = self._app.ProgCnx.escape_string(
                    model.get_value(row, self._sia_col_order[21]))
                _equation4_ = self._app.ProgCnx.escape_string(
                    model.get_value(row, self._sia_col_order[22]))
                _equation5_ = self._app.ProgCnx.escape_string(
                    model.get_value(row, self._sia_col_order[23]))

            elif _conf.BACKEND == 'sqlite3':
                _equation1_ = model.get_value(row, self._sia_col_order[19])
                _equation2_ = model.get_value(row, self._sia_col_order[20])
                _equation3_ = model.get_value(row, self._sia_col_order[21])
                _equation4_ = model.get_value(row, self._sia_col_order[22])
                _equation5_ = model.get_value(row, self._sia_col_order[23])

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
                        _equation1_, \
                        _equation2_, \
                        _equation3_, \
                        _equation4_, \
                        _equation5_, \
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
                self._app.debug_log.error(
                    "assembly.py: Failed to save assembly to similar item table.")
                return True

            return False

        _model_ = self.tvwSIA.get_model()
        _model_.foreach(_save_line, self)

        return False

    def _save_fmeca(self):
        """
        Saves the HARDWARE class FMEA/FMECA information to the open RTK
        Program database.
        """

        def _save_line(model, __path, row, self):
            """
            Saves a single row in the HARDWARE class FMEA/FMECA gtk.TreeModel
            to the open RTK Program database.

            Keyword Arguments:
            model  -- the Assembly Object similar item analysis gtk.TreeModel.
            __path -- the path of the active row in the Assembly Object
                      similar item analysis gtk.TreeModel.
            row    -- the selected row in the Assembly Object similar item
                      analysis gtk.TreeView.
            """

            # Find the type of information in the row.
            #   0 = failure mode
            #   1 = failure mechanism
            #   2 = design control
            #   3 = action
            _type_ = model.get_value(row, len(self._FMECA_col_order))

            if _type_ == 0:  # Failure mode.
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
                            float(model.get_value(row,
                                                  self._FMECA_col_order[14])), \
                            float(model.get_value(row,
                                                  self._FMECA_col_order[15])), \
                            float(model.get_value(row,
                                                  self._FMECA_col_order[16])), \
                            float(model.get_value(row,
                                                  self._FMECA_col_order[17])), \
                            float(model.get_value(row,
                                                  self._FMECA_col_order[18])), \
                            model.get_value(row, self._FMECA_col_order[20]), \
                            model.get_value(row, self._FMECA_col_order[21]),
                            int(model.get_value(row,
                                                self._FMECA_col_order[22])), \
                            int(model.get_value(row,
                                                self._FMECA_col_order[23])), \
                            model.get_value(row, self._FMECA_col_order[24]), \
                            int(model.get_value(row,
                                                self._FMECA_col_order[0])))

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

            elif _type_ == 1:  # Failure mechanism.
                _parent_ = model.get_string_from_iter(model.iter_parent(row))
                _values_ = (model.get_value(row, 1), \
                            self._mechanisms[model.get_value(row, 0)][1],
                            self._mechanisms[model.get_value(row, 0)][2],
                            self._mechanisms[model.get_value(row, 0)][3],
                            self._mechanisms[model.get_value(row, 0)][4],
                            self._mechanisms[model.get_value(row, 0)][5],
                            self._mechanisms[model.get_value(row, 0)][6],
                            _parent_, model.get_value(row, 0))

                _query_ = "UPDATE tbl_fmeca_mechanisms \
                           SET fld_mechanism_description='%s', \
                               fld_rpn_occurrence=%d, fld_rpn_detection=%d, \
                               fld_rpn=%d, fld_rpn_occurrence_new=%d, \
                               fld_rpn_detection_new=%d, fld_rpn_new=%d, \
                               fld_parent='%s' \
                           WHERE fld_mechanism_id=%d" % _values_

            elif _type_ == 2:  # Control.
                _parent_ = model.get_string_from_iter(model.iter_parent(row))
                _values_ = (model.get_value(row, 1), \
                            self._fmeca_controls[model.get_value(row, 0)][1], \
                            _parent_, model.get_value(row, 0))

                _query_ = "UPDATE tbl_fmeca_controls \
                           SET fld_control_description='%s', \
                               fld_control_type=%d, fld_parent='%s' \
                           WHERE fld_control_id=%d" % _values_

            elif _type_ == 3:  # Action.
                _parent = model.get_string_from_iter(model.iter_parent(row))
                _query = "UPDATE tbl_fmeca_actions \
                          SET fld_action_recommended='{0:s}', \
                              fld_action_category='{1:s}', \
                              fld_action_owner='{2:s}', \
                              fld_action_due_date={3:d}, \
                              fld_action_status='{4:s}', \
                              fld_action_taken='{5:s}', \
                              fld_action_approved='{6:s}', \
                              fld_action_approve_date={7:d}, \
                              fld_action_closed='{8:s}', \
                              fld_action_close_date={9:d}, \
                              fld_parent='{10:s}' \
                          WHERE fld_action_id={11:d}".format(
                    model.get_value(row, 1), \
                    self._fmeca_actions[model.get_value(row, 0)][1],
                    self._fmeca_actions[model.get_value(row, 0)][2],
                    self._fmeca_actions[model.get_value(row, 0)][3],
                    self._fmeca_actions[model.get_value(row, 0)][4],
                    self._fmeca_actions[model.get_value(row, 0)][5],
                    self._fmeca_actions[model.get_value(row, 0)][6],
                    self._fmeca_actions[model.get_value(row, 0)][7],
                    self._fmeca_actions[model.get_value(row, 0)][8],
                    self._fmeca_actions[model.get_value(row, 0)][9],
                    _parent, model.get_value(row, 0))

            self._app.DB.execute_query(_query,
                                       None,
                                       self._app.ProgCnx,
                                       commit=True)

            return False

        _model_ = self.tvwFMECA.get_model()
        _model_.foreach(_save_line, self)

        return False

    def _edit_function(self, index):
        """
        Method to edit the Hazard Analysis or the Similar Item Analysis
        functions.

        :param integer index: the index indicating whether to edit a Hazard
                              Analysis or a Similar Item Analysis function.
                              0 = hazard analysis
                              1 = similar item analysis
        :returns: False or True
        :rtype: boolean
        """

        if index == 0:
            (_model_, _row_) = self.tvwRisk.get_selection().get_selected()
            _title_ = _(u"RTK - Edit Hazard Analysis Functions")
            _label_ = _widg.make_label(_(u"You can define up to five "
                                         u"functions.  You can use the system "
                                         u"failure rate, selected assembly "
                                         u"failure rate, the user float, the "
                                         u"user integer values, and results "
                                         u"of other functions.\n\n \
            System hazard rate is hr_sys\n \
            Assembly hazard rate is hr\n \
            User float is uf[1-3]\n \
            User integer is ui[1-3]\n \
            Function result is res[1-5]"), width=600, height=-1, wrap=True)
            _label2_ = _widg.make_label(_(u"For example, hr*uf1+ui2, "
                                          u"multiplies the assembly failure "
                                          u"rate and the user float value "
                                          u"then adds the product to the "
                                          u"second user integer value."),
                                        width=600,
                                        height=-1, wrap=True)
        elif index == 1:
            (_model_, _row_) = self.tvwSIA.get_selection().get_selected()
            _title_ = _(u"RTK - Edit Similar Item Analysis Functions")
            _label_ = _widg.make_label(_(u"You can define up to five "
                                         u"functions.  You can use the system "
                                         u"failure rate, selected assembly "
                                         u"failure rate, the change factor, "
                                         u"the user float, the user integer "
                                         u"values, and results of other "
                                         u"functions.\n\n \
            System hazard rate is hr_sys\n \
            Assembly hazard rate is hr\n \
            Change factor is pi[1-8]\n \
            User float is uf[1-3]\n \
            User integer is ui[1-3]\n \
            Function result is res[1-5]"), width=600, height=-1, wrap=True)
            _label2_ = _widg.make_label(_(u"For example, pi1*pi2+pi3, "
                                          u"multiplies the first two change "
                                          u"factors and adds the value to the "
                                          u"third change factor."),
                                        width=600, height=-1, wrap=True)

        _dialog_ = _widg.make_dialog(_title_, self._app.winWorkBook)

        _fixed_ = gtk.Fixed()

        _y_pos_ = 10
        _fixed_.put(_label_, 5, _y_pos_)
        _y_pos_ += _label_.size_request()[1] + 10
        _fixed_.put(_label2_, 5, _y_pos_)
        _y_pos_ += _label2_.size_request()[1] + 10

        _label_ = _widg.make_label(_(u"User function 1:"))
        _txtFunction1_ = _widg.make_entry()
        if index == 0:
            _txtFunction1_.set_text(_model_.get_value(_row_, 22))
        elif index == 1:
            _txtFunction1_.set_text(_model_.get_value(_row_, 19))

        _fixed_.put(_label_, 5, _y_pos_)
        _fixed_.put(_txtFunction1_, 195, _y_pos_)
        _y_pos_ += 30

        _label_ = _widg.make_label(_(u"User function 2:"))
        _txtFunction2_ = _widg.make_entry()
        if index == 0:
            _txtFunction2_.set_text(_model_.get_value(_row_, 23))
        elif index == 1:
            _txtFunction2_.set_text(_model_.get_value(_row_, 20))
        _fixed_.put(_label_, 5, _y_pos_)
        _fixed_.put(_txtFunction2_, 195, _y_pos_)
        _y_pos_ += 30

        _label_ = _widg.make_label(_(u"User function 3:"))
        _txtFunction3_ = _widg.make_entry()
        if index == 0:
            _txtFunction3_.set_text(_model_.get_value(_row_, 24))
        elif index == 1:
            _txtFunction3_.set_text(_model_.get_value(_row_, 21))
        _fixed_.put(_label_, 5, _y_pos_)
        _fixed_.put(_txtFunction3_, 195, _y_pos_)
        _y_pos_ += 30

        _label_ = _widg.make_label(_(u"User function 4:"))
        _txtFunction4_ = _widg.make_entry()
        if index == 0:
            _txtFunction4_.set_text(_model_.get_value(_row_, 25))
        elif index == 1:
            _txtFunction4_.set_text(_model_.get_value(_row_, 22))
        _fixed_.put(_label_, 5, _y_pos_)
        _fixed_.put(_txtFunction4_, 195, _y_pos_)
        _y_pos_ += 30

        _label_ = _widg.make_label(_(u"User function 5:"))
        _txtFunction5_ = _widg.make_entry()
        if index == 0:
            _txtFunction5_.set_text(_model_.get_value(_row_, 26))
        elif index == 1:
            _txtFunction5_.set_text(_model_.get_value(_row_, 23))
        _fixed_.put(_label_, 5, _y_pos_)
        _fixed_.put(_txtFunction5_, 195, _y_pos_)
        _y_pos_ += 30

        _chkApplyAll_ = gtk.CheckButton(label=_(u"Apply to all assemblies."))
        _fixed_.put(_chkApplyAll_, 5, _y_pos_)

        _fixed_.show_all()

        _dialog_.vbox.pack_start(_fixed_)  #pylint: disable=E1101

        if _dialog_.run() == gtk.RESPONSE_ACCEPT:
            if index == 0:
                _cols_ = [35, 36, 37, 38, 39]
            elif index == 1:
                _cols_ = [19, 20, 21, 22, 23]

            if _chkApplyAll_.get_active():
                while _row_ is not None:
                    _model_.set_value(_row_, _cols_[0],
                                      _txtFunction1_.get_text())
                    _model_.set_value(_row_, _cols_[1],
                                      _txtFunction2_.get_text())
                    _model_.set_value(_row_, _cols_[2],
                                      _txtFunction3_.get_text())
                    _model_.set_value(_row_, _cols_[3],
                                      _txtFunction4_.get_text())
                    _model_.set_value(_row_, _cols_[4],
                                      _txtFunction5_.get_text())
                    _row_ = _model_.iter_next(_row_)
            else:
                _model_.set_value(_row_, _cols_[0], _txtFunction1_.get_text())
                _model_.set_value(_row_, _cols_[1], _txtFunction2_.get_text())
                _model_.set_value(_row_, _cols_[2], _txtFunction3_.get_text())
                _model_.set_value(_row_, _cols_[3], _txtFunction4_.get_text())
                _model_.set_value(_row_, _cols_[4], _txtFunction5_.get_text())

        _dialog_.destroy()

        return False

    def _callback_check(self, check, index):
        """
        Callback function to retrieve and save checkbutton changes.

        Keyword Arguments:
        check -- the checkbutton that called the function.
        index -- the position in the Assembly Object _attribute list
                 associated with the data from the calling checkbutton.
        """

        if index > 87:
            # Determine the failure consequences.
            if self.chkFCQ1.get_active() and not self.chkFCQ2.get_active():
                self.optEO.set_active(True)
            elif not self.chkFCQ1.get_active() and \
                    not self.chkFCQ3.get_active():
                self.optNSH.set_active(True)
            elif self.chkFCQ1.get_active() and self.chkFCQ2.get_active():
                self.optES.set_active(True)
            else:
                self.optHS.set_active(True)

            # Make the correct question available depending on the answer to
            # question 1.
            if self.chkFCQ1.get_active():
                self.chkFCQ2.set_sensitive(True)
                self.chkFCQ3.set_sensitive(False)
            else:
                self.chkFCQ2.set_sensitive(False)
                self.chkFCQ3.set_sensitive(True)

        else:
            (_model_, _row_) = self.treeview.get_selection().get_selected()

            # Update the Hardware Tree.
            _model_.set_value(_row_, index, check.get_active())

            self._update_attributes()

        return False

    def _callback_combo(self, combo, index):
        """
        Callback function to retrieve and save combobox changes.

        Keyword Arguments:
        combo -- the gtk.Combo that called the function.
        index -- the position in the applicable treeview associated with the
                 data from the calling gtk.Combo.
        """

        i = combo.get_active()

        if index < 200:  # Hardware information.
            # Get the Hardware Tree model/selected row and update the
            # Hardware TreeView.
            (_model_, _row_) = self.treeview.get_selection().get_selected()
            _model_.set_value(_row_, index, int(combo.get_active()))

            if index == 10:  # Calculation model
                self._trickledown(_model_, _row_, index,
                                  int(combo.get_active()))
                if int(combo.get_active()) > 2:
                    _title_ = _(u"RTK Information")

                    dialog = _widg.make_dialog(_title_,
                                               _flags_=(
                                                   gtk.DIALOG_MODAL |
                                                   gtk.DIALOG_DESTROY_WITH_PARENT),
                                               _buttons_=(gtk.STOCK_OK,
                                                          gtk.RESPONSE_ACCEPT))

                    _text_ = _(u"%s model not yet implemented.  Contact "
                               u"andrew.rowland@reliaqual.com if you would "
                               u"like to help." % combo.get_active_text())
                    label = _widg.make_label(_text_,
                                             width=250, height=75)
                    dialog.vbox.pack_start(label)  #pylint: disable=E1101
                    label.show()

                    dialog.run()
                    dialog.destroy()

            elif index == 22:  # Active Environment
                self._trickledown(_model_, _row_, index,
                                  int(combo.get_active()))

            elif index == 23:  # Dormant environment
                self._trickledown(_model_, _row_, index,
                                  int(combo.get_active()))

            elif index == 35:  # Hazard rate type
                self.failure_rate_type = i
                # If selected type is hazard rate specified or MTBF specified,
                # set active and predicted values equal to specified values.
                if self.failure_rate_type == 2:  # Specified hazard rate.
                    self.failure_rate_specified = _model_.get_value(_row_, 34)
                    try:
                        self.mtbf_specified = 1.0 / self.failure_rate_specified
                    except ZeroDivisionError:
                        self.mtbf_specified = 0.0
                    _model_.set_value(_row_, 28, self.failure_rate_specified)
                    _model_.set_value(_row_, 32, self.failure_rate_specified)
                    _model_.set_value(_row_, 50, self.mtbf_specified)
                    _model_.set_value(_row_, 51, self.mtbf_specified)
                elif self.failure_rate_type == 3:  # Specified MTBF.
                    self.mtbf_specified = _model_.get_value(_row_, 51)
                    try:
                        self.failure_rate_specified = 1.0 / self.mtbf_specified
                    except ZeroDivisionError:
                        self.failure_rate_specified = 0.0
                    _model_.set_value(_row_, 28, self.failure_rate_specified)
                    _model_.set_value(_row_, 32, self.failure_rate_specified)
                    _model_.set_value(_row_, 34, self.failure_rate_specified)
                    _model_.set_value(_row_, 50, self.mtbf_specified)

            elif index == 43:  # Manufacturer
                _cmbmodel_ = combo.get_model()
                _cmbrow_ = combo.get_active_iter()
                try:
                    self.txtCAGECode.set_text(
                        str(_cmbmodel_.get_value(_cmbrow_, 2)))
                    _model_.set_value(_row_, 9,
                                      str(_cmbmodel_.get_value(_cmbrow_, 2)))
                except TypeError:  # No row is selected
                    pass

            if self.part:  # Update the parts list.
                #self.model.set_value(self.selected_row,
                #                     _index_,
                #                     int(combo.get_active()))
                print "TODO: Write code to update parts list."

            self._update_attributes()

        elif index >= 200 and index < 500:  # Component specific information.
            index -= 200

        # Reliability requirement measure combo box called this function.
        elif index == 500:
            i = int(combo.get_active())
            if i == 0:  # Nothing selected.
                self.txtReliabilityGoal.props.editable = 0
                self.txtReliabilityGoal.set_sensitive(0)
                self.txtMTBFGoal.props.editable = 0
                self.txtMTBFGoal.set_sensitive(0)
                self.txtFailureRateGoal.props.editable = 0
                self.txtFailureRateGoal.set_sensitive(0)
            elif i == 1:  # Expressed as reliability.
                self.txtReliabilityGoal.props.editable = 1
                self.txtReliabilityGoal.set_sensitive(1)
                self.txtMTBFGoal.props.editable = 0
                self.txtMTBFGoal.set_sensitive(0)
                self.txtFailureRateGoal.props.editable = 0
                self.txtFailureRateGoal.set_sensitive(0)
            elif i == 2:  # Expressed as an MTBF.
                self.txtReliabilityGoal.props.editable = 0
                self.txtReliabilityGoal.set_sensitive(0)
                self.txtMTBFGoal.props.editable = 1
                self.txtMTBFGoal.set_sensitive(1)
                self.txtFailureRateGoal.props.editable = 0
                self.txtFailureRateGoal.set_sensitive(0)
            elif i == 3:  # Expressed as a failure rate.
                self.txtReliabilityGoal.props.editable = 0
                self.txtReliabilityGoal.set_sensitive(0)
                self.txtMTBFGoal.props.editable = 0
                self.txtMTBFGoal.set_sensitive(0)
                self.txtFailureRateGoal.props.editable = 1
                self.txtFailureRateGoal.set_sensitive(1)

        # Reliability allocation method combo box called this function.
        # Hide/show the appropriate columns in the Allocation gtk.TreeView().
        elif index == 501:
            i = int(combo.get_active())
            _heading_ = _(u"Weighting Factor")
            if i == 1:  # Equal apportionment selected.
                for col in 0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 13, 19, 20, 21:
                    self.tvwAllocation.get_column(col).set_visible(0)
                for col in 2, 12, 14, 15, 16, 17, 18, 19:
                    self.tvwAllocation.get_column(col).set_visible(1)
                    column = self.tvwAllocation.get_column(col)
                    cells = column.get_cell_renderers()
                    for i in range(len(cells)):
                        cells[i].set_property('background', 'light gray')
                        cells[i].set_property('editable', 0)

            elif i == 2:  # AGREE apportionment selected.
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

                _heading_ = _(u"Importance Measure")

            elif i == 3:  # ARINC apportionment selected.
                for col in 0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 13, 20, 21:
                    self.tvwAllocation.get_column(col).set_visible(0)
                for col in 2, 12, 14, 15, 16, 17, 18, 19:
                    self.tvwAllocation.get_column(col).set_visible(1)
                    column = self.tvwAllocation.get_column(col)
                    cells = column.get_cell_renderers()
                    for i in range(len(cells)):
                        cells[i].set_property('background', 'light gray')
                        cells[i].set_property('editable', 0)

            elif i == 4:  # Feasibility of Objectives selected.
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

            elif i == 5:  # Repairable System apportionment selected.
                for col in 0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, \
                           17, 18, 19:
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

        elif index == 511:  # Component category
            self.category_id = combo.get_active()

            # Get the model and iter from the parts category gtk.ComboBox()
            # then read the value of the category ID.
            _model = combo.get_model()
            _row = combo.get_active_iter()

            # Retrieve part subcategory values.
            _query = "SELECT fld_subcategory_id, fld_subcategory_noun \
                      FROM tbl_subcategory \
                      WHERE fld_category_id=%d \
                      ORDER BY fld_subcategory_noun ASC".format(
                (_model.get_value(_row, 1)))
            _results = self._app.COMDB.execute_query(_query, None,
                                                     self._app.ComCnx)

            try:
                _n_subcategories = len(_results)
            except TypeError:
                _n_subcategories = 0

            _model = self.cmbSubcategory.get_model()
            _model.clear()
            _model.append(None, ['', '', ''])
            for i in range(_n_subcategories):
                _model.append(None, [_results[i][1], _results[i][0], ''])

                # self._load_part_subcategory_combo(combo)

        elif index == 578:  # Component subcategory
            if combo.get_active() > 0:
                self.subcategory_id = combo.get_active()
                # self.part = _util.set_part_model(self.category,
                #                                 self.subcategory)
                # if(self.part is not None):
                #     hbox = self.notebook.get_nth_page(1)
                #     fixed = hbox.get_children()[0].get_children()[0].get_children()[0].get_children()
                #     self.part.assessment_inputs_create(self,
                #                                        fixed,
                #                                        205,
                #                                        self.y_pos[0][0])
                #     hbox = self.notebook.get_nth_page(2)
                #     fixed = hbox.get_children()[0].get_children()[0].get_children()[0].get_children()
                #     self.part.assessment_inputs_load(self)
                #     self.part.assessment_results_create(self,
                #                                         fixed,
                #                                         205,
                #                                         self.y_pos[1][0])
                #     self.part.assessment_results_load(self)

        elif index >= 1000:
            selection = self.tvwFMECA.get_selection()
            (model, row) = selection.get_selected()
            _id_ = model.get_value(row, 0)
            _type_ = model.get_value(row, len(self._FMECA_col_order))

            _index_ = index - 1000

            if _type_ == 1:  # Failure mechanism
                self._mechanisms[_id_][_index_] = i
            elif _type_ == 2:  # Control
                self._fmeca_controls[_id_][_index_] = i
            elif _type_ == 3:  # Action
                self._fmeca_actions[_id_][_index_] = i

        return False

    def _callback_entry(self, entry, __event, convert, index):
        """
        Callback function to retrieve and save entry changes.

        :param entry: the gtk.Entry() that called the function.
        :type entry: gtk.Entry
        :param __event: the gtk.gdk.Event() that called the function.
        :type __event: gtk.gdk.Event
        :param string convert: the data type to convert the entry contents to.
        :param integer index: the position in the applicable treeview
                              associated with the data from the calling
                              gtk.Entry().
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        if convert == 'text':
            if index == 71:
                _textbuffer = self.txtRemarks.get_child().get_child().get_buffer()
                _text_ = _textbuffer.get_text(*_textbuffer.get_bounds())
            else:
                _text_ = entry.get_text()

        elif convert == 'int':
            _text_ = int(entry.get_text())

        elif convert == 'float':
            _text_ = float(entry.get_text().replace('$', ''))

        elif convert == 'date':
            _text_ = datetime.strptime(entry.get_text(),
                                       '%Y-%m-%d').toordinal()

        if index < 200:  # Hardware information.
            # Get the Hardware Tree model and selected row.
            (_model_, _row_) = self.treeview.get_selection().get_selected()

            # Update the Hardware Tree.
            _model_.set_value(_row_, index, _text_)

            if index == 20 or index == 37 or index == 45 or \
                    index == 81 or index == 84:
                # Trickle down values to children assemblies and components if
                # change is made to duty cycle, humidity, mission time, dormant
                # temperature, or vibration
                self._trickledown(_model_, _row_, index, _text_)

            elif index == 34:  # Specified hazard rate
                # Set predicted failure rate to specified value if the
                # hazard rate type is selected as allocated or hazard rate
                # specified.
                self.failure_rate_specified = _text_
                if self.failure_rate_type == 2:
                    try:
                        self.mtbf_specified = 1.0 / _text_
                    except ZeroDivisionError:
                        self.mtbf_specified = 0.0

                    _model_.set_value(_row_, 51, self.mtbf_specified)

            elif index == 51:  # Specified MTBF
                # Set predicted MTBF to specified value if the hazard rate type
                # is selected as allocated or MTBFspecified.
                self.mtbf_specified = _text_
                if self.failure_rate_type == 3:
                    try:
                        self.failure_rate_specified = 1.0 / _text_
                    except ZeroDivisionError:
                        self.failure_rate_specified = 0.0

                    _model_.set_value(_row_, 28, self.failure_rate_specified)

            elif index == 80:  # Active Temperature
                # Number of children.
                _n_children_ = _model_.iter_n_children(_row_)

                # Update the ambient temperature for each of the child
                # components.
                for i in range(_n_children_):
                    chrow = _model_.iter_nth_child(_row_, i)
                    _model_.set_value(chrow, index, _text_)

                    # Now update the Parts List treeview.
                    # partmodel = self._app.COMPONENT.model
                    # partrow = self._app.COMPONENT.selected_row
                    # partmodel.set_value(partrow, 103, _text_)

            if self.part:  # Update the Parts List.
                # TODO: Need code to update the parts list.
                # self.model.set_value(self.selected_row, _index_, _text_)
                print "TODO: Write code to update parts list."

            self._update_attributes()

        elif index >= 200 and index < 500:  # Component specific information.
            index -= 200

        elif index >= 500 and index < 1000:  # Allocation goals.
            if index == 500:
                (MTBFg, FRg) = self._calculate_goals(500)

                self.txtMTBFGoal.set_text(str(fmt.format(MTBFg)))
                self.txtFailureRateGoal.set_text(str(fmt.format(FRg)))

            elif index == 501:
                (Rg, FRg) = self._calculate_goals(501)

                self.txtReliabilityGoal.set_text(str(fmt.format(Rg)))
                self.txtFailureRateGoal.set_text(str(fmt.format(FRg)))

            elif index == 502:
                (Rg, MTBFg) = self._calculate_goals(502)

                self.txtReliabilityGoal.set_text(str(fmt.format(Rg)))
                self.txtMTBFGoal.set_text(str(fmt.format(MTBFg)))

        elif index >= 1000:  # FMECA information.
            selection = self.tvwFMECA.get_selection()
            (model, row) = selection.get_selected()
            _id = model.get_value(row, 0)
            _type = model.get_value(row, len(self._FMECA_col_order))

            _index = index - 1000

            if _type == 1:  # Failure mechanism
                self._mechanisms[_id][_index] = _text_
            elif _type == 2:  # Control
                self._fmeca_controls[_id][_index] = _text_
            elif _type == 3:  # Action
                if _index == 0:
                    _textbuffer = self.txtActionRecommended.get_child().get_child().get_buffer()
                    _text = _textbuffer.get_text(*_textbuffer.get_bounds())
                elif _index == 5:
                    _textbuffer = self.txtActionTaken.get_child().get_child().get_buffer()
                    _text = _textbuffer.get_text(*_textbuffer.get_bounds())

                self._fmeca_actions[_id][_index] = _text

        return False

    def _trickledown(self, model, row, index, value):
        """
        Updates child assemblies and components when certain information is
        changed in the parent assembly.

        Keyword Arguments:
        model -- the HARDWARE class gtk.TreeModel().
        row   -- the selected row in the HARDWARE class gtk.TreeModel().
        index -- the position (column) in the HARDWARE class gtk.TreeModel()
                 associated with the data to be trickled down.
        value -- the value to update the children with.
        """

        _n_children_ = model.iter_n_children(row)

        for i in range(_n_children_):
            _chrow_ = model.iter_nth_child(row, i)
            if model.iter_has_child(_chrow_):
                self._trickledown(model, _chrow_, index, value)
            model.set_value(_chrow_, index, value)
            if model.get_value(_chrow_, 63) == 1:
                self.category_id = model.get_value(_chrow_, 11)
                self.subcategory_id = model.get_value(_chrow_, 78)

        return False

    def _rollup_sia(self):
        """
        Method to 'roll-up' the lower level Similar Item Analysis change
        descriptions to the selected parent Assembly.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        _values_ = _model_.get_string_from_iter(_row_)

        # Select all of the lower level element change descriptions for the
        # selected parent assembly.
        _query_ = "SELECT t2.fld_name, t1.fld_change_desc_1, \
                          t1.fld_change_desc_2, t1.fld_change_desc_3, \
                          t1.fld_change_desc_4, t1.fld_change_desc_5, \
                          t1.fld_change_desc_6, t1.fld_change_desc_7, \
                          t1.fld_change_desc_8 \
                   FROM tbl_similar_item AS t1 \
                   INNER JOIN tbl_system AS t2 \
                   ON t1.fld_assembly_id=t2.fld_assembly_id \
                   WHERE t2.fld_parent_assembly='%s'" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        # Combine the changes descriptions into a single change description for
        # each change category.
        _summary_ = ["", "", "", "", "", "", "", ""]
        for i in range(len(_results_)):
            _system_ = _results_[i][0]
            for j in range(8):
                if _results_[i][j + 1] != '' and \
                        _results_[i][j + 1] is not None:
                    _summary_[j] = _summary_[j] + _system_ + ":\n" + \
                        _results_[i][j + 1] + "\n"

        # Update the selected parent assembly's change descriptions with the
        # combined change description.
        _query = "UPDATE tbl_similar_item \
                  SET fld_change_desc_1='{0:s}', \
                      fld_change_desc_2='{1:s}', \
                      fld_change_desc_3='{2:s}', \
                      fld_change_desc_4='{3:s}', \
                      fld_change_desc_5='{4:s}', \
                      fld_change_desc_6='{5:s}', \
                      fld_change_desc_7='{6:s}', \
                      fld_change_desc_8='{7:s}' \
                  WHERE fld_revision_id={8:d} \
                  AND fld_assembly_id={9:d}".format(
            _summary_[0], _summary_[1], _summary_[2], _summary_[3],
            _summary_[4], _summary_[5], _summary_[6], _summary_[7],
            self.revision_id, self.assembly_id)
        self._app.DB.execute_query(_query,
                                   None,
                                   self._app.ProgCnx,
                                   commit=True)

        return False

    def _trickle_down_risk(self):
        """
        Method to 'trickle down' the higher level Hazard Analysis potential
        hazards to an assemblies immediate children.
        """

        # Retrieve the currently selected assembly potential hazards to
        # trickle down.
        _hazards = []
        _model = self.tvwRisk.get_model()
        _row = _model.get_iter_root()
        while _row is not None:
            _hazards.append(_model.get_value(_row, 3))
            _row = _model.iter_next(_row)

        _n_hazards = len(_hazards)

        # If the selected item has children, trickle down the hazard to all of
        # it's immediate children.
        (_model, _row) = self.treeview.get_selection().get_selected()
        if _model.iter_has_child(_row):
            i = 0
            _child = _model.iter_nth_child(_row, i)
            while _child is not None:
                for j in range(_n_hazards):
                    _query = "INSERT INTO tbl_risk_analysis " \
                             "(fld_revision_id, fld_assembly_id, " \
                             "fld_potential_hazard) " \
                            "VALUES (%d, %d, '%s')" % \
                    (self._app.REVISION.revision_id,
                     _model.get_value(_child, 1), _hazards[j])
                    self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                               commit=True)

                i += 1
                _child = _model.iter_nth_child(_row, i)

        return False

    def _notebook_page_switched(self, __notebook, __page, page_num):
        """
        Called whenever the Work Book notebook page is changed.

        Keyword Arguments:
        __notebook -- the Tree Book notebook widget.
        __page     -- the newly selected page widget.
        page_num   -- the newly selected page number.
                      0 = General Data
                      1 = Allocation
                      2 = Hazard Analysis
                      3 = Similar Items Analysis
                      4 = Assessment Inputs
                      5 = Assessment Results
                      6 = FMEA
                      7 = Maintenance Planning
        """

        if page_num == 0:  # General data tab.
            self.btnAddItem.show()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.hide()
            self.btnEdit.hide()
            self.btnAddItem.set_tooltip_text(_(u"Add components to the "
                                               u"currently selected "
                                               u"assembly."))
        elif page_num == 1:  # Allocation tab
            self.btnAddItem.hide()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.hide()
            self.btnEdit.hide()
            self.btnAddItem.set_tooltip_text(_(u"Add components to the "
                                               u"currently selected "
                                               u"assembly."))
            self.btnAnalyze.set_tooltip_text(_(u"Allocates the reliability to "
                                               u"the child assemblies/parts."))
            self.btnSaveResults.set_tooltip_text(_(u"Saves the allocation "
                                                   u"results for the selected "
                                                   u"assembly."))
        elif page_num == 2:  # Hazard analysis tab
            self.btnAddItem.show()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.show()
            self.btnEdit.show()
            self.btnAddItem.set_tooltip_text(_(u"Adds a hazard to the "
                                               u"selected assembly."))
            self.btnAnalyze.set_tooltip_text(_(u"Performs a risk analysis of "
                                               u"changes to the selected "
                                               u"assembly."))
            self.btnSaveResults.set_tooltip_text(_(u"Saves the risk analysis "
                                                   u"results for the selected "
                                                   u"assembly."))
            self.btnRollup.set_tooltip_text(_(u"Summarizes the lower level "
                                              u"risk analyses."))
            self.btnEdit.set_tooltip_text(_(u"Create/edit current risk "
                                            u"analysis functions."))
        elif page_num == 3:  # Similar items tab
            self.btnAddItem.hide()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.show()
            self.btnEdit.show()
            self.btnAnalyze.set_tooltip_text(_(u"Performs the similar item "
                                               u"analysis."))
            self.btnSaveResults.set_tooltip_text(_(u"Saves the similar item "
                                                   u"analysis results for the "
                                                   u"selected assembly."))
            self.btnRollup.set_tooltip_text(_(u"Summarizes the lower level "
                                              u"similar item analyses."))
            self.btnEdit.set_tooltip_text(_(u"Create/edit current similar "
                                            u"item analysis functions."))
        elif page_num == 4:  # Assessment inputs tab
            self.btnAddItem.show()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.hide()
            self.btnEdit.hide()
            self.btnAddItem.set_tooltip_text(_(u"Add components to the "
                                               u"currently selected "
                                               u"assembly."))
            self.btnAnalyze.set_tooltip_text(_(u"Calculate the hardware "
                                               u"metrics in the open RTK "
                                               u"Program Database."))
        elif page_num == 5:  # Assessment results tab
            self.btnAddItem.show()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.hide()
            self.btnSaveResults.show()
            self.btnRollup.hide()
            self.btnEdit.hide()
        elif page_num == 6:  # FMEA/FMECA tab
            self.btnAddItem.hide()
            self.btnFMECAAdd.show()
            self.btnRemoveItem.show()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.show()
            self.btnEdit.hide()
            self.btnAddItem.set_tooltip_text(_(u"Add a new failure mode."))
            self.btnRemoveItem.set_tooltip_text(_(u"Remove the currently "
                                                  u"selected failure mode."))
            self.btnAnalyze.set_tooltip_text(_(u"Calculates the mode and item "
                                               u"criticality for the selected "
                                               u"allocation method."))
            self.btnSaveResults.set_tooltip_text(_(u"Saves the FMEA/FMECA for "
                                                   u"the selected assembly."))
            self.btnRollup.set_tooltip_text(_(u"Summarizes the lower level "
                                              u"FMEA/FMECA results."))
        elif page_num == 7:  # Maintenance planning tab
            self.btnAddItem.hide()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.show()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.hide()
            self.btnEdit.hide()
            self.btnAddItem.set_tooltip_text(_(u"Add a new maintenance "
                                               u"activity."))
            self.btnRemoveItem.set_tooltip_text(_(u"Remove the currently "
                                                  u"selected maintenance "
                                                  u"activity."))
            # self.btnAnalyze.set_tooltip_text(_(u"Calculates the selected "
            #                                    u"allocation method."))
            # self.btnSaveResults.set_tooltip_text(_(u"Saves the allocation "
            #                                        u"results for the "
            #                                        u"selected assembly."))
        elif page_num == 8:  # RG planning tab
            self.btnAddItem.hide()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.show()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.hide()
            self.btnEdit.hide()
            self.btnAddItem.set_tooltip_text(_(u"Add a new reliability "
                                               u"growth plan."))
            self.btnRemoveItem.set_tooltip_text(_(u"Remove the currently "
                                                  u"selected reliability "
                                                  u"growth plan."))
            # self.btnAnalyze.set_tooltip_text(_(u"Calculates the selected "
            #                                    u"allocation method."))
            # self.btnSaveResults.set_tooltip_text(_(u"Saves the allocation "
            #                                        u"results for the "
            #                                        u"selected assembly."))
        elif page_num == 9:  # RG tracking tab
            self.btnAddItem.show()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.show()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.hide()
            self.btnEdit.hide()
            self.btnAddItem.set_tooltip_text(_(u"Add a new relibility growth "
                                               u"incident."))
            # self.btnAnalyze.set_tooltip_text(_(u"Calculates the selected "
            #                                    u"allocation method."))
            # self.btnSaveResults.set_tooltip_text(_(u"Saves the allocation "
            #                                        u"results for the "
            #                                        u"selected assembly."))
        else:
            self.btnAddItem.hide()
            self.btnFMECAAdd.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.hide()
            self.btnSaveResults.hide()
            self.btnRollup.hide()
            self.btnEdit.hide()

        self._selected_tab = page_num

        return False

    def _toolbutton_pressed(self, button):
        """
        Method to react to the HARDWARE class gtk.ToolButton() clicked events.

        Keyword Arguments:
        button -- the gtk.ToolButton() that was pressed.
        """

        _page_ = self.notebook.get_current_page()

        (__model, _row_) = self.treeview.get_selection().get_selected()

        # If the selected hardware item is an assembly, execute the
        # assembly-specific code.  Otherwise, add 3 to the page number to
        # account for the missing assembly-specific pages in the notebook.
        if not self.part:
            if _page_ == 1:  # Allocation tab.
                if button.get_name() == 'Analyze':
                    self._allocate()
                elif button.get_name() == 'Save':
                    self._save_allocation()
            elif _page_ == 2:  # Hazard analysis tab.
                if button.get_name() == 'Add':
                    _query_ = "INSERT INTO tbl_risk_analysis \
                               (fld_revision_id, fld_assembly_id) \
                               VALUES (%d, %d)" % \
                              (self._app.REVISION.revision_id,
                               self.assembly_id)
                    _results_ = self._app.DB.execute_query(_query_,
                                                           None,
                                                           self._app.ProgCnx,
                                                           commit=True)
                    self.load_notebook()
                elif button.get_name() == 'Analyze':
                    self._calculate_risk()
                elif button.get_name() == 'Save':
                    self._save_hazard_analysis()
                elif button.get_name() == 'Rollup':
                    self._trickle_down_risk()
                elif button.get_name() == 'Edit':
                    self._edit_function(index=0)
            elif _page_ == 3:  # Similar item analysis tab.
                if button.get_name() == 'Analyze':
                    self._calculate_sia()
                elif button.get_name() == 'Save':
                    self._save_sia()
                elif button.get_name() == 'Rollup':
                    self._rollup_sia()
                elif button.get_name() == 'Edit':
                    self._edit_function(index=1)
        else:
            _page_ += 3

        if _page_ == 0:  # General data tab.
            if button.get_name() == 'Add':
                self._add_hardware(button, 2)
            elif button.get_name() == 'Analyze':
                _row_ = self.treeview.get_model().get_iter_root()
                self.calculate(_row_)
            elif button.get_name() == 'Save':
                self.save_hardware()
        elif _page_ == 4:  # Assessment inputs tab.
            if button.get_name() == 'Add':
                self._add_hardware(button, 2)
            elif button.get_name() == 'Analyze':
                _row_ = self.treeview.get_model().get_iter_root()
                self.calculate(_row_)
            elif button.get_name() == 'Save':
                self.save_hardware()
        elif _page_ == 5:  # Assessment results tab.
            if button.get_name() == 'Add':
                self._add_hardware(button, 2)
            elif button.get_name() == 'Analyze':
                _row_ = self.treeview.get_model().get_iter_root()
                self.calculate(_row_)
            elif button.get_name() == 'Save':
                self.save_hardware()
        elif _page_ == 6:  # FMEA/FMECA tab.
            if button.get_label() == 'Mode':
                # Find the id of the next failure mode.
                _query_ = "SELECT seq FROM sqlite_sequence \
                           WHERE name='tbl_fmeca'"
                _last_id_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx)

                try:
                    _last_id_ = _last_id_[0][0] + 1
                except TypeError:
                    _last_id_ = 0

                # Insert the new failure mode.
                _query_ = "INSERT INTO tbl_fmeca \
                           (fld_assembly_id, fld_function_id, fld_mode_id) \
                           VALUES (%d, 0, %d)" % (self.assembly_id, _last_id_)
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           True)

                # Insert a new line in the failure consequence table.
                _query_ = "INSERT INTO tbl_failure_consequences \
                           (fld_assembly_id, fld_mode_id) \
                           VALUES (%d, %d)" % (self.assembly_id, _last_id_)
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           True)

                self._load_fmeca_tab()

            elif button.get_label() == 'Mechanism':
                # Find the id and gtk.TreeIter of the parent failure mode.
                (model, row) = self.tvwFMECA.get_selection().get_selected()
                _mode_id_ = model.get_value(row, 0)
                _parent_ = model.get_string_from_iter(row)

                if _parent_.count(':') != 0:
                    _util.application_error(_(u"A failure mechanism can only "
                                              u"be the child of a failure "
                                              u"mode, not another failure "
                                              u"mechanism, control, or "
                                              u"action."))
                    return True

                # Find the id of the next failure mechanism.
                _query_ = "SELECT seq FROM sqlite_sequence \
                           WHERE name='tbl_fmeca_mechanisms'"
                _next_id_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx)

                try:
                    _next_id_ = _next_id_[0][0] + 1
                except TypeError:
                    _next_id_ = 0

                # Insert the new failure mechanism.
                _query_ = "INSERT INTO tbl_fmeca_mechanisms \
                           (fld_assembly_id, fld_mode_id, \
                            fld_mechanism_id, fld_parent) \
                           VALUES (%d, %d, %d, '%s')" % (self.assembly_id,
                                                         _mode_id_, _next_id_,
                                                         _parent_)
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           True)

                self._load_fmeca_tab()

            elif button.get_label() == 'Control':
                # Find the id and gtk.TreeIter of the parent failure mechanism.
                (model, row) = self.tvwFMECA.get_selection().get_selected()
                _mechanism_id_ = model.get_value(row, 0)
                _parent_ = model.get_string_from_iter(row)

                if _parent_.count(':') != 1:
                    _util.application_error(_(u"A control can only be the "
                                              u"child of a failure mechanism, "
                                              u"not another control, failure "
                                              u"mode, or action."))
                    return True

                # Find the id of the grand-parent failure mode.
                row = model.iter_parent(row)
                _mode_id_ = model.get_value(row, 0)

                # Find the id of the next control.
                _query_ = "SELECT seq FROM sqlite_sequence \
                           WHERE name='tbl_fmeca_controls'"
                _next_id_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx)

                try:
                    _next_id_ = _next_id_[0][0] + 1
                except TypeError:
                    _next_id_ = 0

                # Insert the new control.
                _query_ = "INSERT INTO tbl_fmeca_controls \
                           (fld_assembly_id, fld_mode_id, \
                            fld_mechanism_id, fld_control_id, fld_parent) \
                           VALUES (%d, %d, %d, %d, '%s')" % (self.assembly_id,
                                                             _mode_id_,
                                                             _mechanism_id_,
                                                             _next_id_,
                                                             _parent_)
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           True)

                self._load_fmeca_tab()

            elif button.get_label() == 'Action':
                # Find the id and gtk.TreeIter of the parent failure mechanism.
                (model, row) = self.tvwFMECA.get_selection().get_selected()
                _mechanism_id_ = model.get_value(row, 0)
                _parent_ = model.get_string_from_iter(row)

                if _parent_.count(':') != 1:
                    _util.application_error(_(u"An action can only be the "
                                              u"child of a failure mechanism, "
                                              u"not another action, failure "
                                              u"mode, or control."))
                    return True

                # Find the id of the grand-parent failure mode.
                row = model.iter_parent(row)
                _mode_id_ = model.get_value(row, 0)

                # Find the id of the next control.
                _query_ = "SELECT seq FROM sqlite_sequence \
                           WHERE name='tbl_fmeca_actions'"
                _next_id_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx)

                try:
                    _next_id_ = _next_id_[0][0] + 1
                except TypeError:
                    _next_id_ = 0

                # Insert the new action.
                _query_ = "INSERT INTO tbl_fmeca_actions \
                           (fld_assembly_id, fld_mode_id, \
                            fld_mechanism_id, fld_action_id, fld_parent) \
                           VALUES (%d, %d, %d, %d, '%s')" % (self.assembly_id,
                                                             _mode_id_,
                                                             _mechanism_id_,
                                                             _next_id_,
                                                             _parent_)
                self._app.DB.execute_query(_query_,
                                           None,
                                           self._app.ProgCnx,
                                           True)

                self._load_fmeca_tab()

            elif button.get_name() == 'Remove':
                (model, row) = self.tvwFMECA.get_selection().get_selected()
                _fmeca_len_ = len(self._FMECA_col_order)
                _type_ = model.get_value(row, _fmeca_len_)
                _id_ = model.get_value(row, 0)

                if _type_ == 0:
                    # Delete the failure mode from the FMECA table, then delete
                    # associated failure mechanisms, controls, and actions.
                    _query_ = "DELETE FROM tbl_fmeca \
                               WHERE fld_mode_id=%d" % _id_
                    self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               True)

                    _query_ = "DELETE FROM tbl_fmeca_mechanisms \
                               WHERE fld_mode_id=%d" % _id_
                    self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               True)

                    _query_ = "DELETE FROM tbl_fmeca_controls \
                               WHERE fld_mode_id=%d" % _id_
                    self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               True)

                    _query_ = "DELETE FROM tbl_fmeca_actions \
                               WHERE fld_mode_id=%d" % _id_
                    self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               True)
                elif _type_ == 1:
                    # Delete the failure mechanism from the FMECA mechanisms
                    # table, then delete associated controls and actions.
                    _query_ = "DELETE FROM tbl_fmeca_mechanisms \
                               WHERE fld_mechanism_id=%d" % _id_
                    self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               True)

                    _query_ = "DELETE FROM tbl_fmeca_controls \
                               WHERE fld_mechanism_id=%d" % _id_
                    self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               True)

                    _query_ = "DELETE FROM tbl_fmeca_actions \
                               WHERE fld_mechanism_id=%d" % _id_
                    self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               True)
                elif _type_ == 2:
                    # Delete the control from the FMECA controls table.
                    _query_ = "DELETE FROM tbl_fmeca_controls \
                               WHERE fld_control_id=%d" % _id_
                    self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               True)
                elif _type_ == 3:
                    # Delete the control from the FMECA actions table.
                    _query_ = "DELETE FROM tbl_fmeca_actions \
                               WHERE fld_action_id=%d" % _id_
                    self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               True)

                self._load_fmeca_tab()

            elif button.get_name() == 'Analyze':
                # Calculate the MIL-STD-1629A and automotive RPN criticalities.
                (self._CA,
                 self._ItemCA,
                 self._RPN) = _calc.criticality_analysis(self._CA,
                                                         self._ItemCA,
                                                         self._RPN)

                # Update the RTK program database with the MIL-STD-1629A
                # results.
                _query_ = "UPDATE tbl_fmeca \
                           SET fld_mode_criticality=%g, \
                               fld_mode_failure_rate=%g \
                           WHERE fld_mode_id=%d"

                _keys_ = self._CA.keys()
                for i in range(len(_keys_)):
                    _values_ = (self._CA[_keys_[i]][4], self._CA[_keys_[i]][5],
                                _keys_[i])
                    _query_ = _query_ % _values_

                    _results_ = self._app.DB.execute_query(_query_,
                                                           None,
                                                           self._app.ProgCnx,
                                                           commit=True)

                # Update the RTK program database with the automotive RPN
                # results.
                _query_ = "UPDATE tbl_fmeca_mechanisms \
                           SET fld_rpn=%d, fld_rpn_new=%d \
                           WHERE fld_mechanism_id=%d"

                _keys_ = self._RPN.keys()
                for i in range(len(_keys_)):
                    _values_ = (self._RPN[_keys_[i]][3],
                                self._RPN[_keys_[i]][7],
                                _keys_[i])
                    _query_ = _query_ % _values_
                    _results_ = self._app.DB.execute_query(_query_,
                                                           None,
                                                           self._app.ProgCnx,
                                                           commit=True)

                # Update the RTK program database with the MIL-STD-1629A item
                # criticality.
                _query_ = "UPDATE tbl_system \
                           SET fld_assembly_criticality='%s' \
                           WHERE fld_assembly_id=%d"

                _keys_ = self._ItemCA.keys()
                for i in range(len(_keys_)):
                    _values_ = (self._ItemCA[_keys_[i]][-1], _keys_[i])
                    _query_ = _query_ % _values_
                    _results_ = self._app.DB.execute_query(_query_,
                                                           None,
                                                           self._app.ProgCnx,
                                                           commit=True)

                self._load_fmeca_tab()

            elif button.get_name() == 'Save':
                self._save_fmeca()
        elif _page_ == 7:  # Maintenance planning tab.
            if button.get_name() == 'Add':
                print "Add maintenance activity"
            elif button.get_name() == 'Remove':
                print "Remove maintenance activity"
            elif button.get_name() == 'Analyze':
                print "Maintenance costs"
            elif button.get_name() == 'Save':
                print "Saving maintenance policy"

        return False

    def _allocate(self):
        """
        Method to allocate reliability of selected assembly to lower level
        assemblies.  Only allocates one indenture level down.
        """

        def equal_apportionment(model, N, Ts, Rs):  # pylint: disable=C0103
            '''
            Function to perform equal apportionment of a reliability
            requirement.

            :param model: the gtk.TreeModel() from which to read/write
                          allocation data.
            :type model: gtk.TreeModel()
            :param integer N: the number of assemblies to which the reliability
                              requirement is allocated.
            :param float Ts: the mission or operating time.
            :param float Rs: the reliability requirement.
            :return: False or True
            '''

            try:
                _Wi_ = 1.0 / float(N)
            except ZeroDivisionError:
                return True

            _Ri_ = Rs ** _Wi_  # @IgnorePep8

            try:
                _FRi_ = -1.0 * log(_Ri_) / Ts
            except ZeroDivisionError:
                return True
            try:
                _MTBFi_ = 1.0 / _FRi_
            except ZeroDivisionError:
                return True

            _row_ = model.get_iter_root()
            while _row_ is not None:
                if model.get_value(_row_, 3):
                    model.set_value(_row_, 12, _Wi_)
                    model.set_value(_row_, 15, _FRi_)
                    model.set_value(_row_, 17, _MTBFi_)
                    model.set_value(_row_, 19, _Ri_)

                _row_ = _model_.iter_next(_row_)

            return False

        def agree_apportionment(model, N, Ts, Rs):  # pylint: disable=C0103
            '''
            Function to perform AGREE apportionment of a reliability
            requirement.

            :param model: the gtk.TreeModel() from which to read/write
                          allocation data.
            :type model: gtk.TreeModel()
            :param integer N: the number of assemblies to which the reliability
                              requirement is allocated.
            :param float Ts: the mission or operating time.
            :param float Rs: the reliability requirement.
            :return: False
            '''

            _row_ = model.get_iter_root()
            while _row_ is not None:
                if model.get_value(_row_, 3):
                    _DC_ = float(model.get_value(_row_, 7))
                    _ti_ = Ts * _DC_ / 100.0
                    _wi_ = float(model.get_value(_row_, 12))
                    _ni_ = float(model.get_value(_row_, 5))
                    _MTBFi_ = (N * _wi_ * _ti_) / (-1.0 * _ni_ * log(Rs))
                    _FRi_ = 1.0 / _MTBFi_
                    _Ri_ = exp(-1.0 * _FRi_ * Ts)
                    _model_.set_value(_row_, 6, _ti_)
                    _model_.set_value(_row_, 15, _FRi_)
                    _model_.set_value(_row_, 17, _MTBFi_)
                    _model_.set_value(_row_, 19, _Ri_)

                _row_ = _model_.iter_next(_row_)

            return False

        def arinc_apportionment(model, Ts, lambdas):  # pylint: disable=C0103
            '''
            Function to perform ARINC apportionment of the reliability
            requirement.

            :param model: the gtk.TreeModel() from which to read/write
                          allocation data.
            :type model: gtk.TreeModel()
            :param float Ts: the mission or operating time.
            :param float lambdas: the failure rate requirement to allocate.
            :return: False or True
            '''

            # Calculate the current system failure rate.
            _FRs_ = 0.0
            _row_ = model.get_iter_root()
            while _row_ is not None:
                _FRs_ += float(model.get_value(_row_, 14))
                _row_ = model.iter_next(_row_)

            # Now calculate the allocated values for each sub-system.
            _row_ = model.get_iter_root()
            while _row_ is not None:
                if model.get_value(_row_, 3) == 1:
                    _FRi_ = float(model.get_value(_row_, 14))
                    try:
                        _Wi_ = _FRi_ / _FRs_
                    except ZeroDivisionError:
                        return True
                    _FRi_ = _Wi_ * lambdas
                    try:
                        _MTBFi_ = 1.0 / _FRi_
                    except ZeroDivisionError:
                        return True

                    _Ri_ = exp(-1.0 * _FRi_ * Ts)

                else:
                    _Wi_ = 0.0
                    _FRi_ = 0.0
                    _MTBFi_ = 0.0
                    _Ri_ = 0.0

                model.set_value(_row_, 12, _Wi_)
                model.set_value(_row_, 15, _FRi_)
                model.set_value(_row_, 17, _MTBFi_)
                model.set_value(_row_, 19, _Ri_)

                _row_ = model.iter_next(_row_)

            return False

        def foo_apportionment(model, Ts, lambdas):  # pylint: disable=C0103
            '''
            Function to perform feasibility of objectives apportionment of the
            reliability requirement.

            :param model: the gtk.TreeModel() from which to read/write
                          allocation data.
            :type model: gtk.TreeModel()
            :param float Ts: the mission or operating time.
            :param float lambdas: the failure rate requirement to allocate.
            :return: False or True
            '''
            # First calculate the system failure rate and weighting factor for
            # each sub-system.
            _Wght_ = 0.0
            _row_ = model.get_iter_root()
            while _row_ is not None:
                if model.get_value(_row_, 3):
                    _ri1_ = model.get_value(_row_, 8)
                    _ri2_ = model.get_value(_row_, 9)
                    _ri3_ = model.get_value(_row_, 10)
                    _ri4_ = model.get_value(_row_, 11)
                    _Wi_ = _ri1_ * _ri2_ * _ri3_ * _ri4_
                    _Wght_ += _Wi_
                    model.set_value(_row_, 12, _Wi_)

                _row_ = model.iter_next(_row_)

            _row_ = model.get_iter_root()
            while _row_ is not None:
                if model.get_value(_row_, 3):
                    _Wi_ = model.get_value(_row_, 12)
                    _Ci_ = _Wi_ / _Wght_
                    _FRi_ = _Ci_ * lambdas
                    try:
                        _MTBFi_ = 1.0 / _FRi_
                    except ZeroDivisionError:
                        _MTBFi_ = 0.0
                    _Ri_ = exp(-1.0 * _FRi_ * Ts)

                    model.set_value(_row_, 13, _Ci_)
                    model.set_value(_row_, 15, _FRi_)
                    model.set_value(_row_, 17, _MTBFi_)
                    model.set_value(_row_, 19, _Ri_)

                _row_ = model.iter_next(_row_)

            return False

        _model_ = self.tvwAllocation.get_model()
        _row_ = _model_.get_iter_root()

        # Read the requirement inputs.  Raise an application error if one is
        # missing or can't be converted to float.
        try:
            _Rs_ = float(self.txtReliabilityGoal.get_text())
        except ValueError:
            _util.application_error(_(u"Missing required input: Reliability "
                                      u"goal.\nPlease provide and try again."))
            return True

        try:
            _lambdas_ = float(self.txtFailureRateGoal.get_text())
        except ValueError:
            _util.application_error(_(u"Missing required input: Failure "
                                      u"rate goal.\nPlease provide and try "
                                      u"again."))
            return True

        try:
            _Ts_ = float(self.txtOperTime.get_text())
        except ValueError:
            _util.application_error(_(u"Missing required input: Operating "
                                      u"time.\nPlease provide and try again."))
            return True

        _n_assemblies_ = 0
        while _row_ is not None:
            if _model_.get_value(_row_, 3):
                _n_assemblies_ += 1
            _row_ = _model_.iter_next(_row_)

        # Try to allocate the reliability requirement using the selected
        # methodology.  Raise an application error if unsuccessful.
        if self.cmbAllocationType.get_active() == 1 and \
                equal_apportionment(_model_, _n_assemblies_, _Ts_, _Rs_):
            _util.application_error(_(u"Unable to allocate reliability "
                                      u"requirement.  Check your input values "
                                      u"and try again.  If allocation "
                                      u"continues to fail, please report the "
                                      u"problem to bugs@reliaqual.com."))

        elif self.cmbAllocationType.get_active() == 2 and \
                agree_apportionment(_model_, _n_assemblies_, _Ts_, _Rs_):
            _util.application_error(_(u"Unable to allocate reliability "
                                      u"requirement.  Check your input values "
                                      u"and try again.  If allocation "
                                      u"continues to fail, please report the "
                                      u"problem to bugs@reliaqual.com."))

        elif self.cmbAllocationType.get_active() == 3 and \
                arinc_apportionment(_model_, _Ts_, _lambdas_):
            _util.application_error(_(u"Unable to allocate reliability "
                                      u"requirement.  Check your input values "
                                      u"and try again.  If allocation "
                                      u"continues to fail, please report the "
                                      u"problem to bugs@reliaqual.com."))

        elif self.cmbAllocationType.get_active() == 4 and \
                foo_apportionment(_model_, _Ts_, _lambdas_):
            _util.application_error(_(u"Unable to allocate reliability "
                                      u"requirement.  Check your input values "
                                      u"and try again.  If allocation "
                                      u"continues to fail, please report the "
                                      u"problem to bugs@reliaqual.com."))

        elif self.cmbAllocationType.get_active() < 1 or \
                self.cmbAllocationType.get_active() > 4:
            _util.application_error(_(u"No allocation method selected.  "
                                      u"Please select an allocation method "
                                      u"and try again."))

        self.txtNumElements.set_text(str(_n_assemblies_))

        return False

    def _calculate_goals(self, measure=500):
        """
        Calculates the other two reliability metrics from the HARDWARE class
        similar item analysis goal provided.

        Keyword Arguments:
        measure -- the reliability goal measurement:
                   1. Reliability
                   2. MTBF
                   3. Hazard Rate
        """

        op_time = float(self.txtOperTime.get_text())

        if measure == 500:
            Rg = float(self.txtReliabilityGoal.get_text())
            try:
                MTBFg = -1.0 * op_time / log(Rg)
            except ZeroDivisionError:
                MTBFg = 0.0
            try:
                FRg = 1.0 / MTBFg
            except ZeroDivisionError:
                FRg = 0.0

            return (MTBFg, FRg)

        elif measure == 501:
            MTBFg = float(self.txtMTBFGoal.get_text())
            try:
                FRg = 1.0 / MTBFg
            except ZeroDivisionError:
                FRg = 0.0
            try:
                Rg = exp(-1.0 * op_time / MTBFg)
            except ZeroDivisionError:
                Rg = 1.0

            return (Rg, FRg)

        elif measure == 502:
            FRg = float(self.txtFailureRateGoal.get_text())
            try:
                MTBFg = 1.0 / FRg
            except ZeroDivisionError:
                MTBFg = 0.0
            try:
                Rg = exp(-1.0 * op_time / MTBFg)
            except ZeroDivisionError:
                Rg = 1.0

            return (Rg, MTBFg)

    def _calculate_risk(self):
        """
        Calculates the Assembly Object risk analysis.
        """

        # Get the list of failure probability names then create a dictionary
        # using these probability names as the keys.  The values for each key
        # are a list where the list contains:
        #
        #   Index    Information
        #     0      Count of assembly-level combinations before mitigation.
        #     1      Count of system-level combinations before mitigation.
        #     2      Count of assembly-level combinations after mitigation.
        #     3      Count of system-level combinations after mitigation.
        #     4      Index in the gtk.TreeView() risk map for the first count.
        # {'Probability Name': [Assembly Count, System Count, Assembly Count,
        # System Count, Index]}
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

        # Get the count of hazard criticality and hazard probability
        # combinations for assembly level effects and system level effects.
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

            # {'Severity Name': [Severity Value, {'Probability Name':
            # [Count, P Value, Cell Color]}
            # Increment the count of assembly and system severity/probability
            # combinations.
            try:
                _probs_[_assembly_prob_][0] += 1
                _probs_[_system_prob_][1] += 1
            except KeyError:
                pass

            try:
                _c_ = self._assembly_risks_[_assembly_crit_][0]
                _p_ = \
                    self._assembly_risks_[_assembly_crit_][1][_assembly_prob_][
                        1]
                _assembly_hri_ = _c_ * _p_
                _c_ = self._assembly_risks_[_assembly_crit_f_][0]
                _p_ = \
                    self._assembly_risks_[_assembly_crit_f_][1][
                        _assembly_prob_f_][
                        1]
                _assembly_hri_f_ = _c_ * _p_
            except KeyError:
                _assembly_hri_ = 0
                _assembly_hri_f_ = 0

            try:
                _c_ = self._system_risks_[_system_crit_][0]
                _p_ = self._system_risks_[_system_crit_][1][_system_prob_][1]
                _system_hri_ = _c_ * _p_
                _c_ = self._system_risks_[_system_crit_f_][0]
                _p_ = self._system_risks_[_system_crit_f_][1][_system_prob_f_][
                    1]
                _system_hri_f_ = _c_ * _p_
            except KeyError:
                _system_hri_ = 0
                _system_hri_f_ = 0

            _model_.set_value(_row_, 8, _assembly_hri_)
            _model_.set_value(_row_, 12, _assembly_hri_f_)
            _model_.set_value(_row_, 16, _system_hri_)
            _model_.set_value(_row_, 20, _system_hri_f_)

            # Update the count of severity/probability interactions and
            # calculate the hazard risk index (HRI) for the assembly and the
            # system.
            for i in range(len(_keys_)):
                try:
                    self._assembly_risks_[_assembly_crit_][1][_keys_[i]][0] = \
                        _probs_[_keys_[i]][0]
                except KeyError:
                    pass

                try:
                    self._system_risks_[_system_crit_][1][_keys_[i]][0] = \
                        _probs_[_keys_[i]][1]
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
            # _calculations_['hr_sys'] = model.get_value(row, 2)

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

            # Get the existing results.  This allows the use of the results
            # fields to be manually set to a float values by the user.
            # Essentially creating five more user-defined float values.
            _calculations_['res1'] = model.get_value(row, 27)
            _calculations_['res2'] = model.get_value(row, 28)
            _calculations_['res3'] = model.get_value(row, 29)
            _calculations_['res4'] = model.get_value(row, 30)
            _calculations_['res5'] = model.get_value(row, 31)

            keys = _calculations_.keys()
            values = _calculations_.values()

            for i in range(len(keys)):
                vars()[keys[i]] = values[i]

            # If the system failure intensity is greater than zero, perform
            # the remaining risk calculations.  If not, notify the user and
            # exit this function.
            # if _calculations_['hr_sys'] <= 0.0:
            #     _util.application_error(_(u"The System failure intensity is "
            #                               u"0.  This will likely cause "
            #                               u"erroneous results if used in "
            #                               u"calculations.  You should "
            #                               u"specify or calculate the "
            #                               u"system failure intensity before "
            #                               u"executing risk analysis "
            #                               u"calculations."))
            #     return True

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

            # Get the existing results.  This allows the use of the results
            # fields to be manually set to a float values by the user.
            # Essentially creating five more user-defined float values.
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

    def calculate(self, row):
        """
        Method to calculate the HARDWARE class.

        :param row:
        """

        _model_ = self.treeview.get_model()

        _aaf_ = _model_.get_value(row, self._col_order[2])
        _duty_cycle_ = _model_.get_value(row, self._col_order[20])
        _cost_ = _model_.get_value(row, self._col_order[13])
        _lambdaa_ = 0.0
        _lambdad_ = _model_.get_value(row, self._col_order[29])
        _lambdas_ = _model_.get_value(row, self._col_order[33])
        _lambdap_ = 0.0
        _maf_ = _model_.get_value(row, self._col_order[57])
        _mission_time_ = _model_.get_value(row, self._col_order[45])
        _partcount_ = 0
        _pwrdiss_ = _model_.get_value(row, self._col_order[83])
        _quantity_ = _model_.get_value(row, self._col_order[67])
        _ref_des = _model_.get_value(row, self._col_order[68])

        _n_children_ = _model_.iter_n_children(row)
        _row_ = _model_.iter_children(row)

        if _model_.get_value(row, self._col_order[35]) == 1:  # Assessed
            # Assemblies should not show as overstressed.
            _model_.set_value(row, 60, False)
            _icon = _conf.ICON_DIR + '32x32/assembly.png'
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 16, 16)
            _model_.set_value(row, 95, _icon)

            # Calculate all the children and the sum of their results.
            #_n_children_ = _model_.iter_n_children(row)
            #_row_ = _model_.iter_children(row)
            for i in range(_n_children_):  # @UnusedVariable
                (_c_, _la_, _ld_, _ls_, _lp_,
                 _n_parts_, _power_) = self.calculate(_row_)

                _cost_ += _c_
                _lambdaa_ += _la_
                _lambdad_ += _ld_
                _lambdas_ += _ls_
                _partcount_ += _n_parts_
                _pwrdiss_ += _power_

                _row_ = _model_.iter_next(_row_)

        # Specified, Hazard Rate
        elif _model_.get_value(row, self._col_order[35]) == 2:
            _lambdaa_ = _model_.get_value(row, self._col_order[34])
            for i in range(_n_children_):  # @UnusedVariable
                (_c_, _la_, _ld_, _ls_, _lp_,
                 _n_parts_, _power_) = self.calculate(_row_)

        # Specified, MTBF
        elif _model_.get_value(row, self._col_order[35]) == 3:
            _mtbf_ = _model_.get_value(row, self._col_order[51])
            for i in range(_n_children_):  # @UnusedVariable
                (_c_, _la_, _ld_, _ls_, _lp_,
                 _n_parts_, _power_) = self.calculate(_row_)
            try:
                _lambdaa_ = 1.0 / _mtbf_
            except ZeroDivisionError:
                self._app.user_log.error(_(u"Attempted to divide by zero when "
                                           u"calculating the MTBF.\n Item %s: "
                                           u"Active failure rate = %f") %
                                         (_ref_des, _lambdaa_))
                _lambdaa_ = 0.0

        # Adjust the active hazard rate with the additive adjustment factor,
        # quantity of items, multiplicative adjustment factor, and duty cycle.
        _lambdaa_ = ((_lambdaa_ + _aaf_) * _quantity_ * _maf_ * (
            _duty_cycle_ / 100.0)) / _conf.FRMULT

        # Adjust the dormant hazard rate by the quantity of items.
        _lambdad_ = _lambdad_ * _quantity_ / _conf.FRMULT

        # Calculate the software hazard rate.
        _lambdas_ = _lambdas_ * _quantity_ / _conf.FRMULT

        # Calculate the predicted (total) hazard rate.
        _lambdap_ = _lambdaa_ + _lambdad_ + _lambdas_

        # Determine overall percentage of system hazard rate represented by
        # this particular assembly.
        try:
            _failure_rate_percent_ = _lambdap_ / self._system_ht
        except ZeroDivisionError:
            self._app.user_log.error(_(u"Attempted to divide by zero when "
                                       u"calculating failure rate "
                                       u"percentage.\n Item %s: "
                                       u"Failure rate = %f and system failure "
                                       u"rate = %f") % (_ref_des, _lambdaa_,
                                                        self._system_ht))
            _failure_rate_percent_ = 0.0

        # Calculate the MTBF and mission MTBF.
        try:
            _mtbf_ = 1.0 / _lambdap_
        except ZeroDivisionError:
            self._app.user_log.error(_(u"Attempted to divide by zero when "
                                       u"calculating MTBF.\n Item %s: "
                                       u"Predicted failure rate = %f") %
                                     (_ref_des, _lambdap_))
            _mtbf_ = 0.0
        try:
            _mtbf_mission_ = 1.0 / (_lambdaa_ + _lambdas_)
        except ZeroDivisionError:
            self._app.user_log.error(_(u"Attempted to divide by zero when "
                                       u"calculating mission MTBF.\n Item %s: "
                                       u"Active failure rate = %f and "
                                       u"software failure rate = %f") %
                                     (_ref_des, _lambdaa_, _lambdas_))
            _mtbf_mission_ = 0.0

        # Calculate the mission reliability and limiting reliability.
        _reliability_mission_ = exp(
            -1.0 * (_lambdaa_ + _lambdas_) * _mission_time_)
        _reliability_ = exp(-1.0 * _lambdap_ * _mission_time_)

        # Calculate cost per failure, cost per hour, and total cost.
        try:
            _cost_per_failure_ = _cost_ / (_lambdap_ * _mission_time_)
        except ZeroDivisionError:
            self._app.user_log.error(_(u"Attempted to divide by zero when "
                                       u"calculating cost per failure.\n "
                                       u"Item %s: Predicted failure rate = %f "
                                       u"and mission time = %f") %
                                     (_ref_des, _lambdap_, _mission_time_))
            _cost_per_failure_ = 0.0

        _cost_per_hour_ = _cost_ / _mission_time_

        _model_.set_value(row, 13, _cost_)
        _model_.set_value(row, 14, _cost_per_failure_)
        _model_.set_value(row, 15, _cost_per_hour_)
        _model_.set_value(row, 28, _lambdaa_)
        _model_.set_value(row, 29, _lambdad_)
        _model_.set_value(row, 31, _failure_rate_percent_)
        _model_.set_value(row, 32, _lambdap_)
        _model_.set_value(row, 49, _mtbf_mission_)
        _model_.set_value(row, 50, _mtbf_)
        _model_.set_value(row, 69, _reliability_mission_)
        _model_.set_value(row, 70, _reliability_)
        _model_.set_value(row, 82, _partcount_)
        _model_.set_value(row, 83, _pwrdiss_)

        # Set the system hazard rate attribute to the predicted hazard rate if
        # this is the top-level assembly.
        if _model_.get_value(row, 62) == '-':
            self._system_ht = _lambdap_

        self.load_assessment_results_tab()

        return (_cost_, _lambdaa_, _lambdad_, _lambdas_, _lambdap_,
                _partcount_, _pwrdiss_)
