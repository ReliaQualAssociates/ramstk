# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mechanism.mechanism_integration_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing failure Mechanism integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMechanismRecord
from ramstk.models.dbtables import RAMSTKMechanismTable
from tests import (
    SystemTestDeleteMethods,
    SystemTestGetterSetterMethods,
    SystemTestInsertMethods,
    SystemTestSelectMethods,
)


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestSelectMechanism(SystemTestSelectMethods):
    """Class for testing Mechanism table do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _record = RAMSTKMechanismRecord
    _select_id = 3
    _tag = "mechanism"


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestInsertMechanism(SystemTestInsertMethods):
    """Class for testing Mechanism table do_insert() method."""

    __test__ = True

    _insert_id = 4
    _record = RAMSTKMechanismRecord
    _tag = "mechanism"

    @pytest.mark.skip(reason="Mechanism records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, integration_test_table_model):
        """Should not run because Mechanisms are not hierarchical."""
        pass

    @pytest.mark.skip(reason="Mechanism records are non-hierarchical.")
    def test_do_insert_no_parent(self, test_attributes, integration_test_table_model):
        """Should not run because Mechanisms are not hierarchical."""
        pass


@pytest.mark.usefixtures("integration_test_table_model")
class TestDeleteMechanism(SystemTestDeleteMethods):
    """Class for testing Mechanism table do_delete() method."""

    __test__ = True

    _delete_id = 4
    _next_id = 0
    _record = RAMSTKMechanismRecord
    _tag = "mechanism"

    @pytest.mark.skip(reason="Mechanism records are non-hierarchical.")
    def test_do_delete_with_child(self, integration_test_table_model):
        """Should not run because Mechanisms are not hierarchical."""
        pass


@pytest.mark.usefixtures("integration_test_table_model")
class TestUpdateMechanism:
    """Class for testing Mechanism table do_update() and do_update_all() methods."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKMechanismRecord
    _tag = "mechanism"
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
        """Should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].description = "Test failure mechanism"
        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].rpn_detection = 4
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

    @pytest.mark.integration
    def test_do_update_all(self, integration_test_table_model):
        """Should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, f"succeed_update_all_{self._tag}")

        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].description = "Test failure mechanism"
        integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].rpn_detection = 2
        integration_test_table_model.tree.get_node(self._update_id + 1).data[
            self._tag
        ].description = "Big test failure mechanism"
        integration_test_table_model.tree.get_node(self._update_id + 1).data[
            self._tag
        ].rpn_detection = 7
        pub.sendMessage(f"request_update_all_{self._tag}")

        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .description
            == "Test failure mechanism"
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
            == "Big test failure mechanism"
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
        """Should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_mechanism")

        _mechanism = integration_test_table_model.do_select(self._update_id)
        _mechanism.rpn_detection = {1: 2}
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_mechanism")

    @pytest.mark.integration
    def test_do_update_root_node(self, integration_test_table_model):
        """Should send the fail message when attempting to update the root node."""
        pub.subscribe(self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg")

        pub.sendMessage(f"request_update_{self._tag}", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """Should send the fail message when updating a non-existent record ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

        pub.sendMessage(f"request_update_{self._tag}", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, integration_test_table_model):
        """Should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")

        integration_test_table_model.tree.get_node(self._update_id).data.pop(self._tag)
        pub.sendMessage(f"request_update_{self._tag}", node_id=self._update_id)

        pub.unsubscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")


@pytest.mark.usefixtures("integration_test_table_model")
class TestGetterSetterMechanism(SystemTestGetterSetterMethods):
    """Class for testing Mechanism table getter and setter methods."""

    __test__ = True

    _package = {"rpn_detection": 4}
    _record = RAMSTKMechanismRecord
    _tag = "mechanism"
    _test_id = 4


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestMechanismAnalysisMethods:
    """Class for testing Mechanism analytical methods."""

    def on_succeed_calculate_rpn_mechanism(self, tree: Tree):
        """Listen for succeed_calculate messages."""
        assert isinstance(tree, Tree)
        assert tree.get_node(3).data["mechanism"].rpn == 192
        assert tree.get_node(3).data["mechanism"].rpn_new == 64
        print("\033[36m\n\tsucceed_calculate_mechanism_rpn topic was broadcast.")

    @pytest.mark.integration
    def test_do_calculate_mechanism_rpn(
        self, test_attributes, integration_test_table_model
    ):
        """Should calculate the mechanism RPN."""
        pub.subscribe(
            self.on_succeed_calculate_rpn_mechanism, "succeed_calculate_mechanism_rpn"
        )

        integration_test_table_model.do_select_all(test_attributes)

        integration_test_table_model.tree.get_node(3).data[
            "mechanism"
        ].rpn_occurrence = 8
        integration_test_table_model.tree.get_node(3).data[
            "mechanism"
        ].rpn_detection = 3
        integration_test_table_model.tree.get_node(3).data[
            "mechanism"
        ].rpn_occurrence_new = 4
        integration_test_table_model.tree.get_node(3).data[
            "mechanism"
        ].rpn_detection_new = 2

        pub.sendMessage("request_calculate_mechanism_rpn", severity=8)

        assert (
            integration_test_table_model.tree.get_node(3).data["mechanism"].rpn == 192
        )
        assert (
            integration_test_table_model.tree.get_node(3).data["mechanism"].rpn_new
            == 64
        )

        pub.unsubscribe(
            self.on_succeed_calculate_rpn_mechanism, "succeed_calculate_mechanism_rpn"
        )
