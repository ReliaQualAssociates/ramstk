#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to the
hardware components of the Program.
"""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       component.py is part of The RelKit Project
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

# Modules required for plotting.
import matplotlib
matplotlib.use('GTK')
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure

# Import other RelKit modules.
import calculations as _calc
import configuration as _conf
import utilities as _util
import widgets as _widg

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

import gettext
_ = gettext.gettext


class Component():
    """
    The Components class is used to represent a component in a system being
    analyzed.
    """

    _gd_tab_labels = [[_("Assembly Name:"), _("Part Number:"),
                       _("Alternate Part #:"), _("Category:"),
                       _("Subcategory:"), _("Ref Designator:"),
                       _("Composite Ref Des:"), _("Quantity:"),
                       _("Description:")],
                      [_("Specification:"), _("Page Number:"),
                       _("Figure Number:"), _("Image File:"),
                       _("Attachments:"), _("Mission Time:")],
                      [_("Manufacturer:"), _("CAGE Code:"), _("LCN:"),
                       _("NSN:"), _("Manufacture Year:")],
                      [_("Revision ID:"), _("Repairable?"), _("Tagged?"),
                       _("Remarks:")]]
    _ai_tab_labels = [[_("h(t) Type:"), _("Calculation Model:"),
                       _("Specified h(t):"), _("Specified MTBF:"),
                       _("Software h(t):"), _("Additive Adjustment:"),
                       _("Multiplicative Adjustment:"),
                       _("Allocation Wt Factor:"),
                       _("Failure Distribution:"), _("Scale:"), _("Shape:"),
                       _("Location:")],
                      [_("Burn-In Temp:"), _("Burn-In Time:"),
                       _("# of Lab Devices:"), _("Lab Test Time:"),
                       _("Lab Test Temp:"), _("# of Lab Failures:"),
                       _("Field Op Time:"), _("# of Field Failures:")],
                      [],
                      [_("Min Rated Temp:"), _("Knee Temp:"),
                       _("Max Rated Temp:"), _("Rated Voltage:"),
                       _("Operating Voltage:"), _("Rated Current:"),
                       _("Operating Current:"), _("Rated Power:"),
                       _("Operating Power:"), _("theta JC:"),
                       _("Temperature Rise:"), _("Case Temperature:"),
                       _("Unit Cost:")]]
    _ar_tab_labels = [[_("Active h(t):"), _("Dormant h(t):"),
                       _("Software h(t):"), _("Predicted h(t):"),
                       _("Mission h(t):"), _("h(t) %:"), _("MTBF:"),
                       _("Mission MTBF:"), _("Reliability:"),
                       _("Mission R(t):")],
                      [_("MPMT:"), _("MCMT:"), _("MTTR:"), _("MMT:"),
                       _("Availability:"),
                       _("Mission A(t):")],
                      [],
                      [_("Total Cost:"), _("Cost/Failure:"), _("Cost/Hour:"),
                       _("Assembly Criticality:"), _("Total Part Count:"),
                       _("Total Power Used:"), _("Voltage Ratio:"),
                       _("Current Ratio:"),
                       _("Power Ratio:"), _("Overstressed?:")]]
    _fm_tab_labels = []
    _dv_tab_labels = []
    _ca_tab_labels = []

    def __init__(self, application):
        """
        Initializes the Component Object.

        Keyword Arguments:
        application -- the RelKit application.
        """

        self.fmt = _conf.PLACES

        self._ready = False

        self._app = application

        self.system_model = self._app.HARDWARE.model
        self.system_selected_row = self._app.HARDWARE.selected_row

        self.model = None
        self.selected_row = None
        self.part = None

        self._category = 0
        self._subcategory = 0
        self._mode_id = 0

        self._hrmodel = {}

        self._FMECA = None
        self._fmeca_col_order = []

        self.y_pos = [[5, 5, 5], [5, 5, 5]]

# Create the Notebook for the COMPONENT object.
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

# Create generic toolbar action buttons.  These will call different methods or
# functions depending on the COMPONENT Object notebook tab that is selected.
        self.btnAddItem = gtk.ToolButton(stock_id=gtk.STOCK_ADD)
        self.btnRemoveItem = gtk.ToolButton(stock_id=gtk.STOCK_REMOVE)
        self.btnAnalyze = gtk.ToolButton(stock_id=gtk.STOCK_NO)
        self.btnSaveResults = gtk.ToolButton(stock_id=gtk.STOCK_SAVE)
        self.btnRollup = gtk.ToolButton(stock_id=gtk.STOCK_NO)
        self.btnEdit = gtk.ToolButton(stock_id=gtk.STOCK_EDIT)

# Create the General Data tab widgets for the COMPONENT object.
        self.txtName = _widg.make_entry()
        self.txtPartNum = _widg.make_entry()
        self.txtAltPartNum = _widg.make_entry()
        self.cmbCategory = _widg.make_combo(simple=False)
        self.cmbSubcategory = _widg.make_combo(simple=False)
        self.txtRefDes = _widg.make_entry()
        self.txtCompRefDes = _widg.make_entry()
        self.txtQuantity = _widg.make_entry()
        self.txtDescription = _widg.make_entry()
        self.cmbManufacturer = _widg.make_combo(simple=False)
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
        self.txtRevisionID = _widg.make_entry(_width_=50, editable=False)
        self.chkRepairable = _widg.make_check_button()
        self.chkTagged = _widg.make_check_button()
        self.txtRemarks = _widg.make_text_view(width=400)
        if self._general_data_widgets_create():
            self._app.debug_log.error("component.py: Failed to create General Data tab widgets.")
        if self._general_data_tab_create():
            self._app.debug_log.error("component.py: Failed to update General Data tab.")

# Create the Assessment Input tab widgets for the COMPONENT object.
        self.lblNoCategory = _widg.make_label(_("No category selected for this part."),
                                              width=400)
        self.lblNoSubCategory = _widg.make_label(_("No subcategory selected for this part."),
                                                 width=400)

# Create the FMECA tab widgets for the COMPONENT object.

        self.vbxComponent = gtk.VBox()
        toolbar = self._toolbar_create()

        self.vbxComponent.pack_start(toolbar, expand=False)
        self.vbxComponent.pack_start(self.notebook)

        self._ready = True

    def _toolbar_create(self):
        """ Method to create the toolbar for the Assembly Object work book. """

        toolbar = gtk.Toolbar()

        # Add item button.  Depending on the notebook page selected will
        # determine what type of item is added.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        self.btnAddItem.set_icon_widget(image)
        self.btnAddItem.set_name('Add')
        self.btnAddItem.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnAddItem, 0)

        # Remove item button.  Depending on the notebook page selected will
        # determine what type of item is removed.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        self.btnRemoveItem.set_icon_widget(image)
        self.btnRemoveItem.set_name('Remove')
        self.btnRemoveItem.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnRemoveItem, 1)

        toolbar.insert(gtk.SeparatorToolItem(), 2)

        # Perform analysis button.  Depending on the notebook page selected
        # will determine which analysis is executed.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        self.btnAnalyze.set_icon_widget(image)
        self.btnAnalyze.set_name('Analyze')
        self.btnAnalyze.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnAnalyze, 3)

        # Save results button.  Depending on the notebook page selected will
        # determine which results are saved.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        self.btnSaveResults.set_icon_widget(image)
        self.btnSaveResults.set_name('Save')
        self.btnSaveResults.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnSaveResults, 4)

        toolbar.show()

        return(toolbar)

    def _general_data_widgets_create(self):
        """
        Method to add the additional Component widgets to the General Data tab.
        """

        # Quadrant 1 (upper left) widgets.  These widgets are used to
        # display general information about the selected component.
        self.txtName.set_tooltip_text(_("Enter the name of the selected component."))
        self.txtName.connect('focus-out-event',
                             self._callback_entry, 'text', 558)

        self.txtPartNum.set_tooltip_text(_("Enter the part number of the selected component."))
        self.txtPartNum.connect('focus-out-event',
                                self._callback_entry, 'text', 564)

        self.txtAltPartNum.set_tooltip_text(_("Enter an alternative part number for the selected component."))
        self.txtAltPartNum.connect('focus-out-event',
                                   self._callback_entry, 'text', 504)

        self.cmbCategory.set_tooltip_text(_("Select the type of this component."))
        self.cmbCategory.connect('changed', self._callback_combo, 511)

        query = "SELECT * FROM tbl_category \
                 ORDER BY fld_category_noun ASC"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        model = self.cmbCategory.get_model()
        model.clear()
        model.append(None, ['', 0, ''])
        for i in range(len(results)):
            model.append(None, [results[i][1], results[i][0], ''])

        self.cmbSubcategory.set_tooltip_text(_("Select the sub-type of this component."))
        self.cmbSubcategory.connect('changed', self._callback_combo, 578)

        self.txtRefDes.connect('focus-out-event',
                               self._callback_entry, 'text', 568)

        self.txtCompRefDes.set_tooltip_text(_("Enter the composite reference designator of the selected component."))
        self.txtCompRefDes.connect('focus-out-event',
                                   self._callback_entry, 'text', 512)

        self.txtQuantity.set_tooltip_text(_("Enter the quantity of the selected component."))
        self.txtQuantity.connect('focus-out-event',
                                 self._callback_entry, 'int', 567)

        self.txtDescription.set_tooltip_text(_("Enter a description for the selected component."))
        self.txtDescription.connect('focus-out-event',
                                    self._callback_entry, 'text', 517)

        # Quadrant 2 (upper right) widgets.  These widgets are used to
        # display logistics information about the selected assembly.
        self.cmbManufacturer.set_tooltip_text(_("Select the manufacturer of the selected assembly or component."))
        self.cmbManufacturer.connect('changed',
                                     self._callback_combo, 543)

        query = "SELECT fld_manufacturers_noun, fld_location, fld_cage_code \
                 FROM tbl_manufacturers \
                 ORDER BY fld_manufacturers_noun ASC"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbManufacturer, results, False)

        self.txtCAGECode.set_tooltip_text(_("Enter the Commercial and Government Entity (CAGE) code of the selected component."))
        self.txtCAGECode.connect('focus-out-event',
                                 self._callback_entry, 'text', 509)

        self.txtLCN.set_tooltip_text(_("Enter the logistics control number (LCN) of the selected component."))
        self.txtLCN.connect('focus-out-event',
                            self._callback_entry, 'text', 541)

        self.txtNSN.set_tooltip_text(_("Enter the national stock number (NSN) of the selected component."))
        self.txtNSN.connect('focus-out-event',
                            self._callback_entry, 'text', 559)

        self.txtYearMade.set_tooltip_text(_("Enter the year the selected component was manufactured."))
        self.txtYearMade.connect('focus-out-event',
                                 self._callback_entry, 'int', 587)

        # Quadrant 3 (lower left) widgets.  These widget are used to
        # display requirements information about the selected assembly.
        self.txtSpecification.set_tooltip_text(_("Enter the governing specification for the selected component, if any."))
        self.txtSpecification.connect('focus-out-event',
                                      self._callback_entry, 'text', 577)

        self.txtPageNum.set_tooltip_text(_("Enter the governing specification page number for the selected component."))
        self.txtPageNum.connect('focus-out-event',
                                self._callback_entry, 'text', 561)

        self.txtFigNum.set_tooltip_text(_("Enter the governing specification figure number for the selected component."))
        self.txtFigNum.connect('focus-out-event',
                               self._callback_entry, 'text', 536)

        self.txtImageFile.set_tooltip_text(_("Enter the URL to an image of the selected component."))
        self.txtImageFile.connect('focus-out-event',
                                  self._callback_entry, 'text', 538)

        self.txtAttachments.set_tooltip_text(_("Enter the URL to an attachment associated with the selected component."))
        self.txtAttachments.connect('focus-out-event',
                                    self._callback_entry, 'text', 506)

        self.txtMissionTime.set_tooltip_text(_("Enter the mission time for the selected component."))
        self.txtMissionTime.connect('focus-out-event',
                                    self._callback_entry, 'float', 545)

        # Quadrant 4 (lower right) widgets.  These widgets are used to
        # display miscellaneous information about the selected assembly.
        self.txtRevisionID.set_tooltip_text(_("Displays the currently selected revision."))

        self.chkRepairable.set_tooltip_text(_("Indicates whether or not the selected component is repairable."))
        self.chkRepairable.connect('toggled',
                                   self._callback_check, 575)

        self.chkTagged.set_tooltip_text(_("Indicates whether or not the selected component is tagged."))
        self.chkTagged.connect('toggled',
                               self._callback_check, 579)

        self.txtRemarks.set_tooltip_text(_("Enter any remarks associated with the selected component."))
        self.txtRemarks.get_child().get_child().connect('focus-out-event',
                                                        self._callback_entry,
                                                        'text', 71)

        return False

    def _general_data_tab_create(self):
        """
        Method to create the General Data gtk.Notebook tab and populate it
        with the appropriate widgets.
        """

        hbox = gtk.HBox()

        # Populate quadrant 1 (upper left).
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("General Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned = gtk.VPaned()

        vpaned.pack1(frame, True, True)

        y_pos = 5
        for i in range(len(self._gd_tab_labels[0])):
            label = _widg.make_label(self._gd_tab_labels[0][i], 150, 25)
            fixed.put(label, 5, (30 * i + y_pos))

        fixed.put(self.txtName, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtPartNum, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtAltPartNum, 155, y_pos)
        y_pos += 30
        fixed.put(self.cmbCategory, 155, y_pos)
        y_pos += 35
        fixed.put(self.cmbSubcategory, 155, y_pos)
        y_pos += 35
        fixed.put(self.txtRefDes, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtCompRefDes, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtQuantity, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtDescription, 155, y_pos)

        fixed.show_all()

        # Populate quadrant 2 (upper right).
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Logistics Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned.pack2(frame, True, True)

        hbox.pack_start(vpaned)

        y_pos = 5
        for i in range(len(self._gd_tab_labels[2])):
            label = _widg.make_label(self._gd_tab_labels[2][i], 150, 25)
            fixed.put(label, 5, (30 * i + y_pos))

        fixed.put(self.cmbManufacturer, 155, y_pos)
        y_pos += 35
        fixed.put(self.txtCAGECode, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtLCN, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtNSN, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtYearMade, 155, y_pos)

        fixed.show_all()

        # Populate quadrant 3 (lower left).
        vpaned = gtk.VPaned()

        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Requirements Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned.pack1(frame, True, True)

        y_pos = 5
        for i in range(len(self._gd_tab_labels[1])):
            label = _widg.make_label(self._gd_tab_labels[1][i], 150, 25)
            fixed.put(label, 5, (30 * i + y_pos))

        fixed.put(self.txtSpecification, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtPageNum, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtFigNum, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtImageFile, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtAttachments, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMissionTime, 155, y_pos)

        fixed.show_all()

        # Populate quadrant 4 (lower right).
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Miscellaneous Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned.pack2(frame, True, True)

        hbox.pack_start(vpaned)

        y_pos = 5
        for i in range(len(self._gd_tab_labels[3])):
            label = _widg.make_label(self._gd_tab_labels[3][i], 150, 25)
            fixed.put(label, 5, (30 * i + y_pos))

        fixed.put(self.txtRevisionID, 155, y_pos)
        y_pos += 30
        fixed.put(self.chkRepairable, 155, y_pos)
        y_pos += 30
        fixed.put(self.chkTagged, 155, y_pos)
        y_pos += 30

        fixed.put(self.txtRemarks, 155, y_pos)

        fixed.show_all()

        # Insert the tab.
        label = gtk.Label()
        _heading = _("General\nData")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays general information about the selected component."))

        self.notebook.insert_page(hbox,
                                  tab_label=label,
                                  position=-1)

        return False

    def _general_data_tab_load(self):
        """
        Loads the widgets with general information about the Component Object.
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
        if treemodel.get_value(row, 71) is None:
            self.txtRemarks.set_text("")
        else:
            self.txtRemarks.set_text(treemodel.get_value(row, 71))
        self.chkRepairable.set_active(treemodel.get_value(row, 75))
        self.txtSpecification.set_text(treemodel.get_value(row, 77))
        self.chkTagged.set_active(treemodel.get_value(row, 79))
        self.txtYearMade.set_text(str(treemodel.get_value(row, 87)))
        self.cmbCategory.set_active(treemodel.get_value(row, 11))
        self.cmbSubcategory.set_active(treemodel.get_value(row, 78))

        self._category = self._app.HARDWARE.model.get_value(self._app.HARDWARE.selected_row, 11)
        self._subcategory = self._app.HARDWARE.model.get_value(self._app.HARDWARE.selected_row, 78)

        return False

    def _assessment_inputs_widgets_create(self):
        """ Method to create the Assessment Inputs widgets. """

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
        self.txtWeibullFile = _widg.make_entry()
        self.txtCost = _widg.make_entry()
        self.txtBurnInTemp = _widg.make_entry()
        self.txtBurnInTime = _widg.make_entry()
        self.txtLabDevices = _widg.make_entry()
        self.txtLabTime = _widg.make_entry()
        self.txtLabTemp = _widg.make_entry()
        self.txtLabFailures = _widg.make_entry()
        self.txtFieldTime = _widg.make_entry()
        self.txtFieldFailures = _widg.make_entry()
        self.txtMinTemp = _widg.make_entry()
        self.txtKneeTemp = _widg.make_entry()
        self.txtMaxTemp = _widg.make_entry()
        self.txtRatedVoltage = _widg.make_entry()
        self.txtOpVoltage = _widg.make_entry()
        self.txtRatedCurrent = _widg.make_entry()
        self.txtOpCurrent = _widg.make_entry()
        self.txtRatedPower = _widg.make_entry()
        self.txtOpPower = _widg.make_entry()
        self.txtThetaJC = _widg.make_entry()
        self.txtTempRise = _widg.make_entry()
        self.txtCaseTemp = _widg.make_entry()

        # Quadrant 1 (upper left) widgets.  These widgets are used to
        # display reliability assessment inputs.
        self.cmbHRType.set_tooltip_text(_("Select the method of assessing the failure intensity for the selected component."))

        query = "SELECT fld_hr_type_noun FROM tbl_hr_type"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbHRType, results)
        self.cmbHRType.connect('changed', self._callback_combo, 535)

        self.cmbCalcModel.set_tooltip_text(_("Select the reliability prediction model for the selected component."))

        query = "SELECT fld_model_noun FROM tbl_calculation_model"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbCalcModel, results)
        self.cmbCalcModel.connect('changed', self._callback_combo, 510)

        self.txtSpecifiedHt.set_tooltip_text(_("Enter the specified failure intensity for the selected component."))
        self.txtSpecifiedHt.connect('focus-out-event',
                                    self._callback_entry, 'float', 534)

        self.txtSpecifiedMTBF.set_tooltip_text(_("Enter the specified mean time between failure (MTBF) for the selected component."))
        self.txtSpecifiedMTBF.connect('focus-out-event',
                                      self._callback_entry, 'float', 551)

        self.txtSoftwareHt.set_tooltip_text(_("Enter the software failure rate for the selected component."))
        self.txtSoftwareHt.connect('focus-out-event',
                                   self._callback_entry, 'float', 533)

        self.txtAddAdj.set_tooltip_text(_("Enter any reliability assessment additive adjustment factor for the selected component."))
        self.txtAddAdj.connect('focus-out-event',
                               self._callback_entry, 'float', 502)

        self.txtMultAdj.set_tooltip_text(_("Enter any reliability assessment multiplicative adjustment factor for the selected component."))
        self.txtMultAdj.connect('focus-out-event',
                                self._callback_entry, 'float', 557)

        self.txtAllocationWF.set_tooltip_text(_("Enter the reliability allocation weighting factor for the selected component."))
        self.txtAllocationWF.connect('focus-out-event',
                                     self._callback_entry, 'float', 503)

        self.cmbFailDist.set_tooltip_text(_("Select the distribution of times to failure for the selected component."))

        query = "SELECT fld_distribution_noun \
                 FROM tbl_distributions"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbFailDist, results)
        self.cmbFailDist.connect('changed', self._callback_combo, 524)

        self.txtFailScale.set_tooltip_text(_("Enter the time to failure distribution scale factor."))
        self.txtFailScale.connect('focus-out-event',
                                  self._callback_entry, 'float', 525)

        self.txtFailShape.set_tooltip_text(_("Enter the time to failure distribution shape factor."))
        self.txtFailShape.connect('focus-out-event',
                                  self._callback_entry, 'float', 526)

        self.txtFailLoc.set_tooltip_text(_("Enter the time to failure distribution location factor."))
        self.txtFailLoc.connect('focus-out-event',
                                self._callback_entry, 'float', 527)

        #self.txtWeibullFile.connect('focus-out-event',
        #                            self._callback_entry, 'text', 586)

        # Quadrant 2 (upper right) widgets.  These widgets are used to display
        # maintainability assessment inputs.

        # Quadrant 4 (lower right) widgets.  These widgets are used to display
        # cost assessment inputs.
        self.txtCost.set_tooltip_text(_("Enter the cost of the selected component."))
        self.txtCost.connect('focus-out-event',
                             self._callback_entry, 'float', 513)

        self.txtBurnInTemp.set_tooltip_text(_("Enter the temperature that the selected component will be burned-in."))
        self.txtBurnInTemp.connect('focus-out-event',
                                   self._callback_entry, 'float', 6)

        self.txtBurnInTime.set_tooltip_text(_("Enter the total time the selected component will be burned-in."))
        self.txtBurnInTime.connect('focus-out-event',
                                   self._callback_entry, 'float', 7)

        self.txtLabDevices.set_tooltip_text(_("Enter the total number of units that will be included in life testing in the laboratory."))
        self.txtLabDevices.connect('focus-out-event',
                                   self._callback_entry, "int", 20)

        self.txtLabTime.set_tooltip_text(_("Enter the total time the units will undergo life testing in the laboratory."))
        self.txtLabTime.connect('focus-out-event',
                                self._callback_entry, 'float', 108)

        self.txtLabTemp.set_tooltip_text(_("Enter the temperature the selected component will be exposed to during life testing in the laboratory."))
        self.txtLabTemp.connect('focus-out-event',
                                self._callback_entry, 'float', 106)

        self.txtLabFailures.set_tooltip_text(_("Enter the total number of failure observed during life testing in the laboratory."))
        self.txtLabFailures.connect('focus-out-event',
                                    self._callback_entry, "int", 27)

        self.txtFieldTime.set_tooltip_text(_("Enter the total time that selected component has been fielded."))
        self.txtFieldTime.connect('focus-out-event',
                                  self._callback_entry, 'float', 65)

        self.txtFieldFailures.set_tooltip_text(_("Enter the total number of failure of the selected component that have been observed in the field."))
        self.txtFieldFailures.connect('focus-out-event',
                                      self._callback_entry, "int", 26)

        self.txtMinTemp.set_tooltip_text(_("Enter the minimum design operating temperature of the selected component."))
        self.txtMinTemp.connect('focus-out-event',
                                self._callback_entry, 'float', 56)

        self.txtKneeTemp.set_tooltip_text(_("Enter the knee temperature of the selected component."))
        self.txtKneeTemp.connect('focus-out-event',
                                 self._callback_entry, 'float', 43)

        self.txtMaxTemp.set_tooltip_text(_("Enter the maximum design operating temperature of the selected component."))
        self.txtMaxTemp.connect('focus-out-event',
                                self._callback_entry, 'float', 55)

        self.txtRatedVoltage.set_tooltip_text(_("Enter the maximum rated voltage of the selected component."))
        self.txtRatedVoltage.connect('focus-out-event',
                                     self._callback_entry, 'float', 94)

        self.txtOpVoltage.set_tooltip_text(_("Enter the operating voltage of the selected component."))
        self.txtOpVoltage.connect('focus-out-event',
                                  self._callback_entry, 'float', 66)

        self.txtRatedCurrent.set_tooltip_text(_("Enter the maximum rated current of the selected component."))
        self.txtRatedCurrent.connect('focus-out-event',
                                     self._callback_entry, 'float', 92)

        self.txtOpCurrent.set_tooltip_text(_("Enter the operating current of the selected component."))
        self.txtOpCurrent.connect('focus-out-event',
                                  self._callback_entry, 'float', 62)

        self.txtRatedPower.set_tooltip_text(_("Enter the maximum rated power of the selected component."))
        self.txtRatedPower.connect('focus-out-event',
                                   self._callback_entry, 'float', 93)

        self.txtOpPower.set_tooltip_text(_("Enter the operating power of the selected component."))
        self.txtOpPower.connect('focus-out-event',
                                self._callback_entry, 'float', 64)

        self.txtThetaJC.set_tooltip_text(_("Enter the junction-to-case thermal resistance of the selected component."))
        self.txtThetaJC.connect('focus-out-event',
                                self._callback_entry, 'float', 109)

        self.txtTempRise.set_tooltip_text(_("Enter the ambient to case temperature rise of the selected component."))
        self.txtTempRise.connect('focus-out-event',
                                 self._callback_entry, 'float', 107)

        self.txtCaseTemp.set_tooltip_text(_("Enter the case temperature of the selected component."))
        self.txtCaseTemp.connect('focus-out-event',
                                 self._callback_entry, 'float', 105)

        return False

    def _assessment_inputs_tab_create(self):
        """
        Method to create the Assessment Inputs gtk.Notebook tab and populate it
        with the appropriate widgets.
        """

        hbox = gtk.HBox()

        # Populate quadrant 1 (upper left).
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Reliability Inputs"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hbox.pack_start(frame)

        self.y_pos[0][0] = 5
        y_pos = 5
        for i in range(len(self._ai_tab_labels[0])):
            label = _widg.make_label(self._ai_tab_labels[0][i],
                                     200, 25)
            fixed.put(label, 5, y_pos)
            if(i == 0 or i == 1 or i == 8):
                y_pos += 35
            else:
                y_pos += 30

        fixed.put(self.lblNoCategory, 5, 375)
        fixed.put(self.lblNoSubCategory, 5, 405)

        x_pos = 205
        fixed.put(self.cmbHRType, x_pos, self.y_pos[0][0])
        self.y_pos[0][0] += 35
        fixed.put(self.cmbCalcModel, x_pos, self.y_pos[0][0])
        self.y_pos[0][0] += 35
        fixed.put(self.txtSpecifiedHt, x_pos, self.y_pos[0][0])
        self.y_pos[0][0] += 30
        fixed.put(self.txtSpecifiedMTBF, x_pos, self.y_pos[0][0])
        self.y_pos[0][0] += 30
        fixed.put(self.txtSoftwareHt, x_pos, self.y_pos[0][0])
        self.y_pos[0][0] += 30
        fixed.put(self.txtAddAdj, x_pos, self.y_pos[0][0])
        self.y_pos[0][0] += 30
        fixed.put(self.txtMultAdj, x_pos, self.y_pos[0][0])
        self.y_pos[0][0] += 30
        fixed.put(self.txtAllocationWF, x_pos, self.y_pos[0][0])
        self.y_pos[0][0] += 30
        fixed.put(self.cmbFailDist, x_pos, self.y_pos[0][0])
        self.y_pos[0][0] += 35
        fixed.put(self.txtFailScale, x_pos, self.y_pos[0][0])
        self.y_pos[0][0] += 30
        fixed.put(self.txtFailShape, x_pos, self.y_pos[0][0])
        self.y_pos[0][0] += 30
        fixed.put(self.txtFailLoc, x_pos, self.y_pos[0][0])
        self.y_pos[0][0] += 30
        #fixed.put(self.txtWeibullFile, x_pos, self.y_pos[0][0])
        #self.y_pos[0][0] += 30

        self.part = _util.set_part_model(self._category, self._subcategory)
        if(self.part is not None):
            self.part.assessment_inputs_create(self,
                                               fixed,
                                               x_pos,
                                               self.y_pos[0][0])

        fixed.show_all()

        # Populate quadrant 2 (upper right).
        vpaned = gtk.VPaned()

        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Maintainability Inputs"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned.pack1(frame, True, True)

        self.y_pos[0][1] = 5
        for i in range(len(self._ai_tab_labels[1])):
            label = _widg.make_label(self._ai_tab_labels[1][i],
                                     200, 25)
            fixed.put(label, 5, (30 * i + self.y_pos[0][1]))

        fixed.put(self.txtBurnInTemp, x_pos, self.y_pos[0][1])
        self.y_pos[0][1] += 30
        fixed.put(self.txtBurnInTime, x_pos, self.y_pos[0][1])
        self.y_pos[0][1] += 30
        fixed.put(self.txtLabDevices, x_pos, self.y_pos[0][1])
        self.y_pos[0][1] += 30
        fixed.put(self.txtLabTime, x_pos, self.y_pos[0][1])
        self.y_pos[0][1] += 30
        fixed.put(self.txtLabTemp, x_pos, self.y_pos[0][1])
        self.y_pos[0][1] += 30
        fixed.put(self.txtLabFailures, x_pos, self.y_pos[0][1])
        self.y_pos[0][1] += 30
        fixed.put(self.txtFieldTime, x_pos, self.y_pos[0][1])
        self.y_pos[0][1] += 30
        fixed.put(self.txtFieldFailures, x_pos, self.y_pos[0][1])
        self.y_pos[0][1] += 30

        fixed.show_all()

        # Populate quadrant 4 (lower right)
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Miscellaneous Inputs"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned.pack2(frame, True, True)

        hbox.pack_start(vpaned)

        self.y_pos[0][2] = 5
        for i in range(len(self._ai_tab_labels[3])):
            label = _widg.make_label(self._ai_tab_labels[3][i],
                                     200, 25)
            fixed.put(label, 5, (30 * i + self.y_pos[0][2]))

        fixed.put(self.txtMinTemp, x_pos, self.y_pos[0][2])
        self.y_pos[0][2] += 30
        fixed.put(self.txtKneeTemp, x_pos, self.y_pos[0][2])
        self.y_pos[0][2] += 30
        fixed.put(self.txtMaxTemp, x_pos, self.y_pos[0][2])
        self.y_pos[0][2] += 30
        fixed.put(self.txtRatedVoltage, x_pos, self.y_pos[0][2])
        self.y_pos[0][2] += 30
        fixed.put(self.txtOpVoltage, x_pos, self.y_pos[0][2])
        self.y_pos[0][2] += 30
        fixed.put(self.txtRatedCurrent, x_pos, self.y_pos[0][2])
        self.y_pos[0][2] += 30
        fixed.put(self.txtOpCurrent, x_pos, self.y_pos[0][2])
        self.y_pos[0][2] += 30
        fixed.put(self.txtRatedPower, x_pos, self.y_pos[0][2])
        self.y_pos[0][2] += 30
        fixed.put(self.txtOpPower, x_pos, self.y_pos[0][2])
        self.y_pos[0][2] += 30
        fixed.put(self.txtThetaJC, x_pos, self.y_pos[0][2])
        self.y_pos[0][2] += 30
        fixed.put(self.txtTempRise, x_pos, self.y_pos[0][2])
        self.y_pos[0][2] += 30
        fixed.put(self.txtCaseTemp, x_pos, self.y_pos[0][2])
        self.y_pos[0][2] += 30
        fixed.put(self.txtCost, x_pos, self.y_pos[0][2])
        self.y_pos[0][2] += 30

        fixed.show_all()

        label = gtk.Label()
        _heading = _("Assessment\nInputs")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Allows entering reliability, maintainability, and other assessment inputs for the selected component."))

        self.notebook.insert_page(hbox,
                                  tab_label=label,
                                  position=-1)

        return False

    def _assessment_inputs_tab_load(self):
        """
        Loads the widgets with calculation input information for the Component
        Object.
        """

        _model = self._app.HARDWARE.model
        _row = self._app.HARDWARE.selected_row

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        # Let the user know if the selected part does not have a part
        # category selected.
        if(self._category < 1):
            self.lblNoCategory.show()
        else:
            self.lblNoCategory.hide()

        # Let the user know if the selected part does not have a part
        # subcategory selected.
        if(self._subcategory < 1):
            self.lblNoSubCategory.show()
        else:
            self.lblNoSubCategory.hide()

        self.cmbHRType.set_active(int(_model.get_value(_row, 35)))
        self.cmbCalcModel.set_active(int(_model.get_value(_row, 10)))
        self.txtSpecifiedHt.set_text(str(fmt.format(_model.get_value(_row, 34))))
        self.txtSpecifiedMTBF.set_text(str(_model.get_value(_row, 51)))
        self.txtSoftwareHt.set_text(str(fmt.format(_model.get_value(_row, 33))))
        self.txtAddAdj.set_text(str(_model.get_value(_row, 2)))
        self.txtMultAdj.set_text(str(_model.get_value(_row, 57)))
        self.txtAllocationWF.set_text(str(_model.get_value(_row, 3)))
        self.cmbFailDist.set_active(int(_model.get_value(_row, 24)))
        self.txtFailScale.set_text(str(_model.get_value(_row, 25)))
        self.txtFailShape.set_text(str(_model.get_value(_row, 26)))
        self.txtFailLoc.set_text(str(_model.get_value(_row, 27)))
        #self.txtWeibullFile.set_text(str(_model.get_value(_row, 86)))
        self.txtMissionTime.set_text(str('{0:0.2f}'.format(_model.get_value(_row, 45))))

        _string_ = _util.none_to_string(self.model.get_value(self.selected_row, 6))
        self.txtBurnInTemp.set_text(str('{0:0.2g}'.format(_string_)))
        self.txtBurnInTime.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 7))))
        self.txtLabDevices.set_text(str('{0:0.0g}'.format(self.model.get_value(self.selected_row, 20))))
        self.txtLabTime.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 108))))
        self.txtLabTemp.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 106))))
        self.txtLabFailures.set_text(str('{0:0.0g}'.format(self.model.get_value(self.selected_row, 27))))
        self.txtFieldTime.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 65))))
        self.txtFieldFailures.set_text(str('{0:0.0g}'.format(self.model.get_value(self.selected_row, 26))))

        self.txtMinTemp.set_text(str('{0:0.2f}'.format(self.model.get_value(self.selected_row, 56))))
        self.txtKneeTemp.set_text(str('{0:0.2f}'.format(self.model.get_value(self.selected_row, 43))))
        self.txtMaxTemp.set_text(str('{0:0.2f}'.format(self.model.get_value(self.selected_row, 55))))
        self.txtRatedVoltage.set_text(str(fmt.format(self.model.get_value(self.selected_row, 94))))
        self.txtOpVoltage.set_text(str(fmt.format(self.model.get_value(self.selected_row, 66))))
        self.txtRatedCurrent.set_text(str(fmt.format(self.model.get_value(self.selected_row, 92))))
        self.txtOpCurrent.set_text(str(fmt.format(self.model.get_value(self.selected_row, 62))))
        self.txtRatedPower.set_text(str(fmt.format(self.model.get_value(self.selected_row, 93))))
        self.txtOpPower.set_text(str(fmt.format(self.model.get_value(self.selected_row, 64))))
        self.txtThetaJC.set_text(str(self.model.get_value(self.selected_row, 109)))
        self.txtTempRise.set_text(str(fmt.format(self.model.get_value(self.selected_row, 107))))
        self.txtCaseTemp.set_text(str(fmt.format(self.model.get_value(self.selected_row, 105))))

        self.part = _util.set_part_model(self._category, self._subcategory)
        if(self.part is not None):
            self.part.assessment_inputs_load(self)

        return False

    def _assessment_results_widgets_create(self):
        """ Method to create the Assessment Results widgets. """

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
        self.figDerate = Figure(figsize=(6, 4))
        self.pltDerate = FigureCanvas(self.figDerate)
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
        self.txtVoltageRatio = _widg.make_entry(editable=False, bold=True)
        self.txtCurrentRatio = _widg.make_entry(editable=False, bold=True)
        self.txtPwrRatio = _widg.make_entry(editable=False, bold=True)
        self.chkOverstressed = _widg.make_check_button()
        self.txtOSReason = gtk.TextBuffer()

        # Create the quadrant 1 (upper left) widgets.
        self.txtActiveHt.set_tooltip_text(_("Displays the active failure intensity for the selected component."))
        self.txtDormantHt.set_tooltip_text(_("Displays the dormant failure intensity for the selected component."))
        self.txtSoftwareHt2.set_tooltip_text(_("Displays the software failure intensity for the selected component."))
        self.txtPredictedHt.set_tooltip_text(_("Displays the predicted failure intensity for the selected component.  This is the sum of the active, dormant, and software failure intensities."))
        self.txtMissionHt.set_tooltip_text(_("Displays the mission failure intensity for the selected component."))
        self.txtHtPerCent.set_tooltip_text(_("Displays the percent of the total system failure intensity attributable to the selected component."))
        self.txtMTBF.set_tooltip_text(_("Displays the limiting mean time between failure (MTBF) for the selected component."))
        self.txtMissionMTBF.set_tooltip_text(_("Displays the mission mean time between failure (MTBF) for the selected component."))
        self.txtReliability.set_tooltip_text(_("Displays the limiting reliability for the selected component."))
        self.txtMissionRt.set_tooltip_text(_("Displays the mission reliability for the selected component."))

        # Create the quadrant 2 (upper right) widgets.
        self.txtMPMT.set_tooltip_text(_("Displays the mean preventive maintenance time (MPMT) for the selected component."))
        self.txtMCMT.set_tooltip_text(_("Displays the mean corrective maintenance time (MCMT) for the selected component."))
        self.txtMTTR.set_tooltip_text(_("Displays the mean time to repair (MTTR) for the selected component."))
        self.txtMMT.set_tooltip_text(_("Displays the mean maintenance time (MMT) for the selected component."))
        self.txtAvailability.set_tooltip_text(_("Displays the limiting availability for the selected component."))
        self.txtMissionAt.set_tooltip_text(_("Displays the mission availability for the selected component."))

        # Create the quadrant 4 (lower right) widgets.
        self.txtTotalCost.set_tooltip_text(_("Displays the total cost of the selected component."))
        self.txtCostFailure.set_tooltip_text(_("Displays the cost per failure of the selected component."))
        self.txtCostHour.set_tooltip_text(_("Displays the cost per mission hour of the selected component."))
        self.txtAssemblyCrit.set_tooltip_text(_("Displays the criticality of the selected component.  This is calculated by the FMEA."))
        self.txtPartCount.set_tooltip_text(_("Displays the total number of components used to construct the selected component."))
        self.txtTotalPwr.set_tooltip_text(_("Displays the total power of the selected component."))
        self.txtVoltageRatio.set_tooltip_text(_("Displays the ratio of operating voltage to rated voltage for the selected component."))
        self.txtCurrentRatio.set_tooltip_text(_("Displays the ratio of operating current to rated current for  the selected component."))
        self.txtPwrRatio.set_tooltip_text(_("Displays the ratio of operating power to rated power for the selected component."))
        self.chkOverstressed.set_tooltip_text(_("Indicates whether the selected component is overstressed."))

        return False

    def _assessment_results_tab_create(self):
        """
        Method to create the Calculation Results gtk.Notebook tab and populate
        it with the appropriate widgets.
        """

        hbox = gtk.HBox()

        # Populate quadrant 1 (upper left).
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Reliability Results"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hbox.pack_start(frame)

        self.y_pos[1][0] = 5
        for i in range(len(self._ar_tab_labels[0])):
            label = _widg.make_label(self._ar_tab_labels[0][i],
                                     200, 25)
            fixed.put(label, 5, (30 * i + self.y_pos[1][0]))

        x_pos = 205
        fixed.put(self.txtActiveHt, x_pos, self.y_pos[1][0])
        self.y_pos[1][0] += 30
        fixed.put(self.txtDormantHt, x_pos, self.y_pos[1][0])
        self.y_pos[1][0] += 30
        fixed.put(self.txtSoftwareHt2, x_pos, self.y_pos[1][0])
        self.y_pos[1][0] += 30
        fixed.put(self.txtPredictedHt, x_pos, self.y_pos[1][0])
        self.y_pos[1][0] += 30
        fixed.put(self.txtMissionHt, x_pos, self.y_pos[1][0])
        self.y_pos[1][0] += 30
        fixed.put(self.txtHtPerCent, x_pos, self.y_pos[1][0])
        self.y_pos[1][0] += 30
        fixed.put(self.txtMTBF, x_pos, self.y_pos[1][0])
        self.y_pos[1][0] += 30
        fixed.put(self.txtMissionMTBF, x_pos, self.y_pos[1][0])
        self.y_pos[1][0] += 30
        fixed.put(self.txtReliability, x_pos, self.y_pos[1][0])
        self.y_pos[1][0] += 30
        fixed.put(self.txtMissionRt, x_pos, self.y_pos[1][0])
        self.y_pos[1][0] += 30

        if(self.part is not None):
            self.part.assessment_results_create(self,
                                                fixed,
                                                x_pos,
                                                self.y_pos[1][0])

        frame = gtk.Frame()
        frame.props.height_request = 350
        frame.props.width_request = 450
        frame.add(self.pltDerate)

        fixed.put(frame, 420, 5)

        fixed.show_all()

        # Place quadrant 2 (upper right) widgets.
        vpaned = gtk.VPaned()

        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Maintainability Results"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned.pack1(frame, True, True)

        self.y_pos[1][1] = 5
        for i in range(len(self._ar_tab_labels[1])):
            label = _widg.make_label(self._ar_tab_labels[1][i],
                                     200, 25)
            fixed.put(label, 5, (30 * i + self.y_pos[1][1]))

        fixed.put(self.txtMPMT, x_pos, self.y_pos[1][1])
        self.y_pos[1][1] += 30
        fixed.put(self.txtMCMT, x_pos, self.y_pos[1][1])
        self.y_pos[1][1] += 30
        fixed.put(self.txtMTTR, x_pos, self.y_pos[1][1])
        self.y_pos[1][1] += 30
        fixed.put(self.txtMMT, x_pos, self.y_pos[1][1])
        self.y_pos[1][1] += 30
        fixed.put(self.txtAvailability, x_pos, self.y_pos[1][1])
        self.y_pos[1][1] += 30
        fixed.put(self.txtMissionAt, x_pos, self.y_pos[1][1])
        self.y_pos[1][1] += 30

        fixed.show_all()

        # Place quadrant 4 (lower right) widgets.
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Miscellaneous Results"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned.pack2(frame, True, True)

        hbox.pack_start(vpaned)

        self.y_pos[1][2] = 5
        for i in range(len(self._ar_tab_labels[3])):
            label = _widg.make_label(self._ar_tab_labels[3][i],
                                     200, 25)
            fixed.put(label, 5, (30 * i + self.y_pos[1][2]))

        fixed.put(self.txtTotalCost, x_pos, self.y_pos[1][2])
        self.y_pos[1][2] += 30
        fixed.put(self.txtCostFailure, x_pos, self.y_pos[1][2])
        self.y_pos[1][2] += 30
        fixed.put(self.txtCostHour, x_pos, self.y_pos[1][2])
        self.y_pos[1][2] += 30
        fixed.put(self.txtAssemblyCrit, x_pos, self.y_pos[1][2])
        self.y_pos[1][2] += 30
        fixed.put(self.txtPartCount, x_pos, self.y_pos[1][2])
        self.y_pos[1][2] += 30
        fixed.put(self.txtTotalPwr, x_pos, self.y_pos[1][2])
        self.y_pos[1][2] += 30
        fixed.put(self.txtVoltageRatio, x_pos, self.y_pos[1][2])
        self.y_pos[1][2] += 30
        fixed.put(self.txtCurrentRatio, x_pos, self.y_pos[1][2])
        self.y_pos[1][2] += 30
        fixed.put(self.txtPwrRatio, x_pos, self.y_pos[1][2])
        self.y_pos[1][2] += 30
        fixed.put(self.chkOverstressed, x_pos, self.y_pos[1][2])
        self.y_pos[1][2] += 30

        textview = _widg.make_text_view(buffer_=self.txtOSReason,
                                        width=250)
        textview.set_tooltip_text(_("Displays the reason(s) the selected component is overstressed."))
        fixed.put(textview, x_pos + 30, self.y_pos[1][2])

        fixed.show_all()

        label = gtk.Label()
        _heading = _("Assessment\nResults")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays the results the reliability, maintainability, and other assessments for the selected component."))

        self.notebook.insert_page(hbox,
                                  tab_label=label,
                                  position=-1)

        return False

    def _assessment_results_tab_load(self):
        """
        Loads the widgets with assessment results for the COMPONENT Object.
        """

        _model = self._app.HARDWARE.model
        _row = self._app.HARDWARE.selected_row

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        self.txtCompRefDes.set_text(_model.get_value(_row, 12))

        self.txtActiveHt.set_text(str(fmt.format(_model.get_value(_row, 28))))
        self.txtDormantHt.set_text(str(fmt.format(_model.get_value(_row, 29))))
        self.txtSoftwareHt2.set_text(str(fmt.format(_model.get_value(_row, 33))))
        self.txtPredictedHt.set_text(str(fmt.format(_model.get_value(_row, 32))))
        self.txtMissionHt.set_text(str(fmt.format(_model.get_value(_row, 30))))
        self.txtHtPerCent.set_text(str(fmt.format(_model.get_value(_row, 31))))

        self.txtMTBF.set_text(str('{0:0.2f}'.format(_model.get_value(_row, 50))))
        self.txtMissionMTBF.set_text(str('{0:0.2f}'.format(_model.get_value(_row, 49))))

        self.txtReliability.set_text(str(fmt.format(_model.get_value(_row, 70))))
        self.txtMissionRt.set_text(str(fmt.format(_model.get_value(_row, 69))))

        self.txtMPMT.set_text(str('{0:0.2f}'.format(_model.get_value(_row, 48))))
        self.txtMCMT.set_text(str('{0:0.2f}'.format(_model.get_value(_row, 44))))
        self.txtMTTR.set_text(str('{0:0.2f}'.format(_model.get_value(_row, 52))))
        self.txtMMT.set_text(str('{0:0.2f}'.format(_model.get_value(_row, 46))))

        self.txtAvailability.set_text(str(fmt.format(_model.get_value(_row, 7))))
        self.txtMissionAt.set_text(str(fmt.format(_model.get_value(_row, 8))))

        self.txtTotalCost.set_text(str(locale.currency(_model.get_value(_row, 13))))
        self.txtCostFailure.set_text(str(locale.currency(_model.get_value(_row, 14))))
        self.txtCostHour.set_text(str('${0:0.4g}'.format(_model.get_value(_row, 15))))

        self.txtAssemblyCrit.set_text(str(_model.get_value(_row, 5)))
        self.txtPartCount.set_text(str(fmt.format(_model.get_value(_row, 82))))
        self.txtTotalPwr.set_text(str(fmt.format(_model.get_value(_row, 83))))

        self.txtCurrentRatio.set_text(str(fmt.format(self.model.get_value(self.selected_row, 17))))
        self.txtPwrRatio.set_text(str(fmt.format(self.model.get_value(self.selected_row, 84))))
        self.txtVoltageRatio.set_text(str(fmt.format(self.model.get_value(self.selected_row, 111))))

        self.chkOverstressed.set_active(_model.get_value(_row, 60))

        if(self.part is not None):
            self.part.assessment_results_load(self)

        _derate = self.figDerate.add_subplot(111)
        _derate.set_title(_("Derating Curve for %s at %s") %
                          (self.txtPartNum.get_text(),
                           self.txtRefDes.get_text()))
        _derate.set_xlabel(_(u"Temperature (\u2070C)"))
        _derate.set_ylabel(_("Power (Watts)"))

        # Set up the x, y coordinates for the operating point plot.
        _x_ = []
        _y_ = []
        _x_.append(float(self.txtMinTemp.get_text()))
        _x_.append(float(self.txtKneeTemp.get_text()))
        _x_.append(float(self.txtMaxTemp.get_text()))
        _y_.append(float(self.txtRatedPower.get_text()))
        _y_.append(float(self.txtRatedPower.get_text()))
        _y_.append(0.0)

        _temperature_ = float(self.txtCaseTemp.get_text())
        _power_ = float(self.txtOpPower.get_text())

        _derate.plot(_x_, _y_, 'r.-', linewidth=2)
        _derate.plot(_temperature_, _power_, 'go')
        _derate.axis([0.95 * _x_[0], 1.05 * _x_[2], _y_[2], 1.05 * _y_[0]])

        return False

    def _fmeca_worksheet_widgets_create(self):
        """ Method to create the FMECA widgets. """

        import pango
        from lxml import etree

        # Create the gtk.TreeView for displaying the FMECA information.
        self.tvwFMECA = gtk.TreeView()

        # Retrieve the column heading text from the format file.
        path = "/root/tree[@name='FMECA']/column/usertitle"
        heading = etree.parse(_conf.RELIAFREE_FORMAT_FILE[9]).xpath(path)

        # Retrieve the column datatype from the format file.
        path = "/root/tree[@name='FMECA']/column/datatype"
        datatype = etree.parse(_conf.RELIAFREE_FORMAT_FILE[9]).xpath(path)

        # Retrieve the cellrenderer type from the format file.
        path = "/root/tree[@name='FMECA']/column/widget"
        widget = etree.parse(_conf.RELIAFREE_FORMAT_FILE[9]).xpath(path)

        # Retrieve the column position from the format file.
        path = "/root/tree[@name='FMECA']/column/position"
        position = etree.parse(_conf.RELIAFREE_FORMAT_FILE[9]).xpath(path)

        # Retrieve whether or not the column is editable from the format file.
        path = "/root/tree[@name='FMECA']/column/editable"
        editable = etree.parse(_conf.RELIAFREE_FORMAT_FILE[9]).xpath(path)

        # Retrieve whether or not the column is visible from the format file.
        path = "/root/tree[@name='FMECA']/column/visible"
        visible = etree.parse(_conf.RELIAFREE_FORMAT_FILE[9]).xpath(path)

        # Create a list of GObject datatypes to pass to the model.
        types = []
        for i in range(len(position)):
            types.append(datatype[i].text)

        gobject_types = []
        gobject_types = [gobject.type_from_name(types[ix])
            for ix in range(len(types))]

        query = "SELECT fld_category_noun, \
                        fld_category_value \
                 FROM tbl_risk_category"
        risk_category = self._app.COMDB.execute_query(query,
                                                      None,
                                                      self._app.ComCnx)

        bg_color = _conf.RELIAFREE_COLORS[6]
        fg_color = _conf.RELIAFREE_COLORS[7]

        # Create the model and treeview.
        model = gtk.ListStore(*gobject_types)
        self.tvwFMECA.set_model(model)

        cols = int(len(heading))
        for i in range(cols):
            self._fmeca_col_order.append(int(position[i].text))

            if(widget[i].text == 'combo'):
                cell = gtk.CellRendererCombo()
                cellmodel = gtk.ListStore(gobject.TYPE_STRING,
                                          gobject.TYPE_INT)

                if(i == 11):
                    for j in range(len(risk_category)):
                        cellmodel.append(risk_category[j])

                cell.set_property('has-entry', False)
                cell.set_property('model', cellmodel)
                cell.set_property('text-column', 0)
                cell.set_property('editable', int(editable[i].text))
                cell.connect('edited', _widg.edit_tree, int(position[i].text),
                             model)
            elif(widget[i].text == 'spin'):
                cell = gtk.CellRendererSpin()
                adjustment = gtk.Adjustment(upper=1.0, step_incr=0.05)
                cell.set_property('adjustment', adjustment)
                cell.set_property('digits', 2)
                cell.set_property('editable', int(editable[i].text))
                cell.connect('edited', self._fmeca_tree_edit, i, model)
            elif(widget[i].text == 'check'):
                cell = gtk.CellRendererToggle()
                cell.set_property('activatable', int(editable[i].text))
                cell.connect('toggled', self._fmeca_tree_edit, None, i, model)
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
                    cell.connect('edited', _widg.edit_tree,
                                 int(position[i].text), model)

            column = gtk.TreeViewColumn()
            column.set_visible(int(visible[i].text))
            column.pack_start(cell, True)

            label = gtk.Label(column.get_title())
            label.set_line_wrap(True)
            label.set_alignment(xalign=0.5, yalign=0.5)
            text = "<span weight='bold'>%s</span>" % heading[i].text
            label.set_markup(text)
            label.show_all()
            column.set_widget(label)

            column.set_resizable(True)
            column.set_reorderable(True)
            column.set_sort_column_id(i)
            column.set_sort_indicator(True)

            if(widget[i].text != 'check'):
                column.set_attributes(cell, text=int(position[i].text))
                column.set_cell_data_func(cell, _widg.format_cell,
                                          (int(position[i].text),
                                          datatype[i].text))
                column.connect('notify::width', _widg.resize_wrap, cell)
            else:
                column.set_attributes(cell, active=int(position[i].text))

            self.tvwFMECA.append_column(column)

        self.tvwFMECA.set_tooltip_text(_("Displays the failure mode, effects, and criticality analysis (FMECA) for the selected component."))
        self.tvwFMECA.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        return False

    def _fmeca_worksheet_tab_create(self):
        """
        Method to create the FMECA gtk.Notebook tab and populate it with the
        appropriate widgets.
        """

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwFMECA)

        frame = _widg.make_frame(_label_=_("Failure Mode, Effects, and Criticality Analysis"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        label = gtk.Label()
        _heading = _("FMEA/FMECA\nWorksheet")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Failure mode, effects, and criticality analysis (FMECA) for the selected component."))

        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)
        return False

    def _fmeca_worksheet_tab_load(self):
        """
        Loads the widgets with FMECA information for the COMPONENT Object.
        """

        # Find the revision ID.
        if(_conf.RELIAFREE_MODULES[0] == 1):
            values = (self._app.REVISION.revision_id,
                      self._app.ASSEMBLY.assembly_id)
        else:
            values = (0, self._app.ASSEMBLY.assembly_id)

        # Now load the FMECA gtk.TreeView.
        # Load the FMECA failure mode gtk.TreeView.
        if(_conf.BACKEND == 'mysql'):
            query = "SELECT fld_mode_id, fld_mode_description, \
                            fld_mission_phase, fld_local_effect, \
                            fld_next_effect, fld_end_effect, \
                            fld_detection_method, fld_other_indications, \
                            fld_isolation_method, fld_design_provisions, \
                            fld_operator_provisions, fld_severity_class, \
                            fld_hazard_rate_source, fld_effect_probability, \
                            fld_mode_ratio, fld_mode_failure_rate, \
                            fld_mode_op_time, fld_mode_criticality, \
                            fld_rpn_severity, fld_immediate_cause, \
                            fld_root_cause, fld_rpn_occurence, \
                            fld_detection_control, fld_prevention_control, \
                            fld_rpn_detectability, fld_rpn, \
                            fld_recommended_action, fld_action_taken, \
                            fld_rpn_severity_new, fld_rpn_occurrence_new, \
                            fld_rpn_detectability_new, fld_rpn_new, \
                            fld_critical_item, fld_single_point, \
                            fld_remarks \
                     FROM tbl_fmeca \
                     WHERE fld_revision_id=%d \
                     AND fld_assembly_id=%d \
                     ORDER BY fld_mode_id"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT fld_mode_id, fld_mode_description, \
                            fld_mission_phase, fld_local_effect, \
                            fld_next_effect, fld_end_effect, \
                            fld_detection_method, fld_other_indications, \
                            fld_isolation_method, fld_design_provisions, \
                            fld_operator_provisions, fld_severity_class, \
                            fld_hazard_rate_source, fld_effect_probability, \
                            fld_mode_ratio, fld_mode_failure_rate, \
                            fld_mode_op_time, fld_mode_criticality, \
                            fld_rpn_severity, fld_immediate_cause, \
                            fld_root_cause, fld_rpn_occurence, \
                            fld_detection_control, fld_prevention_control, \
                            fld_rpn_detectability, fld_rpn, \
                            fld_recommended_action, fld_action_taken, \
                            fld_rpn_severity_new, fld_rpn_occurrence_new, \
                            fld_rpn_detectability_new, fld_rpn_new, \
                            fld_critical_item, fld_single_point, \
                            fld_remarks \
                     FROM tbl_fmeca \
                     WHERE fld_revision_id=? \
                     AND fld_assembly_id=? \
                     ORDER BY fld_mode_id"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        model = self.tvwFMECA.get_model()
        model.clear()

        if(not results or results == ''):
            return True

        n_modes = len(results)
        for i in range(n_modes):
            _data = [results[i][0], _util.none_to_string(results[i][1]),
                     _util.none_to_string(results[i][2]),
                     _util.none_to_string(results[i][3]),
                     _util.none_to_string(results[i][4]),
                     _util.none_to_string(results[i][5]),
                     _util.none_to_string(results[i][6]),
                     _util.none_to_string(results[i][7]),
                     _util.none_to_string(results[i][8]),
                     _util.none_to_string(results[i][9]),
                     _util.none_to_string(results[i][10]),
                     _util.none_to_string(results[i][11]),
                     _util.none_to_string(results[i][12]), results[i][13],
                     results[i][14], results[i][15], results[i][16],
                     results[i][17], results[i][18],
                     _util.none_to_string(results[i][19]),
                     _util.none_to_string(results[i][20]), results[i][21],
                     _util.none_to_string(results[i][22]),
                     _util.none_to_string(results[i][23]), results[i][24],
                     results[i][25], _util.none_to_string(results[i][26]),
                     _util.none_to_string(results[i][27]), results[i][28],
                     results[i][29], results[i][30], results[i][31],
                     results[i][32], results[i][33],
                     _util.none_to_string(results[i][34])]

            try:
                model.append(_data)
            except TypeError:
                pass

        return False

    def component_add(self, widget, event):
        """
        Public method to add a new Component to the Program's MySQL or SQLite3
        database.

        Keyword Arguments:
        widget -- the widget that called this function.
        event  -- which button was pressed to call this function.
        """

        n_new_components = _util.add_items(_("Component"))

        for i in range(n_new_components):

            # If no assembly is selected or the selected assembly is the top
            # of the tree, set parent to the top assembly.
            treemodel = self._app.HARDWARE.model
            row = self._app.HARDWARE.selected_row
            if(self._app.HARDWARE.ispart):
                _parent = treemodel.get_value(row, 62)
            else:
                _parent = treemodel.get_string_from_iter(row)

            if(_parent == '-' or _parent is None):
                _parent = '0'

            # Create a description from the part prefix and part index.
            _descrip = str(_conf.RELIAFREE_PREFIX[6]) + ' ' + \
                       str(_conf.RELIAFREE_PREFIX[7])

            # Increment the part index.
            _conf.RELIAFREE_PREFIX[7] = _conf.RELIAFREE_PREFIX[7] + 1

            # First we insert the part into the System table.  Next we
            # find the id of the newly added part.  Thirdly, we add the new
            # part to the functional matrix.  Fourthly, we add the new
            # part to the prediction table.  Finally, we add the new part to
            # the FMECA table.
            values = (self._app.REVISION.revision_id,
                      str(_conf.RELIAFREE_PROG_INFO[3]),
                      _parent, _descrip, 1)

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_system \
                        (fld_revision_id, fld_entered_by, \
                         fld_parent_assembly, \
                         fld_description, fld_part) \
                        VALUES (%d, '%s', '%s', '%s', '%s')"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_system \
                        (fld_revision_id, fld_entered_by, \
                         fld_parent_assembly, \
                         fld_description, fld_part) \
                        VALUES (?, ?, ?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("component.py: Failed to add new component to system table.")
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

            if(assembly_id[0][0] == ''):
                self._app.debug_log.error("component.py: Failed to retrieve ID of new component.")
                return True

            values = (self._app.REVISION.revision_id, assembly_id[0][0])
            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_prediction \
                        (fld_revision_id, fld_assembly_id) \
                        VALUES (%d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_prediction \
                        (fld_revision_id, fld_assembly_id) \
                        VALUES (?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("component.py: Failed to add new component to prediction table.")
                return True

            values = (self._app.REVISION.revision_id, assembly_id[0][0], 0)
            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_functional_matrix \
                         (fld_revision_id, fld_assembly_id, fld_function_id) \
                         VALUES (%d, %d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_functional_matrix \
                         (fld_revision_id, fld_assembly_id, fld_function_id) \
                         VALUES (?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("component.py: Failed to add new component to functional matrix table.")
                return True

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_fmeca_items \
                         (fld_revision_id, fld_assembly_id) \
                         VALUES (%d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_fmeca_items \
                         (fld_revision_id, fld_assembly_id) \
                         VALUES (?, ?)"

            #results = self._app.DB.execute_query(query,
            #                                     values,
            #                                     self._app.ProgCnx,
            #                                     commit=True)

            #if not results:
            #    self._app.debug_log.error("component.py: Failed to add new component to FMECA table.")
            #    return True

        self._app.REVISION.load_tree()
        #TODO: Need to find and select the previously selected revision before loading the hardware tree.
        self._app.HARDWARE.load_tree()

        return False

    def component_delete(self, menuitem):
        """
        Public method to delete the currently selected Component from the
        Program's MySQL or SQLite3 database.

        Keyword Arguments:
        menuitem -- the gtk.MenuItem that called this function.
        """

        # If the selected item isn't a part, then don't delete it.
        if not self._app.HARDWARE.ispart:
            return True

        values = (self._app.REVISION.revision_id,
                  self._app.ASSEMBLY.assembly_id)

        # First delete the part from the System Table.
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
            self._app.debug_log.error("component.py: Failed to delete component from system table.")
            return True

        # Then delete the part information from the Functional Matrix table.
        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_functional_matrix \
                     WHERE fld_revision_id=%d \
                     AND fld_assembly_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_functional_matrix \
                     WHERE fld_revision_id=? \
                     AND fld_assembly_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("component.py: Failed to delete component from functional matrix table.")
            return True

        # Then delete the part information from the Prediction table.
        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_prediction \
                     WHERE fld_revision_id=%d \
                     AND fld_assembly_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_prediction \
                     WHERE fld_revision_id=? \
                     AND fld_assembly_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("component.py: Failed to delete component from prediction table.")
            return True

        # Then delete the part information from the FMECA table.
        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_fmeca_items \
                     WHERE fld_revision_id=%d \
                     AND fld_assembly_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_fmeca_items \
                     WHERE fld_revision_id=? \
                     AND fld_assembly_id=?"

        #results = self._app.DB.execute_query(query,
        #                                     values,
        #                                     self._app.ProgCnx,
        #                                     commit=True)

        #if not results:
        #    self._app.debug_log.error("component.py: Failed to delete component from FMECA table.")
        #    return True

        self._app.REVISION.load_tree()
        #TODO: Need to find and select the previously selected revision before loading the hardware tree.
        self._app.HARDWARE.load_tree()

        return False

    def load_notebook(self):
        """ Function to load the gtk.Notebook for the COMPONENT object. """

        if(self._app.winParts.model != self._app.winParts.full_model):
            self.model = self._app.winParts.model.get_model()
            self.selected_row = self._app.winParts.model.convert_iter_to_child_iter(self._app.winParts.selected_row)
        else:
            self.model = self._app.winParts.full_model
            self.selected_row = self._app.winParts.selected_row

        # Remove existing gtk.Notebook pages except the General Data page.
        while(self.notebook.get_n_pages() > 1):
            self.notebook.remove_page(-1)

        self._general_data_tab_load()
        if self._assessment_inputs_widgets_create():
            self._app.debug_log.error("component.py: Failed to create Assessment Inputs tab widgets.")
        if self._assessment_inputs_tab_create():
            self._app.debug_log.error("component.py: Failed to create Assessment Inputs tab.")
        self._assessment_inputs_tab_load()
        if self._assessment_results_widgets_create():
            self._app.debug_log.error("component.py: Failed to create Assessment Results tab widgets.")
        if self._assessment_results_tab_create():
            self._app.debug_log.error("component.py: Failed to create Assessment Results tab.")
        self._assessment_results_tab_load()
        if self._fmeca_worksheet_widgets_create():
            self._app.debug_log.error("component.py: Failed to create FMECA tab widgets.")
        if self._fmeca_worksheet_tab_create():
            self._app.debug_log.error("component.py: Failed to create FMECA tab.")
        self._fmeca_worksheet_tab_load()

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxComponent)
        self._app.winWorkBook.show_all()

        _title_ = _("RelKit Work Bench: Analyzing %s") % \
                  self.system_model.get_value(self.system_selected_row, 17)
        self._app.winWorkBook.set_title(_title_)
        self.notebook.set_current_page(0)

        return False

    def _load_part_subcategory_combo(self, combo):
        """
        Callback function to load the Component Object subcategory combobox
        when the Component Object category combobox is changed.

        Keyword Arguments:
        combo -- the Component Object category combobox.
        """

        # Get the model and iter from the parts category combo box then read
        # the value of the category ID.
        model = combo.get_model()
        row = combo.get_active_iter()
        values = (int(model.get_value(row, 1)),)

        # Retrieve part subcategory values.
        if(_conf.COM_BACKEND == 'mysql'):
            query = "SELECT fld_subcategory_id, fld_subcategory_noun \
                     FROM tbl_subcategory \
                     WHERE fld_category_id=%d \
                     ORDER BY fld_subcategory_noun ASC"
        elif(_conf.COM_BACKEND == 'sqlite3'):
            query = "SELECT fld_subcategory_id, fld_subcategory_noun \
                     FROM tbl_subcategory \
                     WHERE fld_category_id=? \
                     ORDER BY fld_subcategory_noun ASC"

        results = self._app.COMDB.execute_query(query,
                                                values,
                                                self._app.ComCnx)

        model = gtk.TreeStore(gobject.TYPE_STRING,
                              gobject.TYPE_STRING,
                              gobject.TYPE_STRING)
        model.append(None, ['', '', ''])
        for i in range(len(results)):
            model.append(None, [results[i][1], results[i][0], ''])

        self.cmbSubcategory.set_model(model)
        #self.cmbSubcategory.set_active(treemodel.get_value(row, 78))

        return False

    def _callback_check(self, check, _index_):
        """
        Callback function to retrieve and save checkbutton changes.

        Keyword Arguments:
        check   -- the checkbutton that called the function.
        _index_ -- the position in the Assembly Object _attribute list
                   associated with the data from the calling checkbutton.
        """

        # Update the Hardware Tree.
        self._app.HARDWARE.model.set_value(self._app.HARDWARE.selected_row,
                                           _index_,
                                           check.get_active())

        return False

    def _callback_combo(self, combo, _index_):
        """
        Callback function to retrieve and save combobox changes.

        Keyword Arguments:
        combo   -- the combobox that called the function.
        _index_ -- the position in the Component Object tree model
                   associated with the data from the calling combobox.
        """

        if(_index_ == 511):                 # Component category
            self._category = combo.get_active()
            self._load_part_subcategory_combo(combo)

        elif(_index_ == 543):               # Manufacturer
            cmbmodel = combo.get_model()
            cmbrow = combo.get_active_iter()

            self.txtCAGECode.set_text(str(cmbmodel.get_value(cmbrow, 2)))
            self._app.HARDWARE.model.set_value(self._app.HARDWARE.selected_row,
                                               9,
                                               str(cmbmodel.get_value(cmbrow, 2)))

        elif(_index_ == 578):               # Component subcategory
            if(combo.get_active() > 0):
                self._subcategory = combo.get_active()
                self.part = _util.set_part_model(self._category,
                                                 self._subcategory)
                #if(self.part is not None):
                #    hbox = self.notebook.get_nth_page(1)
                #    fixed = hbox.get_children()[0].get_children()[0].get_children()[0].get_children()
                #    self.part.assessment_inputs_create(self,
                #                                       fixed,
                #                                       205,
                #                                       self.y_pos[0][0])
                #    hbox = self.notebook.get_nth_page(2)
                #    fixed = hbox.get_children()[0].get_children()[0].get_children()[0].get_children()
                #    self.part.assessment_inputs_load(self)
                #    self.part.assessment_results_create(self,
                #                                        fixed,
                #                                        205,
                #                                        self.y_pos[1][0])
                #    self.part.assessment_results_load(self)

        if(_index_ < 500):                  # Update the Parts List.
            self.model.set_value(self.selected_row,
                                 _index_,
                                 int(combo.get_active()))
        else:                               # Update the Hardware tree.
            _index_ -= 500
            self._app.HARDWARE.model.set_value(self._app.HARDWARE.selected_row,
                                               _index_,
                                               int(combo.get_active()))

    def _callback_entry(self, entry, event, convert, _index_):
        """
        Callback function to retrieve and save entry changes.

        Keyword Arguments:
        entry   -- the entry that called the function.
        convert -- the data type to convert the entry contents to.
        _index_ -- the position in the Component Object tree model
                   associated with the data from the calling entry.
        """

        # Update the COMPONENT object calculation data.
        if(convert == 'text'):
            if(_index_ == 71):
                textbuffer = self.txtRemarks.get_child().get_child().get_buffer()
                _text_ = textbuffer.get_text(*textbuffer.get_bounds())
            else:
                _text_ = entry.get_text()

        elif(convert == 'int'):
            _text_ = int(entry.get_text())

        elif(convert == 'float'):
            _text_ = float(entry.get_text())

        if(_index_ < 500):                  # Update the Parts List.
            self.model.set_value(self.selected_row, _index_, _text_)
        else:                               # Update the Hardware tree.
            _index_ -= 500
            self._app.HARDWARE.model.set_value(self._app.HARDWARE.selected_row,
                                               _index_, _text_)

    def _fmeca_tree_edit(self, cell, path, new_text, position, model):
        """
        Called whenever a FMECA failure mode tree or FMECA tree
        gtk.CellRenderer is edited.

        Keyword Arguments:
        cell     -- the CellRenderer that was edited.
        path     -- the TreeView path of the CellRenderer that was edited.
        new_text -- the new text in the edited CellRenderer.
        position -- the column position of the edited CellRenderer.
        model    -- the TreeModel the CellRenderer belongs to.
        """

        _type_ = gobject.type_name(model.get_column_type(position))

        # If this is the critical item or single point column,
        # toggle the check box.
        if(position == 32 or position == 33):
            model[path][position] = not cell.get_active()
        elif(_type_ == 'gchararray'):
            model[path][position] = str(new_text)
        elif(_type_ == 'gint'):
            model[path][position] = int(new_text)
        elif(_type_ == 'gfloat'):
            model[path][position] = float(new_text)

        return False

    def _fmeca_save(self):
        """
        Saves the Assembly Object FMECA gtk.TreeView information to the
        Program's MySQL or SQLite3 database.
        """

        model = self.tvwFMECA.get_model()
        model.foreach(self._fmeca_save_line_item)

        return False

    def _fmeca_save_line_item(self, model, path, row):
        """
        Saves each row in the Assembly Object FMECA failure mode and FMECA
        worksheet treeview model to the database.

        Keyword Arguments:
        model   -- the Assembly Object FMECA failure mode or FMECA worksheet
                   gtk.TreeModel.
        path_   -- the path of the active row in the Assembly Object
                   FMECA gtk.TreeModel.
        row     -- the selected row in the Assembly Object FMECA
                   gtk.TreeView.
        """

        values = (model.get_value(row, 1), model.get_value(row, 2),
                  model.get_value(row, 3), model.get_value(row, 4),
                  model.get_value(row, 5), model.get_value(row, 6),
                  model.get_value(row, 7), model.get_value(row, 8),
                  model.get_value(row, 9), model.get_value(row, 10),
                  model.get_value(row, 11), model.get_value(row, 12),
                  model.get_value(row, 13), model.get_value(row, 14),
                  model.get_value(row, 15), model.get_value(row, 16),
                  model.get_value(row, 17), model.get_value(row, 18),
                  model.get_value(row, 19), model.get_value(row, 20),
                  model.get_value(row, 21), model.get_value(row, 22),
                  model.get_value(row, 23), model.get_value(row, 24),
                  model.get_value(row, 25), model.get_value(row, 26),
                  model.get_value(row, 27), model.get_value(row, 28),
                  model.get_value(row, 29), model.get_value(row, 30),
                  model.get_value(row, 31), model.get_value(row, 32),
                  model.get_value(row, 33), model.get_value(row, 34),
                  model.get_value(row, 0))

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_fmeca \
                     SET fld_mode_description='%s', 'fld_mission_phase=%d, \
                         fld_local_effect=%d, \
                         fld_next_effect='%s', fld_end_effect='%s', \
                         fld_detection_method='%s', \
                         fld_other_indications='%s', \
                         fld_isolation_method='%s', \
                         fld_design_provisions='%s', \
                         fld_operator_provisions='%s', \
                         fld_severity_class=%d, \
                         fld_hazard_rate_source='%s', \
                         fld_effect_probability=%f, fld_mode_ratio=%f, \
                         fld_mode_failure_rate=%f, fld_mode_op_time=%f, \
                         fld_mode_criticality=%f, fld_rpn_severity=%d, \
                         fld_immediate_cause='%s', fld_root_cause='%s', \
                         fld_rpn_occurence=%d, \
                         fld_detection_control='%s', \
                         fld_prevention_control='%s', \
                         fld_rpn_detectability=%d, fld_rpn=%d, \
                         fld_recommended_action='%s', \
                         fld_action_taken='%s', fld_rpn_severity_new=%d, \
                         fld_rpn_occurrence_new=%d, \
                         fld_rpn_detectability_new=%d, fld_rpn_new=%d, \
                         fld_critical_item=%d, fld_single_point=%d, \
                         fld_remarks='%s' \
                     WHERE fld_mode_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_fmeca \
                     SET fld_mode_description=?, fld_mission_phase=?, \
                         fld_local_effect=?, \
                         fld_next_effect=?, fld_end_effect=?, \
                         fld_detection_method=?, \
                         fld_other_indications=?, \
                         fld_isolation_method=?, \
                         fld_design_provisions=?, \
                         fld_operator_provisions=?, \
                         fld_severity_class=?, \
                         fld_hazard_rate_source=?, \
                         fld_effect_probability=?, fld_mode_ratio=?, \
                         fld_mode_failure_rate=?, fld_mode_op_time=?, \
                         fld_mode_criticality=?, fld_rpn_severity=?, \
                         fld_immediate_cause=?, fld_root_cause=?, \
                         fld_rpn_occurence=?, \
                         fld_detection_control=?, \
                         fld_prevention_control=?, \
                         fld_rpn_detectability=?, fld_rpn=?, \
                         fld_recommended_action=?, \
                         fld_action_taken=?, fld_rpn_severity_new=?, \
                         fld_rpn_occurrence_new=?, \
                         fld_rpn_detectability_new=?, fld_rpn_new=?, \
                         fld_critical_item=?, fld_single_point=?, \
                         fld_remarks=? \
                     WHERE fld_mode_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("component.py: Failed to save FMECA information.")
            return True

        return False

    def _mode_add(self):
        """
        Method to add a failure mode to the selected assembly.
        """

        # Find the revision ID.
        if(_conf.RELIAFREE_MODULES[0] == 1):
            values = (self._app.REVISION.revision_id,
                      self._app.ASSEMBLY.assembly_id)
        else:
            values = (0, self._app.ASSEMBLY.assembly_id)

        if(_conf.BACKEND == 'mysql'):
            query = "INSERT INTO tbl_fmeca \
                     (fld_revision_id, fld_assembly_id) \
                     VALUES (%d, %d)"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "INSERT INTO tbl_fmeca \
                     (fld_revision_id, fld_assembly_id) \
                     VALUES (?, ?)"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("component.py: Failed to add new failure mode.")
            return True

        self._fmeca_worksheet_tab_load()

        return False

    def _mode_delete(self):
        """
        Method to remove the selected failure mode from the selected
        assembly.
        """

        # Find the mode ID.
        selection = self.tvwFMECA.get_selection()
        (model, row) = selection.get_selected()

        values = (model.get_value(row, 0),)

        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_fmeca \
                     WHERE fld_mode_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_fmeca \
                     WHERE fld_mode_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("component.py: Failed to delete failure mode.")
            return True

        self._fmeca_worksheet_tab_load()

        return False

    def _notebook_page_switched(self, notebook, page, page_num):
        """
        Called whenever the Tree Book notebook page is changed.

        Keyword Arguments:
        notebook -- the Tree Book notebook widget.
        page     -- the newly selected page widget.
        page_num -- the newly selected page number.
                    0 = General Data
                    1 = Assessment Inputs
                    2 = Assessment Results
                    3 = FMEA/FMECA
                    4 = Maintenance Planning
                    5 = Reliability Test Planning
        """

        self.btnAddItem.show()
        self.btnRemoveItem.show()
        self.btnAnalyze.show()
        self.btnSaveResults.show()

        if(page_num == 0):                  # General data tab
            self.btnAddItem.set_tooltip_text(_("Add a new component to the currently selected assembly."))
            self.btnRemoveItem.set_tooltip_text(_("Delete the currently selected component from the open RelKit Program Database."))
            self.btnAnalyze.set_tooltip_text(_("Calculate the hardware metrics in the open RelKit Program Database."))
            self.btnSaveResults.set_tooltip_text(_("Saves changes to the open RelKit Program Database."))
        elif(page_num == 1):                # Assessment inputs tab
            self.btnAddItem.set_tooltip_text(_("Add a new component to the currently selected assembly."))
            self.btnRemoveItem.set_tooltip_text(_("Delete the currently selected component from the open RelKit Program Database."))
            self.btnAnalyze.set_tooltip_text(_("Calculate the hardware metrics in the open RelKit Program Database."))
            self.btnSaveResults.set_tooltip_text(_("Saves changes to the open RelKit Program Database."))
        elif(page_num == 2):                # Assessment results tab
            self.btnAddItem.set_tooltip_text(_("Add a new component to the currently selected assembly."))
            self.btnRemoveItem.set_tooltip_text(_("Delete the currently selected component from the open RelKit Program Database."))
            self.btnAnalyze.set_tooltip_text(_("Calculate the hardware metrics in the open RelKit Program Database."))
            self.btnSaveResults.set_tooltip_text(_("Saves changes to the open RelKit Program Database."))
        elif(page_num == 3):                # FMEA/FMECA tab
            self.btnAddItem.set_tooltip_text(_("Add a new failure mode, mechanism, or cause to the selected component."))
            self.btnRemoveItem.set_tooltip_text(_("Deletes the selected failure mode, mechanism, or cause."))
            self.btnAnalyze.set_tooltip_text(_("Calculate criticality for the selected component."))
            self.btnSaveResults.set_tooltip_text(_("Save the FMEA/FMECA for the selected component."))
        else:
            self.btnAddItem.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.hide()
            self.btnSaveResults.hide()

        return False

    def _toolbutton_pressed(self, widget):
        """
        Method to react to the COMPONENT Object toolbar button clicked events.

        Keyword Arguments:
        widget -- the toolbar button that was pressed.
        """

        # FMEA calculate criticality.
        # V&V add new task
        # V&V assign existing task
        # Maintenance planning
        # Maintenance planning save changes to selected maintenance policy
        _button_ = widget.get_name()
        _page_ = self.notebook.get_current_page()

        if(_page_ == 0):                    # General data tab.
            if(_button_ == 'Add'):
                self.component_add(widget, None)
            elif(_button_ == 'Remove'):
                self.component_delete(widget)
            elif(_button_ == 'Analyze'):
                _calc.calculate_project(widget, self._app, 3)
            elif(_button_ == 'Save'):
                self._app.HARDWARE.hardware_save()
        elif(_page_ == 1):                  # Assessment inputs tab.
            if(_button_ == 'Add'):
                self.component_add(widget, None)
            elif(_button_ == 'Remove'):
                self.component_delete(widget)
            elif(_button_ == 'Analyze'):
                _calc.calculate_project(widget, self._app, 3)
            elif(_button_ == 'Save'):
                self._app.HARDWARE.hardware_save()
        elif(_page_ == 2):                  # Assessment results tab.
            if(_button_ == 'Add'):
                self.component_add(widget, None)
            elif(_button_ == 'Remove'):
                self.component_delete(widget)
            elif(_button_ == 'Analyze'):
                _calc.calculate_project(widget, self._app, 3)
            elif(_button_ == 'Save'):
                self._app.HARDWARE.hardware_save()
        elif(_page_ == 3):                  # FMEA/FMECA tab.
            if(_button_ == 'Add'):
                #self._mode_add()
                print "Add mode/mechanism/cause"
            elif(_button_ == 'Remove'):
                #self._mode_delete()
                print "Remove mode/mechanism/cause"
            elif(_button_ == 'Analyze'):
                print "Criticality calculations"
            elif(_button_ == 'Save'):
                self._fmeca_save()
        #elif(_page_ == 6):                  # Maintenance planning tab.
        #    if(_button_ == 'Add'):
        #        print "Add maintenance activity"
        #    elif(_button_ == 'Remove'):
        #        print "Remove maintenance activity"
        #    elif(_button_ == 'Analyze'):
        #        print "Maintenance costs"
        #    elif(_button_ == 'Save'):
        #        print "Saving maintenance policy"

        return False
