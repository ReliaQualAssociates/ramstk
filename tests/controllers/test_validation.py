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
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amValidation, dmValidation, mmValidation
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKProgramStatus, RAMSTKValidation

MOCK_STATUS = {
    1: {
        'cost_remaining': 284.98,
        'date_status': date.today() - timedelta(days=1),
        'time_remaining': 125.0
    },
    2: {
        'cost_remaining': 212.32,
        'date_status': date.today(),
        'time_remaining': 112.5
    }
}
MOCK_VALIDATIONS = {
    1: {
        'acceptable_maximum': 0.0,
        'acceptable_mean': 0.0,
        'acceptable_minimum': 0.0,
        'acceptable_variance': 0.0,
        'confidence': 95.0,
        'cost_average': 0.0,
        'cost_ll': 0.0,
        'cost_maximum': 0.0,
        'cost_mean': 0.0,
        'cost_minimum': 0.0,
        'cost_ul': 0.0,
        'cost_variance': 0.0,
        'date_end': date.today() + timedelta(days=30),
        'date_start': date.today(),
        'description': '',
        'measurement_unit': '',
        'name': '',
        'status': 0.0,
        'task_type': '',
        'task_specification': '',
        'time_average': 0.0,
        'time_ll': 0.0,
        'time_maximum': 0.0,
        'time_mean': 0.0,
        'time_minimum': 0.0,
        'time_ul': 0.0,
        'time_variance': 0.0
    },
    2: {
        'acceptable_maximum': 0.0,
        'acceptable_mean': 0.0,
        'acceptable_minimum': 0.0,
        'acceptable_variance': 0.0,
        'confidence': 95.0,
        'cost_average': 0.0,
        'cost_ll': 0.0,
        'cost_maximum': 0.0,
        'cost_mean': 0.0,
        'cost_minimum': 0.0,
        'cost_ul': 0.0,
        'cost_variance': 0.0,
        'date_end': date.today() + timedelta(days=20),
        'date_start': date.today() - timedelta(days=10),
        'description': '',
        'measurement_unit': '',
        'name': '',
        'status': 0.0,
        'task_type': '',
        'task_specification': '',
        'time_average': 0.0,
        'time_ll': 0.0,
        'time_maximum': 0.0,
        'time_mean': 0.0,
        'time_minimum': 0.0,
        'time_ul': 0.0,
        'time_variance': 0.0
    }
}


class MockDao:
    _all_validations = []
    _all_status = []

    def _do_delete_validation(self, record):
        for _idx, _validation in enumerate(self._all_validations):
            if _validation.validation_id == record.validation_id:
                self._all_validations.pop(_idx)

    def _do_delete_status(self, record):
        for _idx, _status in enumerate(self._all_status):
            if _status.status_id == record.status_id:
                self._all_status.pop(_idx)

    def do_delete(self, record):
        try:
            if record == RAMSTKValidation:
                self._do_delete_validation(record)
            elif record == RAMSTKProgramStatus:
                self._do_delete_status(record)
        except AttributeError:
            raise DataAccessError('')

    def do_insert(self, record):
        if record == RAMSTKValidation:
            self._all_validations.append(record)
        elif record == RAMSTKProgramStatus:
            self._all_status.append(record)

    def do_select_all(self, table, key, value):
        if table == RAMSTKValidation:
            self._all_validations = []
            for _key in MOCK_VALIDATIONS:
                _record = table()
                _record.revision_id = value
                _record.validation_id = _key
                _record.set_attributes(MOCK_VALIDATIONS[_key])
                self._all_validations.append(_record)
            return self._all_validations
        elif table == RAMSTKProgramStatus:
            self._all_status = []
            for _key in MOCK_STATUS:
                _record = table()
                _record.revision_id = value
                _record.status_id = _key
                _record.set_attributes(MOCK_STATUS[_key])
                self._all_status.append(_record)
            return self._all_status

    def _do_update_validation(self, record):
        for _key in MOCK_VALIDATIONS:
            if _key == record.validation_id:
                MOCK_VALIDATIONS[_key]['name'] = record.name
                MOCK_VALIDATIONS[_key]['time_maximum'] = record.time_maximum
                MOCK_VALIDATIONS[_key]['time_minimum'] = record.time_minimum
                MOCK_VALIDATIONS[_key]['time_average'] = record.time_average
                MOCK_VALIDATIONS[_key]['cost_minimum'] = record.cost_minimum
                MOCK_VALIDATIONS[_key]['cost_average'] = record.cost_average
                MOCK_VALIDATIONS[_key]['cost_maximum'] = record.cost_maximum
                MOCK_VALIDATIONS[_key]['confidence'] = record.confidence

    def _do_update_status(self, record):
        for _key in MOCK_STATUS:
            if _key == record.status_id:
                MOCK_STATUS[_key]['cost_remaining'] = record.cost_remaining
                MOCK_STATUS[_key]['time_remaining'] = record.time_remaining

    def do_update(self, record):
        if record == RAMSTKValidation:
            self._do_update_validation(record)
        elif record == RAMSTKProgramStatus:
            self._do_update_status(record)

@pytest.fixture
def mock_program_dao(monkeypatch):
    yield MockDao()


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager(self):
        """__init__() should return a Validation data manager."""
        DUT = dmValidation()

        assert isinstance(DUT, dmValidation)
        assert isinstance(DUT.tree, Tree)
        assert DUT.dao is None
        assert DUT._tag == 'validation'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'succeed_select_revision')
        assert pub.isSubscribed(DUT._do_delete_validation,
                                'request_delete_validation')
        assert pub.isSubscribed(DUT.do_insert, 'request_insert_validation')
        assert pub.isSubscribed(DUT.do_update, 'request_update_validation')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_validation')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_validation_attributes')
        assert pub.isSubscribed(DUT.do_get_all_attributes,
                                'request_get_all_validation_attributes')
        assert pub.isSubscribed(DUT.do_get_tree, 'request_get_validation_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_validation_attributes')
        assert pub.isSubscribed(DUT.do_set_all_attributes,
                                'request_set_all_validation_attributes')

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_toml_user_configuration):
        """__init__() should create an instance of the validation analysis manager."""
        DUT = amValidation(test_toml_user_configuration)

        assert isinstance(DUT, amValidation)
        assert isinstance(DUT.RAMSTK_CONFIGURATION, RAMSTKUserConfiguration)
        assert isinstance(DUT._attributes, dict)
        assert DUT._attributes == {}
        assert DUT._tree is None
        assert pub.isSubscribed(DUT.on_get_all_attributes,
                                'succeed_get_all_validation_attributes')
        assert pub.isSubscribed(DUT.on_get_tree, 'succeed_get_validation_tree')

    @pytest.mark.unit
    def test_matrix_manager_create(self):
        """__init__() should create an instance of the validation matrix manager."""
        DUT = mmValidation()

        assert isinstance(DUT, mmValidation)
        assert isinstance(DUT._col_tree, Tree)
        assert isinstance(DUT._col_tree, Tree)
        assert isinstance(DUT.dic_matrices, dict)
        assert DUT.n_row == 1
        assert DUT.n_col == 1
        assert pub.isSubscribed(DUT.do_load, 'succeed_retrieve_matrix')
        assert pub.isSubscribed(DUT._do_create, 'succeed_retrieve_validations')
        # assert pub.isSubscribed(DUT._do_delete_requirement,
        #                         'succeed_delete_requirement')
        assert pub.isSubscribed(DUT._do_delete_hardware,
                                'succeed_delete_hardware')
        assert pub.isSubscribed(DUT.do_delete_row, 'succeed_delete_validation')
        assert pub.isSubscribed(DUT.do_insert_row, 'succeed_insert_validation')
        # assert pub.isSubscribed(DUT._do_insert_requirement,
        #                         'succeed_insert_requirement')
        assert pub.isSubscribed(DUT._do_insert_hardware,
                                'succeed_insert_hardware')
        assert pub.isSubscribed(DUT.do_update,
                                'request_update_validation_matrix')
        assert pub.isSubscribed(DUT._on_get_tree,
                                'succeed_get_validation_tree')
        assert pub.isSubscribed(DUT._on_get_tree,
                                'succeed_get_requirement_tree')
        assert pub.isSubscribed(DUT._on_get_tree, 'succeed_get_hardware_tree')


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_retrieve_validations(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['validation'], RAMSTKValidation)
        print("\033[36m\nsucceed_retrieve_validations topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with RAMSTKValidation instances on success."""
        pub.subscribe(self.on_succeed_retrieve_validations,
                      'succeed_retrieve_validations')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)

        assert isinstance(
            DUT.status_tree.get_node(date.today()).data, dict)
        assert isinstance(
            DUT.status_tree.get_node(date.today()).data['status'],
            RAMSTKProgramStatus)
        assert DUT.status_tree.get_node(date.today()).data[
            'status'].status_id == 2
        assert DUT.status_tree.get_node(date.today()).data[
            'status'].cost_remaining == 212.32
        assert DUT.status_tree.get_node(date.today()).data[
            'status'].time_remaining == 112.5

        pub.unsubscribe(self.on_succeed_retrieve_validations,
                        'succeed_retrieve_validations')

    @pytest.mark.unit
    def test_do_select_validation(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKValidation on success."""
        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(revision_id=1)

        _validation = DUT.do_select(1, table='validation')

        assert isinstance(_validation, RAMSTKValidation)
        assert _validation.acceptable_maximum == 0.0
        assert _validation.name == ''

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is requested."""
        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(revision_id=1)

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Validation ID is requested."""
        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(revision_id=1)

        assert DUT.do_select(100, table='validation') is None

    # TODO: un-skip test_do_create_matrix in test_validation.py.
    @pytest.mark.skip
    def test_do_create_matrix(self, test_program_dao):
        """_do_create() should create an instance of the validation matrix manager."""
        DATAMGR = dmValidation()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = mmValidation()
        DUT._col_tree.create_node(tag='requirements',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0001',
                                  identifier=1,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='FUNC-0001',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0002',
                                  identifier=3,
                                  parent=0,
                                  data=None)

        pub.sendMessage('succeed_select_revision', revision_id=1)

        assert DUT.do_select('vldtn_rqrmnt', 1, 0) == 'REL-0001'
        assert DUT.do_select('vldtn_rqrmnt', 2, 0) == 'FUNC-0001'
        assert DUT.do_select('vldtn_rqrmnt', 3, 0) == 'REL-0002'
        assert DUT.do_select('vldtn_rqrmnt', 1, 1) == 0


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_validation(self, node_id):
        assert node_id == 2
        print("\033[36m\nsucceed_delete_validation topic was broadcast.")

    def on_fail_delete_validation(self, error_message):
        assert error_message == ('Validation ID 300 was not found as a node '
                                 'in the tree.')
        print("\033[35m\nfail_delete_validation topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete_validation(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib Tree."""
        pub.subscribe(self.on_succeed_delete_validation,
                      'succeed_delete_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT._do_delete_validation(DUT.last_id[0])

        assert DUT.last_id[0] == 1

        pub.unsubscribe(self.on_succeed_delete_validation,
                        'succeed_delete_validation')

    @pytest.mark.unit
    def test_do_delete_validation_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message."""
        pub.subscribe(self.on_fail_delete_validation, 'fail_delete_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT._do_delete_validation(300)

        pub.unsubscribe(self.on_fail_delete_validation,
                        'fail_delete_validation')

    # TODO: un-skip test_do_delete_matrix_column in test_validation.py.
    @pytest.mark.skip
    def test_do_delete_matrix_column(self, test_program_dao):
        """do_delete_column() should remove the appropriate column from the requested validation matrix."""
        DATAMGR = dmValidation()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = mmValidation()
        DUT._col_tree.create_node(tag='hardware',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='S1', identifier=1, parent=0, data=None)
        DUT._col_tree.create_node(tag='S1:SS1',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS2',
                                  identifier=3,
                                  parent=0,
                                  data=None)

        pub.sendMessage('succeed_select_revision', revision_id=1)

        assert DUT.do_select('vldtn_hrdwr', 1, 1) == 0

        pub.sendMessage('succeed_delete_hardware', node_id=1)

        with pytest.raises(KeyError):
            DUT.do_select('vldtn_hrdwr', 1, 1)

    # TODO: un-skip test_do_delete_matrix_row in test_validation.py.
    @pytest.mark.skip
    def test_do_delete_row(self, test_program_dao):
        """do_delete_row() should remove the appropriate row from the validation matrices."""
        DATAMGR = dmValidation()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = mmValidation()
        DUT._col_tree.create_node(tag='requirements',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0001',
                                  identifier=1,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='FUNC-0001',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0002',
                                  identifier=3,
                                  parent=0,
                                  data=None)

        pub.sendMessage('succeed_select_revision', revision_id=1)

        assert DUT.do_select('vldtn_rqrmnt', 1, 2) == 0

        pub.sendMessage('succeed_delete_validation', node_id=2)

        with pytest.raises(KeyError):
            DUT.do_select('vldtn_rqrmnt', 1, 2)


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_validation(self, node_id):
        assert node_id == 3
        print("\033[36m\nsucceed_insert_validation topic was broadcast.")

    def on_fail_insert_validation(self, error_msg):
        assert error_msg == ('Attempting to add a validation as a child of '
                             'non-existent parent node 40.')
        print("\033[35m\nfail_insert_validation topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert_validation(self, mock_program_dao):
        """do_insert() should send the success message after successfully inserting a validation task."""
        pub.subscribe(self.on_succeed_insert_validation,
                      'succeed_insert_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_insert()

        assert isinstance(
            DUT.tree.get_node(3).data['validation'], RAMSTKValidation)
        assert DUT.tree.get_node(3).data['validation'].validation_id == 3
        assert DUT.tree.get_node(
            3).data['validation'].name == 'New Validation Task'

        pub.unsubscribe(self.on_succeed_insert_validation,
                        'succeed_insert_validation')

    # TODO: un-skip test_do_insert_matrix_column in test_validation.py.
    @pytest.mark.skip
    def test_do_insert_matrix_column(self, test_program_dao):
        """do_insert_column() should add a column to the right of the requested validation matrix."""
        DATAMGR = dmValidation()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = mmValidation()
        DUT._col_tree.create_node(tag='hardware',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='S1', identifier=1, parent=0, data=None)
        DUT._col_tree.create_node(tag='S1:SS1',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS2',
                                  identifier=3,
                                  parent=0,
                                  data=None)

        pub.sendMessage('succeed_select_revision', revision_id=1)

        with pytest.raises(KeyError):
            DUT.do_select('vldtn_hrdwr', 4, 1)

        pub.sendMessage('succeed_insert_hardware', node_id=4)

        assert DUT.do_select('vldtn_hrdwr', 4, 1) == 0

    # TODO: un-skip test_do_insert_matrix_row in test_validation.py.
    @pytest.mark.skip
    def test_do_insert_row(self, test_program_dao):
        """do_insert_row() should add a row to the end of each validation matrix."""
        DATAMGR = dmValidation()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = mmValidation()
        DUT._col_tree.create_node(tag='requirements',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0001',
                                  identifier=1,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='FUNC-0001',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0002',
                                  identifier=3,
                                  parent=0,
                                  data=None)

        pub.sendMessage('succeed_select_revision', revision_id=1)

        with pytest.raises(KeyError):
            DUT.do_select('vldtn_rqrmnt', 1, 5)

        pub.sendMessage('succeed_insert_validation', node_id=5)

        assert DUT.do_select('vldtn_rqrmnt', 1, 5) == 0


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_validation_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['validation_id'] == 1
        assert attributes['name'] == ''
        assert attributes['time_average'] == 0.0
        print(
            "\033[36m\nsucceed_get_validation_attributes topic was broadcast.")

    def on_succeed_get_all_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['validation_id'] == 1
        assert attributes['name'] == ''
        print(
            "\033[36m\nsucceed_get_all_validation_attributes topic was broadcast"
        )

    def on_succeed_get_validation_tree(self, dmtree):
        assert isinstance(dmtree, Tree)
        assert isinstance(
            dmtree.get_node(1).data['validation'], RAMSTKValidation)
        print("\033[36m\nsucceed_get_validation_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes_validation(self, mock_program_dao):
        """do_get_attributes() should return a dict of validation attributes on success."""
        pub.subscribe(self.on_succeed_get_validation_attrs,
                      'succeed_get_validation_attributes')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_get_attributes(1, 'validation')

        pub.unsubscribe(self.on_succeed_get_validation_attrs,
                        'succeed_get_validation_attributes')

    @pytest.mark.unit
    def test_do_get_all_attributes_data_manager(self, mock_program_dao):
        """do_get_all_attributes() should return a dict of all RAMSTK data tables' attributes on success."""
        pub.subscribe(self.on_succeed_get_all_attrs,
                      'succeed_get_all_validation_attributes')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_get_all_attributes(1)

        pub.unsubscribe(self.on_succeed_get_all_attrs,
                        'succeed_get_all_validation_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(revision_id=1)

        pub.sendMessage('request_set_validation_attributes',
                        node_id=[1],
                        package={'task_specification': 'MIL-HDBK-217F'})
        assert DUT.do_select(
            1, table='validation').task_specification == 'MIL-HDBK-217F'

    @pytest.mark.unit
    def test_do_set_attributes_unknown_attr(self, mock_program_dao):
        """do_set_attributes() should return None and leave all attributes unchanged if passed an attribute key that does not exist."""
        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(revision_id=1)

        pub.sendMessage('request_set_validation_attributes',
                        node_id=[1],
                        package={'task_filliwonga': 'This is a filli-wonga.'})

        with pytest.raises(AttributeError):
            assert DUT.do_select(
                1,
                table='validation').task_filliwonga == 'This is a filli-wonga.'

    @pytest.mark.unit
    def test_do_set_all_attributes(self, mock_program_dao):
        """do_set_all_attributes() should send the success message."""
        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(revision_id=1)

        pub.sendMessage('request_set_all_validation_attributes',
                        attributes={
                            'validation_id':
                            1,
                            'task_specification':
                            'MIL-STD-1629A',
                            'description':
                            'This is a description added by a test.',
                        })
        assert DUT.do_select(
            1, table='validation').task_specification == 'MIL-STD-1629A'
        assert DUT.do_select(
            1, table='validation'
        ).description == 'This is a description added by a test.'

    @pytest.mark.unit
    def test_on_get_tree_data_manager(self, mock_program_dao):
        """on_get_tree() should return the validation treelib Tree."""
        pub.subscribe(self.on_succeed_get_validation_tree,
                      'succeed_get_validation_tree')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_validation_tree,
                        'succeed_get_validation_tree')

    @pytest.mark.unit
    def test_on_get_validation_tree(self, mock_program_dao):
        """_on_get_tree() should respond to the 'succeed_get_validation_tree' message and assign the tree to the _row_tree attribute."""
        DATAMGR = dmValidation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = mmValidation()

        pub.sendMessage('request_get_validation_tree')

        assert isinstance(DUT._row_tree, Tree)
        assert isinstance(DUT._row_tree.get_node(1).data, dict)
        assert isinstance(
            DUT._row_tree.get_node(1).data['validation'], RAMSTKValidation)
        assert DUT._row_tree.get_node(1).data['validation'].validation_id == 1
        assert DUT._row_tree.get_node(1).data[
            'validation'].description == ''

    @pytest.mark.integration
    def test_on_get_requirement_tree(self, test_program_dao):
        """_on_get_tree() should respond to the 'succeed_get_requirement_tree' message and assign the tree to the _col_tree attribute."""
        DATAMGR = dmValidation()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = mmValidation()

        _tree = Tree()
        _tree.create_node(tag='requirements',
                          identifier=0,
                          parent=None,
                          data=None)
        _tree.create_node(tag='REL-0001', identifier=1, parent=0, data=None)
        _tree.create_node(tag='FUNC-0001', identifier=2, parent=0, data=None)
        _tree.create_node(tag='REL-0002', identifier=3, parent=0, data=None)

        pub.sendMessage('succeed_get_requirement_tree', dmtree=_tree)

        assert isinstance(DUT._col_tree, Tree)
        assert DUT._col_tree.get_node(1).data is None


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_validation(self, node_id):
        assert node_id == 1
        print("\033[36m\nsucceed_update_validation topic was broadcast")

    def on_fail_update_validation(self, error_msg):
        assert error_msg == (
            'Attempted to save non-existent validation task with validation '
            'ID 100.')
        print("\033[35m\nfail_update_validation topic was broadcast")

    def on_succeed_update_status(self, node_id):
        assert node_id == date.today()
        print("\033[36m\nsucceed_update_program_status topic was broadcast")

    def on_succeed_update_matrix(self):
        assert True
        print("\033[36m\nsucceed_update_matrix topic was broadcast")

    @pytest.mark.integration
    def test_do_update_data_manager(self, test_program_dao):
        """ do_update() should return a zero error code on success. """
        pub.subscribe(self.on_succeed_update_validation,
                      'succeed_update_validation')

        DUT = dmValidation()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(revision_id=1)

        _validation = DUT.do_select(1, 'validation')
        _validation.name = 'Test Validation'
        _validation.time_maximum = 10.5
        DUT.do_update(1)

        DUT.do_select_all(revision_id=1)
        _validation = DUT.do_select(1, 'validation')

        assert _validation.name == 'Test Validation'
        assert _validation.time_maximum == 10.5

        pub.unsubscribe(self.on_succeed_update_validation,
                        'succeed_update_validation')

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """ do_update() should return a non-zero error code when passed a Validation ID that doesn't exist. """
        pub.subscribe(self.on_fail_update_validation, 'fail_update_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_update(100)

    @pytest.mark.integration
    def test_do_update_status(self, test_program_dao):
        """_do_update_program_status() should broadcast the 'succeed_update_program_status' message on success."""
        pub.subscribe(self.on_succeed_update_status,
                      'succeed_update_program_status')

        DUT = dmValidation()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT._do_update_program_status(47832.00, 528.3)

        DUT.do_select_all(revision_id=1)
        assert DUT.status_tree.get_node(
            date.today()).data['status'].cost_remaining == 47832.00
        assert DUT.status_tree.get_node(
            date.today()).data['status'].time_remaining == 528.3

        pub.unsubscribe(self.on_succeed_update_status,
                        'succeed_update_program_status')

    # TODO: un-skip test_do_update_matrix_manager in test_validation.py.
    @pytest.mark.skip
    def test_do_update_matrix_manager(self, test_program_dao):
        """do_update() should broadcast the 'succeed_update_matrix' on success."""
        DATAMGR = dmValidation()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = mmValidation()
        DUT._col_tree.create_node(tag='requirements',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0001',
                                  identifier=1,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='FUNC-0001',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='REL-0002',
                                  identifier=3,
                                  parent=0,
                                  data=None)

        pub.subscribe(self.on_succeed_update_matrix, 'succeed_update_matrix')

        pub.sendMessage('succeed_select_revision', revision_id=1)

        DUT.dic_matrices['vldtn_rqrmnt'][1][2] = 1
        DUT.dic_matrices['vldtn_rqrmnt'][1][3] = 2
        DUT.dic_matrices['vldtn_rqrmnt'][2][2] = 2
        DUT.dic_matrices['vldtn_rqrmnt'][3][5] = 1

        DUT.do_update(revision_id=1, matrix_type='vldtn_rqrmnt')

        pub.unsubscribe(self.on_succeed_update_matrix, 'succeed_update_matrix')


@pytest.mark.usefixtures('mock_program_dao', 'test_toml_user_configuration')
class TestAnalysisMethods():
    """Class for testing analytical methods."""
    @pytest.mark.unit
    def test_do_calculate_tasks(self, mock_program_dao,
                                test_toml_user_configuration):
        """do_calculate_tasks() should calculate the validation task time and cost."""
        DATAMGR = dmValidation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = amValidation(test_toml_user_configuration)

        pub.sendMessage('request_get_validation_tree')

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
        assert DUT._tree.get_node(
            1).data['validation'].cost_variance == pytest.approx(
                195069.44444444)
