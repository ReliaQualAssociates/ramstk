# pylint: disable=protected-access, non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.ramstk.Button.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Button Module."""

# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf, GObject, Gtk, _


def do_make_buttonbox(view: Any, **kwargs: Any) -> Gtk.ButtonBox:
    r"""
    Create the buttonbox for RAMSTK Views.

    This method creates the base buttonbox used by all RAMSTK Views.  Use a
    buttonbox for a RAMSTK View if there are only buttons to be added.

    :param view: the RAMSTKView() this buttonbox will be embedded in.
    :type view: :class:`ramstk.views.gtk3.widgets.view.RAMSTKBaseView`

    :param \**kwargs: See below

    :Keyword Arguments:
        * *callbacks* (list) -- list of callback functions to assign to each
            button in the butoonbox.
        * *height* (int) -- height of the Gtk.Button() widget.
            Default is 30.
        * *icons* (list) -- list of the icons to display on each button in the
            buttonbox.
        * *orientation* (str) -- the orientation of the buttonbox, either
            horizontal or vertical.  Default is vertical.
        * *tooltips* (list) -- list of tooltips for each button in the
            buttonbox.
        * *width* (int) -- width of the Gtk.Button() widget.
            Default is 200.

    :return: _buttonbox
    :rtype: :class:`Gtk.ButtonBox`
    """
    try:
        _icons = kwargs['icons']
    except KeyError:
        _icons = []
    try:
        _tooltips = kwargs['tooltips']
    except KeyError:
        _tooltips = []
    try:
        _callbacks = kwargs['callbacks']
    except KeyError:
        _callbacks = []
    try:
        _orientation = kwargs['orientation']
    except KeyError:
        _orientation = 'vertical'
    try:
        _height = kwargs['height']
    except KeyError:
        _height = -1
    try:
        _width = kwargs['width']
    except KeyError:
        _width = -1

    # Append the default save and save-all buttons found on all toolbars to
    # List Views, Module Views, and Work Views.
    try:
        _icons.extend(['save', 'save-all'])
        _tooltips.extend(
            [_("Save the currently selected item."),
             _("Save all items.")])
        _callbacks.extend(
            [view._do_request_update, view._do_request_update_all])
    except AttributeError:
        pass

    if _orientation == 'horizontal':
        _buttonbox = Gtk.HButtonBox()
    else:
        _buttonbox = Gtk.VButtonBox()

    _buttonbox.set_layout(Gtk.ButtonBoxStyle.START)

    i = 0
    for _icon in _icons:
        _image = Gtk.Image()
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(view._dic_icons[_icon],
                                                       _height, _width)
        _image.set_from_pixbuf(_icon)

        _button = Gtk.Button()
        _button.set_image(_image)

        _button.props.width_request = _width
        _button.props.height_request = _height

        try:
            _button.set_tooltip_markup(_tooltips[i])
        except IndexError:
            _button.set_tooltip_markup("")

        try:
            _button.connect('clicked', _callbacks[i])
        except IndexError:
            _button.set_sensitive(False)

        _buttonbox.pack_start(_button, True, True, 0)

        i += 1

    return _buttonbox


class RAMSTKButton(Gtk.Button):
    """This is the RAMSTK Button class."""
    def __init__(self, label: str = "...", **kwargs: Any) -> None:  # pylint: disable=unused-argument
        """
        Initialize an instance of the RAMSTK Button.

        :keyword int height: the height of the Gtk.Button().
            Default is 40.
        :keyword int  width: the width of the Gtk.Button().
            Default is 200.
        :keyword str label: the text to display on the Gtk.Button().
            Default is an ellipsis (...).
        :keyword str icon: the image to display on the Gtk.Button().
        :return: None
        :rtype: None
        """
        GObject.GObject.__init__(self, label=label)
        self.show_all()

    def do_set_properties(self, **kwargs: Any) -> None:
        r"""
        Set the properties of the RAMSTK button.

        :param \**kwargs: See below

        :Keyword Arguments:
            * *height* (int) -- height of the Gtk.Button() widget.
                Default is 30.
            * *icon* (str) -- the icon to display on the button.  Default is
                None.
            * *tooltip* (str) -- the tooltip, if any, for the button.
                Default is an empty string.
            * *width* (int) -- width of the Gtk.Button() widget.
                Default is 200.
        :return: None
        :rtype: None
        """
        try:
            _height = kwargs['height']
        except KeyError:
            _height = 40
        try:
            _icon = kwargs['icon']
        except KeyError:
            _icon = None
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
            _height = 40
        if _width == 0:
            _width = 200

        if _icon is not None:
            _image = Gtk.Image()
            _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                _icon,
                _height,
                _width,
            )
            _image.set_from_pixbuf(_icon)
            self.set_image(_image)

        self.set_property('width-request', _width)
        self.set_property('height-request', _height)
        self.set_property('tooltip-markup', _tooltip)


class RAMSTKCheckButton(Gtk.CheckButton):
    """This is the RAMSTK Check Button class."""
    def __init__(self, label: str = "") -> None:
        """
        Initialize an instance of the RAMSTK CheckButton.

        :keyword str label: the text to display with the Gtk.CheckButton().
            Default is an empty string.
        :return: None
        :rtype: None
        """
        GObject.GObject.__init__(self, label=label, use_underline=True)

    def do_set_properties(self, **kwargs: Any) -> None:
        r"""
        Set the properties of the RAMSTK button.

        :param \**kwargs: See below

        :Keyword Arguments:
            * *height* (int) -- height of the Gtk.Button() widget.
                Default is 40.
            * *tooltip* (str) -- the tooltip, if any, for the button.
                Default is an empty string.
            * *width* (int) -- width of the Gtk.Button() widget.
                Default is 200.
        :return: None
        :rtype: None
        """
        try:
            _height = kwargs['height']
        except KeyError:
            _height = 40
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
            _height = 40
        if _width == 0:
            _width = 200

        self.get_child().set_use_markup(True)
        self.get_child().set_line_wrap(True)
        self.get_child().set_property('height-request', _height)
        self.get_child().set_property('width-request', _width)

        self.set_property('tooltip-markup', _tooltip)

    def do_update(self, value: str, handler_id: int) -> None:
        """
        Update the RAMSTK CheckButton with a new value.

        :param str value: the information to update the RAMSTKCheckButton() to
            display.
        :param int handler_id: the handler ID associated with the
            RAMSTKCheckButton().
        :return: None
        :rtype: None
        """
        with self.handler_block(handler_id):
            self.set_active(int(value))
            self.handler_unblock(handler_id)


class RAMSTKOptionButton(Gtk.RadioButton):
    """This is the RAMSTK Option Button class."""
    def __init__(self, group: Gtk.RadioButton = None,
                 label: str = _("")) -> None:
        """
        Initialize an instance of the RAMSTK OptionButton.

        :keyword group: the group the Gtk.RadioButton() belongs to, if any.
            Default is None.
        :type group: :class:`Gtk.RadioButton`
        :keyword str label: the text to place in the label on the
            Gtk.RadioButton().  Default is an empty string.
        :return: None
        :rtype: None
        """
        GObject.GObject.__init__(self, group=group, label=label)
