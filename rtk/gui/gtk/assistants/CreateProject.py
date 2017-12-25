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

from os import remove

# Import other RTK modules.
import Utilities  # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gtk, set_cursor  # pylint: disable=E0401
from gui.gtk import rtk  # pylint: disable=E0401


class CreateProject(object):
    """
    This is the class used to create a new RTK Project database.
    """

    def __init__(self, __button, controller):
        """
        Method to initialize an instance of the Create Project Assistant.

        :param __button: the gtk.ToolButton() that launched this class.
        :type __button: :py:class:`gtk.ToolButton`
        :param controller: the RTK master data controller.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._mdcRTK = controller

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        set_cursor(self._mdcRTK, gtk.gdk.WATCH)

        self._request_create_project()

        set_cursor(self._mdcRTK, gtk.gdk.LEFT_PTR)

    def _request_create_project(self):
        """
        Method to create a RTK Project database using SQLite3.
        """

        _dialog = gtk.FileChooserDialog(
            title=_(u"Create a RTK Program Database"),
            action=gtk.FILE_CHOOSER_ACTION_SAVE,
            buttons=(gtk.STOCK_NEW, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL,
                     gtk.RESPONSE_REJECT))
        _dialog.set_current_folder(self._mdcRTK.RTK_CONFIGURATION.RTK_PROG_DIR)

        if _dialog.run() == gtk.RESPONSE_ACCEPT:
            _new_program = _dialog.get_filename()
            _new_program = _new_program + '.rtk'

            if Utilities.file_exists(_new_program):
                _dlgConfirm = rtk.RTKDialog(
                    _(u"RTK - Confirm Overwrite"),
                    dlgbuttons=(gtk.STOCK_YES, gtk.RESPONSE_YES, gtk.STOCK_NO,
                                gtk.RESPONSE_NO))

                _label = rtk.RTLabel(
                    _(u"RTK Program database already exists. "
                      u"\n\n{0:s}\n\nOverwrite?").format(_new_program),
                    width=-1,
                    height=-1,
                    bold=False,
                    wrap=True)
                _dlgConfirm.vbox.pack_start(_label)  # pylint: disable=E1101
                _label.show()

                if _dlgConfirm.run() == gtk.RESPONSE_YES:
                    _dlgConfirm.destroy()
                    remove(_new_program)
                else:
                    _dlgConfirm.destroy()
                    _dialog.destroy()
                    return True

            self._mdcRTK.RTK_CONFIGURATION.RTK_PROG_INFO['database'] = \
                _new_program

        _dialog.destroy()

        self._mdcRTK.request_create_program()

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
