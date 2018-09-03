# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Entry.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
Entry Module
-------------------------------------------------------------------------------

This module contains RAMSTK entry and textview classes.  These classes are derived
from the applicable pyGTK entry and textview, but are provided with RAMSTK
specific property values and methods.  This ensures a consistent look and feel
to widgets in the RAMSTK application.
"""

# Import the rtk.Widget base class.
from .Widget import gtk, pango  # pylint: disable=E0401


class RAMSTKEntry(gtk.Entry):
    """
    This is the RAMSTK Entry class.
    """

    # pylint: disable=R0913
    def __init__(self,
                 width=200,
                 height=25,
                 editable=True,
                 bold=False,
                 color='#BBDDFF',
                 tooltip='RAMSTK WARNING: Missing tooltip.  '
                 'Please register an Enhancement type bug.'):
        """
        Method to create RAMSTK Entry widgets.

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

        gtk.Entry.__init__(self)

        self.props.width_request = width
        self.props.height_request = height
        self.props.editable = editable

        if bold:
            self.modify_font(pango.FontDescription('bold'))

        if not editable:
            _bg_color = gtk.gdk.Color(color)
            self.modify_base(gtk.STATE_NORMAL, _bg_color)
            self.modify_base(gtk.STATE_ACTIVE, _bg_color)
            self.modify_base(gtk.STATE_PRELIGHT, _bg_color)
            self.modify_base(gtk.STATE_SELECTED, _bg_color)
            self.modify_base(gtk.STATE_INSENSITIVE, gtk.gdk.Color('#BFBFBF'))
            self.modify_font(pango.FontDescription('bold'))

        self.set_tooltip_markup(tooltip)

        self.show()


class RAMSTKTextView(gtk.TextView):
    """
    This is the RAMSTK TextView class.
    """

    def __init__(self, txvbuffer=None, width=200, height=100, tooltip=''):
        """
        Method to create RAMSTK TextView() widgets.  Returns a gtk.TextView()
        embedded in a gtk.ScrolledWindow().

        :keyword txvbuffer: the gtk.TextBuffer() to associate with the
                            RAMSTK TextView().  Default is None.
        :type txvbuffer: :py:class:`gtk.TextBuffer`
        :keyword int width: width of the  RAMSTK TextView() widget.
                            Default is 200.
        :keyword int height: height of the RAMSTK TextView() widget.
                             Default is 100.
        :return: _scrollwindow
        :rtype: gtk.ScrolledWindow
        """
        gtk.TextView.__init__(self)

        self.set_tooltip_markup(tooltip)

        self.set_buffer(txvbuffer)
        self.set_wrap_mode(gtk.WRAP_WORD)

        self.scrollwindow = gtk.ScrolledWindow()
        self.scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
        self.scrollwindow.props.width_request = width
        self.scrollwindow.props.height_request = height
        self.scrollwindow.add_with_viewport(self)

        self.tag_bold = txvbuffer.create_tag('bold', weight=pango.WEIGHT_BOLD)

    def do_get_buffer(self):
        """
        Method to return the gtk.TextBuffer() emedded in the RAMSTK TextView.

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
