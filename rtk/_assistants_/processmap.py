#!/usr/bin/env python
"""
Contains functions for creating the process map navigator.
"""
# TODO: Create this as a new Class.
__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       processmap.py is part of The RTK Project
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

import gettext
import locale
import operator
import string
import sys
import time

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)
import pango

# Import other RTK modules.
try:
    import Configuration as _conf
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.gui.gtk.Widgets as _widg

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ProcessMap(gtk.Window):
    """
    This is the base class for the Process Map.

    :ivar _dicSteps: Dictionary to carry process map step information.
    Key is the step ID; value is a list with the following:

    +-------+------------------------------+
    | Index | Information                  |
    +=======+==============================+
    |   0   | Starting x-position on map   |
    +-------+------------------------------+
    |   1   | Starting y-position on map   |
    +-------+------------------------------+
    |   2   | Ending x-position on map     |
    +-------+------------------------------+
    |   3   | Ending y-position on map     |
    +-------+------------------------------+
    |   4   | Step foreground (text) color |
    +-------+------------------------------+
    |   5   | Step background color        |
    +-------+------------------------------+
    |   6   | Step description             |
    +-------+------------------------------+
    |   7   | RTK Module to activate       |
    +-------+------------------------------+
    |   8   | Work Book page to activate   |
    +-------+------------------------------+
    |   9   | Type of widget to use        |
    +-------+------------------------------+
    """

    def __init__(self, __menuitem, application):

        self._steps = {}

        gtk.Window.__init__(self)
        self.set_title(_(u"RTK Process Map Navigator"))

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        self.set_default_size((_width / 3) - 10, (2 * _height / 7))
        self.maximize()
        self.set_border_width(5)

        self.connect("destroy", lambda w: self.destroy())

        self._app = application

        # Create a layout widget and set it's background color to white.
        self.lytProcessMap = gtk.Layout()
        _map = self.lytProcessMap.get_colormap()
        _color = _map.alloc_color('#FFFFFF')
        _style = self.lytProcessMap.get_style().copy()
        _style.bg[gtk.STATE_NORMAL] = _color
        self.lytProcessMap.set_style(_style)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self.lytProcessMap)

        self.add(_scrollwindow)

        # Parse the process map file and layout the process map.
        _mapfile = _conf.DATA_DIR + '/process.map'
        self._parse_process_map(_mapfile)
        self._layout_process_map()

        self.show_all()

    def _parse_process_map(self, mapfile):
        """
        Method to parse the process map file into instance variables.

        :param str mapfile: the full path to the process map to parse.
        """

        from lxml import etree

        # Retrieve the step identifiers for each step.
        _step_id = etree.parse(mapfile).xpath("/root/map/step/id")

        # Retrieve the x-positions to place the beginning of the widget.
        # This is the upper left corner for a step and the starting
        # x-position for a line.
        _x_start = etree.parse(mapfile).xpath("/root/map/step/xstart")

        # Retrieve the y-positions to place the beginning of the widget.
        # This is the upper left corner for a step and the starting
        # y-position for a line.
        _y_start = etree.parse(mapfile).xpath("/root/map/step/ystart")

        # Retrieve the x-positions to place the ending of the widget.
        # This is the lower right corner for a step and the ending
        # x-position for a line.
        _x_stop = etree.parse(mapfile).xpath("/root/map/step/xstop")

        # Retrieve the y-positions to place the ending of the widget.
        # This is the lower right corner for a step and the ending
        # y-position for a line.
        _y_stop = etree.parse(mapfile).xpath("/root/map/step/ystop")

        # Retrieve the foreground color for each step.
        _foreground = etree.parse(mapfile).xpath("/root/map/step/foreground")

        # Retrieve the background color for each step.
        _background = etree.parse(mapfile).xpath("/root/map/step/background")

        # Retrieve the description for each step.
        _descriptions = etree.parse(mapfile).xpath(
            "/root/map/step/description")

        # Retrieve the module page to select for each step.
        _module = etree.parse(mapfile).xpath("/root/map/step/module")

        # Retrieve the work book page to select for each step.
        _work = etree.parse(mapfile).xpath("/root/map/step/work")

        # Retrieve the type of action for the step.
        _action = etree.parse(mapfile).xpath("/root/map/step/action")

        try:
            _n_steps = len(_descriptions)
        except TypeError:
            _n_steps = 0

        _max_x = 0
        _max_y = 0
        for i in range(_n_steps):
            self._steps[int(_step_id[i].text)] = [
                int(_x_start[i].text),
                int(_y_start[i].text),
                int(_x_stop[i].text),
                int(_y_stop[i].text), _foreground[i].text, _background[i].text,
                _descriptions[i].text,
                int(_module[i].text),
                int(_work[i].text),
                int(_action[i].text)
            ]

            _max_x = max(_max_x, int(_x_stop[i].text) + 10)
            _max_y = max(_max_y, int(_y_stop[i].text) + 10)

        self.lytProcessMap.set_size_request(_max_x, _max_y)

        return False

    def _layout_process_map(self):
        """
        Method to layout the process map.  The process map is a grid with each
        major increment being 100 points.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        for _step in self._steps.keys():
            _x_start = self._steps[_step][0]
            _y_start = self._steps[_step][1]
            _x_end = self._steps[_step][2]
            _y_end = self._steps[_step][3]

            # Create the step.
            if self._steps[_step][9] < 10:
                self._process_step(_step)

            # Create a horizontal line with no arrow.
            elif self._steps[_step][9] == 10:
                _arrow_x_pos = 0
                self._horizontal_line(_x_start, _x_end, _y_start, _arrow_x_pos,
                                      'right')

            # Create a vertical line with no arrow.
            elif self._steps[_step][9] == 11:
                _arrow_y_pos = 0
                self._vertical_line(_x_start, _y_start, _y_end, _arrow_y_pos,
                                    'down')

            # Create a right pointing arrow.
            elif self._steps[_step][9] == 12:
                _arrow_x_pos = _x_end - 15
                self._horizontal_line(_x_start, _x_end, _y_start, _arrow_x_pos,
                                      'right', True)

            # Create a left pointing arrow.
            elif self._steps[_step][9] == 13:
                _arrow_x_pos = _x_start - 5
                self._horizontal_line(_x_start, _x_end, _y_start, _arrow_x_pos,
                                      'left', True)

            # Create a down pointing arrow.
            elif self._steps[_step][9] == 14:
                _arrow_y_pos = _y_end - 55
                self._vertical_line(_x_start, _y_start, _y_end, _arrow_y_pos,
                                    'down', True)

            # Create an up pointing arrow.
            elif self._steps[_step][9] == 15:
                _arrow_y_pos = _y_start - 50
                self._vertical_line(_x_start, _y_start, _y_end, _arrow_y_pos,
                                    'up', True)

            # Create a label.
            elif self._steps[_step][9] == 20:
                self._label(_step)

        return False

    def _process_step(self, step):
        """
        Method to create a process step symbol.

        :param int step: the ID number of the step to create.
        :return: step widget.
        :rtype: gtk.Button
        """

        _x_start = self._steps[step][0]
        _y_start = self._steps[step][1]
        _x_end = self._steps[step][2]
        _y_end = self._steps[step][3]
        _w = _x_end - _x_start
        _h = _y_end - _y_start

        # Create the widget for the step.
        _step = gtk.Button(label=None)
        _step.set_relief(gtk.RELIEF_HALF)
        _step.set_size_request(_w, _h)

        # Set the text in the step.
        _label = gtk.Label()
        _label.props.wrap_mode = pango.WRAP_WORD_CHAR
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_line_wrap(True)
        _label.set_width_chars(20)
        _label.set_markup(
            u"<span weight='bold'>%s</span>" % self._steps[step][6])
        _step.add(_label)

        # Make the background color for the step.
        _map = _step.get_colormap()
        _color = _map.alloc_color(self._steps[step][5])

        # Copy the current step style and replace the background.
        _style = _step.get_style().copy()
        _style.bg[gtk.STATE_NORMAL] = _color

        # Set the step's style to the one just created.
        _step.set_style(_style)

        # Place the step.
        self.lytProcessMap.put(_step, _x_start, _y_start)

        # Connect the step to the callback method unless it is a
        # non-interactive type step.
        if self._steps[step][9] == 1:
            _step.connect('clicked', self._step_select, self._steps[step][7],
                          self._steps[step][8])
        else:
            _step.set_sensitive(False)

        return _step

    def _horizontal_line(self,
                         x_start,
                         x_end,
                         y_start,
                         arrow_x_pos,
                         direction,
                         arrow=False):
        """
        Method to create a horizontal line.

        :param int x_start: the starting x-position of the line.
        :param int x_end: the ending x-position of the line.
        :param int y_start: the starting y-position of the line.
        :param int arrow_x_pos: the x-position of the arrow.
        :param str direction: the direction for the arrow on the line to point.
        :keyword boolean arrow: indicates whether or not to terminate the line
                                with an arrow head.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _w = x_end - x_start

        # Create the line.
        _line = gtk.HSeparator()
        _line.set_size_request(_w, 10)

        # Make the line black.
        _map = _line.get_colormap()
        _color = _map.alloc_color('#000000')

        # Copy the current line style and replace the background.
        _style = _line.get_style().copy()
        _style.bg[gtk.STATE_NORMAL] = _color

        # Set the line's style to the style just created.
        _line.set_style(_style)

        # Place the line.
        self.lytProcessMap.put(_line, x_start, y_start)

        # Place the arrow if applicable.
        if arrow:
            if direction == 'right':
                _arrow = gtk.Arrow(gtk.ARROW_RIGHT, gtk.SHADOW_ETCHED_IN)
            elif direction == 'left':
                _arrow = gtk.Arrow(gtk.ARROW_LEFT, gtk.SHADOW_ETCHED_IN)

            _arrow_width = 20
            _arrow_height = 20
            _arrow_y_pos = y_start - 5

            _arrow.set_size_request(_arrow_width, _arrow_height)

            self.lytProcessMap.put(_arrow, arrow_x_pos, _arrow_y_pos)

        return False

    def _vertical_line(self,
                       x_start,
                       y_start,
                       y_end,
                       arrow_y_pos,
                       direction,
                       arrow=False):
        """
        Method to create a vertical line.

        :param int x_start: the starting x-position of the line.
        :param int y_start: the starting y-position of the line.
        :param int y_end: the ending y-position of the line.
        :param int arrow_y_pos: the y-position of the arrow.
        :param str direction: the direction for the line to point (up or down).
        :keyword boolean arrow: indicates whether or not to terminate the line
                                with an arrow head.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _h = y_end - y_start

        # Create the line.
        _line = gtk.VSeparator()
        _line.set_size_request(10, _h)

        # Make the line black.
        _map = _line.get_colormap()
        _color = _map.alloc_color('#000000')

        # Copy the current line style and replace the background.
        _style = _line.get_style().copy()
        _style.bg[gtk.STATE_NORMAL] = _color

        # Set the line's style to the style just created.
        _line.set_style(_style)

        # Place the line.
        self.lytProcessMap.put(_line, x_start, y_start)

        # Place the arrow if applicable.
        if arrow:
            if direction == 'down':
                _arrow = gtk.Arrow(gtk.ARROW_DOWN, gtk.SHADOW_ETCHED_IN)
            elif direction == 'up':
                _arrow = gtk.Arrow(gtk.ARROW_UP, gtk.SHADOW_ETCHED_IN)

            _arrow_width = 20
            _arrow_height = 100
            _arrow_x_pos = x_start - 5

            _arrow.set_size_request(_arrow_width, _arrow_height)

            self.lytProcessMap.put(_arrow, _arrow_x_pos, arrow_y_pos)

        return False

    def _label(self, step):
        """
        Method to create a label to place on the map.

        :param int step: the ID number of the step to create.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _x_start = self._steps[step][0]
        _y_start = self._steps[step][1]
        _x_end = self._steps[step][2]
        _y_end = self._steps[step][3]
        _text = self._steps[step][6]
        _w = _x_end - _x_start
        _h = _y_end - _y_start

        # Create the label.
        _label = _widg.make_label(_text, _w, _h, wrap=True)
        _event_box = gtk.EventBox()
        _event_box.add(_label)

        # Make the background color for the label.
        _map = _event_box.get_colormap()
        _color = _map.alloc_color(self._steps[step][5])

        # Copy the current label style and replace the background.
        _style = _event_box.get_style().copy()
        _style.bg[gtk.STATE_NORMAL] = _color

        # Set the step's style to the one just created.
        _event_box.set_style(_style)

        # Place the step.
        self.lytProcessMap.put(_event_box, _x_start, _y_start)

        return False

    def _step_select(self, button, module, work):
        """
        Method to select the Module Book page and Work Book page for the step
        in the process that was clicked.

        :param gtk.Button button: the gtk.Button() that represents the step.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        self._app.winTree.notebook.set_current_page(module)

        if module == 0:
            self._app.REVISION.notebook.set_current_page(work)
        elif module == 1:
            self._app.FUNCTION.notebook.set_current_page(work)
        elif module == 2:
            self._app.REQUIREMENT.notebook.set_current_page(work)
        elif module == 3:
            self._app.HARDWARE.notebook.set_current_page(work)
        elif module == 4:
            self._app.SOFTWARE.notebook.set_current_page(work)
        elif module == 5:
            self._app.VALIDATION.notebook.set_current_page(work)
        elif module == 6:
            self._app.TESTING.notebook.set_current_page(work)
        elif module == 7:
            self._app.INCIDENT.notebook.set_current_page(work)
        elif module == 8:
            self._app.DATASET.notebook.set_current_page(work)
