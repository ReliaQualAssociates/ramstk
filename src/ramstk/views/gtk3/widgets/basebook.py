# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.BaseBook.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Book Meta-Class."""

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.views.gtk3 import GObject, Gtk


class RAMSTKBaseBook(Gtk.Notebook):
    """The RAMSTK Book meta-class.

    Attributes of the Base Book are:

    :cvar dict dictab_position: dictionary containing the available
        Gtk.Notebook tab positions and associated noun name.
    :ivar RAMSTK_USER_CONFIGURATION: the RAMSTKUserConfiguration class
        instance.
    """

    RAMSTK_SITE_CONFIGURATION = None

    dic_tab_position = {
        'left': Gtk.PositionType.LEFT,
        'right': Gtk.PositionType.RIGHT,
        'top': Gtk.PositionType.TOP,
        'bottom': Gtk.PositionType.BOTTOM
    }

    def __init__(self, configuration: RAMSTKUserConfiguration) -> None:
        """Initialize an instance of the Module Book class.

        :param configuration: the RAMSTKUserConfiguration class instance.
        """
        GObject.GObject.__init__(self)  # pylint: disable=non-parent-init-called

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dic_handler_id = {'': 0}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.RAMSTK_USER_CONFIGURATION = configuration

        # Subscribe to PyPubSub messages.

    def _set_properties(self, book: str) -> None:
        """Set properties of the RAMSTK Books and widgets.

        :param book: which book to set properties for.
        :return: None
        :rtype: None
        """
        try:
            _tab_position = self.dic_tab_position[
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_TABPOS[book].lower()]
        except KeyError:
            _tab_position = self.dic_tab_position['bottom']
        self.set_tab_pos(_tab_position)
