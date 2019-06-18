# -*- coding: utf-8 -*-
#
#       ramstk.modules.failure_definition.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Failure Defintion Package Data Controller Module."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.modules import RAMSTKDataController

# RAMSTK Local Imports
from . import dtmFailureDefinition


class FailureDefinitionDataController(RAMSTKDataController):
    """
    Provide an interface between Failure Definition data models and RAMSTK views.

    A single Failure Definition data controller can manage one or more Failure
    Definition data models.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Failure Definition data controller instance.

        :param dao: the data access object used to communicate with the
                    connected RAMSTK Program database.
        :type dao: :py:class:`ramstk.dao.DAO.DAO`
        :param configuration: the RAMSTK configuration instance.
        :type configuration: :py:class:`ramstk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
            self,
            configuration,
            model=dtmFailureDefinition(dao, **kwargs),
            ramstk_module='failure_definition',
            **kwargs,
        )

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.request_do_delete, 'request_delete_definition')
        pub.subscribe(self.request_do_insert, 'request_insert_definition')
        pub.subscribe(self.request_do_select_all, 'selected_revision')
        pub.subscribe(self.request_do_update, 'request_update_definition')
        pub.subscribe(
            self.request_do_update_all,
            'request_update_all_definitions',
        )
        pub.subscribe(self.request_set_attributes, 'editing_definition')
