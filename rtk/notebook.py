#!/usr/bin/env python
""" This is the Workbook window for RTK. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       notebook.py is part of The RTK Project
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

# Add localization support.
import gettext
_ = gettext.gettext

# Import other RTK modules.
import configuration as _conf


class WorkBookWindow(gtk.Window):
    """
    The WorkBookWindow class is the NoteBook window used to display
    information about selected Revisions, Requirements, Functions,
    Hardware, Verification and Validation (V&V) Tasks, Reliability Growth
    Testing incidents, and field incidents.
    """

    def __init__(self, application):
        """
        Initializes the WorkBook Class.

        Keyword Arguments:
        application -- the RTK application.
        """

        self._app = application

        self.VISIBLE_PAGE = 0

        # Create a new window and set its properties.
        gtk.Window.__init__(self)
        self.set_resizable(True)
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)
        self.set_title(_(u"RTK Work Book"))

        n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        width = gtk.gdk.screen_width() / n_screens
        height = gtk.gdk.screen_height()

        # On a 1268x1024 screen, the size will be 845x640.
        if _conf.OS == 'Linux':
            self.width = width - 20
            self.height = (5 * height / 8)
        elif _conf.OS == 'Windows':
            self.width = width - 20
            self.height = (5 * height / 8) - 40

        self.set_default_size(self.width, self.height)
        self.set_border_width(5)
        self.set_position(gtk.WIN_POS_NONE)
        self.move((width / 2), (height / 3))

        self.show_all()
