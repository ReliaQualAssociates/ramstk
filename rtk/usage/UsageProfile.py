#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.usage.UsageProfile.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Import modules for localization support.

"""
###############################################################################
Usage Profile Module
###############################################################################
"""

import gettext

from treelib import Tree

# Import other RTK modules.
from datamodels import RTKDataModel
from datamodels import RTKDataController
from dao import RTKMission
from dao import RTKMissionPhase
from dao import RTKEnvironment
from Mission import Model as Mission
from Phase import Model as Phase
from Environment import Model as Environment

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2017 Andrew "weibullguy" Rowland'

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
          |_Mission Phase 13
              |
              |_Environment 131
              |_Environment 132

    Attributes of the Usage Profile data model are:

    :ivar tree: the :py:class:`treelib.Tree` containing all the RTKMission,
                RTKPhase, and RTKEnvironment models that are part of the
                Usage Profile tree.  Node ID is the Mission ID, Phase ID, or
                Environment ID; data is the instance of the RTKMission,
                RTKPhase, or RTKEnvironment model.
    :ivar dao: the :py:class:`rtk.dao.DAO` object used to communicate with the
               RTK Program database.
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
        for _key in _missions:
            _mission = _missions[_key].data
            if _mission is not None:
                self.tree.create_node(tag=_mission.description,
                                      identifier=_mission.mission_id,
                                      parent=0, data=_mission)

                # Add the phases, if any, to the mission.
                _phases = self._dtm_phase.select_all(_mission.mission_id).nodes
                for _key in _phases:
                    _phase = _phases[_key].data
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
                        for _key in _environments:
                            _environment = _environments[_key].data
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

    def insert(self, entity_id, parent_id, type):
        """
        Method to add an entity to the Usage Profile and RTK Program database..

        :param int entity_id: the Revision ID, Mission ID, Mission Phase ID to
                              add the entity to.
        :param int parent_id: the ID of the parent node in the treelib Tree()>
        :param int type: the type of entity to add to the Usage Profile.  Types
                         are:

                         * 0 = Mission
                         * 1 = Mission Phase
                         * 2 = Environment

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        if type == 0:
            _entity = RTKMission()
            _entity.revision_id = entity_id
        elif type == 1:
            _entity = RTKMissionPhase()
            _entity.mission_id = entity_id
        elif type == 2:
            _entity = RTKEnvironment()
            _entity.phase_id = entity_id
        else:
            _entity = None

        _error_code, _msg = RTKDataModel.insert(self, [_entity, ])

        if type == 0:
            _tag = _entity.description
            _node_id = _entity.mission_id
        elif type == 1:
            _tag = _entity.name
            _node_id = int(str(parent_id) + str(_entity.phase_id))
        elif type == 2:
            _tag = _entity.name
            _node_id = int(str(parent_id) + str(_entity.environment_id))

        if _error_code == 0:
            self.tree.create_node(_tag, _node_id, parent=parent_id,
                                  data=_entity)
        else:
            _error_code = 2105
            _msg = 'RTK ERROR: Attempted to add an item to the Usage ' \
                   'Profile with an undefined indenture level.  Level {0:d} ' \
                   'was requested.  Must be one of 0 = Mission, 1 = Mission ' \
                   'Phase, and 2 = Environment.'.format(type)

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

        try:
            _entity = self.tree.get_node(node_id).data
            _error_code, _msg = RTKDataModel.update(self, _entity)
        except AttributeError:
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
        self._dtm_mission = Mission(dao)
        self._dtm_phase = Phase(dao)
        self._dtm_environment = Environment(dao)
        self._dtm_profile = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.tree = Tree()

        # Add the root to the Usage Profile Tree().  This is neccessary to
        # to allow multiple missions for each Usage Profile (Revision) as
        # there can only be one root node in a Tree().
        try:
            self.tree.create_node(tag='Usage Profiles', identifier=0,
                                  parent=None)
        except(tree.MultipleRootError, tree.NodeIDAbsentError,
               tree.DuplicatedNodeIdError):
            pass

    def request_select(self, node_id):
        """
        Method to select the Node data package associated with node_id.

        :param int node_id: the Node ID of the data package to retrieve.
        :return: the instance of the RTKMission, RTKMissionPhase, or
                 RTKEnvironment associated with node_id
        """

        return self.tree.get_node(node_id).data

    def request_select_all(self, revision_id):
        """
        Method to retrieve and build the Usage Profile tree for Revision ID.

        :param int revision_id: the Revision ID to retrieve the Usage Profile
                                and build trees for.
        :return: tree; the Usage Profile treelib Tree().
        :rtype: :py:class:`treelib.Tree`
        """

        return self._dtm_profile.select_all(revision_id)

    def request_insert(self, entity_id, parent_id, type):
        """
        Method to request a Mission, Mission Phase, or Environment be added to
        the Usage Profile.

        :param int entity_id: the Revision ID, Mission ID, Mission Phase ID to
                              add the entity to.
        :param int parent_id: the ID of the parent node in the treelib Tree()>
        :param int type: the type of entity to add to the Usage Profile.  Types
                         are:

                         * 0 = Mission
                         * 1 = Mission Phase
                         * 2 = Environment

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_profile.insert(entity_id,
                                                     parent_id,
                                                     type)

        # If the add was successful log the success message to the user log.
        # Otherwise, update the error message and write it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

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

        :param int level: the level in the tree to add the new entity.  Levels
                          are:

                          * 1 = Mission
                          * 2 = Mission Phase
                          * 3 = Environment

        :param int id: the Mission, Mission Phase, Environment ID to add the
                       entity.
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
