# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.dialogs.date_select_dialog.py is part of the
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKDateSelectDialog module."""

# Standard Library Imports
from datetime import datetime
from typing import Any, Tuple

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk

# RAMSTK Local Imports
from . import RAMSTKBaseDialog


class RAMSTKDateSelectDialog(RAMSTKBaseDialog):
    """The RAMSTKDateSelectDialog class."""

    def __init__(
        self,
        title: str,
        parent: object,
        buttons: Tuple[Any, Any, Any, Any] = (
            Gtk.STOCK_OK,
            Gtk.ResponseType.ACCEPT,
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
        ),
    ) -> None:
        """Initialize an instance of the RAMSTKDateSelectDialog widget.

        :param title: the title text for the RAMSTKDateSelectDialog.
        :param buttons: a tuple containing the buttons and their associated response
            type.
        """
        RAMSTKBaseDialog.__init__(self, title, parent, buttons)

        self.add_buttons(*buttons)
        self.set_title(title)

        self._calendar = Gtk.Calendar()
        self.vbox.pack_start(self._calendar, True, True, 0)
        self.vbox.show_all()

    # ----- ----- RAMSTKDateSelectDialog specific methods. ----- ----- #
    def do_run(self) -> str:
        """Run the RAMSTKDateSelectDialog.

        :return: the selected date or the default date if the dialog is cancelled.
        :rtype: str
        """
        _date = "1970-01-01"

        if self.run() == Gtk.ResponseType.ACCEPT:
            _getdate = self._calendar.get_date()
            _date = (
                datetime(
                    _getdate[0],
                    _getdate[1] + 1,
                    _getdate[2],
                )
                .date()
                .strftime("%Y-%m-%d")
            )

        return _date
