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
####################
Usage Profile Module
####################
"""

import gettext
import locale

from treelib import Node, Tree

# Import other RTK modules.
from Mission import Model as Mission
from Phase import Model as Phase
from Environment import Model as Environment

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2017 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class Model(object):
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

    # Define private class scalar attributes.
    _MISSION = 0
    _PHASE = 1
    _ENVIRONMENT = 2

    # Define public class scalar attributes.
    treUsageProfile = Tree()

    def __init__(self, dao):
        """
        Method to initialize a Usage Profile data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :py:class:`rtk.dao.DAO.DAO`
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = dao

    def add_profile(self, pos, pid, cid):
        """
        Method to add a Mission, Mission Phase, or Environment into the Usage
        Profile.

        :param int pos: the position in the treUsageProfile to add the new
                        item; 0 = Mission, 1 = Mission Phase, 2 = Environment.
        :param int pid: the treUsageProfile identifier that will be the parent
                        of the newly added item.
        :param int cid: the Revision ID, Mission ID, or Phase ID the newly
                        added item is associated with in the RTK Program
                        database.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        _nid = None
        _item = None

        _error_code = 0
        _msg = "RTK SUCCESS: Adding a new item to the Usage Profile."

        if pos == self._MISSION:
            _item = self.mission.add_mission(cid)
            _nid = _item.mission_id

        elif pos == self._PHASE:
            _item = self.phase.add_phase(cid)
            _nid = int(str(pid) + str(_item.phase_id))

        elif pos == self._ENVIRONMENT:
            _item = self.environment.add_environment(cid)
            _nid = int(str(pid) + str(_item.environment_id))

        else:
            _error_code = 3001
            _msg = "RTK ERROR: Adding an item to the Usage Profile."

        return _error_code, _msg

    def delete_profile(self, pos, nid):
        """
        Method to remove an item (Mission, Mission Phase, Environment) and all
        it's children from a Usage Profile.

        :param int pos: the position in the treUsageProfile to add the new
                        item; 0 = Mission, 1 = Mission Phase, 2 = Environment.
        :param int nid: the Node() identifier and item ID (mission_id,
                        phase_id, environment_id) to delete.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Deleting an item from the Usage Profile."

        if pos == self._MISSION:
            self.mission.delete_mission(nid)
        elif pos == self._PHASE:
            self.phase.delete_phase(nid)
        elif pos == self._ENVIRONMENT:
            self.environment.delete_environment(nid)
        else:
            _error_code = 3003
            _msg = "RTK ERROR: Attempted to delete an item from the Usage " \
                   "Profile with an undefined indenture level.  Level " \
                   "{0:d} was requested.  Must be one of 0 = Mission, " \
                   "1 = Mission Phase, and 2 = Environment.".format(pos)

        try:
            self.tree.remove_node(nid)
        # TODO: Create exception class to capture here.
        except:
            _error_code = 3004
            _msg = "RTK ERROR: Failed to delete Node {0:d} from the " \
                   "Usage Profile.".format(nid)

        return _error_code, _msg

    def save_profile(self):
        """
        Method to save changes to the Usage Profile to the RTK Program
        database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code, _msg = self.dao.db_update()

        return _error_code, _msg


class UsageProfile(object):
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

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self.__test = kwargs['test']
        self._configuration = configuration
        self._dtm_mission = Mission(dao)
        self._dtm_phase = Phase(dao)
        self._dtm_environment = Environment(dao)

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
        # TODO: Create exception class to capture here.
        except:
            pass

    def request_select_all(self, revision_id):
        """
        Method to retrieve and build the Usage Profile tree for Revision ID.

        :param int revision_id: the Revision ID to retrieve the Usage Profile
                                and build trees for.
        :return: tree; the Usage Profile treelib Tree().
        :rtype: :py:class:`treelib.Tree`
        """

        _root = self.tree.root
        for _node in self.tree.children(_root):
            self.tree.remove_node(_node.identifier)

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

    def request_insert(self, level, id):
        """
        Method to request a Mission, Mission Phase, or Environment be added to
        the Usage Profile.

        :param int level: the level in the tree to add the new entity.  Levels
                          are:

                          * 1 = Mission
                          * 2 = Mission Phase
                          * 3 = Environment

        :param int id: the Revision, Mission, or Phase ID to add the entity.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if level == 1:
            (_error_code, _msg) = self._dtm_mission.insert(id)
        elif level == 2:
            (_error_code, _msg) = self._dtm_phase.insert(id)
        elif level == 3:
            (_error_code, _msg) = self._dtm_environment(id)

        # If the add was successful log the success message to the user log.
        # Otherwise, update the error message and write it to the debug log.
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_delete(self, level, id):
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

        if level == 1:
            (_error_code, _msg) = self._dtm_mission.delete(id)
        elif level == 2:
            (_error_code, _msg) = self._dtm_phase.delete(id)
        elif level == 3:
            (_error_code, _msg) = self._dtm_environment.delete(id)

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

        _error_code, _msg = self._dtm_mission.update_all()
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        _error_code, _msg = self._dtm_phase.update_all()
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        _error_code, _msg = self._dtm_environment.update_all()
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)
        else:
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

