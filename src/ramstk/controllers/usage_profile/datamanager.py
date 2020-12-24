# -*- coding: utf-8 -*-
#
#       ramstk.controllers.usage_profile.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Usage Profile Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import (
    RAMSTKEnvironment, RAMSTKMission, RAMSTKMissionPhase
)


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Usage Profile data manager.

    This class manages the usage profile data from the RAMSTKMission,
    RAMSTKMissionPhase, and RAMSKTEnvironment data models.
    """

    _tag = 'usage_profile'

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a RAMSTKFailureDefinition, data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.last_id: Dict[str, int] = {
            'mission': -1,
            'mission_phase': -1,
            'environment': -1,
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_usage_profile_attributes')
        pub.subscribe(super().do_update_all,
                      'request_update_all_usage_profiles')

        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self.do_get_tree, 'request_get_usage_profile_tree')
        pub.subscribe(self.do_update, 'request_update_usage_profile')

        pub.subscribe(self._do_delete, 'request_delete_usage_profile')
        pub.subscribe(self._do_insert_environment,
                      'request_insert_environment')
        pub.subscribe(self._do_insert_mission, 'request_insert_mission')
        pub.subscribe(self._do_insert_mission_phase,
                      'request_insert_mission_phase')
        pub.subscribe(self._do_set_attributes,
                      'request_set_usage_profile_attributes')
        pub.subscribe(self._do_set_attributes, 'lvw_editing_usage_profile')
        pub.subscribe(self._do_set_all_attributes,
                      'request_set_all_usage_profile_attributes')

    def do_get_tree(self) -> None:
        """Retrieve the revision treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'succeed_get_usage_profile_tree',
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve the Usage Profile data from the RAMSTK Program database.

        :param attributes: the attributes for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _mission in self.dao.do_select_all(RAMSTKMission,
                                               key=['revision_id'],
                                               value=[self._revision_id]):
            self.tree.create_node(tag='mission',
                                  identifier='{0:d}'.format(
                                      _mission.mission_id),
                                  parent=self._root,
                                  data={'usage_profile': _mission})
            self.last_id['mission'] = _mission.mission_id

            for _phase in self.dao.do_select_all(RAMSTKMissionPhase,
                                                 key=['mission_id'],
                                                 value=[_mission.mission_id]):
                self.tree.create_node(tag='mission_phase',
                                      identifier='{0:d}.{1:d}'.format(
                                          _mission.mission_id,
                                          _phase.phase_id),
                                      parent=str(_mission.mission_id),
                                      data={'usage_profile': _phase})
                self.last_id['mission_phase'] = _phase.phase_id

                for _environment in self.dao.do_select_all(
                        RAMSTKEnvironment,
                        key=['phase_id'],
                        value=[_phase.phase_id]):
                    self.tree.create_node(
                        tag='environment',
                        identifier='{0:d}.{1:d}.{2:d}'.format(
                            _mission.mission_id, _phase.phase_id,
                            _environment.environment_id),
                        parent='{0:d}.{1:d}'.format(_mission.mission_id,
                                                    _phase.phase_id),
                        data={'usage_profile': _environment})
                    self.last_id['environment'] = _environment.environment_id

        pub.sendMessage(
            'succeed_retrieve_usage_profile',
            tree=self.tree,
        )

    def do_update(self, node_id: str) -> None:
        """Update record associated with node ID in RAMSTK Program database.

        :param node_id: the node (usage profile) ID of the record to save.
        :return: None
        :rtype: None
        """
        _method_name: str = inspect.currentframe(  # type: ignore
        ).f_code.co_name

        try:
            self.dao.do_update(
                self.tree.get_node(node_id).data['usage_profile'])
            pub.sendMessage(
                'succeed_update_usage_profile',
                tree=self.tree,
            )
        except AttributeError:
            _error_msg: str = (
                '{1}: Attempted to save non-existent usage profile ID {'
                '0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_usage_profile',
                error_message=_error_msg,
            )
        except (KeyError, TypeError):
            if node_id != 0:
                _error_msg = (
                    '{1}: No data package found for usage profile ID {'
                    '0}.').format(str(node_id), _method_name)
                pub.sendMessage(
                    'do_log_debug',
                    logger_name='DEBUG',
                    message=_error_msg,
                )
                pub.sendMessage(
                    'fail_update_usage_profile',
                    error_message=_error_msg,
                )

    def _do_delete(self, node_id: int) -> None:
        """Remove a usage profile element.

        :param node_id: the usage profile element ID to remove.
        :return: None
        :rtype: None
        """
        try:
            super().do_delete(node_id, 'usage_profile')

            self.tree.remove_node(node_id)

            pub.sendMessage(
                'succeed_delete_usage_profile',
                tree=self.tree,
            )
        except (DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Attempted to delete non-existent usage profile ID {0}.'
            ).format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_delete_usage_profile',
                error_message=_error_msg,
            )

    def _do_insert_environment(self, mission_id: int, phase_id: int) -> None:
        """Add a new environment for phase ID.

        :param mission_id: the mission ID to add the new environment.
        :param phase_id: the mission phase ID to add the new environment.
        :return: None
        :rtype: None
        """
        try:
            _last_id = self.dao.get_last_id('ramstk_environment',
                                            'environment_id')
            _environment = RAMSTKEnvironment()
            _environment.phase_id = phase_id
            _environment.environment_id = _last_id + 1

            self.dao.do_insert(_environment)

            _phase_id = '{0:s}.{1:s}'.format(str(mission_id), str(phase_id))
            _node_id = '{0:s}.{1:s}.{2:s}'.format(
                str(mission_id), str(phase_id),
                str(_environment.environment_id))
            self.tree.create_node(tag='environment',
                                  identifier=_node_id,
                                  parent=_phase_id,
                                  data={'usage_profile': _environment})
            self.last_id['environment'] = _environment.environment_id
            pub.sendMessage(
                "succeed_insert_usage_profile",
                node_id=_node_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_usage_profile",
                error_message=_error.msg,
            )

    def _do_insert_mission(self) -> None:
        """Add a new mission for revision ID.

        :return: None
        :rtype: None
        """
        try:
            _last_id = self.dao.get_last_id('ramstk_mission', 'mission_id')
            _mission = RAMSTKMission()
            _mission.revision_id = self._revision_id
            _mission.mission_id = _last_id + 1

            self.dao.do_insert(_mission)

            _node_id = '{0:d}'.format(_mission.mission_id)

            self.tree.create_node(tag='mission',
                                  identifier=_node_id,
                                  parent=self._root,
                                  data={'usage_profile': _mission})
            self.last_id['mission'] = _mission.mission_id
            pub.sendMessage(
                "succeed_insert_usage_profile",
                node_id=_node_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_usage_profile",
                error_message=_error.msg,
            )

    def _do_insert_mission_phase(self, mission_id: int) -> None:
        """Add a new mission phase for mission ID.

        :param mission_id: the mission ID to add the new mission phase.
        :return: None
        :rtype: None
        """
        try:
            _last_id = self.dao.get_last_id('ramstk_mission_phase', 'phase_id')
            _phase = RAMSTKMissionPhase()
            _phase.mission_id = mission_id
            _phase.phase_id = _last_id + 1

            self.dao.do_insert(_phase)

            _node_id = '{0:d}.{1:d}'.format(mission_id, _phase.phase_id)
            self.tree.create_node(tag='mission_phase',
                                  identifier=_node_id,
                                  parent=str(mission_id),
                                  data={'usage_profile': _phase})
            self.last_id['mission_phase'] = _phase.phase_id
            pub.sendMessage(
                'succeed_insert_usage_profile',
                node_id=_node_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_usage_profile",
                error_message=_error.msg,
            )

    def _do_set_attributes(self, node_id: List, package: Dict) -> None:
        """Set the attributes of the record associated with the Node ID.

        :param node_id: the ID of the record whose attributes are to be set.
        :param package: the key:value for the attribute being updated.
        :return: None
        :rtype: None
        """
        [[_key, _value]] = package.items()

        try:
            _attributes = self.do_select(
                node_id[0], table='usage_profile').get_attributes()
            if _key in _attributes:
                _attributes[_key] = _value

                _level = len(node_id[0].split('.'))
                for _attribute in {
                        1: ['revision_id', 'mission_id'],
                        2: ['mission_id', 'phase_id'],
                        3: ['phase_id', 'environment_id'],
                }[_level]:
                    _attributes.pop(_attribute)

                self.do_select(
                    node_id[0],
                    table='usage_profile').set_attributes(_attributes)

        except (AttributeError, TypeError) as _error:
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error,
            )
            pub.sendMessage(
                'fail_set_usage_profile_attributes',
                node_id=node_id[0],
            )

    def _do_set_all_attributes(self, attributes: Dict[str, Any],
                               node_id: str) -> None:
        """Set all the attributes of the record associated with the Module ID.

        This is a helper function to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param attributes: the aggregate attributes dict for the revision.
        :param node_id: the usage profile ID if the attribute being set
            is a usage profile (mission, mission phase, or environment)
            attribute.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            self._do_set_attributes(node_id=[node_id, ''],
                                    package={_key: attributes[_key]})
