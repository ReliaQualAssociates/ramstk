# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.dialogs.file_chooser_dialog.py is part of the
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKFileChooserDialog module."""

# Standard Library Imports
import os
from typing import Any, Tuple, Union

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets.dialogs.base_dialog import RAMSTKBaseDialog


class RAMSTKFileChooserDialog(Gtk.FileChooserDialog, RAMSTKBaseDialog):
    """The RAMSTKFileChooserDialog class."""

    def __init__(
        self,
        title: str,
        parent: object,
        buttons: Tuple[Any, Any, Any, Any] = (
            Gtk.STOCK_OK,
            Gtk.ResponseType.ACCEPT,
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.REJECT,
        ),
    ) -> None:
        """Initialize an instance of the RAMSTKFileChooserDialog widget.

        :param title: the title text for the RAMSTKFileChooserDialog.
        :param buttons: a tuple containing the buttons and their associated response
            type.
        """
        Gtk.FileChooserDialog(self)
        RAMSTKBaseDialog.__init__(self, title, parent, buttons)

        self.set_action(Gtk.FileChooserAction.SAVE)

    # ----- ----- Standard dialog methods. ----- ----- #
    def do_run(self) -> Tuple[Union[str, None], Union[str, None]]:
        """Run the RAMSTKFileChooserDialog.

        :return: (_filename, _extension); the file name and file extension of the
            selected file.
        :rtype: (str, str) or (None, None)
        """
        _filename = None
        _extension = None

        if self.run() == Gtk.ResponseType.ACCEPT:
            _filename = self.get_filename()
            # pylint: disable=unused-variable
            __, _extension = os.path.splitext(_filename)

        return _filename, _extension

    # ----- ----- RAMSTKFileChooserDialog specific methods. ----- ----- #
    def do_set_file_filters(
        self,
        filters=None,
    ) -> None:
        """Set file filters for the RAMSTKFileChooserDialog.

        :param filters: a list of dicts containing the name of the filter and a list of
            patterns to associate with the filter.
        """
        if filters is None:
            filters = [
                {"name": _("Excel Files"), "patterns": ["*.xls", "*.xlsm", "*.xlsx"]},
                {"name": _("Delimited Text Files"), "patterns": ["*.csv", "*.txt"]},
                {"name": _("All Files"), "patterns": ["*"]},
            ]

        for _filter in filters:
            _filter = Gtk.FileFilter()
            _filter.set_name(_filter["name"])
            for _pattern in _filter["patterns"]:
                _filter.add_pattern(_pattern)
            self.add_filter(_filter)
