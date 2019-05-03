# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.Widget.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Widget Module."""

import sys

import gettext

# Modules required for the GUI.
# Disable the unused-import because Gtk, Gdk, GObject, and Pango are all
# imported from this module by all the other GUI modules.
try:
    import gi
    gi.require_version('Gtk', '3.0')
except ImportError:
    print("FAILED TO IMPORT gi")
    sys.exit(1)
from gi.repository import Gdk, GdkPixbuf, GObject, Gtk, Pango

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

_ = gettext.gettext


def set_cursor(controller, cursor):
    """
    Set the cursor for the Module, List, and Work Book Gdk.Window().

    :param controller: the RAMSTK master data controller.
    :type controller: :class:`ramstk.RAMSTK.RAMSTK`
    :param Gdk.Cursor cursor: the Gdk.Cursor.new() to set.  Only handles
                                  one of the following:
                                  - Gdk.CursorType.X_CURSOR
                                  - Gdk.CursorType.ARROW
                                  - Gdk.CursorType.CENTER_PTR
                                  - Gdk.CIRCLE
                                  - Gdk.CROSS
                                  - Gdk.CROSS_REVERSE
                                  - Gdk.CursorType.CROSSHAIR
                                  - Gdk.DIAMOND_CROSS
                                  - Gdk.DOUBLE_ARROW
                                  - Gdk.DRAFT_LARGE
                                  - Gdk.DRAFT_SMALL
                                  - Gdk.EXCHANGE
                                  - Gdk.FLEUR
                                  - Gdk.GUMBY
                                  - Gdk.HAND1
                                  - Gdk.HAND2
                                  - Gdk.CursorType.LEFT_PTR - non-busy cursor
                                  - Gdk.PENCIL
                                  - Gdk.PLUS
                                  - Gdk.QUESTION_ARROW
                                  - Gdk.CursorType.RIGHT_PTR
                                  - Gdk.SB_DOWN_ARROW
                                  - Gdk.SB_H_DOUBLE_ARROW
                                  - Gdk.SB_LEFT_ARROW
                                  - Gdk.SB_RIGHT_ARROW
                                  - Gdk.SB_UP_ARROW
                                  - Gdk.SB_V_DOUBLE_ARROW
                                  - Gdk.TCROSS
                                  - Gdk.TOP_LEFT_ARROW
                                  - Gdk.CursorType.WATCH - when application is busy
                                  - Gdk.XTERM - selection bar
    :return: None
    :rtype: None
    """
    controller.dic_books['listbook'].get_window().set_cursor(
        Gdk.Cursor.new(cursor))
    controller.dic_books['modulebook'].get_window().set_cursor(
        Gdk.Cursor.new(cursor))
    controller.dic_books['workbook'].get_window().set_cursor(
        Gdk.Cursor.new(cursor))

    Gdk.flush()

    return None
