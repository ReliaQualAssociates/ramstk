# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.mwi.WorkBook.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
PyGTK Multi-Window Interface Work Book
===============================================================================
"""

import sys

# Import modules for localization support.
import gettext
import locale

from pubsub import pub                              # pylint: disable=E0401

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

# Import other RTK modules.
# pylint: disable=E0401
from gui.gtk.workviews.Revision import WorkView as wvwRevision
from gui.gtk.workviews.Function import WorkView as wvwFunction

_ = gettext.gettext


def destroy(__widget, __event=None):
    """
    Quits the RTK application when the X in the upper right corner is
    pressed.

    :param __widget: the gtk.Widget() that called this method.
    :type __widget: :py:class:`gtk.Widget`
    :keyword __event: the gtk.gdk.Event() that called this method.
    :type __event: :py:class:`gtk.gdk.Event`
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    gtk.main_quit()

    return False


class WorkView(gtk.Window):                 # pylint: disable=R0904
    """
    This is the Work Book for the pyGTK multiple window interface.
    """

    def __init__(self, controller):
        """
        Initializes an instance of the Work View class.

        :param controller: the RTK master data controller.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._mdcRTK = controller

        # Initialize public dictionary attributes.
        self.dic_work_view = {'revision': wvwRevision(controller),
                              'function': wvwFunction(controller)}

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        try:
            locale.setlocale(locale.LC_ALL,
                             self._mdcRTK.RTK_CONFIGURATION.RTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        # Create a new window and set its properties.
        gtk.Window.__init__(self)
        self.set_resizable(True)
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)
        self.set_title(_(u"RTK Work Book"))

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        # On a 1268x1024 screen, the size will be 845x640.
        _width = _width - 20
        _height = (5 * _height / 8) - 40

        self.set_default_size(_width, _height)
        self.set_border_width(5)
        self.set_position(gtk.WIN_POS_NONE)
        self.move((_width / 1), (_height / 2))

        self.connect('delete_event', destroy)

        self.show_all()

        self._on_module_change(module='revision')
        pub.subscribe(self._on_module_change, 'mvwSwitchedPage')

    def _on_module_change(self, module=''):
        """
        Method to load the correct ListView for the RTK module that was
        selected in the ModuleBook.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if self.get_child() is not None:
            self.remove(self.get_child())

        if self.dic_work_view[module] is not None:
            self.add(self.dic_work_view[module])
        else:
            _return = True

        return _return
