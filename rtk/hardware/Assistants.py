#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.Assistants.py is part of The RTK Project
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

"""
##################################
Hardware Package Assistants Module
##################################
"""

import gettext
import locale
import sys

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
    import Configuration
    import Utilities
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    import rtk.gui.gtk.Widgets as Widgets

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ImportHardware(gtk.Assistant):
    """
    This is the gtk.Assistant() that walks the user through the process of
    importing Hardware records to the open RTK Program database.
    """

    def __init__(self, revision_id, dao, modulebook):
        """
        Method to initialize an instance of the Import Hardware Assistant.

        :param int revision_id: the ID of the revision to add the incident to.
        :param dao: the :py:class:`rtk.dao.DAO` used to communicate with the
                    RTK Project database.
        :param modulebook: the :py:class:`rtk.Hardware.ModuleBook` to add the
                           the imported Hardware BoM to.
        """

        self._dao = dao
        self._revision_id = revision_id
        self._modulebook = modulebook

        gtk.Assistant.__init__(self)
        self.set_title(_(u"RTK Import Hardware Assistant"))
        self.connect('apply', self._import)
        self.connect('cancel', self._cancel)
        self.connect('close', self._cancel)

        # Initialize some variables.
        self._file_index = [-1] * 96

        # Create the introduction page.
        _fixed = gtk.Fixed()
        _label = Widgets.make_label(_(u"This is the RTK hardware import "
                                      u"assistant.  It will help you import "
                                      u"system hardware information to the "
                                      u"database from external files.  Press "
                                      u"'Forward' to continue or 'Cancel' to "
                                      u"quit the assistant."),
                                    width=600, height=-1, wrap=True)
        _fixed.put(_label, 5, 5)
        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.set_page_title(_fixed, _(u"Introduction"))
        self.set_page_complete(_fixed, True)

        # Create the age to map input file fields to database fields.
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
        _label.set_markup(u"<span weight='bold'>%s</span>" %
                          _("Database\nField"))
        _label.show_all()
        _column.setWidgetset(_label)
        self.tvwFileFields.append_column(_column)

        (_file_fields, self._file_contents) = Widgets.select_source_file(self)
        if len(_file_fields) == 0:
            Utilities.rtk_information(_(u"Source file must have headings for "
                                        u"each column of data.  Please add "
                                        u"headings to the source file and try "
                                        u"again."))
            self._cancel()
        if len(self._file_contents) == 0:
            Utilities.rtk_warning(_(u"No data was found in the source file.  "
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
        _label.set_markup(u"<span weight='bold'>%s</span>" % _("File\nField"))
        _label.show_all()
        _column.setWidgetset(_label)
        self.tvwFileFields.append_column(_column)

        _cell.connect('changed', self._on_cell_combo_changed, 2, _model)

        _db_fields = [_(u"Revision ID"), _(u"Assembly ID"),
                      _(u"Additive Adjustment Factor"), _(u"Allocation Type"),
                      _(u"Alternate Part Number"), _(u"Assembly Criticality"),
                      _(u"Attachments"), _(u"Availability"),
                      _(u"Availability, Mission"), _(u"CAGE Code"),
                      _(u"Calculation Model"), _(u"Category"),
                      _(u"Composite Reference Designator"), _(u"Cost, Unit"),
                      _(u"Cost/Failure"), _(u"Cost/Hour"), _(u"Cost Type"),
                      _(u"Description"), _(u"Detection Failure Rate"),
                      _(u"Detection Percent"), _(u"Duty Cycle"),
                      _(u"Entered By"), _(u"Environment, Active"),
                      _(u"Environment, Dormant"), _(u"Failure Distribution"),
                      _(u"Parameter 1 (Scale)"), _(u"Parameter 2 (Shape)"),
                      _(u"Parameter 3 (Location)"), _(u"Failure Rate, Actve"),
                      _(u"Failure Rate, Dormant"), _(u"Failure Rate, Mission"),
                      _(u"Failure Rate, Percent"),
                      _(u"Failure Rate, Predicted"),
                      _(u"Failure Rate, Software"),
                      _(u"Failure Rate, Specified"), _(u"Failure Rate Type"),
                      _(u"Figure Number"), _(u"Humidity"), _(u"Image File"),
                      _(u"Isolation Failure Rate"), _(u"Isolation Percent"),
                      _(u"Logistics Control Number"), _(u"Level"),
                      _(u"Manufacturer"),
                      _(u"Mean Corrective Maintenance Time"),
                      _(u"Mission Time"), _(u"Mean Maintenance Time"),
                      _(u"Modified By"),
                      _(u"Mean Preventive Maintenance Time"),
                      _(u"MTBF, Mission"), _(u"MTBF, Predicted"),
                      _(u"MTBF, Specified"), _(u"MTTR"),
                      _(u"MTTR Additive Adjustment Factor"),
                      _(u"MTTR, Multiplicative Adjustment Factor"),
                      _(u"MTTR, Specified"), _(u"MTTR Type"),
                      _(u"Multiplicative Adjustment Factor"), _(u"Name"),
                      _(u"NSN"), _(u"Overstressed?"), _(u"Page Number"),
                      _(u"Parent Assembly"), _(u"Part?"), _(u"Part Number"),
                      _(u"Percent Isolation, Group"),
                      _(u"Percent Isolation, Single"), _(u"Quantity"),
                      _(u"Reference Designator"), _(u"Reliability, Mission"),
                      _(u"Reliability, Predicted"), _(u"Remarks"),
                      _(u"Repair Distribution"),
                      _(u"Repair Parameter 1 (Scale)"),
                      _(u"Repair Parameter 2 (Shape)"), _(u"Repairable?"),
                      _(u"RPM"), _(u"Specification Number"), _(u"Subcategory"),
                      _(u"Tagged?"), _(u"Temperature, Active"),
                      _(u"Temperature, Dormant"), _(u"Total Part Quantity"),
                      _(u"Total Power"), _(u"Vibration"),
                      _(u"Weibull Data Set"), _(u"Weibull File"),
                      _(u"Year of Manufacture"), _(u"Hazard Rate Model"),
                      _(u"Reliability Goal Measure"), _(u"Reliability Goal"),
                      _(u"MTBF LCL"), _(u"MTBF UCL"), _(u"h(t) LCL"),
                      _(u"h(t) UCL")]

        for i in range(len(_db_fields)):
            _model.append([i, _db_fields[i], ""])

        self.append_page(_scrollwindow)
        self.set_page_type(_scrollwindow, gtk.ASSISTANT_PAGE_CONTENT)
        self.set_page_title(_scrollwindow, _(u"Select Fields to Import"))
        self.set_page_complete(_scrollwindow, True)

        # Create the page to apply the import criteria.
        _fixed = gtk.Fixed()
        _label = Widgets.make_label(_(u"Press 'Apply' to import the requested "
                                      u"data or 'Cancel' to quit the "
                                      u"assistant."), width=600, height=-1,
                                    wrap=True)
        _fixed.put(_label, 5, 5)
        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONFIRM)
        self.set_page_title(_fixed, _(u"Import Data"))
        self.set_page_complete(_fixed, True)

        self.show_all()

    def _on_cell_combo_changed(self, cell, path, row, position, treemodel):
        """
        Method to respond to gtk.CellRendererCombo() 'changed' signals.

        :param gtk.CellRendererCombo cell: the gtk.CellRendererCombo() that
                                           called this method.
        :param str path: the path in the gtk.TreeView() containing the
                         gtk.CellRendererCombo() that called this method.
        :param gtk.TreeIter row: the new gtk.TreeIter() in the
                                 gtk.CellRendererCombo() that called this
                                 method.
        :param int position: the position of in the gtk.TreeView() of the
                             gtk.CellRendererCombo() that called this function.
        :param gtk.TreeModel treemodel: the gtk.TreeModel() for the
                                        gtk.TreeView().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
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
        :rtype: bool
        """

        if current_page == 0:
            Widgets.select_source_file(self)
        else:
            self.set_current_page(current_page + 1)

    def _import(self, __button):
        """
        Method to perform the import from an external file to the database.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        Utilities.set_cursor(self._app, gtk.gdk.WATCH)

        _contents = []
        for i in range(len(self._file_contents) - 1):
            _temp = []
            for j in range(len(self._file_index)):
                if self._file_index[j] == -1:
                    _temp.append('')
                else:
                    try:
                        _temp.append(self._file_contents[i][self._file_index[j]].rstrip('\t'))
                    except IndexError:
                        _temp.append('')

            # Convert missing integer values to correct default value.
            for i in [0, 1, 3, 5, 11, 22, 23, 24, 43, 60,
                      63, 72, 75, 78, 79, 82, 89]:
                _temp[i] = Utilities.missing_to_default(_temp[i], 0)

            for i in [10, 16, 35, 42, 56, 67, 85]:
                _temp[i] = Utilities.missing_to_default(_temp[i], 1)

            _temp[87] = Utilities.missing_to_default(_temp[87], 2013)

            # Convert missing float values to correct default value.
            for i in [2, 5, 13, 14, 15, 18, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                      34, 39, 40, 44, 46, 48, 49, 50, 51, 52, 54, 55, 65, 66,
                      73, 74, 76, 83, 84, 91, 92, 93, 94]:
                _temp[i] = Utilities.missing_to_default(_temp[i], 0.0)

            for i in [7, 8, 53, 57, 69, 70, 90]:
                _temp[i] = Utilities.missing_to_default(_temp[i], 1.0)

            for i in [80, 81]:
                _temp[i] = Utilities.missing_to_default(_temp[i], 30.0)

            _temp[37] = Utilities.missing_to_default(_temp[37], 50.0)

            for i in [19, 20, 45]:
                _temp[i] = Utilities.missing_to_default(_temp[i], 100.0)

            _contents.append(_temp)

        # Find the top-level assembly and use it to update the top-level record
        # in the database.
        _root = [assembly for assembly in _contents if assembly[62] == '-'][0]

        _values = (int(_root[0]), 0, float(_root[2]), int(_root[3]),
                   str(_root[4]), str(_root[5]), str(_root[6]),
                   float(_root[7]), float(_root[8]), str(_root[9]),
                   int(_root[10]), int(_root[11]), str(_root[12]),
                   float(_root[13]), float(_root[14]), float(_root[15]),
                   int(_root[16]), str(_root[17]), float(_root[18]),
                   float(_root[19]), float(_root[20]), str(_root[21]),
                   int(_root[22]), int(_root[23]), int(_root[24]),
                   float(_root[25]), float(_root[26]), float(_root[27]),
                   float(_root[28]), float(_root[29]), float(_root[30]),
                   float(_root[31]), float(_root[32]), float(_root[33]),
                   float(_root[34]), int(_root[35]), str(_root[36]),
                   float(_root[37]), str(_root[38]), float(_root[39]),
                   float(_root[40]), str(_root[41]), int(_root[42]),
                   int(_root[43]), float(_root[44]), float(_root[45]),
                   float(_root[46]), str(_root[47]), float(_root[48]),
                   float(_root[49]), float(_root[50]), float(_root[51]),
                   float(_root[52]), float(_root[53]), float(_root[54]),
                   float(_root[55]), int(_root[56]), float(_root[57]),
                   str(_root[58]), str(_root[59]), int(_root[60]),
                   str(_root[61]), str(_root[62]), int(_root[63]),
                   str(_root[64]), float(_root[65]), float(_root[66]),
                   int(_root[67]), str(_root[68]), float(_root[69]),
                   float(_root[70]), str(_root[71]), int(_root[72]),
                   float(_root[73]), float(_root[74]), int(_root[75]),
                   float(_root[76]), str(_root[77]), int(_root[78]),
                   int(_root[79]), float(_root[80]), float(_root[81]),
                   int(_root[82]), float(_root[83]), float(_root[84]),
                   int(_root[85]), str(_root[86]), int(_root[87]),
                   str(_root[88]), int(_root[89]), float(_root[90]),
                   float(_root[91]), float(_root[92]), float(_root[93]),
                   float(_root[94]))

        _query = "UPDATE tbl_system \
                  SET fld_revision_id=%d, fld_assembly_id=%d, \
                      fld_add_adj_factor=%f, fld_allocation_type=%d, \
                      fld_alt_part_number='%s', \
                      fld_assembly_criticality='%s', \
                      fld_attachments='%s', fld_availability=%f, \
                      fld_availability_mission=%f, fld_cage_code='%s', \
                      fld_calculation_model=%d, fld_category_id=%d, \
                      fld_comp_ref_des='%s',fld_cost=%f,  \
                      fld_cost_failure=%f, fld_cost_hour=%f, \
                      fld_cost_type=%d, fld_description='%s', \
                      fld_detection_fr=%f, fld_detection_percent=%f, \
                      fld_duty_cycle=%f, fld_entered_by='%s', \
                      fld_environment_active=%d, fld_environment_dormant=%d, \
                      fld_failure_dist=%d, fld_failure_parameter_1=%f, \
                      fld_failure_parameter_2=%f, \
                      fld_failure_parameter_3=%f, \
                      fld_failure_rate_active=%f, \
                      fld_failure_rate_dormant=%f, \
                      fld_failure_rate_mission=%f, \
                      fld_failure_rate_percent=%f, \
                      fld_failure_rate_predicted=%f, \
                      fld_failure_rate_software=%f, \
                      fld_failure_rate_specified=%f, \
                      fld_failure_rate_type=%d, fld_figure_number='%s', \
                      fld_humidity=%f, fld_image_file='%s', \
                      fld_isolation_fr=%f, fld_isolation_percent=%f, \
                      fld_lcn='%s', fld_level=%d, fld_manufacturer=%d, \
                      fld_mcmt=%f, fld_mission_time=%f, fld_mmt=%f, \
                      fld_modified_by='%s', fld_mpmt=%f, \
                      fld_mtbf_mission=%f, fld_mtbf_predicted=%f, \
                      fld_mtbf_specified=%f, fld_mttr=%f, \
                      fld_mttr_add_adj_factor=%f, \
                      fld_mttr_mult_adj_factor=%f, \
                      fld_mttr_specified=%f, fld_mttr_type=%d, \
                      fld_mult_adj_factor=%f, fld_name='%s', \
                      fld_nsn='%s', fld_overstress=%d, \
                      fld_page_number='%s', fld_parent_assembly='%s', \
                      fld_part=%d, fld_part_number='%s', \
                      fld_percent_isolation_group_ri=%f, \
                      fld_percent_isolation_single_ri=%f, \
                      fld_quantity=%d, fld_ref_des='%s', \
                      fld_reliability_mission=%f, \
                      fld_reliability_predicted=%f, fld_remarks='%s', \
                      fld_repair_dist=%d, fld_repair_parameter_1=%f, \
                      fld_repair_parameter_2=%f, fld_repairable=%d, \
                      fld_rpm=%f, fld_specification_number='%s', \
                      fld_subcategory_id=%d, fld_tagged_part=%d, \
                      fld_temperature_active=%f, \
                      fld_temperature_dormant=%f, \
                      fld_total_part_quantity=%d, \
                      fld_total_power_dissipation=%f, fld_vibration=%f, \
                      fld_weibull_data_set=%d, fld_weibull_file='%s', \
                      fld_year_of_manufacture=%d, fld_ht_model='%s', \
                      fld_reliability_goal_measure=%d, \
                      fld_reliability_goal=%f, fld_mtbf_lcl=%f, \
                      fld_mtbf_ucl=%f, fld_failure_rate_lcl=%f, \
                      fld_failure_rate_ucl=%f \
                  WHERE fld_parent_assembly='-'" % _values
        if not self._dao.execute(_query, commit=True):
            Utilities.rtk_error(_(u"Error importing hardware information to "
                                  u"the open RTK Program database."))

            Utilities.set_cursor(self._app, gtk.gdk.LEFT_PTR)

            return True

        else:
            # Find all the children of the top-level assembly.
            _iter = {0: '-'}
            j = 0
            _root = [child for child in _contents if child[62] == str(j)]
            self._add_children(_root, _iter, _contents)

            Utilities.set_cursor(self._app, gtk.gdk.LEFT_PTR)

            self._app.HARDWARE.load_tree()

            return False

    def _add_children(self, root, _iter, contents):
        """
        Method to add all children assemblies to the open RTK Program database.

        :param list root: the list of children assemblies to add.
        :param dict _iter: a dictionary with assembly id as the key and the
                           string representation of the gtk.TreeIter() as the
                           value.
        :param list contents: the contents of the file which is being imported.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for i in range(len(root)):

            # Build the string representation of the assembly's iter.
            _parent_id = int(root[i][62])
            if str(_iter[_parent_id]) == '-':
                _iter[int(root[i][1])] = '0:' + str(i)
                root[i][62] = '0'
            else:
                _iter[int(root[i][1])] = str(_iter[_parent_id]) + \
                                          ':' + str(i)
                root[i][62] = str(_iter[_parent_id])

            _values = (int(root[i][0]), int(root[i][1]),
                       float(root[i][2]), int(root[i][3]),
                       str(root[i][4]), float(root[i][5]),
                       str(root[i][6]), float(root[i][7]),
                       float(root[i][8]), str(root[i][9]),
                       int(root[i][10]), int(root[i][11]),
                       str(root[i][12]), float(root[i][13]),
                       float(root[i][14]), float(root[i][15]),
                       int(root[i][16]), str(root[i][17]),
                       float(root[i][18]), float(root[i][19]),
                       float(root[i][20]), str(root[i][21]),
                       int(root[i][22]), int(root[i][23]),
                       int(root[i][24]), float(root[i][25]),
                       float(root[i][26]), float(root[i][27]),
                       float(root[i][28]), float(root[i][29]),
                       float(root[i][30]), float(root[i][31]),
                       float(root[i][32]), float(root[i][33]),
                       float(root[i][34]), int(root[i][35]),
                       str(root[i][36]), float(root[i][37]),
                       str(root[i][38]), float(root[i][39]),
                       float(root[i][40]), str(root[i][41]),
                       int(root[i][42]), int(root[i][43]),
                       float(root[i][44]), float(root[i][45]),
                       float(root[i][46]), str(root[i][47]),
                       float(root[i][48]), float(root[i][49]),
                       float(root[i][50]), float(root[i][51]),
                       float(root[i][52]), float(root[i][53]),
                       float(root[i][54]), float(root[i][55]),
                       int(root[i][56]), float(root[i][57]),
                       str(root[i][58]), str(root[i][59]),
                       int(root[i][60]), str(root[i][61]),
                       str(root[i][62]), int(root[i][63]),
                       str(root[i][64]), float(root[i][65]),
                       float(root[i][66]), int(root[i][67]),
                       str(root[i][68]), float(root[i][69]),
                       float(root[i][70]), str(root[i][71]),
                       int(root[i][72]), float(root[i][73]),
                       float(root[i][74]), int(root[i][75]),
                       float(root[i][76]), str(root[i][77]),
                       int(root[i][78]), int(root[i][79]),
                       float(root[i][80]), float(root[i][81]),
                       int(root[i][82]), float(root[i][83]),
                       float(root[i][84]), int(root[i][85]),
                       str(root[i][86]), int(root[i][87]),
                       str(root[i][88]), int(root[i][89]),
                       float(root[i][90]), float(root[i][91]),
                       float(root[i][92]), float(root[i][93]),
                       float(root[i][94]))

            _query = "INSERT INTO tbl_system \
                      VALUES (%d, %d, %f, %d, '%s', %f, '%s', %f, \
                              %f, '%s', %d, %d, '%s', %f, %f, %f, \
                              %d, '%s', %f, %f, %f, '%s', %d, %d, \
                              %d, %f, %f, %f, %f, %f, %f, %f, %f, \
                              %f, %f, %d, '%s', %f, '%s', %f, %f, \
                              '%s', %d, %d, %f, %f, %f, '%s', %f, \
                              %f, %f, %f, %f, %f, %f, %f, %d, %f, \
                              '%s', '%s', %d, '%s', '%s', %d, '%s', \
                              %f, %f, %d, '%s', %f, %f, '%s', %d, \
                              %f, %f, %d, %f, '%s', %d, %d, %f, %f, \
                              %d, %f, %f, %d, '%s', %d, '%s', %d, \
                              %f, %f, %f, %f, %f)" % _values
            if not self._dao.execute(_query, commit=True):
                Utilities.rtk_error(_(u"Error importing hardware information "
                                      u"to the open RTK Program database."))
                self._app.import_log.error("Failed to import record: %d" %
                                           int(root[i][1]))
                return True

            else:
                # Add the new hardware to the allocation table, the risk
                # analysis table, the similar items table, the FMECA table and
                # the functional matrix table.
                _values = (int(root[i][0]), int(root[i][1]))
                _query = "INSERT INTO tbl_allocation \
                          (fld_revision_id, fld_assembly_id) \
                          VALUES (%d, %d)" % _values
                if not self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx,
                                                  commit=True):
                    self._app.import_log.error("Failed to import record: %d "
                                               "to the Allocation Table" %
                                               int(root[i][1]))
                    _error = True

                _query = "INSERT INTO tbl_risk_analysis \
                          (fld_revision_id, fld_assembly_id) \
                          VALUES (%d, %d)" % _values
                if not self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx,
                                                  commit=True):
                    self._app.import_log.error("Failed to import record: %d "
                                               "to the Risk Analysis Table" %
                                               int(root[i][1]))
                    _error = True

                _query = "INSERT INTO tbl_similar_item \
                          (fld_revision_id, fld_assembly_id) \
                          VALUES (%d, %d)" % _values
                if not self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx,
                                                  commit=True):
                    self._app.import_log.error("Failed to import record: %d "
                                               "to the Similar Item Table" %
                                               int(root[i][1]))
                    _error = True

                _query = "INSERT INTO tbl_functional_matrix \
                          (fld_revision_id, fld_assembly_id) \
                          VALUES(%d, %d)" % _values
                if not self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx,
                                                  commit=True):
                    self._app.import_log.error("Failed to import record: %d "
                                               "to the Functional Matrix "
                                               "Table" % int(root[i][1]))
                    _error = True

            _children = [child for child in contents
                         if child[62] == root[i][1]]
            if len(_children) > 0:
                self._add_children(_children, _iter, contents)

        return False

    def _cancel(self, __button=None):
        """
        Method to destroy the gtk.Assistant() when the 'Cancel' button is
        pressed.

        :keyword gtk.Button __button: the gtk.Button() that called this method.
        """

        self.destroy()
