# -*- coding: utf-8 -*-
#
#       ramstk.controllers.fmea.analysismanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""FMEA Controller Package analysis manager."""

# Standard Library Imports
from collections import OrderedDict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import criticality
from ramstk.controllers import RAMSTKAnalysisManager


class AnalysisManager(RAMSTKAnalysisManager):
    """
    Contain the attributes and methods of the Function analysis manager.

    This class manages the functional analysis for functional hazards analysis
    (FHA).  Attributes of the function Analysis Manager are:
    """

    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize an instance of the function analysis manager.

        :param configuration: the Configuration instance associated with the
            current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        super(AnalysisManager, self).__init__(configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_get_all_attributes,
                      'succeed_get_all_fmea_attributes')
        pub.subscribe(self.on_get_tree, 'succeed_get_fmea_tree')
