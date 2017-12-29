# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.ScrolledWindow.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""ScrolledWindow Module."""

# Import the rtk.Widget base class.
from .Widget import gtk  # pylint: disable=E0401


class RTKScrolledWindow(gtk.ScrolledWindow):
    """
    This is the RTK ScrolledWindow class.

    This module contains RTK scrolled window classes.  These classes are
    derived from the applicable pyGTK scrolledwindow, but are provided with
    RTK specific property values and methods.  This ensures a consistent look
    and feel to widgets in the RTK application.
    """

    def __init__(self, child, viewport=True):
        """
        Create ScrolledWindow() widgets.

        :param child: the gtk.Widget() to add to the scrolled window.
        :param bool viewport: whether or not to add the child widget with a
                              gtk.ViewPort().
        """
        gtk.ScrolledWindow.__init__(self)

        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        if child is not None:
            if viewport:
                self.add_with_viewport(child)
            else:
                self.add(child)
