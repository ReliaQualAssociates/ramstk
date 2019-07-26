# -*- coding: utf-8 -*-
#
#       ramstk.controllers.validation.aalysismanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Validation Controller Package analysis manager."""

# Standard Library Imports
from collections import OrderedDict
from math import exp

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKAnalysisManager


class AnalysisManager(RAMSTKAnalysisManager):
    """
    Contain the attributes and methods of the Validation analysis manager.

    This class manages the validation analysis for Allocation, MIL-HDBK-217F,
    NSWC, and Similar Item.  Attributes of the validation Analysis Manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the validation item being analyzed.
    """
    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize an instance of the validation analysis manager.

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
                      'succeed_get_all_validation_attributes')
        pub.subscribe(self.on_get_tree, 'succeed_get_validation_tree')
