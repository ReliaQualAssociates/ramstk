# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.similar_item.similar_item_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Similar Item module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKSimilarItemRecord
from ramstk.models.dbtables import RAMSTKHardwareTable, RAMSTKSimilarItemTable
from tests import (
    SystemTestDeleteMethods,
    SystemTestGetterSetterMethods,
    SystemTestInsertMethods,
    SystemTestSelectMethods,
)


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestSelectSimilarItem(SystemTestSelectMethods):
    """Class for testing Similar Item table do_select() and do_select_all() methods."""

    __test__ = True

    _do_select_msg = "selected_revision"
    _record = RAMSTKSimilarItemRecord
    _select_id = 1
    _tag = "similar_item"


@pytest.mark.usefixtures(
    "test_attributes", "integration_test_table_model", "test_hardware_table"
)
class TestInsertSimilarItem:
    """Class for testing the Similar Item do_insert() method."""

    @pytest.mark.integration
    def test_do_insert_sibling_assembly(
        self, test_attributes, integration_test_table_model, test_hardware_table
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
            integration_test_table_model.tree.get_node(9).data["similar_item"],
            RAMSTKSimilarItemRecord,
        )
        assert (
            integration_test_table_model.tree.get_node(9)
            .data["similar_item"]
            .revision_id
            == 1
        )
        assert (
            integration_test_table_model.tree.get_node(9)
            .data["similar_item"]
            .hardware_id
            == 9
        )
        assert (
            integration_test_table_model.tree.get_node(9).data["similar_item"].parent_id
            == 2
        )

    @pytest.mark.integration
    def test_do_insert_part(
        self, test_attributes, integration_test_table_model, test_hardware_table
    ):
        """Should NOT add a record to the record tree and update last_id."""
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

        assert integration_test_table_model.tree.get_node(10) is None


@pytest.mark.usefixtures("integration_test_table_model")
class TestDeleteSimilarItem(SystemTestDeleteMethods):
    """Class for testing Similar Item table do_delete() method."""

    __test__ = True

    _delete_id = 2
    _next_id = 0
    _record = RAMSTKSimilarItemRecord
    _tag = "similar_item"


@pytest.mark.usefixtures("integration_test_table_model")
class TestUpdateSimilarItem:
    """Class for testing SimilarItem update() and update_all() methods."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKSimilarItemRecord
    _tag = "similar_item"
    _update_id = 1

    def on_succeed_update(self, tree):
        """Listen for succeed_update messages."""
        assert isinstance(tree, Tree)
        assert tree.get_node(self._update_id).data[self._tag].parent_id == 0
        assert (
            tree.get_node(self._update_id).data[self._tag].percent_weight_factor
            == 0.9832
        )
        assert tree.get_node(self._update_id).data[self._tag].mtbf_goal == 12000
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
            f"The value for one or more attributes for "
            f"{self._tag.replace('_', ' ')} ID {self._update_id} was the wrong type."
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
        """Should update record attribute."""
        pub.subscribe(
            self.on_succeed_update,
            f"succeed_update_{self._tag}",
        )

        _similar_item = integration_test_table_model.do_select(self._update_id)
        _similar_item.change_description_1 = "This is a description of the change."
        pub.sendMessage(
            f"request_update_{self._tag}",
            node_id=self._update_id,
        )

        assert (
            integration_test_table_model.do_select(self._update_id).change_description_1
            == "This is a description of the change."
        )

        pub.unsubscribe(
            self.on_succeed_update,
            f"succeed_update_{self._tag}",
        )

    @pytest.mark.integration
    def test_do_update_all(self, integration_test_table_model):
        """Should update all the records in the database."""
        pub.subscribe(
            self.on_succeed_update_all,
            f"succeed_update_all_{self._tag}",
        )

        _similar_item = integration_test_table_model.do_select(self._update_id)
        _similar_item.change_description_1 = (
            "This is change description 1 from test_do_update_all"
        )
        _similar_item.quality_from_id = 12000
        _similar_item = integration_test_table_model.do_select(self._update_id + 1)
        _similar_item.change_description_2 = (
            "This is change description 2 from test_do_update_all"
        )
        _similar_item.temperature_to = 18500

        pub.sendMessage(
            f"request_update_all_{self._tag}",
        )

        assert integration_test_table_model.tree.get_node(self._update_id).data[
            self._tag
        ].change_description_1 == (
            "This is change description 1 from test_do_update_all"
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id)
            .data[self._tag]
            .quality_from_id
            == 12000
        )
        assert integration_test_table_model.tree.get_node(self._update_id + 1).data[
            self._tag
        ].change_description_2 == (
            "This is change description 2 from test_do_update_all"
        )
        assert (
            integration_test_table_model.tree.get_node(self._update_id + 1)
            .data[self._tag]
            .temperature_to
            == 18500
        )

        pub.unsubscribe(
            self.on_succeed_update_all,
            f"succeed_update_all_{self._tag}",
        )

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, integration_test_table_model):
        """Should send the do_log_debug message with wrong attribute data type."""
        pub.subscribe(
            self.on_fail_update_wrong_data_type,
            "do_log_debug_msg",
        )

        _similar_item = integration_test_table_model.do_select(self._update_id)
        _similar_item.change_factor_1 = {1: 2}
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
        """Should send the do_log_debug message when attempting to update root node."""
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
        """Should send the do_log_debug message with non-existent ID in tree."""
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
        """Should send the do_log_debug message with no data package in tree."""
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
class TestGetterSetterSimilarItem(SystemTestGetterSetterMethods):
    """Class for testing Similar Item table getter and setter methods."""

    __test__ = True

    _package = {"change_description_1": "Testing set name from moduleview."}
    _record = RAMSTKSimilarItemRecord
    _tag = "similar_item"
    _test_id = 1


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class TestSimilarItemAnalysisMethods:
    """Class for Similar Item analytical methods test suite."""

    def on_succeed_calculate_topic_633(self, tree):
        """Listen for succeed_calculate messages."""
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["similar_item"].change_factor_1 == 0.8
        assert tree.get_node(1).data["similar_item"].change_factor_2 == 1.4
        assert tree.get_node(1).data["similar_item"].change_factor_3 == 1.0
        assert tree.get_node(1).data["similar_item"].result_1 == pytest.approx(
            0.0005607143
        )
        print(
            "\033[36m\n\tsucceed_calculate_similar_item topic was broadcast for "
            "Topic 633."
        )

    def on_succeed_calculate_user_defined(self, tree):
        """Listen for succeed_calculate messages."""
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["similar_item"].change_factor_1 == 0.85
        assert tree.get_node(1).data["similar_item"].change_factor_2 == 1.2
        assert tree.get_node(1).data["similar_item"].result_1 == pytest.approx(
            0.0062934
        )
        print(
            "\033[36m\n\tsucceed_calculate_similar_item topic was broadcast for User "
            "Defined."
        )

    def on_fail_calculate_unknown_method(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == (
            "Failed to calculate similar item reliability for hardware ID 1.  Unknown "
            "similar item method ID 22 selected."
        )
        print(
            "\033[35m\n\tfail_calculate_similar_item topic was broadcast on unknown "
            "method."
        )

    @pytest.mark.integration
    def test_do_calculate_similar_item_topic_633(self, integration_test_table_model):
        """Should calculate the Topic 6.3.3 similar item."""
        pub.subscribe(
            self.on_succeed_calculate_topic_633,
            "succeed_calculate_similar_item",
        )

        integration_test_table_model._node_hazard_rate = 0.000628

        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].similar_item_method_id = 1
        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].environment_from_id = 2
        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].environment_to_id = 3
        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].quality_from_id = 1
        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].quality_to_id = 2
        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].temperature_from = 55.0
        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].temperature_to = 65.0

        pub.sendMessage(
            "request_calculate_similar_item",
            node_id=1,
        )

        assert (
            integration_test_table_model.tree.get_node(1)
            .data["similar_item"]
            .change_factor_1
            == 0.8
        )
        assert (
            integration_test_table_model.tree.get_node(1)
            .data["similar_item"]
            .change_factor_2
            == 1.4
        )
        assert (
            integration_test_table_model.tree.get_node(1)
            .data["similar_item"]
            .change_factor_3
            == 1.0
        )
        assert integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].result_1 == pytest.approx(0.0005607143)

        pub.unsubscribe(
            self.on_succeed_calculate_topic_633,
            "succeed_calculate_similar_item",
        )

    @pytest.mark.integration
    def test_do_calculate_similar_item_user_defined(self, integration_test_table_model):
        """Should calculate user-defined similar item."""
        pub.subscribe(
            self.on_succeed_calculate_user_defined,
            "succeed_calculate_similar_item",
        )

        integration_test_table_model._node_hazard_rate = 0.00617

        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].similar_item_method_id = 2
        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].change_description_1 = "Test change description for factor #1."
        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].change_factor_1 = 0.85
        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].change_factor_2 = 1.2
        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].function_1 = "pi1*pi2*hr"
        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].function_2 = "0"
        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].function_3 = "0"
        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].function_4 = "0"
        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].function_5 = "0"

        pub.sendMessage(
            "request_calculate_similar_item",
            node_id=1,
        )

        assert (
            integration_test_table_model.tree.get_node(1)
            .data["similar_item"]
            .change_factor_1
            == 0.85
        )
        assert (
            integration_test_table_model.tree.get_node(1)
            .data["similar_item"]
            .change_factor_2
            == 1.2
        )
        assert integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].result_1 == pytest.approx(0.0062934)

        pub.unsubscribe(
            self.on_succeed_calculate_user_defined,
            "succeed_calculate_similar_item",
        )

    @pytest.mark.integration
    def test_do_calculate_unknown_method(self, integration_test_table_model):
        """Should send the fail message with unknown similar item method specified."""
        pub.subscribe(
            self.on_fail_calculate_unknown_method,
            "do_log_debug_msg",
        )

        integration_test_table_model.tree.get_node(1).data[
            "similar_item"
        ].similar_item_method_id = 22

        pub.sendMessage(
            "request_calculate_similar_item",
            node_id=1,
        )

        pub.unsubscribe(
            self.on_fail_calculate_unknown_method,
            "do_log_debug_msg",
        )
