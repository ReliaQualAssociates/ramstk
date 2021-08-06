# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.environment.environment_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Environment module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKEnvironment
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmEnvironment
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKEnvironment


@pytest.fixture
def mock_program_dao(monkeypatch):
    _environment_1 = MockRAMSTKEnvironment()
    _environment_1.revision_id = 1
    _environment_1.phase_id = 1
    _environment_1.environment_id = 1
    _environment_1.name = "Condition Name"
    _environment_1.units = "Units"
    _environment_1.minimum = 0.0
    _environment_1.maximum = 0.0
    _environment_1.mean = 0.0
    _environment_1.variance = 0.0
    _environment_1.ramp_rate = 0.0
    _environment_1.low_dwell_time = 0.0
    _environment_1.high_dwell_time = 0.0

    _environment_2 = MockRAMSTKEnvironment()
    _environment_2.revision_id = 1
    _environment_2.phase_id = 1
    _environment_2.environment_id = 2
    _environment_2.name = "Condition Name"
    _environment_2.units = "Units"
    _environment_2.minimum = 0.0
    _environment_2.maximum = 0.0
    _environment_2.mean = 0.0
    _environment_2.variance = 0.0
    _environment_2.ramp_rate = 0.0
    _environment_2.low_dwell_time = 0.0
    _environment_2.high_dwell_time = 0.0

    _environment_3 = MockRAMSTKEnvironment()
    _environment_3.revision_id = 1
    _environment_3.phase_id = 1
    _environment_3.environment_id = 3
    _environment_3.name = "Condition Name"
    _environment_3.units = "Units"
    _environment_3.minimum = 0.0
    _environment_3.maximum = 0.0
    _environment_3.mean = 0.0
    _environment_3.variance = 0.0
    _environment_3.ramp_rate = 0.0
    _environment_3.low_dwell_time = 0.0
    _environment_3.high_dwell_time = 0.0

    DAO = MockDAO()
    DAO.table = [
        _environment_1,
        _environment_2,
        _environment_3,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "phase_id": 1,
        "environment_id": 1,
        "name": "Condition Name",
    }


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmEnvironment()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_environment_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_environment_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_environment")
    pub.unsubscribe(dut.do_update, "request_update_environment")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_environment_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_environment")
    pub.unsubscribe(dut.do_insert, "request_insert_environment")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager(self, test_datamanager):
        """__init__() should return an Environment data manager."""
        assert isinstance(test_datamanager, dmEnvironment)
        assert isinstance(test_datamanager.tree, Tree)
        assert test_datamanager._db_id_colname == "fld_environment_id"
        assert test_datamanager._db_tablename == "ramstk_environment"
        assert test_datamanager._tag == "environment"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_environment_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_tree, "request_get_environment_tree"
        )
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_datamanager.do_update, "request_update_environment"
        )
        assert pub.isSubscribed(
            test_datamanager.do_update_all, "request_update_all_environment"
        )
        assert pub.isSubscribed(
            test_datamanager.do_delete, "request_delete_environment"
        )
        assert pub.isSubscribed(
            test_datamanager.do_insert, "request_insert_environment"
        )


@pytest.mark.usefixtures("test_datamanager", "test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_datamanager):
        """do_select_all() should return a Tree() object populated with RAMSTKMission,
        RAMSTKMissionPhase, and RAMSTKEnvironment instances on success."""
        test_datamanager.do_select_all(attributes=test_attributes)

        assert isinstance(
            test_datamanager.tree.get_node(1).data["environment"], MockRAMSTKEnvironment
        )
        assert isinstance(
            test_datamanager.tree.get_node(2).data["environment"], MockRAMSTKEnvironment
        )
        assert isinstance(
            test_datamanager.tree.get_node(3).data["environment"], MockRAMSTKEnvironment
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_datamanager):
        """do_select() should return the RAMSTKEnvironment instance on success."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _environment = test_datamanager.do_select(1)

        assert isinstance(_environment, MockRAMSTKEnvironment)
        assert _environment.environment_id == 1

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_datamanager):
        """do_select() should return None when a non-existent Revision ID is
        requested."""
        test_datamanager.do_select_all(attributes=test_attributes)

        assert test_datamanager.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """should add the new record to the record tree and update the last_id."""
        test_datamanager.do_select_all(attributes=test_attributes)
        test_datamanager.do_insert(attributes=test_attributes)

        assert test_datamanager.last_id == 4
        assert isinstance(
            test_datamanager.tree.get_node(4).data["environment"], RAMSTKEnvironment
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_datamanager):
        """should remove the deleted record from record tree and update the last_id."""
        test_datamanager.do_select_all(attributes=test_attributes)
        _last_id = test_datamanager.last_id
        test_datamanager.do_delete(_last_id)

        assert test_datamanager.last_id == 2
        assert test_datamanager.tree.get_node(_last_id) is None
