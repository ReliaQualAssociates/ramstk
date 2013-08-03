#!/usr/bin/env python
""" This is the Class that is used to gather credentials for login to
    MySQL databases. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       login.py is part of The RTK Project
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

# Import other RTK modules.
import widgets as _widg
import configuration as _conf

# login.py contains code to create a window that allows the user to enter login
# information for the MySQL server to use.  This includes server, port, MySQL
# user name, and password.

class Login(gtk.Dialog):

    """
    The Login class is used to create a window that allows the user to
    enter login information for the MySQL server to use.  This includes
    server, port, MySQL user name, and password.
    """

    def __init__(self, title):

        """ Initializes the Login Object. """

        gtk.Dialog.__init__(self, title, None,
                            gtk.DIALOG_MODAL,
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                            gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        self.set_title(title)
        self.set_resizable(False)

        self.connect('response', self._ok)
        self.connect('close', self._cancel)

        fixed = gtk.Fixed()
        self.vbox.pack_start(fixed, True, True, 10)

        label = _widg.make_label('Host: ', 75, 25)
        self.txtHost = _widg.make_entry(150, 25)
        self.txtHost.set_text(_conf.RTK_PROG_INFO[0])
        fixed.put(label, 10, 10)
        fixed.put(self.txtHost, 90, 10)

        label = _widg.make_label('Port: ', 75, 25)
        self.txtPort = _widg.make_entry(150, 25)
        self.txtPort.set_text(str(_conf.RTK_PROG_INFO[1]))
        fixed.put(label, 10, 40)
        fixed.put(self.txtPort, 90, 40)

        label = _widg.make_label('User: ', 75, 25)
        self.txtUser = _widg.make_entry(150, 25)
        self.txtUser.set_text(str(_conf.RTK_PROG_INFO[3]))
        fixed.put(label, 10, 75)
        fixed.put(self.txtUser, 90, 75)

        label = _widg.make_label('Password: ', 75, 25)
        self.txtPassword = _widg.make_entry(150, 25)
        self.txtPassword.set_visibility(False)
        self.txtPassword.set_invisible_char("*")
        self.txtPassword.set_activates_default(True)
        self.txtPassword.set_text(str(_conf.RTK_PROG_INFO[4]))
        fixed.put(label, 10, 110)
        fixed.put(self.txtPassword, 90, 110)

        self.vbox.show_all()

        self.run()

    def _ok(self, dialog, response):

        """ Callback function to handle OK button response. """

        if(response != gtk.RESPONSE_ACCEPT):
            self._cancel(dialog)
            return response

        _conf.RTK_PROG_INFO[0] = self.txtHost.get_text()
        _conf.RTK_PROG_INFO[1] = int(self.txtPort.get_text())
        _conf.RTK_PROG_INFO[3] = self.txtUser.get_text()
        _conf.RTK_PROG_INFO[4] = self.txtPassword.get_text()

        self.destroy()

        return response

    def _cancel(self, dialog):

        """ Callback function to handle CANCEL button response. """

        self.destroy()

        return False
