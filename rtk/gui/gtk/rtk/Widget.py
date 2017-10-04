# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Widget.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
This module contains functions for creating, populating, destroying, and
interacting with pyGTK widgets.  Import this module in other modules that
create, populate, destroy, or interact with pyGTK widgets in the RTK
application.  This module is the base class for all RTK widgets.
"""

import sys

import gettext

# Modules required for the GUI.
import pango                                    # pylint: disable=E0401,W0611
try:
    import pygtk                                # pylint: disable=W0611
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk                                  # pylint: disable=W0611
except ImportError:
    sys.exit(1)
try:
    import gobject                              # pylint: disable=W0611
except ImportError:
    sys.exit(1)

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

_ = gettext.gettext
