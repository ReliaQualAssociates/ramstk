# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.scrolledwindow.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK GTK3 ScrolledWindow Module."""

# RAMSTK Package Imports
from ramstk.views.gtk3 import GObject, Gtk


class RAMSTKScrolledWindow(Gtk.ScrolledWindow):
    """The RAMSTKScrolledWindow class."""
    def __init__(self, child: object) -> None:
        """Create ScrolledWindow() widgets.

        :param child: the Gtk.Widget() to add to the scrolled window.
        """
        GObject.GObject.__init__(self)

        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        if child is not None:
            self.add(child)
