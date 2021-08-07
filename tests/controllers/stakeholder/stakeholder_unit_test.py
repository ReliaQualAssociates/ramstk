# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.stakeholder.stakeholder_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Stakeholder module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKStakeholder
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmStakeholder
from ramstk.models.programdb import RAMSTKStakeholder


@pytest.fixture
def mock_program_dao(monkeypatch):
    _stakeholder_1 = MockRAMSTKStakeholder()
    _stakeholder_1.revision_id = 1
    _stakeholder_1.requirement_id = 1
    _stakeholder_1.stakeholder_id = 1
    _stakeholder_1.customer_rank = 1
    _stakeholder_1.description = "Stakeholder Input"
    _stakeholder_1.group = ""
    _stakeholder_1.improvement = 0.0
    _stakeholder_1.overall_weight = 0.0
    _stakeholder_1.planned_rank = 1
    _stakeholder_1.priority = 1
    _stakeholder_1.stakeholder = ""
    _stakeholder_1.user_float_1 = 1.0
    _stakeholder_1.user_float_2 = 1.0
    _stakeholder_1.user_float_3 = 1.0
    _stakeholder_1.user_float_4 = 1.0
    _stakeholder_1.user_float_5 = 1.0

    _stakeholder_2 = MockRAMSTKStakeholder()
    _stakeholder_2.revision_id = 1
    _stakeholder_2.requirement_id = 1
    _stakeholder_2.stakeholder_id = 2
    _stakeholder_2.customer_rank = 1
    _stakeholder_2.description = "Stakeholder Input"
    _stakeholder_2.group = ""
    _stakeholder_2.improvement = 0.0
    _stakeholder_2.overall_weight = 0.0
    _stakeholder_2.planned_rank = 1
    _stakeholder_2.priority = 1
    _stakeholder_2.stakeholder = ""
    _stakeholder_2.user_float_1 = 1.0
    _stakeholder_2.user_float_2 = 1.0
    _stakeholder_2.user_float_3 = 1.0
    _stakeholder_2.user_float_4 = 1.0
    _stakeholder_2.user_float_5 = 1.0

    DAO = MockDAO()
    DAO.table = [
        _stakeholder_1,
        _stakeholder_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "stakeholder_id": 1,
    }


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmStakeholder()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_stakeholder_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_stakeholder_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_stakeholder")
    pub.unsubscribe(dut.do_update, "request_update_stakeholder")
    pub.unsubscribe(dut.do_get_tree, "request_get_stakeholder_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_stakeholder")
    pub.unsubscribe(dut.do_insert, "request_insert_stakeholder")
    pub.unsubscribe(dut.do_calculate_stakeholder, "request_calculate_stakeholder")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for testing controller initialization."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """should return a table manager instance."""
        assert isinstance(test_datamanager, dmStakeholder)
        assert isinstance(test_datamanager.tree, Tree)
        assert test_datamanager._db_id_colname == "fld_stakeholder_id"
        assert test_datamanager._db_tablename == "ramstk_stakeholder"
        assert test_datamanager._tag == "stakeholder"
        assert test_datamanager._root == 0
        assert test_datamanager._lst_id_columns == [
            "revision_id",
            "stakeholder_id",
        ]
        assert test_datamanager._revision_id == 0
        assert test_datamanager._record == RAMSTKStakeholder
        assert test_datamanager.last_id == 0
        assert test_datamanager.pkey == "stakeholder_id"
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_datamanager.do_update, "request_update_stakeholder"
        )
        assert pub.isSubscribed(
            test_datamanager.do_update_all, "request_update_all_stakeholder"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_stakeholder_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_tree, "request_get_stakeholder_tree"
        )
        assert pub.isSubscribed(
            test_datamanager.do_set_attributes, "request_set_stakeholder_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_delete, "request_delete_stakeholder"
        )
        assert pub.isSubscribed(
            test_datamanager.do_insert, "request_insert_stakeholder"
        )
        assert pub.isSubscribed(
            test_datamanager.do_calculate_stakeholder, "request_calculate_stakeholder"
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_datamanager):
        """should return a record tree populated with DB records."""
        test_datamanager.do_select_all(attributes=test_attributes)

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.tree.get_node(1).data, dict)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["stakeholder"], MockRAMSTKStakeholder
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_datamanager):
        """should return the record for the passed record ID."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _stakeholder = test_datamanager.do_select(1)

        assert isinstance(_stakeholder, MockRAMSTKStakeholder)
        assert _stakeholder.description == "Stakeholder Input"
        assert _stakeholder.priority == 1

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

        assert isinstance(_new_record, RAMSTKStakeholder)
        assert _new_record.revision_id == 1
        assert _new_record.stakeholder_id == 3

    @pytest.mark.unit
    def test_do_insert(self, test_attributes, test_datamanager):
        """should add a new record to the records tree and update last_id."""
        test_datamanager.do_select_all(attributes=test_attributes)
        test_datamanager.do_insert(attributes=test_attributes)

        assert test_datamanager.last_id == 3
        assert isinstance(
            test_datamanager.tree.get_node(3).data["stakeholder"], RAMSTKStakeholder
        )
        assert test_datamanager.tree.get_node(3).data["stakeholder"].stakeholder_id == 3
        assert (
            test_datamanager.tree.get_node(3).data["stakeholder"].description
            == "New Stakeholder Input"
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_datamanager):
        """should remove the record from the record tree and update last_id."""
        test_datamanager.do_select_all(attributes=test_attributes)
        _last_id = test_datamanager.last_id
        test_datamanager.do_delete(test_datamanager.last_id)

        assert test_datamanager.last_id == 1
        assert test_datamanager.tree.get_node(_last_id) is None


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    @pytest.mark.unit
    def test_do_calculate_improvement(self, test_attributes, test_datamanager):
        """should calculate the record's improvement factor and overall weight."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _stakeholder = test_datamanager.do_select(1)
        _stakeholder.planned_rank = 3
        _stakeholder.customer_rank = 2
        _stakeholder.priority = 4
        _stakeholder.user_float_1 = 2.6
        test_datamanager.do_update(1)

        test_datamanager._do_calculate_improvement(1)
        _attributes = test_datamanager.do_select(1).get_attributes()

        assert _attributes["improvement"] == 1.2
        assert _attributes["overall_weight"] == 12.48
