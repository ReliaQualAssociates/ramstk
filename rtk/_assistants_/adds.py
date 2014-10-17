#!/usr/bin/env python
"""
Module containing various assistants for adding or creating objects in the
open RTK Program database.  This module contains assistants to guide the user
through the following:

 * Adding a new Revision.
 * Adding a new Test Plan.
 * Adding a new record to a Test Plan.
 * Adding a new Program Incident.
 * Creating a new Survival Analysis data set from program incidents.
 * Adding a new record to a Survival Analysis data set.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       addrecord.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale
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
    import configuration as _conf
    import utilities as _util
    import widgets as _widg
except ImportError:
    import rtk.configuration as _conf
    import rtk.utilities as _util
    import rtk.widgets as _widg

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class AddRevision(object):
    """
    This is the assistant that walks the user through the process of adding
    a new revision to the open RTK Program database.
    """

    def __init__(self, __button, app):
        """
        Initialize on instance of the Add Revision Assistant.

        :param gtk.Button __button: the gtk.Button() widget that called the
                                    assistant.
        :param RTK app: the instance of the RTK application calling the
                        assistant.
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
        _label = _widg.make_label(_text, width=500, height=-1, wrap=True)
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
                                      _(u"Select Additional Information to "
                                        u"Add"))
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
        _textview_ = _widg.make_text_view(txvbuffer=self.txtRemarks,
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
        """
        Method to set the next active page in the assistant.

        :param int current_page: the currently active page in the assistant.
        """

        if current_page == 0:
            self.assistant.set_current_page(1)

        elif current_page == 1:
            self.assistant.set_current_page(2)

        elif current_page == 2:
            self.assistant.set_current_page(3)

    def _add_revision(self, __assistant):
        """
        Method to add the new revision to the RTK Program database.

        :param gtk.Assistant __assistant: the current instance of the
                                          assistant.
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

        # TODO: Move this to the Function class and simply call it from here.
        if self.chkFunction.get_active():
            _query = "SELECT MAX(fld_function_id) FROM tbl_functions"
            _function_id = self._app.DB.execute_query(_query,
                                                      None,
                                                      self._app.ProgCnx)

            if _function_id[0][0] is not None:
                _function_id = _function_id[0][0] + 1

                # Retrieve the information needed to copy the function
                # hierarchy from the base revision to the new revision.
                _query = "SELECT fld_code, fld_level, fld_name, \
                                 fld_parent_id, fld_remarks \
                          FROM tbl_functions \
                          WHERE fld_revision_id=%d" % _base_revision
                _function = self._app.DB.execute_query(_query,
                                                       None,
                                                       self._app.ProgCnx)
            else:
                _function = [('', 0, 'New Function', 0, ''), ]

            try:
                _n_functions = len(_function)
            except TypeError:
                _n_functions = 0

            # Copy the function hierarchy for the new revision.
            for i in range(_n_functions):
                _function_name = _(u"New Function_") + str(i)

                _values = (_revision_id, _function_id, _function[i][0],
                           _function[i][1], _function[i][2],
                           _function[i][3], _function[i][4])
                _query = "INSERT INTO tbl_functions \
                          (fld_revision_id, fld_function_id, fld_code, \
                           fld_level, fld_name, fld_parent_id, \
                           fld_remarks) \
                          VALUES (%d, %d, '%s', %d, '%s', '%s', '%s')" % \
                         _values
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
                _requirement_id = self._app.DB.execute_query(_query, None,
                                                             self._app.ProgCnx)

                if _requirement_id[0][0] is not None:
                    _requirement_id = _requirement_id[0][0] + 1

                    # Retrieve the information needed to copy the requirement
                    # hierarchy from the base revision to the new revision.
                    _query = "SELECT fld_requirement_desc, \
                                     fld_requirement_code, fld_derived, \
                                     fld_parent_requirement, fld_owner, \
                                     fld_specification, fld_page_number, \
                                     fld_figure_number \
                              FROM tbl_requirements \
                              WHERE fld_revision_id=%d" % _base_revision
                    _requirements = self._app.DB.execute_query(_query, None,
                                                            self._app.ProgCnx)

                try:
                    _n_requirements = len(_requirements)
                except(TypeError, UnboundLocalError):
                    _n_requirements = 0

                # Copy the requirement hierarchy for the new revision.
                for i in range(_n_requirements):
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

        _query = "SELECT MAX(fld_assembly_id) FROM tbl_system"
        _assembly_id = self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx)
        if _assembly_id[0][0] is not None:
            _assembly_id = _assembly_id[0][0] + 1

        # TODO: Move this to the Hardware class and simply call it from here.
        if self.chkHardware.get_active():
            # Retrieve the information needed to copy the hardware
            # hierarchy from the base revision to the new revision.
            if self.chkFailureInfo.get_active():
                _query = "SELECT fld_cage_code, fld_category_id, \
                                 fld_description, fld_failure_rate_active, \
                                 fld_failure_rate_dormant, \
                                 fld_failure_rate_software, \
                                 fld_failure_rate_specified, \
                                 fld_failure_rate_type, fld_figure_number, \
                                 fld_lcn, fld_level, fld_manufacturer, \
                                 fld_mission_time, fld_name, fld_nsn, \
                                 fld_page_number, fld_parent_assembly, \
                                 fld_part, fld_part_number, \
                                 fld_quantity, fld_ref_des, fld_remarks, \
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
            _system = self._app.DB.execute_query(_query, None,
                                                 self._app.ProgCnx)

            try:
                _n_hardware = len(_system)
            except TypeError:
                _n_hardware = 0
            # Copy the hardware hierarchy for the new revision.
            for i in range(_n_hardware):
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
                                      %f, %f, %f, %f, %f, %f, '%s')" % \
                             _values
                    if _system[i][17] == 1:
                        _part = True
                    else:
                        _part = False
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
                    if _system[i][17] == 1:
                        _part = True
                    else:
                        _part = False

                self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                           commit=True)

                _values = (_revision_id, _assembly_id)

                # Add the item to the prediction table if it's a part.
                if _part:
                    _query = "INSERT INTO tbl_prediction \
                              (fld_revision_id, fld_assembly_id) \
                              VALUES (%d, %d)" % _values
                    self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                               commit=True)

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

                _query = "INSERT INTO tbl_fmeca \
                          (fld_revision_id, fld_assembly_id) \
                          VALUES(%d, %d)" % _values
                self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                           commit=True)

                if self.chkFunctionMatrix.get_active():
                    _query = "SELECT fld_function_id \
                              FROM tbl_functions \
                              WHERE fld_revision_id=%d" % _revision_id
                    _functions = self._app.DB.execute_query(_query, None,
                                                            self._app.ProgCnx)
                    for i in range(len(_functions)):
                        _query = "INSERT INTO tbl_functional_matrix \
                                  (fld_revision_id, fld_assembly_id, \
                                   fld_function_id) \
                                  VALUES(%d, %d, %d)" % \
                                 (_revision_id, _assembly_id, _functions[i][0])
                        self._app.DB.execute_query(_query, None,
                                                   self._app.ProgCnx,
                                                   commit=True)

                _assembly_id += 1
        else:
            _values = (_revision_id, _assembly_id, _who)
            _query = "INSERT INTO tbl_system \
                                  (fld_revision_id, fld_assembly_id, \
                                   fld_entered_by) \
                      VALUES (%d, %d, '%s')" % _values
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

            _query = "INSERT INTO tbl_fmeca \
                      (fld_revision_id, fld_assembly_id) \
                      VALUES(%d, %d)" % _values
            self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                       commit=True)

        # TODO: Add a checkbox to the assistant to allow the user to select whether or not to duplicate the software structure.
        # TODO: Move this to the Software class and simply call it from here.
        _query = "SELECT MAX(fld_software_id) FROM tbl_software"
        _module_id = self._app.DB.execute_query(_query, None,
                                                self._app.ProgCnx)
        if _module_id[0][0] is not None:
            _module_id = _module_id[0][0] + 1

        _query = "INSERT INTO tbl_software \
                  (fld_revision_id, fld_level_id, fld_description, \
                   fld_parent_module) \
                  VALUES (%d, 0, 'System Software', '-')" % _revision_id
        if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                          commit=True):
            _util.rtk_error(_(u"Error creating system software hierarchy."))
        else:
            # Add the new software module to each of risk analysis tables.
            for i in range(43):
                _query = "INSERT INTO tbl_software_development \
                         (fld_software_id, fld_question_id, fld_y) \
                         VALUES (%d, %d, 0)" % (_module_id, i)
                self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                           commit=True)
            for i in range(50):
                _query = "INSERT INTO tbl_srr_ssr \
                         (fld_software_id, fld_question_id, fld_y, fld_value) \
                         VALUES (%d, %d, 0, 0)" % (_module_id, i)
                self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                           commit=True)
            for i in range(39):
                _query = "INSERT INTO tbl_pdr \
                         (fld_software_id, fld_question_id, fld_y, fld_value) \
                         VALUES (%d, %d, 0, 0)" % (_module_id, i)
                self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                           commit=True)
            for i in range(72):
                _query = "INSERT INTO tbl_cdr \
                         (fld_software_id, fld_question_id, fld_y, fld_value) \
                         VALUES (%d, %d, 0, 0)" % (_module_id, i)
                self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                           commit=True)
            for i in range(24):
                _query = "INSERT INTO tbl_trr \
                         (fld_software_id, fld_question_id, fld_y, fld_value) \
                         VALUES (%d, %d, 0, 0)" % (_module_id, i)
                self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                           commit=True)

        # Reload the revision tree.
        self._app.REVISION.load_tree()

    def _cancel(self, __button):
        """
        Method to destroy the assistant when the 'Cancel' button is
        pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        """

        self.assistant.destroy()


class AddIncident(object):
    """
    This is the gtk.Assistant() that guides the user through the process of
    adding Incident records to the open RTK Program database.
    """

    def __init__(self, __button, app):
        """
        Initialize an instance of the Add Incident Assistant.

        :param gtk.Button __button: the gtk.Button() that called this
                                    Assistant.
        :param RTK app: the current instance of the RTK application.
        """

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_("RTK Add Incident Assistant"))
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
        _query = "SELECT fld_incident_cat_name FROM tbl_incident_category"
        _results = self._app.COMDB.execute_query(_query, None,
                                                 self._app.ComCnx)
        _widg.load_combo(self.cmbCategory, _results)

        _query = "SELECT fld_incident_type_name FROM tbl_incident_type"
        _results = self._app.COMDB.execute_query(_query, None,
                                                 self._app.ComCnx)
        _widg.load_combo(self.cmbType, _results)

        _query = "SELECT fld_criticality_name FROM tbl_criticality"
        _results = self._app.COMDB.execute_query(_query, None,
                                                 self._app.ComCnx)
        _widg.load_combo(self.cmbCriticality, _results)

        _query = "SELECT fld_lifecycle_name FROM tbl_lifecycles"
        _results = self._app.COMDB.execute_query(_query, None,
                                                 self._app.ComCnx)
        _widg.load_combo(self.cmbLifeCycle, _results)

        _query = "SELECT fld_user_lname || ', ' || fld_user_fname \
                  FROM tbl_users ORDER BY fld_user_lname ASC"
        _results = self._app.COMDB.execute_query(_query, None,
                                                 self._app.ComCnx)
        _widg.load_combo(self.cmbReportedBy, _results)

        _query = "SELECT fld_name, fld_assembly_id, fld_description \
                  FROM tbl_system \
                  WHERE fld_revision_id=%d" % \
                 self._app.REVISION.revision_id
        _results = self._app.COMDB.execute_query(_query, None,
                                                 self._app.ProgCnx)
        _widg.load_combo(self.cmbHardware, _results, simple=False)

        _query = "SELECT fld_description, fld_software_id, fld_description \
                  FROM tbl_software \
                  WHERE fld_revision_id=%d" % \
                 self._app.REVISION.revision_id
        _results = self._app.COMDB.execute_query(_query, None,
                                                 self._app.ProgCnx)
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
                   _(u"Affected Unit:"), _(u"Affected Hardware*:"),
                   _(u"Affected Software:"), _(u"Detection Method*:"),
                   _(u"Test Procedure:"), _(u"Test Case:"),
                   _(u"Execution Time*:")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels,
                                             self.fxdPageGeneral, 5, 5)
        _x_pos += 30

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
            self.btnCalendar = _widg.make_button(height=25,
                                                 width=25,
                                                 label="...",
                                                 image=None)
            self.btnCalendar.set_tooltip_text(_(u"Launch a calendar to select "
                                                u"the incident date"))
            self.btnCalendar.connect('clicked', _util.date_select,
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
        self.txtExecutionTime.connect('focus_out_event', self._check_ready, 2)

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

        :param __widget: the gtk.Widget() calling this method.
        :type __widget: gtk.Widget
        :param __event: the gtk.gdkEvent() that called this method.
        :param __event: gtk.gdk.Event
        :param page: the page in the gtk.Assistant() to check.
        :type page: integer
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
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

        _report_date = datetime.strptime(self.txtIncidentDate.get_text(),
                                         '%Y-%m-%d').toordinal()

        try:
            _execution_time = float(self.txtExecutionTime.get_text())
        except ValueError:
            _execution_time = 0.0

        _query = "INSERT INTO tbl_incident (fld_revision_id, \
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
                                            fld_reviewed_date, \
                                            fld_approved_date, \
                                            fld_complete_date) \
                  VALUES (%d, %d, %d, %d, '%s', '%s', %d, '%s', '%s', 1, \
                          '%s', '%s', '%s', '%s', %f, %d, %d, %d)" % \
                 (self._app.REVISION.revision_id,
                  self._app.SOFTWARE.software_id,
                  self.cmbCategory.get_active(),
                  self.cmbType.get_active(),
                  self.txtDescription.get_text(),
                  self.txtDetails.get_text(*self.txtDetails.get_bounds()),
                  self.cmbCriticality.get_active(),
                  self.cmbDetectMethod.get_active(),
                  self.txtRemarks.get_text(*self.txtRemarks.get_bounds()),
                  self.cmbReportedBy.get_active_text(),
                  _report_date,
                  self.txtTestProcedure.get_text(),
                  self.txtTestCase.get_text(),
                  _execution_time, _report_date + 30, _report_date + 30,
                  _report_date + 30)
        if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                          commit=True):
            _util.rtk_error(_(u"Error adding incident."))
            return True

        # Retrieve the newly added incident id.
        # if _conf.BACKEND == 'mysql':
        #     _query = "SELECT LAST_INSERT_ID()"
        # elif _conf.BACKEND == 'sqlite3':
        #     _query = "SELECT seq \
        #               FROM sqlite_sequence \
        #               WHERE name='tbl_incident'"

        # _incident_id = self._app.DB.execute_query(_query, None,
        #                                           self._app.ProgCnx)

        # try:
        #     _incident_id = _incident_id[0][0]
        # except TypeError:
        #     _util.rtk_error(_(u"Failed to retrieve new incident ID."))
        #     return True

        # Add the new incident to the incident detail table.
        # _query = "INSERT INTO tbl_incident_detail (fld_incident_id) \
        #           VALUES (%d)" % _incident_id
        # if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
        #                                   commit=True):
        #     _util.rtk_error(_(u"Failed to add new incident to incident "
        #                       u"details table."))
        #     return True

        # Reload the Incident class gtk.TreeView().
# TODO: Re-load the Incident class gtk.TreeView() after adding a new incident.
        self._app.INCIDENT.load_tree()

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


class AddTestPlan(object):
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
        # self.assistant.set_forward_page_func(self._next_page)

        # self.assistant.connect('prepare', self._set_next_page)
        self.assistant.connect('apply', self._test_plan_add)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

        self._next_page = 0

# --------------------------------------------------------------------------- #
# Create the introduction page.
# --------------------------------------------------------------------------- #
        fixed = gtk.Fixed()
        _text_ = _(u"This is the RTK test plan creation assistant.  It will "
                   u"help you create a new test plan in the open RTK "
                   u"Program.  Press 'Forward' to continue or 'Cancel' to "
                   u"quit the assistant.")
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

        frame = _widg.make_frame(label=_(""))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(fixed)

        # Create the gtk.Combo that allow one of multiple selections.
        self.cmbAssembly = _widg.make_combo(simple=False)
        self.cmbAssembly.set_tooltip_text(_(u"Select the assembly associated "
                                            u"with the test plan."))
        query = "SELECT fld_name, fld_assembly_id, fld_description \
                 FROM tbl_system"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)
        _widg.load_combo(self.cmbAssembly, results, simple=False)

        self.cmbTestType = _widg.make_combo()
        self.cmbTestType.set_tooltip_text(_(u"Select the type of test to "
                                            u"add."))
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
        self.txtName.set_tooltip_text(_(u"Enter a brief description or title "
                                        u"for the test."))

        self.txtDescription = gtk.TextBuffer()
        textview = _widg.make_text_view(txvbuffer=self.txtDescription,
                                        width=555)
        textview.set_tooltip_text(_(u"Enter a detailed description of the "
                                    u"test."))

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

        frame = _widg.make_frame(label=_(""))
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
                                      _(u"Describe the Reliability Growth "
                                        u"Plan"))
        self.assistant.set_page_complete(frame, True)

# --------------------------------------------------------------------------- #
# Create the page to create the test plan.
# --------------------------------------------------------------------------- #
        fixed = gtk.Fixed()
        _text_ = _(u"Press 'Apply' to create the test plan or 'Cancel' to "
                   u"quit the assistant.")
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
        if _cur_page == 2:
            _test_type = self.cmbTestType.get_active()
            if _test_type == 5:
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
        if row is not None:
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

        if _test_type == 5:                # Reliability growth test plan.
            _mi = float(self.txtMTBFI.get_text())
            _mg = float(self.txtMTBFG.get_text())
            _mgp = float(self.txtMTBFGP.get_text())
            _tr = float(self.txtTechReq.get_text())

            query = "INSERT INTO tbl_tests \
                     (fld_assembly_id, fld_test_id, fld_test_name, \
                      fld_test_description, fld_mi, fld_mg, fld_mgp, fld_tr) \
                     VALUES(%d, %d, '%s', '%s', %f, %f, %f, %f)" % \
                    (_assembly_id, _test_id, _title, _description, _mi, _mg,
                     _mgp, _tr)
        if not self._app.DB.execute_query(query, None, self._app.ProgCnx):
            self._app.debug_log.error("adds.py: Failed to add new test plan "
                                      "to test table.")
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
        label = _widg.make_label(_(u"This is the RTK reliability growth "
                                   u"record assistant.  It will help you add "
                                   u"a record for tracking against the "
                                   u"currently selected reliability growth "
                                   u"plan.  Press 'Forward' to continue or "
                                   u"'Cancel' to quit the assistant."),
                                 width=600, height=-1, wrap=True)
        fixed.put(label, 5, 5)
        self.append_page(fixed)
        self.set_page_type(fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.set_page_title(fixed, _(u"Introduction"))
        self.set_page_complete(fixed, True)

# --------------------------------------------------------------------------- #
# Create the page to gather the necessary inputs.
# --------------------------------------------------------------------------- #
        fixed = gtk.Fixed()

        frame = _widg.make_frame(label=_(""))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(fixed)

# Create the gtk.Combo that allow one of multiple selections.
        self.txtDate = _widg.make_entry(width=100)
        self.txtDate.set_tooltip_text(_(u"Date test record was generated.  "
                                        u"This is not necessarily the date "
                                        u"the record is being added."))
        self.btnDate = _widg.make_button(height=25,
                                         width=25,
                                         label="...",
                                         image=None)
        self.btnDate.connect('button-release-event', _util.date_select,
                             self.txtDate)
        self.txtTime = _widg.make_entry()
        self.txtTime.set_tooltip_text(_(u"Test time."))
        self.chkAdditional = _widg.make_check_button(_(u"Additional"))
        self.chkAdditional.set_tooltip_text(_(u"If checked, the test time is "
                                              u"additional test time.  If "
                                              u"unchecked, the test time is "
                                              u"cumulative since the start of "
                                              u"testing."))
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
        _text_ = _(u"Press 'Apply' to add the record or 'Cancel' to quit the "
                   u"assistant without adding the record.")
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

        (_model_,
         _row_) = self._app.TESTING.treeview.get_selection().get_selected()
        _idx_ = self._app.TESTING._lst_col_order[0]

        _query_ = "SELECT MAX(fld_record_id), MAX(fld_right_interval) \
                   FROM tbl_survival_data \
                   WHERE fld_dataset_id=%d" % self._app.TESTING.test_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=False)

        if _results_[0][0] is None or _results_[0][0] == '':
            _last_id_ = 0
        else:
            _last_id_ = _results_[0][0]

        if _results_[0][1] is None or _results_[0][1] == '':
            _last_time_ = 0.0
        else:
            _last_time_ = float(_results_[0][1])

        _last_id_ += 1

        _assembly_id_ = _model_.get_value(_row_, _idx_)
# Read the test time entered by the user.  If this is entered as additional
# test time, calculate the cumulative test time.
        _time_ = float(self.txtTime.get_text())
        if self.chkAdditional.get_active():
            _time_ = _time_ + _last_time_
        _n_fails_ = int(self.txtNumFails.get_text())

        _date_ = datetime.strptime(self.txtDate.get_text(),
                                   '%Y-%m-%d').toordinal()
        _query_ = "INSERT INTO tbl_survival_data \
                   (fld_record_id, fld_dataset_id, fld_left_interval, \
                    fld_right_interval, fld_quantity, fld_unit, \
                    fld_part_num, fld_market, fld_model, fld_mode_type, \
                    fld_assembly_id, fld_request_date) \
                   VALUES (%d, %d, %f, %f, %d, '%s', '%s', '%s', '%s', \
                           %d, %d, %d)" % (_last_id_,
                                           self._app.TESTING.test_id,
                                           0.0, _time_, _n_fails_, '', '',
                                           '', '', 0, _assembly_id_, _date_)
        if not self._app.DB.execute_query(_query_, None, self._app.ProgCnx,
                                          commit=True):
            self._app.debug_log.error("adds.py: Failed to add new test record "
                                      "to survival data table.")
            return True

        self._app.TESTING.load_test_assessment_tree()

        return False

    def _cancel(self, button):
        """
        Method to destroy the gtk.Assistant when the 'Cancel' button is
        pressed.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        self.destroy()


class CreateDataSet(object):
    """
    This is the gtk.Assistant() that walks the user through the process of
    creating a data set for survival analysis from the Field Incident records
    in the open RTK Program database.
    """

    def __init__(self, button, app):
        """
        Method to initialize the Dataset Creation Assistant.

        :param gtk.Button button: the gtk.Button() that called this method.
        :param rtk app: the current instance of the RTK application.
        """

        self._app = app

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


class AddDataset(object):
    """
    This is the gtk.Assistant() that guides the user through the process of
    creating a new data set in the open RTK Program database.
    """

    def __init__(self, __button, app):
        """
        Method to initialize the blank data set creation assistant.

        :param __button: the gtk.Button() that called this assistant.
        :type __button: gtk.Button
        :param app: the RTK application.
        :type app: RTK application
        """

        self._app = app
        self._assembly = ''

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_(u"RTK Survival Analysis Data Set "
                                   u"Assistant"))
        self.assistant.connect('apply', self._add_data_set)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

        # Create the introduction page.
        _fixed = gtk.Fixed()
        _label = _widg.make_label(_(u"This is the RTK Survival Analysis Data "
                                    u"Set Assistant.  It will help you add a "
                                    u"data set to the open RTK Program "
                                    u"database.  Press 'Forward' to continue "
                                    u"or 'Cancel' to quit the assistant."),
                                  width=-1, height=-1, wrap=True)
        _fixed.put(_label, 5, 5)
        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(_fixed, _(u"Introduction"))
        self.assistant.set_page_complete(_fixed, True)

        # Create the page to gather the necessary inputs.
        _fixed = gtk.Fixed()

        _frame = _widg.make_frame(label=_(""))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_fixed)

        # Create the gtk.Widgets() for entering information about the new
        # data set.
        self.cmbAssembly = _widg.make_combo(simple=False)
        self.txtDescription = _widg.make_entry(width=400)
        self.cmbSource = _widg.make_combo()
        self.cmbDistribution = _widg.make_combo()
        self.txtConfidence = _widg.make_entry(width=50)
        self.cmbConfidenceType = _widg.make_combo()
        self.cmbFitMethod = _widg.make_combo()
        self.chkNevadaChart = _widg.make_check_button(label=_(u"Use Nevada "
                                                              u"Chart"))

        # Load the gtk.ComboBox() widgets.
        _query = "SELECT fld_name, fld_assembly_id, fld_description \
                  FROM tbl_system"
        _results = self._app.DB.execute_query(_query, None, self._app.ProgCnx)
        _widg.load_combo(self.cmbAssembly, _results, simple=False)
        _results = [["ALT"], [_(u"Reliability Growth")],
                    [_(u"Reliability Demonstration")], [_(u"Field")]]
        _widg.load_combo(self.cmbSource, _results)
        _results = [[u"MCF"], [u"Kaplan-Meier"], [_(u"NHPP - Power Law")],
                    [u"NHPP - Loglinear"], [_(u"Exponential")],
                    [_(u"Lognormal")], [_(u"Normal")], [u"Weibull"],
                    ["WeiBayes"]]
        _widg.load_combo(self.cmbDistribution, _results)
        _results = [["Lower One-Sided"], ["Upper One-Sided"], ["Two-Sided"]]
        _widg.load_combo(self.cmbConfidenceType, _results)
        _results = [["MLE"], ["Rank Regression"]]
        _widg.load_combo(self.cmbFitMethod, _results)

        # Create and place the labels.
        _labels = [_(u"Assembly:"), _(u"Description:"), _(u"Data Source:"),
                   _(u"Distribution:"), _(u"Confidence:"),
                   _(u"Confidence Type:"), _(u"Fit Method:"), _("")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
        _x_pos += 35

        # Create the tooltip text for the gtk.Widgets()
        self.cmbAssembly.set_tooltip_markup(_(u"Selects the hardware assembly "
                                              u"to associate the data set "
                                              u"with."))
        self.txtDescription.set_tooltip_markup(_(u"Describe the data set to "
                                                 u"be added."))
        self.cmbSource.set_tooltip_markup(_(u"Select the source of the "
                                            u"records in the data set."))
        self.cmbDistribution.set_tooltip_markup(_(u"Select the s-distribution "
                                                  u"to fit the data set."))
        self.txtConfidence.set_tooltip_markup(_(u"Set the s-confidence level "
                                                u"for analysis of the data "
                                                u"set."))
        self.cmbConfidenceType.set_tooltip_markup(_(u"Select the type of "
                                                    u"confidence bounds to "
                                                    u"apply."))
        self.cmbFitMethod.set_tooltip_markup(_(u"Select the method to use for "
                                               u"fitting the data set to the "
                                               u"selected distribution."))
        self.chkNevadaChart.set_tooltip_markup(_(u"Selects whether or not to "
                                                 u"use a Nevada Chart for "
                                                 u"entering the data."))

        # Place the input gtk.Widgets()
        _fixed.put(self.cmbAssembly, _x_pos, _y_pos[0])
        _fixed.put(self.txtDescription, _x_pos, _y_pos[1])
        _fixed.put(self.cmbSource, _x_pos, _y_pos[2])
        _fixed.put(self.cmbDistribution, _x_pos, _y_pos[3])
        _fixed.put(self.txtConfidence, _x_pos, _y_pos[4])
        _fixed.put(self.cmbConfidenceType, _x_pos, _y_pos[5])
        _fixed.put(self.cmbFitMethod, _x_pos, _y_pos[6])
        _fixed.put(self.chkNevadaChart, _x_pos, _y_pos[7])

        self.assistant.append_page(_frame)
        self.assistant.set_page_type(_frame, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(_frame, _(u"Enter Information for the "
                                                u"New Data Set"))
        self.assistant.set_page_complete(_frame, True)

        # Create the page to apply the import criteria.
        _fixed = gtk.Fixed()

        _label = _widg.make_label(_(u"Press 'Apply' to create the requested "
                                    u"data set or 'Cancel' to quit the "
                                    u"assistant."), width=-1, height=-1,
                                  wrap=True)
        _fixed.put(_label, 5, _y_pos[0] + 35)

        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(_fixed, _(u"Create Data Set"))
        self.assistant.set_page_complete(_fixed, True)

        self.assistant.show_all()

    def _add_data_set(self, __button):
        """
        Method to create the new data set and add it to the open RTK Program
        database.

        :param __button: the gtk.Button() that called this method.
        :type __button: gtk.Button
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        _query = "SELECT MAX(fld_dataset_id) FROM tbl_dataset"
        _dataset_id = self._app.DB.execute_query(_query, None,
                                                 self._app.ProgCnx)
        try:
            _dataset_id = _dataset_id[0][0] + 1
        except TypeError:
            _dataset_id = 0

        # Retrieve the inputs provided by the user.
        _model = self.cmbAssembly.get_model()
        _row = self.cmbAssembly.get_active_iter()
        _assembly_id = int(_model.get_value(_row, 1))
        _description = self.txtDescription.get_text()
        _source = self.cmbSource.get_active()
        _distribution = self.cmbDistribution.get_active()
        _confidence = float(self.txtConfidence.get_text())
        _conf_type = self.cmbConfidenceType.get_active()
        _fit_method = self.cmbFitMethod.get_active()
        _nevada = _util.string_to_boolean(self.chkNevadaChart.get_active())

        _query = "INSERT INTO tbl_dataset \
                  (fld_dataset_id, fld_assembly_id, fld_description, \
                   fld_source, fld_distribution_id, fld_confidence, \
                   fld_confidence_type, fld_fit_method, fld_nevada_chart) \
                 VALUES(%d, %d, '%s', %d, %d, %f, %d, %d, %d)" % \
                 (_dataset_id, _assembly_id, _description, _source,
                  _distribution, _confidence, _conf_type, _fit_method, _nevada)

        if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                          commit=True):
            _util.rtk_error(_(u"Error adding new data set."))
            return True
        else:
            _util.rtk_information(_(u"Added data set %s to the open RTK "
                                    u"Program database.") % _description)

            # Re-load the Dataset class gtk.TreeView() to show the newly added
            # data set.
            self._app.DATASET.load_tree()

            return False

    def _cancel(self, __button):
        """
        Method to destroy the gtk.Assistant() when the 'Cancel' button is
        pressed.

        :param __button: the gtk.Button() that called this method.
        :type __button: gtk.Button
        """

        self.assistant.destroy()

        return True


class AddDatasetRecord(object):
    """
    This is the gtk.Assistant() that walks the user through the process of
    adding a record to the currently selected survival data set in the open
    RTK Program database.
    """

    def __init__(self, _button, app):
        """
        Method to initialize the survival data set record addition assistant.

        :param __button: the gtk.Button() that called this assistant.
        :type __button: gtk.Button
        :param app: the RTK application.
        :type app: RTK application
        """

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_(_(u"RTK Survival Analysis Record "
                                     u"Assistant")))
        # self.assistant.connect('apply', self._add_record)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

        # Create the introduction page.
        _fixed = gtk.Fixed()
        _label = _widg.make_label(_(u"This is the RTK survival analysis "
                                    u"record assistant.  It will help you add "
                                    u"a record to the currently selected "
                                    u"survival data set.  Press 'Forward' to "
                                    u"continue or 'Cancel' to quit the "
                                    u"assistant."), width=-1, height=-1,
                                  wrap=True)
        _fixed.put(_label, 5, 5)

        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(_fixed, _(u"Introduction"))
        self.assistant.set_page_complete(_fixed, True)

        # Create the page to gather the necessary failure time inputs.
        _fixed = gtk.Fixed()

        _frame = _widg.make_frame(label=_(""))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_fixed)

        self.txtLeft = _widg.make_entry()
        self.txtRight = _widg.make_entry()
        self.txtQuantity = _widg.make_entry()

        _labels = [_(u"Left:"), _(u"Right:"), _(u"Status:"), _(u"Quantity:"),
                   _(u"Affected Unit:"), _(u"Part Number:"), _(u"Market:"),
                   _(u"Model:"), _(u"Assembly:")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)

        self.txtLeft.set_tooltip_markup(_(u"Left of the interval.  If failure "
                                          u"time is exact, set this equal to "
                                          u"the failure time."))
        self.txtRight.set_tooltip_text(_(u"Right of the interval.  If failure "
                                         u"time is exact, set this equal to "
                                         u"the failure time."))
        self.txtQuantity.set_tooltip_text(_(u"Number of failures observed "
                                            u"during interval or at failure "
                                            u"time."))
        self.txtQuantity.set_text("1")

        _fixed.put(self.txtLeft, _x_pos, _y_pos[0])
        _fixed.put(self.txtRight, _x_pos, _y_pos[1])
        _fixed.put(self.txtQuantity, _x_pos, _y_pos[2])

        self.assistant.append_page(_frame)
        self.assistant.set_page_type(_frame, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(_frame, _(u"Enter Failure Time Data"))
        self.assistant.set_page_complete(_frame, True)

        # Create the page to add the record.
        _fixed = gtk.Fixed()
        _label = _widg.make_label(_(u"Press 'Apply' to add the record to the "
                                    u"selected survival data set or 'Cancel' "
                                    u"to quit the assistant without adding "
                                    u"the record."), width=-1, height=-1,
                                  wrap=True)
        _fixed.put(_label, 5, 5)

        self.assistant.append_page(_fixed)
        self.assistant.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(_fixed, _(u"Add Survival Data Record"))
        self.assistant.set_page_complete(_fixed, True)

        self.assistant.show_all()

    def _cancel(self, __button):
        """
        Method to destroy the gtk.Assistant() when the 'Cancel' button is
        pressed.

        :param __button: the gtk.Button() that called this method.
        :type __button: gtk.Button
        """

        self.assistant.destroy()

        return True
