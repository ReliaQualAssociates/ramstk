#!/usr/bin/env python
"""
##################################
Requirement Package Assistants Module
##################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       Assistants.py is part of The RTK Project
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


class AddRequirement(gtk.Dialog):
    """
    This is the assistant that walks the user through the process of adding
    a new requirement to the open RTK Program database.
    """

    def __init__(self, controller, level=0):
        """
        Initialize on instance of the Add Requirement Assistant.

        :param rtk.requirement.Requirement.Requirement controller: the Requirement data controller instance.
        :keyword int level: the level to add the new Requirement(s).
                            0 = sibling
                            1 = child
        """

        gtk.Dialog.__init__(self, title=_(u"RTK Requirement Addition "
                                          u"Assistant"),
                            parent=None,
                            flags=(gtk.DIALOG_MODAL |
                                   gtk.DIALOG_DESTROY_WITH_PARENT),
                            buttons=(gtk.STOCK_APPLY, gtk.RESPONSE_ACCEPT,
                                     gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        self._controller = controller

        self.txtQuantity = _widg.make_entry(width=50)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the dialog.                       #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()
        self.vbox.pack_start(_fixed)        # pylint: disable=E1101

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        if level == 0:
            _level = 'sibling'
        else:
            _level = 'child'
        _label = _widg.make_label(_(u"This is the RTK Requirement Addition "
                                    u"Assistant.  Enter the information "
                                    u"requested below and then press 'Apply' "
                                    u"to add new {0:s} Requirements to the "
                                    u"RTK Project database.").format(_level),
                                  width=600, height=-1, wrap=True)
        _fixed.put(_label, 5, 10)
        _y_pos = _label.size_request()[1] + 50

        _labels = [_(u"Number of {0:s} requirements to add:").format(_level)]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, _y_pos)
        _x_pos += 50

        # Set the tooltips.
        self.txtQuantity.set_tooltip_text(_(u"Enter the number of {0:s} "
                                            u"Requirements to "
                                            u"add.").format(_level))
        self.txtQuantity.set_text("1")

        # Place the widgets.
        _fixed.put(self.txtQuantity, _x_pos, _y_pos[0])

        _fixed.show_all()

    def _cancel(self, __button):
        """
        Method to destroy the assistant when the 'Cancel' button is
        pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        """

        self.destroy()
