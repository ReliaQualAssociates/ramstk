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
    import gui.gtk.rtk.Widget as Widgets
except ImportError:
    import rtk.gui.gtk.rtk.Widget as Widgets

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 Andrew "Weibullguy" Rowland'

_ = gettext.gettext


class OpenProject(object):
    """
    This is the gtk.Assistant() that guides the user through the process of
    creating a new RTK Project database.
    """

    def __init__(self, __button, controller):
        """
        Method to initialize an instance of the Create Project Assistant.

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

        try:
            locale.setlocale(locale.LC_ALL,
                             self._mdcRTK.RTK_CONFIGURATION.RTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        Widgets.set_cursor(self._mdcRTK, gtk.gdk.WATCH)

        self._request_open_project()

        Widgets.set_cursor(self._mdcRTK, gtk.gdk.LEFT_PTR)

    def _request_open_project(self):
        """
        Method to open or connect to an RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if self._mdcRTK.loaded:
            Widgets.rtk_information(_(u"A database is already open.  Only "
                                      u"one database can be open at a time "
                                      u"in RTK.  You must quit the RTK "
                                      u"application before a new database "
                                      u"can be opened."))
            _return = True

        _dialog = gtk.FileChooserDialog(title=_(u"RTK - Open Program"),
                                        buttons=(gtk.STOCK_OK,
                                                 gtk.RESPONSE_ACCEPT,
                                                 gtk.STOCK_CANCEL,
                                                 gtk.RESPONSE_REJECT))
        _dialog.set_current_folder(self._mdcRTK.RTK_CONFIGURATION.RTK_PROG_DIR)

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
            self._mdcRTK.RTK_CONFIGURATION.RTK_PROG_INFO['database'] = \
                _dialog.get_filename()

        _dialog.destroy()

        self._mdcRTK.request_open_program()

        return _return
