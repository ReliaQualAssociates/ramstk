#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.revision.WorkBook.py is part of The RTK Project
#
# All rights reserved.

"""
###############################
Revision Package Work Book View
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
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration   # pylint: disable=E0401
    import rtk.gui.gtk.Widgets as Widgets       # pylint: disable=E0401
from Assistants import AddRevision

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class WorkView(gtk.VBox):

    """
    The Work Book view displays all the attributes for the selected Revision.
    The attributes of a Work Book view are:

    :ivar _workview: the RTK top level Work View window to embed the Revision
                     Work Book into.
    :ivar _revision_model: the Revision data model whose attributes are being
                           displayed.
    :ivar _usage_model: the Usage Profile data model whose attributes are being
                        displayed.
    :ivar dict _dic_definitions: dictionary containing pointers to the failure
                                 definitions for the Revision being displayed.
                                 Key is the Failure Definition ID; value is the
                                 pointer to the Failure Definition data model.
    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable Revision attribute.
    :ivar dtcRevision: the :py:class:`rtk.revision.Revision.Revision` data
                       controller to use with this Work Book.
    :ivar dtcProfile: the :py:class:`rtk.usage.UsageProfile.UsageProfile` data
                       controller to use with this Work Book.
    :ivar dtcDefinitions: the :py:class:`rtk.failure_definition.Controller`
                          data controller to use with this Work Book.
    :ivar gtk.Button btnAddSibling: the gtk.Button() to add a new item to the
                                    Usage Profile at the same level as the
                                    selected item.
    :ivar gtk.Button btnAddChild: the gtk.Button() to add a new item to the
                                  Usage Profile one level below the selected
                                  item.
    :ivar gtk.Button btnRemoveUsage: the gtk.Button() remove the selected item
                                     and any child items from the Usage
                                     Profile.
    :ivar gtk.Button btnSaveUsage: the gtk.Button() to save the Usage Profile
                                   to the RTK Project database.
    :ivar gtk.Button btnAddDefinition: the gtk.Button() to add a new Failure
                                       Definition to the Revision.
    :ivar gtk.Button btnRemoveDefinition: the gtk.Button() to remove the
                                          selected Failure Definition.
    :ivar gtk.Button btnSaveDefinitions: the gtk.Button() to save the Failure
                                         Definitions to the RTK Project
                                         database.
    :ivar gtk.TreeView tvwMissionProfile: the gtk.TreeView() to display/edit
                                          the usage profile for a Revision.
    :ivar gtk.TreeView tvwFailureDefinitions: the gtk.TreeView() to
                                              display/edit the failure
                                              definitions for a Revision.
    :ivar gtk.Entry txtCode: the gtk.Entry() to display/edit the Revision code.
    :ivar gtk.Entry txtName: the gtk.Entry() to display/edit the Revision name.
    :ivar gtk.Entry txtTotalCost: the gtk.Entry() to display the Revision cost.
    :ivar gtk.Entry txtCostFailure: the gtk.Entry() to display the Revision
                                    cost per failure.
    :ivar gtk.Entry txtCostHour: the gtk.Entry() to display the Revision cost
                                 per operating hour.
    :ivar gtk.Entry txtPartCount: the gtk.Entry() to display the numebr of
                                  hardware components comprising the Revision.
    :ivar gtk.Entry txtRemarks: the gtk.Entry() display/edit the Revision
                                remarks.
    :ivar gtk.Entry txtActiveHt: the gtk.Entry() to display the Revision active
                                 hazard rate.
    :ivar gtk.Entry txtDormantHt: the gtk.Entry() to display the Revision
                                  dormant hazard rate.
    :ivar gtk.Entry txtSoftwareHt: the gtk.Entry() to display the Revision
                                   software hazard rate.
    :ivar gtk.Entry txtPredictedHt: the gtk.Entry() to display the Revision
                                    logistics hazard rate.
    :ivar gtk.Entry txtMissionHt: the gtk.Entry() to display the Revision
                                  mission hazard rate.
    :ivar gtk.Entry txtMTBF: the gtk.Entry() display the Revision logistics
                             MTBF.
    :ivar gtk.Entry txtMissionMTBF: the gtk.Entry() display the Revision
                                    mission MTBF.
    :ivar gtk.Entry txtReliability: the gtk.Entry() display the Revision
                                    logistics reliability.
    :ivar gtk.Entry txtMissionRt: the gtk.Entry() display the Revision mission
                                  reliability.
    :ivar gtk.Entry txtMPMT: the gtk.Entry() to display the Revision mean
                             preventive maintenance time.
    :ivar gtk.Entry txtMCMT: the gtk.Entry() display the Revision mean
                             corrective maintenance time.
    :ivar gtk.Entry txtMTTR: the gtk.Entry() to display the Revision mean time
                             to repair.
    :ivar gtk.Entry txtMMT: the gtk.Entry() display the Revision mean
                            maintenance time.
    :ivar gtk.Entry txtAvailability: the gtk.Entry() to display the Revision
                                     logistics availability.
    :ivar gtk.Entry txtMissionAt: the gtk.Entry() to display the Revision
                                  mission availability.
    """

    def __init__(self, modulebook):
        """
        Method to initialize the Work Book view for the Revision package.

        :param modulebook: the :py:class:`rtk.revision.ModuleBook` to associate
                           with this Work Book.
        """

        gtk.VBox.__init__(self)

        # Initialize private scalar attributes.
        self._modulebook = modulebook
        self._dtc_revision = modulebook.mdcRTK.dtcRevision
        self._dtc_profile = modulebook.mdcRTK.dtcProfile
        self._dtc_definiions = modulebook.mdcRTK.dtcDefinitions
        self._revision_model = None
        self._usage_model = None

        # Initialize private dict attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize public scalar attributes.
        self.revision_id = None

        # General data tab widgets.
        self.txtCode = Widgets.make_entry()
        self.txtName = Widgets.make_entry()
        self.txtTotalCost = Widgets.make_entry(width=75, editable=False)
        self.txtCostFailure = Widgets.make_entry(width=75, editable=False)
        self.txtCostHour = Widgets.make_entry(width=75, editable=False)
        self.txtPartCount = Widgets.make_entry(width=75, editable=False)
        self.txtRemarks = gtk.TextBuffer()

        # Assessment results tab widgets.
        self.txtActiveHt = Widgets.make_entry(width=125, editable=False,
                                              bold=True)
        self.txtDormantHt = Widgets.make_entry(width=125, editable=False,
                                               bold=True)
        self.txtSoftwareHt = Widgets.make_entry(width=125, editable=False,
                                                bold=True)
        self.txtPredictedHt = Widgets.make_entry(width=125, editable=False,
                                                 bold=True)
        self.txtMissionHt = Widgets.make_entry(width=125, editable=False,
                                               bold=True)
        self.txtMTBF = Widgets.make_entry(width=125, editable=False, bold=True)
        self.txtMissionMTBF = Widgets.make_entry(width=125, editable=False,
                                                 bold=True)
        self.txtReliability = Widgets.make_entry(width=125, editable=False,
                                                 bold=True)
        self.txtMissionRt = Widgets.make_entry(width=125, editable=False,
                                               bold=True)
        self.txtMPMT = Widgets.make_entry(width=125, editable=False, bold=True)
        self.txtMCMT = Widgets.make_entry(width=125, editable=False, bold=True)
        self.txtMTTR = Widgets.make_entry(width=125, editable=False, bold=True)
        self.txtMMT = Widgets.make_entry(width=125, editable=False, bold=True)
        self.txtAvailability = Widgets.make_entry(width=125, editable=False,
                                                  bold=True)
        self.txtMissionAt = Widgets.make_entry(width=125, editable=False,
                                               bold=True)

        # Set the gtk.Widget() tooltips.
        self.txtCode.set_tooltip_text(_(u"A unique code for the selected "
                                        u"revision."))
        self.txtName.set_tooltip_text(_(u"The name of the selected "
                                        u"revision."))
        self.txtTotalCost.set_tooltip_text(_(u"Displays the total cost of "
                                             u"the selected revision."))
        self.txtCostFailure.set_tooltip_text(_(u"Displays the cost per "
                                               u"failure of the selected "
                                               u"revision."))
        self.txtCostHour.set_tooltip_text(_(u"Displays the failure cost "
                                            u"per operating hour for the "
                                            u"selected revision."))
        self.txtPartCount.set_tooltip_text(_(u"Displays the total part "
                                             u"count for the selected "
                                             u"revision."))
        self.txtActiveHt.set_tooltip_text(_(u"Displays the active failure "
                                            u"intensity for the selected "
                                            u"revision."))
        self.txtDormantHt.set_tooltip_text(_(u"Displays the dormant "
                                             u"failure intensity for the "
                                             u"selected revision."))
        self.txtSoftwareHt.set_tooltip_text(_(u"Displays the software "
                                              u"failure intensity for the "
                                              u"selected revision."))
        self.txtPredictedHt.set_tooltip_text(_(u"Displays the predicted "
                                               u"failure intensity for "
                                               u"the selected revision.  "
                                               u"This is the sum of the "
                                               u"active, dormant, and "
                                               u"software hazard rates."))
        self.txtMissionHt.set_tooltip_text(_(u"Displays the mission "
                                             u"failure intensity for the "
                                             u"selected revision."))
        self.txtMTBF.set_tooltip_text(_(u"Displays the limiting mean time "
                                        u"between failure (MTBF) for the "
                                        u"selected revision."))
        self.txtMissionMTBF.set_tooltip_text(_(u"Displays the mission "
                                               u"mean time between "
                                               u"failure (MTBF) for the "
                                               u"selected revision."))
        self.txtReliability.set_tooltip_text(_(u"Displays the limiting "
                                               u"reliability for the "
                                               u"selected revision."))
        self.txtMissionRt.set_tooltip_text(_(u"Displays the mission "
                                             u"reliability for the "
                                             u"selected revision."))
        self.txtMPMT.set_tooltip_text(_(u"Displays the mean preventive "
                                        u"maintenance time (MPMT) for the "
                                        u"selected revision."))
        self.txtMCMT.set_tooltip_text(_(u"Displays the mean corrective "
                                        u"maintenance time (MCMT) for the "
                                        u"selected revision."))
        self.txtMTTR.set_tooltip_text(_(u"Displays the mean time to "
                                        u"repair (MTTR) for the selected "
                                        u"revision."))
        self.txtMMT.set_tooltip_text(_(u"Displays the mean maintenance "
                                       u"time (MMT) for the selected "
                                       u"revision.  This includes "
                                       u"preventive and corrective "
                                       u"maintenance."))
        self.txtAvailability.set_tooltip_text(_(u"Displays the logistics "
                                                u"availability for the "
                                                u"selected revision."))
        self.txtMissionAt.set_tooltip_text(_(u"Displays the mission "
                                             u"availability for the "
                                             u"selected revision."))

        # Connect gtk.Widget() signals to callback methods.
        self._lst_handler_id.append(self.txtName.connect('focus-out-event',
                                                         self._on_focus_out, 0))
        self._lst_handler_id.append(self.txtRemarks.connect('changed',
                                                            self._on_focus_out,
                                                            None, 1))
        self._lst_handler_id.append(self.txtCode.connect('focus-out-event',
                                                         self._on_focus_out, 2))

        # Put it all together.
        _toolbar = self._create_toolbar()
        self.pack_start(_toolbar, expand=False)

        _notebook = self._create_notebook()
        self.pack_start(_notebook)

        self.show_all()

    def _create_toolbar(self):
        """
        Method to create the gtk.ToolBar() for the Revision class work book.

        :return: _toolbar
        :rtype: gtk.ToolBar
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        # Add revision button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Adds a new revision to the open RTK "
                                   u"Program database."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/add.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_add_revision)
        _toolbar.insert(_button, _position)
        _position += 1

        # Delete revision button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Removes the currently selected revision "
                                   u"from the open RTK Project database."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/remove.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_delete_revision)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Calculate revision _button_
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Calculate the currently selected "
                                   u"revision."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/calculate.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_calculate_revision)
        _toolbar.insert(_button, _position)
        _position += 1

        # Create report button.
        _button = gtk.MenuToolButton(None, label="")
        _button.set_tooltip_text(_(u"Create Revision reports."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/reports.png')
        _button.set_icon_widget(_image)
        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"Mission and Environmental "
                                          u"Profile"))
        _menu_item.set_tooltip_text(_(u"Creates the mission and environmental "
                                      u"profile report for the currently "
                                      u"selected revision."))
        # _menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Failure Definition"))
        _menu_item.set_tooltip_text(_(u"Creates the failure definition report "
                                      u"for the currently selected revision."))
        # _menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _button.set_menu(_menu)
        _menu.show_all()
        _button.show()
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save revision button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Saves the currently selected revision "
                                   u"to the open RTK Project database."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_save_revision)
        _toolbar.insert(_button, _position)

        _toolbar.show()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Revision class gtk.Notebook().

        :return: _notebook
        :rtype: gtk.Notebook
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

        self._create_general_data_page(_notebook)
        self._create_assessment_results_page(_notebook)

        return _notebook

    def _create_general_data_page(self, notebook):
        """
        Method to create the Revision Work Book page for displaying general
        data about the selected Revision.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the general
                                      data tab.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _frame = Widgets.make_frame(label=_(u"General Information"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame.add(_scrollwindow)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _labels = [_(u"Revision Code:"), _(u"Revision Name:"),
                   _(u"Total Cost:"), _(u"Cost/Failure:"),
                   _(u"Cost/Hour:"), _(u"Total Part Count:"),
                   _(u"Remarks:")]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5)
        _x_pos += 50

        # Place the widgets.
        _fixed.put(self.txtCode, _x_pos, _y_pos[0])
        _fixed.put(self.txtName, _x_pos, _y_pos[1])
        _fixed.put(self.txtTotalCost, _x_pos, _y_pos[2])
        _fixed.put(self.txtCostFailure, _x_pos, _y_pos[3])
        _fixed.put(self.txtCostHour, _x_pos, _y_pos[4])
        _fixed.put(self.txtPartCount, _x_pos, _y_pos[5])

        _textview = Widgets.make_text_view(txvbuffer=self.txtRemarks,
                                           width=400)
        _textview.set_tooltip_text(_(u"Enter any remarks associated with "
                                     u"the selected revision."))
        _fixed.put(_textview, _x_pos, _y_pos[6])

        _fixed.show_all()

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"General\nData") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays general information for the "
                                  u"selected revision."))
        notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _create_assessment_results_page(self, notebook):
        """
        Method to create the Revision Wrok Book page for displaying assessment
        results for the selected Revision.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page to.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HBox()

        # Reliability results containers.
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = Widgets.make_frame(label=_(u"Reliability Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_start(_frame)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display reliability assessment      #
        # results.                                                      #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _labels = [_(u"Active Failure Intensity [\u039B(t)]:"),
                   _(u"Dormant \u039B(t):"), _(u"Software \u039B(t):"),
                   _(u"Predicted \u039B(t):"), _(u"Mission \u039B(t):"),
                   _(u"Mean Time Between Failure [MTBF]:"),
                   _(u"Mission MTBF:"), _(u"Reliability [R(t)]:"),
                   _(u"Mission R(t):")]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5)
        _x_pos += 55

        _fixed.put(self.txtActiveHt, _x_pos, _y_pos[0])
        _fixed.put(self.txtDormantHt, _x_pos, _y_pos[1])
        _fixed.put(self.txtSoftwareHt, _x_pos, _y_pos[2])
        _fixed.put(self.txtPredictedHt, _x_pos, _y_pos[3])
        _fixed.put(self.txtMissionHt, _x_pos, _y_pos[4])
        _fixed.put(self.txtMTBF, _x_pos, _y_pos[5])
        _fixed.put(self.txtMissionMTBF, _x_pos, _y_pos[6])
        _fixed.put(self.txtReliability, _x_pos, _y_pos[7])
        _fixed.put(self.txtMissionRt, _x_pos, _y_pos[8])

        _fixed.show_all()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display maintainability assessment  #
        # results.                                                      #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = Widgets.make_frame(label=_(u"Maintainability Results"))
        _frame.set_shadow_type(gtk.SHADOW_NONE)
        _frame.add(_scrollwindow)

        _hbox.pack_start(_frame)

        # Maintainability results widgets.
        _labels = [_(u"Mean Preventive Maintenance Time [MPMT]:"),
                   _(u"Mean Corrective Maintenance Time [MCMT]:"),
                   _(u"Mean Time to Repair [MTTR]:"),
                   _(u"Mean Maintenance Time [MMT]:"),
                   _(u"Availability [A(t)]:"), _(u"Mission A(t):")]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5)
        _x_pos += 55

        _fixed.put(self.txtMPMT, _x_pos, _y_pos[0])
        _fixed.put(self.txtMCMT, _x_pos, _y_pos[1])
        _fixed.put(self.txtMTTR, _x_pos, _y_pos[2])
        _fixed.put(self.txtMMT, _x_pos, _y_pos[3])
        _fixed.put(self.txtAvailability, _x_pos, _y_pos[4])
        _fixed.put(self.txtMissionAt, _x_pos, _y_pos[5])

        _fixed.show_all()

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Assessment\nResults") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays reliability, maintainability, "
                                  u"and availability assessment results for "
                                  u"the selected revision."))
        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Revision class gtk.Notebook() widgets.

        :param model: the :py:class:`rtk.revision.Revision.Model` whose
                      attributes are to be displayed.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'

        self._revision_model = model
        self.revision_id = self._revision_model.revision_id

        # Load the General Data page.
        self.txtTotalCost.set_text(
            str(locale.currency(self._revision_model.cost)))
        self.txtCostFailure.set_text(
            str(locale.currency(self._revision_model.cost_per_failure)))
        self.txtCostHour.set_text(
            str(locale.currency(self._revision_model.cost_per_hour)))
        self.txtName.set_text(self._revision_model.name)
        self.txtRemarks.set_text(self._revision_model.remarks)
        self.txtPartCount.set_text(
            str('{0:0.0f}'.format(self._revision_model.n_parts)))
        self.txtCode.set_text(str(self._revision_model.code))
        self.txtPartCount.set_text(str(self._revision_model.n_parts))

        # Load the Assessment Results page.
        self.txtAvailability.set_text(
            str(fmt.format(self._revision_model.availability)))
        self.txtMissionAt.set_text(
            str(fmt.format(self._revision_model.mission_availability)))
        self.txtActiveHt.set_text(str(
            fmt.format(self._revision_model.active_hazard_rate)))
        self.txtDormantHt.set_text(
            str(fmt.format(self._revision_model.dormant_hazard_rate)))
        self.txtMissionHt.set_text(
            str(fmt.format(self._revision_model.mission_hazard_rate)))
        self.txtPredictedHt.set_text(
            str(fmt.format(self._revision_model.hazard_rate)))
        self.txtSoftwareHt.set_text(
            str(fmt.format(self._revision_model.software_hazard_rate)))
        self.txtMMT.set_text(str(fmt.format(self._revision_model.mmt)))
        self.txtMCMT.set_text(str(fmt.format(self._revision_model.mcmt)))
        self.txtMPMT.set_text(str(fmt.format(self._revision_model.mpmt)))
        self.txtMissionMTBF.set_text(
            str(fmt.format(self._revision_model.mission_mtbf)))
        self.txtMTBF.set_text(str(fmt.format(self._revision_model.mtbf)))
        self.txtMTTR.set_text(str(fmt.format(self._revision_model.mttr)))
        self.txtMissionRt.set_text(
            str(fmt.format(self._revision_model.mission_reliability)))
        self.txtReliability.set_text(
            str(fmt.format(self._revision_model.reliability)))

        _title = _(u"RTK Work Book: Revision "
                   u"(Analyzing {0:s})").format(self._revision_model.name)
        _workview = self.get_parent()
        _workview.set_title(_title)

        return False

    def update(self):
        """
        Method to update the Work Book widgets with changes to the Revision
        data model attributes.  Called by other views when the Revision data
        model attributes are edited via their gtk.Widgets().

        :return: False on success or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'

        self.txtCode.handler_block(self._lst_handler_id[2])
        self.txtCode.set_text(str(self._revision_model.code))
        self.txtCode.handler_unblock(self._lst_handler_id[2])

        self.txtName.handler_block(self._lst_handler_id[0])
        self.txtName.set_text(str(self._revision_model.name))
        self.txtName.handler_unblock(self._lst_handler_id[0])

        self.txtRemarks.handler_block(self._lst_handler_id[1])
        self.txtRemarks.set_text(self._revision_model.remarks)
        self.txtRemarks.handler_unblock(self._lst_handler_id[1])

        self.txtTotalCost.set_text(
            str(locale.currency(self._revision_model.cost)))
        self.txtCostFailure.set_text(
            str(locale.currency(self._revision_model.cost_per_failure)))
        self.txtCostHour.set_text(
            str(locale.currency(self._revision_model.cost_per_hour)))
        self.txtPartCount.set_text(str(self._revision_model.n_parts))

        self.txtAvailability.set_text(
            str(fmt.format(self._revision_model.availability)))
        self.txtMissionAt.set_text(
            str(fmt.format(self._revision_model.mission_availability)))
        self.txtActiveHt.set_text(str(
            fmt.format(self._revision_model.active_hazard_rate)))
        self.txtDormantHt.set_text(
            str(fmt.format(self._revision_model.dormant_hazard_rate)))
        self.txtMissionHt.set_text(
            str(fmt.format(self._revision_model.mission_hazard_rate)))
        self.txtPredictedHt.set_text(
            str(fmt.format(self._revision_model.hazard_rate)))
        self.txtSoftwareHt.set_text(
            str(fmt.format(self._revision_model.software_hazard_rate)))
        self.txtMMT.set_text(str(fmt.format(self._revision_model.mmt)))
        self.txtMCMT.set_text(str(fmt.format(self._revision_model.mcmt)))
        self.txtMPMT.set_text(str(fmt.format(self._revision_model.mpmt)))
        self.txtMissionMTBF.set_text(
            str(fmt.format(self._revision_model.mission_mtbf)))
        self.txtMTBF.set_text(str(fmt.format(self._revision_model.mtbf)))
        self.txtMTTR.set_text(str(fmt.format(self._revision_model.mttr)))
        self.txtMissionRt.set_text(
            str(fmt.format(self._revision_model.mission_reliability)))
        self.txtReliability.set_text(
            str(fmt.format(self._revision_model.reliability)))

        return False

    def _on_focus_out(self, entry, __event, index):
        """
        Method to retrieve gtk.Entry() changes and assign the new data to the
        appropriate Revision data model attribute.

        :param gtk.Entry entry: the gtk.Entry() that called the method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param int index: the position in the Revision class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Entry().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        entry.handler_block(self._lst_handler_id[index])

        if index == 0:
            _index = 17
            _text = entry.get_text()
            self._revision_model.name = _text
        elif index == 1:
            _index = 20
            _text = self.txtRemarks.get_text(*self.txtRemarks.get_bounds())
            self._revision_model.remarks = _text
        elif index == 2:
            _index = 22
            _text = entry.get_text()
            self._revision_model.code = _text

        self._modulebook.update(_index, _text)

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _request_save_revision(self, __button):
        """
        Method to send request to save the selected revision to the Revision
        data controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                         method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        (_results,
         _error_code) = self._dtc_revision.save_revision(self.revision_id)

        if _error_code != 0:
            _prompt = _(u"An error occurred while attempting to save "
                        u"Revision {0:d}").format(self.revision_id)
            Widgets.rtk_error(_prompt)
            _return = True

        return _return

    def _request_add_revision(self, __button):
        """
        Method to send request to add a new revision to the Revision data
        controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Launch the Add Revision gtk.Assistant().
        AddRevision(self._modulebook)

        return False

    def _request_delete_revision(self, __button):
        """
        Method to send request to delete the selected revision from the
        Revision data controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        (_model,
         _row) = self._modulebook.treeview.get_selection().get_selected()
        _path = _model.get_path(_row)

        (_results,
         _error_code) = self._dtc_revision.delete_revision(self.revision_id)

        if _error_code != 0:
            _prompt = _(u"An error occurred when attempting to delete "
                        u"Revision {0:d}").format(self.revision_id)
            Widgets.rtk_error(_prompt)
            _return = True
        else:
            self._dtc_profile.dicProfiles.pop(self.revision_id)
            self._dtc_definiions.dicDefinitions.pop(self.revision_id)

            # Remove the deleted Revision from the gtk.TreeView().
            _next_row = _model.iter_next(_row)

            _model.remove(_row)
            _model.row_deleted(_path)

            if _next_row is None:
                _next_row = _model.get_iter_root()
            _path = _model.get_path(_next_row)
            _column = self._modulebook.treeview.get_column(0)
            self._modulebook.treeview.set_cursor(_path, None, False)
            self._modulebook.treeview.row_activated(_path, _column)

        return _return

    def _request_calculate_revision(self, __button):
        """
        Method to send request to calculate the selected revision to the
        Revision data controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._dtc_revision.calculate_revision(self.revision_id,
                                              Configuration.RTK_MTIME,
                                              Configuration.FRMULT)

        self.update()

        return False
