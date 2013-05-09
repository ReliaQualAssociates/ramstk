#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to the
hardware assemblies of the Program.
"""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       assembly.py is part of The RelKit Project
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

# Import other RelKit modules.
import calculations as _calc
import configuration as _conf
import imports as _impt
import utilities as _util
import widgets as _widg

import _assistants_.incident as _incs
from _assistants_.hardware import *

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
                         _("Number of Sub-Systems"),
                         _("Number of Sub-Elements"),
                         _("Operating Time"), _("Duty Cycle"),
                         _("Intricacy (1-10)"), _("State of the Art (1-10)"),
                         _("Operating Time (1-10)"), _("Environment (1-10)"),
                         _("Weighting Factor"), _("Percent Weighting Factor"),
                         _("Current Failure Rate"),
                         _("Allocated Failure Rate"),
                         _("Current MTBF"), _("Allocated MTBF"),
                         _("Current Reliability"), _("Allocated Reliability"),
                         _("Current Availability"), _("Allocated Availability")]

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

    n_attributes = 88

    def __init__(self, application):
        """
        Initializes the Assembly Object.

        Keyword Arguments:
        application -- the RelKit application.
        """

        self._ready = False

        self._app = application

        self.system_model = self._app.HARDWARE.model
        self.system_selected_row = self._app.HARDWARE.selected_row

        self.assembly_id = 0
        self._category = 0
        self._subcategory = 0
        self._mode_id = 0

        self._risk_col_order = []
        self._sia_col_order = []

        self._hrmodel = {}

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
        self.btnAddItem = gtk.ToolButton(stock_id = gtk.STOCK_ADD)
        self.btnRemoveItem = gtk.ToolButton(stock_id = gtk.STOCK_REMOVE)
        self.btnAnalyze = gtk.ToolButton(stock_id = gtk.STOCK_NO)
        self.btnSaveResults = gtk.ToolButton(stock_id = gtk.STOCK_SAVE)
        self.btnRollup = gtk.ToolButton(stock_id = gtk.STOCK_NO)
        self.btnEdit = gtk.ToolButton(stock_id = gtk.STOCK_EDIT)

# Create the General Data tab widgets for the ASSEMBLY object.
        self.fxdGenDataQuad1 = gtk.Fixed()
        self.txtName = _widg.make_entry()
        self.txtPartNum = _widg.make_entry()
        self.txtAltPartNum = _widg.make_entry()
        self.txtRefDes = _widg.make_entry()
        self.txtCompRefDes = _widg.make_entry()
        self.txtQuantity = _widg.make_entry()
        self.txtDescription = _widg.make_entry()
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
        self.tvwRisk = gtk.TreeView()
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
        # TODO: Implement FMEA/FMECA for ASSEMBLY.

# Create the Maintenance Planning tab widgets for the ASSEMBLY object.
        # TODO: Implement Maintenance Planning for ASSEMBLY.

        self.vbxAssembly = gtk.VBox()
        toolbar = self._toolbar_create()

        self.vbxAssembly.pack_start(toolbar, expand=False)
        self.vbxAssembly.pack_start(self.notebook)

        self._ready = True

    def _toolbar_create(self):
        """ Method to create the toolbar for the Assembly Object work book. """

        toolbar = gtk.Toolbar()

# Add sibling assembly button.
        button = gtk.ToolButton()
        button.set_tooltip_text(_(u"Adds a new assembly at the same indenture level as the selected assembly to the RelKit Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.assembly_add, 0)
        toolbar.insert(button, 0)

# Add child assembly button.
        button = gtk.ToolButton()
        button.set_tooltip_text(_(u"Adds a new assembly one indenture level subordinate to the selected assembly to the RelKit Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_child.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.assembly_add, 1)
        toolbar.insert(button, 1)

# Delete assembly button
        button = gtk.ToolButton()
        button.set_tooltip_text(_(u"Removes the currently selected assembly from the RelKit Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/delete.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.assembly_delete)
        toolbar.insert(button, 2)

        toolbar.insert(gtk.SeparatorToolItem(), 3)

# Add item button.  Depending on the notebook page selected will determine
# what type of item is added.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        self.btnAddItem.set_icon_widget(image)
        self.btnAddItem.set_name('Add')
        self.btnAddItem.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnAddItem, 4)

# Remove item button.  Depending on the notebook page selected will determine
# what type of item is removed.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        self.btnRemoveItem.set_icon_widget(image)
        self.btnRemoveItem.set_name('Remove')
        self.btnRemoveItem.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnRemoveItem, 5)

# Perform analysis button.  Depending on the notebook page selected will
# determine which analysis is executed.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        self.btnAnalyze.set_icon_widget(image)
        self.btnAnalyze.set_name('Analyze')
        self.btnAnalyze.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnAnalyze, 6)

# Save results button.  Depending on the notebook page selected will determine
# which results are saved.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        self.btnSaveResults.set_icon_widget(image)
        self.btnSaveResults.set_name('Save')
        self.btnSaveResults.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnSaveResults, 7)

        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/rollup.png')
        self.btnRollup.set_icon_widget(image)
        self.btnRollup.set_name('Rollup')
        self.btnRollup.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnRollup, 8)

        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/edit.png')
        self.btnEdit.set_icon_widget(image)
        self.btnEdit.set_name('Edit')
        self.btnEdit.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnEdit, 9)

# Create an import button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/db-import.png')
        button.set_icon_widget(image)
        button.set_name('Import')
        button.connect('clicked', ImportHardware, self._app)
        button.set_tooltip_text(_("Launches the hardware import assistant."))
        toolbar.insert(button, 10)

# Create an export button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/db-export.png')
        button.set_icon_widget(image)
        button.set_name('Export')
        button.connect('clicked', ExportHardware, self._app)
        button.set_tooltip_text(_("Launches the hardware export assistant."))
        toolbar.insert(button, 11)

        toolbar.show()

# Hide the toolbar buttons associated with specific analyses.
        self.btnAddItem.hide()
        self.btnRemoveItem.hide()
        self.btnAnalyze.hide()
        self.btnSaveResults.hide()
        self.btnRollup.hide()
        self.btnEdit.hide()

        return(toolbar)

    def _general_data_widgets_create(self):
        """ Method to create General Data widgets. """

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

        y_pos = 5
        for i in range(len(self._gd_tab_labels[0])):
            label = _widg.make_label(self._gd_tab_labels[0][i], 150, 25)
            self.fxdGenDataQuad1.put(label, 5, (30 * i + y_pos))

        self.fxdGenDataQuad1.put(self.txtName, 155, y_pos)
        y_pos += 30
        self.fxdGenDataQuad1.put(self.txtPartNum, 155, y_pos)
        y_pos += 30
        self.fxdGenDataQuad1.put(self.txtAltPartNum, 155, y_pos)
        y_pos += 90
        self.fxdGenDataQuad1.put(self.txtRefDes, 155, y_pos)
        y_pos += 30
        self.fxdGenDataQuad1.put(self.txtCompRefDes, 155, y_pos)
        y_pos += 30
        self.fxdGenDataQuad1.put(self.txtQuantity, 155, y_pos)
        y_pos += 30
        self.fxdGenDataQuad1.put(self.txtDescription, 155, y_pos)

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

        y_pos = 5
        for i in range(len(self._gd_tab_labels[2])):
            label = _widg.make_label(self._gd_tab_labels[2][i], 150, 25)
            self.fxdGenDataQuad2.put(label, 5, (30 * i + y_pos))

        self.fxdGenDataQuad2.put(self.cmbManufacturer, 155, y_pos)
        y_pos += 30
        self.fxdGenDataQuad2.put(self.txtCAGECode, 155, y_pos)
        y_pos += 30
        self.fxdGenDataQuad2.put(self.txtLCN, 155, y_pos)
        y_pos += 30
        self.fxdGenDataQuad2.put(self.txtNSN, 155, y_pos)
        y_pos += 30
        self.fxdGenDataQuad2.put(self.txtYearMade, 155, y_pos)

        self.fxdGenDataQuad2.show_all()

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

        y_pos = 5
        for i in range(len(self._gd_tab_labels[1])):
            label = _widg.make_label(self._gd_tab_labels[1][i], 150, 25)
            self.fxdGenDataQuad3.put(label, 5, (30 * i + y_pos))

        self.fxdGenDataQuad3.put(self.txtSpecification, 155, y_pos)
        y_pos += 30
        self.fxdGenDataQuad3.put(self.txtPageNum, 155, y_pos)
        y_pos += 30
        self.fxdGenDataQuad3.put(self.txtFigNum, 155, y_pos)
        y_pos += 30
        self.fxdGenDataQuad3.put(self.txtImageFile, 155, y_pos)
        y_pos += 30
        self.fxdGenDataQuad3.put(self.txtAttachments, 155, y_pos)
        y_pos += 30
        self.fxdGenDataQuad3.put(self.txtMissionTime, 155, y_pos)

        self.fxdGenDataQuad3.show_all()

# Quadrant 4 (lower right) widgets.  These widgets are used to display
# miscellaneous information about the selected assembly.
        self.txtRevisionID.set_tooltip_text(_("Displays the currently selected revision."))

        self.chkRepairable.set_tooltip_text(_("Indicates whether or not the selected assembly is repairable."))
        self.chkRepairable.connect('toggled', self._callback_check, 75)

        self.chkTagged.set_tooltip_text(_("Indicates whether or not the selected assembly is tagged."))
        self.chkTagged.connect('toggled', self._callback_check, 79)

        y_pos = 5
        for i in range(len(self._gd_tab_labels[3])):
            label = _widg.make_label(self._gd_tab_labels[3][i], 150, 25)
            self.fxdGenDataQuad4.put(label, 5, (30 * i + y_pos))

        self.fxdGenDataQuad4.put(self.txtRevisionID, 155, y_pos)
        y_pos += 30
        self.fxdGenDataQuad4.put(self.chkRepairable, 155, y_pos)
        y_pos += 30
        self.fxdGenDataQuad4.put(self.chkTagged, 155, y_pos)
        y_pos += 30

        self.txtRemarks.set_tooltip_text(_(u"Enter any remarks associated with the selected assembly."))
        self.txtRemarks.get_child().get_child().connect('focus-out-event',
                                                        self._callback_entry,
                                                        'text', 71)
        self.fxdGenDataQuad4.put(self.txtRemarks, 155, y_pos)

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
            label.set_alignment(xalign=0.5, yalign=0.5)
            text = "<span weight='bold'>%s</span>" % self._al_header_labels[i]
            label.set_markup(text)
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

        y_pos = 5

        label = _widg.make_label(self._al_tab_labels[0], 100, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbRqmtType, 110, y_pos)
        y_pos += 35

        label = _widg.make_label(self._al_tab_labels[1], 100, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtReliabilityGoal, 110, y_pos)
        y_pos += 30

        label = _widg.make_label(self._al_tab_labels[2], 100, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtMTBFGoal, 110, y_pos)
        y_pos += 30

        label = _widg.make_label(self._al_tab_labels[3], 100, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtFailureRateGoal, 110, y_pos)
        y_pos += 30

        label = _widg.make_label(self._al_tab_labels[4], 100, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbAllocationType, 110, y_pos)
        y_pos += 35

        label = _widg.make_label(self._al_tab_labels[5], 100, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtNumElements, 110, y_pos)
        y_pos += 30

        label = _widg.make_label(self._al_tab_labels[6], 100, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtOperTime, 110, y_pos)
        y_pos += 30

        fixed.put(self.chkApplyResults, 5, y_pos)
        y_pos += 45

        fixed.show_all()

        # Load the tab.
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

        if(_conf.RELIAFREE_MODULES[0] == 1):
            values = (model.get_string_from_iter(row),
                      self._app.REVISION.revision_id)
        else:
            values = (model.get_string_from_iter(row), 0)

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        # Get mission time from the HARDWARE gtk.TreeView
        self.cmbAllocationType.set_active(model.get_value(row, 3))
        self.txtOperTime.set_text(str('{0:0.2f}'.format(model.get_value(row, 45))))

        if(_conf.BACKEND == 'mysql'):
            query = "SELECT t1.fld_revision_id, t1.fld_assembly_id, \
                            t2.fld_description, t1.fld_included, \
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
                     AND t1.fld_revision_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT t1.fld_revision_id, t1.fld_assembly_id, \
                            t2.fld_description, t1.fld_included, \
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
                     WHERE t2.fld_parent_assembly=? \
                     AND t1.fld_revision_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        if(_conf.RELIAFREE_MODULES[0] == 1):
            values = (self.assembly_id, self._app.REVISION.revision_id)
        else:
            values = (self.assembly_id, 0)

        if(_conf.BACKEND == 'mysql'):
            query = "SELECT fld_reliability_goal_measure, \
                            fld_reliability_goal \
                     FROM tbl_system \
                     WHERE fld_assembly_id=%d \
                     AND fld_revision_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT fld_reliability_goal_measure, \
                            fld_reliability_goal \
                     FROM tbl_system \
                     WHERE fld_assembly_id=? \
                     AND fld_revision_id=?"

        goal = self._app.DB.execute_query(query,
                                          values,
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

        # Create the gtk.TreeView.
        # Retrieve the column heading text from the format file.
        path = "/root/tree[@name='Risk']/column/usertitle"
        heading = etree.parse(_conf.RELIAFREE_FORMAT_FILE[17]).xpath(path)

        # Retrieve the column datatype from the format file.
        path = "/root/tree[@name='Risk']/column/datatype"
        datatype = etree.parse(_conf.RELIAFREE_FORMAT_FILE[17]).xpath(path)

        # Retrieve the cellrenderer type from the format file.
        path = "/root/tree[@name='Risk']/column/widget"
        widget = etree.parse(_conf.RELIAFREE_FORMAT_FILE[17]).xpath(path)

        # Retrieve the column position from the format file.
        path = "/root/tree[@name='Risk']/column/position"
        position = etree.parse(_conf.RELIAFREE_FORMAT_FILE[17]).xpath(path)

        # Retrieve whether or not the column is editable from the format file.
        path = "/root/tree[@name='Risk']/column/editable"
        editable = etree.parse(_conf.RELIAFREE_FORMAT_FILE[17]).xpath(path)

        # Retrieve whether or not the column is visible from the format file.
        path = "/root/tree[@name='Risk']/column/visible"
        visible = etree.parse(_conf.RELIAFREE_FORMAT_FILE[17]).xpath(path)

        # Create a list of GObject datatypes to pass to the model.
        types = []
        for i in range(len(position)):
            types.append(datatype[i].text)

        gobject_types = []
        gobject_types = [gobject.type_from_name(types[ix])
            for ix in range(len(types))]

        for i in range(8):
            gobject_types.append(gobject.type_from_name('gint'))

        query = "SELECT fld_category_noun, \
                        fld_category_value \
                 FROM tbl_risk_category"
        risk_category = self._app.COMDB.execute_query(query,
                                                      None,
                                                      self._app.ComCnx)

        bg_color = _conf.RELIAFREE_COLORS[6]
        fg_color = _conf.RELIAFREE_COLORS[7]

        # Create the model and treeview.
        model = gtk.TreeStore(*gobject_types)
        self.tvwRisk.set_model(model)

        cols = int(len(heading))
        _visible = False
        for i in range(cols):
            self._risk_col_order.append(int(position[i].text))

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

            column = gtk.TreeViewColumn()
            column.set_visible(int(visible[i].text))
            column.pack_start(cell, True)
            column.set_attributes(cell, text=int(position[i].text))

            label = _widg.make_column_heading(heading[i].text)
            column.set_widget(label)

            column.set_cell_data_func(cell, _widg.format_cell,
                                      (int(position[i].text),
                                      datatype[i].text))
            column.set_resizable(True)
            column.connect('notify::width', _widg.resize_wrap, cell)

            if(i > 0):
                column.set_reorderable(True)

            self.tvwRisk.append_column(column)

        # Add eight more invisible columns at the end to hold the integer
        # values of the risk categories.
        for i in range(7):
            cell = gtk.CellRendererText()
            column = gtk.TreeViewColumn()
            column.set_visible(0)
            column.pack_start(cell, True)
            column.set_attributes(cell, text=cols + i)
            self.tvwRisk.append_column(column)

        self.tvwRisk.set_tooltip_text(_("Displays the risk analysis for the selected Assembly."))
        self.tvwRisk.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        return False

    def _risk_analysis_tab_create(self):
        """
        Method to create the Risk Analysis gtk.Notebook tab and
        populate it with the appropriate widgets.
        """

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add(self.tvwRisk)

        frame = _widg.make_frame()
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        label = gtk.Label()
        _heading = _("Risk\nAnalysis")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays the risk analysis for the selected Assembly."))

        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _risk_analysis_tab_load(self):
        """
        Loads the similar items analysis worksheet with information for the
        selected assembly's children.
        """

        if self._app.HARDWARE.selected_row is not None:
            model = self._app.HARDWARE.model
            row = self._app.HARDWARE.selected_row
            path_ = model.get_string_from_iter(row)

        if(_conf.RELIAFREE_MODULES[0] == 1):
            values = (self._app.REVISION.revision_id, path_)
        else:
            values = (0, path_)

        if(_conf.BACKEND == 'mysql'):
            query = "SELECT t1.fld_risk_id, t2.fld_description, \
                            t1.fld_change_desc_1, t1.fld_change_category_1, \
                            t1.fld_change_effort_1, t1.fld_change_cost_1, \
                            t1.fld_change_desc_2, t1.fld_change_category_2, \
                            t1.fld_change_effort_2, t1.fld_change_cost_2, \
                            t1.fld_change_desc_3, t1.fld_change_category_3, \
                            t1.fld_change_effort_3, t1.fld_change_cost_3, \
                            t1.fld_change_desc_4, t1.fld_change_category_4, \
                            t1.fld_change_effort_4, t1.fld_change_cost_4, \
                            t1.fld_change_desc_5, t1.fld_change_category_5, \
                            t1.fld_change_effort_5, t1.fld_change_cost_5, \
                            t1.fld_change_desc_6, t1.fld_change_category_6, \
                            t1.fld_change_effort_6, t1.fld_change_cost_6, \
                            t1.fld_change_desc_7, t1.fld_change_category_7, \
                            t1.fld_change_effort_7, t1.fld_change_cost_7, \
                            t1.fld_change_desc_8, t1.fld_change_category_8, \
                            t1.fld_change_effort_8, t1.fld_change_cost_8, \
                            t1.fld_function_1, t1.fld_function_2, \
                            t1.fld_function_3, t1.fld_function_4, \
                            t1.fld_function_5, \
                            t1.fld_result_1, t1.fld_result_2, t1.fld_result_3, \
                            t1.fld_result_4, t1.fld_result_5, \
                            t1.fld_user_blob_1, t1.fld_user_blob_2, \
                            t1.fld_user_blob_3, t1.fld_user_float_1, \
                            t1.fld_user_float_2, t1.fld_user_float_3, \
                            t1.fld_user_int_1, t1.fld_user_int_2, \
                            t1.fld_user_int_3, \
                            t1.fld_category_value_1, t1.fld_category_value_2, \
                            t1.fld_category_value_3, t1.fld_category_value_4, \
                            t1.fld_category_value_5, t1.fld_category_value_6, \
                            t1.fld_category_value_7, t1.fld_category_value_8 \
                     FROM tbl_risk_analysis AS t1 \
                     INNER JOIN tbl_system AS t2 \
                     ON t2.fld_assembly_id=t1.fld_assembly_id \
                     WHERE t1.fld_revision_id=%d \
                     AND t2.fld_parent_assembly='%s'"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT t1.fld_risk_id, t2.fld_description, \
                            t1.fld_change_desc_1, t1.fld_change_category_1, \
                            t1.fld_change_effort_1, t1.fld_change_cost_1, \
                            t1.fld_change_desc_2, t1.fld_change_category_2, \
                            t1.fld_change_effort_2, t1.fld_change_cost_2, \
                            t1.fld_change_desc_3, t1.fld_change_category_3, \
                            t1.fld_change_effort_3, t1.fld_change_cost_3, \
                            t1.fld_change_desc_4, t1.fld_change_category_4, \
                            t1.fld_change_effort_4, t1.fld_change_cost_4, \
                            t1.fld_change_desc_5, t1.fld_change_category_5, \
                            t1.fld_change_effort_5, t1.fld_change_cost_5, \
                            t1.fld_change_desc_6, t1.fld_change_category_6, \
                            t1.fld_change_effort_6, t1.fld_change_cost_6, \
                            t1.fld_change_desc_7, t1.fld_change_category_7, \
                            t1.fld_change_effort_7, t1.fld_change_cost_7, \
                            t1.fld_change_desc_8, t1.fld_change_category_8, \
                            t1.fld_change_effort_8, t1.fld_change_cost_8, \
                            t1.fld_function_1, t1.fld_function_2, \
                            t1.fld_function_3, t1.fld_function_4, \
                            t1.fld_function_5, \
                            t1.fld_result_1, t1.fld_result_2, t1.fld_result_3, \
                            t1.fld_result_4, t1.fld_result_5, \
                            t1.fld_user_blob_1, t1.fld_user_blob_2, \
                            t1.fld_user_blob_3, t1.fld_user_float_1, \
                            t1.fld_user_float_2, t1.fld_user_float_3, \
                            t1.fld_user_int_1, t1.fld_user_int_2, \
                            t1.fld_user_int_3, \
                            t1.fld_category_value_1, t1.fld_category_value_2, \
                            t1.fld_category_value_3, t1.fld_category_value_4, \
                            t1.fld_category_value_5, t1.fld_category_value_6, \
                            t1.fld_category_value_7, t1.fld_category_value_8 \
                     FROM tbl_risk_analysis AS t1 \
                     INNER JOIN tbl_system AS t2 \
                     ON t2.fld_assembly_id=t1.fld_assembly_id \
                     WHERE t1.fld_revision_id=? AND t2.fld_parent_assembly=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        model = self.tvwRisk.get_model()
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

    def _similar_item_widgets_create(self):
        """ Method to create the Similar Item Analysis widgets. """

        import pango
        from lxml import etree

        # Create the gtk.TreeView.
        # Retrieve the column heading text from the format file.
        path = "/root/tree[@name='SIA']/column/usertitle"
        heading = etree.parse(_conf.RELIAFREE_FORMAT_FILE[8]).xpath(path)

        # Retrieve the column datatype from the format file.
        path = "/root/tree[@name='SIA']/column/datatype"
        datatype = etree.parse(_conf.RELIAFREE_FORMAT_FILE[8]).xpath(path)

        # Retrieve the cellrenderer type from the format file.
        path = "/root/tree[@name='SIA']/column/widget"
        widget = etree.parse(_conf.RELIAFREE_FORMAT_FILE[8]).xpath(path)

        # Retrieve the column position from the format file.
        path = "/root/tree[@name='SIA']/column/position"
        position = etree.parse(_conf.RELIAFREE_FORMAT_FILE[8]).xpath(path)

        # Retrieve whether or not the column is editable from the format file.
        path = "/root/tree[@name='SIA']/column/editable"
        editable = etree.parse(_conf.RELIAFREE_FORMAT_FILE[8]).xpath(path)

        # Retrieve whether or not the column is visible from the format file.
        path = "/root/tree[@name='SIA']/column/visible"
        visible = etree.parse(_conf.RELIAFREE_FORMAT_FILE[8]).xpath(path)

        # Create a list of GObject datatypes to pass to the model.
        types = []
        for i in range(len(position)):
            types.append(datatype[i].text)

        gobject_types = []
        gobject_types = [gobject.type_from_name(types[ix])
            for ix in range(len(types))]

        bg_color = _conf.RELIAFREE_COLORS[6]
        fg_color = _conf.RELIAFREE_COLORS[7]

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

            column = gtk.TreeViewColumn()
            column.set_visible(int(visible[i].text))
            column.pack_start(cell, True)
            column.set_attributes(cell, text=int(position[i].text))

            label = _widg.make_column_heading(heading[i].text)
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

        if(_conf.RELIAFREE_MODULES[0] == 1):
            values = (self._app.REVISION.revision_id, path_)
        else:
            values = (0, path_)

        if(_conf.BACKEND == 'mysql'):
            query = "SELECT t1.fld_sia_id, t2.fld_description, \
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
                     AND t2.fld_parent_assembly='%s'"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT t1.fld_sia_id, t2.fld_description, \
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
                     WHERE t1.fld_revision_id=? \
                     AND t2.fld_parent_assembly=?"

        results = self._app.DB.execute_query(query,
                                             values,
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

        # Quadrant 1 (upper left) widgets.  These widgets are used to
        # display reliability assessment inputs.
        self.cmbHRType.set_tooltip_text(_("Select the method of assessing the failure intensity for the selected assembly."))

        query = "SELECT fld_hr_type_noun FROM tbl_hr_type"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbHRType, results)
        self.cmbHRType.connect('changed', self._callback_combo, 35)

        self.cmbCalcModel.set_tooltip_text(_("Select the reliability prediction model for the selected assembly."))

        query = "SELECT fld_model_noun FROM tbl_calculation_model"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbCalcModel, results)
        self.cmbCalcModel.connect('changed', self._callback_combo, 10)

        self.txtSpecifiedHt.set_tooltip_text(_("Enter the specified failure intensity for the selected assembly."))
        self.txtSpecifiedHt.connect('focus-out-event',
                                    self._callback_entry, 'float', 34)

        self.txtSpecifiedMTBF.set_tooltip_text(_("Enter the specified mean time between failure (MTBF) for the selected assembly."))
        self.txtSpecifiedMTBF.connect('focus-out-event',
                                      self._callback_entry, 'float', 51)

        self.txtSoftwareHt.set_tooltip_text(_("Enter the software failure rate for the selected assembly."))
        self.txtSoftwareHt.connect('focus-out-event',
                                   self._callback_entry, 'float', 33)

        self.txtAddAdj.set_tooltip_text(_("Enter any reliability assessment additive adjustment factor for the selected assembly."))
        self.txtAddAdj.connect('focus-out-event',
                               self._callback_entry, 'float', 2)

        self.txtMultAdj.set_tooltip_text(_("Enter any reliability assessment multiplicative adjustment factor for the selected assembly."))
        self.txtMultAdj.connect('focus-out-event',
                                self._callback_entry, 'float', 57)

        self.txtAllocationWF.set_tooltip_text(_("Enter the reliability allocation weighting factor for the selected assembly."))
        self.txtAllocationWF.connect('focus-out-event',
                                     self._callback_entry, 'float', 3)

        self.cmbFailDist.set_tooltip_text(_("Select the distribution of times to failure for the selected assembly."))

        query = "SELECT fld_distribution_noun \
                 FROM tbl_distributions"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbFailDist, results)
        self.cmbFailDist.connect('changed', self._callback_combo, 24)

        self.txtFailScale.set_tooltip_text(_("Enter the time to failure distribution scale factor."))
        self.txtFailScale.connect('focus-out-event',
                                  self._callback_entry, 'float', 25)

        self.txtFailShape.set_tooltip_text(_("Enter the time to failure distribution shape factor."))
        self.txtFailShape.connect('focus-out-event',
                                  self._callback_entry, 'float', 26)

        self.txtFailLoc.set_tooltip_text(_("Enter the time to failure distribution location factor."))
        self.txtFailLoc.connect('focus-out-event',
                                self._callback_entry, 'float', 27)

        self.cmbActEnviron.set_tooltip_text(_("Select the active operating environment for the selected assembly."))
        self.cmbActEnviron.connect('changed', self._callback_combo, 22)

        query = "SELECT fld_active_environ_code, fld_active_environ_noun \
                 FROM tbl_active_environs"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        model = self.cmbActEnviron.get_model()
        model.clear()
        self.cmbActEnviron.append_text('')
        for i in range(len(results)):
            self.cmbActEnviron.append_text(results[i][0] + ' - ' +
                                           results[i][1])

        self.txtActTemp.set_tooltip_text(_("Enter the active environment operating temperature for the selected assembly."))
        self.txtActTemp.connect('focus-out-event',
                                self._callback_entry, 'float', 80)

        self.cmbDormantEnviron.set_tooltip_text(_("Select the dormant environment for the selected assembly."))

        query = "SELECT fld_dormant_environ_noun \
                 FROM tbl_dormant_environs"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbDormantEnviron, results)
        self.cmbDormantEnviron.connect('changed', self._callback_combo, 23)

        self.txtDormantTemp.set_tooltip_text(_("Enter the dormant environment temperature for the selected assembly."))
        self.txtDormantTemp.connect('focus-out-event',
                                    self._callback_entry, 'float', 81)

        self.txtDutyCycle.set_tooltip_text(_("Enter the operating duty cycle for the selected assembly."))
        self.txtDutyCycle.connect('focus-out-event',
                                  self._callback_entry, 'float', 20)

        self.txtHumidity.set_tooltip_text(_("Enter the active environment operating humidity for the selected assembly."))
        self.txtHumidity.connect('focus-out-event',
                                 self._callback_entry, 'float', 37)

        self.txtVibration.set_tooltip_text(_("Enter the active environment operating vibration level for the selected assembly."))
        self.txtVibration.connect('focus-out-event',
                                  self._callback_entry, 'float', 84)

        self.txtRPM.set_tooltip_text(_("Enter the active environment operating RPM for the selected assembly."))
        self.txtRPM.connect('focus-out-event',
                            self._callback_entry, 'float', 76)

        self.txtWeibullFile.set_tooltip_text(_("Enter the URL to a survival analysis file for the selected assembly."))
        self.txtWeibullFile.connect('focus-out-event',
                                    self._callback_entry, 'text', 86)

        y_pos = 5
        for i in range(len(self._ai_tab_labels[0])):
            label = _widg.make_label(self._ai_tab_labels[0][i],
                                     150, 25)
            self.fxdRelInputQuad1.put(label, 5, (30 * i + y_pos))

        self.fxdRelInputQuad1.put(self.cmbHRType, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.cmbCalcModel, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtSpecifiedHt, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtSpecifiedMTBF, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtSoftwareHt, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtAddAdj, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtMultAdj, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtAllocationWF, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.cmbFailDist, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtFailScale, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtFailShape, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtFailLoc, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.cmbActEnviron, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtActTemp, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.cmbDormantEnviron, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtDormantTemp, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtDutyCycle, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtHumidity, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtVibration, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtRPM, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad1.put(self.txtWeibullFile, 155, y_pos)

        self.fxdRelInputQuad1.show_all()

        # Create quadrant 2 (upper right) widgets.
        self.cmbMTTRType.set_tooltip_text(_("Select the method of assessing the mean time to repair (MTTR) for the selected assembly."))

        query = "SELECT fld_mttr_type_noun FROM tbl_mttr_type"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbMTTRType, results)
        self.cmbMTTRType.connect('changed', self._callback_combo, 56)

        self.txtSpecifiedMTTR.set_tooltip_text(_("Enter the specified mean time to repair (MTTR) for the selected assembly."))
        self.txtSpecifiedMTTR.connect('focus-out-event',
                                      self._callback_entry, 'float', 55)

        self.txtMTTRAddAdj.set_tooltip_text(_("Enter any mean time to repair (MTTR) assessment additive adjustment factor for the selected assembly."))
        self.txtMTTRAddAdj.connect('focus-out-event',
                                   self._callback_entry, 'float', 53)

        self.txtMTTRMultAdj.set_tooltip_text(_("Enter any mean time to repair (MTTR) assessment multaplicative adjustment factor for the selected assembly."))
        self.txtMTTRMultAdj.connect('focus-out-event',
                                    self._callback_entry, 'float', 54)

        self.cmbRepairDist.set_tooltip_text(_("Select the time to repair distribution for the selected assembly."))

        query = "SELECT fld_distribution_noun FROM tbl_distributions"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbRepairDist, results)
        self.cmbRepairDist.connect('changed', self._callback_combo, 72)

        self.txtRepairScale.set_tooltip_text(_("Enter the time to repair distribution scale parameter."))
        self.txtRepairScale.connect('focus-out-event',
                                    self._callback_entry, 'float', 73)

        self.txtRepairShape.set_tooltip_text(_("Entert the time to repair distribution shape parameter."))
        self.txtRepairShape.connect('focus-out-event',
                                    self._callback_entry, 'float', 74)

        y_pos = 5
        for i in range(len(self._ai_tab_labels[1])):
            label = _widg.make_label(self._ai_tab_labels[1][i],
                                     150, 25)
            self.fxdRelInputQuad2.put(label, 5, (30 * i + y_pos))

        self.fxdRelInputQuad2.put(self.cmbMTTRType, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad2.put(self.txtSpecifiedMTTR, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad2.put(self.txtMTTRAddAdj, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad2.put(self.txtMTTRMultAdj, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad2.put(self.cmbRepairDist, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad2.put(self.txtRepairScale, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad2.put(self.txtRepairShape, 155, y_pos)

        self.fxdRelInputQuad2.show_all()

        # Create quadrrant 4 (lower right) widgets.
        self.cmbCostType.set_tooltip_text(_("Select the method for assessing the cost of the selected assembly."))

        query = "SELECT fld_cost_type_noun FROM tbl_cost_type"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbCostType, results)
        self.cmbCostType.connect('changed', self._callback_combo, 16)

        self.txtCost.set_tooltip_text(_("Enter the cost of the selected assembly."))
        self.txtCost.connect('focus-out-event',
                             self._callback_entry, 'float', 13)

        y_pos = 5
        for i in range(len(self._ai_tab_labels[3])):
            label = _widg.make_label(self._ai_tab_labels[3][i],
                                     150, 25)
            self.fxdRelInputQuad4.put(label, 5, (30 * i + y_pos))

        self.fxdRelInputQuad4.put(self.cmbCostType, 155, y_pos)
        y_pos += 30
        self.fxdRelInputQuad4.put(self.txtCost, 155, y_pos)

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

        frame = _widg.make_frame(_label_=_("Reliability Inputs"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hbox.pack_start(frame)

        # Populate quadrant 2 (upper right).
        vbox = gtk.VBox()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.fxdRelInputQuad2)

        frame = _widg.make_frame(_label_=_("Maintainability Inputs"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vbox.pack_start(frame)

        # Populate quadrant 4 (lower right)
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.fxdRelInputQuad4)

        frame = _widg.make_frame(_label_=_("Miscellaneous Inputs"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vbox.pack_start(frame)

        hbox.pack_start(vbox)

        label = gtk.Label()
        _heading = _("Assessment\nInputs")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Allows entering reliability, maintainability, and other assessment inputs for the selected assembly."))

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

        # Create the quadrant 1 (upper left) widgets.
        self.txtActiveHt.set_tooltip_text(_("Displays the active failure intensity for the selected assembly."))
        self.txtDormantHt.set_tooltip_text(_("Displays the dormant failure intensity for the selected assembly."))
        self.txtSoftwareHt2.set_tooltip_text(_("Displays the software failure intensity for the selected assembly."))
        self.txtPredictedHt.set_tooltip_text(_("Displays the predicted failure intensity for the selected assembly.  This is the sum of the active, dormant, and software failure intensities."))
        self.txtMissionHt.set_tooltip_text(_("Displays the mission failure intensity for the selected assembly."))
        self.txtHtPerCent.set_tooltip_text(_("Displays the percent of the total system failure intensity attributable to the selected assembly."))
        self.txtMTBF.set_tooltip_text(_("Displays the limiting mean time between failure (MTBF) for the selected assembly."))
        self.txtMissionMTBF.set_tooltip_text(_("Displays the mission mean time between failure (MTBF) for the selected assembly."))
        self.txtReliability.set_tooltip_text(_("Displays the limiting reliability for the selected assembly."))
        self.txtMissionRt.set_tooltip_text(_("Displays the mission reliability for the selected assembly."))

        y_pos = 5
        for i in range(len(self._ar_tab_labels[0])):
            label = _widg.make_label(self._ar_tab_labels[0][i],
                                     150, 25)
            self.fxdCalcResultsQuad1.put(label, 5, (30 * i + y_pos))

        self.fxdCalcResultsQuad1.put(self.txtActiveHt, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtDormantHt, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtSoftwareHt2, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtPredictedHt, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtMissionHt, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtHtPerCent, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtMTBF, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtMissionMTBF, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtReliability, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad1.put(self.txtMissionRt, 155, y_pos)

        self.fxdCalcResultsQuad1.show_all()

        # Create the quadrant 2 (upper right) widgets.
        self.txtMPMT.set_tooltip_text(_("Displays the mean preventive maintenance time (MPMT) for the selected assembly."))
        self.txtMCMT.set_tooltip_text(_("Displays the mean corrective maintenance time (MCMT) for the selected assembly."))
        self.txtMTTR.set_tooltip_text(_("Displays the mean time to repair (MTTR) for the selected assembly."))
        self.txtMMT.set_tooltip_text(_("Displays the mean maintenance time (MMT) for the selected assembly."))
        self.txtAvailability.set_tooltip_text(_("Displays the limiting availability for the selected assembly."))
        self.txtMissionAt.set_tooltip_text(_("Displays the mission availability for the selected assembly."))

        y_pos = 5
        for i in range(len(self._ar_tab_labels[1])):
            label = _widg.make_label(self._ar_tab_labels[1][i],
                                     150, 25)
            self.fxdCalcResultsQuad2.put(label, 5, (30 * i + y_pos))

        self.fxdCalcResultsQuad2.put(self.txtMPMT, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad2.put(self.txtMCMT, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad2.put(self.txtMTTR, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad2.put(self.txtMMT, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad2.put(self.txtAvailability, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad2.put(self.txtMissionAt, 155, y_pos)

        self.fxdCalcResultsQuad2.show_all()

        # Create the quadrant 4 (lower right) widgets.
        self.txtTotalCost.set_tooltip_text(_("Displays the total cost of the selected assembly."))
        self.txtCostFailure.set_tooltip_text(_("Displays the cost per failure of the selected assembly."))
        self.txtCostHour.set_tooltip_text(_("Displays the cost per mission hour of the selected assembly."))
        self.txtAssemblyCrit.set_tooltip_text(_("Displays the criticality of the selected assembly.  This is calculated by the FMEA."))
        self.txtPartCount.set_tooltip_text(_("Displays the total number of components used to construct the selected assembly."))
        self.txtTotalPwr.set_tooltip_text(_("Displays the total power of the selected assembly."))

        y_pos = 5
        for i in range(len(self._ar_tab_labels[3])):
            label = _widg.make_label(self._ar_tab_labels[3][i],
                                     150, 25)
            self.fxdCalcResultsQuad4.put(label, 5, (30 * i + y_pos))

        self.fxdCalcResultsQuad4.put(self.txtTotalCost, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad4.put(self.txtCostFailure, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad4.put(self.txtCostHour, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad4.put(self.txtAssemblyCrit, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad4.put(self.txtPartCount, 155, y_pos)
        y_pos += 30
        self.fxdCalcResultsQuad4.put(self.txtTotalPwr, 155, y_pos)

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

        frame = _widg.make_frame(_label_=_("Reliability Results"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hbox.pack_start(frame)

        # Create quadrant 2 (upper right).
        vbox = gtk.VBox()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.fxdCalcResultsQuad2)

        frame = _widg.make_frame(_label_=_("Maintainability Results"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vbox.pack_start(frame)

        # Create quadrant 4 (lower right).
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.fxdCalcResultsQuad4)

        frame = _widg.make_frame(_label_=_("Miscellaneous Results"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vbox.pack_start(frame)

        hbox.pack_start(vbox)

        label = gtk.Label()
        _heading = _("Assessment\nResults")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays the results the reliability, maintainability, and other assessments for the selected assembly."))

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
        _heading = _("Maintenance\nPlanning")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Maintenance planning analysis for the selected assembly."))

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
            return True
        else:
            if(type_ == 0):
                _iter = self._app.HARDWARE.model.iter_parent(self._app.HARDWARE.selected_row)
                _parent = self._app.HARDWARE.model.get_string_from_iter(_iter)
                n_new_assembly = _util.add_items(_("Sibling Assembly"))
            if(type_ == 1):
                _parent = self._app.HARDWARE.model.get_string_from_iter(self._app.HARDWARE.selected_row)
                n_new_assembly = _util.add_items(_("Child Assembly"))

        for i in range(n_new_assembly):

            # Create the default description of the assembly.
            _descrip = str(_conf.RELIAFREE_PREFIX[4]) + ' ' + \
                       str(_conf.RELIAFREE_PREFIX[5])

            # Increment the assembly index.
            _conf.RELIAFREE_PREFIX[5] = _conf.RELIAFREE_PREFIX[5] + 1

            # Find the revision ID.
            if(_conf.RELIAFREE_MODULES[0] == 1):
                _revision = self._app.REVISION.revision_id
                values = (self._app.REVISION.revision_id,
                          str(_conf.RELIAFREE_PROG_INFO[3]),
                          _parent, _descrip)
            else:
                _revision = 0
                values = (0, str(_conf.RELIAFREE_PROG_INFO[3]),
                          _parent, _descrip)

            # First we add the assembly to the system table.  Next we find the
            # the ID of the newly inserted assembly.  Finally, we add this new
            # assembly to the similar item table.
            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_system \
                         (fld_revision_id, fld_entered_by, \
                          fld_parent_assembly, fld_description) \
                         VALUES (%d, '%s', '%s', '%s')"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_system \
                         (fld_revision_id, fld_entered_by, \
                          fld_parent_assembly, fld_description) \
                         VALUES (?, ?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("assembly.py: Failed to add new assembly to system table.")
                return True

            if(_conf.BACKEND == 'mysql'):
                query = "SELECT LAST_INSERT_ID()"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "SELECT seq \
                         FROM sqlite_sequence \
                         WHERE name='tbl_system'"

            assembly_id = self._app.DB.execute_query(query,
                                                     None,
                                                     self._app.ProgCnx)

            if(assembly_id == ''):
                self._app.debug_log.error("assembly.py: Failed to retrieve new assembly ID.")
                return True

            if(_conf.RELIAFREE_MODULES[0] == 1):
                values = (self._app.REVISION.revision_id,
                          assembly_id[0][0])
            else:
                values = (0, assembly_id[0][0])

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_allocation \
                         (fld_revision_id, fld_assembly_id) \
                         VALUES (%d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_allocation \
                         (fld_revision_id, fld_assembly_id) \
                         VALUES (?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("assembly.py: Failed to add new assembly to allocation table.")
                return True

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_risk_analysis \
                         (fld_revision_id, fld_assembly_id) \
                         VALUES (%d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_risk_analysis \
                         (fld_revision_id, fld_assembly_id) \
                         VALUES (?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("assembly.py: Failed to add new assembly to risk analysis table.")
                return True

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_similar_item \
                         (fld_revision_id, fld_assembly_id) \
                         VALUES (%d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_similar_item \
                         (fld_revision_id, fld_assembly_id) \
                         VALUES (?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("assembly.py: Failed to add new assembly to similar items table.")
                return True

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_functional_matrix \
                         (fld_revision_id, fld_assembly_id) \
                         VALUES(%d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_functional_matrix \
                         (fld_revision_id, fld_assembly_id) \
                         VALUES(?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
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

        values = (model.get_string_from_iter(row),)

        # First delete all of the children from the system table.
        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_system \
                     WHERE fld_parent_assembly=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_system \
                     WHERE fld_parent_assembly=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("assembly.py: Failed to delete assembly from system table.")
            return True

        if(_conf.RELIAFREE_MODULES[0] == 1):
            values = (self._app.REVISION.revision_id, model.get_value(row, 1))
        else:
            values = (0, model.get_value(row, 1))

        # Second delete the parent from the system table, then from the
        # similar item table.
        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_system \
                     WHERE fld_revision_id=%d \
                     AND fld_assembly_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_system \
                     WHERE fld_revision_id=? \
                     AND fld_assembly_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("assembly.py: Failed to delete assembly from system table.")
            return True

        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_allocation \
                     WHERE fld_revision_id=%d \
                     AND fld_assembly_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_allocation \
                     WHERE fld_revision_id=? \
                     AND fld_assembly_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("assembly.py: Failed to delete assembly from allocation table.")
            return True

        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_similar_item \
                     WHERE fld_revision_id=%d \
                     AND fld_assembly_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_similar_item \
                     WHERE fld_revision_id=? \
                     AND fld_assembly_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("assembly.py: Failed to delete assembly from similar item table.")
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
                self._app.user_log.error(_("No model dictionary for part %s") % \
                                         self.system_model.get_value(self.system_selected_row, 68))
                self._hrmodel = {}

        self._general_data_tab_load()
        self._allocation_tab_load()
        self._risk_analysis_tab_load()
        self._similar_item_tab_load()
        self._assessment_inputs_tab_load()
        self.assessment_results_tab_load()
        #self._maintenance_planning_tab_load()

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxAssembly)
        self._app.winWorkBook.show_all()

        _title_ = _("RelKit Work Bench: Analyzing %s") % \
                  self.system_model.get_value(self.system_selected_row, 17)
        self._app.winWorkBook.set_title(_title_)

        self.notebook.set_current_page(0)

        self.btnAddItem.hide()
        self.btnRemoveItem.hide()
        self.btnAnalyze.hide()
        self.btnSaveResults.hide()
        self.btnRollup.hide()
        self.btnEdit.hide()

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
            # First calculate the system falure rate and weighting factor
            # for each sub-system.
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

        model = self.tvwRisk.get_model()
        row = model.get_iter_first()

        while row is not None:
            sia = {}

            # Get the change category values.
            sia['cat1'] = model.get_value(row, 53)
            sia['cat2'] = model.get_value(row, 54)
            sia['cat3'] = model.get_value(row, 55)
            sia['cat4'] = model.get_value(row, 56)
            sia['cat5'] = model.get_value(row, 57)
            sia['cat6'] = model.get_value(row, 58)
            sia['cat7'] = model.get_value(row, 59)
            sia['cat8'] = model.get_value(row, 60)

            # Get the change cost values.
            sia['cost1'] = float(model.get_value(row, 5))
            sia['cost2'] = float(model.get_value(row, 9))
            sia['cost3'] = float(model.get_value(row, 13))
            sia['cost4'] = float(model.get_value(row, 17))
            sia['cost5'] = float(model.get_value(row, 21))
            sia['cost6'] = float(model.get_value(row, 25))
            sia['cost7'] = float(model.get_value(row, 29))
            sia['cost8'] = float(model.get_value(row, 33))

            # Get the user-defined float and integer values.
            sia['uf1'] = float(model.get_value(row, 47))
            sia['uf2'] = float(model.get_value(row, 48))
            sia['uf3'] = float(model.get_value(row, 49))
            sia['ui1'] = float(model.get_value(row, 50))
            sia['ui2'] = float(model.get_value(row, 51))
            sia['ui3'] = float(model.get_value(row, 52))

            # Get the user-defined functions.
            sia['equation1'] = model.get_value(row, 34)
            sia['equation2'] = model.get_value(row, 35)
            sia['equation3'] = model.get_value(row, 36)
            sia['equation4'] = model.get_value(row, 37)
            sia['equation5'] = model.get_value(row, 38)

            # Get the existing results.  This allows the use of the
            # results fields to be manually set to a float values by
            # the user.  Essentially creating five more user-defined
            # float values.
            sia['res1'] = model.get_value(row, 39)
            sia['res2'] = model.get_value(row, 40)
            sia['res3'] = model.get_value(row, 41)
            sia['res4'] = model.get_value(row, 42)
            sia['res5'] = model.get_value(row, 43)

            keys = sia.keys()
            values = sia.values()

            for i in range(len(keys)):
                vars()[keys[i]] = values[i]

            try:
                results1 = eval(sia['equation1'])
            except SyntaxError:
                results1 = model.get_value(row, 39)

            try:
                results2 = eval(sia['equation2'])
            except SyntaxError:
                results2 = model.get_value(row, 40)

            try:
                results3 = eval(sia['equation3'])
            except SyntaxError:
                results3 = model.get_value(row, 41)

            try:
                results4 = eval(sia['equation4'])
            except SyntaxError:
                results4 = model.get_value(row, 42)

            try:
                results5 = eval(sia['equation5'])
            except SyntaxError:
                results5 = model.get_value(row, 43)

            model.set_value(row, 39, results1)
            model.set_value(row, 40, results2)
            model.set_value(row, 41, results3)
            model.set_value(row, 42, results4)
            model.set_value(row, 43, results5)

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

            # Get the existing results.  This allows the use of the
            # results fields to be manually set to a float values by
            # the user.  Essentially creating five more user-defined
            # float values.
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

        # SAve the results.
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

        values = (model.get_value(row, 3), model.get_value(row, 4), \
                  model.get_value(row, 5), model.get_value(row, 12), \
                  model.get_value(row, 13), model.get_value(row, 8), \
                  model.get_value(row, 9), model.get_value(row, 10), \
                  model.get_value(row, 11), model.get_value(row, 21), \
                  model.get_value(row, 19), model.get_value(row, 15), \
                  model.get_value(row, 17), model.get_value(row, 0), \
                  model.get_value(row, 1))

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_allocation \
                     SET fld_included=%d, fld_n_sub_systems=%d, \
                         fld_n_sub_elements=%d, fld_weight_factor=%f, \
                         fld_percent_wt_factor=%f, fld_int_factor=%d, \
                         fld_soa_factor=%d, fld_op_time_factor=%d, \
                         fld_env_factor=%d, fld_availability_alloc=%f, \
                         fld_reliability_alloc=%f, fld_failure_rate_alloc=%f, \
                         fld_mtbf_alloc=%f \
                     WHERE fld_revision_id=%d \
                     AND fld_assembly_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_allocation \
                     SET fld_included=?, fld_n_sub_systems=?, \
                         fld_n_sub_elements=?, fld_weight_factor=?, \
                         fld_percent_wt_factor=?, fld_int_factor=?, \
                         fld_soa_factor=?, fld_op_time_factor=?, \
                         fld_env_factor=?, fld_availability_alloc=?, \
                         fld_reliability_alloc=?, fld_failure_rate_alloc=?, \
                         fld_mtbf_alloc=? \
                     WHERE fld_revision_id=? \
                     AND fld_assembly_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
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

            values = (model.get_value(row, 15), model.get_value(row, 17), \
                      measure, value, model.get_value(row, 0), \
                      model.get_value(row, 1))

            if(_conf.BACKEND == 'mysql'):
                query = "UPDATE tbl_system \
                         SET fld_failure_rate_predicted=%f, \
                             fld_mtbf_predicted=%f, \
                             fld_reliability_goal_measure=%d, \
                             fld_reliability_goal=%f \
                         WHERE fld_revision_id=%d \
                         AND fld_assembly_id=%d"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "UPDATE tbl_system \
                         SET fld_failure_rate_predicted=?, \
                             fld_mtbf_predicted=?, \
                             fld_reliability_goal_measure=?, \
                             fld_reliability_goal=? \
                         WHERE fld_revision_id=? \
                         AND fld_assembly_id=?"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

        if not results:
            self._app.debug_log.error("assembly.py: Failed to save assembly to allocation table.")
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

        dialog = _widg.make_dialog(_("RelKit - Edit Risk Analysis or Similar Item Functions"),
                                   self._app.winWorkBook)

        fixed = gtk.Fixed()

        y_pos = 10

        label = _widg.make_label(_("You can define up to five functions using the Risk Analysis or Similar Item data.  You can use the selected assembly hazard rate, change category index, the change factor, the change cost, the user float, the user integer values, and results of other functions.\n\n \
Assembly hazard rate is hr\n \
Risk category index is cat[1-8]\n \
Change factor is pi[1-8]\n \
Change cost is cost[1-8]\n \
User float is uf[1-3]\n \
User integer is ui[1-3]\n \
Function result is res[1-5]\n\n \
For example, pi1*pi2+pi3, multiplies the first change factors and adds the value to the third change factor."), 600, 350)
        fixed.put(label, 5, y_pos)
        y_pos += 260

        label = _widg.make_label(_("User function 1:"))
        txtFunction1 = _widg.make_entry()
        if(_index_ == 0):
            txtFunction1.set_text(model.get_value(row, 34))
        elif(_index_ == 1):
            txtFunction1.set_text(model.get_value(row, 19))

        fixed.put(label, 5, y_pos)
        fixed.put(txtFunction1, 195, y_pos)
        y_pos += 30

        label = _widg.make_label(_("User function 2:"))
        txtFunction2 = _widg.make_entry()
        if(_index_ == 0):
            txtFunction1.set_text(model.get_value(row, 35))
        elif(_index_ == 1):
            txtFunction2.set_text(model.get_value(row, 20))
        fixed.put(label, 5, y_pos)
        fixed.put(txtFunction2, 195, y_pos)
        y_pos += 30

        label = _widg.make_label(_("User function 3:"))
        txtFunction3 = _widg.make_entry()
        if(_index_ == 0):
            txtFunction1.set_text(model.get_value(row, 36))
        elif(_index_ == 1):
            txtFunction3.set_text(model.get_value(row, 21))
        fixed.put(label, 5, y_pos)
        fixed.put(txtFunction3, 195, y_pos)
        y_pos += 30

        label = _widg.make_label(_("User function 4:"))
        txtFunction4 = _widg.make_entry()
        if(_index_ == 0):
            txtFunction1.set_text(model.get_value(row, 37))
        elif(_index_ == 1):
            txtFunction4.set_text(model.get_value(row, 22))
        fixed.put(label, 5, y_pos)
        fixed.put(txtFunction4, 195, y_pos)
        y_pos += 30

        label = _widg.make_label(_("User function 5:"))
        txtFunction5 = _widg.make_entry()
        if(_index_ == 0):
            txtFunction1.set_text(model.get_value(row, 38))
        elif(_index_ == 1):
            txtFunction5.set_text(model.get_value(row, 23))
        fixed.put(label, 5, y_pos)
        fixed.put(txtFunction5, 195, y_pos)
        y_pos += 30

        chkApplyAll = gtk.CheckButton(label="Apply to all assemblies.")
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
                _cols = [34, 35, 36, 37, 38]
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

    def _risk_rollup(self):
        """
        Rolls-up the lower level similar item analysis change descriptions to
        the selected Assembly Object.
        """

        model = self._app.HARDWARE.model
        row = self._app.HARDWARE.selected_row
        values = (model.get_string_from_iter(row),)

        # Select all of the lower level element change descriptions for
        # the selected assembly.
        if(_conf.BACKEND == 'mysql'):
            query = "SELECT t2.fld_description, t1.fld_change_desc_1, \
                            t1.fld_change_desc_2, t1.fld_change_desc_3, \
                            t1.fld_change_desc_4, t1.fld_change_desc_5, \
                            t1.fld_change_desc_6, t1.fld_change_desc_7, \
                            t1.fld_change_desc_8 \
                     FROM tbl_risk_analysis AS t1 \
                     INNER JOIN tbl_system AS t2 \
                     ON t1.fld_assembly_id=t2.fld_assembly_id \
                     WHERE t2.fld_parent_assembly='%s'"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT t2.fld_description, t1.fld_change_desc_1, \
                            t1.fld_change_desc_2, t1.fld_change_desc_3, \
                            t1.fld_change_desc_4, t1.fld_change_desc_5, \
                            t1.fld_change_desc_6, t1.fld_change_desc_7, \
                            t1.fld_change_desc_8 \
                     FROM tbl_risk_analysis AS t1 \
                     INNER JOIN tbl_system AS t2 \
                     ON t1.fld_assembly_id=t2.fld_assembly_id \
                     WHERE t2.fld_parent_assembly=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        # Combine the changes descriptions into a single change description
        # for each change category.
        summary = ["", "", "", "", "", "", "", ""]
        for i in range(len(results)):
            system = results[i][0]
            for j in range(8):
                if(results[i][j+1] != '' and results[i][j+1] is not None):
                    summary[j] = summary[j] + system + ":\n" + \
                                 results[i][j+1] + "\n"

        # Now find the sums of the five result fields.
        if(_conf.BACKEND == 'mysql'):
            query = "SELECT SUM(t1.fld_result_1), SUM(t1.fld_result_2), \
                            SUM(t1.fld_result_3), SUM(t1.fld_result_4), \
                            SUM(t1.fld_result_5) \
                     FROM tbl_risk_analysis AS t1 \
                     INNER JOIN tbl_system AS t2 \
                     ON t1.fld_assembly_id=t2.fld_assembly_id \
                     WHERE t2.fld_parent_assembly='%s'"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT SUM(t1.fld_result_1), SUM(t1.fld_result_2), \
                            SUM(t1.fld_result_3), SUM(t1.fld_result_4), \
                            SUM(t1.fld_result_5) \
                     FROM tbl_risk_analysis AS t1 \
                     INNER JOIN tbl_system AS t2 \
                     ON t1.fld_assembly_id=t2.fld_assembly_id \
                     WHERE t2.fld_parent_assembly=?"

        sums = self._app.DB.execute_query(query,
                                          values,
                                          self._app.ProgCnx)

        # Update the selected assembly's change descriptions with the combined
        # change description.
        if(_conf.RELIAFREE_MODULES[0] == 1):
            values = (summary[0], summary[1], summary[2], summary[3], \
                      summary[4], summary[5], summary[6], summary[7], \
                      sums[0][0], sums[0][1], sums[0][2], sums[0][3], \
                      sums[0][4], \
                      self._app.REVISION.revision_id, self.assembly_id)
        else:
            values = (summary[0], summary[1], summary[2], summary[3], \
                      summary[4], summary[5], summary[6], summary[7], \
                      sums[0][0], sums[0][1], sums[0][2], sums[0][3], \
                      sums[0][4], 0, self.assembly_id)

        # Update the database.
        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_risk_analysis \
                     SET fld_change_desc_1='%s', fld_change_desc_2='%s', \
                         fld_change_desc_3='%s', fld_change_desc_4='%s', \
                         fld_change_desc_5='%s', fld_change_desc_6='%s', \
                         fld_change_desc_7='%s', fld_change_desc_8='%s', \
                         fld_result_1=%d, fld_result_2=%d, \
                         fld_result_3=%d, fld_result_4=%d, \
                         fld_result_5=%d \
                     WHERE fld_revision_id=%d AND fld_assembly_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_risk_analysis \
                     SET fld_change_desc_1=?, fld_change_desc_2=?, \
                         fld_change_desc_3=?, fld_change_desc_4=?, \
                         fld_change_desc_5=?, fld_change_desc_6=?, \
                         fld_change_desc_7=?, fld_change_desc_8=?, \
                         fld_result_1=?, fld_result_2=?, \
                         fld_result_3=?, fld_result_4=?, \
                         fld_result_5=? \
                     WHERE fld_revision_id=? AND fld_assembly_id=?"

        self._app.DB.execute_query(query,
                                   values,
                                   self._app.ProgCnx,
                                   commit=True)

        return False

    def _risk_save(self):
        """
        Saves the Assembly Object risk analysis gtk.TreeView
        information to the Program's MySQL or SQLite3 database.
        """

        model = self.tvwRisk.get_model()
        model.foreach(self._risk_save_line_item)

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
            equation1 = self._app.ProgCnx.escape_string(model.get_value(row, self._risk_col_order[34]))
            equation2 = self._app.ProgCnx.escape_string(model.get_value(row, self._risk_col_order[35]))
            equation3 = self._app.ProgCnx.escape_string(model.get_value(row, self._risk_col_order[36]))
            equation4 = self._app.ProgCnx.escape_string(model.get_value(row, self._risk_col_order[37]))
            equation5 = self._app.ProgCnx.escape_string(model.get_value(row, self._risk_col_order[38]))

        elif(_conf.BACKEND == 'sqlite3'):
            equation1 = model.get_value(row, self._risk_col_order[34])
            equation2 = model.get_value(row, self._risk_col_order[35])
            equation3 = model.get_value(row, self._risk_col_order[36])
            equation4 = model.get_value(row, self._risk_col_order[37])
            equation5 = model.get_value(row, self._risk_col_order[38])

        values = (model.get_value(row, self._risk_col_order[2]), \
                  model.get_value(row, self._risk_col_order[3]), \
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
                  model.get_value(row, self._risk_col_order[22]), \
                  model.get_value(row, self._risk_col_order[23]), \
                  model.get_value(row, self._risk_col_order[24]), \
                  model.get_value(row, self._risk_col_order[25]), \
                  model.get_value(row, self._risk_col_order[26]), \
                  model.get_value(row, self._risk_col_order[27]), \
                  model.get_value(row, self._risk_col_order[28]), \
                  model.get_value(row, self._risk_col_order[29]), \
                  model.get_value(row, self._risk_col_order[30]), \
                  model.get_value(row, self._risk_col_order[31]), \
                  model.get_value(row, self._risk_col_order[32]), \
                  model.get_value(row, self._risk_col_order[33]), \
                  equation1, \
                  equation2, \
                  equation3, \
                  equation4, \
                  equation5, \
                  model.get_value(row, self._risk_col_order[39]), \
                  model.get_value(row, self._risk_col_order[40]), \
                  model.get_value(row, self._risk_col_order[41]), \
                  model.get_value(row, self._risk_col_order[42]), \
                  model.get_value(row, self._risk_col_order[43]), \
                  model.get_value(row, self._risk_col_order[44]), \
                  model.get_value(row, self._risk_col_order[45]), \
                  model.get_value(row, self._risk_col_order[46]), \
                  model.get_value(row, self._risk_col_order[47]), \
                  model.get_value(row, self._risk_col_order[48]), \
                  model.get_value(row, self._risk_col_order[49]), \
                  model.get_value(row, self._risk_col_order[50]), \
                  model.get_value(row, self._risk_col_order[51]), \
                  model.get_value(row, self._risk_col_order[52]), \
                  model.get_value(row, 53), \
                  model.get_value(row, 54), \
                  model.get_value(row, 55), \
                  model.get_value(row, 56), \
                  model.get_value(row, 57), \
                  model.get_value(row, 58), \
                  model.get_value(row, 59), \
                  model.get_value(row, 60), \
                  self._app.REVISION.revision_id, \
                  model.get_value(row, self._risk_col_order[0]))

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_risk_analysis \
                     SET fld_change_desc_1='%s', fld_change_category_1=%d, \
                         fld_change_effort_1=%f, fld_change_cost_1=%f, \
                         fld_change_desc_2='%s', fld_change_category_2=%d, \
                         fld_change_effort_2=%f, fld_change_cost_2=%f, \
                         fld_change_desc_3='%s', fld_change_category_3=%d, \
                         fld_change_effort_3=%f, fld_change_cost_3=%f, \
                         fld_change_desc_4='%s', fld_change_category_4=%d, \
                         fld_change_effort_4=%f, fld_change_cost_4=%f, \
                         fld_change_desc_5='%s', fld_change_category_5=%d, \
                         fld_change_effort_5=%f, fld_change_cost_5=%f, \
                         fld_change_desc_6='%s', fld_change_category_6=%d, \
                         fld_change_effort_6=%f, fld_change_cost_6=%f, \
                         fld_change_desc_7='%s', fld_change_category_7=%d, \
                         fld_change_effort_7=%f, fld_change_cost_7=%f, \
                         fld_change_desc_8='%s', fld_change_category_8=%d, \
                         fld_change_effort_8=%f, fld_change_cost_8=%f, \
                         fld_function_1='%s', fld_function_2='%s', \
                         fld_function_3='%s', fld_function_4='%s', \
                         fld_function_5='%s', \
                         fld_result_1=%f, fld_result_2=%f, fld_result_3=%f, \
                         fld_result_4=%f, fld_result_5=%f, \
                         fld_user_blob_1='%s', fld_user_blob_2='%s', \
                         fld_user_blob_3='%s', fld_user_float_1=%f, \
                         fld_user_float_2=%f, fld_user_float_3=%f, \
                         fld_user_int_1=%d, fld_user_int_2=%d, \
                         fld_user_int_3=%d, \
                         fld_category_value_1=%d, fld_category_value_2=%d, \
                         fld_category_value_3=%d, fld_category_value_4=%d, \
                         fld_category_value_5=%d, fld_category_value_6=%d, \
                         fld_category_value_7=%d, fld_category_value_8=%d \
                     WHERE fld_revision_id=%d \
                     AND fld_risk_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_risk_analysis \
                     SET fld_change_desc_1=?, fld_change_category_1=?, \
                         fld_change_effort_1=?, fld_change_cost_1=?, \
                         fld_change_desc_2=?, fld_change_category_2=?, \
                         fld_change_effort_2=?, fld_change_cost_2=?, \
                         fld_change_desc_3=?, fld_change_category_3=?, \
                         fld_change_effort_3=?, fld_change_cost_3=?, \
                         fld_change_desc_4=?, fld_change_category_4=?, \
                         fld_change_effort_4=?, fld_change_cost_4=?, \
                         fld_change_desc_5=?, fld_change_category_5=?, \
                         fld_change_effort_5=?, fld_change_cost_5=?, \
                         fld_change_desc_6=?, fld_change_category_6=?, \
                         fld_change_effort_6=?, fld_change_cost_6=?, \
                         fld_change_desc_7=?, fld_change_category_7=?, \
                         fld_change_effort_7=?, fld_change_cost_7=?, \
                         fld_change_desc_8=?, fld_change_category_8=?, \
                         fld_change_effort_8=?, fld_change_cost_8=?, \
                         fld_function_1=?, fld_function_2=?, \
                         fld_function_3=?, fld_function_4=?, \
                         fld_function_5=?, \
                         fld_result_1=?, fld_result_2=?, fld_result_3=?, \
                         fld_result_4=?, fld_result_5=?, \
                         fld_user_blob_1=?, fld_user_blob_2=?, \
                         fld_user_blob_3=?, fld_user_float_1=?, \
                         fld_user_float_2=?, fld_user_float_3=?, \
                         fld_user_int_1=?, fld_user_int_2=?, \
                         fld_user_int_3=?, \
                         fld_category_value_1=?, fld_category_value_2=?, \
                         fld_category_value_3=?, fld_category_value_4=?, \
                         fld_category_value_5=?, fld_category_value_6=?, \
                         fld_category_value_7=?, fld_category_value_8=? \
                     WHERE fld_revision_id=? \
                     AND fld_risk_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("assembly.py: Failed to save assembly to risk analysis table.")
            return True

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
            equation1 = self._app.ProgCnx.escape_string(model.get_value(row, self._sia_col_order[19]))
            equation2 = self._app.ProgCnx.escape_string(model.get_value(row, self._sia_col_order[20]))
            equation3 = self._app.ProgCnx.escape_string(model.get_value(row, self._sia_col_order[21]))
            equation4 = self._app.ProgCnx.escape_string(model.get_value(row, self._sia_col_order[22]))
            equation5 = self._app.ProgCnx.escape_string(model.get_value(row, self._sia_col_order[23]))

        elif(_conf.BACKEND == 'sqlite3'):
            equation1 = model.get_value(row, self._sia_col_order[19])
            equation2 = model.get_value(row, self._sia_col_order[20])
            equation3 = model.get_value(row, self._sia_col_order[21])
            equation4 = model.get_value(row, self._sia_col_order[22])
            equation5 = model.get_value(row, self._sia_col_order[23])

        values = (model.get_value(row, self._sia_col_order[3]), \
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

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_similar_item \
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
                     AND fld_sia_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_similar_item \
                     SET fld_change_desc_1=?, fld_change_factor_1=?, \
                         fld_change_desc_2=?, fld_change_factor_2=?, \
                         fld_change_desc_3=?, fld_change_factor_3=?, \
                         fld_change_desc_4=?, fld_change_factor_4=?, \
                         fld_change_desc_5=?, fld_change_factor_5=?, \
                         fld_change_desc_6=?, fld_change_factor_6=?, \
                         fld_change_desc_7=?, fld_change_factor_7=?, \
                         fld_change_desc_8=?, fld_change_factor_8=?, \
                         fld_function_1=?, fld_function_2=?, \
                         fld_function_3=?, fld_function_4=?, \
                         fld_function_5=?, \
                         fld_result_1=?, fld_result_2=?, fld_result_3=?, \
                         fld_result_4=?, fld_result_5=?, \
                         fld_user_blob_1=?, fld_user_blob_2=?, \
                         fld_user_blob_3=?, fld_user_float_1=?, \
                         fld_user_float_2=?, fld_user_float_3=?, \
                         fld_user_int_1=?, fld_user_int_2=?, \
                         fld_user_int_3=? \
                     WHERE fld_revision_id=? \
                     AND fld_sia_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("assembly.py: Failed to save assembly to similar item table.")
            return True

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
        val = model.get_value(row, 1)

        treerow = treemodel.get_iter(path)
        treecol = int(position / 5) + lastcol

        treemodel.set_value(treerow, treecol, val)

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
                    _title_ = _("RelKit Information")

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

        # Reliability allocation method combo box called this function.
        # Hide/show the appropriate columns in the Allocation gtk.TreeView.
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

        from datetime import datetime

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        if(convert == 'text'):
            if(index_ == 71):
                textbuffer = self.txtRemarks.get_child().get_child().get_buffer()
                text_ = textbuffer.get_text(*textbuffer.get_bounds())
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
             index_ < 400):                # Action entries
            _index_ = index_ - 300
            if(_index_ == 1):
                _text_ = self.txtActionPrescribed.get_text(*self.txtActionPrescribed.get_bounds())
            elif(_index_ == 5):
                _text_ = self.txtActionTaken.get_text(*self.txtActionTaken.get_bounds())

            selection = self.tvwActionList.get_selection()
            (model, row) = selection.get_selected()
            model.set_value(row, _index_, _text_)

        elif(index_ >= 500):                # Allocation goals.
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

        return False

    def _callback_check(self, check, index_):
        """
        Callback function to retrieve and save checkbutton changes.

        Keyword Arguments:
        check  -- the checkbutton that called the function.
        index_ -- the position in the Assembly Object _attribute list
                  associated with the data from the calling checkbutton.
        """

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
                    2 = Similar Items Analysis
                    3 = Assessment Inputs
                    4 = Assessment Results
                    4 = FMEA
                    5 = Maintenance Planning
                    6 = Reliability Growth Planning
        """

        if(page_num == 1):                  # Allocation tab
            self.btnAddItem.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.hide()
            self.btnEdit.hide()
            self.btnAnalyze.set_tooltip_text(_("Allocates the reliability to the child assemblies/parts."))
            self.btnSaveResults.set_tooltip_text(_("Saves the allocation results for the selected assembly."))
        elif(page_num == 2):                # Risk analysis tab
            self.btnAddItem.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.show()
            self.btnSaveResults.show()
            self.btnRollup.show()
            self.btnEdit.show()
            self.btnAnalyze.set_tooltip_text(_("Performs a risk analysis of changes to the selected assembly."))
            self.btnSaveResults.set_tooltip_text(_("Saves the risk analysis results for the selected assembly."))
            self.btnRollup.set_tooltip_text(_("Summarizes the lower level risk analyses."))
            self.btnEdit.set_tooltip_text(_("Create/edit current risk analysis functions."))
        elif(page_num == 3):                # Similar items tab
            self.btnAddItem.hide()
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
            self.btnAddItem.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.show()
            self.btnSaveResults.hide()
            self.btnRollup.hide()
            self.btnEdit.hide()
            self.btnAnalyze.set_tooltip_text(_("Calculate the hardware metrics in the open RelKit Program Database."))
        elif(page_num == 5):                # Assessment results tab
            self.btnAddItem.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.hide()
            self.btnSaveResults.hide()
            self.btnRollup.hide()
            self.btnEdit.hide()
        elif(page_num == 6):                # FMEA/FMECA tab
            self.btnAddItem.show()
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
            self.btnAddItem.show()
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
            self.btnAddItem.show()
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

        if(_page_ == 1):                    # Allocation tab.
            if(_button_ == 'Analyze'):
                self._allocate()
            elif(_button_ == 'Save'):
                self._allocation_save()
        elif(_page_ == 2):                  # Risk analysis tab.
            if(_button_ == 'Analyze'):
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
            if(_button_ == 'Analyze'):
                _calc.calculate_project(widget, self._app, 3)
        elif(_page_ == 6):                  # FMEA/FMECA tab.
            if(_button_ == 'Add'):
                print "Add mode/mechanism/cause"
            elif(_button_ == 'Analyze'):
                print "Criticality calculations"
            elif(_button_ == 'Save'):
                print "Saving FMECA"
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
