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
        self.lytProcessMap.set_size_request(650, 500)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add_with_viewport(self.lytProcessMap)

        self.add(_scrollwindow)

        self._layout_process_map()

        self.show_all()

    def _layout_process_map(self):
        """
        Method to layout the process map.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _results = [(10, 10, 200, 100, '#000000', '#C5F1FF',
                     "Gather stakeholder inputs", 2, 0),
                    (10, 165, 200, 100, '#000000', '#E5E5E5',
                     "Define system reliability requirements", 2, 1),
                    (10, 320, 200, 100, '#000000', '#E5E5E5',
                     "Allocate system reliability requirement", 3, 1),
                    (10, 475, 200, 100, '#000000', '#E5E5E5',
                     "Validate sub-system reliability requirements", 2, 2 )]
        try:
            _n_steps = len(_results)
        except TypeError:
            _n_steps = 0

        for i in range(_n_steps):
            # Create the step.
            _step = gtk.Button(label=None)
            _step.set_relief(gtk.RELIEF_HALF)
            _step.set_size_request(_results[i][2], _results[i][3])

            # Make the background color for the step.
            _map = _step.get_colormap()
            _color = _map.alloc_color(_results[i][5])

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
                              _results[i][6] + "</span>")
            _step.add(_label)

            # Create the
            _arrow = gtk.Arrow(gtk.ARROW_DOWN, gtk.SHADOW_ETCHED_IN)
            _arrow.set_size_request(20, 100)
            _line = gtk.VSeparator()
            _line.set_size_request(10, int(0.5 * _results[i][3]))

            # Make the color for the line.
            _map = _line.get_colormap()
            _color = _map.alloc_color(_results[i][4])

            # Copy the current line style and replace the background.
            _style = _line.get_style().copy()
            _style.bg[gtk.STATE_NORMAL] = _color

            # Set the line's style to the one just created.
            _line.set_style(_style)

            # Place the step.
            self.lytProcessMap.put(_step, _results[i][0], _results[i][1])
            self.lytProcessMap.put(_line, _results[i][0] + int(0.5 * _results[i][2]), _results[i][1] + _results[i][3])
            self.lytProcessMap.put(_arrow, _results[i][0] + int(0.5 * _results[i][2]) - 5, _results[i][1] + _results[i][3])

            # Connect the step to the callback method.
            _step.connect('clicked', self._step_select, _results[i][7],
                          _results[i][8])

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
