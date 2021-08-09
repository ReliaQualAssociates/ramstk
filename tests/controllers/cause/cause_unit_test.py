# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.cause.cause_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing failure Cause algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKCause
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmCause
from ramstk.models.programdb import RAMSTKCause


@pytest.fixture
def mock_program_dao(monkeypatch):
    _cause_1 = MockRAMSTKCause()
    _cause_1.revision_id = 1
    _cause_1.mode_id = 6
    _cause_1.mechanism_id = 3
    _cause_1.cause_id = 1
    _cause_1.description = "Test Failure Cause #1 for Mechanism ID 3"
    _cause_1.rpn = 0
    _cause_1.rpn_new = 0
    _cause_1.rpn_detection = 3
    _cause_1.rpn_detection_new = 3
    _cause_1.rpn_occurrence_new = 6
    _cause_1.rpn_occurrence = 4

    _cause_2 = MockRAMSTKCause()
    _cause_2.revision_id = 1
    _cause_2.hardware_id = 1
    _cause_2.mode_id = 6
    _cause_2.mechanism_id = 3
    _cause_2.cause_id = 2
    _cause_2.description = "Test Failure Cause #2 for Mechanism ID 3"
    _cause_2.rpn = 0
    _cause_2.rpn_detection = 6
    _cause_2.rpn_detection_new = 3
    _cause_2.rpn_new = 0
    _cause_2.rpn_occurrence = 6
    _cause_2.rpn_occurrence_new = 4

    DAO = MockDAO()
    DAO.table = [
        _cause_1,
        _cause_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "mode_id": 6,
        "mechanism_id": 3,
        "cause_id": 3,
        "description": "Test Failure Cause #1 for Mechanism ID 3",
    }


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmCause()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_cause_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_cause_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_cause")
    pub.unsubscribe(dut.do_update, "request_update_cause")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_cause_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_cause")
    pub.unsubscribe(dut.do_insert, "request_insert_cause")
    pub.unsubscribe(dut.do_calculate_rpn, "request_calculate_cause_rpn")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """__init__() should return a PoF data manager."""
        assert isinstance(test_datamanager, dmCause)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, MockDAO)
        assert test_datamanager._db_id_colname == "fld_cause_id"
        assert test_datamanager._db_tablename == "ramstk_cause"
        assert test_datamanager._tag == "cause"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert test_datamanager._parent_id == 0
        assert test_datamanager.last_id == 0
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_cause_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "request_set_cause_attributes"
        )
        assert pub.isSubscribed(test_datamanager.do_set_attributes, "wvw_editing_cause")
        assert pub.isSubscribed(test_datamanager.do_update, "request_update_cause")
        assert pub.isSubscribed(test_datamanager.do_get_tree, "request_get_cause_tree")
        assert pub.isSubscribed(test_datamanager.do_delete, "request_delete_cause")
        assert pub.isSubscribed(test_datamanager.do_insert, "request_insert_cause")
        assert pub.isSubscribed(
            test_datamanager.do_calculate_rpn, "request_calculate_cause_rpn"
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_datamanager):
        """should return a Tree() object populated with RAMSTKCause instances."""
        test_datamanager.do_select_all(test_attributes)

        assert isinstance(
            test_datamanager.tree.get_node(1).data["cause"], MockRAMSTKCause
        )
        assert isinstance(
            test_datamanager.tree.get_node(2).data["cause"], MockRAMSTKCause
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_datamanager):
        """do_select() should return an instance of the RAMSTKCause on success."""
        test_datamanager.do_select_all(test_attributes)

        _cause = test_datamanager.do_select(1)

        assert isinstance(_cause, MockRAMSTKCause)
        assert _cause.description == "Test Failure Cause #1 for Mechanism ID 3"
        assert _cause.rpn == 0
        assert _cause.rpn_new == 0
        assert _cause.rpn_detection == 3
        assert _cause.rpn_detection_new == 3
        assert _cause.rpn_occurrence_new == 6
        assert _cause.rpn_occurrence == 4

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_datamanager):
        """do_select() should return None when a non-existent cause ID is requested."""
        test_datamanager.do_select_all(test_attributes)

        assert test_datamanager.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """should add a record to the record tree and update last_id."""
        test_datamanager.do_select_all(test_attributes)
        test_datamanager.do_insert(attributes=test_attributes)

        assert test_datamanager.last_id == 3
        assert isinstance(test_datamanager.tree.get_node(3).data["cause"], RAMSTKCause)


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_datamanager):
        """should remove the record from the record tree and update last_id."""
        test_datamanager.do_select_all(test_attributes)
        test_datamanager.do_delete(2)

        assert test_datamanager.last_id == 1
        assert test_datamanager.tree.get_node(2) is None


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_mechanism_rpn(self, test_attributes, test_datamanager):
        """should calculate the cause RPN."""
        test_datamanager.do_select_all(test_attributes)

        test_datamanager.tree.get_node(1).data["cause"].rpn_occurrence = 8
        test_datamanager.tree.get_node(1).data["cause"].rpn_detection = 3
        test_datamanager.tree.get_node(2).data["cause"].rpn_occurrence = 4
        test_datamanager.tree.get_node(2).data["cause"].rpn_detection = 5

        test_datamanager.do_calculate_rpn(8)

        assert test_datamanager.tree.get_node(1).data["cause"].rpn == 192
        assert test_datamanager.tree.get_node(2).data["cause"].rpn == 160
