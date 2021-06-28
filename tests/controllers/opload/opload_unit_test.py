# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.opload.opload_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
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
    pub.unsubscribe(dut.do_select_all, "selected_mechanism")
    pub.unsubscribe(dut.do_get_tree, "request_get_opload_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_opload")
    pub.unsubscribe(dut._do_insert_opload, "request_insert_opload")

    # Delete the device under test.
    del dut


class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.pof
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a PoF data manager."""
        DUT = dmOpLoad()

        assert isinstance(DUT, dmOpLoad)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "oploads"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert DUT._parent_id == 0
        assert DUT.last_id == 0
        assert pub.isSubscribed(DUT.do_select_all, "selected_mechanism")
        assert pub.isSubscribed(DUT.do_get_attributes, "request_get_opload_attributes")
        assert pub.isSubscribed(DUT.do_set_attributes, "request_set_opload_attributes")
        assert pub.isSubscribed(DUT.do_set_attributes, "wvw_editing_opload")
        assert pub.isSubscribed(DUT.do_update, "request_update_opload")
        assert pub.isSubscribed(DUT.do_get_tree, "request_get_opload_tree")
        assert pub.isSubscribed(DUT._do_delete, "request_delete_opload")
        assert pub.isSubscribed(DUT._do_insert_opload, "request_insert_opload")

        # Unsubscribe from pypubsub topics.
        pub.unsubscribe(DUT.do_get_attributes, "request_get_opload_attributes")
        pub.unsubscribe(DUT.do_set_attributes, "request_set_opload_attributes")
        pub.unsubscribe(DUT.do_set_attributes, "wvw_editing_opload")
        pub.unsubscribe(DUT.do_update, "request_update_opload")
        pub.unsubscribe(DUT.do_select_all, "selected_mechanism")
        pub.unsubscribe(DUT.do_get_tree, "request_get_opload_tree")
        pub.unsubscribe(DUT._do_delete, "request_delete_opload")
        pub.unsubscribe(DUT._do_insert_opload, "request_insert_opload")


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKOpLoad instances on success."""
        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["opload"], MockRAMSTKOpLoad
        )

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """do_select() should return an instance of the RAMSTKOpLoad on
        success."""
        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )

        _opload = test_datamanager.do_select(2, table="opload")

        assert isinstance(_opload, MockRAMSTKOpLoad)
        assert _opload.description == "Test Operating Load #2"
        assert _opload.priority_id == 0

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select_unknown_table(self, test_datamanager):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )

        with pytest.raises(KeyError):
            test_datamanager.do_select(2, table="scibbidy-bibbidy-doo")

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """do_select() should return None when a non-existent opload ID is
        requested."""
        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )

        assert test_datamanager.do_select(100, table="opload") is None


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_insert_sibling(self, test_datamanager):
        """_do_insert_opload() should send the success message after
        successfully inserting an operating load."""
        test_datamanager.do_select_all(
            {"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 2}
        )
        test_datamanager._do_insert_opload(2)

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(3).data["opload"], RAMSTKOpLoad
        )


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """_do_delete() should send the success message with the treelib Tree
        when successfully deleting a test method."""
        test_datamanager._do_delete(2)

        assert test_datamanager.tree.get_node(2) is None
