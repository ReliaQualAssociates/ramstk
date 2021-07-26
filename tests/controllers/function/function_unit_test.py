# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.function.function_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing function module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKFunction
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmFunction
from ramstk.models.programdb import RAMSTKFunction


@pytest.fixture
def mock_program_dao(monkeypatch):
    _function_1 = MockRAMSTKFunction()
    _function_1.revision_id = 1
    _function_1.function_id = 1
    _function_1.availability_logistics = 1.0
    _function_1.availability_mission = 1.0
    _function_1.cost = 0.0
    _function_1.function_code = "PRESS-001"
    _function_1.hazard_rate_logistics = 0.0
    _function_1.hazard_rate_mission = 0.0
    _function_1.level = 0
    _function_1.mcmt = 0.0
    _function_1.mmt = 0.0
    _function_1.mpmt = 0.0
    _function_1.mtbf_logistics = 0.0
    _function_1.mtbf_mission = 0.0
    _function_1.mttr = 0.0
    _function_1.name = "Function Name"
    _function_1.parent_id = 0
    _function_1.remarks = ""
    _function_1.safety_critical = 0
    _function_1.total_mode_count = 0
    _function_1.total_part_count = 0
    _function_1.type_id = 0

    _function_2 = MockRAMSTKFunction()
    _function_2.revision_id = 1
    _function_2.function_id = 2
    _function_2.availability_logistics = 1.0
    _function_2.availability_mission = 1.0
    _function_2.cost = 0.0
    _function_2.function_code = "PRESS-001"
    _function_2.hazard_rate_logistics = 0.0
    _function_2.hazard_rate_mission = 0.0
    _function_2.level = 0
    _function_2.mcmt = 0.0
    _function_2.mmt = 0.0
    _function_2.mpmt = 0.0
    _function_2.mtbf_logistics = 0.0
    _function_2.mtbf_mission = 0.0
    _function_2.mttr = 0.0
    _function_2.name = "Function Name"
    _function_2.parent_id = 1
    _function_2.remarks = ""
    _function_2.safety_critical = 0
    _function_2.total_mode_count = 0
    _function_2.total_part_count = 0
    _function_2.type_id = 0

    DAO = MockDAO()
    DAO.table = [
        _function_1,
        _function_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmFunction()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_function_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_function_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_function")
    pub.unsubscribe(dut.do_update, "request_update_function")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_functions_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_function")
    pub.unsubscribe(dut._do_insert_function, "request_insert_function")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """__init__() should return a Function data manager."""
        assert isinstance(test_datamanager, dmFunction)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, MockDAO)
        assert test_datamanager._tag == "functions"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_datamanager.do_update, "request_update_function")
        assert pub.isSubscribed(
            test_datamanager.do_update_all, "request_update_all_functions"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_function_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_tree, "request_get_functions_tree"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "request_set_function_attributes"
        )
        assert pub.isSubscribed(test_datamanager._do_delete, "request_delete_function")
        assert pub.isSubscribed(
            test_datamanager._do_insert_function, "request_insert_function"
        )


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["function"], MockRAMSTKFunction)
        print("\033[36m\nsucceed_retrieve_functions topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """should return record tree populated with RAMSTKFunction records."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        assert isinstance(
            test_datamanager.tree.get_node(1).data["function"], MockRAMSTKFunction
        )
        assert isinstance(
            test_datamanager.tree.get_node(2).data["function"], MockRAMSTKFunction
        )

    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """should return the RAMSTKFunction record for the requested Function ID."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        _function = test_datamanager.do_select(1, table="function")

        assert isinstance(_function, MockRAMSTKFunction)
        assert _function.availability_logistics == 1.0
        assert _function.name == "Function Name"

    @pytest.mark.unit
    def test_do_select_unknown_table(self, test_datamanager):
        """should raise a KeyError when an unknown table name is requested."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        with pytest.raises(KeyError):
            test_datamanager.do_select(1, table="scibbidy-bibbidy-doo")

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """should return None when a non-existent Function ID is requested."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        assert test_datamanager.do_select(100, table="function") is None


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_datamanager):
        """should add a record to the record tree and update last_id."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_insert_function()

        assert test_datamanager.last_id == 3
        assert isinstance(
            test_datamanager.tree.get_node(3).data["function"], RAMSTKFunction
        )
        assert test_datamanager.tree.get_node(3).data["function"].function_id == 3
        assert test_datamanager.tree.get_node(3).data["function"].name == "New Function"

    @pytest.mark.unit
    def test_do_insert_child(self, test_datamanager):
        """should add a record to the record tree and update last_id."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_insert_function(parent_id=2)

        assert test_datamanager.last_id == 3
        assert isinstance(
            test_datamanager.tree.get_node(3).data["function"], RAMSTKFunction
        )
        assert test_datamanager.tree.get_node(3).data["function"].function_id == 3
        assert test_datamanager.tree.get_node(3).data["function"].name == "New Function"
        assert test_datamanager.tree.get_node(3).data["function"].parent_id == 2


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """should remove a record from the record tree and update last_id."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        _last_id = test_datamanager.last_id
        test_datamanager._do_delete(test_datamanager.last_id)

        assert test_datamanager.last_id == 1
        assert test_datamanager.tree.get_node(_last_id) is None

    @pytest.mark.unit
    def test_do_delete_with_child(self, test_datamanager):
        """should remove a record and children from record tree and update last_id."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_delete(1)

        assert test_datamanager.last_id == 0
        assert test_datamanager.tree.get_node(2) is None
        assert test_datamanager.tree.get_node(1) is None
