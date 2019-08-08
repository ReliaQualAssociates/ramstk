# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_function.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Function algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk import Configuration
from ramstk.controllers import amFunction, dmFunction
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKFunction, RAMSTKHazardAnalysis

ATTRIBUTES = {
    'type_id': 0,
    'total_part_count': 0,
    'availability_mission': 1.0,
    'cost': 0.0,
    'hazard_rate_mission': 0.0,
    'mpmt': 0.0,
    'parent_id': 0,
    'mtbf_logistics': 0.0,
    'safety_critical': 0,
    'mmt': 0.0,
    'hazard_rate_logistics': 0.0,
    'remarks': '',
    'mtbf_mission': 0.0,
    'function_code': 'PRESS-001',
    'name': 'Function Name',
    'level': 0,
    'mttr': 0.0,
    'mcmt': 0.0,
    'availability_logistics': 1.0,
    'total_mode_count': 0,
}


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager(self, test_program_dao):
        """__init__() should return a Function data manager."""
        DUT = dmFunction(test_program_dao)

        assert isinstance(DUT, dmFunction)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'function'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'succeed_select_revision')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_function')
        assert pub.isSubscribed(DUT._do_delete_hazard, 'request_delete_hazard')
        assert pub.isSubscribed(DUT.do_insert, 'request_insert_function')
        assert pub.isSubscribed(DUT.do_insert_hazard, 'request_insert_hazard')
        assert pub.isSubscribed(DUT.do_update, 'request_update_function')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_functions')
        assert pub.isSubscribed(DUT._do_get_attributes,
                                'request_get_function_attributes')
        assert pub.isSubscribed(DUT.do_get_all_attributes,
                                'request_get_all_function_attributes')
        assert pub.isSubscribed(DUT.do_get_tree, 'request_get_function_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_function_attributes')
        assert pub.isSubscribed(DUT.do_set_all_attributes,
                                'request_set_all_function_attributes')

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_configuration):
        """__init__() should create an instance of the function analysis manager."""
        DUT = amFunction(test_configuration)

        assert isinstance(DUT, amFunction)
        assert isinstance(DUT.RAMSTK_CONFIGURATION, Configuration)
        assert isinstance(DUT._attributes, dict)
        assert DUT._attributes == {}
        assert DUT._tree is None
        assert pub.isSubscribed(DUT.on_get_all_attributes,
                                'succeed_get_all_function_attributes')
        assert pub.isSubscribed(DUT.on_get_tree, 'succeed_get_function_tree')
        assert pub.isSubscribed(DUT.do_calculate_fha, 'request_calculate_fha')


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_retrieve_functions(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data['function'], RAMSTKFunction)
        assert isinstance(tree.get_node(1).data['hazards'], dict)
        assert isinstance(
            tree.get_node(1).data['hazards'][1], RAMSTKHazardAnalysis)
        print("\033[36m\nsucceed_retrieve_functions topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all(self, test_program_dao):
        """do_select_all() should return a Tree() object populated with RAMSTKFunction instances on success."""
        pub.subscribe(self.on_succeed_retrieve_functions,
                      'succeed_retrieve_functions')

        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(1)

        pub.unsubscribe(self.on_succeed_retrieve_functions,
                        'succeed_retrieve_functions')

    @pytest.mark.integration
    def test_do_select_function(self, test_program_dao):
        """do_select() should return an instance of the RAMSTKFunction on success."""
        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)

        _function = DUT.do_select(1, table='function')

        assert isinstance(_function, RAMSTKFunction)
        assert _function.availability_logistics == 1.0
        assert _function.name == 'Function Name'

    @pytest.mark.integration
    def test_do_select_hazards(self, test_program_dao):
        """do_select() should return an instance of RAMSTKHazardAnalysis on success."""
        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)

        _failure_definition = DUT.do_select(1, table='hazards')

        assert isinstance(_failure_definition, dict)
        assert isinstance(_failure_definition[1], RAMSTKHazardAnalysis)
        assert _failure_definition[1].potential_hazard == ''

    @pytest.mark.integration
    def test_do_select_unknown_table(self, test_program_dao):
        """do_select() should raise a KeyError when an unknown table name is requested."""
        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.integration
    def test_do_select_non_existent_id(self, test_program_dao):
        """do_select() should return None when a non-existent Function ID is requested."""
        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)

        assert DUT.do_select(100, table='function') is None


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_function(self, node_id):
        assert node_id == 3
        print("\033[36m\nsucceed_delete_function topic was broadcast.")

    def on_fail_delete_function(self, error_msg):
        assert error_msg == ('Attempted to delete non-existent function ID '
                             '300.')
        print("\033[35m\nfail_delete_function topic was broadcast.")

    def on_succeed_delete_hazard(self, node_id):
        assert node_id == 2
        print("\033[36m\nsucceed_delete_hazard topic was broadcast.")

    def on_fail_delete_hazard(self, error_msg):
        assert error_msg == ('Attempted to delete non-existent hazard ID 10 '
                             'from function ID 1.')
        print("\033[35m\nfail_delete_hazard topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete_function(self, test_program_dao):
        """_do_delete() should send the success message with the treelib Tree."""
        pub.subscribe(self.on_succeed_delete_function,
                      'succeed_delete_function')

        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT._do_delete(DUT.last_id)

        assert DUT.last_id == 2

    @pytest.mark.integration
    def test_do_delete_function_non_existent_id(self, test_program_dao):
        """_do_delete() should send the fail message."""
        pub.subscribe(self.on_fail_delete_function, 'fail_delete_function')

        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT._do_delete(300)

    @pytest.mark.integration
    def test_do_delete_hazard(self, test_program_dao):
        """_do_delete_hazard() should send the success method when a hazard is successfully deleted."""
        pub.subscribe(self.on_succeed_delete_hazard, 'succeed_delete_hazard')

        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT._do_delete_hazard(2, 2)

        assert DUT.tree.get_node(2).data['hazards'] == {}

    @pytest.mark.integration
    def test_do_delete_hazard_non_existent_id(self, test_program_dao):
        """_do_delete_hazard() should send the success method when a hazard is successfully deleted."""
        pub.subscribe(self.on_fail_delete_hazard, 'fail_delete_hazard')

        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT._do_delete_hazard(1, 10)


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_function(self, node_id):
        assert node_id == 4
        print("\033[36m\nsucceed_insert_function topic was broadcast.")

    def on_fail_insert_function(self, error_msg):
        assert error_msg == ('Attempting to add a function as a child of '
                             'non-existent parent node 40.')
        print("\033[35m\nfail_insert_function topic was broadcast.")

    def on_succeed_insert_hazard(self, node_id):
        assert node_id == 4
        print("\033[36m\nsucceed_insert_hazard topic was broadcast.")

    def on_fail_insert_hazard(self, error_msg):
        assert error_msg == ('Attempting to add a hazard to a non-existent '
                             'function ID 10.')
        print("\033[35m\nfail_insert_hazard topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling_function(self, test_program_dao):
        """do_insert() should send the success message after successfully inserting a sibling function."""
        pub.subscribe(self.on_succeed_insert_function,
                      'succeed_insert_function')

        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_insert()

        assert isinstance(
            DUT.tree.get_node(4).data['function'], RAMSTKFunction)
        assert DUT.tree.get_node(4).data['function'].function_id == 4
        assert DUT.tree.get_node(4).data['function'].name == 'New Function'
        assert DUT.tree.get_node(4).data['hazards'] == {}

        pub.unsubscribe(self.on_succeed_insert_function,
                        'succeed_insert_function')

    @pytest.mark.integration
    def test_do_insert_child_function(self, test_program_dao):
        """do_insert() should send the success message after successfully inserting a child function."""
        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_insert(parent_id=4)

        assert isinstance(
            DUT.tree.get_node(5).data['function'], RAMSTKFunction)
        assert DUT.tree.get_node(5).data['function'].function_id == 5
        assert DUT.tree.get_node(5).data['function'].name == 'New Function'
        assert DUT.tree.get_node(5).data['hazards'] == {}

    @pytest.mark.integration
    def test_do_insert_function_no_parent(self, test_program_dao):
        """do_insert() should send the fail message if attempting to add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_function, 'fail_insert_function')

        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_insert(parent_id=40)

    @pytest.mark.integration
    def test_insert_hazard(self, test_program_dao):
        """do_insert_hazard() should send the success message after successfully inserting a new hazard."""
        pub.subscribe(self.on_succeed_insert_hazard, 'succeed_insert_hazard')

        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_insert_hazard(1)

        assert isinstance(
            DUT.tree.get_node(1).data['hazards'][4], RAMSTKHazardAnalysis)

    @pytest.mark.integration
    def test_insert_hazard_no_function(self, test_program_dao):
        """do_insert_hazard() should send the fail message when attempting to add a hazard to a non-existent function ID."""
        pub.subscribe(self.on_fail_insert_hazard, 'fail_insert_hazard')

        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_insert_hazard(function_id=10)


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_function_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['function_id'] == 1
        assert attributes['name'] == 'Function Name'
        assert attributes['safety_critical'] == 0
        print("\033[36m\nsucceed_get_function_attributes topic was broadcast.")

    def on_succeed_get_hazard_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes[1].function_id == 1
        assert attributes[1].potential_hazard == ''
        print("\033[36m\nsucceed_get_hazards_attributes topic was broadcast.")

    def on_succeed_get_all_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['function_id'] == 1
        assert attributes['name'] == 'Function Name'
        assert isinstance(attributes['hazards'], dict)
        assert isinstance(attributes['hazards'][1], RAMSTKHazardAnalysis)
        assert attributes['hazards'][1].function_id == 1
        print(
            "\033[36m\nsucceed_get_all_function_attributes topic was broadcast"
        )

    def on_succeed_get_function_tree(self, dmtree):
        assert isinstance(dmtree, Tree)
        assert isinstance(dmtree.get_node(1).data['function'], RAMSTKFunction)
        assert isinstance(dmtree.get_node(1).data['hazards'], dict)
        assert isinstance(
            dmtree.get_node(1).data['hazards'][1], RAMSTKHazardAnalysis)
        print("\033[36m\nsucceed_get_function_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes_function(self, test_program_dao):
        """_do_get_attributes() should return a dict of function attributes on success."""
        pub.subscribe(self.on_succeed_get_function_attrs,
                      'succeed_get_function_attributes')

        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT._do_get_attributes(1, 'function')

    @pytest.mark.integration
    def test_do_get_attributes_hazards(self, test_program_dao):
        """_do_get_attributes() should return a dict of failure definition records on success."""
        pub.subscribe(self.on_succeed_get_hazard_attrs,
                      'succeed_get_hazards_attributes')

        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT._do_get_attributes(1, 'hazards')

    @pytest.mark.integration
    def test_do_get_all_attributes_data_manager(self, test_program_dao):
        """do_get_all_attributes() should return a dict of all RAMSTK data tables' attributes on success."""
        pub.subscribe(self.on_succeed_get_all_attrs,
                      'succeed_get_all_function_attributes')

        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_get_all_attributes(1)

        pub.unsubscribe(self.on_succeed_get_all_attrs,
                        'succeed_get_all_function_attributes')

    @pytest.mark.integration
    def test_do_set_attributes(self, test_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)

        pub.sendMessage('request_set_function_attributes',
                        node_id=1,
                        key='function_code',
                        value='-')
        pub.sendMessage('request_set_function_attributes',
                        node_id=1,
                        key='potential_hazard',
                        value='Donald Trump',
                        hazard_id=1)
        assert DUT.do_select(1, table='function').function_code == '-'
        assert DUT.do_select(
            1, table='hazards')[1].potential_hazard == 'Donald Trump'

    @pytest.mark.integration
    def test_do_set_all_attributes(self, test_program_dao):
        """do_set_all_attributes() should send the success message."""
        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)

        pub.sendMessage('request_set_all_function_attributes',
                        attributes={
                            'function_id': 1,
                            'function_code': '1',
                            'remarks': b'These are remarks added by a test.',
                            'potential_cause': 'Apathy',
                            'potential_hazard': 'Donald Trump & family'
                        },
                        hazard_id=1)
        assert DUT.do_select(1, table='function').function_code == '1'
        assert DUT.do_select(
            1,
            table='function').remarks == b'These are remarks added by a test.'
        assert DUT.do_select(1, table='hazards')[1].potential_cause == 'Apathy'
        assert DUT.do_select(
            1, table='hazards')[1].potential_hazard == 'Donald Trump & family'

        pub.sendMessage('request_set_all_function_attributes',
                        attributes={
                            'function_id': 1,
                            'function_code': '',
                            'remarks': b'',
                            'potential_cause': '',
                            'potential_hazard': ''
                        },
                        hazard_id=1)

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self, test_program_dao):
        """on_get_tree() should return the function treelib Tree."""
        pub.subscribe(self.on_succeed_get_function_tree,
                      'succeed_get_function_tree')

        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_function_tree,
                        'succeed_get_function_tree')

    @pytest.mark.integration
    def test_get_all_attributes_analysis_manager(self, test_program_dao,
                                                 test_configuration):
        """_get_all_attributes() should update the attributes dict on success."""
        DATAMGR = dmFunction(test_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = amFunction(test_configuration)

        pub.sendMessage('request_get_all_function_attributes', node_id=1)

        assert isinstance(DUT._attributes['hazards'][1], RAMSTKHazardAnalysis)
        assert DUT._attributes['revision_id'] == 1
        assert DUT._attributes['function_id'] == 1
        assert DUT._attributes['availability_logistics'] == 1.0

    @pytest.mark.integration
    def test_on_get_tree_analysis_manager(self, test_program_dao,
                                          test_configuration):
        """_on_get_tree() should assign the data manager's tree to the _tree attribute in response to the succeed_get_function_tree message."""
        DATAMGR = dmFunction(test_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = amFunction(test_configuration)
        DATAMGR.do_get_tree()

        assert isinstance(DUT._tree, Tree)
        assert isinstance(
            DUT._tree.get_node(1).data['hazards'][1], RAMSTKHazardAnalysis)


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_function(self, node_id):
        assert node_id == 1
        print("\033[36m\nsucceed_update_function topic was broadcast")

    def on_fail_update_function(self, error_msg):
        assert error_msg == (
            'Attempted to save non-existent function with function ID 100.')
        print("\033[35m\nfail_update_function topic was broadcast")

    @pytest.mark.integration
    def test_do_update_data_manager(self, test_program_dao):
        """ do_update() should return a zero error code on success. """
        pub.subscribe(self.on_succeed_update_function,
                      'succeed_update_function')

        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)

        DUT.tree.get_node(1).data['function'].name = 'Test Function'
        DUT.tree.get_node(1).data['hazards'][1].potential_hazard = 'Big Hazard'
        DUT.do_update(1)

        DUT.do_select_all(revision_id=1)
        assert DUT.tree.get_node(1).data['function'].name == 'Test Function'
        assert DUT.tree.get_node(
            1).data['hazards'][1].potential_hazard == 'Big Hazard'

        pub.unsubscribe(self.on_succeed_update_function,
                        'succeed_update_function')

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_program_dao):
        """ do_update() should return a non-zero error code when passed a Function ID that doesn't exist. """
        pub.subscribe(self.on_fail_update_function, 'fail_update_function')

        DUT = dmFunction(test_program_dao)
        DUT.do_select_all(revision_id=1)
        DUT.do_update(100)


@pytest.mark.usefixtures('test_program_dao', 'test_configuration')
class TestAnalysisMethods():
    """Class for testing analytical methods."""
    @pytest.mark.integration
    def test_do_calculate_hri(self, test_program_dao, test_configuration):
        """do_calculate_hri() should calculate the hazard risk index hazard analysis."""
        DATAMGR = dmFunction(test_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = amFunction(test_configuration)

        pub.sendMessage('request_get_function_tree')

        _hazard = DATAMGR.do_select(1, 'hazards')[1]
        _hazard.assembly_severity = 'Major'
        _hazard.assembly_probability = 'Level A - Frequent'
        _hazard.system_severity = 'Medium'
        _hazard.system_probability = 'Level A - Frequent'
        _hazard.assembly_severity_f = 'Medium'
        _hazard.assembly_probability_f = 'Level B - Reasonably Probable'
        _hazard.system_severity_f = 'Medium'
        _hazard.system_probability_f = 'Level C - Occasional'
        DATAMGR.do_update(1)

        pub.sendMessage('request_calculate_fha', node_id=1)

        assert DUT._attributes['hazards'][1].assembly_hri == 30
        assert DUT._attributes['hazards'][1].system_hri == 20
        assert DUT._attributes['hazards'][1].assembly_hri_f == 16
        assert DUT._attributes['hazards'][1].system_hri_f == 12

    @pytest.mark.integration
    def test_do_calculate_user_defined(self, test_program_dao,
                                       test_configuration):
        """do_calculate_user_defined() should calculate the user-defined hazard analysis."""
        DATAMGR = dmFunction(test_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = amFunction(test_configuration)

        pub.sendMessage('request_get_function_tree')

        _hazard = DATAMGR.do_select(1, 'hazards')[1]
        _hazard.user_float_1 = 1.5
        _hazard.user_float_2 = 0.8
        _hazard.user_int_1 = 2
        _hazard.function_1 = 'uf1*uf2'
        _hazard.function_2 = 'res1/ui1'
        DATAMGR.do_update(1)

        pub.sendMessage('request_calculate_fha', node_id=1)

        assert DUT._attributes['hazards'][1].result_1 == pytest.approx(1.2)
        assert DUT._attributes['hazards'][1].result_2 == pytest.approx(0.6)
