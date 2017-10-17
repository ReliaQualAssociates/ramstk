# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.listviews.Function.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
Function Package List View
###############################################################################
"""

# Import other RTK modules.
from .ListView import RTKListView


class ListView(RTKListView):
    """
    The List View displays all the matrices and lists associated with the
    Function Class.  The attributes of a List View are:
    """

    def __init__(self, controller):
        """
        Method to initialize the List View for the Function package.

        :param controller: the RTK Master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        RTKListView.__init__(self, controller)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
