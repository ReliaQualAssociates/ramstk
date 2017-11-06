# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Widget.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
Widget Module
-------------------------------------------------------------------------------

This module contains functions for interacting with RTK widgets.  This module
is the base class for all RTK widgets.
"""

import sys

import gettext

# Modules required for the GUI.
import pango  # pylint: disable=E0401,W0611
try:
    import pygtk  # pylint: disable=W0611
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk  # pylint: disable=W0611
except ImportError:
    sys.exit(1)
try:
    import gobject  # pylint: disable=W0611
except ImportError:
    sys.exit(1)

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

_ = gettext.gettext


def set_cursor(controller, cursor):
    """
    Function to set the cursor for a gtk.gdk.Window()

    :param controller: the :py:class:`rtk.RTK.RTK` master data controller.
    :param gtk.gdk.Cursor cursor: the gtk.gdk.Cursor() to set.  Only handles
                                  one of the following:
                                  - gtk.gdk.X_CURSOR
                                  - gtk.gdk.ARROW
                                  - gtk.gdk.CENTER_PTR
                                  - gtk.gdk.CIRCLE
                                  - gtk.gdk.CROSS
                                  - gtk.gdk.CROSS_REVERSE
                                  - gtk.gdk.CROSSHAIR
                                  - gtk.gdk.DIAMOND_CROSS
                                  - gtk.gdk.DOUBLE_ARROW
                                  - gtk.gdk.DRAFT_LARGE
                                  - gtk.gdk.DRAFT_SMALL
                                  - gtk.gdk.EXCHANGE
                                  - gtk.gdk.FLEUR
                                  - gtk.gdk.GUMBY
                                  - gtk.gdk.HAND1
                                  - gtk.gdk.HAND2
                                  - gtk.gdk.LEFT_PTR - non-busy cursor
                                  - gtk.gdk.PENCIL
                                  - gtk.gdk.PLUS
                                  - gtk.gdk.QUESTION_ARROW
                                  - gtk.gdk.RIGHT_PTR
                                  - gtk.gdk.SB_DOWN_ARROW
                                  - gtk.gdk.SB_H_DOUBLE_ARROW
                                  - gtk.gdk.SB_LEFT_ARROW
                                  - gtk.gdk.SB_RIGHT_ARROW
                                  - gtk.gdk.SB_UP_ARROW
                                  - gtk.gdk.SB_V_DOUBLE_ARROW
                                  - gtk.gdk.TCROSS
                                  - gtk.gdk.TOP_LEFT_ARROW
                                  - gtk.gdk.WATCH - when application is busy
                                  - gtk.gdk.XTERM - selection bar
    """

    controller.dic_books['listbook'].get_window().set_cursor(
        gtk.gdk.Cursor(cursor))
    controller.dic_books['modulebook'].get_window().set_cursor(
        gtk.gdk.Cursor(cursor))
    controller.dic_books['workbook'].get_window().set_cursor(
        gtk.gdk.Cursor(cursor))

    gtk.gdk.flush()

    return False
