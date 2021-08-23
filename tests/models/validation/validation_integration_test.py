# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.validation.validation_integration_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Validation module integrations."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pandas as pd
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKValidationRecord, RAMSTKValidationTable


@pytest.fixture(scope="class")
def test_tablemodel(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKValidationTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_validation_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_validation_attributes")
    pub.unsubscribe(dut.do_set_attributes, "mvw_editing_validation")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_validation")
    pub.unsubscribe(dut.do_update, "request_update_validation")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_get_tree, "request_get_validation_tree")
    pub.unsubscribe(dut.do_delete, "request_delete_validation")
    pub.unsubscribe(dut.do_insert, "request_insert_validation")
    pub.unsubscribe(dut.do_calculate_plan, "request_calculate_plan")
    pub.unsubscribe(dut._do_calculate_task, "request_calculate_validation_task")
    pub.unsubscribe(dut._do_calculate_all_tasks, "request_calculate_validation_tasks")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["validation"], RAMSTKValidationRecord)
        print("\033[36m\nsucceed_retrieve_validations topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_tablemodel):
        """should clear nodes from an existing records tree and re-populate."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_validations")

        test_tablemodel.do_select_all(attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_validations")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 4
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(4).data["validation"], RAMSTKValidationRecord)
        assert tree.get_node(4).data["validation"].validation_id == 4
        assert tree.get_node(4).data["validation"].name == "New Validation Task"
        print("\033[36m\nsucceed_insert_validation topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  "
            "Database returned:\n\tKey (fld_revision_id)=(30) is not present "
            'in table "ramstk_revision".'
        )
        print("\033[35m\nfail_insert_validation topic was broadcast on no revision.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes):
        """should add a record to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_validation")

        pub.sendMessage("request_insert_validation", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_validation")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_attributes, test_tablemodel):
        """should not add a record when passed a non-existent revision ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_validation")

        test_attributes["revision_id"] = 30
        pub.sendMessage("request_insert_validation", attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_validation")


@pytest.mark.usefixtures("test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_validation topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Validation ID 300.")
        print(
            "\033[35m\nfail_delete_validation topic was broadcast on non-existent ID."
        )

    def on_fail_delete_no_data_package(self, error_message):
        assert error_message == ("Attempted to delete non-existent Validation ID 2.")
        print(
            "\033[35m\nfail_delete_validation topic was broadcast on no data package."
        )

    @pytest.mark.integration
    def test_do_delete_validation(self, test_tablemodel):
        """should remove record from record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_validation")

        pub.sendMessage("request_delete_validation", node_id=test_tablemodel.last_id)

        assert test_tablemodel.last_id == 2

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_validation")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """should send the fail message when passed a non-existent record ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_validation")

        pub.sendMessage("request_delete_validation", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_validation")

    @pytest.mark.integration
    def test_do_delete_no_data_package(self, test_tablemodel):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_delete_no_data_package, "fail_delete_validation")

        test_tablemodel.tree.get_node(2).data.pop("validation")
        pub.sendMessage("request_delete_validation", node_id=2)

        pub.unsubscribe(self.on_fail_delete_no_data_package, "fail_delete_validation")


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["validation"].name == "Test Validation"
        assert tree.get_node(1).data["validation"].time_maximum == 10.5
        print("\033[36m\nsucceed_update_validation topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for validation "
            "ID 1 was the wrong type."
        )
        print(
            "\033[35m\nfail_update_validation topic was broadcast on wrong data "
            "type."
        )

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_validation topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent validation with "
            "validation ID 100."
        )
        print(
            "\033[35m\nfail_update_validation topic was broadcast on non-existent ID."
        )

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for validation ID 1."
        )
        print(
            "\033[35m\nfail_update_validation topic was broadcast on no data package."
        )

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, "succeed_update_validation")

        _validation = test_tablemodel.do_select(1)
        _validation.name = "Test Validation"
        _validation.time_maximum = 10.5
        pub.sendMessage("request_update_validation", node_id=1, table="validation")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_validation")

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        _validation = test_tablemodel.do_select(1)
        _validation.description = "Big test validation #1"
        _validation = test_tablemodel.do_select(2)
        _validation.description = "Big test validation #2"

        pub.sendMessage("request_update_all_validations")

        assert test_tablemodel.do_select(1).description == "Big test validation #1"
        assert test_tablemodel.do_select(2).description == "Big test validation #2"

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_validation")

        _validation = test_tablemodel.do_select(1)
        _validation.time_mean = {1: 2}
        pub.sendMessage("request_update_validation", node_id=1, table="validation")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_validation")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """should send the fail message when attempting to update the root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_validation"
        )

        _validation = test_tablemodel.do_select(1)
        _validation.time_mean = {1: 2}
        pub.sendMessage("request_update_validation", node_id=0, table="validation")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_validation"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """should send the fail message when updating a non-existent record ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_validation")

        pub.sendMessage("request_update_validation", node_id=100, table="validation")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_validation")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_validation")

        test_tablemodel.tree.get_node(1).data.pop("validation")
        pub.sendMessage("request_update_validation", node_id=1, table="validation")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_validation")


@pytest.mark.usefixtures("test_tablemodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["validation_id"] == 1
        assert attributes["name"] == "PRF-0001"
        assert attributes["time_average"] == 0.0
        print("\033[36m\nsucceed_get_validation_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["validation"], RAMSTKValidationRecord)
        print("\033[36m\nsucceed_get_validation_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["validation"].task_specification == "MIL-HDBK-217F"
        print("\033[36m\nsucceed_get_validation_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self):
        """should return the attributes dict."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_validation_attributes"
        )

        pub.sendMessage(
            "request_get_validation_attributes", node_id=1, table="validation"
        )

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_validation_attributes"
        )

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self):
        """should return the records tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_validations_tree"
        )

        pub.sendMessage("request_get_validation_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_validations_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self):
        """should set the value of the attribute requested."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_validations_tree")

        pub.sendMessage(
            "request_set_validation_attributes",
            node_id=[1],
            package={"task_specification": "MIL-HDBK-217F"},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_validations_tree")


@pytest.mark.usefixtures("test_tablemodel")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    def on_succeed_calculate_all_tasks(self, cost_remaining, time_remaining):
        assert cost_remaining == 3400.0
        assert time_remaining == 80.0
        print("\033[36m\nsucceed_calculate_all_tasks topic was broadcast.")

    def on_succeed_calculate_plan(self, attributes):
        assert attributes["plan"].loc[
            pd.to_datetime(date.today() - timedelta(days=10)), "lower"
        ] == pytest.approx(31.0004501932)
        assert attributes["plan"].loc[
            pd.to_datetime(date.today() + timedelta(days=20)), "mean"
        ] == pytest.approx(21.6666667)
        assert (
            attributes["plan"].loc[
                pd.to_datetime(date.today() + timedelta(days=30)), "upper"
            ]
            == 0.0
        )
        assert (
            attributes["assessed"].loc[
                pd.to_datetime(date.today() + timedelta(days=30)), "lower"
            ]
            == 55.0
        )
        assert (
            attributes["assessed"].loc[
                pd.to_datetime(date.today() + timedelta(days=30)), "mean"
            ]
            == 70.0
        )
        assert (
            attributes["assessed"].loc[
                pd.to_datetime(date.today() + timedelta(days=30)), "upper"
            ]
            == 100.0
        )
        print("\033[36m\nsucceed_calculate_verification_plan topic was broadcast")

    @pytest.mark.integration
    def test_do_calculate_all_tasks(self, test_tablemodel):
        """should calculate all the validation tasks time and cost."""
        pub.subscribe(
            self.on_succeed_calculate_all_tasks,
            "succeed_calculate_all_validation_tasks",
        )

        _validation = test_tablemodel.do_select(1)
        _validation.time_minimum = 10.0
        _validation.time_average = 20.0
        _validation.time_maximum = 40.0
        _validation.cost_minimum = 1850.0
        _validation.cost_average = 2200.0
        _validation.cost_maximum = 4500.0
        _validation.confidence = 95.0
        _validation = test_tablemodel.do_select(2)
        _validation.time_minimum = 30.0
        _validation.time_average = 60.0
        _validation.time_maximum = 80.0
        _validation.cost_minimum = 850.0
        _validation.cost_average = 1200.0
        _validation.cost_maximum = 3500.0
        _validation.confidence = 95.0

        pub.sendMessage("request_calculate_validation_tasks")

        assert test_tablemodel.tree.get_node(1).data[
            "validation"
        ].time_ll == pytest.approx(11.86684674)
        assert test_tablemodel.tree.get_node(1).data[
            "validation"
        ].time_mean == pytest.approx(21.66666667)
        assert test_tablemodel.tree.get_node(1).data[
            "validation"
        ].time_ul == pytest.approx(31.46648659)
        assert test_tablemodel.tree.get_node(1).data["validation"].time_variance == 25.0
        assert test_tablemodel.tree.get_node(1).data[
            "validation"
        ].cost_ll == pytest.approx(1659.34924016)
        assert test_tablemodel.tree.get_node(1).data[
            "validation"
        ].cost_mean == pytest.approx(2525.0)
        assert test_tablemodel.tree.get_node(1).data[
            "validation"
        ].cost_ul == pytest.approx(3390.65075984)
        assert test_tablemodel.tree.get_node(1).data[
            "validation"
        ].cost_variance == pytest.approx(195069.44444444)
        assert test_tablemodel.tree.get_node(2).data[
            "validation"
        ].time_ll == pytest.approx(42.00030013)
        assert test_tablemodel.tree.get_node(2).data[
            "validation"
        ].time_mean == pytest.approx(58.33333333)
        assert test_tablemodel.tree.get_node(2).data[
            "validation"
        ].time_ul == pytest.approx(74.66636654)
        assert test_tablemodel.tree.get_node(2).data[
            "validation"
        ].time_variance == pytest.approx(69.44444444)
        assert test_tablemodel.tree.get_node(2).data[
            "validation"
        ].cost_ll == pytest.approx(659.34924016)
        assert test_tablemodel.tree.get_node(2).data[
            "validation"
        ].cost_mean == pytest.approx(1525.0)
        assert test_tablemodel.tree.get_node(2).data[
            "validation"
        ].cost_ul == pytest.approx(2390.65075984)
        assert test_tablemodel.tree.get_node(2).data[
            "validation"
        ].cost_variance == pytest.approx(195069.44444444)

        pub.unsubscribe(
            self.on_succeed_calculate_all_tasks,
            "succeed_calculate_all_validation_tasks",
        )

    @pytest.mark.integration
    def test_do_calculate_verification_plan(self, test_tablemodel):
        """should calculate the planned validation effort time and cost."""
        pub.subscribe(
            self.on_succeed_calculate_plan, "succeed_calculate_verification_plan"
        )

        _validation = test_tablemodel.do_select(1)
        _validation.acceptable_minimum = 55.0
        _validation.acceptable_mean = 70.0
        _validation.acceptable_maximum = 100.0
        _validation.time_minimum = 10.0
        _validation.time_average = 20.0
        _validation.time_maximum = 40.0
        _validation.time_mean = 0.0
        _validation.cost_minimum = 1850.0
        _validation.cost_average = 2200.0
        _validation.cost_maximum = 4500.0
        _validation.confidence = 95.0
        _validation.status = 0.5
        _validation.task_type = 5
        _validation = test_tablemodel.do_select(2)
        _validation.acceptable_minimum = 125.0
        _validation.acceptable_mean = 160.0
        _validation.acceptable_maximum = 190.0
        _validation.time_minimum = 15.0
        _validation.time_average = 32.0
        _validation.time_maximum = 60.0
        _validation.time_mean = 0.0
        _validation.cost_minimum = 750.0
        _validation.cost_average = 1200.0
        _validation.cost_maximum = 2500.0
        _validation.confidence = 95.0
        _validation.status = 0.2

        pub.sendMessage("request_calculate_plan")

        pub.unsubscribe(
            self.on_succeed_calculate_plan, "succeed_calculate_verification_plan"
        )

    @pytest.mark.integration
    def test_do_calculate_verification_plan_with_mean_time(self, test_tablemodel):
        """should calculate the planned validation effort time and cost."""
        _validation = test_tablemodel.do_select(1)
        _validation.acceptable_minimum = 55.0
        _validation.acceptable_mean = 70.0
        _validation.acceptable_maximum = 100.0
        _validation.time_minimum = 10.0
        _validation.time_average = 20.0
        _validation.time_maximum = 40.0
        _validation.time_mean = 10.0
        _validation.cost_minimum = 1850.0
        _validation.cost_average = 2200.0
        _validation.cost_maximum = 4500.0
        _validation.confidence = 95.0
        _validation.status = 0.5
        _validation.task_type = 5
        _validation = test_tablemodel.do_select(2)
        _validation.acceptable_minimum = 125.0
        _validation.acceptable_mean = 160.0
        _validation.acceptable_maximum = 190.0
        _validation.time_minimum = 15.0
        _validation.time_average = 32.0
        _validation.time_maximum = 60.0
        _validation.time_mean = 0.0
        _validation.cost_minimum = 750.0
        _validation.cost_average = 1200.0
        _validation.cost_maximum = 2500.0
        _validation.confidence = 95.0
        _validation.status = 0.2

        pub.sendMessage("request_calculate_plan")
