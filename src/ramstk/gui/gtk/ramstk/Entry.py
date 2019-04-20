# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.Entry.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Entry Module."""

# Import the ramstk.Widget base class.
from .Widget import gtk, pango  # pylint: disable=E0401


class RAMSTKEntry(gtk.Entry):
    """This is the RAMSTK Entry class."""

    # pylint: disable=R0913
    def __init__(self, **kwargs):
        r"""
        Create RAMSTK Entry widgets.

        :param \**kwargs: See below

        :Keyword Arguments:
            * *width* (int) -- width of the gtk.Entry() widget.
                               Default is 200.
            * *height* (int) -- height of the gtk.Entry() widget.
                                Default is 25.
            * *editable* (bool) -- boolean indicating whether gtk.Entry()
                                   should be editable.
                                   Defaults to True.
            * *bold* (bool) -- boolean indicating whether text should be bold.
                               Defaults to False.
            * *color* (str) -- the hexidecimal color to set the background when
                               the gtk.Entry() is not editable.
                               Default is #BBDDFF (light blue).
            * *tooltip* (str) -- the tooltip, if any, for the entry.
                                 Default is an empty string.
        """
        gtk.Entry.__init__(self)

        try:
            _bold = kwargs['bold']
        except KeyError:
            _bold = False
        try:
            _color = kwargs['color']
        except KeyError:
            _color = '#BBDDFF'
        try:
            _editable = kwargs['editable']
        except KeyError:
            _editable = True
        try:
            _height = kwargs['height']
        except KeyError:
            _height = 25
        try:
            _tooltip = kwargs['tooltip']
        except KeyError:
            _tooltip = ''
        try:
            _width = kwargs['width']
        except KeyError:
            _width = 200

        self.props.width_request = _width
        self.props.height_request = _height
        self.props.editable = _editable

        if _bold:
            self.modify_font(pango.FontDescription('bold'))

        if not _editable:
            _bg_color = gtk.gdk.Color(_color)
            self.modify_base(gtk.STATE_NORMAL, _bg_color)
            self.modify_base(gtk.STATE_ACTIVE, _bg_color)
            self.modify_base(gtk.STATE_PRELIGHT, _bg_color)
            self.modify_base(gtk.STATE_SELECTED, _bg_color)
            self.modify_base(gtk.STATE_INSENSITIVE, gtk.gdk.Color('#BFBFBF'))
            self.modify_font(pango.FontDescription('bold'))

        self.set_tooltip_markup(_tooltip)

        self.show()


class RAMSTKTextView(gtk.TextView):
    """This is the RAMSTK TextView class."""

    def __init__(self, txvbuffer=None, width=200, height=100, tooltip=''):
        """
        Create RAMSTK TextView() widgets.

        Returns a gtk.TextView() embedded in a gtk.ScrolledWindow().

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
        Return the gtk.TextBuffer() emedded in the RAMSTK TextView.

        :return: buffer; the embedded gtk.TextBuffer()
        :rtype: :py:class:`gtk.TextBuffer`
        """
        return self.get_buffer()

    def do_get_text(self):
        """
        Retrieve the text from the embedded gtk.TextBuffer().

        :return: text; the text in the gtk.TextBuffer().
        :rtype: str
        """
        _buffer = self.do_get_buffer()

        return _buffer.get_text(*_buffer.get_bounds())
