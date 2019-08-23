# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.Entry.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Entry Module."""

# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk, GObject, Gtk, Pango


class RAMSTKEntry(Gtk.Entry):
    """This is the RAMSTK Entry class."""
    def __init__(self) -> None:
        r"""
        Create a RAMSTK Entry widget.
        """
        GObject.GObject.__init__(self)
        self.show()

    def do_set_properties(self, **kwargs: Any) -> None:
        r"""
        Set the properties of the RAMSTK Entry.

        :param \**kwargs: See below

        :Keyword Arguments:
            * *width* (int) -- width of the Gtk.Entry() widget.
                Default is 200.
            * *height* (int) -- height of the Gtk.Entry() widget.
                Default is 25.
            * *editable* (bool) -- boolean indicating whether Gtk.Entry()
                should be editable.  Defaults to True.
            * *bold* (bool) -- boolean indicating whether text should be bold.
                Defaults to False.
            * *color* (str) -- the hexidecimal color to set the background when
                the Gtk.Entry() is not editable.  Default is #BBDDFF (light
                blue).
            * *tooltip* (str) -- the tooltip, if any, for the entry.
                Default is an empty string.
        :return: None
        :rtype: None
        """
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
            _tooltip = ("Missing tooltip, please file a quality type issue to "
                        "have one added.")
        try:
            _width = kwargs['width']
        except KeyError:
            _width = 200

        if _height == 0:
            _height = 25
        if _width == 0:
            _width = 200

        self.set_property('width-request', _width)
        self.set_property('height-request', _height)
        self.set_property('editable', _editable)

        if _bold:
            self.modify_font(Pango.FontDescription('bold'))

        if not _editable:
            _bg_color = Gdk.RGBA(
                red=float(int(_color[1:3], 16)),
                green=float(int(_color[3:5], 16)),
                blue=float(int(_color[5:7], 16)),
                alpha=1.0,
            )
            self.override_background_color(Gtk.StateFlags.NORMAL, _bg_color)
            self.override_background_color(Gtk.StateFlags.ACTIVE, _bg_color)
            self.override_background_color(Gtk.StateFlags.PRELIGHT, _bg_color)
            self.override_background_color(Gtk.StateFlags.SELECTED, _bg_color)
            self.override_background_color(
                Gtk.StateFlags.INSENSITIVE,
                Gdk.RGBA(191.0, 191.0, 191.0, 1.0),
            )
            self.modify_font(Pango.FontDescription('bold'))

        self.set_tooltip_markup(_tooltip)

    def do_update(self, value: str, handler_id: int) -> None:
        """
        Update the RAMSTK Entry with a new value.

        :param str value: the information to update the RAMSTKEntry() to
            display.
        :param int handler_id: the handler ID associated with the
            RAMSTKEntry().
        :return: None
        :rtype: None
        """
        self.handler_block(handler_id)
        self.set_text(str(value))
        self.handler_unblock(handler_id)


class RAMSTKTextView(Gtk.TextView):
    """This is the RAMSTK TextView class."""
    def __init__(self, txvbuffer: Gtk.TextBuffer = None) -> None:
        """
        Create RAMSTK TextView() widgets.

        Returns a Gtk.TextView() embedded in a Gtk.ScrolledWindow().

        :keyword txvbuffer: the Gtk.TextBuffer() to associate with the
            RAMSTK TextView().  Default is None.
        :type txvbuffer: :class:`Gtk.TextBuffer`
        :keyword int width: width of the  RAMSTK TextView() widget.  Default is
            200.
        :keyword int height: height of the RAMSTK TextView() widget.  Default
            is 100.
        :return: None
        :rtype: None
        """
        GObject.GObject.__init__(self)

        self.set_buffer(txvbuffer)
        self.set_wrap_mode(Gtk.WrapMode.WORD)

        self.scrollwindow = Gtk.ScrolledWindow()
        self.scrollwindow.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC,
        )
        self.scrollwindow.add_with_viewport(self)

        self.tag_bold = txvbuffer.create_tag('bold', weight=Pango.Weight.BOLD)

    def do_get_buffer(self) -> Gtk.TextBuffer:
        """
        Return the Gtk.TextBuffer() emedded in the RAMSTK TextView.

        :return: buffer; the embedded Gtk.TextBuffer()
        :rtype: :class:`Gtk.TextBuffer`
        """
        return self.get_buffer()

    def do_get_text(self) -> Any:
        """
        Retrieve the text from the embedded Gtk.TextBuffer().

        :return: text; the text in the Gtk.TextBuffer().
        :rtype: str
        """
        _buffer = self.do_get_buffer()

        return _buffer.get_text(*_buffer.get_bounds(), True)

    def do_set_properties(self, **kwargs: Any) -> None:
        r"""
        Set the properties of the RAMSTK TextView.

        :param \**kwargs: See below

        :Keyword Arguments:
            * *height* (int) -- height of the Gtk.TextView() widget.
                                Default is 25.
            * *tooltip* (str) -- the tooltip, if any, for the entry.
                                 Default is an empty string.
            * *width* (int) -- width of the Gtk.TextView() widget.
                               Default is 200.
        :return: None
        :rtype: None
        """
        try:
            _height = kwargs['height']
        except KeyError:
            _height = 25
        try:
            _tooltip = kwargs['tooltip']
        except KeyError:
            _tooltip = ("Missing tooltip, please file a quality type issue to "
                        "have one added.")
        try:
            _width = kwargs['width']
        except KeyError:
            _width = 200

        if _height == 0:
            _height = 25
        if _width == 0:
            _width = 200

        self.scrollwindow.set_property('height-request', _height)
        self.set_property('tooltip-markup', _tooltip)
        self.scrollwindow.set_property('width-request', _width)
        self.scrollwindow.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)

    def do_update(self, value: str, handler_id: int) -> None:
        """
        Update the RAMSTK TextView with a new value.

        :param str value: the information to update the RAMSTKTextView() to
            display.
        :param int handler_id: the handler ID associated with the
            RAMSTKTextView().
        :return: None
        :rtype: None
        """
        _buffer = self.do_get_buffer()

        _buffer.handler_block(handler_id)
        _buffer.set_text(str(value))
        _buffer.handler_unblock(handler_id)
