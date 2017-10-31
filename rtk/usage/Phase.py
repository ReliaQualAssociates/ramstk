# -*- coding: utf-8 -*-
#
#       rtk.usage.Phase.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
Mission Phase Module
###############################################################################
"""

# Import other RTK modules.
from dao.RTKMissionPhase import RTKMissionPhase     # pylint: disable=E0401
from datamodels import RTKDataModel                 # pylint: disable=E0401
from datamodels import RTKDataController            # pylint: disable=E0401


class Model(RTKDataModel):
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

    _tag = 'Mission Phases'

    def __init__(self, dao):
        """
        Method to initialize a Mission Phase data model instance.
        """

        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def select(self, phase_id):
        """
        Method to retrieve the instance of the RTKMissionPhase data model for
        the Phase ID passed.

        :param int phase_id: the ID Of the RTKMissionPhase to retrieve.
        :return: the instance of the RTKMissionPhase class that was requested
                 or None if the requested Phase ID does not exist.
        :rtype: :py:class:`rtk.dao.DAO.RTKMissionPhase.Model`
        """

        return RTKDataModel.select(self, phase_id)

    def select_all(self, mission_id):
        """
        Method to retrieve all the Phases from the RTK Program database.

        :param int mission_id: the Mission ID to selecte the Mission Phases
                               for.
        :return: tree; the treelib Tree() of RTKMissionPhase data models that
                 comprise the Mission Phase tree.
        :rtype: :py:class:`treelib.Tree`
        """

        _session = RTKDataModel.select_all(self)

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

        _phase = RTKMissionPhase()
        _phase.mission_id = mission_id

        _error_code, _msg = RTKDataModel.insert(self, [_phase, ])

        if _error_code == 0:
            self.tree.create_node(_phase.name, _phase.phase_id,
                                  parent=0, data=_phase)
            self._last_id = _phase.phase_id         # pylint: disable=W0201

        return _error_code, _msg

    def delete(self, phase_id):
        """
        Method to remove the phase associated with Phase ID.

        :param int phase_id: the ID of the Mission Phase to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        try:
            _phase = self.tree.get_node(phase_id).data
            _error_code, _msg = RTKDataModel.delete(self, _phase)

            if _error_code == 0:
                self.tree.remove_node(phase_id)

        except AttributeError:
            _error_code = 2225
            _msg = 'RTK ERROR: Attempted to delete non-existent Mission ' \
                   'Phase ID {0:d}.'.format(phase_id)

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

        _error_code, _msg = RTKDataModel.update(self, phase_id)

        if _error_code != 0:
            _error_code = 2226
            _msg = 'RTK ERROR: Attempted to save non-existent Mission Phase ' \
                   'ID {0:d}.'.format(phase_id)

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
            try:
                _error_code, _msg = self.update(_node.data.phase_id)
            except AttributeError:
                pass

            # Break if something goes wrong and return.
            if _error_code != 0:
                print _error_code

        return _error_code, _msg


class MissionPhase(RTKDataController):
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

        RTKDataController.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtm_phase = Model(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
