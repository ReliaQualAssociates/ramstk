#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  import.py is part of The RTK Project
#
#  Copyright (C) 2013 Andrew Rowland <darowland@ieee.org>
#
# All rights reserved.

import os
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

# Add localization support.
import locale
import gettext
_ = gettext.gettext

# Import module to read Excel files.
import xlrd

# Import other RTK modules.
import Configuration as _conf
import gui.gtk.Widgets as _widg

class ImportAssistant:

    def __init__(self, widget, application):

        self._app = application

        # Create an assistant to guide the user through the import process.
        assistant = gtk.Assistant()
        assistant.set_title(_("RTK - Importing Data"))

        assistant.set_forward_page_func(self._set_next_page, assistant)
        assistant.connect('apply', self._apply)
        assistant.connect('cancel', self._cancel)

        vbox = gtk.VBox()
        vbox.set_name('Page1')
        vbox.set_border_width(5)
        page = assistant.append_page(vbox)
        assistant.set_page_title(vbox, _("RTK: Importing Data..."))
        assistant.set_page_type(vbox, gtk.ASSISTANT_PAGE_INTRO)
        label = gtk.Label(_("This assistant will guide you through the process of importing various types of data from an external source to the currently open RTK Program database."))
        label.set_line_wrap(True)
        vbox.pack_start(label, True, True, 0)
        assistant.set_page_complete(vbox, True)

        vbox = gtk.VBox()
        vbox.set_name('Page2')
        vbox.set_border_width(5)
        assistant.append_page(vbox)
        assistant.set_page_title(vbox, _("RTK: Select Type of Data to Import..."))
        assistant.set_page_type(vbox, gtk.ASSISTANT_PAGE_CONTENT)
        label = gtk.Label(_("Make a selection from the list below."))
        label.set_line_wrap(True)
        self.rdoFunctions = gtk.RadioButton(label=_("Functions"))
        self.rdoHardware1 = gtk.RadioButton(group=self.rdoFunctions, label=_("Hardware, BOM"))
        self.rdoHardware2 = gtk.RadioButton(group=self.rdoFunctions, label=_("Hardware, Flat List"))
        self.rdoRGIncidents = gtk.RadioButton(group=self.rdoFunctions, label=_("Reliability Growth Testing Incidents"))
        self.rdoBuildData = gtk.RadioButton(group=self.rdoFunctions, label=_("Build Data"))
        self.rdoFieldIncidents = gtk.RadioButton(group=self.rdoFunctions, label=_("Field Incidents"))
        vbox.pack_start(label, True, True, 0)
        vbox.pack_start(self.rdoFunctions, False, False, 0)
        self.rdoFunctions.set_sensitive(False)
        vbox.pack_start(self.rdoHardware1, False, False, 0)
        self.rdoHardware1.set_sensitive(False)
        vbox.pack_start(self.rdoHardware2, False, False, 0)
        vbox.pack_start(self.rdoRGIncidents, False, False, 0)
        self.rdoRGIncidents.set_sensitive(False)
        vbox.pack_start(self.rdoBuildData, False, False, 0)
        vbox.pack_start(self.rdoFieldIncidents, False, False, 0)
        assistant.set_page_complete(vbox, True)

        vbox = gtk.VBox()
        vbox.set_name('Page3')
        vbox.set_border_width(5)
        assistant.append_page(vbox)
        assistant.set_page_title(vbox, _("RTK: Import Data..."))
        assistant.set_page_type(vbox, gtk.ASSISTANT_PAGE_CONFIRM)
        label = gtk.Label(_("Select apply to begin data import..."))
        label.set_line_wrap(True)
        vbox.pack_start(label, True, True, 0)
        assistant.set_page_complete(vbox, True)

        assistant.show_all()

    def _hardware_data_select(self):

        """ Function to select the file containing the hardware data and
            associate the external file fields with the appropriate
            RTK Program database fields.
        """

        import xlrd

        if(self.rdoHardware1.get_active()):
            _title = _("RTK - Import Hardware from BOM")
        elif(self.rdoHardware2.get_active()):
            _title = _("RTK - Import Hardware from flat list")

        filechooser = gtk.FileChooserDialog(_title,
                                            buttons=(gtk.STOCK_CANCEL,
                                                     gtk.RESPONSE_REJECT,
                                                     gtk.STOCK_OK,
                                                     gtk.RESPONSE_ACCEPT))

        filechooser.set_default_response(gtk.RESPONSE_CANCEL)

        # TODO: Add support for importing data from other than Excel files.
        filter = gtk.FileFilter()
        filter.set_name(_("Hardware Files"))
        filter.add_mime_type('text/data')
        filter.add_mime_type('application/excel')
        filter.add_pattern('*.csv')
        #filter.add_pattern('*.dat')
        #filter.add_pattern('*.text')
        #filter.add_pattern('*.txt')
        filter.add_pattern('*.xls')
        filechooser.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name(_("All files"))
        filter.add_pattern('*')
        filechooser.add_filter(filter)

        response = filechooser.run()

        order = []
        sheet = ''
        if(response == gtk.RESPONSE_ACCEPT):
            infile = filechooser.get_filename()
            (name, extension) = os.path.splitext(infile)

            # Open the workbook and get a list of the worksheets.
            sheet = _select_worksheet(infile)
            filechooser.destroy()

            colnames = []
            for i in xrange(sheet.ncols):
                colnames.append(sheet.cell_value(0, i))

            # Display the list of columns in the selected worksheet.
            dialog = _widg.make_dialog(_title)

            hbox = gtk.HBox()

            model = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING)
            s_treeview = gtk.TreeView(model)

            column = gtk.TreeViewColumn()
            column.set_visible(False)
            s_treeview.append_column(column)
            cell = gtk.CellRendererText()
            cell.set_property('editable', False)
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', 0)
            column = gtk.TreeViewColumn(_("Column Heading"))
            s_treeview.append_column(column)
            cell.set_property('editable', False)
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', 1)

            for i in xrange(len(colnames)):
                row = model.append(None, [i, colnames[i]])

            scrollwindow = gtk.ScrolledWindow()
            w, h = gtk.gdk.get_default_root_window().get_size()
            scrollwindow.set_size_request((w / 6), (h / 5))
            scrollwindow.add(s_treeview)
            scrollwindow.show()
            s_treeview.show()
            hbox.pack_start(scrollwindow)

            button = _widg.make_button(width=80, image='assign')
            button.show()
            hbox.pack_start(button, expand=False)

            model = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_INT, gobject.TYPE_STRING)
            d_treeview = gtk.TreeView(model)

            column = gtk.TreeViewColumn(_("RTK Field"))
            d_treeview.append_column(column)
            cell = gtk.CellRendererText()
            cell.set_property('editable', False)
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', 0)
            column = gtk.TreeViewColumn(_("Source Index"))
            column.set_visible(False)
            d_treeview.append_column(column)
            cell = gtk.CellRendererText()
            cell.set_property('editable', False)
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', 1)
            column = gtk.TreeViewColumn(_("Source Field"))
            d_treeview.append_column(column)
            cell = gtk.CellRendererText()
            cell.set_property('editable', False)
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', 2)

            row = model.append(None, [_("Additive Adjustment Factor"), -1, ""])
            row = model.append(None, [_("Alternate Part Number"), -1, ""])
            row = model.append(None, [_("CAGE Code"), -1, ""])
            row = model.append(None, [_("Category"), -1, ""])
            row = model.append(None, [_("Cost"), -1, ""])
            row = model.append(None, [_("Description"), -1, ""])
            row = model.append(None, [_("Duty Cycle"), -1, ""])
            row = model.append(None, [_("Failure Rate, Specified"), -1, ""])
            row = model.append(None, [_("Figure Number"), -1, ""])
            row = model.append(None, [_("LCN"), -1, ""])
            row = model.append(None, [_("Level"), -1, ""])
            row = model.append(None, [_("Mission Time"), -1, ""])
            row = model.append(None, [_("MTBF, Specified"), -1, ""])
            row = model.append(None, [_("Multiplicative Adjustment Factor"), -1, ""])
            row = model.append(None, [_("Name"), -1, ""])
            row = model.append(None, [_("NSN"), -1, ""])
            row = model.append(None, [_("Page Number"), -1, ""])
            row = model.append(None, [_("Parent Assembly"), -1, ""])
            row = model.append(None, [_("Part"), -1, ""])
            row = model.append(None, [_("Part Number"), -1, ""])
            row = model.append(None, [_("Quantity"), -1, ""])
            row = model.append(None, [_("Reference Designator"), -1, ""])
            row = model.append(None, [_("Remarks"), -1, ""])
            row = model.append(None, [_("Specification Number"), -1, ""])
            row = model.append(None, [_("Subcategory"), -1, ""])
            row = model.append(None, [_("Temperature, Active"), -1, ""])
            row = model.append(None, [_("Temperature, Dormant"), -1, ""])
            row = model.append(None, [_("Year of Manufacture"), -1, ""])

            scrollwindow = gtk.ScrolledWindow()
            w, h = gtk.gdk.get_default_root_window().get_size()
            scrollwindow.set_size_request((w / 6), (h / 5))
            scrollwindow.add(d_treeview)
            scrollwindow.show()
            d_treeview.show()
            hbox.pack_start(scrollwindow)

            if(self.rdoHardware2.get_active()):
                fixed = gtk.Fixed()
                label = _widg.make_label(_("Add hardware to which assembly?"),
                                         height=50)
                fixed.put(label, 10, 10)
                self.cmbSystems = _widg.make_combo()
                fixed.put(self.cmbSystems, 10, 65)

                query = "SELECT fld_ref_des \
                         FROM tbl_system \
                         WHERE fld_part=0 \
                         AND fld_parent_assembly='0' \
                         AND fld_ref_des<>''"
                results = self._app.DB.execute_query(query,
                                                     None,
                                                     self._app.ProgCnx)
                _widg.load_combo(self.cmbSystems, results)

                fixed.show_all()
                hbox.pack_start(fixed)

            dialog.vbox.pack_start(hbox)
            hbox.show()

            button.connect('button-release-event', _set_import_order,
                           s_treeview, d_treeview)

            response = dialog.run()

            if(response == gtk.RESPONSE_ACCEPT):
                model = d_treeview.get_model()
                row = model.get_iter_root()
                while row is not None:
                    order.append(model.get_value(row, 1))
                    row = model.iter_next(row)

            dialog.destroy()

        else:
            filechooser.destroy()

        return(response, sheet, order)

    def _hardware_flat_data_import(self):

        """ This function imports hardware information in a flat list format
            from an external source to the program database.
        """

        from datetime import datetime

        if(_conf.RTK_MODULES[0] == 1):
            _revision = self._app.REVISION.revision_id
        else:
            _revision = 0

        _system = self.cmbSystems.get_active_text()

        if(self._response == gtk.RESPONSE_ACCEPT):
            _status = _("Importing Components to %s") % _system
            self._app.winTree.statusbar.push(2, _status)

            self._app.winTree.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            self._app.winWorkBook.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            self._app.winParts.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))

            # Find the path of the selected assembly to add the new components.
            path = self._app.HARDWARE._treepaths[_system]
            row = self._app.HARDWARE.model.get_iter(path)
            path = self._app.HARDWARE.model.get_string_from_iter(row)

            query = "BEGIN TRANSACTION"
            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx)

            for i in xrange(self._sheet.nrows - 1):
                data = []
                x = self._sheet.row_values(i + 1)[self._order[17]]

                # If the assembly code for the curent row of external data is
                # the same as the selected assembly code, import the current
                # row of external data.
                if(x.upper() == _system.upper()):
                    for j in range(len(self._order)):
                        value = self._sheet.row_values(i + 1)[self._order[j]]

                        if((j == 0 or j == 3 or j == 6 or j == 12) and
                           self._order[j] == -1):
                            data.append(0.0)

                        elif((j == 5 or j == 11) and self._order[j] == -1):
                            data.append(100.0)

                        elif(j == 13 and self._order[j] == -1):
                            data.append(1.0)

                        elif((j == 25 or j == 26) and self._order[j] == -1):
                            data.append(30.0)

                        elif((j == 2 or j == 7 or j == 24) and
                             self._order[j] == -1):
                            data.append(0)

                        elif((j == 10 or j == 18 or j == 20) and
                             self._order[j] == -1):
                            data.append(1)

                        elif(j == 27 and self._order[j] == -1):
                            data.append(2010)

                        elif((j == 1 or j == 4 or j == 8 or j == 9 or
                              j == 14 or j == 15 or j == 16 or j == 19 or
                              j == 21 or j == 22 or j == 23) and
                             self._order[j] == -1):
                            data.append('')

                        else:
                            data.append(value)

                    values = (_revision, data[0], data[1], data[2], data[3],
                              data[4], data[5], data[6], data[7], data[8],
                              data[9], data[10], data[11], data[12], data[13],
                              data[14], data[15], data[16], path, data[18],
                              data[19], data[20], data[21], data[22], data[23],
                              data[24], data[25], data[26], data[27])
                                    # Index     Value
                #    0      Additive Adjustment Factor (float)
                #    1          CAGE Code (text)
                #    2      Category (integer)
                #    3      Cost (float)
                #    4          Description (text)
                #    5      Duty Cycle (float)
                #    6      Failure Rate, Specified (float)
                #    7      Failure Rate Type (integer)
                #    8          Figure Number (text)
                #    9          LCN (text)
                #   10      Level(integer)
                #   11      Mission Time (float)
                #   12      MTBF, Specified (float)
                #   13      Multiplicative Adjustment Factor (float)
                #   14          Name (text)
                #   15          NSN (text)
                #   16          Page Number (text)
                #   17          Parent Assembly (text)
                #   18      Part (integer)
                #   19          Part Number (text)
                #   20      Quantity (integer)
                #   21          Reference Designator (text)
                #   22          Remarks (text)
                #   23          Specification Number (text)
                #   24      Subcategory (integer)
                #   25      Temperature, Active (float)
                #   26      Temperature, Dormant (float)
                #   27      Year of Manufacture (integer)
                    if(_conf.BACKEND == 'mysql'):
                        query = "INSERT INTO tbl_system \
                                 (fld_revision_id, fld_add_adj_factor, \
                                  fld_cage_code, fld_category_id, fld_cost, \
                                  fld_description, fld_duty_cycle, \
                                  fld_failure_rate_specified, \
                                  fld_failure_rate_type, fld_figure_number, \
                                  fld_lcn, fld_level, fld_mission_time, \
                                  fld_mtbf_specified, fld_mult_adj_factor, \
                                  fld_name, fld_nsn, fld_page_number, \
                                  fld_parent_assembly, fld_part, \
                                  fld_part_number, fld_quantity, fld_ref_des, \
                                  fld_remarks, fld_specification_number, \
                                  fld_subcategory_id, fld_temperature_active, \
                                  fld_temperature_dormant, \
                                  fld_year_of_manufacture) \
                                 VALUES \
                                 (%d, %f, '%s', %d, %f, '%s', %f, %f, %d, \
                                  '%s', '%s', %d, %f, %f, %f, '%s', '%s', \
                                  '%s', '%s', %d, '%s', %d, '%s', '%s', '%s', \
                                  %d, %f, %f, %d)"
                    elif(_conf.BACKEND == 'sqlite3'):
                        query = "INSERT INTO tbl_system \
                                 (fld_revision_id, fld_add_adj_factor, \
                                  fld_cage_code, fld_category_id, fld_cost, \
                                  fld_description, fld_duty_cycle, \
                                  fld_failure_rate_specified, \
                                  fld_failure_rate_type, fld_figure_number, \
                                  fld_lcn, fld_level, fld_mission_time, \
                                  fld_mtbf_specified, fld_mult_adj_factor, \
                                  fld_name, fld_nsn, fld_page_number, \
                                  fld_parent_assembly, fld_part, \
                                  fld_part_number, fld_quantity, fld_ref_des, \
                                  fld_remarks, fld_specification_number, \
                                  fld_subcategory_id, fld_temperature_active, \
                                  fld_temperature_dormant, \
                                  fld_year_of_manufacture) \
                                 VALUES \
                                 (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                  ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

                    results = self._app.DB.execute_query(query,
                                                         values,
                                                         self._app.ProgCnx,
                                                         commit=True)

                    if(_conf.BACKEND == 'mysql'):
                        query = "SELECT LAST_INSERT_ID()"
                    elif(_conf.BACKEND == 'sqlite3'):
                        query = "SELECT seq \
                                 FROM sqlite_sequence \
                                 WHERE name='tbl_system'"

                    _assembly_id = self._app.DB.execute_query(query,
                                                              None,
                                                              self._app.ProgCnx)

                    values = (_revision, _assembly_id[0][0])
                    if(_conf.BACKEND == 'mysql'):
                        query = "INSERT INTO tbl_prediction \
                                 (fld_revision_id, fld_assembly_id) \
                                 VALUES (%d, %d)"
                    elif(_conf.BACKEND == 'sqlite3'):
                        query = "INSERT INTO tbl_prediction \
                                 (fld_revision_id, fld_assembly_id) \
                                 VALUES (?, ?)"

                    results = self._app.DB.execute_query(query,
                                                         values,
                                                         self._app.ProgCnx,
                                                         commit=True)

                    if(_conf.BACKEND == 'mysql'):
                        query = "INSERT INTO tbl_functional_matrix \
                                 (fld_revision_id, fld_assembly_id) \
                                 VALUES(%d, %d)"
                    elif(_conf.BACKEND == 'sqlite3'):
                        query = "INSERT INTO tbl_functional_matrix \
                                 (fld_revision_id, fld_assembly_id) \
                                 VALUES(?, ?)"

                    results = self._app.DB.execute_query(query,
                                                         values,
                                                         self._app.ProgCnx,
                                                         commit=True)

                    if(_conf.BACKEND == 'mysql'):
                        query = "INSERT INTO tbl_fmeca_items \
                                 (fld_revision_id, fld_assembly_id) \
                                 VALUES (%d, %d)"
                    elif(_conf.BACKEND == 'sqlite3'):
                        query = "INSERT INTO tbl_fmeca_items \
                                 (fld_revision_id, fld_assembly_id) \
                                 VALUES (?, ?)"

                    #results = self._app.DB.execute_query(query,
                    #                                     values,
                    #                                     self._app.ProgCnx,
                    #                                     commit=True)

            query = "END TRANSACTION"
            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx)

            self._app.winTree.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
            self._app.winWorkBook.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
            self._app.winParts.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

            self._app.winTree.statusbar.pop(2)

        return False

    def _build_data_select(self):

        """ Function to select the file containing the build data and
            associate the external file fields with the appropriate
            RTK Program database fields.
        """

        import xlrd

        filechooser = gtk.FileChooserDialog(_("RTK - Import Units"),
                                            buttons=(gtk.STOCK_CANCEL,
                                                     gtk.RESPONSE_REJECT,
                                                     gtk.STOCK_OK,
                                                     gtk.RESPONSE_ACCEPT))

        filechooser.set_default_response(gtk.RESPONSE_CANCEL)

        filter = gtk.FileFilter()
        filter.set_name(_("Hardware Files"))
        filter.add_mime_type('text/data')
        filter.add_mime_type('application/excel')
        filter.add_pattern('*.csv')
        filter.add_pattern('*.dat')
        filter.add_pattern('*.text')
        filter.add_pattern('*.txt')
        filter.add_pattern('*.xls')
        filechooser.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name(_("All files"))
        filter.add_pattern('*')
        filechooser.add_filter(filter)

        response = filechooser.run()

        order = []
        sheet = ''
        if(response == gtk.RESPONSE_ACCEPT):
            infile = filechooser.get_filename()
            (name, extension) = os.path.splitext(infile)

            # Open the workbook and get a list of the worksheets.
            sheet = _select_worksheet(infile)
            filechooser.destroy()

            colnames = []
            for i in xrange(sheet.ncols):
                colnames.append(sheet.cell_value(0, i))

            # Display the list of columns in the selected worksheet.
            dialog = _widg.make_dialog(_("RTK - Import Units"))

            hbox = gtk.HBox()

            model = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING)
            s_treeview = gtk.TreeView(model)

            column = gtk.TreeViewColumn()
            column.set_visible(False)
            s_treeview.append_column(column)
            cell = gtk.CellRendererText()
            cell.set_property('editable', False)
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', 0)
            column = gtk.TreeViewColumn(_("Column Heading"))
            s_treeview.append_column(column)
            cell.set_property('editable', False)
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', 1)

            for i in xrange(len(colnames)):
                row = model.append(None, [i, colnames[i]])

            scrollwindow = gtk.ScrolledWindow()
            w, h = gtk.gdk.get_default_root_window().get_size()
            scrollwindow.set_size_request((w / 6), (h / 5))
            scrollwindow.add(s_treeview)
            scrollwindow.show()
            s_treeview.show()
            hbox.pack_start(scrollwindow)

            button = _widg.make_button(image='assign')
            button.show()
            hbox.pack_start(button)

            model = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_INT, gobject.TYPE_STRING)
            d_treeview = gtk.TreeView(model)

            column = gtk.TreeViewColumn(_("RTK Field"))
            d_treeview.append_column(column)
            cell = gtk.CellRendererText()
            cell.set_property('editable', False)
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', 0)
            column = gtk.TreeViewColumn(_("Source Index"))
            column.set_visible(False)
            d_treeview.append_column(column)
            cell = gtk.CellRendererText()
            cell.set_property('editable', False)
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', 1)
            column = gtk.TreeViewColumn(_("Source Field"))
            d_treeview.append_column(column)
            cell = gtk.CellRendererText()
            cell.set_property('editable', False)
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', 2)

            row = model.append(None, [_("Serial Number"), -1, ""])
            row = model.append(None, [_("Model"), -1, ""])
            row = model.append(None, [_("Market"), -1, ""])
            row = model.append(None, [_("Build Date"), -1, ""])
            row = model.append(None, [_("Delivery Date"), -1, ""])
            row = model.append(None, [_("Warranty Start Date"), -1, ""])
            row = model.append(None, [_("Warranty Period"), -1, ""])
            row = model.append(None, [_("Warranty Type"), -1, ""])

            scrollwindow = gtk.ScrolledWindow()
            w, h = gtk.gdk.get_default_root_window().get_size()
            scrollwindow.set_size_request((w / 6), (h / 5))
            scrollwindow.add(d_treeview)
            scrollwindow.show()
            d_treeview.show()
            hbox.pack_start(scrollwindow)

            dialog.vbox.pack_start(hbox)
            hbox.show()

            button.connect('button-release-event', _set_import_order,
                           s_treeview, d_treeview)

            response = dialog.run()

            if(response == gtk.RESPONSE_ACCEPT):
                model = d_treeview.get_model()
                row = model.get_iter_root()
                while row is not None:
                    order.append(model.get_value(row, 1))
                    row = model.iter_next(row)

            dialog.destroy()

        else:
            filechooser.destroy()

        return(response, sheet, order)

    def _build_data_import(self):

        """ This function imports unit build information from an external
            source to the program database.
        """

        from datetime import datetime

        # Find the revision ID.
        if(_conf.RTK_MODULES[0] == 1):
            _revision_id = self._app.REVISION.revision_id
        else:
            _revision_id  = 0

        if(self._response == gtk.RESPONSE_ACCEPT):
            _status = _("Importing Build Data")
            self._app.winTree.statusbar.push(2, _status)

            self._app.winTree.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            self._app.winWorkBook.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            self._app.winParts.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))

            query = "BEGIN TRANSACTION"
            results = self._app.DB.execute_query(query,
                                                   None,
                                                   self._app.ProgCnx)

            for i in xrange(self._sheet.nrows - 1):
                data = []
                for j in range(len(self._order)):
                    if((j == 0 or j == 1 or j == 2 or j == 7) and self._order[j] == -1):
                        data.append("")

                    # Import build date, delivery date, and warranty date.
                    # Convert dates to ISO format.
                    elif(j == 3 or j == 4 or j == 5):
                        if(self._order[j] != -1):
                            data.append(self._sheet.row_values(i + 1)[self._order[j]])
                            try:
                                d = xlrd.xldate_as_tuple(data[j], 0)
                                if(d[1] == "/" or d[2] == "/"):
                                    dfixed = datetime.strptime(d, '%m/%d/%Y').date().isoformat()
                                elif(d[1] == "-" or d[2] == "-"):
                                    dfixed = datetime.strptime(d, '%d-%b-%y').date().isoformat()
                                else:
                                    dfixed = datetime(*d[0:6]).date().isoformat()
                            except ValueError:
                                dfixed = datetime(1970, 1, 1, 0, 0, 0).date().isoformat()

                            data[j] = dfixed
                        else:
                            data.append(datetime(1970, 1, 1, 0, 0, 0).date().isoformat())

                    # Default to one year warranty period if no field is imported.
                    elif(j == 6 and self._order[j] == -1):
                        data.append(1)

                    else:
                        data.append(self._sheet.row_values(i + 1)[self._order[j]])

                if(data[0] == "" or data[0] is None or data[0] == 0):
                    data[0] = i

                values = (_revision_id, str(data[0]), str(data[1]),
                          str(data[2]), str(data[3]), str(data[4]),
                          str(data[5]), int(data[6]), str(data[7]))

                if(_conf.BACKEND == 'mysql'):
                    query = "INSERT INTO tbl_units \
                             (fld_revision_id, fld_serial_no, \
                              fld_model, fld_market, \
                              fld_build_date, fld_delivery_date, \
                              fld_warranty_date, fld_warranty_period, \
                              fld_warranty_type) \
                             VALUES \
                             (%d, '%s', '%s', '%s', '%s', '%s', '%s', %d, '%s')"
                elif(_conf.BACKEND == 'sqlite3'):
                    query = "INSERT INTO tbl_units \
                             (fld_revision_id, fld_serial_no, \
                              fld_model, fld_market, \
                              fld_build_date, fld_delivery_date, \
                              fld_warranty_date, fld_warranty_period, \
                              fld_warranty_type) \
                             VALUES \
                             (?, ?, ?, ?, ?, ?, ?, ?, ?)"

                results = self._app.DB.execute_query(query,
                                                       values,
                                                       self._app.ProgCnx,
                                                       commit=True)

            query = "END TRANSACTION"
            results = self._app.DB.execute_query(query,
                                                   None,
                                                   self._app.ProgCnx)

            self._app.winTree.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
            self._app.winWorkBook.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
            self._app.winParts.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

            self._app.winTree.statusbar.pop(2)

        return False

    def _field_incident_select(self):

        """ Function to select the file containing the field incident data and
            associate the external file fields with the appropriate RTK
            Program database fields.
        """

        import xlrd

        filechooser = gtk.FileChooserDialog(_("RTK - Import Field Incident Data"),
                                            buttons=(gtk.STOCK_CANCEL,
                                                     gtk.RESPONSE_REJECT,
                                                     gtk.STOCK_OK,
                                                     gtk.RESPONSE_ACCEPT))

        filechooser.set_default_response(gtk.RESPONSE_CANCEL)

        filter = gtk.FileFilter()
        filter.set_name(_("Hardware Files"))
        filter.add_mime_type('text/data')
        filter.add_mime_type('application/excel')
        filter.add_pattern('*.csv')
        filter.add_pattern('*.dat')
        filter.add_pattern('*.text')
        filter.add_pattern('*.txt')
        filter.add_pattern('*.xls')
        filechooser.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name(_("All files"))
        filter.add_pattern('*')
        filechooser.add_filter(filter)

        response = filechooser.run()

        order = []
        sheet = ''
        if(response == gtk.RESPONSE_ACCEPT):
            infile = filechooser.get_filename()
            (name, extension) = os.path.splitext(infile)

            # Open the workbook and get a list of the worksheets.
            sheet = _select_worksheet(filechooser.get_filename())
            filechooser.destroy()

            colnames = []
            for i in xrange(sheet.ncols):
                colnames.append(sheet.cell_value(0, i))

            # Display the list of columns in the selected worksheet.
            dialog = _widg.make_dialog(_("RTK - Import Field Incident Data"))

            hbox = gtk.HBox()

            model = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING)
            s_treeview = gtk.TreeView(model)

            column = gtk.TreeViewColumn()
            column.set_visible(False)
            s_treeview.append_column(column)
            cell = gtk.CellRendererText()
            cell.set_property('editable', False)
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', 0)
            column = gtk.TreeViewColumn(_("Column Heading"))
            s_treeview.append_column(column)
            cell.set_property('editable', False)
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', 1)

            for i in xrange(len(colnames)):
                row = model.append(None, [i, colnames[i]])

            scrollwindow = gtk.ScrolledWindow()
            w, h = gtk.gdk.get_default_root_window().get_size()
            scrollwindow.set_size_request((w / 6), (h / 5))
            scrollwindow.add(s_treeview)
            scrollwindow.show()
            s_treeview.show()
            hbox.pack_start(scrollwindow)

            button = _widg.make_button(image='assign')
            button.show()
            hbox.pack_start(button)

            model = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_INT, gobject.TYPE_STRING)
            d_treeview = gtk.TreeView(model)

            column = gtk.TreeViewColumn(_("RTK Field"))
            d_treeview.append_column(column)
            cell = gtk.CellRendererText()
            cell.set_property('editable', False)
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', 0)
            column = gtk.TreeViewColumn(_("Source Index"))
            column.set_visible(False)
            d_treeview.append_column(column)
            cell = gtk.CellRendererText()
            cell.set_property('editable', False)
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', 1)
            column = gtk.TreeViewColumn(_("Source Field"))
            d_treeview.append_column(column)
            cell = gtk.CellRendererText()
            cell.set_property('editable', False)
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', 2)

            row = model.append(None, [_("Incident ID"), -1, ""])
            row = model.append(None, [_("Incident Type"), -1, ""])
            row = model.append(None, [_("Incident Status"), -1, ""])
            row = model.append(None, [_("Incident Date"), -1, ""])
            row = model.append(None, [_("Closure Date"), -1, ""])
            row = model.append(None, [_("Incident Age"), -1, ""])
            row = model.append(None, [_("Affected Unit"), -1, ""])
            row = model.append(None, [_("Affected System"), -1, ""])
            row = model.append(None, [_("Short Description"), -1, ""])
            row = model.append(None, [_("Long Description"), -1, ""])
            row = model.append(None, [_("Closure Remarks"), -1, ""])
            row = model.append(None, [_("Part Number"), -1, ""])
            row = model.append(None, [_("Age at Incident"), -1, ""])
            row = model.append(None, ["User Boolean 1", -1, ""])
            row = model.append(None, ["User Boolean 2", -1, ""])
            row = model.append(None, ["User Boolean 3", -1, ""])
            row = model.append(None, ["User Boolean 4", -1, ""])
            row = model.append(None, ["User Float 1", -1, ""])
            row = model.append(None, ["User Float 2", -1, ""])
            row = model.append(None, ["User Float 3", -1, ""])
            row = model.append(None, ["User Float 4", -1, ""])
            row = model.append(None, ["User Integer 1", -1, ""])
            row = model.append(None, ["User Integer 2", -1, ""])
            row = model.append(None, ["User Integer 3", -1, ""])
            row = model.append(None, ["User Integer 4", -1, ""])
            row = model.append(None, ["User Memo 1", -1, ""])
            row = model.append(None, ["User Memo 2", -1, ""])
            row = model.append(None, ["User Memo 3", -1, ""])
            row = model.append(None, ["User Memo 4", -1, ""])
            row = model.append(None, ["User Text 1", -1, ""])
            row = model.append(None, ["User Text 2", -1, ""])
            row = model.append(None, ["User Text 3", -1, ""])
            row = model.append(None, ["User Text 4", -1, ""])

            scrollwindow = gtk.ScrolledWindow()
            w, h = gtk.gdk.get_default_root_window().get_size()
            scrollwindow.set_size_request((w / 6), (h / 5))
            scrollwindow.add(d_treeview)
            scrollwindow.show()
            d_treeview.show()
            hbox.pack_start(scrollwindow)

            dialog.vbox.pack_start(hbox)
            hbox.show()

            button.connect('button-release-event', _set_import_order,
                           s_treeview, d_treeview)

            response = dialog.run()

            if(response == gtk.RESPONSE_ACCEPT):
                model = d_treeview.get_model()
                row = model.get_iter_root()
                while row is not None:
                    order.append(model.get_value(row, 1))
                    row = model.iter_next(row)

            dialog.destroy()

        else:
            filechooser.destroy()

        return(response, sheet, order)

    def _field_incident_import(self):
        """
        This function imports field incident information from an external
        source to the program database.
        """

        from datetime import datetime

        if(self._response == gtk.RESPONSE_ACCEPT):
            _status = _("Importing Field Incidents")
            self._app.winTree.statusbar.push(2, _status)

            self._app.winTree.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            self._app.winWorkBook.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            self._app.winParts.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))

            query = "BEGIN TRANSACTION"
            results = self._app.DB.execute_query(query,
                                                   None,
                                                   self._app.ProgCnx)

            for i in xrange(self._sheet.nrows - 1):
                data = []
                for j in range(len(self._order)):
                    if(self._order[j] == -1):
                        data.append(0)
                    else:
                        data.append(self._sheet.row_values(i + 1)[self._order[j]])

                        # Import failure date and repair date.
                        # Convert dates to ISO format.
                        if(j == 3 or j == 4):
                            if(self._order[j] != -1):
                                try:
                                    d = xlrd.xldate_as_tuple(data[j], 0)
                                    if(d[1] == "/" or d[2] == "/"):
                                        dfixed = datetime.strptime(d, '%m/%d/%Y').date().isoformat()
                                    elif(d[1] == "-" or d[2] == "-"):
                                        dfixed = datetime.strptime(d, '%d-%b-%y').date().isoformat()
                                    else:
                                        dfixed = datetime(*d[0:6]).date().isoformat()
                                except:
                                    dfixed = datetime(1970, 1, 1, 0, 0, 0).date().isoformat()

                                data[j] = dfixed
                            else:
                                data[j] = datetime(1970, 1, 1, 0, 0, 0).date().isoformat()

                if(data[0] == "" or data[0] is None or data[0] == 0):
                    data[0] = i

                try:
                    values = (str(data[0]), str(data[1]), str(data[2]),
                              str(data[3]), str(data[4]), int(data[5]),
                              str(data[6]), int(data[7]), str(data[8]),
                              str(data[9]), str(data[10]))
                except ValueError:
                    print "One or more selected columns contain the wrong type of data for the RTK database."

                if(_conf.BACKEND == 'mysql'):
                    query = "INSERT INTO tbl_incident \
                             (fld_incident_id, fld_incident_type, fld_status, \
                              fld_incident_date, fld_closure_date, \
                              fld_incident_age, fld_short_description, \
                              fld_long_description, \
                              fld_remarks) \
                             VALUES \
                             ('%s', '%s', '%s', '%s', '%s', %d, '%s', '%s', \
                              '%s', '%s', '%s')"
                elif(_conf.BACKEND == 'sqlite3'):
                    query = "INSERT INTO tbl_incident \
                             (fld_incident_id, fld_incident_type, fld_status, \
                              fld_incident_date, fld_closure_date, \
                              fld_incident_age, fld_short_description, \
                              fld_long_description, \
                              fld_remarks) \
                             VALUES \
                             (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

                results = self._app.DB.execute_query(query,
                                                       values,
                                                       self._app.ProgCnx,
                                                       commit=True)

                values = (str(data[0]), str(data[11]), float(data[12]))

                if(_conf.BACKEND == 'mysql'):
                    query = "INSERT INTO tbl_incident_detail \
                             (fld_incident_id, fld_part_num, \
                              fld_age_at_incident) \
                             VALUES \
                             ('%s', '%s', %f)"
                elif(_conf.BACKEND == 'sqlite3'):
                    query = "INSERT INTO tbl_incident_detail \
                             (fld_incident_id, fld_part_num, \
                              fld_age_at_incident) \
                             VALUES \
                             (?, ?, ?)"

                results = self._app.DB.execute_query(query,
                                                       values,
                                                       self._app.ProgCnx,
                                                       commit=True)

            query = "END TRANSACTION"
            results = self._app.DB.execute_query(query,
                                                   None,
                                                   self._app.ProgCnx)

            self._app.winTree.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
            self._app.winWorkBook.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
            self._app.winParts.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

            self._app.winTree.statusbar.pop(2)

        return False

    def _set_next_page(self, page, assistant):

        """ Function to determine the next page to display. """

        if(page == 1):
            if(self.rdoHardware1.get_active()):
                (self._response,
                 self._sheet,
                 self._order) = self._hardware_data_select()
            elif(self.rdoHardware2.get_active()):
                (self._response,
                 self._sheet,
                 self._order) = self._hardware_data_select()
            elif(self.rdoBuildData.get_active()):
                (self._response,
                 self._sheet,
                 self._order) = self._build_data_select()
            elif(self.rdoFieldIncidents.get_active()):
                (self._response,
                 self._sheet,
                 self._order) = self._field_incident_select()

        _next_page = page + 1

        return(_next_page)

    def _apply(self, assistant):

        if(self.rdoHardware1.get_active()):
            self._hardware_data_import()
        elif(self.rdoHardware2.get_active()):
            self._hardware_flat_data_import()
        elif(self.rdoBuildData.get_active()):
            self._build_data_import()
        elif(self.rdoFieldIncidents.get_active()):
            self._field_incident_import()
        else:
            print self._order

        assistant.destroy()

        return False

    def _cancel(self, assistant):

        assistant.destroy()

        return False

def _select_worksheet(infile):

    """ This function allows the user to select the worksheet in the workbook
        file that contains the data to import.

        Keyword Arguments:
        infile -- the path to the workbook containing the data to import.
    """

    import xlrd

    book = xlrd.open_workbook(infile)
    sheets = book.sheets()

    dialog = _widg.make_dialog(_("Select Sheet to Import From"))

    model = gtk.TreeStore(gobject.TYPE_STRING)
    treeview = gtk.TreeView(model)

    column = gtk.TreeViewColumn(_("Worksheet"))
    treeview.append_column(column)
    cell = gtk.CellRendererText()
    cell.set_property('editable', False)
    column.pack_start(cell, True)
    column.add_attribute(cell, 'text', 0)

    scrollwindow = gtk.ScrolledWindow()
    w, h = gtk.gdk.get_default_root_window().get_size()
    scrollwindow.set_size_request((w / 6), (h / 6))
    scrollwindow.add(treeview)

    n = len(sheets)
    for i in range(n):
        iter = model.append(None, [sheets[i].name])

    dialog.vbox.pack_start(scrollwindow)
    treeview.show()
    scrollwindow.show()

    response = dialog.run()
    if(response == gtk.RESPONSE_ACCEPT):
        # Get the selected sheet name.
        selection = treeview.get_selection()
        (model, row) = selection.get_selected()
        path = model.get_path(row)
        iter = model.get_iter(path)
        sheet = model.get_value(iter, 0)
        sheet = book.sheet_by_name(sheet)

    else:
        sheet = ""

    dialog.destroy()

    return(sheet)

def _set_import_order(button, s_treeview, d_treeview):

    """ Sets the order columns will be imported from an external Excel
        spreadsheet to the RTK project database table. """

    selection = s_treeview.get_selection()
    (model, row) = selection.get_selected()

    colno = model.get_value(row, 0)
    colname = model.get_value(row, 1)

    selection = d_treeview.get_selection()
    (model, row) = selection.get_selected()

    model.set_value(row, 1, colno)
    model.set_value(row, 2, colname)

    return False
