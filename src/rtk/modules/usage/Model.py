# -*- coding: utf-8 -*-
#
#       rtk.usage.Model.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Usage Profile Package Data Models."""

# Import other RTK modules.
from rtk.modules import RTKDataModel
from rtk.dao import RTKEnvironment, RTKMission, RTKMissionPhase


class UsageProfileDataModel(RTKDataModel):
    """
    Contain the attributes and methods of a Usage Profile.

    Class for Usage Profile data model.  This model builds a Usage Profile from
    the Mission, Phase, and Environment data models.  This is a hierarchical
    relationship, such as:

        * Mission 1
            - Mission Phase 11
                + Environment 111
                + Environment 112
                + Environment 113
            - Mission Phase 12
                + Environment 121
                + Environment 122
        * Mission 2
            - Mission Phase 21
                + Environment 211
                + Environment 212
    """

    _tag = 'Usage Profiles'

    def __init__(self, dao):
        """
        Initialize a Usage Profile data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dtm_mission = MissionDataModel(dao)
        self.dtm_phase = MissionPhaseDataModel(dao)
        self.dtm_environment = EnvironmentDataModel(dao)

    def do_select_all(self, **kwargs):
        """
        Retrieve and build the Usage Profile tree for Revision ID.

        :param int revision_id: the Revision ID to retrieve the Usage Profile
                                and build trees for.
        :return: tree; the Usage Profile treelib Tree().
        :rtype: :py:class:`treelib.Tree`
        """
        _revision_id = kwargs['revision_id']
        RTKDataModel.do_select_all(self, **kwargs)

        # Build the tree.  We concatenate the Mission ID and the Phase ID to
        # create the Node() identifier for Mission Phases.  This prevents the
        # likely case when the first Mission and Phase have the same ID (1) in
        # the database from causing problems when building the tree.  Do the
        # same for the environment by concatenating the Environment ID with the
        # Mission ID and Phase ID.
        _missions = self.dtm_mission.do_select_all(
            revision_id=_revision_id).nodes

        # pylint: disable=too-many-nested-blocks
        for _mkey in _missions:
            _mission = _missions[_mkey].data
            if _mission is not None:
                self.tree.create_node(
                    tag=_mission.description,
                    identifier=_mission.mission_id,
                    parent=0,
                    data=_mission)

                # Add the phases, if any, to the mission.
                _phases = self.dtm_phase.do_select_all(
                    mission_id=_mission.mission_id).nodes
                for _pkey in _phases:
                    _phase = _phases[_pkey].data
                    if _phase is not None:
                        _phase_id = int(
                            str(_mission.mission_id) + str(_phase.phase_id))
                        self.tree.create_node(
                            tag=_phase.description,
                            identifier=_phase_id,
                            parent=_mission.mission_id,
                            data=_phase)

                        # Add the environments, if any, to the phase.
                        _environments = self.dtm_environment.do_select_all(
                            phase_id=_phase.phase_id).nodes
                        for _ekey in _environments:
                            _environment = _environments[_ekey].data
                            if _environment is not None:
                                _env_id = int(
                                    str(_mission.mission_id) +
                                    str(_phase.phase_id) +
                                    str(_environment.environment_id))
                                # The parent must be the concatenated phase ID
                                # used in the tree above, not the Phase ID
                                # attribute of the RTKPhase object.
                                self.tree.create_node(
                                    tag=_environment.name,
                                    identifier=_env_id,
                                    parent=_phase_id,
                                    data=_environment)

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add an entity to the Usage Profile and RTK Program database..

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

        _entity_id = kwargs['entity_id']
        _parent_id = kwargs['parent_id']
        _level = kwargs['level']

        if _level == 'mission':
            _entity = RTKMission()
            _entity.revision_id = _entity_id
        elif _level == 'phase':
            _entity = RTKMissionPhase()
            _entity.mission_id = _entity_id
        elif _level == 'environment':
            _entity = RTKEnvironment()
            _entity.phase_id = _entity_id
        else:
            _entity = None

        _error_code, _msg = RTKDataModel.do_insert(
            self, entities=[
                _entity,
            ])

        if _level == 'mission':
            _tag = _entity.description
            _node_id = _entity.mission_id
        elif _level == 'phase':
            _tag = _entity.name
            _node_id = int(str(_parent_id) + str(_entity.phase_id))
        elif _level == 'environment':
            _tag = _entity.name
            _node_id = int(str(_parent_id) + str(_entity.environment_id))

        if _error_code == 0:
            self.tree.create_node(
                _tag, _node_id, parent=_parent_id, data=_entity)
        else:
            _error_code = 2105
            _msg = 'RTK ERROR: Attempted to add an item to the Usage ' \
                   'Profile with an undefined indenture level.  Level {0:s} ' \
                   'was requested.  Must be one of mission, phase, or ' \
                   'environment.'.format(_level)

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove an entity from the Usage Profile and RTK Program database.

        :param int node_id: the Node ID of the entity to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'Usage Profile entity with Node ID ' \
                          '{0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the entity associated with Node ID to the RTK Program database.

        :param int node_id: the Node ID of the entity to save to the RTK
                            Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Usage Profile ' \
                   'entity with Node ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all Usage Profile entities to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.do_update(_node.identifier)
                _msg = _msg + _debug_msg + '\n'

            except AttributeError:
                _error_code = 1
                _msg = ("RTK ERROR: One or more line items in the usage "
                        "profile did not update.")

        if _error_code == 0:
            _msg = ("RTK SUCCESS: Updating all line items in the usage "
                    "profile.")

        return _error_code, _msg


class MissionDataModel(RTKDataModel):
    """
    Contain the attributes and methods of a Mission.

    The Mission data model contains the attributes and methods of a mission.
    A Usage Profile will consist of one or more missions.  The attributes of a
    Mission are:
    """

    _tag = 'Missions'

    def __init__(self, dao):
        """
        Initialize a Mission data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the RTKMission records from the RTK Program database.

        This method retrieves all the records from the RTKMIssion table in the
        connected RTK Program database.  It then add each to the Mission data
        model treelib.Tree().

        :param int revision_id: the ID of the Revision to retrieve the Mission.
        :return: tree; the treelib Tree() of RTKMission data models that
                 comprise the Mission tree.
        :rtype: :class:`treelib.Tree`
        """
        _revision_id = kwargs['revision_id']
        _session = RTKDataModel.do_select_all(self, **kwargs)

        for _mission in _session.query(RTKMission).\
                filter(RTKMission.revision_id == _revision_id).all():
            self.tree.create_node(
                _mission.description,
                _mission.mission_id,
                parent=0,
                data=_mission)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _mission.mission_id)

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RTKMission table in the RTK Program database.

        :param int revision_id: the Revision ID to add the Mission to.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _revision_id = kwargs['revision_id']
        _mission = RTKMission()
        _mission.revision_id = _revision_id
        _error_code, _msg = RTKDataModel.do_insert(
            self, entities=[
                _mission,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _mission.description,
                _mission.mission_id,
                parent=0,
                data=_mission)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = _mission.mission_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove the RTKMission record associated with Node ID.

        :param int node_id: the ID of the Mission to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'Mission ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the RTKMission record associated with Node ID.

        :param int node_id: the Mission ID of the Mission to save to the RTK
                               Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Mission ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all RTKMission records.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.do_update(_node.identifier)

                _msg = _msg + _debug_msg + '\n'

            except AttributeError:
                _error_code = 1
                _msg = ("RTK ERROR: One or more records in the usage profile "
                        "mission table did not update.")

        if _error_code == 0:
            _msg = ("RTK SUCCESS: Updating all records in the usage profile "
                    "mission table.")

        return _error_code, _msg


class MissionPhaseDataModel(RTKDataModel):
    """
    Contain the attributes and methods of a Mission.

    The Phase data model contains the attributes and methods of a mission
    phase.  A Mission will consist of one or more mission phases.  The
    attributes of a Phase are:
    """

    _tag = 'Mission Phases'

    def __init__(self, dao):
        """
        Initialize a Mission Phase data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the RTKMissionPhase records from the RTK Program database.

        :param int mission_id: the Mission ID to selecte the Mission Phases
                               for.
        :return: tree; the treelib Tree() of RTKMissionPhase data models that
                 comprise the Mission Phase tree.
        :rtype: :class:`treelib.Tree`
        """
        _mission_id = kwargs['mission_id']
        _session = RTKDataModel.do_select_all(self, **kwargs)

        for _phase in _session.query(RTKMissionPhase).\
                filter(RTKMissionPhase.mission_id == _mission_id).all():
            self.tree.create_node(
                _phase.name, _phase.phase_id, parent=0, data=_phase)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _phase.phase_id)

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RTKMissionPhase table in the RTK Program database.

        :param int mission_id: the Mission ID to add the Mission Phase to.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _mission_id = kwargs['mission_id']
        _phase = RTKMissionPhase()
        _phase.mission_id = _mission_id

        _error_code, _msg = RTKDataModel.do_insert(
            self, entities=[
                _phase,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _phase.name, _phase.phase_id, parent=0, data=_phase)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = _phase.phase_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove the RTKMissionPhase record associated with Node ID.

        :param int node_id: the ID of the Mission Phase to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'Mission Phase ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the RTKMissionPhase record associated with Node ID.

        :param int node_id: the Phase ID to save to the RTK Program
                             database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Mission Phase ' \
                   'ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all RTKMissionPhase records.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.do_update(_node.identifier)

                _msg = _msg + _debug_msg + '\n'

            except AttributeError:
                _error_code = 1
                _msg = ("RTK ERROR: One or more records in the usage profile "
                        "mission phase table did not update.")

        if _error_code == 0:
            _msg = ("RTK SUCCESS: Updating all records in the usage profile "
                    "mission phase table.")

        return _error_code, _msg


class EnvironmentDataModel(RTKDataModel):
    """
    Contain the attributes and methods of an Environment.

    The Environment data model contains the attributes and methods of a mission
    phase environment.  A Phase will consist of zero or more environments.  The
    attributes of an Environment are:
    """

    _tag = 'Environments'

    def __init__(self, dao):
        """
        Initialize an Environment data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the RTKEnvironment records from the RTK Program database.

        :param int phase_id: the Mission Phase ID to select the Environments
                             for.
        :return: tree; the treelib Tree() of RTKEnvironment data models
                 that comprise the Environment tree.
        :rtype: :py:class:`treelib.Tree`
        """
        _phase_id = kwargs['phase_id']
        _session = RTKDataModel.do_select_all(self)

        for _environment in _session.query(RTKEnvironment).\
                filter(RTKEnvironment.phase_id == _phase_id).all():
            self.tree.create_node(
                _environment.name,
                _environment.environment_id,
                parent=0,
                data=_environment)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _environment.environment_id)

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RTKEnvironment table in the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _phase_id = kwargs['phase_id']
        _environment = RTKEnvironment()
        _environment.phase_id = _phase_id

        _error_code, _msg = RTKDataModel.do_insert(
            self, entities=[
                _environment,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _environment.name,
                _environment.environment_id,
                parent=0,
                data=_environment)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = _environment.environment_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove the RTKEnvironment record associated with Node ID.

        :param int node_id: the ID of the Environment to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'Environment ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the RTKEnvironment record associated with Node ID.

        :param str node_id: the PyPubSub Tree() node ID of the Environment to
                            save to the RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Environment ' \
                   'ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all RTKEnvironment records to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.do_update(_node.identifier)

                _msg = _msg + _debug_msg + '\n'

            except AttributeError:
                _error_code = 1
                _msg = ("RTK ERROR: One or more records in the usage profile "
                        "environment table did not update.")

        if _error_code == 0:
            _msg = ("RTK SUCCESS: Updating all records in the usage profile "
                    "environment table.")

        return _error_code, _msg
