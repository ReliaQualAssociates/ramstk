# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_program_status.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Validation algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pandas as pd
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from __mocks__ import MOCK_STATUS
from ramstk.controllers import dmProgramStatus
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKProgramStatus


class MockDao:
    _all_status = []

    def do_delete(self, record):
        if record is None:
            raise DataAccessError('')
        else:
            for _idx, _status in enumerate(self._all_status):
                if _status.status_id == record.status_id:
                    self._all_status.pop(_idx)

    def do_insert(self, record):
        if record.revision_id == 30:
            raise DataAccessError('An error occurred with RAMSTK.')
        else:
            self._all_status.append(record)

    def do_select_all(self, table, key=None, value=None, order=None,
                      _all=None):
        self._all_status = []
        for _key in MOCK_STATUS:
            _record = table()
            _record.revision_id = value
            _record.status_id = _key
            _record.set_attributes(MOCK_STATUS[_key])
            self._all_status.append(_record)
        return self._all_status

    def do_update(self, record):
        if isinstance(record, RAMSTKProgramStatus):
            for _key in MOCK_STATUS:
                if _key == record.status_id:
                    MOCK_STATUS[_key]['cost_remaining'] = \
                        float(record.cost_remaining)
                    MOCK_STATUS[_key]['time_remaining'] = \
                        float(record.time_remaining)
        else:
            raise DataAccessError

    def get_last_id(self, table, id_column):
        return max(MOCK_STATUS.keys())


@pytest.fixture
def mock_program_dao(monkeypatch):
    yield MockDao()


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Validation data manager."""
        DUT = dmProgramStatus()

        assert isinstance(DUT, dmProgramStatus)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'program_status'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_update, 'request_update_program_status')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_program_status')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_program_status_attributes')
        assert pub.isSubscribed(DUT.do_get_tree, 'request_get_program_status_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_program_status_attributes')
        assert pub.isSubscribed(DUT._do_delete,
                                'request_delete_program_status')
        assert pub.isSubscribed(DUT._do_insert_program_status,
                                'request_insert_program_status')


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_retrieve_program_status(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['status'], RAMSTKProgramStatus)
        print("\033[36m\nsucceed_retrieve_program_status topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with RAMSTKValidation instances on success."""
        pub.subscribe(self.on_succeed_retrieve_program_status,
                      'succeed_retrieve_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_retrieve_program_status,
                        'succeed_retrieve_program_status')

    @pytest.mark.unit
    def test_do_select_all_tree_loaded(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with RAMSTKValidation instances on success."""
        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_select_all(attributes={'revision_id': 1})

    @pytest.mark.unit
    def test_do_select_program_status(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKValidation on success."""
        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _status = DUT.do_select(2, table='status')

        assert isinstance(_status, RAMSTKProgramStatus)
        assert _status.cost_remaining == 212.32
        assert _status.time_remaining == 112.5

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is requested."""
        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Validation ID is requested."""
        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='status') is None


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_program_status(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_program_status topic was broadcast.")

    def on_fail_delete_program_status(self, error_message):
        assert error_message == ('_do_delete: Attempted to delete non-existent program status ID 300.')
        print("\033[35m\nfail_delete_validation topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete_program_status(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib Tree."""
        pub.subscribe(self.on_succeed_delete_program_status,
                      'succeed_delete_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(DUT.last_id)

        assert DUT.last_id == 1

        pub.unsubscribe(self.on_succeed_delete_program_status,
                        'succeed_delete_program_status')

    @pytest.mark.unit
    def test_do_delete_program_status_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to delete a record that doesn't exist in the database."""
        pub.subscribe(self.on_fail_delete_program_status, 'fail_delete_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_program_status,
                        'fail_delete_program_status')


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_program_status(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_program_status topic was broadcast.")

    def on_fail_insert_program_status_db_error(self, error_message):
        assert error_message == ('An error occurred with RAMSTK.')
        print("\033[35m\nfail_insert_program_status topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert_program_status(self, mock_program_dao):
        """_do_insert_validation() should send the success message after successfully inserting a validation task."""
        pub.subscribe(self.on_succeed_insert_program_status,
                      'succeed_insert_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_program_status()

        assert isinstance(
            DUT.tree.get_node(3).data['status'], RAMSTKProgramStatus)
        assert DUT.tree.get_node(3).data['status'].status_id == 3
        assert DUT.tree.get_node(
            3).data['status'].date_status == date.today()

        pub.unsubscribe(self.on_succeed_insert_program_status,
                        'succeed_insert_program_status')

    @pytest.mark.unit
    def test_do_insert_program_status_database_error(self, mock_program_dao):
        """_do_insert_program_status() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_program_status_db_error,
                      'fail_insert_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._revision_id = 30
        DUT._do_insert_program_status()

        pub.unsubscribe(self.on_fail_insert_program_status_db_error,
                        'fail_insert_program_status')


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_program_status_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['status_id'] == 1
        assert attributes['cost_remaining'] == 284.98
        assert attributes['date_status'] == date.today() - timedelta(days=1)
        assert attributes['time_remaining'] == 125.0
        print(
            "\033[36m\nsucceed_get_program_status_attributes topic was broadcast.")

    def on_succeed_get_all_program_status_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['validation_id'] == 1
        assert attributes['name'] == 'PRF-0001'
        assert attributes['time_average'] == 0.0
        print(
            "\033[36m\nsucceed_get_program_status_attributes topic was broadcast.")

    def on_succeed_get_program_status_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['status'], RAMSTKProgramStatus)
        print("\033[36m\nsucceed_get_program_status_tree topic was broadcast")

    def on_request_get_program_status_tree(self):
        print("\033[36m\nrequest_get_program_status_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_program_status_attributes(self, mock_program_dao):
        """do_get_attributes() should return a dict of validation attributes on success."""
        pub.subscribe(self.on_succeed_get_program_status_attrs,
                      'succeed_get_program_status_attributes')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_attributes(1, 'status')

        pub.unsubscribe(self.on_succeed_get_program_status_attrs,
                        'succeed_get_program_status_attributes')

    @pytest.mark.unit
    def test_do_set_program_status_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_program_status_attributes',
                        node_id=[1],
                        package={'cost_remaining': 8321.54})
        assert DUT.do_select(
            1, table='status').cost_remaining == 8321.54

    @pytest.mark.unit
    def test_do_set_program_status_attributes_unknown_attr(self,
                                                           mock_program_dao):
        """do_set_attributes() should return None and leave all attributes unchanged if passed an attribute key that does not exist."""
        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_program_status_attributes',
                        node_id=[1],
                        package={'task_filliwonga': 'This is a filli-wonga.'})

        with pytest.raises(AttributeError):
            assert DUT.do_select(
                1,
                table='status').task_filliwonga == 'This is a filli-wonga.'

    @pytest.mark.unit
    def test_on_get_program_status_tree(self, mock_program_dao):
        """_on_get_status_tree() should return the status treelib Tree."""
        pub.subscribe(self.on_succeed_get_program_status_tree,
                      'succeed_get_program_status_tree')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_get_program_status_tree')

        pub.unsubscribe(self.on_succeed_get_program_status_tree,
                        'succeed_get_program_status_tree')

    @pytest.mark.unit
    def test_on_calculate_plan(self, mock_program_dao):
        """_do_set_attributes() should update program status on successful calculation of the plan."""
        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('succeed_calculate_all_validation_tasks',
                        cost_remaining=14608.45, time_remaining=469.00)

        _node_id = DUT._dic_status[date.today()]

        assert DUT.tree.get_node(
            _node_id).data['status'].cost_remaining == 14608.45
        assert DUT.tree.get_node(
            _node_id).data['status'].time_remaining == 469.00

    @pytest.mark.unit
    def test_on_calculate_plan_no_status_record(self, mock_program_dao):
        """_do_set_attributes() should update program status on successful calculation of the plan."""
        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._dic_status.pop(date.today())

        pub.sendMessage('succeed_calculate_all_validation_tasks',
                        cost_remaining=1408.45, time_remaining=49.00)

        _node_id = DUT._dic_status[date.today()]

        assert DUT.tree.get_node(
            _node_id).data['status'].cost_remaining == 1408.45
        assert DUT.tree.get_node(
            _node_id).data['status'].time_remaining == 49.00


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_program_status(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data['status'].cost_remaining == 47832.00
        assert tree.get_node(1).data['status'].time_remaining == 528.3
        print("\033[36m\nsucceed_update_program_status topic was broadcast")

    def on_fail_update_program_status(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent program status with '
            'status ID 100.')
        print("\033[35m\nfail_update_program_status topic was broadcast")

    def on_fail_update_program_status_no_data_package(self, error_message):
        assert error_message == ('do_update: No data package found for '
                                 'program status ID 1.')
        print("\033[35m\nfail_update_program_status topic was broadcast")

    def on_fail_update_program_status_wrong_data_type(self, error_message):
        assert error_message == (
            'do_update: The value for one or more attributes for program '
            'status ID 1 was the wrong type.'
        )
        print("\033[35m\nfail_update_program_status topic was broadcast")

    @pytest.mark.unit
    def test_do_update_program_status(self, mock_program_dao):
        """_do_update_program_status() should broadcast the 'succeed_update_program_status' message on success."""
        pub.subscribe(self.on_succeed_update_program_status,
                      'succeed_update_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.tree.get_node(1).data['status'].cost_remaining = 47832.00
        DUT.tree.get_node(1).data['status'].time_remaining = 528.3

        DUT.do_update(1)

        pub.unsubscribe(self.on_succeed_update_program_status,
                        'succeed_update_program_status')

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """ do_update() should raise the 'fail_update_validation' message when passed a Validation ID that doesn't exist. """
        pub.subscribe(self.on_fail_update_program_status,
                      'fail_update_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.do_update(100)

        pub.unsubscribe(self.on_fail_update_program_status,
                        'fail_update_program_status')

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """ do_update() should raise the 'fail_update_validation' message when passed a Validation ID that doesn't exist in the tree. """
        pub.subscribe(self.on_fail_update_program_status_no_data_package,
                      'fail_update_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data.pop('status')

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_program_status_no_data_package,
                        'fail_update_program_status')

    @pytest.mark.unit
    def test_do_update_wrong_data_type(self, mock_program_dao):
        """ do_update() should return a non-zero error code when passed a Requirement ID that doesn't exist. """
        pub.subscribe(self.on_fail_update_program_status_wrong_data_type,
                      'fail_update_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _status = DUT.do_select(1, table='status')
        _status.time_remaining = {1: 2}

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_program_status_wrong_data_type,
                        'fail_update_program_status')

    @pytest.mark.unit
    def test_do_update_wrong_data_type_root_node(self, mock_program_dao):
        """ do_update() should return a non-zero error code when passed
        a Requirement ID that doesn't exist. """
        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _status = DUT.do_select(1, table='status')
        _status.time_remaining = {1: 2}

        DUT.do_update(0)
