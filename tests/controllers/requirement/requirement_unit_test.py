# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.requirement.requirement_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Requirement module algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKRequirement
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmRequirement
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKRequirement


@pytest.fixture
def mock_program_dao(monkeypatch):
    _requirement_1 = MockRAMSTKRequirement()
    _requirement_1.revision_id = 1
    _requirement_1.requirement_id = 1
    _requirement_1.derived = 0
    _requirement_1.description = ""
    _requirement_1.figure_number = ""
    _requirement_1.owner = 0
    _requirement_1.page_number = ""
    _requirement_1.parent_id = 0
    _requirement_1.priority = 0
    _requirement_1.requirement_code = "REL.1"
    _requirement_1.specification = ""
    _requirement_1.requirement_type = 0
    _requirement_1.validated = 0
    _requirement_1.validated_date = date.today()
    _requirement_1.q_clarity_0 = 0
    _requirement_1.q_clarity_1 = 0
    _requirement_1.q_clarity_2 = 0
    _requirement_1.q_clarity_3 = 0
    _requirement_1.q_clarity_4 = 0
    _requirement_1.q_clarity_5 = 0
    _requirement_1.q_clarity_6 = 0
    _requirement_1.q_clarity_7 = 0
    _requirement_1.q_clarity_8 = 0
    _requirement_1.q_complete_0 = 0
    _requirement_1.q_complete_1 = 0
    _requirement_1.q_complete_2 = 0
    _requirement_1.q_complete_3 = 0
    _requirement_1.q_complete_4 = 0
    _requirement_1.q_complete_5 = 0
    _requirement_1.q_complete_6 = 0
    _requirement_1.q_complete_7 = 0
    _requirement_1.q_complete_8 = 0
    _requirement_1.q_complete_9 = 0
    _requirement_1.q_consistent_0 = 0
    _requirement_1.q_consistent_1 = 0
    _requirement_1.q_consistent_2 = 0
    _requirement_1.q_consistent_3 = 0
    _requirement_1.q_consistent_4 = 0
    _requirement_1.q_consistent_5 = 0
    _requirement_1.q_consistent_6 = 0
    _requirement_1.q_consistent_7 = 0
    _requirement_1.q_consistent_8 = 0
    _requirement_1.q_verifiable_0 = 0
    _requirement_1.q_verifiable_1 = 0
    _requirement_1.q_verifiable_2 = 0
    _requirement_1.q_verifiable_3 = 0
    _requirement_1.q_verifiable_4 = 0
    _requirement_1.q_verifiable_5 = 0

    _requirement_2 = MockRAMSTKRequirement()
    _requirement_2.revision_id = 1
    _requirement_2.requirement_id = 2
    _requirement_2.derived = 1
    _requirement_2.description = "Derived requirement #1 for base " "requirement #1."
    _requirement_2.figure_number = ""
    _requirement_2.owner = 0
    _requirement_2.page_number = ""
    _requirement_2.parent_id = 1
    _requirement_2.priority = 0
    _requirement_2.requirement_code = "REL.1.1"
    _requirement_2.specification = ""
    _requirement_2.requirement_type = 0
    _requirement_2.validated = 0
    _requirement_2.validated_date = date.today()
    _requirement_2.q_clarity_0 = 0
    _requirement_2.q_clarity_1 = 0
    _requirement_2.q_clarity_2 = 0
    _requirement_2.q_clarity_3 = 0
    _requirement_2.q_clarity_4 = 0
    _requirement_2.q_clarity_5 = 0
    _requirement_2.q_clarity_6 = 0
    _requirement_2.q_clarity_7 = 0
    _requirement_2.q_clarity_8 = 0
    _requirement_2.q_complete_0 = 0
    _requirement_2.q_complete_1 = 0
    _requirement_2.q_complete_2 = 0
    _requirement_2.q_complete_3 = 0
    _requirement_2.q_complete_4 = 0
    _requirement_2.q_complete_5 = 0
    _requirement_2.q_complete_6 = 0
    _requirement_2.q_complete_7 = 0
    _requirement_2.q_complete_8 = 0
    _requirement_2.q_complete_9 = 0
    _requirement_2.q_consistent_0 = 0
    _requirement_2.q_consistent_1 = 0
    _requirement_2.q_consistent_2 = 0
    _requirement_2.q_consistent_3 = 0
    _requirement_2.q_consistent_4 = 0
    _requirement_2.q_consistent_5 = 0
    _requirement_2.q_consistent_6 = 0
    _requirement_2.q_consistent_7 = 0
    _requirement_2.q_consistent_8 = 0
    _requirement_2.q_verifiable_0 = 0
    _requirement_2.q_verifiable_1 = 0
    _requirement_2.q_verifiable_2 = 0
    _requirement_2.q_verifiable_3 = 0
    _requirement_2.q_verifiable_4 = 0
    _requirement_2.q_verifiable_5 = 0

    DAO = MockDAO()
    DAO.table = [
        _requirement_1,
        _requirement_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmRequirement()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_requirement_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_requirement_attributes")
    pub.unsubscribe(dut.do_set_attributes, "mvw_editing_requirement")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_requirement")
    pub.unsubscribe(dut.do_update, "request_update_requirement")
    pub.unsubscribe(dut.do_create_all_codes, "request_create_all_requirement_codes")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_requirement_tree")
    pub.unsubscribe(dut.do_create_code, "request_create_requirement_code")
    pub.unsubscribe(dut._do_delete, "request_delete_requirement")
    pub.unsubscribe(dut._do_insert_requirement, "request_insert_requirement")

    # Delete the device under test.
    del dut


class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Requirement data manager."""
        DUT = dmRequirement()

        assert isinstance(DUT, dmRequirement)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "requirement"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, "selected_revision")
        assert pub.isSubscribed(DUT.do_update, "request_update_requirement")
        assert pub.isSubscribed(DUT.do_update_all, "request_update_all_requirement")
        assert pub.isSubscribed(
            DUT.do_get_attributes, "request_get_requirement_attributes"
        )
        assert pub.isSubscribed(DUT.do_get_tree, "request_get_requirement_tree")
        assert pub.isSubscribed(
            DUT.do_set_attributes, "request_set_requirement_attributes"
        )
        assert pub.isSubscribed(DUT.do_set_attributes, "wvw_editing_requirement")
        assert pub.isSubscribed(DUT.do_create_code, "request_create_requirement_code")
        assert pub.isSubscribed(DUT._do_delete, "request_delete_requirement")
        assert pub.isSubscribed(
            DUT._do_insert_requirement, "request_insert_requirement"
        )

        # Unsubscribe from pypubsub topics.
        pub.unsubscribe(DUT.do_get_attributes, "request_get_requirement_attributes")
        pub.unsubscribe(DUT.do_set_attributes, "request_set_requirement_attributes")
        pub.unsubscribe(DUT.do_set_attributes, "mvw_editing_requirement")
        pub.unsubscribe(DUT.do_set_attributes, "wvw_editing_requirement")
        pub.unsubscribe(DUT.do_update, "request_update_requirement")
        pub.unsubscribe(DUT.do_create_all_codes, "request_create_all_requirement_codes")
        pub.unsubscribe(DUT.do_select_all, "selected_revision")
        pub.unsubscribe(DUT.do_get_tree, "request_get_requirement_tree")
        pub.unsubscribe(DUT.do_create_code, "request_create_requirement_code")
        pub.unsubscribe(DUT._do_delete, "request_delete_requirement")
        pub.unsubscribe(DUT._do_insert_requirement, "request_insert_requirement")


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """do_select_all() should return a Tree object populated with
        RAMSTKRequirement instances on success."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.tree.get_node(1).data, dict)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["requirement"], MockRAMSTKRequirement
        )

    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """do_select() should return an instance of the RAMSTKRequirement on
        success."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        _requirement = test_datamanager.do_select(1, table="requirement")

        assert isinstance(_requirement, MockRAMSTKRequirement)
        assert _requirement.description == ""
        assert _requirement.priority == 0

    @pytest.mark.unit
    def test_do_select_unknown_table(self, test_datamanager):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        with pytest.raises(KeyError):
            test_datamanager.do_select(1, table="scibbidy-bibbidy-doo")

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """do_select() should return None when a non-existent Requirement ID is
        requested."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})

        assert test_datamanager.do_select(100, table="requirement") is None


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_datamanager):
        """do_insert() should send the success message after successfully
        inserting a new top-level requirement."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_insert_requirement(parent_id=0)

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(3).data["requirement"], RAMSTKRequirement
        )
        assert test_datamanager.tree.get_node(3).data["requirement"].requirement_id == 3
        assert (
            test_datamanager.tree.get_node(3).data["requirement"].description
            == "New Requirement"
        )

    @pytest.mark.unit
    def test_do_insert_child(self, test_datamanager):
        """do_insert() should send the success message after successfully
        inserting a new child requirement."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_insert_requirement(parent_id=1)

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(3).data["requirement"], RAMSTKRequirement
        )
        assert test_datamanager.tree.get_node(3).data["requirement"].parent_id == 1
        assert test_datamanager.tree.get_node(3).data["requirement"].requirement_id == 3
        assert (
            test_datamanager.tree.get_node(3).data["requirement"].description
            == "New Requirement"
        )


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """_do_delete() should send the success message with the treelib
        Tree."""
        test_datamanager.do_select_all(attributes={"revision_id": 1})
        test_datamanager._do_delete(test_datamanager.last_id)

        assert test_datamanager.last_id == 1
