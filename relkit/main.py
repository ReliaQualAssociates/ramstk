#!/usr/bin/env python
""" This is the main program for The RelKit application. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2009 - 2012 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       main.py is part of The RelKit Project
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

import os
import getpass
import datetime
import logging

# Add localization support.
import gettext
_ = gettext.gettext

# Import other RelKit modules.
import configuration as _conf
import mysql as _mysql
import notebook as _note
import partlist as _parts
import sqlite as _sqlite
import tree as _tree
import utilities as _util

# Import all of the RelKit Classes.
from revision import Revision
from function import Function
from requirement import Requirement
from hardware import Hardware
from validation import Validation
from incident import Incident
from assembly import Assembly
from component import Component
from software import Software
from dataset import Dataset


def main():

    """ This is the main function for the RelKit application. """

    app = RelKit()

    gtk.main()

    return 0


class RelKit:

    """ This is the RelKit class. """

    def __init__(self):

        self.ProgCnx = None

        # Read the configuration file.
        _util.read_configuration()

        # Create loggers for the application.  The first is to store log
        # information for RelKit developers.  The second is to log errors
        # for the user.  The user can use these errors to help find problems
        # with their inputs and sich.
        __user_log = _conf.LOG_DIR + '/relkit_user.log'
        __error_log = _conf.LOG_DIR + '/relkit_error.log'
        __import_log = _conf.LOG_DIR + '/relkit_import.log'

        if(not _util.dir_exists(_conf.LOG_DIR)):
            os.makedirs(_conf.LOG_DIR)

        if(_util.file_exists(__user_log)):
            os.remove(__user_log)
        if(_util.file_exists(__error_log)):
            os.remove(__error_log)
        if(_util.file_exists(__import_log)):
            os.remove(__import_log)

        self.debug_log = _util.create_logger("RelKit.debug", logging.DEBUG,
                                             __error_log)
        self.user_log = _util.create_logger("RelKit.user", logging.WARNING,
                                            __user_log)
        self.import_log = _util.create_logger("RelKit.import", logging.WARNING,
                                              __import_log)

        self.LOADED = False
        self.partlist = {}

        # Find out who is using RelKit.
        self._UID = getpass.getuser()
        self._TODAY = datetime.datetime.now()
        self.DATE = "1970-01-01"

        # Get a connection to the common database.
        if(_conf.COM_BACKEND == 'mysql'):
            self.COMDB = _mysql.MySQLInterface(self)
            self.ComCnx = self.COMDB.get_connection(_conf.RELIAFREE_COM_INFO)

        elif(_conf.COM_BACKEND == 'sqlite3'):
            self.COMDB = _sqlite.SQLite3Interface(self)
            _database = _conf.CONF_DIR + _conf.RELIAFREE_COM_INFO[2] + '.rfb'
            self.ComCnx = self.COMDB.get_connection(_database)

        # Get a connection to the program database.
        if(_conf.BACKEND == 'mysql'):
            self.DB = _mysql.MySQLInterface(self)

        elif(_conf.BACKEND == 'sqlite3'):
            self.DB = _sqlite.SQLite3Interface(self)

        # Create the GUI and objects for each of the RelKit classes.
        self.winWorkBook = _note.WorkBookWindow(self)

        self.REVISION = Revision(self)
        self.FUNCTION = Function(self)
        self.REQUIREMENT = Requirement(self)
        self.HARDWARE = Hardware(self)
        self.SOFTWARE = Software(self)
        self.VALIDATION = Validation(self)
        self.INCIDENT = Incident(self)
        self.ASSEMBLY = Assembly(self)
        self.COMPONENT = Component(self)
        self.DATASET = Dataset(self)

        self.winTree = _tree.TreeWindow(self)
        self.winParts = _parts.PartsListWindow(self)

        self.icoStatus = gtk.StatusIcon()
        icon = _conf.ICON_DIR + '32x32/db-disconnected.png'
        icon = gtk.gdk.pixbuf_new_from_file_at_size(icon, 16, 16)
        self.icoStatus.set_from_pixbuf(icon)
        self.icoStatus.set_tooltip(_("RelKit is not currently connected to a program database."))

        self.winTree.present()

    def load_system(self):

        """
        This method loads the RelKit development program database the
        user opens.
        """

        self.winTree.statusbar.push(2, _("Opening Program Database..."))
        self.winTree.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        self.winWorkBook.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        self.winParts.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))

        # Get a connection to the program database and then retrieve the
        # program information.
        query = "SELECT * FROM tbl_program_info"
        if(_conf.BACKEND == 'mysql'):
            self.ProgCnx = self.DB.get_connection(_conf.RELIAFREE_PROG_INFO)
        elif(_conf.BACKEND == 'sqlite3'):
            self.ProgCnx = self.DB.get_connection(_conf.RELIAFREE_PROG_INFO[2])

        results = self.DB.execute_query(query, None, self.ProgCnx)

        for i in range(19):
            _conf.RELIAFREE_PREFIX.append(results[0][i + 1])

        # Find which modules are active in this project.
        for i in range(9):
            _conf.RELIAFREE_MODULES.append(results[0][i + 19])

        icon = _conf.ICON_DIR + '32x32/db-connected.png'
        icon = gtk.gdk.pixbuf_new_from_file_at_size(icon, 16, 16)
        self.icoStatus.set_from_pixbuf(icon)
        self.icoStatus.set_tooltip(_("RelKit is connected to program database %s." %
                                   _conf.RELIAFREE_PROG_INFO[2]))
        self.winTree.set_title(_("RelKit - Analyzing %s" %
                               _conf.RELIAFREE_PROG_INFO[2]))

        self.winTree.load_trees(self)

        if(_conf.RELIAFREE_MODULES[0] == 1):    # Revisions
            self.REVISION.treeview.grab_focus()

        elif(_conf.RELIAFREE_MODULES[1] == 1):  # Requirements
            self.REQUIREMENT.treeview.grab_focus()

        elif(_conf.RELIAFREE_MODULES[2] == 1):  # Functions
            self.FUNCTION.treeview.grab_focus()

        elif(_conf.RELIAFREE_MODULES[3] == 1):  # Hardware
            self.HARDWARE.load_tree()

        elif(_conf.RELIAFREE_MODULES[4] == 1):  # Software
            self.SOFTWARE.load_tree()

        elif(_conf.RELIAFREE_MODULES[5] == 1):  # V&V Tracking
            self.VALIDATION.treeview.grab_focus()

        elif(_conf.RELIAFREE_MODULES[8] == 1):  # Field incident tracking
            self.INCIDENT.treeview.grab_focus()

        self.LOADED = True

        self.winTree.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
        self.winWorkBook.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
        self.winParts.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
        self.winTree.statusbar.pop(2)

if __name__ == '__main__':

    main()
