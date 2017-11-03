#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       exports.py is part of The RTK Project
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

# Import other RTK modules.
try:
    import Configuration as _conf
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.gui.gtk.Widgets as _widg

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, "")

import gettext
_ = gettext.gettext

# TODO: Move this to the Hardware class Assistant.
class ExportHardware:
    """
    This is the gtk.Assistant that walks the user through the process of
    exporting program incident records from the open RTK Program database.
    """

    def __init__(self, button, app):

        from lxml import etree

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_("RTK Export Hardware Assistant"))
        self.assistant.connect('apply', self._export)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

# Create the introduction page.
        fixed = gtk.Fixed()
        _text_ = _("This is the RTK hardware export assistant.  It will help you export the hardware structure from the database to an external file.  Press 'Forward' to continue or 'Cancel' to quit the assistant.")
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
        heading = etree.parse(_conf.RTK_FORMAT_FILE[3]).xpath(path)

        # Retrieve the column position from the format file.
        path = "/root/tree[@name='Hardware']/column/position"
        position = etree.parse(_conf.RTK_FORMAT_FILE[3]).xpath(path)

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
        dialog = gtk.FileChooserDialog(_("RTK: Export to File ..."),
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
