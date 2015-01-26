#!/usr/bin/env python
"""
###############################
Hardware Package Work Book View
###############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.WorkBook.py is part of The RTK Project
#
# All rights reserved.

import sys

# Modules required for the GUI.
import pango
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

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
    import utilities as _util
    import widgets as _widg
    from analyses.allocation.gui.gtk.WorkBook import WorkView as Allocation
    from analyses.hazard.gui.gtk.WorkBook import WorkView as Hazard
    from analyses.similar_item.gui.gtk.WorkBook import WorkView as SimilarItem
    from analyses.fmea.gui.gtk.WorkBook import WorkView as FMECA
    from analyses.pof.gui.gtk.WorkBook import WorkView as PoF
except ImportError:
    import rtk.configuration as _conf
    import rtk.utilities as _util
    import rtk.widgets as _widg
    from rtk.analyses.allocation.gui.gtk.WorkBook import WorkView as Allocation
    from rtk.analyses.hazard.gui.gtk.WorkBook import WorkView as Hazard
    from rtk.analyses.similar_item.gui.gtk.WorkBook import WorkView as SimilarItem
    from rtk.analyses.fmea.gui.gtk.WorkBook import WorkView as FMECA
    from rtk.analyses.pof.gui.gtk.WorkBook import WorkView as PoF
import gui.gtk.Capacitor
# from Assistants import AddHardware

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext

# TODO: Fix all docstrings; copy-paste errors.
class WorkView(gtk.VBox):                   # pylint: disable=R0902, R0904
    """
    The Work Book view displays all the attributes for the selected
    Requirement.  The attributes of a Work Book view are:

    :ivar _workview: the RTK top level Work View window to embed the
                     Requirement Work Book into.
    :ivar _function_model: the Function data model whose attributes are being
                           displayed.

    :ivar _dic_definitions: dictionary containing pointers to the failure
                            definitions for the Revision being displayed.  Key
                            is the Failure Definition ID; value is the pointer
                            to the Failure Definition data model.

    :ivar _lst_handler_id: list containing the ID's of the callback signals for
                           each gtk.Widget() associated with an editable
                           Hardware attribute.

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtName `focus_out_event`                 |
    +----------+-------------------------------------------+
    |     1    | txtPartNum `focus_out_event`              |
    +----------+-------------------------------------------+
    |     2    | txtAltPartNum `focus_out_event`           |
    +----------+-------------------------------------------+
    |     3    | cmbCategory `changed`                     |
    +----------+-------------------------------------------+
    |     4    | cmbSubcategory `changed`                  |
    +----------+-------------------------------------------+
    |     5    | txtRefDes `focus_out_event`               |
    +----------+-------------------------------------------+
    |     6    | txtCompRefDes `focus_out_event`           |
    +----------+-------------------------------------------+
    |     7    | txtQuantity `focus_out_event`             |
    +----------+-------------------------------------------+
    |     8    | txtDescription `focus_out_event`          |
    +----------+-------------------------------------------+
    |     9    | cmbManufacturer `changed`                 |
    +----------+-------------------------------------------+
    |    10    | txtCAGECode `focus_out_event`             |
    +----------+-------------------------------------------+
    |    11    | txtLCN `focus_out_event`                  |
    +----------+-------------------------------------------+
    |    12    | txtNSN `focus_out_event`                  |
    +----------+-------------------------------------------+
    |    13    | txtYearMade `focus_out_event`             |
    +----------+-------------------------------------------+
    |    14    | txtSpecification `focus_out_event`        |
    +----------+-------------------------------------------+
    |    15    | txtPageNum `focus_out_event`              |
    +----------+-------------------------------------------+
    |    16    | txtFigNum `focus_out_event`               |
    +----------+-------------------------------------------+
    |    17    | txtAttachments `focus_out_event`          |
    +----------+-------------------------------------------+
    |    18    | txtMissionTime `focus_out_event`          |
    +----------+-------------------------------------------+
    |    19    | chkRepairable `toggled`                   |
    +----------+-------------------------------------------+
    |    20    | chkTagged `toggled`                       |
    +----------+-------------------------------------------+
    |    21    | txtRemarks `focus_out_event`              |
    +----------+-------------------------------------------+

    :ivar dtcHardware: the :class:`rtk.hardware.Hardware.Hardware` data
                       controller to use with this Work Book.

    :ivar chkSafetyCritical: the :class:`gtk.CheckButton` to display/edit the
                             Function's safety criticality.

    :ivar txtCode: the :class:`gtk.Entry` to display/edit the Function code.
    :ivar txtName: the :class:`gtk.Entry` to display/edit the Function name.
    :ivar txtTotalCost: the :class:`gtk.Entry` to display the Function cost.
    :ivar txtModeCount: the :class:`gtk.Entry` to display the number of
                        hardware failure modes the Function is susceptible to.
    :ivar txtPartCount: the :class:`gtk.Entry` to display the number of
                        hardware components comprising the Function.
    :ivar txtRemarks: the :class:`gtk.Entry` to display/edit the Function
                      remarks.
    :ivar txtPredictedHt: the :class:`gtk.Entry` to display the Function
                          logistics hazard rate.
    :ivar txtMissionHt: the :class:`gtk.Entry` to display the Function mission
                        hazard rate.
    :ivar txtMTBF: the :class:`gtk.Entry` to display the Function logistics
                   MTBF.
    :ivar txtMissionMTBF: the :class:`gtk.Entry` to display the Function
                          mission MTBF.
    :ivar txtMPMT: the :class:`gtk.Entry` to display the Function mean
                   preventive maintenance time.
    :ivar txtMCMT: the :class:`gtk.Entry` to display the Function mean
                   corrective maintenance time.
    :ivar txtMTTR: the :class:`gtk.Entry` to display the Function mean time to
                   repair.
    :ivar txtMMT: the :class:`gtk.Entry` to display the Function mean
                  maintenance time.
    :ivar txtAvailability: the :class:`gtk.Entry` to display the Function
                           logistics availability.
    :ivar txtMissionAt: the :class:`gtk.Entry` to display the Function mission
                        availability.
    """

    def __init__(self, workview, modulebook):
        """
        Initializes the Work Book view for the Requirement package.

        :param rtk.gui.gtk.mwi.WorkView workview: the Work View container to
                                                  insert this Work Book into.
        :param rtk.function.ModuleBook: the Function Module Book to associate
                                        with this Work Book.
        """

        gtk.VBox.__init__(self)

        # Initialize private scalar attributes.
        self._workview = workview
        self._modulebook = modulebook
        self._hardware_model = None
        #self._stakeholder_model = None

        # Initialize private dict attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize public scalar attributes.
        self.dtcHardware = modulebook.dtcHardware

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
        self.txtQuantity = _widg.make_entry(width=50)
        self.txtDescription = _widg.make_entry(width=700)
        self.txtCAGECode = _widg.make_entry()
        self.txtLCN = _widg.make_entry()
        self.txtNSN = _widg.make_entry()
        self.txtYearMade = _widg.make_entry(width=100)
        self.txtSpecification = _widg.make_entry()
        self.txtPageNum = _widg.make_entry()
        self.txtFigNum = _widg.make_entry()
        self.txtImageFile = _widg.make_entry()
        self.txtAttachments = _widg.make_entry()
        self.txtMissionTime = _widg.make_entry(width=75)
        self.txtRevisionID = _widg.make_entry(width=50, editable=False)
        self.txtRemarks = _widg.make_text_view(width=400)

        # Allocation work book view.
        self.wbvwAllocation = Allocation(modulebook.dtcAllocation)

        # Hazard analysis work book view.
        self.wbvwHazard = Hazard(modulebook.dtcHazard)

        # Similar Item Analysis work book view.
        self.wbvwSimilarItem = SimilarItem(modulebook.dtcSimilarItem)

        # Failure Mode and Effects Analysis work book view.
        self.wbvwFMECA = FMECA(modulebook.dtcFMECA)

        # Physics of Failure Analysis work book view.
        self.wbvwPoF = PoF(modulebook.dtcPoF)

        # Assessment Input page widgets.
        self.cmbActEnviron = _widg.make_combo()
        self.cmbCostMethod = _widg.make_combo(200, 30)
        self.cmbDormantEnviron = _widg.make_combo()
        self.cmbFailDist = _widg.make_combo()
        self.cmbHRMethod = _widg.make_combo()
        self.cmbHRModel = _widg.make_combo()
        self.cmbMTTRMethod = _widg.make_combo()
        self.cmbRepairDist = _widg.make_combo()

        self.lblNoCategory = _widg.make_label(_(u"No category selected for "
                                                u"this part."),
                                              width=400)
        self.lblNoSubCategory = _widg.make_label(_(u"No subcategory selected "
                                                   u"for this part."),
                                                 width=400)

        self.txtActTemp = _widg.make_entry(width=100)
        self.txtAddAdj = _widg.make_entry(width=100)
        self.txtCaseTemp = _widg.make_entry(width=100)
        self.txtCost = _widg.make_entry(width=100)
        self.txtDormantTemp = _widg.make_entry(width=100)
        self.txtDutyCycle = _widg.make_entry(width=100)
        self.txtFailScale = _widg.make_entry(width=100)
        self.txtFailShape = _widg.make_entry(width=100)
        self.txtFailLoc = _widg.make_entry(width=100)
        self.txtHumidity = _widg.make_entry(width=100)
        self.txtKneeTemp = _widg.make_entry(width=100)
        self.txtMaxTemp = _widg.make_entry(width=100)
        self.txtMinTemp = _widg.make_entry(width=100)
        self.txtMTTRAddAdj = _widg.make_entry(width=100)
        self.txtMTTRMultAdj = _widg.make_entry(width=100)
        self.txtMultAdj = _widg.make_entry(width=100)
        self.txtOpCurrent = _widg.make_entry(width=100)
        self.txtOpPower = _widg.make_entry(width=100)
        self.txtOpVoltage = _widg.make_entry(width=100)
        self.txtRatedCurrent = _widg.make_entry(width=100)
        self.txtRatedPower = _widg.make_entry(width=100)
        self.txtRatedVoltage = _widg.make_entry(width=100)
        self.txtRepairScale = _widg.make_entry(width=100)
        self.txtRepairShape = _widg.make_entry(width=100)
        self.txtRPM = _widg.make_entry(width=100)
        self.txtSoftwareHt = _widg.make_entry(width=100)
        self.txtSpecifiedHt = _widg.make_entry(width=100)
        self.txtSpecifiedMTBF = _widg.make_entry(width=100)
        self.txtSpecifiedMTTR = _widg.make_entry(width=100)
        self.txtTempRise = _widg.make_entry(width=100)
        self.txtThetaJC = _widg.make_entry(width=100)
        self.txtVibration = _widg.make_entry(width=100)

        self.vpnReliabilityInputs = gtk.VPaned()

        # Assessment Results page widgets.
        self.chkOverstressed = _widg.make_check_button()

        self.figDerate = Figure(figsize=(6, 4))

        self.fraDerate = gtk.Frame()

        self.pltDerate = FigureCanvas(self.figDerate)

        self.txtActiveHt = _widg.make_entry(width=100, editable=False,
                                            bold=True)
        self.txtDormantHt = _widg.make_entry(width=100, editable=False,
                                             bold=True)
        self.txtSoftwareHt2 = _widg.make_entry(width=100, editable=False,
                                               bold=True)
        self.txtPredictedHt = _widg.make_entry(width=100, editable=False,
                                               bold=True)
        self.txtMissionHt = _widg.make_entry(width=100, editable=False,
                                             bold=True)
        self.txtHtPerCent = _widg.make_entry(width=100, editable=False,
                                             bold=True)
        self.txtMTBF = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtMissionMTBF = _widg.make_entry(width=100, editable=False,
                                               bold=True)
        self.txtReliability = _widg.make_entry(width=100, editable=False,
                                               bold=True)
        self.txtMissionRt = _widg.make_entry(width=100, editable=False,
                                             bold=True)
        self.txtMPMT = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtMCMT = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtMTTR = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtMMT = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtAvailability = _widg.make_entry(width=100, editable=False,
                                                bold=True)
        self.txtMissionAt = _widg.make_entry(width=100, editable=False,
                                             bold=True)
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

        self.vbxReliabilityResults = gtk.VBox()

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
        _button.set_tooltip_text(_(u"Adds a new assembly to the RTK Project "
                                   u"at the same hierarchy level as the "
                                   u"selected assembly."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
        _button.set_icon_widget(_image)
        #_button.connect('clicked', self.add_hardware, 0)
        _toolbar.insert(_button, _position)
        _position += 1

        # Add child assembly button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Adds a new assembly to the RTK Project "
                                   u"that is one level subordinate to the "
                                   u"selected assembly."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert_child.png')
        _button.set_icon_widget(_image)
        #self.btnAddChild.connect('clicked', self.add_hardware, 1)
        _toolbar.insert(_button, _position)
        _position += 1

        # Delete assembly button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Removes the currently selected hardware "
                                   u"item from the RTK Project."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        _button.set_icon_widget(_image)
        #_button.connect('clicked', self._delete_hardware)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save results button.  Depending on the notebook page selected will
        # determine which results are saved.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        #_button.connect('clicked', self._toolbutton_pressed)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Create report button.
        _button = gtk.MenuToolButton(None, label="")
        _button.set_tooltip_text(_(u"Create Hardware reports."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/reports.png')
        _button.set_icon_widget(_image)
        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"Allocation Report"))
        _menu_item.set_tooltip_text(_(u"Creates the reliability allocation "
                                      u"report for the currently selected "
                                      u"hardware item."))
        #_menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Hazards Analysis Report"))
        _menu_item.set_tooltip_text(_(u"Creates the hazards analysis report "
                                      u"for the currently selected hardware "
                                      u"item."))
        #_menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Similar Item Analysis Report"))
        _menu_item.set_tooltip_text(_(u"Creates the similar item analysis "
                                      u"report for the currently selected "
                                      u"hardware item."))
        #_menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"FMEA Report"))
        _menu_item.set_tooltip_text(_(u"Creates the FMEA/FMECA "
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
        _image.set_from_file(_conf.ICON_DIR + '32x32/db-import.png')
        _button.set_icon_widget(_image)
        _button.set_name('Import')
        #_button.connect('clicked', ImportHardware, self._app)
        _button.set_tooltip_text(_(u"Launches the hardware import assistant."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Create an export button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/db-export.png')
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
        if _conf.TABPOS[2] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif _conf.TABPOS[2] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif _conf.TABPOS[2] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        self._create_general_data_page(_notebook)

        # Insert the reliability Allocation page.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Allocation") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the reliability allocation for "
                                  u"the selected hardware item."))

        self.wbvwAllocation.create_page()
        _notebook.insert_page(self.wbvwAllocation, tab_label=_label,
                              position=-1)

        # Insert the Hazard Analysis page.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Hazard\nAnalysis") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the hazard analysis for the "
                                  u"selected hardware item."))

        self.wbvwHazard.create_page()
        _notebook.insert_page(self.wbvwHazard, tab_label=_label, position=-1)

        # Insert the Similar Item Analysis page.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Similar Item\nAnalysis") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the similar item analysis for "
                                  u"the selected assembly."))

        self.wbvwSimilarItem.create_page()
        _notebook.insert_page(self.wbvwSimilarItem, tab_label=_label,
                              position=-1)

        self._create_assessment_inputs_page(_notebook)
        self._create_assessment_results_page(_notebook)

        # Insert the Failure Mode and Effects Analysis page.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"FMEA\nWorksheet") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the failure mode and effects "
                                  u"analysis for the selected assembly."))

        self.wbvwFMECA.create_page()
        _notebook.insert_page(self.wbvwFMECA, tab_label=_label, position=-1)

        # Insert the Physics of Failure Analysis page.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Physics of\nFailure\nAnalysis") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the physics of failure analysis "
                                  u"for the selected assembly."))

        self.wbvwPoF.create_page()
        _notebook.insert_page(self.wbvwPoF, tab_label=_label, position=-1)

        return _notebook

    def _create_general_data_page(self, notebook):
        """
        Creates the Hardware class gtk.Notebook() page for displaying general
        data about the selected Hardware item.

        :param gtk.Notebook notebook: the Hardware class gtk.Notebook().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
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

        _frame = _widg.make_frame(label=_(u"General Information"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, True, True)

        # Build the quadrant 3 (lower left) containers.
        _fixed3 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed3)

        _frame = _widg.make_frame(label=_(u"Manufacturer Information"))
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

        _frame = _widg.make_frame(label=_(u"Specification Information"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, True, True)

        # Build the quadrant 4 (lower right) containers.
        _fixed4 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed4)

        _frame = _widg.make_frame(label=_(u"Miscellaneous Information"))
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
        for _cat in self._workview.RTK_CATEGORIES:
            _model.append(None, [self._workview.RTK_CATEGORIES[_cat][0],
                                 self._workview.RTK_CATEGORIES[_cat][1],
                                 ''])

        _model = self.cmbManufacturer.get_model()
        _model.clear()
        _model.append(None, ['', 0, ''])
        for _man in self._workview.RTK_MANUFACTURERS:
            _model.append(None, self._workview.RTK_MANUFACTURERS[_man])

        # Create the labels for quadrant #1.
        _labels = [_(u"Assembly Name:"), _(u"Part Number:"),
                   _(u"Alternate Part #:"), "", "", _(u"Ref Designator:"),
                   _(u"Composite Ref Des:"), _(u"Quantity:"),
                   _(u"Description:")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed1, 5, 5)

        # Create the labels for quadrant #3.
        _labels = [_(u"Manufacturer:"), _(u"CAGE Code:"), _(u"LCN:"),
                   _(u"NSN:"), _(u"Manufacture Year:")]
        (_x_pos2,
         _y_pos2) = _widg.make_labels(_labels, _fixed3, 5, 5)
        _x_pos = max(_x_pos, _x_pos2) + 50

        # Place the quadrant #1 widgets.
        self.txtName.set_tooltip_text(_(u"Displays the name of the selected "
                                        u"hardware item."))
        self.txtPartNum.set_tooltip_text(_(u"Displays the part number of "
                                           u"the selected hardware item."))
        self.txtAltPartNum.set_tooltip_text(_(u"Displays an alternative part "
                                              u"number for the selected "
                                              u"hardware item."))
        self.cmbCategory.set_tooltip_text(_(u"Select the part type for the "
                                            u"component."))
        self.cmbSubcategory.set_tooltip_text(_(u"Select the part sub-type "
                                               u"for the component."))
        self.txtRefDes.set_tooltip_text(_(u"Displays the reference "
                                          u"designator of the selected "
                                          u"hardware item."))
        self.txtCompRefDes.set_tooltip_text(_(u"Displays the composite "
                                              u"reference designator of "
                                              u"the selected hardware item."))
        self.txtQuantity.set_tooltip_text(_(u"Displays the quantity of "
                                            u"the selected hardware item."))
        self.txtDescription.set_tooltip_text(_(u"Displays the description "
                                               u"of the selected hardware "
                                               u"item."))

        _fixed1.put(self.txtName, _x_pos, _y_pos[0])
        _fixed1.put(self.txtPartNum, _x_pos, _y_pos[1])
        _fixed1.put(self.txtAltPartNum, _x_pos, _y_pos[2])
        _fixed1.put(self.lblCategory, 5, _y_pos[3])
        _fixed1.put(self.cmbCategory, _x_pos, _y_pos[3])
        _fixed1.put(self.lblSubcategory, 5, _y_pos[4])
        _fixed1.put(self.cmbSubcategory, _x_pos, _y_pos[4])
        _fixed1.put(self.txtRefDes, _x_pos, _y_pos[5])
        _fixed1.put(self.txtCompRefDes, _x_pos, _y_pos[6])
        _fixed1.put(self.txtQuantity, _x_pos, _y_pos[7])
        _fixed1.put(self.txtDescription, _x_pos, _y_pos[8])

        self._lst_handler_id.append(self.txtName.connect('focus-out-event',
                                                         self._on_focus_out,
                                                         0))
        self._lst_handler_id.append(self.txtPartNum.connect('focus-out-event',
                                                            self._on_focus_out,
                                                            1))
        self._lst_handler_id.append(
            self.txtAltPartNum.connect('focus-out-event',
                                       self._on_focus_out, 2))
        self._lst_handler_id.append(
            self.cmbCategory.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbSubcategory.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(self.txtRefDes.connect('focus-out-event',
                                                           self._on_focus_out,
                                                           5))
        self._lst_handler_id.append(
            self.txtCompRefDes.connect('focus-out-event',
                                       self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.txtQuantity.connect('focus-out-event', self._on_focus_out, 7))
        self._lst_handler_id.append(
            self.txtDescription.connect('focus-out-event',
                                        self._on_focus_out, 8))

        _fixed1.show_all()

        # Place the quadrant #3 widgets.
        self.cmbManufacturer.set_tooltip_text(_(u"Displays the manufacturer "
                                                u"of the selected hardware "
                                                u"item."))
        self.txtCAGECode.set_tooltip_text(_(u"Displays the Commercial and "
                                            u"Government Entity (CAGE) "
                                            u"code of the selected "
                                            u"hardware item."))
        self.txtLCN.set_tooltip_text(_(u"Displays the logistics control "
                                       u"number (LCN) of the selected "
                                       u"hardware item."))
        self.txtNSN.set_tooltip_text(_(u"Displays the national stock number "
                                       u"(NSN) of the selected hardware "
                                       u"item."))
        self.txtYearMade.set_tooltip_text(_(u"Displays the year the selected "
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
            self.txtCAGECode.connect('focus-out-event',
                                     self._on_focus_out, 10))
        self._lst_handler_id.append(
            self.txtLCN.connect('focus-out-event', self._on_focus_out, 11))
        self._lst_handler_id.append(
            self.txtNSN.connect('focus-out-event', self._on_focus_out, 12))
        self._lst_handler_id.append(
            self.txtYearMade.connect('focus-out-event',
                                     self._on_focus_out, 13))

        _fixed3.show_all()

        # Create the labels for quadrant #2.
        _labels = [_(u"Specification:"), _(u"Page Number:"),
                   _(u"Figure Number:"), _(u"Image File:"),
                   _(u"Attachments:"), _(u"Mission Time:")]
        (_x_pos,
         _y_pos) = _widg.make_labels(_labels, _fixed2, 5, 5)

        # Create the labels for quadrant #4.
        _labels = [_(u"Revision ID:"), _(u"Repairable?"), _(u"Tagged?"),
                   _(u"Remarks:")]
        (_x_pos2,
         _y_pos2) = _widg.make_labels(_labels, _fixed4, 5, 5)
        _x_pos = max(_x_pos, _x_pos2) + 50

        # Place the quadrant #2 widgets.
        self.txtSpecification.set_tooltip_text(_(u"Displays the governing "
                                                 u"specification for the "
                                                 u"selected hardware item, if "
                                                 u"any."))
        self.txtPageNum.set_tooltip_text(_(u"Displays the governing "
                                           u"specification page number "
                                           u"for the selected hardware item."))
        self.txtFigNum.set_tooltip_text(_(u"Displays the governing "
                                          u"specification figure number "
                                          u"for the selected hardware item."))
        self.txtImageFile.set_tooltip_text(_(u"Displays the URL to an "
                                             u"image of the selected "
                                             u"hardware item."))
        self.txtAttachments.set_tooltip_text(_(u"Displays the URL to an "
                                               u"attachment associated "
                                               u"with the selected "
                                               u"hardware item."))
        self.txtMissionTime.set_tooltip_text(_(u"Displays the mission time "
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
            self.txtAttachments.connect('focus-out-event',
                                        self._on_focus_out, 17))
        self._lst_handler_id.append(
            self.txtMissionTime.connect('focus-out-event',
                                        self._on_focus_out, 18))

        _fixed2.show_all()

        # Place the quadrant #4 widgets.
        self.txtRevisionID.set_tooltip_text(_(u"Displays the currently "
                                              u"selected revision."))
        self.chkRepairable.set_tooltip_text(_(u"Indicates whether or not "
                                              u"the selected hardware item is "
                                              u"repairable."))
        self.chkTagged.set_tooltip_text(_(u"Indicates whether or not the "
                                          u"selected hardware item is "
                                          u"tagged.  A tagged hardware item "
                                          u"has no specific meaning."))
        self.txtRemarks.set_tooltip_text(_(u"Enter any remarks associated "
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
        _label.set_markup("<span weight='bold'>" + _(u"General\nData") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays general information about "
                                  u"the selected assembly."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_assessment_inputs_page(self, notebook):
        """
        Creates the Hardware class gtk.Notebook() page for displaying the
        assessment inputs for the selected Hardware.

        :param gtk.Notebook notebook: the Hardware class gtk.Notebook() widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hpaned = gtk.HPaned()

        _hpaned2 = gtk.HPaned()
        _hpaned.pack1(_hpaned2, True, False)

        # --------------------------------------------------------------#
        # Build the quadrant 1 (left) container.                        #
        # --------------------------------------------------------------#
        # Add the layout for stress inputs.
        _fixed1 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed1)

        _frame = _widg.make_frame(label=_(u"Stress Inputs"))
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

        _frame = _widg.make_frame(label=_(u"Reliability Inputs"))
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

        _frame = _widg.make_frame(label=_(u"Maintainability Inputs"))
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

        _frame = _widg.make_frame(label=_(u"Miscellaneous Inputs"))
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
        for _idx in self._workview.RTK_HR_TYPE:
            self.cmbHRMethod.append_text(self._workview.RTK_HR_TYPE[_idx])

        _model = self.cmbHRModel.get_model()
        _model.clear()
        self.cmbHRModel.append_text("")
        for _idx in self._workview.RTK_HR_MODEL:
            self.cmbHRModel.append_text(self._workview.RTK_HR_MODEL[_idx])

        _model = self.cmbFailDist.get_model()
        _model.clear()
        self.cmbFailDist.append_text("")
        for _idx in self._workview.RTK_S_DIST:
            self.cmbFailDist.append_text(self._workview.RTK_S_DIST[_idx])

        _model = self.cmbActEnviron.get_model()
        _model.clear()
        self.cmbActEnviron.append_text("")
        for _idx in self._workview.RTK_ACTIVE_ENVIRON:
            self.cmbActEnviron.append_text(
                self._workview.RTK_ACTIVE_ENVIRON[_idx][0])

        _model = self.cmbDormantEnviron.get_model()
        _model.clear()
        self.cmbDormantEnviron.append_text("")
        for _idx in self._workview.RTK_DORMANT_ENVIRON:
            self.cmbDormantEnviron.append_text(
                self._workview.RTK_DORMANT_ENVIRON[_idx])

        # Create the labels for quadrant #1.
        _labels = [_(u"Active Environment:"), _(u"Active Temp:"),
                   _(u"Dormant Environment:"), _(u"Dormant Temp:"),
                   _(u"Duty Cycle:"), _(u"Humidity:"), _(u"Vibration:"),
                   _(u"RPM:"), _(u"Min Rated Temp:"), _(u"Knee Temp:"),
                   _(u"Max Rated Temp:"), _(u"Rated Voltage:"),
                   _(u"Operating Voltage:"), _(u"Rated Current:"),
                   _(u"Operating Current:"), _(u"Rated Power:"),
                   _(u"Operating Power:"), _(u"theta JC:"),
                   _(u"Temperature Rise:"), _(u"Case Temperature:")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed1, 5, 5)
        _x_pos += 50

        # Place the quadrant #1 widgets.
        self.cmbActEnviron.set_tooltip_text(_(u"Selects the active "
                                              u"operating environment for "
                                              u"the selected hardware item."))
        self.txtActTemp.set_tooltip_text(_(u"Displays the active "
                                           u"environment operating "
                                           u"temperature for the selected "
                                           u"hardware item."))
        self.cmbDormantEnviron.set_tooltip_text(_(u"Selects the dormant "
                                                  u"environment for the "
                                                  u"selected hardware item."))
        self.txtDormantTemp.set_tooltip_text(_(u"Displays the dormant "
                                               u"environment temperature "
                                               u"for the selected "
                                               u"hardware item."))
        self.txtDutyCycle.set_tooltip_text(_(u"Displays the operating "
                                             u"duty cycle for the "
                                             u"selected hardware item."))
        self.txtHumidity.set_tooltip_text(_(u"Displays the active "
                                            u"environment operating "
                                            u"humidity for the selected "
                                            u"hardware item."))
        self.txtVibration.set_tooltip_text(_(u"Displays the active "
                                             u"environment operating "
                                             u"vibration level for the "
                                             u"selected hardware item."))
        self.txtRPM.set_tooltip_text(_(u"Displays the active environment "
                                       u"operating RPM for the selected "
                                       u"hardware item."))
        self.txtMinTemp.set_tooltip_text(_(u"The minimum design operating "
                                           u"temperature for the selected"
                                           u"hardware item."))
        self.txtKneeTemp.set_tooltip_text(_(u"The knee temperature for "
                                            u"the selected hardware item."))
        self.txtMaxTemp.set_tooltip_text(_(u"The maximum design operating "
                                           u"temperature for the selected "
                                           u"hardware item."))
        self.txtRatedVoltage.set_tooltip_text(_(u"The maximum rated "
                                                u"voltage for the "
                                                u"selected hardware item."))
        self.txtOpVoltage.set_tooltip_text(_(u"The operating voltage for "
                                             u"the selected hardware item."))
        self.txtRatedCurrent.set_tooltip_text(_(u"The maximum rated "
                                                u"current for the "
                                                u"selected hardware item."))
        self.txtOpCurrent.set_tooltip_text(_(u"The operating current for "
                                             u"the selected hardware item."))
        self.txtRatedPower.set_tooltip_text(_(u"The maximum rated power "
                                              u"for the selected "
                                              u"hardware item."))
        self.txtOpPower.set_tooltip_text(_(u"The operating power for the "
                                           u"selected hardware item."))
        self.txtThetaJC.set_tooltip_text(_(u"The junction-to-case thermal "
                                           u"resistance for the selected "
                                           u"hardware item."))
        self.txtTempRise.set_tooltip_text(_(u"The ambient to case "
                                            u"temperature rise for the "
                                            u"selected hardware item."))
        self.txtCaseTemp.set_tooltip_text(_(u"The case temperature for "
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

        #self._lst_handler_id.append(self.cmbActEnviron.connect('changed', self._on_combo_changed, 30))
        #self._lst_handler_id.append(
        #    self.txtActTemp.connect('focus-out-event',
        #                            self._on_focus_out, 'float', 31))
        #self._lst_handler_id.append(self.cmbDormantEnviron.connect('changed', self._on_combo_changed, 32))
        #self._lst_handler_id.append(
        #    self.txtDormantTemp.connect('focus-out-event',
        #                                self._on_focus_out, 'float', 33))
        #self._lst_handler_id.append(
        #    self.txtDutyCycle.connect('focus-out-event',
        #                              self._on_focus_out, 'float', 34))
        #self._lst_handler_id.append(
        #    self.txtHumidity.connect('focus-out-event',
        #                             self._on_focus_out, 'float', 35))
        #self._lst_handler_id.append(
        #   self.txtVibration.connect('focus-out-event',
        #                             self._on_focus_out, 'float', 36))
        #self._lst_handler_id.append(
        #    self.txtRPM.connect('focus-out-event',
        #                        self._on_focus_out, 'float', 37))

        _labels = [_(u"Calculation Method:"), _(u"Calculation Model:"),
                   _(u"Specified h(t):"), _(u"Specified MTBF:"),
                   _(u"Software h(t):"), _(u"Additive Adj:"),
                   _(u"Multiplicative Adj:"), _(u"Failure Distribution:"),
                   _(u"Scale:"), _(u"Shape:"), _(u"Location:")]

        (_x_pos,
         _y_pos) = _widg.make_labels(_labels, _fixed2, 5, 5)

# TODO: Clean this up when working on the components.  This is a working prototype of the approach to use.
        _cap = gui.gtk.Capacitor.Capacitor()
        _x_pos2 = _cap._create_mil_hdbk_217_stress(_x_pos)
        self.vpnReliabilityInputs.pack2(_cap, True, True)
        _x_pos = max(_x_pos, _x_pos2)

        self.cmbHRMethod.set_tooltip_text(_(u"Selects the method of "
                                            u"assessing the hazard rate for "
                                            u"the selected hardware item."))
        self.cmbHRModel.set_tooltip_text(_(u"Selects the hazard rate model to "
                                           u"use when calculating the hazard "
                                           u"rate for the selected hardware "
                                           u"item."))
        self.txtSpecifiedHt.set_tooltip_text(_(u"Displays the specified "
                                               u"failure intensity for "
                                               u"the selected hardware item."))
        self.txtSpecifiedMTBF.set_tooltip_text(_(u"Displays the specified "
                                                 u"mean time between "
                                                 u"failure (MTBF) for the "
                                                 u"selected hardware item."))
        self.txtSoftwareHt.set_tooltip_text(_(u"Displays the software "
                                              u"failure rate for the "
                                              u"selected hardware item."))
        self.txtAddAdj.set_tooltip_text(_(u"Displays any hazard rate "
                                          u"assessment additive "
                                          u"adjustment factor for the "
                                          u"selected hardware item."))
        self.txtMultAdj.set_tooltip_text(_(u"Displays any hazard rate "
                                           u"assessment multiplicative "
                                           u"adjustment factor for the "
                                           u"selected hardware item."))
        self.cmbFailDist.set_tooltip_text(_(u"Selects the distribution of "
                                            u"times to failure for the "
                                            u"selected hardware item."))
        self.txtFailScale.set_tooltip_text(_(u"Displays the time to "
                                             u"failure distribution scale "
                                             u"factor for the selected "
                                             u"hardware item."))
        self.txtFailShape.set_tooltip_text(_(u"Displays the time to "
                                             u"failure distribution shape "
                                             u"factor for the selected "
                                             u"hardware item."))
        self.txtFailLoc.set_tooltip_text(_(u"Displays the time to failure "
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

        _fixed1.show_all()
        _fixed2.show_all()

        # Create the labels for quadrant #2.
        _labels = [_(u"MTTR Method:"), _(u"Specified MTTR:"),
                   _(u"Additive Adj:"), _(u"Multiplicative Adj:"),
                   _(u"Repair Distribution:"), _(u"Scale:"), _(u"Shape:")]

        (_x_pos,
         _y_pos) = _widg.make_labels(_labels, _fixed3, 5, 5)

        # Create the labels for quadrant #4.
        _labels = [_(u"Cost Method:"), _(u"Unit Cost:")]
        (_x_pos2,
         _y_pos2) = _widg.make_labels(_labels, _fixed4, 5, 5)
        _x_pos = max(_x_pos, _x_pos2) + 50

        # Place the quadrant #3 widgets.
        _model = self.cmbMTTRMethod.get_model()
        _model.clear()
        self.cmbMTTRMethod.append_text("")
        for _idx in self._workview.RTK_MTTR_TYPE:
            self.cmbMTTRMethod.append_text(self._workview.RTK_MTTR_TYPE[_idx])

        _model = self.cmbRepairDist.get_model()
        _model.clear()
        self.cmbRepairDist.append_text("")
        for _idx in self._workview.RTK_S_DIST:
            self.cmbRepairDist.append_text(self._workview.RTK_S_DIST[_idx])

        self.cmbMTTRMethod.set_tooltip_text(_(u"Selects the method of "
                                              u"assessing the mean time to "
                                              u"repair (MTTR) for the "
                                              u"selected hardware item."))
        self.txtSpecifiedMTTR.set_tooltip_text(_(u"Displays the specified "
                                                 u"mean time to repair "
                                                 u"(MTTR) for the "
                                                 u"selected hardware item."))
        self.txtMTTRAddAdj.set_tooltip_text(_(u"Displays the mean time to "
                                              u"repair (MTTR) assessment "
                                              u"additive adjustment "
                                              u"factor for the selected "
                                              u"hardware item."))
        self.txtMTTRMultAdj.set_tooltip_text(_(u"Displays the mean time "
                                               u"to repair (MTTR) "
                                               u"assessment multiplicative "
                                               u"adjustment factor for "
                                               u"the selected hardware item."))
        self.cmbRepairDist.set_tooltip_text(_(u"Selects the time to "
                                              u"repair distribution for "
                                              u"the selected hardware item."))
        self.txtRepairScale.set_tooltip_text(_(u"Displays the time to "
                                               u"repair distribution "
                                               u"scale parameter for the "
                                               u"selected hardware item."))
        self.txtRepairShape.set_tooltip_text(_(u"Displays the time to "
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

        # Place the quadrant #4 widgets.
        _model = self.cmbCostMethod.get_model()
        _model.clear()
        self.cmbCostMethod.append_text("")
        for _idx in self._workview.RTK_COST_TYPE:
            self.cmbCostMethod.append_text(self._workview.RTK_COST_TYPE[_idx])

        self.cmbCostMethod.set_tooltip_text(_(u"Select the method for "
                                              u"assessing the cost of the "
                                              u"selected hardware item."))
        self.txtCost.set_tooltip_text(_(u"The unit cost of the selected "
                                        u"hardware item."))

        _fixed4.put(self.cmbCostMethod, _x_pos, _y_pos2[0])
        _fixed4.put(self.txtCost, _x_pos, _y_pos2[1])

        #self._lst_handler_id.append(self.cmbCostType.connect('changed', self._on_combo_changed, 38))
        #self._lst_handler_id.append(
        #    self.txtCost.connect('focus-out-event',
        #                         self._on_focus_out, 'float', 39))

        _fixed3.show_all()
        _fixed4.show_all()

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Assessment\nInputs") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Allows entering reliability, "
                                  u"maintainability, and other assessment "
                                  u"inputs for the selected hardware item."))

        notebook.insert_page(_hpaned, tab_label=_label, position=-1)

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
        self.fraDerate = self.figDerate.add_subplot(111)

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

        _frame = _widg.make_frame(label=_(u"Operating Stress Results"))
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

        _frame = _widg.make_frame(label=_(u"Reliability Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hpaned2.pack2(_frame, True, False)

        # --------------------------------------------------------------#
        # Build the quadrant #3 (upper right) containers.               #
        # --------------------------------------------------------------#
        _vpaned = gtk.VPaned()
        _hpaned.pack2(_vpaned, True, False)

        _fixed3 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed3)

        _frame = _widg.make_frame(label=_(u"Maintainability Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, True, False)

        # --------------------------------------------------------------#
        # Build the quadrant #4 (lower right) containers.               #
        # --------------------------------------------------------------#
        _fixed4 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed4)

        _frame = _widg.make_frame(label=_(u"Miscellaneous Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack2(_frame, True, False)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display the assessment results.     #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the labels for quadrant #1.
        _labels = [_(u"Total Power Used:"), _(u"Voltage Ratio:"),
                   _(u"Current Ratio:"), _(u"Power Ratio:")]
        (_x_pos,
         _y_pos) = _widg.make_labels(_labels, _fixed1, 5, 5)
        _x_pos += 50
        #self._component_x[1] = _x_pos
        #self._component_y[1] = _y_pos3[3] + 170

        # Place the quadrant #1 widgets.
        self.txtTotalPwr.set_tooltip_text(_(u"The total power of the selected "
                                            u"hardware item."))
        self.txtVoltageRatio.set_tooltip_text(_(u"The ratio of operating "
                                                u"voltage to rated voltage "
                                                u"for the selected hardware "
                                                u"item."))
        self.txtCurrentRatio.set_tooltip_text(_(u"The ratio of operating "
                                                u"current to rated "
                                                u"current for the "
                                                u"selected hardware item."))
        self.txtPwrRatio.set_tooltip_text(_(u"The ratio of operating "
                                            u"power to rated power for "
                                            u"the selected hardware item."))
        self.chkOverstressed.set_tooltip_text(_(u"Indicates whether the "
                                                u"selected hardware item is "
                                                u"overstressed."))

        _fixed1.put(self.txtTotalPwr, _x_pos, _y_pos[0])
        _fixed1.put(self.txtVoltageRatio, _x_pos, _y_pos[1])
        _fixed1.put(self.txtCurrentRatio, _x_pos, _y_pos[2])
        _fixed1.put(self.txtPwrRatio, _x_pos, _y_pos[3])

        _label = _widg.make_label(text=_(u"Overstressed?:"))
        _fixed1.put(_label, 5, _y_pos[3] + 30)
        _fixed1.put(self.chkOverstressed, _x_pos, _y_pos[3] + 30)

        _textview = _widg.make_text_view(txvbuffer=self.txtOSReason,
                                         width=250)
        _textview.set_tooltip_text(_(u"The reason(s) the selected hardware "
                                     u"item is overstressed."))
        _fixed1.put(_textview, 4, _y_pos[3] + 60)

        #self.fraDerate.add(self.pltDerate)
        #_fixed1.put(self.fraDerate, _x_pos + 125, 5)

        # Create the labels for quadrant #1.
        _labels = [_(u"Active h(t):"), _(u"Dormant h(t):"),
                   _(u"Software h(t):"), _(u"Predicted h(t):"),
                   _(u"Mission h(t):"), _(u"h(t) Percent:"),
                   _(u"MTBF:"), _(u"Mission MTBF:"), _(u"Reliability:"),
                   _(u"Mission R(t):")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed2, 5, 5)
        _x_pos += 50

        # Place the quadrant #1 widgets.
        self.txtActiveHt.set_tooltip_text(_(u"Displays the active failure "
                                            u"intensity for the selected "
                                            u"hardware item."))
        self.txtDormantHt.set_tooltip_text(_(u"Displays the dormant "
                                             u"failure intensity for the "
                                             u"selected hardware item."))
        self.txtSoftwareHt2.set_tooltip_text(_(u"Displays the software "
                                               u"failure intensity for "
                                               u"the selected hardware item."))
        self.txtPredictedHt.set_tooltip_text(_(u"Displays the logistics "
                                               u"hazard rate for "
                                               u"the selected hardware item.  "
                                               u"This is the sum of the "
                                               u"active, dormant, and "
                                               u"software hazard rates."))
        self.txtMissionHt.set_tooltip_text(_(u"Displays the mission "
                                             u"failure intensity for the "
                                             u"selected hardware item."))
        self.txtHtPerCent.set_tooltip_text(_(u"Displays the percent of "
                                             u"the total system failure "
                                             u"intensity attributable to "
                                             u"the selected hardware item."))
        self.txtMTBF.set_tooltip_text(_(u"Displays the logistics mean time "
                                        u"between failure (MTBF) for the "
                                        u"selected hardware item."))
        self.txtMissionMTBF.set_tooltip_text(_(u"Displays the mission "
                                               u"mean time between "
                                               u"failure (MTBF) for the "
                                               u"selected hardware item."))
        self.txtReliability.set_tooltip_text(_(u"Displays the logistics "
                                               u"reliability for the "
                                               u"selected hardware item."))
        self.txtMissionRt.set_tooltip_text(_(u"Displays the mission "
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

        # Create the labels for quadrant #3.
        _labels = [_(u"MPMT:"), _(u"MCMT:"), _(u"MTTR:"), _(u"MMT:"),
                   _(u"Availability:"), _(u"Mission A(t):")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed3, 5, 5)

        # Create the labels for quadrant #4.
        _labels = [_(u"Total Cost:"), _(u"Cost/Failure:"),
                   _(u"Cost/Hour:"), _(u"Total Part Count:")]
        (_x_pos2, _y_pos2) = _widg.make_labels(_labels, _fixed4, 5, 5)
        _x_pos = max(_x_pos, _x_pos2) + 50

        # Place the quadrant #3 widgets.
        self.txtMPMT.set_tooltip_text(_(u"Displays the mean preventive "
                                        u"maintenance time (MPMT) for the "
                                        u"selected hardware item."))
        self.txtMCMT.set_tooltip_text(_(u"Displays the mean corrective "
                                        u"maintenance time (MCMT) for the "
                                        u"selected hardware item."))
        self.txtMTTR.set_tooltip_text(_(u"Displays the mean time to "
                                        u"repair (MTTR) for the selected "
                                        u"hardware item."))
        self.txtMMT.set_tooltip_text(_(u"Displays the mean maintenance "
                                       u"time (MMT) for the selected "
                                       u"hardware item."))
        self.txtAvailability.set_tooltip_text(_(u"Displays the logistics "
                                                u"availability for the "
                                                u"selected hardware item."))
        self.txtMissionAt.set_tooltip_text(_(u"Displays the mission "
                                             u"availability for the "
                                             u"selected hardware item."))

        _fixed3.put(self.txtMPMT, _x_pos, _y_pos[0])
        _fixed3.put(self.txtMCMT, _x_pos, _y_pos[1])
        _fixed3.put(self.txtMTTR, _x_pos, _y_pos[2])
        _fixed3.put(self.txtMMT, _x_pos, _y_pos[3])
        _fixed3.put(self.txtAvailability, _x_pos, _y_pos[4])
        _fixed3.put(self.txtMissionAt, _x_pos, _y_pos[5])

        # Place the quadrant #4 widgets.
        self.txtTotalCost.set_tooltip_text(_(u"Displays the total cost of "
                                             u"the selected hardware item."))
        self.txtCostFailure.set_tooltip_text(_(u"Displays the cost per "
                                               u"failure of the selected "
                                               u"hardware item."))
        self.txtCostHour.set_tooltip_text(_(u"Displays the cost per mission "
                                            u"hour of the selected hardware "
                                            u"item."))
        self.txtPartCount.set_tooltip_text(_(u"The total number of components "
                                             u"used to construct the selected "
                                             u"hardware item."))

        _fixed4.put(self.txtTotalCost, _x_pos, _y_pos2[0])
        _fixed4.put(self.txtCostFailure, _x_pos, _y_pos2[1])
        _fixed4.put(self.txtCostHour, _x_pos, _y_pos2[2])
        _fixed4.put(self.txtPartCount, _x_pos, _y_pos2[3])

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>" +
                            _(u"Assessment\nResults") +
                            u"</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the results the reliability, "
                                  u"maintainability, and other "
                                  u"assessments for the selected "
                                  u"assembly."))

        notebook.insert_page(_hpaned, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Loads the Hardware class gtk.Notebook().

        :param rtk.hardware.Hardware.Model model: the :class:`rtk.hardware.Hardware.Model`
                                                  to load.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        self._hardware_model = model

        # --------------------------------------------------------------#
        # Load the General Data information.                            #
        # --------------------------------------------------------------#
        self.txtRevisionID.set_text(str(self._hardware_model.revision_id))
        self.txtAltPartNum.set_text(self._hardware_model.alt_part_number)
        self.txtAttachments.set_text(self._hardware_model.attachments)
        self.txtCAGECode.set_text(self._hardware_model.cage_code)
        self.txtCompRefDes.set_text(self._hardware_model.comp_ref_des)
        self.txtDescription.set_text(self._hardware_model.description)
        self.txtFigNum.set_text(self._hardware_model.figure_number)
        self.txtLCN.set_text(self._hardware_model.lcn)
        self.cmbManufacturer.set_active(self._hardware_model.manufacturer)
        self.txtName.set_text(self._hardware_model.name)
        self.txtNSN.set_text(self._hardware_model.nsn)
        self.txtPageNum.set_text(self._hardware_model.page_number)
        self.txtPartNum.set_text(self._hardware_model.part_number)
        self.txtQuantity.set_text(str(self._hardware_model.quantity))
        self.txtRefDes.set_text(self._hardware_model.ref_des)
        _text = _util.none_to_string(self._hardware_model.remarks)
        _buffer = self.txtRemarks.get_child().get_child().get_buffer()
        _buffer.set_text(_text)
        self.chkRepairable.set_active(self._hardware_model.repairable)
        self.txtSpecification.set_text(
            self._hardware_model.specification_number)
        self.chkTagged.set_active(self._hardware_model.tagged_part)
        self.txtYearMade.set_text(
            str(self._hardware_model.year_of_manufacture))

        # Show/hide the assembly-specific or component-specific widgets as
        # appropriate.
        if self._hardware_model.part:
            self.cmbCategory.set_active(self._hardware_model.category_id)
            self.cmbSubcategory.set_active(self._hardware_model.subcategory_id)

            #self._component = _util.set_part_model(self.category_id,
            #                                       self.subcategory_id)
            self.cmbCategory.show()
            self.cmbSubcategory.show()
            self.lblCategory.show()
            self.lblSubcategory.show()
        else:
            self.cmbCategory.hide()
            self.cmbSubcategory.hide()
            self.lblCategory.hide()
            self.lblSubcategory.hide()

        # --------------------------------------------------------------#
        # Load the Reliability Allocation information.                  #
        # --------------------------------------------------------------#
        # Clear the Allocation View gtk.TreeModel().
        _model = self.wbvwAllocation.tvwAllocation.get_model()
        _model.clear()
        self.wbvwAllocation.load_page(self.dtcHardware,
                                      self._hardware_model.hardware_id)

        # --------------------------------------------------------------#
        # Load the Hazard Analysis information.                         #
        # --------------------------------------------------------------#
        self.wbvwHazard.load_page(self.dtcHardware,
                                  self._hardware_model.hardware_id)

        # --------------------------------------------------------------#
        # Load the Similar Item Analysis information.                   #
        # --------------------------------------------------------------#
        self.wbvwSimilarItem.load_page(self.dtcHardware,
                                       self._hardware_model.hardware_id)

        # --------------------------------------------------------------#
        # Load the Assessment Input information.                        #
        # --------------------------------------------------------------#
        self.cmbHRMethod.set_active(int(self._hardware_model.hazard_rate_method))
        self.txtSpecifiedHt.set_text(
            str(fmt.format(self._hardware_model.hazard_rate_specified)))
        self.txtSpecifiedMTBF.set_text(str(self._hardware_model.mtbf_specified))
        self.txtSoftwareHt.set_text(
            str(fmt.format(self._hardware_model.hazard_rate_software)))
        self.txtAddAdj.set_text(str(self._hardware_model.add_adj_factor))
        self.txtMultAdj.set_text(str(self._hardware_model.mult_adj_factor))
        self.cmbFailDist.set_active(int(self._hardware_model.failure_dist))
        self.txtFailScale.set_text(str(self._hardware_model.failure_parameter_1))
        self.txtFailShape.set_text(str(self._hardware_model.failure_parameter_2))
        self.txtFailLoc.set_text(str(self._hardware_model.failure_parameter_3))
        self.cmbActEnviron.set_active(int(self._hardware_model.environment_active))
        self.txtActTemp.set_text(str(self._hardware_model.temperature_active))
        self.cmbDormantEnviron.set_active(int(self._hardware_model.environment_dormant))
        self.txtDormantTemp.set_text(str(self._hardware_model.temperature_dormant))
        self.txtDutyCycle.set_text(str(self._hardware_model.duty_cycle))
        self.txtHumidity.set_text(str(self._hardware_model.humidity))
        self.txtVibration.set_text(str(self._hardware_model.vibration))
        self.txtRPM.set_text(str(self._hardware_model.rpm))
        self.cmbMTTRMethod.set_active(int(self._hardware_model.mttr_type))
        self.txtSpecifiedMTTR.set_text(str(self._hardware_model.mttr_specified))
        self.txtMTTRAddAdj.set_text(str(self._hardware_model.mttr_add_adj_factor))
        self.txtMTTRMultAdj.set_text(str(self._hardware_model.mttr_mult_adj_factor))
        self.cmbRepairDist.set_active(int(self._hardware_model.repair_dist))
        self.txtRepairScale.set_text(str(self._hardware_model.repair_parameter_1))
        self.txtRepairShape.set_text(str(self._hardware_model.repair_parameter_2))
        self.txtMissionTime.set_text(
            str('{0:0.2f}'.format(self._hardware_model.mission_time)))
        self.cmbCostMethod.set_active(int(self._hardware_model.cost_type))
        self.txtCost.set_text(str(locale.currency(self._hardware_model.cost)))

        # Load the component-specific information.
        if self._hardware_model.part:
            #self._component = _util.set_part_model(self.category_id,
            #                                       self.subcategory_id)

            self.cmbCalcModel.set_active(int(self._hardware_model.calculation_model))
            self.txtMinTemp.set_text(str('{0:0.2f}'.format(self._hardware_model.min_temp)))
            self.txtKneeTemp.set_text(
                str('{0:0.2f}'.format(self.knee_temp)))
            self.txtMaxTemp.set_text(str('{0:0.2f}'.format(self._hardware_model.max_temp)))
            self.txtRatedVoltage.set_text(
                str(fmt.format(self._hardware_model.rated_voltage)))
            self.txtOpVoltage.set_text(str(fmt.format(self._hardware_model.op_voltage)))
            self.txtRatedCurrent.set_text(
                str(fmt.format(self._hardware_model.rated_current)))
            self.txtOpCurrent.set_text(str(fmt.format(self._hardware_model.op_current)))
            self.txtRatedPower.set_text(str(fmt.format(self._hardware_model.rated_power)))
            self.txtOpPower.set_text(str(fmt.format(self._hardware_model.op_power)))
            self.txtThetaJC.set_text(str(self._hardware_model.theta_jc))
            self.txtTempRise.set_text(str(fmt.format(self._hardware_model.temp_rise)))
            self.txtCaseTemp.set_text(str(fmt.format(self._hardware_model.case_temp)))

        # Let the user know if the selected part does not have a part
        # category selected.
        if self._hardware_model.category_id < 1:
            self.lblNoCategory.show()
        else:
            self.lblNoCategory.hide()

        # Let the user know if the selected part does not have a part
        # subcategory selected.
        if self._hardware_model.subcategory_id < 1:
            self.lblNoSubCategory.show()
        else:
            self.lblNoSubCategory.hide()

        # --------------------------------------------------------------#
        # Load the Assessment Result information.                       #
        # --------------------------------------------------------------#
        self.txtActiveHt.set_text(str(fmt.format(self._hardware_model.hazard_rate_active)))
        self.txtDormantHt.set_text(str(fmt.format(self._hardware_model.hazard_rate_dormant)))
        self.txtSoftwareHt2.set_text(
            str(fmt.format(self._hardware_model.hazard_rate_software)))
        self.txtPredictedHt.set_text(str(fmt.format(self._hardware_model.hazard_rate_logistics)))
        self.txtMissionHt.set_text(str(fmt.format(self._hardware_model.hazard_rate_mission)))
        self.txtHtPerCent.set_text(str(fmt.format(self._hardware_model.hazard_rate_percent)))

        self.txtMTBF.set_text(str('{0:0.2f}'.format(self._hardware_model.mtbf_logistics)))
        self.txtMissionMTBF.set_text(str('{0:0.2f}'.format(self._hardware_model.mtbf_mission)))

        self.txtReliability.set_text(str(fmt.format(self._hardware_model.reliability_logistics)))
        self.txtMissionRt.set_text(str(fmt.format(self._hardware_model.reliability_mission)))

        self.txtMPMT.set_text(str('{0:0.2f}'.format(self._hardware_model.mpmt)))
        self.txtMCMT.set_text(str('{0:0.2f}'.format(self._hardware_model.mcmt)))
        self.txtMTTR.set_text(str('{0:0.2f}'.format(self._hardware_model.mttr)))
        self.txtMMT.set_text(str('{0:0.2f}'.format(self._hardware_model.mmt)))

        self.txtAvailability.set_text(str(fmt.format(self._hardware_model.availability_logistics)))
        self.txtMissionAt.set_text(str(fmt.format(self._hardware_model.availability_mission)))

        self.txtTotalCost.set_text(str(locale.currency(self._hardware_model.cost)))
        self.txtCostFailure.set_text(
            str(locale.currency(self._hardware_model.cost_failure)))
        self.txtCostHour.set_text(str('${0:0.4g}'.format(self._hardware_model.cost_hour)))

        self.txtPartCount.set_text(str(fmt.format(self._hardware_model.total_part_quantity)))
        self.txtTotalPwr.set_text(str(fmt.format(self._hardware_model.total_power_dissipation)))

        if self._hardware_model.part:
            self.txtCurrentRatio.set_text(str(fmt.format(self._hardware_model.current_ratio)))
            self.txtPwrRatio.set_text(str(fmt.format(self._hardware_model.power_ratio)))
            self.txtVoltageRatio.set_text(str(fmt.format(self._hardware_model.voltage_ratio)))

            self.chkOverstressed.set_active(self._hardware_model.overstress)

            #if self._component is not None:
            #    self._component.assessment_results_load(self)

        # --------------------------------------------------------------#
        # Load the FMEA/FMECA information.                              #
        # --------------------------------------------------------------#
        self.wbvwFMECA.load_page(self._hardware_model.hardware_id,
                                 self._hardware_model.hazard_rate_logistics)

        # --------------------------------------------------------------#
        # Load the PoF Analysis information.                            #
        # --------------------------------------------------------------#
        self.wbvwPoF.load_page(self._hardware_model.hardware_id)

        return False

    def update(self):

        pass

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

        # Add hardware --> call add_hardware, add_allocation, add_similar_item
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

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        combo.handler_block(self._lst_handler_id[index])
        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):
        """
        Responds to gtk.Entry() focus_out signals and calls the correct
        function or method, passing any parameters as needed.

        :param gtk.Entry entry: the gtk.Entry() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param int index: the index in the handler ID list oc the callback
                          signal associated with the gtk.Entry() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        entry.handler_block(self._lst_handler_id[index])

        if index == 0:
            self._hardware_model.name = entry.get_text()
        elif index == 1:
            self._hardware_model.part_number = entry.get_text()
        elif index == 2:
            self._hardware_model.alt_part_number = entry.get_text()
        elif index == 5:
            self._hardware_model.ref_des = entry.get_text()
        elif index == 6:
            self._hardware_model.comp_ref_des = entry.get_text()
        elif index == 7:
            self._hardware_model.quantity = int(entry.get_text())
        elif index == 8:
            self._hardware_model.description = entry.get_text()
        elif index == 10:
            self._hardware_model.cage_code = entry.get_text()
        elif index == 11:
            self._hardware_model.lcn = entry.get_text()
        elif index == 12:
            self._hardware_model.nsn = entry.get_text()
        elif index == 13:
            self._hardware_model.year_of_manufacture = int(entry.get_text())
        elif index == 14:
            self._hardware_model.specification = entry.get_text()
        elif index == 15:
            self._hardware_model.page_number = entry.get_text()
        elif index == 16:
            self._hardware_model.figure_number = entry.get_text()
        elif index == 17:
            self._hardware_model.attachments = entry.get_text()
        elif index == 18:
            self._hardware_model.mission_time = float(entry.get_text())
        elif index == 21:
            _textbuffer = self.txtRemarks.get_child().get_child().get_buffer()
            _text = _textbuffer.get_text(*_textbuffer.get_bounds())
            self._hardware_model.remarks = _text

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_toggled(self, check, index):

        pass
