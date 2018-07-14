# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.assistants.CreateProject.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
#####################
RTK Assistants Module
#####################
"""

import gettext
import sys

from os.path import basename

from ConfigParser import SafeConfigParser, NoOptionError

# Modules required for the GUI.
import pango  # pylint: disable=E0401
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

# Import other RTK modules.
try:
    import Configuration
    import Utilities
    import gui.gtk.rtk.Widget as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    import rtk.gui.gtk.rtk.Widget as Widgets

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 Andrew "Weibullguy" Rowland'

_ = gettext.gettext


class Options(gtk.Window):  # pylint: disable=R0902
    """
    An assistant to provide a GUI to the various configuration files for RTK.
    """

    def __init__(self, __widget, controller):  # pylint: disable=R0915
        """
        Allows a user to set site-wide options.

        :param gtk.Widget __widget: the gtk.Widget() that called this class.
        :param controller: the :py:class:`rtk.RTK.RTK` master data controller.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._mdcRTK = controller
        self._last_id = -1

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        gtk.Window.__init__(self)

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        self.set_default_size((_width / 3) - 10, (2 * _height / 7))

        self.notebook = gtk.Notebook()

        # ----- ----- ----- -- RTK module options - ----- ----- ----- #
        # Only show the active modules page if a RTK Program database is open.
        if Configuration.RTK_PROG_INFO[2] != '':
            _fixed = gtk.Fixed()

            self.chkRevisions = Widgets.make_check_button(_(u"Revisions"))
            self.chkFunctions = Widgets.make_check_button(_(u"Functions"))
            self.chkRequirements = Widgets.make_check_button(
                _(u"Requirements"))
            self.chkSoftware = Widgets.make_check_button(_(u"Software"))
            self.chkValidation = Widgets.make_check_button(
                _(u"Validation "
                  u"Tasks"))
            self.chkRG = Widgets.make_check_button(_(u"Reliability Tests"))
            self.chkIncidents = Widgets.make_check_button(
                _(u"Program "
                  u"Incidents"))
            self.chkSurvivalAnalysis = Widgets.make_check_button(
                _(u"Survival "
                  u"Analysis"))

            self.btnSaveModules = gtk.Button(stock=gtk.STOCK_SAVE)

            _fixed.put(self.chkRevisions, 5, 5)
            _fixed.put(self.chkFunctions, 5, 35)
            _fixed.put(self.chkRequirements, 5, 65)
            _fixed.put(self.chkSoftware, 5, 95)
            _fixed.put(self.chkValidation, 5, 125)
            _fixed.put(self.chkRG, 5, 155)
            _fixed.put(self.chkIncidents, 5, 185)
            _fixed.put(self.chkSurvivalAnalysis, 5, 215)

            _fixed.put(self.btnSaveModules, 5, 305)

            self.btnSaveModules.connect('clicked', self._save_modules)

            _query = "SELECT fld_revision_active, fld_function_active, \
                             fld_requirement_active, fld_hardware_active, \
                             fld_software_active, fld_vandv_active, \
                             fld_testing_active, fld_rcm_active, \
                             fld_fraca_active, fld_fmeca_active, \
                             fld_survival_active, fld_rbd_active, \
                             fld_fta_active \
                      FROM tbl_program_info"

            #_results = self._mdcRTK.project_dao.execute(_query, commit=False)

            #self.chkRevisions.set_active(_results[0][0])
            #self.chkFunctions.set_active(_results[0][1])
            #self.chkRequirements.set_active(_results[0][2])
            #self.chkSoftware.set_active(_results[0][4])
            #self.chkValidation.set_active(_results[0][5])
            #self.chkRG.set_active(_results[0][6])
            #self.chkIncidents.set_active(_results[0][8])
            #self.chkSurvivalAnalysis.set_active(_results[0][10])

            _label = gtk.Label(_(u"RTK Modules"))
            _label.set_tooltip_text(_(u"Select active RTK modules."))
            self.notebook.insert_page(_fixed, tab_label=_label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        # ----- ----- ----- Create default value options ----- ----- ----- #
        _fixed = gtk.Fixed()

        self.cmbModuleBookTabPosition = Widgets.make_combo(simple=True)
        self.cmbWorkBookTabPosition = Widgets.make_combo(simple=True)
        self.cmbListBookTabPosition = Widgets.make_combo(simple=True)

        self.txtFRMultiplier = Widgets.make_entry()
        self.txtDecimalPlaces = Widgets.make_entry(width=75)
        self.txtMissionTime = Widgets.make_entry(width=75)

        # Create color selection buttons.
        self.btnRevisionBGColor = gtk.ColorButton()
        self.btnRevisionFGColor = gtk.ColorButton()
        self.btnFunctionBGColor = gtk.ColorButton()
        self.btnFunctionFGColor = gtk.ColorButton()
        self.btnRequirementsBGColor = gtk.ColorButton()
        self.btnRequirementsFGColor = gtk.ColorButton()
        self.btnHardwareBGColor = gtk.ColorButton()
        self.btnHardwareFGColor = gtk.ColorButton()
        self.btnSoftwareBGColor = gtk.ColorButton()
        self.btnSoftwareFGColor = gtk.ColorButton()
        self.btnValidationBGColor = gtk.ColorButton()
        self.btnValidationFGColor = gtk.ColorButton()
        self.btnIncidentBGColor = gtk.ColorButton()
        self.btnIncidentFGColor = gtk.ColorButton()
        self.btnTestingBGColor = gtk.ColorButton()
        self.btnTestingFGColor = gtk.ColorButton()

        for _position in ["Bottom", "Left", "Right", "Top"]:
            self.cmbModuleBookTabPosition.append_text(_position)
            self.cmbWorkBookTabPosition.append_text(_position)
            self.cmbListBookTabPosition.append_text(_position)

        _label = Widgets.make_label(_(u"Module Book tab position:"))
        _fixed.put(_label, 5, 5)
        _fixed.put(self.cmbModuleBookTabPosition, 310, 5)
        _label = Widgets.make_label(_(u"Work Book tab position:"))
        _fixed.put(_label, 5, 35)
        _fixed.put(self.cmbWorkBookTabPosition, 310, 35)
        _label = Widgets.make_label(_(u"List Book tab position:"))
        _fixed.put(_label, 5, 65)
        _fixed.put(self.cmbListBookTabPosition, 310, 65)
        _label = Widgets.make_label(_(u"Failure rate multiplier:"))
        _fixed.put(_label, 5, 125)
        _fixed.put(self.txtFRMultiplier, 310, 125)
        _label = Widgets.make_label(_(u"Decimal places:"))
        _fixed.put(_label, 5, 155)
        _fixed.put(self.txtDecimalPlaces, 310, 155)
        _label = Widgets.make_label(_(u"Default mission time:"))
        _fixed.put(_label, 5, 185)
        _fixed.put(self.txtMissionTime, 310, 185)

        _label = Widgets.make_label(
            _(u"Revision Tree Background Color:"), width=350)
        _fixed.put(_label, 5, 225)
        _fixed.put(self.btnRevisionBGColor, 340, 225)
        _label = Widgets.make_label(
            _(u"Revision Tree Foreground Color:"), width=350)
        _fixed.put(_label, 5, 255)
        _fixed.put(self.btnRevisionFGColor, 340, 255)
        _label = Widgets.make_label(
            _(u"Function Tree Background Color:"), width=350)
        _fixed.put(_label, 5, 285)
        _fixed.put(self.btnFunctionBGColor, 340, 285)
        _label = Widgets.make_label(
            _(u"Function Tree Foreground Color:"), width=350)
        _fixed.put(_label, 5, 315)
        _fixed.put(self.btnFunctionFGColor, 340, 315)
        _label = Widgets.make_label(
            _(u"Requirements Tree Background Color:"), width=350)
        _fixed.put(_label, 5, 345)
        _fixed.put(self.btnRequirementsBGColor, 340, 345)
        _label = Widgets.make_label(
            _(u"Requirements Tree Foreground Color:"), width=350)
        _fixed.put(_label, 5, 375)
        _fixed.put(self.btnRequirementsFGColor, 340, 375)
        _label = Widgets.make_label(
            _(u"Hardware Tree Background Color:"), width=350)
        _fixed.put(_label, 5, 405)
        _fixed.put(self.btnHardwareBGColor, 340, 405)
        _label = Widgets.make_label(
            _(u"Hardware Tree Foreground Color:"), width=350)
        _fixed.put(_label, 5, 435)
        _fixed.put(self.btnHardwareFGColor, 340, 435)
        _label = Widgets.make_label(
            _(u"Software Tree Background Color:"), width=350)
        _fixed.put(_label, 5, 465)
        _fixed.put(self.btnSoftwareBGColor, 340, 465)
        _label = Widgets.make_label(
            _(u"Software Tree Foreground Color:"), width=350)
        _fixed.put(_label, 5, 495)
        _fixed.put(self.btnSoftwareFGColor, 340, 495)
        _label = Widgets.make_label(
            _(u"Validation  Tree Background Color:"), width=350)
        _fixed.put(_label, 5, 525)
        _fixed.put(self.btnValidationBGColor, 340, 525)
        _label = Widgets.make_label(
            _(u"Validation Tree Foreground Color:"), width=350)
        _fixed.put(_label, 5, 555)
        _fixed.put(self.btnValidationFGColor, 340, 555)
        _label = Widgets.make_label(
            _(u"Incident Tree Background Color:"), width=350)
        _fixed.put(_label, 5, 585)
        _fixed.put(self.btnIncidentBGColor, 340, 585)
        _label = Widgets.make_label(
            _(u"Incident Tree Foreground Color:"), width=350)
        _fixed.put(_label, 5, 615)
        _fixed.put(self.btnIncidentFGColor, 340, 615)
        _label = Widgets.make_label(
            _(u"Testing Tree Background Color:"), width=350)
        _fixed.put(_label, 5, 645)
        _fixed.put(self.btnTestingBGColor, 340, 645)
        _label = Widgets.make_label(
            _(u"Testing Tree Foreground Color:"), width=350)
        _fixed.put(_label, 5, 675)
        _fixed.put(self.btnTestingFGColor, 340, 675)

        self.btnRevisionBGColor.connect('color-set', self._set_color, 0)
        self.btnRevisionFGColor.connect('color-set', self._set_color, 1)
        self.btnFunctionBGColor.connect('color-set', self._set_color, 2)
        self.btnFunctionFGColor.connect('color-set', self._set_color, 3)
        self.btnRequirementsBGColor.connect('color-set', self._set_color, 4)
        self.btnRequirementsFGColor.connect('color-set', self._set_color, 5)
        self.btnHardwareBGColor.connect('color-set', self._set_color, 6)
        self.btnHardwareFGColor.connect('color-set', self._set_color, 7)
        self.btnSoftwareBGColor.connect('color-set', self._set_color, 21)
        self.btnSoftwareFGColor.connect('color-set', self._set_color, 22)
        self.btnValidationBGColor.connect('color-set', self._set_color, 10)
        self.btnValidationFGColor.connect('color-set', self._set_color, 11)
        self.btnIncidentBGColor.connect('color-set', self._set_color, 12)
        self.btnIncidentFGColor.connect('color-set', self._set_color, 13)
        self.btnTestingBGColor.connect('color-set', self._set_color, 14)
        self.btnTestingFGColor.connect('color-set', self._set_color, 15)

        _label = gtk.Label(_(u"Look & Feel"))
        _label.set_tooltip_text(_(u"Allows setting default values in RTK."))
        self.notebook.insert_page(_fixed, tab_label=_label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        # ----- ----- ----- - Create list edit options - ----- ----- ----- #
        _vpaned = gtk.VPaned()

        _fixed = gtk.Fixed()
        _vpaned.pack1(_fixed)

        self.tvwListEditor = gtk.TreeView()
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING)
        self.tvwListEditor.set_model(_model)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.tvwListEditor)
        _vpaned.pack2(_scrollwindow)

        # ----- ----- ----- ----- - RTK-wide Lists - ----- ----- ----- ----- #
        self.rdoUsers = gtk.RadioButton(
            group=None, label=_(u"Edit list of "
                                u"RTK users"))
        self.rdoStatus = gtk.RadioButton(
            group=self.rdoUsers, label=_(u"Edit status list"))
        self.rdoManufacturers = gtk.RadioButton(
            group=self.rdoUsers, label=_(u"Edit list of "
                                         u"manufacturers"))

        # ----- ----- ----- ----- Requirement Lists ----- ----- ----- ----- #
        self.rdoRequirementTypes = gtk.RadioButton(
            group=self.rdoUsers, label=_(u"Edit requirement "
                                         u"types"))
        self.rdoWorkgroups = gtk.RadioButton(
            group=self.rdoUsers, label=_(u"Edit workgroup list"))

        # ----- ----- ----- ---- FMEA and HazOp Lists ---- ----- ----- ----- #
        self.rdoSeverity = gtk.RadioButton(
            group=self.rdoUsers, label=_(u"Edit failure severity "
                                         u"list"))
        self.rdoFailureProb = gtk.RadioButton(
            group=self.rdoUsers, label=_(u"Edit failure "
                                         u"probability list"))
        self.rdoFMEAActionCat = gtk.RadioButton(
            group=self.rdoUsers,
            label=_(u"Edit FMEA action "
                    u"category list"))
        self.rdoFMEAControls = gtk.RadioButton(
            group=self.rdoUsers, label=_(u"Edit list of FMEA "
                                         u"controls"))
        self.rdoHazard = gtk.RadioButton(
            group=self.rdoUsers, label=_(u"Edit potential hazards "
                                         u"list"))

        # ----- ----- ----- ----- --- PoF Lists --- ----- ----- ----- ----- #
        self.rdoDamageModel = gtk.RadioButton(
            group=self.rdoUsers, label=_(u"Edit list of damage "
                                         u"models"))
        self.rdoPoFPriority = gtk.RadioButton(
            group=self.rdoUsers,
            label=_(u"Edit list of PoF "
                    u"action priorities"))
        self.rdoMeasParam = gtk.RadioButton(
            group=self.rdoUsers,
            label=_(u"Edit list of field "
                    u"measurable parameters"))
        self.rdoClassMeans = gtk.RadioButton(
            group=self.rdoUsers,
            label=_(u"Edit list of methods "
                    u"for classifying "
                    u"loads"))

        # ----- ----- ----- ----- - Software Lists - ----- ----- ----- ----- #
        self.rdoSWAppType = gtk.RadioButton(
            group=self.rdoUsers,
            label=_(u"Edit list of software "
                    u"application types"))
        self.rdoSWDevPhase = gtk.RadioButton(
            group=self.rdoUsers,
            label=_(u"Edit list of "
                    u"software development "
                    u"phases"))

        # ----- ----- ----- ----- Validation Lists ----- ----- ----- ----- #
        self.rdoVandVTasks = gtk.RadioButton(
            group=self.rdoUsers, label=_(u"Edit V&V activity "
                                         u"types"))
        self.rdoMeasurement = gtk.RadioButton(
            group=self.rdoUsers, label=_(u"Edit measurement "
                                         u"units"))

        # ----- ----- ----- ----- Incident Lists ----- ----- ----- ----- #
        self.rdoIncidentType = gtk.RadioButton(
            group=self.rdoUsers, label=_(u"Edit list of "
                                         u"incident types"))
        self.rdoIncidentCategory = gtk.RadioButton(
            group=self.rdoUsers,
            label=_(u"Edit list of "
                    u"incident "
                    u"categories"))
        self.rdoIncidentCriticality = gtk.RadioButton(
            group=self.rdoUsers,
            label=_(u"Edit list of "
                    u"incident "
                    u"criticalities"))
        self.rdoLifeCycle = gtk.RadioButton(
            group=self.rdoUsers, label=_(u"Edit product life-cycle "
                                         u"list"))
        self.rdoDetectionMethod = gtk.RadioButton(
            group=self.rdoUsers,
            label=_(u"Edit list of "
                    u"detection "
                    u"methods"))

        self.btnListEdit = gtk.Button(_(u"Edit List"))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/edit.png')
        self.btnListEdit.set_image(_image)
        self.btnListEdit.connect('clicked', self._edit_list)

        self.btnListAdd = gtk.Button(_(u"Add Item"))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/add.png')
        self.btnListAdd.set_image(_image)
        self.btnListAdd.connect('clicked', self._add_to_list)

        self.btnListRemove = gtk.Button(_(u"Remove Item"))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/remove.png')
        self.btnListRemove.set_image(_image)
        self.btnListRemove.connect('clicked', self._remove_from_list)

        _fixed.put(self.rdoUsers, 5, 5)
        _fixed.put(self.rdoStatus, 5, 35)
        _fixed.put(self.rdoManufacturers, 5, 65)
        _fixed.put(self.rdoRequirementTypes, 5, 95)
        _fixed.put(self.rdoWorkgroups, 5, 125)
        _fixed.put(self.rdoSeverity, 5, 155)
        _fixed.put(self.rdoFailureProb, 5, 185)
        _fixed.put(self.rdoFMEAActionCat, 5, 215)
        _fixed.put(self.rdoFMEAControls, 5, 245)
        self.rdoFMEAControls.set_sensitive(False)
        _fixed.put(self.rdoHazard, 5, 275)
        _fixed.put(self.rdoDamageModel, 5, 305)
        self.rdoDamageModel.set_sensitive(False)
        _fixed.put(self.rdoPoFPriority, 5, 335)
        self.rdoPoFPriority.set_sensitive(False)
        _fixed.put(self.rdoMeasParam, 305, 5)
        _fixed.put(self.rdoClassMeans, 305, 35)
        self.rdoClassMeans.set_sensitive(False)
        _fixed.put(self.rdoSWAppType, 305, 65)
        _fixed.put(self.rdoSWDevPhase, 305, 95)
        _fixed.put(self.rdoVandVTasks, 305, 125)
        _fixed.put(self.rdoMeasurement, 305, 155)
        _fixed.put(self.rdoIncidentType, 305, 185)
        _fixed.put(self.rdoIncidentCategory, 305, 215)
        _fixed.put(self.rdoIncidentCriticality, 305, 245)
        self.rdoIncidentCriticality.set_sensitive(False)
        _fixed.put(self.rdoLifeCycle, 305, 275)
        _fixed.put(self.rdoDetectionMethod, 305, 305)
        self.rdoDetectionMethod.set_sensitive(False)
        _fixed.put(self.btnListEdit, 5, 375)
        _fixed.put(self.btnListAdd, 105, 375)
        _fixed.put(self.btnListRemove, 215, 375)

        for i in range(5):
            _cell = gtk.CellRendererText()
            _cell.set_property('background', '#FFFFFF')
            _cell.set_property('editable', 1)
            _cell.set_property('foreground', '#000000')
            _cell.set_property('wrap-width', 250)
            _cell.set_property('wrap-mode', pango.WRAP_WORD)
            _cell.connect('edited', self._cell_edit, i, _model)

            _column = gtk.TreeViewColumn()
            _column.set_alignment(0.5)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=i)

            self.tvwListEditor.append_column(_column)

        _label = gtk.Label(_(u"Edit Lists"))
        _label.set_tooltip_text(_(u"Allows editing of lists used in RTK."))
        self.notebook.insert_page(_vpaned, tab_label=_label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        # ----- ----- ----- -- Create tree edit options - ----- ----- ----- #
        _fixed = gtk.Fixed()

        self.rdoRevision = gtk.RadioButton(
            group=None, label=_(u"Edit Revision tree "
                                u"layout"))
        self.rdoFunction = gtk.RadioButton(
            group=self.rdoRevision, label=_(u"Edit Function tree "
                                            u"layout"))
        self.rdoRequirement = gtk.RadioButton(
            group=self.rdoRevision,
            label=_(u"Edit Requirement tree "
                    u"layout"))
        self.rdoHardware = gtk.RadioButton(
            group=self.rdoRevision, label=_(u"Edit Hardware tree "
                                            u"layout"))
        self.rdoSoftware = gtk.RadioButton(
            group=self.rdoRevision, label=_(u"Edit Software tree "
                                            u"layout"))
        self.rdoValidation = gtk.RadioButton(
            group=self.rdoRevision, label=_(u"Edit V&V tree layout"))
        self.rdoIncident = gtk.RadioButton(
            group=self.rdoRevision,
            label=_(u"Edit Program Incident "
                    u"tree layout"))
        self.rdoTesting = gtk.RadioButton(
            group=self.rdoRevision, label=_(u"Edit Testing tree layout"))
        self.rdoSurvival = gtk.RadioButton(
            group=self.rdoRevision,
            label=_(u"Edit Survival Analysis "
                    u"tree layout"))

        self.rdoPart = gtk.RadioButton(
            group=self.rdoRevision, label=_(u"Edit Part list layout"))

        self.rdoAllocation = gtk.RadioButton(
            group=self.rdoRevision,
            label=_(u"Edit Reliability "
                    u"Allocation worksheet "
                    u"layout"))
        self.rdoRiskAnalysis = gtk.RadioButton(
            group=self.rdoRevision,
            label=_(u"Edit Risk Analysis "
                    u"worksheet layout"))
        self.rdoSimilarItem = gtk.RadioButton(
            group=self.rdoRevision,
            label=_(u"Edit Similar Item "
                    u"Analysis worksheet "
                    u"layout"))
        self.rdoFMECA = gtk.RadioButton(
            group=self.rdoRevision,
            label=_(u"Edit FMEA/FMECA worksheet "
                    u"layout"))

        self.btnTreeEdit = gtk.Button(stock=gtk.STOCK_EDIT)
        self.btnTreeEdit.connect('button-release-event', self._edit_tree)

        _fixed.put(self.rdoRevision, 5, 5)
        _fixed.put(self.rdoFunction, 5, 35)
        _fixed.put(self.rdoRequirement, 5, 65)
        _fixed.put(self.rdoHardware, 5, 95)
        _fixed.put(self.rdoSoftware, 5, 125)
        _fixed.put(self.rdoValidation, 5, 155)
        _fixed.put(self.rdoTesting, 5, 185)
        _fixed.put(self.rdoIncident, 5, 215)
        _fixed.put(self.rdoSurvival, 5, 245)
        # _fixed.put(self.rdoAllocation, 5, 275)
        _fixed.put(self.rdoPart, 5, 275)
        _fixed.put(self.rdoRiskAnalysis, 5, 305)
        _fixed.put(self.rdoSimilarItem, 5, 335)
        _fixed.put(self.rdoFMECA, 5, 365)
        _fixed.put(self.btnTreeEdit, 5, 405)

        _label = gtk.Label(_(u"Edit Tree Layouts"))
        _label.set_tooltip_text(
            _(u"Allows editing of tree layouts used in "
              u"RTK."))
        self.notebook.insert_page(_fixed, tab_label=_label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        # ----- ----- ----- Create tree edit gtk.TreeView ----- ----- ----- #
        _labels = [
            _(u"Default\nTitle"),
            _(u"User\nTitle"),
            _(u"Column\nPosition"),
            _(u"Can\nEdit?"),
            _(u"Is\nVisible?")
        ]

        _vbox = gtk.VBox()

        self.tvwEditTree = gtk.TreeView()
        _model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING)
        self.tvwEditTree.set_model(_model)

        for i in range(5):
            if i == 0:
                _cell = gtk.CellRendererText()
                _cell.set_property('background', 'light gray')
                _cell.set_property('editable', 0)
                _cell.set_property('foreground', '#000000')
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD)
            elif i > 0 and i < 3:
                _cell = gtk.CellRendererText()
                _cell.set_property('background', '#FFFFFF')
                _cell.set_property('editable', 1)
                _cell.set_property('foreground', '#000000')
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD)
                _cell.connect('edited', self._cell_edit, i, _model)
            elif i > 4:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
            else:
                _cell = gtk.CellRendererToggle()
                _cell.set_property('activatable', 1)
                _cell.connect('toggled', self._cell_toggled, i, _model)

            _label = gtk.Label()
            _label.set_line_wrap(True)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_markup("<span weight='bold'>" + _labels[i] + "</span>")
            _label.show_all()

            _column = gtk.TreeViewColumn()
            _column.set_widget(_label)
            _column.set_alignment(0.5)
            _column.pack_start(_cell, True)
            if i < 3:
                _column.set_attributes(_cell, text=i)
            elif i > 4:
                _column.set_visible(0)
            else:
                _column.set_attributes(_cell, active=i)

            self.tvwEditTree.append_column(_column)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.tvwEditTree)

        _vbox.pack_start(_scrollwindow)

        _fixed = gtk.Fixed()

        self.btnSave = gtk.Button(_(u"Save"))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/save.png')
        self.btnSave.set_image(_image)
        self.btnSave.connect('clicked', self._save_options)

        self.btnQuit = gtk.Button(_(u"Close"), stock=gtk.STOCK_CANCEL)
        self.btnQuit.connect('clicked', self._quit)

        _vbox.pack_end(_fixed, expand=False)

        _label = gtk.Label(_(u"Editor"))
        _label.set_tooltip_text(_(u"Displays the editor."))
        self.notebook.insert_page(_vbox, tab_label=_label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        _vbox = gtk.VBox()
        _vbox.pack_start(self.notebook)

        _buttonbox = gtk.HButtonBox()
        _buttonbox.set_layout(gtk.BUTTONBOX_END)
        _buttonbox.pack_start(self.btnSave)
        _buttonbox.pack_start(self.btnQuit)
        _vbox.pack_end(_buttonbox, expand=False)

        self.add(_vbox)

        self._load_defaults()

        self.show_all()

    def _load_defaults(self):
        """
        Method to load the current default values from the RTK configuration
        file.
        """

        _tab_pos = {'bottom': 0, 'left': 1, 'right': 2, 'top': 3}

        # Make a backup of the original configuration file.
        _conf_file = Configuration.CONF_DIR + 'RTK.conf'
        self.set_title(_(u"RTK - Options ({0:s})").format(_conf_file))

        _parser = SafeConfigParser()

        if Utilities.file_exists(_conf_file):
            _parser.read(_conf_file)

            # Set tab positions.
            self.cmbModuleBookTabPosition.set_active(_tab_pos[_parser.get(
                'General', 'moduletabpos')])
            self.cmbWorkBookTabPosition.set_active(_tab_pos[_parser.get(
                'General', 'worktabpos')])
            self.cmbListBookTabPosition.set_active(_tab_pos[_parser.get(
                'General', 'listtabpos')])

            # Set numerical values.
            self.txtFRMultiplier.set_text(
                str(_parser.get('General', 'frmultiplier')))
            self.txtDecimalPlaces.set_text(
                str(_parser.get('General', 'decimal')))
            self.txtMissionTime.set_text(
                str(_parser.get('General', 'calcreltime')))

            # Set color options.
            try:
                _color = gtk.gdk.Color(
                    '%s' % _parser.get('Colors', 'revisionbg'))
                self.btnRevisionBGColor.set_color(_color)
            except ValueError:
                self.btnRevisionBGColor.set_color(gtk.gdk.Color('#FFFFFF'))
            try:
                _color = gtk.gdk.Color(
                    '%s' % _parser.get('Colors', 'revisionfg'))
                self.btnRevisionFGColor.set_color(_color)
            except ValueError:
                self.btnRevisionFGColor.set_color(gtk.gdk.Color('#000000'))
            try:
                _color = gtk.gdk.Color(
                    '%s' % _parser.get('Colors', 'functionbg'))
                self.btnFunctionBGColor.set_color(_color)
            except ValueError:
                self.btnFunctionBGColor.set_color(gtk.gdk.Color('#FFFFFF'))
            try:
                _color = gtk.gdk.Color(
                    '%s' % _parser.get('Colors', 'functionfg'))
                self.btnFunctionFGColor.set_color(_color)
            except ValueError:
                self.btnFunctionFGColor.set_color(gtk.gdk.Color('#000000'))
            try:
                _color = gtk.gdk.Color(
                    '%s' % _parser.get('Colors', 'requirementbg'))
                self.btnRequirementsBGColor.set_color(_color)
            except ValueError:
                self.btnRequirementsBGColor.set_color(gtk.gdk.Color('#FFFFFF'))
            try:
                _color = gtk.gdk.Color(
                    '%s' % _parser.get('Colors', 'requirementfg'))
                self.btnRequirementsFGColor.set_color(_color)
            except ValueError:
                self.btnRequirementsFGColor.set_color(gtk.gdk.Color('#000000'))
            try:
                _color = gtk.gdk.Color(
                    '%s' % _parser.get('Colors', 'assemblybg'))
                self.btnHardwareBGColor.set_color(_color)
            except ValueError:
                self.btnHardwareBGColor.set_color(gtk.gdk.Color('#FFFFFF'))
            try:
                _color = gtk.gdk.Color(
                    '%s' % _parser.get('Colors', 'assemblyfg'))
                self.btnHardwareFGColor.set_color(_color)
            except (ValueError, NoOptionError):
                self.btnHardwareFGColor.set_color(gtk.gdk.Color('#000000'))
            try:
                _color = gtk.gdk.Color(
                    '%s' % _parser.get('Colors', 'validationbg'))
                self.btnValidationBGColor.set_color(_color)
            except ValueError:
                self.btnValidationBGColor.set_color(gtk.gdk.Color('#FFFFFF'))
            try:
                _color = gtk.gdk.Color(
                    '%s' % _parser.get('Colors', 'validationfg'))
                self.btnValidationFGColor.set_color(_color)
            except ValueError:
                self.btnValidationFGColor.set_color(gtk.gdk.Color('#000000'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors', 'rgbg'))
                self.btnTestingBGColor.set_color(_color)
            except ValueError:
                self.btnTestingBGColor.set_color(gtk.gdk.Color('#FFFFFF'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors', 'rgfg'))
                self.btnTestingFGColor.set_color(_color)
            except ValueError:
                self.btnTestingFGColor.set_color(gtk.gdk.Color('#000000'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors', 'fracabg'))
                self.btnIncidentBGColor.set_color(_color)
            except ValueError:
                self.btnIncidentBGColor.set_color(gtk.gdk.Color('#FFFFFF'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors', 'fracafg'))
                self.btnIncidentFGColor.set_color(_color)
            except ValueError:
                self.btnIncidentFGColor.set_color(gtk.gdk.Color('#000000'))

        return False

    @staticmethod
    def _set_color(colorbutton, rtk_colors):
        """
        Method to set the selected color.

        :param gtk.ColorButton colorbutton: the gtk.ColorButton() that called
                                            this method.
        :param int rtk_colors: the position in the RTK_COLORS global variable.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Retrieve the six digit hexidecimal version of the selected color.
        _color = colorbutton.get_color()
        try:
            _red = "{0:#0{1}}".format('%X' % int(_color.red / 255), 2)
        except ValueError:
            _red = '%X' % int(_color.red / 255)
        try:
            _green = "{0:#0{1}}".format('%X' % int(_color.green / 255), 2)
        except ValueError:
            _green = '%X' % int(_color.green / 255)
        try:
            _blue = "{0:#0{1}}".format('%X' % int(_color.blue / 255), 2)
        except ValueError:
            _blue = '%X' % int(_color.blue / 255)
        _color = '#%s%s%s' % (_red, _green, _blue)

        # Set the color variable.
        Configuration.RTK_COLORS[rtk_colors] = _color

        return False

    def _edit_tree(self, __button, __event):
        """
        Method to edit gtk.TreeView() layouts.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from lxml import etree

        (_name, _fmt_idx) = self._get_format_info()

        # Retrieve the default heading text from the format file.
        _path = "/root/tree[@name='%s']/column/defaulttitle" % _name
        _default = etree.parse(
            Configuration.RTK_FORMAT_FILE[_fmt_idx]).xpath(_path)

        # Retrieve the default heading text from the format file.
        _path = "/root/tree[@name='%s']/column/usertitle" % _name
        _user = etree.parse(
            Configuration.RTK_FORMAT_FILE[_fmt_idx]).xpath(_path)

        # Retrieve the column position from the format file.
        _path = "/root/tree[@name='%s']/column/position" % _name
        _position = etree.parse(
            Configuration.RTK_FORMAT_FILE[_fmt_idx]).xpath(_path)

        # Retrieve whether or not the column is editable from the format file.
        _path = "/root/tree[@name='%s']/column/editable" % _name
        _editable = etree.parse(
            Configuration.RTK_FORMAT_FILE[_fmt_idx]).xpath(_path)

        # Retrieve whether or not the column is visible from the format file.
        _path = "/root/tree[@name='%s']/column/visible" % _name
        _visible = etree.parse(
            Configuration.RTK_FORMAT_FILE[_fmt_idx]).xpath(_path)

        # Retrieve datatypes from the format file.
        _path = "/root/tree[@name='%s']/column/datatype" % _name
        _datatype = etree.parse(
            Configuration.RTK_FORMAT_FILE[_fmt_idx]).xpath(_path)

        # Retrieve widget types from the format file.
        _path = "/root/tree[@name='%s']/column/widget" % _name
        _widget = etree.parse(
            Configuration.RTK_FORMAT_FILE[_fmt_idx]).xpath(_path)

        _model = self.tvwEditTree.get_model()
        _model.clear()

        for _index, __ in enumerate(_default):
            _data = [
                _default[_index].text, _user[_index].text,
                int(_position[_index].text),
                int(_editable[_index].text),
                int(_visible[_index].text), _datatype[_index].text,
                _widget[_index].text
            ]
            _model.append(_data)

        if Configuration.RTK_PROG_INFO[2] == '':
            self.notebook.set_current_page(3)
        else:
            self.notebook.set_current_page(4)
        _child = self.notebook.get_nth_page(self.notebook.get_current_page())
        self.notebook.set_tab_label_text(_child, _(u"Edit %s Tree" % _name))

        return False

    def _cell_edit(self, __cell, path, new_text, position, model):
        """
        Called whenever a gtk.TreeView() gtk.CellRenderer() is edited.

        :param __cell: the gtk.CellRenderer() that was edited.
        :type __cell: gtk.CellRenderer
        :param path: the gtk.TreeView() path of the gtk.CellRenderer() that was
                     edited.
        :type path: string
        :param new_text: the new text in the edited gtk.CellRenderer().
        :type new_text: string
        :param position: the column position of the edited gtk.CellRenderer().
        :type position: integer
        :param model: the gtk.TreeModel() the gtk.CellRenderer() belongs to.
        :type model: gtk.TreeModel
        """

        _type = gobject.type_name(model.get_column_type(position))

        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        return False

    def _cell_toggled(self, cell, path, position, model):
        """
        Called whenever a gtl.TreeView() gtk.CellRenderer() is edited.

        :param cell: the gtk.CellRenderer() that was edited.
        :param path: the gtk.TreeView() path of the gtk.CellRenderer() that
                     was edited.
        :param position: the column position of the edited gtk.CellRenderer().
        :param model: the gtk.TreeModel() the gtk.CellRenderer() belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        model[path][position] = not cell.get_active()

        return False

    def _edit_list(self, __button):
        """
        Method to edit drop down list items.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if self.rdoUsers.get_active():
            _query = "SELECT fld_user_id, fld_user_lname, fld_user_fname, \
                             fld_user_email, fld_user_phone, fld_user_group \
                      FROM tbl_users \
                      ORDER BY fld_user_lname, fld_user_fname"

            _header = [
                "", "User Last Name", "User First Name", "eMail", "Phone",
                "Work Group"
            ]
            _pad = ()
            _table = 'tbl_usres'
        elif self.rdoStatus.get_active():
            _query = "SELECT fld_status_id, fld_status_name, \
                             fld_status_description \
                      FROM tbl_status \
                      ORDER BY fld_status_name"

            _header = ["", "Status", "Description", "", "", ""]
            _pad = ('', '', '')
            _table = 'tbl_status'
        elif self.rdoManufacturers.get_active():
            _query = "SELECT fld_manufacturers_id, fld_manufacturers_noun, \
                             fld_location, fld_cage_code \
                      FROM tbl_manufacturers \
                      ORDER BY fld_manufacturers_noun ASC"

            _header = ["", "Manufacturer", "Location", "CAGE Code", "", ""]
            _pad = ('', '')
            _table = 'tbl_manufacturers'
        elif self.rdoRequirementTypes.get_active():
            _query = "SELECT fld_requirement_type_id, \
                             fld_requirement_type_desc, \
                             fld_requirement_type_code \
                      FROM tbl_requirement_type \
                      ORDER BY fld_requirement_type_desc ASC"

            _header = ["", "Requirement Type", "Code", "", "", ""]
            _pad = ('', '', '')
            _table = 'tbl_requirement_type'
        elif self.rdoWorkgroups.get_active():
            _query = "SELECT fld_group_id, fld_group_name \
                      FROM tbl_groups \
                      ORDER BY fld_group_name ASC"

            _header = ["", "Work Group", "", "", "", ""]
            _pad = ('', '', '', '')
            _table = 'tbl_groups'
        elif self.rdoSeverity.get_active():
            _query = "SELECT fld_severity_id, fld_name, fld_category, \
                             fld_description \
                      FROM tbl_severity \
                      ORDER BY fld_name ASC"

            _header = [
                "", "Severity Name", "Severity Category", "Description", "", ""
            ]
            _pad = ('', '')
            _table = 'tbl_severity'
        elif self.rdoFailureProb.get_active():
            _query = "SELECT fld_probability_id, fld_probability_name, \
                             fld_probability_value \
                      FROM tbl_failure_probability \
                      ORDER BY fld_probability_value DESC"

            _header = ["", "Probability Name", "Probability Value", "", "", ""]
            _pad = ('', '', '')
            _table = 'tbl_failure_probability'
        elif self.rdoFMEAActionCat.get_active():
            _query = "SELECT fld_action_id, fld_action_name \
                      FROM tbl_action_category \
                      ORDER BY fld_action_name"

            _header = ["", "Action", "", "", "", ""]
            _pad = ('', '', '', '')
            _table = 'tbl_action_category'
        elif self.rdoFMEAControls.get_active():
            print "Edit FMEA controls"
        elif self.rdoHazard.get_active():
            _query = "SELECT fld_hazard_id, fld_category, fld_subcategory \
                      FROM tbl_hazards \
                      ORDER BY fld_category, fld_subcategory"

            _header = ["", "Hazard Category", "Hazard", "", "", ""]
            _pad = ('', '', '')
            _table = 'tbl_hazards'
        elif self.rdoDamageModel.get_active():
            print "Edit damage models"
        elif self.rdoPoFPriority.get_active():
            print "Edit PoF priority"
        elif self.rdoMeasParam.get_active():
            _query = "SELECT fld_measurement_id, fld_measurement_name \
                      FROM tbl_measurements \
                      ORDER BY fld_measurement_name"

            _header = ["", "Measurement", "", "", "", ""]
            _pad = ('', '', '', '')
            _table = 'tbl_measurements'
        elif self.rdoClassMeans.get_active():
            print "Edit classification means"
        elif self.rdoSWAppType.get_active():
            _query = "SELECT fld_application_id, fld_application_desc, \
                             fld_fault_density, fld_transformation_ratio \
                      FROM tbl_software_application \
                      ORDER BY fld_application_desc"

            _header = [
                "", "Application", "Fault Density", "Transformation Ratio", "",
                ""
            ]
            _pad = ('', '')
            _table = 'tbl_software_application'
        elif self.rdoSWDevPhase.get_active():
            _query = "SELECT fld_phase_id, fld_phase_desc \
                      FROM tbl_development_phase \
                      ORDER BY fld_phase_desc"

            _header = ["", "Development Phase", "", "", "", ""]
            _pad = ('', '', '', '')
            _table = 'tbl_development_phase'
        elif self.rdoVandVTasks.get_active():
            _query = "SELECT fld_validation_type_id, \
                             fld_validation_type_desc, \
                             fld_validation_type_code \
                      FROM tbl_validation_type \
                      ORDER BY fld_validation_type_desc"

            _header = ["", "Validation Type", "Code", "", "", ""]
            _pad = ('', '', '')
            _table = 'tbl_validation_type'
        elif self.rdoMeasurement.get_active():
            _query = "SELECT fld_measurement_id, fld_measurement_code \
                      FROM tbl_measurement_units \
                      ORDER BY fld_measurement_code ASC"

            _header = ["", "Measurement Unit", "", "", "", ""]
            _pad = ('', '', '', '')
            _table = 'tbl_measurement_units'
        elif self.rdoIncidentType.get_active():
            _query = "SELECT fld_incident_type_id, fld_incident_type_name \
                      FROM tbl_incident_type \
                      ORDER BY fld_incident_type_name"

            _header = ["", "Incident Type", "", "", "", ""]
            _pad = ('', '', '', '')
            _table = 'tbl_incident_type'
        elif self.rdoIncidentCategory.get_active():
            _query = "SELECT fld_incident_cat_id, fld_incident_cat_name \
                      FROM tbl_incident_category \
                      ORDER BY fld_incident_cat_name"

            _header = ["", "Incident Category", "", "", "", ""]
            _pad = ('', '', '', '')
            _table = 'tbl_incident_category'
        elif self.rdoIncidentCriticality.get_active():
            print "Edit incident criticality"
        elif self.rdoLifeCycle.get_active():
            _query = "SELECT fld_lifecycle_id, fld_lifecycle_name \
                      FROM tbl_lifecycles \
                      ORDER BY fld_lifecycle_name"

            _header = ["", "Lifecycle", "", "", "", ""]
            _pad = ('', '', '', '')
            _table = 'tbl_lifecycles'
        elif self.rdoDetectionMethod.get_active():
            print "Edit detection methods"

        (_results, _error_code, __) = self._mdcRTK.site_dao.execute(
            _query, commit=False)
        self._last_id = self._mdcRTK.site_dao.get_last_id(_table)[0]
        try:
            _n_entries = len(_results)
        except TypeError:
            _n_entries = 0

        # Update the column headings and set appropriate columns visible.
        _columns = self.tvwListEditor.get_columns()
        for _index, _column in enumerate(_columns):
            _column.set_title(_header[_index])
            if _header[_index] == '':
                _column.set_visible(False)
            else:
                _column.set_visible(True)

        # Load the results.
        _model = self.tvwListEditor.get_model()
        _model.clear()
        for i in range(_n_entries):
            _model.append(_results[i] + _pad)

        return False

    def _add_to_list(self, __button):
        """
        Method to add a row to the list editor gtk.TreeView().

        :param gtk.Button __button: the gtk.Button() that called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Add a new row.
        self._last_id += 1
        _model = self.tvwListEditor.get_model()
        _row = _model.append([self._last_id, "", "", "", "", ""])

        # Select and activate the new row.
        _path = _model.get_path(_row)
        _column = self.tvwListEditor.get_column(1)
        self.tvwListEditor.row_activated(_path, _column)
        self.tvwListEditor.set_cursor(_path, _column, True)

        return False

    def _remove_from_list(self, __button):
        """
        Method to remove the selected row from the list editor gtk.TreeView().

        :param gtk.Button __button: the gtk.Button() that called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_model, _row) = self.tvwListEditor.get_selection().get_selected()

        if self.rdoMeasurement.get_active():
            _query = "DELETE FROM tbl_measurement_units \
                      WHERE fld_measurement_id=%d"                                                                                                                                                                                                                                                                                                             % \
                     _model.get_value(_row, 0)
        elif self.rdoRequirementTypes.get_active():
            _query = "DELETE FROM tbl_requirement_type \
                      WHERE fld_requirement_type_id=%d"                                                                                                                                                                                                                                                                                                                                           % \
                     _model.get_value(_row, 0)
        elif self.rdoVandVTasks.get_active():
            _query = "DELETE tbl_validation_type \
                      WHERE fld_validation_type_id=%d"                                                                                                                                                                                                                                                                                                                                     % \
                     _model.get_value(_row, 0)
        elif self.rdoUsers.get_active():
            Widgets.rtk_information(
                _(u"You cannot remove a user from the RTK "
                  u"Program.  Retaining all users, past "
                  u"and present, is necessary to ensure "
                  u"audit trails remain intact."))
            return False
        elif self.rdoWorkgroups.get_active():
            Widgets.rtk_information(
                _(u"You cannot remove a workgroup from "
                  u"the RTK Program.  Retaining all "
                  u"workgroups, past and present, is "
                  u"necessary to ensure audit trails "
                  u"remain intact."))
            return False

        if not self._mdcRTK.site_dao.execute(_query, commit=True):
            Widgets.rtk_error(_(u"Problem removing entry from list."))
            return True

        _model.remove(_row)

        return False

    def _get_format_info(self):
        """
        Method to retrieve the name and index of the selected format file.
        """

        if self.rdoRevision.get_active():
            _name = 'Revision'
            _fmt_idx = 0
        elif self.rdoFunction.get_active():
            _name = 'Function'
            _fmt_idx = 1
        elif self.rdoRequirement.get_active():
            _name = 'Requirement'
            _fmt_idx = 2
        elif self.rdoHardware.get_active():
            _name = 'Hardware'
            _fmt_idx = 3
        elif self.rdoSoftware.get_active():
            _name = 'Software'
            _fmt_idx = 15
        elif self.rdoValidation.get_active():
            _name = 'Validation'
            _fmt_idx = 4
        elif self.rdoTesting.get_active():
            _name = 'Testing'
            _fmt_idx = 11
        elif self.rdoIncident.get_active():
            _name = 'Incidents'
            _fmt_idx = 14
        elif self.rdoSurvival.get_active():
            _name = 'Dataset'
            _fmt_idx = 16
        elif self.rdoPart.get_active():
            _name = 'Parts'
            _fmt_idx = 7
        elif self.rdoRiskAnalysis.get_active():
            _name = 'Risk'
            _fmt_idx = 17
        elif self.rdoSimilarItem.get_active():
            _name = 'SIA'
            _fmt_idx = 8
        elif self.rdoFMECA.get_active():
            _name = 'FMECA'
            _fmt_idx = 9

        return _name, _fmt_idx

    def _save_options(self, __button):
        """
        Method to select the proper save function depending on the selected
        page in the gtk.Notebook().

        :param gtk.Button __button: the gtk.Button() that called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from shutil import copyfile

        # Make a backup of the original configuration file.
        _conf_file = Configuration.CONF_DIR + 'RTK.conf'
        copyfile(_conf_file, _conf_file + '.bak')

        # Find out which page is selected in the gtk.Notebook().
        _page = self.notebook.get_current_page()
        if Configuration.RTK_PROG_INFO[2] == '':
            _page += 1

        # Call the proper save function.
        if _page == 0:
            _error = self._save_modules()
        elif _page == 1:
            _error = self._save_defaults()
        elif _page == 2:
            _error = self._save_list()
        elif _page == 4:
            _error = self._save_tree_layout()

        if _error:
            Widgets.rtk_warning(
                _(u"Problem saving your RTK configuration.  "
                  u"Restoring previous configuration values."))
            copyfile(_conf_file + '.bak', _conf_file)
            return True

        return False

    def _save_modules(self):
        """
        Method to save the configuration changes made by the user.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Save the active modules for the open RTK Program database.
        if Configuration.RTK_PROG_INFO[2] != '':
            _values = (self.chkRevisions.get_active(),
                       self.chkFunctions.get_active(),
                       self.chkRequirements.get_active(),
                       self.chkSoftware.get_active(),
                       self.chkValidation.get_active(),
                       self.chkRG.get_active(), 0,
                       self.chkIncidents.get_active(), 0,
                       self.chkSurvivalAnalysis.get_active(), 0, 0)

            _query = "UPDATE tbl_program_info \
                      SET fld_revision_active=%d, fld_function_active=%d, \
                          fld_requirement_active=%d, fld_software_active=%d, \
                          fld_vandv_active=%d, fld_testing_active=%d, \
                          fld_rcm_active=%d, fld_fraca_active=%d, \
                          fld_fmeca_active=%d, fld_survival_active=%d, \
                          fld_rbd_active=%d, fld_fta_active=%d" % _values
            if not self._mdcRTK.project_dao.execute(_query, commit=True):
                return True

        return False

    def _save_defaults(self):
        """
        Method to save the default values to the RTK configuration file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _conf_file = Configuration.CONF_DIR + 'RTK.conf'

        _parser = SafeConfigParser()

        # Write the new colors to the configuration file.
        if Utilities.file_exists(_conf_file):
            _parser.read(_conf_file)

            try:
                _parser.set('General', 'frmultiplier',
                            str(float(self.txtFRMultiplier.get_text()) / 1.0))
            except ValueError:
                _parser.set('General', 'frmultiplier', '1.0')

            try:
                _parser.set('General', 'calcreltime',
                            str(float(self.txtMissionTime.get_text()) / 1.0))
            except ValueError:
                _parser.set('General', 'calcreltime', '10.0')

            try:
                _parser.set('General', 'decimal',
                            str(int(self.txtDecimalPlaces.get_text()) / 1))
            except ValueError:
                _parser.set('General', 'decimal', '6')

            try:
                _parser.set(
                    'General', 'moduletabpos',
                    self.cmbModuleBookTabPosition.get_active_text().lower())
            except AttributeError:
                _parser.set('General', 'moduletabpos', 'top')

            try:
                _parser.set(
                    'General', 'listtabpos',
                    self.cmbListBookTabPosition.get_active_text().lower())
            except AttributeError:
                _parser.set('General', 'listtabpos', 'right')

            try:
                _parser.set(
                    'General', 'worktabpos',
                    self.cmbWorkBookTabPosition.get_active_text().lower())
            except AttributeError:
                _parser.set('General', 'worktabpos', 'bottom')

            _parser.set('Colors', 'revisionbg', Configuration.RTK_COLORS[0])
            _parser.set('Colors', 'revisionfg', Configuration.RTK_COLORS[1])
            _parser.set('Colors', 'functionbg', Configuration.RTK_COLORS[2])
            _parser.set('Colors', 'functionfg', Configuration.RTK_COLORS[3])
            _parser.set('Colors', 'requirementbg', Configuration.RTK_COLORS[4])
            _parser.set('Colors', 'requirementfg', Configuration.RTK_COLORS[5])
            _parser.set('Colors', 'assemblybg', Configuration.RTK_COLORS[6])
            _parser.set('Colors', 'assemblyfg', Configuration.RTK_COLORS[7])
            _parser.set('Colors', 'validationbg', Configuration.RTK_COLORS[8])
            _parser.set('Colors', 'validationfg', Configuration.RTK_COLORS[9])
            _parser.set('Colors', 'rgbg', Configuration.RTK_COLORS[10])
            _parser.set('Colors', 'rgfg', Configuration.RTK_COLORS[11])
            _parser.set('Colors', 'fracabg', Configuration.RTK_COLORS[12])
            _parser.set('Colors', 'fracafg', Configuration.RTK_COLORS[13])

            try:
                _parser.write(open(_conf_file, 'w'))
            except EnvironmentError:
                _return = True

        return _return

    def _save_list(self):
        """
        Method for saving the currently active list in the List Editor
        gtk.TreeView().
        """

        Widgets.set_cursor(self._mdcRTK, gtk.gdk.WATCH)

        _model = self.tvwListEditor.get_model()
        _model.foreach(self._save_line_item, self)

        Widgets.set_cursor(self._mdcRTK, gtk.gdk.LEFT_PTR)

        return False

    def _save_line_item(self, model, __path, row):
        """
        Method to save an individual gtk.TreeIter() in the List Editor
        gtk.TreeView().

        :param gtk.TreeModel model: the List Editor gtk.TreeModel().
        :param str __path: the path of the active gtk.TreeIter() in the List
                           Editor gtk.TreeModel().
        :param gtk.TreeIter row: the selected gtk.TreeIter() in the List
                                 Editor gtk.TreeModel().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if self.rdoUsers.get_active():
            _query = "INSERT INTO tbl_users \
                      (fld_user_lname, fld_user_fname, \
                       fld_user_email, fld_user_phone, fld_user_group) \
                      VALUES('{0:s}', '{1:s}', '{2:s}', '{3:s}', \
                             '{4:s}')".format(
                model.get_value(row, 1), model.get_value(row, 2),
                model.get_value(row, 3), model.get_value(row, 4),
                model.get_value(row, 5))
        elif self.rdoStatus.get_active():
            _query = "INSERT OR REPLACE INTO tbl_status \
                      (fld_status_id, fld_status_name, \
                       fld_status_description) \
                      VALUES({0:d}, '{1:s}', \
                             '{2:s}')".format(
                model.get_value(row, 0), model.get_value(row, 1),
                model.get_value(row, 2))
        elif self.rdoManufacturers.get_active():
            _query = "INSERT OR REPLACE INTO tbl_manufacturers \
                      (fld_manufacturers_noun, fld_location, \
                       fld_cage_code, fld_manufacturers_id) \
                      VALUES('{0:s}', '{1:s}', \
                             '{2:s}', {3:d})".format(
                model.get_value(row, 1), model.get_value(row, 2),
                model.get_value(row, 3), model.get_value(row, 0))
        elif self.rdoRequirementTypes.get_active():
            _query = "INSERT OR REPLACE INTO tbl_requirement_type \
                      (fld_requirement_type_id, \
                       fld_requirement_type_desc, \
                       fld_requirement_type_code) \
                      VALUES({0:d}, '{1:s}', \
                             '{2:s}')".format(
                model.get_value(row, 0), model.get_value(row, 1),
                model.get_value(row, 2))
        elif self.rdoWorkgroups.get_active():
            _query = "INSERT OR REPLACE INTO tbl_groups \
                      (fld_group_id, fld_group_name) \
                      VALUES({0:d}, '{1:s}')".format(
                model.get_value(row, 0), model.get_value(row, 1))
        elif self.rdoSeverity.get_active():
            _query = "INSERT OR REPLACE INTO tbl_severity \
                      (fld_severity_id, fld_name, fld_category, \
                       fld_description) \
                      VALUES({0:d}, '{1:s}', \
                             '{2:s}', '{3:s}')".format(
                model.get_value(row, 0), model.get_value(row, 1),
                model.get_value(row, 2), model.get_value(row, 3))
        elif self.rdoFailureProb.get_active():
            _query = "INSERT OR REPLACE INTO tbl_failure_probability \
                      (fld_probability_id, fld_probability_name, \
                       fld_probability_value) \
                      VALUES({0:d}, '{1:s}', \
                             '{2:s}')".format(
                model.get_value(row, 0), model.get_value(row, 1),
                model.get_value(row, 2))
        elif self.rdoFMEAActionCat.get_active():
            _query = "INSERT OR REPLACE INTO tbl_action_category \
                      (fld_action_id, fld_action_name) \
                      VALUES({0:d}, '{1:s}')".format(
                model.get_value(row, 0), model.get_value(row, 1))
        elif self.rdoFMEAControls.get_active():
            print "Save FMEA controls"
        elif self.rdoHazard.get_active():
            _query = "INSERT OR REPLACE INTO tbl_hazards \
                      (fld_hazard_id, fld_category, fld_subcategory) \
                      VALUES({0:d}, '{1:s}', \
                             '{2:s}')".format(
                model.get_value(row, 0), model.get_value(row, 1),
                model.get_value(row, 2))
        elif self.rdoDamageModel.get_active():
            print "Save damage models"
        elif self.rdoPoFPriority.get_active():
            print "Save PoF priority"
        elif self.rdoMeasParam.get_active():
            _query = "INSERT OR REPLACE INTO tbl_measurements \
                      (fld_measurement_id, fld_measurement_name) \
                      VALUES({0:d}, '{1:s}')".format(
                model.get_value(row, 0), model.get_value(row, 1))
        elif self.rdoClassMeans.get_active():
            print "Save classification means"
        elif self.rdoSWAppType.get_active():
            _query = "INSERT OR REPLACE INTO tbl_software_application \
                      (fld_application_id, fld_application_desc, \
                       fld_fault_density, fld_transformation_ratio) \
                      VALUES({0:d}, '{1:s}', \
                             '{2:s}', '{3:s}')".format(
                model.get_value(row, 0), model.get_value(row, 1),
                model.get_value(row, 2), model.get_value(row, 3))
        elif self.rdoSWDevPhase.get_active():
            _query = "INSERT OR REPLACE INTO tbl_development_phase \
                      (fld_phase_id, fld_phase_desc) \
                      VALUES({0:d}, '{1:s}')".format(
                model.get_value(row, 0), model.get_value(row, 1))
        elif self.rdoVandVTasks.get_active():
            _query = "INSERT OR REPLACE INTO tbl_validation_type \
                      (fld_validation_type_id, fld_validation_type_desc, \
                       fld_validation_type_code) \
                      VALUES({0:d}, '{1:s}', \
                             '{2:s}')".format(
                model.get_value(row, 0), model.get_value(row, 1),
                model.get_value(row, 2))
        elif self.rdoMeasurement.get_active():
            _query = "INSERT OR REPLACE INTO tbl_measurement_units \
                      (fld_measurement_id, fld_measurement_code) \
                      VALUES({0:d}, '{1:s}')".format(
                model.get_value(row, 0), model.get_value(row, 1))
        elif self.rdoIncidentType.get_active():
            _query = "INSERT OR REPLACE INTO tbl_incident_type \
                      (fld_incident_type_id, fld_incident_type_name) \
                      VALUES({0:d}, '{1:s}')".format(
                model.get_value(row, 0), model.get_value(row, 1))
        elif self.rdoIncidentCategory.get_active():
            _query = "INSERT OR REPLACE INTO tbl_incident_category \
                      (fld_incident_cat_id, fld_incident_cat_name) \
                      VALUES({0:d}, '{1:s}')".format(
                model.get_value(row, 0), model.get_value(row, 1))
        elif self.rdoIncidentCriticality.get_active():
            print "Save incident criticality"
        elif self.rdoLifeCycle.get_active():
            _query = "INSERT OR REPLACE INTO tbl_lifecycles \
                      (fld_lifecycle_id, fld_lifecycle_name) \
                      VALUES({0:d}, '{1:s}')".format(
                model.get_value(row, 0), model.get_value(row, 1))
        elif self.rdoDetectionMethod.get_active():
            print "Save detection methods"

        # Update the RTK Common Database table.
        (_results, _error_code, __) = self._mdcRTK.site_dao.execute(
            _query, commit=True)

        return False

    def _save_tree_layout(self):
        """
        Method for saving the gtk.TreeView() layout file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_name, _fmt_idx) = self._get_format_info()

        # Get the format file for the gtk.TreeView to be edited.
        _format_file = Configuration.RTK_FORMAT_FILE[_fmt_idx]
        _basename = basename(_format_file)

        # Open the format file for writing.
        _file = open(_format_file, 'w')

        # Create the new format file.
        _file.write("<!--\n")
        _file.write("-*- coding: utf-8 -*-\n\n")
        _file.write("%s is part of the RTK Project\n\n" % _basename)
        _file.write('Copyright 2011-2014 Andrew "Weibullguy" Rowland '
                    '<andrew DOT rowland AT reliaqual DOT com>\n\n')
        _file.write("All rights reserved.-->\n\n")
        _file.write("<!-- This file contains information used by the RTK "
                    "application to draw\n")
        _file.write("various widgets.  These values can be changed by the "
                    "user to personalize\n")
        _file.write("their experience. -->\n\n")

        _file.write("<root>\n")
        _file.write('\t<tree name="%s">\n' % _name)

        _model = self.tvwEditTree.get_model()
        _row = _model.get_iter_first()
        while _row is not None:
            _file.write("\t\t<column>\n")
            _file.write("\t\t\t<defaulttitle>%s</defaulttitle>\n" %
                        _model.get_value(_row, 0))
            _file.write("\t\t\t<usertitle>%s</usertitle>\n" % _model.get_value(
                _row, 1))
            _file.write(
                "\t\t\t<datatype>%s</datatype>\n" % _model.get_value(_row, 5))
            _file.write(
                '\t\t\t<position>%d</position>\n' % _model.get_value(_row, 2))
            _file.write(
                "\t\t\t<widget>%s</widget>\n" % _model.get_value(_row, 6))
            _file.write(
                "\t\t\t<editable>%d</editable>\n" % _model.get_value(_row, 3))
            _file.write(
                "\t\t\t<visible>%d</visible>\n" % _model.get_value(_row, 4))
            _file.write("\t\t</column>\n")

            _row = _model.iter_next(_row)

        _file.write("\t</tree>\n")
        _file.write("</root>")
        _file.close()

        return False

    def _quit(self, __button):
        """
        Method to quit the options gtk.Assistant().

        :param gtk.Button __button: the gtk.Button() that called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.destroy()

        return False
