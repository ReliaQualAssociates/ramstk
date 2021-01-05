# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_allocations.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Allocation BoM module algorithms and models."""

# Third Party Imports
import pytest
from __mocks__ import MOCK_ALLOCATION
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amAllocation, dmAllocation
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKAllocation


class MockDao:
    _all_allocation = []

    def do_delete(self, record):
        if record is None:
            raise DataAccessError('')
        else:
            for _idx, _record in enumerate(self._all_allocation):
                if _record.hardware_id == record.hardware_id:
                    self._all_allocation.pop(_idx)

    def do_insert(self, record):
        if record.hardware_id == 5:
            raise DataAccessError('An error occurred with RAMSTK.')
        elif record == RAMSTKAllocation:
            self._all_allocation.append(record)

    def do_insert_many(self, records):
        for _record in records:
            self.do_insert(_record)

    def do_select_all(self,
                      table,
                      key=None,
                      value=None,
                      order=None,
                      _all=False):
        if table == RAMSTKAllocation:
            self._all_allocation = []
            for _key in MOCK_ALLOCATION:
                _record = table()
                _record.revision_id = value
                _record.hardware_id = _key
                _record.set_attributes(MOCK_ALLOCATION[_key])
                self._all_allocation.append(_record)

            return self._all_allocation

    def do_update(self, record):
        for _key in MOCK_ALLOCATION:
            if _key == record.hardware_id:
                MOCK_ALLOCATION[_key]['mtbf_goal'] = float(record.mtbf_goal)


@pytest.fixture
def mock_program_dao(monkeypatch):
    yield MockDao()


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Allocation data manager."""
        DUT = dmAllocation()

        assert isinstance(DUT, dmAllocation)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'allocations'
        assert DUT._root == 0
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_allocation_attributes')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_allocation_attributes')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'wvw_editing_allocation')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_allocations')
        assert pub.isSubscribed(DUT.do_get_tree, 'request_get_allocation_tree')
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_set_all_attributes,
                                'succeed_calculate_allocation_goals')
        assert pub.isSubscribed(DUT.do_update, 'request_update_allocation')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_hardware')
        assert pub.isSubscribed(DUT._do_insert_allocation,
                                'request_insert_allocation')

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_toml_user_configuration):
        """__init__() should create an instance of the allocation analysis
        manager."""
        DUT = amAllocation(test_toml_user_configuration)

        assert isinstance(DUT, amAllocation)
        assert isinstance(DUT.RAMSTK_USER_CONFIGURATION,
                          RAMSTKUserConfiguration)
        assert isinstance(DUT._attributes, dict)
        assert isinstance(DUT._tree, Tree)
        assert DUT._attributes == {}
        assert DUT._node_hazard_rate == 0.0
        assert DUT._system_hazard_rate == 0.0
        assert pub.isSubscribed(DUT.on_get_all_attributes,
                                'succeed_get_allocation_attributes')
        assert pub.isSubscribed(DUT.on_get_tree, 'succeed_get_allocation_tree')
        assert pub.isSubscribed(DUT.on_get_tree, 'succeed_update_allocation')
        assert pub.isSubscribed(DUT._do_calculate_allocation,
                                'request_allocate_reliability')
        assert pub.isSubscribed(DUT._do_calculate_allocation_goals,
                                'request_calculate_allocation_goals')
        assert pub.isSubscribed(DUT._do_calculate_allocation,
                                'request_calculate_allocation')
        assert pub.isSubscribed(DUT._on_select_hardware, 'selected_hardware')


@pytest.mark.usefixtures('mock_program_dao', 'test_toml_user_configuration')
class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['allocation'], RAMSTKAllocation)
        print("\033[36m\nsucceed_retrieve_allocation topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all_allocation(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKAllocation instances on success."""
        pub.subscribe(self.on_succeed_select_all,
                      'succeed_retrieve_allocation')

        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_allocation')

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all() should clear nodes from an existing allocation
        tree."""
        pub.subscribe(self.on_succeed_select_all,
                      'succeed_retrieve_allocation')

        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_allocation')

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Allocation ID is
        requested."""
        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='allocation') is None


@pytest.mark.usefixtures('mock_program_dao', 'test_toml_user_configuration')
class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_allocation(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_allocation topic was broadcast.")

    def on_fail_delete_allocation_non_existent_id(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent allocation record with hardware ID 300."
        )
        print("\033[36m\nfail_delete_allocation topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete_allocation,
                      'succeed_delete_allocation')

        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_delete_hardware', node_id=DUT.last_id)

        assert DUT.last_id == 2

        pub.unsubscribe(self.on_succeed_delete_allocation,
                        'succeed_delete_allocation')

    @pytest.mark.unit
    def test_do_delete_with_children(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete_allocation,
                      'succeed_delete_allocation')

        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_delete_hardware', node_id=2)

        assert DUT.last_id == 1

        pub.unsubscribe(self.on_succeed_delete_allocation,
                        'succeed_delete_allocation')

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message."""
        pub.subscribe(self.on_fail_delete_allocation_non_existent_id,
                      'fail_delete_allocation')

        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_delete_hardware', node_id=300)

        pub.subscribe(self.on_fail_delete_allocation_non_existent_id,
                      'fail_delete_allocation')


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['hardware_id'] == 2
        assert attributes['availability_alloc'] == 0.0
        assert attributes['env_factor'] == 1
        assert attributes['goal_measure_id'] == 1
        assert attributes['hazard_rate_alloc'] == 0.0
        assert attributes['hazard_rate_goal'] == 0.0
        assert attributes['included'] == 1
        assert attributes['int_factor'] == 1
        assert attributes['allocation_method_id'] == 1
        assert attributes['mtbf_alloc'] == 0.0
        assert attributes['mtbf_goal'] == 0.0
        assert attributes['n_sub_systems'] == 1
        assert attributes['n_sub_elements'] == 1
        assert attributes['parent_id'] == 1
        assert attributes['percent_weight_factor'] == 0.0
        assert attributes['reliability_alloc'] == 1.0
        assert attributes['op_time_factor'] == 1
        assert attributes['soa_factor'] == 1
        assert attributes['weight_factor'] == 1
        print(
            "\033[36m\nsucceed_get_allocation_attributes topic was broadcast.")

    def on_succeed_get_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['allocation'], RAMSTKAllocation)
        print("\033[36m\nsucceed_get_allocation_tree topic was broadcast.")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """do_get_attributes() should return a dict of allocation attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes,
                      'succeed_get_allocation_attributes')

        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage(
            'request_get_allocation_attributes',
            node_id=2,
            table='allocation',
        )

        pub.unsubscribe(self.on_succeed_get_attributes,
                        'succeed_get_allocation_attributes')

    @pytest.mark.unit
    def test_get_all_attributes_analysis_manager(self, mock_program_dao,
                                                 test_toml_user_configuration):
        """_get_all_attributes() should update the attributes dict on
        success."""
        # This test would require using the dmHardware() to get the attributes.
        DATAMGR = dmAllocation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DUT = amAllocation(test_toml_user_configuration)

        pub.sendMessage('request_get_allocation_attributes',
                        node_id=2,
                        table='allocation')

        assert DUT._attributes['hardware_id'] == 2
        assert DUT._attributes['mtbf_alloc'] == 0.0

    @pytest.mark.unit
    def test_on_get_tree(self, mock_program_dao, test_toml_user_configuration):
        """_on_get_tree() should assign the data manager's tree to the _tree
        attribute in response to the succeed_get_allocation_tree message."""
        pub.subscribe(self.on_succeed_get_tree, 'succeed_get_allocation_tree')

        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_get_allocation_tree')

        pub.unsubscribe(self.on_succeed_get_tree,
                        'succeed_get_allocation_tree')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_allocation_attributes',
                        node_id=[2, -1],
                        package={'hazard_rate_goal': 0.00005})
        pub.sendMessage('request_set_allocation_attributes',
                        node_id=[2, -1],
                        package={'reliability_goal': 0.9995})
        assert DUT.do_select(2, table='allocation').hazard_rate_goal == 0.00005
        assert DUT.do_select(2, table='allocation').reliability_goal == 0.9995

    @pytest.mark.unit
    @pytest.mark.parametrize("method_id", [1, 2, 3, 4])
    def test_do_get_allocation_goal(self, mock_program_dao,
                                    test_toml_user_configuration, method_id):
        """do_calculate_goal() should return the proper allocation goal
        measure."""
        DATAMGR = dmAllocation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DUT = amAllocation(test_toml_user_configuration)

        pub.sendMessage('request_get_allocation_tree')
        pub.sendMessage('request_get_allocation_attributes',
                        node_id=2,
                        table='allocation')

        DUT._attributes['allocation_method_id'] = method_id
        DUT._attributes['hazard_rate_goal'] = 0.00002681
        DUT._attributes['reliability_goal'] = 0.9995

        _goal = DUT._do_get_allocation_goal()

        if method_id in [2, 4]:
            assert _goal == 0.00002681
        else:
            assert _goal == 0.9995


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_allocation(self, node_id, tree):
        assert node_id == 4
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(node_id).data['allocation'], RAMSTKAllocation)
        assert tree.get_node(node_id).data['allocation'].revision_id == 1
        assert tree.get_node(node_id).data['allocation'].hardware_id == 4
        assert tree.get_node(node_id).data['allocation'].parent_id == 1
        print("\033[36m\nsucceed_insert_allocation topic was broadcast.")

    def on_fail_insert_allocation_db_error(self, error_message):
        assert error_message == ('An error occurred with RAMSTK.')
        print("\033[35m\nfail_insert_allocation topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new sibling allocation assembly."""
        pub.subscribe(self.on_succeed_insert_allocation,
                      'succeed_insert_allocation')

        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_insert_allocation',
                        hardware_id=4,
                        parent_id=1)

        pub.unsubscribe(self.on_succeed_insert_allocation,
                        'succeed_insert_allocation')

    @pytest.mark.unit
    def test_do_insert_allocation_database_error(self, mock_program_dao):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_allocation_db_error,
                      'fail_insert_allocation')

        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_allocation(hardware_id=5, parent_id=0)

        pub.unsubscribe(self.on_fail_insert_allocation_db_error,
                        'fail_insert_allocation')


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_allocation(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data['allocation'].parent_id == 1
        assert tree.get_node(
            2).data['allocation'].percent_weight_factor == 0.9832
        assert tree.get_node(2).data['allocation'].mtbf_goal == 12000
        print("\033[36m\nsucceed_update_allocation topic was broadcast.")

    def on_fail_update_allocation_non_existent_id(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent allocation record ID '
            '100.')
        print("\033[35m\nfail_update_allocation topic was broadcast")

    def on_fail_update_allocation_no_data(self, error_message):
        assert error_message == ('do_update: No data package found for '
                                 'allocation record ID 1.')
        print("\033[35m\nfail_update_allocation topic was broadcast")

    def on_fail_update_allocation_wrong_data_type(self, error_message):
        assert error_message == (
            'do_update: The value for one or more attributes for allocation '
            'record ID 1 was the wrong type.')
        print("\033[35m\nfail_update_allocation topic was broadcast")

    @pytest.mark.unit
    def test_do_update_data_manager(self, mock_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update_allocation,
                      'succeed_update_allocation')

        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _allocation = DUT.do_select(2, table='allocation')
        _allocation.percent_weight_factor = 0.9832
        _allocation = DUT.do_select(2, table='allocation')
        _allocation.mtbf_goal = 12000

        pub.sendMessage('request_update_allocation', node_id=2)

        pub.unsubscribe(self.on_succeed_update_allocation,
                        'succeed_update_allocation')

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Allocation ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_allocation_non_existent_id,
                      'fail_update_allocation')

        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.do_update(100)

        pub.unsubscribe(self.on_fail_update_allocation_non_existent_id,
                        'fail_update_allocation')

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_allocation_no_data,
                      'fail_update_allocation')

        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data.pop('allocation')

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_allocation_no_data,
                        'fail_update_allocation')

    @pytest.mark.unit
    def test_do_update_wrong_data_type(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_allocation_wrong_data_type,
                      'fail_update_allocation')

        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _allocation = DUT.do_select(1, table='allocation')
        _allocation.mtbf_goal = {1: 2}

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_allocation_wrong_data_type,
                        'fail_update_allocation')

    @pytest.mark.unit
    def test_do_update_wrong_data_type_root_node(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _allocation = DUT.do_select(1, table='allocation')
        _allocation.mtbf_goal = {1: 2}

        DUT.do_update(0)

    @pytest.mark.unit
    def test_do_update_all(self, mock_program_dao):
        """do_update_all() should return a zero error code on success."""
        DUT = dmAllocation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        def on_message(tree):
            assert isinstance(tree, Tree)

        pub.subscribe(on_message, 'succeed_update_allocation')

        pub.sendMessage('request_update_all_allocation')


@pytest.mark.usefixtures('mock_program_dao', 'test_toml_user_configuration')
class TestAnalysisMethods():
    """Class for allocation methods test suite."""
    def on_succeed_calculate_agree(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data[
            'allocation'].hazard_rate_alloc == pytest.approx(0.03160455)
        assert tree.get_node(2).data['allocation'].mtbf_alloc == pytest.approx(
            31.6410171)
        assert tree.get_node(
            2).data['allocation'].reliability_alloc == pytest.approx(0.7290263)
        print("\033[36m\nsucceed_calculate_allocation topic was broadcast.")

    def on_succeed_calculate_arinc(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data[
            'allocation'].hazard_rate_alloc == pytest.approx(0.01731191)
        assert tree.get_node(2).data['allocation'].mtbf_alloc == pytest.approx(
            57.7637037)
        assert tree.get_node(
            2).data['allocation'].reliability_alloc == pytest.approx(0.1770734)
        print("\033[36m\nsucceed_calculate_allocation topic was broadcast.")

    def on_fail_calculate_arinc(self, error_message):
        assert error_message == ('_do_calculate_arinc_weight_factor: Failed '
                                 'to allocate reliability for allocation '
                                 'record ID 2.  System hazard rate was 0.0.')
        print("\033[35m\nfail_calculate_allocation topic was broadcast")

    def on_succeed_calculate_equal(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data[
            'allocation'].hazard_rate_alloc == pytest.approx(5.012542e-05)
        assert tree.get_node(2).data['allocation'].mtbf_alloc == pytest.approx(
            19949.9582288)
        assert tree.get_node(
            2).data['allocation'].reliability_alloc == pytest.approx(0.995)
        print("\033[36m\nsucceed_calculate_allocation topic was broadcast.")

    def on_succeed_calculate_foo(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(
            2).data['allocation'].hazard_rate_alloc == pytest.approx(0.1151243)
        assert tree.get_node(2).data['allocation'].mtbf_alloc == pytest.approx(
            8.6862670)
        assert tree.get_node(2).data[
            'allocation'].reliability_alloc == pytest.approx(1.000500334e-05)
        print("\033[36m\nsucceed_calculate_allocation topic was broadcast.")

    @pytest.mark.unit
    def test_do_calculate_goals_reliability_specified(
            self, mock_program_dao, test_toml_user_configuration):
        """do_calculate_goal() should calculate the equivalent h(t) and MTBF
        goals from a specified reliability goal."""
        DUT = amAllocation(test_toml_user_configuration)

        DATAMGR = dmAllocation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._tree.get_node(1).data['allocation'].hardware_id = 1
        DUT._tree.get_node(1).data['allocation'].goal_measure_id = 1
        DUT._tree.get_node(1).data['allocation'].mission_time = 100.0
        DUT._tree.get_node(1).data['allocation'].reliability_goal = 0.99732259

        pub.sendMessage('request_calculate_allocation_goals',
                        node=DUT._tree.get_node(1))

        assert DUT._tree.get_node(
            1).data['allocation'].hazard_rate_goal == pytest.approx(0.00002681)
        assert DUT._tree.get_node(
            1).data['allocation'].mtbf_goal == pytest.approx(37299.5151063)

    @pytest.mark.unit
    def test_do_calculate_goals_hazard_rate_specified(
            self, mock_program_dao, test_toml_user_configuration):
        """do_calculate_goal() should calculate the equivalent MTBF and R(t)
        goals from a specified hazard rate goal."""
        DUT = amAllocation(test_toml_user_configuration)

        DATAMGR = dmAllocation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._tree.get_node(1).data['allocation'].hardware_id = 1
        DUT._tree.get_node(1).data['allocation'].goal_measure_id = 2
        DUT._tree.get_node(1).data['allocation'].mission_time = 100.0
        DUT._tree.get_node(1).data['allocation'].hazard_rate_goal = 0.00002681

        pub.sendMessage('request_calculate_allocation_goals',
                        node=DUT._tree.get_node(1))

        assert DUT._tree.get_node(
            1).data['allocation'].mtbf_goal == pytest.approx(37299.5151063)
        assert DUT._tree.get_node(
            1).data['allocation'].reliability_goal == pytest.approx(0.99732259)

    @pytest.mark.unit
    def test_do_calculate_goals_mtbf_specified(self, mock_program_dao,
                                               test_toml_user_configuration):
        """do_calculate_goal() should calculate the equivalent h(t) and R(t)
        goals from a specified MTBF goal."""
        DUT = amAllocation(test_toml_user_configuration)

        DATAMGR = dmAllocation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._tree.get_node(1).data['allocation'].hardware_id = 1
        DUT._tree.get_node(1).data['allocation'].goal_measure_id = 3
        DUT._tree.get_node(1).data['allocation'].mission_time = 100.0
        DUT._tree.get_node(1).data['allocation'].mtbf_goal = 37300.0

        pub.sendMessage('request_calculate_allocation_goals',
                        node=DUT._tree.get_node(1))

        assert DUT._tree.get_node(1).data[
            'allocation'].hazard_rate_goal == pytest.approx(2.68096515e-05)
        assert DUT._tree.get_node(
            1).data['allocation'].reliability_goal == pytest.approx(0.99732259)

    @pytest.mark.unit
    def test_do_calculate_agree_allocation(self, mock_program_dao,
                                           test_toml_user_configuration):
        """do_calculate_allocation() should apportion the node ID reliability
        goal using the AGREE method."""
        pub.subscribe(self.on_succeed_calculate_agree,
                      'succeed_calculate_allocation')

        DUT = amAllocation(test_toml_user_configuration)

        DATAMGR = dmAllocation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._tree.get_node(1).data['allocation'].allocation_method_id = 2
        DUT._tree.get_node(1).data['allocation'].reliability_goal = 0.717
        DUT._tree.get_node(2).data['allocation'].duty_cycle = 90.0
        DUT._tree.get_node(2).data['allocation'].mission_time = 10.0
        DUT._tree.get_node(2).data['allocation'].n_sub_elements = 4
        DUT._tree.get_node(2).data['allocation'].weight_factor = 0.95

        pub.sendMessage('request_allocate_reliability', node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_agree,
                        'succeed_calculate_allocation')

    @pytest.mark.unit
    def test_do_calculate_arinc_allocation(self, mock_program_dao,
                                           test_toml_user_configuration):
        """do_calculate_allocation() should apportion the node ID reliability
        goal using the ARINC method."""
        pub.subscribe(self.on_succeed_calculate_arinc,
                      'succeed_calculate_allocation')

        DUT = amAllocation(test_toml_user_configuration)

        DATAMGR = dmAllocation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._node_hazard_rate = 0.000628
        DUT._system_hazard_rate = 0.002681

        DUT._tree.get_node(1).data['allocation'].allocation_method_id = 3
        DUT._tree.get_node(1).data['allocation'].goal_measure_id = 2
        DUT._tree.get_node(1).data['allocation'].hazard_rate_goal = 0.000617
        DUT._tree.get_node(2).data['allocation'].hazard_rate_active = 0.000628

        pub.sendMessage('request_allocate_reliability', node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_arinc,
                        'succeed_calculate_allocation')

    @pytest.mark.unit
    def test_do_calculate_arinc_allocation_zero_system_hazard_rate(
            self, mock_program_dao, test_toml_user_configuration):
        """do_calculate_allocation() should send an error message when
        attempting to allocate an assembly with a zero hazard rate using the
        ARINC method."""
        pub.subscribe(self.on_fail_calculate_arinc,
                      'fail_calculate_allocation')

        DUT = amAllocation(test_toml_user_configuration)

        DATAMGR = dmAllocation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._node_hazard_rate = 0.000628
        DUT._system_hazard_rate = 0.0

        DUT._tree.get_node(1).data['allocation'].allocation_method_id = 3
        DUT._tree.get_node(1).data['allocation'].goal_measure_id = 2
        DUT._tree.get_node(1).data['allocation'].hazard_rate_active = 0.0
        DUT._tree.get_node(1).data['allocation'].hazard_rate_goal = 0.000617
        DUT._tree.get_node(2).data['allocation'].hazard_rate_active = 0.000628

        pub.sendMessage('request_allocate_reliability', node_id=1)

        pub.unsubscribe(self.on_fail_calculate_arinc,
                        'fail_calculate_allocation')

    @pytest.mark.unit
    def test_do_calculate_equal_allocation(self, mock_program_dao,
                                           test_toml_user_configuration):
        """do_calculate_allocation() should apportion the node ID reliability
        goal using the equal apportionment method."""
        pub.subscribe(self.on_succeed_calculate_equal,
                      'succeed_calculate_allocation')

        DUT = amAllocation(test_toml_user_configuration)

        DATAMGR = dmAllocation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._tree.get_node(1).data['allocation'].allocation_method_id = 1
        DUT._tree.get_node(1).data['allocation'].goal_measure_id = 1
        DUT._tree.get_node(1).data['allocation'].reliability_goal = 0.995

        pub.sendMessage('request_allocate_reliability', node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_equal,
                        'succeed_calculate_allocation')

    @pytest.mark.unit
    def test_do_calculate_foo_allocation(self, mock_program_dao,
                                         test_toml_user_configuration):
        """do_calculate_allocation() should apportion the node ID reliability
        goal using the feasibility of objectives method."""
        pub.subscribe(self.on_succeed_calculate_foo,
                      'succeed_calculate_allocation')

        DUT = amAllocation(test_toml_user_configuration)

        DATAMGR = dmAllocation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._tree.get_node(1).data['allocation'].allocation_method_id = 4
        DUT._tree.get_node(1).data['allocation'].goal_measure_id = 1
        DUT._tree.get_node(1).data['allocation'].hazard_rate_goal = 0.000617
        DUT._tree.get_node(2).data['allocation'].env_factor = 6
        DUT._tree.get_node(2).data['allocation'].soa_factor = 2
        DUT._tree.get_node(2).data['allocation'].op_time_factor = 9
        DUT._tree.get_node(2).data['allocation'].int_factor = 3

        pub.sendMessage('request_allocate_reliability', node_id=1)

        pub.unsubscribe(self.on_succeed_calculate_foo,
                        'succeed_calculate_allocation')

    @pytest.mark.unit
    def test_do_calculate_no_allocation_method(self, mock_program_dao,
                                               test_toml_user_configuration):
        """do_calculate_allocation() should apportion the node ID reliability
        goal using the feasibility of objectives method."""
        DUT = amAllocation(test_toml_user_configuration)

        DATAMGR = dmAllocation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        DUT._tree.get_node(1).data['allocation'].allocation_method_id = 16
        DUT._tree.get_node(1).data['allocation'].goal_measure_id = 1
        DUT._tree.get_node(1).data['allocation'].hazard_rate_goal = 0.000617

        assert DUT._do_calculate_allocation(1) is None

    @pytest.mark.unit
    def test_on_select_hardware(self, mock_program_dao,
                                test_toml_user_configuration):
        """_on_select_hardware() should assign the node hazard rate to the
        _node_hazard_rate attribute."""
        DUT = amAllocation(test_toml_user_configuration)

        DATAMGR = dmAllocation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('selected_hardware',
                        attributes={
                            'hazard_rate_active': 0.00032,
                            'hardware_id': 2
                        })

        assert DUT._node_hazard_rate == 0.00032
        assert DUT._system_hazard_rate == 0.0

    @pytest.mark.unit
    def test_on_select_hardware_system(self, mock_program_dao,
                                       test_toml_user_configuration):
        """_on_select_hardware() should assign the node and system hazard rate
        when the system node is selected."""
        DUT = amAllocation(test_toml_user_configuration)

        DATAMGR = dmAllocation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('selected_hardware',
                        attributes={
                            'hazard_rate_active': 0.00032,
                            'hardware_id': 1
                        })

        assert DUT._node_hazard_rate == 0.00032
        assert DUT._system_hazard_rate == 0.00032
