# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_validation.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Validation algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pandas as pd
import pytest
from __mocks__ import (
    MOCK_FNCTN_TREE, MOCK_HRDWR_TREE,
    MOCK_RQRMNT_TREE, MOCK_STATUS, MOCK_VALIDATIONS
)
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amValidation, dmRequirement, dmValidation
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKProgramStatus, RAMSTKValidation


class MockDao:
    _all_validations = []

    def _do_delete_validation(self, record):
        _popped = False
        for _idx, _validation in enumerate(self._all_validations):
            if _validation.validation_id == record.validation_id:
                self._all_validations.pop(_idx)
                _popped = True

        if not _popped:
            self._all_validations.pop(record.validation_id)

    def do_delete(self, record):
        if record is None:
            raise DataAccessError('')
        elif isinstance(record, RAMSTKValidation):
            self._do_delete_validation(record)

    def do_insert(self, record):
        if record.revision_id == 30:
            raise DataAccessError('An error occurred with RAMSTK.')
        else:
            self._all_validations.append(record)

    def do_select_all(self,
                      table,
                      key=None,
                      value=None,
                      order=None,
                      _all=None):
        if table == RAMSTKValidation:
            self._all_validations = []
            for _key in MOCK_VALIDATIONS:
                _record = table()
                _record.revision_id = value
                _record.validation_id = _key
                _record.set_attributes(MOCK_VALIDATIONS[_key])
                self._all_validations.append(_record)
            return self._all_validations

    def do_update(self, record):
        if isinstance(record, RAMSTKValidation):
            for _key in MOCK_VALIDATIONS:
                if _key == record.validation_id:
                    MOCK_VALIDATIONS[_key]['name'] = record.name
                    MOCK_VALIDATIONS[_key][
                        'time_maximum'] = record.time_maximum
                    MOCK_VALIDATIONS[_key]['time_mean'] = float(
                        record.time_mean)
                    MOCK_VALIDATIONS[_key][
                        'time_minimum'] = record.time_minimum
                    MOCK_VALIDATIONS[_key][
                        'time_average'] = record.time_average
                    MOCK_VALIDATIONS[_key][
                        'cost_minimum'] = record.cost_minimum
                    MOCK_VALIDATIONS[_key][
                        'cost_average'] = record.cost_average
                    MOCK_VALIDATIONS[_key][
                        'cost_maximum'] = record.cost_maximum
                    MOCK_VALIDATIONS[_key]['confidence'] = record.confidence

    def get_last_id(self, table, id_column):
        return max(MOCK_VALIDATIONS.keys())


@pytest.fixture
def mock_program_dao(monkeypatch):
    yield MockDao()


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Validation data manager."""
        DUT = dmValidation()

        assert isinstance(DUT, dmValidation)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'validations'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_update, 'request_update_validation')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_validation')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_validation_attributes')
        assert pub.isSubscribed(DUT.do_get_tree,
                                'request_get_validations_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_validation_attributes')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_validation')
        assert pub.isSubscribed(DUT._do_insert_validation,
                                'request_insert_validation')

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_toml_user_configuration):
        """__init__() should create an instance of the validation analysis
        manager."""
        DUT = amValidation(test_toml_user_configuration)

        assert isinstance(DUT, amValidation)
        assert isinstance(DUT.RAMSTK_USER_CONFIGURATION,
                          RAMSTKUserConfiguration)
        assert isinstance(DUT._attributes, dict)
        assert isinstance(DUT._tree, Tree)
        assert isinstance(DUT._status_tree, Tree)
        assert DUT._attributes == {}
        assert pub.isSubscribed(DUT.on_get_all_attributes,
                                'succeed_get_all_validation_attributes')
        assert pub.isSubscribed(DUT.on_get_tree,
                                'succeed_get_validations_tree')
        assert pub.isSubscribed(DUT._on_get_status_tree,
                                'succeed_get_status_tree')
        assert pub.isSubscribed(DUT._do_calculate_task,
                                'request_calculate_validation_task')
        assert pub.isSubscribed(DUT._do_calculate_all_tasks,
                                'request_calculate_validation_tasks')
        assert pub.isSubscribed(DUT.do_calculate_plan,
                                'request_calculate_plan')


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_retrieve_validations(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['validation'], RAMSTKValidation)
        print("\033[36m\nsucceed_retrieve_validations topic was broadcast.")

    def on_request_select_matrix(self, matrix_type):
        assert matrix_type == 'vldtn_hrdwr'
        print("\033[36m\nrequest_select_matrix topic was broadcast for the "
              "vldtn_hrdwr matrix.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKValidation instances on success."""
        pub.subscribe(self.on_succeed_retrieve_validations,
                      'succeed_retrieve_validations')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_retrieve_validations,
                        'succeed_retrieve_validations')

    @pytest.mark.unit
    def test_do_select_validation(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKValidation on
        success."""
        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _validation = DUT.do_select(1, table='validation')

        assert isinstance(_validation, RAMSTKValidation)
        assert _validation.acceptable_maximum == 30.0
        assert _validation.name == 'PRF-0001'

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Validation ID is
        requested."""
        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='validation') is None


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_validation(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_validation topic was broadcast.")

    def on_fail_delete_validation(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent validation task ID 300.'
        )
        print("\033[35m\nfail_delete_validation topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete_validation(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete_validation,
                      'succeed_delete_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(DUT.last_id)

        assert DUT.last_id == 2

        pub.unsubscribe(self.on_succeed_delete_validation,
                        'succeed_delete_validation')

    @pytest.mark.unit
    def test_do_delete_validation_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to delete
        a record that doesn't exist in the database."""
        pub.subscribe(self.on_fail_delete_validation, 'fail_delete_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_validation,
                        'fail_delete_validation')


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_validation(self, node_id, tree):
        assert node_id == 4
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_validation topic was broadcast.")

    def on_fail_insert_validation(self, error_message):
        assert error_message == (
            'Attempting to add a validation as a child of '
            'non-existent parent node 40.')
        print("\033[35m\nfail_insert_validation topic was broadcast.")

    def on_fail_insert_validation_db_error(self, error_message):
        assert error_message == ('An error occurred with RAMSTK.')
        print("\033[35m\nfail_insert_validation topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert_validation(self, mock_program_dao):
        """_do_insert_validation() should send the success message after
        successfully inserting a validation task."""
        pub.subscribe(self.on_succeed_insert_validation,
                      'succeed_insert_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_validation(parent_id=0)

        assert isinstance(
            DUT.tree.get_node(4).data['validation'], RAMSTKValidation)
        assert DUT.tree.get_node(4).data['validation'].validation_id == 4
        assert DUT.tree.get_node(
            4).data['validation'].name == 'New Validation Task'

        pub.unsubscribe(self.on_succeed_insert_validation,
                        'succeed_insert_validation')

    @pytest.mark.unit
    def test_do_insert_validation_database_error(self, mock_program_dao):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_validation_db_error,
                      'fail_insert_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._revision_id = 30
        DUT._do_insert_validation(parent_id=0)

        pub.unsubscribe(self.on_fail_insert_validation_db_error,
                        'fail_insert_validation')


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_validation_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['validation_id'] == 1
        assert attributes['name'] == 'PRF-0001'
        assert attributes['time_average'] == 0.0
        print(
            "\033[36m\nsucceed_get_validation_attributes topic was broadcast.")

    def on_succeed_get_validation_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['validation'], RAMSTKValidation)
        print("\033[36m\nsucceed_get_validation_tree topic was broadcast")

    def on_request_get_validation_tree(self):
        print("\033[36m\nrequest_get_validation_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes_validation(self, mock_program_dao):
        """do_get_attributes() should return a dict of validation attributes on
        success."""
        pub.subscribe(self.on_succeed_get_validation_attrs,
                      'succeed_get_validation_attributes')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_attributes(1, 'validation')

        pub.unsubscribe(self.on_succeed_get_validation_attrs,
                        'succeed_get_validation_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_validation_attributes',
                        node_id=[1],
                        package={'task_specification': 'MIL-HDBK-217F'})
        assert DUT.do_select(
            1, table='validation').task_specification == 'MIL-HDBK-217F'

    @pytest.mark.unit
    def test_do_set_attributes_unknown_attr(self, mock_program_dao):
        """do_set_attributes() should return None and leave all attributes
        unchanged if passed an attribute key that does not exist."""
        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_validation_attributes',
                        node_id=[1],
                        package={'task_filliwonga': 'This is a filli-wonga.'})

        with pytest.raises(AttributeError):
            assert DUT.do_select(
                1,
                table='validation').task_filliwonga == 'This is a filli-wonga.'

    @pytest.mark.unit
    def test_on_get_validation_tree(self, mock_program_dao):
        """on_get_tree() should return the validation treelib Tree."""
        pub.subscribe(self.on_succeed_get_validation_tree,
                      'succeed_get_validation_tree')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_validation_tree,
                        'succeed_get_validation_tree')

    @pytest.mark.unit
    def test_analysis_manager_do_request_trees(self, mock_program_dao,
                                               test_toml_user_configuration):
        """_do_request_tree() should send the tree request messages."""
        pub.subscribe(self.on_request_get_validation_tree,
                      'request_get_validations_tree')

        DUT = amValidation(test_toml_user_configuration)

        DATAMGR = dmValidation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        assert isinstance(DUT._tree, Tree)
        assert isinstance(
            DUT._tree.get_node(1).data['validation'], RAMSTKValidation)

        pub.unsubscribe(self.on_request_get_validation_tree,
                        'request_get_validations_tree')


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_validation(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_update_validation topic was broadcast")

    def on_fail_update_validation(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent validation task with validation ID 100.'
        )
        print("\033[35m\nfail_update_validation topic was broadcast")

    def on_fail_update_validation_no_data_package(self, error_message):
        assert error_message == (
            'do_update: No data package found for validation task ID 1.')
        print("\033[35m\nfail_update_validation topic was broadcast")

    def on_fail_update_validation_wrong_data_type(self, error_message):
        assert error_message == (
            'do_update: The value for one or more attributes for validation '
            'task ID 1 was the wrong type.')
        print("\033[35m\nfail_update_validation topic was broadcast")

    @pytest.mark.unit
    def test_do_update_data_manager(self, mock_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update_validation,
                      'succeed_update_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _validation = DUT.do_select(1, 'validation')
        _validation.name = 'Test Validation'
        _validation.time_maximum = 10.5
        DUT.do_update(1)

        DUT.do_select_all(attributes={'revision_id': 1})
        _validation = DUT.do_select(1, 'validation')

        assert _validation.name == 'Test Validation'
        assert _validation.time_maximum == 10.5

        pub.unsubscribe(self.on_succeed_update_validation,
                        'succeed_update_validation')

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should raise the 'fail_update_validation' message when
        passed a Validation ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_validation, 'fail_update_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.do_update(100)

        pub.unsubscribe(self.on_fail_update_validation,
                        'fail_update_validation')

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update() should raise the 'fail_update_validation' message when
        passed a Validation ID that doesn't exist in the tree."""
        pub.subscribe(self.on_fail_update_validation_no_data_package,
                      'fail_update_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data.pop('validation')
        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_validation_no_data_package,
                        'fail_update_validation')

    @pytest.mark.unit
    def test_do_update_wrong_data_type(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_validation_wrong_data_type,
                      'fail_update_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _validation = DUT.do_select(1, table='validation')
        _validation.time_mean = {1: 2}

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_validation_wrong_data_type,
                        'fail_update_validation')

    @pytest.mark.unit
    def test_do_update_wrong_data_type_root_node(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _validation = DUT.do_select(1, table='validation')
        _validation.time_mean = {1: 2}

        DUT.do_update(0)


@pytest.mark.usefixtures('mock_program_dao', 'test_toml_user_configuration')
class TestAnalysisMethods():
    """Class for testing analytical methods."""
    def on_succeed_calculate_verification_plan(self, attributes):
        assert attributes['plan'].loc[pd.to_datetime(date.today()
                                               - timedelta(days=10)),
                                'lower'] == pytest.approx(50.0004502)
        assert attributes['plan'].loc[pd.to_datetime(date.today()
                                               + timedelta(days=20)),
                                'mean'] == pytest.approx(55.666667)
        assert attributes['plan'].loc[pd.to_datetime(date.today()
                                               + timedelta(days=30)),
                                'upper'] == 0.0
        assert attributes['assessed'].loc[pd.to_datetime(date.today()
                                                   + timedelta(days=30)),
                                    'lower'] == 10.0
        assert attributes['assessed'].loc[pd.to_datetime(date.today()
                                                   + timedelta(days=30)),
                                    'mean'] == 20.0
        assert attributes['assessed'].loc[pd.to_datetime(date.today()
                                                   + timedelta(days=30)),
                                    'upper'] == 30.0
        print(
            "\033[36m\nsucceed_calculate_verification_plan topic was broadcast"
        )

    @pytest.mark.skip
    def test_do_select_actuals(self, mock_program_dao,
                               test_toml_user_configuration):
        """_do_select_actuals() should return a pandas DataFrame() containing
        actual plan status."""
        DATAMGR = dmValidation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT = amValidation(test_toml_user_configuration)

        pub.sendMessage('request_get_status_tree')

        _actuals = DUT._do_select_actuals()

        assert isinstance(_actuals, pd.DataFrame)
        assert _actuals.loc[pd.to_datetime(date.today()), 'cost'] == 212.32
        assert _actuals.loc[pd.to_datetime(date.today()), 'time'] == 112.5

    @pytest.mark.unit
    def test_do_calculate_task(self, mock_program_dao,
                               test_toml_user_configuration):
        """do_calculate_task() should calculate the validation task time and
        cost."""
        DATAMGR = dmValidation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DUT = amValidation(test_toml_user_configuration)

        pub.sendMessage('request_get_validations_tree')

        _validation = DATAMGR.do_select(1, 'validation')
        _validation.time_minimum = 10.0
        _validation.time_average = 20.0
        _validation.time_maximum = 40.0
        _validation.cost_minimum = 1850.0
        _validation.cost_average = 2200.0
        _validation.cost_maximum = 4500.0
        _validation.confidence = 95.0
        DATAMGR.do_update(1)

        pub.sendMessage('request_calculate_validation_task', node_id=1)

        assert DUT._tree.get_node(
            1).data['validation'].time_ll == pytest.approx(11.86684674)
        assert DUT._tree.get_node(
            1).data['validation'].time_mean == pytest.approx(21.66666667)
        assert DUT._tree.get_node(
            1).data['validation'].time_ul == pytest.approx(31.46648659)
        assert DUT._tree.get_node(1).data['validation'].time_variance == 25.0
        assert DUT._tree.get_node(
            1).data['validation'].cost_ll == pytest.approx(1659.34924016)
        assert DUT._tree.get_node(
            1).data['validation'].cost_mean == pytest.approx(2525.0)
        assert DUT._tree.get_node(
            1).data['validation'].cost_ul == pytest.approx(3390.65075984)
        assert DUT._tree.get_node(1).data[
            'validation'].cost_variance == pytest.approx(195069.44444444)

    @pytest.mark.unit
    def test_do_calculate_all_tasks(self, mock_program_dao,
                                    test_toml_user_configuration):
        """_do_calculate_all_tasks() should calculate the validation tasks time
        and cost."""
        DATAMGR = dmValidation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DUT = amValidation(test_toml_user_configuration)

        pub.sendMessage('request_get_validations_tree')

        _validation = DATAMGR.do_select(1, 'validation')
        _validation.time_minimum = 10.0
        _validation.time_average = 20.0
        _validation.time_maximum = 40.0
        _validation.cost_minimum = 1850.0
        _validation.cost_average = 2200.0
        _validation.cost_maximum = 4500.0
        _validation.confidence = 95.0
        DATAMGR.do_update(1)

        pub.sendMessage('request_calculate_validation_tasks')

        assert DUT._tree.get_node(
            1).data['validation'].time_ll == pytest.approx(11.86684674)
        assert DUT._tree.get_node(
            1).data['validation'].time_mean == pytest.approx(21.66666667)
        assert DUT._tree.get_node(
            1).data['validation'].time_ul == pytest.approx(31.46648659)
        assert DUT._tree.get_node(1).data['validation'].time_variance == 25.0
        assert DUT._tree.get_node(
            1).data['validation'].cost_ll == pytest.approx(1659.34924016)
        assert DUT._tree.get_node(
            1).data['validation'].cost_mean == pytest.approx(2525.0)
        assert DUT._tree.get_node(
            1).data['validation'].cost_ul == pytest.approx(3390.65075984)
        assert DUT._tree.get_node(1).data[
            'validation'].cost_variance == pytest.approx(195069.44444444)

    @pytest.mark.unit
    def test_do_calculate_verification_plan(self, mock_program_dao,
                                            test_toml_user_configuration):
        """do_calculate_plan() should calculate the planned validation effort
        time and cost."""
        pub.subscribe(self.on_succeed_calculate_verification_plan,
                      'succeed_calculate_verification_plan')

        DATAMGR = dmValidation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DUT = amValidation(test_toml_user_configuration)

        pub.sendMessage('request_get_validations_tree')

        _validation = DATAMGR.do_select(1, 'validation')
        _validation.time_minimum = 10.0
        _validation.time_average = 20.0
        _validation.time_maximum = 40.0
        _validation.time_mean = 0.0
        _validation.cost_minimum = 1850.0
        _validation.cost_average = 2200.0
        _validation.cost_maximum = 4500.0
        _validation.confidence = 95.0
        DATAMGR.do_update(1)
        _validation = DATAMGR.do_select(2, 'validation')
        _validation.time_minimum = 15.0
        _validation.time_average = 32.0
        _validation.time_maximum = 60.0
        _validation.time_mean = 0.0
        _validation.cost_minimum = 750.0
        _validation.cost_average = 1200.0
        _validation.cost_maximum = 2500.0
        _validation.confidence = 95.0
        DATAMGR.do_update(2)

        pub.sendMessage('request_calculate_plan')

        pub.unsubscribe(self.on_succeed_calculate_verification_plan,
                        'succeed_calculate_verification_plan')
