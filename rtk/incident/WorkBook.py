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
try:
    import gobject
except ImportError:
    sys.exit(1)

# Import other RTK modules.
try:
    import Configuration as _conf
    import Utilities as _util
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.Utilities as _util
    import rtk.gui.gtk.Widgets as _widg
from Assistants import AddIncident, AddComponents, FilterIncident, ImportIncident

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
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

    def __init__(self, workview, modulebook):
        """
        Initializes the Work Book view for the Incident package.

        :param workview: the :py:class:`rtk.gui.gtk.mwi.WorkView` container to
                         insert this Work Book into.
        :param modulebook: the :py:class:`rtk.incident.ModuleBook` to
                           associate with this Work Book.
        """

        gtk.VBox.__init__(self)

        # Initialize private dict attributes.
        self._dic_hardware = {}
        self._dic_software = {}

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._workview = workview
        self._modulebook = modulebook
        self._model = None
        self._component = None
        self._action = None

        # Initialize public scalar attributes.
        self.dtcIncident = modulebook.dtcIncident
        self.dtcComponents = modulebook.dtcComponents

        # Dataset class Work Book toolbar widgets.
        self.chkAllRevisions = _widg.make_check_button(_(u"Include incidents "
                                                         u"from all "
                                                         u"revisions"))

        # Create the Program Incident page widgets.
        self.btnAddComponent = _widg.make_button(width=35, image='add')
        self.btnRemoveComponent = _widg.make_button(width=35, image='remove')
        self.btnSaveComponents = _widg.make_button(width=35, image='save')

        self.chkAccepted = _widg.make_check_button(label=_(u"Accepted"))
        self.chkReviewed = _widg.make_check_button(label=_(u"Reviewed"))

        self.cmbHardware = _widg.make_combo(simple=False)
        self.cmbSoftware = _widg.make_combo(simple=False)
        self.cmbCategory = _widg.make_combo()
        self.cmbType = _widg.make_combo()
        self.cmbStatus = _widg.make_combo()
        self.cmbCriticality = _widg.make_combo()
        self.cmbLifeCycle = _widg.make_combo()
        self.cmbRequestBy = _widg.make_combo()

        self.tvwComponentList = gtk.TreeView()

        self.txtID = _widg.make_entry(width=100, editable=False)
        self.txtRequestDate = _widg.make_entry(width=100, editable=False)
        self.txtAge = _widg.make_entry(width=100, editable=False)
        self.txtShortDescription = _widg.make_entry(width=550)

        self.txtLongDescription = _widg.make_text_view(width=550, height=200)
        self.txtRemarks = _widg.make_text_view(width=550, height=200)

        # Create the Chargeability page widgets.
        self.cmbChargeable1 = _widg.make_combo(width=75)
        self.cmbChargeable2 = _widg.make_combo(width=75)
        self.cmbChargeable3 = _widg.make_combo(width=75)
        self.cmbChargeable4 = _widg.make_combo(width=75)
        self.cmbChargeable5 = _widg.make_combo(width=75)
        self.cmbRelevant1 = _widg.make_combo(width=75)
        self.cmbRelevant2 = _widg.make_combo(width=75)
        self.cmbRelevant3 = _widg.make_combo(width=75)
        self.cmbRelevant4 = _widg.make_combo(width=75)
        self.cmbRelevant5 = _widg.make_combo(width=75)
        self.cmbRelevant6 = _widg.make_combo(width=75)
        self.cmbRelevant7 = _widg.make_combo(width=75)
        self.cmbRelevant8 = _widg.make_combo(width=75)
        self.cmbRelevant9 = _widg.make_combo(width=75)
        self.cmbRelevant10 = _widg.make_combo(width=75)
        self.cmbRelevant11 = _widg.make_combo(width=75)
        self.cmbRelevant12 = _widg.make_combo(width=75)
        self.cmbRelevant13 = _widg.make_combo(width=75)
        self.cmbRelevant14 = _widg.make_combo(width=75)
        self.cmbRelevant15 = _widg.make_combo(width=75)
        self.cmbRelevant16 = _widg.make_combo(width=75)
        self.cmbRelevant17 = _widg.make_combo(width=75)
        self.cmbRelevant18 = _widg.make_combo(width=75)

        self.lblChargeable1 = _widg.make_label(_(u"1. This failure occurred "
                                                 u"on or was caused by "
                                                 u"equipment outside the "
                                                 u"scope of this test plan."),
                                               width=-1, height=-1, wrap=True)
        self.lblChargeable2 = _widg.make_label(_(u"2. This failure occurred "
                                                 u"on or was caused by "
                                                 u"customer furnished "
                                                 u"equipment."), width=-1,
                                               height=-1, wrap=True)
        self.lblChargeable3 = _widg.make_label(_(u"3. This failure occurred "
                                                 u"on or was caused by "
                                                 u"supplier furnished "
                                                 u"equipment."), width=-1,
                                               height=-1, wrap=True)
        self.lblChargeable4 = _widg.make_label(_(u"4. This failure of "
                                                 u"supplier furnished "
                                                 u"equipment was the caused "
                                                 u"by system-integration "
                                                 u"errors."), width=-1,
                                               height=-1, wrap=True)
        self.lblChargeable5 = _widg.make_label(_(u"5. This supplier provided "
                                                 u"equipment did or would "
                                                 u"have passed normal receipt "
                                                 u"inspection and testing."),
                                               width=-1, height=-1, wrap=True)
        self.lblChargeable = _widg.make_label("", width=-1, height=-1,
                                              wrap=True)

        self.lblRelevant1 = _widg.make_label(_(u"1. This failure is an early "
                                               u"life failure."), width=-1,
                                             height=-1, wrap=True)
        self.lblRelevant2 = _widg.make_label(_(u"2. This failure was due to "
                                               u"an operator error such that "
                                               u"the error could be expected "
                                               u"during normal operations."),
                                             width=-1, height=-1, wrap=True)
        self.lblRelevant3 = _widg.make_label(_(u"3. This failure was due to "
                                               u"test setup errors."),
                                             width=-1, height=-1, wrap=True)
        self.lblRelevant4 = _widg.make_label(_(u"4. This is a consumable item "
                                               u"that has exceeded its "
                                               u"expected life."), width=-1,
                                             height=-1, wrap=True)
        self.lblRelevant5 = _widg.make_label(_(u"5. Life data indicates an "
                                               u"unacceptable percentage of "
                                               u"these items will not reach "
                                               u"the specified life."),
                                             width=-1, height=-1, wrap=True)
        self.lblRelevant6 = _widg.make_label(_(u"6. The parts contributing to "
                                               u"the failure are "
                                               u"representative of design "
                                               u"intent."), width=-1,
                                             height=-1, wrap=True)
        self.lblRelevant7 = _widg.make_label(_(u"7. The failure would or "
                                               u"could have occurred for the "
                                               u"new design if the parts were "
                                               u"representative."), width=-1,
                                             height=-1, wrap=True)
        self.lblRelevant8 = _widg.make_label(_(u"8. The parts contributing to "
                                               u"the failure are conforming "
                                               u"to design specifications."),
                                             width=-1, height=-1, wrap=True)
        self.lblRelevant9 = _widg.make_label(_(u"9. The failure would or "
                                               u"could have occurred if the "
                                               u"parts were conforming."),
                                             width=-1, height=-1, wrap=True)
        self.lblRelevant10 = _widg.make_label(_(u"10. The parts were made "
                                                u"using production tooling "
                                                u"and a production process."),
                                              width=-1, height=-1, wrap=True)
        self.lblRelevant11 = _widg.make_label(_(u"11. A production process "
                                                u"could have generated the "
                                                u"nonconformance."), width=-1,
                                              height=-1, wrap=True)
        self.lblRelevant12 = _widg.make_label(_(u"12. The parts would or "
                                                u"could have passed normal "
                                                u"production inspection and "
                                                u"testing."), width=-1,
                                              height=-1, wrap=True)
        self.lblRelevant13 = _widg.make_label(_(u"13. Performance was "
                                                u"originally acceptable and "
                                                u"is no longer (i.e., "
                                                u"degradation has occurred)."),
                                              width=-1, height=-1, wrap=True)
        self.lblRelevant14 = _widg.make_label(_(u"14. We can measure the "
                                                u"performance issue and "
                                                u"compare to requirements."),
                                              width=-1, height=-1, wrap=True)
        self.lblRelevant15 = _widg.make_label(_(u"15. Performance is within "
                                                u"requirements."), width=-1,
                                              height=-1, wrap=True)
        self.lblRelevant16 = _widg.make_label(_(u"16. There exist acceptance "
                                                u"standards to which "
                                                u"performance can be "
                                                u"compared."), width=-1,
                                              height=-1, wrap=True)
        self.lblRelevant17 = _widg.make_label(_(u"17. By existing standards "
                                                u"we can accept the issue."),
                                              width=-1, height=-1, wrap=True)
        self.lblRelevant18 = _widg.make_label(_(u"18. We can accept this "
                                                u"issue."), width=-1,
                                              height=-1, wrap=True)
        self.lblRelevant = _widg.make_label("", width=-1, height=-1, wrap=True)

        # Create the Incident Analysis page widgets.
        self.btnReviewDate = _widg.make_button(height=25, width=25,
                                               label="...", image='calendar')
        self.btnApproveDate = _widg.make_button(height=25, width=25,
                                                label="...", image='calendar')
        self.btnClosureDate = _widg.make_button(height=25, width=25,
                                                label="...", image='calendar')

        self.cmbDetectionMethod = _widg.make_combo()
        self.cmbReviewBy = _widg.make_combo()
        self.cmbApproveBy = _widg.make_combo()
        self.cmbCloseBy = _widg.make_combo()

        self.txtTest = _widg.make_entry()
        self.txtTestCase = _widg.make_entry()
        self.txtExecutionTime = _widg.make_entry(width=100)
        self.txtAnalysis = _widg.make_text_view(width=550, height=200)
        self.txtReviewDate = _widg.make_entry(width=100, editable=False)
        self.txtApproveDate = _widg.make_entry(width=100, editable=False)
        self.txtCloseDate = _widg.make_entry(width=100, editable=False)

        # Create the Incident Actions page widgets.
        self.btnAddAction = _widg.make_button(width=35, image='add')
        self.btnSaveAction = _widg.make_button(width=35, image='save')
        self.btnActionDueDate = _widg.make_button(height=25, width=25,
                                                  label="...",
                                                  image='calendar')
        self.btnActionApproveDate = _widg.make_button(height=25, width=25,
                                                      label="...",
                                                      image='calendar')
        self.btnActionCloseDate = _widg.make_button(height=25, width=25,
                                                    label="...",
                                                    image='calendar')

        self.cmbActionOwner = _widg.make_combo()
        self.cmbActionApproveBy = _widg.make_combo()
        self.cmbActionCloseBy = _widg.make_combo()
        self.cmbActionStatus = _widg.make_combo()

        self.tvwActionList = gtk.TreeView()

        self.txtPrescribedAction = _widg.make_text_view(width=550, height=200)
        self.txtActionTaken = _widg.make_text_view(width=550, height=200)
        self.txtActionDueDate = _widg.make_entry(width=100, editable=False)
        self.txtActionApproveDate = _widg.make_entry(width=100, editable=False)
        self.txtActionCloseDate = _widg.make_entry(width=100, editable=False)

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
        _image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 0)
        _button.set_tooltip_text(_(u"Add a new incident to the open RTK "
                                   u"Program database."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Save incident button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.set_name('Save')
        _button.connect('clicked', self._on_button_clicked, 5)
        _button.set_tooltip_text(_(u"Saves the currently selected incident "
                                   u"to the open RTK Program database."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Create a filter button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/filter.png')
        _button.set_icon_widget(_image)
        _button.set_name('Filter')
        _button.connect('clicked', self._on_button_clicked, 6)
        _button.set_tooltip_text(_(u"Launches the Program Incident filter "
                                   u"assistant."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Create an import button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/db-import.png')
        _button.set_icon_widget(_image)
        _button.set_name('Import')
        _button.connect('clicked', self._on_button_clicked, 7)
        _button.set_tooltip_text(_(u"Launches the Program Incident import "
                                   u"assistant."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Create an export button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/db-export.png')
        _button.set_icon_widget(_image)
        _button.set_name('Export')
        _button.connect('clicked', self._on_button_clicked, 8)
        _button.set_tooltip_text(_(u"Launches the Program Incident export "
                                   u"assistant."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Create a data set creation button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/wizard.png')
        _button.set_icon_widget(_image)
        _button.set_name('Data Set')
        _button.connect('clicked', self._on_button_clicked, 9)
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
        self.chkAllRevisions.connect('toggled', self._on_check_toggled, 22)

        _toolbar.show()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Incident class gtk.Notebook().
        """

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
        _hpaned = gtk.HPaned()
        _vpaned = gtk.VPaned()

        # Build quadrant 1 (upper left).
        _fixed1 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed1)

        _frame = _widg.make_frame(label=_(u"Incident Details"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, False, True)

        # Build quadrant 2 (lower left).
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        _hbox = gtk.HBox()
        _hbox.pack_start(_bbox, False, False)

        _bbox.pack_start(self.btnAddComponent, False, False)
        _bbox.pack_start(self.btnRemoveComponent, False, False)
        _bbox.pack_start(self.btnSaveComponents, False, False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwComponentList)

        _frame = _widg.make_frame(label=_(u"Component Information"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)
        _vpaned.pack2(_hbox, False, True)

        self.btnAddComponent.set_tooltip_text(_(u"Adds an affected component "
                                                u"to the selected incident."))
        self.btnRemoveComponent.set_tooltip_text(_(u"Removes the selected "
                                                   u"component from the list "
                                                   u"of affected components "
                                                   u"for the selected "
                                                   u"incident."))
        self.btnSaveComponents.set_tooltip_text(_(u"Saves the affected "
                                                  u"component list to the "
                                                  u"open RTK Program "
                                                  u"database."))

        self.btnAddComponent.connect('clicked', self._on_button_clicked, 2)
        self.btnRemoveComponent.connect('clicked', self._on_button_clicked, 3)
        self.btnSaveComponents.connect('clicked', self._on_button_clicked, 4)

        _hpaned.pack1(_vpaned, False, True)

        # Build quadrant 3 (upper right).
        _fixed3 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed3)

        _frame = _widg.make_frame(label=_(u"Incident Descriptions"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hpaned.pack2(_frame, False, True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display analysis input information. #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.ComboBox() widgets in quadrant #1.
        self.cmbCategory.append_text("")
        for i in range(len(_conf.RTK_INCIDENT_CATEGORY)):
            self.cmbCategory.append_text(_conf.RTK_INCIDENT_CATEGORY[i])

        self.cmbType.append_text("")
        for i in range(len(_conf.RTK_INCIDENT_TYPE)):
            self.cmbType.append_text(_conf.RTK_INCIDENT_TYPE[i])

        self.cmbStatus.append_text("")
        for i in range(len(_conf.RTK_INCIDENT_STATUS)):
            self.cmbStatus.append_text(_conf.RTK_INCIDENT_STATUS[i])

        self.cmbCriticality.append_text("")
        for i in range(len(_conf.RTK_INCIDENT_CRITICALITY)):
            self.cmbCriticality.append_text(_conf.RTK_INCIDENT_CRITICALITY[i])

        self.cmbLifeCycle.append_text("")
        for i in range(len(_conf.RTK_LIFECYCLE)):
            self.cmbLifeCycle.append_text(_conf.RTK_LIFECYCLE[i])

        self.cmbRequestBy.append_text("")
        for i in range(len(_conf.RTK_USERS)):
            self.cmbRequestBy.append_text(_conf.RTK_USERS[i])

        # Set the labels on the left half.
        _labels = [_(u"Incident ID:"), _(u"Incident Category:"),
                   _(u"Incident Type:"), _(u"Life Cycle:"),
                   _(u"Incident Criticality:"), _(u"Affected Assembly:"),
                   _(u"Affected Software:")]
        (_x_pos11, _y_pos11) = _widg.make_labels(_labels, _fixed1, 5, 5)
        _x_pos11 += 30

        # Set the labels on the right half.
        _labels = [_(u"Reported By:"), _(u"Date Opened:"), _(u"Incident Age:"),
                   _(u"Incident Status:")]
        (_x_pos12, _y_pos12) = _widg.make_labels(_labels, _fixed1,
                                                 _x_pos11 + 215, 35)
        _x_pos12 += 390

        # Set the tooltips for the widgets in quadrant #1.
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

        # Place the quadrant #1 widgets.
        _fixed1.put(self.txtID, _x_pos11, _y_pos11[0])
        _fixed1.put(self.chkAccepted, _x_pos11 + 110, _y_pos11[0])
        _fixed1.put(self.chkReviewed, _x_pos11 + 220, _y_pos11[0])
        _fixed1.put(self.cmbCategory, _x_pos11, _y_pos11[1])
        _fixed1.put(self.cmbType, _x_pos11, _y_pos11[2])
        _fixed1.put(self.cmbLifeCycle, _x_pos11, _y_pos11[3])
        _fixed1.put(self.cmbCriticality, _x_pos11, _y_pos11[4])
        _fixed1.put(self.cmbHardware, _x_pos11, _y_pos11[5])
        _fixed1.put(self.cmbSoftware, _x_pos11, _y_pos11[6])

        _fixed1.put(self.cmbRequestBy, _x_pos12, _y_pos12[0])
        _fixed1.put(self.txtRequestDate, _x_pos12, _y_pos12[1])
        _fixed1.put(self.txtAge, _x_pos12, _y_pos12[2])
        _fixed1.put(self.cmbStatus, _x_pos12, _y_pos12[3])

        _fixed1.show_all()

        # Connect the quadrant #1 widgets' signals to callback functions.
        self._lst_handler_id.append(
            self.chkAccepted.connect('toggled', self._on_check_toggled, 0))
        self._lst_handler_id.append(
            self.chkReviewed.connect('toggled', self._on_check_toggled, 1))
        self._lst_handler_id.append(
            self.cmbCategory.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbCriticality.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.cmbStatus.connect('changed', self._on_combo_changed, 5))
        self._lst_handler_id.append(
            self.cmbHardware.connect('changed', self._on_combo_changed, 6))
        self._lst_handler_id.append(
            self.cmbSoftware.connect('changed', self._on_combo_changed, 7))
        self._lst_handler_id.append(
            self.cmbRequestBy.connect('changed', self._on_combo_changed, 8))
        self._lst_handler_id.append(
            self.cmbLifeCycle.connect('changed', self._on_combo_changed, 9))
        self._lst_handler_id.append(
            self.txtRequestDate.connect('focus-out-event',
                                        self._on_focus_out, 10))

        # Place the quadrant 2 (lower left) widgets.
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
        self.tvwComponentList.set_model(_model)

        _headings = [_(u"Component\nID"), _(u"Part\nNumber"),
                     _(u"Initial\nInstall"), _(u"Failure"), _(u"Suspension"),
                     _(u"OOT\nFailure"), _("CND/NFF"), _(u"Interval\nCensored"),
                     _(u"Use\nOperating\nTime"), _(u"Use\nCalendar\nTime"),
                     _(u"Time to\nFailure"), _(u"Age at\nFailure")]
        for _index, _heading in enumerate(_headings):
            _column = gtk.TreeViewColumn()

            if i in [0, 1, 10, 11]:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _cell.set_property('background', 'light gray')
                _cell.set_property('foreground', 'black')
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=_index)
            else:
                _cell = gtk.CellRendererToggle()
                _cell.set_property('activatable', 1)
                _cell.connect('toggled', self._on_cellrenderer_toggle, None,
                              _index, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, active=_index)

            _label = _widg.make_column_heading(_heading)
            _column.set_widget(_label)
            _column.set_clickable(True)
            _column.set_resizable(True)
            _column.set_sort_column_id(_index)
            if i == 0:
                _column.set_visible(False)

            self.tvwComponentList.append_column(_column)

        # Connect the quadrant #2 widgets to callback functions.
        self.tvwComponentList.connect('cursor_changed',
                                      self._on_component_select, None, None)
        self.tvwComponentList.connect('row_activated',
                                      self._on_component_select)

        # Set the tooltips for the widgets in quadrant #3.
        self.txtShortDescription.set_tooltip_text(_(u"Short problem "
                                                    u"description."))

        # Place the quadrant #3 (upper right) widgets.
        _label = _widg.make_label(_(u"Brief Problem Description:"),
                                  width=225)
        _fixed3.put(_label, 5, 5)
        _fixed3.put(self.txtShortDescription, 5, 35)

        _label = _widg.make_label(_(u"Detailed Problem Description:"),
                                  width=225)
        _fixed3.put(_label, 5, 65)
        _fixed3.put(self.txtLongDescription, 5, 100)

        _label = _widg.make_label(_(u"Remarks:"))
        _fixed3.put(_label, 5, 305)
        _fixed3.put(self.txtRemarks, 5, 330)

        # Connect the quadrant #3 widgets' signals to callback functions.
        self._lst_handler_id.append(
            self.txtShortDescription.connect('focus-out-event',
                                             self._on_focus_out, 11))
        _textbuffer = self.txtLongDescription.get_child().get_child().get_buffer()
        self._lst_handler_id.append(_textbuffer.connect('changed',
                                                        self._on_focus_out,
                                                        _textbuffer, 12))
        _textbuffer = self.txtRemarks.get_child().get_child().get_buffer()
        self._lst_handler_id.append(_textbuffer.connect('changed',
                                                        self._on_focus_out,
                                                        _textbuffer, 13))

        _fixed3.show_all()

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

        _frame = _widg.make_frame(label=_(u"Incident Relevancy"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_start(_frame, expand=True)

        _fixed2 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed2)

        _frame = _widg.make_frame(label=_(u"Incident Chargeability"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, expand=True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display the chargeability analysis. #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.ComboBox().
        _results = [[_(u"No")], [_(u"Yes")]]
        _widg.load_combo(self.cmbRelevant1, _results)
        _widg.load_combo(self.cmbRelevant2, _results)
        _widg.load_combo(self.cmbRelevant3, _results)
        _widg.load_combo(self.cmbRelevant4, _results)
        _widg.load_combo(self.cmbRelevant5, _results)
        _widg.load_combo(self.cmbRelevant6, _results)
        _widg.load_combo(self.cmbRelevant7, _results)
        _widg.load_combo(self.cmbRelevant8, _results)
        _widg.load_combo(self.cmbRelevant9, _results)
        _widg.load_combo(self.cmbRelevant10, _results)
        _widg.load_combo(self.cmbRelevant11, _results)
        _widg.load_combo(self.cmbRelevant12, _results)
        _widg.load_combo(self.cmbRelevant13, _results)
        _widg.load_combo(self.cmbRelevant14, _results)
        _widg.load_combo(self.cmbRelevant15, _results)
        _widg.load_combo(self.cmbRelevant16, _results)
        _widg.load_combo(self.cmbRelevant17, _results)
        _widg.load_combo(self.cmbRelevant18, _results)
        _widg.load_combo(self.cmbChargeable1, _results)
        _widg.load_combo(self.cmbChargeable2, _results)
        _widg.load_combo(self.cmbChargeable3, _results)
        _widg.load_combo(self.cmbChargeable4, _results)
        _widg.load_combo(self.cmbChargeable5, _results)

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
        _frame = _widg.make_frame(label=_(u"Software Incident"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_fixed1)
        _hbox2.pack_start(_frame, expand=False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self.txtAnalysis)

        _frame = _widg.make_frame(label=_(u"Incident Analysis"))
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
        for i in range(len(_conf.RTK_DETECTION_METHODS)):
            self.cmbDetectionMethod.append_text(_conf.RTK_DETECTION_METHODS[i])

        # Load the gtk.ComboBox() widgets in quadrant #3.
        self.cmbReviewBy.append_text("")
        self.cmbApproveBy.append_text("")
        self.cmbCloseBy.append_text("")
        for i in range(len(_conf.RTK_USERS)):
            self.cmbReviewBy.append_text(_conf.RTK_USERS[i])
            self.cmbApproveBy.append_text(_conf.RTK_USERS[i])
            self.cmbCloseBy.append_text(_conf.RTK_USERS[i])

        # Set the tooltips for the widgets in quadrant #1.
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

        # Place the quadrant #1 widgets.
        _labels = [_(u"Detection Method:"), _(u"Found in Test:"),
                   _(u"Found in Test Case:"), _(u"Execution Time:")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed1, 5, 5)
        _x_pos += 30

        _fixed1.put(self.cmbDetectionMethod, _x_pos, _y_pos[0])
        _fixed1.put(self.txtTest, _x_pos, _y_pos[1] + 5)
        _fixed1.put(self.txtTestCase, _x_pos, _y_pos[2] + 5)
        _fixed1.put(self.txtExecutionTime, _x_pos, _y_pos[3] + 5)

        self._lst_handler_id.append(
            self.cmbDetectionMethod.connect('changed',
                                            self._on_combo_changed, 14))

        self._lst_handler_id.append(
            self.txtTest.connect('focus-out-event', self._on_focus_out, 15))
        self._lst_handler_id.append(
            self.txtTestCase.connect('focus-out-event',
                                     self._on_focus_out, 16))
        self._lst_handler_id.append(
            self.txtExecutionTime.connect('focus-out-event',
                                          self._on_focus_out, 17))

        # Set the tooltips for the widgets in quedrant #3.
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

        # Place the quadrant #3 widgets.
        _labels = [_(u"Reviewed By:"), _(u"Date Reviewed:"),
                   _(u"Approved By:"), _(u"Date Approved:"), _(u"Closed By:"),
                   _(u"Date Closed:")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed2, 5, 5)
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

        # Connect the quadrant #1 widgets' signals to callback functions.
        self.btnReviewDate.connect('button-release-event', _util.date_select,
                                   self.txtReviewDate)
        self.btnApproveDate.connect('button-release-event', _util.date_select,
                                    self.txtApproveDate)
        self.btnClosureDate.connect('button-release-event', _util.date_select,
                                    self.txtCloseDate)
        self._lst_handler_id.append(
            self.cmbReviewBy.connect('changed', self._on_combo_changed, 18))
        self._lst_handler_id.append(
            self.cmbApproveBy.connect('changed', self._on_combo_changed, 19))
        self._lst_handler_id.append(
            self.cmbCloseBy.connect('changed', self._on_combo_changed, 20))
        _textbuffer = self.txtAnalysis.get_child().get_child().get_buffer()
        self._lst_handler_id.append(_textbuffer.connect('changed',
                                                        self._on_focus_out,
                                                        _textbuffer, 21))

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

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwActionList)

        _hbox2 = gtk.HBox()

        _hpaned.pack1(_scrollwindow, True, False)
        _hpaned.pack2(_hbox2, True, True)

        _vbox = gtk.VBox()
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self.txtPrescribedAction)

        _frame = _widg.make_frame(_(u"Prescribed Action"))
        _frame.add(_scrollwindow)

        _vbox.pack_start(_frame)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self.txtActionTaken)

        _frame = _widg.make_frame(_(u"Action Taken"))
        _frame.add(_scrollwindow)

        _vbox.pack_end(_frame)

        _hbox2.pack_start(_vbox, True, True)
        _hbox2.pack_end(_fixed, False, False)

        _bbox.pack_start(self.btnAddAction, False, False)
        _bbox.pack_start(self.btnSaveAction, False, False)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display Incident action information.#
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Set the tooltips for the widgets in quadrant #1 (left-most).
        self.btnAddAction.set_tooltip_text(_(u"Adds an action to the selected "
                                             u"incident."))
        self.btnSaveAction.set_tooltip_text(_(u"Saves the selected action."))

        # Connect the widgets in quadrant #1 to callback methods.
        self.btnAddAction.connect('clicked', self._on_button_clicked, 1)
        self.btnSaveAction.connect('clicked', self._on_button_clicked, 10)

        # Create the Action List in quadrant #2 (left middle).
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING)
        self.tvwActionList.set_model(_model)

        _headings = [_(u"Action\nID"), _(u"Prescribed\nAction"),
                     _(u"Action\nTaken"), _(u"Action\nOwner"), _(u"Due Date"),
                     _(u"Action\nStatus"), _("Approved By"),
                     _(u"Approval\nDate"), _(u"Closed By"),
                     _(u"Closure\nDate")]
        for _index, _heading in enumerate(_headings):
            _column = gtk.TreeViewColumn()

            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _cell.set_property('background', 'light gray')
            _cell.set_property('foreground', 'black')
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=_index)

            _label = _widg.make_column_heading(_heading)
            _column.set_widget(_label)
            _column.set_clickable(True)
            _column.set_resizable(True)
            _column.set_sort_column_id(_index)
            if _index in [1, 2]:
                _column.set_visible(False)

            self.tvwActionList.append_column(_column)

        # Connect the widgets in quadrant #2 to callback methods.
        self.tvwActionList.connect('cursor_changed',
                                   self._on_action_select, None, None)
        self.tvwActionList.connect('row_activated', self._on_action_select)

        # Set the tooltips for the widgets in quadrant #3 (right middle).
        self.txtPrescribedAction.set_tooltip_text(_(u"Displays the prescribed "
                                                    u"action."))
        self.txtActionTaken.set_tooltip_text(_(u"Displays the actual action "
                                               u"that was taken.  This may "
                                               u"differ from the prescribed "
                                               u"action."))

        # Connect the widgets in quadrant #3 to callback methods.
        _buffer = self.txtPrescribedAction.get_child().get_child().get_buffer()
        self._lst_handler_id.append(_buffer.connect('changed',
                                                    self._on_focus_out,
                                                    _buffer, 22))
        _buffer = self.txtActionTaken.get_child().get_child().get_buffer()
        self._lst_handler_id.append(_buffer.connect('changed',
                                                    self._on_focus_out,
                                                    _buffer, 23))

        # Load the gtk.ComboBox() widgets in quadrant #4 (right-most).
        self.cmbActionOwner.append_text("")
        for i in range(len(_conf.RTK_USERS)):
            self.cmbActionOwner.append_text(_conf.RTK_USERS[i])

        self.cmbActionApproveBy.append_text("")
        for i in range(len(_conf.RTK_USERS)):
            self.cmbActionApproveBy.append_text(_conf.RTK_USERS[i])

        self.cmbActionCloseBy.append_text("")
        for i in range(len(_conf.RTK_USERS)):
            self.cmbActionCloseBy.append_text(_conf.RTK_USERS[i])

        self.cmbActionStatus.append_text("")
        for i in [0, 2, 6, 7, 8, 9]:
            self.cmbActionStatus.append_text(_conf.RTK_INCIDENT_STATUS[i])

        # Set the labels for quadrant #4.
        _labels = [_(u"Action Owner:"), _(u"Due Date:"), _(u"Status:"),
                   _(u"Approved By:"), _(u"Approval Date:"), _(u"Closed By:"),
                   _(u"Closure Date:")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5, 35)
        _x_pos += 30

        # Set the tooltips for the widgets in quadrant #4.
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

        # Connect widgets in quadrant #4 to callback methods.
        self.btnActionDueDate.connect('button-release-event',
                                      _util.date_select,
                                      self.txtActionDueDate)
        self.btnActionApproveDate.connect('button-release-event',
                                          _util.date_select,
                                          self.txtActionApproveDate)
        self.btnActionCloseDate.connect('button-release-event',
                                        _util.date_select,
                                        self.txtActionCloseDate)

        self._lst_handler_id.append(
            self.cmbActionOwner.connect('changed', self._on_combo_changed, 24))
        self._lst_handler_id.append(
            self.txtActionDueDate.connect('changed', self._on_focus_out,
                                          self.txtActionDueDate, 25))
        self._lst_handler_id.append(
            self.cmbActionStatus.connect('changed',
                                         self._on_combo_changed, 26))
        self._lst_handler_id.append(
            self.cmbActionApproveBy.connect('changed',
                                            self._on_combo_changed, 27))
        self._lst_handler_id.append(
            self.txtActionApproveDate.connect('changed', self._on_focus_out,
                                              self.txtActionApproveDate, 28))
        self._lst_handler_id.append(
            self.cmbActionCloseBy.connect('changed',
                                          self._on_combo_changed, 29))
        self._lst_handler_id.append(
            self.txtActionCloseDate.connect('changed', self._on_focus_out,
                                            self.txtActionCloseDate, 30))

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Incident\nActions") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays actions related to the selected "
                                  u"incident."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Incident class gtk.Notebook().

        :param model: the :py:class:`rtk.incident.Incident.Model` whose
                      attributes will be loaded into the display widgets.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        self._model = model

        self.cmbHardware.handler_block(self._lst_handler_id[6])
        self.cmbSoftware.handler_block(self._lst_handler_id[7])

        _widg.load_combo(self.cmbHardware, _conf.RTK_HARDWARE_LIST,
                         simple=False)
        for i in range(len(_conf.RTK_HARDWARE_LIST)):
            self._dic_hardware[_conf.RTK_HARDWARE_LIST[i][1]] = i + 1

        _widg.load_combo(self.cmbSoftware, _conf.RTK_SOFTWARE_LIST,
                         simple=False)
        for i in range(len(_conf.RTK_SOFTWARE_LIST)):
            self._dic_software[_conf.RTK_SOFTWARE_LIST[i][1]] = i + 1

        self.cmbHardware.handler_unblock(self._lst_handler_id[6])
        self.cmbSoftware.handler_unblock(self._lst_handler_id[7])

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

        _date = _util.ordinal_to_date(model.request_date)
        self.txtRequestDate.set_text(str(_date))
        self.cmbStatus.set_active(model.status)
        self.txtAge.set_text(str(model.incident_age))

        self.txtShortDescription.set_text(_util.none_to_string(
            model.short_description))
        _buffer = self.txtLongDescription.get_child().get_child().get_buffer()
        _buffer.set_text(_util.none_to_string(model.detail_description))
        _buffer = self.txtRemarks.get_child().get_child().get_buffer()
        _buffer.set_text(_util.none_to_string(model.remarks))

        # Load the incident analysis page.
        #self.cmbDetectionMethod.set_active(self._model.detection_method)
        self.txtTest.set_text(_util.none_to_string(model.test))
        self.txtTestCase.set_text(_util.none_to_string(model.test_case))
        self.txtExecutionTime.set_text(str(model.execution_time))

        _buffer = self.txtAnalysis.get_child().get_child().get_buffer()
        _buffer.set_text(_util.none_to_string(model.analysis))

        self.cmbReviewBy.set_active(model.review_by)
        _date = _util.ordinal_to_date(model.review_date)
        self.txtReviewDate.set_text(str(_date))

        self.cmbApproveBy.set_active(model.approve_by)
        _date = _util.ordinal_to_date(model.approve_date)
        self.txtApproveDate.set_text(str(_date))

        self.cmbCloseBy.set_active(model.close_by)
        _date = _util.ordinal_to_date(model.close_date)
        self.txtCloseDate.set_text(str(_date))

        self.load_component_list()
        if self._component is not None:
            self._load_chargeability_page()
        self._load_actions_list()

        return False

    def load_component_list(self):
        """
        Method to load the component list for the selected incident.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _model = self.tvwComponentList.get_model()
        _model.clear()

        _results = self._modulebook.request_load_components(self._model.incident_id)

        try:
            _n_components = len(_results)
        except TypeError:
            _n_components = 0

        for i in range(_n_components):
            _data = (_results[i][1], _results[i][45], _results[i][7],
                     _results[i][3], _results[i][4], _results[i][6],
                     _results[i][5], _results[i][8], _results[i][9],
                     _results[i][10], _results[i][11], _results[i][12])
            _model.append(_data)

        _row = _model.get_iter_root()
        self.tvwComponentList.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.tvwComponentList.get_column(0)
            self.tvwComponentList.row_activated(_path, _column)

        return False

    def _load_chargeability_page(self):
        """
        Method to load the Incident chargeability page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        # Parse the relevancy questions.                                    #
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        _visible = [True, False, False, False, False, False, False, False,
                    False, False, False, False, False, False, False, False,
                    False, False]

        # Question #1.
        if self._component.lstRelevant[0] == 0:     # Goto 2.
            _visible[1] = True
        elif self._component.lstRelevant[0] == 1:   # Stop.
            _visible[1] = False
            self._component.lstRelevant[1:18] = [-1, -1, -1, -1, -1, -1, -1,
                                                 -1, -1, -1, -1, -1, -1, -1,
                                                 -1, -1, -1]
            self._component.relevant = 0
        else:
            _visible[1] = False

        # Question #2.
        if self._component.lstRelevant[1] == 0:     # Goto 3.
            _visible[2] = True
        elif self._component.lstRelevant[1] == 1:   # Stop.
            _visible[2] = False
            self._component.lstRelevant[2:18] = [-1, -1, -1, -1, -1, -1, -1,
                                                 -1, -1, -1, -1, -1, -1, -1,
                                                 -1, -1]
            self._component.relevant = 1
        else:
            _visible[2] = False

        # Question #3.
        if self._component.lstRelevant[2] == 0:     # Goto 4.
            _visible[3] = True
        elif self._component.lstRelevant[2] == 1:   # Stop.
            _visible[3] = False
            self._component.lstRelevant[3:18] = [-1, -1, -1, -1, -1, -1, -1,
                                                 -1, -1, -1, -1, -1, -1, -1,
                                                 -1]
            self._component.relevant = 0
        else:
            _visible[3] = False

        # Question #4.
        if self._component.lstRelevant[3] == 0:     # Goto 5.
            _visible[4] = True
        elif self._component.lstRelevant[3] == 1:   # Stop.
            _visible[4] = False
            self._component.lstRelevant[4:18] = [-1, -1, -1, -1, -1, -1, -1,
                                                 -1, -1, -1, -1, -1, -1, -1]
            self._component.relevant = 0
        else:
            _visible[4] = False

        # Question #5.
        if self._component.lstRelevant[4] == 0:     # Stop.
            _visible[5] = False
            self._component.lstRelevant[5:18] = [-1, -1, -1, -1, -1, -1, -1,
                                                 -1, -1, -1, -1, -1, -1]
            self._component.relevant = 0
        elif self._component.lstRelevant[4] == 1:   # Goto 6.
            _visible[5] = True
        else:
            _visible[5] = False

        # Question #6.
        if self._component.lstRelevant[5] == 0:     # Goto 7.
            _visible[6] = True
            _visible[7] = False
        elif self._component.lstRelevant[5] == 1:   # Goto 8.
            _visible[6] = False
            _visible[7] = True
        else:
            _visible[6] = False
            _visible[7] = False

        # Question #7.
        if self._component.lstRelevant[6] == 0:     # Stop.
            self._component.lstRelevant[7:18] = [-1, -1, -1, -1, -1, -1, -1,
                                                 -1, -1, -1, -1, -1, -1]
            self._component.relevant = 1
        elif self._component.lstRelevant[6] == 1:   # Stop.
            self._component.lstRelevant[7:18] = [-1, -1, -1, -1, -1, -1, -1,
                                                 -1, -1, -1, -1, -1, -1]
            self._component.relevant = 1

        # Question #8.
        if self._component.lstRelevant[7] == 0:     # Goto 9.
            _visible[8] = True
        elif self._component.lstRelevant[7] == 1:   # Stop.
            _visible[8] = False
            self._component.lstRelevant[8:18] = [-1, -1, -1, -1, -1, -1, -1,
                                                 -1, -1, -1, -1]
            self._component.relevant = 1
        else:
            _visible[8] = False

        # Question #9.
        if self._component.lstRelevant[8] == 0:     # Goto 10.
            _visible[9] = True
        elif self._component.lstRelevant[8] == 1:   # Stop.
            _visible[9] = False
            self._component.lstRelevant[9:18] = [-1, -1, -1, -1, -1, -1, -1,
                                                 -1, -1, -1, -1]
            self._component.relevant = 1
        else:
            _visible[9] = False

        # Question #10.
        if self._component.lstRelevant[9] == 0:     # Goto 11.
            _visible[10] = True
            _visible[11] = False
        elif self._component.lstRelevant[9] == 1:   # Goto 12.
            _visible[10] = False
            _visible[11] = True
        else:
            _visible[10] = False
            _visible[11] = False

        # Question #11.
        if self._component.lstRelevant[10] == 0:    # Stop.
            _visible[11] = False
            self._component.lstRelevant[11:18] = [-1, -1, -1, -1, -1, -1, -1,
                                                  -1, -1, -1]
            self._component.relevant = 0
        elif self._component.lstRelevant[10] == 1:  # Goto 12.
            _visible[11] = True

        # Question #12.
        if self._component.lstRelevant[11] == 0:    # Goto 13.
            _visible[12] = True
        elif self._component.lstRelevant[11] == 1:  # Stop.
            _visible[12] = False
            self._component.lstRelevant[12:18] = [-1, -1, -1, -1, -1, -1, -1,
                                                  -1, -1]
            self._component.relevant = 1

        # Question #13.
        if self._component.lstRelevant[12] == 0:    # Stop.
            _visible[13] = False
            self._component.lstRelevant[13:18] = [-1, -1, -1, -1, -1, -1, -1,
                                                  -1]
            self._component.relevant = 0
        elif self._component.lstRelevant[12] == 1:  # Goto 14.
            _visible[13] = True
        else:
            _visible[13] = False

        # Question #14.
        if self._component.lstRelevant[13] == 0:    # Goto 16.
            _visible[14] = False
            _visible[15] = True
            self._component.lstRelevant[14] = -1
        elif self._component.lstRelevant[13] == 1:  # Goto 15.
            _visible[14] = True
            _visible[15] = False
            self._component.lstRelevant[15] = -1
        else:
            _visible[14] = False
            _visible[15] = False

        # Question #15.
        if self._component.lstRelevant[14] == 0:    # Goto 18.
            _visible[17] = True
        elif self._component.lstRelevant[14] == 1:  # Stop.
            _visible[17] = False
            self._component.lstRelevant[17] = -1
            self._component.relevant = 0
        else:
            _visible[17] = False

        # Question #16.
        if self._component.lstRelevant[15] == 0:    # Goto 18.
            _visible[16] = False
            _visible[17] = True
            self._component.lstRelevant[16] = -1
        elif self._component.lstRelevant[15] == 1:  # Goto 17.
            _visible[16] = True
            _visible[17] = False

        # Question #17.
        if self._component.lstRelevant[16] == 0:    # Goto 18.
            _visible[17] = True
        elif self._component.lstRelevant[16] == 1:  # Stop.
            _visible[17] = False
            self._component.lstRelevant[17] = -1
            self._component.relevant = 0

        # Question #18.
        if self._component.lstRelevant[17] == 0:    # Stop.
            self._component.relevant = 1
        elif self._component.lstRelevant[17] == 1:  # Stop.
            self._component.relevant = 0

        if self.cmbRelevant10.get_active() == 2:
            _visible[10] = False

        if self._component.relevant == 0:
            self.lblRelevant.set_text(_(u"Failure is NOT relevant."))
        elif self._component.relevant == 1:
            self.lblRelevant.set_text(_(u"Failure IS relevant."))
        else:
            self.lblRelevant.set_text("")

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

        self.cmbRelevant1.set_active(self._component.lstRelevant[0] + 1)
        self.cmbRelevant2.set_active(self._component.lstRelevant[1] + 1)
        self.cmbRelevant3.set_active(self._component.lstRelevant[2] + 1)
        self.cmbRelevant4.set_active(self._component.lstRelevant[3] + 1)
        self.cmbRelevant5.set_active(self._component.lstRelevant[4] + 1)
        self.cmbRelevant6.set_active(self._component.lstRelevant[5] + 1)
        self.cmbRelevant7.set_active(self._component.lstRelevant[6] + 1)
        self.cmbRelevant8.set_active(self._component.lstRelevant[7] + 1)
        self.cmbRelevant9.set_active(self._component.lstRelevant[8] + 1)
        self.cmbRelevant10.set_active(self._component.lstRelevant[9] + 1)
        self.cmbRelevant11.set_active(self._component.lstRelevant[10] + 1)
        self.cmbRelevant12.set_active(self._component.lstRelevant[11] + 1)
        self.cmbRelevant13.set_active(self._component.lstRelevant[12] + 1)
        self.cmbRelevant14.set_active(self._component.lstRelevant[13] + 1)
        self.cmbRelevant15.set_active(self._component.lstRelevant[14] + 1)
        self.cmbRelevant16.set_active(self._component.lstRelevant[15] + 1)
        self.cmbRelevant17.set_active(self._component.lstRelevant[16] + 1)
        self.cmbRelevant18.set_active(self._component.lstRelevant[17] + 1)

        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        # Parse the chargeability questions.                                #
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        _visible = [True, False, False, False, False]

        # Question #1.
        if self._component.lstChargeable[0] == 0:      # Goto 2.
            _visible[1] = True
        elif self._component.lstChargeable[0] == 1:    # Stop.
            _visible[1] = False
            self._component.lstChargeable[1:5] = [-1, -1, -1, -1]
            self._component.chargeable = 0
        else:
            _visible[1] = False

        # Question #2.
        if self._component.lstChargeable[1] == 0:      # Goto 3.
            _visible[2] = True
        elif self._component.lstChargeable[1] == 1:    # Stop.
            _visible[2] = False
            self._component.lstChargeable[2:5] = [-1, -1, -1]
            self._component.chargeable = 0
        else:
            _visible[2] = False

        # Question #3.
        if self._component.lstChargeable[2] == 0:      # Stop.
            _visible[3] = False
            self._component.lstChargeable[3:5] = [-1, -1, -1]
            self._component.chargeable = 1
        elif self._component.lstChargeable[2] == 1:    # Goto 4.
            _visible[3] = True
        else:
            _visible[3] = False

        # Question #4.
        if self._component.lstChargeable[3] == 0:      # Goto 5.
            _visible[4] = True
        elif self._component.lstChargeable[3] == 1:    # Stop.
            self._component.chargeable = 1
            _visible[4] = False
            self._component.lstChargeable[4:5] = [-1, -1]
        else:
            _visible[4] = False

        # Question #5.
        if self._component.lstChargeable[4] == 0:      # Stop.
            self._component.chargeable = 0
        elif self._component.lstChargeable[4] == 1:    # Stop.
            self._component.chargeable = 1

        if self._component.chargeable == 0:
            self.lblChargeable.set_text(_(u"Failure is NOT chargeable."))
        elif self._component.chargeable == 1:
            self.lblChargeable.set_text(_(u"Failure IS chargeable."))
        else:
            self.lblChargeable.set_text("")

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

        self.cmbChargeable1.set_active(self._component.lstChargeable[0] + 1)
        self.cmbChargeable2.set_active(self._component.lstChargeable[1] + 1)
        self.cmbChargeable3.set_active(self._component.lstChargeable[2] + 1)
        self.cmbChargeable4.set_active(self._component.lstChargeable[3] + 1)
        self.cmbChargeable5.set_active(self._component.lstChargeable[4] + 1)

        return False

    def _load_actions_list(self):
        """
        Method to load the Incident actions list.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # TODO: Move this to the ListView.
        _model = self.tvwActionList.get_model()
        _model.clear()

        _results = self._modulebook.request_load_actions(self._model.incident_id)

        try:
            _n_actions = len(_results)
        except TypeError:
            _n_actions = 0

        for i in range(_n_actions):
            _owner = ""
            _approver = ""
            _closer = ""

            if _results[i][4] > 0:
                _owner = _conf.RTK_USERS[_results[i][4] - 1]
            if _results[i][7] > 0:
                _approver = _conf.RTK_USERS[_results[i][7] - 1]
            if _results[i][10] > 0:
                _closer = _conf.RTK_USERS[_results[i][10] - 1]

            _data = (_results[i][1], _results[i][2], _results[i][3],
                     _owner, _util.ordinal_to_date(_results[i][5]),
                     _conf.RTK_INCIDENT_STATUS[_results[i][6]], _approver,
                     _util.ordinal_to_date(_results[i][8]), _closer,
                     _util.ordinal_to_date(_results[i][11]))
            _model.append(_data)

        _row = _model.get_iter_root()
        self.tvwActionList.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.tvwActionList.get_column(0)
            self.tvwActionList.row_activated(_path, _column)

        return False

    def _load_actions_page(self):
        """
        Method to load the Incident action page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.cmbActionOwner.set_active(self._action.action_owner)
        self.cmbActionApproveBy.set_active(self._action.approved_by)
        self.cmbActionCloseBy.set_active(self._action.closed_by)
        self.cmbActionStatus.set_active(self._action.status)

        _buffer = self.txtPrescribedAction.get_child().get_child().get_buffer()
        _buffer.set_text(_util.none_to_string(self._action.prescribed_action))
        _buffer = self.txtActionTaken.get_child().get_child().get_buffer()
        _buffer.set_text(_util.none_to_string(self._action.action_taken))

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
            str(_util.ordinal_to_date(self._action.due_date)))
        self.txtActionApproveDate.set_text(
            str(_util.ordinal_to_date(self._action.approved_date)))
        self.txtActionCloseDate.set_text(
            str(_util.ordinal_to_date(self._action.closed_date)))

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

        self.txtTest.set_text(_util.none_to_string(self._model.test))
        self.txtTestCase.set_text(_util.none_to_string(self._model.test_case))
        self.txtExecutionTime.set_text(str(self._model.execution_time))

        return False

    def _on_action_select(self, treeview, __path, __column):
        """
        Callback function to handle events for the Incident action list
        gtk.TreeView().  It is called whenever an Incident action
        gtk.TreeView() row is activated.

        :param gtk.TreeView treeview: the affected component gtk.TreeView().
        :param str __path: the actived row gtk.TreeView() path.
        :param gtk.TreeViewColumn __column: the actived gtk.TreeViewColumn().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_model, _row) = treeview.get_selection().get_selected()

        if _row is not None:
            _action_id = _model.get_value(_row, 0)
            self._action = self._modulebook.dtcActions.dicActions[_action_id]

            self._load_actions_page()

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

        if index == 0:
            AddIncident(self._model.revision_id, self._modulebook._dao,
                        self._modulebook)
        elif index == 1:
            self._modulebook.request_add_action(self._model.incident_id)
            self._load_actions_list()
        elif index == 2:
            AddComponents(self._model.revision_id, self._model.incident_id,
                          self._modulebook._dao,
                          self._modulebook.dtcComponents, self)
        elif index == 3:
            (_model,
             _row) = self.tvwComponentList.get_selection().get_selected()
            _component_id = _model.get_value(_row, 0)

            self._modulebook.request_delete_component(self._model.incident_id,
                                                      _component_id)
            self.load_component_list()
        elif index == 4:
            _model = self.tvwComponentList.get_model()
            _row = _model.get_iter_root()

            while _row is not None:
                _component_id = _model.get_value(_row, 0)
                self._modulebook.request_save_component(_component_id)
                _row = _model.iter_next(_row)
        elif index == 5:
            self._modulebook.dtcIncident.save_incident(self._model.incident_id)
        elif index == 6:
            FilterIncident(self._model.revision_id, self._modulebook)
        elif index == 7:
            ImportIncident(self._model.revision_id, self._modulebook._dao,
                           self._modulebook)
        elif index == 8:
            # TODO: Create an export incident wizard.
            #ExportIncident()
            print "Export incident list."
        elif index == 9:
            # TODO: Update create data set wizard after refactoring Survival Analysis module.
            #CreateDataSet, self._app)
            print "Create data set from incidents."
        elif index == 10:
            self._modulebook.request_save_action(self._action.action_id)

        return False

    def _on_cellrenderer_toggle(self, cell, path, __new_text, position, model):
        """
        Method to respond to component list gtk.TreeView() gtk.CellRenderer()
        editing.

        :param gtk.CellRenderer cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer() that
                         was edited.
        :param str __new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().  Where position is:
                             0 = component ID
                             1 = part number
                             2 = initial installation
                             3 = failure
                             4 = suspension
                             5 = OCC fault
                             6 = CND/NFF
                             7 = interval censored
                             8 = use operating time
                             9 = use calendar time
        :param gtk.TreeModel model: the gtk.TreeModel() the edited
                                    gtk.CellRenderer() belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _value = not cell.get_active()
        model[path][position] = _value

        if position == 2:                   # Initial installation.
            self._component.initial_installation = 1
            self._component.failure = 0
            self._component.suspension = 0
            self._component.occ_fault = 0
            self._component.cnd_nff = 0
            self._component.interval_censored = 0
            model[path][3] = 0
            model[path][4] = 0
            model[path][5] = 0
            model[path][6] = 0
            model[path][7] = 0
        elif position == 3:                 # Failure.
            self._component.initial_installation = 0
            self._component.failure = 1
            self._component.suspension = 0
            self._component.occ_fault = 0
            self._component.cnd_nff = 0
            self._component.interval_censored = 0
            model[path][2] = 0
            model[path][4] = 0
            model[path][5] = 0
            model[path][6] = 0
            model[path][7] = 0
        elif position == 4:                 # Suspension (right).
            self._component.initial_installation = 0
            self._component.failure = 0
            self._component.suspension = 1
            self._component.occ_fault = 0
            self._component.cnd_nff = 0
            self._component.interval_censored = 0
            model[path][2] = 0
            model[path][3] = 0
            model[path][5] = 0
            model[path][6] = 0
            model[path][7] = 0
        elif position == 5:                 # OCC fault.
            self._component.initial_installation = 0
            self._component.failure = 0
            self._component.suspension = 0
            self._component.occ_fault = 1
            self._component.cnd_nff = 0
            self._component.interval_censored = 0
            model[path][2] = 0
            model[path][3] = 0
            model[path][4] = 0
            model[path][6] = 0
            model[path][7] = 0
        elif position == 6:                 # CND/NFF fault.
            self._component.initial_installation = 0
            self._component.failure = 0
            self._component.suspension = 0
            self._component.occ_fault = 0
            self._component.cnd_nff = 1
            self._component.interval_censored = 0
            model[path][2] = 0
            model[path][3] = 0
            model[path][4] = 0
            model[path][5] = 0
            model[path][7] = 0
        elif position == 7:                 # Interval censored.
            self._component.initial_installation = 0
            self._component.failure = 0
            self._component.suspension = 0
            self._component.occ_fault = 0
            self._component.cnd_nff = 0
            self._component.interval_censored = 1
            model[path][2] = 0
            model[path][3] = 0
            model[path][4] = 0
            model[path][5] = 0
            model[path][6] = 0
        elif position == 8:                 # Use operating time.
            self._component.use_op_time = 1
            self._component.use_cal_time = 0
            model[path][9] = 0
        elif position == 9:                 # Use calendar time.
            self._component.use_op_time = 0
            self._component.use_cal_time = 1
            model[path][8] = 0

        return False

    def _on_check_toggled(self, checkbutton, index):
        """
        Method to respond to gtk.CheckButton() toggled signals.

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

        if index == 0:
            self._model.accepted = _new_text
            self._modulebook.update(index + 31, _new_text)
        elif index == 1:
            self._model.reviewed = _new_text
            self._modulebook.update(index + 19, _new_text)
        elif index == 22:
            self._modulebook.load_all_revisions = _new_text

        checkbutton.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_combo_changed(self, combo, index):
        """
        Method to respond to gtk.ComboBox() changed signals.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.ComboBox() that
                          called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        combo.handler_block(self._lst_handler_id[index])

        if index == 2:
            self._model.incident_category = combo.get_active()
            _new_text = _conf.RTK_INCIDENT_CATEGORY[combo.get_active() - 1]
            self._modulebook.update(index, _new_text)
        elif index == 3:
            self._model.incident_type = combo.get_active()
            _new_text = _conf.RTK_INCIDENT_TYPE[combo.get_active() - 1]
            self._modulebook.update(index, _new_text)
        elif index == 4:
            self._model.criticality = combo.get_active()
            _new_text = _conf.RTK_INCIDENT_CRITICALITY[combo.get_active() - 1]
            self._modulebook.update(index + 2, _new_text)
        elif index == 5:
            self._model.status = combo.get_active()
            _new_text = _conf.RTK_INCIDENT_STATUS[combo.get_active() - 1]
            self._modulebook.update(index + 4, _new_text)
        elif index == 6:
            _model = combo.get_model()
            _row = combo.get_active_iter()
            try:
                self._model.hardware_id = int(_model.get_value(_row, 1))
            except ValueError:
                self._model.hardware_id = 0
        elif index == 7:
            _model = combo.get_model()
            _row = combo.get_active_iter()
            try:
                self._model.software_id = int(_model.get_value(_row, 1))
            except ValueError:
                self._model.software_id = 0
        elif index == 8:
            self._model.request_by = combo.get_active()
            _new_text = _conf.RTK_USERS[combo.get_active() - 1]
            self._modulebook.update(index + 10, _new_text)
        elif index == 9:
            self._model.life_cycle = combo.get_active()
            _new_text = _conf.RTK_LIFECYCLE[combo.get_active() - 1]
            self._modulebook.update(index + 21, _new_text)
        elif index == 14:
            self._model.detection_method = combo.get_active()
            _new_text = _conf.RTK_DETECTION_METHODS[combo.get_active() - 1]
            self._modulebook.update(index - 7, _new_text)
        elif index == 18:
            self._model.review_by = combo.get_active()
            _new_text = _conf.RTK_USERS[combo.get_active() - 1]
            self._modulebook.update(index + 3, _new_text)
        elif index == 19:
            self._model.approve_by = combo.get_active()
            _new_text = _conf.RTK_USERS[combo.get_active() - 1]
            self._modulebook.update(index + 5, _new_text)
        elif index == 20:
            self._model.close_by = combo.get_active()
            _new_text = _conf.RTK_USERS[combo.get_active() - 1]
            self._modulebook.update(index + 7, _new_text)
        elif index == 24:
            self._action.action_owner = combo.get_active()
            _new_text = _conf.RTK_USERS[combo.get_active() - 1]
            (_model, _row) = self.tvwActionList.get_selection().get_selected()
            _model.set_value(_row, 3, _new_text)
        elif index == 26:
            self._action.status = combo.get_active()
            # We only use a sub-set of the status so we can't use indexing.
            _new_text = combo.get_active_text()
            (_model, _row) = self.tvwActionList.get_selection().get_selected()
            _model.set_value(_row, 5, _new_text)
        elif index == 27:
            self._action.approved_by = combo.get_active()
            _new_text = _conf.RTK_USERS[combo.get_active() - 1]
            (_model, _row) = self.tvwActionList.get_selection().get_selected()
            _model.set_value(_row, 6, _new_text)
        elif index == 29:
            self._action.closed_by = combo.get_active()
            _new_text = _conf.RTK_USERS[combo.get_active() - 1]
            (_model, _row) = self.tvwActionList.get_selection().get_selected()
            _model.set_value(_row, 8, _new_text)

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_component_select(self, treeview, __path, __column):
        """
        Callback function to handle events for the affected component list
        gtk.TreeView().  It is called whenever an affected component
        gtk.TreeView() row is activated.

        :param gtk.TreeView treeview: the affected component gtk.TreeView().
        :param str __path: the actived row gtk.TreeView() path.
        :param gtk.TreeViewColumn __column: the actived gtk.TreeViewColumn().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_model, _row) = treeview.get_selection().get_selected()

        if _row is not None:
            _component_id = _model.get_value(_row, 0)
            self._component = self.dtcComponents.dicComponents[_component_id]

            self._load_chargeability_page()

        return False

    def _on_focus_out(self, entry, __event, index):     # pylint: disable=R0912
        """
        Method to respond to gtk.Entry() focus_out signals.

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

        if index == 10:
            _new_text = _util.date_to_ordinal(entry.get_text())
            self._model.request_date = _new_text
            self._modulebook.update(index + 18, _new_text)
        elif index == 11:
            _new_text = entry.get_text()
            self._model.short_description = _new_text
            self._modulebook.update(index - 7, _new_text)
        elif index == 12:
            _new_text = entry.get_text(*entry.get_bounds())
            self._model.long_description = _new_text
            self._modulebook.update(index - 7, _new_text)
        elif index == 13:
            _new_text = entry.get_text(*entry.get_bounds())
            self._model.remarks = _new_text
            self._modulebook.update(index - 5, _new_text)
        elif index == 15:
            _new_text = entry.get_text()
            self._model.test = _new_text
            self._modulebook.update(index - 5, _new_text)
        elif index == 16:
            _new_text = entry.get_text()
            self._model.test_case = _new_text
            self._modulebook.update(index - 5, _new_text)
        elif index == 17:
            _new_text = float(entry.get_text())
            self._model.execution_time = _new_text
            self._modulebook.update(index - 5, _new_text)
        elif index == 21:
            _new_text = entry.get_text(*entry.get_bounds())
            self._model.analysis = _new_text
            self._modulebook.update(index + 9, _new_text)
        elif index == 22:
            _new_text = entry.get_text(*entry.get_bounds())
            self._action.prescribed_action = _new_text
            (_model, _row) = self.tvwActionList.get_selection().get_selected()
            _model.set_value(_row, 1, _new_text)
        elif index == 23:
            _new_text = entry.get_text(*entry.get_bounds())
            self._action.action_taken = _new_text
            (_model, _row) = self.tvwActionList.get_selection().get_selected()
            _model.set_value(_row, 2, _new_text)
        elif index == 25:
            _new_text = entry.get_text()
            self._action.due_date = _util.date_to_ordinal(_new_text)
            (_model, _row) = self.tvwActionList.get_selection().get_selected()
            _model.set_value(_row, 4, _new_text)
        elif index == 27:
            _new_text = entry.get_text()
            self._action.approved_date = _util.date_to_ordinal(_new_text)
            (_model, _row) = self.tvwActionList.get_selection().get_selected()
            _model.set_value(_row, 8, _new_text)
        elif index == 30:
            _new_text = entry.get_text()
            self._action.closed_date = _util.date_to_ordinal(_new_text)
            (_model, _row) = self.tvwActionList.get_selection().get_selected()
            _model.set_value(_row, 9, _new_text)

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

        self._component.lstRelevant[index - 100] = combo.get_active() - 1

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

        self._component.lstChargeable[index] = combo.get_active() - 1

        self._load_chargeability_page()

        return False
