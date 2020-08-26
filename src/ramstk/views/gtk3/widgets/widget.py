# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.widget.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK GTK3 Base Widget Module."""

# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.views.gtk3 import GObject, _


class RAMSTKWidget():
    """This is the RAMSTK Base Widget class."""
    def __init__(self) -> None:
        r"""
        Create RAMSTK Base widgets.
        """
        GObject.GObject.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dic_handler_id: Dict[str, int] = {'': 0}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.height: int = -1
        self.width: int = -1

    def do_set_properties(self, **kwargs: Any) -> None:
        r"""
        Set the properties of the RAMSTK combobox.

        :param \**kwargs: See below

        :Keyword Arguments:
            * *height* (int) -- height of the RAMSTKWidget().
            * *tooltip* (str) -- the tooltip, if any, for the combobox.
                Default is a message to file a QA-type issue to have one added.
            * *width* (int) -- width of the RAMSTKWidget().
        :return: None
        :rtype: None
        """
        _height = kwargs.get('height', self._default_height)
        _tooltip = kwargs.get(
            'tooltip',
            _("Missing tooltip, please file a quality type issue to have one "
              "added."))
        _width = kwargs.get('width', self._default_width)

        if _height == 0:
            _height = self._default_height
        if _width == 0:
            _width = self._default_width

        self.height = _height
        self.width = _width
        self.set_property('height-request', _height)
        self.set_property('tooltip-markup', _tooltip)
        self.set_property('width-request', _width)
