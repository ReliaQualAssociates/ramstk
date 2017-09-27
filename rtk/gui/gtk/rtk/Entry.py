# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Entry.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
This module contains functions for creating, populating, destroying, and
interacting with pyGTK widgets.  Import this module in other modules that
create, populate, destroy, or interact with pyGTK widgets in the RTK
application.  This module is specific to data entry and data display widgets.
"""

import gettext
import sys

# Modules required for the GUI.
import pango
try:
    from pygtk import require
    require('2.0')
except ImportError:
    sys.exit(1)
try:
    from gtk import STATE_SELECTED, WRAP_WORD, Entry, STATE_ACTIVE, \
        POLICY_AUTOMATIC, STATE_INSENSITIVE, ScrolledWindow, STATE_PRELIGHT, \
        TextView, STATE_NORMAL, gdk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class RTKEntry(gtk.Entry):
    """
    This is the RTK Entry class.
    """

    def __init__(self, width=200, height=25, editable=True, bold=False,
                 color='#BBDDFF',
                 tooltip='RTK WARNING: Missing tooltip.  '
                         'Please register an Enhancement type bug.'):
        """
        Method to create RTK Entry widgets.

        :keyword int width: width of the gtk.Entry() widget.  Default is 200.
        :keyword int height: height of the gtk.Entry() widget.  Default is 25.
        :keyword bool editable: boolean indicating whether gtk.Entry()
                                should be editable.  Defaults to True.
        :keyword boolean bold: boolean indicating whether text should be bold.
                               Defaults to False.
        :keyword str color: the hexidecimal color to set the background when
                            the gtk.Entry() is not editable.  Defaults to
                            #BBDDFF (light blue).
        :return: _entry
        :rtype: gtk.Entry
        """

        Entry.__init__(self)

        self.props.width_request = width
        self.props.height_request = height
        self.props.editable = editable

        if bold:
            self.modify_font(pango.FontDescription('bold'))

        if not editable:
            _bg_color = gdk.Color(color)
            self.modify_base(STATE_NORMAL, _bg_color)
            self.modify_base(STATE_ACTIVE, _bg_color)
            self.modify_base(STATE_PRELIGHT, _bg_color)
            self.modify_base(STATE_SELECTED, _bg_color)
            self.modify_base(STATE_INSENSITIVE, _bg_color)
            self.modify_font(pango.FontDescription('bold'))

        self.set_tooltip_markup(tooltip)

        self.show()


class RTKTextView(gtk.TextView):
    """
    This is the RTK TextView class.
    """

    def __init__(self, txvbuffer=None, width=200, height=100, tooltip=''):
        """
        Method to create RTK TextView() widgets.  Returns a gtk.TextView()
        embedded in a gtk.ScrolledWindow().

        :keyword txvbuffer: the gtk.TextBuffer() to associate with the
                            RTK TextView().  Default is None.
        :type txvbuffer: :py:class:`gtk.TextBuffer`
        :keyword int width: width of the  RTK TextView() widget.
                            Default is 200.
        :keyword int height: height of the RTK TextView() widget.
                             Default is 100.
        :return: _scrollwindow
        :rtype: gtk.ScrolledWindow
        """

        TextView.__init__(self)

        self.set_tooltip_markup(tooltip)

        self.set_buffer(txvbuffer)
        self.set_wrap_mode(WRAP_WORD)

        self.scrollwindow = ScrolledWindow()
        self.scrollwindow.set_policy(POLICY_AUTOMATIC,
                                     POLICY_AUTOMATIC)
        self.scrollwindow.props.width_request = width
        self.scrollwindow.props.height_request = height
        self.scrollwindow.add_with_viewport(self)

    def do_get_buffer(self):
        """
        Method to return the gtk.TextBuffer() emedded in the RTK TextView.

        :return: buffer; the embedded gtk.TextBuffer()
        :rtype: :py:class:`gtk.TextBuffer`
        """

        return self.get_buffer()

    def do_get_text(self):
        """
        Method to retrieve the text from the embedded gtk.TextBuffer().

        :return: text; the text in the gtk.TextBuffer().
        :rtype: str
        """

        _buffer = self.do_get_buffer()

        return _buffer.get_text(*_buffer.get_bounds())
