# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_mode.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing PoF algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO, MockRAMSTKMode
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmMode
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKMode


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mode_1 = MockRAMSTKMode()
    _mode_1.revision_id = 1
    _mode_1.hardware_id = 1
    _mode_1.mode_id = 1
    _mode_1.effect_local = ""
    _mode_1.mission = "Default Mission"
    _mode_1.other_indications = ""
    _mode_1.mode_criticality = 0.0
    _mode_1.single_point = 0
    _mode_1.design_provisions = ""
    _mode_1.type_id = 0
    _mode_1.rpn_severity_new = 1
    _mode_1.effect_next = ""
    _mode_1.detection_method = ""
    _mode_1.operator_actions = ""
    _mode_1.critical_item = 0
    _mode_1.hazard_rate_source = ""
    _mode_1.severity_class = ""
    _mode_1.description = "Test Failure Mode #1"
    _mode_1.mission_phase = ""
    _mode_1.mode_probability = ""
    _mode_1.remarks = ""
    _mode_1.mode_ratio = 0.0
    _mode_1.mode_hazard_rate = 0.0
    _mode_1.rpn_severity = 1
    _mode_1.isolation_method = ""
    _mode_1.effect_end = ""
    _mode_1.mode_op_time = 0.0
    _mode_1.effect_probability = 0.8

    _mode_2 = MockRAMSTKMode()
    _mode_2.revision_id = 1
    _mode_2.hardware_id = 1
    _mode_2.mode_id = 2
    _mode_2.effect_local = ""
    _mode_2.mission = "Default Mission"
    _mode_2.other_indications = ""
    _mode_2.mode_criticality = 0.0
    _mode_2.single_point = 0
    _mode_2.design_provisions = ""
    _mode_2.type_id = 0
    _mode_2.rpn_severity_new = 1
    _mode_2.effect_next = ""
    _mode_2.detection_method = ""
    _mode_2.operator_actions = ""
    _mode_2.critical_item = 0
    _mode_2.hazard_rate_source = ""
    _mode_2.severity_class = ""
    _mode_2.description = "Test Failure Mode #2"
    _mode_2.mission_phase = ""
    _mode_2.mode_probability = ""
    _mode_2.remarks = ""
    _mode_2.mode_ratio = 0.0
    _mode_2.mode_hazard_rate = 0.0
    _mode_2.rpn_severity = 1
    _mode_2.isolation_method = ""
    _mode_2.effect_end = ""
    _mode_2.mode_op_time = 0.0
    _mode_2.effect_probability = 0.0

    DAO = MockDAO()
    DAO.table = [
        _mode_1,
        _mode_2,
    ]

    yield DAO


@pytest.fixture(scope="function")
def test_datamanager(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = dmMode()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mode_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mode_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_mode")
    pub.unsubscribe(dut.do_update, "request_update_mode")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_mode_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_mode")
    pub.unsubscribe(dut._do_insert_mode, "request_insert_mode")

    # Delete the device under test.
    del dut


class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a PoF data manager."""
        DUT = dmMode()

        assert isinstance(DUT, dmMode)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "modes"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert DUT._parent_id == 0
        assert DUT.last_id == 0
        assert pub.isSubscribed(DUT.do_get_attributes, "request_get_mode_attributes")
        assert pub.isSubscribed(DUT.do_get_tree, "request_get_mode_tree")
        assert pub.isSubscribed(DUT.do_select_all, "selected_revision")
        assert pub.isSubscribed(DUT.do_update, "request_update_mode")
        assert pub.isSubscribed(DUT.do_update_all, "request_update_all_modes")
        assert pub.isSubscribed(DUT._do_delete, "request_delete_mode")
        assert pub.isSubscribed(DUT._do_insert_mode, "request_insert_mode")

        pub.unsubscribe(DUT.do_get_attributes, "request_get_mode_attributes")
        pub.unsubscribe(DUT.do_set_attributes, "request_set_mode_attributes")
        pub.unsubscribe(DUT.do_set_attributes, "wvw_editing_mode")
        pub.unsubscribe(DUT.do_update, "request_update_mode")
        pub.unsubscribe(DUT.do_select_all, "selected_revision")
        pub.unsubscribe(DUT.do_get_tree, "request_get_mode_tree")
        pub.unsubscribe(DUT._do_delete, "request_delete_mode")
        pub.unsubscribe(DUT._do_insert_mode, "request_insert_mode")


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMode, RAMSTKMechanism, RAMSTKOpLoad, RAMSTKOpStress, and
        RAMSTKTestMethod instances on success."""
        test_datamanager.do_select_all({"revision_id": 1, "hardware_id": 1})

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(
            test_datamanager.tree.get_node(1).data["mode"], MockRAMSTKMode
        )

    @pytest.mark.unit
    def test_do_select(self, test_datamanager):
        """do_select() should return an instance of the RAMSTKMode on
        success."""
        test_datamanager.do_select_all({"revision_id": 1, "hardware_id": 1})

        _mode = test_datamanager.do_select(1, table="mode")

        assert isinstance(_mode, MockRAMSTKMode)
        assert _mode.effect_probability == 0.8
        assert _mode.description == "Test Failure Mode #1"

    @pytest.mark.unit
    def test_do_select_unknown_table(self, test_datamanager):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        test_datamanager.do_select_all({"revision_id": 1, "hardware_id": 1})

        with pytest.raises(KeyError):
            test_datamanager.do_select(2, table="scibbidy-bibbidy-doo")

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_datamanager):
        """do_select() should return None when a non-existent PoF ID is
        requested."""
        test_datamanager.do_select_all({"revision_id": 1, "hardware_id": 1})

        assert test_datamanager.do_select(100, table="mode") is None


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_datamanager):
        """_do_insert_opload() should send the success message after
        successfully inserting an operating load."""
        test_datamanager.do_select_all({"revision_id": 1, "hardware_id": 1})
        test_datamanager._do_insert_mode()

        assert isinstance(test_datamanager.tree, Tree)
        assert isinstance(test_datamanager.tree.get_node(3).data["mode"], RAMSTKMode)
        assert test_datamanager.tree.get_node(3).data["mode"].mode_id == 3
        assert test_datamanager.tree.get_node(3).data["mode"].description is None


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_mode topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent mode ID 300."
        )
        print("\033[35m\nfail_delete_mode topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent mode ID 2."
        )
        print("\033[35m\nfail_delete_mode topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, test_datamanager):
        """_do_delete() should send the success message with the treelib Tree
        when successfully deleting a test method."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_mode")

        test_datamanager.do_select_all({"revision_id": 1, "hardware_id": 1})
        test_datamanager._do_delete(4)

        assert test_datamanager.tree.get_node(4) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_mode")

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to delete
        a node ID that doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_mode")

        test_datamanager.do_select_all({"revision_id": 1, "hardware_id": 1})
        test_datamanager._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_mode")

    @pytest.mark.unit
    def test_do_delete_not_in_tree(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_mode")

        test_datamanager.do_select_all({"revision_id": 1, "hardware_id": 1})
        test_datamanager.tree.remove_node(2)
        test_datamanager._do_delete(2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_mode")
