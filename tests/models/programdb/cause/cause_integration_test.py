# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.cause.cause_integration_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing failure Cause integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKCauseRecord
from ramstk.models.dbtables import RAMSTKCauseTable
from tests import (
    SystemTestDeleteMethods,
    SystemTestGetterSetterMethods,
    SystemTestInsertMethods,
    SystemTestSelectMethods,
)


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestSelectCause(SystemTestSelectMethods):
    """Class for testing Cause table do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _record = RAMSTKCauseRecord
    _select_id = 3
    _tag = "cause"


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestInsertCause(SystemTestInsertMethods):
    """Class for testing Cause table do_insert() method."""

    __test__ = True

    _insert_id = 3
    _record = RAMSTKCauseRecord
    _tag = "cause"

    @pytest.mark.skip(reason="Cause records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, integration_test_table_model):
        """Should not run because Causes are not hierarchical."""
        pass

    @pytest.mark.skip(reason="Cause records are non-hierarchical.")
    def test_do_insert_no_parent(self, test_attributes, integration_test_table_model):
        """Should not run because Causes are not hierarchical."""
        pass


@pytest.mark.usefixtures("integration_test_table_model")
class TestDeleteCause(SystemTestDeleteMethods):
    """Class for testing Cause table do_delete() method."""

    __test__ = True

    _delete_id = 3
    _next_id = 0
    _record = RAMSTKCauseRecord
    _tag = "cause"

    @pytest.mark.skip(reason="Cause records are non-hierarchical.")
    def test_do_delete_with_child(self, integration_test_table_model):
        """Should not run because Causes are not hierarchical."""
        pass


@pytest.mark.usefixtures("integration_test_table_model")
class TestUpdateCause:
    """Class for testing Cause table do_update() and do_update_all() methods."""

    __test__ = True

    _record = RAMSTKCauseRecord
    _tag = "cause"
    _update_id = 3

    def on_succeed_update(self, tree):
        """Listen for succeed_update messages."""
        assert isinstance(tree, Tree)
        print(f"\033[36m\n\tsucceed_update_{self._tag} topic was broadcast.")

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
        """Should update record in database and records tree."""
        pub.subscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].description = "Test failure cause"
        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].rpn_detection = 4
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

    @pytest.mark.integration
    def test_do_update_all(self, integration_test_table_model):
        """Should update all records in database and records tree."""
        pub.subscribe(self.on_succeed_update_all, f"succeed_update_all_{self._tag}")

        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].description = "Test failure cause"
        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].rpn_detection = 2
        integration_test_table_model.tree.get_node(self._update_id + 1).data[
            self._tag
        ].description = "Big test failure cause"
        integration_test_table_model.tree.get_node(self._update_id + 1).data[
            self._tag
        ].rpn_detection = 7
        pub.sendMessage(f"request_update_all_{self._tag}")

        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .description
            == "Test failure cause"
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .rpn_detection
            == 2
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id + 1)
            .data[self._tag]
            .description
            == "Big test failure cause"
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id + 1)
            .data[self._tag]
            .rpn_detection
            == 7
        )

        pub.unsubscribe(self.on_succeed_update_all, f"succeed_update_all_{self._tag}")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, integration_test_table_model):
        """Should send fail message if attribute has wrong data type."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

        _cause = integration_test_table_model.do_select(self._update_id)
        _cause.rpn_detection = {1: 2}
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, integration_test_table_model):
        """Should send fail message when attempting to update root node."""
        pub.subscribe(self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg")

        _cause = integration_test_table_model.do_select(self._update_id)
        _cause.rpn_detection_new = {1: 2}
        pub.sendMessage(f"request_update_{self._tag}", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """Should send fail message when node ID does not exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

        pub.sendMessage(f"request_update_{self._tag}", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, integration_test_table_model):
        """Should send fail message when node ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")

        integration_test_table_model.tree.get_node(self._update_id).data.pop(self._tag)
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")


@pytest.mark.usefixtures("integration_test_table_model")
class TestGetterSetterCause(SystemTestGetterSetterMethods):
    """Class for testing Cause table getter and setter methods."""

    __test__ = True

    _package = {"rpn_detection": 4}
    _record = RAMSTKCauseRecord
    _tag = "cause"
    _test_id = 3


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestCauseAnalysisMethods:
    """Class for testing Cause analytical methods."""

    def on_succeed_calculate_rpn_cause(self, tree: Tree):
        """Listen for succeed_calculate messages."""
        assert isinstance(tree, Tree)
        assert tree.get_node(3).data["cause"].rpn == 192
        assert tree.get_node(3).data["cause"].rpn_new == 64
        print("\033[36m\nsucceed_calculate_cause_rpn topic was broadcast.")

    @pytest.mark.integration
    def test_do_calculate_cause_rpn(
        self, test_attributes, integration_test_table_model
    ):
        """Should calculate the cause RPN."""
        pub.subscribe(
            self.on_succeed_calculate_rpn_cause, "succeed_calculate_cause_rpn"
        )

        integration_test_table_model.do_select_all(test_attributes)

        integration_test_table_model.tree.get_node(3).data["cause"].rpn_occurrence = 8
        integration_test_table_model.tree.get_node(3).data["cause"].rpn_detection = 3
        integration_test_table_model.tree.get_node(3).data[
            "cause"
        ].rpn_occurrence_new = 4
        integration_test_table_model.tree.get_node(3).data[
            "cause"
        ].rpn_detection_new = 2

        pub.sendMessage("request_calculate_cause_rpn", severity=8)

        assert integration_test_table_model.tree.get_node(3).data["cause"].rpn == 192
        assert integration_test_table_model.tree.get_node(3).data["cause"].rpn_new == 64

        pub.unsubscribe(
            self.on_succeed_calculate_rpn_cause, "succeed_calculate_cause_rpn"
        )
