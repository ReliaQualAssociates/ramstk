#!/usr/bin/env python
"""
===========================================
PyGTK Multi-Window Interface List Book View
===========================================
"""

# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.mwi.ListBook.py is part of the RTK Project
#
# All rights reserved.

import sys

# Import modules for localization support.
import gettext
import locale

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

# Import other RTK modules.
try:
    import Configuration as _conf
except ImportError:
    import rtk.Configuration as _conf

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def destroy(__widget, __event=None):
    """
    Quits the RTK application when the X in the upper right corner is
    pressed.

    :param gtk.Widget __widget: the gtk.Widget() that called this method.
    :keyword gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                    method.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    gtk.main_quit()

    return False


class ListView(gtk.Window):                 # pylint: disable=R0904
    """
    This is the List View class for the pyGTK multiple window interface.
    """

    def __init__(self):
        """
        Method to initialize an instance of the RTK List View class.
        """

        # Create a new window and set its properties.
        gtk.Window.__init__(self)
        self.set_title(_(u"RTK Matrices & Lists"))
        self.set_resizable(True)
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        self.set_default_size((_width / 3) - 10, (2 * _height / 7))
        self.set_border_width(5)
        self.set_position(gtk.WIN_POS_NONE)
        self.move((2 * _width / 3), 0)

        self.connect('delete_event', destroy)

        self.show_all()
