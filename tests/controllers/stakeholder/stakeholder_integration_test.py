# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.stakeholder.stakeholder_integration_test.py is part
#       of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Stakeholder module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import amStakeholder, dmStakeholder
from ramstk.models.programdb import RAMSTKStakeholder


@pytest.fixture(scope="class")
def test_analysismanager(test_toml_user_configuration):
    # Create the device under test (dut) and connect to the configuration.
    dut = amStakeholder(test_toml_user_configuration)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.on_get_all_attributes, "succeed_get_stakeholder_attributes")
    pub.unsubscribe(dut.on_get_tree, "succeed_get_stakeholder_tree")
    pub.unsubscribe(dut.do_calculate_stakeholder, "request_calculate_stakeholder")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmStakeholder()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_stakeholder_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_stakeholder_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_stakeholder")
    pub.unsubscribe(dut.do_update, "request_update_stakeholders")
    pub.unsubscribe(dut.do_get_tree, "request_get_stakeholder_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut._do_delete, "request_delete_stakeholder")
    pub.unsubscribe(dut._do_insert_stakeholder, "request_insert_stakeholder")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting "
            "to add a record.  Database returned:\n\tKey "
            "(fld_revision_id)=(40) is not present in "
            'table "ramstk_revision".'
        )
        print("\033[35m\nfail_insert_stakeholder topic was broadcast")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_datamanager):
        """_do_insert_stakeholder() should send the success message after
        successfully inserting a new top-level stakeholder."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_stakeholder")

        test_datamanager._revision_id = 40
        test_datamanager._do_insert_stakeholder()

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_stakeholder")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["stakeholder"].description == ("Test Stakeholder")
        print("\033[36m\nsucceed_update_stakeholder topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for stakeholder "
            "input ID 1 was the wrong type."
        )
        print("\033[35m\nfail_update_stakeholder topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should broadcast the succeed update message on
        success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_stakeholders")

        _stakeholder = test_datamanager.do_select(1, table="stakeholder")
        _stakeholder.description = "Test Stakeholder"
        test_datamanager.do_update(1, table="stakeholder")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_stakeholders")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update_all() should update all the functions in the database."""
        _stakeholder = test_datamanager.do_select(1, table="stakeholder")
        _stakeholder.description = "Big test stakeholder #1"
        _stakeholder = test_datamanager.do_select(2, table="stakeholder")
        _stakeholder.description = "Big test stakeholder #2"

        test_datamanager.do_update_all()

        assert (
            test_datamanager.do_select(1, table="stakeholder").description
            == "Big test stakeholder #1"
        )
        assert (
            test_datamanager.do_select(2, table="stakeholder").description
            == "Big test stakeholder #2"
        )

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should broadcast the fail update message when one or
        more attribute values is the wrong data type."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_stakeholders")

        _stakeholder = test_datamanager.do_select(1, table="stakeholder")
        _stakeholder.user_float_1 = {1: 2}

        test_datamanager.do_update(1, table="stakeholder")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_stakeholders")

    @pytest.mark.integration
    def test_do_update_root_node(self, test_datamanager):
        """do_update() should broadcast the fail update message when one or
        more attribute values is the wrong data type and it is attempting to
        update the root node."""
        _stakeholder = test_datamanager.do_select(1, table="stakeholder")
        _stakeholder.user_float_1 = {1: 2}

        test_datamanager.do_update(0, table="stakeholder")
