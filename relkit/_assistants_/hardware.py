#!/usr/bin/env python

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2012 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       hardware.py is part of The RelKit Project
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

    def __init__(self, button, app):

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_("RelKit Import Hardware Assistant"))
        self.assistant.connect('apply', self._import)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

# Initialize some variables.
        self._file_index = [-1] * 92

# Create the introduction page.
        fixed = gtk.Fixed()
        _text_ = _("This is the RelKit hardware import assistant.  It will help you import system hardware information to the database from external files.  Press 'Forward' to continue or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(fixed, _("Introduction"))
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
                      "Reliability Goal Measure", "Reliability Goal"]

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
        dialog = gtk.FileChooserDialog(_("RelKit: Import Hardware from File ..."),
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

        model = self.tvwFileFields.get_model()
        row = model.get_iter_root()

        # Find the number ofexisting incidents.
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
                        _temp.append(self._file_contents[i][self._file_index[j]].rstrip('\n'))
                    except IndexError:
                        _temp.append('')

            # Convert missing integer values to correct default value.
            for i in [0, 1, 3, 5, 11, 22, 23, 24, 43, 60,
                      63, 67, 72, 75, 78, 79, 82, 89]:
                _temp[i] = self._missing_to_default(_temp[i], 0)

            for i in [10, 16, 35, 42, 56, 68, 85]:
                _temp[i] = self._missing_to_default(_temp[i], 1)

            _temp[87] = self._missing_to_default(_temp[87], 2012)

            # Convert missing float values to correct default value.
            for i in [2, 5, 13, 14, 15, 18, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                      34, 39, 40, 44, 46, 48, 49, 50, 51, 52, 54, 55, 65, 66,
                      73, 74, 76, 83, 84]:
                _temp[i] = self._missing_to_default(_temp[i], 0.0)

            for i in [7, 8, 53, 57, 69, 70, 90]:
                _temp[i] = self._missing_to_default(_temp[i], 1.0)

            for i in [80, 81]:
                _temp[i] = self._missing_to_default(_temp[i], 30.0)

            _temp[37] = self._missing_to_default(_temp[37], 50.0)

            for i in [19, 20, 45]:
                _temp[i] = self._missing_to_default(_temp[i], 100.0)

            contents.append(_temp)

        # Find the top-level assembly and use it to update the top-level
        # record in the database.
        _root = [assembly for assembly in contents if assembly[62] == '-'][0]

        values = (int(_root[0]), 0, float(_root[2]), int(_root[3]),
                  str(_root[4]), float(_root[5]), str(_root[6]),
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
                  str(_root[88]), int(_root[89]), float(_root[90]))

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_system \
                     SET fld_revision_id=%d, fld_assembly_id=%d, \
                         fld_add_adj_factor=%f, fld_allocation_type=%d, \
                         fld_alt_part_number='%s', \
                         fld_assembly_criticality=%f, \
                         fld_attachments='%s', fld_availability=%f, \
                         fld_availability_mission=%f, fld_cage_code='%s', \
                         fld_calculation_model=%d, fld_category_id=%d, \
                         fld_cost=%f, fld_comp_ref_des='%s', \
                         fld_cost_failure=%f, fld_cost_hour=%f, \
                         fld_cost_type=%d, \
                         fld_description='%s', fld_detection_fr=%f, \
                         fld_detection_percent=%f, fld_duty_cycle=%f, \
                         fld_entered_by='%s', fld_environment_active=%d, \
                         fld_environment_dormant=%d, fld_failure_dist=%d, \
                         fld_failure_parameter_1=%f, \
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
                         fld_reliability_goal=%f \
                     WHERE fld_parent_assembly='-'"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_system \
                     SET fld_revision_id=?, fld_assembly_id=?, \
                         fld_add_adj_factor=?, fld_allocation_type=?, \
                         fld_alt_part_number=?, \
                         fld_assembly_criticality=?, \
                         fld_attachments=?, fld_availability=?, \
                         fld_availability_mission=?, fld_cage_code=?, \
                         fld_calculation_model=?, fld_category_id=?, \
                         fld_comp_ref_des=?, fld_cost=?, fld_cost_failure=?, \
                         fld_cost_hour=?, fld_cost_type=?, \
                         fld_description=?, fld_detection_fr=?, \
                         fld_detection_percent=?, fld_duty_cycle=?, \
                         fld_entered_by=?, fld_environment_active=?, \
                         fld_environment_dormant=?, fld_failure_dist=?, \
                         fld_failure_parameter_1=?, \
                         fld_failure_parameter_2=?, \
                         fld_failure_parameter_3=?, \
                         fld_failure_rate_active=?, \
                         fld_failure_rate_dormant=?, \
                         fld_failure_rate_mission=?, \
                         fld_failure_rate_percent=?, \
                         fld_failure_rate_predicted=?, \
                         fld_failure_rate_software=?, \
                         fld_failure_rate_specified=?, \
                         fld_failure_rate_type=?, fld_figure_number=?, \
                         fld_humidity=?, fld_image_file=?, \
                         fld_isolation_fr=?, fld_isolation_percent=?, \
                         fld_lcn=?, fld_level=?, fld_manufacturer=?, \
                         fld_mcmt=?, fld_mission_time=?, fld_mmt=?, \
                         fld_modified_by=?, fld_mpmt=?, \
                         fld_mtbf_mission=?, fld_mtbf_predicted=?, \
                         fld_mtbf_specified=?, fld_mttr=?, \
                         fld_mttr_add_adj_factor=?, \
                         fld_mttr_mult_adj_factor=?, \
                         fld_mttr_specified=?, fld_mttr_type=?, \
                         fld_mult_adj_factor=?, fld_name=?, \
                         fld_nsn=?, fld_overstress=?, \
                         fld_page_number=?, fld_parent_assembly=?, \
                         fld_part=?, fld_part_number=?, \
                         fld_percent_isolation_group_ri=?, \
                         fld_percent_isolation_single_ri=?, \
                         fld_quantity=?, fld_ref_des=?, \
                         fld_reliability_mission=?, \
                         fld_reliability_predicted=?, fld_remarks=?, \
                         fld_repair_dist=?, fld_repair_parameter_1=?, \
                         fld_repair_parameter_2=?, fld_repairable=?, \
                         fld_rpm=?, fld_specification_number=?, \
                         fld_subcategory_id=?, fld_tagged_part=?, \
                         fld_temperature_active=?, \
                         fld_temperature_dormant=?, \
                         fld_total_part_quantity=?, \
                         fld_total_power_dissipation=?, fld_vibration=?, \
                         fld_weibull_data_set=?, fld_weibull_file=?, \
                         fld_year_of_manufacture=?, fld_ht_model=?, \
                         fld_reliability_goal_measure=?, \
                         fld_reliability_goal=? \
                     WHERE fld_parent_assembly='-'"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        # Now find all the children of the top-level assembly.
        j = 0
        while len(_root) > 0:
            _root = [assembly for assembly in contents if assembly[62] == str(j)]

            for i in range(len(_root)):

                # Build the parent assembly path.
                if(_root[i][62] != '0'):
                    _root[i][62] = int(_root[i][62]) - 1
                    _root[i][62] = '0:' + str(_root[i][62])

                try:
                    values = (int(_root[i][0]), int(_root[i][1]),
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
                              float(_root[i][90]))

                    if(_conf.BACKEND == 'mysql'):
                        query = "INSERT INTO tbl_system \
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
                                         %d, %f, %f, %d, '%s', %d, '%s', %d, %f)"
                    elif(_conf.BACKEND == 'sqlite3'):
                        query = "INSERT INTO tbl_system \
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                         ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                         ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                         ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                         ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                         ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                         ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                         ?, ?, ?, ?, ?, ?, ?)"

                    results = self._app.DB.execute_query(query,
                                                         values,
                                                         self._app.ProgCnx,
                                                         commit=True)

                except ValueError:
                # If there is a problem with the input data, don't import the
                # record.
                    self._app.import_log.error("Failed to import record: %d" % contents[i][1])

                # Now add the new hardware to the Allocation table and the
                # Similar Items table.
                try:
                    values = (int(_root[i][0]), int(_root[i][1]))

                    if(_conf.BACKEND == 'mysql'):
                        query = "INSERT INTO tbl_allocation \
                                 (fld_revision_id, fld_assembly_id) \
                                 VALUES (%d, %d)"
                    elif(_conf.BACKEND == 'sqlite3'):
                        query = "INSERT INTO tbl_allocation \
                                 (fld_revision_id, fld_assembly_id) \
                                 VALUES (?, ?)"

                    results = self._app.DB.execute_query(query,
                                                         values,
                                                         self._app.ProgCnx,
                                                         commit=True)

                    if(_conf.BACKEND == 'mysql'):
                        query = "INSERT INTO tbl_risk_analysis \
                                 (fld_revision_id, fld_assembly_id) \
                                 VALUES (%d, %d)"
                    elif(_conf.BACKEND == 'sqlite3'):
                        query = "INSERT INTO tbl_risk_analysis \
                                 (fld_revision_id, fld_assembly_id) \
                                 VALUES (?, ?)"

                    results = self._app.DB.execute_query(query,
                                                         values,
                                                         self._app.ProgCnx,
                                                         commit=True)

                    if(_conf.BACKEND == 'mysql'):
                        query = "INSERT INTO tbl_similar_item \
                                 (fld_revision_id, fld_assembly_id) \
                                 VALUES (%d, %d)"
                    elif(_conf.BACKEND == 'sqlite3'):
                        query = "INSERT INTO tbl_similar_item \
                                 (fld_revision_id, fld_assembly_id) \
                                 VALUES (?, ?)"

                    results = self._app.DB.execute_query(query,
                                                         values,
                                                         self._app.ProgCnx,
                                                         commit=True)
                except ValueError:
                # If there is a problem with the input data, don't import the
                # record.
                    self._app.import_log.error("Failed to import record: %d to the Allocation, Risk Analysis, or Similar Item Table" % contents[i][1])

            j += 1

        self._app.HARDWARE.load_tree()

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


class ExportHardware:

    def __init__(self, button, app):

        from lxml import etree

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_("RelKit Export Hardware Assistant"))
        self.assistant.connect('apply', self._export)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

# Create the introduction page.
        fixed = gtk.Fixed()
        _text_ = _("This is the RelKit hardware export assistant.  It will help you export the hardware structure from the database to an external file.  Press 'Forward' to continue or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(fixed, _("Introduction"))
        self.assistant.set_page_complete(fixed, True)

# Create the page to select the fields for exporting.
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                              gobject.TYPE_BOOLEAN)
        self.tvwDatabaseFields = gtk.TreeView(model)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwDatabaseFields)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        label = gtk.Label(column.get_title())
        label.set_line_wrap(True)
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_markup("<span weight='bold'>%s</span>" % _("Database\nField"))
        label.show_all()
        column.set_widget(label)
        self.tvwDatabaseFields.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._field_selected, None, 2, model)
        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, active=2)
        label = gtk.Label(column.get_title())
        label.set_line_wrap(True)
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_markup("<span weight='bold'>%s</span>" % _("Select to\nExport"))
        label.show_all()
        column.set_widget(label)
        self.tvwDatabaseFields.append_column(column)

        # Retrieve the column heading text from the format file.
        path = "/root/tree[@name='Hardware']/column/usertitle"
        heading = etree.parse(_conf.RELIAFREE_FORMAT_FILE[3]).xpath(path)

        # Retrieve the column position from the format file.
        path = "/root/tree[@name='Hardware']/column/position"
        position = etree.parse(_conf.RELIAFREE_FORMAT_FILE[3]).xpath(path)

        for i in range(int(len(heading))):
            data = [heading[i].text, int(position[i].text), 0]
            model.append(data)

        self.assistant.append_page(scrollwindow)
        self.assistant.set_page_type(scrollwindow, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(scrollwindow,
                                      _("Select Fields to Export"))
        self.assistant.set_page_complete(scrollwindow, True)

# Create the page to apply the export criteria.
        fixed = gtk.Fixed()
        _text_ = _("Press 'Apply' to export the requested data or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed,
                                     gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(fixed, _("Export Data"))
        self.assistant.set_page_complete(fixed, True)

        self.assistant.show_all()

    def _field_selected(self, cell, path, new_text, position, model):
        """
        Called whenever a TreeView CellRenderer is edited.

        Keyword Arguments:
        cell     -- the CellRenderer that was edited.
        path     -- the TreeView path of the CellRenderer that was edited.
        new_text -- the new text in the edited CellRenderer.
        position -- the column position of the edited CellRenderer.
        model    -- the TreeModel the CellRenderer belongs to.
        """

        convert = gobject.type_name(model.get_column_type(position))

        model[path][position] = not cell.get_active()

        return False

    def _export(self, button):
        """
        Method to export the data when the 'Apply' button is pressed.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        import csv

        _export_fields = []
        _headings = []

        # Get the gtk.TreeModel and the first row of the gtk.TreeView with the
        # list of fields available for exporting.
        model = self.tvwDatabaseFields.get_model()
        row = model.get_iter_first()

        # Iterate through the gtk.TreeModel to find the rows the user would
        # like to export.
        while row is not None:
            field = model.get_value(row, 1) # Index.
            use = model.get_value(row, 2)   # Boolean use or not use.
            if use:
                _export_fields.append(field)
                _headings.append(model.get_value(row, 0))
            row = model.iter_next(row)

        # Get the gtk.TreeModel and first row for the HARDWARE Object.
        model = self._app.HARDWARE.model
        row = model.get_iter_first()

        # Iterate through the HARDWARE object gtk.TreeModel to get the values
        # the user has specified.
        results = self._get_values(model, row, _export_fields)

        # Get the user's selected file and write the results.
        dialog = gtk.FileChooserDialog(_("RelKit: Export to File ..."),
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
        filter.add_pattern("*.csv")
        filter.add_pattern("*.txt")
        dialog.add_filter(filter)

        # Run the dialog and write the file.
        response = dialog.run()
        if(response == gtk.RESPONSE_ACCEPT):
            _filename = dialog.get_filename()
            dialog.destroy()
            _len = len(_filename)
            _ext = _filename[_len - 3:_len]
            if(_ext != 'csv' and _ext != 'txt'):
                _filename = _filename + '.txt'

            with open(_filename, 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter='\t',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(_headings)
                for i in range(len(results)):
                    writer.writerow(results[i])
        else:
            dialog.destroy()

    def _get_values(self, model, row, _index_):
        """
        Method to iteratively read the desired values for exporting.

        Keyword Arguments:
        model
        row
        _index_
        """

        results = []

        while row is not None:
            interim = []
            for i in range(len(_index_)):
                interim.append(model.get_value(row, _index_[i]))
            results.append(interim)
            if model.iter_has_child(row):
                row = model.iter_children(row)
                res = self._get_values(model, row, _index_)
                results = results + res
                row = model.iter_parent(row)

            row = model.iter_next(row)

        return(results)

    def _cancel(self, button):
        """
        Method to destroy the gtk.Assistant when the 'Cancel' button is
        pressed.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        self.assistant.destroy()
