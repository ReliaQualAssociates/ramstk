#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.mwi.WorkBook.py is part of The RTK Project
#
# All rights reserved.

"""
===========================================
PyGTK Multi-Window Interface Work Book View
===========================================
"""

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
__copyright__ = 'Copyright 2007 - 2014 Andrew "Weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def destroy(__widget, __event=None):
    """
    Quits the RTK application when the X in the upper right corner is
    pressed.

    :param gtk.Widget __widget: the gtk.Widget() that called this function.
    :keyword gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                    function.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    gtk.main_quit()

    return False


class WorkView(gtk.Window):                 # pylint: disable=R0904
    """
    This is the Work View for the pyGTK multiple window interface.
    """

    def __init__(self):
        """
        Initializes an instance of the Work View class.
        """

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
        self.move((_width / 1), (_height / 2))

        self.connect('delete_event', destroy)

        self.show_all()
