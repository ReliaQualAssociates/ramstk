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

from _assistants_.incident import *

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
