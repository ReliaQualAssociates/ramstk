#!/usr/bin/env python
"""
This is the Work Book view for RTK.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       WorkBook.py is part of The RTK Project
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

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
except ImportError:
    import rtk.configuration as _conf

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class WorkView(gtk.Window):
    """
    This is the Work View for the pyGTK multiple window interface.
    """

    def __init__(self):
        """
        Initializes the Work View class.
        """

        self.VISIBLE_PAGE = 0

        # Create a new window and set its properties.
        gtk.Window.__init__(self)
        self.set_resizable(True)
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)
        self.set_title(_(u"RTK Work Book"))

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        # On a 1268x1024 screen, the size will be 845x640.
        if _conf.OS == 'Linux':
            _width = _width - 20
            _height = (5 * _height / 8)
        elif _conf.OS == 'Windows':
            _width = _width - 20
            _height = (5 * _height / 8) - 40

        self.set_default_size(_width, _height)
        self.set_border_width(5)
        self.set_position(gtk.WIN_POS_NONE)
        self.move((_width / 2), (_height / 3))

        self.connect('delete_event', self.destroy)

        self.show_all()

    def create_work_book(self, view, controller):
        """
        """

        return view(controller, self.notebook)

    def destroy(self, __widget, __event=None, data=None):
        """
        Method to quit the RTK application when the X in the upper
        right corner is pressed.

        :param gtk.Widget __widget: the gtk.Widget() that called this method.
        :keyword gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                        method.
        :keyword data: any user-supplied data.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        gtk.main_quit()

        return False
