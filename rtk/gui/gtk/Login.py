#!/usr/bin/env python
"""
===========================
PyGTK Database Login Dialog
===========================
"""

# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.Login.py is part of the RTK Project
#
# All rights reserved.

import sys

# Import modules for localization support.
import gettext
import locale

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
    import Configuration
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.gui.gtk.Widgets as Widgets

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Login(gtk.Dialog):
    """
    The Login class is used to create a window that allows the user to
    enter login information for the database server to use.  This includes
    server, port, user name, and password.
    """

    def __init__(self, title):
        """
        Method to initialize the Login Object.

        :param str title:
        """

        gtk.Dialog.__init__(self, title, None,
                            gtk.DIALOG_MODAL,
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                             gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        self.set_title(title)
        self.set_resizable(False)

        # Create gtk.Widgets() for user inputs.
        self.txtHost = Widgets.make_entry(150, 25)
        self.txtPort = Widgets.make_entry(150, 25)
        self.txtUser = Widgets.make_entry(150, 25)
        self.txtPassword = Widgets.make_entry(150, 25)
        self.txtPassword.set_visibility(False)
        self.txtPassword.set_invisible_char("*")
        self.txtPassword.set_activates_default(True)

        # Create the Login dialog.
        _fixed = gtk.Fixed()

        _label = Widgets.make_label('Host: ', 75, 25)
        _fixed.put(_label, 10, 10)
        _fixed.put(self.txtHost, 90, 10)

        _label = Widgets.make_label('Port: ', 75, 25)
        _fixed.put(_label, 10, 40)
        _fixed.put(self.txtPort, 90, 40)

        _label = Widgets.make_label('User: ', 75, 25)
        _fixed.put(_label, 10, 75)
        _fixed.put(self.txtUser, 90, 75)

        _label = Widgets.make_label('Password: ', 75, 25)
        _fixed.put(_label, 10, 110)
        _fixed.put(self.txtPassword, 90, 110)

        # Load user input gtk.Widgets() with configuration file information.
        self.txtHost.set_text(Configuration.RTK_PROG_INFO[0])
        self.txtPort.set_text(str(Configuration.RTK_PROG_INFO[1]))
        self.txtUser.set_text(str(Configuration.RTK_PROG_INFO[3]))
        self.txtPassword.set_text(str(Configuration.RTK_PROG_INFO[4]))

        # Connect gtk.Widgets() to callback methods.
        self.connect('response', self._ok)
        self.connect('close', self._cancel)

        self.vbox.pack_start(_fixed, True, True, 10)
        self.vbox.show_all()

        self.run()

    def _ok(self, __dialog, response):
        """
        Method to handle OK button response.
        """

        if response == gtk.RESPONSE_ACCEPT:
            Configuration.RTK_PROG_INFO[0] = self.txtHost.get_text()
            Configuration.RTK_PROG_INFO[1] = int(self.txtPort.get_text())
            Configuration.RTK_PROG_INFO[3] = self.txtUser.get_text()
            Configuration.RTK_PROG_INFO[4] = self.txtPassword.get_text()

        self.destroy()

        return response

    def _cancel(self, __dialog):
        """
        Method to handle CANCEL button response.
        """

        self.destroy()

        return False
