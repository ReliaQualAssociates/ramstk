#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Button.py is part of the RTK Project
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
application.  This module is specific to button widgets.
"""

import gettext
import sys

# Modules required for the GUI.
try:
    from pygtk import require
    require('2.0')
except ImportError:
    sys.exit(1)
try:
    from gtk import Button, RadioButton, Image, CheckButton
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


class RTKCheckButton(gtk.CheckButton):
    """
    This is the RTK CheckButton class.
    """

    def __init__(self, label="", width=-1,
                 tooltip='RTK WARNING: Missing tooltip.  '
                         'Please register an Enhancement type bug.'):
        """
        Method to create CheckButton widgets.

        :keyword str label: the text to display with the gtk.CheckButton().
                            Default is an empty string.
        :keyword int width: the desired width of the gtk.CheckButton().
                            Default is -1 or a natural request.
        :keyword str tooltip: the tooltip to display when hovering over the
                              CheckButton.
        :return: _checkbutton
        :rtype: :py:class:`gtk.CheckButton`
        """

        gtk.CheckButton.__init__(self, label=label, use_underline=True)

        self.set_tooltip_markup(tooltip)

        self.get_child().set_use_markup(True)
        self.get_child().set_line_wrap(True)
        self.get_child().props.width_request = width


class RTKOptionButton(gtk.RadioButton):
    """
    This is the RTK OptionButton class.
    """

    def __init__(self, btngroup=None, btnlabel=_(u"")):
        """
        Method to create OptionButton widgets.

        :keyword str btngroup: the group the gtk.RadioButton() belongs to, if
                               any.  Default is None.
        :keyword str btnlabel: the text to place in the label on the
                               gtk.RadioButton().  Default is an empty string.
        :return: _optbutton
        :rtype: :py:class:`gtk.RadioButton`
        """

        gtk.RadioButton.__init__(self, group=btngroup, label=btnlabel)


class RTKButton(gtk.Button):
        """
        This is the RTK Button class.
        """

        def __init__(self, height=40, width=200, label="", icon=None):
            """
            Method to create Button widgets.

            :keyword int height: the height of the gtk.Button().
                                 Default is 40.
            :keyword int  width: the width of the gtk.Button().
                                 Default is 200.
            :keyword str label: the text to display on the gtk.Button().
                                Default is an empty string.
            :keyword str icon: the image to display on the gtk.Button().
                               Options for this argument are:

                                - add
                                - assign
                                - calculate
                                - commit
                                - default (default)

            :return: _button
            :rtype: :py:class:`gtk.Button`
            """

            gtk.Button.__init__(self, label=label)

            if width == 0:
                width = 200

            if icon is not None:
                _image = Image()
                _image.set_from_file(icon)
                self.set_image(_image)

            self.props.width_request = width
            self.props.height_request = height
