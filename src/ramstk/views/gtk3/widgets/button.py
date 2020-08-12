# pylint: disable=protected-access, non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.ramstk.Button.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Button Module."""

# Standard Library Imports
from typing import Any, Union

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf, Gtk, _

# RAMSTK Local Imports
from .widget import RAMSTKWidget


def do_make_buttonbox(view: Any,
                      **kwargs: Any) -> Union[Gtk.HButtonBox, Gtk.VButtonBox]:
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
    except AttributeError as _error:
        #// TODO: Handle AttributeError in do_make_buttonbox().
        #//
        #// This error is a programming error not a runtime error.  It would
        #// be the result of a view not having an icon or callback function in
        #// the default list.  The solution should be to ensure the icons and
        #// functions lists above are in the base view for each type of view.
        print(_error)

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
        except IndexError as _error:
            _button.set_sensitive(False)

        _buttonbox.pack_start(_button, True, True, 0)

        i += 1

    return _buttonbox


class RAMSTKButton(Gtk.Button, RAMSTKWidget):
    """This is the RAMSTK Button class."""

    # Define private class scalar attributes.
    _default_height = 30
    _default_width = 200

    def __init__(self, label: str = "...") -> None:
        """
        Initialize an instance of the RAMSTKButton().

        :keyword str label: the text to display on the RAMSTKButton().
            Default is an ellipsis (...).
        :return: None
        :rtype: None
        """
        # noinspection PyCallByClass,PyTypeChecker
        RAMSTKWidget.__init__(self)

        self.set_label(label)
        self.show_all()

    def do_set_properties(self, **kwargs: Any) -> None:
        r"""
        Set the properties of the RAMSTKButton.

        :param \**kwargs: See below

        :Keyword Arguments:
            * *height* (int) -- height of the RAMSTKButton() widget.
                Default is 30.
            * *icon* (str) -- the icon to display on the button.  Default is
                None.
            * *tooltip* (str) -- the tooltip, if any, for the button.
                Default is a message to file a QA-type issue to have one added.
            * *width* (int) -- width of the RAMSTKButton() widget.
                Default is 200.
        :return: None
        :rtype: None
        """
        super().do_set_properties(**kwargs)

        try:
            _icon = kwargs['icon']
        except KeyError:
            _icon = None

        if _icon is not None:
            _image = Gtk.Image()
            _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                _icon,
                self.height,
                self.width,
            )
            _image.set_from_pixbuf(_icon)
            self.set_image(_image)


class RAMSTKCheckButton(Gtk.CheckButton, RAMSTKWidget):
    """This is the RAMSTK Check Button class."""

    # Define private class scalar attributes.
    _default_height = 20
    _default_width = 200

    def __init__(self, label: str = "") -> None:
        """
        Initialize an instance of the RAMSTK CheckButton.

        :keyword str label: the text to display with the Gtk.CheckButton().
            Default is an empty string.
        :return: None
        :rtype: None
        """
        # noinspection PyCallByClass,PyTypeChecker
        RAMSTKWidget.__init__(self)

        self.set_label(label)

    def do_set_properties(self, **kwargs: Any) -> None:
        r"""
        Set the properties of the RAMSTK button.

        :param \**kwargs: See below

        :Keyword Arguments:
            * *height* (int) -- height of the RAMSTKCheckButton() widget.
                Default is 40.
            * *tooltip* (str) -- the tooltip, if any, for the button.
                Default is a message to file a QA-type issue to have one added.
            * *width* (int) -- width of the RAMSTKCheckButton() widget.
                Default is 200.
        :return: None
        :rtype: None
        """
        super().do_set_properties(**kwargs)

        self.set_use_underline(True)
        self.get_child().set_use_markup(True)
        self.get_child().set_line_wrap(True)
        self.get_child().set_property('height-request', self.height)
        self.get_child().set_property('width-request', self.width)

    def do_update(self, value: int, signal: str = '') -> None:
        """
        Update the RAMSTK CheckButton with a new value.

        :param int value: the information to update the RAMSTKCheckButton() to
            display.
        :keyword str signal: the name of the signal whose handler ID the
            RAMSTKCheckButton() needs to block.
        :return: None
        :rtype: None
        """
        _handler_id = self.dic_handler_id[signal]

        self.handler_block(_handler_id)
        self.set_active(int(value))
        self.handler_unblock(_handler_id)


class RAMSTKOptionButton(Gtk.RadioButton, RAMSTKWidget):
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
        # noinspection PyCallByClass,PyTypeChecker
        RAMSTKWidget.__init__(self)

        self.set_group(group)
        self.set_label(label)


class RAMSTKSpinButton(Gtk.SpinButton, RAMSTKWidget):
    """This is the RAMSTK Spin Button class."""

    # Define private class scalar attributes.
    _default_height = 30
    _default_width = 200

    def __init__(self) -> None:
        """
        Initialize an instance of the RAMSTKSpinButton().

        :return: None
        :rtype: None
        """
        # noinspection PyCallByClass,PyTypeChecker
        RAMSTKWidget.__init__(self)

        self.show_all()

    def do_set_properties(self, **kwargs: Any) -> None:
        r"""
        Set the properties of the RAMSTKSpinButton.

        :param \**kwargs: See below

        :Keyword Arguments:
            * *height* (int) -- height of the RAMSTKButton() widget.
                Default is 30.
            * *limits* (list) -- the list of values for the spin button
                Gtk.Adjustment().
            * *tooltip* (str) -- the tooltip, if any, for the button.
                Default is a message to file a QA-type issue to have one added.
            * *width* (int) -- width of the RAMSTKButton() widget.
                Default is 200.
        :return: None
        :rtype: None
        """
        super().do_set_properties(**kwargs)

        try:
            _limits = kwargs['limits']
        except KeyError:
            _limits = [0, 0, 100, 1, 0.1]
        try:
            _numeric = kwargs['numeric']
        except KeyError:
            _numeric = True
        try:
            _snap_to_ticks = kwargs['ticks']
        except KeyError:
            _snap_to_ticks = True

        self.set_adjustment(
            Gtk.Adjustment(_limits[0], _limits[1], _limits[2], _limits[3],
                           _limits[4]))
        self.set_numeric(_numeric)
        self.set_snap_to_ticks(_snap_to_ticks)
        self.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)

    def do_update(self, value: int, signal: str = '') -> None:
        """
        Update the RAMSTK Spin Button with a new value.

        :param int value: the information to update the RAMSTKSpinButton() to
            display.
        :keyword str signal: the name of the signal whose handler ID the
            RAMSTKSpinButton() needs to block.
        :return: None
        :rtype: None
        """
        _handler_id = self.dic_handler_id[signal]

        self.handler_block(_handler_id)
        self.set_value(int(value))
        self.handler_unblock(_handler_id)
