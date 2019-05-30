# -*- coding: utf-8 -*-
#
#       ramstk.usage.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Usage Profile Package Data Controller."""

# Import third party modules.
from pubsub import pub

# Import other RAMSTK modules.
from ramstk.modules import RAMSTKDataController
from . import dtmUsageProfile


class UsageProfileDataController(RAMSTKDataController):
    """
    Provide an interface for the Usage Profile data model and an RAMSTK view.

    The Usage Profile controller provides an interface between the Usage
    Profile data model and an RAMSTK view model.  A single Usage Profile
    controller can control one or more Usage Profile data models.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize an instance of the Usage Profile data controller.

        :param dao: the RAMSTK Program DAO instance to pass to the Mission,
                    Mission Phase, and Environment Data Models.
        :type dao: :py:class:`ramstk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RAMSTK application.
        :type configuration: :py:class:`ramstk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
            self,
            configuration,
            model=dtmUsageProfile(dao, **kwargs),
            ramstk_module='usage_profile',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.request_do_delete, 'request_delete_profile')
        pub.subscribe(self._request_do_insert, 'request_insert_profile')
        pub.subscribe(self.request_do_select_all, 'selected_revision')
        pub.subscribe(self.request_do_update, 'request_update_profile')
        pub.subscribe(self.request_do_update_all,
                      'request_update_all_profiles')
        pub.subscribe(self.request_set_attributes, 'editing_profile')

    def _request_do_insert(self, entity_id, parent_id, level, **kwargs):
        """
        Request to add a record.

        This method will add a RAMSTKMission, RAMSTKMissionPhase, or
        RAMSTKEnvironment record.

        :param int entity_id: the RAMSTK Program database Revision ID,
                              Mission ID, or Mission Phase ID to add the entity
                              to.
        :param int parent_id: the Node ID of the parent node in the treelib
                              Tree().
        :param str level: the level of entity to add to the Usage Profile.
                          Levels are:

                          * mission
                          * phase
                          * environment

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_insert(
            entity_id=entity_id, parent_id=parent_id, level=level)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_last_id(self, **kwargs):
        """
        Request the last Mission, Mission Phase, or Environment ID used.

        :return: the last Mission, Mission Phase, or Environment ID used.
        :rtype: int
        """
        _entity = kwargs['entity']

        if _entity == 'mission':
            _last_id = self._dtm_data_model.dtm_mission.last_id
        elif _entity == 'phase':
            _last_id = self._dtm_data_model.dtm_phase.last_id
        elif _entity == 'environment':
            _last_id = self._dtm_data_model.dtm_environment.last_id
        else:
            _last_id = None

        return _last_id
