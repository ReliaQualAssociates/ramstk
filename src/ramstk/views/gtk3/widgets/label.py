# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.Label.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKLabel module."""

# Standard Library Imports
from datetime import date
from typing import Dict, List, Tuple, Union

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, Pango

# RAMSTK Local Imports
from .widget import RAMSTKBaseWidget, WidgetProperties


class RAMSTKLabel(Gtk.Label, RAMSTKBaseWidget):
    """The RAMSTKLabel class."""

    # Define private class attributes.
    _default_height = 25
    _default_width = 190
    _edit_signal = ""

    def __init__(self, text: str) -> None:
        """Initialize an instance of the RAMSTKLabel widget.

        :param text: the text to display in the label.
        """
        RAMSTKBaseWidget.__init__(self)

        self.dic_properties["label"] = "<span>" + text + "</span>"

        self.set_markup(self.dic_properties["label"])
        self.show()

    # ----- ----- Standard widget methods. ----- ----- #
    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKLabel.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKLabel.
        """
        super().do_set_properties(properties)

        self.dic_properties["angle"] = properties.get("angle", 0.0)
        self.dic_properties["bold"] = properties.get("bold", True)
        self.dic_properties["ellipsize"] = properties.get(
            "ellipsize", Pango.EllipsizeMode.NONE
        )
        self.dic_properties["label"] = (
            "<span>" + properties.get("label", "") + "</span>"
        )
        self.dic_properties["lines"] = properties.get("lines", -1)
        self.dic_properties["justify"] = properties.get(
            "justify", Gtk.Justification.RIGHT
        )
        self.dic_properties["wrap"] = properties.get("wrap", False)

        self.set_property("wrap", self.dic_properties["wrap"])
        self.set_property("justify", self.dic_properties["justify"])
        if self.dic_properties["justify"] == Gtk.Justification.CENTER:
            self.set_xalign(0.5)
        elif self.dic_properties["justify"] == Gtk.Justification.LEFT:
            self.set_xalign(0.05)
        else:
            self.set_xalign(0.99)
        self.set_yalign(0.5)

        if self.dic_properties["bold"]:
            self.dic_properties["label"] = "<b>" + self.dic_properties["label"] + "</b>"
        self.set_markup(self.dic_properties["label"])
        self.set_property(
            "tooltip-markup",
            self.dic_properties["tooltip"],
        )

    def do_update(self, package: Dict[str, Union[bool, date, float, int, str]]) -> None:
        """Update the RAMSTKLabel to a new value.

        :param package: the date package to use to update the RAMSTKLabel.
        """
        _field: str
        _value: str

        _field, _raw_value = next(iter(package.items()))
        _value = str(_raw_value)

        if _field != self.field:
            return

        self.dic_properties["label"] = "<span>" + _value + "</span>"
        if self.dic_properties["bold"]:
            self.dic_properties["label"] = "<b>" + self.dic_properties["label"] + "</b>"
        self.set_markup(self.dic_properties["label"])


def do_make_label_group(
    label_text: List[str],
) -> Tuple[int, List[RAMSTKLabel]]:
    """Make and place a group of RAMSTKLabels.

    The width of each label is set using a natural request.  This ensures the label
    doesn't cut off letters.  The maximum size of the labels is determined and used to
    set the left position of widget displaying the data described by the label.  This
    ensures everything lines up.  It also returns a list of y-coordinates indicating the
    placement of each label that is used to place the corresponding widget.

    :param label_text: a list containing the text for each label.
    :return: (_max_x, _lst_labels) the width of the label with the longest text and a
        list of the RAMSTKLabel instances.
    :rtype: tuple of (integer, list of RAMSTKLabel)
    """
    _lst_labels = []
    _max_x = 0

    _char_width = max(len(_label_text) for _label_text in label_text)

    for _label_text in label_text:
        _label = RAMSTKLabel(_label_text)
        _label.set_width_chars(_char_width)
        _max_x = max(_max_x, _label.get_preferred_size()[0].width)
        _lst_labels.append(_label)

    return _max_x, _lst_labels
