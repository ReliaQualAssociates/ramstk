#!/usr/bin/env python
"""
##############################
FMEA Package Assistants Module
##############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.gui.gtk.Assistants.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale
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

# Import other RTK modules.
try:
    import configuration as _conf
    import widgets as _widg
except ImportError:
    import rtk.configuration as _conf
    import rtk.widgets as _widg

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class AddControlAction(gtk.Dialog):
    """
    This is the assistant that walks the user through the process of adding
    a new design control or action to the selected failure cause.
    """

    def __init__(self):
        """
        Initialize on instance of the Add Control or Action Assistant.
        """

        gtk.Dialog.__init__(self, title=_(u"RTK FMEA/FMECA Design Control and "
                                          u"Action Addition Assistant"),
                            parent=None,
                            flags=(gtk.DIALOG_MODAL |
                                   gtk.DIALOG_DESTROY_WITH_PARENT),
                            buttons=(gtk.STOCK_APPLY, gtk.RESPONSE_ACCEPT,
                                     gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        self.rdoControl = _widg.make_option_button(None, _(u"Add control"))
        self.rdoAction = _widg.make_option_button(self.rdoControl,
                                                  _(u"Add action"))

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the dialog.                       #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()
        self.vbox.pack_start(_fixed)        # pylint: disable=E1101

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _label = _widg.make_label(_(u"This is the RTK Design Control and "
                                    u"Action Addition Assistant.  Enter the "
                                    u"information requested below and then "
                                    u"press 'Apply' to add a new design "
                                    u"control or action to the RTK Project "
                                    u"database."),
                                  width=600, height=-1, wrap=True)
        _fixed.put(_label, 5, 10)
        _y_pos = _label.size_request()[1] + 50

        # Set the tooltips.
        self.rdoControl.set_tooltip_text(_(u"Select to add a design control"
                                           u"to the selected failure cause."))

        # Place the widgets.
        _fixed.put(self.rdoControl, 10, _y_pos)
        _fixed.put(self.rdoAction, 10, _y_pos + 35)

        _fixed.show_all()

    def _cancel(self, __button):
        """
        Method to destroy the assistant when the 'Cancel' button is
        pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        """

        self.destroy()
