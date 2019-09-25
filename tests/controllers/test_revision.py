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
from ramstk.controllers import dmRevision
from ramstk.models.programdb import (
    RAMSTKEnvironment, RAMSTKFailureDefinition,
    RAMSTKMission, RAMSTKMissionPhase, RAMSTKRevision
)

ATTRIBUTES = {
    'revision_id': 1,
    'availability_logistics': 0.9986,
    'availability_mission': 0.99934,
    'cost': 12532.15,
    'cost_per_failure': 0.0000352,
    'cost_per_hour': 1.2532,
    'hazard_rate_active': 0.0,
    'hazard_rate_dormant': 0.0,
    'hazard_rate_logistics': 0.0,
    'hazard_rate_mission': 0.0,
    'hazard_rate_software': 0.0,
    'mmt': 0.0,
    'mcmt': 0.0,
    'mpmt': 0.0,
    'mtbf_logistics': 0.0,
    'mtbf_mission': 0.0,
    'mttr': 0.0,
    'name': 'Original Revision',
    'reliability_logistics': 0.99986,
    'reliability_mission': 0.99992,
    'remarks': b'This is the original revision.',
    'n_parts': 128,
    'revision_code': 'Rev. -',
    'program_time': 2562,
    'program_time_sd': 26.83,
    'program_cost': 26492.83,
    'program_cost_sd': 15.62,
}


@pytest.mark.usefixtures('test_program_dao')
class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager(self):
        """__init__() should return a Revision data manager."""
        DUT = dmRevision()

        assert isinstance(DUT, dmRevision)
        assert isinstance(DUT.tree, Tree)
        assert DUT.dao is None
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


@pytest.mark.usefixtures('test_program_dao')
class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    @pytest.mark.integration
    def test_do_select_all(self, test_program_dao):
        """do_select_all() should return a Tree() object populated with RAMSTKRevision instances on success."""
        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
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

    @pytest.mark.integration
    def test_do_select_revision(self, test_program_dao):
        """do_select() should return an instance of the RAMSTKRevision on success."""
        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        _revision = DUT.do_select(1, table='revision')

        assert isinstance(_revision, RAMSTKRevision)
        assert _revision.availability_logistics == 1.0
        assert _revision.name == 'Test Revision'

    @pytest.mark.integration
    def test_do_select_failure_definition(self, test_program_dao):
        """do_select() should return an instance of RAMSTKFailureDefinition on success."""
        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        _failure_definition = DUT.do_select(1, table='failure_definitions')

        assert isinstance(_failure_definition, dict)
        assert isinstance(_failure_definition[1], RAMSTKFailureDefinition)
        assert _failure_definition[1].definition == b'Failure Definition'

    @pytest.mark.integration
    def test_do_select_usage_profile(self, test_program_dao):
        """do_select() should return the usage profile treelib Tree() on success."""
        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        _usage_profile = DUT.do_select(1, table='usage_profile')

        assert isinstance(_usage_profile, Tree)
        assert isinstance(_usage_profile.get_node('1').data, RAMSTKMission)
        assert isinstance(
            _usage_profile.get_node('1.1').data, RAMSTKMissionPhase)
        assert isinstance(
            _usage_profile.get_node('1.1.1').data, RAMSTKEnvironment)

    @pytest.mark.integration
    def test_do_select_unknown_table(self, test_program_dao):
        """do_select() should raise a KeyError when an unknown table name is requested."""
        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.integration
    def test_do_select_non_existent_id(self, test_program_dao):
        """do_select() should return None when a non-existent Revision ID is requested."""
        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        assert DUT.do_select(100, table='revision') is None


@pytest.mark.usefixtures('test_program_dao')
class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_revision(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_revision topic was broadcast.")

    def on_fail_delete_revision(self, error_message):
        assert error_message == (
            'Attempted to delete non-existent revision ID '
            '300.')
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

    @pytest.mark.integration
    def test_do_delete_revision(self, test_program_dao):
        """_do_delete() should send the success message with the treelib Tree."""
        pub.subscribe(self.on_succeed_delete_revision,
                      'succeed_delete_revision')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT._do_delete(DUT.last_id)

        assert DUT.last_id == 1

    @pytest.mark.integration
    def test_do_delete_revision_non_existent_id(self, test_program_dao):
        """_do_delete() should send the fail message when attempting to delete a non-existent revision."""
        pub.subscribe(self.on_fail_delete_revision, 'fail_delete_revision')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT._do_delete(300)

    @pytest.mark.integration
    def test_do_delete_failure_definition(self, test_program_dao):
        """_do_delete_failure_definition() should send the success message after successfully deleting a definition."""
        pub.subscribe(self.on_succeed_delete_failure_definition,
                      'succeed_delete_failure_definition')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT._do_delete_failure_definition(1, 1)

        with pytest.raises(KeyError):
            __ = DUT.tree.get_node(1).data['failure_definitions'][1]

        pub.unsubscribe(self.on_succeed_delete_failure_definition,
                        'succeed_delete_failure_definition')

    @pytest.mark.integration
    def test_do_delete_failure_definition_non_existent_id(
            self, test_program_dao):
        """_do_delete_failure_definition() should send the fail message when attempting to delete a non-existent failure definition."""
        pub.subscribe(self.on_fail_delete_failure_definition,
                      'fail_delete_failure_definition')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT._do_delete_failure_definition(1, 10)

    @pytest.mark.integration
    def test_do_delete_mission(self, test_program_dao):
        """_do_delete_mission() should send the success message after successfully deleting a mission."""
        pub.subscribe(self.on_succeed_delete_mission, 'succeed_delete_mission')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT._do_delete_mission(1, '1')

        assert not DUT.tree.get_node(1).data['usage_profile'].contains('1')
        assert not DUT.tree.get_node(1).data['usage_profile'].contains('1.1')
        assert not DUT.tree.get_node(1).data['usage_profile'].contains('1.1.1')

    @pytest.mark.integration
    def test_do_delete_mission_non_existent_id(self, test_program_dao):
        """_do_delete_mission() should send the sfail message when attempting to delete a non-existent mission ID."""
        pub.subscribe(self.on_fail_delete_mission, 'fail_delete_mission')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT._do_delete_mission(1, '10')

    @pytest.mark.integration
    def test_do_delete_mission_phase(self, test_program_dao):
        """_do_delete_mission_phase() should send the success message after successfully deleting a mission phase."""
        pub.subscribe(self.on_succeed_delete_mission_phase,
                      'succeed_delete_mission_phase')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT._do_delete_mission_phase(1, '2', '2.2')

        assert not DUT.tree.get_node(1).data['usage_profile'].contains('2.2')
        assert not DUT.tree.get_node(1).data['usage_profile'].contains('2.2.2')

    @pytest.mark.integration
    def test_do_delete_mission_phase_non_existent_id(self, test_program_dao):
        """_do_delete_mission_phase() should send the fail message when attempting to delete a non-existent mission phase."""
        pub.subscribe(self.on_fail_delete_mission_phase,
                      'fail_delete_mission_phase')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT._do_delete_mission_phase(1, '2', '2.20')

    @pytest.mark.integration
    def test_do_delete_environment(self, test_program_dao):
        """_do_delete_environment() should send the success message after successfully deleting an environment."""
        pub.subscribe(self.on_succeed_delete_environment,
                      'succeed_delete_environment')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT._do_delete_environment(1, '3.3', '3.3.3')

        assert not DUT.tree.get_node(1).data['usage_profile'].contains('3.3.3')

    @pytest.mark.integration
    def test_do_delete_environment_non_existent_id(self, test_program_dao):
        """_do_delete_environment() should send the fail message when attempting to delete a non-existent environment."""
        pub.subscribe(self.on_fail_delete_environment,
                      'fail_delete_environment')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT._do_delete_environment(1, '3.3', '3.3.30')


@pytest.mark.usefixtures('test_program_dao')
class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_revision_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['revision_id'] == 1
        assert attributes['name'] == 'Test Revision'
        assert attributes['program_time'] == 0.0
        print("\033[36m\nsucceed_get_revision_attributes topic was broadcast")

    def on_succeed_get_failure_definition_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes[1].revision_id == 1
        assert attributes[1].definition == b'Failure Definition'
        print(
            "\033[36m\nsucceed_get_failure_definitions_attributes topic was broadcast"
        )

    def on_succeed_get_usage_profile_attrs(self, attributes):
        assert isinstance(attributes, Tree)
        assert attributes.get_node('1').data.revision_id == 1
        assert attributes.get_node('1').data.time_units == 'hours'
        print(
            "\033[36m\nsucceed_get_usage_profile_attributes topic was broadcast"
        )

    def on_succeed_get_all_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['revision_id'] == 1
        assert attributes['name'] == 'Test Revision'
        assert attributes['program_time'] == 0.0
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

    @pytest.mark.integration
    def test_do_get_attributes_revision(self, test_program_dao):
        """_do_get_attributes() should return a dict of revision attributes on success."""
        pub.subscribe(self.on_succeed_get_revision_attrs,
                      'succeed_get_revision_attributes')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT._do_get_attributes(1, 'revision')

    @pytest.mark.integration
    def test_do_get_attributes_failure_definitions(self, test_program_dao):
        """_do_get_attributes() should return a dict of failure definition records on success."""
        pub.subscribe(self.on_succeed_get_failure_definition_attrs,
                      'succeed_get_failure_definitions_attributes')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT._do_get_attributes(1, 'failure_definitions')

    @pytest.mark.integration
    def test_do_get_attributes_usage_profile(self, test_program_dao):
        """_do_get_attributes() should return treelib Tree() on success."""
        pub.subscribe(self.on_succeed_get_usage_profile_attrs,
                      'succeed_get_usage_profile_attributes')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT._do_get_attributes(1, 'usage_profile')

    @pytest.mark.integration
    def test_do_get_all_attributes_data_manager(self, test_program_dao):
        """do_get_all_attributes() should return a dict of all RAMSTK data tables' attributes on success."""
        pub.subscribe(self.on_succeed_get_all_attrs,
                      'succeed_get_all_revision_attributes')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT.do_get_all_attributes(1)

    @pytest.mark.integration
    def test_do_set_attributes(self, test_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        pub.sendMessage('request_set_revision_attributes',
                        node_id=1,
                        key='revision_code',
                        value='-')
        pub.sendMessage('request_set_revision_attributes',
                        node_id=1,
                        key='definition',
                        value=b'Test Description',
                        definition_id=1)
        pub.sendMessage('request_set_revision_attributes',
                        node_id=1,
                        key='description',
                        value=b'This is the mission description.',
                        usage_id='1')
        pub.sendMessage('request_set_revision_attributes',
                        node_id=1,
                        key='phase_end',
                        value=5.12,
                        usage_id='1.1')
        pub.sendMessage('request_set_revision_attributes',
                        node_id=1,
                        key='minimum',
                        value=5.12,
                        usage_id='1.1.1')
        assert DUT.do_select(1, table='revision').revision_code == '-'
        assert DUT.do_select(
            1,
            table='failure_definitions')[1].definition == b'Test Description'
        assert DUT.do_select(
            1, table='usage_profile').get_node('1').data.description == (
                b'This is the mission description.')
        assert DUT.do_select(
            1, table='usage_profile').get_node('1.1').data.phase_end == 5.12
        assert DUT.do_select(
            1, table='usage_profile').get_node('1.1.1').data.minimum == 5.12

    @pytest.mark.integration
    def test_do_set_all_attributes(self, test_program_dao):
        """do_set_all_attributes() should send the success message."""
        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        pub.sendMessage('request_set_all_revision_attributes',
                        attributes={
                            'revision_id': 1,
                            'revision_code': '1',
                            'remarks': b'These are remarks added by a test.',
                            'total_part_count': 28,
                            'definition': b'Failure Definition',
                            'phase_end': 0.0
                        },
                        definition_id=1,
                        usage_id='1.1')
        assert DUT.do_select(1, table='revision').revision_code == '1'
        assert DUT.do_select(
            1,
            table='revision').remarks == b'These are remarks added by a test.'
        assert DUT.do_select(1, table='revision').total_part_count == 28
        assert DUT.do_select(
            1,
            table='failure_definitions')[1].definition == b'Failure Definition'
        assert DUT.do_select(
            1, table='usage_profile').get_node('1.1').data.phase_end == 0.0

    @pytest.mark.integration
    def test_on_get_tree(self, test_program_dao):
        """on_get_tree() should return the revision treelib Tree."""
        pub.subscribe(self.on_succeed_get_revision_tree,
                      'succeed_get_revision_tree')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT.do_get_tree()

    @pytest.mark.integration
    def test_do_get_last_id(self, test_program_dao):
        """do_get_last_id() should broadcast the success message with the last ID aste payload."""
        pub.subscribe(self.on_succeed_get_last_id,
                      'succeed_get_last_revision_id')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT.do_get_last_id('revision')

        pub.unsubscribe(self.on_succeed_get_last_id,
                        'succeed_get_last_revision_id')

@pytest.mark.usefixtures('test_program_dao')
class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_revision(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_revision topic was broadcast")

    def on_succeed_insert_failure_definition(self, tree):
        assert isinstance(tree, dict)
        assert isinstance(tree[4], RAMSTKFailureDefinition)
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

    @pytest.mark.integration
    def test_do_insert(self, test_program_dao):
        """do_insert() should send the success message after successfully inserting a new revision."""
        pub.subscribe(self.on_succeed_insert_revision,
                      'succeed_insert_revision')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT.do_insert()

        assert isinstance(
            DUT.tree.get_node(3).data['revision'], RAMSTKRevision)
        assert DUT.tree.get_node(3).data['revision'].revision_id == 3
        assert DUT.tree.get_node(3).data['revision'].name == 'New Revision'
        assert isinstance(
            DUT.tree.get_node(3).data['failure_definitions'], dict)
        assert isinstance(DUT.tree.get_node(3).data['usage_profile'], Tree)

    @pytest.mark.integration
    def test_do_insert_failure_definition(self, test_program_dao):
        """do_insert() should send the success message after successfully inserting a new failure definition."""
        pub.subscribe(self.on_succeed_insert_failure_definition,
                      'succeed_insert_failure_definition')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT.do_insert_failure_definition(1)

        assert isinstance(
            DUT.tree.get_node(1).data['failure_definitions'], dict)
        assert isinstance(
            DUT.tree.get_node(1).data['failure_definitions'][4],
            RAMSTKFailureDefinition)

    @pytest.mark.integration
    def test_do_insert_mission(self, test_program_dao):
        """do_insert() should send the success message after successfully inserting a new mission."""
        pub.subscribe(self.on_succeed_insert_mission, 'succeed_insert_mission')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT.do_insert_mission(1)

        assert isinstance(DUT.tree.get_node(1).data['usage_profile'], Tree)
        assert isinstance(
            DUT.tree.get_node(1).data['usage_profile'].get_node('3').data,
            RAMSTKMission)

    @pytest.mark.integration
    def test_do_insert_mission_phase(self, test_program_dao):
        """do_insert() should send the success message after successfully inserting a new mission phase."""
        pub.subscribe(self.on_succeed_insert_mission_phase,
                      'succeed_insert_mission_phase')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT.do_insert_mission_phase(1, 1)

        assert isinstance(DUT.tree.get_node(1).data['usage_profile'], Tree)
        assert isinstance(
            DUT.tree.get_node(1).data['usage_profile'].get_node(
                str('1.4')).data, RAMSTKMissionPhase)

    @pytest.mark.integration
    def test_do_insert_environment(self, test_program_dao):
        """do_insert() should send the success message after successfully inserting a new environment."""
        pub.subscribe(self.on_succeed_insert_environment,
                      'succeed_insert_environment')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT.do_insert_environment(1, 1, 1)

        assert isinstance(DUT.tree.get_node(1).data['usage_profile'], Tree)
        assert isinstance(
            DUT.tree.get_node(1).data['usage_profile'].get_node(
                str('1.1.4')).data, RAMSTKEnvironment)


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

    def on_succeed_update_failure_definition(self, node_id):
        assert node_id == 1
        print(
            "\033[36m\nsucceed_update_failure_definition topic was broadcast")

    def on_fail_update_failure_definition(self, error_message):
        assert error_message == (
            'Attempted to save non-existent failure definition with ID 100.')
        print("\033[35m\nfail_update_failure_definition topic was broadcast")

    def on_succeed_update_usage_profile(self, node_id):
        assert node_id == '1'
        print("\033[36m\nsucceed_update_usage_profile topic was broadcast")

    def on_fail_update_usage_profile(self, error_message):
        assert error_message == (
            'Attempted to save non-existent usage profile element with ID 1.10.'
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
        _failure_definition[1].definition = b'Failure Definition'
        _usage_profile = DUT.do_select(1, table='usage_profile')
        _usage_profile.get_node('1.1').data.phase_end = 0.0
        DUT.do_update(1)

        DUT.do_select_all()
        _revision = DUT.do_select(1, table='revision')

        assert _revision.name == 'Test Revision'
        _failure_definition = DUT.do_select(1, table='failure_definitions')
        assert _failure_definition[1].definition == b'Failure Definition'
        _usage_profile = DUT.do_select(1, table='usage_profile')
        assert _usage_profile.get_node('1.1').data.phase_end == 0.0

        pub.unsubscribe(self.on_succeed_update_revision,
                        'succeed_update_revision')

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_program_dao):
        """ do_update() should return a non-zero error code when passed a Revision ID that doesn't exist. """
        pub.subscribe(self.on_fail_update_revision, 'fail_update_revision')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT.do_update(100)

        pub.unsubscribe(self.on_fail_update_revision, 'fail_update_revision')

    @pytest.mark.integration
    def test_do_update_failure_definition(self, test_program_dao):
        """do_update_failure_definition() should broadcast the succeed message on success."""
        pub.subscribe(self.on_succeed_update_failure_definition,
                      'succeed_update_failure_definition')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        _failure_definition = DUT.do_select(1, table='failure_definitions')
        _failure_definition[1].definition = b'Big test definition'

        DUT._do_update_failure_definition(1, 1)
        _failure_definition = DUT.do_select(1, table='failure_definitions')

        assert _failure_definition[1].definition == b'Big test definition'

        pub.unsubscribe(self.on_succeed_update_failure_definition,
                        'succeed_update_failure_definition')

    @pytest.mark.integration
    def test_do_update_failure_definition_non_existent_id(
            self, test_program_dao):
        """do_update_failure_definition() should broadcast the fail message when attempting to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_failure_definition,
                      'fail_update_failure_definition')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT._do_update_failure_definition(1, 100)

        pub.unsubscribe(self.on_fail_update_failure_definition,
                        'fail_update_failure_definition')

    @pytest.mark.integration
    def test_do_update_all_failure_definition(self, test_program_dao):
        """do_update_all failure_definition() should return None on success."""
        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        _failure_definition = DUT.do_select(1, table='failure_definitions')
        _failure_definition[1].definition = b'Big test definition #1'
        _failure_definition[2].definition = b'Big test definition #2'

        assert DUT._do_update_all_failure_definition(1) is None

        _failure_definition = DUT.do_select(1, table='failure_definitions')
        assert _failure_definition[1].definition == b'Big test definition #1'

        _failure_definition = DUT.do_select(1, table='failure_definitions')
        assert _failure_definition[2].definition == b'Big test definition #2'

    @pytest.mark.integration
    def test_do_update_usage_profile(self, test_program_dao):
        """do_update_usage_profile() should broadcast the succeed message on success."""
        pub.subscribe(self.on_succeed_update_usage_profile,
                      'succeed_update_usage_profile')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        _mission = DUT.do_select(1, table='usage_profile').get_node('1').data
        _mission.description = b'Big ole failure mode'

        DUT._do_update_usage_profile(1, '1')
        _mission = DUT.do_select(1, table='usage_profile').get_node('1').data

        assert _mission.description == b'Big ole failure mode'

        pub.unsubscribe(self.on_succeed_update_usage_profile,
                        'succeed_update_usage_profile')

    @pytest.mark.integration
    def test_do_update_usage_profile_non_existent_id(self, test_program_dao):
        """do_update_usage_profile() should broadcast the fail message when attempting to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_usage_profile,
                      'fail_update_usage_profile')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT._do_update_usage_profile(1, '1.10')

        pub.unsubscribe(self.on_fail_update_usage_profile,
                        'fail_update_usage_profile')
