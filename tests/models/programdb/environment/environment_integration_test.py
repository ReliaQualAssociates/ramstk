# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.environment.environment_integration_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Environment module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKEnvironmentRecord
from tests import (
    SystemTestDeleteMethods,
    SystemTestGetterSetterMethods,
    SystemTestInsertMethods,
    SystemTestSelectMethods,
)


@pytest.mark.usefixtures(
    "test_attributes",
    "integration_test_table_model",
    "test_suite_logger",
)
class TestSelectEnvironment(SystemTestSelectMethods):
    """Class for testing Environment do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _record = RAMSTKEnvironmentRecord
    _select_id = 1
    _tag = "environment"


@pytest.mark.usefixtures(
    "test_attributes",
    "integration_test_table_model",
    "test_suite_logger",
)
class TestInsertEnvironment(SystemTestInsertMethods):
    """Class for testing Environment table do_insert() method."""

    __test__ = True

    _insert_id = 1
    _record = RAMSTKEnvironmentRecord
    _tag = "environment"

    @pytest.mark.skip(reason="Environment records are non-hierarchical.")
    def test_do_insert_sibling(self, test_attributes, integration_test_table_model):
        """Should not run because Environment is not hierarchical."""
        pass

    @pytest.mark.skip(reason="Environment records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, integration_test_table_model):
        """Should not run because Environment is not hierarchical."""
        pass

    @pytest.mark.skip(reason="Environment records are non-hierarchical.")
    def test_do_insert_no_parent(self, test_attributes, integration_test_table_model):
        """Should not run because Environment is not hierarchical."""
        pass

    @pytest.mark.skip(reason="Environment records are added by database.")
    def test_do_insert_no_revision(self, test_attributes, integration_test_table_model):
        """Should not run because Environment are added by database."""
        pass


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestDeleteEnvironment(SystemTestDeleteMethods):
    """Class for testing Environment table do_delete() method."""

    __test__ = True

    _delete_id = 1
    _record = RAMSTKEnvironmentRecord
    _tag = "environment"

    @pytest.mark.skip(reason="Environment records are deleted by database.")
    def test_do_delete(self, integration_test_table_model):
        """Should not run because Environment are deleted by database."""
        pass

    @pytest.mark.skip(reason="Environment records are deleted by database.")
    def test_do_delete_with_child(self, integration_test_table_model):
        """Should not run because Environment are deleted by database."""
        pass

    @pytest.mark.skip(reason="Environment records are deleted by database.")
    def test_do_delete_non_existent_id(self):
        """Should not run because Environment are deleted by database."""
        pass


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestUpdateEnvironment:
    """Class for testing Environment update() and update_all() methods."""

    __test__ = True

    _record = RAMSTKEnvironmentRecord
    _tag = "environment"
    _update_id = 1

    def on_succeed_update(self, tree):
        """Listen for succeed_update messages."""
        assert isinstance(tree, Tree)
        print(f"\033[36m\n\tsucceed_update_{self._update_id} topic was broadcast.")

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
            f"The value for one or more attributes for "
            f"{self._tag.replace('_', ' ')} ID {self._update_id} was the wrong type."
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
            message == f"Attempted to save non-existent {self._tag.replace('_', ' ')} "
            f"with {self._tag.replace('_', ' ')} ID 100."
        )
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on non-existent "
            f"ID."
        )

    def on_fail_update_no_data_package(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert (
            message == f"No data package found for {self._tag.replace('_', ' ')} "
            f"ID {self._update_id}."
        )
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on no data "
            f"package."
        )

    @pytest.mark.integration
    def test_do_update(self, integration_test_table_model):
        """Should send the success message after updating an environment record."""
        pub.subscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

        _environment = integration_test_table_model.do_select(self._update_id)
        _environment.name = "Big test environment"
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

    @pytest.mark.integration
    def test_do_update_all(self, integration_test_table_model):
        """Should send the success message after updating all environment records."""
        pub.subscribe(self.on_succeed_update_all, f"succeed_update_all_{self._tag}")

        _environment = integration_test_table_model.do_select(self._update_id)
        _environment.name = "Even bigger test environment"

        pub.sendMessage(f"request_update_all_{self._tag}")

        assert (
            integration_test_table_model.do_select(self._update_id).name
            == "Even bigger test environment"
        )

        pub.subscribe(self.on_succeed_update_all, f"succeed_update_all_{self._tag}")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, integration_test_table_model):
        """Should send the fail message when data type is wrong for attribute."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

        _environment = integration_test_table_model.do_select(self._update_id)
        _environment.name = {1: 2}
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, integration_test_table_model):
        """Should send the fail message when data type is wrong for root node."""
        pub.subscribe(self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg")

        _environment = integration_test_table_model.do_select(self._update_id)
        _environment.name = {1: 2}
        pub.sendMessage(f"request_update_{self._tag}", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """Should send the fail message when the environment ID does not exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

        pub.sendMessage(f"request_update_{self._tag}", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, integration_test_table_model):
        """Should send the fail message when no record exists for environment ID."""
        pub.subscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")

        integration_test_table_model.tree.get_node(self._update_id).data.pop(self._tag)
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")


@pytest.mark.usefixtures(
    "integration_test_table_model",
    "test_suite_logger",
)
class TestGetterSetterEnvironment(SystemTestGetterSetterMethods):
    """Class for testing Environment table getter and setter methods."""

    __test__ = True

    _package = {"name": "This is the environment name."}
    _record = RAMSTKEnvironmentRecord
    _tag = "environment"
    _test_id = 1
