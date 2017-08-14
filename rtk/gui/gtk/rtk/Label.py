#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Label.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This module contains functions for creating, populating, destroying, and
interacting with pyGTK widgets.  Import this module in other modules that
create, populate, destroy, or interact with pyGTK widgets in the RTK
application.  This module is specific to label widgets.
"""

import gettext
import sys

# Modules required for the GUI.
import pango
try:
    from pygtk import require
    require('2.0')
except ImportError:
    sys.exit(1)
try:
    from gtk import JUSTIFY_LEFT, JUSTIFY_CENTER, Label
except ImportError:
    sys.exit(1)
try:
    import gtk.glade  # @UnusedImport
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

_ = gettext.gettext


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

    for __, label_text in enumerate(text):
        _label = RTKLabel(label_text, width=-1, height=-1, wrap=wrap)
        _max_x = max(_max_x, _label.size_request()[0])
        container.put(_label, x_pos, y_pos)
        _lst_y_pos.append(y_pos)
        y_pos += max(_label.size_request()[1], y_inc) + 5

    return _max_x, _lst_y_pos


class RTKLabel(gtk.Label):
    """
    This is the RTK Label class.
    """

    def __init__(self, text, width=190, height=25, bold=True, wrap=False,
                 justify=JUSTIFY_LEFT,
                 tooltip='RTK WARNING: Missing tooltip.  '
                         'Please register an Enhancement type bug.'):
        """
        Function to create gtk.Label() widgets.

        :param str text: the text to display in the gtk.Label() widget.
        :param int width: width of the gtk.Label() widget.  Default is 190.
        :param int height: height of the gtk.Label() widget.  Default is 25.
        :param bool bold: boolean indicating whether text should be bold.
                          Default is True.
        :param bool wrap: boolean indicating whether the label text should wrap
                          or not.
        :param justify: the justification type when the label wraps and
                        contains more than one line.  Default is
                        gtk.JUSTIFY_LEFT.
        :type justify: GTK Justification Constant
        """

        gtk.Label.__init__(self)

        self.set_markup("<span>" + text + "</span>")
        self.set_line_wrap(wrap)
        self.set_justify(justify)
        self.set_tooltip_markup(tooltip)
        if justify == JUSTIFY_CENTER:
            self.set_alignment(xalign=0.5, yalign=0.5)
        elif justify == JUSTIFY_LEFT:
            self.set_alignment(xalign=0.05, yalign=0.5)
        else:
            self.set_alignment(xalign=0.95, yalign=0.5)
        self.props.width_request = width
        self.props.height_request = height

        if not bold:
            self.modify_font(pango.FontDescription('normal'))
        else:
            self.modify_font(pango.FontDescription('bold'))

        self.show_all()
