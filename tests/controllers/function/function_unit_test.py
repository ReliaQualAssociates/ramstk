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
from ramstk.db.base import BaseDatabase
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
    _function_2.parent_id = 0
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
    """Test fixture for Function data manager."""
    dut = dmFunction()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.

    # Delete the device under test.
    del dut


class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Function data manager."""
        DUT = dmFunction()

        assert isinstance(DUT, dmFunction)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "functions"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, "selected_revision")
        assert pub.isSubscribed(DUT.do_update, "request_update_function")
        assert pub.isSubscribed(DUT.do_update_all, "request_update_all_functions")
        assert pub.isSubscribed(
            DUT.do_get_attributes, "request_get_function_attributes"
        )
        assert pub.isSubscribed(DUT.do_get_tree, "request_get_functions_tree")
        assert pub.isSubscribed(
            DUT.do_set_attributes, "request_set_function_attributes"
        )
        assert pub.isSubscribed(DUT._do_delete, "request_delete_function")
        assert pub.isSubscribed(DUT._do_insert_function, "request_insert_function")


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["function"], MockRAMSTKFunction)
        print("\033[36m\nsucceed_retrieve_functions topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKFunction instances on success."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_functions")

        test_datamanager.do_select_all(attributes={"revision_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_functions")

    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """do_select() should return an instance of the RAMSTKFunction on
        success."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        _function = test_datamanager.do_select(1, table="function")

        assert isinstance(_function, MockRAMSTKFunction)
        assert _function.availability_logistics == 1.0
        assert _function.name == "Function Name"

    @pytest.mark.unit
    def test_do_select_unknown_table(self, test_datamanager):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        with pytest.raises(KeyError):
            test_datamanager.do_select(1, table="scibbidy-bibbidy-doo")

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """do_select() should return None when a non-existent Function ID is
        requested."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        assert test_datamanager.do_select(100, table="function") is None


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_function topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent function ID 300."
        )
        print("\033[35m\nfail_delete_function topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent function ID 2."
        )
        print("\033[35m\nfail_delete_function topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_function")

        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_delete(test_datamanager.last_id)

        assert test_datamanager.last_id == 1

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_function")

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to delete
        a function ID that doesn't exist in the database."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_function")

        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_function")

    @pytest.mark.unit
    def test_do_delete_not_in_tree(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_function")

        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager.tree.remove_node(2)
        test_datamanager._do_delete(2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_function")


@pytest.mark.usefixtures("test_datamanager")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["function_id"] == 1
        assert attributes["name"] == "Function Name"
        assert attributes["safety_critical"] == 0
        print("\033[36m\nsucceed_get_function_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["function"], MockRAMSTKFunction)
        print("\033[36m\nsucceed_get_function_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes(self, test_datamanager):
        """_do_get_attributes() should return a dict of function attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_function_attributes")

        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager.do_get_attributes(1, "function")

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_function_attributes"
        )

    @pytest.mark.unit
    def test_do_set_attributes(self, test_datamanager):
        """do_set_attributes() should send the success message."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager.do_set_attributes(
            node_id=[1, -1], package={"function_code": "-"}
        )

        assert test_datamanager.do_select(1, table="function").function_code == "-"

    @pytest.mark.unit
    def test_on_get_data_manager_tree(self, test_datamanager):
        """on_get_tree() should return the function treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_function_tree"
        )

        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager.do_get_tree()

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_function_tree"
        )


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_function topic was broadcast.")

    def on_succeed_insert_child(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        assert tree.get_node(3).data["function"].parent_id == 2
        print("\033[36m\nsucceed_insert_function topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "_do_insert_function: Attempted to insert "
            "child function under non-existent function ID 40."
        )
        print("\033[35m\nfail_insert_function topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_datamanager):
        """_do_insert_function() should send the success message after
        successfully inserting a sibling function."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_function")

        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_insert_function()

        assert isinstance(
            test_datamanager.tree.get_node(3).data["function"], RAMSTKFunction
        )
        assert test_datamanager.tree.get_node(3).data["function"].function_id == 3
        assert test_datamanager.tree.get_node(3).data["function"].name == "New Function"

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_function")

    @pytest.mark.unit
    def test_do_insert_child(self, test_datamanager):
        """_do_insert_function() should send the success message after
        successfully inserting a child function."""
        pub.subscribe(self.on_succeed_insert_child, "succeed_insert_function")

        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_insert_function(parent_id=2)

        assert isinstance(
            test_datamanager.tree.get_node(3).data["function"], RAMSTKFunction
        )
        assert test_datamanager.tree.get_node(3).data["function"].function_id == 3
        assert test_datamanager.tree.get_node(3).data["function"].name == "New Function"

        pub.unsubscribe(self.on_succeed_insert_child, "succeed_insert_function")

    @pytest.mark.unit
    def test_do_insert_no_parent(self, test_datamanager):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_function")

        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_insert_function(parent_id=40)

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_function")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_fail_update_non_existent_id(self, error_message):
        assert (
            error_message == "do_update: Attempted to save non-existent function "
            "with function ID 100."
        )
        print("\033[35m\nfail_update_function topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == "do_update: No data package found for function ID 1."
        print("\033[35m\nfail_update_function topic was broadcast")

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Function ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_function")

        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager.do_update(100, "function")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_function")

    @pytest.mark.unit
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Function ID that has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_function")

        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager.tree.get_node(1).data.pop("function")
        test_datamanager.do_update(1, "function")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_function")
