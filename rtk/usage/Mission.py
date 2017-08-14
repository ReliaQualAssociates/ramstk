#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.usage.Mission.py is part of The RTK Project
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

"""
###############################################################################
Mission Module
###############################################################################
"""

from treelib import Tree, tree

# Import other RTK modules.
try:
    import Utilities as Utilities
    from dao.DAO import RTKMission
    from datamodels import RTKDataModel
    from datamodels import RTKDataController
except ImportError:
    import rtk.Utilities as Utilities               # pylint: disable=E0401
    from rtk.dao.DAO import RTKMission              # pylint: disable=E0401
    from rtk.datamodels import RTKDataModel         # pylint: disable=E0401
    from rtk.datamodels import RTKDataController    # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'


class Model(RTKDataModel):
    """
    The Mission data model contains the attributes and methods of a mission.
    A Usage Profile will consist of one or more missions.  The attributes of a
    Mission are:

    :ivar tree: the :py:class:`treelib.Tree` containing all the RTKMission
                models that are part of the Mission tree.  Node ID is the
                Mission ID; data is the instance of the RTKMission model.
    :ivar int _last_id: the last Mission ID used in the RTK Program database.
    :ivar dao: the :py:class:`rtk.dao.DAO` object used to communicate with the
               RTK Program database.
    """

    _tag = 'Missions'

    def __init__(self, dao):
        """
        Method to initialize a Mission data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :py:class:`rtk.dao.DAO.DAO`
        """

        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select(self, mission_id):
        """
        Method to retrieve the instance of the RTKMission data model for the
        Mission ID passed.

        :param int mission_id: the ID Of the Mission to retrieve.
        :return: the instance of the RTKMission class that was requested or
                 None if the requested Mission ID does not exist.
        :rtype: :py:class:`rtk.dao.RTKRevision.RTKRevision`
        """

        return RTKDataModel.select(self, mission_id)

    def select_all(self, revision_id):
        """
        Method to retrieve all the RTKMissions from the RTK Program database.

        :param int revision_id: the ID of the Revision to retrieve the Mission.
        :return: tree; the treelib Tree() of RTKMission data models that
                 comprise the Mission tree.
        :rtype: :py:class:`treelib.Tree`
        """

        _session = RTKDataModel.select_all(self)

        for _mission in _session.query(RTKMission).\
                filter(RTKMission.revision_id == revision_id).all():
            self.tree.create_node(_mission.description, _mission.mission_id,
                                  parent=0, data=_mission)

        _session.close()

        return self.tree

    def insert(self, revision_id):
        """
        Method to add a Mission to the RTK Program database for Revision ID.

        :param int revision_id: the Revision ID to add the Mission to.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _mission = RTKMission()
        _mission.revision_id = revision_id

        _error_code, _msg = RTKDataModel.insert(self, [_mission, ])

        if _error_code == 0:
            self.tree.create_node(_mission.description, _mission.mission_id,
                                  parent=0, data=_mission)
            self._last_id = _mission.mission_id

        return _error_code, _msg

    def delete(self, mission_id):
        """
        Method to remove the mission associated with Mission ID.

        :param int mission_id: the ID of the Mission to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _mission = self.tree.get_node(mission_id).data
            _error_code, _msg = RTKDataModel.delete(self, _mission)

            if _error_code == 0:
                self.tree.remove_node(mission_id)

        except AttributeError:
            _error_code = 2115
            _msg = 'RTK ERROR: Attempted to delete non-existent Mission ' \
                   'ID {0:d}.'.format(mission_id)

        return _error_code, _msg

    def update(self, mission_id):
        """
        Method to update the mission associated with Mission ID to the RTK
        Program database.

        :param int mission_id: the Mission ID of the Mission to save to the RTK
                               Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _mission = self.tree.get_node(mission_id).data
            _error_code, _msg = RTKDataModel.update(self, _mission)
        except AttributeError:
            _error_code = 2116
            _msg = 'RTK ERROR: Attempted to save non-existent Mission ID ' \
                   '{0:d}.'.format(mission_id)

        return _error_code, _msg

    def update_all(self):
        """
        Method to save all Missions to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.mission_id)
            except AttributeError:
                pass

            # Break if something goes wrong and return.
            if _error_code != 0:
                print _error_code

        return _error_code, _msg


class Mission(RTKDataController):
    """
    The Mission controller provides an interface between the Mission data model
    and an RTK view model.  A single Mission controller can control one or more
    Mission data models.  Currently the Mission controller is unused.

    :ivar _dtm_mission: the :py:class:`rtk.usage.Mission.Model` associated with
                         the Mission Data Controller.
    :ivar _configuration: the :py:class:`rtk.Configuration.Configuration`
                          instance associated with the current RTK instance.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize a Mission controller instance.

        :param dao: the RTK Program DAO instance to pass to the Mission Data
                    Model.
        :type dao: :py:class:`rtk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """

        RTKDataController.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtm_mission = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        pass
