# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.revision.revision_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing revision module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKRevision
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmRevision
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKRevision


@pytest.fixture
def mock_program_dao(monkeypatch):
    _revision_1 = MockRAMSTKRevision()
    _revision_1.revision_id = 1
    _revision_1.availability_logistics = 0.9986
    _revision_1.availability_mission = 0.99934
    _revision_1.cost = 12532.15
    _revision_1.cost_failure = 0.0000352
    _revision_1.cost_hour = 1.2532
    _revision_1.hazard_rate_active = 0.0
    _revision_1.hazard_rate_dormant = 0.0
    _revision_1.hazard_rate_logistics = 0.0
    _revision_1.hazard_rate_mission = 0.0
    _revision_1.hazard_rate_software = 0.0
    _revision_1.mmt = 0.0
    _revision_1.mcmt = 0.0
    _revision_1.mpmt = 0.0
    _revision_1.mtbf_logistics = 0.0
    _revision_1.mtbf_mission = 0.0
    _revision_1.mttr = 0.0
    _revision_1.name = "Original Revision"
    _revision_1.reliability_logistics = 0.99986
    _revision_1.reliability_mission = 0.99992
    _revision_1.remarks = "This is the original revision."
    _revision_1.revision_code = "Rev. -"
    _revision_1.program_time = 2562
    _revision_1.program_time_sd = 26.83
    _revision_1.program_cost = 26492.83
    _revision_1.program_cost_sd = 15.62

    _revision_2 = MockRAMSTKRevision()
    _revision_2.revision_id = 2
    _revision_2.availability_logistics = 1.0
    _revision_2.availability_mission = 1.0
    _revision_2.cost = 0.0
    _revision_2.cost_failure = 0.0
    _revision_2.cost_hour = 0.0
    _revision_2.hazard_rate_active = 0.0
    _revision_2.hazard_rate_dormant = 0.0
    _revision_2.hazard_rate_logistics = 0.0
    _revision_2.hazard_rate_mission = 0.0
    _revision_2.hazard_rate_software = 0.0
    _revision_2.mmt = 0.0
    _revision_2.mcmt = 0.0
    _revision_2.mpmt = 0.0
    _revision_2.mtbf_logistics = 0.0
    _revision_2.mtbf_mission = 0.0
    _revision_2.mttr = 0.0
    _revision_2.name = "Revision A"
    _revision_2.reliability_logistics = 1.0
    _revision_2.reliability_mission = 1.0
    _revision_2.remarks = "This is the second revision."
    _revision_2.revision_code = "Rev. A"
    _revision_2.program_time = 0
    _revision_2.program_time_sd = 0.0
    _revision_2.program_cost = 0.0
    _revision_2.program_cost_sd = 0.0

    DAO = MockDAO()
    DAO.table = [
        _revision_1,
        _revision_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Test fixture for Function data manager."""
    dut = dmRevision()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_revision_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_revision_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_revision")
    pub.unsubscribe(dut.do_update, "request_update_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_revision_tree")
    pub.unsubscribe(dut.do_select_all, "request_retrieve_revisions")
    pub.unsubscribe(dut._do_delete, "request_delete_revision")
    pub.unsubscribe(dut._do_insert_revision, "request_insert_revision")

    # Delete the device under test.
    del dut


class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Revision data manager."""
        DUT = dmRevision()

        assert isinstance(DUT, dmRevision)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "revision"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, "request_retrieve_revisions")
        assert pub.isSubscribed(DUT.do_update, "request_update_revision")
        assert pub.isSubscribed(DUT.do_update_all, "request_update_all_revision")
        assert pub.isSubscribed(
            DUT.do_get_attributes, "request_get_revision_attributes"
        )
        assert pub.isSubscribed(DUT.do_get_tree, "request_get_revision_tree")
        assert pub.isSubscribed(
            DUT.do_set_attributes, "request_set_revision_attributes"
        )
        assert pub.isSubscribed(DUT._do_delete, "request_delete_revision")
        assert pub.isSubscribed(DUT._do_insert_revision, "request_insert_revision")

        # Unsubscribe from pypubsub topics.
        pub.unsubscribe(DUT.do_get_attributes, "request_get_revision_attributes")
        pub.unsubscribe(DUT.do_set_attributes, "request_set_revision_attributes")
        pub.unsubscribe(DUT.do_set_attributes, "wvw_editing_revision")
        pub.unsubscribe(DUT.do_update, "request_update_revision")
        pub.unsubscribe(DUT.do_get_tree, "request_get_revision_tree")
        pub.unsubscribe(DUT.do_select_all, "request_retrieve_revisions")
        pub.unsubscribe(DUT._do_delete, "request_delete_revision")
        pub.unsubscribe(DUT._do_insert_revision, "request_insert_revision")


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKRevision instances on success."""
        test_datamanager.do_select_all()

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["revision"], MockRAMSTKRevision
        )

    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """do_select() should return an instance of the RAMSTKRevision on
        success."""
        test_datamanager.do_select_all()

        _revision = test_datamanager.do_select(1, table="revision")

        assert isinstance(_revision, MockRAMSTKRevision)
        assert _revision.availability_logistics == 0.9986
        assert _revision.name == "Original Revision"

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, test_datamanager):
        """do_select() should clear any existing tree when selecting
        revisions."""
        test_datamanager.do_select_all()
        test_datamanager.do_select_all()

    @pytest.mark.unit
    def test_do_select_unknown_table(self, test_datamanager):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        test_datamanager.do_select_all()

        with pytest.raises(KeyError):
            test_datamanager.do_select(1, table="scibbidy-bibbidy-doo")

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """do_select() should return None when a non-existent Revision ID is
        requested."""
        test_datamanager.do_select_all()

        assert test_datamanager.do_select(100, table="revision") is None


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_datamanager):
        """_do_insert_revision() should send the success message after
        successfully inserting a new revision."""
        test_datamanager.do_select_all()
        test_datamanager._do_insert_revision()

        assert isinstance(
            test_datamanager.tree.get_node(3).data["revision"], RAMSTKRevision
        )
        assert test_datamanager.tree.get_node(3).data["revision"].revision_id == 3
        assert test_datamanager.tree.get_node(3).data["revision"].name == "New Revision"


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """_do_delete() should send the success message with the treelib
        Tree."""
        test_datamanager.do_select_all()
        test_datamanager._do_delete(2)

        assert test_datamanager.last_id == 1
        assert test_datamanager.tree.get_node(2) is None
