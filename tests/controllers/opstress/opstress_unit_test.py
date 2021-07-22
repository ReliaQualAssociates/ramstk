# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.opstress.opstress_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Operating Stress algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKOpStress
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmOpStress
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKOpStress


@pytest.fixture
def mock_program_dao(monkeypatch):
    _opstress_1 = MockRAMSTKOpStress()
    _opstress_1.revision_id = 1
    _opstress_1.hardware_id = 1
    _opstress_1.mode_id = 1
    _opstress_1.mechanism_id = 1
    _opstress_1.load_id = 1
    _opstress_1.stress_id = 1
    _opstress_1.description = "Test Operating Stress #1"
    _opstress_1.load_history = "Waterfall histogram"
    _opstress_1.measurable_parameter = ""
    _opstress_1.remarks = ""

    _opstress_2 = MockRAMSTKOpStress()
    _opstress_2.revision_id = 1
    _opstress_2.hardware_id = 1
    _opstress_2.mode_id = 1
    _opstress_2.mechanism_id = 1
    _opstress_2.load_id = 1
    _opstress_2.stress_id = 2
    _opstress_2.description = "Test Operating Stress #2"
    _opstress_2.load_history = "Histogram"
    _opstress_2.measurable_parameter = ""
    _opstress_2.remarks = ""

    DAO = MockDAO()
    DAO.table = [
        _opstress_1,
        _opstress_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmOpStress()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opstress_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opstress_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opstress")
    pub.unsubscribe(dut.do_update, "request_update_opstress")
    pub.unsubscribe(dut.do_select_all, "selected_load")
    pub.unsubscribe(dut.do_get_tree, "request_get_opstress_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_opstress")
    pub.unsubscribe(dut._do_insert_opstress, "request_insert_opstress")

    # Delete the device under test.
    del dut


class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.pof
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a PoF data manager."""
        DUT = dmOpStress()

        assert isinstance(DUT, dmOpStress)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "opstress"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert DUT._parent_id == 0
        assert DUT.last_id == 0
        assert pub.isSubscribed(DUT.do_select_all, "selected_load")
        assert pub.isSubscribed(
            DUT.do_get_attributes, "request_get_opstress_attributes"
        )
        assert pub.isSubscribed(
            DUT.do_set_attributes, "request_set_opstress_attributes"
        )
        assert pub.isSubscribed(DUT.do_set_attributes, "wvw_editing_opstress")
        assert pub.isSubscribed(DUT.do_update, "request_update_opstress")
        assert pub.isSubscribed(DUT.do_get_tree, "request_get_opstress_tree")
        assert pub.isSubscribed(DUT._do_delete, "request_delete_opstress")
        assert pub.isSubscribed(DUT._do_insert_opstress, "request_insert_opstress")

        # Unsubscribe from pypubsub topics.
        pub.unsubscribe(DUT.do_get_attributes, "request_get_opstress_attributes")
        pub.unsubscribe(DUT.do_set_attributes, "request_set_opstress_attributes")
        pub.unsubscribe(DUT.do_set_attributes, "wvw_editing_opstress")
        pub.unsubscribe(DUT.do_update, "request_update_opstress")
        pub.unsubscribe(DUT.do_select_all, "selected_load")
        pub.unsubscribe(DUT.do_get_tree, "request_get_opstress_tree")
        pub.unsubscribe(DUT._do_delete, "request_delete_opstress")
        pub.unsubscribe(DUT._do_insert_opstress, "request_insert_opstress")


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKOpStress instances on success."""
        test_datamanager.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["opstress"], MockRAMSTKOpStress
        )

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """do_select() should return an instance of the RAMSTKOpStress on
        success."""
        test_datamanager.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        _opstress = test_datamanager.do_select(2, table="opstress")

        assert isinstance(_opstress, MockRAMSTKOpStress)
        assert _opstress.description == "Test Operating Stress #2"

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select_unknown_table(self, test_datamanager):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        test_datamanager.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        with pytest.raises(KeyError):
            test_datamanager.do_select(2, table="scibbidy-bibbidy-doo")

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """do_select() should return None when a non-existent opstress ID is
        requested."""
        test_datamanager.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        assert test_datamanager.do_select(100, table="opstress") is None


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.pof
    @pytest.mark.unit
    def test_do_insert_sibling(self, test_datamanager):
        """_do_insert_opstress() should send the success message after
        successfully inserting an operating load."""
        test_datamanager.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        test_datamanager._do_insert_opstress(2)

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(3).data["opstress"], RAMSTKOpStress
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
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        test_datamanager._do_delete(2)

        assert test_datamanager.tree.get_node(2) is None
