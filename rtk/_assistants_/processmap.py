#!/usr/bin/env python
"""
Contains functions for creating analysis reports.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       processmap.py is part of The RTK Project
#
# All rights reserved.

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
import configuration as _conf

_ = gettext.gettext


class ProcessMap(gtk.Window):
    """
    This is the base class for the Process Map.
    """

    def __init__(self, __menuitem, application):

        self._steps = {}

        gtk.Window.__init__(self)
        self.set_title(_(u"Process Map Navigator"))

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        self.set_default_size((_width / 3) - 10, (2 * _height / 7))
        self.set_border_width(5)

        self.connect("destroy", lambda w: self.destroy())

        self._app = application

        self.lytProcessMap = gtk.Layout()
        self.lytProcessMap.set_size_request(1000, 1000)

        _scrollwindow = gtk.ScrolledWindow()
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

        # Retrieve the x-positions for each step.
        _x_pos = etree.parse(mapfile).xpath("/root/map/step/xposition")

        # Retrieve the y-positions for each step.
        _y_pos = etree.parse(mapfile).xpath("/root/map/step/yposition")

        # Retrieve the widths for each step.
        _width = etree.parse(mapfile).xpath("/root/map/step/width")

        # Retrieve the heights for each step.
        _height = etree.parse(mapfile).xpath("/root/map/step/height")

        # Retrieve the foreground color for each step.
        _foreground = etree.parse(mapfile).xpath("/root/map/step/foreground")

        # Retrieve the background color for each step.
        _background = etree.parse(mapfile).xpath("/root/map/step/background")

        # Retrieve the description for each step.
        _descriptions = etree.parse(mapfile).xpath("/root/map/step/description")

        # Retrieve the module page to select for each step.
        _module = etree.parse(mapfile).xpath("/root/map/step/module")

        # Retrieve the work book page for each step.
        _work = etree.parse(mapfile).xpath("/root/map/step/work")

        # Retrieve the step id to connect to.
        _next_step = etree.parse(mapfile).xpath("/root/map/step/connect")

        try:
            _n_steps = len(_descriptions)
        except TypeError:
            _n_steps = 0

        for i in range(_n_steps):
            try:
                _connect = int(_next_step[i].text)
            except TypeError:
                _connect = -1

            self._steps[int(_step_id[i].text)] = [int(_x_pos[i].text),
                                                  int(_y_pos[i].text),
                                                  int(_width[i].text),
                                                  int(_height[i].text),
                                                  _foreground[i].text,
                                                  _background[i].text,
                                                  _descriptions[i].text,
                                                  int(_module[i].text),
                                                  int(_work[i].text),
                                                  _connect]

        return False

    def _layout_process_map(self):
        """
        Method to layout the process map.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        for _key in self._steps.keys():
            # Create the step.
            _step = gtk.Button(label=None)
            _step.set_relief(gtk.RELIEF_HALF)
            _step.set_size_request(self._steps[_key][2], self._steps[_key][3])

            # Make the background color for the step.
            _map = _step.get_colormap()
            _color = _map.alloc_color(self._steps[_key][5])

            # Copy the current step style and replace the background.
            _style = _step.get_style().copy()
            _style.bg[gtk.STATE_NORMAL] = _color

            # Set the step's style to the one just created.
            _step.set_style(_style)

            # Set the text in the step.
            _label = gtk.Label()
            _label.props.wrap_mode = pango.WRAP_WORD_CHAR
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_line_wrap(True)
            _label.set_width_chars(20)
            _label.set_markup("<span weight='bold'>" +
                              self._steps[_key][6] + "</span>")
            _step.add(_label)

            # Create the lines and arrows that connect the steps together.
            _connect_to = self._steps[_key][9]
            if _connect_to != -1:

                if self._steps[_key][0] == self._steps[_connect_to][0]:
                    _direction = gtk.ARROW_DOWN

                    # Create a vertical line.
                    _line = gtk.VSeparator()
                    _line_width = 10
                    _line_height = int(0.5 * self._steps[_key][3])

                    _line_x_pos = self._steps[_key][0] + \
                                  int(0.5 * self._steps[_key][2])
                    _line_y_pos = self._steps[_key][1] + self._steps[_key][3]

                    _arrow_width = 20
                    _arrow_height = 100
                    _arrow_x_pos = _line_x_pos - 5
                    _arrow_y_pos = _line_y_pos

                elif self._steps[_key][0] < self._steps[_connect_to][0]:
                    _direction = gtk.ARROW_RIGHT

                    # Create a horizontal line.
                    _line = gtk.HSeparator()
                    _line_width = int(0.5 * self._steps[_key][2])
                    _line_height = 10

                    _line_x_pos = self._steps[_key][0] + self._steps[_key][2]
                    _line_y_pos = self._steps[_key][1] + \
                                  int(0.5 * self._steps[_key][3])

                    _arrow_width = 20
                    _arrow_height = 20
                    _arrow_x_pos = self._steps[_connect_to][0] - 13
                    _arrow_y_pos = _line_y_pos - 5

                #elif (self._steps[_key][0] != self._steps[_connect_to][0] and
                #      self._steps[_key][1] != self._steps[_connect_to][1]):
                #    _direction = gtk.ARROW_LEFT

                _arrow = gtk.Arrow(_direction, gtk.SHADOW_ETCHED_IN)
                _arrow.set_size_request(_arrow_width, _arrow_height)

                # Make the line black.
                _line.set_size_request(_line_width, _line_height)
                _map = _line.get_colormap()
                _color = _map.alloc_color('#000000')

                # Copy the current line style and replace the background.
                _style = _line.get_style().copy()
                _style.bg[gtk.STATE_NORMAL] = _color

                # Set the line's style to the style just created.
                _line.set_style(_style)

                # Place the lines and arrows.
                self.lytProcessMap.put(_line, _line_x_pos, _line_y_pos)
                self.lytProcessMap.put(_arrow, _arrow_x_pos, _arrow_y_pos)

            # Place the step.
            self.lytProcessMap.put(_step, self._steps[_key][0],
                                   self._steps[_key][1])

            # Connect the step to the callback method.
            _step.connect('clicked', self._step_select,
                          self._steps[_key][7], self._steps[_key][8])

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
