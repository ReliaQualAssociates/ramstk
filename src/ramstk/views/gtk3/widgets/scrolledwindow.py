# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.scrolledwindow.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKScrolledWindow module."""

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk


class RAMSTKScrolledWindow(Gtk.ScrolledWindow):
    """The RAMSTKScrolledWindow class."""

    def __init__(self, child: object) -> None:
        """Initialize an instance of the RAMSTKScrolledWindow widget.

        :param child: the Gtk.Widget to add to the RAMSTKScrolledWindow.
        """
        Gtk.ScrolledWindow.__init__(self)

        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        if child is not None:
            self.add(child)  # type: ignore[attr-defined]
