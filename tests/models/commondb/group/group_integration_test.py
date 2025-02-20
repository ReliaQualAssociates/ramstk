# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.group.group_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Group module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKGroupRecord
from tests import SystemTestGetterSetterMethods, SystemTestSelectMethods


@pytest.mark.usefixtures(
    "test_attributes",
    "integration_test_table_model",
    "test_suite_logger",
)
class TestSelectGroup(SystemTestSelectMethods):
    """Class for testing Group table do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "request_select_group"
    _record = RAMSTKGroupRecord
    _tag = "group"


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestUpdateGroup:
    """Class for testing Group table do_update() and do_update_all() methods."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKGroupRecord
    _tag = "group"
    _update_id = 1

    def on_succeed_update(self, tree):
        """Listen for succeed_update messages."""
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["group"].description == "New Group"
        assert tree.get_node(1).data["group"].group_type == "swinger"
        print("\033[36m\nsucceed_update_group topic was broadcast")

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
        pub.subscribe(self.on_succeed_update, "succeed_update_group")

        integration_test_table_model.tree.get_node(1).data[
            "group"
        ].description = "New Group"
        integration_test_table_model.tree.get_node(1).data[
            "group"
        ].group_type = "swinger"
        integration_test_table_model.do_update(1)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_group")

        assert (
            integration_test_table_model.tree.get_node(1).data["group"].description
            == "New Group"
        )
        assert (
            integration_test_table_model.tree.get_node(1).data["group"].group_type
            == "swinger"
        )

        integration_test_table_model.tree.get_node(1).data[
            "group"
        ].description = "Engineering, RMS"
        integration_test_table_model.tree.get_node(1).data["group"].group_type = "work"
        integration_test_table_model.do_update(1)

        assert (
            integration_test_table_model.tree.get_node(1).data["group"].description
            == "Engineering, RMS"
        )
        assert (
            integration_test_table_model.tree.get_node(1).data["group"].group_type
            == "work"
        )

    @pytest.mark.integration
    def test_do_update_all(self, integration_test_table_model):
        """Should update all the records in the database."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all_group")

        pub.sendMessage("request_update_all_group")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all_group")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, integration_test_table_model):
        """Should send the do_log_debug message with wrong attribute data type."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_group")

        integration_test_table_model.tree.get_node(1).data["group"].group_type = None
        integration_test_table_model.do_update(1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_group")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, integration_test_table_model):
        """Should send the do_log_debug message when attempting to update root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_group"
        )

        integration_test_table_model.tree.get_node(1).data["group"].group_type = None
        integration_test_table_model.do_update(0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_group"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, integration_test_table_model):
        """Should send the do_log_debug message with non-existent ID in tree."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_group")

        integration_test_table_model.do_select_all({"group_id": 1})
        integration_test_table_model.do_update("skullduggery")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_group")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, integration_test_table_model):
        """Should send the do_log_debug message with no data package in tree."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_group")

        integration_test_table_model.tree.get_node(1).data.pop("group")
        integration_test_table_model.do_update(1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_group")


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestGetterSetterGroup(SystemTestGetterSetterMethods):
    """Class for testing Group table getter and setter methods."""

    __test__ = True

    _package = {"group_type": "swinger"}
    _record = RAMSTKGroupRecord
    _tag = "group"
    _test_id = 1
