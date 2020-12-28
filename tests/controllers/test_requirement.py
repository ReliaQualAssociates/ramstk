# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_requirement.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Requirement algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from __mocks__ import MOCK_REQUIREMENTS
from ramstk.controllers import dmRequirement
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKRequirement


class MockDao:
    _all_requirements = []

    def do_delete(self, item):
        for _idx, _requirement in enumerate(self._all_requirements):
            try:
                if _requirement.requirement_id == item.requirement_id:
                    self._all_requirements.pop(_idx)
            except AttributeError:
                raise DataAccessError('')

    def do_insert(self, record):
        if record.parent_id == 30:
            raise DataAccessError('An error occurred with RAMSTK.')
        else:
            self._all_requirements.append(record)

    def do_select_all(self,
                      table,
                      key=None,
                      value=None,
                      order=None,
                      _all=False):
        if table == RAMSTKRequirement:
            self._all_requirements = []
            for _key in MOCK_REQUIREMENTS:
                _record = table()
                _record.revision_id = value
                _record.requirement_id = _key
                _record.set_attributes(MOCK_REQUIREMENTS[_key])
                self._all_requirements.append(_record)

            return self._all_requirements

    def do_update(self, record):
        if isinstance(record, RAMSTKRequirement):
            for _key in MOCK_REQUIREMENTS:
                if _key == record.requirement_id:
                    MOCK_REQUIREMENTS[_key]['derived'] = record.derived
                    MOCK_REQUIREMENTS[_key]['description'] = record.description
                    MOCK_REQUIREMENTS[_key]['figure_number'] = \
                        record.figure_number
                    MOCK_REQUIREMENTS[_key]['owner'] = record.owner
                    MOCK_REQUIREMENTS[_key]['page_number'] = record.page_number
                    MOCK_REQUIREMENTS[_key]['parent_id'] = record.parent_id
                    MOCK_REQUIREMENTS[_key]['priority'] = int(record.priority)
                    MOCK_REQUIREMENTS[_key]['requirement_code'] = \
                        record.requirement_code
                    MOCK_REQUIREMENTS[_key]['specification'] = \
                        record.specification
                    MOCK_REQUIREMENTS[_key]['requirement_type'] = \
                        record.requirement_type
                    MOCK_REQUIREMENTS[_key]['validated'] = record.validated
                    MOCK_REQUIREMENTS[_key][
                        'validated_date'] = record.validated_date

    def get_last_id(self, table, id_column):
        return max(MOCK_REQUIREMENTS.keys())


@pytest.fixture
def mock_program_dao(monkeypatch):
    yield MockDao()


class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Requirement data manager."""
        DUT = dmRequirement()

        assert isinstance(DUT, dmRequirement)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'requirements'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_update, 'request_update_requirement')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_requirements')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_requirement_attributes')
        assert pub.isSubscribed(DUT.do_get_tree,
                                'request_get_requirements_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_requirement_attributes')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'wvw_editing_requirement')
        assert pub.isSubscribed(DUT.do_create_code,
                                'request_create_requirement_code')
        assert pub.isSubscribed(DUT._do_delete,
                                'request_delete_requirement')
        assert pub.isSubscribed(DUT._do_insert_requirement,
                                'request_insert_requirement')


class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_retrieve_requirements(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_retrieve_requirements topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all(1) should return a Tree() object populated with RAMSTKRequirement instances on success."""
        pub.subscribe(self.on_succeed_retrieve_requirements,
                      'succeed_retrieve_requirements')
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.tree.get_node(1).data, dict)
        assert isinstance(
            DUT.tree.get_node(1).data['requirement'], RAMSTKRequirement)

        pub.unsubscribe(self.on_succeed_retrieve_requirements,
                        'succeed_retrieve_requirements')

    @pytest.mark.unit
    def test_do_select_requirement(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKRequirement on success."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _requirement = DUT.do_select(1, table='requirement')

        assert isinstance(_requirement, RAMSTKRequirement)
        assert _requirement.description == ''
        assert _requirement.priority == 0

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is requested."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Requirement ID is requested."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='requirement') is None


class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_requirement(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_requirement topic was broadcast.")

    def on_fail_delete_requirement(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent requirement ID 300.')
        print("\033[35m\nfail_delete_requirement topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete_requirement(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib Tree."""
        pub.subscribe(self.on_succeed_delete_requirement,
                      'succeed_delete_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(DUT.last_id)

        assert DUT.last_id == 1

        pub.unsubscribe(self.on_succeed_delete_requirement,
                        'succeed_delete_requirement')

    @pytest.mark.unit
    def test_do_delete_requirement_with_children(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib Tree."""
        pub.subscribe(self.on_succeed_delete_requirement,
                      'succeed_delete_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(1)

        pub.unsubscribe(self.on_succeed_delete_requirement,
                        'succeed_delete_requirement')

    @pytest.mark.unit
    def test_do_delete_requirement_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to delete a non-existent requirement."""
        pub.subscribe(self.on_fail_delete_requirement,
                      'fail_delete_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_requirement,
                        'fail_delete_requirement')


class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_requirement_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['requirement_id'] == 1
        assert attributes['description'] == ''
        assert attributes['priority'] == 0
        print(
            "\033[36m\nsucceed_get_requirement_attributes topic was broadcast")

    def on_succeed_get_requirement_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data, dict)
        assert isinstance(
            tree.get_node(1).data['requirement'], RAMSTKRequirement)
        print("\033[36m\nsucceed_get_requirement_tree topic was broadcast")

    def on_succeed_create_requirement_code(self, requirement_code):
        assert requirement_code == 'DOYLE-0001'
        print("\033[36m\nsucceed_create_requirement_code topic was "
              "broadcast")

    def on_fail_create_requirement_code(self, error_message):
        assert error_message == 'No data package found for requirement ID 10.'
        print("\033[36m\nfail_create_requirement_code topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes_requirement(self, mock_program_dao):
        """_do_get_attributes() should return a dict of requirement attributes on success."""
        pub.subscribe(self.on_succeed_get_requirement_attrs,
                      'succeed_get_requirement_attributes')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_attributes(1, 'requirement')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_requirement_attributes',
                        node_id=[1, -1],
                        package={'requirement_code': 'REQ-0001'})
        assert DUT.do_select(
            1, table='requirement').requirement_code == 'REQ-0001'

    @pytest.mark.unit
    def test_do_set_attributes_no_date(self, mock_program_dao):
        """do_set_attributes() should set validation date to today() if no value is passed."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_requirement_attributes',
                        node_id=[1, -1],
                        package={'validated_date': None})
        assert DUT.do_select(
            1, table='requirement').validated_date == date.today()

    @pytest.mark.unit
    def test_on_get_tree(self, mock_program_dao):
        """on_get_tree() should return the requirement treelib Tree."""
        pub.subscribe(self.on_succeed_get_requirement_tree,
                      'succeed_get_requirements_tree')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_requirement_tree,
                        'succeed_get_requirements_tree')

    @pytest.mark.unit
    def test_do_create_requirement_code(self, mock_program_dao):
        """do_create_requirement_code() should return"""
        pub.subscribe(self.on_succeed_create_requirement_code,
                      'succeed_create_requirement_code')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_create_requirement_code',
                        node_id=1,
                        prefix="DOYLE")

        pub.unsubscribe(self.on_succeed_create_requirement_code,
                      'succeed_create_requirement_code')

    @pytest.mark.unit
    def test_fail_do_create_requirement_code(self, mock_program_dao):
        """do_create_requirement_code() should send the fail message when there is no node in the tree for the passed Requirement ID."""
        pub.subscribe(self.on_fail_create_requirement_code,
                      'fail_create_requirement_code')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_create_requirement_code',
                        node_id=10,
                        prefix="DOYLE")

        pub.unsubscribe(self.on_fail_create_requirement_code,
                        'fail_create_requirement_code')

    @pytest.mark.unit
    def test_do_create_all_requirement_codes(self, mock_program_dao):
        """do_create_requirement_code() should return"""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_create_all_requirement_codes', prefix="DOYLE")

        assert DUT.tree.get_node(
            2).data['requirement'].requirement_code == 'DOYLE-0002'


class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_requirement(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_requirement topic was broadcast")

    def on_fail_insert_requirement_no_parent(self, error_message):
        assert error_message == ('_do_insert_requirement: Attempted to insert child requirement under non-existent requirement ID 32.')
        print("\033[35m\nfail_insert_requirement topic was broadcast")

    def on_fail_insert_requirement_db_error(self, error_message):
        assert error_message == ('An error occurred with RAMSTK.')
        print("\033[35m\nfail_insert_requirement topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert_sibling_requirement(self, mock_program_dao):
        """do_insert() should send the success message after successfully inserting a new top-level requirement."""
        pub.subscribe(self.on_succeed_insert_requirement,
                      'succeed_insert_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_requirement(parent_id=0)

        assert isinstance(
            DUT.tree.get_node(3).data['requirement'], RAMSTKRequirement)
        assert DUT.tree.get_node(3).data['requirement'].requirement_id == 3
        assert DUT.tree.get_node(
            3).data['requirement'].description == 'New Requirement'

        pub.unsubscribe(self.on_succeed_insert_requirement,
                        'succeed_insert_requirement')

    @pytest.mark.unit
    def test_do_insert_child_requirement(self, mock_program_dao):
        """do_insert() should send the success message after successfully inserting a new child requirement."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_requirement(parent_id=1)

        assert isinstance(
            DUT.tree.get_node(3).data['requirement'], RAMSTKRequirement)
        assert DUT.tree.get_node(3).data['requirement'].parent_id == 1
        assert DUT.tree.get_node(3).data['requirement'].requirement_id == 3
        assert DUT.tree.get_node(
            3).data['requirement'].description == 'New Requirement'

    @pytest.mark.unit
    def test_do_insert_child_requirement_non_existent_id(
            self, mock_program_dao):
        """do_insert() should send the fail message attempting to add a child to a non-existent requirement."""
        pub.subscribe(self.on_fail_insert_requirement_no_parent,
                      'fail_insert_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_requirement(parent_id=32)

        pub.unsubscribe(self.on_fail_insert_requirement_no_parent,
                        'fail_insert_requirement')

    @pytest.mark.unit
    def test_do_insert_requirement_database_error(self, mock_program_dao):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_requirement_db_error,
                      'fail_insert_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_requirement(parent_id=30)

        pub.unsubscribe(self.on_fail_insert_requirement_db_error,
                        'fail_insert_requirement')


class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_requirement(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_update_requirement topic was broadcast")

    def on_fail_update_requirement_no_id(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent requirement with requirement ID 100.'
        )
        print("\033[35m\nfail_update_requirement topic was broadcast")

    def on_fail_update_requirement_no_package(self, error_message):
        assert error_message == (
            'do_update: No data package found for requirement ID 1.'
        )
        print("\033[35m\nfail_update_requirement topic was broadcast")

    def on_fail_update_requirement_wrong_data_type(self, error_message):
        assert error_message == (
            'do_update: The value for one or more attributes for requirement ID 1 was the wrong type.'
        )
        print("\033[35m\nfail_update_requirement topic was broadcast")

    @pytest.mark.unit
    def test_do_update_data_manager(self, mock_program_dao):
        """ do_update() should return a zero error code on success. """
        pub.subscribe(self.on_succeed_update_requirement,
                      'succeed_update_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _requirement = DUT.do_select(1, table='requirement')
        _requirement.description = 'Test Requirement'
        DUT.do_update(1)

        DUT.do_select_all(attributes={'revision_id': 1})
        _requirement = DUT.do_select(1, table='requirement')

        assert _requirement.description == 'Test Requirement'

        pub.unsubscribe(self.on_succeed_update_requirement,
                        'succeed_update_requirement')

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """ do_update() should return a non-zero error code when passed a Requirement ID that doesn't exist. """
        pub.subscribe(self.on_fail_update_requirement_no_id,
                      'fail_update_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_update(100)

        pub.unsubscribe(self.on_fail_update_requirement_no_id,
                        'fail_update_requirement')

    @pytest.mark.unit
    def test_do_update_data_manager_no_data_package(self, mock_program_dao):
        """ do_update() should send the fail_update_requirement message when there is no data package attached to the node. """
        pub.subscribe(self.on_fail_update_requirement_no_package,
                      'fail_update_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data.pop('requirement')
        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_requirement_no_package,
                        'fail_update_requirement')

    @pytest.mark.unit
    def test_do_update_wrong_data_type(self, mock_program_dao):
        """ do_update() should return a non-zero error code when passed a Requirement ID that doesn't exist. """
        pub.subscribe(self.on_fail_update_requirement_wrong_data_type,
                      'fail_update_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _requirement = DUT.do_select(1, table='requirement')
        _requirement.priority = {1: 2}

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_requirement_wrong_data_type,
                        'fail_update_requirement')

    @pytest.mark.unit
    def test_do_update_wrong_data_type_root_node(self, mock_program_dao):
        """ do_update() should return a non-zero error code when passed
        a Requirement ID that doesn't exist. """
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _requirement = DUT.do_select(1, table='requirement')
        _requirement.priority = {1: 2}

        DUT.do_update(0)
