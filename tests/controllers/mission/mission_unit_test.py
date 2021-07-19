# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mission.mission_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Mission module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKMission
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmMission
from ramstk.db.base import BaseDatabase
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
    pub.unsubscribe(dut._do_delete, "request_delete_mission")
    pub.unsubscribe(dut._do_insert_mission, "request_insert_mission")

    # Delete the device under test.
    del dut


class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return an Mission data manager."""
        DUT = dmMission()

        assert isinstance(DUT, dmMission)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "missions"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_get_attributes, "request_get_mission_attributes")
        assert pub.isSubscribed(DUT.do_get_tree, "request_get_mission_tree")
        assert pub.isSubscribed(DUT.do_select_all, "selected_revision")
        assert pub.isSubscribed(DUT.do_update, "request_update_mission")
        assert pub.isSubscribed(DUT.do_update_all, "request_update_all_missions")
        assert pub.isSubscribed(DUT._do_delete, "request_delete_mission")
        assert pub.isSubscribed(DUT._do_insert_mission, "request_insert_mission")

        pub.unsubscribe(DUT.do_get_attributes, "request_get_mission_attributes")
        pub.unsubscribe(DUT.do_set_attributes, "request_set_mission_attributes")
        pub.unsubscribe(DUT.do_set_attributes, "lvw_editing_usage_profile")
        pub.unsubscribe(DUT.do_update, "request_update_mission")
        pub.unsubscribe(DUT.do_select_all, "selected_revision")
        pub.unsubscribe(DUT.do_get_tree, "request_get_mission_tree")
        pub.unsubscribe(DUT._do_delete, "request_delete_mission")
        pub.unsubscribe(DUT._do_insert_mission, "request_insert_mission")


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """do_select_all() should return a Tree() object on success."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["mission"], MockRAMSTKMission
        )
        assert isinstance(
            test_datamanager.tree.get_node(2).data["mission"], MockRAMSTKMission
        )

    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """do_select() should return the RAMSTKMission instance on success."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        _mission = test_datamanager.do_select(1, table="mission")

        assert isinstance(_mission, MockRAMSTKMission)
        assert _mission.mission_id == 1

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

        assert test_datamanager.do_select(100, table="mission") is None


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_datamanager):
        """do_insert() should send the success message after successfully
        inserting a new mission."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_insert_mission()

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(3).data["mission"], RAMSTKMission
        )


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """_do_delete_mission() should send the success message after
        successfully deleting a mission."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_delete(1)

        assert test_datamanager.tree.get_node(1) is None
