# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.matrixviews.MatrixView.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
RTKMatrixView Meta-Class Module
-------------------------------------------------------------------------------
"""

# Import other RTK modules.
from gui.gtk.rtk.Widget import _, gobject, gtk  # pylint: disable=E0401,W0611
from gui.gtk import rtk  # pylint: disable=E0401,W0611


class RTKMatrixView(gtk.HBox, rtk.RTKBaseMatrix):
    """
    This is the meta class for all RTK Matrix View classes.  Attributes of the
    RTKMatrixView are:
    """

    def __init__(self, controller):
        """
        Method to initialize the List View.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        gtk.HBox.__init__(self)
        rtk.RTKMatrixView.__init__(self, controller)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.hbx_tab_label = gtk.HBox()
