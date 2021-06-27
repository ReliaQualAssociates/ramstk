# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mechanism.mechanism_integration_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing failure Mechanism integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmMechanism


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmMechanism()
    dut.do_connect(test_program_dao)
    dut.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 6})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_mechanism_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_mechanism_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_mechanism")
    pub.unsubscribe(dut.do_update, "request_update_mechanism")
    pub.unsubscribe(dut.do_select_all, "selected_mode")
    pub.unsubscribe(dut.do_get_tree, "request_get_mechanism_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_mechanism")
    pub.unsubscribe(dut._do_insert_mechanism, "request_insert_mechanism")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_revision_id, fld_hardware_id, fld_mode_id)=(1, 1, "
            '100) is not present in table "ramstk_mode".'
        )
        print("\033[35m\nfail_insert_mechanism topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_revision_id, fld_hardware_id, fld_mode_id)=(10, "
            '1, 100) is not present in table "ramstk_mode".'
        )
        print("\033[35m\nfail_insert_mechanism topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_datamanager):
        """_do_insert_mechanism() should send the fail message if attempting to
        add an operating load to a non-existent mechanism ID."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_mechanism")

        test_datamanager._parent_id = 100
        test_datamanager._do_insert_mechanism()

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_mechanism")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_datamanager):
        """_do_insert_mechanism() should send the success message after
        successfully inserting an operating stress."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_mechanism")

        test_datamanager._revision_id = 10
        test_datamanager._do_insert_mechanism()

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_mechanism")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["mechanism"].description == (
            "Test failure " "mechanism"
        )
        assert tree.get_node(1).data["mechanism"].rpn_detection == 4
        print("\033[36m\nsucceed_update_mechanism topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for mechanism ID 1 was "
            "the wrong type."
        )
        print("\033[35m\nfail_update_mechanism topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_mechanism")

        test_datamanager.tree.get_node(1).data[
            "mechanism"
        ].description = "Test failure mechanism"
        test_datamanager.tree.get_node(1).data["mechanism"].rpn_detection = 4
        test_datamanager.do_update(1, table="mechanism")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_mechanism")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update_all() should broadcast the succeed message on success."""
        pub.sendMessage("request_update_all_mechanisms")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_mechanism")

        _mechanism = test_datamanager.do_select(1, table="mechanism")
        _mechanism.rpn_detection = {1: 2}

        test_datamanager.do_update(1, table="mechanism")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_mechanism")

    @pytest.mark.integration
    def test_do_update_root_node(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        _mechanism = test_datamanager.do_select(1, table="mechanism")
        _mechanism.rpn_detection_new = {1: 2}

        test_datamanager.do_update(0, table="mechanism")
