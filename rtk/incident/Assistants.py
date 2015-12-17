#!/usr/bin/env python
"""
##################################
Incident Package Assistants Module
##################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.incident.Assistants.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale
import sys

from os import name
from datetime import datetime

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

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class AddIncident(object):
    """
    This is the gtk.Assistant() that guides the user through the process of
    adding Incident records to the open RTK Program database.
    """

    def __init__(self, revision_id, dao, modulebook):
        """
        Initialize an instance of the Add Incident Assistant.

        :param gtk.Button __button: the gtk.Button() that called this
                                    Assistant.
        :param int revision_id: the ID of the revision to add the incident to.
        :param dao: the :py:class:`rtk.dao.DAO` used to communicate with the
                    RTK Project database.
        :param modulebook: the :py:class:`rtk.Incident.ModuleBook` to add the
                           the new incident to.
        """

        self._dao = dao
        self._revision_id = revision_id
        self._modulebook = modulebook

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_(u"RTK Add Incident Assistant"))
        self.assistant.connect('apply', self._add_incident)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

        # Create the introduction page.
        _fixed = gtk.Fixed()
        _label = _widg.make_label(_(u"This is the RTK incident addition "
                                    u"assistant.  It will help you add a new "
                                    u"hardware or software incident to the "
                                    u"database.  Press 'Forward' to continue "
                                    u"or 'Cancel' to quit the assistant."),
                                  width=-1, height=-1, wrap=True)
        _fixed.put(_label, 5, 5)
        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(_fixed, _(u"Introduction"))
        self.assistant.set_page_complete(_fixed, True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the incident information page.                             #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        self.cmbCategory = _widg.make_combo()
        self.cmbType = _widg.make_combo()
        self.cmbCriticality = _widg.make_combo()
        self.cmbLifeCycle = _widg.make_combo()
        self.cmbHardware = _widg.make_combo(simple=False)
        self.cmbSoftware = _widg.make_combo(simple=False)
        self.cmbUnit = _widg.make_combo()
        self.cmbReportedBy = _widg.make_combo()
        self.cmbDetectMethod = _widg.make_combo()

        self.txtIncidentDate = _widg.make_entry(width=100)
        self.txtTestProcedure = _widg.make_entry()
        self.txtTestCase = _widg.make_entry()
        self.txtExecutionTime = _widg.make_entry(width=100)

        # Load the gtk.ComboBox() widgets.
        self.cmbReportedBy.append_text("")
        for i in range(len(_conf.RTK_USERS)):
            self.cmbReportedBy.append_text(_conf.RTK_USERS[i])
        self.cmbCategory.append_text("")
        for i in range(len(_conf.RTK_INCIDENT_CATEGORY)):
            self.cmbCategory.append_text(_conf.RTK_INCIDENT_CATEGORY[i])
        self.cmbType.append_text("")
        for i in range(len(_conf.RTK_INCIDENT_TYPE)):
            self.cmbType.append_text(_conf.RTK_INCIDENT_TYPE[i])
        self.cmbCriticality.append_text("")
        for i in range(len(_conf.RTK_INCIDENT_CRITICALITY)):
            self.cmbCriticality.append_text(_conf.RTK_INCIDENT_CRITICALITY[i])
        self.cmbLifeCycle.append_text("")
        for i in range(len(_conf.RTK_LIFECYCLE)):
            self.cmbLifeCycle.append_text(_conf.RTK_LIFECYCLE[i])

        _query = "SELECT fld_name, fld_hardware_id, fld_description \
                  FROM rtk_hardware \
                  WHERE fld_revision_id={0:d} \
                  AND fld_part=0".format(revision_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)
        _widg.load_combo(self.cmbHardware, _results, simple=False)

        _query = "SELECT fld_description, fld_software_id, fld_description \
                  FROM rtk_software \
                  WHERE fld_revision_id={0:d}".format(revision_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)
        _widg.load_combo(self.cmbSoftware, _results, simple=False)

        _results = [[_(u"Code Review")], [_(u"Error/Anomaly Analysis")],
                    [_(u"Structure Analysis")], [_(u"Random Testing")],
                    [_(u"Functional Testing")], [_(u"Branch Testing")]]
        _widg.load_combo(self.cmbDetectMethod, _results)

        # Create and place the labels.
        self.fxdPageGeneral = gtk.Fixed()

        _labels = [_(u"Incident Date*:"), _(u"Reported By*:"),
                   _(u"Incident Category*:"), _(u"Incident Type:"),
                   _(u"Incident Criticality:"), _(u"Life Cycle:"),
                   _(u"Affected Unit:"), _(u"Affected Assembly*:"),
                   _(u"Affected Software:"), _(u"Detection Method*:"),
                   _(u"Test Procedure:"), _(u"Test Case:"),
                   _(u"Execution Time*:")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels,
                                             self.fxdPageGeneral, 5, 5)
        _x_pos += 40

        self.txtIncidentDate.set_tooltip_text(_(u"Enter the date the incident "
                                                u"occurred."))
        self.cmbReportedBy.set_tooltip_text(_(u"Enter the name of the person "
                                              u"reporting the incident.  "
                                              u"Defaults to currently logged "
                                              u"in user."))
        self.cmbCategory.set_tooltip_text(_(u"Select the category this "
                                            u"incident represents."))
        self.cmbType.set_tooltip_text(_(u"Select the type of problem this "
                                        u"incident represents."))
        self.cmbCriticality.set_tooltip_text(_(u"Select the severity of the "
                                               u"discrepancy."))
        self.txtTestProcedure.set_tooltip_text(_(u"Enter the test procedure "
                                                 u"being run when the "
                                                 u"incident occurred."))
        self.txtTestCase.set_tooltip_text(_(u"Enter the test case being run "
                                            u"when the incident occurred."))
        self.txtExecutionTime.set_tooltip_text(_(u"Enter the execution time "
                                                 u"when the incident "
                                                 u"occurred."))

        # Add a calendar widget for date selection if we are on a posix
        # platform.  The calendar widget doesn't work for shit on Windoze.
        if name == 'posix':
            self.btnCalendar = _widg.make_button(height=25, width=25,
                                                 label="...", image=None)
            self.btnCalendar.set_tooltip_text(_(u"Launch a calendar to select "
                                                u"the incident date"))
            self.btnCalendar.connect('clicked', _util.date_select, None,
                                     self.txtIncidentDate)
            self.fxdPageGeneral.put(self.btnCalendar, _x_pos + 105, _y_pos[0])

        self.fxdPageGeneral.put(self.txtIncidentDate, _x_pos, _y_pos[0])
        self.fxdPageGeneral.put(self.cmbReportedBy, _x_pos, _y_pos[1])
        self.fxdPageGeneral.put(self.cmbCategory, _x_pos, _y_pos[2])
        self.fxdPageGeneral.put(self.cmbType, _x_pos, _y_pos[3])
        self.fxdPageGeneral.put(self.cmbCriticality, _x_pos, _y_pos[4])
        self.fxdPageGeneral.put(self.cmbLifeCycle, _x_pos, _y_pos[5])
        self.fxdPageGeneral.put(self.cmbUnit, _x_pos, _y_pos[6])
        self.fxdPageGeneral.put(self.cmbHardware, _x_pos, _y_pos[7])
        self.fxdPageGeneral.put(self.cmbSoftware, _x_pos, _y_pos[8])
        self.fxdPageGeneral.put(self.cmbDetectMethod, _x_pos, _y_pos[9])
        self.fxdPageGeneral.put(self.txtTestProcedure, _x_pos, _y_pos[10])
        self.fxdPageGeneral.put(self.txtTestCase, _x_pos, _y_pos[11])
        self.fxdPageGeneral.put(self.txtExecutionTime, _x_pos, _y_pos[12])

        # Connect widget signals to callback functions.
        # self.txtIncidentDate.connect('focus_out_event', self._check_ready, 2)
        self.cmbReportedBy.connect('changed', self._check_ready, None, 2)
        self.cmbCategory.connect('changed', self._check_ready, None, 2)
        self.cmbHardware.connect('changed', self._check_ready, None, 2)
        self.cmbSoftware.connect('changed', self._check_ready, None, 2)
        self.cmbDetectMethod.connect('changed', self._check_ready, None, 2)

        self.assistant.append_page(self.fxdPageGeneral)
        self.assistant.set_page_type(self.fxdPageGeneral,
                                     gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(self.fxdPageGeneral, _(u"Program "
                                                             u"Incident: "
                                                             u"General "
                                                             u"Information"))

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the incident descriptions page.                            #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        self.txtDescription = _widg.make_entry(width=595)
        self.txtDetails = gtk.TextBuffer()
        self.txtRemarks = gtk.TextBuffer()

        # Assign tooltips to the widgets.
        self.txtDescription.set_tooltip_text(_(u"Enter a brief description of "
                                               u"the incident being "
                                               u"reported."))

        # Place the widgets.
        self.fxdPageDescription = gtk.Fixed()

        _label = _widg.make_label(_(u"Brief Description*"))
        _x_pos = _label.size_request()[0]
        self.fxdPageDescription.put(_label, 5, 5)

        _label = _widg.make_label(_(u"Detailed Description*"))
        self.fxdPageDescription.put(_label, 5, 35)

        _label = _widg.make_label(_(u"Remarks"))
        self.fxdPageDescription.put(_label, 5, 370)

        self.fxdPageDescription.put(self.txtDescription, _x_pos, 5)
        _textview = _widg.make_text_view(txvbuffer=self.txtDetails,
                                         width=795, height=300)
        _textview.set_tooltip_text(_(u"Enter a detailed description of the "
                                     u"incident being reported."))
        self.fxdPageDescription.put(_textview, 5, 65)

        _textview = _widg.make_text_view(txvbuffer=self.txtRemarks,
                                         width=795, height=150)
        _textview.set_tooltip_text(_(u"Enter any additional, pertinent "
                                     u"remarks related to the incident being "
                                     u"reported."))
        self.fxdPageDescription.put(_textview, 5, 400)

        self.txtDescription.connect('focus_out_event', self._check_ready, 3)
        self.txtDetails.connect('changed', self._check_ready, None, 3)

        self.assistant.append_page(self.fxdPageDescription)
        self.assistant.set_page_type(self.fxdPageDescription,
                                     gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(self.fxdPageDescription,
                                      _(u"Program Incident: Incident "
                                        u"Description"))

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the confirmation page.                                     #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()

        _label = _widg.make_label(_(u"Press 'Apply' to create the incident or "
                                    u"'Cancel' to quit the assistant without "
                                    u"adding the incident."),
                                  width=-1, height=-1, wrap=True)
        _fixed.put(_label, 5, 5)

        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed,
                                     gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(_fixed, _(u"Incident: Confirm Addition "
                                                u"of New Incident"))
        self.assistant.set_page_complete(_fixed, True)

        self.assistant.show_all()

        # hide the widgets that are specific to software unless a software
        # module is selected.
        self.cmbDetectMethod.set_sensitive(False)
        self.txtTestProcedure.set_sensitive(False)
        self.txtTestCase.set_sensitive(False)
        self.txtExecutionTime.set_sensitive(False)

    def _check_ready(self, __widget, __event=None, page=0):
        """
        Method to check if all the required data is filled in before allowing
        the assistant to continue.

        :param gtk.Widget __widget: the gtk.Widget() calling this method.
        :param gtk.gdk.Event __event: the gtk.gdkEvent() that called this
                                      method.
        :param int page: the page in the gtk.Assistant() to check.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if self.cmbSoftware.get_active() > 0:
            self.cmbDetectMethod.set_sensitive(True)
            self.txtTestProcedure.set_sensitive(True)
            self.txtTestCase.set_sensitive(True)
            self.txtExecutionTime.set_sensitive(True)
        else:
            self.cmbDetectMethod.set_sensitive(False)
            self.txtTestProcedure.set_sensitive(False)
            self.txtTestCase.set_sensitive(False)
            self.txtExecutionTime.set_sensitive(False)

        if page == 2 and self.cmbSoftware.get_active() <= 0:
            if(self.txtIncidentDate.get_text() != '' and
               self.cmbReportedBy.get_active_text() != '' and
               self.cmbCategory.get_active() > 0 and
               self.cmbHardware.get_active() > 0):
                self.assistant.set_page_complete(self.fxdPageGeneral, True)
            else:
                self.assistant.set_page_complete(self.fxdPageGeneral, False)
        elif page == 2 and self.cmbSoftware.get_active() > 0:
            if(self.txtIncidentDate.get_text() != '' and
               self.cmbReportedBy.get_active_text() != '' and
               self.cmbCategory.get_active() > 0 and
               self.cmbHardware.get_active() > 0 and
               self.cmbDetectMethod.get_active() > 0 and
               self.txtExecutionTime.get_text() != ''):
                self.assistant.set_page_complete(self.fxdPageGeneral, True)
            else:
                self.assistant.set_page_complete(self.fxdPageGeneral, False)
        elif page == 3:
            if(self.txtDescription.get_text() != '' and
               self.txtDetails.get_text(*self.txtDetails.get_bounds()) != ''):
                self.assistant.set_page_complete(self.fxdPageDescription, True)
            else:
                self.assistant.set_page_complete(self.fxdPageDescription,
                                                 False)

        return False

    def _add_incident(self, __assistant):
        """
        Method to add the new incident to the open RTK Program database.

        :param assistant: the gtk.Assistant() that represents the wizard.
        :type assistant: gtk.Assistant
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        _report_date = int(datetime.strptime(self.txtIncidentDate.get_text(),
                                             '%Y-%m-%d').toordinal())

        # Retrieve the hardware ID.
        _model = self.cmbHardware.get_model()
        _row = self.cmbHardware.get_active_iter()
        _hardware_id = int(_model.get_value(_row, 1))

        # Retrieve the software ID if reporting a software problem.
        _model = self.cmbSoftware.get_model()
        _row = self.cmbSoftware.get_active_iter()
        try:
            _software_id = int(_model.get_value(_row, 1))
        except TypeError:
            _software_id = 0

        # Retrieve the execution time if reporting a software problem.
        try:
            _execution_time = float(self.txtExecutionTime.get_text())
        except ValueError:
            _execution_time = 0.0

        _query = "INSERT INTO rtk_incident \
                  (fld_revision_id, fld_hardware_id, fld_sftwr_id, \
                   fld_incident_category, fld_incident_type, \
                   fld_short_description, fld_long_description, \
                   fld_criticality, fld_detection_method, fld_remarks, \
                   fld_status, fld_request_by, fld_request_date, \
                   fld_test_found, fld_test_case, fld_execution_time, \
                   fld_reviewed_date, fld_approved_date, fld_complete_date) \
                  VALUES (%d, %d, %d, %d, %d, '%s', '%s', %d, %d, '%s', 1, \
                          %d, %d, '%s', '%s', %f, %d, %d, %d)" % \
                 (self._revision_id, _hardware_id, _software_id,
                  self.cmbCategory.get_active(), self.cmbType.get_active(),
                  self.txtDescription.get_text(),
                  self.txtDetails.get_text(*self.txtDetails.get_bounds()),
                  self.cmbCriticality.get_active(),
                  self.cmbDetectMethod.get_active(),
                  self.txtRemarks.get_text(*self.txtRemarks.get_bounds()),
                  self.cmbReportedBy.get_active(), _report_date,
                  self.txtTestProcedure.get_text(),
                  self.txtTestCase.get_text(),
                  _execution_time, _report_date + 30, _report_date + 30,
                  _report_date + 30)
        (_results, _error_code, _last_id) = self._dao.execute(_query,
                                                              commit=True)

        # Reload the Incident class gtk.TreeView().
        self._modulebook.request_load_data(self._dao, self._revision_id)

        return False

    def _cancel(self, __button):
        """
        Method to destroy the gtk.Assistant() when the 'Cancel' button is
        pressed.

        :param __button: the gtk.Button() that called this method.
        :type __button: gtk.Button
        @return: True
        @rtype: boolean
        """

        self.assistant.destroy()

        return True


class AddComponents(object):
    """
    This is the gtk.Assistant() that guides the user through the process of
    adding an affected component to the selected program Incident.
    """

    def __init__(self, revision_id, incident_id, dao, controller, workbook):
        """
        Initialize an instance of the Add Component Assistant.

        :param int revision_id: the Revision ID to select the components for.
        :param int incident_id: the Incident ID to add the component to.
        :param dao: the :py:class:`rtk.dao.DAO` data access object used to
                    communicate with the open RTK Program database.
        :param controller: the :py:class:`rtk.incident.component.Component`
                           data controller managing the component list.
        :param workbook: the :py:class:`rtk.incident.WorkBook.WorkView`
                         associated with the selected incident.
        """

        self._incident_id = incident_id
        self._controller = controller
        self._workbook = workbook

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_(u"RTK Add Affected Component Assistant"))
        self.assistant.connect('apply', self._add_component)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

        # Create the introduction page.
        _fixed = gtk.Fixed()
        _label = _widg.make_label(_(u"This is the RTK incident affected "
                                    u"component assistant.  It will help you "
                                    u"add an affected component to the "
                                    u"currently selected program Incident.  "
                                    u"Press 'Forward' to continue or 'Cancel' "
                                    u"to quit the assistant."),
                                  width=-1, height=-1, wrap=True)
        _fixed.put(_label, 5, 5)
        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(_fixed, _(u"Introduction"))
        self.assistant.set_page_complete(_fixed, True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the incident information page.                             #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        self.cmbHardware = _widg.make_combo(simple=False)
        #self.cmbSoftware = _widg.make_combo(simple=False)

        # Load the gtk.ComboBox() widgets.
        _query = "SELECT fld_name, fld_hardware_id, fld_description \
                  FROM rtk_hardware \
                  WHERE fld_revision_id={0:d} \
                  AND fld_part=1".format(revision_id)
        (_results, _error_code, __) = dao.execute(_query, commit=False)
        _widg.load_combo(self.cmbHardware, _results, simple=False)

        # Create and place the labels.
        self.fxdPageGeneral = gtk.Fixed()

        _labels = [_(u"Select Component*:")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels,
                                             self.fxdPageGeneral, 5, 5)
        _x_pos += 40

        self.fxdPageGeneral.put(self.cmbHardware, _x_pos, _y_pos[0])

        # Connect widget signals to callback functions.
        self.cmbHardware.connect('changed', self._check_ready, None, 2)

        self.assistant.append_page(self.fxdPageGeneral)
        self.assistant.set_page_type(self.fxdPageGeneral,
                                     gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(self.fxdPageGeneral, _(u"Select "
                                                             u"Component"))

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the confirmation page.                                     #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()

        _label = _widg.make_label(_(u"Press 'Apply' to add the affected "
                                    u"component or 'Cancel' to quit the "
                                    u"assistant without adding the "
                                    u"component."),
                                  width=-1, height=-1, wrap=True)
        _fixed.put(_label, 5, 5)

        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed,
                                     gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(_fixed, _(u"Confirm Addition of the New "
                                                u"Component"))
        self.assistant.set_page_complete(_fixed, True)

        self.assistant.show_all()

    def _check_ready(self, __widget, __event=None, __page=0):
        """
        Method to check if all the required data is filled in before allowing
        the assistant to continue.

        :param gtk.Widget __widget: the gtk.Widget() calling this method.
        :param gtk.gdk.Event __event: the gtk.gdkEvent() that called this
                                      method.
        :param int page: the page in the gtk.Assistant() to check.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if self.cmbHardware.get_active() > 0:
            self.assistant.set_page_complete(self.fxdPageGeneral, True)
        else:
            self.assistant.set_page_complete(self.fxdPageGeneral, False)

        return False

    def _add_component(self, __assistant):
        """
        Method to add the new incident to the open RTK Program database.

        :param gtk.Assistant __assistant: the gtk.Assistant() that represents
                                          the wizard.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Retrieve the hardware ID.
        _model = self.cmbHardware.get_model()
        _row = self.cmbHardware.get_active_iter()
        _hardware_id = int(_model.get_value(_row, 1))

        self._controller.add_component(self._incident_id, _hardware_id)
        self._workbook.load_component_list()

        return False

    def _cancel(self, __button):
        """
        Method to destroy the gtk.Assistant() when the 'Cancel' button is
        pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :return: True
        :rtype: boolean
        """

        self.assistant.destroy()

        return True


class FilterIncident(object):
    """
    This is the gtk.Assistant that walks the user through the process of
    filtering program incident records in the open RTK Program database.
    """

    # Lists of search criteria to use for the various gtk.Combo widgets.
    _criteria0 = [["="], ["!="], [">"], ["<"], [">="], ["<="],
                  [_("LIKE")], [_("NOT LIKE")]]
    _criteria1 = [[_("LIKE")], [_("NOT LIKE")]]
    _criteria2 = [["="], ["!="], [">"], ["<"], [">="], ["<="]]
    _criteria3 = [["="], ["!="]]

    _compound = [[_("AND")], [_("OR")]]

    _fi_tab_labels = [[_("Incident ID:"), _("Incident Category:"),
                       _("Incident Type:"), _("Incident Status:"),
                       _("Incident Criticality:"), _("Incident Age:"),
                       _("Incident Lifecycle:"), _("Affected Assembly:")],
                      [_("Short Description:"), _("Long Description:"),
                       _("Remarks:"), _("Analysis:")],
                      [_("Found in Test:"), _("Found in Test Case:")],
                      [_("Requested By:"), _("Requested Date:"),
                       _("Reviewed By:"), _("Reviewed Date:"),
                       _("Approved By:"), _("Approved Date:"),
                       _("Closed By:"), _("Closed Date:")]]

    def __init__(self, revision_id, modulebook):
        """
        Method to initialize the Program Incident Filter Assistant.

        :param int revision_id: the revision ID to select the filtered
                                incidents for.
        :param modulebook: the :py:class:`rtk.Incident.ModuleBook` to add the
                           the new incident to.
        """

        self._revision_id = revision_id
        self._modulebook = modulebook

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_("RTK Filter Incidents Assistant"))
        self.assistant.connect('apply', self._filter)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

        # Create the introduction page.
        fixed = gtk.Fixed()
        _text_ = _("This is the RTK incident filter assistant.\n\nIt will help you filter program incidents in the database so you can view only those you're interested in seeing.\n\nPress 'Forward' to continue or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=600, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(fixed, _("Introduction"))
        self.assistant.set_page_complete(fixed, True)

        # Create the gtk.Combo widgets that will be used to select compounding
        # statements (i.e., AND, OR).
        self.cmbCompound1 = _widg.make_combo(width=75)
        self.cmbCompound2 = _widg.make_combo(width=75)
        self.cmbCompound3 = _widg.make_combo(width=75)
        self.cmbCompound4 = _widg.make_combo(width=75)
        self.cmbCompound5 = _widg.make_combo(width=75)
        self.cmbCompound6 = _widg.make_combo(width=75)
        self.cmbCompound7 = _widg.make_combo(width=75)
        self.cmbCompound8 = _widg.make_combo(width=75)
        self.cmbCompound9 = _widg.make_combo(width=75)
        self.cmbCompound10 = _widg.make_combo(width=75)
        self.cmbCompound11 = _widg.make_combo(width=75)
        self.cmbCompound12 = _widg.make_combo(width=75)
        self.cmbCompound13 = _widg.make_combo(width=75)
        self.cmbCompound14 = _widg.make_combo(width=75)
        self.cmbCompound15 = _widg.make_combo(width=75)
        self.cmbCompound16 = _widg.make_combo(width=75)
        self.cmbCompound17 = _widg.make_combo(width=75)
        self.cmbCompound18 = _widg.make_combo(width=75)
        self.cmbCompound19 = _widg.make_combo(width=75)
        self.cmbCompound20 = _widg.make_combo(width=75)
        self.cmbCompound21 = _widg.make_combo(width=75)
        self.cmbCompound22 = _widg.make_combo(width=75)
        self.cmbCompound23 = _widg.make_combo(width=75)
        _widg.load_combo(self.cmbCompound1, self._compound)
        _widg.load_combo(self.cmbCompound2, self._compound)
        _widg.load_combo(self.cmbCompound3, self._compound)
        _widg.load_combo(self.cmbCompound4, self._compound)
        _widg.load_combo(self.cmbCompound5, self._compound)
        _widg.load_combo(self.cmbCompound6, self._compound)
        _widg.load_combo(self.cmbCompound7, self._compound)
        _widg.load_combo(self.cmbCompound8, self._compound)
        _widg.load_combo(self.cmbCompound9, self._compound)
        _widg.load_combo(self.cmbCompound10, self._compound)
        _widg.load_combo(self.cmbCompound11, self._compound)
        _widg.load_combo(self.cmbCompound12, self._compound)
        _widg.load_combo(self.cmbCompound13, self._compound)
        _widg.load_combo(self.cmbCompound14, self._compound)
        _widg.load_combo(self.cmbCompound15, self._compound)
        _widg.load_combo(self.cmbCompound16, self._compound)
        _widg.load_combo(self.cmbCompound17, self._compound)
        _widg.load_combo(self.cmbCompound18, self._compound)
        _widg.load_combo(self.cmbCompound19, self._compound)
        _widg.load_combo(self.cmbCompound20, self._compound)
        _widg.load_combo(self.cmbCompound21, self._compound)
        _widg.load_combo(self.cmbCompound22, self._compound)
        _widg.load_combo(self.cmbCompound23, self._compound)

        # Create the page to select filter criteria related to the type,
        # category, status, criticality, and age of the incident.
        self.cmbCriteriaID = _widg.make_combo(width=100)
        self.txtFilterID = _widg.make_entry(width=100)
        self.cmbCriteriaCategory = _widg.make_combo(width=100)
        self.cmbFilterCategory = _widg.make_combo(width=100)
        self.cmbCriteriaType = _widg.make_combo(width=100)
        self.cmbFilterType = _widg.make_combo(width=100)
        self.cmbCriteriaStatus = _widg.make_combo(width=100)
        self.cmbFilterStatus = _widg.make_combo(width=100)
        self.cmbCriteriaCriticality = _widg.make_combo(width=100)
        self.cmbFilterCriticality = _widg.make_combo(width=100)
        self.cmbCriteriaAge = _widg.make_combo(width=100)
        self.txtFilterAge = _widg.make_entry(width=100)
        self.cmbCriteriaLifeCycle = _widg.make_combo(width=100)
        self.cmbFilterLifeCycle = _widg.make_combo(width=100)
        self.cmbCriteriaAssembly = _widg.make_combo(width=100)
        self.cmbAssembly = _widg.make_combo(width=100, simple=False)

        # Load the gtk.ComboBox().
        _widg.load_combo(self.cmbCriteriaID, self._criteria2)

        _widg.load_combo(self.cmbCriteriaCategory, self._criteria3)
        self.cmbFilterCategory.append_text("")
        for i in range(len(_conf.RTK_INCIDENT_CATEGORY)):
            self.cmbFilterCategory.append_text(_conf.RTK_INCIDENT_CATEGORY[i])

        _widg.load_combo(self.cmbCriteriaType, self._criteria3)
        self.cmbFilterType.append_text("")
        for i in range(len(_conf.RTK_INCIDENT_TYPE)):
            self.cmbFilterType.append_text(_conf.RTK_INCIDENT_TYPE[i])

        _widg.load_combo(self.cmbCriteriaStatus, self._criteria3)

        _widg.load_combo(self.cmbCriteriaCriticality, self._criteria3)
        self.cmbFilterCriticality.append_text("")
        for i in range(len(_conf.RTK_INCIDENT_CRITICALITY)):
            self.cmbFilterCriticality.append_text(
                _conf.RTK_INCIDENT_CRITICALITY[i])

        _widg.load_combo(self.cmbCriteriaAge, self._criteria2)

        _widg.load_combo(self.cmbCriteriaLifeCycle, self._criteria2)
        self.cmbFilterLifeCycle.append_text("")
        for i in range(len(_conf.RTK_LIFECYCLE)):
            self.cmbFilterLifeCycle.append_text(_conf.RTK_LIFECYCLE[i])

        _widg.load_combo(self.cmbCriteriaAssembly, self._criteria3)
        _widg.load_combo(self.cmbAssembly, _conf.RTK_HARDWARE_LIST,
                         simple=False)

        # Set the tooltips.
        self.txtFilterID.set_tooltip_text(_(u"Sets the incident ID filter "
                                            u"criterion."))
        self.cmbFilterCategory.set_tooltip_text(_(u"Sets the incident "
                                                  u"category filter "
                                                  u"criterion."))
        self.cmbFilterType.set_tooltip_text(_(u"Sets the incident type filter "
                                              u"criterion."))
        self.cmbFilterStatus.set_tooltip_text(_(u"Sets the incident status "
                                                u"filter criterion."))
        self.cmbFilterCriticality.set_tooltip_text(_(u"Sets the incident "
                                                     u"criticality filter "
                                                     u"criterion."))
        self.txtFilterAge.set_tooltip_text(_(u"Sets the incident age filter "
                                             u"criterion."))
        self.cmbFilterLifeCycle.set_tooltip_text(_(u"Sets the incident life "
                                                   u"cycle filter criterion."))
        self.cmbAssembly.set_tooltip_text(_(u"Sets the affected assembly "
                                            u"filter criterion."))

        fixed = gtk.Fixed()

        y_pos = 5
        for i in range(len(self._fi_tab_labels[0])):
            label = _widg.make_label(self._fi_tab_labels[0][i], 150, 25)
            fixed.put(label, 5, (35 * i + y_pos))

        fixed.put(self.cmbCriteriaID, 190, y_pos)
        fixed.put(self.txtFilterID, 300, y_pos)
        fixed.put(self.cmbCompound1, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaCategory, 190, y_pos)
        fixed.put(self.cmbFilterCategory, 300, y_pos)
        fixed.put(self.cmbCompound2, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaType, 190, y_pos)
        fixed.put(self.cmbFilterType, 300, y_pos)
        fixed.put(self.cmbCompound3, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaStatus, 190, y_pos)
        fixed.put(self.cmbFilterStatus, 300, y_pos)
        fixed.put(self.cmbCompound4, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaCriticality, 190, y_pos)
        fixed.put(self.cmbFilterCriticality, 300, y_pos)
        fixed.put(self.cmbCompound5, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaAge, 190, y_pos)
        fixed.put(self.txtFilterAge, 300, y_pos)
        fixed.put(self.cmbCompound6, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaLifeCycle, 190, y_pos)
        fixed.put(self.cmbFilterLifeCycle, 300, y_pos)
        fixed.put(self.cmbCompound7, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaAssembly, 190, y_pos)
        fixed.put(self.cmbAssembly, 300, y_pos)
        fixed.put(self.cmbCompound23, 410, y_pos)

        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(fixed, _("Set Filter Criteria: Incident Details"))
        self.assistant.set_page_complete(fixed, True)

        # Create the page to select filter criteria related to the short
        # description, long description, remarks, and analysis of the incident.
        self.cmbCriteriaShortDesc = _widg.make_combo(width=100)
        _widg.load_combo(self.cmbCriteriaShortDesc, self._criteria1)
        self.txtFilterShortDesc = _widg.make_entry(width=100)
        self.txtFilterShortDesc.set_tooltip_text(_(u"Sets the field incident "
                                                   u"short description filter "
                                                   u"criterion."))

        self.cmbCriteriaLongDesc = _widg.make_combo(width=100)
        _widg.load_combo(self.cmbCriteriaLongDesc, self._criteria1)
        self.txtFilterLongDesc = _widg.make_entry(width=100)
        self.txtFilterLongDesc.set_tooltip_text(_(u"Sets the incident long "
                                                  u"description filter "
                                                  u"criterion."))

        self.cmbCriteriaRemarks = _widg.make_combo(width=100)
        _widg.load_combo(self.cmbCriteriaRemarks, self._criteria1)
        self.txtFilterRemarks = _widg.make_entry(width=100)
        self.txtFilterRemarks.set_tooltip_text(_(u"Sets the incident closure "
                                                 u"remarks filter criterion."))

        self.cmbCriteriaAnalysis = _widg.make_combo(width=100)
        _widg.load_combo(self.cmbCriteriaAnalysis, self._criteria1)
        self.txtFilterAnalysis = _widg.make_entry(width=100)
        self.txtFilterAnalysis.set_tooltip_text(_(u"Sets the incident "
                                                  u"analysis filter "
                                                  u"criterion."))

        fixed = gtk.Fixed()

        y_pos = 5
        for i in range(len(self._fi_tab_labels[1])):
            label = _widg.make_label(self._fi_tab_labels[1][i], 150, 25)
            fixed.put(label, 5, (35 * i + y_pos))

        fixed.put(self.cmbCriteriaShortDesc, 190, y_pos)
        fixed.put(self.txtFilterShortDesc, 300, y_pos)
        fixed.put(self.cmbCompound8, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaLongDesc, 190, y_pos)
        fixed.put(self.txtFilterLongDesc, 300, y_pos)
        fixed.put(self.cmbCompound9, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaRemarks, 190, y_pos)
        fixed.put(self.txtFilterRemarks, 300, y_pos)
        fixed.put(self.cmbCompound10, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaAnalysis, 190, y_pos)
        fixed.put(self.txtFilterAnalysis, 300, y_pos)
        fixed.put(self.cmbCompound11, 410, y_pos)
        y_pos += 35

        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(fixed, _("Set Filter Criteria: Descriptions, Remarks, and Analysis"))
        self.assistant.set_page_complete(fixed, True)

        # Create the page to select filter criteria related to the test and
        # test case that discovered the problem reported in the incident.
        self.cmbCriteriaTest = _widg.make_combo(width=100)
        _widg.load_combo(self.cmbCriteriaTest, self._criteria1)
        self.txtFilterTest = _widg.make_entry(width=100)
        self.txtFilterTest.set_tooltip_text(_(u"Sets the incident test filter "
                                              u"criterion."))

        self.cmbCriteriaTestCase = _widg.make_combo(width=100)
        _widg.load_combo(self.cmbCriteriaTestCase, self._criteria1)
        self.txtFilterTestCase = _widg.make_entry(width=100)
        self.txtFilterTestCase.set_tooltip_text(_(u"Sets the incident test "
                                                  u"case filter criterion."))

        fixed = gtk.Fixed()

        y_pos = 5
        for i in range(len(self._fi_tab_labels[2])):
            label = _widg.make_label(self._fi_tab_labels[2][i], 150, 25)
            fixed.put(label, 5, (35 * i + y_pos))

        fixed.put(self.cmbCriteriaTest, 190, y_pos)
        fixed.put(self.txtFilterTest, 300, y_pos)
        fixed.put(self.cmbCompound12, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaTestCase, 190, y_pos)
        fixed.put(self.txtFilterTestCase, 300, y_pos)
        fixed.put(self.cmbCompound13, 410, y_pos)
        y_pos += 35

        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(fixed, _(u"Set Filter Criteria: Test "
                                               u"Information"))
        self.assistant.set_page_complete(fixed, True)

        # Create the page to select filter criteria reliated to the request by,
        # request date, reviewed by, reviewed date, approved by, approved date,
        # closed by, and closed date of the incident.
        self.cmbCriteriaRequestBy = _widg.make_combo(width=100)
        self.cmbFilterRequestBy = _widg.make_combo(width=100)
        self.cmbCriteriaRequestDate = _widg.make_combo(width=100)
        self.txtFilterRequestDate = _widg.make_entry(width=100)
        self.cmbCriteriaReviewBy = _widg.make_combo(width=100)
        self.cmbFilterReviewBy = _widg.make_combo(width=100)
        self.cmbCriteriaReviewDate = _widg.make_combo(width=100)
        self.txtFilterReviewDate = _widg.make_entry(width=100)
        self.cmbCriteriaApproveBy = _widg.make_combo(width=100)
        self.cmbFilterApproveBy = _widg.make_combo(width=100)
        self.cmbCriteriaApproveDate = _widg.make_combo(width=100)
        self.txtFilterApproveDate = _widg.make_entry(width=100)
        self.cmbCriteriaCloseBy = _widg.make_combo(width=100)
        self.cmbFilterCloseBy = _widg.make_combo(width=100)
        self.cmbCriteriaCloseDate = _widg.make_combo(width=100)
        self.txtFilterCloseDate = _widg.make_entry(width=100)
        self.chkFilterAccepted = _widg.make_check_button(label=_(u"Is Accepted"))
        self.chkFilterReviewed = _widg.make_check_button(label=_(u"Is Reviewed"))

        # Load the gtk.ComboBox.
        _widg.load_combo(self.cmbCriteriaRequestBy, self._criteria3)
        self.cmbFilterRequestBy.append_text("")
        for i in range(len(_conf.RTK_USERS)):
            self.cmbFilterRequestBy.append_text(_conf.RTK_USERS[i])

        _widg.load_combo(self.cmbCriteriaRequestDate, self._criteria2)

        _widg.load_combo(self.cmbCriteriaReviewBy, self._criteria3)
        self.cmbFilterReviewBy.append_text("")
        for i in range(len(_conf.RTK_USERS)):
            self.cmbFilterReviewBy.append_text(_conf.RTK_USERS[i])

        _widg.load_combo(self.cmbCriteriaReviewDate, self._criteria2)

        _widg.load_combo(self.cmbCriteriaApproveBy, self._criteria3)
        self.cmbFilterApproveBy.append_text("")
        for i in range(len(_conf.RTK_USERS)):
            self.cmbFilterApproveBy.append_text(_conf.RTK_USERS[i])

        _widg.load_combo(self.cmbCriteriaApproveDate, self._criteria2)

        _widg.load_combo(self.cmbCriteriaCloseBy, self._criteria3)
        self.cmbFilterCloseBy.append_text("")
        for i in range(len(_conf.RTK_USERS)):
            self.cmbFilterCloseBy.append_text(_conf.RTK_USERS[i])

        _widg.load_combo(self.cmbCriteriaCloseDate, self._criteria2)

        # Set the tooltips
        self.cmbFilterRequestBy.set_tooltip_text(_(u"Sets the incident "
                                                   u"requested by filter "
                                                   u"criterion."))
        self.txtFilterRequestDate.set_tooltip_text(_(u"Sets the incident "
                                                     u"requested date filter "
                                                     u"criterion."))
        self.cmbFilterReviewBy.set_tooltip_text(_(u"Sets the incident "
                                                  u"reviewed by filter "
                                                  u"criterion."))
        self.txtFilterReviewDate.set_tooltip_text(_(u"Sets the incident "
                                                    u"reviewed date filter "
                                                    u"criterion."))
        self.cmbFilterApproveBy.set_tooltip_text(_(u"Sets the incident "
                                                   u"approved by filter "
                                                   u"criterion."))
        self.txtFilterApproveDate.set_tooltip_text(_(u"Sets the incident "
                                                     u"approved date filter "
                                                     u"criterion."))
        self.cmbFilterCloseBy.set_tooltip_text(_(u"Sets the incident closed "
                                                 u"by filter criterion."))
        self.txtFilterCloseDate.set_tooltip_text(_(u"Sets the incident closed "
                                                   u"date filter criterion."))
        self.chkFilterAccepted.set_tooltip_text(_(u"Only return accepted or "
                                                  u"unaccepted incidents."))
        self.chkFilterReviewed.set_tooltip_text(_(u"Only return reviewed or "
                                                  u"unreviewed incidents."))

        fixed = gtk.Fixed()

        y_pos = 5
        for i in range(len(self._fi_tab_labels[3])):
            label = _widg.make_label(self._fi_tab_labels[3][i], 150, 25)
            fixed.put(label, 5, (35 * i + y_pos))

        fixed.put(self.cmbCriteriaRequestBy, 190, y_pos)
        fixed.put(self.cmbFilterRequestBy, 300, y_pos)
        fixed.put(self.cmbCompound14, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaRequestDate, 190, y_pos)
        fixed.put(self.txtFilterRequestDate, 300, y_pos)
        fixed.put(self.cmbCompound15, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaReviewBy, 190, y_pos)
        fixed.put(self.cmbFilterReviewBy, 300, y_pos)
        fixed.put(self.cmbCompound16, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaReviewDate, 190, y_pos)
        fixed.put(self.txtFilterReviewDate, 300, y_pos)
        fixed.put(self.cmbCompound17, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaApproveBy, 190, y_pos)
        fixed.put(self.cmbFilterApproveBy, 300, y_pos)
        fixed.put(self.cmbCompound18, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaApproveDate, 190, y_pos)
        fixed.put(self.txtFilterApproveDate, 300, y_pos)
        fixed.put(self.cmbCompound19, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaCloseBy, 190, y_pos)
        fixed.put(self.cmbFilterCloseBy, 300, y_pos)
        fixed.put(self.cmbCompound20, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbCriteriaCloseDate, 190, y_pos)
        fixed.put(self.txtFilterCloseDate, 300, y_pos)
        fixed.put(self.cmbCompound21, 410, y_pos)
        y_pos += 35

        fixed.put(self.chkFilterAccepted, 190, y_pos)
        fixed.put(self.cmbCompound22, 300, y_pos)
        fixed.put(self.chkFilterReviewed, 410, y_pos)

        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(fixed, _(u"Set Filter Criteria: People and Dates"))
        self.assistant.set_page_complete(fixed, True)

        # Create the page to apply the filter criteria.
        _fixed = gtk.Fixed()
        _text = _(u"Press 'Apply' to apply the filter criteria or 'Cancel' to quit the assistant.")
        _label = _widg.make_label(_text, width=600, height=150)
        _fixed.put(_label, 5, 5)
        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(_fixed, _(u"Apply Filter Criteria"))
        self.assistant.set_page_complete(_fixed, True)

        self.assistant.show_all()

    def _filter(self, __button):
        """
        Method to create the SQL query for filtering the Program Incidents.

        :param gtk.Button __button: the gtk.Button() that called this method.
        """

        _criteria = []
        _inputs = []
        _compound = []

        # Read the user inputs for the different fields that can be used to
        # filter with.
        _criteria.append(self.cmbCriteriaID.get_active_text())
        _inputs.append(self.txtFilterID.get_text())
        _compound.append(self.cmbCompound1.get_active_text())

        _criteria.append(self.cmbCriteriaCategory.get_active_text())
        _inputs.append(self.cmbFilterCategory.get_active())
        _compound.append(self.cmbCompound2.get_active_text())

        _criteria.append(self.cmbCriteriaType.get_active_text())
        _inputs.append(self.cmbFilterType.get_active())
        _compound.append(self.cmbCompound3.get_active_text())

        _criteria.append(self.cmbCriteriaStatus.get_active_text())
        _inputs.append(self.cmbFilterStatus.get_active())
        _compound.append(self.cmbCompound4.get_active_text())

        _criteria.append(self.cmbCriteriaCriticality.get_active_text())
        _inputs.append(self.cmbFilterCriticality.get_active())
        _compound.append(self.cmbCompound5.get_active_text())

        _criteria.append(self.cmbCriteriaAge.get_active_text())
        _inputs.append(self.txtFilterAge.get_text())
        _compound.append(self.cmbCompound6.get_active_text())

        _criteria.append(self.cmbCriteriaLifeCycle.get_active_text())
        _inputs.append(self.cmbFilterLifeCycle.get_active())
        _compound.append(self.cmbCompound7.get_active_text())

        _criteria.append(self.cmbCriteriaShortDesc.get_active_text())
        _inputs.append(self.txtFilterShortDesc.get_text())
        _compound.append(self.cmbCompound8.get_active_text())

        _criteria.append(self.cmbCriteriaLongDesc.get_active_text())
        _inputs.append(self.txtFilterLongDesc.get_text())
        _compound.append(self.cmbCompound9.get_active_text())

        _criteria.append(self.cmbCriteriaRemarks.get_active_text())
        _inputs.append(self.txtFilterRemarks.get_text())
        _compound.append(self.cmbCompound10.get_active_text())

        _criteria.append(self.cmbCriteriaAnalysis.get_active_text())
        _inputs.append(self.txtFilterAnalysis.get_text())
        _compound.append(self.cmbCompound11.get_active_text())

        _criteria.append(self.cmbCriteriaTest.get_active_text())
        _inputs.append(self.txtFilterTest.get_text())
        _compound.append(self.cmbCompound12.get_active_text())

        _criteria.append(self.cmbCriteriaTestCase.get_active_text())
        _inputs.append(self.txtFilterTestCase.get_text())
        _compound.append(self.cmbCompound13.get_active_text())

        _criteria.append(self.cmbCriteriaRequestBy.get_active_text())
        _inputs.append(self.cmbFilterRequestBy.get_active_text())
        _compound.append(self.cmbCompound14.get_active_text())

        _criteria.append(self.cmbCriteriaRequestDate.get_active_text())
        _inputs.append(self.txtFilterRequestDate.get_text())
        _compound.append(self.cmbCompound15.get_active_text())

        _criteria.append(self.cmbCriteriaReviewBy.get_active_text())
        _inputs.append(self.cmbFilterReviewBy.get_active_text())
        _compound.append(self.cmbCompound16.get_active_text())

        _criteria.append(self.cmbCriteriaReviewDate.get_active_text())
        _inputs.append(self.txtFilterReviewDate.get_text())
        _compound.append(self.cmbCompound17.get_active_text())

        _criteria.append(self.cmbCriteriaApproveBy.get_active_text())
        _inputs.append(self.cmbFilterApproveBy.get_active_text())
        _compound.append(self.cmbCompound18.get_active_text())

        _criteria.append(self.cmbCriteriaApproveDate.get_active_text())
        _inputs.append(self.txtFilterApproveDate.get_text())
        _compound.append(self.cmbCompound19.get_active_text())

        _criteria.append(self.cmbCriteriaCloseBy.get_active_text())
        _inputs.append(self.cmbFilterCloseBy.get_active_text())
        _compound.append(self.cmbCompound20.get_active_text())

        _criteria.append(self.cmbCriteriaCloseDate.get_active_text())
        _inputs.append(self.txtFilterCloseDate.get_text())
        _compound.append(self.cmbCompound21.get_active_text())

        _inputs.append(self.chkFilterAccepted.get_active())
        _compound.append(self.cmbCompound22.get_active_text())

        _inputs.append(self.chkFilterReviewed.get_active())

        _criteria.append(self.cmbCriteriaAssembly.get_active_text())
        _model = self.cmbAssembly.get_model()
        _row = self.cmbAssembly.get_active_iter()
        if _row is not None:
            _text = int(_model.get_value(_row, 1))
        else:
            _text = 0
        _inputs.append(_text)
        _compound.append(self.cmbCompound23.get_active_text())

        # Build the query from the user-provided inputs.
        if all(_c is None for _c in _criteria):
            query = None
        elif _conf.RTK_MODULES[0] == 1:
            query = "SELECT * FROM rtk_incident \
                     WHERE fld_revision_id=%d AND " % \
            self._revision_id
        else:
            query = "SELECT * FROM rtk_incident \
                     WHERE fld_revision_id=0 AND "

        if _criteria[0] is not None and _criteria[0] != '':
            query = query + "fld_incident_id" + _criteria[0] + _inputs[0]
        if _compound[0] is not None and _compound[0] != '':
            query = query + " " + _compound[0] + " "

        if _criteria[1] is not None and _criteria[1] != '':
            query = query + "fld_incident_category" + _criteria[1] + \
                    str(_inputs[1])
        if _compound[1] is not None and _compound[1] != '':
            query = query + " " + _compound[1] + " "

        if _criteria[2] is not None and _criteria[2] != '':
            query = query + "fld_incident_type" + _criteria[2] + \
                    str(_inputs[2])
        if _compound[2] is not None and _compound[2] != '':
            query = query + " " + _compound[2] + " "

        if _criteria[3] is not None and _criteria[3] != '':
            query = query + "fld_status" + _criteria[3] + str(_inputs[3])
        if _compound[3] is not None and _compound[3] != '':
            query = query + " " + _compound[3] + " "

        if _criteria[4] is not None and _criteria[4] != '':
            query = query + "fld_criticality" + _criteria[4] + str(_inputs[4])
        if _compound[4] is not None and _compound[4] != '':
            query = query + " " + _compound[4] + " "

        if _criteria[5] is not None and _criteria[5] != '':
            query = query + "fld_incident_age" + _criteria[5] + str(_inputs[5])
        if _compound[5] is not None and _compound[5] != '':
            query = query + " " + _compound[5] + " "

        if _criteria[6] is not None and _criteria[6] != '':
            query = query + "fld_life_cycle" + _criteria[6] + str(_inputs[6])
        if _compound[6] is not None and _compound[6] != '':
            query = query + " " + _compound[6] + " "

        if _criteria[21] is not None and _criteria[21] != '':
            query = query + "fld_hardware_id" + _criteria[21] + \
                    str(_inputs[23])
        if _compound[22] is not None and _compound[22] != '':
            query = query + " " + _compound[22] + " "

        if _criteria[7] is not None and _criteria[7] != '':
            query = query + "fld_short_description " + _criteria[7] + \
                    " '%" + _inputs[7] + "%'"
        if _compound[7] is not None and _compound[7] != '':
            query = query + " " + _compound[7] + " "

        if _criteria[8] is not None and _criteria[8] != '':
            query = query + "fld_long_description " + _criteria[8] + \
                    " '%" + _inputs[8] + "%'"
        if _compound[8] is not None and _compound[8] != '':
            query = query + " " + _compound[8] + " "

        if _criteria[9] is not None and _criteria[9] != '':
            query = query + "fld_remarks " + _criteria[9] + \
                    " '%" + _inputs[9] + "%'"
        if _compound[9] is not None and _compound[9] != '':
            query = query + " " + _compound[9] + " "

        if _criteria[10] is not None and _compound[10] != '':
            query = query + "fld_analysis " + _criteria[10] + \
                    " '%" + _inputs[10] + "%'"
        if _compound[10] is not None and _compound[10] != '':
            query = query + " " + _compound[10] + " "

        if _criteria[11] is not None and _compound[11] != '':
            query = query + "fld_test_found " + _criteria[11] + \
                    " '%" + _inputs[11] + "%'"
        if _compound[11] is not None and _compound[11] != '':
            query = query + " " + _compound[11] + " "

        if _criteria[12] is not None and _compound[12] != '':
            query = query + "fld_test_case " + _criteria[12] + \
                    " '%" + _inputs[12] + "%'"
        if _compound[12] is not None and _compound[12] != '':
            query = query + " " + _compound[12] + " "

        if _criteria[13] is not None and _compound[13] != '':
            query = query + "fld_request_by" + _criteria[13] + \
                    "'" + _inputs[13] + "'"
        if _compound[13] is not None and _compound[13] != '':
            query = query + " " + _compound[13] + " "

        if _criteria[14] is not None and _compound[14] != '':
            query = query + "fld_request_date" + _criteria[14] + \
                    str(datetime.strptime(_inputs[14], "%Y-%m-%d").toordinal())
        if _compound[14] is not None and _compound[14] != '':
            query = query + " " + _compound[14] + " "

        if _criteria[15] is not None and _compound[15] != '':
            query = query + "fld_reviewed_by" + _criteria[15] + \
                    "'" + _inputs[15] + "'"
        if _compound[15] is not None and _compound[15] != '':
            query = query + " " + _compound[15] + " "

        if _criteria[16] is not None and _compound[16] != '':
            query = query + "fld_reviewed_date" + _criteria[16] + \
                    str(datetime.strptime(_inputs[16], "%Y-%m-%d").toordinal())
        if _compound[16] is not None and _compound[16] != '':
            query = query + " " + _compound[16] + " "

        if _criteria[17] is not None and _compound[17] != '':
            query = query + "fld_approved_by" + _criteria[17] + \
                    "'" + _inputs[17] + "'"
        if _compound[17] is not None and _compound[17] != '':
            query = query + " " + _compound[17] + " "

        if _criteria[18] is not None and _compound[18] != '':
            query = query + "fld_approved_date" + _criteria[18] + \
                    str(datetime.strptime(_inputs[18], "%Y-%m-%d").toordinal())
        if _compound[18] is not None and _compound[18] != '':
            query = query + " " + _compound[18] + " "

        if _criteria[19] is not None and _compound[19] != '':
            query = query + "fld_complete_by" + _criteria[19] + \
                    "'" + _inputs[19] + "'"
        if _compound[19] is not None and _compound[19] != '':
            query = query + " " + _compound[19] + " "

        if _criteria[20] is not None and _compound[20] != '':
            query = query + "fld_complete_date" + _criteria[20] + \
                    str(datetime.strptime(_inputs[20], "%Y-%m-%d").toordinal())
        if _compound[20] is not None and _compound[20] != '':
            query = query + " " + _compound[20] + " "

        if _inputs[21]:
            query = query + "fld_accepted=%d" % 1
        if _compound[21] is not None and _compound[21] != '':
            query = query + " " + _compound[21] + " "

        if _inputs[22]:
            query = query + "fld_reviewed=%d" % 1

        self._modulebook.request_filter_incidents(self._revision_id, query)

    def _cancel(self, __button):
        """
        Method to destroy the gtk.Assistant when the 'Cancel' button is
        pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        """

        self.assistant.destroy()


class ImportIncident(gtk.Assistant):
    """
    This is the gtk.Assistant() that walks the user through the process of
    importing program incident records to the open RTK Program database.
    """

    def __init__(self, revision_id, dao, modulebook):
        """
        Initialize an instance of the Import Incident Assistant.
        """

        self._dao = dao
        self._revision_id = revision_id
        self._modulebook = modulebook

        gtk.Assistant.__init__(self)
        self.set_title(_(u"RTK Import Incidents Assistant"))
        self.connect('apply', self._import)
        self.connect('cancel', self._cancel)
        self.connect('close', self._cancel)

        # Initialize some variables.
        self._file_index = [-1] * 76

        # Create the introduction page.
        _fixed = gtk.Fixed()
        _label = _widg.make_label(_(u"This is the RTK incident import "
                                    u"assistant.  It will help you import "
                                    u"program incidents to the database from "
                                    u"external files.  Press 'Forward' to "
                                    u"continue or 'Cancel' to quit the "
                                    u"assistant."), width=600, height=-1,
                                  wrap=True)
        _fixed.put(_label, 5, 5)
        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.set_page_title(_fixed, _(u"Introduction"))
        self.set_page_complete(_fixed, True)

        # Create the gtk.TreeView to map input file fields to database fields.
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING)
        self.tvwFileFields = gtk.TreeView(_model)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwFileFields)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('background', 'light gray')
        _column = gtk.TreeViewColumn()
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)
        _column.set_resizable(True)
        _column.set_visible(False)
        self.tvwFileFields.append_column(_column)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('background', 'light gray')
        _column = gtk.TreeViewColumn()
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=1)
        _column.set_resizable(True)
        _label = gtk.Label(_column.get_title())
        _label.set_line_wrap(True)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_markup("<span weight='bold'>{0:s}</span>".format(_(u"Database\nField")))
        _label.show_all()
        _column.set_widget(_label)
        self.tvwFileFields.append_column(_column)

        _title = _(u"RTK: Import Hardware from File ...")
        (_file_fields,
         self._file_contents) = _util.select_source_file(self, _title)
        if len(_file_fields) == 0:
            _util.rtk_information(_(u"Source file must have headings for each "
                                    u"column of data.  Please add headings to "
                                    u"the source file and try again."))
            self._cancel()
        if len(self._file_contents) == 0:
            _util.rtk_warning(_(u"No data was found in the source file.  "
                                u"Please check the contents of the source "
                                u"file and try again."))
            self._cancel()

        _cell = gtk.CellRendererCombo()
        _cellmodel = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT)
        _cellmodel.append(["", -1])
        for i in range(len(_file_fields)):
            _cellmodel.append([_file_fields[i], i])

        _cell.set_property('editable', 1)
        _cell.set_property('has-entry', False)
        _cell.set_property('model', _cellmodel)
        _cell.set_property('text-column', 0)

        _column = gtk.TreeViewColumn()
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=2)
        _column.set_resizable(True)
        _label = gtk.Label(_column.get_title())
        _label.set_line_wrap(True)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_markup("<span weight='bold'>{0:s}</span>".format(_(u"File\nField")))
        _label.show_all()
        _column.set_widget(_label)
        self.tvwFileFields.append_column(_column)

        _cell.connect('changed', self._callback_combo_cell, 2, _model)

        _db_fields = [_(u"Revision ID"), _(u"Incident ID"),
                      _(u"Incident Category"), _(u"Incident Type"),
                      _(u"Short Description"), _(u"Long Description"),
                      _(u"Criticality"), _(u"Detection Method"),
                      _(u"Remarks"), _(u"Status"), _(u"Found During Test"),
                      _(u"Found During Test Case"), _(u"Execution Time"),
                      _(u"Affected Unit"), _(u"Incident Cost"),
                      _(u"Incident Age"), _(u"Hardware ID"), _(u"Software ID"),
                      _(u"Requested By"), _(u"Request Date"), _(u"Reviewed"),
                      _(u"Reviewed By"), _(u"Reviewed Date"), _(u"Approved"),
                      _(u"Approved By"), _(u"Approved Date"), _(u"Closed"),
                      _(u"Closed By"), _(u"Closed Date"), _(u"Life Cycle"),
                      _(u"Analysis"), _(u"Accepted"), _(u"Part Number"),
                      _(u"Age at Incident"), _(u"Failure"), _(u"Suspension"),
                      _(u"No Fault Found"), _(u"Out of Calibration"),
                      _(u"Initial Installation"), _(u"Interval Censored")]

        for i in range(len(_db_fields)):
            _model.append([i, _db_fields[i], ""])

        self.append_page(_scrollwindow)
        self.set_page_type(_scrollwindow, gtk.ASSISTANT_PAGE_CONTENT)
        self.set_page_title(_scrollwindow, _(u"Select Fields to Import"))
        self.set_page_complete(_scrollwindow, True)

        # Create the page to apply the import criteria.
        _fixed = gtk.Fixed()
        _label = _widg.make_label(_(u"Press 'Apply' to import the requested "
                                    u"data or 'Cancel' to quit the "
                                    u"assistant."),
                                  width=600, height=-1, wrap=True)
        _fixed.put(_label, 5, 5)
        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONFIRM)
        self.set_page_title(_fixed, _(u"Import Data"))
        self.set_page_complete(_fixed, True)

        self.show_all()

    def _callback_combo_cell(self, cell, path, row, position, treemodel):
        """
        Called whenever a TreeView CellRendererCombo changes.

        :param gtk.CellRendererCombo cell: the gtk.CellRendererCombo() that
                                           called this method.
        :param str path: the path in the gtk.TreeView() containing the
                         gtk.CellRendererCombo() that called this function.
        :param gtk.TreeIter row: the new gtk.TreeIter() in the
                                 gtk.CellRendererCombo() that called this
                                 method.
        :param int position: the position of in the gtk.TreeView() of the
                             gtk.CellRendererCombo() that called this function.
        :param gtk.TreeModel treemodel: the gtk.TreeModel() for the
                                        gtk.TreeView().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _model = cell.get_property('model')
        _text = _model.get_value(row, 0)
        _index = _model.get_value(row, 1)

        _row = treemodel.get_iter(path)

        _position = treemodel.get_value(_row, 0)
        self._file_index[_position] = _index

        treemodel.set_value(_row, position, _text)

        return False

    def _forward_page_select(self, current_page):
        """
        Method to select the next page to display in the gtk.Assistant().

        :param int current_page: the currently selected page in the
                                 gtk.Assistant().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if current_page == 0:
            _util.select_source_file()
        else:
            self.assistant.set_current_page(current_page + 1)

    def _import(self, __button):
        """
        Method to perform the import from an external file to the database.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _import_error = False

        _util.set_cursor(self, gtk.gdk.WATCH)

        # Find the number of existing incidents.
        if _conf.BACKEND == 'mysql':
            _query = "SELECT COUNT(*) FROM rtk_incident"
        elif _conf.BACKEND == 'sqlite3':
            _query = "SELECT COALESCE(MAX(fld_incident_id)+1, 0) \
                      FROM rtk_incident"
        (_num_incidents, _error_code, __) = self._dao.execute(_query,
                                                              commit=False)

        #self._app.import_log.info('The following records could not be '
        #                          'imported to the open RTK database:\n')

        for i in range(len(self._file_contents) - 1):
            _contents = []

            for j in range(len(self._file_index)):
                if self._file_index[j] == -1:
                    _contents.append('')
                else:
                    try:
                        _contents.append(
                            self._file_contents[i][self._file_index[j]])
                    except IndexError:
                        _contents.append('')

            _contents[14] = _contents[14].replace('$', '')

            # Remove any single and double quotes from the description and
            # remarks fields.
            for j in[4, 5, 8]:
                _contents[j] = _contents[j].replace('\'', '')
                _contents[j] = _contents[j].replace('\"', '')

            # Remove any commas that may be in numerical fields.
            for j in [12, 14, 15]:
                _contents[j] = _contents[j].replace(',', '')

            # Convert all the date fields to ordinal dates.
            for j in [19, 22, 25, 28]:
                _contents[j] = _util.date_to_ordinal(_contents[j])

            # Convert missing values to correct default value.
            for j in [0, 1, 2, 3, 6, 7, 13, 15, 18, 20, 21, 23, 24, 26, 27,
                      29, 31, 32, 35, 36, 37, 38, 39]:
                try:
                    _contents[j] = _util.missing_to_default(int(_contents[j]),
                                                            0)
                except ValueError:
                    _contents[j] = 0

            for j in [16, 17]:
                try:
                    _contents[j] = _util.missing_to_default(int(_contents[j]),
                                                            -1)
                except ValueError:
                    _contents[j] = -1

            for j in [12, 14, 33]:
                try:
                    _contents[j] = _util.missing_to_default(float(_contents[j]),
                                                            0.0)
                except ValueError:
                    _contents[j] = 0.0

            for j in [9, 34]:
                try:
                    _contents[j] = _util.missing_to_default(int(_contents[j]),
                                                            1)
                except ValueError:
                    _contents[j] = 1

            if _contents[1] == 0 or _contents[1] is None or _contents[1] == '':
                _contents[1] = _num_incidents[0][0] + i + 1

            _query = "INSERT INTO rtk_incident \
                      VALUES ({0:d}, {1:d}, {2:d}, {3:d}, '{4:s}', '{5:s}', \
                              {6:d}, {7:d}, '{8:s}', {9:d}, '{10:s}', \
                              '{11:s}', {12:f}, {13:d}, {14:f}, {15:d}, \
                              {16:d}, {17:d}, {18:d}, {19:d}, {20:d}, \
                              {21:d}, {22:d}, {23:d}, {24:d}, {25:d}, \
                              {26:d}, {27:d}, {28:d}, {29:d}, '{30:s}', \
                              {31:d})".format(_contents[0], _contents[1],
                                              _contents[2], _contents[3],
                                              _contents[4], _contents[5],
                                              _contents[6], _contents[7],
                                              _contents[8], _contents[9],
                                              _contents[10], _contents[11],
                                              _contents[12], _contents[13],
                                              _contents[14], _contents[15],
                                              _contents[16], _contents[17],
                                              _contents[18], _contents[19],
                                              _contents[20], _contents[21],
                                              _contents[22], _contents[23],
                                              _contents[24], _contents[25],
                                              _contents[26], _contents[27],
                                              _contents[28], _contents[29],
                                              _contents[30], _contents[31])
            (_results,
             _error_code, __) = self._dao.execute(_query, commit=True)

            _query = "INSERT INTO rtk_incident_detail \
                      (fld_incident_id, fld_component_id, \
                       fld_age_at_incident, fld_failure, fld_suspension, \
                       fld_cnd_nff, fld_occ_fault, fld_initial_installation, \
                       fld_interval_censored) \
                      VALUES ({0:d}, {1:d}, {2:f}, {3:d}, \
                              {4:d}, {5:d}, {6:d}, {7:d}, \
                              {8:d})".format(_contents[1], _contents[32],
                                             _contents[33], _contents[34],
                                             _contents[35], _contents[36],
                                             _contents[37], _contents[38],
                                             _contents[39])
            (_results,
             _error_code, __) = self._dao.execute(_query, commit=True)

        #if _import_error:
        #    _util.rtk_information(_(u"Error importing one or more program "
        #                            u"incidents.  Refer to the import log %s "
        #                            u"for more details.") %
        #                          _conf.LOG_DIR + "RTK_import.log")

        _util.set_cursor(self, gtk.gdk.LEFT_PTR)

        # Reload the Incident class gtk.TreeView().
        self._modulebook.request_load_data(self._dao, self._revision_id)

        return False

    def _cancel(self, __button=None):
        """
        Method to destroy the gtk.Assistant() when the 'Cancel' button is
        pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        """

        self.destroy()


class CreateDataSet(object):
    """
    This is the gtk.Assistant() that walks the user through the process of
    creating a data set for survival analysis from the Field Incident records
    in the open RTK Program database.
    """

    def __init__(self, __button):
        """
        Method to initialize the Dataset Creation Assistant.

        :param gtk.Button __button: the gtk.Button() that called this method.
        """

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_(u"RTK Survival Data Set Creation "
                                   u"Assistant"))
        self.assistant.connect('apply', self._create)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

        # Create the introduction page.
        _fixed = gtk.Fixed()
        _label = _widg.make_label(_(u"This is the RTK survival data set "
                                    u"assistant.  It will help you create a "
                                    u"data set for survival (Weibull) "
                                    u"analysis from the Program Incidents.  "
                                    u"Press 'Forward' to continue or 'Cancel' "
                                    u"to quit the assistant."),
                                  width=600, height=150, wrap=True)
        _fixed.put(_label, 5, 5)
        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(_fixed, _(u"Introduction"))
        self.assistant.set_page_complete(_fixed, True)

        # Create a page to select where data set should be saved.
        _fixed = gtk.Fixed()

        _frame = _widg.make_frame(label=_(""))
        _frame.set_shadow_type(gtk.SHADOW_NONE)
        _frame.add(_fixed)

        # Create the radio buttons that select the output as database or file.
        self.optDatabase = gtk.RadioButton(label=_(u"Save Data Set to "
                                                   u"Database"))
        self.optFile = gtk.RadioButton(group=self.optDatabase,
                                       label=_(u"Save Data Set to File"))
        self.chkNevadaChart = _widg.make_check_button(label=_(u"Create Nevada "
                                                              u"chart from "
                                                              u"data."))

        _fixed.put(self.optDatabase, 5, 5)
        _fixed.put(self.optFile, 5, 35)
        _fixed.put(self.chkNevadaChart, 5, 65)

        # Create the radio buttons that allow choice of MTTF or MTBF estimates.
        self.optMTTF = gtk.RadioButton(label=_(u"Include only the first "
                                               u"failure time for each unit."))
        self.optMTBBD = gtk.RadioButton(group=self.optMTTF,
                                        label=_(u"Include only distinct "
                                                u"failure times for each "
                                                u"unit."))
        self.optMTBF = gtk.RadioButton(group=self.optMTTF,
                                       label=_(u"Include all failure times "
                                               u"for each unit."))

        _fixed.put(self.optMTTF, 5, 105)
        _fixed.put(self.optMTBBD, 5, 135)
        _fixed.put(self.optMTBF, 5, 165)

        # Create the checkbutton to include or exclude zero hour failures.
        self.chkIncludeZeroHour = _widg.make_check_button(
            label=_(u"Include zero hour failures."))
        self.chkIncludeZeroHour.set_active(True)

        _fixed.put(self.chkIncludeZeroHour, 5, 205)

        self.assistant.append_page(_frame)
        self.assistant.set_page_type(_frame, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(_frame, _(u"Select Where to Save Data "
                                                u"Set"))
        self.assistant.set_page_complete(_frame, True)

        # Create a page to select where data set should be saved.
        _fixed = gtk.Fixed()

        _frame = _widg.make_frame(label=_(""))
        _frame.set_shadow_type(gtk.SHADOW_NONE)
        _frame.add(_fixed)

        self.cmbAssembly = _widg.make_combo(simple=False)

        _query = "SELECT fld_name, fld_assembly_id, fld_description \
                  FROM rtk_hardware \
                  WHERE fld_revision_id=%d" % self._app.REVISION.revision_id
        _results = self._app.DB.execute_query(_query,
                                              None,
                                              self._app.ProgCnx)
        _widg.load_combo(self.cmbAssembly, _results, simple=False)

        self.txtDescription = _widg.make_entry()
        self.txtConfidence = _widg.make_entry(width=50)

        _label = _widg.make_label(_(u"Data Set Description:"), width=200)
        _fixed.put(_label, 5, 5)
        _fixed.put(self.txtDescription, 210, 5)

        _label = _widg.make_label(_(u"Analysis Confidence (%):"), width=200)
        _fixed.put(_label, 5, 35)
        _fixed.put(self.txtConfidence, 210, 35)

        _label = _widg.make_label(_(u"Assign to Assembly:"), width=200)
        _fixed.put(_label, 5, 65)
        _fixed.put(self.cmbAssembly, 210, 65)

        self.assistant.append_page(_frame)
        self.assistant.set_page_type(_frame, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(_frame,
                                      _(u"Describe the Data Set"))
        self.assistant.set_page_complete(_frame, True)

        # Create the page to apply the import criteria.
        _fixed = gtk.Fixed()
        _label = _widg.make_label(_(u"Press 'Apply' to create the requested "
                                    u"data set or 'Cancel' to quit the "
                                    u"assistant."), width=600, height=150)
        _fixed.put(_label, 5, 5)
        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed,
                                     gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(_fixed, _(u"Create Data Set"))
        self.assistant.set_page_complete(_fixed, True)

        self.assistant.show_all()

    def _create(self, button):
        """
        Method to create the desired data set.

        :param gtk.Button button: the gtk.Button() that called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _window_ = self.assistant.get_root_window()
        _window_.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))

        _records = {}
        _data_set = []

        model = self.cmbAssembly.get_model()
        row = self.cmbAssembly.get_active_iter()
        if row is not None:
            _assembly_id = int(model.get_value(row, 1))
        else:
            _assembly_id = 0
        _confidence = float(self.txtConfidence.get_text())
        _description = self.txtDescription.get_text()

        self._app.user_log.info('The following records contained inconsistent '
                                'information and were not used in the '
                                'creation of the data set:\n')
        # First create a new dataset in the RTK Program database or create a
        # new file to output the results to.
        if self.optDatabase.get_active():
            if _conf.BACKEND == 'mysql':
                _query = "INSERT INTO tbl_dataset (fld_assembly_id, \
                                                   fld_description, \
                                                   fld_confidence) \
                          VALUES (%d, '%s', %f)" % \
                         (_assembly_id, _description, _confidence)

            elif _conf.BACKEND == 'sqlite3':
                # First find the last dataset id in the table.
                _query = "SELECT MAX(fld_dataset_id) \
                           FROM tbl_dataset"
                _dataset_id = self._app.DB.execute_query(_query, None,
                                                         self._app.ProgCnx)
                _dataset_id = _dataset_id[0][0]
                if _dataset_id is None or not _dataset_id or _dataset_id == '':
                    _dataset_id = 1
                else:
                    _dataset_id += 1

                _query = "INSERT INTO tbl_dataset (fld_dataset_id, \
                                                   fld_assembly_id, \
                                                   fld_description, \
                                                   fld_confidence) \
                          VALUES (%d, %d, '%s', %f)" % \
                         (_dataset_id, _assembly_id, _description,
                          _confidence)

            if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=True):
                _util.rtk_error(_(u"Error creating new data set."))
                return True

            # Find the ID of the last dataset to be created if using the MySQL
            # backend.  This is the value that will be written to
            # fld_dataset_id in tbl_survival_data.
            if _conf.BACKEND == 'mysql':
                _query = "SELECT LAST_INSERT_ID()"
                _dataset_id = self._app.DB.execute_query(_query, None,
                                                         self._app.ProgCnx)
                _dataset_id = _dataset_id[0][0]
        else:
            _dialog = gtk.FileChooserDialog(_(u"RTK: Save Data Set to "
                                              u"File ..."),
                                            None,
                                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                             gtk.STOCK_CANCEL,
                                             gtk.RESPONSE_REJECT))
            _dialog.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
            if _dialog.run() == gtk.RESPONSE_ACCEPT:
                _filename = _dialog.get_filename()

            _dialog.destroy()

            _dataset_id = 0

            _file = open(_filename, 'w')
            _file.write("Data Set Description: " +
                        self.txtDescription.get_text() + "\n")
            _file.write("\n")
            _file.write("Record_ID\tLeft\tRight\tStatus\tQuantity\tUnit\tTBF\tAssembly_ID\tRequest_Date\tAssembly_ID\n")

        _starttime = 0.01
        if self.chkIncludeZeroHour.get_active():
            _starttime = 0.0

        # Select everything from the incident detail table in the Program
        # database.
        #   Index   Field
        #     0     Unit
        #     1     Incident ID
        #     2     Part Number
        #     3     Age at Incident
        #     4     Failure
        #     5     Suspension
        #     6     CND/NFF
        #     7     OCC
        #     8     Initial Installation
        #     9     Interval Censored
        #    10     Date of the failure
        #    11     ID of the affected assembly
        if self.optMTTF.get_active():
            _query = "SELECT t2.fld_unit, t1.fld_incident_id, \
                             t1.fld_part_num, t1.fld_age_at_incident, \
                             t1.fld_failure, t1.fld_suspension, \
                             t1.fld_cnd_nff, t1.fld_occ_fault, \
                             t1.fld_initial_installation, \
                             t1.fld_interval_censored, t2.fld_request_date, \
                             t2.fld_hardware_id \
                      FROM tbl_incident_detail AS t1 \
                      INNER JOIN \
                      ( \
                          SELECT DISTINCT MIN(fld_unit, fld_request_date), \
                                          fld_incident_id, fld_request_date, \
                                          fld_unit, fld_hardware_id \
                          FROM tbl_incident \
                          GROUP BY fld_unit \
                      ) AS t2 \
                      ON t2.fld_incident_id=t1.fld_incident_id \
                      WHERE t1.fld_age_at_incident >= %f \
                      ORDER BY t2.fld_unit ASC, \
                               t1.fld_age_at_incident ASC, \
                               t2.fld_request_date ASC" % _starttime
            _results = self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx)

        elif self.optMTBBD.get_active():
            _query = "SELECT t2.fld_unit, t1.fld_incident_id, \
                             t1.fld_part_num, t1.fld_age_at_incident, \
                             t1.fld_failure, t1.fld_suspension, \
                             t1.fld_cnd_nff, t1.fld_occ_fault, \
                             t1.fld_initial_installation, \
                             t1.fld_interval_censored, t2.fld_request_date, \
                             t2.fld_hardware_id \
                      FROM tbl_incident_detail AS t1 \
                      INNER JOIN \
                      ( \
                         SELECT fld_incident_id, fld_request_date, fld_unit, \
                                fld_hardware_id \
                         FROM tbl_incident \
                         GROUP BY fld_unit, fld_request_date \
                      ) AS t2 \
                      ON t2.fld_incident_id=t1.fld_incident_id \
                      WHERE t1.fld_age_at_incident >= %f \
                      GROUP BY t2.fld_unit,t1.fld_age_at_incident \
                      ORDER BY t2.fld_unit ASC, \
                               t1.fld_age_at_incident ASC, \
                               t2.fld_request_date ASC" % _starttime
            _results = self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx)

        elif self.optMTBF.get_active():
            _query = "SELECT t2.fld_unit, t1.fld_incident_id, \
                             t1.fld_part_num, t1.fld_age_at_incident, \
                             t1.fld_failure, t1.fld_suspension, \
                             t1.fld_cnd_nff, t1.fld_occ_fault, \
                             t1.fld_initial_installation, \
                             t1.fld_interval_censored, t2.fld_request_date, \
                             t2.fld_hardware_id \
                      FROM tbl_incident_detail AS t1 \
                      INNER JOIN tbl_incident AS t2 \
                      ON t2.fld_incident_id=t1.fld_incident_id \
                      WHERE t1.fld_age_at_incident >= %f \
                      ORDER BY t2.fld_unit ASC, \
                               t1.fld_age_at_incident ASC, \
                               t2.fld_request_date ASC" % _starttime
            _results = self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx)

        _n_records = len(_results)

        # Load the results into the survival data table in the RTK Program
        # database or write the results to the open file.
        if self.optDatabase.get_active():
            # Add the first record to the survival data table in the open
            # RTK Program database.
            _base_query = "INSERT INTO tbl_survival_data \
                           (fld_record_id, fld_dataset_id, \
                            fld_left_interval, fld_right_interval, \
                            fld_status, fld_quantity, fld_unit, fld_tbf, \
                            fld_assembly_id, fld_request_date) \
                           VALUES (%d, %d, %f, %f, '%s', %d, '%s', %f, %d, \
                                   %d)"
            _values = (0, _dataset_id, 0.0, float(_results[0][3]),
                       "Interval Censored", 1, _results[0][0],
                       float(_results[0][3]), _results[0][11],
                       _results[0][10])

            # Add the remaining records to the survival data table in the
            # open RTK Program database.
            _n_inconsistent = 0
            _left = 0.0
            for i in range(1, _n_records):
                # Add the current record to the database.
                _query = _base_query % _values
                self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                           commit=True)

                # Create the next set of values to insert to the RTK
                # Program database.
                if _results[i][0] == _results[i - 1][0]:  # Same unit.
                    # Failures did not occur at same time, thus the left of
                    # the interval is the failure time of the previous record.
                    if _results[i][3] != _results[i - 1][3]:
                        _left = float(_results[i - 1][3])

                    # Check the consistency of the two adjacent records.  Any
                    # inconsistent records will be logged, but they are always
                    # added to the dataset.
                    if self._consistency_check(_results[i - 1], _results[i]):
                        _n_inconsistent += 1

                else:                       # Different units.
                    _left = 0.0
                    if i < _n_records - 1:  # Not the last record.
                        # If the failure date of the current record is greater
                        # than the next record's failure date, then log the
                        # inconsistency.
                        if _results[i][10] > _results[i + 1][10]:
                            _next_date = _util.ordinal_to_date(
                                _results[i + 1][10])
                            _current_date = _util.ordinal_to_date(
                                _results[i][10])
                            _errmsg = _(u"The failure date of record #%d, "
                                        u"which occurred on '%s' on unit "
                                        u"'%s', is earlier than the failure "
                                        u"date of record #%d, which occurred "
                                        u"on '%s' on unit '%s'.  Failure "
                                        u"dates should not decrease over "
                                        u"time." % (int(_results[i][1]),
                                                    _current_date,
                                                    _results[i][0],
                                                    int(_results[i + 1][1]),
                                                    _next_date,
                                                    _results[i + 1][0]))
                            self._app.user_log.error(_errmsg)
                            _n_inconsistent += 1

                _right = float(_results[i][3])
                _tbf = _right - _left
                _values = (i, _dataset_id, _left, _right, 'Interval Censored',
                           1, _results[i][0], _tbf, _results[i][11],
                           _results[i][10])

        else:
            # Write the first record to the open file.
            _file.write('0\t0\t' + str(_results[0][3]) + '\t' +
                        'Interval Censored\t1\t' + str(_results[0][0]) +
                        '\t' + str(_results[0][3]) + '\t' +
                        str(_results[0][11]) + '\t' +
                        str(_results[0][10]) + '\n')

            # Write the remaining records to the open file.
            _n_inconsistent = 0
            for i in range(1, _n_records):
                # Create the next set of values to insert to the RTK
                # Program database.
                if _results[i][0] == _results[i - 1][0]:  # Same unit.
                    # Failures occurred at same time.
                    if _results[i][3] == _results[i - 1][3]:
                        _left = float(_results[i][3])
                    else:
                        _left = float(_results[i - 1][3])

                    _tbf = float(_results[i][3]) - float(_results[i - 1][3])
                    _file.write(str(i) + '\t' + str(_results[i - 1][3]) +
                                '\t' + str(_results[i][3]) +
                                '\tInterval Censored\t1\t' +
                                str(_results[i][0]) + '\t' +
                                str(_tbf) + '\t' +
                                str(_results[i][11]) + '\t' +
                                str(_results[i][10]) + '\n')
                    # Check the consistency of the two adjacent records.  Any
                    # inconsistent records will be logged, but they are always
                    # added to the dataset.
                    if self._consistency_check(_results[i - n], _results[i]):
                        _n_inconsistent += 1

                else:                       # Different unit.
                    if i < _n_records - 1:  # Not the last record.
                        # The failure date of the current record is less than
                        # the next record's failure date.
                        if _results[i][10] > _results[i + 1][10]:
                            _next_date = _util.ordinal_to_date(
                                _results[i + 1][10])
                            _current_date = _util.ordinal_to_date(
                                _results[i][10])
                            _errmsg = _(u"The failure date of record #%d, "
                                        u"which occurred on '%s' on unit "
                                        u"'%s', is earlier than the failure "
                                        u"date of record #%d, which occurred "
                                        u"on '%s' on unit '%s'.  Failure "
                                        u"dates should not decrease over "
                                        u"time." % (int(_results[i][1]),
                                                    _current_date,
                                                    _results[i][0],
                                                    int(_results[i + 1][1]),
                                                    _next_date,
                                                    _results[i + 1][0]))
                            self._app.user_log.error(_errmsg)
                            _n_inconsistent += 1

                    _right = float(_results[i][3])
                    _tbf = float(_results[i][3])
                    _file.write(str(i) + '\t0.0\t' + str(_right) +
                                '\tInterval Censored\t1\t' +
                                str(_results[i][0]) + '\t' + str(_tbf) + '\t' +
                                str(_results[i][11]) + '\t' +
                                str(_results[i][10]) + '\n')

        _window_.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

        if _n_inconsistent > 0:
            _util.rtk_information(_(u"There were %d records with inconsistent "
                                    u"information.  These were not used in "
                                    u"the creation of the dataset. Please see "
                                    u"file '%s' for details." %
                                    (_n_inconsistent,
                                     _conf.LOG_DIR + 'RTK_error.log')))

        # Load the dataset gtk.TreeView with the newly created dataset if it
        # was created in the RTK Program database.
        if self.optDatabase.get_active():
            self._app.DATASET.load_tree()
            # self._app.DATASET.load_notebook()
            # _page = sum(_conf.RTK_MODULES[:11])
            # self._app.winTree.notebook.set_current_page(_page)

        return False

    def _consistency_check(self, results1, results2):
        """
        Function to check the consistency of the data records.

        :param list results1: the previous record in the data set.
        :param list results2: the current record in the data set.
        :return: False if records are consistent or True if not.
        :rtype: boolean
        """

        _err = False

        if results2[10] < results1[10]:     # Failure dates are descending.
            _previous_date = _util.ordinal_to_date(results1[10])
            _current_date = _util.ordinal_to_date(results2[10])
            _errmsg = _(u"The failure date of record #%d, which occurred on "
                        u"'%s' on unit '%s', is earlier than the failure time "
                        u"of record #%d, which occurred on '%s' on unit "
                        u"'%s'.  Failure dates should not decrease over "
                        u"time." % (int(results2[1]), _current_date,
                                    results2[0], int(results1[1]),
                                    _previous_date, results2[0]))
            _err = True

        if _err:
            self._app.user_log.error(_errmsg)

        return _err

    def _cancel(self, __button):
        """
        Method to destroy the gtk.Assistant() when the 'Cancel' button is
        pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        """

        self.assistant.destroy()
