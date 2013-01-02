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

# Create the Dataset Description tab.
        self.cmbType = _widg.make_combo()
        self.cmbConfMethod = _widg.make_combo()

        self.tvwDataSet = gtk.TreeView()

        self.txtDescription = _widg.make_entry(_width_=400)
        self.txtConfidence = _widg.make_entry(_width_=100)
        if self._general_data_widgets_create():
            self.debug_app._log.error("dataset.py: Failed to create General Data widgets.")
        if self._general_data_tab_create():
            self.debug_app._log.error("dataset.py: Failed to create General Data tab.")

        self.vbxDataset = gtk.VBox()
        toolbar = self._toolbar_create()

        self.vbxDataset.pack_start(toolbar, expand=False)
        self.vbxDataset.pack_start(self.notebook)

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
        button.connect('clicked', self._component_add)
        button.set_tooltip_text(_("Adds a record to the selected data set."))
        toolbar.insert(button, 0)

        toolbar.show()

        return(toolbar)

    def _general_data_widgets_create(self):
        """ Method to create the General Data widgets. """

        # Quadrant 1 (upper left) widgets.
        self.txtDescription.set_tooltip_text(_("Description of the selected data set."))

        self.cmbType.set_tooltip_text(_("Selects and displays the type or source of the selected data set."))
        results = ["", "Field", "ALT"]
        _widg.load_combo(self.cmbType, results)
        #self.cmbType.connect('changed', self._callback_combo, 2)

        self.cmbConfMethod.set_tooltip_text(_("Selects and displays the method for developing confidence bounds."))
        results = ["", "Fisher Matrix", "Bootstrap"]
        _widg.load_combo(self.cmbConfMethod, results)
        #self.cmbConfMethod.connect('changed', self._callback_combo, 3)

        #self.chkAccepted.set_tooltip_text(_("Displays whether the field incident has been accepted by the responsible owner."))
        #self.chkAccepted.connect('toggled', self._callback_check, 31)

        #self.chkReviewed.set_tooltip_text(_("Displays whether the field incident has been reviewed by the responsible owner."))
        #self.chkReviewed.connect('toggled', self._callback_check, 20)

        # Quadrant 2 (upper right) widgets.

        return False

    def _general_data_tab_create(self):

        return False
