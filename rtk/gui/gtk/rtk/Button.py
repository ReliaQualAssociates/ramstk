# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Button.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
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

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class RTKCheckButton(CheckButton):
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

        CheckButton.__init__(self, label=label, use_underline=True)

        self.set_tooltip_markup(tooltip)

        self.get_child().set_use_markup(True)
        self.get_child().set_line_wrap(True)
        self.get_child().props.width_request = width


class RTKOptionButton(RadioButton):
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

        RadioButton.__init__(self, group=btngroup, label=btnlabel)


class RTKButton(Button):
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
        :return: None
        """

        Button.__init__(self, label=label)

        if width == 0:
            width = 200

        if icon is not None:
            _image = Image()
            _image.set_from_file(icon)
            self.set_image(_image)

        self.props.width_request = width
        self.props.height_request = height

        self.show_all()
