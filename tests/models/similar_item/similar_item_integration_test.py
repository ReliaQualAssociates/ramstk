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
from ramstk.models import RAMSTKSimilarItemRecord, RAMSTKSimilarItemTable


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKSimilarItemTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_similar_item_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_similar_item_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_similar_item")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_similar_item")
    pub.unsubscribe(dut.do_update, "request_update_similar_item")
    pub.unsubscribe(dut.do_get_tree, "request_get_similar_item_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_similar_item")
    pub.unsubscribe(dut.do_insert, "request_insert_similar_item")
    pub.unsubscribe(dut.do_calculate_similar_item, "request_calculate_similar_item")
    pub.unsubscribe(
        dut.do_roll_up_change_descriptions, "request_roll_up_change_descriptions"
    )

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data["similar_item"], RAMSTKSimilarItemRecord
        )
        print("\033[36m\nsucceed_retrieve_similar_item topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_datamanager):
        """should clear nodes from an existing records tree and re-populate."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_similar_item")

        test_datamanager.do_select_all(attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_similar_item")


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestInsertMethods:
    """Class for testing the insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 8
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(node_id).data["similar_item"], RAMSTKSimilarItemRecord
        )
        assert tree.get_node(node_id).data["similar_item"].revision_id == 1
        assert tree.get_node(node_id).data["similar_item"].hardware_id == 8
        assert tree.get_node(node_id).data["similar_item"].parent_id == 2
        print("\033[36m\nsucceed_insert_similar_item topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  "
            "Database returned:\n\tKey (fld_revision_id)=(40) is not present "
            'in table "ramstk_revision".'
        )
        print("\033[35m\nfail_insert_similar_item topic was broadcast on no revision.")

    def on_fail_insert_no_hardware(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_hardware_id)=(15) is not present in table "
            '"ramstk_hardware".'
        )
        print("\033[35m\nfail_insert_similar_item topic was broadcast on no hardware.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_datamanager):
        """should add a record to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_similar_item")

        assert test_datamanager.tree.get_node(8) is None

        test_attributes["hardware_id"] = 8
        test_attributes["parent_id"] = 2
        pub.sendMessage("request_insert_similar_item", attributes=test_attributes)

        assert isinstance(
            test_datamanager.tree.get_node(8).data["similar_item"],
            RAMSTKSimilarItemRecord,
        )

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_similar_item")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_attributes, test_datamanager):
        """should not add a record when passed a non-existent revision ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_similar_item")

        assert test_datamanager.tree.get_node(9) is None

        test_attributes["revision_id"] = 40
        test_attributes["hardware_id"] = 9
        test_attributes["parent_id"] = 1
        pub.sendMessage("request_insert_similar_item", attributes=test_attributes)

        assert test_datamanager.tree.get_node(9) is None

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_similar_item")

    @pytest.mark.integration
    def test_do_insert_no_hardware(self, test_attributes, test_datamanager):
        """should not add a record when passed a non-existent hardware ID."""
        pub.subscribe(self.on_fail_insert_no_hardware, "fail_insert_similar_item")

        assert test_datamanager.tree.get_node(15) is None

        test_attributes["hardware_id"] = 15
        pub.sendMessage("request_insert_similar_item", attributes=test_attributes)

        assert test_datamanager.tree.get_node(15) is None

        pub.unsubscribe(self.on_fail_insert_no_hardware, "fail_insert_similar_item")


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_similar_item topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "Attempted to delete non-existent Similar Item ID 300."
        )
        print(
            "\033[35m\nfail_delete_similar_item topic was broadcast on non-existent "
            "ID."
        )

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == ("Attempted to delete non-existent Similar Item ID 2.")
        print(
            "\033[35m\nfail_delete_similar_item topic was broadcast on no data package."
        )

    @pytest.mark.integration
    def test_do_delete(self, test_datamanager):
        """should remove record from record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_similar_item")

        _last_id = test_datamanager.last_id
        pub.sendMessage("request_delete_similar_item", node_id=_last_id)

        assert test_datamanager.tree.get_node(_last_id) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_similar_item")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """should send the fail message when passed a non-existent record ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_similar_item")

        pub.sendMessage("request_delete_similar_item", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_similar_item")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_datamanager):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_similar_item")

        test_datamanager.tree.get_node(2).data.pop("similar_item")
        pub.sendMessage("request_delete_similar_item", node_id=2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_similar_item")


@pytest.mark.usefixtures("test_datamanager")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["similar_item"].parent_id == 1
        assert tree.get_node(2).data["similar_item"].percent_weight_factor == 0.9832
        assert tree.get_node(2).data["similar_item"].mtbf_goal == 12000
        print("\033[36m\nsucceed_update_similar_item topic was broadcast.")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast for Similar Item.")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for similar item "
            "ID 1 was the wrong type."
        )
        print(
            "\033[35m\nfail_update_similar_item topic was broadcast on wrong data "
            "type."
        )

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_similar_item topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent similar item with "
            "similar item ID 100."
        )
        print(
            "\033[35m\nfail_update_similar_item topic was broadcast on non-existent "
            "ID."
        )

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for similar item ID 1."
        )
        print(
            "\033[35m\nfail_update_similar_item topic was broadcast on no data package."
        )

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, "succeed_update_similar_item")

        _similar_item = test_datamanager.do_select(1)
        _similar_item.change_description_1 = "This is a description of the change."
        pub.sendMessage("request_update_similar_item", node_id=2, table="similar_item")

        assert (
            test_datamanager.do_select(1).change_description_1
            == "This is a description of the change."
        )

        pub.unsubscribe(self.on_succeed_update, "succeed_update_similar_item")

    @pytest.mark.integration
    def test_do_update_all(self, test_datamanager):
        """should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        _similar_item = test_datamanager.do_select(1)
        _similar_item.change_description_1 = (
            "This is change description 1 from test_do_update_all"
        )
        _similar_item.quality_from_id = 12000
        _similar_item = test_datamanager.do_select(2)
        _similar_item.change_description_2 = (
            "This is change description 2 from test_do_update_all"
        )
        _similar_item.temperature_to = 18500

        pub.sendMessage("request_update_all_similar_items")

        assert test_datamanager.tree.get_node(1).data[
            "similar_item"
        ].change_description_1 == (
            "This is change description 1 from test_do_update_all"
        )
        assert (
            test_datamanager.tree.get_node(1).data["similar_item"].quality_from_id
            == 12000
        )
        assert test_datamanager.tree.get_node(2).data[
            "similar_item"
        ].change_description_2 == (
            "This is change description 2 from test_do_update_all"
        )
        assert (
            test_datamanager.tree.get_node(2).data["similar_item"].temperature_to
            == 18500
        )

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_similar_item")

        _similar_item = test_datamanager.do_select(1)
        _similar_item.change_factor_1 = {1: 2}
        pub.sendMessage("request_update_similar_item", node_id=1, table="similar_item")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_similar_item")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """should send the fail message when attempting to update the root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_similar_item"
        )

        _similar_item = test_datamanager.do_select(1)
        _similar_item.change_factor_1 = {1: 2}

        pub.sendMessage("request_update_similar_item", node_id=0, table="similar_item")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_similar_item"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """should send the fail message when updating a non-existent record ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_similar_item")

        pub.sendMessage(
            "request_update_similar_item", node_id=100, table="similar_item"
        )

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_similar_item")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_similar_item")

        test_datamanager.tree.get_node(1).data.pop("similar_item")
        pub.sendMessage("request_update_similar_item", node_id=1, table="similar_item")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_similar_item")


@pytest.mark.usefixtures("test_datamanager")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["change_description_1"] == ""
        assert attributes["change_description_2"] == ""
        assert attributes["change_description_3"] == ""
        assert attributes["change_description_4"] == ""
        assert attributes["change_description_5"] == ""
        assert attributes["change_description_6"] == ""
        assert attributes["change_description_7"] == ""
        assert attributes["change_description_8"] == ""
        assert attributes["change_description_9"] == ""
        assert attributes["change_description_10"] == ""
        assert attributes["change_factor_1"] == 0.85
        assert attributes["change_factor_2"] == 1.2
        assert attributes["change_factor_3"] == 1.0
        assert attributes["change_factor_4"] == 1.0
        assert attributes["change_factor_5"] == 1.0
        assert attributes["change_factor_6"] == 1.0
        assert attributes["change_factor_7"] == 1.0
        assert attributes["change_factor_8"] == 1.0
        assert attributes["change_factor_9"] == 1.0
        assert attributes["change_factor_10"] == 1.0
        assert attributes["environment_from_id"] == 2
        assert attributes["environment_to_id"] == 3
        assert attributes["function_1"] == "pi1*pi2*hr"
        assert attributes["function_2"] == "0"
        assert attributes["function_3"] == "0"
        assert attributes["function_4"] == "0"
        assert attributes["function_5"] == "0"
        assert attributes["parent_id"] == 1
        assert attributes["similar_item_method_id"] == 2
        assert attributes["quality_from_id"] == 1
        assert attributes["quality_to_id"] == 2
        assert attributes["result_1"] == 0.0
        assert attributes["result_2"] == 0.0
        assert attributes["result_3"] == 0.0
        assert attributes["result_4"] == 0.0
        assert attributes["result_5"] == 0.0
        assert attributes["temperature_from"] == 55.0
        assert attributes["temperature_to"] == 65.0
        assert attributes["user_blob_1"] == ""
        assert attributes["user_blob_2"] == ""
        assert attributes["user_blob_3"] == ""
        assert attributes["user_blob_4"] == ""
        assert attributes["user_blob_5"] == ""
        assert attributes["user_float_1"] == 0.0
        assert attributes["user_float_2"] == 0.0
        assert attributes["user_float_3"] == 0.0
        assert attributes["user_float_4"] == 0.0
        assert attributes["user_float_5"] == 0.0
        assert attributes["user_int_1"] == 0
        assert attributes["user_int_2"] == 0
        assert attributes["user_int_3"] == 0
        assert attributes["user_int_4"] == 0
        assert attributes["user_int_5"] == 0
        print("\033[36m\nsucceed_get_similar_item_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data["similar_item"], RAMSTKSimilarItemRecord
        )
        print("\033[36m\nsucceed_get_similar_item_tree topic was broadcast.")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert (
            tree.get_node(1).data["similar_item"].change_description_1
            == "Testing set name from moduleview."
        )
        print("\033[36m\nsucceed_get_similar_item_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self):
        """should return the attributes dict."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_similar_item_attributes"
        )

        pub.sendMessage(
            "request_get_similar_item_attributes", node_id=2, table="similar_item"
        )

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_similar_item_attributes"
        )

    @pytest.mark.integration
    def test_on_get_data_manager_tree(self):
        """should return the records tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_similar_item_tree"
        )

        pub.sendMessage("request_get_similar_item_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_similar_item_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self):
        """should set the value of the attribute requested."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_similar_item_tree")

        pub.sendMessage(
            "request_set_similar_item_attributes",
            node_id=[1],
            package={"change_description_1": "Testing set name from moduleview."},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_similar_item_tree")


@pytest.mark.usefixtures("test_attributes", "test_datamanager")
class TestAnalysisMethods:
    """Class for similar item analysis methods test suite."""

    def on_succeed_calculate_topic_633(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["similar_item"].change_factor_1 == 0.8
        assert tree.get_node(1).data["similar_item"].change_factor_2 == 1.4
        assert tree.get_node(1).data["similar_item"].change_factor_3 == 1.0
        assert tree.get_node(1).data["similar_item"].result_1 == pytest.approx(
            0.0005607143
        )
        print(
            "\033[36m\nsucceed_calculate_similar_item topic was broadcast for "
            "Topic 633."
        )

    def on_succeed_calculate_user_defined(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["similar_item"].change_factor_1 == 0.85
        assert tree.get_node(1).data["similar_item"].change_factor_2 == 1.2
        assert tree.get_node(1).data["similar_item"].result_1 == pytest.approx(
            0.0062934
        )
        print(
            "\033[36m\nsucceed_calculate_similar_item topic was broadcast for User "
            "Defined."
        )

    def on_fail_calculate_unknown_method(self, error_message):
        assert error_message == (
            "Failed to calculate similar item reliability for hardware ID 1.  Unknown "
            "similar item method ID 22 selected."
        )
        print(
            "\033[35m\nfail_calculate_similar_item topic was broadcast on unknown "
            "method."
        )

    @pytest.mark.integration
    def test_do_calculate_similar_item_topic_633(self, test_datamanager):
        """should calculate the Topic 6.3.3 similar item."""
        pub.subscribe(
            self.on_succeed_calculate_topic_633, "succeed_calculate_similar_item"
        )

        test_datamanager._node_hazard_rate = 0.000628

        test_datamanager.tree.get_node(1).data[
            "similar_item"
        ].similar_item_method_id = 1
        test_datamanager.tree.get_node(1).data["similar_item"].environment_from_id = 2
        test_datamanager.tree.get_node(1).data["similar_item"].environment_to_id = 3
        test_datamanager.tree.get_node(1).data["similar_item"].quality_from_id = 1
        test_datamanager.tree.get_node(1).data["similar_item"].quality_to_id = 2
        test_datamanager.tree.get_node(1).data["similar_item"].temperature_from = 55.0
        test_datamanager.tree.get_node(1).data["similar_item"].temperature_to = 65.0

        pub.sendMessage("request_calculate_similar_item", node_id=1)

        assert (
            test_datamanager.tree.get_node(1).data["similar_item"].change_factor_1
            == 0.8
        )
        assert (
            test_datamanager.tree.get_node(1).data["similar_item"].change_factor_2
            == 1.4
        )
        assert (
            test_datamanager.tree.get_node(1).data["similar_item"].change_factor_3
            == 1.0
        )
        assert test_datamanager.tree.get_node(1).data[
            "similar_item"
        ].result_1 == pytest.approx(0.0005607143)

        pub.unsubscribe(
            self.on_succeed_calculate_topic_633, "succeed_calculate_similar_item"
        )

    @pytest.mark.integration
    def test_do_calculate_similar_item_user_defined(self, test_datamanager):
        """should calculate user-defined similar item."""
        pub.subscribe(
            self.on_succeed_calculate_user_defined, "succeed_calculate_similar_item"
        )

        test_datamanager._node_hazard_rate = 0.00617

        test_datamanager.tree.get_node(1).data[
            "similar_item"
        ].similar_item_method_id = 2
        test_datamanager.tree.get_node(1).data[
            "similar_item"
        ].change_description_1 = "Test change description for factor #1."
        test_datamanager.tree.get_node(1).data["similar_item"].change_factor_1 = 0.85
        test_datamanager.tree.get_node(1).data["similar_item"].change_factor_2 = 1.2
        test_datamanager.tree.get_node(1).data["similar_item"].function_1 = "pi1*pi2*hr"
        test_datamanager.tree.get_node(1).data["similar_item"].function_2 = "0"
        test_datamanager.tree.get_node(1).data["similar_item"].function_3 = "0"
        test_datamanager.tree.get_node(1).data["similar_item"].function_4 = "0"
        test_datamanager.tree.get_node(1).data["similar_item"].function_5 = "0"

        pub.sendMessage("request_calculate_similar_item", node_id=1)

        assert (
            test_datamanager.tree.get_node(1).data["similar_item"].change_factor_1
            == 0.85
        )
        assert (
            test_datamanager.tree.get_node(1).data["similar_item"].change_factor_2
            == 1.2
        )
        assert test_datamanager.tree.get_node(1).data[
            "similar_item"
        ].result_1 == pytest.approx(0.0062934)

        pub.unsubscribe(
            self.on_succeed_calculate_user_defined, "succeed_calculate_similar_item"
        )

    @pytest.mark.integration
    def test_do_calculate_unknown_method(self, test_datamanager):
        """should send the fail message with unknown similar item method specified."""
        pub.subscribe(
            self.on_fail_calculate_unknown_method, "fail_calculate_similar_item"
        )

        test_datamanager.tree.get_node(1).data[
            "similar_item"
        ].similar_item_method_id = 22

        pub.sendMessage("request_calculate_similar_item", node_id=1)

        pub.unsubscribe(
            self.on_fail_calculate_unknown_method, "fail_calculate_similar_item"
        )
