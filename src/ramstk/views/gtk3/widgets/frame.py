# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.frame.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKFrame module."""

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk

# RAMSTK Local Imports
from .label import RAMSTKLabel
from .widget import RAMSTKBaseWidget, WidgetProperties


class RAMSTKFrame(Gtk.Frame, RAMSTKBaseWidget):
    """The RAMSTKFrame class."""

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKFrame widget."""
        RAMSTKBaseWidget.__init__(self)

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKFrame.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKFrame.
        """
        super().do_set_properties(properties)

        self.dic_properties["label"] = str(properties.get("title", ""))
        self.dic_properties["shadow_type"] = properties.get(
            "shadow_type",
            Gtk.ShadowType.ETCHED_OUT,
        )

        _label: RAMSTKLabel = RAMSTKLabel(self.dic_properties["label"])
        _label.do_set_properties(properties)
        _label.show_all()
        self.set_label_widget(_label)
        self.set_shadow_type(self.dic_properties["shadow_type"])
