# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.Label.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Label Module."""

# RAMSTK Local Imports
# Import the ramstk.Widget base class.
from .Widget import GObject, Gtk, Pango


def do_make_label_group(text, container, x_pos, y_pos, **kwargs):
    r"""
    Make and place a group of labels.

    The width of each label is set using a natural request.  This ensures the
    label doesn't cut off letters.  The maximum size of the labels is
    determined and used to set the left position of widget displaying the data
    described by the label.  This ensures everything lines up.  It also returns
    a list of y-coordinates indicating the placement of each label that is used
    to place the corresponding widget.

    :param list text: a list containing the text for each label.
    :param Gtk.Widget container: the container widget to place the labels in.
    :param int x_pos: the x position in the container for the left edge of all
                      labels.
    :param int y_pos: the y position in the container of the first label.
    :param \**kwargs: See below

        :Keyword Arguments:
            * *y_inc* (int) -- the amount to increment the y_pos between each
                               label.
            * *wrap* (bool) -- boolean indicating whether the label text should
                               wrap or not.

    :return: (_int_max_x, _lst_y_pos)
             the width of the label with the longest text and a list of the y
             position for each label in the container.  Use this list to place
             Gtk.Entry(), Gtk.ComboBox(), etc. so they line up with their
             associated label.
    :rtype: tuple of (integer, list of integers)
    """
    try:
        _y_inc = kwargs['y_inc']
    except KeyError:
        _y_inc = 25
    try:
        _wrap = kwargs['wrap']
    except KeyError:
        _wrap = True

    _lst_y_pos = []
    _max_x = 0

    _char_width = max([len(_label_text) for _label_text in text])

    for __, _label_text in enumerate(text):
        _label = RAMSTKLabel(
            _label_text,
            width=-1,
            height=-1,
            wrap=_wrap,
            justify=Gtk.Justification.RIGHT,
        )
        _label.set_width_chars(_char_width)
        _max_x = max(_max_x, _label.get_preferred_size()[0].width)
        container.put(_label, x_pos, y_pos)
        _lst_y_pos.append(y_pos)
        y_pos += max(_label.get_preferred_size()[0].height, _y_inc) + 5

    return _max_x, _lst_y_pos


class RAMSTKLabel(Gtk.Label):
    """This is the RAMSTK Label class."""

    # pylint: disable=R0913
    def __init__(self, text, **kwargs):
        r"""
        Create RAMSTK Label widgets.

        :param str text: the text to display in the Gtk.Label() widget.
        :param \**kwargs: See below

        :Keyword Arguments:
            * *width* (int) -- width of the Gtk.Label() widget.
                               Default is 190.
            * *height* (int) -- height of the Gtk.Label() widget.
                                Default is 25.
            * *bold* (bool) -- boolean indicating whether text should be bold.
                               Default is True.
            * *wrap* (bool) -- boolean indicating whether the label text should
                               wrap or not.
                               Default is False.
            * *justify* (str) -- the justification type when the label wraps
                                 and contains more than one line.
                                 Default is JUSTIFY_LEFT.
            * *tooltip* (str) -- the tooltip, if any, for the label.
                                 Default is an empty string.
        """
        GObject.GObject.__init__(self)

        try:
            _bold = kwargs['bold']
        except KeyError:
            _bold = True
        try:
            _height = kwargs['height']
        except KeyError:
            _height = 25
        try:
            _justify = kwargs['justify']
        except KeyError:
            _justify = Gtk.Justification.LEFT
        try:
            _tooltip = kwargs['tooltip']
        except KeyError:
            _tooltip = ''
        try:
            _width = kwargs['width']
        except KeyError:
            _width = 190
        try:
            _wrap = kwargs['wrap']
        except KeyError:
            _wrap = False

        self.set_markup("<span>" + text + "</span>")
        self.set_line_wrap(_wrap)
        self.set_justify(_justify)
        self.set_tooltip_markup(_tooltip)
        if _justify == Gtk.Justification.CENTER:
            self.set_alignment(xalign=0.5, yalign=0.5)
        elif _justify == Gtk.Justification.LEFT:
            self.set_alignment(xalign=0.05, yalign=0.5)
        else:
            self.set_alignment(xalign=0.99, yalign=0.5)
        self.props.width_request = _width
        self.props.height_request = _height

        if not _bold:
            self.modify_font(Pango.FontDescription('normal'))
        else:
            self.modify_font(Pango.FontDescription('bold'))

        self.show_all()

    def get_attribute(self, attribute):
        """
        Get the value of the requested attribute.

        :param str attribute: the name of the attribute to retrieve.
        :return: the value of the requested attribute.
        """
        # The natural size = default size and the requested size = minimum size.
        _attributes = {
            'height': self.get_preferred_size()[1].height,
            'width': self.get_preferred_size()[1].width,
        }

        return _attributes[attribute]
