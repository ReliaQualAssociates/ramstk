#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.WorkBook.py is part of The RTK Project
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
"""
###############################
Hardware Package Work Book View
###############################
"""

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
    from analyses.allocation.gui.gtk.WorkBook import WorkView as Allocation
    from analyses.hazard.gui.gtk.WorkBook import WorkView as Hazard
    from analyses.similar_item.gui.gtk.WorkBook import WorkView as SimilarItem
    from analyses.fmea.gui.gtk.WorkBook import WorkView as FMECA
    from analyses.pof.gui.gtk.WorkBook import WorkView as PoF
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    import rtk.gui.gtk.Widgets as Widgets
    from rtk.analyses.allocation.gui.gtk.WorkBook import WorkView as Allocation
    from rtk.analyses.hazard.gui.gtk.WorkBook import WorkView as Hazard
    from rtk.analyses.similar_item.gui.gtk.WorkBook import WorkView \
        as SimilarItem
    from rtk.analyses.fmea.gui.gtk.WorkBook import WorkView as FMECA
    from rtk.analyses.pof.gui.gtk.WorkBook import WorkView as PoF
import __gui.gtk.Capacitor as gCapacitor
import __gui.gtk.Connection as gConnection
import __gui.gtk.Inductor as gInductor
import __gui.gtk.IntegratedCircuit as gIntegratedCircuit
import __gui.gtk.Meter as gMeter
import __gui.gtk.Crystal as gCrystal
import __gui.gtk.Filter as gFilter
import __gui.gtk.Fuse as gFuse
import __gui.gtk.Lamp as gLamp
import __gui.gtk.Relay as gRelay
import __gui.gtk.Resistor as gResistor
import __gui.gtk.Semiconductor as gSemiconductor
import __gui.gtk.Switch as gSwitch
# from Assistants import AddHardware

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class WorkView(gtk.VBox):  # pylint: disable=R0902, R0904
    """
    The Work Book view displays all the attributes for the selected
    Hardware item.  The attributes of a Work Book view are:

    :ivar _workview: the RTK top level Work View window to embed the
                     Hardware Work Book into.
    :ivar _hardware_model: the Hardware data model whose attributes are being
                           displayed.
    :ivar dict _dic_definitions: dictionary containing pointers to the failure
                                 definitions for the Revision being displayed.
                                 Key is the Failure Definition ID; value is the
                                 pointer to the Failure Definition data model.
    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable Hardware attribute.

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtName - `focus_out_event`               |
    +----------+-------------------------------------------+
    |     1    | txtPartNum - `focus_out_event`            |
    +----------+-------------------------------------------+
    |     2    | txtAltPartNum - `focus_out_event`         |
    +----------+-------------------------------------------+
    |     3    | cmbCategory - `changed`                   |
    +----------+-------------------------------------------+
    |     4    | cmbSubcategory - `changed`                |
    +----------+-------------------------------------------+
    |     5    | txtRefDes - `focus_out_event`             |
    +----------+-------------------------------------------+
    |     6    | txtCompRefDes - `focus_out_event`         |
    +----------+-------------------------------------------+
    |     7    | txtQuantity - `focus_out_event`           |
    +----------+-------------------------------------------+
    |     8    | txtDescription - `focus_out_event`        |
    +----------+-------------------------------------------+
    |     9    | cmbManufacturer - `changed`               |
    +----------+-------------------------------------------+
    |    10    | txtCAGECode - `focus_out_event`           |
    +----------+-------------------------------------------+
    |    11    | txtLCN - `focus_out_event`                |
    +----------+-------------------------------------------+
    |    12    | txtNSN - `focus_out_event`                |
    +----------+-------------------------------------------+
    |    13    | txtYearMade - `focus_out_event`           |
    +----------+-------------------------------------------+
    |    14    | txtSpecification - `focus_out_event`      |
    +----------+-------------------------------------------+
    |    15    | txtPageNum - `focus_out_event`            |
    +----------+-------------------------------------------+
    |    16    | txtFigNum - `focus_out_event`             |
    +----------+-------------------------------------------+
    |    17    | txtAttachments - `focus_out_event`        |
    +----------+-------------------------------------------+
    |    18    | txtMissionTime - `focus_out_event`        |
    +----------+-------------------------------------------+
    |    19    | chkRepairable - `toggled`                 |
    +----------+-------------------------------------------+
    |    20    | chkTagged - `toggled`                     |
    +----------+-------------------------------------------+
    |    21    | txtRemarks - `focus_out_event`            |
    +----------+-------------------------------------------+

    :ivar dtcHardware: the :py:class:`rtk.hardware.Hardware.Hardware` data
                       controller to use with this Work Book.
    :ivar chkSafetyCritical: the :py:class:`gtk.CheckButton` to display/edit
                             the Hardware's safety criticality.
    :ivar txtName: the :py:class:`gtk.Entry` to display/edit the Hardware name.
    :ivar txtTotalCost: the :py:class:`gtk.Entry` to display the Hardware cost.
    :ivar txtPartCount: the :py:class:`gtk.Entry` to display the number of
                        Components comprising the Assembly.
    :ivar txtRemarks: the :py:class:`gtk.Entry` to display/edit the Hardware
                      remarks.
    :ivar txtPredictedHt: the :py:class:`gtk.Entry` to display the Hardware
                          logistics hazard rate.
    :ivar txtMissionHt: the :py:class:`gtk.Entry` to display the Hardware
                        mission hazard rate.
    :ivar txtMTBF: the :py:class:`gtk.Entry` to display the Hardware logistics
                   MTBF.
    :ivar txtMissionMTBF: the :py:class:`gtk.Entry` to display the Hardware
                          mission MTBF.
    :ivar txtMPMT: the :py:class:`gtk.Entry` to display the Hardware mean
                   preventive maintenance time.
    :ivar txtMCMT: the :py:class:`gtk.Entry` to display the Hardware mean
                   corrective maintenance time.
    :ivar txtMTTR: the :py:class:`gtk.Entry` to display the Hardware mean time
                   to repair.
    :ivar txtMMT: the :py:class:`gtk.Entry` to display the Hardware mean
                  maintenance time.
    :ivar txtAvailability: the :py:class:`gtk.Entry` to display the Hardware
                           logistics availability.
    :ivar txtMissionAt: the :py:class:`gtk.Entry` to display the Hardware
                        mission availability.
    """

    def __init__(self, modulebook):
        """
        Initializes the Work Book view for the Hardware package.

        :param modulebook: the :py:class:`rtk.hardware.ModuleBook` to associate
                           with this Work Book.

        """

        gtk.VBox.__init__(self)

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._modulebook = modulebook
        self._hardware_model = None
        self._obj_inputs = None
        self._obj_results = None

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define public scalar attributes.
        self.dtcBoM = self._modulebook.mdcRTK.dtcHardwareBoM
        self.dtcAllocation = self._modulebook.mdcRTK.dtcAllocation
        self.dtcHazard = self._modulebook.mdcRTK.dtcHazard
        self.dtcSimilarItem = self._modulebook.mdcRTK.dtcSimilarItem
        self.dtcFMECA = self._modulebook.mdcRTK.dtcFMEA
        self.dtcPoF = self._modulebook.mdcRTK.dtcPoF

        # General Data page widgets.
        self.chkRepairable = Widgets.make_check_button()
        self.chkTagged = Widgets.make_check_button()

        self.cmbCategory = Widgets.make_combo(simple=False)
        self.cmbManufacturer = Widgets.make_combo(simple=False)
        self.cmbSubcategory = Widgets.make_combo(simple=False)

        self.txtName = Widgets.make_entry()
        self.txtPartNum = Widgets.make_entry()
        self.txtAltPartNum = Widgets.make_entry()
        self.txtRefDes = Widgets.make_entry()
        self.txtCompRefDes = Widgets.make_entry()
        self.txtQuantity = Widgets.make_entry(width=50)
        self.txtDescription = Widgets.make_entry(width=700)
        self.txtCAGECode = Widgets.make_entry()
        self.txtLCN = Widgets.make_entry()
        self.txtNSN = Widgets.make_entry()
        self.txtYearMade = Widgets.make_entry(width=100)
        self.txtSpecification = Widgets.make_entry()
        self.txtPageNum = Widgets.make_entry()
        self.txtFigNum = Widgets.make_entry()
        self.txtImageFile = Widgets.make_entry()
        self.txtAttachments = Widgets.make_entry()
        self.txtMissionTime = Widgets.make_entry(width=75)
        self.txtRevisionID = Widgets.make_entry(width=50, editable=False)
        self.txtRemarks = Widgets.make_text_view(width=400)

        # Allocation work book view.
        self.wbvwAllocation = Allocation(modulebook.mdcRTK.dtcAllocation,
                                         modulebook)

        # Hazard analysis work book view.
        self.wbvwHazard = Hazard(modulebook.mdcRTK.dtcHazard, modulebook)

        # Similar Item Analysis work book view.
        self.wbvwSimilarItem = SimilarItem(modulebook.mdcRTK.dtcSimilarItem,
                                           modulebook)

        # Failure Mode and Effects Analysis work book view.
        self.wbvwFMECA = FMECA(modulebook.mdcRTK.dtcFMEA, modulebook)

        # Physics of Failure Analysis work book view.
        self.wbvwPoF = PoF(modulebook.mdcRTK.dtcPoF, modulebook)

        # Assessment Input page widgets.
        self.btnCalculate = Widgets.make_button(width=35, image='calculate')
        self.btnCalculateAll = Widgets.make_button(
            width=35, image='calculate-all')

        self.cmbActEnviron = Widgets.make_combo()
        self.cmbCostMethod = Widgets.make_combo(200, 30)
        self.cmbDormantEnviron = Widgets.make_combo()
        self.cmbFailDist = Widgets.make_combo()
        self.cmbHRMethod = Widgets.make_combo()
        self.cmbHRModel = Widgets.make_combo()
        self.cmbMTTRMethod = Widgets.make_combo()
        self.cmbRepairDist = Widgets.make_combo()

        self.txtActTemp = Widgets.make_entry(width=100)
        self.txtAddAdj = Widgets.make_entry(width=100)
        self.txtCaseTemp = Widgets.make_entry(width=100)
        self.txtCost = Widgets.make_entry(width=100)
        self.txtDormantTemp = Widgets.make_entry(width=100)
        self.txtDutyCycle = Widgets.make_entry(width=100)
        self.txtFailScale = Widgets.make_entry(width=100)
        self.txtFailShape = Widgets.make_entry(width=100)
        self.txtFailLoc = Widgets.make_entry(width=100)
        self.txtHumidity = Widgets.make_entry(width=100)
        self.txtKneeTemp = Widgets.make_entry(width=100)
        self.txtMaxTemp = Widgets.make_entry(width=100)
        self.txtMinTemp = Widgets.make_entry(width=100)
        self.txtMTTRAddAdj = Widgets.make_entry(width=100)
        self.txtMTTRMultAdj = Widgets.make_entry(width=100)
        self.txtMultAdj = Widgets.make_entry(width=100)
        self.txtOpCurrent = Widgets.make_entry(width=100)
        self.txtOpPower = Widgets.make_entry(width=100)
        self.txtOpVoltage = Widgets.make_entry(width=100)
        self.txtRatedCurrent = Widgets.make_entry(width=100)
        self.txtRatedPower = Widgets.make_entry(width=100)
        self.txtRatedVoltage = Widgets.make_entry(width=100)
        self.txtRepairScale = Widgets.make_entry(width=100)
        self.txtRepairShape = Widgets.make_entry(width=100)
        self.txtRPM = Widgets.make_entry(width=100)
        self.txtSoftwareHt = Widgets.make_entry(width=100)
        self.txtSpecifiedHt = Widgets.make_entry(width=100)
        self.txtSpecifiedMTBF = Widgets.make_entry(width=100)
        self.txtSpecifiedMTTR = Widgets.make_entry(width=100)
        self.txtTempRise = Widgets.make_entry(width=100)
        self.txtThetaJC = Widgets.make_entry(width=100)
        self.txtVibration = Widgets.make_entry(width=100)

        self.vpnReliabilityInputs = gtk.VPaned()

        # Assessment Results page widgets.
        self.chkOverstressed = Widgets.make_check_button()

        self.fraDerate = gtk.Frame()

        self.txtActiveHt = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtDormantHt = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtSoftwareHt2 = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtPredictedHt = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtMissionHt = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtHtPerCent = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtMTBF = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtMissionMTBF = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtReliability = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtMissionRt = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtMPMT = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtMCMT = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtMTTR = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtMMT = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtAvailability = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtMissionAt = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtTotalCost = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtCostFailure = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtCostHour = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtAssemblyCrit = Widgets.make_entry(
            width=300, editable=False, bold=True)
        self.txtPartCount = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtTotalPwr = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtPartCount = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtTotalPwr = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtVoltageRatio = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtCurrentRatio = Widgets.make_entry(
            width=100, editable=False, bold=True)
        self.txtPwrRatio = Widgets.make_entry(
            width=100, editable=False, bold=True)

        self.txtOSReason = gtk.TextBuffer()

        self.vpnReliabilityResults = gtk.VPaned()

        # Set gtk.Widgets() tooltip text.
        self.btnCalculate.set_tooltip_text(
            _(u"Calculate the reliability "
              u"assessment for the selected "
              u"hardware item."))
        self.btnCalculateAll.set_tooltip_text(
            _(u"Calculate the reliability "
              u"assessment for the entire "
              u"system."))

        # Connect gtk.Widget() signals to callback methods.
        self.btnCalculate.connect('clicked', self._on_button_clicked, 50)
        self.btnCalculateAll.connect('clicked', self._on_button_clicked, 51)

        # Put it all together.
        _toolbar = self._create_toolbar()
        self.pack_start(_toolbar, expand=False)

        _notebook = self._create_notebook()
        self.pack_start(_notebook)

        self.show_all()

    def _create_toolbar(self):
        """
        Method to create the toolbar for the Hardware class Work Book.

        :return: _toolbar
        :rtype: gtk.Toolbar
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        # Add sibling assembly button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(
            _(u"Adds a new assembly to the RTK Project "
              u"at the same hierarchy level as the "
              u"selected assembly."))
        _image = gtk.Image()
        _image.set_from_file(
            Configuration.ICON_DIR + '32x32/insert_sibling.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 0)
        _toolbar.insert(_button, _position)
        _position += 1

        # Add child assembly button.
        _button = gtk.MenuToolButton(None, label="")
        _button.set_tooltip_text(
            _(u"Adds a new assembly or component to the "
              u"RTK Project that is one level "
              u"subordinate to the selected assembly."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/insert_child.png')
        _button.set_icon_widget(_image)
        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"Assembly"))
        _menu_item.set_tooltip_text(
            _(u"Adds one or more subordinate "
              u"assemblies to the currently selected "
              u"hardware item."))
        _menu_item.connect('activate', self._on_button_clicked, 1)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Component"))
        _menu_item.set_tooltip_text(
            _(u"Adds one or more components to the "
              u"currently selected hardware item."))
        _menu_item.connect('activate', self._on_button_clicked, 2)
        _menu.add(_menu_item)
        _button.set_menu(_menu)
        _menu.show_all()
        _button.show()
        _toolbar.insert(_button, _position)
        _position += 1

        # Delete assembly button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(
            _(u"Removes the currently selected hardware "
              u"item from the RTK Project.  This will "
              u"also remove all hardware items "
              u"subordinate to the currently selected "
              u"hardware item."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/remove.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 3)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save hardware item button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 4)
        _toolbar.insert(_button, _position)
        _position += 1

        # Save BoM (save-all) button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/save-all.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 5)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Create report button.
        _button = gtk.MenuToolButton(None, label="")
        _button.set_tooltip_text(_(u"Create Hardware reports."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/reports.png')
        _button.set_icon_widget(_image)
        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"Allocation Report"))
        _menu_item.set_tooltip_text(
            _(u"Creates the reliability allocation "
              u"report for the currently selected "
              u"hardware item."))
        #_menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Hazards Analysis Report"))
        _menu_item.set_tooltip_text(
            _(u"Creates the hazards analysis report "
              u"for the currently selected hardware "
              u"item."))
        #_menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Similar Item Analysis Report"))
        _menu_item.set_tooltip_text(
            _(u"Creates the similar item analysis "
              u"report for the currently selected "
              u"hardware item."))
        #_menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"FMEA Report"))
        _menu_item.set_tooltip_text(
            _(u"Creates the FMEA/FMECA "
              u"report for the currently selected "
              u"hardware item."))
        #_menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _button.set_menu(_menu)
        _menu.show_all()
        _button.show()
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Create an import button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/db-import.png')
        _button.set_icon_widget(_image)
        _button.set_name('Import')
        #_button.connect('clicked', ImportHardware, self._app)
        _button.set_tooltip_text(_(u"Launches the hardware import assistant."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Create an export button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/db-export.png')
        _button.set_icon_widget(_image)
        _button.set_name('Export')
        #_button.connect('clicked', ExportHardware, self._app)
        _button.set_tooltip_text(_(u"Launches the hardware export assistant."))
        _toolbar.insert(_button, _position)

        _toolbar.show()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Hardware class gtk.Notebook().

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

        # Insert the reliability Allocation page.
        _label = gtk.Label()
        _label.set_markup(
            "<span weight='bold'>" + _(u"Allocation") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays the reliability allocation for "
              u"the selected hardware item."))

        self.wbvwAllocation.create_page()
        _notebook.insert_page(
            self.wbvwAllocation, tab_label=_label, position=-1)

        # Insert the Hazard Analysis page.
        _label = gtk.Label()
        _label.set_markup(
            "<span weight='bold'>" + _(u"Hazard\nAnalysis") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays the hazard analysis for the "
              u"selected hardware item."))

        self.wbvwHazard.create_page()
        _notebook.insert_page(self.wbvwHazard, tab_label=_label, position=-1)

        # Insert the Similar Item Analysis page.
        _label = gtk.Label()
        _label.set_markup(
            "<span weight='bold'>" + _(u"Similar Item\nAnalysis") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays the similar item analysis for "
              u"the selected assembly."))

        self.wbvwSimilarItem.create_page()
        _notebook.insert_page(
            self.wbvwSimilarItem, tab_label=_label, position=-1)

        self._create_assessment_inputs_page(_notebook)
        self._create_assessment_results_page(_notebook)

        # Insert the Failure Mode and Effects Analysis page.
        _label = gtk.Label()
        _label.set_markup(
            "<span weight='bold'>" + _(u"FMEA\nWorksheet") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays the failure mode and effects "
              u"analysis for the selected assembly."))

        self.wbvwFMECA.create_page()
        _notebook.insert_page(self.wbvwFMECA, tab_label=_label, position=-1)

        # Insert the Physics of Failure Analysis page.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Physics of\nFailure\nAnalysis") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays the physics of failure analysis "
              u"for the selected assembly."))

        self.wbvwPoF.create_page()
        _notebook.insert_page(self.wbvwPoF, tab_label=_label, position=-1)

        return _notebook

    def _create_general_data_page(self, notebook):
        """
        Method to create the Hardware class gtk.Notebook() page for displaying
        general data about the selected Hardware item.

        :param gtk.Notebook notebook: the Hardware class gtk.Notebook().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HBox()
        _vpaned = gtk.VPaned()

        # Build the quadrant 1 (upper left) containers.
        _fixed1 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed1)

        _frame = Widgets.make_frame(label=_(u"General Information"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, True, True)

        # Build the quadrant 3 (lower left) containers.
        _fixed3 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed3)

        _frame = Widgets.make_frame(label=_(u"Manufacturer Information"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack2(_frame, True, True)

        _hbox.pack_start(_vpaned)

        # Build the quadrant 2 (upper right) containers.
        _vpaned = gtk.VPaned()

        _fixed2 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed2)

        _frame = Widgets.make_frame(label=_(u"Specification Information"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, True, True)

        # Build the quadrant 4 (lower right) containers.
        _fixed4 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed4)

        _frame = Widgets.make_frame(label=_(u"Miscellaneous Information"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack2(_frame, True, True)

        _hbox.pack_start(_vpaned)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.ComboBox() widgets.
        _model = self.cmbCategory.get_model()
        _model.clear()
        _model.append(None, ['', 0, ''])
        for _cat in Configuration.RTK_CATEGORIES:
            _model.append(None, [
                Configuration.RTK_CATEGORIES[_cat][0],
                Configuration.RTK_CATEGORIES[_cat][1], ''
            ])

        _model = self.cmbManufacturer.get_model()
        _model.clear()
        _model.append(None, ['', 0, ''])
        for _man in Configuration.RTK_MANUFACTURERS:
            _model.append(None, [
                _man[0] + " - " + _man[1] + " (" + _man[2] + ")", _man[1],
                _man[2]
            ])

        # Create the labels for quadrant #1.
        _labels = [
            _(u"Assembly Name:"),
            _(u"Part Number:"),
            _(u"Alternate Part #:"),
            _(u"Category:"),
            _(u"Sub-Category:"),
            _(u"Ref. Designator:"),
            _(u"Composite Ref Des:"),
            _(u"Quantity:"),
            _(u"Description:")
        ]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed1, 5, 5)

        # Create the labels for quadrant #3.
        _labels = [
            _(u"Manufacturer:"),
            _(u"CAGE Code:"),
            _(u"LCN:"),
            _(u"NSN:"),
            _(u"Manufacture Year:")
        ]
        (_x_pos2, _y_pos2) = Widgets.make_labels(_labels, _fixed3, 5, 5)
        _x_pos = max(_x_pos, _x_pos2) + 50

        # Place the quadrant #1 widgets.
        self.txtName.set_tooltip_text(
            _(u"Displays the name of the selected "
              u"hardware item."))
        self.txtPartNum.set_tooltip_text(
            _(u"Displays the part number of "
              u"the selected hardware item."))
        self.txtAltPartNum.set_tooltip_text(
            _(u"Displays an alternative part "
              u"number for the selected "
              u"hardware item."))
        self.cmbCategory.set_tooltip_text(
            _(u"Select the part type for the "
              u"component."))
        self.cmbSubcategory.set_tooltip_text(
            _(u"Select the part sub-type "
              u"for the component."))
        self.txtRefDes.set_tooltip_text(
            _(u"Displays the reference "
              u"designator of the selected "
              u"hardware item."))
        self.txtCompRefDes.set_tooltip_text(
            _(u"Displays the composite "
              u"reference designator of "
              u"the selected hardware item."))
        self.txtQuantity.set_tooltip_text(
            _(u"Displays the quantity of "
              u"the selected hardware item."))
        self.txtDescription.set_tooltip_text(
            _(u"Displays the description "
              u"of the selected hardware "
              u"item."))

        _fixed1.put(self.txtName, _x_pos, _y_pos[0])
        _fixed1.put(self.txtPartNum, _x_pos, _y_pos[1])
        _fixed1.put(self.txtAltPartNum, _x_pos, _y_pos[2])
        _fixed1.put(self.cmbCategory, _x_pos, _y_pos[3])
        _fixed1.put(self.cmbSubcategory, _x_pos, _y_pos[4])
        _fixed1.put(self.txtRefDes, _x_pos, _y_pos[5])
        _fixed1.put(self.txtCompRefDes, _x_pos, _y_pos[6])
        _fixed1.put(self.txtQuantity, _x_pos, _y_pos[7])
        _fixed1.put(self.txtDescription, _x_pos, _y_pos[8])

        self._lst_handler_id.append(
            self.txtName.connect('focus-out-event', self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.txtPartNum.connect('focus-out-event', self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtAltPartNum.connect('focus-out-event', self._on_focus_out,
                                       2))
        self._lst_handler_id.append(
            self.cmbCategory.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbSubcategory.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.txtRefDes.connect('focus-out-event', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtCompRefDes.connect('focus-out-event', self._on_focus_out,
                                       6))
        self._lst_handler_id.append(
            self.txtQuantity.connect('focus-out-event', self._on_focus_out, 7))
        self._lst_handler_id.append(
            self.txtDescription.connect('focus-out-event', self._on_focus_out,
                                        8))

        _fixed1.show_all()

        # Place the quadrant #3 widgets.
        self.cmbManufacturer.set_tooltip_text(
            _(u"Displays the manufacturer "
              u"of the selected hardware "
              u"item."))
        self.txtCAGECode.set_tooltip_text(
            _(u"Displays the Commercial and "
              u"Government Entity (CAGE) "
              u"code of the selected "
              u"hardware item."))
        self.txtLCN.set_tooltip_text(
            _(u"Displays the logistics control "
              u"number (LCN) of the selected "
              u"hardware item."))
        self.txtNSN.set_tooltip_text(
            _(u"Displays the national stock number "
              u"(NSN) of the selected hardware "
              u"item."))
        self.txtYearMade.set_tooltip_text(
            _(u"Displays the year the selected "
              u"hardware item was "
              u"manufactured."))
        _fixed3.put(self.cmbManufacturer, _x_pos, _y_pos2[0])
        _fixed3.put(self.txtCAGECode, _x_pos, _y_pos2[1])
        _fixed3.put(self.txtLCN, _x_pos, _y_pos2[2])
        _fixed3.put(self.txtNSN, _x_pos, _y_pos2[3])
        _fixed3.put(self.txtYearMade, _x_pos, _y_pos2[4])

        self._lst_handler_id.append(
            self.cmbManufacturer.connect('changed', self._on_combo_changed, 9))
        self._lst_handler_id.append(
            self.txtCAGECode.connect('focus-out-event', self._on_focus_out,
                                     10))
        self._lst_handler_id.append(
            self.txtLCN.connect('focus-out-event', self._on_focus_out, 11))
        self._lst_handler_id.append(
            self.txtNSN.connect('focus-out-event', self._on_focus_out, 12))
        self._lst_handler_id.append(
            self.txtYearMade.connect('focus-out-event', self._on_focus_out,
                                     13))

        _fixed3.show_all()

        # Create the labels for quadrant #2.
        _labels = [
            _(u"Specification:"),
            _(u"Page Number:"),
            _(u"Figure Number:"),
            _(u"Image File:"),
            _(u"Attachments:"),
            _(u"Mission Time:")
        ]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed2, 5, 5)

        # Create the labels for quadrant #4.
        _labels = [
            _(u"Revision ID:"),
            _(u"Repairable?"),
            _(u"Tagged?"),
            _(u"Remarks:")
        ]
        (_x_pos2, _y_pos2) = Widgets.make_labels(_labels, _fixed4, 5, 5)
        _x_pos = max(_x_pos, _x_pos2) + 50

        # Place the quadrant #2 widgets.
        self.txtSpecification.set_tooltip_text(
            _(u"Displays the governing "
              u"specification for the "
              u"selected hardware item, if "
              u"any."))
        self.txtPageNum.set_tooltip_text(
            _(u"Displays the governing "
              u"specification page number "
              u"for the selected hardware item."))
        self.txtFigNum.set_tooltip_text(
            _(u"Displays the governing "
              u"specification figure number "
              u"for the selected hardware item."))
        self.txtImageFile.set_tooltip_text(
            _(u"Displays the URL to an "
              u"image of the selected "
              u"hardware item."))
        self.txtAttachments.set_tooltip_text(
            _(u"Displays the URL to an "
              u"attachment associated "
              u"with the selected "
              u"hardware item."))
        self.txtMissionTime.set_tooltip_text(
            _(u"Displays the mission time "
              u"for the selected hardware "
              u"item."))

        _fixed2.put(self.txtSpecification, _x_pos, _y_pos[0])
        _fixed2.put(self.txtPageNum, _x_pos, _y_pos[1])
        _fixed2.put(self.txtFigNum, _x_pos, _y_pos[2])
        _fixed2.put(self.txtImageFile, _x_pos, _y_pos[3])
        _fixed2.put(self.txtAttachments, _x_pos, _y_pos[4])
        _fixed2.put(self.txtMissionTime, _x_pos, _y_pos[5])

        self._lst_handler_id.append(
            self.txtSpecification.connect('focus-out-event',
                                          self._on_focus_out, 14))
        self._lst_handler_id.append(
            self.txtPageNum.connect('focus-out-event', self._on_focus_out, 15))
        self._lst_handler_id.append(
            self.txtFigNum.connect('focus-out-event', self._on_focus_out, 16))
        self._lst_handler_id.append(
            self.txtAttachments.connect('focus-out-event', self._on_focus_out,
                                        17))
        self._lst_handler_id.append(
            self.txtMissionTime.connect('focus-out-event', self._on_focus_out,
                                        18))

        _fixed2.show_all()

        # Place the quadrant #4 widgets.
        self.txtRevisionID.set_tooltip_text(
            _(u"Displays the currently "
              u"selected revision."))
        self.chkRepairable.set_tooltip_text(
            _(u"Indicates whether or not "
              u"the selected hardware item is "
              u"repairable."))
        self.chkTagged.set_tooltip_text(
            _(u"Indicates whether or not the "
              u"selected hardware item is "
              u"tagged.  A tagged hardware item "
              u"has no specific meaning."))
        self.txtRemarks.set_tooltip_text(
            _(u"Enter any remarks associated "
              u"with the selected hardware "
              u"item."))

        _fixed4.put(self.txtRevisionID, _x_pos, _y_pos2[0])
        _fixed4.put(self.chkRepairable, _x_pos, _y_pos2[1])
        _fixed4.put(self.chkTagged, _x_pos, _y_pos2[2])
        _fixed4.put(self.txtRemarks, _x_pos, _y_pos2[3])

        self._lst_handler_id.append(
            self.chkRepairable.connect('toggled', self._on_toggled, 19))
        self._lst_handler_id.append(
            self.chkTagged.connect('toggled', self._on_toggled, 20))
        self._lst_handler_id.append(21)
        #    self.txtRemarks.get_child().get_child().connect('focus-out-event',
        #                                                    self._on_focus_out,
        #                                                    21))

        _fixed4.show_all()

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup(
            "<span weight='bold'>" + _(u"General\nData") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays general information about "
              u"the selected assembly."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_assessment_inputs_page(self, notebook):  # pylint: disable=R0914, R0915
        """
        Creates the Hardware class gtk.Notebook() page for displaying the
        assessment inputs for the selected Hardware.

        :param gtk.Notebook notebook: the Hardware class gtk.Notebook() widget.
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

        _hpaned2 = gtk.HPaned()
        _hpaned.pack1(_hpaned2, True, False)

        _bbox.pack_start(self.btnCalculate, False, False)
        _bbox.pack_end(self.btnCalculateAll, False, False)

        # --------------------------------------------------------------#
        # Build the quadrant 1 (left) container.                        #
        # --------------------------------------------------------------#
        # Add the layout for stress inputs.
        _fixed1 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed1)

        _frame = Widgets.make_frame(label=_(u"Stress Inputs"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hpaned2.pack1(_frame, True, False)

        # --------------------------------------------------------------#
        # Build the quadrant 2 (middle) container.                      #
        # --------------------------------------------------------------#
        # Add the layout for reliability inputs.
        _fixed2 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed2)

        _frame = Widgets.make_frame(label=_(u"Reliability Inputs"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.vpnReliabilityInputs.pack1(_frame, True, True)

        _hpaned2.pack2(self.vpnReliabilityInputs, True, False)

        # --------------------------------------------------------------#
        # Build the quadrant 2 (upper right) container.                 #
        # --------------------------------------------------------------#
        _vpaned = gtk.VPaned()
        _hpaned.pack2(_vpaned, True, False)

        # Add the layout for common maintainability inputs.  These input
        # widgets will be used for assembly and component inputs.
        _fixed3 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed3)

        _frame = Widgets.make_frame(label=_(u"Maintainability Inputs"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, True, False)

        # --------------------------------------------------------------#
        # Build the quadrant 4 (lower right) container.                 #
        # --------------------------------------------------------------#
        # Add the layout for common miscellaneous inputs.  These input
        # widgets will be used for assembly and component inputs.
        _fixed4 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed4)

        _frame = Widgets.make_frame(label=_(u"Miscellaneous Inputs"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack2(_frame, True, False)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display the assessment inputs.      #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load all the gtk.ComboBox() widgets.
        _model = self.cmbHRMethod.get_model()
        _model.clear()
        self.cmbHRMethod.append_text("")
        for __, _type in enumerate(Configuration.RTK_HR_TYPE):
            self.cmbHRMethod.append_text(_type)

        _model = self.cmbHRModel.get_model()
        _model.clear()
        self.cmbHRModel.append_text("")
        for __, _model in enumerate(Configuration.RTK_HR_MODEL):
            self.cmbHRModel.append_text(_model)

        _model = self.cmbFailDist.get_model()
        _model.clear()
        self.cmbFailDist.append_text("")
        for __, _dist in enumerate(Configuration.RTK_S_DIST):
            self.cmbFailDist.append_text(_dist)

        _model = self.cmbActEnviron.get_model()
        _model.clear()
        self.cmbActEnviron.append_text("")
        for __, _environ in enumerate(Configuration.RTK_ACTIVE_ENVIRON):
            self.cmbActEnviron.append_text(_environ[0])

        _model = self.cmbDormantEnviron.get_model()
        _model.clear()
        self.cmbDormantEnviron.append_text("")
        for __, _environ in enumerate(Configuration.RTK_DORMANT_ENVIRON):
            self.cmbDormantEnviron.append_text(_environ)

        # Create the labels for quadrant 1.
        _labels = [
            _(u"Active Environment:"),
            _(u"Active Temp:"),
            _(u"Dormant Environment:"),
            _(u"Dormant Temp:"),
            _(u"Duty Cycle:"),
            _(u"Humidity:"),
            _(u"Vibration:"),
            _(u"RPM:"),
            _(u"Min Rated Temp:"),
            _(u"Knee Temp:"),
            _(u"Max Rated Temp:"),
            _(u"Rated Voltage:"),
            _(u"Operating Voltage:"),
            _(u"Rated Current:"),
            _(u"Operating Current:"),
            _(u"Rated Power:"),
            _(u"Operating Power:"),
            _(u"theta JC:"),
            _(u"Temperature Rise:"),
            _(u"Case Temperature:")
        ]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed1, 5, 5)
        _x_pos += 50

        # Place the quadrant 1 widgets.
        self.cmbActEnviron.set_tooltip_text(
            _(u"Selects the active "
              u"operating environment for "
              u"the selected hardware item."))
        self.txtActTemp.set_tooltip_text(
            _(u"Displays the active "
              u"environment operating "
              u"temperature for the selected "
              u"hardware item."))
        self.cmbDormantEnviron.set_tooltip_text(
            _(u"Selects the dormant "
              u"environment for the "
              u"selected hardware item."))
        self.txtDormantTemp.set_tooltip_text(
            _(u"Displays the dormant "
              u"environment temperature "
              u"for the selected "
              u"hardware item."))
        self.txtDutyCycle.set_tooltip_text(
            _(u"Displays the operating "
              u"duty cycle for the "
              u"selected hardware item."))
        self.txtHumidity.set_tooltip_text(
            _(u"Displays the active "
              u"environment operating "
              u"humidity for the selected "
              u"hardware item."))
        self.txtVibration.set_tooltip_text(
            _(u"Displays the active "
              u"environment operating "
              u"vibration level for the "
              u"selected hardware item."))
        self.txtRPM.set_tooltip_text(
            _(u"Displays the active environment "
              u"operating RPM for the selected "
              u"hardware item."))
        self.txtMinTemp.set_tooltip_text(
            _(u"The minimum design operating "
              u"temperature for the selected"
              u"hardware item."))
        self.txtKneeTemp.set_tooltip_text(
            _(u"The knee temperature for "
              u"the selected hardware item."))
        self.txtMaxTemp.set_tooltip_text(
            _(u"The maximum design operating "
              u"temperature for the selected "
              u"hardware item."))
        self.txtRatedVoltage.set_tooltip_text(
            _(u"The maximum rated "
              u"voltage for the "
              u"selected hardware item."))
        self.txtOpVoltage.set_tooltip_text(
            _(u"The operating voltage for "
              u"the selected hardware item."))
        self.txtRatedCurrent.set_tooltip_text(
            _(u"The maximum rated "
              u"current for the "
              u"selected hardware item."))
        self.txtOpCurrent.set_tooltip_text(
            _(u"The operating current for "
              u"the selected hardware item."))
        self.txtRatedPower.set_tooltip_text(
            _(u"The maximum rated power "
              u"for the selected "
              u"hardware item."))
        self.txtOpPower.set_tooltip_text(
            _(u"The operating power for the "
              u"selected hardware item."))
        self.txtThetaJC.set_tooltip_text(
            _(u"The junction-to-case thermal "
              u"resistance for the selected "
              u"hardware item."))
        self.txtTempRise.set_tooltip_text(
            _(u"The ambient to case "
              u"temperature rise for the "
              u"selected hardware item."))
        self.txtCaseTemp.set_tooltip_text(
            _(u"The case temperature for "
              u"the selected hardware item."))

        _fixed1.put(self.cmbActEnviron, _x_pos, _y_pos[0])
        _fixed1.put(self.txtActTemp, _x_pos, _y_pos[1])
        _fixed1.put(self.cmbDormantEnviron, _x_pos, _y_pos[2])
        _fixed1.put(self.txtDormantTemp, _x_pos, _y_pos[3])
        _fixed1.put(self.txtDutyCycle, _x_pos, _y_pos[4])
        _fixed1.put(self.txtHumidity, _x_pos, _y_pos[5])
        _fixed1.put(self.txtVibration, _x_pos, _y_pos[6])
        _fixed1.put(self.txtRPM, _x_pos, _y_pos[7])
        _fixed1.put(self.txtMinTemp, _x_pos, _y_pos[8])
        _fixed1.put(self.txtKneeTemp, _x_pos, _y_pos[9])
        _fixed1.put(self.txtMaxTemp, _x_pos, _y_pos[10])
        _fixed1.put(self.txtRatedVoltage, _x_pos, _y_pos[11])
        _fixed1.put(self.txtOpVoltage, _x_pos, _y_pos[12])
        _fixed1.put(self.txtRatedCurrent, _x_pos, _y_pos[13])
        _fixed1.put(self.txtOpCurrent, _x_pos, _y_pos[14])
        _fixed1.put(self.txtRatedPower, _x_pos, _y_pos[15])
        _fixed1.put(self.txtOpPower, _x_pos, _y_pos[16])
        _fixed1.put(self.txtThetaJC, _x_pos, _y_pos[17])
        _fixed1.put(self.txtTempRise, _x_pos, _y_pos[18])
        _fixed1.put(self.txtCaseTemp, _x_pos, _y_pos[19])

        self._lst_handler_id.append(
            self.cmbActEnviron.connect('changed', self._on_combo_changed, 22))
        self._lst_handler_id.append(
            self.txtActTemp.connect('focus-out-event', self._on_focus_out, 23))
        self._lst_handler_id.append(
            self.cmbDormantEnviron.connect('changed', self._on_combo_changed,
                                           24))
        self._lst_handler_id.append(
            self.txtDormantTemp.connect('focus-out-event', self._on_focus_out,
                                        25))
        self._lst_handler_id.append(
            self.txtDutyCycle.connect('focus-out-event', self._on_focus_out,
                                      26))
        self._lst_handler_id.append(
            self.txtHumidity.connect('focus-out-event', self._on_focus_out,
                                     27))
        self._lst_handler_id.append(
            self.txtVibration.connect('focus-out-event', self._on_focus_out,
                                      28))
        self._lst_handler_id.append(
            self.txtRPM.connect('focus-out-event', self._on_focus_out, 29))

        # Create the labels for quadrant 2.
        _labels = [
            _(u"Calculation Method:"),
            _(u"Calculation Model:"),
            _(u"Specified h(t):"),
            _(u"Specified MTBF:"),
            _(u"Software h(t):"),
            _(u"Additive Adj:"),
            _(u"Multiplicative Adj:"),
            _(u"Failure Distribution:"),
            _(u"Scale:"),
            _(u"Shape:"),
            _(u"Location:")
        ]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed2, 5, 5)
        _x_pos += 50

        # Place the quadrant 2 widgets.
        self.cmbHRMethod.set_tooltip_text(
            _(u"Selects the method of "
              u"assessing the hazard rate for "
              u"the selected hardware item."))
        self.cmbHRModel.set_tooltip_text(
            _(u"Selects the hazard rate model to "
              u"use when calculating the hazard "
              u"rate for the selected hardware "
              u"item."))
        self.txtSpecifiedHt.set_tooltip_text(
            _(u"Displays the specified "
              u"failure intensity for "
              u"the selected hardware item."))
        self.txtSpecifiedMTBF.set_tooltip_text(
            _(u"Displays the specified "
              u"mean time between "
              u"failure (MTBF) for the "
              u"selected hardware item."))
        self.txtSoftwareHt.set_tooltip_text(
            _(u"Displays the software "
              u"failure rate for the "
              u"selected hardware item."))
        self.txtAddAdj.set_tooltip_text(
            _(u"Displays any hazard rate "
              u"assessment additive "
              u"adjustment factor for the "
              u"selected hardware item."))
        self.txtMultAdj.set_tooltip_text(
            _(u"Displays any hazard rate "
              u"assessment multiplicative "
              u"adjustment factor for the "
              u"selected hardware item."))
        self.cmbFailDist.set_tooltip_text(
            _(u"Selects the distribution of "
              u"times to failure for the "
              u"selected hardware item."))
        self.txtFailScale.set_tooltip_text(
            _(u"Displays the time to "
              u"failure distribution scale "
              u"factor for the selected "
              u"hardware item."))
        self.txtFailShape.set_tooltip_text(
            _(u"Displays the time to "
              u"failure distribution shape "
              u"factor for the selected "
              u"hardware item."))
        self.txtFailLoc.set_tooltip_text(
            _(u"Displays the time to failure "
              u"distribution location "
              u"factor for the selected "
              u"hardware item."))

        _fixed2.put(self.cmbHRMethod, _x_pos, _y_pos[0])
        _fixed2.put(self.cmbHRModel, _x_pos, _y_pos[1])
        _fixed2.put(self.txtSpecifiedHt, _x_pos, _y_pos[2])
        _fixed2.put(self.txtSpecifiedMTBF, _x_pos, _y_pos[3])
        _fixed2.put(self.txtSoftwareHt, _x_pos, _y_pos[4])
        _fixed2.put(self.txtAddAdj, _x_pos, _y_pos[5])
        _fixed2.put(self.txtMultAdj, _x_pos, _y_pos[6])
        _fixed2.put(self.cmbFailDist, _x_pos, _y_pos[7])
        _fixed2.put(self.txtFailScale, _x_pos, _y_pos[8])
        _fixed2.put(self.txtFailShape, _x_pos, _y_pos[9])
        _fixed2.put(self.txtFailLoc, _x_pos, _y_pos[10])

        self._lst_handler_id.append(
            self.cmbHRMethod.connect('changed', self._on_combo_changed, 30))
        self._lst_handler_id.append(
            self.cmbHRModel.connect('changed', self._on_combo_changed, 31))
        self._lst_handler_id.append(
            self.txtSpecifiedHt.connect('focus-out-event', self._on_focus_out,
                                        32))
        self._lst_handler_id.append(
            self.txtSpecifiedMTBF.connect('focus-out-event',
                                          self._on_focus_out, 33))
        self._lst_handler_id.append(
            self.txtSoftwareHt.connect('focus-out-event', self._on_focus_out,
                                       34))
        self._lst_handler_id.append(
            self.txtAddAdj.connect('focus-out-event', self._on_focus_out, 35))
        self._lst_handler_id.append(
            self.txtMultAdj.connect('focus-out-event', self._on_focus_out, 36))
        self._lst_handler_id.append(
            self.cmbFailDist.connect('changed', self._on_combo_changed, 37))
        self._lst_handler_id.append(
            self.txtFailScale.connect('focus-out-event', self._on_focus_out,
                                      38))
        self._lst_handler_id.append(
            self.txtFailShape.connect('focus-out-event', self._on_focus_out,
                                      39))
        self._lst_handler_id.append(
            self.txtFailLoc.connect('focus-out-event', self._on_focus_out, 40))

        _fixed1.show_all()
        _fixed2.show_all()

        # Create the labels for quadrant #2.
        _labels = [
            _(u"MTTR Method:"),
            _(u"Specified MTTR:"),
            _(u"Additive Adj:"),
            _(u"Multiplicative Adj:"),
            _(u"Repair Distribution:"),
            _(u"Scale:"),
            _(u"Shape:")
        ]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed3, 5, 5)

        # Create the labels for quadrant #4.
        _labels = [_(u"Cost Method:"), _(u"Unit Cost:")]
        (_x_pos2, _y_pos2) = Widgets.make_labels(_labels, _fixed4, 5, 5)
        _x_pos = max(_x_pos, _x_pos2) + 50

        # Place the quadrant #3 widgets.
        _model = self.cmbMTTRMethod.get_model()
        _model.clear()
        self.cmbMTTRMethod.append_text("")
        for __, _type in enumerate(Configuration.RTK_MTTR_TYPE):
            self.cmbMTTRMethod.append_text(_type)

        _model = self.cmbRepairDist.get_model()
        _model.clear()
        self.cmbRepairDist.append_text("")
        for __, _dist in enumerate(Configuration.RTK_S_DIST):
            self.cmbRepairDist.append_text(_dist)

        self.cmbMTTRMethod.set_tooltip_text(
            _(u"Selects the method of "
              u"assessing the mean time to "
              u"repair (MTTR) for the "
              u"selected hardware item."))
        self.txtSpecifiedMTTR.set_tooltip_text(
            _(u"Displays the specified "
              u"mean time to repair "
              u"(MTTR) for the "
              u"selected hardware item."))
        self.txtMTTRAddAdj.set_tooltip_text(
            _(u"Displays the mean time to "
              u"repair (MTTR) assessment "
              u"additive adjustment "
              u"factor for the selected "
              u"hardware item."))
        self.txtMTTRMultAdj.set_tooltip_text(
            _(u"Displays the mean time "
              u"to repair (MTTR) "
              u"assessment multiplicative "
              u"adjustment factor for "
              u"the selected hardware item."))
        self.cmbRepairDist.set_tooltip_text(
            _(u"Selects the time to "
              u"repair distribution for "
              u"the selected hardware item."))
        self.txtRepairScale.set_tooltip_text(
            _(u"Displays the time to "
              u"repair distribution "
              u"scale parameter for the "
              u"selected hardware item."))
        self.txtRepairShape.set_tooltip_text(
            _(u"Displays the time to "
              u"repair distribution "
              u"shape parameter for the "
              u"selected hardware item."))

        _fixed3.put(self.cmbMTTRMethod, _x_pos, _y_pos[0])
        _fixed3.put(self.txtSpecifiedMTTR, _x_pos, _y_pos[1])
        _fixed3.put(self.txtMTTRAddAdj, _x_pos, _y_pos[2])
        _fixed3.put(self.txtMTTRMultAdj, _x_pos, _y_pos[3])
        _fixed3.put(self.cmbRepairDist, _x_pos, _y_pos[4])
        _fixed3.put(self.txtRepairScale, _x_pos, _y_pos[5])
        _fixed3.put(self.txtRepairShape, _x_pos, _y_pos[6])

        self._lst_handler_id.append(
            self.cmbMTTRMethod.connect('changed', self._on_combo_changed, 41))
        self._lst_handler_id.append(
            self.txtSpecifiedMTTR.connect('focus-out-event',
                                          self._on_focus_out, 42))
        self._lst_handler_id.append(
            self.txtMTTRAddAdj.connect('focus-out-event', self._on_focus_out,
                                       43))
        self._lst_handler_id.append(
            self.txtMTTRMultAdj.connect('focus-out-event', self._on_focus_out,
                                        44))
        self._lst_handler_id.append(
            self.cmbRepairDist.connect('changed', self._on_combo_changed, 45))
        self._lst_handler_id.append(
            self.txtRepairScale.connect('focus-out-event', self._on_focus_out,
                                        46))
        self._lst_handler_id.append(
            self.txtRepairShape.connect('focus-out-event', self._on_focus_out,
                                        47))

        # Place the quadrant #4 widgets.
        _model = self.cmbCostMethod.get_model()
        _model.clear()
        self.cmbCostMethod.append_text("")
        for __, _type in enumerate(Configuration.RTK_COST_TYPE):
            self.cmbCostMethod.append_text(_type)

        self.cmbCostMethod.set_tooltip_text(
            _(u"Select the method for "
              u"assessing the cost of the "
              u"selected hardware item."))
        self.txtCost.set_tooltip_text(
            _(u"The unit cost of the selected "
              u"hardware item."))

        _fixed4.put(self.cmbCostMethod, _x_pos, _y_pos2[0])
        _fixed4.put(self.txtCost, _x_pos, _y_pos2[1])

        self._lst_handler_id.append(
            self.cmbCostMethod.connect('changed', self._on_combo_changed, 48))
        self._lst_handler_id.append(
            self.txtCost.connect('focus-out-event', self._on_focus_out, 49))
        self._lst_handler_id.append(
            self.txtMinTemp.connect('focus-out-event', self._on_focus_out, 50))
        self._lst_handler_id.append(
            self.txtKneeTemp.connect('focus-out-event', self._on_focus_out,
                                     51))
        self._lst_handler_id.append(
            self.txtMaxTemp.connect('focus-out-event', self._on_focus_out, 52))
        self._lst_handler_id.append(
            self.txtRatedVoltage.connect('focus-out-event', self._on_focus_out,
                                         53))
        self._lst_handler_id.append(
            self.txtOpVoltage.connect('focus-out-event', self._on_focus_out,
                                      54))
        self._lst_handler_id.append(
            self.txtRatedCurrent.connect('focus-out-event', self._on_focus_out,
                                         55))
        self._lst_handler_id.append(
            self.txtOpCurrent.connect('focus-out-event', self._on_focus_out,
                                      56))
        self._lst_handler_id.append(
            self.txtRatedPower.connect('focus-out-event', self._on_focus_out,
                                       57))
        self._lst_handler_id.append(
            self.txtOpPower.connect('focus-out-event', self._on_focus_out, 58))
        self._lst_handler_id.append(
            self.txtThetaJC.connect('focus-out-event', self._on_focus_out, 59))
        self._lst_handler_id.append(
            self.txtTempRise.connect('focus-out-event', self._on_focus_out,
                                     60))
        self._lst_handler_id.append(
            self.txtCaseTemp.connect('focus-out-event', self._on_focus_out,
                                     61))

        _fixed3.show_all()
        _fixed4.show_all()

        _label = gtk.Label()
        _label.set_markup(
            "<span weight='bold'>" + _(u"Assessment\nInputs") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Allows entering reliability, "
              u"maintainability, and other assessment "
              u"inputs for the selected hardware item."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_assessment_results_page(self, notebook):
        """
        Creates the Hardware class gtk.Notebook() page for displaying the
        assessment results for the selected Hardware.

        :param gtk.Notebook notebook: the Hardware class gtk.Notebook().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.fraDerate.props.height_request = 350
        self.fraDerate.props.width_request = 450

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hpaned = gtk.HPaned()

        # --------------------------------------------------------------#
        # Build the quadrant 1 (left) container.                        #
        # --------------------------------------------------------------#
        # Add the layout for stress results.
        _fixed1 = gtk.Fixed()

        _hpaned2 = gtk.HPaned()
        _hpaned.pack1(_hpaned2, True, False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed1)

        _frame = Widgets.make_frame(label=_(u"Operating Stress Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hpaned2.pack1(_frame, True, False)

        # --------------------------------------------------------------#
        # Build the quadrant 2 (middle) container.                      #
        # --------------------------------------------------------------#
        # Add the layout for reliability results.
        _fixed2 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed2)

        _frame = Widgets.make_frame(label=_(u"Reliability Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.vpnReliabilityResults.pack1(_frame, True, True)

        _hpaned2.pack2(self.vpnReliabilityResults, True, False)

        # --------------------------------------------------------------#
        # Build the quadrant 3 (upper right) containers.                #
        # --------------------------------------------------------------#
        _vpaned = gtk.VPaned()
        _hpaned.pack2(_vpaned, True, False)

        _fixed3 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed3)

        _frame = Widgets.make_frame(label=_(u"Maintainability Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, True, False)

        # --------------------------------------------------------------#
        # Build the quadrant 4 (lower right) containers.                #
        # --------------------------------------------------------------#
        _fixed4 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed4)

        _frame = Widgets.make_frame(label=_(u"Miscellaneous Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack2(_frame, True, False)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display the assessment results.     #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the labels for quadrant #1.
        _labels = [
            _(u"Total Power Used:"),
            _(u"Voltage Ratio:"),
            _(u"Current Ratio:"),
            _(u"Power Ratio:")
        ]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed1, 5, 5)
        _x_pos += 50

        # Place the quadrant 1 widgets.
        self.txtTotalPwr.set_tooltip_text(
            _(u"The total power of the selected "
              u"hardware item."))
        self.txtVoltageRatio.set_tooltip_text(
            _(u"The ratio of operating "
              u"voltage to rated voltage "
              u"for the selected hardware "
              u"item."))
        self.txtCurrentRatio.set_tooltip_text(
            _(u"The ratio of operating "
              u"current to rated "
              u"current for the "
              u"selected hardware item."))
        self.txtPwrRatio.set_tooltip_text(
            _(u"The ratio of operating "
              u"power to rated power for "
              u"the selected hardware item."))
        self.chkOverstressed.set_tooltip_text(
            _(u"Indicates whether the "
              u"selected hardware item is "
              u"overstressed."))

        _fixed1.put(self.txtTotalPwr, _x_pos, _y_pos[0])
        _fixed1.put(self.txtVoltageRatio, _x_pos, _y_pos[1])
        _fixed1.put(self.txtCurrentRatio, _x_pos, _y_pos[2])
        _fixed1.put(self.txtPwrRatio, _x_pos, _y_pos[3])

        _label = Widgets.make_label(text=_(u"Overstressed?:"))
        _fixed1.put(_label, 5, _y_pos[3] + 30)
        _fixed1.put(self.chkOverstressed, _x_pos, _y_pos[3] + 30)

        _textview = Widgets.make_text_view(
            txvbuffer=self.txtOSReason, width=250)

        _textview.set_tooltip_text(
            _(u"The reason(s) the selected hardware "
              u"item is overstressed."))
        _fixed1.put(_textview, 4, _y_pos[3] + 60)

        _fixed1.put(self.fraDerate, 5, _y_pos[3] + 175)

        # Create the labels for quadrant 2.
        _labels = [
            _(u"Active h(t):"),
            _(u"Dormant h(t):"),
            _(u"Software h(t):"),
            _(u"Predicted h(t):"),
            _(u"Mission h(t):"),
            _(u"h(t) Percent:"),
            _(u"MTBF:"),
            _(u"Mission MTBF:"),
            _(u"Reliability:"),
            _(u"Mission R(t):")
        ]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed2, 5, 5)

        _x_pos += 50

        # Place the quadrant 2 widgets.
        self.txtActiveHt.set_tooltip_text(
            _(u"Displays the active failure "
              u"intensity for the selected "
              u"hardware item."))
        self.txtDormantHt.set_tooltip_text(
            _(u"Displays the dormant "
              u"failure intensity for the "
              u"selected hardware item."))
        self.txtSoftwareHt2.set_tooltip_text(
            _(u"Displays the software "
              u"failure intensity for "
              u"the selected hardware item."))
        self.txtPredictedHt.set_tooltip_text(
            _(u"Displays the logistics "
              u"hazard rate for "
              u"the selected hardware item.  "
              u"This is the sum of the "
              u"active, dormant, and "
              u"software hazard rates."))
        self.txtMissionHt.set_tooltip_text(
            _(u"Displays the mission "
              u"failure intensity for the "
              u"selected hardware item."))
        self.txtHtPerCent.set_tooltip_text(
            _(u"Displays the percent of "
              u"the total system failure "
              u"intensity attributable to "
              u"the selected hardware item."))
        self.txtMTBF.set_tooltip_text(
            _(u"Displays the logistics mean time "
              u"between failure (MTBF) for the "
              u"selected hardware item."))
        self.txtMissionMTBF.set_tooltip_text(
            _(u"Displays the mission "
              u"mean time between "
              u"failure (MTBF) for the "
              u"selected hardware item."))
        self.txtReliability.set_tooltip_text(
            _(u"Displays the logistics "
              u"reliability for the "
              u"selected hardware item."))
        self.txtMissionRt.set_tooltip_text(
            _(u"Displays the mission "
              u"reliability for the "
              u"selected hardware item."))

        _fixed2.put(self.txtActiveHt, _x_pos, _y_pos[0])
        _fixed2.put(self.txtDormantHt, _x_pos, _y_pos[1])
        _fixed2.put(self.txtSoftwareHt2, _x_pos, _y_pos[2])
        _fixed2.put(self.txtPredictedHt, _x_pos, _y_pos[3])
        _fixed2.put(self.txtMissionHt, _x_pos, _y_pos[4])
        _fixed2.put(self.txtHtPerCent, _x_pos, _y_pos[5])
        _fixed2.put(self.txtMTBF, _x_pos, _y_pos[6])
        _fixed2.put(self.txtMissionMTBF, _x_pos, _y_pos[7])
        _fixed2.put(self.txtReliability, _x_pos, _y_pos[8])
        _fixed2.put(self.txtMissionRt, _x_pos, _y_pos[9])

        _fixed1.show_all()
        _fixed2.show_all()

        # Create the labels for quadrant 3.
        _labels = [
            _(u"MPMT:"),
            _(u"MCMT:"),
            _(u"MTTR:"),
            _(u"MMT:"),
            _(u"Availability:"),
            _(u"Mission A(t):")
        ]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed3, 5, 5)

        # Create the labels for quadrant #4.
        _labels = [
            _(u"Total Cost:"),
            _(u"Cost/Failure:"),
            _(u"Cost/Hour:"),
            _(u"Total Part Count:")
        ]
        (_x_pos2, _y_pos2) = Widgets.make_labels(_labels, _fixed4, 5, 5)

        _x_pos = max(_x_pos, _x_pos2) + 50

        # Place the quadrant #3 widgets.
        self.txtMPMT.set_tooltip_text(
            _(u"Displays the mean preventive "
              u"maintenance time (MPMT) for the "
              u"selected hardware item."))
        self.txtMCMT.set_tooltip_text(
            _(u"Displays the mean corrective "
              u"maintenance time (MCMT) for the "
              u"selected hardware item."))
        self.txtMTTR.set_tooltip_text(
            _(u"Displays the mean time to "
              u"repair (MTTR) for the selected "
              u"hardware item."))
        self.txtMMT.set_tooltip_text(
            _(u"Displays the mean maintenance "
              u"time (MMT) for the selected "
              u"hardware item."))
        self.txtAvailability.set_tooltip_text(
            _(u"Displays the logistics "
              u"availability for the "
              u"selected hardware item."))
        self.txtMissionAt.set_tooltip_text(
            _(u"Displays the mission "
              u"availability for the "
              u"selected hardware item."))

        _fixed3.put(self.txtMPMT, _x_pos, _y_pos[0])
        _fixed3.put(self.txtMCMT, _x_pos, _y_pos[1])
        _fixed3.put(self.txtMTTR, _x_pos, _y_pos[2])
        _fixed3.put(self.txtMMT, _x_pos, _y_pos[3])
        _fixed3.put(self.txtAvailability, _x_pos, _y_pos[4])
        _fixed3.put(self.txtMissionAt, _x_pos, _y_pos[5])

        # Place the quadrant #4 widgets.
        self.txtTotalCost.set_tooltip_text(
            _(u"Displays the total cost of "
              u"the selected hardware item."))
        self.txtCostFailure.set_tooltip_text(
            _(u"Displays the cost per "
              u"failure of the selected "
              u"hardware item."))
        self.txtCostHour.set_tooltip_text(
            _(u"Displays the cost per mission "
              u"hour of the selected hardware "
              u"item."))
        self.txtPartCount.set_tooltip_text(
            _(u"The total number of components "
              u"used to construct the selected "
              u"hardware item."))

        _fixed4.put(self.txtTotalCost, _x_pos, _y_pos2[0])
        _fixed4.put(self.txtCostFailure, _x_pos, _y_pos2[1])
        _fixed4.put(self.txtCostHour, _x_pos, _y_pos2[2])
        _fixed4.put(self.txtPartCount, _x_pos, _y_pos2[3])

        _label = gtk.Label()
        _label.set_markup(
            _(u"<span weight='bold'>" + _(u"Assessment\nResults") + u"</span>")
        )
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays the results the reliability, "
              u"maintainability, and other "
              u"assessments for the selected "
              u"assembly."))

        notebook.insert_page(_hpaned, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Loads the Hardware class gtk.Notebook().

        :param model: the :py:class:`rtk.hardware.Hardware.Model` to load.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._hardware_model = model

        # --------------------------------------------------------------#
        # Load the General Data information.                            #
        # --------------------------------------------------------------#
        self.txtRevisionID.set_text(str(model.revision_id))
        self.txtAltPartNum.set_text(model.alt_part_number)
        self.txtAttachments.set_text(model.attachments)
        self.txtCAGECode.set_text(model.cage_code)
        self.txtCompRefDes.set_text(model.comp_ref_des)
        self.txtDescription.set_text(model.description)
        self.txtFigNum.set_text(model.figure_number)
        self.txtLCN.set_text(model.lcn)
        self.cmbManufacturer.set_active(model.manufacturer)
        self.txtName.set_text(model.name)
        self.txtNSN.set_text(model.nsn)
        self.txtPageNum.set_text(model.page_number)
        self.txtPartNum.set_text(model.part_number)
        self.txtQuantity.set_text(str(model.quantity))
        self.txtRefDes.set_text(model.ref_des)
        _text = Utilities.none_to_string(model.remarks)

        _buffer = self.txtRemarks.get_child().get_child().get_buffer()
        _buffer.set_text(_text)
        self.txtSpecification.set_text(model.specification_number)
        self.chkTagged.set_active(model.tagged_part)
        self.txtYearMade.set_text(str(model.year_of_manufacture))

        # Show/hide the assembly-specific or component-specific widgets as
        # appropriate.
        if model.part == 1:
            self.cmbSubcategory.handler_block(self._lst_handler_id[4])
            self.cmbCategory.show()
            self.cmbSubcategory.show()
            self.cmbCategory.set_active(model.category_id)
            self.cmbSubcategory.set_active(model.subcategory_id)
            self.chkRepairable.hide()
            self.cmbSubcategory.handler_unblock(self._lst_handler_id[4])
        else:
            self.cmbCategory.hide()
            self.cmbSubcategory.hide()
            self.chkRepairable.show()
            self.chkRepairable.set_active(model.repairable)

            # ----------------------------------------------------------#
            # Load the Reliability Allocation information.              #
            # ----------------------------------------------------------#
            # Clear the Allocation View gtk.TreeModel().
            self.wbvwAllocation.load_page(self.dtcBoM, model.hardware_id)

            # ----------------------------------------------------------#
            # Load the Similar Item Analysis information.               #
            # ----------------------------------------------------------#
            self.wbvwSimilarItem.load_page(self.dtcBoM, model.hardware_id)

        # --------------------------------------------------------------#
        # Load the Hazard Analysis information.                         #
        # --------------------------------------------------------------#
        self.wbvwHazard.load_page(self.dtcBoM, model.hardware_id)

        # --------------------------------------------------------------#
        # Load the Assessment Input information.                        #
        # --------------------------------------------------------------#
        self._load_assessment_inputs_page()

        # --------------------------------------------------------------#
        # Load the Assessment Result information.                       #
        # --------------------------------------------------------------#
        self._load_assessment_results_page()

        # --------------------------------------------------------------#
        # Load the FMEA/FMECA information.                              #
        # --------------------------------------------------------------#
        self.wbvwFMECA.load_page(model.hardware_id,
                                 model.hazard_rate_logistics)

        # --------------------------------------------------------------#
        # Load the PoF Analysis information.                            #
        # --------------------------------------------------------------#
        self.wbvwPoF.load_page(model.hardware_id)

        self.get_children()[1].set_current_page(0)

        return False

    def _load_assessment_inputs_page(self):
        """
        Method to load the assessment inputs page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'

        self.cmbHRMethod.set_active(
            int(self._hardware_model.hazard_rate_method))
        self.txtSpecifiedHt.set_text(
            str(fmt.format(self._hardware_model.hazard_rate_specified)))
        self.txtSpecifiedMTBF.set_text(
            str(self._hardware_model.mtbf_specified))

        self.txtSoftwareHt.set_text(
            str(fmt.format(self._hardware_model.hazard_rate_software)))
        self.txtAddAdj.set_text(str(self._hardware_model.add_adj_factor))
        self.txtMultAdj.set_text(str(self._hardware_model.mult_adj_factor))
        self.cmbFailDist.set_active(int(self._hardware_model.failure_dist))
        self.txtFailScale.set_text(
            str(self._hardware_model.failure_parameter_1))
        self.txtFailShape.set_text(
            str(self._hardware_model.failure_parameter_2))
        self.txtFailLoc.set_text(str(self._hardware_model.failure_parameter_3))
        self.cmbActEnviron.set_active(
            int(self._hardware_model.environment_active))
        self.txtActTemp.set_text(str(self._hardware_model.temperature_active))
        self.cmbDormantEnviron.set_active(
            int(self._hardware_model.environment_dormant))
        self.txtDormantTemp.set_text(
            str(self._hardware_model.temperature_dormant))
        self.txtDutyCycle.set_text(str(self._hardware_model.duty_cycle))
        self.txtHumidity.set_text(str(self._hardware_model.humidity))
        self.txtVibration.set_text(str(self._hardware_model.vibration))
        self.txtRPM.set_text(str(self._hardware_model.rpm))
        self.cmbMTTRMethod.set_active(int(self._hardware_model.mttr_type))
        self.txtSpecifiedMTTR.set_text(
            str(self._hardware_model.mttr_specified))
        self.txtMTTRAddAdj.set_text(
            str(self._hardware_model.mttr_add_adj_factor))
        self.txtMTTRMultAdj.set_text(
            str(self._hardware_model.mttr_mult_adj_factor))
        self.cmbRepairDist.set_active(int(self._hardware_model.repair_dist))
        self.txtRepairScale.set_text(
            str(self._hardware_model.repair_parameter_1))
        self.txtRepairShape.set_text(
            str(self._hardware_model.repair_parameter_2))

        self.txtMissionTime.set_text(
            str('{0:0.2f}'.format(self._hardware_model.mission_time)))
        self.txtCost.set_text(str(locale.currency(self._hardware_model.cost)))
        self.txtMinTemp.set_text(
            str('{0:0.2f}'.format(self._hardware_model.min_rated_temperature)))
        self.txtMaxTemp.set_text(
            str('{0:0.2f}'.format(self._hardware_model.max_rated_temperature)))
        self.txtRatedVoltage.set_text(
            str(fmt.format(self._hardware_model.rated_voltage)))
        self.txtOpVoltage.set_text(
            str(fmt.format(self._hardware_model.operating_voltage)))
        self.txtRatedCurrent.set_text(
            str(fmt.format(self._hardware_model.rated_current)))
        self.txtOpCurrent.set_text(
            str(fmt.format(self._hardware_model.operating_current)))
        self.txtRatedPower.set_text(
            str(fmt.format(self._hardware_model.rated_power)))
        self.txtOpPower.set_text(
            str(fmt.format(self._hardware_model.operating_power)))
        self.txtTempRise.set_text(
            str(fmt.format(self._hardware_model.temperature_rise)))

        # Load the component-specific information.
        if self._hardware_model.part == 1:
            self.cmbHRModel.set_active(
                int(self._hardware_model.hazard_rate_type))
            self.txtKneeTemp.set_text(
                str('{0:0.2f}'.format(self._hardware_model.knee_temperature)))
            self.txtThetaJC.set_text(
                str(self._hardware_model.thermal_resistance))
            self.txtCaseTemp.set_text(
                str(fmt.format(self._hardware_model.junction_temperature)))

            self._create_component_inputs()

        else:
            if self.vpnReliabilityInputs.get_child2() is not None:
                self.vpnReliabilityInputs.remove(
                    self.vpnReliabilityInputs.get_child2())

            self.cmbCostMethod.set_active(int(self._hardware_model.cost_type))

        return False

    def _load_assessment_results_page(self):
        """
        Method to load the assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'

        self.txtActiveHt.set_text(
            str(fmt.format(self._hardware_model.hazard_rate_active)))
        self.txtDormantHt.set_text(
            str(fmt.format(self._hardware_model.hazard_rate_dormant)))
        self.txtSoftwareHt2.set_text(
            str(fmt.format(self._hardware_model.hazard_rate_software)))
        self.txtPredictedHt.set_text(
            str(fmt.format(self._hardware_model.hazard_rate_logistics)))
        self.txtMissionHt.set_text(
            str(fmt.format(self._hardware_model.hazard_rate_mission)))
        self.txtHtPerCent.set_text(
            str(fmt.format(self._hardware_model.hazard_rate_percent)))

        self.txtMTBF.set_text(
            str('{0:0.2f}'.format(self._hardware_model.mtbf_logistics)))
        self.txtMissionMTBF.set_text(
            str('{0:0.2f}'.format(self._hardware_model.mtbf_mission)))

        self.txtReliability.set_text(
            str(fmt.format(self._hardware_model.reliability_logistics)))
        self.txtMissionRt.set_text(
            str(fmt.format(self._hardware_model.reliability_mission)))

        self.txtMPMT.set_text(
            str('{0:0.2f}'.format(self._hardware_model.mpmt)))
        self.txtMCMT.set_text(
            str('{0:0.2f}'.format(self._hardware_model.mcmt)))
        self.txtMTTR.set_text(
            str('{0:0.2f}'.format(self._hardware_model.mttr)))

        self.txtMMT.set_text(str('{0:0.2f}'.format(self._hardware_model.mmt)))

        self.txtAvailability.set_text(
            str(fmt.format(self._hardware_model.availability_logistics)))
        self.txtMissionAt.set_text(
            str(fmt.format(self._hardware_model.availability_mission)))

        self.txtTotalCost.set_text(
            str(locale.currency(self._hardware_model.cost)))
        self.txtCostFailure.set_text(
            str(locale.currency(self._hardware_model.cost_failure)))
        self.txtCostHour.set_text(
            str('${0:0.4g}'.format(self._hardware_model.cost_hour)))

        # Load the component-specific results.
        if self._hardware_model.part == 1:
            self.txtCurrentRatio.set_text(
                str(fmt.format(self._hardware_model.current_ratio)))
            self.txtPwrRatio.set_text(
                str(fmt.format(self._hardware_model.power_ratio)))
            self.txtVoltageRatio.set_text(
                str(fmt.format(self._hardware_model.voltage_ratio)))

            self.chkOverstressed.set_active(self._hardware_model.overstress)
            self.txtOSReason.set_text(self._hardware_model.reason)

            self._create_component_results()

        else:
            if self.vpnReliabilityResults.get_child2() is not None:
                self.vpnReliabilityResults.remove(
                    self.vpnReliabilityResults.get_child2())

            self.fraDerate.hide()

            self.txtPartCount.set_text(
                str(fmt.format(self._hardware_model.total_part_quantity)))
            self.txtTotalPwr.set_text(
                str(fmt.format(self._hardware_model.total_power_dissipation)))

        return False

    def _create_component_inputs(self):
        """
        Method to create the component-specific assessment input widgets.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # WARNING: Refactor _create_component_inputs; current McCabe Complexity metric = 19.
        if self.vpnReliabilityInputs.get_child2() is not None:
            self.vpnReliabilityInputs.remove(
                self.vpnReliabilityInputs.get_child2())

        if self._hardware_model.category_id == 1:
            self._obj_inputs = gCapacitor.Inputs(self._hardware_model)
        elif self._hardware_model.category_id == 2:
            self._obj_inputs = gConnection.Inputs(self._hardware_model)
        elif self._hardware_model.category_id == 3:
            self._obj_inputs = gInductor.Inputs(self._hardware_model)
        elif self._hardware_model.category_id == 4:
            self._obj_inputs = gIntegratedCircuit.Inputs(self._hardware_model)
        elif self._hardware_model.category_id == 5:
            self._obj_inputs = gMeter.Inputs(self._hardware_model)
        elif self._hardware_model.category_id == 6:
            if self._hardware_model.subcategory_id == 1:
                self._obj_inputs = gCrystal.Inputs(self._hardware_model)
            elif self._hardware_model.subcategory_id == 2:
                self._obj_inputs = gFilter.Inputs(self._hardware_model)
            elif self._hardware_model.subcategory_id == 3:
                self._obj_inputs = gFuse.Inputs(self._hardware_model)
            elif self._hardware_model.subcategory_id == 4:
                self._obj_inputs = gLamp.Inputs(self._hardware_model)
        elif self._hardware_model.category_id == 7:
            self._obj_inputs = gRelay.Inputs(self._hardware_model)
        elif self._hardware_model.category_id == 8:
            self._obj_inputs = gResistor.Inputs(self._hardware_model)
        elif self._hardware_model.category_id == 9:
            self._obj_inputs = gSemiconductor.Inputs(self._hardware_model)
        elif self._hardware_model.category_id == 10:
            self._obj_inputs = gSwitch.Inputs(self._hardware_model)

        if self._obj_inputs is not None:
            self.vpnReliabilityInputs.pack2(self._obj_inputs, True, True)

        if (self._hardware_model.hazard_rate_type == 1
                and self._hardware_model.category_id > 0
                and self._hardware_model.subcategory_id > 0):
            self._obj_inputs.create_217_count_inputs(x_pos=5)
            self._obj_inputs.load_217_count_inputs(self._hardware_model)
        elif (self._hardware_model.hazard_rate_type == 2
              and self._hardware_model.category_id > 0
              and self._hardware_model.subcategory_id > 0):
            self._obj_inputs.create_217_stress_inputs(x_pos=5)
            self._obj_inputs.load_217_stress_inputs(self._hardware_model)

        self.vpnReliabilityInputs.show_all()

        return False

    def _create_component_results(self):
        """
        Method to create the component-specific assessment results widgets.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # WARNING: Refactor _create_component_results; current McCabe Complexity metric = 19.
        if self._hardware_model.category_id == 1:
            self._obj_results = gCapacitor.Results(self._hardware_model)
        elif self._hardware_model.category_id == 2:
            self._obj_results = gConnection.Results(self._hardware_model)
        elif self._hardware_model.category_id == 3:
            self._obj_results = gInductor.Results(self._hardware_model)
        elif self._hardware_model.category_id == 4:
            self._obj_results = gIntegratedCircuit.Results(
                self._hardware_model)

        elif self._hardware_model.category_id == 5:
            self._obj_results = gMeter.Results(self._hardware_model)
        elif self._hardware_model.category_id == 6:
            if self._hardware_model.subcategory_id == 1:
                self._obj_results = gCrystal.Results(self._hardware_model)
            elif self._hardware_model.subcategory_id == 2:
                self._obj_results = gFilter.Results(self._hardware_model)
            elif self._hardware_model.subcategory_id == 3:
                self._obj_results = gFuse.Results(self._hardware_model)
            elif self._hardware_model.subcategory_id == 4:
                self._obj_results = gLamp.Results(self._hardware_model)
        elif self._hardware_model.category_id == 7:
            self._obj_results = gRelay.Results(self._hardware_model)
        elif self._hardware_model.category_id == 8:
            self._obj_results = gResistor.Results(self._hardware_model)
        elif self._hardware_model.category_id == 9:
            self._obj_results = gSemiconductor.Results(self._hardware_model)
        elif self._hardware_model.category_id == 10:
            self._obj_results = gSwitch.Results(self._hardware_model)

        if self.vpnReliabilityResults.get_child2() is not None:
            self.vpnReliabilityResults.remove(
                self.vpnReliabilityResults.get_child2())

        if self._obj_results is not None:
            self.vpnReliabilityResults.pack2(self._obj_results, True, True)

        if self.fraDerate.get_child() is not None:
            self.fraDerate.remove(self.fraDerate.get_child())

        if (self._hardware_model.hazard_rate_type == 1
                and self._hardware_model.category_id > 0
                and self._hardware_model.subcategory_id > 0):
            self._obj_results.create_217_count_results(x_pos=5)
            self._obj_results.load_217_count_results(self._hardware_model)
        elif (self._hardware_model.hazard_rate_type == 2
              and self._hardware_model.category_id > 0
              and self._hardware_model.subcategory_id > 0):
            self._obj_results.create_217_stress_results(x_pos=5)
            self._obj_results.load_217_stress_results(self._hardware_model)
            self._obj_results.load_derate_plot(self._hardware_model,
                                               self.fraDerate)

        self.vpnReliabilityResults.show_all()

        return False

    def _on_button_clicked(self, __button, index):
        """
        Method to respond to gtk.Button() clicked signals and call the correct
        function or method, passing any parameters as needed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if index == 0:  # Add sibling assembly.
            # Find the parent hardware item.
            (_model,
             _row) = self._modulebook.treeview.get_selection().get_selected()
            _row = _model.iter_parent(_row)
            self._request_add_hardware(0, _model, _row)

        elif index == 1:  # Add child assembly.
            # Find the parent hardware item.
            (_model,
             _row) = self._modulebook.treeview.get_selection().get_selected()

            self._request_add_hardware(0, _model, _row)

        elif index == 2:  # Add component.
            # Find the parent hardware item.
            (_model,
             _row) = self._modulebook.treeview.get_selection().get_selected()

            self._request_add_hardware(1, _model, _row)

        elif index == 3:
            self._request_delete_hardware()

        elif index == 4:
            self.dtcBoM.save_hardware_item(self._hardware_model.hardware_id)

        elif index == 5:
            self.dtcBoM.save_bom()

        elif index == 50:
            self.dtcBoM.request_calculate(self._hardware_model.hardware_id)
            self._load_assessment_results_page()
            self._modulebook.update_all()

        elif index == 51:
            self.dtcBoM.request_calculate(0)
            self._load_assessment_results_page()

            self._modulebook.update_all()

        return False

    def _request_add_hardware(self, hardware_type, model, piter):
        """
        Method to call the BoM data controller function 'add_hardware' and
        then update the Hardware Work Book gtk.TreeView() with the newly added
        hardware item.

        :param int hardware_type: the type of Hardware item to add.
                                  * 0 = Assembly
                                  * 1 = Component
        :param gtk.TreeModel model: the gtk.TreeModel() displaying the Hardware
                                    hierarchy.
        :param gtk.TreeIter piter: the gtk.TreeIter() that will be the parent
                                   of the newly added hardware item.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _parent_id = model.get_value(piter, 1)

        # Add the new hardware item to the database and dtcBoM dictionary.
        (_hardware, _error_code) = self.dtcBoM.add_hardware(
            self._hardware_model.revision_id, hardware_type, _parent_id)

        # If the Hardware Item was successfully added, add a record to the
        # Similar Item table, FMEA table, and PoF table.  Add a row to the
        # matrix table for the Hardware/Testing and Hardware/Validation
        # matrices.  If the Hardware item was an Assembly, add a column to the
        # Function/Hardware and Requirement/Hardware matrices.
        if _error_code == 0:
            _hardware.ref_des = "Ref. Des."
            self.dtcSimilarItem.add_similar_item(_hardware.hardware_id,
                                                 _parent_id)
            self.dtcFMECA.add_fmea(_hardware.hardware_id)
            self.dtcPoF.add_pof(_hardware.hardware_id)

            # If the Hardware Item was an Assembly, add a record to the
            # Allocation table.
            if hardware_type == 0:
                _hardware.name = _(u"New Assembly")
                self.dtcAllocation.add_allocation(_hardware.hardware_id,
                                                  _parent_id)

                # Update the module book view to show the new assembly.
                _icon = Configuration.ICON_DIR + '32x32/assembly.png'
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)

                _data = list(_hardware.get_attributes()) + \
                        [0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                         0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '',
                         '', '', '', ''] + [_icon]

            elif hardware_type == 1:
                _hardware.name = _(u"New Component")
                # Update the module book view to show the new component.
                _icon = Configuration.ICON_DIR + '32x32/component.png'
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)

                _data = list(_hardware.get_attributes()) + \
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                         0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', '',
                         '', ''] + [_icon]

            for _matrix_id in [0, 3]:
                self._modulebook.mdcRTK.dtcMatrices.add_column(
                    _matrix_id, _hardware.hardware_id)

            for _matrix_id in [6, 7]:
                self._modulebook.mdcRTK.dtcMatrices.add_row(
                    _matrix_id,
                    _hardware.parent_id,
                    _hardware.hardware_id,
                    val1=_hardware.ref_des,
                    val2=_hardware.name)

            model.append(piter, _data)
            self._modulebook.treeview.expand_all()

        return False

    def _request_delete_hardware(self):
        """
        Method to call the BoM data controller function 'delete_hardware' and
        then update the Hardware Work Book gtk.TreeView().

        :param gtk.TreeModel model: the gtk.TreeModel() holding the Hardware
                                    data.
        :param gtk.TreeIter row: the gtk.TreeIter() that will be removed from
                                 the gtk.TreeModel().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Find the selected hardware item.
        _selection = self._modulebook.treeview.get_selection()
        (_model, _row) = _selection.get_selected()

        # Delete the selected hardware item from the database and the
        # Hardware data controller dictionary.
        self.dtcBoM.delete_hardware(self._hardware_model.hardware_id)

        # Delete the Similar Item analysis associated with the Hardware item.
        self.dtcSimilarItem.delete_similar_item(
            self._hardware_model.hardware_id)

        # Delete the Hazards associated with the Hardware item.
        _hazards = [
            _key for _key in self.dtcHazard.dicHazard.keys()
            if _key[0] == self._hardware_model.hardware_id
        ]
        for __, _hazard in enumerate(_hazards):
            self.dtcHazard.delete_hazard(_hazard[0], _hazard[1])

        # If the Hardware item was an Assembly, delete the associated
        # Allocation.
        if self._hardware_model.part == 0:
            self.dtcAllocation.delete_allocation(
                self._hardware_model.hardware_id)

        # Refresh the Hardware gtkTreeView().
        if _row is not None:
            _path = _model.get_path(_row)
            _model.remove(_row)
            _selection.select_path(_path)

        return False

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
        # TODO: Consider refactoring _on_combo_changed; current McCabe Complexity metric = 12.
        combo.handler_block(self._lst_handler_id[index])

        if index == 3:  # Component category.
            # Find the database index of the newly selected component.
            _model = self.cmbCategory.get_model()
            _row = self.cmbCategory.get_active_iter()
            _index = int(_model.get_value(_row, 1))
            self._hardware_model.category_id = combo.get_active()

            # Get the list of subcategories for the selected category.
            try:
                _subcats = Configuration.RTK_SUBCATEGORIES[_index]
            except KeyError:
                _subcats = []

            _n_subcats = len(_subcats)

            # Load the subcategory gtk.ComboBox() with the appropriate list
            # of subcategories.
            _model = self.cmbSubcategory.get_model()
            _model.clear()
            _model.append(None, ['', 0, ''])
            for i in range(_n_subcats):
                _model.append(None, [_subcats[i][1], _subcats[i][0], ''])
            self.cmbSubcategory.show()

        elif index == 4:  # Component subcategory.
            self._hardware_model.subcategory_id = combo.get_active()

            # Get the attributes from the current Hardware data model and
            # pad them with the extra attributes of an Assembly.
            _attributes = self._hardware_model.get_attributes()
            _attributes = _attributes[:86] + (0.0, 0.0, 0.0, 0.0) + \
                          _attributes[86:]

            # Retrieve the appropriate data model for the newly selected
            # component and set it's attributes using the attributes of the
            # previously selected Component.  Not all attributes will map,
            # but this will reduce the amount of rework needed for the user
            # to update the attributes of the new Component.
            _hardware = self.dtcBoM.load_component(_attributes)

            # Update the BoM data controller dictionary and the Hardware
            # Work View with the new Hardware model instance.
            self.dtcBoM.dicHardware[
                self._hardware_model.hardware_id] = _hardware
            self._hardware_model = _hardware

            # Load the new attributes.
            if self._hardware_model.subcategory_id > 0:
                self._load_assessment_inputs_page()
                self._load_assessment_results_page()

        elif index == 9:  # Manufacturer.
            self._hardware_model.manufacturer = combo.get_active()
        elif index == 22:  # Active environment.
            self._hardware_model.environment_active = combo.get_active()
        elif index == 24:  # Dormant environment.
            self._hardware_model.environment_dormant = combo.get_active()
        elif index == 30:  # Hazard rate method.
            self._hardware_model.hazard_rate_method = combo.get_active()
        elif index == 31:  # Hazard rate prediction model.
            self._hardware_model.hazard_rate_type = combo.get_active()
            self._load_assessment_inputs_page()
            self._load_assessment_results_page()
        elif index == 37:  # Failure distribution.
            self._hardware_model.failure_dist = combo.get_active()
        elif index == 48:  # Cost calculation method.
            self._hardware_model.cost_type = combo.get_active()

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):  # pylint: disable=R0912
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
        # FIXME: Refactor _on_focus_out; current McCabe Complexity metric = 45.
        entry.handler_block(self._lst_handler_id[index])

        if index == 0:
            self._hardware_model.name = entry.get_text()
            self._modulebook.update(19, entry.get_text())
        elif index == 1:
            self._hardware_model.part_number = entry.get_text()
            self._modulebook.update(25, entry.get_text())
        elif index == 2:
            self._hardware_model.alt_part_number = entry.get_text()
            self._modulebook.update(2, entry.get_text())
        elif index == 5:
            self._hardware_model.ref_des = entry.get_text()
            self._modulebook.update(27, entry.get_text())
        elif index == 6:
            self._hardware_model.comp_ref_des = entry.get_text()
            self._modulebook.update(5, entry.get_text())
        elif index == 7:
            self._hardware_model.quantity = int(entry.get_text())
            self._modulebook.update(26, int(entry.get_text()))
        elif index == 8:
            self._hardware_model.description = entry.get_text()
            self._modulebook.update(9, entry.get_text())
        elif index == 10:
            self._hardware_model.cage_code = entry.get_text()
            self._modulebook.update(4, entry.get_text())
        elif index == 11:
            self._hardware_model.lcn = entry.get_text()
            self._modulebook.update(15, entry.get_text())
        elif index == 12:
            self._hardware_model.nsn = entry.get_text()
            self._modulebook.update(20, entry.get_text())
        elif index == 13:
            self._hardware_model.year_of_manufacture = int(entry.get_text())
            self._modulebook.update(37, int(entry.get_text()))
        elif index == 14:
            self._hardware_model.specification_number = entry.get_text()
            self._modulebook.update(32, entry.get_text())
        elif index == 15:
            self._hardware_model.page_number = entry.get_text()
            self._modulebook.update(22, entry.get_text())
        elif index == 16:
            self._hardware_model.figure_number = entry.get_text()
            self._modulebook.update(13, entry.get_text())
        elif index == 17:
            self._hardware_model.attachments = entry.get_text()
            self._modulebook.update(3, entry.get_text())
        elif index == 18:
            self._hardware_model.mission_time = float(entry.get_text())
            self._modulebook.update(18, float(entry.get_text()))
        elif index == 21:
            _textbuffer = self.txtRemarks.get_child().get_child().get_buffer()
            _text = _textbuffer.get_text(*_textbuffer.get_bounds())
            self._hardware_model.remarks = _text
            self._modulebook.update(30, _text)
        elif index == 23:
            self._hardware_model.temperature_active = float(entry.get_text())
            self._modulebook.update(34, float(entry.get_text()))
        elif index == 25:
            self._hardware_model.temperature_dormant = float(entry.get_text())
            self._modulebook.update(35, float(entry.get_text()))
        elif index == 26:
            self._hardware_model.duty_cycle = float(entry.get_text())
            self._modulebook.update(10, float(entry.get_text()))
        elif index == 27:
            self._hardware_model.humidity = float(entry.get_text())
            self._modulebook.update(14, float(entry.get_text()))
        elif index == 28:
            self._hardware_model.vibration = float(entry.get_text())
            self._modulebook.update(36, float(entry.get_text()))
        elif index == 29:
            self._hardware_model.rpm = float(entry.get_text())
            self._modulebook.update(31, float(entry.get_text()))
        elif index == 32:
            self._hardware_model.hazard_rate_specified = float(
                entry.get_text())
            self._modulebook.update(67, float(entry.get_text()))
        elif index == 33:
            self._hardware_model.mtbf_specified = float(entry.get_text())
            self._modulebook.update(76, float(entry.get_text()))
        elif index == 34:
            self._hardware_model.hazard_rate_software = float(entry.get_text())
            self._modulebook.update(66, float(entry.get_text()))
        elif index == 35:
            self._hardware_model.add_adj_factor = float(entry.get_text())
            self._modulebook.update(50, float(entry.get_text()))
        elif index == 36:
            self._hardware_model.mult_adj_factor = float(entry.get_text())
            self._modulebook.update(80, float(entry.get_text()))
        elif index == 38:  # Failure distribution scale
            self._hardware_model.failure_parameter_1 = float(entry.get_text())
            self._modulebook.update(56, float(entry.get_text()))
        elif index == 39:  # Failure distribution shape
            self._hardware_model.failure_parameter_2 = float(entry.get_text())
            self._modulebook.update(57, float(entry.get_text()))
        elif index == 40:  # Failure distribution location
            self._hardware_model.failure_parameter_3 = float(entry.get_text())
            self._modulebook.update(58, float(entry.get_text()))
        elif index == 49:
            self._hardware_model.cost = float(entry.get_text().strip('$'))
            self._modulebook.update(6, float(entry.get_text().strip('$')))
        elif index == 50:
            self._hardware_model.min_rated_temperature = float(
                entry.get_text())

            self._modulebook.update(40, float(entry.get_text()))
        elif index == 51:
            self._hardware_model.knee_temperature = float(entry.get_text())
            self._modulebook.update(93, float(entry.get_text()))
        elif index == 52:
            self._hardware_model.max_rated_temperature = float(
                entry.get_text())
            self._modulebook.update(39, float(entry.get_text()))
        elif index == 53:
            self._hardware_model.rated_voltage = float(entry.get_text())
            self._modulebook.update(47, float(entry.get_text()))
        elif index == 54:
            self._hardware_model.operating_voltage = float(entry.get_text())
            self._modulebook.update(43, float(entry.get_text()))
        elif index == 55:
            self._hardware_model.rated_current = float(entry.get_text())
            self._modulebook.update(45, float(entry.get_text()))
        elif index == 56:
            self._hardware_model.operating_current = float(entry.get_text())
            self._modulebook.update(41, float(entry.get_text()))
        elif index == 57:
            self._hardware_model.rated_power = float(entry.get_text())
            self._modulebook.update(46, float(entry.get_text()))
        elif index == 58:
            self._hardware_model.operating_power = float(entry.get_text())
            self._modulebook.update(42, float(entry.get_text()))
        elif index == 59:
            self._hardware_model.thermal_resistance = float(entry.get_text())
            self._modulebook.update(94, float(entry.get_text()))
        elif index == 60:
            self._hardware_model.temperature_rise = float(entry.get_text())
            self._modulebook.update(48, float(entry.get_text()))
        elif index == 61:
            self._hardware_model.case_temperature = float(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_toggled(self, check, index):
        """
        Responds to gtk.CheckButton() toggled signals and calls the correct
        function or method, passing any parameters as needed.

        :param gtk.CheckButton check: the gtk.CheckButton() that called this
                                      method.
        :param int index: the index in the handler ID list oc the callback
                          signal associated with the gtk.CheckButton() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        check.handler_block(self._lst_handler_id[index])

        if index == 19:  # Repairable
            self._hardware_model.repairable = int(check.get_active())
        elif index == 20:  # Tagged part
            self._hardware_model.tagged_part = int(check.get_active())

        check.handler_unblock(self._lst_handler_id[index])

        return False
