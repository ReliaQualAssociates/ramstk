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

    _fi_tab_labels = [[_("Incident ID:"), _("Incident Category:"),
                       _("Incident Type:"), _("Incident Status:"),
                       _("Incident Criticality:"), _("Incident Age:"),
                       _("Incident Lifecycle:")],
                      [_("Short Description:"), _("Long Description:"),
                       _("Remarks:"), _("Analysis:")],
                      [_("Found in Test:"), _("Found in Test Case:")],
                      [_("Requested By:"), _("Requested Date:"),
                       _("Reviewed By:"), _("Reviewed Date:"),
                       _("Approved By:"), _("Approved Date:"),
                       _("Closed By:"), _("Closed Date:")]]

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
        self.cmbCompound12 = _widg.make_combo(_width_=75)
        self.cmbCompound13 = _widg.make_combo(_width_=75)
        self.cmbCompound14 = _widg.make_combo(_width_=75)
        self.cmbCompound15 = _widg.make_combo(_width_=75)
        self.cmbCompound16 = _widg.make_combo(_width_=75)
        self.cmbCompound17 = _widg.make_combo(_width_=75)
        self.cmbCompound18 = _widg.make_combo(_width_=75)
        self.cmbCompound19 = _widg.make_combo(_width_=75)
        self.cmbCompound20 = _widg.make_combo(_width_=75)
        self.cmbCompound21 = _widg.make_combo(_width_=75)
        self.cmbCompound22 = _widg.make_combo(_width_=75)
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

# Create the page to select filter criteria related to the type, category,
# status, criticality, and age of the incident.
        self.cmbCriteriaID = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaID, self._criteria2)
        self.txtFilterID = _widg.make_entry(_width_=100)
        self.txtFilterID.set_tooltip_text(_("Sets the incident ID filter criterion."))

        self.cmbCriteriaCategory = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaCategory, self._criteria3)
        self.cmbFilterCategory = _widg.make_combo(_width_=100)
        self.cmbFilterCategory.set_tooltip_text(_("Sets the incident category filter criterion."))
        query = "SELECT fld_incident_cat_name FROM tbl_incident_category"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ComCnx)
        _widg.load_combo(self.cmbFilterCategory, results, simple=True)

        self.cmbCriteriaType = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaType, self._criteria3)
        self.cmbFilterType = _widg.make_combo(_width_=100)
        self.cmbFilterType.set_tooltip_text(_("Sets the incident type filter criterion."))
        query = "SELECT fld_incident_type_name \
                 FROM tbl_incident_type"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ComCnx)
        _widg.load_combo(self.cmbFilterType, results, simple=True)

        self.cmbCriteriaStatus = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaStatus, self._criteria3)
        self.cmbFilterStatus = _widg.make_combo(_width_=100)
        self.cmbFilterStatus.set_tooltip_text(_("Sets the incident status filter criterion."))
        query = "SELECT fld_status_name FROM tbl_status"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ComCnx)
        _widg.load_combo(self.cmbFilterStatus, results, simple=True)

        self.cmbCriteriaCriticality = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaCriticality, self._criteria3)
        self.cmbFilterCriticality = _widg.make_combo(_width_=100)
        self.cmbFilterCriticality.set_tooltip_text(_("Sets the incident criticality filter criterion."))
        query = "SELECT fld_criticality_name FROM tbl_criticality"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ComCnx)
        _widg.load_combo(self.cmbFilterCriticality, results, simple=True)

        self.cmbCriteriaAge = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaAge, self._criteria2)
        self.txtFilterAge = _widg.make_entry(_width_=100)
        self.txtFilterAge.set_tooltip_text(_("Sets the incident age filter criterion."))

        self.cmbCriteriaLifeCycle = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaLifeCycle, self._criteria2)
        self.cmbFilterLifeCycle = _widg.make_combo(_width_=100)
        self.cmbFilterLifeCycle.set_tooltip_text(_("Sets the incident life cycle filter criterion."))
        query = "SELECT fld_lifecycle_name FROM tbl_lifecycles"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ComCnx)
        _widg.load_combo(self.cmbFilterLifeCycle, results, simple=True)

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

        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(fixed, _("Set Filter Criteria: Incident Status"))
        self.assistant.set_page_complete(fixed, True)

# Create the page to select filter criteria related to the short description,
# long description, remarks, and analysis of the incident.
        self.cmbCriteriaShortDesc = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaShortDesc, self._criteria1)
        self.txtFilterShortDesc = _widg.make_entry(_width_=100)
        self.txtFilterShortDesc.set_tooltip_text(_("Sets the field incident short description filter criterion."))

        self.cmbCriteriaLongDesc = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaLongDesc, self._criteria1)
        self.txtFilterLongDesc = _widg.make_entry(_width_=100)
        self.txtFilterLongDesc.set_tooltip_text(_("Sets the incident long description filter criterion."))

        self.cmbCriteriaRemarks = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaRemarks, self._criteria1)
        self.txtFilterRemarks = _widg.make_entry(_width_=100)
        self.txtFilterRemarks.set_tooltip_text(_("Sets the incident closure remarks filter criterion."))

        self.cmbCriteriaAnalysis = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaAnalysis, self._criteria1)
        self.txtFilterAnalysis = _widg.make_entry(_width_=100)
        self.txtFilterAnalysis.set_tooltip_text(_("Sets the incident analysis filter criterion."))

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

# Create the page to select filter criteria related to the test and test case
# that discoverd the problem reported in the incident.
        self.cmbCriteriaTest = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaTest, self._criteria1)
        self.txtFilterTest = _widg.make_entry(_width_=100)
        self.txtFilterTest.set_tooltip_text(_("Sets the incident test filter criterion."))

        self.cmbCriteriaTestCase = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaTestCase, self._criteria1)
        self.txtFilterTestCase = _widg.make_entry(_width_=100)
        self.txtFilterTestCase.set_tooltip_text(_("Sets the incident test case filter criterion."))

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
        self.assistant.set_page_title(fixed, _("Set Filter Criteria: Test Information"))
        self.assistant.set_page_complete(fixed, True)

# Create the page to select filter criteria reliated to the request by, request
# date, reviewed by, reviewed date, approved by, approved date, closed by, and
# closed date of the incident.
        self.cmbCriteriaRequestBy = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaRequestBy, self._criteria3)
        self.cmbFilterRequestBy = _widg.make_combo(_width_=100)
        self.cmbFilterRequestBy.set_tooltip_text(_("Sets the incident requested by filter criterion."))
        query = "SELECT fld_user_lname || ', ' || fld_user_fname \
                 FROM tbl_users"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ComCnx)
        _widg.load_combo(self.cmbFilterRequestBy, results, simple=True)

        self.cmbCriteriaRequestDate = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaRequestDate, self._criteria2)
        self.txtFilterRequestDate = _widg.make_entry(_width_=100)
        self.txtFilterRequestDate.set_tooltip_text(_("Sets the incident requested date filter criterion."))

        self.cmbCriteriaReviewBy = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaReviewBy, self._criteria3)
        self.cmbFilterReviewBy = _widg.make_combo(_width_=100)
        self.cmbFilterReviewBy.set_tooltip_text(_("Sets the incident reviewed by filter criterion."))
        _widg.load_combo(self.cmbFilterReviewBy, results, simple=True)

        self.cmbCriteriaReviewDate = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaReviewDate, self._criteria2)
        self.txtFilterReviewDate = _widg.make_entry(_width_=100)
        self.txtFilterReviewDate.set_tooltip_text(_("Sets the incident reviewed date filter criterion."))

        self.cmbCriteriaApproveBy = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaApproveBy, self._criteria3)
        self.cmbFilterApproveBy = _widg.make_combo(_width_=100)
        self.cmbFilterApproveBy.set_tooltip_text(_("Sets the incident approved by filter criterion."))
        _widg.load_combo(self.cmbFilterApproveBy, results, simple=True)

        self.cmbCriteriaApproveDate = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaApproveDate, self._criteria2)
        self.txtFilterApproveDate = _widg.make_entry(_width_=100)
        self.txtFilterApproveDate.set_tooltip_text(_("Sets the incident approved date filter criterion."))

        self.cmbCriteriaCloseBy = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaCloseBy, self._criteria3)
        self.cmbFilterCloseBy = _widg.make_combo(_width_=100)
        self.cmbFilterCloseBy.set_tooltip_text(_("Sets the incident closed by filter criterion."))
        _widg.load_combo(self.cmbFilterCloseBy, results, simple=True)

        self.cmbCriteriaCloseDate = _widg.make_combo(_width_=100)
        _widg.load_combo(self.cmbCriteriaCloseDate, self._criteria2)
        self.txtFilterCloseDate = _widg.make_entry(_width_=100)
        self.txtFilterCloseDate.set_tooltip_text(_("Sets the incident closed date filter criterion."))

        self.chkFilterAccepted = _widg.make_check_button(_label_=_("Is Accepted"))
        self.chkFilterAccepted.set_tooltip_text(_("Only return accepted or unaccepted incidents."))

        self.chkFilterReviewed = _widg.make_check_button(_label_=_("Is Reviewed"))
        self.chkFilterReviewed.set_tooltip_text(_("Only return reviewed or unreviewed incidents."))

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
        self.assistant.set_page_title(fixed, _("Set Filter Criteria: People and Dates"))
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

        from datetime import datetime

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
        if(_compound[0] is not None and _compound[0] != ''):
            query = query + " " + _compound[0] + " "

        if(_criteria[1] is not None and _criteria[1] != ''):
            query = query + "fld_incident_category" + _criteria[1] + \
                    str(_inputs[1])
        if(_compound[1] is not None and _compound[1] != ''):
            query = query + " " + _compound[1] + " "

        if(_criteria[2] is not None and _criteria[2] != ''):
            query = query + "fld_incident_type" + _criteria[2] + \
                    str(_inputs[2])
        if(_compound[2] is not None and _compound[2] != ''):
            query = query + " " + _compound[2] + " "

        if(_criteria[3] is not None and _criteria[3] != ''):
            query = query + "fld_status" + _criteria[3] + \
                    str(_inputs[3])
        if(_compound[3] is not None and _compound[3] != ''):
            query = query + " " + _compound[3] + " "

        if(_criteria[4] is not None and _criteria[4] != ''):
            query = query + "fld_criticality" + _criteria[4] + \
                    str(_inputs[4])
        if(_compound[4] is not None and _compound[4] != ''):
            query = query + " " + _compound[4] + " "

        if(_criteria[5] is not None and _criteria[5] != ''):
            query =  query + "fld_incident_age" + _criteria[5] + \
                     str(_inputs[5])
        if(_compound[5] is not None and _compound[5] != ''):
            query = query + " " + _compound[5] + " "

        if(_criteria[6] is not None and _criteria[6] != ''):
            query =  query + "fld_life_cycle" + _criteria[6] + \
                     str(_inputs[6])
        if(_compound[6] is not None and _compound[6] != ''):
            query = query + " " + _compound[6] + " "

        if(_criteria[7] is not None and _criteria[7] != ''):
            query = query + "fld_short_description " + _criteria[7] + \
                    " '%" + _inputs[7] + "%'"
        if(_compound[7] is not None and _compound[7] != ''):
            query = query + " " + _compound[7] + " "

        if(_criteria[8] is not None and _criteria[8] != ''):
            query = query + "fld_long_description " + _criteria[8] + \
                    " '%" + _inputs[8] + "%'"
        if(_compound[8] is not None and _compound[8] != ''):
            query = query + " " + _compound[8] + " "

        if(_criteria[9] is not None and _criteria[9] != ''):
            query = query + "fld_remarks " + _criteria[9] + \
                    " '%" + _inputs[9] + "%'"
        if(_compound[9] is not None and _compound[9] != ''):
            query = query + " " + _compound[9] + " "

        if(_criteria[10] is not None and _compound[10] != ''):
            query = query + "fld_analysis " + _criteria[10] + \
                    " '%" + _inputs[10] + "%'"
        if(_compound[10] is not None and _compound[10] != ''):
            query = query + " " + _compound[10] + " "

        if(_criteria[11] is not None and _compound[11] != ''):
            query = query + "fld_test_found " + _criteria[11] + \
                    " '%" + _inputs[11] + "%'"
        if(_compound[11] is not None and _compound[11] != ''):
            query = query + " " + _compound[11] + " "

        if(_criteria[12] is not None and _compound[12] != ''):
            query = query + "fld_test_case " + _criteria[12] + \
                    " '%" + _inputs[12] + "%'"
        if(_compound[12] is not None and _compound[12] != ''):
            query = query + " " + _compound[12] + " "

        if(_criteria[13] is not None and _compound[13] != ''):
            query = query + "fld_request_by" + _criteria[13] + \
                    "'" + _inputs[13] + "'"
        if(_compound[13] is not None and _compound[13] != ''):
            query = query + " " + _compound[13] + " "

        if(_criteria[14] is not None and _compound[14] != ''):
            query = query + "fld_request_date" + _criteria[14] + \
                    str(datetime.strptime(_inputs[14],"%Y-%m-%d").toordinal())
        if(_compound[14] is not None and _compound[14] != ''):
            query = query + " " + _compound[14] + " "

        if(_criteria[15] is not None and _compound[15] != ''):
            query = query + "fld_reviewed_by" + _criteria[15] + \
                    "'" + _inputs[15] + "'"
        if(_compound[15] is not None and _compound[15] != ''):
            query = query + " " + _compound[15] + " "

        if(_criteria[16] is not None and _compound[16] != ''):
            query = query + "fld_reviewed_date" + _criteria[16] + \
                    str(datetime.strptime(_inputs[16],"%Y-%m-%d").toordinal())
        if(_compound[16] is not None and _compound[16] != ''):
            query = query + " " + _compound[16] + " "

        if(_criteria[17] is not None and _compound[17] != ''):
            query = query + "fld_approved_by" + _criteria[17] + \
                    "'" + _inputs[17] + "'"
        if(_compound[17] is not None and _compound[17] != ''):
            query = query + " " + _compound[17] + " "

        if(_criteria[18] is not None and _compound[18] != ''):
            query = query + "fld_approved_date" + _criteria[18] + \
                    str(datetime.strptime(_inputs[18],"%Y-%m-%d").toordinal())
        if(_compound[18] is not None and _compound[18] != ''):
            query = query + " " + _compound[18] + " "

        if(_criteria[19] is not None and _compound[19] != ''):
            query = query + "fld_complete_by" + _criteria[19] + \
                    "'" + _inputs[19] + "'"
        if(_compound[19] is not None and _compound[19] != ''):
            query = query + " " + _compound[19] + " "

        if(_criteria[20] is not None and _compound[20] != ''):
            query = query + "fld_complete_date" + _criteria[20] + \
                    str(datetime.strptime(_inputs[20],"%Y-%m-%d").toordinal())
        if(_compound[20] is not None and _compound[20] != ''):
            query = query + " " + _compound[20] + " "

        if(_inputs[21]):
            query = query + "fld_accepted=%d" % 1
        if(_compound[21] is not None and _compound[21] != ''):
            query = query + " " + _compound[21] + " "

        if(_inputs[22]):
            query = query + "fld_reviewed=%d" % 1

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
