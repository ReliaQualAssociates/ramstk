# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.ScrolledWindow.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""ScrolledWindow Module."""

# Import the ramstk.Widget base class.
from .Widget import gtk  # pylint: disable=E0401


class RAMSTKScrolledWindow(Gtk.ScrolledWindow):
    """
    This is the RAMSTK ScrolledWindow class.

    This module contains RAMSTK scrolled window classes.  These classes are
    derived from the applicable pyGTK scrolledwindow, but are provided with
    RAMSTK specific property values and methods.  This ensures a consistent look
    and feel to widgets in the RAMSTK application.
    """

    def __init__(self, child, viewport=True):
        """
        Create ScrolledWindow() widgets.

        :param child: the Gtk.Widget() to add to the scrolled window.
        :param bool viewport: whether or not to add the child widget with a
                              Gtk.ViewPort().
        """
        GObject.GObject.__init__(self)

        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        if child is not None:
            if viewport:
                self.add_with_viewport(child)
            else:
                self.add(child)
