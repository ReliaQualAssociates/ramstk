# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mission_phase.mission_phase_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Mission Phase module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKMissionPhase
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmMissionPhase
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKMissionPhase


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mission_phase_1 = MockRAMSTKMissionPhase()
    _mission_phase_1.revision_id = 1
    _mission_phase_1.mission_id = 1
    _mission_phase_1.phase_id = 1
    _mission_phase_1.description = "Phase #1 for mission #1"
    _mission_phase_1.name = "Start Up"
    _mission_phase_1.phase_start = 0.0
    _mission_phase_1.phase_end = 0.0

    _mission_phase_2 = MockRAMSTKMissionPhase()
    _mission_phase_2.revision_id = 1
    _mission_phase_2.mission_id = 1
    _mission_phase_2.phase_id = 2
    _mission_phase_2.description = "Phase #2 for mission #1"
    _mission_phase_2.name = "Operation"
    _mission_phase_2.phase_start = 0.0
    _mission_phase_2.phase_end = 0.0

    _mission_phase_3 = MockRAMSTKMissionPhase()
    _mission_phase_3.revision_id = 1
    _mission_phase_3.mission_id = 1
    _mission_phase_3.phase_id = 3
    _mission_phase_3.description = "Phase #3 for mission #1"
    _mission_phase_3.name = "Shut Down"
    _mission_phase_3.phase_start = 0.0
    _mission_phase_3.phase_end = 0.0

    DAO = MockDAO()
    DAO.table = [
        _mission_phase_1,
        _mission_phase_2,
        _mission_phase_3,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test class."""
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmMissionPhase()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mission_phase_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mission_phase_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_mission_phase")
    pub.unsubscribe(dut.do_update, "request_update_mission_phase")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mission_phase_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_mission_phase")
    pub.unsubscribe(dut._do_insert_mission_phase, "request_insert_mission_phase")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager(self, test_datamanager):
        """__init__() should return an MissionPhase data manager."""
        assert isinstance(test_datamanager, dmMissionPhase)
        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.dao, MockDAO)
        assert test_datamanager._tag == "mission_phase"
        assert test_datamanager._root == 0
        assert test_datamanager._revision_id == 0
        assert pub.isSubscribed(
            test_datamanager.do_get_attributes, "request_get_mission_phase_attributes"
        )
        assert pub.isSubscribed(
            test_datamanager.do_get_tree, "request_get_mission_phase_tree"
        )
        assert pub.isSubscribed(test_datamanager.do_select_all, "selected_revision")
        assert pub.isSubscribed(
            test_datamanager.do_update, "request_update_mission_phase"
        )
        assert pub.isSubscribed(
            test_datamanager.do_update_all, "request_update_all_mission_phase"
        )
        assert pub.isSubscribed(
            test_datamanager.do_delete, "request_delete_mission_phase"
        )
        assert pub.isSubscribed(
            test_datamanager._do_insert_mission_phase, "request_insert_mission_phase"
        )


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMissionPhase instances on success."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["mission_phase"],
            MockRAMSTKMissionPhase,
        )
        assert isinstance(
            test_datamanager.tree.get_node(2).data["mission_phase"],
            MockRAMSTKMissionPhase,
        )

    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """do_select() should return the RAMSTKMission instance on success."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        _mission_phase = test_datamanager.do_select(1, table="mission_phase")

        assert isinstance(_mission_phase, MockRAMSTKMissionPhase)
        assert _mission_phase.phase_id == 1

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """do_select() should return None when a non-existent Revision ID is
        requested."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        assert test_datamanager.do_select(100, table="mission_phase") is None


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_datamanager):
        """do_insert() should send the success message after successfully
        inserting a new mission."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_insert_mission_phase(mission_id=1)

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(4).data["mission_phase"], RAMSTKMissionPhase
        )


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """_do_delete() should remove the passed mission phase ID."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager.do_delete(1)

        assert test_datamanager.tree.get_node(1) is None
