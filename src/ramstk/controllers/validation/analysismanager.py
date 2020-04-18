# -*- coding: utf-8 -*-
#
#       ramstk.controllers.validation.aalysismanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Validation Controller Package analysis manager."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.controllers import RAMSTKAnalysisManager


class AnalysisManager(RAMSTKAnalysisManager):
    """
    Contain the attributes and methods of the Validation analysis manager.

    This class manages the validation analysis for Allocation, MIL-HDBK-217F,
    NSWC, and Similar Item.  Attributes of the validation Analysis Manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the validation item being analyzed.
    """
    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 **kwargs: Dict[str, Any]) -> None:
        """
        Initialize an instance of the validation analysis manager.

        :param configuration: the Configuration instance associated with the
            current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        super().__init__(configuration, **kwargs)

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
        pub.subscribe(self.do_calculate_tasks,
                      'request_calculate_validation_tasks')

    def do_calculate_tasks(self) -> None:
        """
        Calculate mean, standard error, and bounds on the task time and cost.

        These values are calculated assuming a beta distribution (typical
        project management assumption).

        :return: None
        :rtype: None
        """
        # Retrieve all the attributes from all the RAMSTK data tables for the
        # requested function.  We need to build a comprehensive dict of
        # attributes to pass to the various analysis methods/functions.
        pub.sendMessage('request_get_validation_tree')

        _program_cost_remaining = 0.0
        _program_time_remaining = 0.0

        for _node in self._tree.all_nodes()[1:]:
            _node.data['validation'].calculate_task_time()
            _node.data['validation'].calculate_task_cost()

            _program_cost_remaining += (_node.data['validation'].cost_average
                                        * _node.data['validation'].status)
            _program_time_remaining += (_node.data['validation'].time_average
                                        * _node.data['validation'].status)

        pub.sendMessage('succeed_calculate_tasks',
                        cost_remaining=_program_cost_remaining,
                        time_remaining=_program_time_remaining)
