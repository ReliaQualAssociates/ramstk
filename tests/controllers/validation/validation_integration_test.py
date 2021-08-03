# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.validation.validation_integration_test.py is part of
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
from ramstk.controllers import amValidation, dmProgramStatus, dmValidation
from ramstk.models.programdb import RAMSTKValidation


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "validation_id": 1,
        "name": "New Validation Task",
    }


@pytest.fixture(scope="class")
def test_analysismanager(test_toml_user_configuration):
    # Create the device under test (dut) and connect to the configuration.
    dut = amValidation(test_toml_user_configuration)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.on_get_all_attributes, "succeed_get_all_validation_attributes")
    pub.unsubscribe(dut.on_get_tree, "succeed_get_validation_tree")
    pub.unsubscribe(dut.do_calculate_plan, "request_calculate_plan")
    pub.unsubscribe(dut._do_calculate_all_tasks, "request_calculate_validation_tasks")
    pub.unsubscribe(dut._do_calculate_task, "request_calculate_validation_task")
    pub.unsubscribe(dut._do_request_status_tree, "succeed_retrieve_validations")
    pub.unsubscribe(dut._on_get_status_tree, "succeed_retrieve_program_status")
    pub.unsubscribe(dut._on_get_status_tree, "succeed_get_program_status_tree")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmValidation()
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

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_programstatus(test_program_dao):
    dut = dmProgramStatus()
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
    pub.unsubscribe(dut._do_set_attributes, "succeed_calculate_all_validation_tasks")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["validation"], RAMSTKValidation)
        print("\033[36m\nsucceed_retrieve_validations topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_datamanager):
        """do_select_all() should return a Tree() object populated with
        RAMSTKValidation instances on success."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_validations")

        test_datamanager.do_select_all(attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_validations")


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 4
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(4).data["validation"], RAMSTKValidation)
        assert tree.get_node(4).data["validation"].validation_id == 4
        assert tree.get_node(4).data["validation"].name == "New Validation Task"
        print("\033[36m\nsucceed_insert_validation topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  "
            "Database returned:\n\tKey (fld_revision_id)=(30) is not present "
            'in table "ramstk_revision".'
        )
        print("\033[35m\nfail_insert_validation topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes):
        """_do_insert_validation() should send the success message after
        successfully inserting a validation task."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_validation")

        pub.sendMessage("request_insert_validation", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_validation")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_attributes, test_datamanager):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent revision ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_validation")

        test_datamanager._fkey["revision_id"] = 30
        pub.sendMessage("request_insert_validation", attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_validation")


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_validation topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Validation ID 300.")
        print("\033[35m\nfail_delete_validation topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == ("Attempted to delete non-existent Validation ID 2.")
        print("\033[35m\nfail_delete_validation topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete_validation(self, test_datamanager):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_validation")

        pub.sendMessage("request_delete_validation", node_id=test_datamanager.last_id)

        assert test_datamanager.last_id == 2

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_validation")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """_do_delete() should send the fail message when attempting to delete
        a record that doesn't exist in the database."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_validation")

        pub.sendMessage("request_delete_validation", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_validation")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_validation")

        test_datamanager.tree.remove_node(2)
        pub.sendMessage("request_delete_validation", node_id=2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_validation")


@pytest.mark.usefixtures("test_datamanager")
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
        print("\033[35m\nfail_update_validation topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_validation topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent validation with "
            "validation ID 100."
        )
        print("\033[35m\nfail_update_validation topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for validation ID 1."
        )
        print("\033[35m\nfail_update_validation topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_validation")

        _validation = test_datamanager.do_select(1, "validation")
        _validation.name = "Test Validation"
        _validation.time_maximum = 10.5
        pub.sendMessage("request_update_validation", node_id=1, table="validation")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_validation")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """do_update_all() should update all the functions in the database."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        _validation = test_datamanager.do_select(1, table="validation")
        _validation.description = "Big test validation #1"
        _validation = test_datamanager.do_select(2, table="validation")
        _validation.description = "Big test validation #2"

        pub.sendMessage("request_update_all_validations")

        assert (
            test_datamanager.do_select(1, table="validation").description
            == "Big test validation #1"
        )
        assert (
            test_datamanager.do_select(2, table="validation").description
            == "Big test validation #2"
        )

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_validation")

        _validation = test_datamanager.do_select(1, table="validation")
        _validation.time_mean = {1: 2}
        pub.sendMessage("request_update_validation", node_id=1, table="validation")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_validation")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_validation"
        )

        _validation = test_datamanager.do_select(1, table="validation")
        _validation.time_mean = {1: 2}
        pub.sendMessage("request_update_validation", node_id=0, table="validation")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_validation"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """do_update() should raise the 'fail_update_validation' message when
        passed a Validation ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_validation")

        pub.sendMessage("request_update_validation", node_id=100, table="validation")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_validation")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update() should raise the 'fail_update_validation' message when
        passed a Validation ID that doesn't exist in the tree."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_validation")

        test_datamanager.tree.get_node(1).data.pop("validation")
        pub.sendMessage("request_update_validation", node_id=1, table="validation")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_validation")


@pytest.mark.usefixtures("test_toml_user_configuration")
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
        assert isinstance(tree.get_node(1).data["validation"], RAMSTKValidation)
        print("\033[36m\nsucceed_get_validation_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["validation"].task_specification == "MIL-HDBK-217F"
        print("\033[36m\nsucceed_get_validation_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self):
        """do_get_attributes() should return a dict of validation attributes on
        success."""
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
    def test_on_get_tree_analysis_manager(self, test_analysismanager, test_datamanager):
        """_do_request_tree() should send the tree request messages."""
        test_datamanager.do_get_tree()

        assert isinstance(test_analysismanager._tree, Tree)
        assert isinstance(
            test_analysismanager._tree.get_node(1).data["validation"], RAMSTKValidation
        )

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self):
        """on_get_tree() should return the validation treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_validations_tree"
        )

        pub.sendMessage("request_get_validation_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_validations_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self):
        """do_set_attributes() should send the success message."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_validations_tree")

        pub.sendMessage(
            "request_set_validation_attributes",
            node_id=[1],
            package={"task_specification": "MIL-HDBK-217F"},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_validations_tree")


@pytest.mark.usefixtures(
    "test_analysismanager", "test_datamanager", "test_programstatus"
)
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    def on_succeed_calculate_plan(self, attributes):
        assert attributes["plan"].loc[
            pd.to_datetime(date.today() - timedelta(days=10)), "lower"
        ] == pytest.approx(50.0004502)
        assert attributes["plan"].loc[
            pd.to_datetime(date.today() + timedelta(days=20)), "mean"
        ] == pytest.approx(55.666667)
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
            == 10.0
        )
        assert (
            attributes["assessed"].loc[
                pd.to_datetime(date.today() + timedelta(days=30)), "mean"
            ]
            == 20.0
        )
        assert (
            attributes["assessed"].loc[
                pd.to_datetime(date.today() + timedelta(days=30)), "upper"
            ]
            == 30.0
        )
        print("\033[36m\nsucceed_calculate_verification_plan topic was broadcast")

    @pytest.mark.integration
    def test_do_select_actual_status(self, test_analysismanager):
        """should return a pandas DataFrame() containing actual plan status."""
        pub.sendMessage("request_get_validation_tree")
        pub.sendMessage(
            "succeed_calculate_all_validation_tasks",
            cost_remaining=212.32,
            time_remaining=112.5,
        )
        pub.sendMessage("request_get_program_status_tree")

        _actuals = test_analysismanager._do_select_actual_status()

        assert isinstance(_actuals, pd.DataFrame)
        assert _actuals.loc[pd.to_datetime(date.today()), "cost"] == 212.32
        assert _actuals.loc[pd.to_datetime(date.today()), "time"] == 112.5

    @pytest.mark.skip
    def test_do_calculate_verification_plan(
        self, test_analysismanager, test_datamanager
    ):
        """do_calculate_plan() should calculate the planned validation effort
        time and cost."""
        pub.subscribe(
            self.on_succeed_calculate_plan, "succeed_calculate_verification_plan"
        )

        test_datamanager.do_get_tree()
        _validation = test_datamanager.do_select(1, "validation")
        _validation.time_minimum = 10.0
        _validation.time_average = 20.0
        _validation.time_maximum = 40.0
        _validation.time_mean = 0.0
        _validation.cost_minimum = 1850.0
        _validation.cost_average = 2200.0
        _validation.cost_maximum = 4500.0
        _validation.confidence = 95.0
        test_datamanager.do_update(1, table="validation")
        _validation = test_datamanager.do_select(2, "validation")
        _validation.time_minimum = 15.0
        _validation.time_average = 32.0
        _validation.time_maximum = 60.0
        _validation.time_mean = 0.0
        _validation.cost_minimum = 750.0
        _validation.cost_average = 1200.0
        _validation.cost_maximum = 2500.0
        _validation.confidence = 95.0
        test_datamanager.do_update(2, table="validation")

        test_analysismanager.do_calculate_plan()

        pub.unsubscribe(
            self.on_succeed_calculate_plan, "succeed_calculate_verification_plan"
        )
