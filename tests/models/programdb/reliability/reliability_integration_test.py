# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.reliability.reliability_integration_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Reliability module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKReliabilityRecord
from ramstk.models.dbtables import RAMSTKHardwareTable, RAMSTKReliabilityTable
from tests import (
    SystemTestDeleteMethods,
    SystemTestGetterSetterMethods,
    SystemTestInsertMethods,
    SystemTestSelectMethods,
)


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestSelectReliability(SystemTestSelectMethods):
    """Class for testing Reliability table do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _record = RAMSTKReliabilityRecord
    _select_id = 1
    _tag = "reliability"


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestInsertReliability(SystemTestInsertMethods):
    """Class for testing Reliability table do_insert() method."""

    __test__ = True

    _insert_id = 8
    _record = RAMSTKReliabilityRecord
    _tag = "reliability"

    @pytest.mark.integration
    def test_do_insert_sibling_assembly(
        self, test_attributes, integration_test_table_model, test_hardware_table_model
    ):
        """Should add a record to the record tree and update last_id."""
        assert integration_test_table_model.tree.get_node(9) is None

        pub.sendMessage(
            "request_insert_hardware",
            attributes={
                "revision_id": 1,
                "hardware_id": 9,
                "parent_id": 2,
                "part": 0,
            },
        )

        assert isinstance(
            integration_test_table_model.tree.get_node(9).data[self._tag],
            RAMSTKReliabilityRecord,
        )
        assert (
            integration_test_table_model.tree.get_node(9).data[self._tag].revision_id
            == 1
        )
        assert (
            integration_test_table_model.tree.get_node(9).data[self._tag].hardware_id
            == 9
        )

    @pytest.mark.integration
    def test_do_insert_part(
        self, test_attributes, integration_test_table_model, test_hardware_table_model
    ):
        """Should add a record to the record tree and update last_id."""
        assert integration_test_table_model.tree.get_node(10) is None

        pub.sendMessage(
            "request_insert_hardware",
            attributes={
                "revision_id": 1,
                "hardware_id": 10,
                "parent_id": 2,
                "part": 1,
            },
        )

        assert isinstance(
            integration_test_table_model.tree.get_node(10).data[self._tag],
            RAMSTKReliabilityRecord,
        )
        assert (
            integration_test_table_model.tree.get_node(10).data[self._tag].revision_id
            == 1
        )
        assert (
            integration_test_table_model.tree.get_node(10).data[self._tag].hardware_id
            == 10
        )

    @pytest.mark.skip(reason="Reliability records are added by database.")
    def test_do_insert_sibling(self, test_attributes, integration_test_table_model):
        """Should not run because Reliability are added by database."""
        pass

    @pytest.mark.skip(reason="Reliability records are added by database.")
    def test_do_insert_child(self, test_attributes, integration_test_table_model):
        """Should not run because Reliability are added by database."""
        pass

    @pytest.mark.skip(reason="Reliability records are added by database.")
    def test_do_insert_no_parent(self, test_attributes, integration_test_table_model):
        """Should not run because Reliability are added by database."""
        pass

    @pytest.mark.skip(reason="Reliability records are added by database.")
    def test_do_insert_no_revision(self, test_attributes, integration_test_table_model):
        """Should not run because Reliability are added by database."""
        pass


@pytest.mark.usefixtures("integration_test_table_model")
class TestDeleteReliability(SystemTestDeleteMethods):
    """Class for testing Reliability table do_delete() method."""

    __test__ = True

    _delete_id = 1
    _record = RAMSTKReliabilityRecord
    _tag = "reliability"

    @pytest.mark.skip(reason="Reliability records are deleted by database.")
    def test_do_delete_with_child(self, integration_test_table_model):
        """Should not run because Reliability are deleted by database."""
        pass

    @pytest.mark.skip(reason="Reliability records are deleted by database.")
    def test_do_delete_non_existent_id(self):
        """Should not run because Reliability are deleted by database."""
        pass


@pytest.mark.usefixtures("integration_test_table_model")
class TestUpdateReliability:
    """Class for testing Reliability table do_update() and do_update_all() methods."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKReliabilityRecord
    _tag = "reliability"
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

    def on_fail_update_root_node(self, logger_name, message):
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
        pub.subscribe(
            self.on_succeed_update,
            f"succeed_update_{self._tag}",
        )

        _reliability = integration_test_table_model.do_select(self._update_id)
        _reliability.category_id = 5
        _reliability.subcategory_id = 81
        pub.sendMessage(
            f"request_update_{self._tag}",
            node_id=self._update_id,
        )

        pub.unsubscribe(
            self.on_succeed_update,
            f"succeed_update_{self._tag}",
        )

    @pytest.mark.integration
    def test_do_update_all(self, integration_test_table_model):
        """Should update all records in the records tree."""
        pub.subscribe(
            self.on_succeed_update_all,
            f"succeed_update_all_{self._tag}",
        )

        _reliability = integration_test_table_model.do_select(self._update_id - 1)
        _reliability.category_id = 5
        _reliability.subcategory_id = 81
        _reliability = integration_test_table_model.do_select(self._update_id)
        _reliability.category_id = 12
        _reliability.subcategory_id = 71

        pub.sendMessage(f"request_update_all_{self._tag}")

        assert (
            integration_test_table_model.tree.get_node(self._update_id - 1)
            .data[self._tag]
            .category_id
            == 5
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id - 1)
            .data[self._tag]
            .subcategory_id
            == 81
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .category_id
            == 12
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .subcategory_id
            == 71
        )

        pub.unsubscribe(
            self.on_succeed_update_all,
            f"succeed_update_all_{self._tag}",
        )

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, integration_test_table_model):
        """Should send the fail message when the wrong data type is assigned."""
        pub.subscribe(
            self.on_fail_update_wrong_data_type,
            "do_log_debug_msg",
        )

        _reliability = integration_test_table_model.do_select(self._update_id)
        _reliability.hazard_rate_active = {1: 2}
        pub.sendMessage(
            f"request_update_{self._tag}",
            node_id=self._update_id,
        )

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

        pub.sendMessage(
            f"request_update_{self._tag}",
            node_id=0,
        )

        pub.unsubscribe(
            self.on_fail_update_root_node,
            "do_log_debug_msg",
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """Should send the fail message when updating a non-existent record ID."""
        pub.subscribe(
            self.on_fail_update_non_existent_id,
            "do_log_debug_msg",
        )

        pub.sendMessage(
            f"request_update_{self._tag}",
            node_id=100,
        )

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
        pub.sendMessage(
            f"request_update_{self._tag}",
            node_id=self._update_id,
        )

        pub.unsubscribe(
            self.on_fail_update_no_data_package,
            "do_log_debug_msg",
        )


@pytest.mark.usefixtures("integration_test_table_model")
class TestGetterSetterReliability(SystemTestGetterSetterMethods):
    """Class for testing Reliability table getter and setter methods."""

    __test__ = True

    _package = {"location_parameter": 65.5}
    _record = RAMSTKReliabilityRecord
    _tag = "reliability"
    _test_id = 1
