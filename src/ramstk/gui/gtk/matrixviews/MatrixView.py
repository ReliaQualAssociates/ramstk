# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.matrixviews.MatrixView.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKMatrixView Meta-Class Module."""

# Import other RAMSTK modules.
from ramstk.gui.gtk.ramstk.Widget from gi.repository import Gtk
from ramstk.gui.gtk import ramstk


class RAMSTKMatrixView(Gtk.HBox, ramstk.RAMSTKBaseMatrix):
    """
    This is the meta class for all RAMSTK Matrix View classes.

    Attributes of the RAMSTKMatrixView are:

    :ivar hbx_tab_label: the Gtk.HBox() containing the label for the List and
                         Matrix View page.
    :type hbx_tab_label: :class:`Gtk.HBox`
    """

    def __init__(self, controller, **kwargs):
        """
        Initialize the List View.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :py:class:`ramstk.RAMSTK.RAMSTK`
        """
        GObject.GObject.__init__(self)
        ramstk.RAMSTKBaseMatrix.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.hbx_tab_label = Gtk.HBox()
