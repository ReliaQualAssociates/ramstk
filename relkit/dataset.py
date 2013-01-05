#!/usr/bin/env python
""" This is the Class that is used to represent and hold information related
    to Program survival data sets. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       dataset.py is part of The RelKit Project
#
# All rights reserved.

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

# Import other RelKit modules.
import configuration as _conf
import imports as _impt
import utilities as _util
import widgets as _widg

#from _assistants_.dataset import *

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

import gettext
_ = gettext.gettext


class Dataset:
    """
    The Dataset class is used to represent the survival data sets associated
    with the system being analyzed.
    """

    _gd_tab_labels = [_("Description:"), _("Data Source:"), _("Distribution:"),
                      _("Fit Method:"), _("Confidence:"),
                      _("Confidence Method:")]

    def __init__(self, application):
        """
        Initializes the Dataset Object.

        Keyword Arguments:
        application -- the RelKit application.
        """

        self._ready = False

        self._app = application

        self.treeview = None
        self.model = None
        self.selected_row = None
        self.dataset_id = 0
        self.n_datasets = 0
        self._col_order = []

# Create the Notebook for the SOFTWARE object.
        self.notebook = gtk.Notebook()
        if(_conf.TABPOS[2] == 'left'):
            self.notebook.set_tab_pos(gtk.POS_LEFT)
        elif(_conf.TABPOS[2] == 'right'):
            self.notebook.set_tab_pos(gtk.POS_RIGHT)
        elif(_conf.TABPOS[2] == 'top'):
            self.notebook.set_tab_pos(gtk.POS_TOP)
        else:
            self.notebook.set_tab_pos(gtk.POS_BOTTOM)

# Create the Dataset Description tab widgets.
        self.cmbConfMethod = _widg.make_combo()
        self.cmbDistribution = _widg.make_combo()
        self.cmbFitMethod = _widg.make_combo()
        self.cmbSource = _widg.make_combo()

        self.tvwDataSet = gtk.TreeView()

        self.txtConfidence = _widg.make_entry(_width_=100)
        self.txtDescription = _widg.make_entry(_width_=400)
        if self._general_data_widgets_create():
            self.debug_app._log.error("dataset.py: Failed to create General Data widgets.")
        if self._general_data_tab_create():
            self.debug_app._log.error("dataset.py: Failed to create General Data tab.")

        self.vbxDataset = gtk.VBox()
        toolbar = self._toolbar_create()

        self.vbxDataset.pack_start(toolbar, expand=False)
        self.vbxDataset.pack_start(self.notebook)

    def create_tree(self):
        """
        Creates the DATASET treeview and connects it to callback functions to
        handle editting.  Background and foreground colors can be set using the
        user-defined values in the RelKit configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()

        model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING)
        self.treeview = gtk.TreeView(model)
        #(self.treeview, self._col_order) = _widg.make_treeview('Hardware', 3,
        #                                                       self._app,
        #                                                       None,
        #                                                       bg_color,
        #                                                       fg_color)

        self.treeview.set_tooltip_text(_("Displays a list of survival data sets."))
        self.treeview.set_enable_tree_lines(True)
        scrollwindow.add(self.treeview)
        self.model = self.treeview.get_model()

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn(_("Dataset\nID"))
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        self.treeview.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 1)
        #cell.connect('toggled', self._component_list_edit, None, 2, model)
        column = gtk.TreeViewColumn(_("Dataset\nDescription"))
        column.pack_start(cell, True)
        column.set_attributes(cell, text=1)
        self.treeview.append_column(column)

        self.treeview.set_search_column(0)
        self.treeview.set_reorderable(True)

        #self.treeview.connect('cursor_changed', self._treeview_row_changed,
        #                      None, None)
        #self.treeview.connect('row_activated', self._treeview_row_changed)

        return(scrollwindow)

    def _toolbar_create(self):
        """
        Method to create the toolbar for the INCIDENT Object work book.
        """

        toolbar = gtk.Toolbar()

# Add item button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_ADD)
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        button.set_icon_widget(image)
        button.set_name('Add')
        #button.connect('clicked', self._component_add)
        button.set_tooltip_text(_("Adds a record to the selected data set."))
        toolbar.insert(button, 0)

        toolbar.show()

        return(toolbar)

    def _general_data_widgets_create(self):
        """ Method to create the General Data widgets. """

        # Quadrant 1 (upper left) widgets.
        self.cmbConfMethod.set_tooltip_text(_("Selects and displays the method for developing confidence bounds."))
        results = [["", "Fisher Matrix", "Bootstrap"]]
        _widg.load_combo(self.cmbConfMethod, results)
        #self.cmbConfMethod.connect('changed', self._callback_combo, 3)

        self.cmbDistribution.set_tooltip_text(_("Selects and displays the statistical distribution used to fit the data."))
        results = [["", "MCF", "Kaplan-Meier", "Gamma", "Exponential",
                    "Lognormal", "Normal", "Weibull", "WeiBayes"]]
        _widg.load_combo(self.cmbDistribution, results)
        #self.cmbDistribution.connect('changed', self._callback_combo, 3)

        self.cmbFitMethod.set_tooltip_text(_("Selects and displays the method used to fit the data to the selected distribution."))
        results = [["", "Rank Regression", "MLE"]]
        _widg.load_combo(self.cmbFitMethod, results)
        #self.cmbFitMethod.connect('changed', self_callback_combo, 3)

        self.cmbSource.set_tooltip_text(_("Selects and displays the source of the selected data set."))
        results = [["", "ALT", "Reliability Growth",
                    "Reliability Demonstration", "Field"]]
        _widg.load_combo(self.cmbSource, results)
        #self.cmbSource.connect('changed', self._callback_combo, 2)

        self.txtConfidence.set_tooltip_text(_("Desired statistical confidence"))
        self.txtDescription.set_tooltip_text(_("Description of the selected data set."))

        #self.chkAccepted.set_tooltip_text(_("Displays whether the field incident has been accepted by the responsible owner."))
        #self.chkAccepted.connect('toggled', self._callback_check, 31)

        #self.chkReviewed.set_tooltip_text(_("Displays whether the field incident has been reviewed by the responsible owner."))
        #self.chkReviewed.connect('toggled', self._callback_check, 20)

        # Quadrant 2 (upper right) widgets.

        return False

    def _general_data_tab_create(self):
        """
        Method to create the General Data gtk.Notebook tab and populate it
        with the appropriate widgets for the DATASET object.
        """

        hbox = gtk.HBox()

        fixed = gtk.Fixed()

        # Populate quadrant 1 (upper left).
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("General Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        y_pos = 5
        for i in range(len(self._gd_tab_labels)):
            label = _widg.make_label(self._gd_tab_labels[i], 150, 25)
            fixed.put(label, 5, (30 * i + y_pos))

        fixed.put(self.txtDescription, 5, y_pos)
        y_pos += 30

        fixed.put(self.cmbSource, 5, y_pos)
        y_pos += 35

        fixed.put(self.cmbDistribution, 5, y_pos)
        y_pos += 35

        fixed.put(self.cmbFitMethod, 5, y_pos)
        y_pos += 35

        fixed.put(self.txtConfidence, 5, y_pos)
        y_pos += 30

        fixed.put(self.cmbConfMethod, 5, y_pos)
        y_pos += 35

        fixed.show_all()

        vpaned = gtk.VPaned()

        vpaned.pack1(frame, True, True)

        hbox.pack_start(vpaned)

        # Insert the tab.
        label = gtk.Label()
        _heading = _("General\nData")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays general information about the selected dataset."))

        self.notebook.insert_page(hbox,
                                  tab_label=label,
                                  position=-1)

        return False

    def load_tree(self):
        """
        Loads the Hardware treeview model with system information.  This
        information can be stored either in a MySQL or SQLite3 database.
        """

        if(_conf.RELIAFREE_MODULES[0] == 1):
            values = (self._app.REVISION.revision_id,)
        else:
            values = (0,)

        query = "SELECT * FROM tbl_dataset"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            return True

        n_datasets = len(results)

        self.model.clear()
        self.selected_row = None

        # Load the model with the returned results.
        for i in range(n_datasets):
            _data_ = (results[i][0], results[i][2])
            self.model.append(_data_)

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        root = self.model.get_iter_root()
        if root is not None:
            path = self.model.get_path(root)
            col = self.treeview.get_column(0)
            self.treeview.row_activated(path, col)

        return False

    def load_notebook(self):
        """ Method to load the DATASET Object gtk.Notebook. """

        return False
