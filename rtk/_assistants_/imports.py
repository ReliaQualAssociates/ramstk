#!/usr/bin/env python

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2012 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       import.py is part of The RelKit Project
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


class ImportHardware:
    """
    This is the gtk.Assistant that walks the user through the process of
    importing Hardware records to the open RelKit Program database.
    """

    def __init__(self, button, app):
        """
        Initialize an instance of the Import Hardware Assistant.

        Keyword Arguments:
        button -- the gtk.Button widget that calling this Assistant.
        app    -- the instance of the RelKit application calling the Assistant.
        """
        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_(u"RelKit Import Hardware Assistant"))
        self.assistant.connect('apply', self._import)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

# Initialize some variables.
        self._file_index = [-1] * 96

# Create the introduction page.
        fixed = gtk.Fixed()
        _text_ = _(u"This is the RelKit hardware import assistant.  It will help you import system hardware information to the database from external files.  Press 'Forward' to continue or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=600, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(fixed, _(u"Introduction"))
        self.assistant.set_page_complete(fixed, True)

# Create the age to map input file fields to database fields.
        model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                              gobject.TYPE_STRING)
        self.tvwFileFields = gtk.TreeView(model)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwFileFields)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        column.set_resizable(True)
        column.set_visible(False)
        self.tvwFileFields.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, text=1)
        column.set_resizable(True)
        label = gtk.Label(column.get_title())
        label.set_line_wrap(True)
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_markup(u"<span weight='bold'>%s</span>" % _("Database\nField"))
        label.show_all()
        column.set_widget(label)
        self.tvwFileFields.append_column(column)

        cell = gtk.CellRendererCombo()
        cellmodel = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT)
        (_file_fields, self._file_contents) = self._select_source_file()
        cellmodel.append(["", -1])
        for i in range(len(_file_fields)):
            cellmodel.append([_file_fields[i], i])

        cell.set_property('editable', 1)
        cell.set_property('has-entry', False)
        cell.set_property('model', cellmodel)
        cell.set_property('text-column', 0)

        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, text=2)
        column.set_resizable(True)
        label = gtk.Label(column.get_title())
        label.set_line_wrap(True)
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_markup(u"<span weight='bold'>%s</span>" % _("File\nField"))
        label.show_all()
        column.set_widget(label)
        self.tvwFileFields.append_column(column)

        cell.connect('changed', self._callback_combo_cell, 2, model)

        _db_fields = ["Revision ID", "Assembly ID",
                      "Additive Adjustment Factor", "Allocation Type",
                      "Alternate Part Number", "Assembly Criticality",
                      "Attachments", "Availability", "Availability, Mission",
                      "CAGE Code", "Calculation Model", "Category",
                      "Composite Reference Designator", "Cost, Unit",
                      "Cost/Failure", "Cost/Hour", "Cost Type", "Description",
                      "Detection Failure Rate", "Detection Percent",
                      "Duty Cycle", "Entered By", "Environment, Active",
                      "Environment, Dormant", "Failure Distribution",
                      "Parameter 1 (Scale)", "Parameter 2 (Shape)",
                      "Parameter 3 (Location)", "Failure Rate, Actve",
                      "Failure Rate, Dormant", "Failure Rate, Mission",
                      "Failure Rate, Percent", "Failure Rate, Predicted",
                      "Failure Rate, Software", "Failure Rate, Specified",
                      "Failure Rate Type", "Figure Number", "Humidity",
                      "Image File", "Isolation Failure Rate",
                      "Isolation Percent", "Logistics Control Number",
                      "Level", "Manufacturer",
                      "Mean Corrective Maintenance Time", "Mission Time",
                      "Mean Maintenance Time", "Modified By",
                      "Mean Preventive Maintenance Time", "MTBF, Mission",
                      "MTBF, Predicted", "MTBF, Specified", "MTTR",
                      "MTTR Additive Adjustment Factor",
                      "MTTR, Multiplicative Adjustment Factor",
                      "MTTR, Specified", "MTTR Type",
                      "Multiplicative Adjustment Factor", "Name", "NSN",
                      "Overstressed?", "Page Number", "Parent Assembly",
                      "Part?", "Part Number", "Percent Isolation, Group",
                      "Percent Isolation, Single", "Quantity",
                      "Reference Designator", "Reliability, Mission",
                      "Reliability, Predicted", "Remarks",
                      "Repair Distribution", "Repair Parameter 1 (Scale)",
                      "Repair Parameter 2 (Shape)", "Repairable?", "RPM",
                      "Specification Number", "Subcategory", "Tagged?",
                      "Temperature, Active", "Temperature, Dormant",
                      "Total Part Quantity", "Total Power", "Vibration",
                      "Weibull Data Set", "Weibull File",
                      "Year of Manufacture", "Hazard Rate Model",
                      "Reliability Goal Measure", "Reliability Goal",
                      "MTBF LCL", "MTBF UCL", "h(t) LCL", "h(t) UCL"]

        for i in range(len(_db_fields)):
            model.append([i, _db_fields[i], ""])

        self.assistant.append_page(scrollwindow)
        self.assistant.set_page_type(scrollwindow, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(scrollwindow,
                                      _(u"Select Fields to Import"))
        self.assistant.set_page_complete(scrollwindow, True)

# Create the page to apply the import criteria.
        fixed = gtk.Fixed()
        _text_ = _(u"Press 'Apply' to import the requested data or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed,
                                     gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(fixed, _(u"Import Data"))
        self.assistant.set_page_complete(fixed, True)

        self.assistant.show_all()

    def _callback_combo_cell(self, cell, path, row, position, treemodel):
        """
        Called whenever a TreeView CellRendererCombo changes.

        Keyword Arguments:
        cell      -- the gtk.CellRendererCombo that called this function
        path      -- the path in the gtk.TreeView containing the
                     gtk.CellRendererCombo that called this function.
        row       -- the new gtk.TreeIter in the gtk.CellRendererCombo that
                     called this function.
        position  -- the position of in the gtk.TreeView of the
                     gtk.CellRendererCombo that called this function.
        treemodel -- the gtk.TreeModel for the gtk.TreeView.
        lastcol   -- the index of the last visible column in the
                     gtk.TreeView.
        """

        model = cell.get_property('model')
        _text = model.get_value(row, 0)
        _index  = model.get_value(row, 1)

        treerow = treemodel.get_iter(path)

        _position = treemodel.get_value(treerow, 0)
        self._file_index.insert(_position, _index)

        treemodel.set_value(treerow, position, _text)

        return False

    def _forward_page_select(self, current_page):

        if(current_page == 0):
            self._select_source_file()
        else:
            self.assistant.set_current_page(current_page + 1)

    def _select_source_file(self):

        import os

        # Get the user's selected file and write the results.
        dialog = gtk.FileChooserDialog(_(u"RelKit: Import Hardware from File ..."),
                                       None,
                                       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                        gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        dialog.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)

        # Set some filters to select all files or only some text files.
        filter = gtk.FileFilter()
        filter.set_name(u"All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("Text Files (csv, txt)")
        filter.add_mime_type("text/csv")
        filter.add_mime_type("text/txt")
        filter.add_mime_type("application/xls")
        filter.add_pattern("*.csv")
        filter.add_pattern("*.txt")
        filter.add_pattern("*.xls")
        dialog.add_filter(filter)

        # Run the dialog and write the file.
        _contents = []
        response = dialog.run()
        if(response == gtk.RESPONSE_ACCEPT):
            _filename = dialog.get_filename()
            (name, extension) = os.path.splitext(_filename)

            _file = open(_filename, 'r')

            for _line in _file:
                _contents.append([_line.rstrip('\n')])

            _headers = str(_contents[0][0]).rsplit('\t')
            for i in range(len(_contents) - 1):
                _contents[i] = str(_contents[i + 1][0]).rsplit('\t')
        else:
            _headers = []

        dialog.destroy()

        return(_headers, _contents)

    def _import(self, button):
        """
        Method to perform the import from an external file to the database.

        Keyword Arguments:
        button -- the gtk.Button widget that called this method.
        """

        from datetime import datetime

        model = self.tvwFileFields.get_model()
        row = model.get_iter_root()

# Find the number of existing hardware items.
        if(_conf.BACKEND == 'mysql'):
            query = "SELECT COUNT(*) FROM tbl_system"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT COALESCE(MAX(fld_assembly_id)+1, 0) FROM tbl_system"

        num_assemblies = self._app.DB.execute_query(query,
                                                    None,
                                                    self._app.ProgCnx)

        contents = []

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
                _temp[i] = self._missing_to_default(_temp[i], 0)

            for i in [10, 16, 35, 42, 56, 67, 85]:
                _temp[i] = self._missing_to_default(_temp[i], 1)

            _temp[87] = self._missing_to_default(_temp[87], 2013)

            # Convert missing float values to correct default value.
            for i in [2, 5, 13, 14, 15, 18, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                      34, 39, 40, 44, 46, 48, 49, 50, 51, 52, 54, 55, 65, 66,
                      73, 74, 76, 83, 84, 91, 92, 93, 94]:
                _temp[i] = self._missing_to_default(_temp[i], 0.0)

            for i in [7, 8, 53, 57, 69, 70, 90]:
                _temp[i] = self._missing_to_default(_temp[i], 1.0)

            for i in [80, 81]:
                _temp[i] = self._missing_to_default(_temp[i], 30.0)

            _temp[37] = self._missing_to_default(_temp[37], 50.0)

            for i in [19, 20, 45]:
                _temp[i] = self._missing_to_default(_temp[i], 100.0)

            contents.append(_temp)

# Find the top-level assembly and use it to update the top-level record in the
# database.
        _root = [assembly for assembly in contents if assembly[62] == '-'][0]

        _values_ = (int(_root[0]), 0, float(_root[2]), int(_root[3]),
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

        _query_ = "UPDATE tbl_system \
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
                   WHERE fld_parent_assembly='-'" % _values_
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        # Now find all the children of the top-level assembly.
        _iter_ = {0:'-'}
        j = 0
        _root = [child for child in contents if child[62] == str(j)]
        _iter_ = self._add_children(_root, _iter_, contents)

        self._app.HARDWARE.load_tree()

        return False

    def _add_children(self, _root, _iter_, contents):

        for i in range(len(_root)):
            _parent_id_ = int(_root[i][62])
            if(str(_iter_[_parent_id_]) == '-'):
                _iter_[int(_root[i][1])] = '0:' + str(i)
                _root[i][62] = '0'
            else:
                _iter_[int(_root[i][1])] = str(_iter_[_parent_id_]) + ':' + str(i)
                _root[i][62] = str(_iter_[_parent_id_])


            try:
                _values_ = (int(_root[i][0]), int(_root[i][1]),
                            float(_root[i][2]), int(_root[i][3]),
                            str(_root[i][4]), float(_root[i][5]),
                            str(_root[i][6]), float(_root[i][7]),
                            float(_root[i][8]), str(_root[i][9]),
                            int(_root[i][10]), int(_root[i][11]),
                            str(_root[i][12]), float(_root[i][13]),
                            float(_root[i][14]), float(_root[i][15]),
                            int(_root[i][16]), str(_root[i][17]),
                            float(_root[i][18]), float(_root[i][19]),
                            float(_root[i][20]), str(_root[i][21]),
                            int(_root[i][22]), int(_root[i][23]),
                            int(_root[i][24]), float(_root[i][25]),
                            float(_root[i][26]), float(_root[i][27]),
                            float(_root[i][28]), float(_root[i][29]),
                            float(_root[i][30]), float(_root[i][31]),
                            float(_root[i][32]), float(_root[i][33]),
                            float(_root[i][34]), int(_root[i][35]),
                            str(_root[i][36]), float(_root[i][37]),
                            str(_root[i][38]), float(_root[i][39]),
                            float(_root[i][40]), str(_root[i][41]),
                            int(_root[i][42]), int(_root[i][43]),
                            float(_root[i][44]), float(_root[i][45]),
                            float(_root[i][46]), str(_root[i][47]),
                            float(_root[i][48]), float(_root[i][49]),
                            float(_root[i][50]), float(_root[i][51]),
                            float(_root[i][52]), float(_root[i][53]),
                            float(_root[i][54]), float(_root[i][55]),
                            int(_root[i][56]), float(_root[i][57]),
                            str(_root[i][58]), str(_root[i][59]),
                            int(_root[i][60]), str(_root[i][61]),
                            str(_root[i][62]), int(_root[i][63]),
                            str(_root[i][64]), float(_root[i][65]),
                            float(_root[i][66]), int(_root[i][67]),
                            str(_root[i][68]), float(_root[i][69]),
                            float(_root[i][70]), str(_root[i][71]),
                            int(_root[i][72]), float(_root[i][73]),
                            float(_root[i][74]), int(_root[i][75]),
                            float(_root[i][76]), str(_root[i][77]),
                            int(_root[i][78]), int(_root[i][79]),
                            float(_root[i][80]), float(_root[i][81]),
                            int(_root[i][82]), float(_root[i][83]),
                            float(_root[i][84]), int(_root[i][85]),
                            str(_root[i][86]), int(_root[i][87]),
                            str(_root[i][88]), int(_root[i][89]),
                            float(_root[i][90]), float(_root[i][91]),
                            float(_root[i][92]), float(_root[i][93]),
                            float(_root[i][94]))

                _query_ = "INSERT INTO tbl_system \
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
                                   %f, %f, %f, %f, %f)" % _values_
                _results_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx,
                                                       commit=True)

            except:
                # If there is a problem with the input data, don't import
                # the record.
                self._app.import_log.error("Failed to import record: %d" % _root[i][1])

            # Now add the new hardware to the allocation table, the risk
            # analysis table, the similar items table, the FMECA table and
            # the functional matrix table.
            try:
                _values_ = (int(_root[i][0]), int(_root[i][1]))
                _query_ = "INSERT INTO tbl_allocation \
                           (fld_revision_id, fld_assembly_id) \
                           VALUES (%d, %d)" % _values_
                _results_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx,
                                                       commit=True)

                _query_ = "INSERT INTO tbl_risk_analysis \
                           (fld_revision_id, fld_assembly_id) \
                           VALUES (%d, %d)" % _values_
                _results_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx,
                                                       commit=True)

                _query_ = "INSERT INTO tbl_similar_item \
                           (fld_revision_id, fld_assembly_id) \
                           VALUES (%d, %d)" % _values_
                _results_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx,
                                                       commit=True)

                _query_ = "INSERT INTO tbl_fmeca \
                           (fld_revision_id, fld_assembly_id) \
                           VALUES (%d, %d)" % _values_
                _results_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx,
                                                       commit=True)

                _query_ = "INSERT INTO tbl_functional_matrix \
                           (fld_revision_id, fld_assembly_id) \
                           VALUES(%d, %d)" % _values_
                _results_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx,
                                                       commit=True)

            except ValueError:
            # If there is a problem with the input data, don't import the
            # record.
                self._app.import_log.error("Failed to import record: %d to the Allocation, Risk Analysis, or Similar Item Table" % _root[i][1])

            _children_ = [child for child in contents if child[62] == _root[i][1]]
            if(len(_children_) > 0):
                _iter_ = self._add_children(_children_, _iter_, contents)

        return(_iter_)

    def _missing_to_default(self, field, default_value):

        if(field == ''):
            field = default_value

        return(field)

    def _cancel(self, button):
        """
        Method to destroy the gtk.Assistant when the 'Cancel' button is
        pressed.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        self.assistant.destroy()


class ImportIncident:
    """
    This is the gtk.Assistant that walks the user through the process of
    importing program incident records to the open RelKit Program database.
    """

    def __init__(self, button, app):
        """
        Initialize an instance of the Import Incident Assistant.

        Keyword Arguments:
        button -- the gtk.Button widget that calling this Assistant.
        app    -- the instance of the RelKit application calling the Assistant.
        """

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_("RelKit Import Incidents Assistant"))
        self.assistant.connect('apply', self._import)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

# Initialize some variables.
        self._file_index = [-1] * 76

# Create the introduction page.
        fixed = gtk.Fixed()
        _text_ = _("This is the RelKit incident import assistant.  It will help you import program incidents to the database from external files.  Press 'Forward' to continue or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(fixed, _("Introduction"))
        self.assistant.set_page_complete(fixed, True)

# Create the gtk.TreeView to map input file fields to database fields.
        model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                              gobject.TYPE_STRING)
        self.tvwFileFields = gtk.TreeView(model)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwFileFields)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        column.set_resizable(True)
        column.set_visible(False)
        self.tvwFileFields.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, text=1)
        column.set_resizable(True)
        label = gtk.Label(column.get_title())
        label.set_line_wrap(True)
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_markup("<span weight='bold'>%s</span>" % _("Database\nField"))
        label.show_all()
        column.set_widget(label)
        self.tvwFileFields.append_column(column)

        cell = gtk.CellRendererCombo()
        cellmodel = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT)
        (_file_fields, self._file_contents) = self._select_source_file()
        cellmodel.append(["", -1])
        for i in range(len(_file_fields)):
            cellmodel.append([_file_fields[i], i])

        cell.set_property('editable', 1)
        cell.set_property('has-entry', False)
        cell.set_property('model', cellmodel)
        cell.set_property('text-column', 0)

        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, text=2)
        column.set_resizable(True)
        label = gtk.Label(column.get_title())
        label.set_line_wrap(True)
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_markup("<span weight='bold'>%s</span>" % _("File\nField"))
        label.show_all()
        column.set_widget(label)
        self.tvwFileFields.append_column(column)

        cell.connect('changed', self._callback_combo_cell, 2, model)

        _db_fields = ["Revision ID", "Incident ID", "Incident Category",
                      "Incident Type", "Short Description", "Long Description",
                      "Criticality", "Detection Method", "Remarks", "Status",
                      "Found During Test", "Found During Test Case",
                      "Execution Time", "Affected Unit", "Incident Cost",
                      "Incident Age", "Hardware ID", "Software ID",
                      "Requested By", "Request Date", "Reviewed",
                      "Reviewed By", "Reviewed Date", "Approved",
                      "Approved By", "Approved Date", "Closed",
                      "Closed By", "Closed Date", "Life Cycle", "Analysis",
                      "Accepted", "Part Number", "Age at Incident", "Failure",
                      "Suspension", "No Fault Found", "Out of Calibration",
                      "Initial Installation", "Interval Censored"]

        for i in range(len(_db_fields)):
            model.append([i, _db_fields[i], ""])

        self.assistant.append_page(scrollwindow)
        self.assistant.set_page_type(scrollwindow, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(scrollwindow,
                                      _("Select Fields to Import"))
        self.assistant.set_page_complete(scrollwindow, True)

# Create the page to apply the import criteria.
        fixed = gtk.Fixed()
        _text_ = _("Press 'Apply' to import the requested data or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed,
                                     gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(fixed, _("Import Data"))
        self.assistant.set_page_complete(fixed, True)

        self.assistant.show_all()

    def _callback_combo_cell(self, cell, path, row, position, treemodel):
        """
        Called whenever a TreeView CellRendererCombo changes.

        Keyword Arguments:
        cell      -- the gtk.CellRendererCombo that called this function
        path      -- the path in the gtk.TreeView containing the
                     gtk.CellRendererCombo that called this function.
        row       -- the new gtk.TreeIter in the gtk.CellRendererCombo that
                     called this function.
        position  -- the position of in the gtk.TreeView of the
                     gtk.CellRendererCombo that called this function.
        treemodel -- the gtk.TreeModel for the gtk.TreeView.
        lastcol   -- the index of the last visible column in the
                     gtk.TreeView.
        """

        model = cell.get_property('model')
        _text = model.get_value(row, 0)
        _index  = model.get_value(row, 1)

        treerow = treemodel.get_iter(path)

        _position = treemodel.get_value(treerow, 0)
        self._file_index.insert(_position, _index)

        treemodel.set_value(treerow, position, _text)

        return False

    def _forward_page_select(self, current_page):

        if(current_page == 0):
            self._select_source_file()
        else:
            self.assistant.set_current_page(current_page + 1)

    def _select_source_file(self):

        import os

        # Get the user's selected file and write the results.
        dialog = gtk.FileChooserDialog(_("RelKit: Import Incidents from File ..."),
                                       None,
                                       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                        gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        dialog.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)

        # Set some filters to select all files or only some text files.
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("Text Files (csv, txt)")
        filter.add_mime_type("text/csv")
        filter.add_mime_type("text/txt")
        filter.add_mime_type("application/xls")
        filter.add_pattern("*.csv")
        filter.add_pattern("*.txt")
        filter.add_pattern("*.xls")
        dialog.add_filter(filter)

        # Run the dialog and write the file.
        response = dialog.run()
        if(response == gtk.RESPONSE_ACCEPT):
            _filename = dialog.get_filename()
            (name, extension) = os.path.splitext(_filename)

        dialog.destroy()

        _contents = []
        _file = open(_filename, 'r')

        for _line in _file:
            _contents.append([_line])

        _headers = str(_contents[0][0]).rsplit('\t')
        for i in range(len(_contents) - 1):
            _contents[i] = str(_contents[i + 1][0]).rsplit('\t')

        return(_headers, _contents)

    def _import(self, button):
        """
        Method to perform the import from an external file to the database.

        Keyword Arguments:
        button -- the gtk.Button widget that called this method.
        """

        from datetime import datetime

        window = self.assistant.get_root_window()
        window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))

        model = self.tvwFileFields.get_model()
        row = model.get_iter_root()

        # Find the number of 6existing incidents.
        if(_conf.BACKEND == 'mysql'):
            query = "SELECT COUNT(*) FROM tbl_incident"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT COALESCE(MAX(fld_incident_id)+1, 0) FROM tbl_incident"

        num_incidents = self._app.DB.execute_query(query,
                                                   None,
                                                   self._app.ProgCnx)

        for i in range(len(self._file_contents) - 1):
            contents = []

            for j in range(len(self._file_index)):
                if self._file_index[j] == -1:
                    contents.append('')
                else:
                    try:
                        contents.append(self._file_contents[i][self._file_index[j]])
                    except IndexError:
                        contents.append('')

            contents[14] = contents[14].lstrip('$')

            # Convert all the date fields to ordinal dates.
            contents[19] = _util.date_to_ordinal(contents[19])
            contents[22] = _util.date_to_ordinal(contents[22])
            contents[25] = _util.date_to_ordinal(contents[25])
            contents[28] = _util.date_to_ordinal(contents[28])

            # Convert all the True/False fields to integer.
            contents[31] = _util.string_to_boolean(contents[31])
            contents[34] = _util.string_to_boolean(contents[34])
            contents[35] = _util.string_to_boolean(contents[35])
            contents[36] = _util.string_to_boolean(contents[36])
            contents[37] = _util.string_to_boolean(contents[37])
            contents[38] = _util.string_to_boolean(contents[38])
            contents[39] = _util.string_to_boolean(contents[39])
            contents[40] = _util.string_to_boolean(contents[40])
            contents[41] = _util.string_to_boolean(contents[41])

            # Convert missing values to correct default value.
            contents[0] = self._missing_to_default(contents[0], 0)
            contents[2] = self._missing_to_default(contents[2], 0)
            contents[3] = self._missing_to_default(contents[3], 0)
            contents[6] = self._missing_to_default(contents[6], 1)
            contents[9] = self._missing_to_default(contents[9], 0)
            contents[12] = self._missing_to_default(contents[12], 0.0)
            contents[14] = self._missing_to_default(contents[14], 0.0)
            contents[15] = self._missing_to_default(contents[15], 0)
            contents[16] = self._missing_to_default(contents[16], -1)
            contents[17] = self._missing_to_default(contents[17], -1)
            contents[18] = self._missing_to_default(contents[18], 0)
            contents[20] = self._missing_to_default(contents[20], 0)
            contents[21] = self._missing_to_default(contents[21], 0)
            contents[23] = self._missing_to_default(contents[23], 0)
            contents[24] = self._missing_to_default(contents[24], 0)
            contents[26] = self._missing_to_default(contents[26], 0)
            contents[27] = self._missing_to_default(contents[27], 0)
            contents[28] = self._missing_to_default(contents[28], 0)
            contents[29] = self._missing_to_default(contents[29], 0)
            contents[42] = self._missing_to_default(contents[42], 0.0)

            if(contents[1] == 0 or contents[1] is None or contents[1] == ''):
                contents[1] = num_incidents[0][0] + i + 1

            try:
                values = (int(contents[0]), int(contents[1]), int(contents[2]),
                          int(contents[3]), contents[4], contents[5],
                          int(contents[6]), contents[7], contents[8],
                          int(contents[9]), contents[10], contents[11],
                          float(contents[12]), contents[13],
                          float(contents[14]), int(contents[15]),
                          int(contents[16]), int(contents[17]), contents[18],
                          int(contents[19]), int(contents[20]),
                          contents[21], int(contents[22]), int(contents[23]),
                          contents[24], int(contents[25]), int(contents[26]),
                          contents[27], int(contents[28]), int(contents[29]),
                          contents[30], int(contents[31]))

                if(_conf.BACKEND == 'mysql'):
                    query = "INSERT INTO tbl_incident \
                             VALUES (%d, %d, %d, %d, '%s', '%s', %d, '%s', '%s', \
                                     %d, '%s', '%s', %f, '%s', %f, %d, %d, %d, \
                                     %d, '%s', %d, %d, '%s', %d, %d, '%s', %d, \
                                     %d, '%s', %d, '%s', %d)"
                elif(_conf.BACKEND == 'sqlite3'):
                    query = "INSERT INTO tbl_incident \
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                     ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                     ?, ?)"

                results = self._app.DB.execute_query(query,
                                                     values,
                                                     self._app.ProgCnx,
                                                     commit=True)

            except ValueError:
                self._app.import_log.error("Failed to import record %d into tbl_incident" % contents[1])
                #self._app.import_log.error(contents)

            try:
                values = (str(contents[1]), str(contents[32]),
                          float(contents[33]), int(contents[34]),
                          int(contents[35]), int(contents[36]),
                          int(contents[37]), int(contents[38]),
                          int(contents[39]), int(contents[40]),
                          int(contents[41]), float(contents[42]), 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

                if(_conf.BACKEND == 'mysql'):
                    query = "INSERT INTO tbl_incident_detail \
                             VALUES ('%s', '%s', %f, %d, %d, %d, %d, %d, %d, \
                                     %d, %d, %f, %d, %d, %d, %d, %d, %d, %d, \
                                     %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                                     %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, \
                                     %d, %d, %d, %d, %d, %d)"
                elif(_conf.BACKEND == 'sqlite3'):
                    query = "INSERT INTO tbl_incident_detail \
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                     ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                     ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                     ?, ?, ?, ?, ?, ?)"

                results = self._app.DB.execute_query(query,
                                                     values,
                                                     self._app.ProgCnx,
                                                     commit=True)

            except ValueError:
                self._app.import_log.error("Failed to import record %d into tbl_incident_detail" % contents[1])

        # Load the INCIDENT treeview with the newly imported records.
        values = (self._app.REVISION.revision_id, )
        if(_conf.BACKEND == 'mysql'):
            query = "SELECT * FROM tbl_incident\
                     WHERE fld_revision_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT * FROM tbl_incident\
                     WHERE fld_revision_id=?"

        window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

        self._app.INCIDENT.load_tree(query, values)

        return False

    def _missing_to_default(self, field, default_value):

        if(field == ''):
            field = default_value

        return(field)

    def _cancel(self, button):
        """
        Method to destroy the gtk.Assistant when the 'Cancel' button is
        pressed.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        self.assistant.destroy()
