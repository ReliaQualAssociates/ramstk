# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_method.method_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Test Method algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKTestMethod
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmTestMethod
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKTestMethod


@pytest.fixture
def mock_program_dao(monkeypatch):
    _test_method_1 = MockRAMSTKTestMethod()
    _test_method_1.revision_id = 1
    _test_method_1.hardware_id = 1
    _test_method_1.mode_id = 1
    _test_method_1.mechanism_id = 1
    _test_method_1.load_id = 1
    _test_method_1.test_id = 1
    _test_method_1.description = "Test Test Method #1"
    _test_method_1.boundary_conditions = "Waters"
    _test_method_1.remarks = ""

    _test_method_2 = MockRAMSTKTestMethod()
    _test_method_2.revision_id = 1
    _test_method_2.hardware_id = 1
    _test_method_2.mode_id = 1
    _test_method_2.mechanism_id = 1
    _test_method_2.load_id = 1
    _test_method_2.test_id = 2
    _test_method_2.description = "Test Test Method #2"
    _test_method_2.boundary_conditions = "Sands"
    _test_method_2.remarks = ""

    DAO = MockDAO()
    DAO.table = [
        _test_method_1,
        _test_method_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmTestMethod()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_test_method_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_test_method_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_test_method")
    pub.unsubscribe(dut.do_update, "request_update_test_method")
    pub.unsubscribe(dut.do_select_all, "selected_load")
    pub.unsubscribe(dut.do_get_tree, "request_get_test_method_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_test_method")
    pub.unsubscribe(dut._do_insert_test_method, "request_insert_test_method")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.pof
    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """__init__() should return a PoF data manager."""
        assert isinstance(test_datamanager, dmTestMethod)
        assert isinstance(test_datamanager.tree, Tree)
        assert test_datamanager._tag == "test_methods"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert test_datamanager._parent_id == 0
        assert test_datamanager.last_id == 0
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_load")
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_test_method_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "request_set_test_method_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "wvw_editing_test_method"
        )
        assert pub.isSubscribed(
            test_datamanager.do_update, "request_update_test_method"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_tree, "request_get_test_method_tree"
        )
        assert pub.isSubscribed(
            test_datamanager._do_delete, "request_delete_test_method"
        )
        assert pub.isSubscribed(
            test_datamanager._do_insert_test_method, "request_insert_test_method"
        )


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKTestMethod instances on success."""
        test_datamanager.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["test_method"], MockRAMSTKTestMethod
        )

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """do_select() should return an instance of the RAMSTKTestMethod on
        success."""
        test_datamanager.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        _test_method = test_datamanager.do_select(2, table="test_method")

        assert isinstance(_test_method, MockRAMSTKTestMethod)
        assert _test_method.description == "Test Test Method #2"
        assert _test_method.boundary_conditions == "Sands"

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select_unknown_table(self, test_datamanager):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        test_datamanager.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        with pytest.raises(KeyError):
            test_datamanager.do_select(2, table="scibbidy-bibbidy-doo")

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """do_select() should return None when a non-existent test_method ID is
        requested."""
        test_datamanager.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        assert test_datamanager.do_select(100, table="test_method") is None


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_insert_sibling(self, test_datamanager):
        """_do_insert_test_method() should send the success message after
        successfully inserting an operating load."""
        test_datamanager.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        test_datamanager._do_insert_test_method(1)

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(3).data["test_method"], RAMSTKTestMethod
        )


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """_do_delete() should send the success message with the treelib Tree
        when successfully deleting a test method."""
        test_datamanager.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        test_datamanager._do_delete(test_datamanager.last_id)

        assert test_datamanager.last_id == 1
