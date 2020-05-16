# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.Entry.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Entry Module."""

# Standard Library Imports
from datetime import datetime
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, Pango

# RAMSTK Local Imports
from .widget import RAMSTKWidget


class RAMSTKEntry(Gtk.Entry, RAMSTKWidget):
    """This is the RAMSTK Entry class."""

    # Define private class scalar attributes.
    _default_height = 25
    _default_width = 200

    def __init__(self) -> None:
        r"""
        Create a RAMSTK Entry widget.
        """
        RAMSTKWidget.__init__(self)

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
        super().do_set_properties(**kwargs)

        try:
            _bold = kwargs['bold']
        except KeyError:
            _bold = False
        try:
            _editable = kwargs['editable']
        except KeyError:
            _editable = True

        self.set_property('editable', _editable)

        if _bold:
            self.modify_font(Pango.FontDescription('bold'))

    def do_update(self, value: str, handler_id: int = 0,
                  signal: str = '') -> None:
        """
        Update the RAMSTK Entry with a new value.

        :param str value: the information to update the RAMSTKEntry() to
            display.
        :keyword int handler_id: the handler ID associated with the
            RAMSTKComboBox().  This input will be removed in a future
            version in preference for using the signal ID dict.
        :keyword str signal: the name of the signal whose handler ID the
            RAMSTKEntry() needs to block.
        :return: None
        :rtype: None
        """
        # TODO: Remove this try construct after all views calling this
        #  method have been updated to account for the widget attribute
        #  containing the signal handler IDs.
        try:
            _handler_id = self.dic_handler_id[signal]
        except KeyError:
            _handler_id = handler_id

        self.handler_block(_handler_id)
        try:
            self.set_text(datetime.strftime(value, '%Y-%m-%d'))
        except TypeError:
            self.set_text(str(value))
        self.handler_unblock(_handler_id)


class RAMSTKTextView(Gtk.TextView, RAMSTKWidget):
    """This is the RAMSTK TextView class."""

    # Define private class scalar attributes.
    _default_height = 100
    _default_width = 200

    def __init__(self, txvbuffer: Gtk.TextBuffer = None) -> None:
        """
        Create RAMSTK TextView() widgets.

        Returns a Gtk.TextView() embedded in a Gtk.ScrolledWindow().

        :keyword txvbuffer: the Gtk.TextBuffer() to associate with the
            RAMSTKTextView().  Default is None.
        :type txvbuffer: :class:`Gtk.TextBuffer`
        :keyword int width: width of the  RAMSTKTextView() widget.  Default is
            200.
        :keyword int height: height of the RAMSTKTextView() widget.  Default
            is 100.
        :return: None
        :rtype: None
        """
        RAMSTKWidget.__init__(self)

        self.set_buffer(txvbuffer)
        self.set_wrap_mode(Gtk.WrapMode.WORD)

        self.scrollwindow = Gtk.ScrolledWindow()
        self.scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                     Gtk.PolicyType.AUTOMATIC)
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
        super().do_set_properties(**kwargs)

        self.scrollwindow.set_property('height-request', self.height)
        self.scrollwindow.set_property('width-request', self.width)
        self.scrollwindow.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)

    def do_update(self, value: str, handler_id: int, signal: str = '') -> None:
        """
        Update the RAMSTK TextView with a new value.

        :param str value: the information to update the RAMSTKTextView() to
            display.
        :param int handler_id: the handler ID associated with the
            RAMSTKTextView().
        :keyword str signal: the name of the signal whose handler ID the
            RAMSTKTextView() needs to block.
        :return: None
        :rtype: None
        """
        # TODO: Remove this try construct after all views calling this
        #  method have been updated to account for the widget attribute
        #  containing the signal handler IDs.
        try:
            _handler_id = self.dic_handler_id[signal]
        except KeyError:
            _handler_id = handler_id

        _buffer = self.do_get_buffer()

        _buffer.handler_block(_handler_id)
        _buffer.set_text(str(value))
        _buffer.handler_unblock(_handler_id)
