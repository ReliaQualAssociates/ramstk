# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.program_info.program_info_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Program Information integrations."""


# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKProgramInfoRecord
from tests import SystemTestGetterSetterMethods, SystemTestSelectMethods


@pytest.mark.usefixtures(
    "test_attributes",
    "integration_test_table_model",
    "test_suite_logger",
)
class TestSelectProgramInfo(SystemTestSelectMethods):
    """Class for testing ProgramInfo table do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _record = RAMSTKProgramInfoRecord
    _select_id = 1
    _tag = "preference"


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestUpdateProgramInfo:
    """Class for testing ProgramInfo table do_update() and do_update_all() methods."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKProgramInfoRecord
    _tag = "preference"
    _update_id = 1

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

    def on_fail_update_root_node(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == "Attempting to update the root node 0."
        print(f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert (
            message == f"Attempted to save non-existent "
            f"{self._tag.replace('_', ' ')} with"
            f" {self._tag.replace('_', ' ')} "
            f"ID 100."
        )
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on non-existent "
            f"ID."
        )

    def on_fail_update_no_data_package(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert (
            message == f"No data package found for {self._tag.replace('_', ' ')} ID "
            f"{self._update_id}."
        )
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on no data "
            f"package."
        )

    @pytest.mark.integration
    def test_do_update(self, integration_test_table_model):
        """Should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].hardware_active = 0
        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].vandv_active = 0

        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .hardware_active
            == 0
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .vandv_active
            == 0
        )

        pub.unsubscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].hardware_active = 1
        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].vandv_active = 1

        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .hardware_active
            == 1
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .vandv_active
            == 1
        )

    @pytest.mark.integration
    def test_do_update_all(self, integration_test_table_model):
        """Should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, f"succeed_update_all_{self._tag}")

        pub.sendMessage(f"request_update_all_{self._tag}")

        pub.unsubscribe(self.on_succeed_update_all, f"succeed_update_all_{self._tag}")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, integration_test_table_model):
        """Should send the fail message when the wrong data type is assigned."""
        pub.subscribe(
            self.on_fail_update_wrong_data_type,
            "do_log_debug_msg",
        )

        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].hardware_active = {0: 1}
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(
            self.on_fail_update_wrong_data_type,
            "do_log_debug_msg",
        )

    @pytest.mark.integration
    def test_do_update_root_node(self, integration_test_table_model):
        """Should send the fail message when attempting to update the root node."""
        pub.subscribe(
            self.on_fail_update_root_node,
            "do_log_debug_msg",
        )

        pub.sendMessage(f"request_update_{self._tag}", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node,
            "do_log_debug_msg",
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, integration_test_table_model):
        """Should send the fail message when updating a non-existent record ID."""
        pub.subscribe(
            self.on_fail_update_non_existent_id,
            "do_log_debug_msg",
        )

        pub.sendMessage(f"request_update_{self._tag}", node_id=100)

        pub.unsubscribe(
            self.on_fail_update_non_existent_id,
            "do_log_debug_msg",
        )

    @pytest.mark.integration
    def test_do_update_no_data_package(self, integration_test_table_model):
        """Should send the fail message when the record ID has no data package."""
        pub.subscribe(
            self.on_fail_update_no_data_package,
            "do_log_debug_msg",
        )

        integration_test_table_model.tree.get_node(self._update_id).data.pop(self._tag)
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(
            self.on_fail_update_no_data_package,
            "do_log_debug_msg",
        )


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestGetterSetterProgramInfo(SystemTestGetterSetterMethods):
    """Class for testing Program Information table getter and setter methods."""

    __test__ = True

    _package = {"function_active": 0}
    _record = RAMSTKProgramInfoRecord
    _tag = "preference"
    _test_id = 1
