# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.revision.revision_integration_test.py is
#       part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing revision module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmRevision


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    dut = dmRevision()
    dut.do_connect(test_program_dao)
    dut.do_select_all()

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


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class to test data controller update methods using actual database."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["revision"].name == "Test Revision"
        print("\033[36m\nsucceed_update_revision topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for revision ID "
            "1 was the wrong type."
        )
        print("\033[35m\nfail_update_revision topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should send the succeed_update_revision message on
        success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_revision")

        _revision = test_datamanager.do_select(1, table="revision")
        _revision.name = "Test Revision"
        test_datamanager.do_update(1, table="revision")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_revision")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update() should send the succeed_update_revision message on
        success."""
        _revision = test_datamanager.do_select(1, table="revision")
        _revision.name = "Test Revision"

        test_datamanager.do_update(1, table="revision")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_revision")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update() should send the succeed_update_revision message on
        success."""
        _revision = test_datamanager.do_select(1, table="revision")
        _revision.name = "Test Revision"

        pub.sendMessage("request_update_all_revisions")

        _revision = test_datamanager.do_select(1, table="revision")
        assert _revision.name == "Test Revision"

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should send the fail_update_revision message when passed
        a revision ID that that has a wrong data type for one or more
        attributes."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_revision")

        test_datamanager.tree.get_node(1).data["revision"].cost = None
        test_datamanager.do_update(1, table="revision")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_revision")

    @pytest.mark.integration
    def test_do_update_root_node(self, test_datamanager):
        """do_update() should end the fail_update_revision message when passed
        a revision ID that has no data package."""
        test_datamanager.do_update(0, table="revision")
