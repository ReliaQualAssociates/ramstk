# -*- coding: utf-8 -*-
#
#       rtk.usage.Environment.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
Environment Module
###############################################################################
"""

# Import other RTK modules.
from dao import RTKEnvironment                      # pylint: disable=E0401
from datamodels import RTKDataModel                 # pylint: disable=E0401
from datamodels import RTKDataController            # pylint: disable=E0401


class Model(RTKDataModel):
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

    _tag = 'Environments'

    def __init__(self, dao):
        """
        Method to initialize an Environment data model instance.

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

    def select(self, environment_id):
        """
        Method to retrieve the instance of the RTKEnvironment data model for
        the Environment ID passed.

        :param int environment_id: the ID Of the RTKEnvironment to retrieve.
        :return: the instance of the RTKEnvironment class that was requested
                 or None if the requested Environment ID does not exist.
        :rtype: :py:class:`rtk.dao.DAO.RTKEnvironment.Model`
        """

        return RTKDataModel.select(self, environment_id)

    def select_all(self, phase_id):
        """
        Method to retrieve all the Environments from the RTK Program database.

        :param int phase_id: the Mission Phase ID to select the Environments
                             for.
        :return: tree; the treelib Tree() of RTKEnvironment data models
                 that comprise the Environment tree.
        :rtype: :py:class:`treelib.Tree`
        """

        _session = RTKDataModel.select_all(self)

        for _environment in _session.query(RTKEnvironment).\
                filter(RTKEnvironment.phase_id == phase_id).all():
            try:
                self.tree.create_node(_environment.name,
                                      _environment.environment_id,
                                      parent=0, data=_environment)
            except AttributeError:
                pass

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

        _environment = RTKEnvironment()
        _environment.phase_id = phase_id

        _error_code, _msg = RTKDataModel.insert(self, [_environment, ])

        if _error_code == 0:
            self.tree.create_node(_environment.name,
                                  _environment.environment_id,
                                  parent=0, data=_environment)
            self._last_id = _environment.environment_id # pylint: disable=W0201

        return _error_code, _msg

    def delete(self, environment_id):
        """
        Method to remove the phase associated with Environment ID.

        :param int environment_id: the ID of the Environment to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _environment = self.tree.get_node(environment_id).data
            _error_code, _msg = RTKDataModel.delete(self, _environment)

            if _error_code == 0:
                self.tree.remove_node(environment_id)

        except AttributeError:
            _error_code = 1000
            _msg = 'RTK ERROR: Attempted to delete non-existent Environment ' \
                   'ID {0:d}.'.format(environment_id)

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

        _error_code, _msg = RTKDataModel.update(self, environment_id)

        if _error_code != 0:
            _error_code = 2136
            _msg = 'RTK ERROR: Attempted to save non-existent Environment ' \
                   'ID {0:d}.'.format(environment_id)

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
            try:
                _error_code, _msg = self.update(_node.data.environment_id)
            except AttributeError:
                pass

            # Break if something goes wrong and return.
            if _error_code != 0:
                print _error_code

        return _error_code, _msg


class Environment(RTKDataController):
    """
    The Environment controller provides an interface between the Environment
    data model and an RTK view model.  A single Environment controller can
    control one or more Environment data models.  Currently the Environment
    controller is unused.

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

        RTKDataController.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtm_environment = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
