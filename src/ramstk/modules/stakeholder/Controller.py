# -*- coding: utf-8 -*-
#
#       ramstk.modules.stakeholder.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Stakeholder Package Data Controller."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.modules import RAMSTKDataController

# RAMSTK Local Imports
from . import dtmStakeholder


class StakeholderDataController(RAMSTKDataController):
    """
    Provide an interface between the Stakeholder data model and an RAMSTK View.

    A single Stakeholder controller can manage one or more Stakeholder data
    models.  The attributes of a Stakeholder data controller are:
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Stakeholder data controller instance.

        :param dao: the RAMSTK Program DAO instance to pass to the Stakeholder
                    Data Model.
        :type dao: :class:`ramstk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
            self,
            configuration,
            model=dtmStakeholder(dao, **kwargs),
            ramstk_module='stakeholder',
            **kwargs,
        )

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self.request_do_calculate,
            'request_calculate_stakeholder',
        )
        pub.subscribe(
            self.request_do_calculate_all,
            'request_calculate_all_stakeholders',
        )
        pub.subscribe(self.request_do_delete, 'request_delete_stakeholder')
        pub.subscribe(self.request_do_insert, 'request_insert_stakeholder')
        pub.subscribe(self.request_do_select_all, 'selected_revision')
        pub.subscribe(self.request_do_update, 'request_update_stakeholder')
        pub.subscribe(
            self.request_do_update_all,
            'request_update_all_stakeholders',
        )
        pub.subscribe(self.request_set_attributes, 'editing_stakeholder')
