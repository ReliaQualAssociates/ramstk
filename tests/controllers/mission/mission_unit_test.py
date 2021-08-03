# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mission.mission_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Mission module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKMission
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmMission
from ramstk.models.programdb import RAMSTKMission


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mission_1 = MockRAMSTKMission()
    _mission_1.revision_id = 1
    _mission_1.mission_id = 1
    _mission_1.description = "Test mission #1"
    _mission_1.mission_time = 100.0
    _mission_1.time_units = "hours"

    _mission_2 = MockRAMSTKMission()
    _mission_2.revision_id = 1
    _mission_2.mission_id = 2
    _mission_2.description = "Test mission #2"
    _mission_2.mission_time = 24.0
    _mission_2.time_units = "hours"

    DAO = MockDAO()
    DAO.table = [
        _mission_1,
        _mission_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_attributes():
    yield {"revision_id": 1, "mission_id": 1}


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmMission()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mission_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mission_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_usage_profile")
    pub.unsubscribe(dut.do_update, "request_update_mission")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mission_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mission")
    pub.unsubscribe(dut.do_insert, "request_insert_mission")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self, test_datamanager):
        """__init__() should return an Mission data manager."""
        assert isinstance(test_datamanager, dmMission)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, MockDAO)
        assert test_datamanager._db_id_colname == "fld_mission_id"
        assert test_datamanager._db_tablename == "ramstk_mission"
        assert test_datamanager._tag == "mission"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_mission_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_tree, "request_get_mission_tree"
        )
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_datamanager.do_update, "request_update_mission")
        assert pub.isSubscribed(
            test_datamanager.do_update_all, "request_update_all_mission"
        )
        assert pub.isSubscribed(test_datamanager.do_delete, "request_delete_mission")
        assert pub.isSubscribed(test_datamanager.do_insert, "request_insert_mission")


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_datamanager):
        """do_select_all() should return a Tree() object on success."""
        test_datamanager.do_select_all(attributes=test_attributes)

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["mission"], MockRAMSTKMission
        )
        assert isinstance(
            test_datamanager.tree.get_node(2).data["mission"], MockRAMSTKMission
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_datamanager):
        """do_select() should return the RAMSTKMission instance on success."""
        test_datamanager.do_select_all(attributes=test_attributes)

        _mission = test_datamanager.do_select(1)

        assert isinstance(_mission, MockRAMSTKMission)
        assert _mission.mission_id == 1

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
        """do_insert() should send the success message after successfully
        inserting a new mission."""
        test_datamanager.do_select_all(attributes=test_attributes)
        test_datamanager.do_insert(attributes=test_attributes)

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(3).data["mission"], RAMSTKMission
        )


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_datamanager):
        """_do_delete_mission() should send the success message after
        successfully deleting a mission."""
        test_datamanager.do_select_all(attributes=test_attributes)
        test_datamanager.do_delete(1)

        assert test_datamanager.tree.get_node(1) is None
