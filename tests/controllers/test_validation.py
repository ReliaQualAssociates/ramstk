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
from ramstk import Configuration
from ramstk.controllers.validation import amValidation, dmValidation
from ramstk.dao import DAO
from ramstk.models.programdb import RAMSTKValidation

ATTRIBUTES = {
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
    'description': b'',
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


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager(self, test_program_dao):
        """__init__() should return a Validation data manager."""
        DUT = dmValidation(test_program_dao)

        assert isinstance(DUT, dmValidation)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, DAO)
        assert DUT._tag == 'validation'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'succeed_select_revision')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_validation')
        assert pub.isSubscribed(DUT.do_insert, 'request_insert_validation')
        assert pub.isSubscribed(DUT.do_update, 'request_update_validation')
        assert pub.isSubscribed(DUT.do_update_all, 'request_update_all_validation')
        assert pub.isSubscribed(DUT.do_get_attributes, 'request_get_validation_attributes')
        assert pub.isSubscribed(DUT.do_get_all_attributes, 'request_get_all_validation_attributes')
        assert pub.isSubscribed(DUT.do_get_tree, 'request_get_validation_tree')
        assert pub.isSubscribed(DUT.do_set_attributes, 'request_set_validation_attributes')
        assert pub.isSubscribed(DUT.do_set_all_attributes, 'request_set_all_validation_attributes')

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_configuration):
        """__init__() should create an instance of the validation analysis manager."""
        DUT = amValidation(test_configuration)

        assert isinstance(DUT, amValidation)
        assert isinstance(DUT.RAMSTK_CONFIGURATION, Configuration)
        assert isinstance(DUT._attributes, dict)
        assert DUT._attributes == {}
        assert DUT._tree is None
        assert pub.isSubscribed(DUT.on_get_all_attributes,
                                'succeed_get_all_validation_attributes')
        assert pub.isSubscribed(DUT.on_get_tree, 'succeed_get_validation_tree')


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_retrieve_validations(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['validation'], RAMSTKValidation)
        print("\033[36m\nsucceed_retrieve_validations topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all(self, test_program_dao):
        """do_select_all() should return a Tree() object populated with RAMSTKValidation instances on success."""
        pub.subscribe(self.on_succeed_retrieve_validations, 'succeed_retrieve_validations')

        DUT = dmValidation(test_program_dao)
        DUT.do_select_all(1)

        pub.unsubscribe(self.on_succeed_retrieve_validations, 'succeed_retrieve_validations')

    @pytest.mark.integration
    def test_do_select_validation(self, test_program_dao):
        """do_select() should return an instance of the RAMSTKValidation on success."""
        DUT = dmValidation(test_program_dao)
        DUT.do_select_all(revision_id=1)

        _validation = DUT.do_select(1, table='validation')

        assert isinstance(_validation, RAMSTKValidation)
        assert _validation.acceptable_maximum == 0.0
        assert _validation.name == ''

    @pytest.mark.integration
    def test_do_select_unknown_table(self, test_program_dao):
        """do_select() should raise a KeyError when an unknown table name is requested."""
        DUT = dmValidation(test_program_dao)
        DUT.do_select_all(revision_id=1)

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.integration
    def test_do_select_non_existent_id(self, test_program_dao):
        """do_select() should return None when a non-existent Validation ID is requested."""
        DUT = dmValidation(test_program_dao)
        DUT.do_select_all(revision_id=1)

        assert DUT.do_select(100, table='validation') is None


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_validation(self, node_id):
        assert node_id == 3
        print("\033[36m\nsucceed_delete_validation topic was broadcast.")

    def on_fail_delete_validation(self, error_msg):
        assert error_msg == ('Attempted to delete non-existent validation ID '
                             '300.')
        print("\033[35m\nfail_delete_validation topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete_validation(self, test_program_dao):
        """_do_delete() should send the success message with the treelib Tree."""
        pub.subscribe(self.on_succeed_delete_validation, 'succeed_delete_validation')

        DUT = dmValidation(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT._do_delete(DUT.last_id)

        assert DUT.last_id == 2

    @pytest.mark.integration
    def test_do_delete_validation_non_existent_id(self, test_program_dao):
        """_do_delete() should send the fail message."""
        pub.subscribe(self.on_fail_delete_validation, 'fail_delete_validation')

        DUT = dmValidation(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT._do_delete(300)


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_validation(self, node_id):
        assert node_id == 4
        print("\033[36m\nsucceed_insert_validation topic was broadcast.")

    def on_fail_insert_validation(self, error_msg):
        assert error_msg == ('Attempting to add a validation as a child of '
                             'non-existent parent node 40.')
        print("\033[35m\nfail_insert_validation topic was broadcast.")

    def on_succeed_insert_hazard(self, node_id):
        assert node_id == 4
        print("\033[36m\nsucceed_insert_hazard topic was broadcast.")

    def on_fail_insert_hazard(self, error_msg):
        assert error_msg == ('Attempting to add a hazard to a non-existent '
                             'validation ID 10.')
        print("\033[35m\nfail_insert_hazard topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_validation(self, test_program_dao):
        """do_insert() should send the success message after successfully inserting a validation task."""
        pub.subscribe(self.on_succeed_insert_validation, 'succeed_insert_validation')

        DUT = dmValidation(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_insert()

        assert isinstance(DUT.tree.get_node(4).data['validation'], RAMSTKValidation)
        assert DUT.tree.get_node(4).data['validation'].validation_id == 4
        assert DUT.tree.get_node(4).data['validation'].name == 'New Validation Task'

        pub.unsubscribe(self.on_succeed_insert_validation, 'succeed_insert_validation')


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_validation_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['validation_id'] == 1
        assert attributes['name'] == ''
        assert attributes['time_average'] == 0.0
        print("\033[36m\nsucceed_get_validation_attributes topic was broadcast.")

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

    @pytest.mark.integration
    def test_do_get_attributes_validation(self, test_program_dao):
        """do_get_attributes() should return a dict of validation attributes on success."""
        pub.subscribe(self.on_succeed_get_validation_attrs, 'succeed_get_validation_attributes')

        DUT = dmValidation(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_get_attributes(1, 'validation')

    @pytest.mark.integration
    def test_do_get_all_attributes_data_manager(self, test_program_dao):
        """do_get_all_attributes() should return a dict of all RAMSTK data tables' attributes on success."""
        pub.subscribe(self.on_succeed_get_all_attrs, 'succeed_get_all_validation_attributes')

        DUT = dmValidation(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_get_all_attributes(1)

        pub.unsubscribe(self.on_succeed_get_all_attrs, 'succeed_get_all_validation_attributes')

    @pytest.mark.integration
    def test_do_set_attributes(self, test_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmValidation(test_program_dao)
        DUT.do_select_all(revision_id=1)

        pub.sendMessage('request_set_validation_attributes',
                        node_id=1,
                        key='task_specification',
                        value='MIL-HDBK-217F')
        assert DUT.do_select(
            1, table='validation').task_specification == 'MIL-HDBK-217F'

    @pytest.mark.integration
    def test_do_set_all_attributes(self, test_program_dao):
        """do_set_all_attributes() should send the success message."""
        DUT = dmValidation(test_program_dao)
        DUT.do_select_all(revision_id=1)

        pub.sendMessage('request_set_all_validation_attributes',
                        attributes={
                            'validation_id': 1,
                            'task_specification': 'MIL-STD-1629A',
                            'description': b'This is a description added by a test.',
                        })
        assert DUT.do_select(1, table='validation').task_specification == 'MIL-STD-1629A'
        assert DUT.do_select(
            1,
            table='validation').description == b'This is a description added by a test.'

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self, test_program_dao):
        """on_get_tree() should return the validation treelib Tree."""
        pub.subscribe(self.on_succeed_get_validation_tree, 'succeed_get_validation_tree')

        DUT = dmValidation(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_validation_tree, 'succeed_get_validation_tree')


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
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

    @pytest.mark.integration
    def test_do_update_data_manager(self, test_program_dao):
        """ do_update() should return a zero error code on success. """
        pub.subscribe(self.on_succeed_update_validation, 'succeed_update_validation')

        DUT = dmValidation(test_program_dao)
        DUT.do_select_all(revision_id=1)

        DUT.tree.get_node(1).data['validation'].name = 'Test Validation'
        DUT.tree.get_node(1).data['validation'].time_maximum = 10.5
        DUT.do_update(1)

        DUT.do_select_all(revision_id=1)
        assert DUT.tree.get_node(1).data['validation'].name == 'Test Validation'
        assert DUT.tree.get_node(1).data['validation'].time_maximum == 10.5

        pub.unsubscribe(self.on_succeed_update_validation, 'succeed_update_validation')

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_program_dao):
        """ do_update() should return a non-zero error code when passed a Validation ID that doesn't exist. """
        pub.subscribe(self.on_fail_update_validation, 'fail_update_validation')

        DUT = dmValidation(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_update(100)


#@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
#class TestAnalysisMethods():
#    """Class for testing analytical methods."""
