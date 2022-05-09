# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.action.action_integration_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing FMEA Action integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKActionRecord
from ramstk.models.dbtables import RAMSTKActionTable
from tests import (
    SystemTestDeleteMethods,
    SystemTestGetterSetterMethods,
    SystemTestInsertMethods,
    SystemTestSelectMethods,
)


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestSelectAction(SystemTestSelectMethods):
    """Class for testing Action table do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _record = RAMSTKActionRecord
    _select_id = 3
    _tag = "action"


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestInsertAction(SystemTestInsertMethods):
    """Class for testing Action table do_insert() method."""

    __test__ = True

    _insert_id = 3
    _record = RAMSTKActionRecord
    _tag = "action"

    @pytest.mark.skip(reason="Action records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, integration_test_table_model):
        """Should not run because Actions are not hierarchical."""
        pass

    @pytest.mark.skip(reason="Action records are non-hierarchical.")
    def test_do_insert_no_parent(self, test_attributes, integration_test_table_model):
        """Should not run because Actions are not hierarchical."""
        pass


@pytest.mark.usefixtures("integration_test_table_model")
class TestDeleteAction(SystemTestDeleteMethods):
    """Class for testing Action table do_delete() method."""

    __test__ = True

    _delete_id = 3
    _next_id = 0
    _record = RAMSTKActionRecord
    _tag = "action"

    @pytest.mark.skip(reason="Action records are non-hierarchical.")
    def test_do_delete_with_child(self, integration_test_table_model):
        """Should not run because Actions are not hierarchical."""
        pass


@pytest.mark.usefixtures("integration_test_table_model")
class TestUpdateAction:
    """Class for testing Action table do_update() and do_update_all() methods."""

    __test__ = True

    _record = RAMSTKActionRecord
    _tag = "action"
    _update_id = 2

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
        """Should update record attribute."""
        pub.subscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].description = "Get a clue."
        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].action_closed = 1
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .description
            == "Get a clue."
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .action_closed
            == 1
        )

        pub.unsubscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

    @pytest.mark.integration
    def test_do_update_all(self, integration_test_table_model):
        """Should update all the records in the database."""
        pub.subscribe(self.on_succeed_update_all, f"succeed_update_all_{self._tag}")

        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].description = "Test failure action"
        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].rpn_detection = 2
        integration_test_table_model.tree.get_node(self._update_id + 1).data[
            self._tag
        ].description = "Big test failure action"
        integration_test_table_model.tree.get_node(self._update_id + 1).data[
            self._tag
        ].rpn_detection = 7
        pub.sendMessage(f"request_update_all_{self._tag}")

        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .description
            == "Test failure action"
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
            == "Big test failure action"
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
        """Should send the do_log_debug message with wrong attribute data type."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

        _action = integration_test_table_model.do_select(self._update_id)
        _action.action_approved = {1: 2}
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, integration_test_table_model):
        """Should send the do_log_debug message when attempting to update root node."""
        pub.subscribe(self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg")

        _action = integration_test_table_model.do_select(self._update_id + 1)
        _action.action_closed = {1: 2}
        pub.sendMessage(f"request_update_{self._tag}", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """Should send the do_log_debug message with non-existent ID in tree."""
        pub.subscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

        pub.sendMessage(f"request_update_{self._tag}", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, integration_test_table_model):
        """Should send the do_log_debug message with no data package in tree."""
        pub.subscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")

        integration_test_table_model.tree.get_node(self._update_id).data.pop(self._tag)
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")


@pytest.mark.usefixtures("integration_test_table_model")
class TestGetterSetterAction(SystemTestGetterSetterMethods):
    """Class for testing Action table getter and setter methods."""

    __test__ = True

    _package = {"action_owner": "John Jacob Jingleheimer Schmidt"}
    _record = RAMSTKActionRecord
    _tag = "action"
    _test_id = 1
