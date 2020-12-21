# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_revision.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Revision algorithms and models."""

# Third Party Imports
import pytest
from __mocks__ import MOCK_ENVIRONMENTS, MOCK_MISSION_PHASES, MOCK_MISSIONS
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmUsageProfile
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import (
    RAMSTKEnvironment, RAMSTKMission, RAMSTKMissionPhase
)


class MockDao:
    _all_missions = []
    _all_mission_phases = []
    _all_environments = []

    def _do_delete_mission(self, record):
        for _idx, _record in enumerate(self._all_missions):
            if _record.mission_id == record.mission_id:
                self._all_missions.pop(_idx)

    def _do_delete_mission_phases(self, record):
        for _idx, _record in enumerate(self._all_mission_phases):
            if _record.phase_id == record.phase_id:
                self._all_mission_phases.pop(_idx)

    def _do_delete_environments(self, record):
        for _idx, _record in enumerate(self._all_environments):
            if _record.environment_id == record.environment_id:
                self._all_environments.pop(_idx)

    def do_delete(self, record):
        if record == RAMSTKMission:
            self._do_delete_mission(record)
        elif record == RAMSTKMissionPhase:
            self._do_delete_mission_phases(record)
        elif record == RAMSTKEnvironment:
            self._do_delete_environments(record)

    def do_insert(self, record):
        if isinstance(record, RAMSTKMission) and record.revision_id == 1:
            self._all_missions.append(record)
            print(self._all_missions)
        elif isinstance(record, RAMSTKMissionPhase) and record.mission_id <\
                10:
            self._all_mission_phases.append(record)
        elif isinstance(record, RAMSTKEnvironment) and record.phase_id < 10:
            self._all_environments.append(record)
        else:
            raise DataAccessError('An error occured with RAMSTK.')

    def _do_select_all_missions(self, table, value):
        _idx = 1
        self._all_missions = []
        for _key in MOCK_MISSIONS:
            _record = table()
            _record.revision_id = value[0]
            _record.mission_id = _idx
            _record.set_attributes(MOCK_MISSIONS[_key])
            self._all_missions.append(_record)
            _idx += 1

        return self._all_missions

    def _do_select_all_mission_phases(self, table, value):
        _idx = 1
        self._all_mission_phases = []
        for _key in MOCK_MISSION_PHASES:
            _record = table()
            _record.mission_id = value
            _record.phase_id = _idx
            _record.set_attributes(MOCK_MISSION_PHASES[_key])
            self._all_mission_phases.append(_record)
            _idx += 1

        return self._all_mission_phases

    def _do_select_all_environments(self, table, value):
        _idx = 1
        self._all_environments = []
        for _key in MOCK_ENVIRONMENTS:
            _record = table()
            _record.phase_id = value
            _record.environment_id = _idx
            _record.set_attributes(MOCK_ENVIRONMENTS[_key])
            self._all_environments.append(_record)
            _idx += 1

        return self._all_environments

    def do_select_all(self, table, key, value, order=None, _all=False):
        if table == RAMSTKMission:
            return self._do_select_all_missions(table, value)
        elif table == RAMSTKMissionPhase:
            for _mission in self._all_missions:
                return self._do_select_all_mission_phases(
                    table, _mission.mission_id)
        elif table == RAMSTKEnvironment:
            for _phase in self._all_mission_phases:
                return self._do_select_all_environments(table, _phase.phase_id)

    def do_update(self, record):
        for _key in MOCK_MISSIONS:
            if _key == record.mission_id:
                MOCK_MISSIONS[_key]['description'] = record.description

    def get_last_id(self, table, id_column):
        if table == 'ramstk_environment':
            return max(MOCK_ENVIRONMENTS.keys())
        elif table == 'ramstk_mission':
            return max(MOCK_MISSIONS.keys())
        elif table == 'ramstk_mission_phase':
            return max(MOCK_MISSION_PHASES.keys())


@pytest.fixture
def mock_program_dao(monkeypatch):
    yield MockDao()


class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager(self):
        """__init__() should return a Revision data manager."""
        DUT = dmUsageProfile()

        assert isinstance(DUT, dmUsageProfile)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'usage_profile'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_usage_profile_attributes')
        assert pub.isSubscribed(DUT.do_get_tree,
                                'request_get_usage_profile_tree')
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_update, 'request_update_usage_profile')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_usage_profiles')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_usage_profile')
        assert pub.isSubscribed(DUT._do_insert_environment,
                                'request_insert_environment')
        assert pub.isSubscribed(DUT._do_insert_mission,
                                'request_insert_mission')
        assert pub.isSubscribed(DUT._do_insert_mission_phase,
                                'request_insert_mission_phase')
        assert pub.isSubscribed(DUT._do_set_attributes,
                                'request_set_usage_profile_attributes')
        assert pub.isSubscribed(DUT._do_set_all_attributes,
                                'request_set_all_usage_profile_attributes')


class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMission, RAMSTKMissionPhase, and RAMSTKEnvironment instances on
        success."""
        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert isinstance(DUT.tree, Tree)
        assert isinstance(
            DUT.tree.get_node('1').data['usage_profile'], RAMSTKMission)
        assert isinstance(
            DUT.tree.get_node('1.1').data['usage_profile'], RAMSTKMissionPhase)
        assert isinstance(
            DUT.tree.get_node('1.1.1').data['usage_profile'],
            RAMSTKEnvironment)

    @pytest.mark.unit
    def test_do_select_all_tree_loaded(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMission, RAMSTKMissionPhase, and RAMSTKEnvironment instances on
        success when the tree is already populated."""
        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_select_all(attributes={'revision_id': 1})

        assert isinstance(DUT.tree, Tree)
        assert isinstance(
            DUT.tree.get_node('1').data['usage_profile'], RAMSTKMission)
        assert isinstance(
            DUT.tree.get_node('1.1').data['usage_profile'], RAMSTKMissionPhase)
        assert isinstance(
            DUT.tree.get_node('1.1.1').data['usage_profile'],
            RAMSTKEnvironment)

    @pytest.mark.unit
    def test_do_select_mission(self, mock_program_dao):
        """do_select() should return the RAMSTKMission instance on success."""
        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _mission = DUT.do_select('1', table='usage_profile')

        assert isinstance(_mission, RAMSTKMission)

    @pytest.mark.unit
    def test_do_select_mission_phase(self, mock_program_dao):
        """do_select() should return the RAMSTKMissionPhase instance on
        success."""
        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _mission = DUT.do_select('1.1', table='usage_profile')

        assert isinstance(_mission, RAMSTKMissionPhase)

    @pytest.mark.unit
    def test_do_select_mission(self, mock_program_dao):
        """do_select() should return the RAMSTKEnvironment instance on
        success."""
        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _mission = DUT.do_select('1.1.1', table='usage_profile')

        assert isinstance(_mission, RAMSTKEnvironment)

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(1, table='scibbidy-bibbidy-doo') is None

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Revision ID is
        requested."""
        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='usage_profile') is None


class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_mission(self, node_id, tree):
        assert node_id == '1'
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_mission topic was broadcast.")

    def on_fail_delete_mission(self, error_message):
        assert error_message == ('_do_delete: Attempted to delete non-existent usage '
                                 'profile ID 10.')
        print("\033[35m\nfail_delete_mission topic was broadcast.")

    def on_succeed_delete_mission_phase(self, node_id, tree):
        assert node_id == '2.2'
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_mission_phase topic was broadcast.")

    def on_fail_delete_mission_phase(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent usage profile '
            'ID 2.20.')
        print("\033[35m\nfail_delete_mission_phase topic was broadcast.")

    def on_succeed_delete_environment(self, node_id, tree):
        assert node_id == '1.1.1'
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_environment topic was broadcast.")

    def on_fail_delete_environment(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent usage profile ID 3.3.30.')
        print("\033[35m\nfail_delete_environment topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete_mission(self, mock_program_dao):
        """_do_delete_mission() should send the success message after
        successfully deleting a mission."""
        pub.subscribe(self.on_succeed_delete_mission,
                      'succeed_delete_usage_profile')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete('1')

        assert not DUT.tree.contains('1.1.1')
        assert not DUT.tree.contains('1.1')
        assert not DUT.tree.contains('1')

        pub.unsubscribe(self.on_succeed_delete_mission,
                        'succeed_delete_usage_profile')

    @pytest.mark.unit
    def test_do_delete_mission_non_existent_id(self, mock_program_dao):
        """_do_delete_mission() should send the sfail message when attempting
        to delete a non-existent mission ID."""
        pub.subscribe(self.on_fail_delete_mission, 'fail_delete_usage_profile')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete('10')

        pub.unsubscribe(self.on_fail_delete_mission,
                        'fail_delete_usage_profile')

    @pytest.mark.unit
    def test_do_delete_mission_phase(self, mock_program_dao):
        """_do_delete_mission_phase() should send the success message after
        successfully deleting a mission phase."""
        pub.subscribe(self.on_succeed_delete_mission_phase,
                      'succeed_delete_usage_profile')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete('2.2')

        assert not DUT.tree.contains('2.2.2')
        assert not DUT.tree.contains('2.2')

        pub.unsubscribe(self.on_succeed_delete_mission_phase,
                        'succeed_delete_usage_profile')

    @pytest.mark.unit
    def test_do_delete_mission_phase_non_existent_id(self, mock_program_dao):
        """_do_delete_mission_phase() should send the fail message when
        attempting to delete a non-existent mission phase."""
        pub.subscribe(self.on_fail_delete_mission_phase,
                      'fail_delete_usage_profile')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete('2.20')

        pub.unsubscribe(self.on_fail_delete_mission_phase,
                        'fail_delete_usage_profile')

    @pytest.mark.unit
    def test_do_delete_environment(self, mock_program_dao):
        """_do_delete_environment() should send the success message after
        successfully deleting an environment."""
        pub.subscribe(self.on_succeed_delete_environment,
                      'succeed_delete_usage_profile')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete('3.3.3')

        assert not DUT.tree.contains('3.3.3')

        pub.unsubscribe(self.on_succeed_delete_environment,
                        'succeed_delete_usage_profile')

    @pytest.mark.unit
    def test_do_delete_environment_non_existent_id(self, mock_program_dao):
        """_do_delete_environment() should send the fail message when
        attempting to delete a non-existent environment."""
        pub.subscribe(self.on_fail_delete_environment,
                      'fail_delete_usage_profile')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete('3.3.30')

        pub.unsubscribe(self.on_fail_delete_environment,
                        'fail_delete_usage_profile')


class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_usage_profile_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['revision_id'] == 1
        print(
            "\033[36m\nsucceed_get_usage_profile_attributes topic was broadcast"
        )

    def on_succeed_get_usage_profile_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node('1').data['usage_profile'], RAMSTKMission)
        assert isinstance(
            tree.get_node('1.1').data['usage_profile'], RAMSTKMissionPhase)
        assert isinstance(
            tree.get_node('1.1.1').data['usage_profile'], RAMSTKEnvironment)
        print("\033[36m\nsucceed_get_revision_tree topic was broadcast")

    def on_fail_set_usage_profile_attrs(self, node_id):
        assert node_id == 0
        print("\033[36m\nfail_set_usage_profile_attributes topic was "
              "broadcast")

    @pytest.mark.unit
    def test_do_get_attributes_usage_profile(self, mock_program_dao):
        """_do_get_attributes() should return treelib Tree() on success."""
        pub.subscribe(self.on_succeed_get_usage_profile_attrs,
                      'succeed_get_usage_profile_attributes')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_attributes('1', 'usage_profile')

        pub.unsubscribe(self.on_succeed_get_usage_profile_attrs,
                        'succeed_get_usage_profile_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage(
            'request_set_usage_profile_attributes',
            node_id=['1', ''],
            package={'description': 'This is the mission description.'})
        pub.sendMessage('request_set_usage_profile_attributes',
                        node_id=['1.1', ''],
                        package={'phase_end': 5.12})
        pub.sendMessage('request_set_usage_profile_attributes',
                        node_id=['1.1.1', ''],
                        package={'minimum': 5.12})
        assert DUT.do_select('1', table='usage_profile').description == (
            'This is the mission description.')
        assert DUT.do_select('1.1', table='usage_profile').phase_end == 5.12
        assert DUT.do_select('1.1.1', table='usage_profile').minimum == 5.12

    @pytest.mark.unit
    def test_do_set_attributes_root_node(self, mock_program_dao):
        """do_set_attributes() should send the fail message."""
        pub.subscribe(self.on_fail_set_usage_profile_attrs,
                      'fail_set_usage_profile_attributes')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage(
            'request_set_usage_profile_attributes',
            node_id=[0, ''],
            package={'description': 'This is the mission description.'})

        pub.unsubscribe(self.on_fail_set_usage_profile_attrs,
                        'fail_set_usage_profile_attributes')

    @pytest.mark.unit
    def test_do_set_all_attributes(self, mock_program_dao):
        """do_set_all_attributes() should send the success message."""
        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_all_usage_profile_attributes',
                        attributes={
                            'phase_start': 5.12,
                            'phase_end': 10.24
                        },
                        node_id='1.1')
        assert DUT.do_select('1.1', table='usage_profile').phase_end == 10.24
        assert DUT.do_select('1.1', table='usage_profile').phase_start == 5.12

    @pytest.mark.unit
    def test_do_set_all_attributes_extra_attributes(self, mock_program_dao):
        """do_set_all_attributes() should send the success message."""
        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_all_usage_profile_attributes',
                        attributes={
                            'phase_start': 5.12,
                            'phase_end': 10.24,
                            'funpack': 'Fun Packer',
                        },
                        node_id='1.1')
        assert DUT.do_select('1.1', table='usage_profile').phase_end == 10.24
        assert DUT.do_select('1.1', table='usage_profile').phase_start == 5.12

    @pytest.mark.unit
    def test_on_get_tree(self, mock_program_dao):
        """on_get_tree() should return the revision treelib Tree."""
        pub.subscribe(self.on_succeed_get_usage_profile_tree,
                      'succeed_get_usage_profile_tree')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_usage_profile_tree,
                        'succeed_get_usage_profile_tree')


class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_mission(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_mission topic was broadcast")

    def on_fail_insert_mission(self, error_message):
        assert error_message == ('An error occured with RAMSTK.')
        print("\033[35m\nfail_insert_function topic was broadcast.")

    def on_succeed_insert_mission_phase(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_mission_phase topic was broadcast")

    def on_fail_insert_mission_phase(self, error_message):
        assert error_message == ('An error occured with RAMSTK.')
        print("\033[35m\nfail_insert_function topic was broadcast.")

    def on_succeed_insert_environment(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_environment topic was broadcast")

    def on_fail_insert_environment(self, error_message):
        assert error_message == ('An error occured with RAMSTK.')
        print("\033[35m\nfail_insert_function topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert_mission(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new mission."""
        pub.subscribe(self.on_succeed_insert_mission,
                      'succeed_insert_usage_profile')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_mission()

        assert isinstance(
            DUT.tree.get_node('3').data['usage_profile'], RAMSTKMission)

        pub.unsubscribe(self.on_succeed_insert_mission,
                        'succeed_insert_usage_profile')

    @pytest.mark.unit
    def test_do_insert_mission_no_revision(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new mission."""
        pub.subscribe(self.on_fail_insert_mission,
                      'fail_insert_usage_profile')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._revision_id = 4
        DUT._do_insert_mission()

        pub.unsubscribe(self.on_fail_insert_mission,
                        'fail_insert_usage_profile')

    @pytest.mark.unit
    def test_do_insert_mission_phase(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new mission phase."""
        pub.subscribe(self.on_succeed_insert_mission_phase,
                      'succeed_insert_mission_phase')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_mission_phase(1)

        assert isinstance(DUT.tree, Tree)
        assert isinstance(
            DUT.tree.get_node('1.4').data['usage_profile'], RAMSTKMissionPhase)

        pub.unsubscribe(self.on_succeed_insert_mission_phase,
                        'succeed_insert_mission_phase')

    @pytest.mark.unit
    def test_do_insert_mission_phase_no_mission(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new mission phase."""
        pub.subscribe(self.on_fail_insert_mission_phase,
                      'fail_insert_mission_phase')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_mission_phase(mission_id=40)

        pub.unsubscribe(self.on_fail_insert_mission_phase,
                        'fail_insert_mission_phase')

    @pytest.mark.unit
    def test_do_insert_environment(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new environment."""
        pub.subscribe(self.on_succeed_insert_environment,
                      'succeed_insert_environment')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_environment(1, 1)

        assert isinstance(DUT.tree, Tree)
        assert isinstance(
            DUT.tree.get_node('1.1.4').data['usage_profile'],
            RAMSTKEnvironment)

        pub.unsubscribe(self.on_succeed_insert_environment,
                        'succeed_insert_environment')

    @pytest.mark.unit
    def test_do_insert_environment(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new environment."""
        pub.subscribe(self.on_fail_insert_environment,
                      'fail_insert_environment')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_environment(mission_id=1, phase_id=40)

        pub.unsubscribe(self.on_fail_insert_environment,
                        'fail_insert_environment')


@pytest.mark.usefixtures('test_program_dao')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_usage_profile(self, node_id):
        assert node_id == '1'
        print("\033[36m\nsucceed_update_usage_profile topic was broadcast")

    def on_fail_update_usage_profile(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent usage profile ID 1.10.')
        print("\033[35m\nfail_update_usage_profile topic was broadcast")

    def on_fail_update_usage_profile_no_data_package(self, error_message):
        assert error_message == (
            'do_update: No data package found for usage profile ID 1.1.')
        print("\033[35m\nfail_update_usage_profile topic was broadcast")

    def on_fail_update_usage_profile_root_node(self, error_message):
        assert error_message == (
            'do_update: No data package found for usage profile ID 0.')
        print("\033[35m\nfail_update_usage_profile topic was broadcast")

    @pytest.mark.integration
    def test_do_update_usage_profile(self, test_program_dao):
        """do_update_usage_profile() should broadcast the succeed message on
        success."""
        pub.subscribe(self.on_succeed_update_usage_profile,
                      'succeed_update_usage_profile')

        DUT = dmUsageProfile()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _mission = DUT.do_select('1', table='usage_profile')
        _mission.description = 'Big ole mission'

        DUT.do_update('1')
        _mission = DUT.do_select('1', table='usage_profile')

        assert _mission.description == 'Big ole mission'

        pub.unsubscribe(self.on_succeed_update_usage_profile,
                        'succeed_update_usage_profile')

    @pytest.mark.unit
    def test_do_update_usage_profile_non_existent_id(self, mock_program_dao):
        """do_update_usage_profile() should broadcast the fail message when
        attempting to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_usage_profile,
                      'fail_update_usage_profile')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_update('1.10')

        pub.unsubscribe(self.on_fail_update_usage_profile,
                        'fail_update_usage_profile')

    @pytest.mark.unit
    def test_do_update_usage_profile_no_data_package(self, mock_program_dao):
        """do_update_usage_profile() should broadcast the fail message when
        attempting to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_usage_profile_no_data_package,
                      'fail_update_usage_profile')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node('1.1').data.pop('usage_profile')
        DUT.do_update('1.1')

        pub.unsubscribe(self.on_fail_update_usage_profile_no_data_package,
                        'fail_update_usage_profile')

    @pytest.mark.unit
    def test_do_update_usage_profile_root_node(self, mock_program_dao):
        """do_update_usage_profile() should broadcast the fail message when
        attempting to save the root node."""
        pub.subscribe(self.on_fail_update_usage_profile_root_node,
                      'fail_update_usage_profile')

        DUT = dmUsageProfile()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_update(0)

        pub.unsubscribe(self.on_fail_update_usage_profile_root_node,
                        'fail_update_usage_profile')

    @pytest.mark.integration
    def test_do_update_all_usage_profile(self, test_program_dao):
        """do_update_usage_profile() should broadcast the succeed message on
        success."""
        DUT = dmUsageProfile()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_update_all_usage_profiles')
