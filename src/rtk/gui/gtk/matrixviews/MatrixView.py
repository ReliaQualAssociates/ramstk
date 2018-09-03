# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.matrixviews.MatrixView.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""The RAMSTKMatrixView Meta-Class Module."""

# Import other RAMSTK modules.
from rtk.gui.gtk.rtk.Widget import gtk
from rtk.gui.gtk import rtk


class RAMSTKMatrixView(gtk.HBox, rtk.RAMSTKBaseMatrix):
    """
    This is the meta class for all RAMSTK Matrix View classes.

    Attributes of the RAMSTKMatrixView are:

    :ivar hbx_tab_label: the gtk.HBox() containing the label for the List and
                         Matrix View page.
    :type hbx_tab_label: :class:`gtk.HBox`
    """

    def __init__(self, controller, **kwargs):
        """
        Initialize the List View.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :py:class:`rtk.RAMSTK.RAMSTK`
        """
        gtk.HBox.__init__(self)
        rtk.RAMSTKBaseMatrix.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.hbx_tab_label = gtk.HBox()
