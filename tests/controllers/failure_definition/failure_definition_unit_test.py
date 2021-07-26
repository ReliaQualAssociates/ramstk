# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.failure_definition.failure_definition.unit_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing failure definition module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKFailureDefinition
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmFailureDefinition
from ramstk.models.programdb import RAMSTKFailureDefinition


@pytest.fixture
def mock_program_dao(monkeypatch):
    _definition_1 = MockRAMSTKFailureDefinition()
    _definition_1.revision_id = 1
    _definition_1.definition_id = 1
    _definition_1.definition = "Mock Failure Definition 1"

    _definition_2 = MockRAMSTKFailureDefinition()
    _definition_2.revision_id = 1
    _definition_2.definition_id = 2
    _definition_2.definition = "Mock Failure Definition 2"

    DAO = MockDAO()
    DAO.table = [
        _definition_1,
        _definition_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmFailureDefinition()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_failure_definition_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_failure_definition_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_failure_definition")
    pub.unsubscribe(dut.do_update, "request_update_failure_definition")
    pub.unsubscribe(dut.do_get_tree, "request_get_failure_definition_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut._do_delete, "request_delete_failure_definition")
    pub.unsubscribe(
        dut._do_insert_failure_definition, "request_insert_failure_definition"
    )

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """__init__() should return a Revision data manager."""
        assert isinstance(test_datamanager, dmFailureDefinition)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, MockDAO)
        assert test_datamanager._tag == "failure_definition"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes,
            "request_get_failure_definition_attributes",
        )
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_datamanager.do_update, "request_update_failure_definition"
        )
        assert pub.isSubscribed(
            test_datamanager.do_update_all, "request_update_all_failure_definition"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_tree, "request_get_failure_definition_tree"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes,
            "request_set_failure_definition_attributes",
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "lvw_editing_failure_definition"
        )
        assert pub.isSubscribed(
            test_datamanager._do_delete, "request_delete_failure_definition"
        )
        assert pub.isSubscribed(
            test_datamanager._do_insert_failure_definition,
            "request_insert_failure_definition",
        )


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKFailureDefinition instances on success."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["failure_definition"],
            MockRAMSTKFailureDefinition,
        )

    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """do_select() should return an instance of RAMSTKFailureDefinition on
        success."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        _failure_definition = test_datamanager.do_select(1, table="failure_definition")

        assert isinstance(_failure_definition, MockRAMSTKFailureDefinition)
        assert _failure_definition.definition == "Mock Failure Definition 1"

    @pytest.mark.unit
    def test_do_select_unknown_table(self, test_datamanager):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        with pytest.raises(KeyError):
            test_datamanager.do_select(1, table="scibbidy-bibbidy-doo")

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """do_select() should return None when a non-existent Revision ID is
        requested."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        assert test_datamanager.do_select(100, table="failure_definition") is None


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_datamanager):
        """should add new record to record tree and update last_id."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_insert_failure_definition()

        assert test_datamanager.last_id == 3
        assert isinstance(
            test_datamanager.tree[3].data["failure_definition"], RAMSTKFailureDefinition
        )


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """should remove record from record tree and update last_id."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        _last_id = test_datamanager.last_id
        test_datamanager._do_delete(node_id=test_datamanager.last_id)

        assert test_datamanager.last_id == 1
        assert test_datamanager.tree.get_node(_last_id) is None
