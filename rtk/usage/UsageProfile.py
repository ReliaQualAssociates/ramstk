# -*- coding: utf-8 -*-
#
#       rtk.usage.UsageProfile.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
Usage Profile Module
###############################################################################
"""

# Import modules for localization support.
import gettext

from pubsub import pub                              # pylint: disable=E0401

# Import other RTK modules.
# pylint: disable=E0401
from dao import RTKMission, RTKMissionPhase, RTKEnvironment
from datamodels import RTKDataModel                 # pylint: disable=E0401
from datamodels import RTKDataController            # pylint: disable=E0401
from .Mission import Model as Mission
from .Phase import Model as Phase
from .Environment import Model as Environment

_ = gettext.gettext


class Model(RTKDataModel):
    """
    Class for Usage Profile data model.  This model builds a Usage Profile from
    the Mission, Phase, and Environment data models.  This is a hierarchical
    relationship, such as:

          Mission 1
          |
          |_Mission Phase 11
          |   |
          |   |_Environment 111
          |   |_Environment 112
          |   |_Environment 113
          |
          |_Mission Phase 12
          |   |
          |   |_Environment 121
          |   |_Environment 122
          |
          Mission 2
          |
          |_Mission Phase 21
              |
              |_Environment 211
              |_Environment 212
    """

    _tag = 'Usage Profiles'

    def __init__(self, dao):
        """
        Method to initialize a Usage Profile data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :py:class:`rtk.dao.DAO.DAO`
        """

        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtm_mission = Mission(dao)
        self._dtm_phase = Phase(dao)
        self._dtm_environment = Environment(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select_all(self, revision_id):
        """
        Method to retrieve and build the Usage Profile tree for Revision ID.

        :param int revision_id: the Revision ID to retrieve the Usage Profile
                                and build trees for.
        :return: tree; the Usage Profile treelib Tree().
        :rtype: :py:class:`treelib.Tree`
        """

        RTKDataModel.select_all(self)

        # Build the tree.  We concatenate the Mission ID and the Phase ID to
        # create the Node() identifier for Mission Phases.  This prevents the
        # likely case when the first Mission and Phase have the same ID (1) in
        # the database from causing problems when building the tree.  Do the
        # same for the environment by concatenating the Environment ID with the
        # Mission ID and Phase ID.
        _missions = self._dtm_mission.select_all(revision_id).nodes

        # pylint: disable=too-many-nested-blocks
        for _mkey in _missions:
            _mission = _missions[_mkey].data
            if _mission is not None:
                self.tree.create_node(tag=_mission.description,
                                      identifier=_mission.mission_id,
                                      parent=0, data=_mission)

                # Add the phases, if any, to the mission.
                _phases = self._dtm_phase.select_all(_mission.mission_id).nodes
                for _pkey in _phases:
                    _phase = _phases[_pkey].data
                    if _phase is not None:
                        _phase_id = int(str(_mission.mission_id) +
                                        str(_phase.phase_id))
                        self.tree.create_node(tag=_phase.description,
                                              identifier=_phase_id,
                                              parent=_mission.mission_id,
                                              data=_phase)

                        # Add the environments, if any, to the phase.
                        _environments = self._dtm_environment.select_all(
                            _phase.phase_id).nodes
                        for _ekey in _environments:
                            _environment = _environments[_ekey].data
                            if _environment is not None:
                                _env_id = int(str(_mission.mission_id) +
                                              str(_phase.phase_id) +
                                              str(_environment.environment_id))
                                # The parent must be the concatenated phase ID
                                # used in the tree above, not the Phase ID
                                # attribute of the RTKPhase object.
                                self.tree.create_node(tag=_environment.name,
                                                      identifier=_env_id,
                                                      parent=_phase_id,
                                                      data=_environment)

        return self.tree

    def insert(self, entity_id, parent_id, level):
        """
        Method to add an entity to the Usage Profile and RTK Program database..

        :param int entity_id: the RTK Program database Revision ID, Mission ID,
                              Mission Phase ID to add the entity to.
        :param int parent_id: the Node ID of the parent node in the treelib
                              Tree().
        :param str level: the type of entity to add to the Usage Profile.
                          Levels are:

                          * mission
                          * phase
                          * environment

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _tag = 'Tag'
        _node_id = -1

        if level == 'mission':
            _entity = RTKMission()
            _entity.revision_id = entity_id
        elif level == 'phase':
            _entity = RTKMissionPhase()
            _entity.mission_id = entity_id
        elif level == 'environment':
            _entity = RTKEnvironment()
            _entity.phase_id = entity_id
        else:
            _entity = None

        _error_code, _msg = RTKDataModel.insert(self, [_entity, ])

        if level == 'mission':
            _tag = _entity.description
            _node_id = _entity.mission_id
        elif level == 'phase':
            _tag = _entity.name
            _node_id = int(str(parent_id) + str(_entity.phase_id))
        elif level == 'environment':
            _tag = _entity.name
            _node_id = int(str(parent_id) + str(_entity.environment_id))

        if _error_code == 0:
            self.tree.create_node(_tag, _node_id, parent=parent_id,
                                  data=_entity)
        else:
            _error_code = 2105
            _msg = 'RTK ERROR: Attempted to add an item to the Usage ' \
                   'Profile with an undefined indenture level.  Level {0:s} ' \
                   'was requested.  Must be one of mission, phase, or ' \
                   'environment.'.format(level)

        return _error_code, _msg

    def delete(self, node_id):
        """
        Method to remove an entity from the Usage Profile and RTK Program
        database.

        :param int node_id: the Node ID of the entity to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _entity = self.tree.get_node(node_id).data
            _error_code, _msg = RTKDataModel.delete(self, _entity)

            if _error_code == 0:
                self.tree.remove_node(node_id)

        except AttributeError:
            _error_code = 2105
            _msg = 'RTK ERROR: Attempted to delete a non-existent entity ' \
                   'with Node ID {0:d} from the Usage Profile.'.format(node_id)

        return _error_code, _msg

    def update(self, node_id):
        """
        Method to update the environment associated with Phase ID to the RTK
        Program database.

        :param int node_id: the Node ID of the entity to save to the RTK
                            Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
            _error_code = 2106
            _msg = 'RTK ERROR: Attempted to save non-existent Usage Profile ' \
                   'item with Node ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def update_all(self):
        """
        Method to save all Usage Profile data packages to the RTK Program
        database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = ''

        for _key in self.tree.nodes:
            if _key != 0:
                _error_code, _msg = self.update(_key)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print _error_code

        return _error_code, _msg


class UsageProfile(RTKDataController):
    """
    The Usage Profile controller provides an interface between the Usage
    Profile data model and an RTK view model.  A single Usage Profile
    controller can control one or more Usage Profile data models.

    :ivar _dao: the :py:class:`rtk.dao.DAO.DAO` used to communicate with the
                RTK Project database.
    :ivar dict dicProfiles: Dictionary of the Usage Profile data models
                            controlled.  Key is the Revision ID; value is a
                            pointer to the instance of the Usage Profile data
                            model.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize an instance of the Usage Profile data controller.

        :param dao: the RTK Program DAO instance to pass to the Mission,
                    Mission Phase, and Environment Data Models.
        :type dao: :py:class:`rtk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """

        RTKDataController.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self.__test = kwargs['test']
        self._dtm_profile = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select(self, node_id):
        """
        Method to select the Node data package associated with node_id.

        :param int node_id: the Node ID of the data package to retrieve.
        :return: the instance of the RTKMission, RTKMissionPhase, or
                 RTKEnvironment associated with node_id
        """

        return self._dtm_profile.select(node_id)

    def request_select_all(self, revision_id):
        """
        Method to retrieve and build the Usage Profile tree for Revision ID.

        :param int revision_id: the Revision ID to retrieve the Usage Profile
                                and build trees for.
        :return: tree; the Usage Profile treelib Tree().
        :rtype: :py:class:`treelib.Tree`
        """

        return self._dtm_profile.select_all(revision_id)

    def request_insert(self, entity_id, parent_id, level):
        """
        Method to request a Mission, Mission Phase, or Environment be added to
        the Usage Profile.

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

        _return = False

        _error_code, _msg = self._dtm_profile.insert(entity_id, parent_id,
                                                     level)

        # If the add was successful log the success message to the user log.
        # Otherwise, update the error message and write it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self.__test:
                if level == 0:
                    pub.sendMessage('addedMission')
                elif level == 1:
                    pub.sendMessage('addedPhase')
                elif level == 2:
                    pub.sendMessage('addedEnvironment')

        else:
            _msg = _msg + '  Failed to add a new Usage Profile entity to ' \
                          'the RTK Program '
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_delete(self, node_id):
        """
        Method to request Mission, Mission Phase, or Environment and it's
        children be deleted from the Usage Profile.

        :param int node_id: the Mission, Mission Phase, Environment ID to add
                            the entity.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_profile.delete(node_id)

        # If the delete was successful log the success message to the user log.
        # Otherwise, update the error message and log it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_update_all(self):
        """
        Method to request the Usage Profile be saved to the RTK Program
        database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_profile.update_all()

        # If the update was successful log the success message to the user log.
        # Otherwise, update the error message and log it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_get_attributes(self, node_id):
        """
        Method to request the attributes from the selected Usage Profile data
        model.

        :param int node_id: the Node ID of the data package to retrieve.
        :return: _attributes
        :rtype: list
        """

        _node = self.request_select(node_id)

        return list(_node.get_attributes())
