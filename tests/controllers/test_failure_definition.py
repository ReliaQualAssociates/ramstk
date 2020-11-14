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
from __mocks__ import MOCK_FAILURE_DEFINITIONS
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmFailureDefinition
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKFailureDefinition


class MockDao:
    _all_failure_definitions = []

    def do_delete(self, record):
        for _idx, _record in enumerate(self._all_failure_definitions):
            if _record.definition_id == record.definition_id:
                self._all_failure_definitions.pop(_idx)

    def do_insert(self, record):
        self._all_failure_definitions.append(record)

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

    def do_select_all(self, table, key, value, order=None, _all=False):
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

    def do_update(self, record):
        for _key in MOCK_FAILURE_DEFINITIONS:
            if _key == record.definition_id:
                MOCK_FAILURE_DEFINITIONS[_key]['definition'] = \
                    record.definition

    def get_last_id(self, table, id_column):
        return max(MOCK_FAILURE_DEFINITIONS.keys())


@pytest.fixture
def mock_program_dao(monkeypatch):
    yield MockDao()


class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager(self):
        """__init__() should return a Revision data manager."""
        DUT = dmFailureDefinition()

        assert isinstance(DUT, dmFailureDefinition)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'failure_definition'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_failure_definition_attributes')
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_update,
                                'request_update_failure_definition')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_failure_definitions')
        assert pub.isSubscribed(DUT.do_get_tree,
                                'request_get_failure_definition_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_failure_definition_attributes')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'lvw_editing_failure_definition')
        assert pub.isSubscribed(DUT._do_delete_failure_definition,
                                'request_delete_failure_definition')
        assert pub.isSubscribed(DUT._do_insert_failure_definition,
                                'request_insert_failure_definition')


class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with RAMSTKFailureDefinition instances on success."""
        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert isinstance(DUT.tree, Tree)
        assert isinstance(
            DUT.tree.get_node(1).data['failure_definition'],
            RAMSTKFailureDefinition)

    @pytest.mark.unit
    def test_do_select_all_tree_loaded(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with RAMSTKFailureDefinition instances on success when there is already a tree of definitions."""
        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_select_all(attributes={'revision_id': 1})

        assert isinstance(DUT.tree, Tree)
        assert isinstance(
            DUT.tree.get_node(1).data['failure_definition'],
            RAMSTKFailureDefinition)

    @pytest.mark.unit
    def test_do_select_failure_definition(self, mock_program_dao):
        """do_select() should return an instance of RAMSTKFailureDefinition on
        success."""
        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _failure_definition = DUT.do_select(1, table='failure_definition')

        assert isinstance(_failure_definition, RAMSTKFailureDefinition)
        assert _failure_definition.definition == 'Failure Definition'

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Revision ID is
        requested."""
        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='failure_definition') is None


class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_failure_definition(self, node_id, tree):
        assert node_id == 1
        assert isinstance(tree, Tree)
        print(
            "\033[36m\nsucceed_delete_failure_definition topic was broadcast.")

    def on_fail_delete_failure_definition(self, error_message):
        assert error_message == ('Attempted to delete non-existent failure '
                                 'definition ID 10.')
        print("\033[35m\nfail_delete_failure_definition topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete_failure_definition(self, mock_program_dao):
        """_do_delete_failure_definition() should send the success message
        after successfully deleting a definition."""
        pub.subscribe(self.on_succeed_delete_failure_definition,
                      'succeed_delete_failure_definition')

        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete_failure_definition(1)

        with pytest.raises(AttributeError):
            __ = DUT.tree.get_node(1).data['failure_definition']

        pub.unsubscribe(self.on_succeed_delete_failure_definition,
                        'succeed_delete_failure_definition')

    @pytest.mark.unit
    def test_do_delete_failure_definition_non_existent_id(
            self, mock_program_dao):
        """_do_delete_failure_definition() should send the fail message when
        attempting to delete a non-existent failure definition."""
        pub.subscribe(self.on_fail_delete_failure_definition,
                      'fail_delete_failure_definition')

        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete_failure_definition(10)

        pub.unsubscribe(self.on_fail_delete_failure_definition,
                        'fail_delete_failure_definition')


class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_failure_definition_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes[1].revision_id == 1
        assert attributes[1].definition == 'Failure Definition'
        print(
            "\033[36m\nsucceed_get_failure_definitions_attributes topic was broadcast"
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

    def on_succeed_get_failure_definition_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['failure_definition'],
            RAMSTKFailureDefinition)
        print(
            "\033[36m\nsucceed_get_failure_definition_tree topic was broadcast"
        )

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """_do_get_attributes() should return a dict of failure definition records on success."""
        pub.subscribe(self.on_succeed_get_failure_definition_attrs,
                      'succeed_get_failure_definitions_attributes')

        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_attributes(1, 'failure_definition')

        pub.unsubscribe(self.on_succeed_get_failure_definition_attrs,
                        'succeed_get_failure_definitions_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_failure_definition_attributes',
                        node_id=[1, 1, ''],
                        package={'definition': 'Test Description'})

        assert DUT.do_select(
            1, table='failure_definition').definition == 'Test Description'

    @pytest.mark.unit
    def test_do_set_all_attributes(self, mock_program_dao):
        """do_set_all_attributes() should send the success message."""
        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_all_failure_definition_attributes',
                        attributes={'definition_id': 1,
                                    'definition': 'Failure Definition'})
        assert DUT.do_select(
            1,
            table='failure_definition').definition == 'Failure Definition'

    @pytest.mark.unit
    def test_do_set_all_attributes_extra_attribute(self, mock_program_dao):
        """do_set_all_attributes() should send the success message."""
        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_all_failure_definition_attributes',
                        attributes={'definition_id': 1,
                                    'definition': 'Failure Definition',
                                    'funpack': 'Fun Packer'})
        assert DUT.do_select(
            1,
            table='failure_definition').definition == 'Failure Definition'

    @pytest.mark.unit
    def test_on_get_tree(self, mock_program_dao):
        """on_get_tree() should return the failure definition treelib Tree."""
        pub.subscribe(self.on_succeed_get_failure_definition_tree,
                      'succeed_get_failure_definition_tree')

        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_failure_definition_tree,
                        'succeed_get_failure_definition_tree')


class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_failure_definition(self, node_id, tree):
        assert node_id == 2
        assert isinstance(tree, Tree)
        assert isinstance(tree[2].data['failure_definition'],
                          RAMSTKFailureDefinition)
        print(
            "\033[36m\nsucceed_insert_failure_definition topic was broadcast")

    @pytest.mark.unit
    def test_do_insert(self, mock_program_dao):
        """do_insert() should send the success message after successfully inserting a new failure definition."""
        pub.subscribe(self.on_succeed_insert_failure_definition,
                      'succeed_insert_failure_definition')

        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_failure_definition()

        assert isinstance(
            DUT.tree.get_node(1).data['failure_definition'],
            RAMSTKFailureDefinition)

        pub.unsubscribe(self.on_succeed_insert_failure_definition,
                        'succeed_insert_failure_definition')


@pytest.mark.usefixtures('test_program_dao')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_failure_definition(self, node_id):
        assert node_id == 1
        print(
            "\033[36m\nsucceed_update_failure_definition topic was broadcast")

    def on_fail_update_failure_definition(self, error_message):
        assert error_message == (
            'No data package found for failure definition ID 100.')
        print("\033[35m\nfail_update_failure_definition topic was broadcast")

    @pytest.mark.integration
    def test_do_update_data_manager(self, test_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update_failure_definition,
                      'succeed_update_failure_definition')

        DUT = dmFailureDefinition()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _failure_definition = DUT.do_select(1, table='failure_definition')
        _failure_definition.definition = 'Big test definition'

        DUT.do_update(1)
        _failure_definition = DUT.do_select(1, table='failure_definition')

        assert _failure_definition.definition == 'Big test definition'

        pub.unsubscribe(self.on_succeed_update_failure_definition,
                        'succeed_update_failure_definition')

    @pytest.mark.unit
    def test_do_update_failure_definition_non_existent_id(
            self, mock_program_dao):
        """do_update_failure_definition() should broadcast the fail message
        when attempting to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_failure_definition,
                      'fail_update_failure_definition')

        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_update(100)

        pub.unsubscribe(self.on_fail_update_failure_definition,
                        'fail_update_failure_definition')

    @pytest.mark.integration
    def test_do_update_all_failure_definition(self, test_program_dao):
        """do_update_all failure_definition() should return None on success."""
        DUT = dmFailureDefinition()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _failure_definition = DUT.do_select(1, table='failure_definition')
        _failure_definition.definition = 'Big test definition #1'
        _failure_definition = DUT.do_select(2, table='failure_definition')
        _failure_definition.definition = 'Big test definition #2'

        assert DUT.do_update_all() is None

        _failure_definition = DUT.do_select(1, table='failure_definition')
        assert _failure_definition.definition == 'Big test definition #1'

        _failure_definition = DUT.do_select(2, table='failure_definition')
        assert _failure_definition.definition == 'Big test definition #2'
