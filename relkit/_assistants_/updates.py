#!/usr/bin/env python

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2012 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       updates.py is part of The RelKit Project
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


class AssignMTBFResults:
    """
    Assigns the MTBF and failure rate results to the assembly associated with
    the dataset.  Values are assigned to the specified fields.
    """

    def __init__(self, button, app):
        """
        Method to initialize the Survival Analysis Results Assignment
        Assistant.

        Keyword Arguments:
        button -- the gtk.Button widget that called this method.
        app    -- the RelKit application.
        """

        self._app = app

        self.assistant = gtk.Assistant()
        self.assistant.set_title(_("RelKit Survival Analysis Results Assignment Assistant"))
        self.assistant.connect('apply', self._assign)
        self.assistant.connect('cancel', self._cancel)
        self.assistant.connect('close', self._cancel)

        self.tvwAssemblies = gtk.TreeView()

# Create the introduction page.
        fixed = gtk.Fixed()
        _text_ = _("This is the RelKit survival analysis result assignment assistant.  It will help you assign the results of the currently selected dataset to the revision and assembly of your selection.  Press 'Forward' to continue or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.assistant.set_page_title(fixed, _("Introduction"))
        self.assistant.set_page_complete(fixed, True)

# Gather a list of existing assemblies and revision names from the open RelKit
# project database.
        query = "SELECT t1.fld_name, t2.fld_name, t1.fld_assembly_id \
                 FROM tbl_system AS t1 \
                 INNER JOIN tbl_revisions AS t2 \
                 WHERE t1.fld_revision_id=t2.fld_revision_id \
                 ORDER BY t1.fld_description ASC"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

        n_assemblies = len(results)

# Create a page to select the revision and assembly to assign the results.
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_INT)

# Load a gtk.ListStore with the results of the query.
        if(results != '' and n_assemblies > 0):
            for i in range(n_assemblies):
                model.append(results[i])

        self.tvwAssemblies.set_model(model)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Assembly"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        self.tvwAssemblies.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Revision"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=1)
        self.tvwAssemblies.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_(u"Assembly ID"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=2)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwAssemblies)

        frame = _widg.make_frame(_label_=_(""))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        self.assistant.append_page(frame)
        self.assistant.set_page_type(frame, gtk.ASSISTANT_PAGE_CONTENT)
        self.assistant.set_page_title(frame,
                                      _(u"Select Assembly to Assign Results"))
        self.assistant.set_page_complete(frame, True)

# Create the page to assign the results.
        fixed = gtk.Fixed()
        _text_ = _(u"Press 'Apply' to assign the results to the selected assembly or 'Cancel' to quit the assistant.")
        label = _widg.make_label(_text_, width=500, height=150)
        fixed.put(label, 5, 5)
        self.assistant.append_page(fixed)
        self.assistant.set_page_type(fixed,
                                     gtk.ASSISTANT_PAGE_CONFIRM)
        self.assistant.set_page_title(fixed, _(u"Assign Results"))
        self.assistant.set_page_complete(fixed, True)

        self.assistant.show_all()

    def _assign(self, button):
        """
        Method to create the desired data set.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        selection = self.tvwAssemblies.get_selection()
        (model, row) = selection.get_selected()

        _mtbf_ = float(self._app.DATASET.txtMTBF.get_text())
        _mtbfll_ = float(self._app.DATASET.txtMTBFLL.get_text())
        _mtbful_ = float(self._app.DATASET.txtMTBFUL.get_text())
        _fr_ = 1.0 / _mtbf_
        _frll_ = 1.0 / _mtbfll_
        _frul_ = 1.0 / _mtbful_

        query = "UPDATE tbl_system \
                 SET fld_mtbf_specified=%f, fld_mtbf_lcl=%f, fld_mtbf_ucl=%f, \
                     fld_failure_rate_specified=%f, fld_failure_rate_lcl=%f, \
                     fld_failure_rate_ucl=%f, fld_failure_rate_type=3 \
                 WHERE fld_assembly_id=%d" % \
                 (_mtbf_, _mtbfll_, _mtbful_, _fr_, _frll_, _frul_,
                  model.get_value(row, 2))

        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

# Load the hardware gtk.TreeView with the new information.
        self._app.HARDWARE.load_tree()
        _page = sum(_conf.RELIAFREE_MODULES[:4])
        self._app.winTree.notebook.set_current_page(_page - 1)

        return False

    def _cancel(self, button):
        """
        Method to destroy the gtk.Assistant when the 'Cancel' button is
        pressed.

        Keyword Arguments:
        button -- the gtk.Button that called this method.
        """

        self.assistant.destroy()
