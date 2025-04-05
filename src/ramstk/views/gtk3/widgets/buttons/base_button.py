# pylint: disable=protected-access, non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.buttons.base_button.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKButton module."""

# Standard Library Imports
from typing import Any, Union

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf, Gtk
from ramstk.views.gtk3.widgets.widget import RAMSTKBaseWidget, WidgetProperties


def do_make_buttonbox(
    view: Any, **kwargs: Any
) -> Union[Gtk.HButtonBox, Gtk.VButtonBox]:
    """Create a buttonbox for RAMSTK views.

    This method creates the base buttonbox used by all RAMSTK Views.  Use a
    buttonbox for a RAMSTK View if there are only buttons to be added.

    :param view: the RAMSTKView this buttonbox will be embedded in.
    :return: _buttonbox
    :rtype: :class:`Gtk.ButtonBox`
    """
    _callbacks = kwargs.get("callbacks", [])
    _height = kwargs.get("height", -1)
    _icons = kwargs.get("icons", [])
    _orientation = kwargs.get("orientation", "vertical")
    _tooltips = kwargs.get("tooltips", [])
    _width = kwargs.get("width", -1)

    if _orientation == "horizontal":
        _buttonbox = Gtk.HButtonBox()
    else:
        _buttonbox = Gtk.VButtonBox()

    _buttonbox.set_layout(Gtk.ButtonBoxStyle.START)

    for _idx, _icon in enumerate(_icons):
        _image = Gtk.Image()
        # FIXME: Need to update this to not access the view's _dic_icons.  Maybe make
        #  that a public dict or pass that dict to this function rather than the view
        #  itself.  Option 2 probably makes most sense.
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            view._dic_icons[_icon], _height, _width
        )
        _image.set_from_pixbuf(_icon)

        _button = Gtk.Button()
        _button.set_image(_image)

        _button.props.width_request = _width
        _button.props.height_request = _height

        try:
            _button.set_tooltip_markup(_tooltips[_idx])
        except IndexError:
            _button.set_tooltip_markup("")

        try:
            _button.connect("clicked", _callbacks[_idx])
        except IndexError:
            _button.set_sensitive(False)

        _buttonbox.pack_start(_button, True, True, 0)

    return _buttonbox


class RAMSTKButton(Gtk.Button, RAMSTKBaseWidget):
    """The RAMSTKButton class."""

    # Define private class attributes.
    _default_height = 30
    _default_width = 200

    def __init__(self, label: str = "...") -> None:
        """Initialize an instance of the RAMSTKButton widget.

        :param label: the text to display on the RAMSTKButton.  Default is an
            ellipsis (...).
        """
        RAMSTKBaseWidget.__init__(self)

        self.label_text = label

        self.set_label(label)
        self.show_all()

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKButton.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKButton.
        """
        super().do_set_properties(properties)

        self.dic_properties["always_show_image"] = properties.get(
            "always_show_image", True
        )
        self.dic_properties["icon"] = properties.get("icon", "none")
        self.dic_properties["use_underline"] = properties.get("use_underline", True)

        self.set_always_show_image(self.dic_properties["always_show_image"])
        self.set_use_underline(self.dic_properties["use_underline"])
        if self.dic_properties["icon"] != "none":
            self.set_label("")
            _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                self.dic_properties["icon"],
                self.dic_properties["height_request"],
                self.dic_properties["width_request"],
            )
            _image = Gtk.Image()
            _image.set_from_pixbuf(_icon)
            self.set_image(_image)
