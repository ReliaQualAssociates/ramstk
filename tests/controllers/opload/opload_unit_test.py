# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.opload.opload_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Operating Load algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKOpLoad
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmOpLoad
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKOpLoad


@pytest.fixture
def mock_program_dao(monkeypatch):
    _opload_1 = MockRAMSTKOpLoad()
    _opload_1.revision_id = 1
    _opload_1.hardware_id = 1
    _opload_1.mode_id = 6
    _opload_1.mechanism_id = 2
    _opload_1.load_id = 1
    _opload_1.damage_model = ""
    _opload_1.description = "Test Operating Load #1"
    _opload_1.priority_id = 0

    _opload_2 = MockRAMSTKOpLoad()
    _opload_2.revision_id = 1
    _opload_2.hardware_id = 1
    _opload_2.mode_id = 6
    _opload_2.mechanism_id = 2
    _opload_2.load_id = 2
    _opload_2.damage_model = ""
    _opload_2.description = "Test Operating Load #2"
    _opload_2.priority_id = 0

    DAO = MockDAO()
    DAO.table = [
        _opload_1,
        _opload_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
        "load_id": 3,
    }


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmOpLoad()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opload")
    pub.unsubscribe(dut.do_update, "request_update_opload")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_opload_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_opload")
    pub.unsubscribe(dut.do_insert, "request_insert_opload")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """__init__() should return a PoF data manager."""
        assert isinstance(test_datamanager, dmOpLoad)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, MockDAO)
        assert test_datamanager._db_id_colname == "fld_load_id"
        assert test_datamanager._db_tablename == "ramstk_op_load"
        assert test_datamanager._tag == "opload"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert test_datamanager._parent_id == 0
        assert test_datamanager.last_id == 0
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_opload_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "request_set_opload_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "wvw_editing_opload"
        )
        assert pub.isSubscribed(test_datamanager.do_update, "request_update_opload")
        assert pub.isSubscribed(test_datamanager.do_get_tree, "request_get_opload_tree")
        assert pub.isSubscribed(test_datamanager.do_delete, "request_delete_opload")
        assert pub.isSubscribed(test_datamanager.do_insert, "request_insert_opload")


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_datamanager):
        """do_select_all() should return a Tree() object populated with RAMSTKOpLoad
        instances on success."""
        test_datamanager.do_select_all(attributes=test_attributes)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["opload"], MockRAMSTKOpLoad
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_datamanager):
        """do_select() should return an instance of the RAMSTKOpLoad on success."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _opload = test_datamanager.do_select(2)

        assert isinstance(_opload, MockRAMSTKOpLoad)
        assert _opload.description == "Test Operating Load #2"
        assert _opload.priority_id == 0

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_datamanager):
        """do_select() should return None when a non-existent opload ID is
        requested."""
        test_datamanager.do_select_all(attributes=test_attributes)

        assert test_datamanager.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """_do_insert_opload() should send the success message after successfully
        inserting an operating load."""
        test_datamanager.do_select_all(attributes=test_attributes)
        test_datamanager.do_insert(attributes=test_attributes)

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(3).data["opload"], RAMSTKOpLoad
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_datamanager):
        """_do_delete() should send the success message with the treelib Tree when
        successfully deleting a test method."""
        test_datamanager.do_select_all(attributes=test_attributes)
        test_datamanager.do_delete(2)

        assert test_datamanager.tree.get_node(2) is None
