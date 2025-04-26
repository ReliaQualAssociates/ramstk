# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.entry.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKEntry module."""

# Standard Library Imports
from datetime import date, datetime
from typing import Dict, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, Pango

# RAMSTK Local Imports
from .widget import RAMSTKBaseWidget, WidgetProperties


class RAMSTKEntry(Gtk.Entry, RAMSTKBaseWidget):
    """The RAMSTKEntry class."""

    # Define private scalar class attributes.
    _default_height = 25
    _default_width = 200
    _edit_signal = "changed"

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKEntry widget."""
        RAMSTKBaseWidget.__init__(self)

        self.show()

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKEntry.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKEntry.
        """
        super().do_set_properties(properties)

        self.dic_properties["bold"] = properties.get("bold", False)
        self.dic_properties["editable"] = properties.get("editable", True)
        self.dic_properties["input_purpose"] = properties.get(
            "input_purpose",
            Gtk.InputPurpose.FREE_FORM,
        )
        self.dic_properties["invisible_char"] = properties.get("invisible_char", "*")
        self.dic_properties["xalign"] = properties.get("xalign", True)

        self.set_property("editable", self.dic_properties["editable"])

        if self.dic_properties["bold"]:
            self.modify_font(Pango.FontDescription("bold"))

        self.set_input_purpose(self.dic_properties["input_purpose"])
        self.set_invisible_char(self.dic_properties["invisible_char"])

    def do_update(self, package: Dict[str, Union[bool, date, float, int, str]]) -> None:
        """Update the RAMSTKEntry with a new value.

        :param package: the date package to use to update the RAMSTKEntry.
        """
        _field, _value = next(iter(package.items()))

        if _field != self.field:
            return

        if isinstance(_value, date):
            _value = datetime.strftime(_value, "%Y-%m-%d")

        try:
            self.handler_block(self.dic_handler_id[self._edit_signal])
            self.set_text(_value)
            self.handler_unblock(self.dic_handler_id[self._edit_signal])
        except KeyError:
            self.set_text(_value)

    def on_changed(
        self, __entry: RAMSTKBaseWidget  # pylint: disable=unused-argument
    ) -> None:
        """Retrieve the data package for the RAMSTKEntry on value changes.

        This method also sends a PyPubSub message along with the data package for
        listeners to update with the new value.

        :param __entry: the RAMSTKEntry whose edited signal called this method.
        """
        try:
            self.handler_block(self.dic_handler_id[self._edit_signal])
            _package = {self.field: self.do_get_text()}
            self.handler_unblock(self.dic_handler_id[self._edit_signal])
        except KeyError:
            _package = {self.field: self.do_get_text()}

        pub.sendMessage(self.send_topic, node_id=self.record_id, package=_package)

    # ----- ----- RAMSTKEntry specific methods. ----- ----- #
    def do_get_text(self) -> Union[float, int, str, None]:
        """Retrieve the text displayed in the RAMSTKEntry.

        This method will return the correct datatype (float, int, str) associated with
        the database field associated with the RAMSTKEntry.

        :return: the text in the RAMSTKEntry.
        """
        _value: Union[float, int, str, None] = None

        if self.datatype == "gfloat":
            _value = float(self.get_text())
        elif self.datatype == "gint":
            _value = int(self.get_text())
        elif self.datatype == "gchararray":
            _value = str(self.get_text())

        return _value


class RAMSTKTextView(Gtk.TextView, RAMSTKBaseWidget):
    """The RAMSTKTextView class."""

    # Define private class scalar attributes.
    _default_height = 100
    _default_width = 200
    _edit_signal = "changed"

    def __init__(self, txtbuffer: Gtk.TextBuffer) -> None:
        """Initialize an instance of the RAMSTKTextView widget.

        :param txtbuffer: the Gtk.TextBuffer to associate with the RAMSTKTextView.
        """
        RAMSTKBaseWidget.__init__(self)

        self.dic_properties["buffer"] = txtbuffer
        self.tag_bold = self.dic_properties["buffer"].create_tag(  # type: ignore[union-attr] # noqa
            "bold", weight=Pango.Weight.BOLD
        )
        self.set_buffer(self.dic_properties["buffer"])

        self.scrollwindow = Gtk.ScrolledWindow()
        self.scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrollwindow.add_with_viewport(self)

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKTextView.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKTextView.
        """
        super().do_set_properties(properties)

        self.dic_properties["buffer"] = properties.get("buffer", Gtk.TextBuffer())
        self.dic_properties["editable"] = properties.get("editable", True)
        self.dic_properties["justify"] = properties.get(
            "justify",
            Gtk.Justification.RIGHT,
        )
        self.dic_properties["wrap_mode"] = properties.get(
            "wrap_mode", Gtk.WrapMode.WORD
        )

        self.set_buffer(self.dic_properties["buffer"])
        self.set_editable(self.dic_properties["editable"])
        self.set_justification(self.dic_properties["justify"])
        self.set_wrap_mode(self.dic_properties["wrap_mode"])

    def do_update(self, package: Dict[str, Union[bool, date, float, int, str]]) -> None:
        """Update the RAMSTKTextView with a new value.

        :param package: the date package to use to update the RAMSTKTextView.
        """
        _field, _value = next(iter(package.items()))

        if _field != self.field:
            return

        try:
            self.dic_properties["buffer"].handler_block(  # type: ignore[union-attr]
                self.dic_handler_id[self._edit_signal]
            )
            self.dic_properties["buffer"].set_text(str(_value))  # type: ignore[union-attr] # noqa
            self.dic_properties["buffer"].handler_unblock(  # type: ignore[union-attr]
                self.dic_handler_id[self._edit_signal]
            )
        except KeyError:
            self.dic_properties["buffer"].set_text(str(_value))  # type: ignore[union-attr] # noqa

    def on_changed(self) -> None:
        """Retrieve the data package for the RAMSTKTextView on value changes.

        This method also sends a PyPubSub message along with the data package for
        listeners to update with the new value.
        """
        try:
            self.dic_properties["buffer"].handler_block(  # type: ignore[union-attr]
                self.dic_handler_id[self._edit_signal]
            )
            _package = {self.field: self.do_get_text()}
            self.dic_properties["buffer"].handler_unblock(  # type: ignore[union-attr]
                self.dic_handler_id[self._edit_signal]
            )
        except KeyError:
            _package = {self.field: self.do_get_text()}

        pub.sendMessage(self.topic, node_id=self.record_id, package=_package)

    # ----- ----- RAMSTKTextView specific methods. ----- ----- #
    def do_get_text(self) -> str:
        """Retrieve the text from the embedded Gtk.TextBuffer().

        :return: text; the text in the Gtk.TextBuffer().
        :rtype: str
        """
        return self.dic_properties["buffer"].get_text(  # type: ignore[union-attr] # noqa
            *self.dic_properties["buffer"].get_bounds(), True  # type: ignore[union-attr] # noqa
        )
