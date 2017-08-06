#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.usage.Phase.py is part of The RTK Project
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
Mission Phase Module
###############################################################################
"""

from treelib import Tree, tree

# Import other RTK modules.
try:
    import Utilities as Utilities
    from dao.RTKMissionPhase import RTKMissionPhase
except ImportError:
    import rtk.Utilities as Utilities       # pylint: disable=E0401
    from rtk.dao.RTKMissionPhase import \
        RTKMissionPhase                     # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Phase data model contains the attributes and methods of a mission
    phase.  A Mission will consist of one or more mission phases.  The
    attributes of a Phase are:

    :ivar tree: the :py:class:`treelib.Tree` containing all the RTKMissionPhase
                models that are part of the Mission Phase tree.  Node ID is the
                Phase ID; data is the instance of the RTKMissionPhase model.
    :ivar int _last_id: the last Mission Phase ID used in the RTK Program
                        database.
    :ivar dao: the :py:class:`rtk.dao.DAO` object used to communicate with the
               RTK Program database.
    """

    def __init__(self, dao):
        """
        Method to initialize a Mission Phase data model instance.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._last_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = dao
        self.tree = Tree()

    def select(self, phase_id):
        """
        Method to retrieve the instance of the RTKMissionPhase data model for
        the Phase ID passed.

        :param int phase_id: the ID Of the RTKMissionPhase to retrieve.
        :return: the instance of the RTKMissionPhase class that was requested
                 or None if the requested Phase ID does not exist.
        :rtype: :py:class:`rtk.dao.DAO.RTKMissionPhase.Model`
        """

        try:
            _phase = self.tree.get_node(phase_id).data
        except AttributeError:
            _phase = None
        except tree.NodeIDAbsentError:
            _phase = None

        return _phase

    def select_all(self, mission_id):
        """
        Method to retrieve all the Phases from the RTK Program database.

        :param int mission_id: the Mission ID to selecte the Mission Phases
                               for.
        :return: tree; the treelib Tree() of RTKMissionPhase data models that
                 comprise the Mission Phase tree.
        :rtype: :py:class:`treelib.Tree`
        """

        _session = self.dao.RTK_SESSION(bind=self.dao.engine, autoflush=False,
                                        expire_on_commit=False)

        if self.tree.contains(0):
            self.tree.remove_node(0)

        self.tree.create_node('Mission Phases', 0)
        for _phase in _session.query(RTKMissionPhase).\
                filter(RTKMissionPhase.mission_id == mission_id).all():
            self.tree.create_node(_phase.name, _phase.phase_id,
                                  parent=0, data=_phase)

        _session.close()

        return self.tree

    def insert(self, mission_id):
        """
        Method to add a Mission Phase to the RTK Program database for Mission
        ID.

        :param int mission_id: the Mission ID to add the Mission Phase to.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _session = self.dao.RTK_SESSION(bind=self.dao.engine, autoflush=False,
                                        expire_on_commit=False)

        _phase = RTKMissionPhase()
        _phase.mission_id = mission_id
        _error_code, _msg = self.dao.db_add([_phase, ], _session)

        _session.close()

        if _error_code == 0:
            self.tree.create_node(_phase.name, _phase.phase_id,
                                  parent=0, data=_phase)
            self._last_id = _phase.phase_id

        return _error_code, _msg

    def delete(self, phase_id):
        """
        Method to remove the phase associated with Phase ID.

        :param int phase_id: the ID of the Mission Phase to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _session = self.dao.RTK_SESSION(bind=self.dao.engine, autoflush=False,
                                        expire_on_commit=False)

        try:
            _phase = self.tree.get_node(phase_id).data
            _error_code, _msg = self.dao.db_delete(_phase, _session)

            if _error_code == 0:
                self.tree.remove_node(phase_id)

        except AttributeError:
            _error_code = 1000
            _msg = 'RTK ERROR: Attempted to delete non-existent Mission ' \
                   'Phase ID {0:d}.'.format(phase_id)

        _session.close()

        return _error_code, _msg

    def update(self, phase_id):
        """
        Method to update the phase associated with Phase ID to the RTK
        Program database.

        :param int phase_id: the Phase ID to save to the RTK Program
                             database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _session = self.dao.RTK_SESSION(bind=self.dao.engine,
                                        autoflush=True,
                                        autocommit=False,
                                        expire_on_commit=False)

        try:
            _phase = self.tree.get_node(phase_id).data
        except AttributeError:
            _phase = None

        if _phase is not None:
            _session.add(self.tree.get_node(phase_id).data)
            _error_code, _msg = self.dao.db_update(_session)

        else:
            _error_code = 1000
            _msg = 'RTK ERROR: Attempted to save non-existent Mission Phase ' \
                   'ID {0:d}.'.format(phase_id)

        _session.close()

        return _error_code, _msg

    def update_all(self):
        """
        Method to save all Mission Phases to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            _phase_id = _node.identifier
            _error_code, _msg = self.update(_phase_id)

            # Break if something goes wrong and return.
            if _error_code != 0:
                print _error_code

        return _error_code, _msg


class MissionPhase(object):
    """
    The Phase controller provides an interface between the Phase data model
    and an RTK view model.  A single Phase controller can control one or more
    Phase data models.  Currently the Phase controller is unused.

    :ivar __test: control variable used to suppress certain code during
                  testing.
    :ivar _dtm_phase: the :py:class:`rtk.usage.Phase.Model` associated with
                      the Mission Phase Data Controller.
    :ivar _configuration: the :py:class:`rtk.Configuration.Configuration`
                          instance associated with the current RTK instance.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize a Mission Phase controller instance.

        :param dao: the RTK Program DAO instance to pass to the Mission Phase
                    Data Model.
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
        self._dtm_phase = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        pass
