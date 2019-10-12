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
    """
    The RAMSTK Book meta-class.

    Attributes of the Base Book are:

    :cvar dict dictab_position: dictionary containing the available
        Gtk.Notebook tab positions and associated noun name.
    :ivar RAMSTK_USER_CONFIGURATION: the RAMSTKUserConfiguration class instance.
    :type RAMSTK_USER_CONFIGURATION: :class:`ramstk.configuration.RAMSTKUserConfiguration`
    """

    dic_tab_position = {
        'left': Gtk.PositionType.LEFT,
        'right': Gtk.PositionType.RIGHT,
        'top': Gtk.PositionType.TOP,
        'bottom': Gtk.PositionType.BOTTOM
    }

    def __init__(self, configuration: RAMSTKUserConfiguration) -> None:
        """
        Initialize an instance of the Module Book class.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        GObject.GObject.__init__(self)  # pylint: disable=non-parent-init-called
        self.RAMSTK_USER_CONFIGURATION = configuration
