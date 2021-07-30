# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.action.action_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing FMEA Action algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKAction
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmAction
from ramstk.models.programdb import RAMSTKAction


@pytest.fixture
def mock_program_dao(monkeypatch):
    _action_1 = MockRAMSTKAction()
    _action_1.revision_id = 1
    _action_1.hardware_id = 1
    _action_1.mode_id = 6
    _action_1.mechanism_id = 3
    _action_1.cause_id = 3
    _action_1.action_id = 1
    _action_1.description = "Test FMEA Action #1 for Cause ID #3."
    _action_1.type_id = "Detection"

    _action_2 = MockRAMSTKAction()
    _action_2.revision_id = 1
    _action_2.hardware_id = 1
    _action_2.mode_id = 6
    _action_2.mechanism_id = 3
    _action_2.cause_id = 3
    _action_2.action_id = 2
    _action_2.description = "Test FMEA Action #2 for Cause ID #3."
    _action_2.type_id = "Prevention"

    DAO = MockDAO()
    DAO.table = [
        _action_1,
        _action_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmAction()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_action_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_action_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_action")
    pub.unsubscribe(dut.do_update, "request_update_action")
    pub.unsubscribe(dut.do_select_all, "selected_cause")
    pub.unsubscribe(dut.do_get_tree, "request_get_action_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_action")
    pub.unsubscribe(dut.do_insert, "request_insert_action")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateActionlers:
    """Class for actionler initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """__init__() should return a PoF data manager."""
        assert isinstance(test_datamanager, dmAction)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, MockDAO)
        assert test_datamanager._tag == "action"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert test_datamanager._parent_id == 0
        assert test_datamanager.last_id == 0
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_cause")
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_action_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "request_set_action_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "wvw_editing_action"
        )
        assert pub.isSubscribed(test_datamanager.do_update, "request_update_action")
        assert pub.isSubscribed(test_datamanager.do_get_tree, "request_get_action_tree")
        assert pub.isSubscribed(test_datamanager._do_delete, "request_delete_action")
        assert pub.isSubscribed(test_datamanager.do_insert, "request_insert_action")


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """should return a Tree() object populated with RAMSTKAction instances."""
        test_datamanager.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "cause_id": 3,
            }
        )

        assert isinstance(
            test_datamanager.tree.get_node(1).data["action"], MockRAMSTKAction
        )
        assert isinstance(
            test_datamanager.tree.get_node(2).data["action"], MockRAMSTKAction
        )

    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """should return an instance of the RAMSTKAction on success."""
        test_datamanager.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "cause_id": 3,
            }
        )

        _action = test_datamanager.do_select(1, table="action")

        assert isinstance(_action, MockRAMSTKAction)
        assert _action.description == "Test FMEA Action #1 for Cause ID #3."
        assert _action.type_id == "Detection"

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """should return None when a non-existent action ID is requested."""
        test_datamanager.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "cause_id": 3,
            }
        )

        assert test_datamanager.do_select(100, table="action") is None


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_datamanager):
        """should add a record to the record tree and update last_id."""
        _attributes = {
            "revision_id": 1,
            "hardware_id": 1,
            "mode_id": 6,
            "mechanism_id": 3,
            "cause_id": 3,
            "action_id": 1,
        }
        test_datamanager.do_select_all(_attributes)
        test_datamanager.do_insert(_attributes)

        assert test_datamanager.last_id == 3
        assert isinstance(
            test_datamanager.tree.get_node(3).data["action"], RAMSTKAction
        )


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """should remove the record from the record tree and update last_id."""
        test_datamanager.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 3,
                "cause_id": 3,
            }
        )
        test_datamanager._do_delete(2)

        assert test_datamanager.last_id == 1
        assert test_datamanager.tree.get_node(2) is None
