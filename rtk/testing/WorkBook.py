#!/usr/bin/env python
"""
##############################
Testing Package Work Book View
##############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.testing.WorkBook.py is part of The RTK Project
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

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
    import widgets as _widg
except ImportError:
    import rtk.configuration as _conf
    import rtk.widgets as _widg
# from Assistants import AddTesting
import gui.gtk.Growth

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext

# TODO: Fix all docstrings; copy-paste errors.
class WorkView(gtk.VBox):                   # pylint: disable=R0902, R0904
    """
    The Work Book view displays all the attributes for the selected
    Testing item.  The attributes of a Work Book view are:

    :ivar _workview: the RTK top level Work View window to embed the
                     Testing Work Book into.
    :ivar _testing_model: the Testing data model whose attributes are being
                           displayed.

    :ivar _dic_definitions: dictionary containing pointers to the failure
                            definitions for the Revision being displayed.  Key
                            is the Failure Definition ID; value is the pointer
                            to the Failure Definition data model.

    :ivar _lst_handler_id: list containing the ID's of the callback signals for
                           each gtk.Widget() associated with an editable
                           Testing attribute.

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

    :ivar dtcTesting: the :class:`rtk.testing.Testing.Testing` data
                       controller to use with this Work Book.

    :ivar chkSafetyCritical: the :class:`gtk.CheckButton` to display/edit the
                             Testing's safety criticality.

    :ivar txtName: the :class:`gtk.Entry` to display/edit the Testing name.
    :ivar txtTotalCost: the :class:`gtk.Entry` to display the Testing cost.
    :ivar txtPartCount: the :class:`gtk.Entry` to display the number of
                        Components comprising the Assembly.
    :ivar txtRemarks: the :class:`gtk.Entry` to display/edit the Testing
                      remarks.
    :ivar txtPredictedHt: the :class:`gtk.Entry` to display the Testing
                          logistics hazard rate.
    :ivar txtMissionHt: the :class:`gtk.Entry` to display the Testing mission
                        hazard rate.
    :ivar txtMTBF: the :class:`gtk.Entry` to display the Testing logistics
                   MTBF.
    :ivar txtMissionMTBF: the :class:`gtk.Entry` to display the Testing
                          mission MTBF.
    :ivar txtMPMT: the :class:`gtk.Entry` to display the Testing mean
                   preventive maintenance time.
    :ivar txtMCMT: the :class:`gtk.Entry` to display the Testing mean
                   corrective maintenance time.
    :ivar txtMTTR: the :class:`gtk.Entry` to display the Testing mean time to
                   repair.
    :ivar txtMMT: the :class:`gtk.Entry` to display the Testing mean
                  maintenance time.
    :ivar txtAvailability: the :class:`gtk.Entry` to display the Testing
                           logistics availability.
    :ivar txtMissionAt: the :class:`gtk.Entry` to display the Testing mission
                        availability.
    """

    def __init__(self, workview, modulebook):
        """
        Initializes the Work Book view for the Testing package.

        :param workview: the :py:class:`rtk.gui.gtk.mwi.WorkView` container to
                         insert this Work Book into.
        :param modulebook: the :py:class:`rtk.testing.ModuleBook` to associate
                           with this Work Book.
        """

        gtk.VBox.__init__(self)

        # Initialize private dict attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._workview = workview
        self._modulebook = modulebook
        self._testing_model = None
        self._obj_planning = None
        self._obj_feasibility = None
        self._obj_assessment = None

        # Initialize public scalar attributes.
        self.dtcTesting = modulebook.dtcTesting
        self.dtcGrowth = modulebook.dtcGrowth

        # General Data page widgets.
        self.cmbTestType = _widg.make_combo(simple=True)
        self.spnConfidence = gtk.SpinButton()
        self.spnConsumerRisk = gtk.SpinButton()
        self.spnProducerRisk = gtk.SpinButton()
        self.txtName = _widg.make_entry(width=400)
        self.txtAttachment = _widg.make_text_view(width=400)
        self.txtDescription = _widg.make_text_view(width=400)
        self.txtCumTime = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        self.txtCumFails = _widg.make_entry(width=100, editable=False,
                                            bold=True)

        # Test Planning page widgets.
        self.btnCalculate = _widg.make_button(width=35, image='calculate')
        self.btnSave = _widg.make_button(width=35, image='save')

        self.hbxPlanning = gtk.HBox()

        # Test Feasibility page widgets.
        self.btnFeasibility = _widg.make_button(width=35, image='calculate')
        self.btnFeasibilitySave = _widg.make_button(width=35, image='save')

        self.hbxFeasibility = gtk.HBox()

        # Test Results page widgets.
        self.btnAddRecord = _widg.make_button(width=35, image='add')
        self.btnDeleteRecord = _widg.make_button(width=35, image='remove')
        self.btnAssess = _widg.make_button(width=35, image='calculate')
        self.btnAssessSave = _widg.make_button(width=35, image='save')

        self.hbxAssessment = gtk.HBox()

        # Put it all together.
        _toolbar = self._create_toolbar()
        self.pack_start(_toolbar, expand=False)

        _notebook = self._create_notebook()
        self.pack_start(_notebook)

        self.show_all()

    def _create_toolbar(self):
        """
        Method to create the toolbar for the Testing class Work Book.

        :return: _toolbar
        :rtype: gtk.Toolbar
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        # Add test button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Adds a new test."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 0)
        _toolbar.insert(_button, 0)
        _position += 1

        # Delete test button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Removes the currently selected test from "
                                   u"from the RTK Program Database."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 1)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save all tests button
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 2)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)

        _toolbar.show()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Testing class gtk.Notebook().

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
        self._create_planning_inputs_page(_notebook)
        self._create_feasibility_page(_notebook)
        self._create_test_result_page(_notebook)

        return _notebook

    def _create_general_data_page(self, notebook):
        """
        Method to create the Testing class gtk.Notebook() page for
        displaying general data about the selected Testing.

        :param gtk.Notebook notebook: the Testing class gtk.Notebook() widget.
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
        # Load the gtk.ComboBox()
        _test_types = [_(u"HALT/HASS"), _(u"ALT"), _(u"ESS"),
                       _(u"Reliability Growth"),
                       _(u"Reliability Demonstration"), _(u"PRAT")]
        _model = self.cmbTestType.get_model()
        _model.clear()
        self.cmbTestType.append_text("")
        for i in range(len(_test_types)):
            self.cmbTestType.append_text(_test_types[i])

        # Create the labels.
        _labels = [_(u"Test Name:"), _(u"Test Description:"),
                   _(u"Test Type:"), _(u"Confidence:"), _(u"Consumer's Risk:"),
                   _(u"Producer's Risk:"), _(u"Cumulative Time:"),
                   _(u"Cumulative Failures:"), _(u"Attachments:")]

        (_x_pos, _y_pos) = _widg.make_labels(_labels[:2], _fixed, 5, 5)
        (_x_pos1, _y_pos1) = _widg.make_labels(_labels[2:], _fixed, 5,
                                               _y_pos[1] + 105)
        _x_pos = max(_x_pos, _x_pos1) + 25

        # Place the widgets.
        self.txtName.set_tooltip_text(_(u"Enter the name of the selected "
                                        u"test."))
        self.txtDescription.set_tooltip_text(_(u"Enter a description of "
                                               u"the selected test."))
        self.cmbTestType.set_tooltip_text(_(u"Select the type of the "
                                            u"of the selected test."))
        self.spnConfidence.set_tooltip_text(_(u"Sets the statistical "
                                              u"confidence for results "
                                              u"obtained from the selected "
                                              u"test."))
        self.spnConsumerRisk.set_tooltip_text(_(u"The consumer (Type I) "
                                                u"risk.  This is the risk of "
                                                u"accepting a system when the "
                                                u"true reliability is below "
                                                u"the technical requirement."))
        self.spnProducerRisk.set_tooltip_text(_(u"The producer (Type II) "
                                                u"risk.  This is the risk of "
                                                u"rejecting a system when the "
                                                u"true reliability is at "
                                                u"least the goal "
                                                u"reliability."))
        self.txtAttachment.set_tooltip_text(_(u"Enter the URL to any "
                                              u"attachment associated with "
                                              u"the selected test."))
        self.txtCumTime.set_tooltip_text(_(u"Displays the cumulative test "
                                           u"time for the selected test."))
        self.txtCumFails.set_tooltip_text(_(u"Displays the cumulative number "
                                            u"of failures for the selected "
                                            u"test."))

        _fixed.put(self.txtName, _x_pos, _y_pos[0])
        _fixed.put(self.txtDescription, _x_pos, _y_pos[1])
        _fixed.put(self.cmbTestType, _x_pos, _y_pos1[0])
        _fixed.put(self.spnConfidence, _x_pos, _y_pos1[1])
        _fixed.put(self.spnConsumerRisk, _x_pos, _y_pos1[2])
        _fixed.put(self.spnProducerRisk, _x_pos, _y_pos1[3])
        _fixed.put(self.txtCumTime, _x_pos, _y_pos1[4])
        _fixed.put(self.txtCumFails, _x_pos, _y_pos1[5])
        _fixed.put(self.txtAttachment, _x_pos, _y_pos1[6])

        _textview = self.txtDescription.get_child().get_child()
        self._lst_handler_id.append(
            _textview.connect('focus-out-event', self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.cmbTestType.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.spnConfidence.connect('value-changed',
                                       self._on_value_changed, 2))
        self._lst_handler_id.append(
            self.spnConsumerRisk.connect('value-changed',
                                         self._on_value_changed, 3))
        self._lst_handler_id.append(
            self.spnProducerRisk.connect('value-changed',
                                         self._on_value_changed, 4))

        # Configure the gtk.SpinButtons.
        self.spnConfidence.set_digits(int(_conf.PLACES))
        self.spnConfidence.set_increments(0.1, 1.0)
        self.spnConfidence.set_range(0.0, 100.0)

        self.spnConsumerRisk.set_digits(int(_conf.PLACES))
        self.spnConsumerRisk.set_increments(0.1, 1.0)
        self.spnConsumerRisk.set_range(0.0, 100.0)

        self.spnProducerRisk.set_digits(int(_conf.PLACES))
        self.spnProducerRisk.set_increments(0.1, 1.0)
        self.spnProducerRisk.set_range(0.0, 100.0)

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
                                  u"the selected test."))
        notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _create_planning_inputs_page(self, notebook):   # pylint: disable=R0914, R0915
        """
        Creates the Testing class gtk.Notebook() page for displaying the test
        planning inputs for the selected Test.

        :param gtk.Notebook notebook: the Testing class gtk.Notebook() widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        self.hbxPlanning.pack_start(_bbox, False, True)

        _bbox.pack_start(self.btnCalculate, False, False)
        _bbox.pack_start(self.btnSave, False, False)

        self.btnCalculate.set_tooltip_text(_(u"Calculate missing test "
                                             u"planning inputs."))
        self.btnSave.set_tooltip_text(_(u"Saves changes to the test planning "
                                        u"inputs."))

        self.btnSave.connect('clicked', self._on_button_clicked, 51)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Test\nPlanning\nInputs") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Allows entering test planning inputs for "
                                  u"the selected test."))

        notebook.insert_page(self.hbxPlanning, tab_label=_label, position=-1)

        return False

    def _create_feasibility_page(self, notebook):   # pylint: disable=R0914, R0915
        """
        Creates the Testing class gtk.Notebook() page for displaying the test
        feasibility assessment for the selected Test.

        :param gtk.Notebook notebook: the Testing class gtk.Notebook() widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        self.hbxFeasibility.pack_start(_bbox, False, True)

        _bbox.pack_start(self.btnFeasibility, False, False)
        _bbox.pack_end(self.btnFeasibilitySave, False, False)

        self.btnFeasibility.set_tooltip_text(_(u"Assess the feasibility of "
                                               u"the selected test plan."))
        self.btnFeasibilitySave.set_tooltip_text(_(u"Saves changes to the "
                                                   u"test planning inputs."))

        self.btnFeasibilitySave.connect('clicked', self._on_button_clicked, 51)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Test\nFeasibility") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the feasibility criteria for the "
                                  u"selected test."))

        notebook.insert_page(self.hbxFeasibility, tab_label=_label,
                             position=-1)

        return False

    def _create_test_result_page(self, notebook):   # pylint: disable=R0914, R0915
        """
        Creates the Testing class gtk.Notebook() page for displaying the test
        results for the selected Test.

        :param gtk.Notebook notebook: the Testing class gtk.Notebook() widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        self.hbxAssessment.pack_start(_bbox, False, True)

        _bbox.pack_start(self.btnAddRecord, False, False)
        _bbox.pack_start(self.btnDeleteRecord, False, False)
        _bbox.pack_start(self.btnAssess, False, False)
        _bbox.pack_start(self.btnAssessSave, False, False)

        self.btnAssess.set_tooltip_text(_(u"Assesses the current reliability "
                                          u"of the system under test."))

        self.btnAssessSave.connect('clicked', self._on_button_clicked, 51)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Test\nResults") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the test results for the "
                                  u"selected test."))

        notebook.insert_page(self.hbxAssessment, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Testing class gtk.Notebook().

        :param model: the :py:class:`rtk.testing.Testing.Model` to load.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        self._testing_model = model

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the General Data information.                            #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        self.cmbTestType.set_active(model.test_type)
        self.spnConfidence.set_value(float(model.confidence))
        self.spnConsumerRisk.set_value(float(model.consumer_risk))
        self.spnProducerRisk.set_value(float(model.producer_risk))
        self.txtName.set_text(str(model.name))
        _textview = self.txtAttachment.get_children()[0].get_children()[0].get_buffer()
        _textview.set_text(model.attachment)
        _textview = self.txtDescription.get_children()[0].get_children()[0].get_buffer()
        _textview.set_text(model.description)
        self.txtCumTime.set_text(str(fmt.format(model.cum_time)))
        self.txtCumFails.set_text(str(fmt.format(model.cum_failures)))

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the Planning Data information.                           #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        try:
            self.hbxPlanning.remove(
                self.hbxPlanning.get_children()[1])
        except IndexError:
            pass
        self._obj_planning = gui.gtk.Growth.Planning(self.dtcGrowth)
        self.hbxPlanning.pack_end(self._obj_planning, True, True)

        self._obj_planning.create_page()
        self._obj_planning.load_page(self._testing_model)

        self.btnCalculate.connect('button-release-event',
                                  self._obj_planning.on_button_clicked, 50)

        self.hbxPlanning.show_all()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the Feasibility Data information.                        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        try:
            self.hbxFeasibility.remove(
                self.hbxFeasibility.get_children()[1])
        except IndexError:
            pass
        self._obj_feasibility = gui.gtk.Growth.Feasibility(self.dtcGrowth)
        self.hbxFeasibility.pack_end(self._obj_feasibility, True, True)

        self._obj_feasibility.create_page()
        self._obj_feasibility.load_page(self._testing_model)

        self.btnFeasibility.connect('button-release-event',
                                    self._obj_feasibility.on_button_clicked,
                                    50)

        self.hbxFeasibility.show_all()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the Assessment Data information.                         #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        try:
            self.hbxAssessment.remove(
                self.hbxAssessment.get_children()[1])
        except IndexError:
            pass
        self._obj_assessment = gui.gtk.Growth.Assessment(self.dtcGrowth)
        self.hbxAssessment.pack_end(self._obj_assessment, True, True)

        self._obj_assessment.create_page()
        self._obj_assessment.load_page(self._testing_model)

        self.btnAddRecord.connect('button-release-event',
                                  self._obj_assessment.on_button_clicked, 0)
        self.btnDeleteRecord.connect('button-release-event',
                                     self._obj_assessment.on_button_clicked, 1)
        self.btnAssess.connect('button-release-event',
                               self._obj_assessment.on_button_clicked, 2)
        self.btnAssessSave.connect('button-release-event',
                                   self._obj_assessment.on_button_clicked, 3)

        self.hbxAssessment.show_all()

        self.get_children()[1].set_current_page(0)

        return False

    def _request_add_testing(self, test_type, model, parent, testing_id):
        """
        Method to call the Testing data controller function 'add_test' and
        then update the Testing Work Book gtk.TreeView() with the newly added
        test.

        :param int test_type: the type of Testing item to add.
                              * 1 = HALT/HASS
                              * 2 = ALT
                              * 3 = ESS
                              * 4 = Reliability Growth
                              * 5 = Reliability Demonstration
                              * 6 = PRAT
        :param gtk.TreeModel model: the gtk.TreeModel() displaying the Testing
                                    hierarchy.
        :param gtk.TreeIter parent: the gtk.TreeIter() that will be the parent
                                    of the newly added testing item.
        :param int testing_id: the testing ID of the parent Testing module.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Add the new testing item to the database and dtcTesting dictionary.
        (_testing, _error_code) = self.dtcTesting.add_testing(
            self._testing_model.revision_id, test_type, testing_id)

        if test_type == 1:
            _icon = _conf.ICON_DIR + '32x32/csci.png'
        elif test_type == 2:
            _icon = _conf.ICON_DIR + '32x32/unit.png'

        # Update the module book view to show the new assembly.
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _data = list(_testing.get_attributes()) + [_icon]

        model.append(parent, _data)
        self._modulebook.treeview.expand_all()

        return False

    def _request_delete_testing(self):
        """
        Method to call the BoM data controller function 'delete_testing' and
        then update the Testing Work Book gtk.TreeView() with the newly added
        testing item.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Find the selected testing item.
        _selection = self._modulebook.treeview.get_selection()
        (_model, _row) = _selection.get_selected()

        # Delete the selected testing item from the database and the
        # Testing data controller dictionary.
        self.dtcTesting.delete_testing(self._testing_model.testing_id)

        # Refresh the Testing gtkTreeView().
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

        if index == 0:
            if self._testing_model.test_type == 4:
                self.dtcGrowth.add_test(self._testing_model.test_id)

        elif index == 1:
            if self._testing_model.test_type == 4:
                self.dtcGrowth.delete_test(self._testing_model.test_id)

        elif index == 2:
            if self._testing_model.test_type == 4:
                self.dtcGrowth.save_all_tests()

        elif index == 50:
            if self._testing_model.test_type == 4:
                self.dtcGrowth.request_calculate(self._testing_model.test_id)

            #self._load_assessment_results_page()

        elif index == 51:
            if self._testing_model.test_type == 4:
                self.dtcGrowth.save_test(self._testing_model.test_id)

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

        if index == 1:                      # Testing level
            self._testing_model.level_id = combo.get_active()
            #self._modulebook.update(2, self._testing_model.level_id)
        elif index == 2:                    # Testing application
            self._testing_model.application_id = combo.get_active()
            #self._modulebook.update(4, self._testing_model.application_id)
        elif index == 3:                    # Development phase
            self._testing_model.phase_id = combo.get_active()
            #self._modulebook.update(5, self._testing_model.phase_id)
            self._load_risk_analysis_page()
        elif index == 4:                    # Test confidence level
            self._testing_model.tcl = combo.get_active()
            #self._modulebook.update(37, self._testing_model.tcl)
        elif index == 5:
            self._testing_model.test_path = combo.get_active()
            #self._modulebook.update(38, self._testing_model.test_path)
        elif index == 6:
            self._testing_model.test_effort = combo.get_active()
            #self._modulebook.update(40, self._testing_model.test_effort)
        elif index == 7:
            self._testing_model.test_approach = combo.get_active()
            #self._modulebook.update(41, self._testing_model.test_approach)

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index): # pylint: disable=R0912
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
            self._testing_model.description = _textbuffer.get_text(*_textbuffer.get_bounds())
            self._modulebook.update(3, self._testing_model.description)

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_value_changed(self, button, index):     # pylint: disable=R0912
        """
        Responds to gtk.SpinButton() value_changed signals and calls the
        correct function or method, passing any parameters as needed.

        :param gtk.SpinButton button: the gtk.SpinButton() that called this
                                      method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.SpinButton() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        button.handler_block(self._lst_handler_id[index])

        if index == 2:
            self._testing_model.confidence = button.get_value()
        elif index == 3:
            self._testing_model.consumer_risk = button.get_value()
        elif index == 4:
            self._testing_model.producer_risk = button.get_value()

        button.handler_unblock(self._lst_handler_id[index])

        return False
