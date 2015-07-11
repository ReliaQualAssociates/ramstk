#!/usr/bin/env python
"""
###############################
Software Package Work Book View
###############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.software.WorkBook.py is part of The RTK Project
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

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
    import utilities as _util
    import widgets as _widg
except ImportError:
    import rtk.configuration as _conf
    import rtk.utilities as _util
    import rtk.widgets as _widg
import gui.gtk.DevelopmentEnvironment as DevEnv
import gui.gtk.SRR as SRR
import gui.gtk.PDR as PDR
import gui.gtk.CDR as CDR
import gui.gtk.TRR as TRR
import gui.gtk.TestSelection as TestSelection
# from Assistants import AddSoftware

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _set_risk_color(risk, module):
    """
    Function to find the hexadecimal code for the risk level colors.

    :param dict risk: dictionary containing the Software class risk factors.
    :param int module: the software id used as a key for accessing the correct
                       risk factors from the risk dictionary.
    :return: a dictionary containing the hexadecimal color values for each
             risk factor.
    :rtype: dictionary
    """

    _color = {}

    # Find the Application risk level.
    if risk[module][0] == 1.0:
        _color['A'] = '#90EE90'             # Green
    elif risk[module][0] == 2.0:
        _color['A'] = '#FFFF79'             # Yellow
    elif risk[module][0] == 3.0:
        _color['A'] = '#FFC0CB'             # Red
    else:
        _color['A'] = '#D3D3D3'             # Light grey

    # Find the Development risk level.
    if risk[module][1] == 0.5:
        _color['D'] = '#90EE90'             # Green
    elif risk[module][1] == 1.0:
        _color['D'] = '#FFFF79'             # Yellow
    elif risk[module][1] == 2.0:
        _color['D'] = '#FFC0CB'             # Red
    else:
        _color['D'] = '#D3D3D3'             # Light grey

    # Find the Anomaly Management risk level.
    if risk[module][2] == 0.9:
        _color['SA'] = '#90EE90'            # Green
    elif risk[module][2] == 1.1:
        _color['SA'] = '#FFC0CB'            # Red
    elif risk[module][2] == 1.0:
        _color['SA'] = '#FFFF79'            # Yellow
    elif risk[module][2] == 0.0:
        _color['SA'] = '#D3D3D3'            # Light grey

    # Find the Requirement Traceability risk level.
    if risk[module][3] == 0.9:
        _color['ST'] = '#90EE90'            # Green
    elif risk[module][3] == 1.0:
        _color['ST'] = '#FFFF79'            # Yellow
    elif risk[module][3] == 1.1:
        _color['ST'] = '#FFC0CB'            # Red
    else:
        _color['ST'] = '#D3D3D3'            # Light grey

    # Find the Software Quality risk level.
    if risk[module][4] == 1.0:
        _color['SQ'] = '#90EE90'            # Green
    elif risk[module][4] == 1.1:
        _color['SQ'] = '#FFC0CB'            # Red
    else:
        _color['SQ'] = '#D3D3D3'            # Light grey

    # Find the Language Type risk level.
    if risk[module][5] == 1.0:
        _color['SL'] = '#90EE90'            # Green
    elif risk[module][5] > 1.0 and risk[module][5] <= 1.2:
        _color['SL'] = '#FFFF79'            # Yellow
    elif risk[module][5] > 1.2:
        _color['SL'] = '#FFC0CB'            # Red
    else:
        _color['SL'] = '#D3D3D3'            # Light grey

    # Find the Complexity risk level.
    if risk[module][6] >= 0.8 and risk[module][6] < 1.0:
        _color['SX'] = '#90EE90'            # Green
    elif risk[module][6] >= 1.0 and risk[module][6] <= 1.2:
        _color['SX'] = '#FFFF79'            # Yellow
    elif risk[module][6] > 1.2:
        _color['SX'] = '#FFC0CB'            # Red
    else:
        _color['SX'] = '#D3D3D3'            # Light grey

    # Find the Modularity risk level.
    if risk[module][7] >= 0.9 and risk[module][7] < 1.2:
        _color['SM'] = '#90EE90'            # Green
    elif risk[module][7] >= 1.2 and risk[module][7] <= 1.5:
        _color['SM'] = '#FFFF79'            # Yellow
    elif risk[module][7] > 1.5:
        _color['SM'] = '#FFC0CB'            # Red
    else:
        _color['SM'] = '#D3D3D3'            # Light grey

    # Find the overall risk level.
    if risk[module][8] > 0.0 and risk[module][8] <= 1.5:
        _color['Risk'] = '#90EE90'          # Green
    elif risk[module][8] > 1.5 and risk[module][8] < 3.5:
        _color['Risk'] = '#FFFF79'          # Yellow
    elif risk[module][8] >= 3.5:
        _color['Risk'] = '#FFC0CB'          # Red
    else:
        _color['Risk'] = '#D3D3D3'          # Light grey

    return _color


class WorkView(gtk.VBox):                   # pylint: disable=R0902, R0904
    """
    The Work Book view displays all the attributes for the selected
    Software item.  The attributes of a Work Book view are:

    :ivar _workview: the RTK top level Work View window to embed the
                     Software Work Book into.
    :ivar _software_model: the Software data model whose attributes are being
                           displayed.

    :ivar _dic_definitions: dictionary containing pointers to the failure
                            definitions for the Revision being displayed.  Key
                            is the Failure Definition ID; value is the pointer
                            to the Failure Definition data model.

    :ivar _lst_handler_id: list containing the ID's of the callback signals for
                           each gtk.Widget() associated with an editable
                           Software attribute.

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

    :ivar dtcSoftware: the :class:`rtk.software.Software.Software` data
                       controller to use with this Work Book.

    :ivar chkSafetyCritical: the :class:`gtk.CheckButton` to display/edit the
                             Software's safety criticality.

    :ivar txtName: the :class:`gtk.Entry` to display/edit the Software name.
    :ivar txtTotalCost: the :class:`gtk.Entry` to display the Software cost.
    :ivar txtPartCount: the :class:`gtk.Entry` to display the number of
                        Components comprising the Assembly.
    :ivar txtRemarks: the :class:`gtk.Entry` to display/edit the Software
                      remarks.
    :ivar txtPredictedHt: the :class:`gtk.Entry` to display the Software
                          logistics hazard rate.
    :ivar txtMissionHt: the :class:`gtk.Entry` to display the Software mission
                        hazard rate.
    :ivar txtMTBF: the :class:`gtk.Entry` to display the Software logistics
                   MTBF.
    :ivar txtMissionMTBF: the :class:`gtk.Entry` to display the Software
                          mission MTBF.
    :ivar txtMPMT: the :class:`gtk.Entry` to display the Software mean
                   preventive maintenance time.
    :ivar txtMCMT: the :class:`gtk.Entry` to display the Software mean
                   corrective maintenance time.
    :ivar txtMTTR: the :class:`gtk.Entry` to display the Software mean time to
                   repair.
    :ivar txtMMT: the :class:`gtk.Entry` to display the Software mean
                  maintenance time.
    :ivar txtAvailability: the :class:`gtk.Entry` to display the Software
                           logistics availability.
    :ivar txtMissionAt: the :class:`gtk.Entry` to display the Software mission
                        availability.
    """

    def __init__(self, workview, modulebook):
        """
        Initializes the Work Book view for the Software package.

        :param rtk.gui.gtk.mwi.WorkView workview: the Work View container to
                                                  insert this Work Book into.
        :param rtk.function.ModuleBook: the Function Module Book to associate
                                        with this Work Book.
        """

        gtk.VBox.__init__(self)

        # Initialize private dict attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []
        self._lst_obj_risk_analyses = [None, None, None, None, None, None,
                                       None]

        # Initialize private scalar attributes.
        self._workview = workview
        self._modulebook = modulebook
        self._software_model = None

        # Initialize public scalar attributes.
        self.dtcBoM = modulebook.dtcBoM

        # General Data page widgets.
        self.cmbApplication = _widg.make_combo(simple=False)
        self.cmbDevelopment = _widg.make_combo(simple=False)
        self.cmbLevel = _widg.make_combo(simple=False)
        self.cmbPhase = _widg.make_combo(simple=False)
        self.txtDescription = _widg.make_text_view(width=400)

        # Risk Analysis page widgets.
        self.btnCalculate = _widg.make_button(width=35, image='calculate')
        self.btnSave = _widg.make_button(width=35, image='save')

        self.nbkRiskAnalysis = gtk.Notebook()
        self.tvwRiskMap = gtk.TreeView()

        # Test Planning page widgets.
        self.btnTestCalculate = _widg.make_button(width=35, image='calculate')
        self.btnTestSave = _widg.make_button(width=35, image='save')

        self.cmbTCL = _widg.make_combo(simple=True)
        self.cmbTestPath = _widg.make_combo(simple=True)
        self.cmbTestEffort = _widg.make_combo(simple=True)
        self.cmbTestApproach = _widg.make_combo(simple=True)

        self.fraTestSelection = _widg.make_frame(
            label=_(u"Test Technique Selection"))

        self.hpnTestPlanning = gtk.HPaned()

        self.scwCSCITestSelection = None
        self.scwUnitTestSelection = None

        self.txtLaborTest = _widg.make_entry(width=75)
        self.txtLaborDev = _widg.make_entry(width=75)
        self.txtBudgetTest = _widg.make_entry(width=75)
        self.txtBudgetDev = _widg.make_entry(width=75)
        self.txtScheduleTest = _widg.make_entry(width=75)
        self.txtScheduleDev = _widg.make_entry(width=75)
        self.txtBranches = _widg.make_entry(width=75)
        self.txtBranchesTest = _widg.make_entry(width=75)
        self.txtInputs = _widg.make_entry(width=75)
        self.txtInputsTest = _widg.make_entry(width=75)
        self.txtUnits = _widg.make_entry(width=75)
        self.txtUnitsTest = _widg.make_entry(width=75)
        self.txtInterfaces = _widg.make_entry(width=75)
        self.txtInterfacesTest = _widg.make_entry(width=75)

        # Reliability Estimation page widgets.
        self.btnEstimate = _widg.make_button(width=35, image='calculate')

        self.txtEC = _widg.make_entry(width=75)
        self.txtET = _widg.make_entry(width=75)
        self.txtOS = _widg.make_entry(width=75)
        self.txtDRTest = _widg.make_entry(width=75)
        self.txtTestTime = _widg.make_entry(width=75)
        self.txtDREOT = _widg.make_entry(width=75)
        self.txtTestTimeEOT = _widg.make_entry(width=75)
        self.txtTE = _widg.make_entry(width=75, editable=False)
        self.txtTM = _widg.make_entry(width=75, editable=False)
        self.txtTC = _widg.make_entry(width=75, editable=False)
        self.txtFT1 = _widg.make_entry(width=75, editable=False)
        self.txtFT2 = _widg.make_entry(width=75, editable=False)
        self.txtRENAVG = _widg.make_entry(width=75, editable=False)
        self.txtRENEOT = _widg.make_entry(width=75, editable=False)
        self.txtEV = _widg.make_entry(width=75, editable=False)
        self.txtEW = _widg.make_entry(width=75, editable=False)
        self.txtE = _widg.make_entry(width=75, editable=False)
        self.txtF = _widg.make_entry(width=75, editable=False)

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
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
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
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert_child.png')
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
        _image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
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
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
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
        if _conf.TABPOS[2] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif _conf.TABPOS[2] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif _conf.TABPOS[2] == 'top':
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
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                 gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = _widg.make_frame(label=_(u"General Information"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.ComboBox() widgets.
        _model = self.cmbLevel.get_model()
        _model.clear()
        _model.append(None, ['', 0, ''])
        for _level in self._workview.RTK_SW_LEVELS:
            _model.append(None, [self._workview.RTK_SW_LEVELS[_level], 0, ''])

        _model = self.cmbApplication.get_model()
        _model.clear()
        _model.append(None, ['', 0, ''])
        for _app in self._workview.RTK_SW_APPLICATION:
            _model.append(None, [self._workview.RTK_SW_APPLICATION[_app],
                                 0, ''])

        _model = self.cmbPhase.get_model()
        _model.clear()
        _model.append(None, ['', 0, ''])
        for _phase in self._workview.RTK_SW_DEV_PHASES:
            _model.append(None, [self._workview.RTK_SW_DEV_PHASES[_phase],
                                 0, ''])

        # Create the labels.
        _labels = [_(u"Module Description:"), _(u"Application Level:"),
                   _(u"Application Type:"), _(u"Development Phase:")]

        (_x_pos, _y_pos) = _widg.make_labels(_labels[1:], _fixed, 5, 110)
        _x_pos += 25

        # Place the widgets.
        self.txtDescription.set_tooltip_text(_(u"Enter a description of "
                                               u"the selected software "
                                               u"module."))
        self.cmbLevel.set_tooltip_text(_(u"Select the application level "
                                         u"of the selected software "
                                         u"module."))
        self.cmbApplication.set_tooltip_text(_(u"Select the application "
                                               u"type of the selected "
                                               u"software module."))
        self.cmbPhase.set_tooltip_text(_(u"Select the development phase "
                                         u"for the selected software "
                                         u"module."))

        _label = _widg.make_label(_labels[0])
        _fixed.put(_label, 5, 5)
        _fixed.put(self.txtDescription, _x_pos, 5)
        _fixed.put(self.cmbLevel, _x_pos, _y_pos[0])
        _fixed.put(self.cmbApplication, _x_pos, _y_pos[1])
        _fixed.put(self.cmbPhase, _x_pos, _y_pos[2])

        _textview = self.txtDescription.get_child().get_child()
        self._lst_handler_id.append(
            _textview.connect('focus-out-event', self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.cmbLevel.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbPhase.connect('changed', self._on_combo_changed, 3))

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
        :rtype: boolean
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

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.tvwRiskMap)

        _hpaned.pack1(self.nbkRiskAnalysis, resize=True, shrink=True)
        _hpaned.pack2(_scrollwindow, resize=True, shrink=True)

        _bbox.pack_start(self.btnCalculate, False, False)
        _bbox.pack_start(self.btnSave, False, False)

        self.btnCalculate.set_tooltip_text(_(u"Calculate the reliability "
                                             u"risk assessment."))
        self.btnSave.set_tooltip_text(_(u"Saves the reliability risk "
                                        u"assessment."))

        self.btnCalculate.connect('clicked', self._on_button_clicked, 50)
        self.btnSave.connect('clicked', self._on_button_clicked, 51)

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

        # Add the risk map.
        _headings = [_(u"Software\nModule"), _(u"Application\nRisk"),
                     _(u"Organization\nRisk"), _(u"Anomaly\nManagement\nRisk"),
                     _(u"Traceability\nRisk"), _(u"Quality\nAssurance\nRisk"),
                     _(u"Language\nRisk"), _(u"Code\nComplexity\nRisk"),
                     _(u"Modularity\nRisk"), _(u"Overall\nRisk")]

        _model = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING)
        self.tvwRiskMap.set_model(_model)
        self.tvwRiskMap.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        _cell = gtk.CellRendererText()       # Cell background color.
        _cell.set_property('visible', False)
        _column = gtk.TreeViewColumn()
        _column.set_visible(False)
        _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)

        self.tvwRiskMap.append_column(_column)

        for i in range(1, 11):
            _label = gtk.Label()
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_property('angle', 90)
            _label.set_markup("<span weight='bold'>" +
                              _headings[i-1] +
                              "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column = gtk.TreeViewColumn()
            _column.set_widget(_label)
            _column.set_visible(True)
            _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
            _cell = gtk.CellRendererText()       # Cell background color.
            _cell.set_property('visible', True)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, background=i)
            if i == 1:
                _column.set_attributes(_cell, text=i)

            self.tvwRiskMap.append_column(_column)

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
        :rtype: boolean
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

        self.btnTestCalculate.set_tooltip_text(_(u"Calculate the test plan "
                                                 u"risk reduction."))
        self.btnTestSave.set_tooltip_text(_(u"Saves the test plan risk "
                                            u"reduction assessment."))

        self.btnTestCalculate.connect('clicked', self._on_button_clicked, 52)
        self.btnTestSave.connect('clicked', self._on_button_clicked, 53)

        _vpaned = gtk.VPaned()

        # Add the test planning widgets to the upper left half.
        _fxdtopleft = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdtopleft)

        _frame = _widg.make_frame(label=_(u"Test Planning"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)
        _frame.show_all()

        _vpaned.pack1(_frame, resize=True, shrink=True)

        # Add the test effort widgets to the lower left half.
        _fxdbottomleft = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdbottomleft)

        _frame = _widg.make_frame(label=_(u"Test Effort &amp; Coverage"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack2(_frame, resize=True, shrink=True)

        _hpaned.pack1(_vpaned, resize=True, shrink=True)

        # Add the test technique selection widgets to the upper right half.
        self.scwCSCITestSelection = TestSelection.CSCITestSelection()
        self.scwCSCITestSelection.create_test_planning_matrix()

        self.scwUnitTestSelection = TestSelection.UnitTestSelection()
        self.scwUnitTestSelection.create_test_planning_matrix()

        self.fraTestSelection.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        _hpaned.pack2(self.fraTestSelection, resize=True, shrink=True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display risk analysis information.  #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.Combo()
        _list = [["Low"], ["Medium"], ["High"], ["Very High"]]
        _widg.load_combo(self.cmbTCL, _list, True)

        _list = [[_(u"Choose techniques based on software category")],
                 [_(u"Choose techniques based on types of software errors")]]
        _widg.load_combo(self.cmbTestPath, _list, True)

        _list = [[_(u"Alternative 1, Labor Hours")],
                 [_(u"Alternative 2, Budget")],
                 [_(u"Alternative 3, Schedule")]]
        _widg.load_combo(self.cmbTestEffort, _list, True)

        _list = [[_(u"Test Until Method is Exhausted")],
                 [_(u"Stopping Rules")]]
        _widg.load_combo(self.cmbTestApproach, _list, True)

        # Place the labels in the upper left pane.
        _labels = [_(u"Test Confidence Level:"), _(u"Test Path:"),
                   _(u"Test Effort:"), _(u"Test Approach:")]
        _max1 = 0
        (_max1, _y_pos1) = _widg.make_labels(_labels, _fxdtopleft,
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
        (_x_pos_left, _y_pos2) = _widg.make_labels(_labels, _fxdbottomleft,
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
         _y_pos) = _widg.make_labels(_labels, _fxdbottomleft,
                                     _x_pos_left+105, 5)
        _x_pos_right += _x_pos_left + 150

        # Place the widgets in the upper left pane.
        self.cmbTCL.set_tooltip_text(_(u"Select the desired software test "
                                       u"confidence level."))
        self.cmbTestPath.set_tooltip_text(_(u"Select the path for determining "
                                            u"software testing techniques."))
        self.cmbTestEffort.set_tooltip_text(_(u"Select the software test "
                                              u"effort alternative."))
        self.cmbTestApproach.set_tooltip_text(_(u"Select the software test "
                                                u"approach."))

        _fxdtopleft.put(self.cmbTCL, _x_pos_left, _y_pos1[0])
        _fxdtopleft.put(self.cmbTestPath, _x_pos_left, _y_pos1[1])
        _fxdtopleft.put(self.cmbTestEffort, _x_pos_left, _y_pos1[2])
        _fxdtopleft.put(self.cmbTestApproach, _x_pos_left, _y_pos1[3])

        self._lst_handler_id.append(
            self.cmbTCL.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.cmbTestPath.connect('changed', self._on_combo_changed, 5))
        self._lst_handler_id.append(
            self.cmbTestEffort.connect('changed', self._on_combo_changed, 6))
        self._lst_handler_id.append(
            self.cmbTestApproach.connect('changed', self._on_combo_changed, 7))

        _fxdtopleft.show_all()

        # Place the widgets in the lower left pane.
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
        :rtype: boolean
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

        self.btnEstimate.set_tooltip_text(_(u"Estimate the software failure "
                                            u"rates."))

        self.btnEstimate.connect('clicked', self._on_button_clicked, 54)

        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = _widg.make_frame(label=_(u"Reliability Estimation Results"))
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
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
        _x_pos += 45

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
        Loads the Software class gtk.Notebook().

        :param model: the :py:class: `rtk.software.Software.Model` to load.
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
        for _child in self.fraTestSelection.get_children():
            self.fraTestSelection.remove(_child)

        if model.level_id == 2:             # CSCI
            self.scwCSCITestSelection.load_test_selections(model)
            self.fraTestSelection.add(self.scwCSCITestSelection)
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
            self.scwUnitTestSelection.load_test_selections(model)
            self.fraTestSelection.add(self.scwUnitTestSelection)
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
        self.fraTestSelection.resize_children()

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
        Loads the Software class gtk.Notebook() risk analysis page.

        Show the pages according to the following

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

        if self._software_model.level_id == 1:             # System
            _lst_show = [0]
            _lst_hide = [1, 2, 3, 4, 5, 6]

        if self._software_model.phase_id == 1:             # Concept/planning
            _lst_show = [0]
            _lst_hide = [1, 2, 3, 4, 5, 6]
        elif self._software_model.phase_id == 2:           # Requirements review
            if self._software_model.level_id == 2:         # CSCI
                _lst_show = [0, 1]
                _lst_hide = [2, 3, 4, 5, 6]
            elif self._software_model.level_id == 3:       # Unit
                _lst_show = [0]
                _lst_hide = [1, 2, 3, 4, 5, 6]
        elif self._software_model.phase_id == 3:           # Preliminary design review
            if self._software_model.level_id == 2:         # CSCI
                _lst_show = [0, 1, 2]
                _lst_hide = [3, 4, 5, 6]
            elif self._software_model.level_id == 3:       # Unit
                _lst_show = [0]
                _lst_hide = [1, 2, 3, 4, 5, 6]
        elif self._software_model.phase_id == 4:           # Critical design review
            if self._software_model.level_id == 2:         # CSCI
                _lst_show = [0, 1, 2, 3]
                _lst_hide = [4, 5, 6]
            elif self._software_model.level_id == 3:       # Unit
                _lst_show = [0, 4]
                _lst_hide = [1, 2, 3, 5, 6]
        elif self._software_model.phase_id == 5:           # Test readiness review
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

        # Load the risk map.
        _software = self.dtcBoM.dicSoftware.values()
        _top_module = [_s for _s in _software if _s.software_id == 0]

        _model = self.tvwRiskMap.get_model()
        _model.clear()

        self._load_risk_map(_top_module, _software, _model)

        return False

    def _load_assessment_results_page(self):
        """
        Loads the Software class gtk.Notebook() risk assessment page.

        :return: False if successful or True if an error is encountered.
        :rtype
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        self.txtEC.set_text(str(fmt.format(self._software_model.ec)))
        self.txtET.set_text(str(fmt.format(self._software_model.et)))
        self.txtOS.set_text(str(fmt.format(self._software_model.os)))
        self.txtDRTest.set_text(str(fmt.format(self._software_model.dr_test)))
        self.txtTestTime.set_text(str(fmt.format(self._software_model.test_time)))
        self.txtDREOT.set_text(str(fmt.format(self._software_model.dr_eot)))
        self.txtTestTimeEOT.set_text(str(fmt.format(self._software_model.test_time_eot)))

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
                _util.rtk_information(_(u"Can not add a sibling to the "
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

        elif index == 50:
            self.dtcBoM.request_calculate()

            # Load the risk map.
            _software = self.dtcBoM.dicSoftware.values()
            _top_module = [_s for _s in _software if _s.software_id == 0]

            _model = self.tvwRiskMap.get_model()
            _model.clear()

            self._load_risk_map(_top_module, _software, _model)

            self._load_assessment_results_page()

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

        elif index == 53:
            self.dtcBoM.save_test_selections(self._software_model.software_id)

        elif index == 54:
            self.dtcBoM.request_calculate()

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
            _icon = _conf.ICON_DIR + '32x32/csci.png'
        elif software_type == 2:
            _icon = _conf.ICON_DIR + '32x32/unit.png'

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

        :param gtk.TreeModel model: the gtk.TreeModel() holding the Software
                                    data.
        :param gtk.TreeIter row: the gtk.TreeIter() that will be removed from
                                 the gtk.TreeModel().
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

    def _load_risk_map(self, parents, software, model, row=None):
        """
        Method to load the Software class Risk Map.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _dicRisk = {}

        for _software in parents:
            _data = [_software.software_id, _software.description]
            _dicRisk[_software.software_id] = [_software.a_risk,
                                               _software.d_risk, _software.sa,
                                               _software.st, _software.sq,
                                               _software.sl, _software.sx,
                                               _software.sm, _software.rpfom]

            # Get the hexidecimal color code for each risk factor.
            _color = _set_risk_color(_dicRisk, _software.software_id)

            if _software.parent_id == -1:   # It's the top level element.
                row = None

            _data.append(_color['A'])
            _data.append(_color['D'])
            _data.append(_color['SA'])
            _data.append(_color['ST'])
            _data.append(_color['SQ'])
            _data.append(_color['SL'])
            _data.append(_color['SX'])
            _data.append(_color['SM'])
            _data.append(_color['Risk'])

            _piter = model.append(row, _data)

            _parents = [_s for _s in software if _s.parent_id == _software.software_id]
            self._load_risk_map(_parents, software, model, _piter)

        self.tvwRiskMap.expand_all()

        return False
