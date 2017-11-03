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
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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

# TODO: Move this to the Incident class.
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
