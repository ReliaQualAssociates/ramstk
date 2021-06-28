# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.opload.opload_integration_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing operating load integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmOpLoad


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmOpLoad()
    dut.do_connect(test_program_dao)
    dut.do_select_all(
        attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6, "mechanism_id": 1}
    )

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_opload_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_opload")
    pub.unsubscribe(dut.do_update, "request_update_opload")
    pub.unsubscribe(dut.do_select_all, "selected_mechanism")
    pub.unsubscribe(dut.do_get_tree, "request_get_opload_tree")
    pub.unsubscribe(dut._do_delete, "request_delete_opload")
    pub.unsubscribe(dut._do_insert_opload, "request_insert_opload")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_revision_id, fld_hardware_id, fld_mode_id, "
            "fld_mechanism_id)=(1, 1, 6, 100) is not present in table "
            '"ramstk_mechanism".'
        )
        print("\033[35m\nfail_insert_opload topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_revision_id, fld_hardware_id, fld_mode_id, "
            "fld_mechanism_id)=(10, 1, 6, 1) is not present in table "
            '"ramstk_mechanism".'
        )
        print("\033[35m\nfail_insert_opload topic was broadcast.")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_datamanager):
        """_do_insert_opload() should send the fail message if attempting to
        add an operating load to a non-existent opload ID."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_opload")

        test_datamanager._parent_id = 100
        test_datamanager._do_insert_opload(100)

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_opload")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_datamanager):
        """_do_insert_opload() should send the success message after
        successfully inserting an operating stress."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_opload")

        test_datamanager._revision_id = 10
        test_datamanager._do_insert_opload(1)

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_opload")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["opload"].description == ("Test failure " "opload")
        assert tree.get_node(1).data["opload"].rpn_detection == 4
        print("\033[36m\nsucceed_update_opload topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for opload ID 1 was "
            "the wrong type."
        )
        print("\033[35m\nfail_update_opload topic was broadcast")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_opload")

        test_datamanager.tree.get_node(1).data[
            "opload"
        ].description = "Test failure opload"
        test_datamanager.tree.get_node(1).data["opload"].rpn_detection = 4
        test_datamanager.do_update(1, table="opload")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_opload")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update_all() should broadcast the succeed message on success."""
        pub.sendMessage("request_update_all_oploads")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_opload")

        _opload = test_datamanager.do_select(1, table="opload")
        _opload.rpn_detection = {1: 2}

        test_datamanager.do_update(1, table="opload")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_opload")

    @pytest.mark.pof
    @pytest.mark.integration
    def test_do_update_root_node(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        _opload = test_datamanager.do_select(1, table="opload")
        _opload.rpn_detection_new = {1: 2}

        test_datamanager.do_update(0, table="opload")
