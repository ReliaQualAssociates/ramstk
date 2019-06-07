# -*- coding: utf-8 -*-
#
#       ramstk.revision.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Revision Package Data Controller."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.modules import RAMSTKDataController

# RAMSTK Local Imports
from . import dtmRevision


class RevisionDataController(RAMSTKDataController):
    """
    Provide an interface between the Revision data model and an RAMSTK view model.

    A single Revision controller can manage one or more Revision data models.
    The attributes of a Revision data controller are:
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Revision data controller instance.

        :param dao: the RAMSTK Program DAO instance to pass to the Revision Data
                    Model.
        :type dao: :py:class:`ramstk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RAMSTK application.
        :type configuration: :py:class:`ramstk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
            self,
            configuration,
            model=dtmRevision(dao, **kwargs),
            ramstk_module='revision',
            **kwargs,
        )

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.request_do_delete, 'request_delete_revision')
        pub.subscribe(self.request_do_insert, 'request_insert_revision')
        pub.subscribe(self.request_do_update, 'request_update_revision')
        pub.subscribe(
            self.request_do_update_all,
            'request_update_all_revisions',
        )
        pub.subscribe(self.request_set_attributes, 'mvw_editing_revision')
        pub.subscribe(self.request_set_attributes, 'wvw_editing_revision')
