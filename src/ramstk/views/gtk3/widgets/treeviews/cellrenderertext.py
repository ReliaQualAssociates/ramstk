# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.treeviews.cellrenderertext.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKCellRendererText module."""

# Standard Library Imports
from datetime import date
from typing import Dict, Optional, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk, Gtk, Pango

# RAMSTK Local Imports
from ..widget import RAMSTKBaseWidget, WidgetProperties


class RAMSTKCellRendererText(Gtk.CellRendererText, RAMSTKBaseWidget):
    """The RAMSTKCellRendererText class."""

    # Define private scalar class attributes.
    _default_height = 25
    _default_width = 25
    _edit_signal = "edited"

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKCellRendererText widget."""
        RAMSTKBaseWidget.__init__(self)

        # Initialize public attributes.
        self.tree_model: Optional[Gtk.TreeStore] = None
        self.tree_row: Optional[Gtk.TreeIter] = None

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKCellRendererText.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKCellRendererText.
        """
        super().do_set_properties(properties)

        self.dic_properties["alignment"] = properties.get(
            "alignment", Pango.Alignment.LEFT
        )
        self.dic_properties["background_rgba"] = properties.get(
            "background_rgba", Gdk.RGBA(255.0, 255.0, 255.0, 1.0)
        )
        self.dic_properties["foreground_rgba"] = properties.get(
            "foreground_rgba", Gdk.RGBA(0.0, 0.0, 0.0, 1.0)
        )
        self.dic_properties["wrap_mode"] = properties.get(
            "wrap_mode", Pango.WrapMode.WORD
        )
        self.dic_properties["wrap_width"] = properties.get("wrap_width", 25)
        self.dic_properties["xalign"] = properties.get("xalign", 0.5)
        self.dic_properties["yalign"] = properties.get("yalign", 0.5)

        self.set_property("background-rgba", self.dic_properties["background_rgba"])
        self.set_property("foreground-rgba", self.dic_properties["foreground_rgba"])
        self.set_property("wrap-mode", self.dic_properties["wrap_mode"])
        self.set_property("wrap-width", self.dic_properties["wrap_width"])
        self.set_alignment(self.dic_properties["xalign"], self.dic_properties["yalign"])

    def do_update(self, package: Dict[str, Union[bool, date, float, int, str]]) -> None:
        """Update the RAMSTKCellRendererText with a new value.

        :param package: the date package to use to update the RAMSTKCellRendererText.
        """
        if not package:
            return

        _key, _value = next(iter(package.items()))

        if self.tree_row is not None:
            self.tree_model.set_value(  # type: ignore[union-attr]
                self.tree_row,
                self.index,
                _value,
            )

    def on_changed(
        self,
        __cellrender: Gtk.CellRenderer,
        path: str,
        new_text: str,
    ):
        """Retrieve the data package for the RAMSTKCellRendererText on value changes.

        This method also sends a PyPubSub message along with the data package for
        listeners to update with the new value.

        :param __cellrender: the RAMSTKCellRendererText that just changed.
        :param path: the RAMSTKTreeView path to the RAMSTKCellRendererText that just
            changed.
        :param new_text: the new text in the RAMSTKCellRendererText.
        """
        _new_text: Union[float, int, str] = ""

        _type_dic: Dict[str, Union[float, int, str]] = {
            "gchararray": str(new_text),
            "gint": int(new_text),
            "gfloat": float(new_text),
        }
        _new_text = _type_dic[str(self.datatype)]

        self.tree_model[  # type: ignore[index] # pylint: disable=unsubscriptable-object
            path
        ][self.index] = _new_text
        _package = {self.field: _new_text}

        pub.sendMessage(self.send_topic, node_id=self.record_id, package=_package)
