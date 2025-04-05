# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.dialogs.message_dialog.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKMessageDialog module."""

# Standard Library Imports
from typing import Any, Tuple

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.widgets.dialogs.base_dialog import RAMSTKBaseDialog


class RAMSTKMessageDialog(Gtk.MessageDialog, RAMSTKBaseDialog):
    """TheRAMSTKMessageDialog class.

    It used for RAMSTK error, warning, and information messages.
    """

    def __init__(
        self,
        title: str,
        parent: object,
        buttons: Tuple[Any, Any, Any, Any] = (
            Gtk.STOCK_OK,
            Gtk.ResponseType.OK,
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
        ),
    ) -> None:
        """Initialize an instance of the RAMSTKMessageDialog widget.

        :param title: the title text for the RAMSTKMessageDialog.
        :param parent: the parent window for the RAMSTKMessageDialog.
        :param buttons: a tuple containing the buttons and their associated response
            type.
        """
        Gtk.MessageDialog.__init__(self)
        RAMSTKBaseDialog.__init__(self, title, parent, buttons)

        self.show_all()

    # ----- ----- RAMSTKMessageDialog specific methods. ----- ----- #
    def do_set_message(self, message: str) -> None:
        """Set the message to display in the RAMSTKMessageDialog.

        :param message: the message for the RAMSTKMessageDialog to display.
        """
        self.set_markup(message)

    def do_set_message_type(self, message_type: str = "error") -> None:
        """Set RAMSTKMessageDialog message type.

        :param message_type: the RAMSTKMessageDialog message type. Options are error,
            warning, information, or question. Default is error.
        """
        _dic_message_type = {
            "error": Gtk.MessageType.ERROR,
            "warning": Gtk.MessageType.WARNING,
            "info": Gtk.MessageType.INFO,
            "question": Gtk.MessageType.QUESTION,
            "debug": Gtk.MessageType.OTHER,
        }

        _prompt = self.get_property("text")

        if message_type == "error":
            # Set the prompt to bold text with a hyperlink to the RAMSTK bugs
            # e-mail address.
            _prompt = (
                f"<b>{_prompt}</b>\n\nCheck the error log for additional information "
                f"(if any).  Please <span foreground='blue' underline='single'><a "
                f"href='https://github.com/ReliaQualAssociates/ramstk/issues'>raise "
                f"an issue</a></span> with a detailed description of the problem and "
                f"the error log attached if the problem persists."
            )

        self.set_markup(_prompt)
        self.set_property("message-type", _dic_message_type[message_type])

        if message_type in {"error", "warning", "info", "debug"}:
            self.add_buttons("_OK", Gtk.ResponseType.OK)
        elif message_type == "question":
            self.add_buttons(
                "_Yes",
                Gtk.ResponseType.YES,
                "_No",
                Gtk.ResponseType.NO,
            )
