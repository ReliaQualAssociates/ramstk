#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to the
hardware assemblies of the Program.
"""

__author__ = 'Andrew Rowland <andrew.rowland@reliaqual.com>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       assembly.py is part of The RTK Project
#
# All rights reserved.

import sys

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
try:
    import pango
except ImportError:
    sys.exit(1)

from datetime import datetime
from lxml import etree

# Import other RTK modules.
import calculations as _calc
import configuration as _conf
import imports as _impt
import utilities as _util
import widgets as _widg

from hardware import Hardware

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, "")

import gettext
_ = gettext.gettext


class Assembly(Hardware):
    """
    The ASSEMBLY meta-class is used to represent a hardware assembly.  It is
    super-classed by the ASSEMBLY class to provide assembly specific
    information and methods.
    """

# TODO: Add tooltips to all widgets.
