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
from typing import Any, Callable, Union

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

        _bold_flag = kwargs.get("bold", False)
        _editable_flag = kwargs.get("editable", True)

        self.set_property("editable", _editable_flag)

        if _bold_flag:
            self.override_font(Pango.FontDescription("bold"))

    def do_update(
        self,
        value_obj: Union[bool, float, int, str],
        signal_str: str = "changed",
    ) -> None:
        """Update the RAMSTK Entry with a new value.

        :param value_obj: the information to update the RAMSTKEntry() to display.
        :param signal_str: the name of the signal whose handler ID the RAMSTKEntry()
            needs to block.
        :return: None
        :rtype: None
        """
        try:
            _value_str = datetime.strftime(value_obj, "%Y-%m-%d")  # type: ignore
        except TypeError:
            _value_str = str(value_obj)

        # Sometimes there is no handler ID for the RAMSTKEntry().  This
        # usually happens when the widget is being used to display results
        # and has no associated callback method.
        try:
            _handler_id = self.dic_handler_id[signal_str]

            self.handler_block(_handler_id)
            self.set_text(_value_str)
            self.handler_unblock(_handler_id)
        except KeyError:
            self.set_text(_value_str)


class RAMSTKTextView(Gtk.TextView, RAMSTKWidget):
    """The RAMSTK TextView class."""

    # Define private class scalar attributes.
    _default_height = 100
    _default_width = 200

    def __init__(self, buffer_obj: Gtk.TextBuffer) -> None:
        """Create RAMSTK TextView() widgets.

        Returns a Gtk.TextView() embedded in a Gtk.ScrolledWindow().

        :param buffer_obj: the Gtk.TextBuffer() to associate with the RAMSTKTextView().
        :return: None
        :rtype: None
        """
        RAMSTKWidget.__init__(self)

        self.set_buffer(buffer_obj)
        self.set_wrap_mode(Gtk.WrapMode.WORD)

        self.scrollwindow = Gtk.ScrolledWindow()
        self.scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrollwindow.add_with_viewport(self)

        self.tag_bold = buffer_obj.create_tag("bold", weight=Pango.Weight.BOLD)

    # pylint: disable=arguments-differ
    def connect(
        self,
        signal_str: str,
        callback_obj: Callable,
        position_idx: int,
        message_str: str,
    ) -> int:
        """Connect textview's buffer to a callback method or function.

        :param signal_str: the name of the signal whose handler ID the Gtk.TextBuffer()
            needs to block.
        :param callback_obj: the function or method to handle RAMSTKTextView() edits.
        :param position_idx: the index position in the view using the RAMSTKTextView().
        :param message_str: the pubsub message the RAMSTKTextView() responds to.
        """
        _buffer_obj = self.do_get_buffer()
        return _buffer_obj.connect(
            signal_str,
            callback_obj,
            position_idx,
            message_str,
            self,
        )

    def do_get_buffer(self) -> Gtk.TextBuffer:
        """Return the Gtk.TextBuffer() emedded in the RAMSTKTextView().

        :return: buffer; the embedded Gtk.TextBuffer()
        :rtype: :class:`Gtk.TextBuffer`
        """
        return self.get_buffer()

    def do_get_text(self) -> Any:
        """Retrieve the text from the embedded Gtk.TextBuffer().

        :return: text; the text in the Gtk.TextBuffer().
        :rtype: str
        """
        _buffer_obj = self.do_get_buffer()
        _start_obj, _end_obj = _buffer_obj.get_bounds()

        return _buffer_obj.get_text(_start_obj, _end_obj, True)

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

        self.scrollwindow.set_property("height-request", self.height)
        self.scrollwindow.set_property("width-request", self.width)
        self.scrollwindow.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)

    def do_update(
        self,
        value_str: str,
        signal_str: str = "changed",
    ) -> None:
        """Update the RAMSTK TextView with a new value.

        :param value_str: the information to update the RAMSTKTextView() to display.
        :param signal_str: the name of the signal whose handler ID the RAMSTKTextView()
            needs to block.
        :return: None
        :rtype: None
        """
        _buffer_obj = self.do_get_buffer()

        # Sometimes there is no handler ID for the RAMSTKTextView().  This
        # usually happens when the widget is being used to display results
        # and has no associated callback method.
        try:
            _handler_id = self.dic_handler_id[signal_str]

            _buffer_obj.handler_block(_handler_id)
            _buffer_obj.set_text(value_str)
            _buffer_obj.handler_unblock(_handler_id)
        except KeyError:
            _buffer_obj.set_text(value_str)
