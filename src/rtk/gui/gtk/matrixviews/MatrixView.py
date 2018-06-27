# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.matrixviews.MatrixView.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""The RTKMatrixView Meta-Class Module."""

# Import other RTK modules.
from rtk.gui.gtk.rtk.Widget import gtk
from rtk.gui.gtk import rtk


class RTKMatrixView(gtk.HBox, rtk.RTKBaseMatrix):
    """
    This is the meta class for all RTK Matrix View classes.

    Attributes of the RTKMatrixView are:

    :ivar hbx_tab_label: the gtk.HBox() containing the label for the List and
                         Matrix View page.
    :type hbx_tab_label: :class:`gtk.HBox`
    """

    def __init__(self, controller, **kwargs):
        """
        Initialize the List View.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """
        gtk.HBox.__init__(self)
        rtk.RTKBaseMatrix.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.hbx_tab_label = gtk.HBox()
