# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Label.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
This module contains functions for creating, populating, destroying, and
interacting with pyGTK widgets.  Import this module in other modules that
create, populate, destroy, or interact with pyGTK widgets in the RTK
application.  This module is specific to RTK label widgets.
"""

# Import the rtk.Widget base class.
from .Widget import gtk, pango                      # pylint: disable=E0401


def make_label_group(text, container, x_pos, y_pos, y_inc=25, wrap=True):
    """
    Function to make and place a group of labels.  The width of each label is
    set using a natural request.  This ensures the label doesn't cut off
    letters.  The maximum size of the labels is determined and used to set the
    left position of widget displaying the data described by the label.  This
    ensures everything lines up.  It also returns a list of y-coordinates
    indicating the placement of each label that is used to place the
    corresponding widget.

    :param list text: a list containing the text for each label.
    :param gtk.Widget container: the container widget to place the labels in.
    :param int x_pos: the x position in the container for the left edge of all
                      labels.
    :param int y_pos: the y position in the container of the first label.
    :keyword int y_inc: the amount to increment the y_pos between each label.
    :keyword boolean wrap: boolean indicating whether the label text should
                           wrap or not.
    :return: (_int_max_x, _lst_y_pos)
             the width of the label with the longest text and a list of the y
             position for each label in the container.  Use this list to place
             gtk.Entry(), gtk.ComboBox(), etc. so they line up with their
             associated label.
    :rtype: tuple of (integer, list of integers)
    """

    _lst_y_pos = []
    _max_x = 0

    _char_width = max([len(_label_text) for _label_text in text])

    for __, _label_text in enumerate(text):
        _label = RTKLabel(_label_text, width=-1, height=-1, wrap=wrap,
                          justify=gtk.JUSTIFY_RIGHT)
        _label.set_width_chars(_char_width)
        _max_x = max(_max_x, _label.size_request()[0])
        container.put(_label, x_pos, y_pos)
        _lst_y_pos.append(y_pos)
        y_pos += max(_label.size_request()[1], y_inc) + 5

    return _max_x, _lst_y_pos


class RTKLabel(gtk.Label):
    """
    This is the RTK Label class.
    """
    # pylint: disable=R0913
    def __init__(self, text, width=190, height=25, bold=True, wrap=False,
                 justify=gtk.JUSTIFY_LEFT,
                 tooltip='RTK WARNING: Missing tooltip.  '
                         'Please register an Enhancement type bug.'):
        """
        Method to create Label() widgets.

        :param str text: the text to display in the gtk.Label() widget.
        :param int width: width of the gtk.Label() widget.  Default is 190.
        :param int height: height of the gtk.Label() widget.  Default is 25.
        :param bool bold: boolean indicating whether text should be bold.
                          Default is True.
        :param bool wrap: boolean indicating whether the label text should wrap
                          or not.
        :param justify: the justification type when the label wraps and
                        contains more than one line.  Default is
                        JUSTIFY_LEFT.
        :type justify: GTK Justification Constant
        """

        gtk.Label.__init__(self)

        self.set_markup("<span>" + text + "</span>")
        self.set_line_wrap(wrap)
        self.set_justify(justify)
        self.set_tooltip_markup(tooltip)
        if justify == gtk.JUSTIFY_CENTER:
            self.set_alignment(xalign=0.5, yalign=0.5)
        elif justify == gtk.JUSTIFY_LEFT:
            self.set_alignment(xalign=0.05, yalign=0.5)
        else:
            self.set_alignment(xalign=0.99, yalign=0.5)
        self.props.width_request = width
        self.props.height_request = height

        if not bold:
            self.modify_font(pango.FontDescription('normal'))
        else:
            self.modify_font(pango.FontDescription('bold'))

        self.show_all()
