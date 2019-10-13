# pylint: disable=unused-import, wrong-import-position
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.__init__.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 GUI package."""

# Standard Library Imports
import gettext
import sys

try:
    import gi  # isort:skip
    gi.require_version('Gdk', '3.0')
    gi.require_version('Gtk', '3.0')
except ImportError:
    print("Failed to import package gi; exiting.")
    sys.exit(1)
from gi.repository import Gdk, GdkPixbuf, GObject, Gtk, Pango  # isort:skip

_ = gettext.gettext  # isort:skip

from .desktop import RAMSTKDesktop  # isort:skip
