# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.assistants.OpenProject.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Open Project Assistant Module."""

# Import other RAMSTK modules.
from rtk.gui.gtk.rtk.Widget import _, gtk, set_cursor
from rtk.gui.gtk import rtk

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2018 Doyle "weibullguy" Rowland'


class OpenProject(object):
    """
    This is the gtk.Assistant() that guides the user through the process of
    creating a new RAMSTK Project database.
    """

    def __init__(self, __button, controller):
        """
        Method to initialize an instance of the Create Project Assistant.

        :param gtk.ToolButton __button: the gtk.ToolButton() that launched this
                                        class.
        :param controller: the :py:class:`rtk.RAMSTK.RAMSTK` master data controller.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._mdcRAMSTK = controller

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        set_cursor(self._mdcRAMSTK, gtk.gdk.WATCH)

        self._do_request_open_project()

        set_cursor(self._mdcRAMSTK, gtk.gdk.LEFT_PTR)

    def _do_request_open_project(self):
        """
        Open or connect to a RAMSTK Program database.

        :return: None
        :rtype: None
        """
        if self._mdcRAMSTK.loaded:
            _prompt = _(u"A database is already open.  Only one database can "
                        u"be open at a time in RAMSTK.  You must close the "
                        u"currently open RAMSTK database before a new "
                        u"database can be opened.")
            _icon = (self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
                     '/32x32/information.png')
            _dialog = rtk.RAMSTKMessageDialog(_prompt, _icon, 'information')
            if _dialog.run() == gtk.RESPONSE_OK:
                _dialog.destroy()

        else:
            _dialog = gtk.FileChooserDialog(
                title=_(u"RAMSTK - Open Program"),
                buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL,
                         gtk.RESPONSE_REJECT))
            _dialog.set_current_folder(
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_PROG_DIR)

            # Set some filters to select all files or only some text files.
            _filter = gtk.FileFilter()
            _filter.set_name(_(u"RAMSTK Program Databases"))
            _filter.add_pattern("*.rtk")
            _dialog.add_filter(_filter)

            _filter = gtk.FileFilter()
            _filter.set_name(_(u"All files"))
            _filter.add_pattern("*")
            _dialog.add_filter(_filter)

            if _dialog.run() == gtk.RESPONSE_ACCEPT:
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_PROG_INFO['database'] = \
                    _dialog.get_filename()

            _dialog.destroy()

            self._mdcRAMSTK.request_do_open_program()

        return None
