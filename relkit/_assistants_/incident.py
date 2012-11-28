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

class FilterIncident:

# Lists of search criteria to use for the various gtk.Combo widgets.
    _criteria0 = [["="], ["!="], [">"], ["<"], [">="], ["<="],
                  [_("LIKE")], [_("NOT LIKE")]]
    _criteria1 = [[_("LIKE")], [_("NOT LIKE")]]
    _criteria2 = [["="], ["!="], [">"], ["<"], [">="], ["<="]]
    _criteria3 = [["="], ["!="]]

    _compound = [[_("AND")], [_("OR")]]

    _fi_tab_labels = [[_("Incident ID:"), _("Incident Type:"),
                       _("Incident Status:"), _("Date Opened:"),
                       _("Date Closed:"), _("Incident Age:"),
                       _("Affected Unit:"), _("Affected System:"),
                       _("Accepted"), _("Reviewed")],
                      [_("Brief Description:"), _("Long Description:"),
                       _("Closure Remarks:")],
                      [],
                      [_("Incident ID"), _("Incident Type"),
                       _("Short Description"), _("Long Description"),
                       _("Remarks"), _("Incident Date"), _("Closure Date"),
                       _("Incident Age"), _("Status"), _("Affected Unit"),
                       _("Affected System"), _("Is Accepted"),
                       _("Is Reviewed")]]

    def __init__(self, button, app):

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_("RelKit Filter Incidents Assistant"))
        self.assistant.connect('apply', self._filter)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

        # Create the introduction page.
        fixed = gtk.Fixed()
        _text_ = _("This is the RelKit incident filter assistant.\n\nIt will help you filter program incidents in the database so you can view only those you're interested in seeing.\n\nPress 'Forward' to continue or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(fixed, _("Introduction"))
        self.assistant.set_page_complete(fixed, True)

# Create the gtk.Combo widgets that will be used to select compounding
# statements (i.e., AND, OR).
        self.cmbCompound1 = _widg.make_combo(_width_=75)
        self.cmbCompound2 = _widg.make_combo(_width_=75)
        self.cmbCompound3 = _widg.make_combo(_width_=75)
        self.cmbCompound4 = _widg.make_combo(_width_=75)
        self.cmbCompound5 = _widg.make_combo(_width_=75)
        self.cmbCompound6 = _widg.make_combo(_width_=75)
        self.cmbCompound7 = _widg.make_combo(_width_=75)
        self.cmbCompound8 = _widg.make_combo(_width_=75)
        self.cmbCompound9 = _widg.make_combo(_width_=75)
        self.cmbCompound10 = _widg.make_combo(_width_=75)
        self.cmbCompound11 = _widg.make_combo(_width_=75)
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

# Create the gtk.Combo widgets that will be used to select the comparison
# criteria (e.g., =, <>, LIKE, etc.) for the different fields.
        self.cmbFilterIncidentID = _widg.make_combo(_width_=100)
        self.cmbFilterIncidentID.set_tooltip_text(_("Sets the field incident ID filter criterion."))
        _widg.load_combo(self.cmbFilterIncidentID, self._criteria0)

        self.cmbFilterIncidentType = _widg.make_combo(_width_=100)
        self.cmbFilterIncidentType.set_tooltip_text(_("Sets the field incident type filter criterion."))
        _widg.load_combo(self.cmbFilterIncidentType, self._criteria3)

        self.cmbFilterIncidentTypeList = _widg.make_combo(_width_=100)
        self.cmbFilterIncidentTypeList.set_tooltip_text(_("Sets the field incident type filter criterion."))
        query = "SELECT fld_incident_type_name \
                 FROM tbl_incident_type"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ComCnx)
        _widg.load_combo(self.cmbFilterIncidentTypeList, results, simple=True)

        self.cmbFilterShortDesc = _widg.make_combo(_width_=100)
        self.cmbFilterShortDesc.set_tooltip_text(_("Sets the field incident short description filter criterion."))
        _widg.load_combo(self.cmbFilterShortDesc, self._criteria1)

        self.cmbFilterLongDesc = _widg.make_combo(_width_=100)
        self.cmbFilterLongDesc.set_tooltip_text(_("Sets the field incident long description filter criterion."))
        _widg.load_combo(self.cmbFilterLongDesc, self._criteria1)

        self.cmbFilterRemarks = _widg.make_combo(_width_=100)
        self.cmbFilterRemarks.set_tooltip_text(_("Sets the field incident closure remarks filter criterion."))
        _widg.load_combo(self.cmbFilterRemarks, self._criteria1)

        self.cmbFilterIncidentDate = _widg.make_combo(_width_=100)
        self.cmbFilterIncidentDate.set_tooltip_text(_("Sets the field incident occurrence date filter criterion."))
        _widg.load_combo(self.cmbFilterIncidentDate, self._criteria2)

        self.cmbFilterClosureDate = _widg.make_combo(_width_=100)
        self.cmbFilterClosureDate.set_tooltip_text(_("Sets the field incident closure date filter criterion."))
        _widg.load_combo(self.cmbFilterClosureDate, self._criteria2)

        self.cmbFilterIncidentAge = _widg.make_combo(_width_=100)
        self.cmbFilterIncidentAge.set_tooltip_text(_("Sets the field incident age filter criterion."))
        _widg.load_combo(self.cmbFilterIncidentAge, self._criteria2)

        self.cmbFilterStatus = _widg.make_combo(_width_=100)
        self.cmbFilterStatus.set_tooltip_text(_("Sets the field incident status filter criterion."))
        _widg.load_combo(self.cmbFilterStatus, self._criteria3)

        self.cmbFilterMachine = _widg.make_combo(_width_=100)
        self.cmbFilterMachine.set_tooltip_text(_("Sets the field incident unit serial number filter criterion."))
        _widg.load_combo(self.cmbFilterMachine, self._criteria2)

        self.cmbFilterSystem = _widg.make_combo(_width_=100)
        self.cmbFilterSystem.set_tooltip_text(_("Sets the field incident affected system filter criterion."))
        _widg.load_combo(self.cmbFilterSystem, self._criteria3)

        self.cmbFilterSystemList = _widg.make_combo(_width_=100)
        self.cmbFilterSystemList.set_tooltip_text(_("Sets the field incident affected system filter criterion."))
        query = "SELECT fld_name \
                 FROM tbl_system \
                 WHERE fld_parent_assembly='0' \
                 AND fld_part=0"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)
        _widg.load_combo(self.cmbFilterSystemList, results, simple=True)

# Create the gtk.Entry widgets used to provide the user-desired filter criteria
        self.txtFilterIncidentID = _widg.make_entry(_width_=100)
        self.txtFilterIncidentID.set_tooltip_text(_("Sets the field incident ID filter criterion."))

        self.txtFilterShortDesc = _widg.make_entry(_width_=100)
        self.txtFilterShortDesc.set_tooltip_text(_("Sets the field incident short description filter criterion."))

        self.txtFilterLongDesc = _widg.make_entry(_width_=100)
        self.txtFilterLongDesc.set_tooltip_text(_("Sets the field incident long description filter criterion."))

        self.txtFilterRemarks = _widg.make_entry(_width_=100)
        self.txtFilterRemarks.set_tooltip_text(_("Sets the field incident closure remarks filter criterion."))

        self.txtFilterIncidentDate = _widg.make_entry(_width_=100)
        self.txtFilterIncidentDate.set_tooltip_text(_("Sets the field incident occurrence date filter criterion."))

        self.txtFilterClosureDate = _widg.make_entry(_width_=100)
        self.txtFilterClosureDate.set_tooltip_text(_("Sets the field incident closure date filter criterion."))

        self.txtFilterIncidentAge = _widg.make_entry(_width_=100)
        self.txtFilterIncidentAge.set_tooltip_text(_("Sets the field incident age filter criterion."))

        self.txtFilterStatus = _widg.make_entry(_width_=100)
        self.txtFilterStatus.set_tooltip_text(_("Sets the field incident status filter criterion."))

        self.txtFilterMachine = _widg.make_entry(_width_=100)
        self.txtFilterMachine.set_tooltip_text(_("Sets the field incident unit serial number filter criterion."))

        self.chkFilterAccepted = _widg.make_check_button(self._fi_tab_labels[3][11])
        self.chkFilterAccepted.set_tooltip_text(_("Deletes the selected component from the selected field incident."))

        self.chkFilterReviewed = _widg.make_check_button(self._fi_tab_labels[3][12])
        self.chkFilterReviewed.set_tooltip_text(_("Deletes the selected component from the selected field incident."))

# Create the page to select filter criteria.
        y_pos = 5
        fixed = gtk.Fixed()
        _text_ = _("Create Program Incident filter...")
        label = _widg.make_label(_text_, width=300)
        fixed.put(label, 5, y_pos)
        y_pos += 30

        for i in range(len(self._fi_tab_labels[3]) - 2):
            label = _widg.make_label(self._fi_tab_labels[3][i], 150, 25)
            fixed.put(label, 5, (35 * i + y_pos))

        fixed.put(self.cmbFilterIncidentID, 190, y_pos)
        fixed.put(self.txtFilterIncidentID, 300, y_pos)
        fixed.put(self.cmbCompound1, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbFilterIncidentType, 190, y_pos)
        fixed.put(self.cmbFilterIncidentTypeList, 300, y_pos)
        fixed.put(self.cmbCompound2, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbFilterShortDesc, 190, y_pos)
        fixed.put(self.txtFilterShortDesc, 300, y_pos)
        fixed.put(self.cmbCompound3, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbFilterLongDesc, 190, y_pos)
        fixed.put(self.txtFilterLongDesc, 300, y_pos)
        fixed.put(self.cmbCompound4, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbFilterRemarks, 190, y_pos)
        fixed.put(self.txtFilterRemarks, 300, y_pos)
        fixed.put(self.cmbCompound5, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbFilterIncidentDate, 190, y_pos)
        fixed.put(self.txtFilterIncidentDate, 300, y_pos)
        fixed.put(self.cmbCompound6, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbFilterClosureDate, 190, y_pos)
        fixed.put(self.txtFilterClosureDate, 300, y_pos)
        fixed.put(self.cmbCompound7, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbFilterIncidentAge, 190, y_pos)
        fixed.put(self.txtFilterIncidentAge, 300, y_pos)
        fixed.put(self.cmbCompound8, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbFilterStatus, 190, y_pos)
        fixed.put(self.txtFilterStatus, 300, y_pos)
        fixed.put(self.cmbCompound9, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbFilterMachine, 190, y_pos)
        fixed.put(self.txtFilterMachine, 300, y_pos)
        fixed.put(self.cmbCompound10, 410, y_pos)
        y_pos += 35

        fixed.put(self.cmbFilterSystem, 190, y_pos)
        fixed.put(self.cmbFilterSystemList, 300, y_pos)
        fixed.put(self.cmbCompound11, 410, y_pos)
        y_pos += 35

        fixed.put(self.chkFilterAccepted, 15, y_pos)
        y_pos += 35

        fixed.put(self.chkFilterReviewed, 15, y_pos)

        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(fixed, _("Set Filter Criteria"))
        self.assistant.set_page_complete(fixed, True)

# Create the page to apply the filter criteria.
        fixed = gtk.Fixed()
        _text_ = _("Press 'Apply' to apply the filter criteria or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed,
                                     gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(fixed, _("Apply Filter Criteria"))
        self.assistant.set_page_complete(fixed, True)

        self.assistant.show_all()

    def _filter(self, button):
        """
        Method to create the SQL query for filtering the Program Incidents.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        _criteria = []
        _inputs = []
        _connectors = []

        # Read the user inputs for the different fields that can be used to
        # filter with.
        _criteria.append(self.cmbFilterIncidentID.get_active_text())
        _inputs.append(self.txtFilterIncidentID.get_text())
        _connectors.append(self.cmbCompound1.get_active_text())

        _criteria.append(self.cmbFilterIncidentType.get_active_text())
        _inputs.append(self.cmbFilterIncidentTypeList.get_active_text())
        _connectors.append(self.cmbCompound2.get_active_text())

        _criteria.append(self.cmbFilterShortDesc.get_active_text())
        _inputs.append(self.txtFilterShortDesc.get_text())
        _connectors.append(self.cmbCompound3.get_active_text())

        _criteria.append(self.cmbFilterLongDesc.get_active_text())
        _inputs.append(self.txtFilterLongDesc.get_text())
        _connectors.append(self.cmbCompound4.get_active_text())

        _criteria.append(self.cmbFilterRemarks.get_active_text())
        _inputs.append(self.txtFilterRemarks.get_text())
        _connectors.append(self.cmbCompound5.get_active_text())

        _criteria.append(self.cmbFilterIncidentDate.get_active_text())
        _inputs.append(self.txtFilterIncidentDate.get_text())
        _connectors.append(self.cmbCompound6.get_active_text())

        _criteria.append(self.cmbFilterClosureDate.get_active_text())
        _inputs.append(self.txtFilterClosureDate.get_text())
        _connectors.append(self.cmbCompound7.get_active_text())

        _criteria.append(self.cmbFilterIncidentAge.get_active_text())
        _inputs.append(self.txtFilterIncidentAge.get_text())
        _connectors.append(self.cmbCompound8.get_active_text())

        _criteria.append(self.cmbFilterStatus.get_active_text())
        _inputs.append(self.txtFilterStatus.get_text())
        _connectors.append(self.cmbCompound9.get_active_text())

        _criteria.append(self.cmbFilterMachine.get_active_text())
        _inputs.append(self.txtFilterMachine.get_text())
        _connectors.append(self.cmbCompound10.get_active_text())

        _criteria.append(self.cmbFilterSystem.get_active_text())
        _inputs.append(self.cmbFilterSystemList.get_active())
        _connectors.append(self.cmbCompound11.get_active_text())

        _inputs.append(self.chkFilterAccepted.get_active())
        _inputs.append(self.chkFilterReviewed.get_active())

        # Build the query from the user-provided inputs.
        if(_conf.RELIAFREE_MODULES[0] == 1):
            query = "SELECT * FROM tbl_incident \
                     WHERE fld_revision_id=%d AND " % \
            self._app.REVISION.revision_id
        else:
            query = "SELECT * FROM tbl_incident \
                     WHERE fld_revision_id=0 AND "

        if(_criteria[0] is not None and _criteria[0] != ''):
            query = query + "fld_incident_id" + _criteria[0] + _inputs[0]
        if(_connectors[0] is not None and _connectors[0] != ''):
            query = query + " " + _connectors[0] + " "

        if(_criteria[1] is not None and _criteria[1] != ''):
            query = query + "fld_incident_type" + _criteria[1] + \
                    "'" + _inputs[1] + "'"
        if(_connectors[1] is not None and _connectors[1] != ''):
            query = query + " " + _connectors[1] + " "

        if(_criteria[2] is not None and _criteria[2] != ''):
            query = query + "fld_short_description " + _criteria[2] + \
                    " '%" + _inputs[2] + "%'"
        if(_connectors[2] is not None and _connectors[2] != ''):
            query = query + " " + _connectors[2] + " "

        if(_criteria[3] is not None and _criteria[3] != ''):
            query = query + "fld_long_description " + _criteria[3] + \
                    " '%" + _inputs[3] + "%'"
        if(_connectors[3] is not None and _connectors[3] != ''):
            query = query + " " + _connectors[3] + " "

        if(_criteria[4] is not None and _criteria[4] != ''):
            query = query + "fld_remarks " + _criteria[4] + \
                    " '%" + _inputs[4] + "%'"
        if(_connectors[4] is not None and _connectors[4] != ''):
            query = query + " " + _connectors[4] + " "

        if(_criteria[5] is not None and _criteria[5] != ''):
            query =  query + "fld_request_date" + _criteria[5] + \
                     "'" + _inputs[5] + "'"
        if(_connectors[5] is not None and _connectors[5] != ''):
            query = query + " " + _connectors[5] + " "

        if(_criteria[6] is not None and _criteria[6] != ''):
            query = query + "fld_complete_date" + _criteria[6] + \
                    "'" + _inputs[6] + "'"
        if(_connectors[6] is not None and _connectors[6] != ''):
            query = query + " " + _connectors[6] + " "

        if(_criteria[7] is not None and _criteria[7] != ''):
            query = query + "fld_incident_age" + _criteria[7]
            query = query + "%d" % int(_inputs[7])
        if(_connectors[7] is not None and _connectors[7] != ''):
            query = query + " " + _connectors[7] + " "

        if(_criteria[8] is not None and _criteria[8] != ''):
            query = query + "fld_status" + _criteria[8] + \
                    "'" + _inputs[8] + "'"
        if(_connectors[8] is not None and _connectors[8] != ''):
            query = query + " " + _connectors[8] + " "

        if(_criteria[9] is not None and _connectors[9] != ''):
            query = query + "fld_machine" + _criteria[9] + \
                    "'" + _inputs[9] + "'"
        if(_connectors[9] is not None and _connectors[9] != ''):
            query = query + " " + _connectors[9] + " "

        if(_inputs[11]):
            query = query + " AND fld_accepted=%d" % 1
        else:
            query = query + " AND fld_accepted=%d" % 0

        if(_inputs[12]):
            query = query + " AND fld_reviewed=%d" % 1
        else:
            query = query + " AND fld_reviewed=%d" % 0

        self._app.INCIDENT.load_tree(query, None)

    def _cancel(self, button):
        """
        Method to destroy the gtk.Assistant when the 'Cancel' button is
        pressed.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        self.assistant.destroy()

class AddIncident:

    def __init__(self, button, app):

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

    def _cancel(self, button):
        """
        Method to destroy the gtk.Assistant when the 'Cancel' button is
        pressed.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        self.assistant.destroy()

class ImportIncident:

    def __init__(self, button, app):

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_("RelKit Import Incidents Assistant"))
        #self.assistant.connect('apply', self._import)
        self.assistant.connect('cancel', self._cancel)

        # Create the introduction page.
        fixed = gtk.Fixed()
        _text_ = _("This is the RelKit incident filter assistant.  It will help you import program incidents to the database from external files.  Press 'Forward' to continue or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=300, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(fixed, _("Introduction"))
        self.assistant.set_page_complete(fixed, True)

        self.assistant.show_all()
