# -*- coding: utf-8 -*-
#
#       ramstk.usage.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Usage Profile Package Data Models."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.dao import RAMSTKEnvironment, RAMSTKMission, RAMSTKMissionPhase
from ramstk.modules import RAMSTKDataModel


class UsageProfileDataModel(RAMSTKDataModel):
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
    _root = 0

    def __init__(self, dao, **kwargs):
        """
        Initialize a Usage Profile data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._test = kwargs['test']

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dtm_mission = MissionDataModel(dao)
        self.dtm_phase = MissionPhaseDataModel(dao)
        self.dtm_environment = EnvironmentDataModel(dao)

    def do_delete(self, node_id):
        """
        Remove an entity from the Usage Profile and RAMSTK Program database.

        :param int node_id: the Node ID of the entity to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = (
                "RAMSTK ERROR: Attempted to delete non-existent Mission, "
                "Mission Phase, or Environment ID "
                "{0:s}."
            ).format(str(node_id))
        else:
            self.last_id = max(self.tree.nodes.keys())

            # If we're not running a test, let anyone who cares know a Mission,
            # Mission Phase, or Environment was deleted.
            if not self._test:
                pub.sendMessage('deleted_usage_profile', tree=self.tree)

        return _error_code, _msg

    def do_insert(self, **kwargs):
        """
        Add an entity to the Usage Profile and RAMSTK Program database..

        :param int entity_id: the RAMSTK Program database Revision ID, Mission
                              ID, Mission Phase ID to add the entity to.
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
            _entity = RAMSTKMission()
            _entity.revision_id = _entity_id
        elif _level == 'phase':
            _entity = RAMSTKMissionPhase()
            _entity.mission_id = _entity_id
        elif _level == 'environment':
            _entity = RAMSTKEnvironment()
            _entity.phase_id = _entity_id
        else:
            _entity = None

        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _entity,
            ],
        )

        if _error_code == 0:
            if _level == 'mission':
                _tag = _entity.description
                _node_id = _entity.mission_id
            elif _level == 'phase':
                _tag = _entity.name
                _node_id = int(str(_parent_id) + str(_entity.phase_id))
            elif _level == 'environment':
                _tag = _entity.name
                _node_id = int(str(_parent_id) + str(_entity.environment_id))

            self.tree.create_node(
                _tag, _node_id, parent=_parent_id, data=_entity,
            )

            # If we're not running a test, let anyone who cares know a Function
            # was deleted.
            if not self._test:
                pub.sendMessage('inserted_usage_profile', tree=self.tree)
        else:
            _error_code = 2005
            _msg = (
                "RAMSTK ERROR: Attempted to add an item to the Usage "
                "Profile with an undefined indenture level.  Level "
                "{0:s} was requested.  Must be one of mission, "
                "phase, or environment."
            ).format(_level)

        return _error_code, _msg

    def do_select_all(self, **kwargs):
        """
        Retrieve and build the Usage Profile tree for Revision ID.

        :param int revision_id: the Revision ID to retrieve the Usage Profile
                                and build trees for.
        :return: None
        :rtype: None
        """
        _revision_id = kwargs['revision_id']
        RAMSTKDataModel.do_select_all(self, **kwargs)

        # Build the tree.  We concatenate the Mission ID and the Phase ID to
        # create the Node() identifier for Mission Phases.  This prevents the
        # likely case when the first Mission and Phase have the same ID (1) in
        # the database from causing problems when building the tree.  Do the
        # same for the environment by concatenating the Environment ID with the
        # Mission ID and Phase ID.
        _missions = self.dtm_mission.do_select_all(
            revision_id=_revision_id,
        ).nodes

        # pylint: disable=too-many-nested-blocks
        for _mkey in _missions:
            _mission = _missions[_mkey].data
            if _mission is not None:
                self.tree.create_node(
                    tag=_mission.description,
                    identifier=_mission.mission_id,
                    parent=self._root,
                    data=_mission,
                )

                # Add the phases, if any, to the mission.
                _phases = self.dtm_phase.do_select_all(
                    mission_id=_mission.mission_id,
                ).nodes
                for _pkey in _phases:
                    _phase = _phases[_pkey].data
                    if _phase is not None:
                        _phase_id = int(
                            str(_mission.mission_id) + str(_phase.phase_id),
                        )
                        self.tree.create_node(
                            tag=_phase.description,
                            identifier=_phase_id,
                            parent=_mission.mission_id,
                            data=_phase,
                        )

                        # Add the environments, if any, to the phase.
                        _environments = self.dtm_environment.do_select_all(
                            phase_id=_phase.phase_id,
                        ).nodes
                        for _ekey in _environments:
                            _environment = _environments[_ekey].data
                            if _environment is not None:
                                _env_id = int(
                                    str(_mission.mission_id) +
                                    str(_phase.phase_id) +
                                    str(_environment.environment_id),
                                )
                                # The parent must be the concatenated phase ID
                                # used in the tree above, not the Phase ID
                                # attribute of the RAMSTKPhase object.
                                self.tree.create_node(
                                    tag=_environment.name,
                                    identifier=_env_id,
                                    parent=_phase_id,
                                    data=_environment,
                                )

        # If we're not running a test and there were requirements returned,
        # let anyone who cares know the Requirements have been selected.
        if not self._test and self.tree.size() > 1:
            pub.sendMessage('retrieved_usage_profile', tree=self.tree)

    def do_update(self, node_id):
        """
        Update the entity associated with Node ID to the RAMSTK Program database.

        :param int node_id: the Node ID of the entity to save to the RAMSTK
                            Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code == 0:
            if not self._test:
                _attributes = self.do_select(node_id).get_attributes()
                pub.sendMessage(
                    'updated_usage_profile', attributes=_attributes,
                )
        else:
            _error_code = 2005
            _msg = (
                "RAMSTK ERROR: Attempted to save non-existent Usage "
                "Profile entity with Node ID {0:d}."
            ).format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all Usage Profile entities to the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all line items in the usage "
                "profile."
            )

        return _error_code, _msg


class MissionDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a Mission.

    The Mission data model contains the attributes and methods of a mission.
    A Usage Profile will consist of one or more missions.  The attributes of a
    Mission are:
    """

    _tag = 'Missions'
    _root = 0

    def __init__(self, dao):
        """
        Initialize a Mission data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the RAMSTKMission records from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKMIssion table in
        the connected RAMSTK Program database.  It then add each to the Mission
        data model treelib.Tree().

        :param int revision_id: the ID of the Revision to retrieve the Mission.
        :return: tree; the treelib Tree() of RAMSTKMission data models that
        comprise the Mission tree.
        :rtype: :class:`treelib.Tree`
        """
        _revision_id = kwargs['revision_id']
        _session = RAMSTKDataModel.do_select_all(self, **kwargs)

        for _mission in _session.query(RAMSTKMission).\
                filter(RAMSTKMission.revision_id == _revision_id).all():
            self.tree.create_node(
                _mission.description,
                _mission.mission_id,
                parent=self._root,
                data=_mission,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            try:
                self.last_id = max(self.last_id, _mission.mission_id)
            except TypeError:
                self.last_id = _mission.mission_id

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKMission table in the RAMSTK Program database.

        :param int revision_id: the Revision ID to add the Mission to.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _revision_id = kwargs['revision_id']
        _mission = RAMSTKMission()
        _mission.revision_id = _revision_id
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _mission,
            ],
        )

        if _error_code == 0:
            self.tree.create_node(
                _mission.description,
                _mission.mission_id,
                parent=self._root,
                data=_mission,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = _mission.mission_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove the RAMSTKMission record associated with Node ID.

        :param int node_id: the ID of the Mission to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'Mission ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the RAMSTKMission record associated with Node ID.

        :param int node_id: the Mission ID of the Mission to save to the RAMSTK
                               Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent Mission ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKMission records.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all records in the usage profile "
                "mission table."
            )

        return _error_code, _msg


class MissionPhaseDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a Mission.

    The Phase data model contains the attributes and methods of a mission
    phase.  A Mission will consist of one or more mission phases.  The
    attributes of a Phase are:
    """

    _tag = 'Mission Phases'
    _root = 0

    def __init__(self, dao):
        """
        Initialize a Mission Phase data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the RAMSTKMissionPhase records from the RAMSTK Program database.

        :param int mission_id: the Mission ID to selecte the Mission Phases
                               for.
        :return: tree; the treelib Tree() of RAMSTKMissionPhase data models that
                 comprise the Mission Phase tree.
        :rtype: :class:`treelib.Tree`
        """
        _mission_id = kwargs['mission_id']
        _session = RAMSTKDataModel.do_select_all(self, **kwargs)

        for _phase in _session.query(RAMSTKMissionPhase).\
                filter(RAMSTKMissionPhase.mission_id == _mission_id).all():
            self.tree.create_node(
                _phase.name, _phase.phase_id, parent=self._root, data=_phase,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            try:
                self.last_id = max(self.last_id, _phase.phase_id)
            except TypeError:
                self.last_id = _phase.phase_id

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKMissionPhase table in the RAMSTK Program database.

        :param int mission_id: the Mission ID to add the Mission Phase to.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _mission_id = kwargs['mission_id']
        _phase = RAMSTKMissionPhase()
        _phase.mission_id = _mission_id

        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _phase,
            ],
        )

        if _error_code == 0:
            self.tree.create_node(
                _phase.name, _phase.phase_id, parent=self._root, data=_phase,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = _phase.phase_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove the RAMSTKMissionPhase record associated with Node ID.

        :param int node_id: the ID of the Mission Phase to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'Mission Phase ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the RAMSTKMissionPhase record associated with Node ID.

        :param int node_id: the Phase ID to save to the RAMSTK Program
                             database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent Mission Phase ' \
                   'ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKMissionPhase records.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all records in the usage profile "
                "mission phase table."
            )

        return _error_code, _msg


class EnvironmentDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of an Environment.

    The Environment data model contains the attributes and methods of a mission
    phase environment.  A Phase will consist of zero or more environments.  The
    attributes of an Environment are:
    """

    _tag = 'Environments'
    _root = 0

    def __init__(self, dao):
        """
        Initialize an Environment data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all RAMSTKEnvironment records from the RAMSTK Program database.

        :param int phase_id: the Mission Phase ID to select the Environments
        for.
        :return: tree; the treelib Tree() of RAMSTKEnvironment data models
        that comprise the Environment tree.
        :rtype: :py:class:`treelib.Tree`
        """
        _phase_id = kwargs['phase_id']
        _session = RAMSTKDataModel.do_select_all(self)

        for _environment in _session.query(RAMSTKEnvironment).\
                filter(RAMSTKEnvironment.phase_id == _phase_id).all():
            self.tree.create_node(
                _environment.name,
                _environment.environment_id,
                parent=self._root,
                data=_environment,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            try:
                self.last_id = max(self.last_id, _environment.environment_id)
            except TypeError:
                self.last_id = _environment.environment_id

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKEnvironment table in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _phase_id = kwargs['phase_id']
        _environment = RAMSTKEnvironment()
        _environment.phase_id = _phase_id

        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _environment,
            ],
        )

        if _error_code == 0:
            self.tree.create_node(
                _environment.name,
                _environment.environment_id,
                parent=self._root,
                data=_environment,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = _environment.environment_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove the RAMSTKEnvironment record associated with Node ID.

        :param int node_id: the ID of the Environment to be removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'Environment ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the RAMSTKEnvironment record associated with Node ID.

        :param str node_id: the PyPubSub Tree() node ID of the Environment to
                            save to the RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent Environment ' \
                   'ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKEnvironment records to the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all records in the usage profile "
                "environment table."
            )

        return _error_code, _msg
