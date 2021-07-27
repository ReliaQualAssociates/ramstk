# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.program_status.program_status_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Program Status module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKProgramStatus
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmProgramStatus
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKProgramStatus


@pytest.fixture
def mock_program_dao(monkeypatch):
    _status_1 = MockRAMSTKProgramStatus()
    _status_1.revision_id = 1
    _status_1.status_id = 1
    _status_1.cost_remaining = 284.98
    _status_1.date_status = date.today() - timedelta(days=1)
    _status_1.time_remaining = 125.0

    _status_2 = MockRAMSTKProgramStatus()
    _status_2.revision_id = 1
    _status_2.status_id = 2
    _status_2.cost_remaining = 212.32
    _status_2.date_status = date.today()
    _status_2.time_remaining = 112.5

    DAO = MockDAO()
    DAO.table = [
        _status_1,
        _status_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmProgramStatus()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_program_status_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_program_status_attributes")
    pub.unsubscribe(dut.do_update, "request_update_program_status")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_program_status_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_program_status")
    pub.unsubscribe(dut._do_insert_program_status, "request_insert_program_status")
    pub.unsubscribe(dut._do_set_attributes, "succeed_calculate_all_validation_tasks")

    # Delete the device under test.
    del dut


class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Validation data manager."""
        DUT = dmProgramStatus()

        assert isinstance(DUT, dmProgramStatus)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "program_status"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, "selected_revision")
        assert pub.isSubscribed(DUT.do_update, "request_update_program_status")
        assert pub.isSubscribed(DUT.do_update_all, "request_update_all_program_status")
        assert pub.isSubscribed(
            DUT.do_get_attributes, "request_get_program_status_attributes"
        )
        assert pub.isSubscribed(DUT.do_get_tree, "request_get_program_status_tree")
        assert pub.isSubscribed(
            DUT.do_set_attributes, "request_set_program_status_attributes"
        )
        assert pub.isSubscribed(DUT._do_delete, "request_delete_program_status")
        assert pub.isSubscribed(
            DUT._do_insert_program_status, "request_insert_program_status"
        )

        # Unsubscribe from pypubsub topics.
        pub.unsubscribe(DUT.do_get_attributes, "request_get_program_status_attributes")
        pub.unsubscribe(DUT.do_set_attributes, "request_set_program_status_attributes")
        pub.unsubscribe(DUT.do_update, "request_update_program_status")
        pub.unsubscribe(DUT.do_select_all, "selected_revision")
        pub.unsubscribe(DUT.do_get_tree, "request_get_program_status_tree")
        pub.unsubscribe(DUT._do_delete, "request_delete_program_status")
        pub.unsubscribe(DUT._do_insert_program_status, "request_insert_program_status")
        pub.unsubscribe(
            DUT._do_set_attributes, "succeed_calculate_all_validation_tasks"
        )


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKValidation instances on success."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["program_status"],
            MockRAMSTKProgramStatus,
        )

    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """do_select() should return an instance of the RAMSTKValidation on
        success."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        _status = test_datamanager.do_select(2, table="program_status")

        assert isinstance(_status, MockRAMSTKProgramStatus)
        assert _status.cost_remaining == 212.32
        assert _status.time_remaining == 112.5

    @pytest.mark.unit
    def test_do_select_unknown_table(self, test_datamanager):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        with pytest.raises(KeyError):
            test_datamanager.do_select(1, table="scibbidy-bibbidy-doo")

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """do_select() should return None when a non-existent Validation ID is
        requested."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        assert test_datamanager.do_select(100, table="program_status") is None


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_datamanager):
        """_do_insert_opstress() should send the success message after
        successfully inserting an operating load."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_insert_program_status()

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(3).data["program_status"],
            RAMSTKProgramStatus,
        )


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """_do_delete() should send the success message with the treelib
        Tree."""
        test_datamanager._do_delete(2)

        assert test_datamanager.tree.get_node(2) is None


@pytest.mark.usefixtures("test_datamanager")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_on_calculate_plan(self, test_datamanager):
        """_do_set_attributes() should update program status on successful
        calculation of the plan."""
        test_datamanager._do_set_attributes(
            cost_remaining=14608.45, time_remaining=469.00
        )

        _node_id = test_datamanager._dic_status[date.today()]

        assert (
            test_datamanager.tree.get_node(_node_id)
            .data["program_status"]
            .cost_remaining
            == 14608.45
        )
        assert (
            test_datamanager.tree.get_node(_node_id)
            .data["program_status"]
            .time_remaining
            == 469.00
        )
