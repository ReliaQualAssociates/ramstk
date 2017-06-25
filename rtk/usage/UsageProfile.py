#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.usage.UsageProfile.py is part of The RTK Project
#
# All rights reserved.

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
try:
    import Configuration as Configuration
except ImportError:
    import rtk.Configuration as Configuration
from Mission import Model as Mission
from Phase import Model as Phase
from Environment import Model as Environment

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

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

    :cvar int _MISSION: flow control variable equal to 0.
    :cvar int _PHASE: flow control variable equal to 1.
    :cvar int _ENVIRONMENT: flow control variable equal to 2.
    :cvar Tree treUsageProfile: the Tree() containing the hierarchical Usage
                                Profile.  Node ID is comprised of the Mission
                                ID, Phase ID, and Environement ID; data is the
                                instance of the Mission, Phase, or Environment
                                data model object associated with the Node().

    :ivar dao: the `:py:class:dao.DAO.DAO` that is connected to the RTK Program
               database.
    :ivar mission: the `:py:class:rtk.usage.Mission.Model` associated with this
                   Usage Profile.
    :ivar phase: the `:py:class:rtk.usage.Phase.Model` associated with this
                 Usage Profile.
    :ivar environment: the `:py:class:rtk.usage.Environment.Model` associated
                       with this Usage Profile.
    """

    # Define private class scalar attributes.
    _MISSION = 0
    _PHASE = 1
    _ENVIRONMENT = 2

    # Define public class scalar attributes.
    treUsageProfile = Tree()

    def __init__(self):
        """
        Method to initialize a Usage Profile data model instance.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = None
        self.last_id = None

        self.mission = Mission()
        self.phase = Phase()
        self.environment = Environment()

        # Add the root to the Usage Profile Tree().  This is neccessary to
        # to allow multiple missions for each Usage Profile (Revision) as
        # there can only be one root node in a Tree().
        try:
            self.treUsageProfile.create_node(tag='Usage Profiles',
                                             identifier=0, parent=None)
        except:
            pass

    def retrieve_profile(self, dao, revision_id):
        """
        Method to retrieve and build the Usage Profile tree for Revision ID.

        :param dao: the `:py:class:rtk.dao.DAO.DAO` object connected to the RTK
                    Program database.
        :param int revision_id: the Revision ID to retrieve the Usage Profile
                                and build trees for.
        :return: treUsageProfile; the Usage Profile Tree().
        :rtype: Tree()
        """

        self.dao = dao

        _root = self.treUsageProfile.root
        for _node in self.treUsageProfile.children(_root):
            self.treUsageProfile.remove_node(_node.identifier)

        # Build the tree.  We concatenate the Mission ID and the Phase ID to
        # create the Node() identifier for Mission Phases.  This prevents the
        # likely case when the first Mission and Phase have the same ID (1) in
        # the database from causing problems when building the tree.  Do the
        # same for the environment by concatenating the Environment ID with the
        # Mission ID and Phase ID.
        _dic_missions = self.mission.retrieve_all(self.dao, revision_id)
        for _mission in _dic_missions.values():
            _mnode = self.treUsageProfile.create_node(
                tag=_mission.description, identifier=_mission.mission_id,
                parent=0, data=_mission)

            if not isinstance(_mnode, Node):
                _msg = "ERROR: Failed to create a Node() for Mission ID " \
                       "{0:d}".format(_mission.mission_id)
                Configuration.RTK_DEBUG_LOG.error(_msg)
                break
            else:
                _dic_phases = self.phase.retrieve_all(self.dao,
                                                      _mission.mission_id)
                for _phase in _dic_phases.values():
                    _phase_id = int(str(_mission.mission_id) +
                                    str(_phase.phase_id))
                    _pnode = self.treUsageProfile.create_node(
                        tag=_phase.description, identifier=_phase_id,
                        parent=_mission.mission_id, data=_phase)

                    if not isinstance(_pnode, Node):
                        _msg = "RTK ERROR: Failed to create a Node() for " \
                               "Mission ID {0:d} and Phase ID {1:d}.".\
                            format(_mission.mission_id, _phase.phase_id)
                        Configuration.RTK_DEBUG_LOG.error(_msg)
                        break
                else:
                    _dic_environments = self.environment.retrieve_all(
                        self.dao, _phase.phase_id)
                    for _environment in _dic_environments.values():
                        _env_id = int(str(_mission.mission_id) +
                                      str(_phase.phase_id) +
                                      str(_environment.environment_id))
                        # The parent must be the concatenated phase ID used in
                        # the tree above, not the Phase ID attribute of the
                        # RTKPhase object.
                        _enode = self.treUsageProfile.create_node(
                            tag=_environment.name, identifier=_env_id,
                            parent=_phase_id, data=_environment)

                        if not isinstance(_enode, Node):
                            _msg = "RTK ERROR: Failed to create a Node() " \
                                   "for Mission ID {0:d}, Phase ID {1:d}, " \
                                   "and Environment ID {2:d}.".\
                                format(_mission.mission_id, _phase.phase_id,
                                       _environment.environment_id)
                            Configuration.RTK_DEBUG_LOG.error(_msg)
                            break

        return self.treUsageProfile

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
            _msg = "RTK ERROR: Attempted to add an item to the Usage " \
                   "Profile with an undefined indenture level.  Level " \
                   "{0:d} was requested.  Must be one of 0 = Mission, " \
                   "1 = Mission Phase, and 2 = Environment.".format(pos)

        if _error_code == 0:
            try:
                self.treUsageProfile.create_node(tag='', identifier=_nid,
                                                 parent=pid, data=_item)

            except:
                _error_code = 3002
                _msg = "RTK ERROR: Creating a new node in the Usage Profile " \
                       "Tree."

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
            self.treUsageProfile.remove_node(nid)

        except:
            _error_code = 3004
            _msg = _("RTK ERROR: Failed to delete Node {0:d} from the " \
                     "Usage Profile.").format(nid)

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

    def __init__(self):
        """
        Class for Usage Profile data controller.  Attributes of the Usage Profile
        data controller are:

        :ivar usage_model: the `:py:test:rtk.usage.Usage.Model` associated with the
                           data controller instance.
        """

    def __init__(self):
        """
        Method to initialize an instance of the Usage Profile data controller.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.usage_model = Model()

    def request_usage_profile(self, dao, revision_id):
        """
        Method to request the Usage Profile tree from the Usage Profile data
        model.

        :param dao: the `:py:class:rtk.dao.DAO.DAO` object connected to the RTK
                    Program database.
        :param int revision_id: the Revision ID to retrieve the Usage Profile
                                and build trees for.
        :return: the Usage Profile Tree().
        :rtype: Tree()
        """

        return self.usage_model.retrieve_profile(dao, revision_id)

    def request_add_mission(self, revision_id):
        """
        Method to request a Mission be added to Revision ID.

        :param int revision_id: the Revision ID this Mission will be
                                associated with.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        return self.usage_model.add_profile(0, 0, revision_id)

    def request_add_phase(self, pid, mission_id):
        """
        Method to request a Mission Phase be added to Mission ID.

        :param int pid: the parent identifer in treUsageProfile for the new
                        Mission Phase.
        :param int mission_id: the Mission ID this Phase will be associated
                               with.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        return self.usage_model.add_profile(1, pid, mission_id)

    def request_add_environment(self, pid, phase_id):
        """
        Method to request an Environment be added to Phase ID.

        :param int pid: the parent identifer in treUsageProfile for the new
                        Environment.
        :param int phase_id: the Phase ID this Environment will be associated
                             with.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        return self.usage_model.add_profile(2, pid, phase_id)

    def request_delete_mission(self, nid, mission_id):
        """
        Method to request Mission ID and it's children be deleted from the
        Usage Profile.

        :param int nid: the Node() identifer in treUsageProfile for the Mission
                        to be deleted.
        :param int mission_id: the Mission ID to delete.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        return self.usage_model.delete_profile(0, mission_id)

    def request_delete_phase(self, nid, phase_id):
        """
        Method to request Phase ID and it's children be deleted from the
        Usage Profile.

        :param int nid: the Node() identifer in treUsageProfile for the Phase
                        to be deleted.
        :param int phase_id: the Phase ID to delete.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        return self.usage_model.delete_profile(1, phase_id)

    def request_delete_environment(self, nid, environment_id):
        """
        Method to request Environment ID be deleted from the Usage Profile.

        :param int nid: the Node() identifer in treUsageProfile for the
                        Environment to be deleted.
        :param int environment_id: the Environment ID to delete.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        return self.usage_model.delete_profile(2, environment_id)

    def request_save_profile(self):
        """
        Method to request the Usage Profile be saved to the RTK Program
        database.

        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        return self.usage_model.save_profile()
