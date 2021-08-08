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
def test_attributes():
    yield {
        "revision_id": 1,
        "status_id": 1,
    }


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
    pub.unsubscribe(dut.do_delete, "request_delete_program_status")
    pub.unsubscribe(dut.do_insert, "request_insert_program_status")
    pub.unsubscribe(dut.do_get_actual_status, "request_get_actual_status")
    pub.unsubscribe(dut._do_set_attributes, "succeed_calculate_all_validation_tasks")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """should return a table manager instance."""
        assert isinstance(test_datamanager, dmProgramStatus)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, MockDAO)
        assert test_datamanager._db_id_colname == "fld_status_id"
        assert test_datamanager._db_tablename == "ramstk_program_status"
        assert test_datamanager._tag == "program_status"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_datamanager.do_update, "request_update_program_status"
        )
        assert pub.isSubscribed(
            test_datamanager.do_update_all, "request_update_all_program_status"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_program_status_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_tree, "request_get_program_status_tree"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "request_set_program_status_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_delete, "request_delete_program_status"
        )
        assert pub.isSubscribed(
            test_datamanager.do_insert, "request_insert_program_status"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_actual_status, "request_get_actual_status"
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_datamanager):
        """should return a record tree populated with DB records."""
        test_datamanager.do_select_all(attributes=test_attributes)

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["program_status"],
            MockRAMSTKProgramStatus,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_datamanager):
        """should return the record for the passed record ID."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _status = test_datamanager.do_select(2)

        assert isinstance(_status, MockRAMSTKProgramStatus)
        assert _status.cost_remaining == 212.32
        assert _status.time_remaining == 112.5

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_datamanager):
        """should return None when a non-existent record ID is requested."""
        test_datamanager.do_select_all(attributes=test_attributes)

        assert test_datamanager.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the insert() method."""

    @pytest.mark.unit
    def test_do_get_new_record(self, test_attributes, test_datamanager):
        """should return a new record instance with ID fields populated."""
        test_datamanager.do_select_all(attributes=test_attributes)
        _new_record = test_datamanager.do_get_new_record(test_attributes)

        assert isinstance(_new_record, RAMSTKProgramStatus)
        assert _new_record.revision_id == 1
        assert _new_record.status_id == 3
        assert _new_record.date_status == date.today()

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """should add a new record to the records tree and update last_id."""
        test_datamanager.do_select_all(attributes=test_attributes)
        test_datamanager.do_insert(attributes=test_attributes)

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(3).data["program_status"],
            RAMSTKProgramStatus,
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_datamanager):
        """should remove the record from the record tree and update last_id."""
        test_datamanager.do_select_all(attributes=test_attributes)
        test_datamanager.do_delete(2)

        assert test_datamanager.tree.get_node(2) is None
