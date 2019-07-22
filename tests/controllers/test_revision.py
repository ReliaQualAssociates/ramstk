# pylint: disable=protected-access, no-self-use
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
from ramstk.controllers.revision import dmRevision
from ramstk.dao import DAO
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


@pytest.mark.usefixtures('test_dao', 'test_configuration')
class TestCreateControllers():
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager(self, test_dao):
        """__init__() should return a Revision data manager."""
        DUT = dmRevision(test_dao)

        assert isinstance(DUT, dmRevision)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, DAO)
        assert DUT._tag == 'revision'
        assert DUT._root == 0
        assert DUT._revision_id == 0


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.integration
    def test_do_select_all(self, test_dao):
        """do_select_all() should return a Tree() object populated with RAMSTKRevision instances on success."""
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        def on_message(tree):
            assert isinstance(tree, Tree)
            assert isinstance(
                tree.get_node(1).data['revision'], RAMSTKRevision)
            assert isinstance(
                tree.get_node(1).data['failure_definitions'], dict)
            assert isinstance(
                tree.get_node(1).data['failure_definitions'][1], RAMSTKFailureDefinition)
            assert isinstance(
                tree.get_node(1).data['usage_profile'], Tree)

        pub.subscribe(on_message, 'succeed_retrieve_revisions')

        pub.sendMessage('request_retrieve_revisions')

    @pytest.mark.integration
    def test_do_select_revision(self, test_dao):
        """do_select() should return an instance of the RAMSTKRevision on success."""
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        _revision = DUT.do_select(1, table='revision')

        assert isinstance(_revision, RAMSTKRevision)
        assert _revision.availability_logistics == 1.0
        assert _revision.name == 'Test Revision'

    @pytest.mark.integration
    def test_do_select_failure_definition(self, test_dao):
        """do_select() should return an instance of RAMSTKFailureDefinition on success."""
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        _failure_definition = DUT.do_select(1, table='failure_definitions')

        assert isinstance(_failure_definition, dict)
        assert isinstance(_failure_definition[1], RAMSTKFailureDefinition)
        assert _failure_definition[1].definition == b'Failure Definition'

    @pytest.mark.integration
    def test_do_select_usage_profile(self, test_dao):
        """do_select() should return the usage profile treelib Tree() on success."""
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        _usage_profile = DUT.do_select(1, table='usage_profile')

        assert isinstance(_usage_profile, Tree)
        assert isinstance(_usage_profile.get_node('1').data, RAMSTKMission)
        assert isinstance(_usage_profile.get_node('1.1').data, RAMSTKMissionPhase)
        assert isinstance(_usage_profile.get_node('1.1.1').data, RAMSTKEnvironment)

    @pytest.mark.integration
    def test_do_select_unknown_table(self, test_dao):
        """do_select() should raise a KeyError when an unknown table name is requested."""
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.integration
    def test_do_select_non_existent_id(self, test_dao):
        """do_select() should return None when a non-existent Revision ID is requested."""
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        assert DUT.do_select(100, table='revision') is None


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestDeleteMethods():
    """Class for testing the data manager delete() method."""

    @pytest.mark.integration
    def test_do_delete(self, test_dao):
        """_do_delete() should send the success message with the treelib Tree."""
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        def on_message(node_id):
            assert node_id == 2
            assert DUT.last_id == 1

        pub.subscribe(on_message, 'succeed_delete_revision')

        pub.sendMessage('request_delete_revision', node_id=DUT.last_id)

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self, test_dao):
        """_do_delete() should send the fail message."""
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        def on_message(error_msg):
            assert error_msg == 'Attempted to delete non-existent revision ID 300.'

        pub.subscribe(on_message, 'fail_delete_revision')

        DUT._do_delete(300)


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestGetterSetter():
    """Class for testing methods that get or set."""

    @pytest.mark.integration
    def test_do_get_attributes_revision(self, test_dao):
        """do_get_attributes() should return a dict of revision attributes on success."""
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        def on_message(attributes):
            assert isinstance(attributes, dict)
            assert attributes['revision_id'] == 1
            assert attributes['name'] == 'Test Revision'
            assert attributes['program_time'] == 0.0

        pub.subscribe(on_message, 'succeed_get_revision_attributes')

        pub.sendMessage('request_get_revision_attributes',
                        node_id=1,
                        table='revision')

    @pytest.mark.integration
    def test_do_get_attributes_failure_definitions(self, test_dao):
        """do_get_attributes() should return a dict of failure definition records on success."""
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        def on_message(attributes):
            assert isinstance(attributes, dict)
            assert attributes[1].revision_id == 1
            assert attributes[1].definition == b'Failure Definition'

        pub.subscribe(on_message, 'succeed_get_revision_attributes')

        pub.sendMessage('request_get_revision_attributes',
                        node_id=1,
                        table='failure_definitions')

    @pytest.mark.integration
    def test_do_get_attributes_usage_profile(self, test_dao):
        """do_get_attributes() should return treelib Tree() on success."""
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        def on_message(attributes):
            assert isinstance(attributes, Tree)
            assert attributes.get_node('1').data.revision_id == 1
            assert attributes.get_node('1').data.time_units == 'hours'

        pub.subscribe(on_message, 'succeed_get_revision_attributes')

        pub.sendMessage('request_get_revision_attributes',
                        node_id=1,
                        table='usage_profile')

    @pytest.mark.integration
    def test_do_get_all_attributes_data_manager(self, test_dao):
        """do_get_all_attributes() should return a dict of all RAMSTK data tables' attributes on success."""
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        def on_message(attributes):
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

        pub.subscribe(on_message, 'succeed_get_all_revision_attributes')

        pub.sendMessage('request_get_all_revision_attributes', node_id=1)

    @pytest.mark.integration
    def test_do_set_attributes(self, test_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmRevision(test_dao)
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
                        key='phase_end',
                        value=5.12,
                        usage_id='1.1')
        assert DUT.do_select(1, table='revision').revision_code == '-'
        assert DUT.do_select(
            1,
            table='failure_definitions')[1].definition == b'Test Description'
        assert DUT.do_select(1, table='usage_profile').get_node('1.1').data.phase_end == 5.12

    @pytest.mark.integration
    def test_do_set_all_attributes(self, test_dao):
        """do_set_all_attributes() should send the success message."""
        DUT = dmRevision(test_dao)
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
        assert DUT.do_select(1, table='usage_profile').get_node('1.1').data.phase_end == 0.0

        pub.sendMessage('request_set_all_revision_attributes',
                        attributes={
                            'revision_id': 1,
                            'revision_code': '',
                            'remarks': b'',
                            'total_part_count': 1,
                            'phase_end': 0.0
                        },
                        definition_id=1,
                        usage_id='1.1')

    @pytest.mark.integration
    def test_on_get_tree(self, test_dao):
        """on_get_tree() should return the revision treelib Tree."""
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        def on_message(dmtree):
            assert isinstance(dmtree, Tree)
            assert isinstance(
                dmtree.get_node(1).data['revision'], RAMSTKRevision)
            assert isinstance(
                dmtree.get_node(1).data['failure_definitions'], dict)
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

        pub.subscribe(on_message, 'succeed_get_revision_tree')

        pub.sendMessage('request_get_revision_tree')


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestInsertMethods():
    """Class for testing the data manager insert() method."""

    @pytest.mark.integration
    def test_do_insert(self, test_dao):
        """do_insert() should send the success message after successfully inserting a new revision."""
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        def on_message(node_id):
            assert node_id == 3
            assert isinstance(
                DUT.tree.get_node(node_id).data['revision'], RAMSTKRevision)
            assert DUT.tree.get_node(node_id).data['revision'].revision_id == 3
            assert DUT.tree.get_node(
                node_id).data['revision'].name == 'New Revision'
            assert isinstance(
                DUT.tree.get_node(node_id).data['failure_definitions'], dict)
            assert isinstance(
                DUT.tree.get_node(node_id).data['usage_profile'], Tree)

        pub.subscribe(on_message, 'succeed_insert_revision')

        pub.sendMessage('request_insert_revision')


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""

    @pytest.mark.integration
    def test_do_update_data_manager(self, test_dao):
        """ do_update() should return a zero error code on success. """
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        def on_message(node_id):
            DUT.do_select_all()
            _revision = DUT.do_select(node_id, table='revision')
            assert node_id == 1
            assert _revision.name == 'Test Revision'
            _failure_definition = DUT.do_select(node_id,
                                                table='failure_definitions')
            assert _failure_definition[1].definition == b'Failure Definition'
            _usage_profile = DUT.do_select(1, table='usage_profile')
            assert _usage_profile.get_node('1.1').data.phase_end == 0.0

        pub.subscribe(on_message, 'succeed_update_revision')

        _revision = DUT.do_select(1, table='revision')
        _revision.name = 'Test Revision'
        _failure_definition = DUT.do_select(1, table='failure_definitions')
        _failure_definition[1].definition = b'Failure Definition'
        _usage_profile = DUT.do_select(1, table='usage_profile')
        _usage_profile.get_node('1.1').data.phase_end = 0.0

        pub.sendMessage('request_update_revision', node_id=1)

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_dao):
        """ do_update() should return a non-zero error code when passed a Revision ID that doesn't exist. """
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        def on_message(error_msg):
            assert error_msg == (
                'Attempted to save non-existent revision with revision ID '
                '100.')

        pub.subscribe(on_message, 'fail_update_revision')

        DUT.do_update(100)

    @pytest.mark.integration
    def test_do_update_all(self, test_dao):
        """ do_update_all() should return a zero error code on success. """
        DUT = dmRevision(test_dao)
        DUT.do_select_all()

        def on_message(node_id):
            _fd_keys = DUT.do_select(
                node_id, table='failure_definitions').keys()
            assert DUT.do_select(node_id,
                                 table='revision').revision_id == node_id
            assert DUT.do_select(
                node_id, table='failure_definitions')[_fd_keys[0]].revision_id == node_id
            assert DUT.do_select(
                node_id, table='usage_profile').get_node('1').revision_id == node_id

        pub.subscribe(on_message, 'succeed_update_revision')

        pub.sendMessage('request_update_all_revisions')
