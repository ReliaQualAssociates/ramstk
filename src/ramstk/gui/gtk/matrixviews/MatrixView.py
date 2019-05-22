# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.matrixviews.MatrixView.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKMatrixView Meta-Class Module."""

# Import other RAMSTK modules.
from ramstk.gui.gtk.ramstk.Widget import GObject, Gtk
from ramstk.gui.gtk.ramstk import RAMSTKBaseMatrix


class RAMSTKMatrixView(Gtk.HBox, RAMSTKBaseMatrix):
    """
    This is the meta class for all RAMSTK Matrix View classes.

    Attributes of the RAMSTKMatrixView are:

    :ivar hbx_tab_label: the Gtk.HBox() containing the label for the List and
                         Matrix View page.
    :type hbx_tab_label: :class:`Gtk.HBox`
    """

    def __init__(self, configuration, **kwargs):
        """
        Initialize an instance of the RAMSTK Matrix View.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        GObject.GObject.__init__(self)
        RAMSTKBaseMatrix.__init__(self, configuration**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.
