# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.assistants.CreateProject.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
#####################
RTK Assistants Module
#####################
"""

import gettext
import sys

from os import remove

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
    import gui.gtk.rtk.Widget as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.gui.gtk.rtk.Widget as Widgets

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 Andrew "Weibullguy" Rowland'

_ = gettext.gettext


class DeleteProject(object):
    """
    This is the gtk.Assistant() that guides the user through the process of
    deleting an existing RTK Program database.
    """

    def __init__(self, __button, controller):
        """
        Method to initialize an instance of the Delete Project Assistant.

        :param gtk.ToolButton __button: the gtk.ToolButton() that launched this
                                        class.
        :param controller: the :py:class:`rtk.RTK.RTK` master data controller.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._mdcRTK = controller

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        Widgets.set_cursor(self._mdcRTK, gtk.gdk.WATCH)

        if Configuration.BACKEND == 'mysql':
            self._request_delete_mysql_project()
        elif Configuration.BACKEND == 'sqlite3':
            self._request_delete_sqlite3_project()

        Widgets.set_cursor(self._mdcRTK, gtk.gdk.LEFT_PTR)

    def _request_delete_mysql_project(self):
        """
        Method to delete a RTK Project database using MySQL/MariaDB.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # TODO: Update MySQL/MariaDB code.
        pass
        #query = "SHOW DATABASES"
        #cnx = app.DB.get_connection(Configuration.RTK_PROG_INFO)
        #results = app.DB.execute_query(query,
        #                               None,
        #                               cnx)

        #dialog = Widgets.make_dialog(_("RTK - Delete Program"))

        #model = gtk.TreeStore(gobject.TYPE_STRING)
        #treeview = gtk.TreeView(model)

        #column = gtk.TreeViewColumn('Program')
        #treeview.append_column(column)
        #cell = gtk.CellRendererText()
        #cell.set_property('editable', False)
        #column.pack_start(cell, True)
        #column.add_attribute(cell, 'text', 0)

        #scrollwindow = gtk.ScrolledWindow()
        #width, height = gtk.gdk.get_default_root_window().get_size()
        #scrollwindow.set_size_request((width / 6), (height / 6))
        #scrollwindow.add(treeview)

        #numprograms = len(results)
        #for i in range(numprograms):
        # Don't display the MySQL administrative/test databases.
        #    if(results[i][0] != 'information_schema' and
        #       results[i][0] != 'test'):
        #        model.append(None, [results[i][0]])

        #dialog.vbox.pack_start(scrollwindow)    # pylint: disable=E1101
        #treeview.show()
        #scrollwindow.show()

        #if dialog.run() == gtk.RESPONSE_ACCEPT:
        #    (_model, _row) = treeview.get_selection().get_selected()
        #    project = _model.get_value(_row, 0)
        #else:
        #    dialog.destroy()

        #if confirm_action(_("Really delete %s?") % project, 'question'):
        #    query = "DROP DATABASE IF EXISTS %s"
        #    results = app.DB.execute_query(query,
        #                                   project,
        #                                   cnx)

        #    dialog.destroy()
        #else:
        #    dialog.destroy()

        #cnx.close()

        #return False

    def _request_delete_sqlite3_project(self):
        """
        Method to delete a RTK Project database using SQLite3.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _dialog = gtk.FileChooserDialog(
            title=_(u"RTK - Delete Program"),
            buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL,
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
            _project = _dialog.get_filename()

            _prompt = _(u"Really delete {0:s}?").format(_project)
            _confirm = self._confirm_action(_prompt)
            if _confirm:
                remove(_project)
                _dialog.destroy()
            else:
                _dialog.destroy()
        else:
            _dialog.destroy()

        return False

    @staticmethod
    def _confirm_action(prompt):
        """
        Method to confirm deleting a Project.

        :param str prompt: the prompt to display in the dialog.
        :param str image: the icon to display in the dialog.
        :param gtk.Window parent: the parent gtk.Window(), if any, for the
                                  dialog.
        :return: True if action is confirmed or False otherwise.
        :rtype: bool
        """

        _return = False

        _dialog = Widgets.make_dialog("")

        _hbox = gtk.HBox()

        _img = Configuration.ICON_DIR + '32x32/question.png'
        _image = gtk.Image()
        _image.set_from_file(_img)
        _hbox.pack_start(_image)

        _label = Widgets.make_label(prompt, height=-1, width=-1)
        _hbox.pack_end(_label)
        _dialog.vbox.pack_start(_hbox)  # pylint: disable=E1101
        _hbox.show_all()

        if _dialog.run() == gtk.RESPONSE_ACCEPT:
            _dialog.destroy()
            _return = True
        else:
            _dialog.destroy()

        return _return

    def _cancel(self, __button):
        """
        Method to destroy the Create Project Assistant.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :return: True
        :rtype: boolean
        """

        self.assistant.destroy()

        return True
