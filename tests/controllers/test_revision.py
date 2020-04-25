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
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from __mocks__ import (
    MOCK_ENVIRONMENTS, MOCK_FAILURE_DEFINITIONS,
    MOCK_MISSION_PHASES, MOCK_MISSIONS, MOCK_REVISIONS
)
from ramstk.controllers import dmRevision
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import (
    RAMSTKEnvironment, RAMSTKFailureDefinition,
    RAMSTKMission, RAMSTKMissionPhase, RAMSTKRevision
)


class MockDao:
    _all_revisions = []
    _all_failure_definitions = []
    _all_missions = []
    _all_mission_phases = []
    _all_environments = []

    def _do_delete_revision(self, record):
        for _idx, _revision in enumerate(self._all_revisions):
            if _revision.revision_id == record.revision_id:
                self._all_revisions.pop(_idx)

    def _do_delete_failure_definition(self, record):
        for _idx, _record in enumerate(self._all_failure_definitions):
            if _record.definition_id == record.definition_id:
                self._all_failure_definitions.pop(_idx)

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
        if record == RAMSTKRevision:
            try:
                self._do_delete_revision(record)
            except AttributeError:
                raise DataAccessError('')
        elif record == RAMSTKFailureDefinition:
            self._do_delete_failure_definition(record)
        elif record == RAMSTKMission:
            self._do_delete_mission(record)
        elif record == RAMSTKMissionPhase:
            self._do_delete_mission_phases(record)
        elif record == RAMSTKEnvironment:
            self._do_delete_environments(record)

    def do_insert(self, record):
        if record == RAMSTKRevision:
            self._all_revisions.append(record)
        elif record == RAMSTKFailureDefinition:
            self._all_failure_definitions.append(record)
        elif record == RAMSTKMission:
            self._all_missions.append(record)
        elif record == RAMSTKMissionPhase:
            self._all_mission_phases.append(record)
        elif record == RAMSTKEnvironment:
            self._all_environments.append(record)

    def _do_select_all_revisions(self, table):
        self._all_revisions = []
        for _key in MOCK_REVISIONS:
            _record = table()
            _record.revision_id = _key
            _record.set_attributes(MOCK_REVISIONS[_key])
            self._all_revisions.append(_record)

        return self._all_revisions

    def _do_select_all_failure_definitions(self, table, value):
        _idx = 1
        self._all_failure_definitions = []
        for _key in MOCK_FAILURE_DEFINITIONS:
            _record = table()
            _record.revision_id = value
            _record.definition_id = _idx
            _record.set_attributes(MOCK_FAILURE_DEFINITIONS[_key])
            self._all_failure_definitions.append(_record)
            _idx += 1

        return self._all_failure_definitions

    def _do_select_all_missions(self, table, value):
        _idx = 1
        self._all_missions = []
        for _key in MOCK_MISSIONS:
            _record = table()
            _record.revision_id = value
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

    def do_select_all(self, table, key, value, order=None,
                      _all=False):
        if table == RAMSTKRevision:
            return self._do_select_all_revisions(table)
        elif table == RAMSTKFailureDefinition:
            return self._do_select_all_failure_definitions(table, value)
        elif table == RAMSTKMission:
            return self._do_select_all_missions(table, value)
        elif table == RAMSTKMissionPhase:
            for _mission in self._all_missions:
                return self._do_select_all_mission_phases(
                    table, _mission.mission_id)
        elif table == RAMSTKEnvironment:
            for _phase in self._all_mission_phases:
                return self._do_select_all_environments(table, _phase.phase_id)

    def do_update(self, record):
        for _key in MOCK_REVISIONS:
            if _key == record.revision_id:
                MOCK_REVISIONS[_key]['name'] = record.name

    def get_last_id(self, table, id_column):
        if table == 'ramstk_revision':
            return max(MOCK_REVISIONS.keys())
        elif table == 'ramstk_environment':
            return max(MOCK_ENVIRONMENTS.keys())
        elif table == 'ramstk_failure_definition':
            return max(MOCK_FAILURE_DEFINITIONS.keys())
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
        DUT = dmRevision()

        assert isinstance(DUT, dmRevision)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'revision'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all,
                                'request_retrieve_revisions')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_revision')
        assert pub.isSubscribed(DUT._do_delete_failure_definition,
                                'request_delete_failure_definition')
        assert pub.isSubscribed(DUT._do_delete_mission,
                                'request_delete_mission')
        assert pub.isSubscribed(DUT._do_delete_mission_phase,
                                'request_delete_mission_phase')
        assert pub.isSubscribed(DUT._do_delete_environment,
                                'request_delete_environment')
        assert pub.isSubscribed(DUT.do_insert, 'request_insert_revision')
        assert pub.isSubscribed(DUT.do_insert_mission,
                                'request_insert_mission')
        assert pub.isSubscribed(DUT.do_insert_mission_phase,
                                'request_insert_mission_phase')
        assert pub.isSubscribed(DUT.do_insert_environment,
                                'request_insert_environment')
        assert pub.isSubscribed(DUT.do_update, 'request_update_revision')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_revisions')
        assert pub.isSubscribed(DUT._do_get_attributes,
                                'request_get_revision_attributes')
        assert pub.isSubscribed(DUT.do_get_all_attributes,
                                'request_get_all_revision_attributes')
        assert pub.isSubscribed(DUT.do_get_tree, 'request_get_revision_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_revision_attributes')
        assert pub.isSubscribed(DUT.do_set_all_attributes,
                                'request_set_all_revision_attributes')


class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with RAMSTKRevision instances on success."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        assert isinstance(DUT.tree, Tree)
        assert isinstance(
            DUT.tree.get_node(1).data['revision'], RAMSTKRevision)
        assert isinstance(
            DUT.tree.get_node(1).data['failure_definitions'], dict)
        assert isinstance(
            DUT.tree.get_node(1).data['failure_definitions'][1],
            RAMSTKFailureDefinition)
        assert isinstance(DUT.tree.get_node(1).data['usage_profile'], Tree)

    @pytest.mark.unit
    def test_do_select_revision(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKRevision on success."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        _revision = DUT.do_select(1, table='revision')

        assert isinstance(_revision, RAMSTKRevision)
        assert _revision.availability_logistics == 0.9986
        assert _revision.name == 'Original Revision'

    @pytest.mark.unit
    def test_do_select_failure_definition(self, mock_program_dao):
        """do_select() should return an instance of RAMSTKFailureDefinition on success."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        _failure_definition = DUT.do_select(1, table='failure_definitions')

        assert isinstance(_failure_definition, dict)
        assert isinstance(_failure_definition[1], RAMSTKFailureDefinition)
        assert _failure_definition[1].definition == 'Failure Definition'

    @pytest.mark.unit
    def test_do_select_usage_profile(self, mock_program_dao):
        """do_select() should return the usage profile treelib Tree() on success."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        _usage_profile = DUT.do_select(1, table='usage_profile')

        assert isinstance(_usage_profile, Tree)
        assert isinstance(_usage_profile.get_node('1').data, RAMSTKMission)
        assert isinstance(
            _usage_profile.get_node('1.1').data, RAMSTKMissionPhase)
        assert isinstance(
            _usage_profile.get_node('1.1.1').data, RAMSTKEnvironment)

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is requested."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Revision ID is requested."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        assert DUT.do_select(100, table='revision') is None


class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_revision(self, node_id, tree):
        assert node_id == 2
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_revision topic was broadcast.")

    def on_fail_delete_revision(self, error_message):
        assert error_message == (
            'Attempted to delete non-existent revision ID 300.')
        print("\033[35m\nfail_delete_revision topic was broadcast.")

    def on_succeed_delete_failure_definition(self, tree):
        assert isinstance(tree, dict)
        assert isinstance(tree[1], RAMSTKFailureDefinition)
        print(
            "\033[36m\nsucceed_delete_failure_definition topic was broadcast.")

    def on_fail_delete_failure_definition(self, error_message):
        assert error_message == ('Attempted to delete non-existent failure '
                                 'definition ID 10 from revision ID 1.')
        print("\033[35m\nfail_delete_failure_definition topic was broadcast.")

    def on_succeed_delete_mission(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_mission topic was broadcast.")

    def on_fail_delete_mission(self, error_message):
        assert error_message == ('Attempted to delete non-existent mission ID '
                                 '10 from revision ID 1.')
        print("\033[35m\nfail_delete_mission topic was broadcast.")

    def on_succeed_delete_mission_phase(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_mission_phase topic was broadcast.")

    def on_fail_delete_mission_phase(self, error_message):
        assert error_message == (
            'Attempted to delete non-existent mission phase '
            'ID 2.20 from mission ID 2.')
        print("\033[35m\nfail_delete_mission_phase topic was broadcast.")

    def on_succeed_delete_environment(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_environment topic was broadcast.")

    def on_fail_delete_environment(self, error_message):
        assert error_message == (
            'Attempted to delete non-existent environment ID '
            '3.3.30 from mission phase ID 3.3.')
        print("\033[35m\nfail_delete_environment topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete_revision(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib Tree."""
        pub.subscribe(self.on_succeed_delete_revision,
                      'succeed_delete_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_delete(DUT.last_id)

        assert DUT.last_id == 1

        pub.unsubscribe(self.on_succeed_delete_revision,
                        'succeed_delete_revision')

    @pytest.mark.unit
    def test_do_delete_revision_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to delete a non-existent revision."""
        pub.subscribe(self.on_fail_delete_revision, 'fail_delete_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_revision, 'fail_delete_revision')

    @pytest.mark.unit
    def test_do_delete_failure_definition(self, mock_program_dao):
        """_do_delete_failure_definition() should send the success message after successfully deleting a definition."""
        pub.subscribe(self.on_succeed_delete_failure_definition,
                      'succeed_delete_failure_definition')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_delete_failure_definition(1, 1)

        with pytest.raises(KeyError):
            __ = DUT.tree.get_node(1).data['failure_definitions'][1]

        pub.unsubscribe(self.on_succeed_delete_failure_definition,
                        'succeed_delete_failure_definition')

    @pytest.mark.unit
    def test_do_delete_failure_definition_non_existent_id(
            self, mock_program_dao):
        """_do_delete_failure_definition() should send the fail message when attempting to delete a non-existent failure definition."""
        pub.subscribe(self.on_fail_delete_failure_definition,
                      'fail_delete_failure_definition')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_delete_failure_definition(1, 10)

        pub.unsubscribe(self.on_fail_delete_failure_definition,
                        'fail_delete_failure_definition')

    @pytest.mark.unit
    def test_do_delete_mission(self, mock_program_dao):
        """_do_delete_mission() should send the success message after successfully deleting a mission."""
        pub.subscribe(self.on_succeed_delete_mission, 'succeed_delete_mission')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_delete_mission(1, '1')

        assert not DUT.tree.get_node(1).data['usage_profile'].contains('1')
        assert not DUT.tree.get_node(1).data['usage_profile'].contains('1.1')
        assert not DUT.tree.get_node(1).data['usage_profile'].contains('1.1.1')

        pub.unsubscribe(self.on_succeed_delete_mission,
                        'succeed_delete_mission')

    @pytest.mark.unit
    def test_do_delete_mission_non_existent_id(self, mock_program_dao):
        """_do_delete_mission() should send the sfail message when attempting to delete a non-existent mission ID."""
        pub.subscribe(self.on_fail_delete_mission, 'fail_delete_mission')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_delete_mission(1, '10')

        pub.unsubscribe(self.on_fail_delete_mission, 'fail_delete_mission')

    @pytest.mark.unit
    def test_do_delete_mission_phase(self, mock_program_dao):
        """_do_delete_mission_phase() should send the success message after successfully deleting a mission phase."""
        pub.subscribe(self.on_succeed_delete_mission_phase,
                      'succeed_delete_mission_phase')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_delete_mission_phase(1, '2', '2.2')

        assert not DUT.tree.get_node(1).data['usage_profile'].contains('2.2')
        assert not DUT.tree.get_node(1).data['usage_profile'].contains('2.2.2')

        pub.unsubscribe(self.on_succeed_delete_mission_phase,
                        'succeed_delete_mission_phase')

    @pytest.mark.unit
    def test_do_delete_mission_phase_non_existent_id(self, mock_program_dao):
        """_do_delete_mission_phase() should send the fail message when attempting to delete a non-existent mission phase."""
        pub.subscribe(self.on_fail_delete_mission_phase,
                      'fail_delete_mission_phase')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_delete_mission_phase(1, '2', '2.20')

        pub.unsubscribe(self.on_fail_delete_mission_phase,
                        'fail_delete_mission_phase')

    @pytest.mark.unit
    def test_do_delete_environment(self, mock_program_dao):
        """_do_delete_environment() should send the success message after successfully deleting an environment."""
        pub.subscribe(self.on_succeed_delete_environment,
                      'succeed_delete_environment')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_delete_environment(1, '3.3', '3.3.3')

        assert not DUT.tree.get_node(1).data['usage_profile'].contains('3.3.3')

        pub.unsubscribe(self.on_succeed_delete_environment,
                        'succeed_delete_environment')

    @pytest.mark.unit
    def test_do_delete_environment_non_existent_id(self, mock_program_dao):
        """_do_delete_environment() should send the fail message when attempting to delete a non-existent environment."""
        pub.subscribe(self.on_fail_delete_environment,
                      'fail_delete_environment')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_delete_environment(1, '3.3', '3.3.30')

        pub.unsubscribe(self.on_fail_delete_environment,
                        'fail_delete_environment')


class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_revision_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['revision_id'] == 1
        assert attributes['name'] == 'Original Revision'
        assert attributes['program_time'] == 2562
        print("\033[36m\nsucceed_get_revision_attributes topic was broadcast")

    def on_succeed_get_failure_definition_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes[1].revision_id == 1
        assert attributes[1].definition == 'Failure Definition'
        print(
            "\033[36m\nsucceed_get_failure_definitions_attributes topic was broadcast"
        )

    def on_succeed_get_usage_profile_attrs(self, attributes):
        assert isinstance(attributes, Tree)
        assert attributes.get_node('1').data.revision_id == 1
        assert attributes.get_node('1').data.time_units == 'hours'
        assert attributes.get_node('2.2').data.description == ('Phase #1 for '
                                                               'mission #2')
        assert attributes.get_node('1.1.1').data.name == 'Condition Name'
        print(
            "\033[36m\nsucceed_get_usage_profile_attributes topic was broadcast"
        )

    def on_succeed_get_all_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['revision_id'] == 1
        assert attributes['name'] == 'Original Revision'
        assert attributes['program_time'] == 2562
        assert isinstance(attributes['failure_definitions'], dict)
        assert isinstance(attributes['failure_definitions'][1],
                          RAMSTKFailureDefinition)
        assert attributes['failure_definitions'][1].revision_id == 1
        assert isinstance(attributes['usage_profile'], Tree)
        assert attributes['usage_profile'].get_node('1').data.revision_id == 1
        print(
            "\033[36m\nsucceed_get_all_revision_attributes topic was broadcast"
        )

    def on_succeed_get_revision_tree(self, dmtree):
        assert isinstance(dmtree, Tree)
        assert isinstance(dmtree.get_node(1).data['revision'], RAMSTKRevision)
        assert isinstance(dmtree.get_node(1).data['failure_definitions'], dict)
        assert isinstance(
            dmtree.get_node(1).data['failure_definitions'][1],
            RAMSTKFailureDefinition)
        assert isinstance(
            dmtree.get_node(1).data['usage_profile'].get_node('1').data,
            RAMSTKMission)
        assert isinstance(
            dmtree.get_node(1).data['usage_profile'].get_node('1.1').data,
            RAMSTKMissionPhase)
        assert isinstance(
            dmtree.get_node(1).data['usage_profile'].get_node('1.1.1').data,
            RAMSTKEnvironment)
        print("\033[36m\nsucceed_get_revision_tree topic was broadcast")

    def on_succeed_get_last_id(self, last_id):
        assert last_id == 2
        print("\033[36m\nsucceed_get_last_id topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes_revision(self, mock_program_dao):
        """_do_get_attributes() should return a dict of revision attributes on success."""
        pub.subscribe(self.on_succeed_get_revision_attrs,
                      'succeed_get_revision_attributes')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_get_attributes(1, 'revision')

        pub.unsubscribe(self.on_succeed_get_revision_attrs,
                        'succeed_get_revision_attributes')

    @pytest.mark.unit
    def test_do_get_attributes_failure_definitions(self, mock_program_dao):
        """_do_get_attributes() should return a dict of failure definition records on success."""
        pub.subscribe(self.on_succeed_get_failure_definition_attrs,
                      'succeed_get_failure_definitions_attributes')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_get_attributes(1, 'failure_definitions')

        pub.unsubscribe(self.on_succeed_get_failure_definition_attrs,
                        'succeed_get_failure_definitions_attributes')

    @pytest.mark.unit
    def test_do_get_attributes_usage_profile(self, mock_program_dao):
        """_do_get_attributes() should return treelib Tree() on success."""
        pub.subscribe(self.on_succeed_get_usage_profile_attrs,
                      'succeed_get_usage_profile_attributes')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_get_attributes(1, 'usage_profile')

        pub.unsubscribe(self.on_succeed_get_usage_profile_attrs,
                        'succeed_get_usage_profile_attributes')

    @pytest.mark.unit
    def test_do_get_all_attributes_data_manager(self, mock_program_dao):
        """do_get_all_attributes() should return a dict of all RAMSTK data tables' attributes on success."""
        pub.subscribe(self.on_succeed_get_all_attrs,
                      'succeed_get_all_revision_attributes')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.do_get_all_attributes(1)

        pub.unsubscribe(self.on_succeed_get_all_attrs,
                        'succeed_get_all_revision_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        pub.sendMessage('request_set_revision_attributes',
                        node_id=[1, -1, ''],
                        package={'revision_code': '-'})
        pub.sendMessage('request_set_revision_attributes',
                        node_id=[1, 1, ''],
                        package={'definition': 'Test Description'})
        pub.sendMessage(
            'request_set_revision_attributes',
            node_id=[1, -1, '1'],
            package={'description': 'This is the mission description.'})
        pub.sendMessage('request_set_revision_attributes',
                        node_id=[1, -1, '1.1'],
                        package={'phase_end': 5.12})
        pub.sendMessage('request_set_revision_attributes',
                        node_id=[1, -1, '1.1.1'],
                        package={'minimum': 5.12})
        assert DUT.do_select(1, table='revision').revision_code == '-'
        assert DUT.do_select(
            1,
            table='failure_definitions')[1].definition == 'Test Description'
        assert DUT.do_select(
            1, table='usage_profile').get_node('1').data.description == (
                'This is the mission description.')
        assert DUT.do_select(
            1, table='usage_profile').get_node('1.1').data.phase_end == 5.12
        assert DUT.do_select(
            1, table='usage_profile').get_node('1.1.1').data.minimum == 5.12

    @pytest.mark.unit
    def test_do_set_all_attributes(self, mock_program_dao):
        """do_set_all_attributes() should send the success message."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        pub.sendMessage('request_set_all_revision_attributes',
                        attributes={
                            'revision_id': 1,
                            'revision_code': '1',
                            'remarks': 'These are remarks added by a test.',
                            'total_part_count': 28,
                            'definition': 'Failure Definition',
                            'phase_end': 0.0
                        },
                        definition_id=1,
                        usage_id='1.1')
        assert DUT.do_select(1, table='revision').revision_code == '1'
        assert DUT.do_select(
            1,
            table='revision').remarks == 'These are remarks added by a test.'
        assert DUT.do_select(1, table='revision').total_part_count == 28
        assert DUT.do_select(
            1,
            table='failure_definitions')[1].definition == 'Failure Definition'
        assert DUT.do_select(
            1, table='usage_profile').get_node('1.1').data.phase_end == 0.0

    @pytest.mark.unit
    def test_on_get_tree(self, mock_program_dao):
        """on_get_tree() should return the revision treelib Tree."""
        pub.subscribe(self.on_succeed_get_revision_tree,
                      'succeed_get_revision_tree')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_revision_tree,
                        'succeed_get_revision_tree')

    @pytest.mark.unit
    def test_do_get_last_id(self, mock_program_dao):
        """do_get_last_id() should broadcast the success message with the last ID aste payload."""
        pub.subscribe(self.on_succeed_get_last_id,
                      'succeed_get_last_revision_id')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.do_get_last_id('revision')

        pub.unsubscribe(self.on_succeed_get_last_id,
                        'succeed_get_last_revision_id')


class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_revision(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_revision topic was broadcast")

    def on_succeed_insert_failure_definition(self, tree):
        assert isinstance(tree, dict)
        assert isinstance(tree[2], RAMSTKFailureDefinition)
        print(
            "\033[36m\nsucceed_insert_failure_definition topic was broadcast")

    def on_succeed_insert_mission(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_mission topic was broadcast")

    def on_succeed_insert_mission_phase(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_mission_phase topic was broadcast")

    def on_succeed_insert_environment(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_environment topic was broadcast")

    @pytest.mark.unit
    def test_do_insert(self, mock_program_dao):
        """do_insert() should send the success message after successfully inserting a new revision."""
        pub.subscribe(self.on_succeed_insert_revision,
                      'succeed_insert_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.do_insert()

        assert isinstance(
            DUT.tree.get_node(3).data['revision'], RAMSTKRevision)
        assert DUT.tree.get_node(3).data['revision'].revision_id == 3
        assert DUT.tree.get_node(3).data['revision'].name == 'New Revision'
        assert isinstance(
            DUT.tree.get_node(3).data['failure_definitions'], dict)
        assert isinstance(DUT.tree.get_node(3).data['usage_profile'], Tree)

        pub.unsubscribe(self.on_succeed_insert_revision,
                        'succeed_insert_revision')

    @pytest.mark.unit
    def test_do_insert_failure_definition(self, mock_program_dao):
        """do_insert() should send the success message after successfully inserting a new failure definition."""
        pub.subscribe(self.on_succeed_insert_failure_definition,
                      'succeed_insert_failure_definition')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.do_insert_failure_definition(1)

        assert isinstance(
            DUT.tree.get_node(1).data['failure_definitions'], dict)
        assert isinstance(
            DUT.tree.get_node(1).data['failure_definitions'][2],
            RAMSTKFailureDefinition)

        pub.unsubscribe(self.on_succeed_insert_failure_definition,
                        'succeed_insert_failure_definition')

    @pytest.mark.unit
    def test_do_insert_mission(self, mock_program_dao):
        """do_insert() should send the success message after successfully inserting a new mission."""
        pub.subscribe(self.on_succeed_insert_mission, 'succeed_insert_mission')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.do_insert_mission(1)

        assert isinstance(DUT.tree.get_node(1).data['usage_profile'], Tree)
        assert isinstance(
            DUT.tree.get_node(1).data['usage_profile'].get_node('3').data,
            RAMSTKMission)

        pub.unsubscribe(self.on_succeed_insert_mission,
                        'succeed_insert_mission')

    @pytest.mark.unit
    def test_do_insert_mission_phase(self, mock_program_dao):
        """do_insert() should send the success message after successfully inserting a new mission phase."""
        pub.subscribe(self.on_succeed_insert_mission_phase,
                      'succeed_insert_mission_phase')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.do_insert_mission_phase(1, 1)

        assert isinstance(DUT.tree.get_node(1).data['usage_profile'], Tree)
        assert isinstance(
            DUT.tree.get_node(1).data['usage_profile'].get_node(
                str('1.4')).data, RAMSTKMissionPhase)
        pub.unsubscribe(self.on_succeed_insert_mission_phase,
                        'succeed_insert_mission_phase')

    @pytest.mark.unit
    def test_do_insert_environment(self, mock_program_dao):
        """do_insert() should send the success message after successfully inserting a new environment."""
        pub.subscribe(self.on_succeed_insert_environment,
                      'succeed_insert_environment')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.do_insert_environment(1, 1, 1)

        assert isinstance(DUT.tree.get_node(1).data['usage_profile'], Tree)
        assert isinstance(
            DUT.tree.get_node(1).data['usage_profile'].get_node(
                str('1.1.4')).data, RAMSTKEnvironment)

        pub.unsubscribe(self.on_succeed_insert_environment,
                        'succeed_insert_environment')


@pytest.mark.usefixtures('test_program_dao')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_revision(self, node_id):
        assert node_id == 1
        print("\033[36m\nsucceed_update_revision topic was broadcast")

    def on_fail_update_revision(self, error_message):
        assert error_message == (
            'Attempted to save non-existent revision with revision ID 100.')
        print("\033[35m\nfail_update_revision topic was broadcast")

    def on_fail_update_revision_no_data_package(self, error_message):
        assert error_message == (
            'No data package found for revision ID 1.')
        print("\033[35m\nfail_update_revision topic was broadcast")

    def on_succeed_update_failure_definition(self, node_id):
        assert node_id == 1
        print(
            "\033[36m\nsucceed_update_failure_definition topic was broadcast")

    def on_fail_update_failure_definition(self, error_message):
        assert error_message == (
            'No data package found for failure definition ID 100.')
        print("\033[35m\nfail_update_failure_definition topic was broadcast")

    def on_fail_update_failure_definition_no_revision(self, error_message):
        assert error_message == (
            'No revision ID 10 found when attempting to save failure '
            'definition with ID 1.')
        print("\033[35m\nfail_update_failure_definition topic was broadcast")

    def on_succeed_update_usage_profile(self, node_id):
        assert node_id == '1'
        print("\033[36m\nsucceed_update_usage_profile topic was broadcast")

    def on_fail_update_usage_profile(self, error_message):
        assert error_message == (
            'Attempted to save non-existent usage profile element with ID 1.10.'
        )
        print("\033[35m\nfail_update_usage_profile topic was broadcast")

    def on_fail_update_usage_profile_no_data_package(self, error_message):
        assert error_message == (
            'No data package found for usage profile ID 1.1.'
        )
        print("\033[35m\nfail_update_usage_profile topic was broadcast")

    @pytest.mark.integration
    def test_do_update_data_manager(self, test_program_dao):
        """ do_update() should return a zero error code on success. """
        pub.subscribe(self.on_succeed_update_revision,
                      'succeed_update_revision')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        _revision = DUT.do_select(1, table='revision')
        _revision.name = 'Test Revision'
        _failure_definition = DUT.do_select(1, table='failure_definitions')
        _failure_definition[1].definition = 'Failure Definition'
        _usage_profile = DUT.do_select(1, table='usage_profile')
        _usage_profile.get_node('1.1').data.phase_end = 0.0
        DUT.do_update(1)

        DUT.do_select_all()
        _revision = DUT.do_select(1, table='revision')

        assert _revision.name == 'Test Revision'
        _failure_definition = DUT.do_select(1, table='failure_definitions')
        assert _failure_definition[1].definition == 'Failure Definition'
        _usage_profile = DUT.do_select(1, table='usage_profile')
        assert _usage_profile.get_node('1.1').data.phase_end == 0.0

        pub.unsubscribe(self.on_succeed_update_revision,
                        'succeed_update_revision')

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """ do_update() should return a non-zero error code when passed a Revision ID that doesn't exist. """
        pub.subscribe(self.on_fail_update_revision, 'fail_update_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.do_update(100)

        pub.unsubscribe(self.on_fail_update_revision, 'fail_update_revision')

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """ do_update() should raise the 'fail_update_validation' message when passed a Validation ID that doesn't exist in the tree. """
        pub.subscribe(self.on_fail_update_revision_no_data_package,
                      'fail_update_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        DUT.tree.get_node(1).data.pop('revision')

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_revision_no_data_package,
                        'fail_update_revision')

    @pytest.mark.integration
    def test_do_update_failure_definition(self, test_program_dao):
        """do_update_failure_definition() should broadcast the succeed message on success."""
        pub.subscribe(self.on_succeed_update_failure_definition,
                      'succeed_update_failure_definition')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        _failure_definition = DUT.do_select(1, table='failure_definitions')
        _failure_definition[1].definition = 'Big test definition'

        DUT._do_update_failure_definition(1, 1)
        _failure_definition = DUT.do_select(1, table='failure_definitions')

        assert _failure_definition[1].definition == 'Big test definition'

        pub.unsubscribe(self.on_succeed_update_failure_definition,
                        'succeed_update_failure_definition')

    @pytest.mark.unit
    def test_do_update_failure_definition_non_existent_id(
            self, mock_program_dao):
        """do_update_failure_definition() should broadcast the fail message when attempting to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_failure_definition,
                      'fail_update_failure_definition')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_update_failure_definition(1, 100)

        pub.unsubscribe(self.on_fail_update_failure_definition,
                        'fail_update_failure_definition')

    @pytest.mark.unit
    def test_do_update_failure_definition_non_existent_revision(
            self, mock_program_dao):
        """do_update_failure_definition() should broadcast the fail message when attempting to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_failure_definition_no_revision,
                      'fail_update_failure_definition')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_update_failure_definition(10, 1)

        pub.unsubscribe(self.on_fail_update_failure_definition_no_revision,
                        'fail_update_failure_definition')

    @pytest.mark.integration
    def test_do_update_all_failure_definition(self, test_program_dao):
        """do_update_all failure_definition() should return None on success."""
        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        _failure_definition = DUT.do_select(1, table='failure_definitions')
        _failure_definition[1].definition = 'Big test definition #1'
        _failure_definition[2].definition = 'Big test definition #2'

        assert DUT._do_update_all_failure_definition(1) is None

        _failure_definition = DUT.do_select(1, table='failure_definitions')
        assert _failure_definition[1].definition == 'Big test definition #1'

        _failure_definition = DUT.do_select(1, table='failure_definitions')
        assert _failure_definition[2].definition == 'Big test definition #2'

    @pytest.mark.integration
    def test_do_update_usage_profile(self, test_program_dao):
        """do_update_usage_profile() should broadcast the succeed message on success."""
        pub.subscribe(self.on_succeed_update_usage_profile,
                      'succeed_update_usage_profile')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        _mission = DUT.do_select(1, table='usage_profile').get_node('1').data
        _mission.description = 'Big ole mission'

        DUT._do_update_usage_profile(1, '1')
        _mission = DUT.do_select(1, table='usage_profile').get_node('1').data

        assert _mission.description == 'Big ole mission'

        pub.unsubscribe(self.on_succeed_update_usage_profile,
                        'succeed_update_usage_profile')

    @pytest.mark.unit
    def test_do_update_usage_profile_non_existent_id(self, mock_program_dao):
        """do_update_usage_profile() should broadcast the fail message when attempting to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_usage_profile,
                      'fail_update_usage_profile')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_update_usage_profile(1, '1.10')

        pub.unsubscribe(self.on_fail_update_usage_profile,
                        'fail_update_usage_profile')

    @pytest.mark.unit
    def test_do_update_usage_profile_no_data_package(self, mock_program_dao):
        """do_update_usage_profile() should broadcast the fail message when attempting to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_usage_profile_no_data_package,
                      'fail_update_usage_profile')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.tree.get_node(1).data.pop('usage_profile')
        DUT._do_update_usage_profile(1, '1.1')

        pub.unsubscribe(self.on_fail_update_usage_profile_no_data_package,
                        'fail_update_usage_profile')

    @pytest.mark.integration
    def test_do_update_all_usage_profile(self, test_program_dao):
        """do_update_usage_profile() should broadcast the succeed message on success."""
        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        pub.sendMessage('request_update_all_usage_profiles', revision_id=1)
