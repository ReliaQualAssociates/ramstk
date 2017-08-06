#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.usage.Environment.py is part of The RTK Project
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
Environment Module
###############################################################################
"""

from treelib import Tree, tree

# Import other RTK modules.
try:
    import Utilities as Utilities
    from dao.DAO import RTKEnvironment
except ImportError:
    import rtk.Utilities as Utilities           # pylint: disable=E0401
    from rtk.dao.DAO import RTKEnvironment      # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Environment data model contains the attributes and methods of a mission
    phase environment.  A Phase will consist of zero or more environments.  The
    attributes of an Environment are:

    :ivar tree: the :py:class:`treelib.Tree` containing all the RTKEnvironment
                models that are part of the Environment tree.  Node ID is the
                Mission ID; data is the instance of the RTKMission model.
    :ivar int _last_id: the last Environment ID used in the RTK Program
                        database.
    :ivar dao: the :py:class:`rtk.dao.DAO` object used to communicate with the
               RTK Program database.
    """

    def __init__(self, dao):
        """
        Method to initialize an Environment data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :py:class:`rtk.dao.DAO.DAO`
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

    def select(self, environment_id):
        """
        Method to retrieve the instance of the RTKEnvironment data model for
        the Environment ID passed.

        :param int environment_id: the ID Of the RTKEnvironment to retrieve.
        :return: the instance of the RTKEnvironment class that was requested
                 or None if the requested Environment ID does not exist.
        :rtype: :py:class:`rtk.dao.DAO.RTKEnvironment.Model`
        """

        try:
            _environment = self.tree.get_node(environment_id).data
        except AttributeError:
            _environment = None
        except tree.NodeIDAbsentError:
            _environment = None

        return _environment

    def select_all(self, phase_id):
        """
        Method to retrieve all the Environments from the RTK Program database.

        :param int phase_id: the Mission Phase ID to select the Environments
                             for.
        :return: tree; the treelib Tree() of RTKEnvironment data models
                 that comprise the Environment tree.
        :rtype: :py:class:`treelib.Tree`
        """

        _session = self.dao.RTK_SESSION(bind=self.dao.engine, autoflush=False,
                                        expire_on_commit=False)

        if self.tree.contains(0):
            self.tree.remove_node(0)

        self.tree.create_node('Environments', 0)
        for _environment in _session.query(RTKEnvironment).\
                filter(RTKEnvironment.phase_id == phase_id).all():
            self.tree.create_node(_environment.name,
                                  _environment.environment_id,
                                  parent=0, data=_environment)

        _session.close()

        return self.tree

    def insert(self, phase_id):
        """
        Method to add an Evnironmental condition to the RTK Program database
        for Environment ID.

        :param int phase_id: the Mission Phase ID to add the Environment to.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _session = self.dao.RTK_SESSION(bind=self.dao.engine, autoflush=False,
                                        expire_on_commit=False)

        _environment = RTKEnvironment()
        _environment.phase_id = phase_id
        _error_code, _msg = self.dao.db_add([_environment, ], _session)

        _session.close()

        if _error_code == 0:
            self.tree.create_node(_environment.name,
                                  _environment.environment_id,
                                  parent=0, data=_environment)
            self._last_id = _environment.environment_id

        return _error_code, _msg

    def delete(self, environment_id):
        """
        Method to remove the phase associated with Environment ID.

        :param int environment_id: the ID of the Environment to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _session = self.dao.RTK_SESSION(bind=self.dao.engine, autoflush=False,
                                        expire_on_commit=False)

        try:
            _environment = self.tree.get_node(environment_id).data
            (_error_code, _msg) = self.dao.db_delete(_environment, _session)

            if _error_code == 0:
                self.tree.remove_node(environment_id)

        except AttributeError:
            _error_code = 1000
            _msg = 'RTK ERROR: Attempted to delete non-existent Environment ' \
                   'ID {0:d}.'.format(environment_id)

        _session.close()

        return _error_code, _msg

    def update(self, environment_id):
        """
        Method to update the environment associated with Phase ID to the RTK
        Program database.

        :param int environment_id: the Environment ID to save to the RTK
                                   Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _session = self.dao.RTK_SESSION(bind=self.dao.engine,
                                        autoflush=True,
                                        autocommit=False,
                                        expire_on_commit=False)

        try:
            _environment = self.tree.get_node(environment_id).data
        except AttributeError:
            _environment = None

        if _environment is not None:
            _session.add(self.tree.get_node(environment_id).data)
            (_error_code, _msg) = self.dao.db_update(_session)

        else:
            _error_code = 1000
            _msg = 'RTK ERROR: Attempted to save non-existent Environment ' \
                   'ID {0:d}.'.format(environment_id)

        _session.close()

        return _error_code, _msg

    def update_all(self):
        """
        Method to save all Environments to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            _environment_id = _node.identifier
            _error_code, _msg = self.update(_environment_id)

            # Break if something goes wrong and return.
            if _error_code != 0:
                print _error_code

        return _error_code, _msg


class Environment(object):
    """
    The Environment controller provides an interface between the Environment
    data model and an RTK view model.  A single Environment controller can
    control one or more Environment data models.  Currently the Environment
    controller is unused.

    :ivar __test: control variable used to suppress certain code during
                  testing.
    :ivar _dtm_environment: the :py:class:`rtk.usage.Environment.Model`
                            associated with the Environment Data Controller.
    :ivar _configuration: the :py:class:`rtk.Configuration.Configuration`
                          instance associated with the current RTK instance.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize a Environment controller instance.

        :param dao: the RTK Program DAO instance to pass to the Environment
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
        self._dtm_environment = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        pass
