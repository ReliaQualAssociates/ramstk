# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.program_status.program_status_integration_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Program Status module integrations."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pandas as pd
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKProgramStatusRecord, RAMSTKProgramStatusTable


@pytest.fixture(scope="class")
def test_tablemodel(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKProgramStatusTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_program_status_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_program_status_attributes")
    pub.unsubscribe(dut.do_update, "request_update_program_status")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_program_status_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_program_status")
    pub.unsubscribe(dut.do_insert, "request_insert_program_status")
    pub.unsubscribe(dut.do_get_actual_status, "request_get_actual_status")
    pub.unsubscribe(dut._do_set_attributes, "succeed_calculate_all_validation_tasks")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data["program_status"], RAMSTKProgramStatusRecord
        )
        print("\033[36m\nsucceed_retrieve_program_status topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_tablemodel):
        """should clear nodes from an existing records tree and re-populate."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_program_statuss")

        test_tablemodel.do_select_all(attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_program_statuss")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 4
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(4).data["program_status"], RAMSTKProgramStatusRecord
        )
        assert tree.get_node(4).data["program_status"].status_id == 4
        assert tree.get_node(4).data["program_status"].date_status == date.today()
        print("\033[36m\nsucceed_insert_program_status topic was broadcast.")

    def on_fail_insert_duplicate_date(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  "
            "Database returned:\n\tKey (fld_date_status)=({}) already exists.".format(
                date.today()
            )
        )
        print(
            "\033[35m\nfail_insert_program_status topic was broadcast on duplicate "
            "date."
        )

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a record to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_program_status")

        pub.sendMessage("request_insert_program_status", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_program_status")

    @pytest.mark.integration
    def test_do_insert_duplicate_date(self, test_attributes, test_tablemodel):
        """should not add a record if date is being duplicated."""
        pub.subscribe(self.on_fail_insert_duplicate_date, "fail_insert_program_status")

        test_attributes["date_status"] = date.today()
        pub.sendMessage("request_insert_program_status", attributes=test_attributes)

        pub.unsubscribe(
            self.on_fail_insert_duplicate_date, "fail_insert_program_status"
        )


@pytest.mark.usefixtures("test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_program_status topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "Attempted to delete non-existent Program Status ID 300."
        )
        print(
            "\033[35m\nfail_delete_program_status topic was broadcast on "
            "non-existent ID."
        )

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            "Attempted to delete non-existent Program Status ID 1."
        )
        print(
            "\033[35m\nfail_delete_program_status topic was broadcast on no data "
            "package."
        )

    @pytest.mark.integration
    def test_do_delete(self, test_tablemodel):
        """should remove record from record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_program_status")

        assert test_tablemodel.last_id == 3

        pub.sendMessage(
            "request_delete_program_status", node_id=test_tablemodel.last_id
        )

        assert test_tablemodel.last_id == 2

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_program_status")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self, test_tablemodel):
        """should send the fail message when passed a non-existent record ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_program_status")

        pub.sendMessage("request_delete_program_status", node_id=300)

        pub.unsubscribe(
            self.on_fail_delete_non_existent_id, "fail_delete_program_status"
        )

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_tablemodel):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_program_status")

        test_tablemodel.tree.get_node(1).data.pop("program_status")
        pub.sendMessage("request_delete_program_status", node_id=1)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_program_status")


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["program_status"].cost_remaining == 47832.00
        assert tree.get_node(1).data["program_status"].time_remaining == 528.3
        print("\033[36m\nsucceed_update_program_status topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for program "
            "status ID 1 was the wrong type."
        )
        print(
            "\033[35m\nfail_update_program_status topic was broadcast on wrong data "
            "type."
        )

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_program_status topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent program status with "
            "program status ID 100."
        )
        print(
            "\033[35m\nfail_update_program_status topic was broadcast on "
            "non-existent ID."
        )

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for program status ID 1."
        )
        print(
            "\033[35m\nfail_update_program_status topic was broadcast on no data "
            "package."
        )

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, "succeed_update_program_status")

        test_tablemodel.tree.get_node(1).data[
            "program_status"
        ].cost_remaining = 47832.00
        test_tablemodel.tree.get_node(1).data["program_status"].time_remaining = 528.3

        pub.sendMessage(
            "request_update_program_status", node_id=1, table="program_status"
        )

        pub.unsubscribe(self.on_succeed_update, "succeed_update_program_status")

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        pub.sendMessage("request_update_all_program_ststus")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_program_status")

        _status = test_tablemodel.do_select(1)
        _status.time_remaining = {1: 2}

        pub.sendMessage(
            "request_update_program_status", node_id=1, table="program_status"
        )

        pub.unsubscribe(
            self.on_fail_update_wrong_data_type, "fail_update_program_status"
        )

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """should send the fail message when attempting to update the root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_program_status"
        )

        _status = test_tablemodel.do_select(1)
        _status.time_remaining = {1: 2}

        pub.sendMessage(
            "request_update_program_status", node_id=0, table="program_status"
        )

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_program_status"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_tablemodel):
        """should send the fail message when updating a non-existent record ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_program_status")

        test_tablemodel.do_update(100, table="program_status")

        pub.unsubscribe(
            self.on_fail_update_non_existent_id, "fail_update_program_status"
        )

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_program_status")

        test_tablemodel.tree.get_node(1).data.pop("program_status")
        test_tablemodel.do_update(1, table="program_status")

        pub.unsubscribe(
            self.on_fail_update_no_data_package, "fail_update_program_status"
        )


@pytest.mark.usefixtures("test_tablemodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["status_id"] == 1
        assert attributes["cost_remaining"] == 0.0
        assert attributes["date_status"] == date.today() - timedelta(days=30)
        assert attributes["time_remaining"] == 0.0
        print("\033[36m\nsucceed_get_program_status_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data["program_status"], RAMSTKProgramStatusRecord
        )
        print("\033[36m\nsucceed_get_program_status_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["program_status"].cost_remaining == 0.0
        print("\033[36m\nsucceed_get_program_status_tree topic was broadcast")

    def on_succeed_get_actual_status(self, status):
        assert isinstance(status, pd.DataFrame)
        assert status.loc[pd.to_datetime(date.today()), "cost"] == 14608.45
        assert status.loc[pd.to_datetime(date.today()), "time"] == 469.0
        print("\033[36m\nsucceed_get_actual_status topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_tablemodel):
        """should return the attributes dict."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_program_status_attributes"
        )

        pub.sendMessage(
            "request_get_program_status_attributes", node_id=1, table="program_status"
        )

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_program_status_attributes"
        )

    @pytest.mark.integration
    def test_on_get_data_manager_tree(self, test_tablemodel):
        """should return the records tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_program_status_tree"
        )

        pub.sendMessage("request_get_program_status_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_program_status_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_tablemodel):
        """should set the value of the attribute requested."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_program_status_tree")

        pub.sendMessage(
            "request_set_opstress_attributes",
            node_id=[1, ""],
            package={"description": "Big test operating load."},
        )

        pub.unsubscribe(
            self.on_succeed_set_attributes, "succeed_get_program_status_tree"
        )

    @pytest.mark.integration
    def test_do_get_actual_status(self, test_attributes, test_tablemodel):
        """should update and return program status."""
        pub.subscribe(self.on_succeed_get_actual_status, "succeed_get_actual_status")

        test_tablemodel._do_set_attributes(
            cost_remaining=14608.45, time_remaining=469.00
        )

        _node_id = test_tablemodel._dic_status[date.today()]

        pub.sendMessage("request_get_actual_status")

        assert (
            test_tablemodel.tree.get_node(_node_id)
            .data["program_status"]
            .cost_remaining
            == 14608.45
        )
        assert (
            test_tablemodel.tree.get_node(_node_id)
            .data["program_status"]
            .time_remaining
            == 469.00
        )

        pub.unsubscribe(self.on_succeed_get_actual_status, "succeed_get_actual_status")
