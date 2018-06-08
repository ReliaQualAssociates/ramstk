# -*- coding: utf-8 -*-
#
#       rtk.usage.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Usage Profile Package Data Controller."""

from pubsub import pub

# Import other RTK modules.
from rtk.modules import RTKDataController
from . import dtmUsageProfile


class UsageProfileDataController(RTKDataController):
    """
    Provide an interface for the Usage Profile data model and an RTK view.

    The Usage Profile controller provides an interface between the Usage
    Profile data model and an RTK view model.  A single Usage Profile
    controller can control one or more Usage Profile data models.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize an instance of the Usage Profile data controller.

        :param dao: the RTK Program DAO instance to pass to the Mission,
                    Mission Phase, and Environment Data Models.
        :type dao: :py:class:`rtk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """
        RTKDataController.__init__(
            self,
            configuration,
            model=dtmUsageProfile(dao),
            rtk_module='usage_profile',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_do_insert(self, **kwargs):
        """
        Request to add a RTKMission, RTKMissionPhase, or RTKEnvironment record.

        :param int entity_id: the RTK Program database Revision ID, Mission ID,
                              or Mission Phase ID to add the entity to.
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
        _entity_id = kwargs['entity_id']
        _parent_id = kwargs['parent_id']
        _level = kwargs['level']
        _error_code, _msg = self._dtm_data_model.do_insert(
            entity_id=_entity_id, parent_id=_parent_id, level=_level)

        # If the add was successful log the success message to the user log.
        # Otherwise, update the error message and write it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self._test:
                if _level == 0:
                    pub.sendMessage('addedMission')
                elif _level == 1:
                    pub.sendMessage('addedPhase')
                elif _level == 2:
                    pub.sendMessage('addedEnvironment')

        else:
            _msg = _msg + '  Failed to add a new Usage Profile entity to ' \
                          'the RTK Program '
            self._configuration.RTK_DEBUG_LOG.error(_msg)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_do_delete(self, node_id):
        """
        Request to delete a RTKMission, RTKMissionPhase, or RTKEnvironment.

        :param int node_id: the Mission, Mission Phase, Environment ID to add
                            the entity.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_delete(node_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_do_update(self, node_id):
        """
        Request to update an RTKMission, RTKMissionPhase, or RTKEnvironment.

        :param int node_id: the ID of the entity to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update(node_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_do_update_all(self, **kwargs):
        """
        Request to update all records in the Usage Profile tables.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update_all(**kwargs)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
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
