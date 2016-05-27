#!/usr/bin/env python
"""
#####################
RTK Assistants Module
#####################
"""

# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.Assistants.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale
import sys
import ntpath

from os import name, remove
from datetime import datetime

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
try:
    import Configuration
    import Utilities
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    import rtk.gui.gtk.Widgets as Widgets

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 Andrew "Weibullguy" Rowland'

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext



class CreateProject(object):
    """
    This is the class used to create a new RTK Project database.
    """

    def __init__(self, __button, controller):
        """
        Method to initialize an instance of the Create Project Assistant.

        :param controller: the :py:class:`rtk.RTK.RTK` master data controller.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._mdcRTK = controller

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        Utilities.set_cursor(self._mdcRTK, gtk.gdk.WATCH)

        if Configuration.BACKEND == 'mysql':
            self._create_mysql_project()
        elif Configuration.BACKEND == 'sqlite3':
            self._create_sqlite3_project()

        Utilities.set_cursor(self._mdcRTK, gtk.gdk.LEFT_PTR)

    def _create_mysql_project(self):
        """
        Method to create a RTK Project database using MySQL/MariaDB.
        """
# TODO: Update MySQL/MariaDB code.
        login = _login.Login(_(u"Create a RTK Program Database"))
        if login.answer != gtk.RESPONSE_ACCEPT:
            return True

        dialog = Widgets.make_dialog(_(u"RTK - New Program"))

        label = Widgets.make_label(_(u"New Program Name"))
        txtProgName = Widgets.make_entry()
        dialog.vbox.pack_start(label)           # pylint: disable=E1101
        dialog.vbox.pack_start(txtProgName)     # pylint: disable=E1101
        label.show()
        txtProgName.show()

        label = Widgets.make_label(_(u"Assigned User"))
        txtUser = Widgets.make_entry()
        dialog.vbox.pack_start(label)           # pylint: disable=E1101
        dialog.vbox.pack_start(txtUser)         # pylint: disable=E1101
        label.show()
        txtUser.show()

        label = Widgets.make_label(_(u"Using Password"))
        txtPasswd = Widgets.make_entry()
        txtPasswd.set_invisible_char("*")
        dialog.vbox.pack_start(label)           # pylint: disable=E1101
        dialog.vbox.pack_start(txtPasswd)       # pylint: disable=E1101
        label.show()
        txtPasswd.show()

        if dialog.run() == gtk.RESPONSE_ACCEPT:
            new_program = txtProgName.get_text()
            user = txtUser.get_text()
            passwd = txtPasswd.get_text()

        dialog.destroy()

        Configuration.RTK_PROG_INFO[2] = None
        query = "CREATE DATABASE IF NOT EXISTS %s"
        cnx = app.DB.get_connection(Configuration.RTK_PROG_INFO)
        results = app.DB.execute_query(query,
                                       new_program,
                                       cnx,
                                       commit=True)
        cnx.close()
        if not results:
            return True

        Configuration.RTK_PROG_INFO[2] = new_program
        cnx = app.DB.get_connection(Configuration.RTK_PROG_INFO)

        sqlfile = open(Configuration.DATA_DIR + 'newprogram_mysql.sql', 'r')

        queries = sqlfile.read().split(';')
        program = "USE '%s'"
        results = app.DB.execute_query(program, new_program, cnx, commit=True)
        for __, _query in enumerate(queries):
            results = app.DB.execute_query(_query, cnx, commit=True)

        values = (new_program, user, passwd)
        query = "GRANT DELETE, INSERT, SELECT, UPDATE \
                 ON %s.* TO '%s'@'%%' \
                 IDENTIFIED BY '%s'"
        results = app.DB.execute_query(query, values, cnx, commit=False)

        query = "FLUSH PRIVILEGES"
        results = app.DB.execute_query(query, None, cnx, commit=False)

        cnx.close()

    def _create_sqlite3_project(self):
        """
        Method to create a RTK Project database using SQLite3.
        """

        _dialog = gtk.FileChooserDialog(title=_(u"Create a RTK Program "
                                                u"Database"),
                                        action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                        buttons=(gtk.STOCK_NEW,
                                                 gtk.RESPONSE_ACCEPT,
                                                 gtk.STOCK_CANCEL,
                                                 gtk.RESPONSE_REJECT))
        _dialog.set_current_folder(Configuration.PROG_DIR)

        if _dialog.run() == gtk.RESPONSE_ACCEPT:
            _new_program = _dialog.get_filename()
            _new_program = _new_program.rsplit('.')[0]
            _new_program = _new_program + '.rtk'

            if Utilities.file_exists(_new_program):
                _dlgConfirm = Widgets.make_dialog(_(u"RTK - Confirm Overwrite"),
                                                  dlgbuttons=(gtk.STOCK_YES,
                                                              gtk.RESPONSE_YES,
                                                              gtk.STOCK_NO,
                                                              gtk.RESPONSE_NO))

                _label = Widgets.make_label(_(u"RTK Program database already "
                                              u"exists.\n\n{0:s}\n\n"
                                              u"Overwrite?").format(
                                                _new_program),
                                            width=-1, height=-1, bold=False,
                                            wrap=True)
                _dlgConfirm.vbox.pack_start(_label)     # pylint: disable=E1101
                _label.show()

                if _dlgConfirm.run() == gtk.RESPONSE_YES:
                    _dlgConfirm.destroy()
                    remove(_new_program)
                else:
                    _dlgConfirm.destroy()
                    _dialog.destroy()
                    return True

            _new_program = ntpath.basename(_new_program)
            Configuration.RTK_PROG_INFO[2] = _new_program

        _dialog.destroy()

        self._mdcRTK.request_create_project()

        return False

    def _cancel(self, __button):
        """
        Method to destroy the Create Project Assistant.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :return: True
        :rtype: boolean
        """

        self.assistant.destroy()

        return True


class OpenProject(object):
    """
    This is the gtk.Assistant() that guides the user through the process of
    creating a new RTK Project database.
    """

    def __init__(self, __button, controller):
        """
        Method to initialize an instance of the Create Project Assistant.

        :param controller: the :py:class:`rtk.RTK.RTK` master data controller.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._mdcRTK = controller

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        Utilities.set_cursor(self._mdcRTK, gtk.gdk.WATCH)

        if Configuration.BACKEND == 'mysql':
            self._open_mysql_project()
        elif Configuration.BACKEND == 'sqlite3':
            self._open_sqlite3_project()

        Utilities.set_cursor(self._mdcRTK, gtk.gdk.LEFT_PTR)

    def _open_mysql_project(self):
        """
        Method to open a MySQL/MariaDB RTK program database.
        """
# TODO: Update the MySQL/MariaDB code.
        pass
    #    login = _login.Login(_(u"RTK Program Database Login"))

    #    if login.answer != gtk.RESPONSE_ACCEPT:
    #        return True

    #    _query = "SHOW DATABASES"
    #    _cnx = app.DB.get_connection(Configuration.RTK_PROG_INFO)
    #    results = app.DB.execute_query(query, None, cnx)

    #    dialog = Widgets.make_dialog(_(u"RTK: Open Program"))

    #    model = gtk.TreeStore(gobject.TYPE_STRING)
    #    treeview = gtk.TreeView(model)

    #    column = gtk.TreeViewColumn(_(u"Program"))
    #    treeview.append_column(column)
    #    cell = gtk.CellRendererText()
    #    cell.set_property('editable', False)
    #    column.pack_start(cell, True)
    #    column.add_attribute(cell, 'text', 0)

    #    scrollwindow = gtk.ScrolledWindow()
    #    width, height = gtk.gdk.get_default_root_window().get_size()
    #    scrollwindow.set_size_request((width / 6), (height / 6))
    #    scrollwindow.add(treeview)

    #    for __, _database in enumerate(results):
            # Don't display the MySQL administrative/test databases.
    #        if(_database[0] != 'information_schema' and
    #           _database[0] != 'test' and
    #           _database[0] != 'mysql' and
    #           _database[0] != 'RTKcom' and
    #           _database[0] != '#mysql50#lost+found'):
    #            model.append(None, [_database[0]])

    #    dialog.vbox.pack_start(scrollwindow)    # pylint: disable=E1101
    #    scrollwindow.show_all()

    #    if dialog.run() == gtk.RESPONSE_ACCEPT:
    #        (_model, _row) = treeview.get_selection().get_selected()
    #        Configuration.RTK_PROG_INFO[2] = _model.get_value(_row, 0)
    #        set_cursor(application, gtk.gdk.WATCH)
    #        dialog.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
    #        application.open_project()

    #    dialog.destroy()

    #    cnx.close()

    def _open_sqlite3_project(self):
        """
        Method to open a SQLite3 RTK program database.
        """

        _dialog = gtk.FileChooserDialog(title=_(u"RTK - Open Program"),
                                        buttons=(gtk.STOCK_OK,
                                                 gtk.RESPONSE_ACCEPT,
                                                 gtk.STOCK_CANCEL,
                                                 gtk.RESPONSE_REJECT))
        _dialog.set_current_folder(Configuration.PROG_DIR)

        # Set some filters to select all files or only some text files.
        _filter = gtk.FileFilter()
        _filter.set_name(_(u"RTK Program Databases"))
        _filter.add_pattern("*.rtk")
        _dialog.add_filter(_filter)

        _filter = gtk.FileFilter()
        _filter.set_name(_(u"All files"))
        _filter.add_pattern("*")
        _dialog.add_filter(_filter)

        if _dialog.run() == gtk.RESPONSE_ACCEPT:
            Configuration.RTK_PROG_INFO[2] = _dialog.get_filename()

        _dialog.destroy()

        self._mdcRTK.request_open_project()

        return False


#def import_project(__widget, __app):
#    """
#    Imports project information from external files such as Excel, CVS, other
#    delimited text files, etc.

#    :param gtk.Widget __widget: the gtk.Widget() that called this function.
#    :param rtk __app: the current instance of the RTK application.
#    :return: False if successful or True if an error is encountered.
#    :rtype: bool
#    """

#    _dialog = gtk.FileChooserDialog(_(u"Select Project to Import"), None,
#                                    gtk.FILE_CHOOSER_ACTION_OPEN,
#                                    (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
#                                     gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

#    if _dialog.run() == gtk.RESPONSE_ACCEPT:
#        print "Importing project."

#    _dialog.destroy()

#    return False
