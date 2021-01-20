# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.assistants.export.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle "weibullguy" Rowland
"""Export Assistant Module."""

# Standard Library Imports
import os

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKFileChooser, RAMSTKMessageDialog


class ExportProject(RAMSTKFileChooser):
    """Assistant to walk user through the process of exporting records."""

    RAMSTK_USER_CONFIGURATION = RAMSTKUserConfiguration()

    def __init__(self, __button: Gtk.ToolButton,
                 configuration: RAMSTKUserConfiguration,
                 parent: object) -> None:
        """Initialize an instance of the Export Assistant.

        :param __button: the Gtk.ToolButton() that launched an instance of this
            class.
        :param configuration: the RAMSTKUserConfiguration class instance.
        :param parent: the parent window to associate this dialog with.
        """
        super().__init__(_("RAMSTK Export"), parent)

        # Initialize private dict variables.

        # Initialize private list variables.

        # Initialize private scalar variables.
        self._parent = parent

        # Initialize public dict variables.

        # Initialize public list variables.

        # Initialize public scalar variables.
        self.RAMSTK_USER_CONFIGURATION = configuration

        self.set_current_folder(self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_DIR)

        for _module in [
                'functions', 'requirements', 'hardwares', 'validations'
        ]:
            pub.sendMessage('request_get_{0}_tree'.format(_module))

        self._do_select_file()

    def _do_quit(self) -> None:
        """Quit the RAMSTK Export Assistant.

        :return: None
        :rtype: None
        """
        self.destroy()

    def _do_select_file(self) -> None:
        """Select the input file to export data to.

        :return: None
        :rtype: None
        """
        _cansave = False
        (_filename, _extension) = self.do_run()

        if _filename is not None:
            _filetype = {
                '.csv': 'csv',
                '.txt': 'text',
                '.xls': 'excel',
                '.xlsm': 'excel',
                '.xlsx': 'excel'
            }[_extension]  # type: ignore

            if os.path.exists(_filename):
                _dialog = RAMSTKMessageDialog(self._parent)
                _dialog.do_set_message(
                    _("File {0} already exists.  Overwrite?").format(
                        _filename))
                _dialog.do_set_message_type('question')
                _response = _dialog.do_run()
                if _response == Gtk.ResponseType.YES:
                    _dialog.destroy()
                    os.remove(_filename)
                    _cansave = True
                else:
                    _dialog.destroy()
            else:
                _cansave = True

            if _cansave:
                pub.sendMessage(
                    'request_export_data',
                    file_type=_filetype,
                    file_name=_filename,
                )
            else:
                self._do_select_file()

        self._do_quit()
