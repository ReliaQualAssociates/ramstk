# pylint: disable=protected-access, non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.buttons.file_chooser_button.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKFileChooserButton module."""

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk

# RAMSTK Local Imports
from ..widget import WidgetProperties
from . import RAMSTKButton


class RAMSTKFileChooserButton(Gtk.FileChooserButton, RAMSTKButton):
    """The RAMSTKFileChooserButton class."""

    def __init__(self, label: str = "...") -> None:
        """Initialize an instance of the RAMSTKFileChooserButton widget.

        :param label: the text for the RAMSTKFileChooserButton label.
        """
        RAMSTKButton.__init__(self)

        self.dic_properties["label"] = label

        self.set_title(label)
        self.show_all()

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKFileChooserButton.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKFileChooserButton.
        """
        super().do_set_properties(properties)

        self.dic_properties["action"] = properties.get("action")

        self.set_action(self.dic_properties["action"])
