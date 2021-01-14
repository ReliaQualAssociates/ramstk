# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.Label.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Label Module."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk

# RAMSTK Local Imports
from .widget import RAMSTKWidget


class RAMSTKLabel(Gtk.Label, RAMSTKWidget):
    """The RAMSTK Label class."""

    # Define private class scalar attributes.
    _default_height = 25
    _default_width = 190

    def __init__(self, text: str) -> None:
        """Create RAMSTKLabel widget.

        :param text: the text to display in the label.
        """
        RAMSTKWidget.__init__(self)

        self.set_markup("<span>" + text + "</span>")
        self.show_all()

    def get_attribute(self, attribute: str) -> Any:
        """Get the value of the requested attribute.

        :param attribute: the name of the attribute to retrieve.
        :return: the value of the requested attribute.
        """
        # The natural size = default size and the requested size = minimum size
        _attributes = {
            'height': self.get_preferred_height()[1],
            'width': self.get_preferred_width()[1]
        }

        return _attributes[attribute]

    def do_set_properties(self, **kwargs: Any) -> None:
        """Set the RAMSTKFrame properties.

        :Keyword Arguments:
            * *width* (int) -- width of the Gtk.Label() widget.  Default is
                190.
            * *height* (int) -- height of the Gtk.Label() widget.  Default is
                25.
            * *bold* (bool) -- boolean indicating whether text should be bold.
                Default is True.
            * *wrap* (bool) -- boolean indicating whether the label text should
                wrap or not.  Default is False.
            * *justify* (str) -- the justification type when the label wraps
                and contains more than one line.  Default is JUSTIFY_LEFT.
            * *tooltip* (str) -- the tooltip, if any, for the label.
                Default is an empty string.
        :return: None
        :rtype: None
        """
        super().do_set_properties(**kwargs)

        _bold = kwargs.get('bold', True)
        _justify = kwargs.get('justify', Gtk.Justification.LEFT)
        _wrap = kwargs.get('wrap', False)

        self.set_property('wrap', _wrap)
        self.set_property('justify', _justify)
        if _justify == Gtk.Justification.CENTER:
            self.set_xalign(0.5)
            self.set_yalign(0.5)
        elif _justify == Gtk.Justification.LEFT:
            self.set_xalign(0.05)
            self.set_yalign(0.5)
        else:
            self.set_xalign(0.99)
            self.set_yalign(0.5)

        if _bold:
            _text = self.get_property('label')
            _text = '<b>' + _text + '</b>'
            self.set_markup(_text)


def do_make_label_group(
        text: List[str], **kwargs: Dict[str,
                                        Any]) -> Tuple[int, List[RAMSTKLabel]]:
    """Make and place a group of labels.

    The width of each label is set using a natural request.  This ensures the
    label doesn't cut off letters.  The maximum size of the labels is
    determined and used to set the left position of widget displaying the data
    described by the label.  This ensures everything lines up.  It also returns
    a list of y-coordinates indicating the placement of each label that is used
    to place the corresponding widget.

    :param text: a list containing the text for each label.
    :return: (_max_x, _lst_labels)
        the width of the label with the longest text and a list of the
        RAMSTKLabel() instances.
    :rtype: tuple of (integer, list of RAMSTKLabel())
    """
    _bold = kwargs.get('bold', True)
    _justify = kwargs.get('justify', Gtk.Justification.RIGHT)
    _wrap = kwargs.get('wrap', True)

    _lst_labels = []
    _max_x = 0

    _char_width = max([len(_label_text) for _label_text in text])

    # pylint: disable=unused-variable
    for __, _label_text in enumerate(text):
        _label = RAMSTKLabel(_label_text)
        _label.do_set_properties(bold=_bold,
                                 height=-1,
                                 justify=_justify,
                                 width=-1,
                                 wrap=_wrap)
        _label.set_width_chars(_char_width)
        _max_x = max(_max_x, _label.get_attribute('width'))
        _lst_labels.append(_label)

    return _max_x, _lst_labels
