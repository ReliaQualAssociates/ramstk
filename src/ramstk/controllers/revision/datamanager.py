# -*- coding: utf-8 -*-
#
#       ramstk.controllers.revision.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Revision Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub
from treelib import Tree
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import (
    RAMSTKEnvironment, RAMSTKFailureDefinition,
    RAMSTKMission, RAMSTKMissionPhase, RAMSTKRevision
)


class DataManager(RAMSTKDataManager):
    """
    Contain the attributes and methods of the Revision data manager.

    This class manages the revision data from the RAMSTKRevision,
    RAMSTKFailureDefinition, RAMSTKMission, RAMSTKMissionPhase, and
    RAMSKTEnvironment data models.
    """

    _tag = 'revision'
    _root = 0

    def __init__(self, **kwargs: Any) -> None:  # pylint:
        # disable=unused-argument
        """Initialize a Revision data manager instance."""
        RAMSTKDataManager.__init__(self, **kwargs)

        # Initialize private dictionary attributes.
        self._last_id = {
            'failure_definition': 1,
            'mission': 1,
            'mission_phase': 1,
            'environment': 1
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_select_all, 'request_retrieve_revisions')
        pub.subscribe(self._do_delete, 'request_delete_revision')
        pub.subscribe(self._do_delete_failure_definition,
                      'request_delete_failure_definition')
        pub.subscribe(self._do_delete_mission, 'request_delete_mission')
        pub.subscribe(self._do_delete_mission_phase,
                      'request_delete_mission_phase')
        pub.subscribe(self._do_delete_environment,
                      'request_delete_environment')
        pub.subscribe(self.do_insert, 'request_insert_revision')
        pub.subscribe(self.do_insert_failure_definition,
                      'request_insert_failure_definition')
        pub.subscribe(self.do_insert_mission, 'request_insert_mission')
        pub.subscribe(self.do_insert_mission_phase,
                      'request_insert_mission_phase')
        pub.subscribe(self.do_insert_environment, 'request_insert_environment')
        pub.subscribe(self.do_update, 'request_update_revision')
        pub.subscribe(self._do_update_failure_definition,
                      'request_update_failure_definition')
        pub.subscribe(self._do_update_usage_profile,
                      'request_update_usage_profile')
        pub.subscribe(self.do_update_all, 'request_update_all_revisions')
        pub.subscribe(self._do_update_all_failure_definition,
                      'request_update_all_failure_definitions')
        pub.subscribe(self._do_update_all_usage_profiles,
                      'request_update_all_usage_profiles')
        pub.subscribe(self._do_get_attributes,
                      'request_get_revision_attributes')
        pub.subscribe(self.do_get_all_attributes,
                      'request_get_all_revision_attributes')
        pub.subscribe(self.do_get_tree, 'request_get_revision_tree')
        pub.subscribe(self.do_set_attributes,
                      'request_set_revision_attributes')
        pub.subscribe(self.do_set_all_attributes,
                      'request_set_all_revision_attributes')
        pub.subscribe(self._do_set_failure_definition,
                      'lvw_editing_failure_definition')
        pub.subscribe(self._do_set_usage_profile, 'lvw_editing_usage_profile')
        pub.subscribe(self.do_set_attributes, 'wvw_editing_revision')

    def _do_delete(self, node_id: int) -> None:
        """
        Remove a revision.

        :param int node_id: the node (revision) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            RAMSTKDataManager.do_delete(self, node_id, 'revision')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_revision',
                            node_id=node_id,
                            tree=self.tree)
        except DataAccessError:
            _error_msg = ("Attempted to delete non-existent revision ID "
                          "{0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_revision', error_message=_error_msg)
        except NodeIDAbsentError:
            _error_msg = ("Revision ID {0:s} was not found as a node "
                          "in the tree.").format(str(node_id))
            pub.sendMessage('fail_delete_revision', error_message=_error_msg)

    def _do_delete_failure_definition(self, revision_id: int,
                                      node_id: int) -> None:
        """
        Remove a failure definition.

        :param int revision_id: the revision ID to remove the failure
            definition from.
        :param int node_id: the failure definition ID to remove.
        :return: None
        :rtype: None
        """
        _dic_definitions = RAMSTKDataManager.do_select(self, revision_id,
                                                       'failure_definitions')
        try:
            self.dao.do_delete(_dic_definitions[node_id])

            _dic_definitions.pop(node_id)
            self.tree.get_node(
                revision_id).data['failure_definitions'] = _dic_definitions

            pub.sendMessage('succeed_delete_failure_definition',
                            tree=_dic_definitions)
        except KeyError:
            pub.sendMessage('fail_delete_failure_definition',
                            error_message=("Attempted to delete non-existent "
                                           "failure definition ID {0:s} from "
                                           "revision ID {1:s}.").format(
                                               str(node_id), str(revision_id)))

    def _do_delete_mission(self, revision_id: int, node_id: int) -> None:
        """
        Remove a mission from revision ID.

        :param int revision_id: the revision ID to remove the mission from.
        :param int node_id: the mission ID to remove.
        :return: None
        :rtype: None
        """
        try:
            _profile_tree = self._do_delete_profile(revision_id, node_id)
            pub.sendMessage('succeed_delete_mission', tree=_profile_tree)
        except AttributeError:
            pub.sendMessage('fail_delete_mission',
                            error_message=("Attempted to delete non-existent "
                                           "mission ID {0:s} from revision ID "
                                           "{1:s}.").format(
                                               str(node_id), str(revision_id)))

    def _do_delete_mission_phase(self, revision_id: int, mission_id: int,
                                 node_id: int) -> None:
        """
        Remove a mission phase from mission ID.

        :param int revision_id: the revision ID to remove the mission from.
        :param int mission_id: the mission ID to remove the mission phase from.
        :param int node_id: the mission phase ID to remove.
        :return: None
        :rtype: None
        """
        try:
            _profile_tree = self._do_delete_profile(revision_id, node_id)
            pub.sendMessage('succeed_delete_mission_phase', tree=_profile_tree)
        except AttributeError:
            pub.sendMessage(
                'fail_delete_mission_phase',
                error_message=("Attempted to delete non-existent "
                               "mission phase ID {0:s} from mission "
                               "ID {1:s}.").format(str(node_id),
                                                   str(mission_id)))

    def _do_delete_environment(self, revision_id: int, phase_id: int,
                               node_id: int) -> None:
        """
        Remove a environment.

        :param int revision_id: the revision ID to remove the environment from.
        :param int phase_id: the mission phase ID to remove the environment
            from.
        :param int node_id: the environment ID to remove.
        :return: None
        :rtype: None
        """
        try:
            _profile_tree: Tree = self._do_delete_profile(revision_id, node_id)
            pub.sendMessage('succeed_delete_environment', tree=_profile_tree)
        except AttributeError:
            pub.sendMessage('fail_delete_environment',
                            error_message=("Attempted to delete non-existent "
                                           "environment ID {0:s} from mission "
                                           "phase ID {1:s}.").format(
                                               str(node_id), str(phase_id)))

    def _do_delete_profile(self, revision_id: int, node_id: int) -> Tree:
        """
        Remove a usage profile element.

        :param int revision_id: the revision ID to remove the usage profile
            element from.
        :param int node_id: the usage profile element ID to remove.
        :return: _profile_tree; the treelib.Tree() holding the usage profile
            for revision_id.
        :rtype: :class:`treelib.Tree`
        """
        _profile_tree = RAMSTKDataManager.do_select(self, revision_id,
                                                    'usage_profile')

        self.dao.do_delete(_profile_tree.get_node(str(node_id)).data)
        _profile_tree.remove_node(str(node_id))
        self.tree.get_node(revision_id).data['usage_profile'] = _profile_tree

        return _profile_tree

    def _do_get_attributes(self, node_id: int, table: str) -> None:
        """
        Retrieve the RAMSTK data table attributes for the revision.

        .. important:: the failure definition will return a dict of all the
            failure definitions associated with the node (revision) ID.  This
            dict uses the definition ID as the key and the instance of the
            RAMSTKFailureDefinition as the value.  The subscibing methods and
            functions will need to unpack this dict.

        .. important:: the usage profile will return a treelib Tree() of all
            the usage profiles associated with the node (revision) ID.  The
            subscribing methods and functions will need to parse this Tree().

        :param int node_id: the node (revision) ID of the revision to get the
            attributes for.
        :param str table: the RAMSTK data table to retrieve the attributes
            from.
        :return: None
        :rtype: None
        """
        if table in ['failure_definitions', 'usage_profile']:
            _attributes = self.do_select(node_id, table=table)
        else:
            _attributes = self.do_select(node_id, table=table).get_attributes()

        pub.sendMessage('succeed_get_{0:s}_attributes'.format(table),
                        attributes=_attributes)

    def _do_select_usage_profile(self, revision_id: int) -> Tree:
        """
        Retrieve the usage profile data from the RAMSTK Program database.

        :param int revision_id: the Revision ID to select the Usage Profile
            for.
        :return: _tree; the usage profile treelib Tree().
        :rtype: :class:`treelib.Tree()`
        """
        _tree = Tree()
        _tree.create_node(tag='usage_profile',
                          identifier=revision_id,
                          parent=None)

        for _mission in self.dao.do_select_all(RAMSTKMission,
                                               key=RAMSTKMission.revision_id,
                                               value=revision_id):
            _tree.create_node(tag=_mission.description,
                              identifier='{0:d}'.format(_mission.mission_id),
                              parent=revision_id,
                              data=_mission)
            self._last_id['mission'] = _mission.mission_id

            for _phase in self.dao.do_select_all(
                    RAMSTKMissionPhase,
                    key=RAMSTKMissionPhase.mission_id,
                    value=_mission.mission_id):
                _tree.create_node(tag=_phase.description,
                                  identifier='{0:d}.{1:d}'.format(
                                      _mission.mission_id, _phase.phase_id),
                                  parent=str(_mission.mission_id),
                                  data=_phase)
                self._last_id['mission_phase'] = _phase.phase_id

                for _environment in self.dao.do_select_all(
                        RAMSTKEnvironment,
                        key=RAMSTKEnvironment.phase_id,
                        value=_phase.phase_id):
                    _tree.create_node(tag=_environment.name,
                                      identifier='{0:d}.{1:d}.{2:d}'.format(
                                          _mission.mission_id, _phase.phase_id,
                                          _environment.environment_id),
                                      parent='{0:d}.{1:d}'.format(
                                          _mission.mission_id,
                                          _phase.phase_id),
                                      data=_environment)
                    self._last_id['environment'] = _environment.environment_id

        return _tree

    def _do_set_failure_definition(self, node_id: List, package: Dict) -> None:
        """
        Set the attributes of the record associated with definition ID.

        This is a helper method to set the desired failure definition attribute
        since the failure definitions are carried in a dict and we need to
        select the correct record to update.

        :param list node_id: the ID of the revision and the failure
            definition in the RAMSTK Program database table whose attributes
            are to be set.
        :param dict package: the key:value pair of the attribute to set.
        :return: None
        :rtype: None
        """
        try:
            _attributes = self.do_select(
                node_id[0],
                table='failure_definitions')[node_id[1]].get_attributes()
            _attributes.pop('revision_id')
            _attributes.pop('definition_id')
        except KeyError:
            _attributes = {}

        for _key in list(package.keys()):
            if _key in _attributes:
                _attributes[_key] = package[_key]
                self.do_select(node_id[0], table='failure_definitions')[
                    node_id[1]].set_attributes(_attributes)

    def _do_set_usage_profile(self, node_id: List, package: Dict) -> None:
        """
        Set the attributes of the record associated with usage ID.

        This is a helper method to set the desired usage profile attribute
        since the usage profile is carried as a treelib Tree() and we need to
        select the correct node (record) to update.

        :param list node_id: the ID of the revision and the usage profile in
            the RAMSTK Program database table whose attributes are to be set.
        :param dict package: the key:value pair of the attribute to set.
        :return: None
        :rtype: None
        """
        try:
            _attributes = self.do_select(node_id[0],
                                         table='usage_profile').get_node(
                                             node_id[2]).data.get_attributes()

            if len(node_id[2].split('.')) == 1:
                _attributes.pop('revision_id')
                _attributes.pop('mission_id')
            elif len(node_id[2].split('.')) == 2:
                _attributes.pop('mission_id')
                _attributes.pop('phase_id')
            elif len(node_id[2].split('.')) == 3:
                _attributes.pop('phase_id')
                _attributes.pop('environment_id')

        except (AttributeError, KeyError):
            _attributes = {}

        for _key in list(package.keys()):
            if _key in _attributes:
                _attributes[_key] = package[_key]
                self.do_select(node_id[0], table='usage_profile').get_node(
                    node_id[2]).data.set_attributes(_attributes)

    def _do_update_all_failure_definition(self, revision_id: int) -> None:
        """
        Update all the failure defintions.

        :param int revision_id: the revision ID whose failure definitions are
            to be updated.
        :return: None
        :rtype: None
        """
        for _definition_id in self.tree.get_node(
                revision_id).data['failure_definitions']:
            self._do_update_failure_definition(revision_id, _definition_id)

    def _do_update_failure_definition(self, revision_id: int,
                                      node_id: int) -> None:
        """
        Update the failure definition associated with node ID in database.

        :param int revision_id: the revision ID whose failure definition is
            to be updated.
        :param int node_id: the node (failure definition) ID of the failure
            definition to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.do_update(
                self.tree.get_node(revision_id).data['failure_definitions']
                [node_id])
            pub.sendMessage('succeed_update_failure_definition',
                            node_id=node_id)
        except (DataAccessError, KeyError):
            pub.sendMessage('fail_update_failure_definition',
                            error_message=('Attempted to save non-existent '
                                           'failure definition with ID '
                                           '{0:s}.').format(str(node_id)))
        except TypeError:
            if node_id != 0:
                pub.sendMessage('fail_update_failure_definition',
                                error_message=('No data package found for '
                                               'failure definition ID '
                                               '{0:s}.').format(str(node_id)))

    def _do_update_all_usage_profiles(self, revision_id: int) -> None:
        """
        Update all the failure definitions.

        :param int revision_id: the revision ID whose failure definitions are
            to be updated.
        :return: None
        :rtype: None
        """
        for _profile in self.tree.get_node(
                revision_id).data['usage_profile'].all_nodes():
            self._do_update_usage_profile(revision_id,
                                          str(_profile.identifier))

    def _do_update_usage_profile(self, revision_id: int, node_id: str) -> None:
        """
        Update the usage profile item associated with node ID in database.

        :param int revision_id: the revision ID for the usage profile to
            update.
        :param str node_id: the node (mission, mission phase, or environment)
            ID of the usage profile element to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.do_update(
                self.tree.get_node(revision_id).data['usage_profile'].get_node(
                    node_id).data)
            pub.sendMessage('succeed_update_usage_profile', node_id=node_id)
        except (AttributeError, DataAccessError):
            pub.sendMessage('fail_update_usage_profile',
                            error_message=('Attempted to save non-existent '
                                           'usage profile element with ID '
                                           '{0:s}.').format(str(node_id)))
        except TypeError:
            if node_id != 0:
                pub.sendMessage('fail_update_usage_profile',
                                error_message=('No data package found for '
                                               'usage profile ID '
                                               '{0:s}.').format(str(node_id)))

    def do_get_all_attributes(self, node_id: int) -> None:
        """
        Retrieve all RAMSTK data tables' attributes for the revision.

        This is a helper method to be able to retrieve all the revision's
        attributes in a single call.  It's used primarily by the
        AnalysisManager.

        :param int node_id: the node (revision) ID of the revision item to
            get the attributes for.
        :return: None
        :rtype: None
        """
        _attributes: Dict[str, Any] = {
            'failure_definitions': {},
            'usage_profile': None
        }
        for _table in ['revision', 'failure_definitions', 'usage_profile']:
            if _table == 'failure_definitions':
                _attributes['failure_definitions'].update(
                    self.do_select(node_id, table=_table))
            elif _table == 'usage_profile':
                _attributes['usage_profile'] = self.do_select(node_id,
                                                              table=_table)
            else:
                _attributes.update(
                    self.do_select(node_id, table=_table).get_attributes())

        pub.sendMessage('succeed_get_all_revision_attributes',
                        attributes=_attributes)

    def do_get_tree(self) -> None:
        """
        Retrieve the revision treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_revision_tree', dmtree=self.tree)

    def do_insert(self) -> None:  # pylint: disable=arguments-differ
        """
        Add a new revision.

        :return: None
        :rtype: None
        :raise: AttributeError if not connected to a RAMSTK program database.
        """
        _tree = Tree()

        try:
            _last_id = self.dao.get_last_id('ramstk_revision', 'revision_id')
            _revision = RAMSTKRevision(revision_id=_last_id + 1,
                                       name='New Revision')
            self.dao.do_insert(_revision)

            self.last_id = _revision.revision_id
            _tree.create_node(tag='usage_profile',
                              identifier=self.last_id,
                              parent=None)
            self.tree.create_node(tag=_revision.name,
                                  identifier=self.last_id,
                                  parent=self._root,
                                  data={
                                      'revision': _revision,
                                      'failure_definitions': {},
                                      'usage_profile': _tree
                                  })
            self.do_insert_failure_definition(self.last_id)
            self.do_insert_mission(self.last_id)
            pub.sendMessage('succeed_insert_revision',
                            node_id=self.last_id,
                            tree=self.tree)
        except DataAccessError as _error:
            print(_error)
            pub.sendMessage("fail_insert_revision",
                            error_message=("Failed to insert revision into "
                                           "program database."))

    def do_insert_environment(self, revision_id: int, mission_id: int,
                              phase_id: int) -> None:
        """
        Add a new environment for phase ID.

        :param int revision_id: the revision ID to add the new environment.
        :param int mission_id: the mission ID to add the new environment.
        :param int phase_id: the mission phase ID to add the new environment.
        :return: None
        :rtype: None
        """
        try:
            _last_id = self.dao.get_last_id('ramstk_environment',
                                            'environment_id')
            _environment = RAMSTKEnvironment(phase_id=phase_id,
                                             environment_id=_last_id + 1)
            self.dao.do_insert(_environment)
            self._last_id['environment'] = _environment.environment_id
            _phase_id = '{0:s}.{1:s}'.format(str(mission_id), str(phase_id))
            _environment_id = '{0:s}.{1:s}.{2:s}'.format(
                str(mission_id), str(phase_id),
                str(_environment.environment_id))
            self.tree.get_node(revision_id).data['usage_profile'].create_node(
                tag=_environment.name,
                identifier=str(_environment_id),
                parent=str(_phase_id),
                data=_environment)
            _profile_tree = RAMSTKDataManager.do_select(
                self, revision_id, 'usage_profile')
            pub.sendMessage("succeed_insert_environment", tree=_profile_tree)
        except DataAccessError as _error:
            print(_error)
            pub.sendMessage("fail_insert_environment", error_message=_error)

    def do_insert_failure_definition(self, revision_id: int) -> None:
        """
        Add a new failure definition for revision ID.

        :param int revision_id: the revision ID to add the new failure
            definition to.
        :return: None
        :rtype: None
        """
        try:
            _last_id = self.dao.get_last_id('ramstk_failure_definition',
                                            'definition_id')
            _failure_definition = RAMSTKFailureDefinition(
                revision_id=revision_id, definition_id=_last_id + 1)
            self.dao.do_insert(_failure_definition)
            self.tree.get_node(revision_id).data['failure_definitions'][
                _failure_definition.definition_id] = _failure_definition
            _dic_definitions = RAMSTKDataManager.do_select(
                self, revision_id, 'failure_definitions')
            self._last_id['failure_definition'] = \
                _failure_definition.definition_id
            pub.sendMessage("succeed_insert_failure_definition",
                            tree=_dic_definitions)
        except DataAccessError as _error:
            print(_error)
            pub.sendMessage("fail_insert_failure_definition",
                            error_message=_error)

    def do_insert_mission(self, revision_id: int) -> None:
        """
        Add a new mission for revision ID.

        :param int revision_id: the revision ID to add the new mission.
        :return: None
        :rtype: None
        """
        try:
            _last_id = self.dao.get_last_id('ramstk_mission', 'mission_id')
            _mission = RAMSTKMission(revision_id=revision_id,
                                     mission_id=_last_id + 1)
            self.dao.do_insert(_mission)

            self.tree.get_node(revision_id).data['usage_profile'].create_node(
                tag=_mission.description,
                identifier='{0:s}'.format(str(_mission.mission_id)),
                parent=revision_id,
                data=_mission)
            _profile_tree = RAMSTKDataManager.do_select(
                self, revision_id, 'usage_profile')
            self._last_id['mission'] = _mission.mission_id
            pub.sendMessage("succeed_insert_mission", tree=_profile_tree)
        except DataAccessError as _error:
            print(_error)
            pub.sendMessage("fail_insert_mission", error_message=_error)

    def do_insert_mission_phase(self, revision_id: int,
                                mission_id: int) -> None:
        """
        Add a new mission phase for mission ID.

        :param int revision_id: the revision ID to add the new mission phase.
        :param int mission_id: the mission ID to add the new mission phase.
        :return: None
        :rtype: None
        """
        try:
            _last_id = self.dao.get_last_id('ramstk_mission_phase', 'phase_id')
            _phase = RAMSTKMissionPhase(mission_id=mission_id,
                                        phase_id=_last_id + 1)
            self.dao.do_insert(_phase)
            self._last_id['mission_phase'] = _phase.phase_id

            _phase_id = '{0:s}.{1:s}'.format(str(mission_id),
                                             str(_phase.phase_id))
            self.tree.get_node(revision_id).data['usage_profile'].create_node(
                tag=_phase.description,
                identifier=str(_phase_id),
                parent=str(mission_id),
                data=_phase)
            _profile_tree = RAMSTKDataManager.do_select(
                self, revision_id, 'usage_profile')
            pub.sendMessage("succeed_insert_mission_phase", tree=_profile_tree)
        except DataAccessError as _error:
            print(_error)
            pub.sendMessage("fail_insert_mission_phase", error_message=_error)

    def do_select_all(self) -> None:
        """
        Retrieve all the Revision data from the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _revision in self.dao.do_select_all(
                RAMSTKRevision,
                key=None,
                value=None,
                order=RAMSTKRevision.revision_id):

            _failure_definitions = self.dao.do_select_all(
                RAMSTKFailureDefinition,
                key=RAMSTKFailureDefinition.revision_id,
                value=_revision.revision_id)
            _failure_definitions = self.do_build_dict(_failure_definitions,
                                                      'definition_id')
            try:
                self._last_id['failure_definitions'] = max(
                    _failure_definitions.keys())
            except ValueError:  # No failure definitions for current revision.
                pass

            _usage_profile = self._do_select_usage_profile(
                _revision.revision_id)

            _data_package = {
                'revision': _revision,
                'failure_definitions': _failure_definitions,
                'usage_profile': _usage_profile
            }

            self.tree.create_node(tag=_revision.name,
                                  identifier=_revision.revision_id,
                                  parent=self._root,
                                  data=_data_package)

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_revisions', tree=self.tree)

    def do_set_all_attributes(self,
                              attributes: Dict[str, Any],
                              definition_id: int = -1,
                              usage_id: str = '') -> None:
        """
        Set all the attributes of the record associated with the Module ID.

        This is a helper function to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param dict attributes: the aggregate attributes dict for the revision.
        :keyword definition_id: the failure definition ID if the attribute
            being set is a failure definition attribute.
        :type definition_id: int
        :keyword str usage_id: the usage profile ID if the attribute being set
            is a usage profile (mission, mission phase, or environment)
            attribute.
        :type usage_id: str
        :return: None
        :rtype: None
        """
        for _key in attributes:
            self.do_set_attributes(
                node_id=[attributes['revision_id'], definition_id, usage_id],
                package={_key: attributes[_key]})

    def do_set_attributes(self, node_id: List, package: Dict) -> None:
        """
        Set the attributes of the record associated with the Node ID.

        :param list node_id: a list of the ID's of the record in the RAMSTK
            Program database table whose attributes are to be set.  The list
            is:

                0 - Revision ID
                1 - Failure Definition ID
                2 - Usage ID

        :param dict package: the key:value for the attribute being updated.
        :return: None
        :rtype: None
        """
        [[_key, _value]] = package.items()

        for _table in ['revision', 'failure_definitions', 'usage_profile']:
            if _table == 'failure_definitions':
                self._do_set_failure_definition(node_id, package)
            elif _table == 'usage_profile':
                self._do_set_usage_profile(node_id, package)
            else:
                _attributes = self.do_select(node_id[0],
                                             table=_table).get_attributes()
                if _key in _attributes:
                    _attributes[_key] = _value

                    try:
                        _attributes.pop('revision_id')
                    except KeyError:
                        pass

                    self.do_select(node_id[0],
                                   table=_table).set_attributes(_attributes)

    def do_update(self, node_id: int) -> None:
        """
        Update the record associated with node ID in RAMSTK Program database.

        :param int node_id: the node (revision) ID of the revision to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.do_update(self.tree.get_node(node_id).data['revision'])
            pub.sendMessage('succeed_update_revision', node_id=node_id)
        except (AttributeError, DataAccessError):
            pub.sendMessage('fail_update_revision',
                            error_message=('Attempted to save non-existent '
                                           'revision with revision ID '
                                           '{0:s}.').format(str(node_id)))
        except TypeError:
            if node_id != 0:
                pub.sendMessage('fail_update_revision',
                                error_message=('No data package found for '
                                               'revision ID {0:s}.').format(
                                                   str(node_id)))
