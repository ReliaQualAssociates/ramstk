#!/usr/bin/env python
'''
Module containing various assistants for adding or creating objects in the
open RTK Program database.  This module contains assistants to guide the user
through the following:

1. Adding a new Revision.
2. Adding a new Test Plan.
3. Adding a new record to a Test Plan.
4. Adding a new Program Incident.
5. Creating a new Survival Analysis data set from program incidents.
6. Adding a new record to a Survival Analysis data set.
'''

__author__ = 'Andrew Rowland <andrew.rowland@reliaqual.com>'
__copyright__ = 'Copyright 2012 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       addrecord.py is part of The RTK Project
#
# All rights reserved.

import os
import sys
import pango

from os import environ, name
from datetime import date, datetime

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
    import rtk.configuration as _conf       #pylint: disable=F0401
    import rtk.utilities as _util           #pylint: disable=F0401
    import rtk.widgets as _widg             #pylint: disable=F0401
except ImportError:
    import configuration as _conf           #pylint: disable=F0401
    import utilities as _util               #pylint: disable=F0401
    import widgets as _widg                 #pylint: disable=F0401

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, "")

import gettext
_ = gettext.gettext


class AddRevision(object):
    """
    This is the assistant that walks the user through the process of adding
    a new revision to the open RTK Program database.
    """

    def __init__(self, __button, app):
        """
        Initialize on instance of the Add Revision Assistant.

        :param __button: the gtk.Button() widget that called the assistant.
        :type __button: gtk.Button
        :param app: the instance of the RTK application calling the assistant.
        :type app: RTK application
        """

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_(u"RTK Revision Addition Assistant"))
        self.assistant.connect('apply', self._add_revision)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

        # Create the introduction page.
        _fixed = gtk.Fixed()
        _text = _(u"This is the RTK Revision Addition Assistant.  It will "
                  u"help you add a new revision to the database.  Press "
                  u"'Forward' to continue or 'Cancel' to quit the assistant.")
        _label = _widg.make_label(_text, width=-1, height=150)
        _fixed.put(_label, 5, 5)
        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(_fixed, _(u"Introduction"))
        self.assistant.set_page_complete(_fixed, True)

        # Create the pages to select other information to add.
        y_pos = 5
        self.fxdPageOtherInfo = gtk.Fixed()
        _label = _widg.make_label(_(u"Select additional information "
                                    u"to add..."), width=300)
        self.fxdPageOtherInfo.put(_label, 5, y_pos)
        y_pos += 30

        self.chkFunction = gtk.CheckButton(_(u"_Functions"))
        self.fxdPageOtherInfo.put(self.chkFunction, 5, y_pos)
        y_pos += 30

        self.chkFunctionMatrix = gtk.CheckButton(_(u"Functional _Matrix"))
        self.fxdPageOtherInfo.put(self.chkFunctionMatrix, 5, y_pos)
        y_pos += 30

        self.chkRequirements = gtk.CheckButton(_(u"_Requirements"))
        self.fxdPageOtherInfo.put(self.chkRequirements, 5, y_pos)
        y_pos += 30

        self.chkHardware = gtk.CheckButton(_(u"_Hardware"))
        self.fxdPageOtherInfo.put(self.chkHardware, 5, y_pos)
        y_pos += 30

        self.chkFailureInfo = gtk.CheckButton(_(u"Include reliability "
                                                u"information"))
        self.fxdPageOtherInfo.put(self.chkFailureInfo, 5, y_pos)
        y_pos += 30

        _label = _widg.make_label(_(u"Select existing Revision to duplicate."),
                                  width=300)
        self.cmbBaseRevision = _widg.make_combo(simple=False)
        self.fxdPageOtherInfo.put(_label, 5, y_pos)
        self.fxdPageOtherInfo.put(self.cmbBaseRevision, 305, y_pos)

        _query = "SELECT fld_revision_code, fld_name, fld_revision_id \
                  FROM tbl_revisions"
        _results = self._app.DB.execute_query(_query,
                                              None,
                                              self._app.ProgCnx)

        _list = []
        for i in range(len(_results)):
            _list.append([_results[i][0] + '-' + _results[i][1], '',
                          _results[i][2]])
        _widg.load_combo(self.cmbBaseRevision, _list, simple=False)

        self.assistant.append_page(self.fxdPageOtherInfo)
        self.assistant.set_page_type(self.fxdPageOtherInfo,
                                     gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(self.fxdPageOtherInfo,
                                      _(u"Select Additional Information to Add"))
        self.assistant.set_page_complete(self.fxdPageOtherInfo, True)

        # Create the software incident general information page.
        self.fxdPageSetValues = gtk.Fixed()
        _label = _widg.make_label(_(u"Revision Code:"))
        self.txtRevisionCode = _widg.make_entry(width=100)
        self.txtRevisionCode.set_tooltip_text(_(u"Enter a code for the new "
                                                u"revision.  Leave blank to "
                                                u"use the default revision "
                                                u"code."))
        self.fxdPageSetValues.put(_label, 5, 5)
        self.fxdPageSetValues.put(self.txtRevisionCode, 200, 5)

        _label = _widg.make_label(_(u"Revision Name:"))
        self.txtRevisionName = _widg.make_entry()
        self.txtRevisionName.set_tooltip_text(_(u"Enter a name for the new "
                                                u"revision.  Leave blank to "
                                                u"use the default revision "
                                                u"name."))
        self.fxdPageSetValues.put(_label, 5, 35)
        self.fxdPageSetValues.put(self.txtRevisionName, 200, 35)

        _label = _widg.make_label(_(u"Remarks:"))
        self.txtRemarks = gtk.TextBuffer()
        self.fxdPageSetValues.put(_label, 5, 65)
        _textview_ = _widg.make_text_view(buffer=self.txtRemarks,
                                          width=300, height=100)
        self.fxdPageSetValues.put(_textview_, 200, 65)

        self.assistant.append_page(self.fxdPageSetValues)
        self.assistant.set_page_type(self.fxdPageSetValues,
                                     gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(self.fxdPageSetValues, _(u"Set Values "
                                                               u"for New "
                                                               u"Revision"))
        self.assistant.set_page_complete(self.fxdPageSetValues, True)

        _fixed = gtk.Fixed()
        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed,
                                     gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(_fixed, _(u"Revision: Confirm Addition"))
        self.assistant.set_page_complete(_fixed, True)

        self.assistant.show_all()

    def _forward_page_select(self, current_page):
        '''
        Method to set the next active page in the assistant.

        :param integer current_page: the currently active page in the
                                     assistant.
        '''

        if current_page == 0:
            self.assistant.set_current_page(1)

        elif current_page == 1:
            self.assistant.set_current_page(2)

        elif current_page == 2:
            self.assistant.set_current_page(3)

    def _add_revision(self, __assistant):
        """
        Method to add the new revision to the RTK Program database.

        :param __assistant: the current instance of the assistant.
        """

        # Find out who is logged in and adding this revision.
        if name == 'posix':
            _who = environ['USER']
        elif name == 'nt':
            _who = environ['USERNAME']

        # Find the current maximum Revision ID and increment it by one for the
        # new Revision ID.
        _query = "SELECT MAX(fld_revision_id) FROM tbl_revisions"
        _revision_id = self._app.DB.execute_query(_query,
                                                  None,
                                                  self._app.ProgCnx)
        _revision_id = _revision_id[0][0] + 1

        # Create the revision code.
        _revision_code = self.txtRevisionCode.get_text()
        if _revision_code == '' or _revision_code is None:
            _revision_code = '{0} {1}'.format(str(_conf.RTK_PREFIX[0]),
                                              str(_conf.RTK_PREFIX[1]))

            # Increment the revision index.
            _conf.RTK_PREFIX[1] += 1

        _revision_name = self.txtRevisionName.get_text()
        if _revision_name == '' or _revision_name is None:
            _revision_name = 'New Revision'

        _revision_remarks = self.txtRemarks.get_text(*self.txtRemarks.get_bounds())

        # First we add the new revision.  Second we retrieve thew new revision
        # id.  Third, we create a new, top-level system entry for this
        # revision.
        _query = "INSERT INTO tbl_revisions (fld_revision_id, fld_name, \
                                             fld_remarks, fld_revision_code) \
                  VALUES ({0:d}, '{1:s}', '{2:s}', '{3:s}')".format(
                  _revision_id, _revision_name, _revision_remarks,
                  _revision_code)
        self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                   commit=True)

        _model = self.cmbBaseRevision.get_model()
        _row = self.cmbBaseRevision.get_active_iter()
        _base_revision = int(_model.get_value(_row, 2))

        if self.chkFunction.get_active():
            _query = "SELECT MAX(fld_function_id) FROM tbl_functions"
            _function_id = self._app.DB.execute_query(_query,
                                                      None,
                                                      self._app.ProgCnx)

            if _function_id[0][0] is not None:
                _function_id = _function_id[0][0] + 1

                # Retrieve the information needed to copy the function hierarchy
                # from the base revision to the new revision.
                _query = "SELECT fld_code, fld_level, fld_name, \
                                 fld_parent_id, fld_remarks \
                          FROM tbl_functions \
                          WHERE fld_revision_id=%d" % _base_revision
                _function = self._app.DB.execute_query(_query,
                                                       None,
                                                       self._app.ProgCnx)

                # Copy the function hierarchy for the new revision.
                for i in range(len(_function)):
                    _function_name = _(u"New Function_") + str(i)

                    _values = (_revision_id, _function_id, _function[i][0],
                               _function[i][1], _function[i][2],
                               _function[i][3], _function[i][4])
                    _query = "INSERT INTO tbl_functions \
                              (fld_revision_id, fld_function_id, fld_code, \
                               fld_level, fld_name, fld_parent_id, \
                               fld_remarks) \
                              VALUES (%d, %d, '%s', %d, '%s', '%s', '%s')" % _values
                    self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                               commit=True)

                    if self.chkFunctionMatrix.get_active():
                        _query = "INSERT INTO tbl_functional_matrix \
                                  (fld_revision_id, fld_function_id) \
                                  VALUES (%d, %d)" % (_revision_id, _function_id)
                        self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                                   commit=True)

                    _function_id += 1

        if self.chkRequirements.get_active():
            _query = "SELECT MAX(fld_requirement_id) FROM tbl_requirements"
            _requirement_id = self._app.DB.execute_query(_query,
                                                         None,
                                                         self._app.ProgCnx)

            if _requirement_id[0][0] is not None:
                _requirement_id = _requirement_id[0][0] + 1

                # Retrieve the information needed to copy the requirement
                # hierarchy from the base revision to the new revision.
                _query = "SELECT fld_requirement_desc, fld_requirement_code, \
                                 fld_derived, fld_parent_requirement, \
                                 fld_owner, fld_specification, \
                                 fld_page_number, fld_figure_number \
                          FROM tbl_requirements \
                          WHERE fld_revision_id=%d" % _base_revision
                _requirements = self._app.DB.execute_query(_query,
                                                           None,
                                                           self._app.ProgCnx)

                # Copy the requirement hierarchy for the new revision.
                for i in range(len(_requirements)):
                    _query = "INSERT INTO tbl_requirements \
                              (fld_revision_id, fld_requirement_id, \
                               fld_requirement_desc, fld_requirement_code, \
                               fld_derived, fld_parent_requirement, \
                               fld_owner, fld_specification, \
                               fld_page_number, fld_figure_number) \
                              VALUES ({0:d}, {1:d}, '{2:s}', '{3:s}', {4:d}, \
                                      '{5:s}', '{6:s}', '{7:s}', '{8:s}', \
                                      '{9:s}')".format(
                              _revision_id, _requirement_id,
                              _requirements[i][0], _requirements[i][1],
                              _requirements[i][2], _requirements[i][3],
                              _requirements[i][4], _requirements[i][5],
                              _requirements[i][6], _requirements[i][7])
                    self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                               commit=True)

                    _requirement_id += 1

        if self.chkHardware.get_active():
            _query = "SELECT MAX(fld_assembly_id) FROM tbl_system"
            _assembly_id = self._app.DB.execute_query(_query,
                                                      None,
                                                      self._app.ProgCnx)

            if _assembly_id[0][0] is not None:
                _assembly_id = _assembly_id[0][0] + 1

                # Retrieve the information needed to copy the hardware
                # hierarchy from the base revision to the new revision.
                if self.chkFailureInfo.get_active():
                    _query = "SELECT fld_cage_code, fld_category_id, \
                                     fld_description, \
                                     fld_failure_rate_active, \
                                     fld_failure_rate_dormant, \
                                     fld_failure_rate_software, \
                                     fld_failure_rate_specified, \
                                     fld_failure_rate_type, \
                                     fld_figure_number, \
                                     fld_lcn, fld_level, fld_manufacturer, \
                                     fld_mission_time, fld_name, fld_nsn, \
                                     fld_page_number, fld_parent_assembly, \
                                     fld_part, fld_part_number, \
                                     fld_quantity, \
                                     fld_ref_des, fld_remarks, \
                                     fld_specification_number, \
                                     fld_subcategory_id, fld_mtbf_predicted, \
                                     fld_mtbf_specified, fld_mtbf_lcl, \
                                     fld_mtbf_ucl, fld_failure_rate_lcl, \
                                     fld_failure_rate_ucl \
                              FROM tbl_system \
                              WHERE fld_revision_id=%d" % _base_revision
                else:
                    _query = "SELECT fld_cage_code, fld_category_id, \
                                     fld_description, fld_figure_number, \
                                     fld_lcn, fld_level, fld_manufacturer, \
                                     fld_mission_time, fld_name, fld_nsn, \
                                     fld_page_number, fld_parent_assembly, \
                                     fld_part, fld_part_number, \
                                     fld_quantity, fld_ref_des, fld_remarks, \
                                     fld_specification_number, \
                                     fld_subcategory_id \
                              FROM tbl_system \
                              WHERE fld_revision_id=%d" % _base_revision
                _system = self._app.DB.execute_query(_query,
                                                     None,
                                                     self._app.ProgCnx)

                # Copy the hardware hierarchy for the new revision.
                for i in range(len(_system)):
                    if self.chkFailureInfo.get_active():
                        _values = (_revision_id, _assembly_id,
                                   _system[i][0], _system[i][1],
                                   _system[i][2], _system[i][3],
                                   _system[i][4], _system[i][5],
                                   _system[i][6], _system[i][7],
                                   _system[i][8], _system[i][9],
                                   _system[i][10], _system[i][11],
                                   _system[i][12], _system[i][13],
                                   _system[i][14], _system[i][15],
                                   _system[i][16], _system[i][17],
                                   _system[i][18], _system[i][19],
                                   _system[i][20], _system[i][21],
                                   _system[i][22], _system[i][23],
                                   _system[i][24], _system[i][25],
                                   _system[i][26], _system[i][27],
                                   _system[i][28], _system[i][29], _who)
                        _query = "INSERT INTO tbl_system \
                                  (fld_revision_id, fld_assembly_id, \
                                   fld_cage_code, fld_category_id, \
                                   fld_description, fld_failure_rate_active, \
                                   fld_failure_rate_dormant, \
                                   fld_failure_rate_software, \
                                   fld_failure_rate_specified, \
                                   fld_failure_rate_type, fld_figure_number, \
                                   fld_lcn, fld_level, fld_manufacturer, \
                                   fld_mission_time, fld_name, fld_nsn, \
                                   fld_page_number, fld_parent_assembly, \
                                   fld_part, fld_part_number, fld_quantity, \
                                   fld_ref_des, fld_remarks, \
                                   fld_specification_number, \
                                   fld_subcategory_id, fld_mtbf_predicted, \
                                   fld_mtbf_specified, fld_mtbf_lcl, \
                                   fld_mtbf_ucl, fld_failure_rate_lcl, \
                                   fld_failure_rate_ucl, fld_entered_by) \
                                  VALUES (%d, %d, '%s', %d, '%s', %f, %f, \
                                          %f, %f, %d, '%s', '%s', %d, %d, \
                                          %f, '%s', '%s', '%s', '%s', %d, \
                                          '%s', %d, '%s', '%s', '%s', %d, \
                                          %f, %f, %f, %f, %f, %f, '%s')" % _values
                    else:
                        _values = (_revision_id, _assembly_id,
                                   _system[i][0], _system[i][1],
                                   _system[i][2], _system[i][3],
                                   _system[i][4], _system[i][5],
                                   _system[i][6], _system[i][7],
                                   _system[i][8], _system[i][9],
                                   _system[i][10], _system[i][11],
                                   _system[i][12], _system[i][13],
                                   _system[i][14], _system[i][15],
                                   _system[i][16], _system[i][17],
                                   _system[i][18], _who)
                        _query = "INSERT INTO tbl_system \
                                  (fld_revision_id, fld_assembly_id, \
                                   fld_cage_code, fld_category_id, \
                                   fld_description, fld_figure_number, \
                                   fld_lcn, fld_level, fld_manufacturer, \
                                   fld_mission_time, fld_name, fld_nsn, \
                                   fld_page_number, fld_parent_assembly, \
                                   fld_part, fld_part_number, fld_quantity, \
                                   fld_ref_des, fld_remarks, \
                                   fld_specification_number, \
                                   fld_subcategory_id, fld_entered_by) \
                                  VALUES (%d, %d, '%s', %d, '%s', '%s', \
                                          '%s', %d, %d, %f, '%s', '%s', \
                                          '%s', '%s', %d, '%s', %d, '%s', \
                                          '%s', '%s', %d, '%s')" % _values
                    self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                               commit=True)

                    _values = (_revision_id, _assembly_id)
                    _query = "INSERT INTO tbl_allocation \
                              (fld_revision_id, fld_assembly_id) \
                              VALUES (%d, %d)" % _values
                    self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                               commit=True)

                    _query = "INSERT INTO tbl_risk_analysis \
                              (fld_revision_id, fld_assembly_id) \
                              VALUES (%d, %d)" % _values
                    self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                               commit=True)

                    _query = "INSERT INTO tbl_similar_item \
                              (fld_revision_id, fld_assembly_id) \
                              VALUES (%d, %d)" % _values
                    self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                               commit=True)

                    _query = "INSERT INTO tbl_functional_matrix \
                              (fld_revision_id, fld_assembly_id) \
                              VALUES(%d, %d)" % _values
                    self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                               commit=True)

                    _query = "INSERT INTO tbl_fmeca \
                              (fld_revision_id, fld_assembly_id) \
                              VALUES(%d, %d)" % _values
                    self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                               commit=True)

                    _assembly_id += 1

        # Reload the revision tree.
        self._app.REVISION.load_tree()

    def _cancel(self, __button):
        """
        Method to destroy the assistant when the 'Cancel' button is
        pressed.

        :param __button: the gtk.Button() that called this method.
        :type __button: gtk.Button
        """

        self.assistant.destroy()


class AddIncident:
    """
    This is the gtkAssistant that walks the user through the process of adding
    Field Incident records to the open RTK Program database.
    """

    def __init__(self, button, app):
        """
        Initialize on instance of the Add Incident Assistant.

        Keyword Arguments:
        button -- the gtk.Button widget that calling this Assistant.
        app    -- the instance of the RTK application calling the Assistant.
        """

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_("RTK Add Incident Assistant"))
        self.assistant.connect('apply', self._add_incident)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

# Create the introduction page.
        fixed = gtk.Fixed()
        _text_ = _("This is the RTK incident addition assistant.  It will help you add a new hardware or software incident to the database.  Press 'Forward' to continue or 'Cancel' to quit the assistant.")
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
        self.txtIncidentDate = _widg.make_entry(width=100)
        self.txtIncidentDate.set_tooltip_text(_("Enter the date the incident occurred."))
        self.txtIncidentDate.connect('focus_out_event', self._check_ready, 2)
        self.fxdPageSWGeneral.put(label, x_pos, y_pos)
        x_pos += 195
        self.fxdPageSWGeneral.put(self.txtIncidentDate, x_pos, y_pos)
        x_pos += 105

        # Add a calendar widget for date selection if we are on a posix
        # platform.  The calendar widget doesn't work for shit on Windoze.
        if(name == 'posix'):
            self.btnCalendar = _widg.make_button(height=25,
                                                 width=25,
                                                 label="...",
                                                 image=None)
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
        self.txtDescription = _widg.make_entry(width=795)
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
        textview = _widg.make_text_view(buffer=self.txtDetails, width=795)
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
        textview = _widg.make_text_view(buffer=self.txtRemarks, width=795)
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
        textview = _widg.make_text_view(buffer=self.txtEffect, width=795)
        textview.set_tooltip_text(_("Describe the effect on the system or user of the incident being reported."))
        self.fxdPageSWTest.put(label, 5, y_pos)
        y_pos += 30
        self.fxdPageSWTest.put(textview, 5, y_pos)
        y_pos += 120

        _text_ = _("Recommended Solution:")
        label = _widg.make_label(_text_)
        self.txtSolution = gtk.TextBuffer()
        textview = _widg.make_text_view(buffer=self.txtSolution, width=795)
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
    creating a new test plan in the open RTK Program database.
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
        app    -- the RTK application.
        """

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_(u"RTK Test Plan Creation Assistant"))
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
        _text_ = _(u"This is the RTK test plan creation assistant.  It will help you create a new test plan in the open RTK Program.  Press 'Forward' to continue or 'Cancel' to quit the assistant.")
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
        self.txtName = _widg.make_entry(width=400)
        self.txtName.set_tooltip_text(_(u"Enter a brief description or title for the test."))

        self.txtDescription = gtk.TextBuffer()
        textview = _widg.make_text_view(buffer=self.txtDescription,
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

        self.txtMTBFI = _widg.make_entry(width=50)
        self.txtMTBFG = _widg.make_entry(width=50)
        self.txtMTBFGP = _widg.make_entry(width=50)
        self.txtTechReq = _widg.make_entry(width=50)

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
        open RTK Program.

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

        self._app.TESTING.load_tree

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
    RTK Program database.
    """

    _labels = [_(u"Date:"), _(u"Time:"), _(u"Number of Failures:")]

    def __init__(self, app):
        """
        Method to initialize the Reliability Growth Record Add Assistant.

        Keyword Arguments:
        app    -- the RTK application.
        """

        gtk.Assistant.__init__(self)
        self.set_title(_(u"RTK Reliability Growth Record Assistant"))
        self.connect('apply', self._test_record_add)
        self.connect('cancel', self._cancel)
        self.connect('close', self._cancel)

        self._app = app

# --------------------------------------------------------------------------- #
# Create the introduction page.
# --------------------------------------------------------------------------- #
        fixed = gtk.Fixed()
        _text_ = _(u"This is the RTK reliability growth record assistant.  It will help you add a record for tracking against the currently selected reliability growth plan.  Press 'Forward' to continue or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=-1, wrap=True)
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
        self.txtDate = _widg.make_entry(width=100)
        self.txtDate.set_tooltip_text(_(u"Date test record was generated.  This is not necessarily the date the record is being added."))
        self.btnDate = _widg.make_button(height=25,
                                         width=25,
                                         label="...",
                                         image=None)
        self.btnDate.connect('released', _util.date_select,
                             self.txtDate)
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
        fixed.put(self.btnDate, 260, 5)

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
        _text_ = _(u"Press 'Apply' to add the record or 'Cancel' to quit the assistant without adding the record.")
        label = _widg.make_label(_text_, width=500, height=-1, wrap=True)
        fixed.put(label, 5, 5)
        self.append_page(fixed)
        self.set_page_type(fixed, gtk.ASSISTANT_PAGE_CONFIRM)
        self.set_page_title(fixed, _(u"Add Reliability Growth Record"))
        self.set_page_complete(fixed, True)

        self.show_all()

    def _test_record_add(self, button):
        """
        Method to add a new test record for the selected test plan to the
        open RTK Program.

        Keyword Arguments:
        button -- the gtk.ToolButton that called this method.
        """

        (_model_, _row_) = self._app.TESTING.treeview.get_selection().get_selected()
        _idx_ = self._app.TESTING._col_order[0]

        _query_ = "SELECT MAX(fld_record_id), MAX(fld_right_interval) \
                   FROM tbl_survival_data \
                   WHERE fld_dataset_id=%d" % self._app.TESTING.test_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=False)

        if(_results_[0][0] is None or _results_[0][0] == ''):
            _last_id_ = 0
        else:
            _last_id_ = _results_[0][0]

        if(_results_[0][1] is None or _results_[0][1] == ''):
            _last_time_ = 0.0
        else:
            _last_time_ = float(_results_[0][1])

        _last_id_ += 1

        _assembly_id_ = _model_.get_value(_row_, _idx_)
# Read the test time entered by the user.  If this is entered as additional
# test time, calculate the cumulative test time.
        _time_ = float(self.txtTime.get_text())
        if(self.chkAdditional.get_active()):
            _time_ = _time_ + _last_time_
        _n_fails_ = int(self.txtNumFails.get_text())

        _date_ = datetime.strptime(self.txtDate.get_text(), '%Y-%m-%d').toordinal()
        _query_ = "INSERT INTO tbl_survival_data \
                   (fld_record_id, fld_dataset_id, fld_left_interval, \
                    fld_right_interval, fld_quantity, fld_unit, \
                    fld_part_num, fld_market, fld_model, fld_mode_type, \
                    fld_assembly_id, fld_request_date) \
                   VALUES (%d, %d, %f, %f, %d, '%s', '%s', '%s', '%s', \
                           %d, %d, %d)" % (_last_id_, \
                                           self._app.TESTING.test_id, \
                                           0.0, _time_, _n_fails_, '', '', \
                                           '', '', 0, _assembly_id_, _date_)

        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
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
    in the open RTK Program database.
    """

    def __init__(self, button, app):
        """
        Method to initialize the Dataset Creation Assistant.

        Keyword Arguments:
        :param button: the gtk.Button() that called this method.
        :type button: gtk.Button
        :param app: the RTK application.
        :type app: RTK application
        """

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_("RTK Survival Data Set Creation Assistant"))
        self.assistant.connect('apply', self._create)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

        # Create the introduction page.
        _fixed = gtk.Fixed()
        _text = _(u"This is the RTK survival data set assistant.  It will\n"
                  u"help you create a data set for survival (Weibull)\n"
                  u"analysis from the Program Incidents.  Press 'Forward'\n"
                  u"to continue or 'Cancel' to quit the assistant.")
        _label = _widg.make_label(_text, width=-1, height=150)
        _fixed.put(_label, 5, 5)
        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(_fixed, _(u"Introduction"))
        self.assistant.set_page_complete(_fixed, True)

        # Create a page to select where data set should be saved.
        _fixed = gtk.Fixed()

        _frame = _widg.make_frame(_label_=_(""))
        _frame.set_shadow_type(gtk.SHADOW_NONE)
        _frame.add(_fixed)

        # Create the radio buttons that select the output as database or file.
        self.optDatabase = gtk.RadioButton(label=_(u"Save Data Set to "
                                                   u"Database"))
        self.optFile = gtk.RadioButton(group=self.optDatabase,
                                       label=_(u"Save Data Set to File"))
        self.chkNevadaChart = _widg.make_check_button(
                              _label_=_(u"Create Nevada chart from data."))

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
                                  _label_=_(u"Include zero hour failures."))
        self.chkIncludeZeroHour.set_active(True)

        _fixed.put(self.chkIncludeZeroHour, 5, 205)

        self.assistant.append_page(_frame)
        self.assistant.set_page_type(_frame, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(_frame,
                                      _(u"Select Where to Save Data Set"))
        self.assistant.set_page_complete(_frame, True)

        # Create a page to select where data set should be saved.
        _fixed = gtk.Fixed()

        _frame = _widg.make_frame(_label_=_(""))
        _frame.set_shadow_type(gtk.SHADOW_NONE)
        _frame.add(_fixed)

        self.cmbAssembly = _widg.make_combo(simple=False)

        _query = "SELECT fld_name, fld_assembly_id, fld_description \
                  FROM tbl_system \
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
        _text = _(u"Press 'Apply' to create the requested data set or "
                  u"'Cancel' to quit the assistant.")
        _label = _widg.make_label(_text, width=600, height=150)
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

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        _window_ = self.assistant.get_root_window()
        _window_.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))

        _records_ = {}
        _data_set_ = []

        model = self.cmbAssembly.get_model()
        row = self.cmbAssembly.get_active_iter()
        if(row is not None):
            _assembly_id_ = int(model.get_value(row, 1))
        else:
            _assembly_id_ = 0
        _confidence_ = float(self.txtConfidence.get_text())
        _description_ = self.txtDescription.get_text()

# First create a new dataset in the RTK Program database or create a new file
# to output the results to.
        if(self.optDatabase.get_active()):
            if(_conf.BACKEND == 'mysql'):
                _query_ = "INSERT INTO tbl_dataset (fld_assembly_id, \
                                                    fld_description, \
                                                    fld_confidence) \
                           VALUES (%d, '%s', %f)" % \
                           (_assembly_id_, _description_, _confidence_)

            elif(_conf.BACKEND == 'sqlite3'):
                # First find the last dataset id in the table.
                _query_ = "SELECT MAX(fld_dataset_id) \
                           FROM tbl_dataset"
                _dataset_id_ = self._app.DB.execute_query(_query_,
                                                          None,
                                                          self._app.ProgCnx)
                _dataset_id_ = _dataset_id_[0][0]
                if(_dataset_id_ is None or not _dataset_id_ or
                   _dataset_id_ == ''):
                    _dataset_id_ = 1
                else:
                    _dataset_id_ += 1

                _query_ = "INSERT INTO tbl_dataset (fld_dataset_id, \
                                                    fld_assembly_id, \
                                                    fld_description, \
                                                    fld_confidence) \
                           VALUES (%d, %d, '%s', %f)" % \
                           (_dataset_id_, _assembly_id_, _description_,
                            _confidence_)

            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

# Find the ID of the last dataset to be created if using the MySQL backend.
# This is the value that will be written to the fld_dataset_id field in the
# tbl_survival_data table.
            if(_conf.BACKEND == 'mysql'):
                _query_ = "SELECT LAST_INSERT_ID()"
                _dataset_id_ = self._app.DB.execute_query(_query_,
                                                          None,
                                                          self._app.ProgCnx)
                _dataset_id_ = _dataset_id_[0][0]
        else:
            _dialog_ = gtk.FileChooserDialog(_("RTK: Save Data Set to File ..."),
                                             None,
                                             gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                             (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                              gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
            _dialog_.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
            _response_ = _dialog_.run()
            if(_response_ == gtk.RESPONSE_ACCEPT):
                _filename_ = _dialog_.get_filename()

            _dialog_.destroy()

            _dataset_id_ = 0

            _file_ = open(_filename_, 'w')
            _file_.write("Data Set Description: " + self.txtDescription.get_text() + "\n")
            _file_.write("\n")
            _file_.write("Record_ID\tLeft\tRight\tStatus\tQuantity\tUnit\tTBF\tAssembly_ID\tRequest_Date\tAssembly_ID\n")

        _starttime_ = 0.01
        if(self.chkIncludeZeroHour.get_active()):
            _starttime_ = 0.0

# Select everything from the incident detail table in the Program database.
#   Index       Field
#     0      Unit
#     1      Incident ID
#     2      Part Number
#     3      Age at Incident
#     4      Failure
#     5      Suspension
#     6      CND/NFF
#     7      OCC
#     8      Initial Installation
#     9      Interval Censored
        if(self.optMTTF.get_active()):
            _query_ = "SELECT t2.fld_unit, t1.fld_incident_id, \
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
                                t2.fld_request_date ASC, \
                                t1.fld_age_at_incident ASC" % _starttime_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

        elif(self.optMTBBD.get_active()):
            _query_ = "SELECT t2.fld_unit, t1.fld_incident_id, \
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
                                t2.fld_request_date ASC, \
                                t1.fld_age_at_incident ASC" % _starttime_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

        elif(self.optMTBF.get_active()):
            _query_ = "SELECT t2.fld_unit, t1.fld_incident_id, \
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
                                t2.fld_request_date ASC, \
                                t1.fld_age_at_incident ASC" % _starttime_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

        _n_records_ = len(_results_)

# Load the results into the survival data table in the RTK Program database
# or write the results to the open file.
        if(self.optDatabase.get_active()):
            # Add the first record to the survival data table in the open
            # RTK Program database.
            _base_query_ = "INSERT INTO tbl_survival_data \
                            (fld_record_id, fld_dataset_id, \
                             fld_left_interval, fld_right_interval, \
                             fld_status, fld_quantity, fld_unit, fld_tbf, \
                             fld_assembly_id, fld_request_date) \
                            VALUES (%d, %d, %f, %f, '%s', %d, '%s', %f, %d, %d)"
            _values_ = (0, _dataset_id_, 0.0, float(_results_[0][3]),
                        "Interval Censored", 1, _results_[0][0],
                        float(_results_[0][3]), _results_[0][11],
                        _results_[0][10])

            # Add the remaining records to the survival data table in the
            # open RTK Program database.
            _add_ = True
            n = 1
            _n_inconsistent_ = 0
            for i in range(1, _n_records_):
                # If the current record passed the consistency check with the
                # previous record, then add it to the database.
                if(_add_):
                    _query_ = _base_query_ % _values_
                    _inserts_ = self._app.DB.execute_query(_query_,
                                                           None,
                                                           self._app.ProgCnx,
                                                           commit=True)

                # Create the next set of values to insert to the RTK
                # Program database if it passes the consistency check.
                if(_results_[i][0] == _results_[i - n][0]): # Same unit.
                    if(not self._consistency_check(_results_[i - n],
                                                   _results_[i])):

                        if(_results_[i][3] == _results_[i - n][3]): # Failures occurred at same time.
                            _left_ = float(_values_[2])
                        else:
                            _left_ = float(_results_[i - n][3])

                        _right_ = float(_results_[i][3])
                        _tbf_ = _right_ - _left_
                        _values_ = (i, _dataset_id_, _left_, _right_,
                                    'Interval Censored', 1, _results_[i][0],
                                    _tbf_, _results_[i][11], _results_[i][10])
                        _add_ = True
                        n = 1

                    else:
                        _add_ = False
                        n += 1
                        _n_inconsistent_ += 1

                else:                                       # Different unit.
                    if(i < _n_records_ - 1):
                        if(_results_[i][3] <= _results_[i + 1][3]):
                            _left_ = 0.0
                            _right_ = float(_results_[i][3])
                            _tbf_ = _right_ - _left_
                            _values_ = (i, _dataset_id_, _left_, _right_,
                                        'Interval Censored', 1,
                                        _results_[i][0], _tbf_,
                                        _results_[i][11], _results_[i][10])
                            _add_ = True
                            n = 1
                        else:
                            _add_ = False
                            n += 1
                            _n_inconsistent_ += 1
                    else:
                        _left_ = 0.0
                        _right_ = float(_results_[i][3])
                        _tbf_ = _right_ - _left_
                        _values_ = (i, _dataset_id_, _left_, _right_,
                                    'Interval Censored', 1,
                                    _results_[i][0], _tbf_, _results_[i][11],
                                    _results_[i][10])
                        _add_ = True
                        n = 1
        else:
            # Write the first record to the open file.
            _file_.write('0\t0\t' + str(_results_[0][3]) + '\t' +
                         'Interval Censored\t1\t' + str(_results_[0][0]) +
                         '\t' + str(_results_[0][3]) + '\t' +
                         str(_results_[0][11]) + '\t' +
                         str(_results_[0][10]) + '\n')

            # Write the remaining records to the open file.
            _n_inconsistent_ = 0
            for i in range(1, _n_records_):
                # Write the next record to the open file if it passes the
                # consistency check.
                n = 1
                if(_results_[i][0] == _results_[i - 1][0]): # Same unit.
                    if(not self._consistency_check(_results_[i - 1],
                                                   _results_[i])):

                        if(_results_[i][3] == _results_[i - n][3]): # Failures occurred at same time.
                            _left_ = float(_results_[i][3])
                        else:
                            _left_ = float(_results_[i - n][3])

                        _tbf_ = float(_results_[i][3]) - float(_results_[i - 1][3])
                        _file_.write(str(i) + '\t' + str(_results_[i - 1][3]) +
                                     '\t' + str(_results_[i][3]) +
                                     '\tInterval Censored\t1\t' +
                                     str(_results_[i][0]) + '\t' +
                                     str(_tbf_) + '\t' + str(_results_[i][11]) +
                                     '\t' + str(_results_[i][10]) + '\n')
                        n = 1

                    else:
                        n += 1
                        _n_inconsistent_ += 1

                else:                                      # Different unit.
                    _tbf_ = float(_results_[i][3])
                    _file_.write(str(i) + '\t0.0\t' +
                                 str(_results_[i][3]) +
                                 '\tInterval Censored\t1\t' +
                                 str(_results_[i][0]) + '\t' +
                                 str(_tbf_) + '\t' + str(_results_[i][11]) +
                                 '\t' + str(_results_[i][10]) + '\n')

        _window_.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

        if(_n_inconsistent_ > 0):
            _prompt_ = _(u"There were %d records with inconsistent information.  These were not used in the creation of the dataset. Please see file '%s' for details." % (_n_inconsistent_, _conf.LOG_DIR + 'RTK_import.log'))
            _util.application_error(_prompt_)

# Load the dataset gtk.TreeView with the newly created dataset if it was
# created in teh RTK Program database.
        if(self.optDatabase.get_active()):
            self._app.DATASET.load_tree
            _page_ = sum(_conf.RTK_MODULES[:11])
            self._app.winTree.notebook.set_current_page(_page_ - 1)

        return False

    def _consistency_check(self, _results1_, _results2_):
        """
        Function to check the consistency of the data records.

        Keyword Arguments:
        _results1_ -- the previous record in the data set.
        _results2_ -- the current record in the data set.
        """

        _err_ = False

        if(_results2_[3] < _results1_[3]):      # Failure times are descending.
            #_previous_date_ = _util.ordinal_to_date(_results1_[10])
            #_current_date_ = _util.ordinal_to_date(_results2_[10])
            #_errmsg_ = "The failure time of record #%d, which occurred on '%s' on unit '%s', is earlier than the failure time of record #%d, which occurred on '%s' on unit '%s'.  Failure times should not decrease over time." % (int(_results2_[1]), _current_date_, _results2_[0], int(_results1_[1]), _previous_date_, _results2_[0])
            _err_ = True

        #if(_err_):
        #    self._app.import_log.error(_errmsg_)

        return(_err_)

    def _cancel(self, button):
        """
        Method to destroy the gtk.Assistant when the 'Cancel' button is
        pressed.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        self.assistant.destroy()


class AddDatasetRecord:
    """
    This is the gtk.Assistant that walks the user through the process of
    adding a record to the currently selected survival dataset in the open
    RTK Program database.
    """

    _labels = [_(u"Left:"), _(u"Right:"), _(u"Status:"), _(u"Quantity:"),
               _(u"Affected Unit:"), _(u"Part Number:"), _(u"Market:"),
               _(u"Model:"), _(u"Assembly:")]

    def __init__(self, app):
        """
        Method to initialize the Reliability Growth Record Add Assistant.

        Keyword Arguments:
        button -- the gtk.ToolButton that called this assistant.
        app    -- the RTK application.
        """

        gtk.Assistant.__init__(self)
        self.set_title(_(u"RTK Survival Analysis Record Assistant"))
        #self.connect('apply', self._test_record_add)
        #self.connect('cancel', self._cancel)
        #self.connect('close', self._cancel)

        self._app = app

# --------------------------------------------------------------------------- #
# Create the introduction page.
# --------------------------------------------------------------------------- #
        fixed = gtk.Fixed()
        _text_ = _(u"This is the RTK survival analysis record assistant.  It will help you add a record to the currently selected survival dataset.  Press 'Forward' to continue or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.append_page(fixed)
        self.set_page_type(fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.set_page_title(fixed, _(u"Introduction"))
        self.set_page_complete(fixed, True)

# --------------------------------------------------------------------------- #
# Create the page to gather the necessary failure time inputs.
# --------------------------------------------------------------------------- #
        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_(""))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(fixed)

# Create the gtk.Combo that allow one of multiple selections.
        self.txtLeft = _widg.make_entry()
        self.txtLeft.set_tooltip_text(_(u"Left of the interval.  If failure time is exact, set this equal to the failure time."))
        self.txtRight = _widg.make_entry()
        self.txtRight.set_tooltip_text(_(u"Left of the interval.  If failure time is exact, set this equal to the failure time."))
        self.txtQuantity = _widg.make_entry()
        self.txtQuantity.set_tooltip_text(_(u"Number of failures observed during interval or at failure time."))
        self.txtQuantity.set_text("1")

        label = _widg.make_label(self._labels[0], 150, 25)
        fixed.put(label, 5, 5)
        fixed.put(self.txtLeft, 160, 5)

        label = _widg.make_label(self._labels[1], 150, 25)
        fixed.put(label, 5, 40)
        fixed.put(self.txtRight, 160, 40)

        label = _widg.make_label(self._labels[2], 150, 25)
        fixed.put(label, 5, 75)
        fixed.put(self.txtQuantity, 160, 75)

        self.append_page(frame)
        self.set_page_type(frame, gtk.ASSISTANT_PAGE_CONTENT)
        self.set_page_title(frame, _(u"Enter Failure Time Data"))
        self.set_page_complete(frame, True)

# --------------------------------------------------------------------------- #
# Create the page to gather details regarding the failed item(s).
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# Create the page to apply the import criteria.
# --------------------------------------------------------------------------- #
        fixed = gtk.Fixed()
        _text_ = _(u"Press 'Apply' to add the record to the selected survival data set or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.append_page(fixed)
        self.set_page_type(fixed, gtk.ASSISTANT_PAGE_CONFIRM)
        self.set_page_title(fixed, _(u"Add Survival Data Record"))
        self.set_page_complete(fixed, True)

        self.show_all()
