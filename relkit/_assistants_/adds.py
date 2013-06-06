#!/usr/bin/env python

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2012 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       addrecord.py is part of The RelKit Project
#
# All rights reserved.

import os
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
    """
    This is the gtkAssistant that walks the user through the process of adding
    a Field Incident records to the open RelKit Program database.
    """

    def __init__(self, button, app):
        """
        Initialize on instance of the Add Incident Assistant.

        Keyword Arguments:
        button -- the gtk.Button widget that calling this Assistant.
        app    -- the instance of the RelKit application calling the Assistant.
        """

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_("RelKit Add Incident Assistant"))
        self.assistant.connect('apply', self._add_incident)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

# Create the introduction page.
        fixed = gtk.Fixed()
        _text_ = _("This is the RelKit incident addition assistant.  It will help you add a new hardware or software incident to the database.  Press 'Forward' to continue or 'Cancel' to quit the assistant.")
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
        """
        Method to display the calendar object.

        Keyword Arguments:
        button -- the button calling this method.
        """

        self.winCalendar = gtk.Window()
        self.winCalendar.add(self.calIncidentDate)

        self.winCalendar.show_all()

    def _select_date(self, calendar):
        """
        Method to get the selected date from the calendar object.

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
        """
        Method to check if all the required data is filled in before allowing
        the assistant to continue.

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
        """
        Method to add the new software incident to the incidents table.

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

    def _cancel(self, button):
        """
        Method to destroy the gtk.Assistant when the 'Cancel' button is
        pressed.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        self.assistant.destroy()


class AddTestPlan:
    """
    This is the gtk.Assistant that walks the user through the process of
    creating a new test plan in the open RelKit Program database.
    """

    _labels = [_(u"Assembly:"), _(u"Test Type:"), _(u"Test Title:"),
               _(u"Detailed Test Description")]

    _rg_labels = [_(u"Initial MTBF:"), _(u"Goal MTBF:"),
                  _(u"Growth Potential MTBF:"), _(u"Technical Requirement:")]

    def __init__(self, button, app):
        """
        Method to initialize the Test Plan Creation Assistant.

        Keyword Arguments:
        button -- the gtk.Button widget that called this method.
        app    -- the RelKit application.
        """

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_(u"RelKit Test Plan Creation Assistant"))
        #self.assistant.set_forward_page_func(self._next_page)

        #self.assistant.connect('prepare', self._set_next_page)
        self.assistant.connect('apply', self._test_plan_add)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

        self._next_page = 0

# --------------------------------------------------------------------------- #
# Create the introduction page.
# --------------------------------------------------------------------------- #
        fixed = gtk.Fixed()
        _text_ = _(u"This is the RelKit test plan creation assistant.  It will help you create a new test plan in the open RelKit Program.  Press 'Forward' to continue or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(fixed, _(u"Introduction"))
        self.assistant.set_page_complete(fixed, True)

# --------------------------------------------------------------------------- #
# Create a page to describe the overall test plan.
# --------------------------------------------------------------------------- #
        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_(""))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(fixed)

# Create the gtk.Combo that allow one of multiple selections.
        self.cmbAssembly = _widg.make_combo(simple=False)
        self.cmbAssembly.set_tooltip_text(_(u"Select the assembly associated with the test plan."))
        query = "SELECT fld_name, fld_assembly_id, fld_description \
                 FROM tbl_system"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)
        _widg.load_combo(self.cmbAssembly, results, simple=False)

        self.cmbTestType = _widg.make_combo()
        self.cmbTestType.set_tooltip_text(_(u"Select the type of test to add."))
        results = [[u"HALT"], [u"HASS"], [u"ALT"], [u"ESS"],
                   [u"Reliability Growth"], [u"Reliability Demonstration"],
                   [u"PRVT"]]
        _widg.load_combo(self.cmbTestType, results)

        label = _widg.make_label(self._labels[0], 150, 25)
        fixed.put(label, 5, 5)
        fixed.put(self.cmbAssembly, 160, 5)

        label = _widg.make_label(self._labels[1], 150, 25)
        fixed.put(label, 5, 40)
        fixed.put(self.cmbTestType, 160, 40)

# Create the gtk.Entry that allow free-form user input.
        self.txtName = _widg.make_entry(_width_=400)
        self.txtName.set_tooltip_text(_(u"Enter a brief description or title for the test."))

        self.txtDescription = gtk.TextBuffer()
        textview = _widg.make_text_view(buffer_=self.txtDescription,
                                        width=555)
        textview.set_tooltip_text(_(u"Enter a detailed description of the test."))

        label = _widg.make_label(self._labels[2], 160, 25)
        fixed.put(label, 5, 75)
        fixed.put(self.txtName, 160, 75)

        label = _widg.make_label(self._labels[3], 250, 25)
        fixed.put(label, 5, 105)
        fixed.put(textview, 5, 130)

        self.assistant.append_page(frame)
        self.assistant.set_page_type(frame, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(frame,
                                      _(u"Describe the Test Plan"))
        self.assistant.set_page_complete(frame, True)

# --------------------------------------------------------------------------- #
# Create a page to describe the reliability growth test plan.
# --------------------------------------------------------------------------- #
        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_(""))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(fixed)

        self.txtMTBFI = _widg.make_entry(_width_=50)
        self.txtMTBFG = _widg.make_entry(_width_=50)
        self.txtMTBFGP = _widg.make_entry(_width_=50)
        self.txtTechReq = _widg.make_entry(_width_=50)

        label = _widg.make_label(self._rg_labels[0], 250, 25)
        fixed.put(label, 5, 5)
        fixed.put(self.txtMTBFI, 260, 5)

        label = _widg.make_label(self._rg_labels[1], 250, 25)
        fixed.put(label, 5, 35)
        fixed.put(self.txtMTBFG, 260, 35)

        label = _widg.make_label(self._rg_labels[2], 250, 25)
        fixed.put(label, 5, 65)
        fixed.put(self.txtMTBFGP, 260, 65)

        label = _widg.make_label(self._rg_labels[3], 250, 25)
        fixed.put(label, 5, 95)
        fixed.put(self.txtTechReq, 260, 95)

        self.assistant.append_page(frame)
        self.assistant.set_page_type(frame, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(frame,
                                      _(u"Describe the Reliability Growth Plan"))
        self.assistant.set_page_complete(frame, True)

# --------------------------------------------------------------------------- #
# Create the page to create the test plan.
# --------------------------------------------------------------------------- #
        fixed = gtk.Fixed()
        _text_ = _(u"Press 'Apply' to create the test plan or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed,
                                     gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(fixed, _(u"Create Test Plan"))
        self.assistant.set_page_complete(fixed, True)

        self.assistant.show_all()

    def _set_next_page(self, _assistant_, _page_):

        _cur_page = self.assistant.get_current_page()
        if(_cur_page == 2):
            _test_type = self.cmbTestType.get_active()
            if(_test_type == 5):
                self._next_page = 2
            else:
                self._next_page = 3
        else:
            self._next_page += 1

        return False

    def _next_page(self, _page_):

        self.assistant.set_current_page(self._next_page)

        return False

    def _test_plan_add(self, button):
        """
        Method to add a new test plan for the selected hardware item to the
        open RelKit Program.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

# Find the assembly ID selected by the user.  If none is selected, use the
# top-level assembly by default.
        model = self.cmbAssembly.get_model()
        row = self.cmbAssembly.get_active_iter()
        if(row is not None):
            _assembly_id = int(model.get_value(row, 1))
        else:
            _assembly_id = 0

        _title = self.txtName.get_text()

        _bounds = self.txtDescription.get_bounds()
        _description = self.txtDescription.get_text(_bounds[0], _bounds[1])

# Find the ID of the last test.
        query = "SELECT MAX(fld_test_id) FROM tbl_tests"
        _test_id = self._app.DB.execute_query(query,
                                              None,
                                              self._app.ProgCnx)
        _test_id = int(_test_id[0][0]) + 1

# Find out what type of test we're trying to add.  Then build the correct
# query for the test type.
        _test_type = self.cmbTestType.get_active()

        if(_test_type == 5):                # Reliability growth test plan.
            _mi = float(self.txtMTBFI.get_text())
            _mg = float(self.txtMTBFG.get_text())
            _mgp = float(self.txtMTBFGP.get_text())
            _tr = float(self.txtTechReq.get_text())

            query = "INSERT INTO tbl_tests \
                     (fld_assembly_id, fld_test_id, fld_test_name, \
                      fld_test_description, fld_mi, fld_mg, fld_mgp, fld_tr) \
                     VALUES(%d, %d, '%s', '%s', %f, %f, %f, %f)" % \
                     (_assembly_id, _test_id, _title, _description, \
                      _mi, _mg, _mgp, _tr)

        _results = self._app.DB.execute_query(query,
                                              None,
                                              self._app.ProgCnx)
        if not _results:
            self._app.debug_log.error("adds.py: Failed to add new test plan to test table.")
            return True

        self._app.TESTING.load_tree()

        return False

    def _cancel(self, button):
        """
        Method to destroy the gtk.Assistant when the 'Cancel' button is
        pressed.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        self.assistant.destroy()


class AddRGRecord(gtk.Assistant):
    """
    This is the gtk.Assistant that walks the user through the process of
    adding a test record to the currently selected test plan in the open
    RelKit Program database.
    """

    _labels = [_(u"Date:"), _(u"Time:"), _(u"Number of Failures:")]

    def __init__(self, button, app):
        """
        Method to initialize the Reliability Growth Record Add Assistant.

        Keyword Arguments:
        button -- the gtk.ToolButton that called this assistant.
        app    -- the RelKit application.
        """

        gtk.Assistant.__init__(self)
        self.set_title(_(u"RelKit Reliability Growth Record Assistant"))
        self.connect('apply', self._test_record_add)
        self.connect('cancel', self._cancel)
        self.connect('close', self._cancel)

        self._app = app

# --------------------------------------------------------------------------- #
# Create the introduction page.
# --------------------------------------------------------------------------- #
        fixed = gtk.Fixed()
        _text_ = _(u"This is the RelKit reliability growth record assistant.  It will help you add a record for reliability growth tracking against the currently selected reliability growth plan.  Press 'Forward' to continue or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.append_page(fixed)
        self.set_page_type(fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.set_page_title(fixed, _(u"Introduction"))
        self.set_page_complete(fixed, True)

# --------------------------------------------------------------------------- #
# Create the page to gather the necessary inputs.
# --------------------------------------------------------------------------- #
        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_(""))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(fixed)

# Create the gtk.Combo that allow one of multiple selections.
        self.txtDate = _widg.make_entry()
        self.txtDate.set_tooltip_text(_(u"Date test record was generated.  This is not necessarily the date the record is being added."))
        self.txtTime = _widg.make_entry()
        self.txtTime.set_tooltip_text(_(u"Test time."))
        self.chkAdditional = _widg.make_check_button(_(u"Additional"))
        self.chkAdditional.set_tooltip_text(_(u"If checked, the test time is additional test time.  If unchecked, the test time is cumulative since the start of testing."))
        self.chkAdditional.set_active(False)
        self.txtNumFails = _widg.make_entry()
        self.txtNumFails.set_tooltip_text(_(u"Number of failures observed."))
        self.txtNumFails.set_text("1")

        label = _widg.make_label(self._labels[0], 150, 25)
        fixed.put(label, 5, 5)
        fixed.put(self.txtDate, 160, 5)

        label = _widg.make_label(self._labels[1], 150, 25)
        fixed.put(label, 5, 40)
        fixed.put(self.txtTime, 160, 40)
        fixed.put(self.chkAdditional, 365, 40)

        label = _widg.make_label(self._labels[2], 150, 25)
        fixed.put(label, 5, 75)
        fixed.put(self.txtNumFails, 160, 75)

        self.append_page(frame)
        self.set_page_type(frame, gtk.ASSISTANT_PAGE_CONTENT)
        self.set_page_title(frame, _(u"Enter Reliability Growth Data"))
        self.set_page_complete(frame, True)

# --------------------------------------------------------------------------- #
# Create the page to apply the import criteria.
# --------------------------------------------------------------------------- #
        fixed = gtk.Fixed()
        _text_ = _(u"Press 'Apply' to create the requested data set or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.append_page(fixed)
        self.set_page_type(fixed, gtk.ASSISTANT_PAGE_CONFIRM)
        self.set_page_title(fixed, _(u"Add Reliability Growth Record"))
        self.set_page_complete(fixed, True)

        self.show_all()

    def _test_record_add(self, button):
        """
        Method to add a new test record for the selected test plan to the
        open RelKit Program.

        Keyword Arguments:
        button -- the gtk.ToolButton that called this method.
        """

        model = self._app.TESTING.model
        row = self._app.TESTING.selected_row
        idx = self._app.TESTING._col_order[0]

        query = "SELECT MAX(fld_record_id), MAX(fld_right_interval) \
                 FROM tbl_survival_data \
                 WHERE fld_dataset_id=%d" % self._app.TESTING.test_id
        _results = self._app.DB.execute_query(query,
                                              None,
                                              self._app.ProgCnx,
                                              commit=False)

        if(_results[0][0] is None or _results[0][0] == ''):
            _last_id = 0
        else:
            _last_id = _results[0][0]

        if(_results[0][1] is None or _results[0][1] == ''):
            _last_time = 0.0
        else:
            _last_time = float(_results[0][1])

        _last_id += 1

        _assembly_id = model.get_value(row, idx)
# Read the test time entered by the user.  If this is entered as additional
# test time, calculate the cumulative test time.
        _time = float(self.txtTime.get_text())
        if(self.chkAdditional.get_active()):
            _time = _time + _last_time
        _n_fails = int(self.txtNumFails.get_text())

        query = "INSERT INTO tbl_survival_data \
                 (fld_record_id, fld_dataset_id, fld_left_interval, \
                  fld_right_interval, fld_quantity, fld_unit, \
                  fld_part_num, fld_market, fld_model, fld_mode_type, \
                  fld_assembly_id) \
                 VALUES (%d, %d, %f, %f, %d, '%s', '%s', '%s', '%s', \
                         %d, %d)" % (_last_id, self._app.TESTING.test_id, \
                                     0.0, _time, _n_fails, '', '', '', '', \
                                     0, _assembly_id)

        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("adds.py: Failed to add new test record to survival data table.")
            return True

        self._app.TESTING._load_test_assessment_tree()

        return False

    def _cancel(self, button):
        """
        Method to destroy the gtk.Assistant when the 'Cancel' button is
        pressed.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        self.destroy()


class CreateDataSet:
    """
    This is the gtk.Assistant that walks the user through the process of
    creating a datset for survival analysis from the Field Incident records
    in the open RelKit Program database.
    """

    def __init__(self, button, app):
        """
        Method to initialize the Dataset Creation Assistant.

        Keyword Arguments:
        button -- the gtk.Button widget that called this method.
        app    -- the RelKit application.
        """

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_("RelKit Survival Data Set Creation Assistant"))
        self.assistant.connect('apply', self._create)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

# Create the introduction page.
        fixed = gtk.Fixed()
        _text_ = _("This is the RelKit survival data set assistant.  It will help you create a data set for survival (Weibull) analysis from the Program Incidents.  Press 'Forward' to continue or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(fixed, _("Introduction"))
        self.assistant.set_page_complete(fixed, True)

# Create a page to select where data set should be saved.
        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_(""))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(fixed)

# Create the radio buttons that select the output as database or file.
        self.optDatabase = gtk.RadioButton(label=_(u"Save Data Set to Database"))
        self.optFile = gtk.RadioButton(group=self.optDatabase,
                                       label="Save Data Set to File")

        fixed.put(self.optDatabase, 5, 5)
        fixed.put(self.optFile, 5, 35)

# Create the radio buttons that allow choice of MTTF or MTBF estimates.
        self.optMTTF = gtk.RadioButton(label=_(u"Only include first failure time for each unit."))
        self.optMTBF = gtk.RadioButton(group=self.optMTTF,
                                       label=_(u"Include all failure times for each unit."))

        fixed.put(self.optMTTF, 5, 75)
        fixed.put(self.optMTBF, 5, 105)

# Create the checkbutton to include or exclude zero hour failures.
        self.chkIncludeZeroHour = _widg.make_check_button(
        _label_=_(u"Include zero hour failures."))
        self.chkIncludeZeroHour.set_active(True)

        fixed.put(self.chkIncludeZeroHour, 5, 145)

        self.assistant.append_page(frame)
        self.assistant.set_page_type(frame, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(frame,
                                      _("Select Where to Save Data Set"))
        self.assistant.set_page_complete(frame, True)

# Create a page to select where data set should be saved.
        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_(""))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(fixed)

        self.txtDescription = _widg.make_entry()
        self.txtConfidence = _widg.make_entry(_width_=50)

        label = _widg.make_label("Data Set Description:")
        fixed.put(label, 5, 5)
        fixed.put(self.txtDescription, 205, 5)

        label = _widg.make_label("Analysis Confidence (%):")
        fixed.put(label, 5, 35)
        fixed.put(self.txtConfidence, 205, 35)

        self.assistant.append_page(frame)
        self.assistant.set_page_type(frame, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(frame,
                                      _("Describe the Data Set"))
        self.assistant.set_page_complete(frame, True)

# Create the page to apply the import criteria.
        fixed = gtk.Fixed()
        _text_ = _("Press 'Apply' to create the requested data set or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed,
                                     gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(fixed, _("Create Data Set"))
        self.assistant.set_page_complete(fixed, True)

        self.assistant.show_all()

    def _create(self, button):
        """
        Method to create the desired data set.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        window = self.assistant.get_root_window()
        window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))

        _parts = dict()
        _data_set = []

        _starttime_ = 0.01
        if(self.chkIncludeZeroHour.get_active()):
            _starttime_ = 0.0

# TODO: Revise the following query to include the hardware id from tbl_incident.
# Select everything from the incident detail table in the Program database.
#   Index       Field
#     0      Incident ID
#     1      Part Number
#     2      Age at Incident
#     3      Failure
#     4      Suspension
#     5      CND/NFF
#     6      OCC
#     7      Initial Installation
#     8      Interval Censored
#     9      Assembly ID
        query = "SELECT t1.fld_incident_id, t1.fld_part_num, \
                        t1.fld_age_at_incident, t1.fld_failure, \
                        t1.fld_suspension, t1.fld_cnd_nff, t1.fld_occ_fault, \
                        t1.fld_initial_installation, \
                        t1.fld_interval_censored, t2.fld_hardware_id \
                 FROM tbl_incident_detail AS t1 \
                 INNER JOIN tbl_incident AS t2 \
                 ON t2.fld_incident_id=t1.fld_incident_id \
                 WHERE t1.fld_age_at_incident >= %f \
                 ORDER BY t1.fld_incident_id ASC" % _starttime_
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

# Create a dictionary using the incident id as the key and the remaining
# columns in a list as the value.
        n_parts = len(results)
        for i in range(n_parts):
            _parts[results[i][0]] = results[i][1:]

# Create a list of lists.
#    0.0 Unit
#    0.1.0 Part Number
#    0.1.1 Failure Time
#    0.1.2 Failure
#    0.1.3 Suspension
#    0.1.4 CND/NFF
#    0.1.5 OCC
#    0.1.6 Initial Installation
#    0.1.7 Interval Censored
#    0.1.8 Assembly ID
# ['HTC8128', (u'50468', 465.0, 0, 0, 0, 0, 0, 1, 4)]
        model = self._app.INCIDENT.model
        row = model.get_iter_root()

        while row is not None:
            _temp = []
# Append the "Affected Unit" from the INCIDENT Object's gtk.TreeView.  Then
# append the failure information from the _parts dictionary created above.
            try:
                _temp.append(model.get_value(row, 13))
                _temp.append(_parts[str(model.get_value(row, 1))][0:])
            except KeyError:
                # TODO: Add error log message here.
                pass

# Add the temporary record if it has all the information needed.
            if(len(_temp) == 2):
                _data_set.append(_temp)

            row = model.iter_next(row)

# Sort the data set by unit first, then age at time of failure.
        try:
            _data_set.sort(key=lambda x:(str(x[0]), float(x[1][1])))
        except IndexError:
            pass

# Add a new dataset.
        _confidence = float(self.txtConfidence.get_text())
        if(self.optDatabase.get_active()):
            query = "INSERT INTO tbl_dataset (fld_assembly_id, \
                                              fld_description, \
                                              fld_confidence) \
                     VALUES (%d, '%s', %f)" % \
                     (self._app.ASSEMBLY.assembly_id,
                      self.txtDescription.get_text(), _confidence)
            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx,
                                                 commit=True)

# Find the ID of the last dataset to be created.  This is the value that will
# be written to the fld_dtaset_id field in the tbl_survival_data table.
            if(_conf.BACKEND == 'mysql'):
                query = "SELECT LAST_INSERT_ID()"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "SELECT seq \
                         FROM sqlite_sequence \
                         WHERE name='tbl_dataset'"

            dataset_id = self._app.DB.execute_query(query,
                                                    None,
                                                    self._app.ProgCnx)
            dataset_id = dataset_id[0][0]
        else:
            dialog = gtk.FileChooserDialog(_("RelKit: Save Data Set to File ..."),
                                           None,
                                           gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                           (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                            gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
            dialog.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
            response = dialog.run()
            if(response == gtk.RESPONSE_ACCEPT):
                _filename = dialog.get_filename()

            dialog.destroy()

            dataset_id = 0

            f = open(_filename, 'w')
            f.write("Data Set Description: " + self.txtDescription.get_text() + "\n")
            f.write("\n")
            f.write("Dataset_ID\tLeft\tRight\tStatus\tQuantity\tUnit\tPart_Number\t \t \tTBF\tMode Type\n")

        try:
            _event = _data_set[0][1][2]
            _right = _data_set[0][1][3]
            _interval = _data_set[0][1][7]
        except IndexError:
            _event = 0
            _right = 0
            _interval = 1

        if(_event):
            _status = "Event"
        elif(_right):
            _status = "Right Censored"
        elif(_interval):
            _status = "Interval Censored"
        else:
            _status = "Interval Censored"

        _tbf = float(_data_set[0][1][1])
        values = (dataset_id, 0.0, float(_data_set[0][1][1]),
                  _status, 1, str(_data_set[0][0]),
                  str(_data_set[0][1][0]), '', '', float(_tbf), 0,
                  int(_data_set[0][1][8]))

# Insert the first data set record.
        _record_id = 1
        if(self.optDatabase.get_active()):
            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_survival_data \
                         (fld_record_id, fld_dataset_id, fld_left_interval, \
                          fld_right_interval, fld_status, fld_quantity, \
                          fld_unit, fld_part_num, fld_market, fld_model, \
                          fld_tbf, fld_mode_type, fld_assembly_id) \
                         VALUES (%d, %d, %f, %f, '%s', %d, '%s', '%s', '%s', \
                                 '%s', %f, %d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_survival_data \
                         (fld_record_id, fld_dataset_id, fld_left_interval, \
                          fld_right_interval, fld_status, fld_quantity, \
                          fld_unit, fld_part_num, fld_market, fld_model, \
                          fld_tbf, fld_mode_type, fld_assembly_id) \
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)
        else:
            f.write(str(_record_id) + '\t' + str(dataset_id) + '\t0.0' + '\t' +
                    str(_data_set[0][1][1]) + '\t' + _status + '\t1\t' +
                    str(_data_set[0][0]) + '\t' + str(_data_set[0][1][0]) +
                    '\t ' + '\t ' + '\t' + str(_tbf) + '0\t' +
                    str(_data_set[0][1][0]) + '\n')

        _unit = _data_set[0][0]             # Get the first unit.
        _record_id += 1
        for i in range(1, len(_data_set)):
            try:
                _event = _data_set[0][1][2]
                _right = _data_set[0][1][3]
                _interval = _data_set[0][1][7]
            except IndexError:
                _event = 0
                _right = 0
                _interval = 1

            if(_event):
                _status = "Event"
            elif(_right):
                _status = "Right Censored"
            elif(_interval):
                _status = "Interval Censored"
            else:
                _status = "Interval Censored"

            if(_data_set[i][0] == _unit):
                if(_data_set[i][1][1] != _data_set[i - 1][1][1]):
                    _left = _data_set[i - 1][1][1]
                else:
                    _left = 0.0
            else:
                _left = 0.0

            _tbf = float(_data_set[i][1][1]) - float(_left)

            if(self.optDatabase.get_active()):
                values = (_record_id, dataset_id, float(_left),
                          float(_data_set[i][1][1]), _status, 1,
                          str(_data_set[i][0]), str(_data_set[i][1][0]),
                          '', '', float(_tbf), 0, int(_data_set[i][1][8]))
                results = self._app.DB.execute_query(query,
                                                     values,
                                                     self._app.ProgCnx,
                                                     commit=True)
            else:
                f.write(str(_record_id)  + '\t' + str(dataset_id) + '\t' +
                        str(_left) + '\t' + str(_data_set[i][1][1]) + '\t' +
                        str(_status) + '\t1\t' + str(_data_set[i][0]) + '\t' +
                        str(_data_set[i][1][0]) + '\t ' + '\t ' + '\t' +
                        str(_tbf) + '0\t' + '\t ' +
                        str(_data_set[i][1][8]) + '\n')

            _unit = _data_set[i][0]
            _record_id += 1

        try:
            f.close()
        except UnboundLocalError:
            pass

        window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

# Load the dataset gtk.TreeView with the newly created dataset.
        self._app.DATASET.load_tree()
        _page = sum(_conf.RELIAFREE_MODULES[:11])
        self._app.winTree.notebook.set_current_page(_page - 1)

        return False

    def _cancel(self, button):
        """
        Method to destroy the gtk.Assistant when the 'Cancel' button is
        pressed.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        self.assistant.destroy()
