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

        self.assistant.set_forward_page_func(self._forward_page_select)

# Create the introduction page.
        fixed = gtk.Fixed()
        _text_ = _("This is the RelKit hardware import assistant.  It will help you import a hardware structure from an external file to the program database.  Press 'Forward' to continue or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(fixed, _("Introduction"))
        self.assistant.set_page_complete(fixed, True)

# Create the page to map input file fields to database fields.
        hbox = gtk.HBox()

        model = gtk.ListStore(gobject.TYPE_STRING)
        self.tvwFileFields = gtk.TreeView(model)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwFileFields)

        self.cell = gtk.CellRendererCombo()
        cellmodel = gtk.ListStore(gobject.TYPE_STRING)
        self.cell.set_property('has-entry', False)
        self.cell.set_property('model', cellmodel)
        self.cell.set_property('editable', 1)
        self.cell.set_property('text-column', 0)
        #self.cell.connect('changed', self._callback_combo_cell,
        #                  int(position[i].text), model, cols)
        column = gtk.TreeViewColumn()
        column.pack_start(self.cell, True)
        column.set_attributes(self.cell, text=0)
        label = gtk.Label(column.get_title())
        label.set_line_wrap(True)
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_markup("<span weight='bold'>%s</span>" % _("File\nField"))
        label.show_all()
        column.set_widget(label)
        self.tvwFileFields.append_column(column)

        hbox.pack_start(scrollwindow)

        model = gtk.ListStore(gobject.TYPE_STRING)
        self.tvwDBFields = gtk.TreeView(model)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwDBFields)

        hbox.pack_start(scrollwindow)

        self.assistant.append_page(hbox)
        self.assistant.set_page_type(hbox, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(hbox,
                                      _("Select Fields to Import"))
        self.assistant.set_page_complete(hbox, True)

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

    def _forward_page_select(self, current_page):

        if(current_page == 1):
            self._select_source_file()
        else:
            self.assistant.set_current_page(current_page + 1)

    def _select_source_file(self):

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
        #filter.add_mime_type("application/xls")
        filter.add_pattern("*.csv")
        filter.add_pattern("*.txt")
        #filter.add_pattern("*.xls")
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

        model = self.tvwFileFields.get_model()
        model.clear()
        _list = str(_contents[0][0]).rsplit('\t')
        for i in range(len(_list)):
            _data= []
            _data.append("")
            for j in range(len(_list)):
                _data.append(_list[j])
        print _data
        model = self.cell.get_property("model")
        for i in range(len(_data) - 1):
            print _data[i]
            model.append([_data[i]])


    def _import(self, button):
        """
        Method to import the data when the 'Apply' button is pressed.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        print "Import some shit"

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
