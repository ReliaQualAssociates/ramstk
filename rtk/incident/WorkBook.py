#!/usr/bin/env python
"""
###############################
Incident Package Work Book View
###############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.incident.WorkBook.py is part of The RTK Project
#
# All rights reserved.

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
from Assistants import AddIncident, FilterIncident, ImportIncident, \
                       CreateDataSet

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
    Incident item.  The attributes of a Work Book view are:

    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable Incident attribute.

    :ivar _workview: the RTK top level :py:class:`rtk.gui.gtk.WorkBook` window
                     to embed the Incident Work Book into.
    :ivar _model: the Incident :py:class:`rtk.incident.Incident.Model`
                  whose attributes are being displayed.
    :ivar dtcIncident: the :py:class:`rtk.incident.Incident.Incident`
                         to use with this Work Book.

    :ivar gtk.Button btnEndDate:
    :ivar gtk.Button btnStartDate:
    :ivar gtk.Combo cmbTaskType:
    :ivar gtk.Combo cmbMeasurementUnit:
    :ivar gtk.SpinButton spnStatus:
    :ivar gtk.Entry txtID:
    :ivar gtk.Entry txtMaxAcceptable:
    :ivar gtk.Entry txtMeanAcceptable:
    :ivar gtk.Entry txtMinAcceptable:
    :ivar gtk.Entry txtVarAcceptable:
    :ivar gtk.Entry txtSpecification:
    :ivar gtk.Entry txtTask:
    :ivar gtk.Entry txtEndDate:
    :ivar gtk.Entry txtStartDate:
    :ivar gtk.Entry txtMinTime:
    :ivar gtk.Entry txtExpTime:
    :ivar gtk.Entry txtMaxTime:
    :ivar gtk.Entry txtMinCost:
    :ivar gtk.Entry txtExpCost:
    :ivar gtk.Entry txtMaxCost:
    :ivar gtk.Entry txtMeanTimeLL:
    :ivar gtk.Entry txtMeanTime:
    :ivar gtk.Entry txtMeanTimeUL:
    :ivar gtk.Entry txtMeanCostLL:
    :ivar gtk.Entry txtMeanCost:
    :ivar gtk.Entry txtMeanCostUL:
    :ivar gtk.Entry txtProjectTimeLL:
    :ivar gtk.Entry txtProjectTime:
    :ivar gtk.Entry txtProjectTimeUL:
    :ivar gtk.Entry txtProjectCostLL:
    :ivar gtk.Entry txtProjectCost:
    :ivar gtk.Entry txtProjectCostUL:
    :ivar mpl.FigureCanvas pltPlot1:
    :ivar mpl.Axes axAxis1:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtTask `focus_out_event`                 |
    +----------+-------------------------------------------+
    |     1    | cmbTaskType `changed`                     |
    +----------+-------------------------------------------+
    |     2    | txtSpecification `focus_out_event`        |
    +----------+-------------------------------------------+
    |     3    | cmbMeasurementUnit `changed`              |
    +----------+-------------------------------------------+
    |     4    | txtMinAcceptable `focus_out_event`        |
    +----------+-------------------------------------------+
    |     5    | txtMeanAcceptable `focus_out_event`       |
    +----------+-------------------------------------------+
    |     6    | txtMaxAcceptable `focus_out_event`        |
    +----------+-------------------------------------------+
    |     7    | txtVarAcceptable `focus_out_event`        |
    +----------+-------------------------------------------+
    |     8    | txtStartDate `changed` `focus_out_event`  |
    +----------+-------------------------------------------+
    |     9    | txtEndDate `changed` `focus_out_event`    |
    +----------+-------------------------------------------+
    |    10    | spnStatus `value_changed`                 |
    +----------+-------------------------------------------+
    |    11    | txtMinTime `focus_out_event`              |
    +----------+-------------------------------------------+
    |    12    | txtExpTime `focus_out_event`              |
    +----------+-------------------------------------------+
    |    13    | txtMaxTime `focus_out_event`              |
    +----------+-------------------------------------------+
    |    14    | txtMinCost `focus_out_event`              |
    +----------+-------------------------------------------+
    |    15    | txtExpCost `focus_out_event`              |
    +----------+-------------------------------------------+
    |    16    | txtMaxCost `focus_out_event`              |
    +----------+-------------------------------------------+
    """

    def __init__(self, modulebook):
        """
        Method to initialize the Work Book view for the Incident package.

        :param workview: the :py:class:`rtk.gui.gtk.mwi.WorkView` container to
                         insert this Work Book into.
        :param modulebook: the :py:class:`rtk.incident.ModuleBook` to
                           associate with this Work Book.
        """

        gtk.VBox.__init__(self)

        # Define private dictionary attributes.
        self._dic_hardware = {}
        self._dic_software = {}

        # Define private list attributes.
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._modulebook = modulebook
        self._model = None
        self._component = None
        self._action = None

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.mdcRTK = modulebook.mdcRTK

        # Dataset class Work Book toolbar widgets.
        self.chkAllRevisions = Widgets.make_check_button(_(u"Include "
                                                           u"incidents from "
                                                           u"all revisions"))

        # Create the Program Incident page widgets.
        self.chkAccepted = Widgets.make_check_button(label=_(u"Accepted"))
        self.chkReviewed = Widgets.make_check_button(label=_(u"Reviewed"))

        self.cmbHardware = Widgets.make_combo(simple=False)
        self.cmbSoftware = Widgets.make_combo(simple=False)
        self.cmbCategory = Widgets.make_combo()
        self.cmbType = Widgets.make_combo()
        self.cmbStatus = Widgets.make_combo()
        self.cmbCriticality = Widgets.make_combo()
        self.cmbLifeCycle = Widgets.make_combo()
        self.cmbRequestBy = Widgets.make_combo()

        self.txtID = Widgets.make_entry(width=100, editable=False)
        self.txtRequestDate = Widgets.make_entry(width=100, editable=False)
        self.txtAge = Widgets.make_entry(width=100, editable=False)
        self.txtShortDescription = Widgets.make_entry(width=750)

        self.txtLongDescription = Widgets.make_text_view(width=550, height=200)
        self.txtRemarks = Widgets.make_text_view(width=550, height=200)

        # Create the Chargeability page widgets.
        self.cmbChargeable1 = Widgets.make_combo(width=75)
        self.cmbChargeable2 = Widgets.make_combo(width=75)
        self.cmbChargeable3 = Widgets.make_combo(width=75)
        self.cmbChargeable4 = Widgets.make_combo(width=75)
        self.cmbChargeable5 = Widgets.make_combo(width=75)
        self.cmbRelevant1 = Widgets.make_combo(width=75)
        self.cmbRelevant2 = Widgets.make_combo(width=75)
        self.cmbRelevant3 = Widgets.make_combo(width=75)
        self.cmbRelevant4 = Widgets.make_combo(width=75)
        self.cmbRelevant5 = Widgets.make_combo(width=75)
        self.cmbRelevant6 = Widgets.make_combo(width=75)
        self.cmbRelevant7 = Widgets.make_combo(width=75)
        self.cmbRelevant8 = Widgets.make_combo(width=75)
        self.cmbRelevant9 = Widgets.make_combo(width=75)
        self.cmbRelevant10 = Widgets.make_combo(width=75)
        self.cmbRelevant11 = Widgets.make_combo(width=75)
        self.cmbRelevant12 = Widgets.make_combo(width=75)
        self.cmbRelevant13 = Widgets.make_combo(width=75)
        self.cmbRelevant14 = Widgets.make_combo(width=75)
        self.cmbRelevant15 = Widgets.make_combo(width=75)
        self.cmbRelevant16 = Widgets.make_combo(width=75)
        self.cmbRelevant17 = Widgets.make_combo(width=75)
        self.cmbRelevant18 = Widgets.make_combo(width=75)

        self.lblChargeable1 = Widgets.make_label(_(u"1. This failure occurred "
                                                   u"on or was caused by "
                                                   u"equipment outside the "
                                                   u"scope of this test "
                                                   u"plan."),
                                                 width=-1, height=-1,
                                                 wrap=True)
        self.lblChargeable2 = Widgets.make_label(_(u"2. This failure occurred "
                                                   u"on or was caused by "
                                                   u"customer furnished "
                                                   u"equipment."), width=-1,
                                                 height=-1, wrap=True)
        self.lblChargeable3 = Widgets.make_label(_(u"3. This failure occurred "
                                                   u"on or was caused by "
                                                   u"supplier furnished "
                                                   u"equipment."), width=-1,
                                                 height=-1, wrap=True)
        self.lblChargeable4 = Widgets.make_label(_(u"4. This failure of "
                                                   u"supplier furnished "
                                                   u"equipment was the caused "
                                                   u"by system-integration "
                                                   u"errors."), width=-1,
                                                 height=-1, wrap=True)
        self.lblChargeable5 = Widgets.make_label(_(u"5. This supplier "
                                                   u"provided equipment did "
                                                   u"or would have passed "
                                                   u"normal receipt "
                                                   u"inspection and testing."),
                                                 width=-1, height=-1,
                                                 wrap=True)
        self.lblChargeable = Widgets.make_label("", width=-1, height=-1,
                                                wrap=True)

        self.lblRelevant1 = Widgets.make_label(_(u"1. This failure is an "
                                                 u"early life failure."),
                                               width=-1, height=-1, wrap=True)
        self.lblRelevant2 = Widgets.make_label(_(u"2. This failure was due to "
                                                 u"an operator error such "
                                                 u"that the error could be "
                                                 u"expected during normal "
                                                 u"operations."),
                                               width=-1, height=-1, wrap=True)
        self.lblRelevant3 = Widgets.make_label(_(u"3. This failure was due to "
                                                 u"test setup errors."),
                                               width=-1, height=-1, wrap=True)
        self.lblRelevant4 = Widgets.make_label(_(u"4. This is a consumable "
                                                 u"item that has exceeded its "
                                                 u"expected life."), width=-1,
                                               height=-1, wrap=True)
        self.lblRelevant5 = Widgets.make_label(_(u"5. Life data indicates an "
                                                 u"unacceptable percentage of "
                                                 u"these items will not reach "
                                                 u"the specified life."),
                                               width=-1, height=-1, wrap=True)
        self.lblRelevant6 = Widgets.make_label(_(u"6. The parts contributing "
                                                 u"to the failure are "
                                                 u"representative of design "
                                                 u"intent."), width=-1,
                                               height=-1, wrap=True)
        self.lblRelevant7 = Widgets.make_label(_(u"7. The failure would or "
                                                 u"could have occurred for "
                                                 u"the new design if the "
                                                 u"parts were "
                                                 u"representative."),
                                               width=-1, height=-1, wrap=True)
        self.lblRelevant8 = Widgets.make_label(_(u"8. The parts contributing "
                                                 u"to the failure are "
                                                 u"conforming to design "
                                                 u"specifications."),
                                               width=-1, height=-1, wrap=True)
        self.lblRelevant9 = Widgets.make_label(_(u"9. The failure would or "
                                                 u"could have occurred if the "
                                                 u"parts were conforming."),
                                               width=-1, height=-1, wrap=True)
        self.lblRelevant10 = Widgets.make_label(_(u"10. The parts were made "
                                                  u"using production tooling "
                                                  u"and a production "
                                                  u"process."),
                                                width=-1, height=-1, wrap=True)
        self.lblRelevant11 = Widgets.make_label(_(u"11. A production process "
                                                  u"could have generated the "
                                                  u"nonconformance."),
                                                width=-1, height=-1, wrap=True)
        self.lblRelevant12 = Widgets.make_label(_(u"12. The parts would or "
                                                  u"could have passed normal "
                                                  u"production inspection and "
                                                  u"testing."), width=-1,
                                                height=-1, wrap=True)
        self.lblRelevant13 = Widgets.make_label(_(u"13. Performance was "
                                                  u"originally acceptable and "
                                                  u"is no longer (i.e., "
                                                  u"degradation has "
                                                  u"occurred)."),
                                                width=-1, height=-1, wrap=True)
        self.lblRelevant14 = Widgets.make_label(_(u"14. We can measure the "
                                                  u"performance issue and "
                                                  u"compare to requirements."),
                                                width=-1, height=-1, wrap=True)
        self.lblRelevant15 = Widgets.make_label(_(u"15. Performance is within "
                                                  u"requirements."), width=-1,
                                                height=-1, wrap=True)
        self.lblRelevant16 = Widgets.make_label(_(u"16. There exist "
                                                  u"acceptance standards to "
                                                  u"which performance can be "
                                                  u"compared."), width=-1,
                                                height=-1, wrap=True)
        self.lblRelevant17 = Widgets.make_label(_(u"17. By existing standards "
                                                  u"we can accept the issue."),
                                                width=-1, height=-1, wrap=True)
        self.lblRelevant18 = Widgets.make_label(_(u"18. We can accept this "
                                                  u"issue."), width=-1,
                                                height=-1, wrap=True)
        self.lblRelevant = Widgets.make_label("", width=-1, height=-1,
                                              wrap=True)

        # Create the Incident Analysis page widgets.
        self.btnReviewDate = Widgets.make_button(height=25, width=25,
                                                 label="...",
                                                 image='calendar')
        self.btnApproveDate = Widgets.make_button(height=25, width=25,
                                                  label="...",
                                                  image='calendar')
        self.btnClosureDate = Widgets.make_button(height=25, width=25,
                                                  label="...",
                                                  image='calendar')

        self.cmbDetectionMethod = Widgets.make_combo()
        self.cmbReviewBy = Widgets.make_combo()
        self.cmbApproveBy = Widgets.make_combo()
        self.cmbCloseBy = Widgets.make_combo()

        self.txtTest = Widgets.make_entry()
        self.txtTestCase = Widgets.make_entry()
        self.txtExecutionTime = Widgets.make_entry(width=100)
        self.txtAnalysis = Widgets.make_text_view(width=550, height=200)
        self.txtReviewDate = Widgets.make_entry(width=100, editable=False)
        self.txtApproveDate = Widgets.make_entry(width=100, editable=False)
        self.txtCloseDate = Widgets.make_entry(width=100, editable=False)

        # Create the Incident Actions page widgets.
        self.btnSaveAction = Widgets.make_button(width=35, image='save')
        self.btnActionDueDate = Widgets.make_button(height=25, width=25,
                                                    label="...",
                                                    image='calendar')
        self.btnActionApproveDate = Widgets.make_button(height=25, width=25,
                                                        label="...",
                                                        image='calendar')
        self.btnActionCloseDate = Widgets.make_button(height=25, width=25,
                                                      label="...",
                                                      image='calendar')

        self.cmbActionOwner = Widgets.make_combo()
        self.cmbActionApproveBy = Widgets.make_combo()
        self.cmbActionCloseBy = Widgets.make_combo()
        self.cmbActionStatus = Widgets.make_combo()

        self.tvwActionList = gtk.TreeView()

        self.txtPrescribedAction = Widgets.make_text_view(width=550,
                                                          height=200)
        self.txtActionTaken = Widgets.make_text_view(width=550, height=200)
        self.txtActionDueDate = Widgets.make_entry(width=100, editable=False)
        self.txtActionApproveDate = Widgets.make_entry(width=100,
                                                       editable=False)
        self.txtActionCloseDate = Widgets.make_entry(width=100, editable=False)

        # Set gtk.Widget() tooltips.
        self.chkAccepted.set_tooltip_text(_(u"Displays whether the incident "
                                            u"has been accepted by the "
                                            u"responsible owner."))
        self.chkReviewed.set_tooltip_text(_(u"Displays whether the incident "
                                            u"has been reviewed by the "
                                            u"responsible owner."))
        self.cmbCategory.set_tooltip_text(_(u"Selects and displays the "
                                            u"category of the selected "
                                            u"incident."))
        self.cmbType.set_tooltip_text(_(u"Selects and displays the type of "
                                        u"incident for the selected "
                                        u"incident."))
        self.cmbStatus.set_tooltip_text(_(u"Displays the status of the "
                                          u"selected incident."))
        self.cmbCriticality.set_tooltip_text(_(u"Displays the criticality "
                                               u"of the selected incident."))
        self.cmbLifeCycle.set_tooltip_text(_(u"Displays the product life "
                                             u"cycle during which the "
                                             u"incident occurred."))
        self.cmbRequestBy.set_tooltip_text(_(u"Displays the name of the "
                                             u"individual reporting the "
                                             u"incident."))
        self.txtID.set_tooltip_text(_(u"Displays the unique code for the "
                                      u"selected incident."))
        self.txtRequestDate.set_tooltip_text(_(u"Displays the date the "
                                               u"incident was opened."))
        self.txtAge.set_tooltip_text(_(u"Displays the age of the incident in "
                                       u"days."))
        self.txtShortDescription.set_tooltip_text(_(u"Short problem "
                                                    u"description."))
        self.txtPrescribedAction.set_tooltip_text(_(u"Displays the prescribed "
                                                    u"action."))
        self.txtActionTaken.set_tooltip_text(_(u"Displays the actual action "
                                               u"that was taken.  This may "
                                               u"differ from the prescribed "
                                               u"action."))
        self.btnSaveAction.set_tooltip_text(_(u"Saves the selected action."))
        self.cmbActionOwner.set_tooltip_text(_(u"Selects and displays the "
                                               u"person responsible for "
                                               u"completing the action."))
        self.txtActionDueDate.set_tooltip_text(_(u"Displays the due date for "
                                                 u"the action."))
        self.btnActionDueDate.set_tooltip_text(_(u"Selects the due date for "
                                                 u"the action."))
        self.cmbActionStatus.set_tooltip_text(_(u"Selects and displays the "
                                                u"status of the action."))
        self.cmbActionApproveBy.set_tooltip_text(_(u"Selects and displays the "
                                                   u"the person approving the "
                                                   u"actual action taken."))
        self.txtActionApproveDate.set_tooltip_text(_(u"Displays the date the "
                                                     u"action was approved."))
        self.btnActionApproveDate.set_tooltip_text(_(u"Selects the date the "
                                                     u"action was approved."))
        self.cmbActionCloseBy.set_tooltip_text(_(u"Selects and displays the "
                                                 u"the person closing the "
                                                 u"action."))
        self.txtActionCloseDate.set_tooltip_text(_(u"Displays the date the "
                                                   u"action was closed."))
        self.btnActionCloseDate.set_tooltip_text(_(u"Selects the date the "
                                                   u"action was closed."))
        self.cmbDetectionMethod.set_tooltip_markup(_(u"Displays the "
                                                     u"method used to "
                                                     u"detect the "
                                                     u"reported problem."))
        self.txtTest.set_tooltip_markup(_(u"Displays the software test "
                                          u"being executed when the "
                                          u"reported problem was "
                                          u"discovered."))
        self.txtTestCase.set_tooltip_markup(_(u"Displays the software "
                                              u"test case being executed "
                                              u"when the reported problem "
                                              u"was discovered."))
        self.txtExecutionTime.set_tooltip_markup(_(u"Displays the time "
                                                   u"(CPU or calendar "
                                                   u"time) into the test "
                                                   u"when the reported "
                                                   u"problem was "
                                                   u"discovered."))
        self.btnClosureDate.set_tooltip_text(_(u"Select the date the incident "
                                               u"analysis was reviewed."))
        self.btnApproveDate.set_tooltip_text(_(u"Select the date the incident "
                                               u"analysis was approved."))
        self.btnClosureDate.set_tooltip_text(_(u"Select the date the incident "
                                               u"was closed."))
        self.cmbReviewBy.set_tooltip_text(_(u"Displays the name of the "
                                            u"individual who reviewed the "
                                            u"incident analysis."))
        self.cmbApproveBy.set_tooltip_text(_(u"Displays the name of the "
                                             u"individual who approved "
                                             u"the analysis."))
        self.cmbCloseBy.set_tooltip_text(_(u"Displays the name of the "
                                           u"individual who closed the "
                                           u"incident."))
        self.txtReviewDate.set_tooltip_text(_(u"Displays the date the "
                                              u"incident analysis was "
                                              u"reviewed."))
        self.txtApproveDate.set_tooltip_text(_(u"Displays the date the "
                                               u"analysis was approved."))
        self.txtCloseDate.set_tooltip_text(_(u"Displays the date the "
                                             u"incident was closed."))

        # Connect gtk.Widget() signals to callback methods.
        self._lst_handler_id.append(
            self.btnSaveAction.connect('clicked', self._on_button_clicked, 0))

        self.btnActionDueDate.connect('button-release-event',
                                      Widgets.date_select,
                                      self.txtActionDueDate)
        self.btnActionApproveDate.connect('button-release-event',
                                          Widgets.date_select,
                                          self.txtActionApproveDate)
        self.btnActionCloseDate.connect('button-release-event',
                                        Widgets.date_select,
                                        self.txtActionCloseDate)
        self.btnReviewDate.connect('button-release-event',
                                   Widgets.date_select, self.txtReviewDate)
        self.btnApproveDate.connect('button-release-event',
                                    Widgets.date_select, self.txtApproveDate)
        self.btnClosureDate.connect('button-release-event',
                                    Widgets.date_select, self.txtCloseDate)

        self._lst_handler_id.append(
            self.chkAccepted.connect('toggled', self._on_check_toggled, 1))
        self._lst_handler_id.append(
            self.chkReviewed.connect('toggled', self._on_check_toggled, 2))
        self._lst_handler_id.append(
            self.chkAllRevisions.connect('toggled', self._on_check_toggled, 3))

        self._lst_handler_id.append(
            self.cmbCategory.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self._on_combo_changed, 5))
        self._lst_handler_id.append(
            self.cmbCriticality.connect('changed', self._on_combo_changed, 6))
        self._lst_handler_id.append(
            self.cmbStatus.connect('changed', self._on_combo_changed, 7))
        self._lst_handler_id.append(
            self.cmbHardware.connect('changed', self._on_combo_changed, 8))
        self._lst_handler_id.append(
            self.cmbSoftware.connect('changed', self._on_combo_changed, 9))
        self._lst_handler_id.append(
            self.cmbRequestBy.connect('changed', self._on_combo_changed, 10))
        self._lst_handler_id.append(
            self.cmbLifeCycle.connect('changed', self._on_combo_changed, 11))
        self._lst_handler_id.append(
            self.cmbDetectionMethod.connect('changed',
                                            self._on_combo_changed, 12))
        self._lst_handler_id.append(
            self.cmbReviewBy.connect('changed', self._on_combo_changed, 13))
        self._lst_handler_id.append(
            self.cmbApproveBy.connect('changed', self._on_combo_changed, 14))
        self._lst_handler_id.append(
            self.cmbCloseBy.connect('changed', self._on_combo_changed, 15))
        self._lst_handler_id.append(
            self.cmbActionOwner.connect('changed', self._on_combo_changed, 16))
        self._lst_handler_id.append(
            self.cmbActionStatus.connect('changed',
                                         self._on_combo_changed, 17))
        self._lst_handler_id.append(
            self.cmbActionApproveBy.connect('changed',
                                            self._on_combo_changed, 18))
        self._lst_handler_id.append(
            self.cmbActionCloseBy.connect('changed',
                                          self._on_combo_changed, 19))

        self._lst_handler_id.append(
            self.txtRequestDate.connect('focus-out-event',
                                        self._on_focus_out, 20))
        self._lst_handler_id.append(
            self.txtShortDescription.connect('focus-out-event',
                                             self._on_focus_out, 21))
        _buffer = self.txtLongDescription.get_child().get_child().get_buffer()
        self._lst_handler_id.append(_buffer.connect('changed',
                                                    self._on_focus_out,
                                                    _buffer, 22))
        _buffer = self.txtRemarks.get_child().get_child().get_buffer()
        self._lst_handler_id.append(_buffer.connect('changed',
                                                    self._on_focus_out,
                                                    _buffer, 23))
        self._lst_handler_id.append(
            self.txtTest.connect('focus-out-event', self._on_focus_out, 24))
        self._lst_handler_id.append(
            self.txtTestCase.connect('focus-out-event',
                                     self._on_focus_out, 25))
        self._lst_handler_id.append(
            self.txtExecutionTime.connect('focus-out-event',
                                          self._on_focus_out, 26))
        _buffer = self.txtAnalysis.get_child().get_child().get_buffer()
        self._lst_handler_id.append(_buffer.connect('changed',
                                                    self._on_focus_out,
                                                    _buffer, 27))
        _buffer = self.txtPrescribedAction.get_child().get_child().get_buffer()
        self._lst_handler_id.append(_buffer.connect('changed',
                                                    self._on_focus_out,
                                                    _buffer, 28))
        _buffer = self.txtActionTaken.get_child().get_child().get_buffer()
        self._lst_handler_id.append(_buffer.connect('changed',
                                                    self._on_focus_out,
                                                    _buffer, 29))
        self._lst_handler_id.append(
            self.txtActionDueDate.connect('changed', self._on_focus_out,
                                          self.txtActionDueDate, 30))
        self._lst_handler_id.append(
            self.txtActionApproveDate.connect('changed', self._on_focus_out,
                                              self.txtActionApproveDate, 31))
        self._lst_handler_id.append(
            self.txtActionCloseDate.connect('changed', self._on_focus_out,
                                            self.txtActionCloseDate, 32))

        self._lst_handler_id.append(
            self.txtReviewDate.connect('changed', self._on_focus_out,
                                       self.txtActionCloseDate, 33))
        self._lst_handler_id.append(
            self.txtApproveDate.connect('changed', self._on_focus_out,
                                        self.txtActionCloseDate, 34))
        self._lst_handler_id.append(
            self.txtCloseDate.connect('changed', self._on_focus_out,
                                      self.txtActionCloseDate, 35))

        # Put it all together.
        _toolbar = self._create_toolbar()
        self.pack_start(_toolbar, expand=False)

        self._notebook = self._create_notebook()
        self.pack_end(self._notebook)

        self.show_all()

    def _create_toolbar(self):
        """
        Method to create the toolbar for the Incident class Work Book.
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        # Add item menu.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/add.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 1)
        _button.set_tooltip_text(_(u"Add a new incident to the open RTK "
                                   u"Program database."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Save incident button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.set_name('Save')
        _button.connect('clicked', self._on_button_clicked, 2)
        _button.set_tooltip_text(_(u"Saves the currently selected incident "
                                   u"to the open RTK Program database."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Create a filter button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/filter.png')
        _button.set_icon_widget(_image)
        _button.set_name('Filter')
        _button.connect('clicked', self._on_button_clicked, 3)
        _button.set_tooltip_text(_(u"Launches the Program Incident filter "
                                   u"assistant."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Create an import button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/db-import.png')
        _button.set_icon_widget(_image)
        _button.set_name('Import')
        _button.connect('clicked', self._on_button_clicked, 4)
        _button.set_tooltip_text(_(u"Launches the Program Incident import "
                                   u"assistant."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Create an export button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/db-export.png')
        _button.set_icon_widget(_image)
        _button.set_name('Export')
        _button.connect('clicked', self._on_button_clicked, 5)
        _button.set_tooltip_text(_(u"Launches the Program Incident export "
                                   u"assistant."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Create a data set creation button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/wizard.png')
        _button.set_icon_widget(_image)
        _button.set_name('Data Set')
        _button.connect('clicked', self._on_button_clicked, 6)
        _button.set_tooltip_text(_(u"Launches the Data Set creation "
                                   u"assistant."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Add a checkbutton to allow the user to load all incidents from all
        # revisions when checked.  The default will be to leave this unchecked.
        self.chkAllRevisions.set_tooltip_text(_(u"Whether or not to include "
                                                u"incidents from all "
                                                u"revisions (checked) or only "
                                                u"the currently selected "
                                                u"revision (un-checked)."))
        self.chkAllRevisions.set_active(False)
        _alignment = gtk.Alignment(xalign=0.5, yalign=0.5)
        _alignment.add(self.chkAllRevisions)
        _toolitem = gtk.ToolItem()
        _toolitem.add(_alignment)
        _toolbar.insert(_toolitem, _position)

        _toolbar.show()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Incident class gtk.Notebook().
        """

        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if Configuration.TABPOS[2] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif Configuration.TABPOS[2] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif Configuration.TABPOS[2] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        self._create_incident_details_page(_notebook)
        self._create_chargeability_page(_notebook)
        self._create_incident_analysis_page(_notebook)
        self._create_action_page(_notebook)

        return _notebook

    def _create_incident_details_page(self, notebook):
        """
        Method to create the Incident class gtk.Notebook() page for
        displaying general information related to the selected incident.

        :param gtk.Notebook notebook: the Incident class gtk.Notebook()
                                      widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hpaned = gtk.HBox()
        _vbox = gtk.VBox()

        # Build the left side.
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = Widgets.make_frame(label=_(u"Incident Details"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hpaned.pack_start(_frame, expand=True, fill=True)
        _hpaned.pack_end(_vbox, expand=True, fill=True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display analysis input information. #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.ComboBox() widgets.
        self.cmbCategory.append_text("")
        for i in range(len(Configuration.RTK_INCIDENT_CATEGORY)):
            self.cmbCategory.append_text(
                Configuration.RTK_INCIDENT_CATEGORY[i])

        self.cmbType.append_text("")
        for i in range(len(Configuration.RTK_INCIDENT_TYPE)):
            self.cmbType.append_text(Configuration.RTK_INCIDENT_TYPE[i])

        self.cmbStatus.append_text("")
        for i in range(len(Configuration.RTK_INCIDENT_STATUS)):
            self.cmbStatus.append_text(Configuration.RTK_INCIDENT_STATUS[i])

        self.cmbCriticality.append_text("")
        for i in range(len(Configuration.RTK_INCIDENT_CRITICALITY)):
            self.cmbCriticality.append_text(
                Configuration.RTK_INCIDENT_CRITICALITY[i])

        self.cmbLifeCycle.append_text("")
        for i in range(len(Configuration.RTK_LIFECYCLE)):
            self.cmbLifeCycle.append_text(Configuration.RTK_LIFECYCLE[i])

        self.cmbRequestBy.append_text("")
        for i in range(len(Configuration.RTK_USERS)):
            self.cmbRequestBy.append_text(Configuration.RTK_USERS[i])

        _labels = [_(u"Incident ID:"), _(u"Incident Category:"),
                   _(u"Incident Type:"), _(u"Life Cycle:"),
                   _(u"Incident Criticality:"), _(u"Affected Assembly:"),
                   _(u"Affected Software:"), _(u"Reported By:"),
                   _(u"Date Opened:"), _(u"Incident Age:"),
                   _(u"Incident Status:")]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5)
        _x_pos += 30

        _fixed.put(self.txtID, _x_pos, _y_pos[0])
        _fixed.put(self.chkAccepted, _x_pos + 110, _y_pos[0])
        _fixed.put(self.chkReviewed, _x_pos + 220, _y_pos[0])
        _fixed.put(self.cmbCategory, _x_pos, _y_pos[1])
        _fixed.put(self.cmbType, _x_pos, _y_pos[2])
        _fixed.put(self.cmbLifeCycle, _x_pos, _y_pos[3])
        _fixed.put(self.cmbCriticality, _x_pos, _y_pos[4])
        _fixed.put(self.cmbHardware, _x_pos, _y_pos[5])
        _fixed.put(self.cmbSoftware, _x_pos, _y_pos[6])
        _fixed.put(self.cmbRequestBy, _x_pos, _y_pos[7])
        _fixed.put(self.txtRequestDate, _x_pos, _y_pos[8])
        _fixed.put(self.txtAge, _x_pos, _y_pos[9])
        _fixed.put(self.cmbStatus, _x_pos, _y_pos[10])

        _fixed.show_all()

        # Place the right side widgets.
        _fixed = gtk.Fixed()
        _vpaned = gtk.VPaned()

        _vbox.pack_start(_fixed, expand=False, fill=False)
        _vbox.pack_end(_vpaned, expand=True, fill=True)

        _labels = [_(u"Brief Problem Description:")]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5)
        _x_pos += 40

        _fixed.put(self.txtShortDescription, _x_pos, _y_pos[0])

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self.txtLongDescription)

        _frame = Widgets.make_frame(_(u"Detailed Problem Description:"))
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, resize=True, shrink=False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self.txtRemarks)

        _frame = Widgets.make_frame(_(u"Remarks:"))
        _frame.add(_scrollwindow)

        _vpaned.pack2(_frame, resize=True, shrink=False)

        _fixed.show_all()

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Incident\nDetails") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays details about the selected "
                                  u"incident."))

        notebook.insert_page(_hpaned, tab_label=_label, position=-1)

        return False

    def _create_chargeability_page(self, notebook):
        """
        Method to create the Incident class gtk.Notebook() page for
        displaying the failure relevancy and failure chargeability questions
        for the selected incident.  Only visible if the incident occurred
        during reliability growth testing.

        :param gtk.Notebook notebook: the Incident class gtk.Notebook()
                                      widget.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HBox()

        _fixed1 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed1)

        _frame = Widgets.make_frame(label=_(u"Incident Relevancy"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_start(_frame, expand=True)

        _fixed2 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed2)

        _frame = Widgets.make_frame(label=_(u"Incident Chargeability"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, expand=True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display the chargeability analysis. #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.ComboBox().
        _results = [[_(u"No")], [_(u"Yes")]]
        Widgets.load_combo(self.cmbRelevant1, _results)
        Widgets.load_combo(self.cmbRelevant2, _results)
        Widgets.load_combo(self.cmbRelevant3, _results)
        Widgets.load_combo(self.cmbRelevant4, _results)
        Widgets.load_combo(self.cmbRelevant5, _results)
        Widgets.load_combo(self.cmbRelevant6, _results)
        Widgets.load_combo(self.cmbRelevant7, _results)
        Widgets.load_combo(self.cmbRelevant8, _results)
        Widgets.load_combo(self.cmbRelevant9, _results)
        Widgets.load_combo(self.cmbRelevant10, _results)
        Widgets.load_combo(self.cmbRelevant11, _results)
        Widgets.load_combo(self.cmbRelevant12, _results)
        Widgets.load_combo(self.cmbRelevant13, _results)
        Widgets.load_combo(self.cmbRelevant14, _results)
        Widgets.load_combo(self.cmbRelevant15, _results)
        Widgets.load_combo(self.cmbRelevant16, _results)
        Widgets.load_combo(self.cmbRelevant17, _results)
        Widgets.load_combo(self.cmbRelevant18, _results)
        Widgets.load_combo(self.cmbChargeable1, _results)
        Widgets.load_combo(self.cmbChargeable2, _results)
        Widgets.load_combo(self.cmbChargeable3, _results)
        Widgets.load_combo(self.cmbChargeable4, _results)
        Widgets.load_combo(self.cmbChargeable5, _results)

        # Place the quadrant #1 widgets.
        _y_pos = 5
        _fixed1.put(self.lblRelevant1, 5, _y_pos)
        _fixed1.put(self.cmbRelevant1, 505, _y_pos)
        _y_pos += self.lblRelevant1.size_request()[1] + 35
        _fixed1.put(self.lblRelevant2, 5, _y_pos)
        _fixed1.put(self.cmbRelevant2, 505, _y_pos)
        _y_pos += self.lblRelevant2.size_request()[1] + 35
        _fixed1.put(self.lblRelevant3, 5, _y_pos)
        _fixed1.put(self.cmbRelevant3, 505, _y_pos)
        _y_pos += self.lblRelevant3.size_request()[1] + 35
        _fixed1.put(self.lblRelevant4, 5, _y_pos)
        _fixed1.put(self.cmbRelevant4, 505, _y_pos)
        _y_pos += self.lblRelevant4.size_request()[1] + 35
        _fixed1.put(self.lblRelevant5, 5, _y_pos)
        _fixed1.put(self.cmbRelevant5, 505, _y_pos)
        _y_pos += self.lblRelevant5.size_request()[1] + 35
        _fixed1.put(self.lblRelevant6, 5, _y_pos)
        _fixed1.put(self.cmbRelevant6, 505, _y_pos)
        _y_pos += self.lblRelevant6.size_request()[1] + 35
        _fixed1.put(self.lblRelevant7, 5, _y_pos)
        _fixed1.put(self.cmbRelevant7, 505, _y_pos)
        _y_pos += self.lblRelevant7.size_request()[1] + 35
        _fixed1.put(self.lblRelevant8, 5, _y_pos)
        _fixed1.put(self.cmbRelevant8, 505, _y_pos)
        _y_pos += self.lblRelevant8.size_request()[1] + 35
        _fixed1.put(self.lblRelevant9, 5, _y_pos)
        _fixed1.put(self.cmbRelevant9, 505, _y_pos)
        _y_pos += self.lblRelevant9.size_request()[1] + 35
        _fixed1.put(self.lblRelevant10, 5, _y_pos)
        _fixed1.put(self.cmbRelevant10, 505, _y_pos)
        _y_pos += self.lblRelevant10.size_request()[1] + 35
        _fixed1.put(self.lblRelevant11, 5, _y_pos)
        _fixed1.put(self.cmbRelevant11, 505, _y_pos)
        _y_pos += self.lblRelevant11.size_request()[1] + 35
        _fixed1.put(self.lblRelevant12, 5, _y_pos)
        _fixed1.put(self.cmbRelevant12, 505, _y_pos)
        _y_pos += self.lblRelevant12.size_request()[1] + 35
        _fixed1.put(self.lblRelevant13, 5, _y_pos)
        _fixed1.put(self.cmbRelevant13, 505, _y_pos)
        _y_pos += self.lblRelevant13.size_request()[1] + 35
        _fixed1.put(self.lblRelevant14, 5, _y_pos)
        _fixed1.put(self.cmbRelevant14, 505, _y_pos)
        _y_pos += self.lblRelevant14.size_request()[1] + 35
        _fixed1.put(self.lblRelevant15, 5, _y_pos)
        _fixed1.put(self.cmbRelevant15, 505, _y_pos)
        _y_pos += self.lblRelevant15.size_request()[1] + 35
        _fixed1.put(self.lblRelevant16, 5, _y_pos)
        _fixed1.put(self.cmbRelevant16, 505, _y_pos)
        _y_pos += self.lblRelevant16.size_request()[1] + 35
        _fixed1.put(self.lblRelevant17, 5, _y_pos)
        _fixed1.put(self.cmbRelevant17, 505, _y_pos)
        _y_pos += self.lblRelevant17.size_request()[1] + 35
        _fixed1.put(self.lblRelevant18, 5, _y_pos)
        _fixed1.put(self.cmbRelevant18, 505, _y_pos)
        _fixed1.put(self.lblRelevant, 655, 5)

        # Connect widgets to callback methods.
        self.cmbRelevant1.connect('changed', self._on_relevancy_changed, 100)
        self.cmbRelevant2.connect('changed', self._on_relevancy_changed, 101)
        self.cmbRelevant3.connect('changed', self._on_relevancy_changed, 102)
        self.cmbRelevant4.connect('changed', self._on_relevancy_changed, 103)
        self.cmbRelevant5.connect('changed', self._on_relevancy_changed, 104)
        self.cmbRelevant6.connect('changed', self._on_relevancy_changed, 105)
        self.cmbRelevant7.connect('changed', self._on_relevancy_changed, 106)
        self.cmbRelevant8.connect('changed', self._on_relevancy_changed, 107)
        self.cmbRelevant9.connect('changed', self._on_relevancy_changed, 108)
        self.cmbRelevant10.connect('changed', self._on_relevancy_changed, 109)
        self.cmbRelevant11.connect('changed', self._on_relevancy_changed, 110)
        self.cmbRelevant12.connect('changed', self._on_relevancy_changed, 111)
        self.cmbRelevant13.connect('changed', self._on_relevancy_changed, 112)
        self.cmbRelevant14.connect('changed', self._on_relevancy_changed, 113)
        self.cmbRelevant15.connect('changed', self._on_relevancy_changed, 114)
        self.cmbRelevant16.connect('changed', self._on_relevancy_changed, 115)
        self.cmbRelevant17.connect('changed', self._on_relevancy_changed, 116)
        self.cmbRelevant18.connect('changed', self._on_relevancy_changed, 117)

        # Place the quadrant #2 widgets.
        _y_pos = 5
        _fixed2.put(self.lblChargeable1, 5, _y_pos)
        _fixed2.put(self.cmbChargeable1, 505, _y_pos)
        _y_pos += self.lblChargeable1.size_request()[1] + 35
        _fixed2.put(self.lblChargeable2, 5, _y_pos)
        _fixed2.put(self.cmbChargeable2, 505, _y_pos)
        _y_pos += self.lblChargeable2.size_request()[1] + 35
        _fixed2.put(self.lblChargeable3, 5, _y_pos)
        _fixed2.put(self.cmbChargeable3, 505, _y_pos)
        _y_pos += self.lblChargeable3.size_request()[1] + 35
        _fixed2.put(self.lblChargeable4, 5, _y_pos)
        _fixed2.put(self.cmbChargeable4, 505, _y_pos)
        _y_pos += self.lblChargeable4.size_request()[1] + 35
        _fixed2.put(self.lblChargeable5, 5, _y_pos)
        _fixed2.put(self.cmbChargeable5, 505, _y_pos)
        _fixed2.put(self.lblChargeable, 655, 5)

        # Connect widgets to callback methods.
        self.cmbChargeable1.connect('changed',
                                    self._on_chargeability_changed, 0)
        self.cmbChargeable2.connect('changed',
                                    self._on_chargeability_changed, 1)
        self.cmbChargeable3.connect('changed',
                                    self._on_chargeability_changed, 2)
        self.cmbChargeable4.connect('changed',
                                    self._on_chargeability_changed, 3)
        self.cmbChargeable5.connect('changed',
                                    self._on_chargeability_changed, 4)

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Incident\nChargeability") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the chargeability analysis of "
                                  u"the selected incident."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_incident_analysis_page(self, notebook):
        """
        Method to create the Incident class gtk.Notebook() page for
        displaying the analysis of the selected incident.

        :param gtk.Notebook notebook: the Incident class gtk.Notebook()
                                      widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HBox()
        _hbox2 = gtk.HBox()
        _hbox.pack_start(_hbox2)

        _fixed1 = gtk.Fixed()

        _frame = Widgets.make_frame(label=_(u"Software Incident"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_fixed1)
        _hbox2.pack_start(_frame, expand=False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self.txtAnalysis)

        _frame = Widgets.make_frame(label=_(u"Incident Analysis"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox2.pack_end(_frame)

        _fixed2 = gtk.Fixed()
        _hbox.pack_end(_fixed2, expand=False)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display analysis input information. #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.ComboBox() widgets in quadrant #1.
        self.cmbDetectionMethod.append_text("")
        for i in range(len(Configuration.RTK_DETECTION_METHODS)):
            self.cmbDetectionMethod.append_text(
                Configuration.RTK_DETECTION_METHODS[i])

        # Load the gtk.ComboBox() widgets in quadrant #3.
        self.cmbReviewBy.append_text("")
        self.cmbApproveBy.append_text("")
        self.cmbCloseBy.append_text("")
        for i in range(len(Configuration.RTK_USERS)):
            self.cmbReviewBy.append_text(Configuration.RTK_USERS[i])
            self.cmbApproveBy.append_text(Configuration.RTK_USERS[i])
            self.cmbCloseBy.append_text(Configuration.RTK_USERS[i])

        # Place the quadrant #1 widgets.
        _labels = [_(u"Detection Method:"), _(u"Found in Test:"),
                   _(u"Found in Test Case:"), _(u"Execution Time:")]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed1, 5, 5)
        _x_pos += 30

        _fixed1.put(self.cmbDetectionMethod, _x_pos, _y_pos[0])
        _fixed1.put(self.txtTest, _x_pos, _y_pos[1] + 5)
        _fixed1.put(self.txtTestCase, _x_pos, _y_pos[2] + 5)
        _fixed1.put(self.txtExecutionTime, _x_pos, _y_pos[3] + 5)

        # Place the quadrant #3 widgets.
        _labels = [_(u"Reviewed By:"), _(u"Date Reviewed:"),
                   _(u"Approved By:"), _(u"Date Approved:"), _(u"Closed By:"),
                   _(u"Date Closed:")]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed2, 5, 5)
        _x_pos += 30

        _fixed2.put(self.cmbReviewBy, _x_pos, _y_pos[0])
        _fixed2.put(self.txtReviewDate, _x_pos, _y_pos[1] + 5)
        _fixed2.put(self.btnReviewDate, _x_pos + 105, _y_pos[1] + 5)
        _fixed2.put(self.cmbApproveBy, _x_pos, _y_pos[2] + 5)
        _fixed2.put(self.txtApproveDate, _x_pos, _y_pos[3] + 5)
        _fixed2.put(self.btnApproveDate, _x_pos + 105, _y_pos[3] + 5)
        _fixed2.put(self.cmbCloseBy, _x_pos, _y_pos[4] + 5)
        _fixed2.put(self.txtCloseDate, _x_pos, _y_pos[5] + 5)
        _fixed2.put(self.btnClosureDate, _x_pos + 105, _y_pos[5] + 5)

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Incident\nAnalysis") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the analysis of the selected "
                                  u"incident."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_action_page(self, notebook):
        """
        Method to create the page for creating, displaying, and documenting
        (corrective) actions associated with the selected Incident.

        :param gtk.Notebook notebook: the Incident class gtk.Notebook()
                                      widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HBox()
        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        _hpaned = gtk.HPaned()

        _hbox.pack_start(_bbox, False, False)
        _hbox.pack_end(_hpaned, True, True)

        _vbox = gtk.VBox()

        _hpaned.pack1(_vbox, True, False)

        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self.txtPrescribedAction)

        _frame = Widgets.make_frame(_(u"Prescribed Action"))
        _frame.add(_scrollwindow)

        _vbox.pack_start(_frame)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self.txtActionTaken)

        _frame = Widgets.make_frame(_(u"Action Taken"))
        _frame.add(_scrollwindow)

        _vbox.pack_end(_frame)

        _hpaned.pack2(_fixed, False, False)

        _bbox.pack_start(self.btnSaveAction, False, False)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display Incident action information.#
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.ComboBox() widgets in quadrant #4 (right-most).
        self.cmbActionOwner.append_text("")
        for i in range(len(Configuration.RTK_USERS)):
            self.cmbActionOwner.append_text(Configuration.RTK_USERS[i])

        self.cmbActionApproveBy.append_text("")
        for i in range(len(Configuration.RTK_USERS)):
            self.cmbActionApproveBy.append_text(Configuration.RTK_USERS[i])

        self.cmbActionCloseBy.append_text("")
        for i in range(len(Configuration.RTK_USERS)):
            self.cmbActionCloseBy.append_text(Configuration.RTK_USERS[i])

        self.cmbActionStatus.append_text("")
        for i in [0, 2, 6, 7, 8, 9]:
            self.cmbActionStatus.append_text(
                Configuration.RTK_INCIDENT_STATUS[i])

        # Set the labels for quadrant #4.
        _labels = [_(u"Action Owner:"), _(u"Due Date:"), _(u"Status:"),
                   _(u"Approved By:"), _(u"Approval Date:"), _(u"Closed By:"),
                   _(u"Closure Date:")]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5, 35)
        _x_pos += 30

        # Place the widgets in quadrant #4.
        _fixed.put(self.cmbActionOwner, _x_pos, _y_pos[0])
        _fixed.put(self.txtActionDueDate, _x_pos, _y_pos[1])
        _fixed.put(self.btnActionDueDate, _x_pos + 105, _y_pos[1])
        _fixed.put(self.cmbActionStatus, _x_pos, _y_pos[2])
        _fixed.put(self.cmbActionApproveBy, _x_pos, _y_pos[3])
        _fixed.put(self.txtActionApproveDate, _x_pos, _y_pos[4])
        _fixed.put(self.btnActionApproveDate, _x_pos + 105, _y_pos[4])
        _fixed.put(self.cmbActionCloseBy, _x_pos, _y_pos[5])
        _fixed.put(self.txtActionCloseDate, _x_pos, _y_pos[6])
        _fixed.put(self.btnActionCloseDate, _x_pos + 105, _y_pos[6])

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Incident\nActions") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Display the details of the selected "
                                  u"action related to the selected incident."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Incident class gtk.Notebook().

        :param model: the :py:class:`rtk.incident.Incident.Model` whose
                      attributes will be loaded into the display widgets.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._model = model

        self.cmbHardware.handler_block(self._lst_handler_id[8])
        self.cmbSoftware.handler_block(self._lst_handler_id[9])

        Widgets.load_combo(self.cmbHardware, Configuration.RTK_HARDWARE_LIST,
                           simple=False)
        for i in range(len(Configuration.RTK_HARDWARE_LIST)):
            self._dic_hardware[Configuration.RTK_HARDWARE_LIST[i][1]] = i + 1

        Widgets.load_combo(self.cmbSoftware, Configuration.RTK_SOFTWARE_LIST,
                           simple=False)
        for i in range(len(Configuration.RTK_SOFTWARE_LIST)):
            self._dic_software[Configuration.RTK_SOFTWARE_LIST[i][1]] = i + 1

        self.cmbHardware.handler_unblock(self._lst_handler_id[8])
        self.cmbSoftware.handler_unblock(self._lst_handler_id[9])

        self.txtID.set_text(str(model.incident_id))
        self.chkReviewed.set_active(model.reviewed)
        self.chkAccepted.set_active(model.accepted)

        self.cmbCategory.set_active(model.incident_category)
        self.cmbType.set_active(model.incident_type)
        self.cmbCriticality.set_active(model.criticality)
        self.cmbLifeCycle.set_active(model.life_cycle)
        self.cmbRequestBy.set_active(model.request_by)

        try:
            self.cmbHardware.set_active(self._dic_hardware[model.hardware_id])
        except KeyError:
            self.cmbHardware.set_active(0)
        try:
            self.cmbSoftware.set_active(self._dic_software[model.software_id])
        except KeyError:
            self.cmbSoftware.set_active(0)

        _date = Utilities.ordinal_to_date(model.request_date)
        self.txtRequestDate.set_text(str(_date))
        self.cmbStatus.set_active(model.status)
        self.txtAge.set_text(str(model.incident_age))

        self.txtShortDescription.set_text(Utilities.none_to_string(
            model.short_description))
        _buffer = self.txtLongDescription.get_child().get_child().get_buffer()
        _buffer.set_text(Utilities.none_to_string(model.detail_description))
        _buffer = self.txtRemarks.get_child().get_child().get_buffer()
        _buffer.set_text(Utilities.none_to_string(model.remarks))

        # Load the chargeability page.
        self._load_chargeability_page()

        # Load the incident analysis page.
        self.cmbDetectionMethod.set_active(model.detection_method)
        self.txtTest.set_text(Utilities.none_to_string(model.test))
        self.txtTestCase.set_text(Utilities.none_to_string(model.test_case))
        self.txtExecutionTime.set_text(str(model.execution_time))

        _buffer = self.txtAnalysis.get_child().get_child().get_buffer()
        _buffer.set_text(Utilities.none_to_string(model.analysis))

        self.cmbReviewBy.set_active(model.review_by)
        _date = Utilities.ordinal_to_date(model.review_date)
        self.txtReviewDate.set_text(str(_date))

        self.cmbApproveBy.set_active(model.approve_by)
        _date = Utilities.ordinal_to_date(model.approve_date)
        self.txtApproveDate.set_text(str(_date))

        self.cmbCloseBy.set_active(model.close_by)
        _date = Utilities.ordinal_to_date(model.close_date)
        self.txtCloseDate.set_text(str(_date))

        return False

    def _determine_relevancy(self):
        """
        Method to determine the Incident relevancy.

        :return: _visible
        :rtype: list
        """
        # FIXME: Refactor _determine_relevancy; current McCabe Complexity metric = 53.
        _visible = [True, False, False, False, False, False, False, False,
                    False, False, False, False, False, False, False, False,
                    False, False]

        # Question #1.
        if self._model.lstRelevant[0] == 0:     # Goto 2.
            _visible[1] = True
        elif self._model.lstRelevant[0] == 1:   # Stop.
            _visible[1] = False
            self._model.lstRelevant[1:18] = [-1, -1, -1, -1, -1, -1, -1, -1,
                                             -1, -1, -1, -1, -1, -1, -1, -1,
                                             -1]
            self._model.relevant = 0
        else:
            _visible[1] = False

        # Question #2.
        if self._model.lstRelevant[1] == 0:     # Goto 3.
            _visible[2] = True
        elif self._model.lstRelevant[1] == 1:   # Stop.
            _visible[2] = False
            self._model.lstRelevant[2:18] = [-1, -1, -1, -1, -1, -1, -1, -1,
                                             -1, -1, -1, -1, -1, -1, -1, -1]
            self._model.relevant = 1
        else:
            _visible[2] = False

        # Question #3.
        if self._model.lstRelevant[2] == 0:     # Goto 4.
            _visible[3] = True
        elif self._model.lstRelevant[2] == 1:   # Stop.
            _visible[3] = False
            self._model.lstRelevant[3:18] = [-1, -1, -1, -1, -1, -1, -1, -1,
                                             -1, -1, -1, -1, -1, -1, -1]
            self._model.relevant = 0
        else:
            _visible[3] = False

        # Question #4.
        if self._model.lstRelevant[3] == 0:     # Goto 5.
            _visible[4] = True
        elif self._model.lstRelevant[3] == 1:   # Stop.
            _visible[4] = False
            self._model.lstRelevant[4:18] = [-1, -1, -1, -1, -1, -1, -1, -1,
                                             -1, -1, -1, -1, -1, -1]
            self._model.relevant = 0
        else:
            _visible[4] = False

        # Question #5.
        if self._model.lstRelevant[4] == 0:     # Stop.
            _visible[5] = False
            self._model.lstRelevant[5:18] = [-1, -1, -1, -1, -1, -1, -1, -1,
                                             -1, -1, -1, -1, -1]
            self._model.relevant = 0
        elif self._model.lstRelevant[4] == 1:   # Goto 6.
            _visible[5] = True
        else:
            _visible[5] = False

        # Question #6.
        if self._model.lstRelevant[5] == 0:     # Goto 7.
            _visible[6] = True
            _visible[7] = False
        elif self._model.lstRelevant[5] == 1:   # Goto 8.
            _visible[6] = False
            _visible[7] = True
        else:
            _visible[6] = False
            _visible[7] = False

        # Question #7.
        if self._model.lstRelevant[6] == 0:     # Stop.
            self._model.lstRelevant[7:18] = [-1, -1, -1, -1, -1, -1, -1, -1,
                                             -1, -1, -1, -1, -1]
            self._model.relevant = 1
        elif self._model.lstRelevant[6] == 1:   # Stop.
            self._model.lstRelevant[7:18] = [-1, -1, -1, -1, -1, -1, -1, -1,
                                             -1, -1, -1, -1, -1]
            self._model.relevant = 1

        # Question #8.
        if self._model.lstRelevant[7] == 0:     # Goto 9.
            _visible[8] = True
        elif self._model.lstRelevant[7] == 1:   # Stop.
            _visible[8] = False
            self._model.lstRelevant[8:18] = [-1, -1, -1, -1, -1, -1, -1, -1,
                                             -1, -1, -1]
            self._model.relevant = 1
        else:
            _visible[8] = False

        # Question #9.
        if self._model.lstRelevant[8] == 0:     # Goto 10.
            _visible[9] = True
        elif self._model.lstRelevant[8] == 1:   # Stop.
            _visible[9] = False
            self._model.lstRelevant[9:18] = [-1, -1, -1, -1, -1, -1, -1, -1,
                                             -1, -1, -1]
            self._model.relevant = 1
        else:
            _visible[9] = False

        # Question #10.
        if self._model.lstRelevant[9] == 0:     # Goto 11.
            _visible[10] = True
            _visible[11] = False
        elif self._model.lstRelevant[9] == 1:   # Goto 12.
            _visible[10] = False
            _visible[11] = True
        else:
            _visible[10] = False
            _visible[11] = False

        # Question #11.
        if self._model.lstRelevant[10] == 0:    # Stop.
            _visible[11] = False
            self._model.lstRelevant[11:18] = [-1, -1, -1, -1, -1, -1, -1, -1,
                                              -1, -1]
            self._model.relevant = 0
        elif self._model.lstRelevant[10] == 1:  # Goto 12.
            _visible[11] = True

        # Question #12.
        if self._model.lstRelevant[11] == 0:    # Goto 13.
            _visible[12] = True
        elif self._model.lstRelevant[11] == 1:  # Stop.
            _visible[12] = False
            self._model.lstRelevant[12:18] = [-1, -1, -1, -1, -1, -1, -1, -1,
                                              -1]
            self._model.relevant = 1

        # Question #13.
        if self._model.lstRelevant[12] == 0:    # Stop.
            _visible[13] = False
            self._model.lstRelevant[13:18] = [-1, -1, -1, -1, -1, -1, -1, -1]
            self._model.relevant = 0
        elif self._model.lstRelevant[12] == 1:  # Goto 14.
            _visible[13] = True
        else:
            _visible[13] = False

        # Question #14.
        if self._model.lstRelevant[13] == 0:    # Goto 16.
            _visible[14] = False
            _visible[15] = True
            self._model.lstRelevant[14] = -1
        elif self._model.lstRelevant[13] == 1:  # Goto 15.
            _visible[14] = True
            _visible[15] = False
            self._model.lstRelevant[15] = -1
        else:
            _visible[14] = False
            _visible[15] = False

        # Question #15.
        if self._model.lstRelevant[14] == 0:    # Goto 18.
            _visible[17] = True
        elif self._model.lstRelevant[14] == 1:  # Stop.
            _visible[17] = False
            self._model.lstRelevant[17] = -1
            self._model.relevant = 0
        else:
            _visible[17] = False

        # Question #16.
        if self._model.lstRelevant[15] == 0:    # Goto 18.
            _visible[16] = False
            _visible[17] = True
            self._model.lstRelevant[16] = -1
        elif self._model.lstRelevant[15] == 1:  # Goto 17.
            _visible[16] = True
            _visible[17] = False

        # Question #17.
        if self._model.lstRelevant[16] == 0:    # Goto 18.
            _visible[17] = True
        elif self._model.lstRelevant[16] == 1:  # Stop.
            _visible[17] = False
            self._model.lstRelevant[17] = -1
            self._model.relevant = 0

        # Question #18.
        if self._model.lstRelevant[17] == 0:    # Stop.
            self._model.relevant = 1
        elif self._model.lstRelevant[17] == 1:  # Stop.
            self._model.relevant = 0

        if self.cmbRelevant10.get_active() == 2:
            _visible[10] = False

        if self._model.relevant == 0:
            self.lblRelevant.set_text(_(u"Failure is NOT relevant."))
        elif self._model.relevant == 1:
            self.lblRelevant.set_text(_(u"Failure IS relevant."))
        else:
            self.lblRelevant.set_text("")

        return _visible

    def _determine_chargeablity(self):
        """
        Method to determine the Incident chargeability.

        :return: _visible
        :rtype: list
        """
# WARNING: Refactor _determine_chargeability; current McCabe Complexity metric = 19.
        _visible = [False, False, False, False, False]

        if self._model.relevant == 1:
            _visible[0] = True

        # Question #1.
        if self._model.lstChargeable[0] == 0:      # Goto 2.
            _visible[1] = True
        elif self._model.lstChargeable[0] == 1:    # Stop.
            _visible[1] = False
            self._model.lstChargeable[1:5] = [-1, -1, -1, -1]
            self._model.chargeable = 0
        else:
            _visible[1] = False

        # Question #2.
        if self._model.lstChargeable[1] == 0:      # Goto 3.
            _visible[2] = True
        elif self._model.lstChargeable[1] == 1:    # Stop.
            _visible[2] = False
            self._model.lstChargeable[2:5] = [-1, -1, -1]
            self._model.chargeable = 0
        else:
            _visible[2] = False

        # Question #3.
        if self._model.lstChargeable[2] == 0:      # Stop.
            _visible[3] = False
            self._model.lstChargeable[3:5] = [-1, -1, -1]
            self._model.chargeable = 1
        elif self._model.lstChargeable[2] == 1:    # Goto 4.
            _visible[3] = True
        else:
            _visible[3] = False

        # Question #4.
        if self._model.lstChargeable[3] == 0:      # Goto 5.
            _visible[4] = True
        elif self._model.lstChargeable[3] == 1:    # Stop.
            self._model.chargeable = 1
            _visible[4] = False
            self._model.lstChargeable[4:5] = [-1, -1]
        else:
            _visible[4] = False

        # Question #5.
        if self._model.lstChargeable[4] == 0:      # Stop.
            self._model.chargeable = 0
        elif self._model.lstChargeable[4] == 1:    # Stop.
            self._model.chargeable = 1

        if self._model.chargeable == 0:
            self.lblChargeable.set_text(_(u"Failure is NOT chargeable."))
        elif self._model.chargeable == 1:
            self.lblChargeable.set_text(_(u"Failure IS chargeable."))
        else:
            self.lblChargeable.set_text("")

        return _visible

    def _load_chargeability_page(self):
        """
        Method to load the Incident chargeability page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _visible = self._determine_relevancy()

        self.cmbRelevant1.set_visible(_visible[0])
        self.lblRelevant1.set_visible(_visible[0])
        self.cmbRelevant2.set_visible(_visible[1])
        self.lblRelevant2.set_visible(_visible[1])
        self.cmbRelevant3.set_visible(_visible[2])
        self.lblRelevant3.set_visible(_visible[2])
        self.cmbRelevant4.set_visible(_visible[3])
        self.lblRelevant4.set_visible(_visible[3])
        self.cmbRelevant5.set_visible(_visible[4])
        self.lblRelevant5.set_visible(_visible[4])
        self.cmbRelevant6.set_visible(_visible[5])
        self.lblRelevant6.set_visible(_visible[5])
        self.cmbRelevant7.set_visible(_visible[6])
        self.lblRelevant7.set_visible(_visible[6])
        self.cmbRelevant8.set_visible(_visible[7])
        self.lblRelevant8.set_visible(_visible[7])
        self.cmbRelevant9.set_visible(_visible[8])
        self.lblRelevant9.set_visible(_visible[8])
        self.cmbRelevant10.set_visible(_visible[9])
        self.lblRelevant10.set_visible(_visible[9])
        self.cmbRelevant11.set_visible(_visible[10])
        self.lblRelevant11.set_visible(_visible[10])
        self.cmbRelevant12.set_visible(_visible[11])
        self.lblRelevant12.set_visible(_visible[11])
        self.cmbRelevant13.set_visible(_visible[12])
        self.lblRelevant13.set_visible(_visible[12])
        self.cmbRelevant14.set_visible(_visible[13])
        self.lblRelevant14.set_visible(_visible[13])
        self.cmbRelevant15.set_visible(_visible[14])
        self.lblRelevant15.set_visible(_visible[14])
        self.cmbRelevant16.set_visible(_visible[15])
        self.lblRelevant16.set_visible(_visible[15])
        self.cmbRelevant17.set_visible(_visible[16])
        self.lblRelevant17.set_visible(_visible[16])
        self.cmbRelevant18.set_visible(_visible[17])
        self.lblRelevant18.set_visible(_visible[17])

        self.cmbRelevant1.set_active(self._model.lstRelevant[0] + 1)
        self.cmbRelevant2.set_active(self._model.lstRelevant[1] + 1)
        self.cmbRelevant3.set_active(self._model.lstRelevant[2] + 1)
        self.cmbRelevant4.set_active(self._model.lstRelevant[3] + 1)
        self.cmbRelevant5.set_active(self._model.lstRelevant[4] + 1)
        self.cmbRelevant6.set_active(self._model.lstRelevant[5] + 1)
        self.cmbRelevant7.set_active(self._model.lstRelevant[6] + 1)
        self.cmbRelevant8.set_active(self._model.lstRelevant[7] + 1)
        self.cmbRelevant9.set_active(self._model.lstRelevant[8] + 1)
        self.cmbRelevant10.set_active(self._model.lstRelevant[9] + 1)
        self.cmbRelevant11.set_active(self._model.lstRelevant[10] + 1)
        self.cmbRelevant12.set_active(self._model.lstRelevant[11] + 1)
        self.cmbRelevant13.set_active(self._model.lstRelevant[12] + 1)
        self.cmbRelevant14.set_active(self._model.lstRelevant[13] + 1)
        self.cmbRelevant15.set_active(self._model.lstRelevant[14] + 1)
        self.cmbRelevant16.set_active(self._model.lstRelevant[15] + 1)
        self.cmbRelevant17.set_active(self._model.lstRelevant[16] + 1)
        self.cmbRelevant18.set_active(self._model.lstRelevant[17] + 1)

        _visible = self._determine_chargeablity()

        self.cmbChargeable1.set_visible(_visible[0])
        self.lblChargeable1.set_visible(_visible[0])
        self.cmbChargeable2.set_visible(_visible[1])
        self.lblChargeable2.set_visible(_visible[1])
        self.cmbChargeable3.set_visible(_visible[2])
        self.lblChargeable3.set_visible(_visible[2])
        self.cmbChargeable4.set_visible(_visible[3])
        self.lblChargeable4.set_visible(_visible[3])
        self.cmbChargeable5.set_visible(_visible[4])
        self.lblChargeable5.set_visible(_visible[4])

        self.cmbChargeable1.set_active(self._model.lstChargeable[0] + 1)
        self.cmbChargeable2.set_active(self._model.lstChargeable[1] + 1)
        self.cmbChargeable3.set_active(self._model.lstChargeable[2] + 1)
        self.cmbChargeable4.set_active(self._model.lstChargeable[3] + 1)
        self.cmbChargeable5.set_active(self._model.lstChargeable[4] + 1)

        return False

    def load_action_page(self, action_id):
        """
        Method to load the Incident action page.

        :param int action_id: the ID of the Incident Action to load.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._action = self.mdcRTK.dtcAction.dicActions[action_id]

        self.cmbActionOwner.set_active(self._action.action_owner)
        self.cmbActionApproveBy.set_active(self._action.approved_by)
        self.cmbActionCloseBy.set_active(self._action.closed_by)
        self.cmbActionStatus.set_active(self._action.status)

        _buffer = self.txtPrescribedAction.get_child().get_child().get_buffer()
        _buffer.set_text(
            Utilities.none_to_string(self._action.prescribed_action))
        _buffer = self.txtActionTaken.get_child().get_child().get_buffer()
        _buffer.set_text(Utilities.none_to_string(self._action.action_taken))

        # Disable or enable various widgets to prevent changes being made to
        # an action after it passes through certain stages.
        if self._action.status > 1:         # Past initiation.
            self.txtPrescribedAction.get_child().get_child().set_editable(False)
            self.cmbActionOwner.set_button_sensitivity(gtk.SENSITIVITY_OFF)
            self.btnActionDueDate.set_visible(False)
        else:
            self.txtPrescribedAction.get_child().get_child().set_editable(True)
            self.cmbActionOwner.set_button_sensitivity(gtk.SENSITIVITY_ON)
            self.btnActionDueDate.set_visible(True)

        if self._action.status > 3:         # Past ready for approval.
            self.cmbApproveBy.set_button_sensitivity(gtk.SENSITIVITY_OFF)
            self.btnActionApproveDate.set_visible(False)
        else:
            self.cmbApproveBy.set_button_sensitivity(gtk.SENSITIVITY_ON)
            self.btnActionApproveDate.set_visible(True)

        if self._action.status == 6:        # Closed
            self.txtActionTaken.get_child().get_child().set_editable(False)
            self.cmbCloseBy.set_button_sensitivity(gtk.SENSITIVITY_OFF)
            self.btnActionCloseDate.set_visible(False)
        else:
            self.txtActionTaken.get_child().get_child().set_editable(True)
            self.cmbCloseBy.set_button_sensitivity(gtk.SENSITIVITY_ON)
            self.btnActionCloseDate.set_visible(True)

        self.txtActionDueDate.set_text(
            str(Utilities.ordinal_to_date(self._action.due_date)))
        self.txtActionApproveDate.set_text(
            str(Utilities.ordinal_to_date(self._action.approved_date)))
        self.txtActionCloseDate.set_text(
            str(Utilities.ordinal_to_date(self._action.closed_date)))

        return False

    def update(self):
        """
        Updates the Work Book widgets with changes to the Incident data model
        attributes.  Called by other views when the Incident data model
        attributes are edited via their gtk.Widgets().
        """

        self.cmbCategory.handler_block(self._lst_handler_id[2])
        self.cmbCategory.set_active(self._model.incident_category)
        self.cmbCategory.handler_unblock(self._lst_handler_id[2])

        self.cmbType.handler_block(self._lst_handler_id[3])
        self.cmbType.set_active(self._model.incident_type)
        self.cmbType.handler_unblock(self._lst_handler_id[3])

        self.cmbCriticality.handler_block(self._lst_handler_id[4])
        self.cmbCriticality.set_active(self._model.criticality)
        self.cmbCriticality.handler_unblock(self._lst_handler_id[4])

        self.cmbStatus.handler_block(self._lst_handler_id[5])
        self.cmbStatus.set_active(self._model.status)
        self.cmbStatus.handler_unblock(self._lst_handler_id[5])

        self.cmbLifeCycle.handler_block(self._lst_handler_id[9])
        self.cmbLifeCycle.set_active(self._model.life_cycle)
        self.cmbLifeCycle.handler_unblock(self._lst_handler_id[9])

        self.cmbDetectionMethod.handler_block(self._lst_handler_id[14])
        self.cmbDetectionMethod.set_active(self._model.detection_method)
        self.cmbDetectionMethod.handler_unblock(self._lst_handler_id[14])

        self.txtTest.set_text(Utilities.none_to_string(self._model.test))
        self.txtTestCase.set_text(
            Utilities.none_to_string(self._model.test_case))
        self.txtExecutionTime.set_text(str(self._model.execution_time))

        return False

    def _on_button_clicked(self, __button, index):
        """
        Method to respond to gtk.Button() 'clicked' signals and call the
        correct function or method, passing any parameters as needed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if index == 0:
            self._modulebook.request_save_action(self._action.action_id)
        elif index == 1:
            AddIncident(self._model.revision_id, self._modulebook._dao,
                        self._modulebook)
        elif index == 2:
            self.mdcRTK.dtcIncident.save_incident(self._model.incident_id)
        elif index == 3:
            FilterIncident(self._model.revision_id, self._modulebook)
        elif index == 4:
            ImportIncident(self._model.revision_id, self._modulebook._dao,
                           self._modulebook)
        elif index == 5:
# TODO: Create an export incident wizard.
            #ExportIncident()
            print "Export incident list."
        elif index == 6:
            CreateDataSet(self._model.revision_id, self._modulebook._dao,
                          self._modulebook)

        return False

    def _on_check_toggled(self, checkbutton, index):
        """
        Method to respond to gtk.CheckButton() 'toggled' signals.

        :param gtk.CheckButton checkbutton: the gtk.CheckButton() calling this
                                            method.
        :param int index: the index in the handler ID List of the callback
                          signal associated with the gtk.CheckButton that
                          called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        checkbutton.handler_block(self._lst_handler_id[index])

        _new_text = checkbutton.get_active()

        if index == 1:
            self._model.accepted = _new_text
            self._modulebook.update(index + 30, _new_text)
        elif index == 2:
            self._model.reviewed = _new_text
            self._modulebook.update(index + 18, _new_text)
        elif index == 3:
            self._modulebook.load_all_revisions = _new_text

        checkbutton.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_combo_changed(self, combo, index):
        """
        Method to respond to gtk.ComboBox() 'changed' signals.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.ComboBox() that
                          called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# WARNING: Refactor _on_combo_changed; current McCabe Complexity metric = 17.
        _selection = self._modulebook.listbook.tvwActionList.get_selection()

        combo.handler_block(self._lst_handler_id[index])

        if index == 4:
            self._model.incident_category = combo.get_active()
            _new_text = Configuration.RTK_INCIDENT_CATEGORY[combo.get_active() - 1]
            self._modulebook.update(index - 2, _new_text)
        elif index == 5:
            self._model.incident_type = combo.get_active()
            _new_text = Configuration.RTK_INCIDENT_TYPE[combo.get_active() - 1]
            self._modulebook.update(index - 2, _new_text)
        elif index == 6:
            self._model.criticality = combo.get_active()
            _new_text = Configuration.RTK_INCIDENT_CRITICALITY[combo.get_active() - 1]
            self._modulebook.update(index, _new_text)
        elif index == 7:
            self._model.status = combo.get_active()
            _new_text = Configuration.RTK_INCIDENT_STATUS[combo.get_active() - 1]
            self._modulebook.update(index + 2, _new_text)
        elif index == 8:
            _model = combo.get_model()
            _row = combo.get_active_iter()
            try:
                self._model.hardware_id = int(_model.get_value(_row, 1))
            except TypeError:
                self._model.hardware_id = 0
            except ValueError:
                self._model.hardware_id = 0
        elif index == 9:
            _model = combo.get_model()
            _row = combo.get_active_iter()
            try:
                self._model.software_id = int(_model.get_value(_row, 1))
            except TypeError:
                self._model.software_id = 0
            except ValueError:
                self._model.software_id = 0
        elif index == 10:
            self._model.request_by = combo.get_active()
            _new_text = Configuration.RTK_USERS[combo.get_active() - 1]
            self._modulebook.update(index + 8, _new_text)
        elif index == 11:
            self._model.life_cycle = combo.get_active()
            _new_text = Configuration.RTK_LIFECYCLE[combo.get_active() - 1]
            self._modulebook.update(index + 18, _new_text)
        elif index == 12:
            self._model.detection_method = combo.get_active()
            _new_text = Configuration.RTK_DETECTION_METHODS[combo.get_active() - 1]
            self._modulebook.update(index - 5, _new_text)
        elif index == 13:
            self._model.review_by = combo.get_active()
            _new_text = Configuration.RTK_USERS[combo.get_active() - 1]
            self._modulebook.update(index + 8, _new_text)
        elif index == 14:
            self._model.approve_by = combo.get_active()
            _new_text = Configuration.RTK_USERS[combo.get_active() - 1]
            self._modulebook.update(index + 10, _new_text)
        elif index == 15:
            self._model.close_by = combo.get_active()
            _new_text = Configuration.RTK_USERS[combo.get_active() - 1]
            self._modulebook.update(index + 12, _new_text)
        elif index == 16:
            self._action.action_owner = combo.get_active()
            _new_text = Configuration.RTK_USERS[combo.get_active() - 1]
            (_model,
             _row) = _selection.get_selected()
            _model.set_value(_row, 3, _new_text)
        elif index == 17:
            self._action.status = combo.get_active()
            # We only use a sub-set of the status so we can't use indexing.
            _new_text = combo.get_active_text()
            (_model,
             _row) = _selection.get_selected()
            _model.set_value(_row, 5, _new_text)
        elif index == 18:
            self._action.approved_by = combo.get_active()
            _new_text = Configuration.RTK_USERS[combo.get_active() - 1]
            (_model,
             _row) = _selection.get_selected()
            _model.set_value(_row, 6, _new_text)
        elif index == 19:
            self._action.closed_by = combo.get_active()
            _new_text = Configuration.RTK_USERS[combo.get_active() - 1]
            (_model,
             _row) = _selection.get_selected()
            _model.set_value(_row, 8, _new_text)

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):     # pylint: disable=R0912
        """
        Method to respond to gtk.Entry() 'focus_out' signals.

        :param gtk.Entry entry: the gtk.Entry() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Entry() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """
# WARNING: Refactor _on_focus_out; current McCabe Complexity metric = 17.
        entry.handler_block(self._lst_handler_id[index])

        _selection = self._modulebook.listbook.tvwActionList.get_selection()
        (_model,
         _row) = _selection.get_selected()

        if index == 20:
            _new_text = Utilities.date_to_ordinal(entry.get_text())
            self._model.request_date = _new_text
            self._modulebook.update(index - 1, _new_text)
        elif index == 21:
            _new_text = entry.get_text()
            self._model.short_description = _new_text
            self._modulebook.update(index - 17, _new_text)
        elif index == 22:
            _new_text = entry.get_text(*entry.get_bounds())
            self._model.long_description = _new_text
            self._modulebook.update(index - 17, _new_text)
        elif index == 23:
            _new_text = entry.get_text(*entry.get_bounds())
            self._model.remarks = _new_text
            self._modulebook.update(index - 15, _new_text)
        elif index == 24:
            _new_text = entry.get_text()
            self._model.test = _new_text
            self._modulebook.update(index - 14, _new_text)
        elif index == 25:
            _new_text = entry.get_text()
            self._model.test_case = _new_text
            self._modulebook.update(index - 14, _new_text)
        elif index == 16:
            _new_text = float(entry.get_text())
            self._model.execution_time = _new_text
            self._modulebook.update(index - 14, _new_text)
        elif index == 27:
            _new_text = entry.get_text(*entry.get_bounds())
            self._model.analysis = _new_text
            self._modulebook.update(index + 3, _new_text)
        elif index == 28:
            _new_text = entry.get_text(*entry.get_bounds())
            self._action.prescribed_action = _new_text
            _model.set_value(_row, 1, _new_text)
        elif index == 29:
            _new_text = entry.get_text(*entry.get_bounds())
            self._action.action_taken = _new_text
            _model.set_value(_row, 2, _new_text)
        elif index == 30:
            _new_text = entry.get_text()
            self._action.due_date = Utilities.date_to_ordinal(_new_text)
            _model.set_value(_row, 4, _new_text)
        elif index == 31:
            _new_text = entry.get_text()
            self._action.approved_date = Utilities.date_to_ordinal(_new_text)
            _model.set_value(_row, 8, _new_text)
        elif index == 32:
            _new_text = entry.get_text()
            self._action.closed_date = Utilities.date_to_ordinal(_new_text)
            _model.set_value(_row, 9, _new_text)
        elif index == 33:
            _new_text = entry.get_text()
            self._model.review_date = Utilities.date_to_ordinal(_new_text)
            self._modulebook.update(index - 11, _new_text)
        elif index == 34:
            _new_text = entry.get_text()
            self._model.approve_date = Utilities.date_to_ordinal(_new_text)
            self._modulebook.update(index - 9, _new_text)
        elif index == 35:
            _new_text = entry.get_text()
            self._model.close_date = Utilities.date_to_ordinal(_new_text)
            self._modulebook.update(index - 7, _new_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_relevancy_changed(self, combo, index):
        """
        Method to enable the next relevancy question.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called this method.
        :param int index: the index of the relevancy question being answered.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._model.lstRelevant[index - 100] = combo.get_active() - 1

        self._load_chargeability_page()

        return False

    def _on_chargeability_changed(self, combo, index):
        """
        Method to enable the next chargeability question.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called this method.
        :param int index: the index of the relevancy question being answered.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._model.lstChargeable[index] = combo.get_active() - 1

        self._load_chargeability_page()

        return False
