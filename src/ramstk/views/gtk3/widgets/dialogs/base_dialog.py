# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.dialogs.base_dialog.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKBaseDialog module."""

# Standard Library Imports
from typing import Any, Optional, Tuple

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk

# RAMSTK Local Imports
from ..widget import RAMSTKBaseWidget, WidgetProperties


class RAMSTKBaseDialog(Gtk.Dialog, RAMSTKBaseWidget):
    """The RAMSTKBaseDialog class."""

    def __init__(
        self,
        title: str,
        parent: object,
        buttons: Optional[Tuple[Any, Any, Any, Any]] = None,
    ) -> None:
        """Initialize an instance of the RAMSTKBaseDialog widget.

        :param title: the title text for the RAMSTKBaseDialog.
        :param parent: the parent window for the RAMSTKBaseDialog.
        :param buttons: a tuple containing the buttons and their associated response
            type.
        """
        RAMSTKBaseWidget.__init__(self)

        if not buttons:
            buttons = (
                Gtk.STOCK_OK,
                Gtk.ResponseType.OK,
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
            )
        self.add_buttons(*buttons)
        if not parent in Gtk.Window.list_toplevels() and parent is not None:
            self.set_parent(parent)
        self.set_title(title)

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKBaseDialog.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKBaseDialog.
        """
        super().do_set_properties(properties)

        self.dic_properties["destroy_with_parent"] = properties.get(
            "destroy_with_parent", True
        )
        self.dic_properties["modal"] = properties.get("modal", True)
        self.dic_properties["parent"] = properties.get("parent", None)

        self.set_transient_for(self.dic_properties["parent"])
        self.set_destroy_with_parent(self.dic_properties["destroy_with_parent"])
        self.set_modal(self.dic_properties["modal"])

    # ----- ----- RAMSTKBaseDialog specific methods. ----- ----- #
    def do_destroy(self) -> None:  # pylint: disable=arguments-differ
        """Destroy the RAMSTKBaseDialog."""
        self.destroy()

    def do_run(self) -> Any:
        """Run the RAMSTKBaseDialog."""
        return self.run()

    def do_set_widget_attributes(self) -> None:
        """Set the properties of the RAMSTKBaseDialog widgets."""
        for _widget in self._lst_widget_configuration:
            _widget["widget"].do_set_properties(_widget["attributes"])

    def do_set_widget_callbacks(self) -> None:
        """Set the callback method for the RAMSTKBaseDialog widgets."""
        self.handler_id = self.connect(
            self._edit_signal,
            self.on_changed,
        )

    def do_set_widget_properties(self) -> None:
        """Set the properties of the RAMSTKBaseDialog widgets."""
        for _widget in self._lst_widget_configuration:
            _widget["widget"].do_set_properties(_widget["properties"])
