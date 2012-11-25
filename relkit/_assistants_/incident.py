#!/usr/bin/env python

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2012 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       add_incident.py is part of The RelKit Project
#
# All rights reserved.

import sys
import pango

from os import environ, name
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

# Import other RelKit modules.
import configuration as _conf
import widgets as _widg

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except:
    locale.setlocale(locale.LC_ALL, "")

import gettext
_ = gettext.gettext

class AddIncident:

    def __init__(self, button, app):

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_("RelKit Incident Wizard"))
        self.assistant.connect('apply', self._add_incident)
        self.assistant.connect('cancel', self._cancel)

        # Create the introduction page.
        fixed = gtk.Fixed()
        _text_ = _("This is the RelKit incident addition wizard.  It will help you add a new hardware or software incident to the database.  Press 'Forward' to continue or 'Cancel' to quit the wizard.")
        label = _widg.make_label(_text_, width=300, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(fixed, _("Introduction"))
        self.assistant.set_page_complete(fixed, True)

        # Create the pages to select either hardware or software incident.
        y_pos = 5
        self.fxdPageType = gtk.Fixed()
        _text_ = _("Select type of incident to add...")
        label = _widg.make_label(_text_, width=300)
        self.fxdPageType.put(label, 5, y_pos)
        y_pos += 30

        self.rdoHardware = gtk.RadioButton(None, _("_Hardware"))
        self.fxdPageType.put(self.rdoHardware, 5, y_pos)
        y_pos += 30

        self.rdoSoftware = gtk.RadioButton(self.rdoHardware, _("_Software"))
        self.fxdPageType.put(self.rdoSoftware, 5, y_pos)
        y_pos += 30

        self.rdoProcess = gtk.RadioButton(self.rdoHardware, _("_Process"))
        self.fxdPageType.put(self.rdoProcess, 5, y_pos)

        self.assistant.append_page(self.fxdPageType)
        self.assistant.set_page_type(self.fxdPageType, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(self.fxdPageType, _("Incident Type"))
        self.assistant.set_page_complete(self.fxdPageType, True)

        # Create the software incident general information page.
        x_pos = 5
        y_pos = 5
        self.fxdPageSWGeneral = gtk.Fixed()
        _text_ = _("Incident Date*:")
        label = _widg.make_label(_text_)
        self.txtIncidentDate = _widg.make_entry(_width_=100)
        self.txtIncidentDate.set_tooltip_text(_("Enter the date the incident occurred."))
        self.txtIncidentDate.connect('focus_out_event', self._check_ready, 2)
        self.fxdPageSWGeneral.put(label, x_pos, y_pos)
        x_pos += 195
        self.fxdPageSWGeneral.put(self.txtIncidentDate, x_pos, y_pos)
        x_pos += 105

        # Add a calendar widget for date selection if we are on a posix
        # platform.  The calendar widget doesn't work for shit on Windoze.
        if(name == 'posix'):
            self.btnCalendar = _widg.make_button(25, 25, "...", None)
            self.btnCalendar.set_tooltip_text(_("Launch a calendar to select the incident date"))
            self.btnCalendar.connect('clicked', self._show_calendar)
            self.calIncidentDate = gtk.Calendar()
            self.calIncidentDate.connect('day_selected_double_click',
                                         self._select_date)
            self.fxdPageSWGeneral.put(self.btnCalendar, x_pos, y_pos)
            x_pos += 100
            _who = environ['USER']

        elif(name == 'nt'):
            _who = environ['USERNAME']

        _text_ = _("Reported By*:")
        label = _widg.make_label(_text_)
        self.txtReportedBy = _widg.make_entry()
        self.txtReportedBy.set_tooltip_text(_("Enter the name of the person reporting the incident.  Defaults to currently logged in user."))
        self.txtReportedBy.set_text(_who)
        self.txtReportedBy.connect('focus_out_event', self._check_ready, 2)
        self.fxdPageSWGeneral.put(label, x_pos, y_pos)
        x_pos += 200
        self.fxdPageSWGeneral.put(self.txtReportedBy, x_pos, y_pos)
        y_pos += 30

        _text_ = _("Incident Type:")
        label = _widg.make_label(_text_)
        self.cmbIncidentType = _widg.make_combo()
        self.cmbIncidentType.set_tooltip_text(_("Select the type of problem this incident represents."))
        _types = [[_("Planning")], [_("Concept")], [_("Requirement")],
                  [_("Design")], [_("Coding")], [_("Database")],
                  [_("Test Information")], [_("Manuals")], [_("Other")]]
        _widg.load_combo(self.cmbIncidentType, _types)
        self.fxdPageSWGeneral.put(label, 5, y_pos)
        self.fxdPageSWGeneral.put(self.cmbIncidentType, 200, y_pos)
        y_pos += 35

        _text_ = _("Description*:")
        label = _widg.make_label(_text_)
        self.txtDescription = _widg.make_entry(_width_=795)
        self.txtDescription.set_tooltip_text(_("Enter a brief description of the incident being reported."))
        self.txtDescription.connect('focus_out_event', self._check_ready, 2)
        self.fxdPageSWGeneral.put(label, 5, y_pos)
        y_pos += 30
        self.fxdPageSWGeneral.put(self.txtDescription, 5, y_pos)
        y_pos += 30

        _text_ = _("Details*:")
        label = _widg.make_label(_text_)
        self.txtDetails = gtk.TextBuffer()
        self.txtDetails.connect('changed', self._check_ready, None, 2)
        textview = _widg.make_text_view(buffer_=self.txtDetails, width=795)
        textview.set_tooltip_text(_("Describe in detail the incident being reported."))
        self.fxdPageSWGeneral.put(label, 5, y_pos)
        y_pos += 30
        self.fxdPageSWGeneral.put(textview, 5, y_pos)
        y_pos += 120

        _text_ = _("Incident Criticality*:")
        label = _widg.make_label(_text_)
        self.cmbIncidentCriticality = _widg.make_combo()
        self.cmbIncidentCriticality.set_tooltip_text(_("Select the severity of the discrepancy."))
        results = [["1"], ["2"], ["3"], ["4"], ["5"]]
        _widg.load_combo(self.cmbIncidentCriticality, results)
        self.cmbIncidentCriticality.connect('changed', self._check_ready,
                                            None, 2)
        self.fxdPageSWGeneral.put(label, 5, y_pos)
        self.fxdPageSWGeneral.put(self.cmbIncidentCriticality, 200, y_pos)
        y_pos += 35

        _text_ = _("Method of Detection*:")
        label = _widg.make_label(_text_)
        self.cmbDetectMethod = _widg.make_combo()
        _methods = [[_("Code Review")], [_("Error/Anomaly Analysis")],
                    [_("Structure Analysis")], [_("Random Testing")],
                    [_("Functional Testing")], [_("Branch Testing")]]
        _widg.load_combo(self.cmbDetectMethod, _methods)
        self.cmbDetectMethod.connect('changed', self._check_ready, None, 2)
        self.fxdPageSWGeneral.put(label, 5, y_pos)
        self.fxdPageSWGeneral.put(self.cmbDetectMethod, 200, y_pos)
        y_pos += 35

        _text_ = _("Remarks:")
        label = _widg.make_label(_text_)
        self.txtRemarks = gtk.TextBuffer()
        textview = _widg.make_text_view(buffer_=self.txtRemarks, width=795)
        textview.set_tooltip_text(_("Enter any remarks related to the incident being reported."))
        self.fxdPageSWGeneral.put(label, 5, y_pos)
        y_pos += 30
        self.fxdPageSWGeneral.put(textview, 5, y_pos)

        self.assistant.append_page(self.fxdPageSWGeneral)
        self.assistant.set_page_type(self.fxdPageSWGeneral,
                                     gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(self.fxdPageSWGeneral, _("Software Incident: General Information"))

        # Create the software incident test information page.
        y_pos = 5
        self.fxdPageSWTest = gtk.Fixed()
        _text_ = _("Test Procedure*:")
        label = _widg.make_label(_text_)
        self.txtTestProcedure = _widg.make_entry()
        self.txtTestProcedure.set_tooltip_text(_("Enter the test procedure being run when the incident occurred."))
        self.txtTestProcedure.connect('focus_out_event', self._check_ready, 3)
        self.fxdPageSWTest.put(label, 5, y_pos)
        self.fxdPageSWTest.put(self.txtTestProcedure, 200, y_pos)
        y_pos += 30

        _text_ = _("Test Case*:")
        label = _widg.make_label(_text_)
        self.txtTestCase = _widg.make_entry()
        self.txtTestCase.set_tooltip_text(_("Enter the test case being run when the incident occurred."))
        self.txtTestCase.connect('focus_out_event', self._check_ready, 3)
        self.fxdPageSWTest.put(label, 5, y_pos)
        self.fxdPageSWTest.put(self.txtTestCase, 200, y_pos)
        y_pos += 30

        _text_ = _("Execution Time*:")
        label = _widg.make_label(_text_)
        self.txtExecutionTime = _widg.make_entry()
        self.txtExecutionTime.set_tooltip_text(_("Enter the execution time when the incident occurred."))
        self.txtExecutionTime.connect('focus_out_event', self._check_ready, 3)
        self.fxdPageSWTest.put(label, 5, y_pos)
        self.fxdPageSWTest.put(self.txtExecutionTime, 200, y_pos)
        y_pos += 30

        _text_ = _("Effect:")
        label = _widg.make_label(_text_)
        self.txtEffect = gtk.TextBuffer()
        textview = _widg.make_text_view(buffer_=self.txtEffect, width=795)
        textview.set_tooltip_text(_("Describe the effect on the system or user of the incident being reported."))
        self.fxdPageSWTest.put(label, 5, y_pos)
        y_pos += 30
        self.fxdPageSWTest.put(textview, 5, y_pos)
        y_pos += 120

        _text_ = _("Recommended Solution:")
        label = _widg.make_label(_text_)
        self.txtSolution = gtk.TextBuffer()
        textview = _widg.make_text_view(buffer_=self.txtSolution, width=795)
        textview.set_tooltip_text(_("Describe any recommended solution for the incident being reported."))
        self.fxdPageSWTest.put(label, 5, y_pos)
        y_pos += 30
        self.fxdPageSWTest.put(textview, 5, y_pos)

        self.assistant.append_page(self.fxdPageSWTest)
        self.assistant.set_page_type(self.fxdPageSWTest,
                                     gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(self.fxdPageSWTest, _("Software Incident: Test Information"))

        fixed = gtk.Fixed()
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed,
                                     gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(fixed, _("Incident: Confirm Addition"))
        self.assistant.set_page_complete(fixed, True)

        self.assistant.show_all()

    def _forward_page_select(self, current_page):

        if(current_page == 0):
            self.assistant.set_current_page(1)

        elif(current_page == 1):
            if(self.rdoHardware.get_active()):
                print "Going to page 2 hardware"
            elif(self.rdoSoftware.get_active()):
                self.assistant.set_current_page(2)

        elif(current_page == 2):
            self.assistant.set_current_page(3)

    def _show_calendar(self, button):

        """ Method to display the calendar object.

            Keyword Arguments:
            button -- the button calling this method.
        """

        self.winCalendar = gtk.Window()
        self.winCalendar.add(self.calIncidentDate)

        self.winCalendar.show_all()

    def _select_date(self, calendar):

        """ Method to get the selected date from the calendar object.

            Keyword Arguments:
            calendar -- the calendar from which the date is being selected.
        """

        _date = self.calIncidentDate.get_date()
        Y = _date[0]
        m = _date[1] + 1
        d = _date[2]

        self.txtIncidentDate.set_text("%d-%d-%d" % (Y, m, d))

        self.winCalendar.destroy()

        return False

    def _check_ready(self, widget, event, _page_):

        """ Method to check if all the required data is filled in before
            allowing the assistant to continue.

            Keyword Arguments:
            widget -- the widget calling this method.
            event  -- the gtk.gdk.Event calling this method.
            _page_ -- the page in the assistant to check.
        """

        if(_page_ == 2):
            if(self.txtIncidentDate.get_text() != '' and
               self.txtReportedBy.get_text() != '' and
               self.txtDescription.get_text() != '' and
               self.txtDetails.get_text(*self.txtDetails.get_bounds()) != '' and
               self.cmbIncidentCriticality.get_active() > 0 and
               self.cmbDetectMethod.get_active() > 0):
                self.assistant.set_page_complete(self.fxdPageSWGeneral, True)
        elif(_page_ == 3):
            if(self.txtTestProcedure.get_text() != '' and
               self.txtTestCase.get_text() != '' and
               self.txtExecutionTime.get_text() != ''):
                self.assistant.set_page_complete(self.fxdPageSWTest, True)

    def _add_incident(self, assistant):

        """ Method to add the new software incident to the incidents table.

            Keyword Arguments:
            assistant -- the gtk.Assistant that represents the wizard.
        """

        values = (self._app.REVISION.revision_id,
                  self._app.SOFTWARE.software_id,
                  self.cmbIncidentType.get_active(),
                  self.txtDescription.get_text(),
                  self.txtDetails.get_text(*self.txtDetails.get_bounds()),
                  self.cmbIncidentCriticality.get_active(),
                  self.cmbDetectMethod.get_active(),
                  self.txtRemarks.get_text(*self.txtRemarks.get_bounds()),
                  self.txtReportedBy.get_text(),
                  datetime.strptime(self.txtIncidentDate.get_text(), '%Y-%m-%d').toordinal(),
                  self.txtTestProcedure.get_text(),
                  self.txtTestCase.get_text(),
                  float(self.txtExecutionTime.get_text()),
                  self.txtEffect.get_text(*self.txtEffect.get_bounds()),
                  self.txtSolution.get_text(*self.txtSolution.get_bounds()))

        if(_conf.BACKEND == 'mysql'):
            query = "INSERT INTO tbl_incident (fld_revision_id, \
                                               fld_software_id, \
                                               fld_incident_category, \
                                               fld_incident_type, \
                                               fld_short_description, \
                                               fld_long_description, \
                                               fld_criticality, \
                                               fld_detection_method, \
                                               fld_remarks, \
                                               fld_status, \
                                               fld_request_by, \
                                               fld_request_date, \
                                               fld_test_found, \
                                               fld_test_case, \
                                               fld_execution_time, \
                                               fld_effect, \
                                               fld_recommended_solution) \
                     VALUES (%d, %d, 2, %d, '%s', '%s', \
                             %d, '%s', '%s', 1, '%s', '%s', \
                             '%s', '%s', %f, '%s', '%s')"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "INSERT INTO tbl_incident (fld_revision_id, \
                                               fld_software_id, \
                                               fld_incident_category, \
                                               fld_incident_type, \
                                               fld_short_description, \
                                               fld_long_description, \
                                               fld_criticality, \
                                               fld_detection_method, \
                                               fld_remarks, \
                                               fld_status, \
                                               fld_request_by, \
                                               fld_request_date, \
                                               fld_test_found, \
                                               fld_test_case, \
                                               fld_execution_time, \
                                               fld_effect, \
                                               fld_recommended_solution) \
                     VALUES (?, ?, 2, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?)"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        # Retrieve the newly added incident id.
        if(_conf.BACKEND == 'mysql'):
            query = "SELECT LAST_INSERT_ID()"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT seq \
                     FROM sqlite_sequence \
                     WHERE name='tbl_incident'"

        incident_id = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx)

        if(incident_id == ''):
            self._app.debug_log.error("software.py: Failed to retrieve new incident ID.")

        # Add the new incident to the incident detail table.
        values = (incident_id[0][0],)
        if(_conf.BACKEND == 'mysql'):
            query = "INSERT INTO tbl_incident_detail (fld_incident_id) \
                     VALUES (%d)"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "INSERT INTO tbl_incident_detail (fld_incident_id) \
                     VALUES (?)"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if(results == '' or not results):
            self._app.debug_log.error("software.py: Failed to add new incident to incident details table.")

        #self.assistant.destroy()

    def _cancel(self, button):

        """ Method to destroy the gtk.Assistant when the 'Cancel' button is
            pressed.

            Keyword Arguments:
            button -- the gtk.Button that called this method.
        """

        self.assistant.destroy()
