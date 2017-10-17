# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.listviews.Revision.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
Revision Package List Book View
###############################################################################
"""

# Import other RTK modules.
# pylint: disable=E0401
from gui.gtk.listviews.UsageProfile import ListView as lvwUsageProfile
# pylint: disable=E0401
from gui.gtk.listviews.FailureDefinition \
    import ListView as lvwFailureDefinition
from .ListView import RTKListView


class ListView(RTKListView):
    """
    The List View displays all the matrices and lists associated with the
    Revision Class.  The attributes of a List View are:
    """

    def __init__(self, controller):
        """
        Method to initialize the List View for the Revision package.

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
        self.lvw_usage_profile = lvwUsageProfile(controller)
        self.lvw_failure_definition = lvwFailureDefinition(controller)

        self._notebook.insert_page(
            self.lvw_usage_profile,
            tab_label=self.lvw_usage_profile.hbx_tab_label,
            position=-1)
        self._notebook.insert_page(
            self.lvw_failure_definition,
            tab_label=self.lvw_failure_definition.hbx_tab_label,
            position=-1)
