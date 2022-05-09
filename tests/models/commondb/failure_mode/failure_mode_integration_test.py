# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.failure_mode.failure_mode_integration_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Failure Mode module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKFailureModeRecord
from ramstk.models.dbtables import RAMSTKFailureModeTable
from tests import (
    SystemTestDeleteMethods,
    SystemTestGetterSetterMethods,
    SystemTestInsertMethods,
    SystemTestSelectMethods,
)


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestSelectFailureMode(SystemTestSelectMethods):
    """Class for testing Failure Mode table do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "request_select_failure_mode"
    _record = RAMSTKFailureModeRecord
    _tag = "failure_mode"


@pytest.mark.usefixtures("integration_test_table_model")
class TestUpdateFailureMode:
    """Class for testing Failure Mode table do_update() and do_update_all() methods."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKFailureModeRecord
    _tag = "failure_mode"
    _update_id = 1

    def on_succeed_update(self, tree):
        """Listen for succeed_update messages."""
        assert isinstance(tree, Tree)
        assert tree.get_node(3).data["failure_mode"].description == "New Failure Mode"
        assert tree.get_node(3).data["failure_mode"].mode_ratio == 0.5
        print("\033[36m\nsucceed_update_failure_mode topic was broadcast")

    def on_succeed_update_all(self):
        """Listen for succeed_update messages."""
        print(
            f"\033[36m\n\tsucceed_update_all topic was broadcast on update all "
            f"{self._tag}s"
        )

    def on_fail_update_wrong_data_type(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == (
            f"The value for one or more attributes for {self._tag} ID "
            f"{self._update_id} was the wrong type."
        )
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on wrong data "
            f"type."
        )

    def on_fail_update_root_node_wrong_data_type(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == "Attempting to update the root node 0."
        print(f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert (
            message == f"Attempted to save non-existent {self._tag} with {self._tag} "
            f"ID 100."
        )
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on non-existent "
            f"ID."
        )

    def on_fail_update_no_data_package(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == f"No data package found for {self._tag} ID {self._update_id}."
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on no data "
            f"package."
        )

    @pytest.mark.integration
    def test_do_update(self, integration_test_table_model):
        """Should update record attribute."""
        pub.subscribe(self.on_succeed_update, "succeed_update_failure_mode")

        integration_test_table_model.tree.get_node(3).data[
            "failure_mode"
        ].description = "New Failure Mode"
        integration_test_table_model.tree.get_node(3).data[
            "failure_mode"
        ].mode_ratio = 0.5
        integration_test_table_model.do_update(3)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_failure_mode")

        assert (
            integration_test_table_model.tree.get_node(3)
            .data["failure_mode"]
            .description
            == "New Failure Mode"
        )
        assert (
            integration_test_table_model.tree.get_node(3)
            .data["failure_mode"]
            .mode_ratio
            == 0.5
        )

        integration_test_table_model.tree.get_node(3).data[
            "failure_mode"
        ].description = "Short (pin-to-pin)"
        integration_test_table_model.tree.get_node(3).data[
            "failure_mode"
        ].mode_ratio = 0.8
        integration_test_table_model.do_update(3)

        assert (
            integration_test_table_model.tree.get_node(3)
            .data["failure_mode"]
            .description
            == "Short (pin-to-pin)"
        )
        assert (
            integration_test_table_model.tree.get_node(3)
            .data["failure_mode"]
            .mode_ratio
            == 0.8
        )

    @pytest.mark.integration
    def test_do_update_all(self, integration_test_table_model):
        """Should update all the records in the database."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all_mode")

        pub.sendMessage("request_update_all_failure_mode")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all_mode")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, integration_test_table_model):
        """Should send the do_log_debug message with wrong attribute data type."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_mode")

        integration_test_table_model.tree.get_node(3).data[
            "failure_mode"
        ].mode_ratio = "Hi ya"
        integration_test_table_model.do_update(3)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_mode")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, integration_test_table_model):
        """Should send the do_log_debug message when attempting to update root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_failure_mode"
        )

        integration_test_table_model.tree.get_node(3).data[
            "failure_mode"
        ].mode_ratio = "Hey bud"
        integration_test_table_model.do_update(0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_failure_mode"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, integration_test_table_model):
        """Should send the do_log_debug message with non-existent ID in tree."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_failure_mode")

        integration_test_table_model.do_select_all(
            {
                "category_id": 3,
                "subcategory_id": 24,
                "mode_id": 3,
            }
        )
        integration_test_table_model.do_update("skullduggery")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_failure_mode")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, integration_test_table_model):
        """Should send the do_log_debug message with no data package in tree."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_failure_mode")

        integration_test_table_model.tree.get_node(3).data.pop("failure_mode")
        integration_test_table_model.do_update(3)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_failure_mode")


@pytest.mark.usefixtures("integration_test_table_model")
class TestGetterSetterFailureMode(SystemTestGetterSetterMethods):
    """Class for testing Failure Mode table getter and setter methods."""

    __test__ = True

    _package = {"mode_ratio": 0.8}
    _record = RAMSTKFailureModeRecord
    _tag = "failure_mode"
    _test_id = 1
