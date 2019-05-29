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
# Disable the unused-import because pango, pygtk, gtk, and gobject are all
# imported from this module by all the other GUI modules.
import pango  # pylint: disable=unused-import   # noqa
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
    import gobject  # pylint: disable=unused-import     # noqa
except ImportError:
    sys.exit(1)

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

_ = gettext.gettext


def set_cursor(controller, cursor):
    """
    Set the cursor for the Module, List, and Work Book gtk.gdk.Window().

    :param controller: the RAMSTK master data controller.
    :type controller: :class:`ramstk.RAMSTK.RAMSTK`
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
    :return: None
    :rtype: None
    """
    controller.dic_books['listbook'].get_window().set_cursor(
        gtk.gdk.Cursor(cursor))
    controller.dic_books['modulebook'].get_window().set_cursor(
        gtk.gdk.Cursor(cursor))
    controller.dic_books['workbook'].get_window().set_cursor(
        gtk.gdk.Cursor(cursor))

    gtk.gdk.flush()

    return None
