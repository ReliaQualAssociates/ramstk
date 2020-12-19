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
    """The RAMSTK Entry class."""

    # Define private scalar class attributes.
    _default_height = 25
    _default_width = 200

    def __init__(self) -> None:
        """Create a RAMSTK Entry widget."""
        RAMSTKWidget.__init__(self)

        self.show()

    def do_get_text(self):
        """Wrap the Gtk.Entry().get_text() method for consistent calls.

        :return: the text in the RAMSTKEntry().
        :rtype: str
        """
        return self.get_text()

    def do_set_properties(self, **kwargs: Any) -> None:
        """Set the properties of the RAMSTK Entry.

        Accepts the following keyword arguments:

            * *width* -- width of the Gtk.Entry() widget.
                Default is 200.
            * *height* -- height of the Gtk.Entry() widget.
                Default is 25.
            * *editable* -- boolean indicating whether Gtk.Entry()
                should be editable.  Defaults to True.
            * *bold* -- boolean indicating whether text should be bold.
                Defaults to False.
            * *color* -- the hexidecimal color to set the background when
                the Gtk.Entry() is not editable.  Default is #BBDDFF (light
                blue).
            * *tooltip* -- the tooltip, if any, for the entry.
                Default is an empty string.
        :return: None
        :rtype: None
        """
        super().do_set_properties(**kwargs)

        _bold = kwargs.get('bold', False)
        _editable = kwargs.get('editable', True)

        self.set_property('editable', _editable)

        if _bold:
            self.modify_font(Pango.FontDescription('bold'))

    def do_update(self, value: Any, signal: str = '') -> None:
        """Update the RAMSTK Entry with a new value.

        :param value: the information to update the RAMSTKEntry() to
            display.
        :keyword signal: the name of the signal whose handler ID the
            RAMSTKEntry() needs to block.
        :return: None
        :rtype: None
        """
        try:
            _value = datetime.strftime(value, '%Y-%m-%d')
        except TypeError:
            _value = str(value)

        # Sometimes there is no handler ID for the RAMSTKEntry().  This
        # usually happens when the widget is being used to display results
        # and has no associated callback method.
        try:
            _handler_id = self.dic_handler_id[signal]

            self.handler_block(_handler_id)
            self.set_text(_value)
            self.handler_unblock(_handler_id)
        except KeyError:
            self.set_text(_value)


class RAMSTKTextView(Gtk.TextView, RAMSTKWidget):
    """The RAMSTK TextView class."""

    # Define private class scalar attributes.
    _default_height = 100
    _default_width = 200

    def __init__(self, txvbuffer: Gtk.TextBuffer) -> None:
        """Create RAMSTK TextView() widgets.

        Returns a Gtk.TextView() embedded in a Gtk.ScrolledWindow().

        :param txvbuffer: the Gtk.TextBuffer() to associate with the
            RAMSTKTextView().
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
        """Return the Gtk.TextBuffer() emedded in the RAMSTK TextView.

        :return: buffer; the embedded Gtk.TextBuffer()
        :rtype: :class:`Gtk.TextBuffer`
        """
        return self.get_buffer()

    def do_get_text(self) -> Any:
        """Retrieve the text from the embedded Gtk.TextBuffer().

        :return: text; the text in the Gtk.TextBuffer().
        :rtype: str
        """
        _buffer = self.do_get_buffer()

        return _buffer.get_text(*_buffer.get_bounds(), True)

    def do_set_properties(self, **kwargs: Any) -> None:
        """Set the properties of the RAMSTK TextView.

        Accepts the following keyword arguments:

            * *height* -- height of the Gtk.TextView() widget.  Default is 25.
            * *tooltip* -- the tooltip, if any, for the entry.  Default is an
                empty string.
            * *width* -- width of the Gtk.TextView() widget.  Default is 200.
        :return: None
        :rtype: None
        """
        super().do_set_properties(**kwargs)

        self.scrollwindow.set_property('height-request', self.height)
        self.scrollwindow.set_property('width-request', self.width)
        self.scrollwindow.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)

    def do_update(self, value: str, signal: str = '') -> None:
        """Update the RAMSTK TextView with a new value.

        :param value: the information to update the RAMSTKTextView() to
            display.
        :keyword str signal: the name of the signal whose handler ID the
            RAMSTKTextView() needs to block.
        :return: None
        :rtype: None
        """
        _buffer = self.do_get_buffer()

        # Sometimes there is no handler ID for the RAMSTKTextView().  This
        # usually happens when the widget is being used to display results
        # and has no associated callback method.
        try:
            _handler_id = self.dic_handler_id[signal]

            _buffer.handler_block(_handler_id)
            _buffer.set_text(str(value))
            _buffer.handler_unblock(_handler_id)
        except KeyError:
            _buffer.set_text(str(value))
