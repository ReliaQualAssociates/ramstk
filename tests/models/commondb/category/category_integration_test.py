# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.category.category_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Category module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKCategoryRecord
from ramstk.models.dbtables import RAMSTKCategoryTable


@pytest.fixture(scope="class")
def test_tablemodel(test_common_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKCategoryTable()
    dut.do_connect(test_common_dao)
    dut.do_select_all({"category_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_category_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_category_attributes")
    pub.unsubscribe(dut.do_update, "request_update_category")
    pub.unsubscribe(dut.do_get_tree, "request_get_category_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_category_attributes")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["category"], RAMSTKCategoryRecord)
        # There should be a root node with no data package and a node with
        # the one RAMSTKCategoryRecord record.
        assert len(tree.all_nodes()) == 2
        print("\033[36m\nsucceed_retrieve_category topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_tablemodel):
        """do_select_all() should clear nodes from an existing Category tree."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_category")

        test_tablemodel.do_select_all({"category_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_category")


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["category"].description == "New Category"
        assert tree.get_node(1).data["category"].harsh_ir_limit == 0.5
        print("\033[36m\nsucceed_update_category topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for category ID 1 was the "
            "wrong type."
        )
        print("\033[35m\nfail_update_category topic was broadcast on wrong type.")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_category topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent category with category ID "
            "skullduggery."
        )
        print("\033[35m\nfail_update_category topic was broadcast on non-existent ID.")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for category ID 1.")
        print("\033[35m\nfail_update_category topic was broadcast on no data package.")

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_category")

        test_tablemodel.tree.get_node(1).data["category"].description = "New Category"
        test_tablemodel.tree.get_node(1).data["category"].harsh_ir_limit = 0.5
        test_tablemodel.do_update(1)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_category")

        assert (
            test_tablemodel.tree.get_node(1).data["category"].description
            == "New Category"
        )
        assert test_tablemodel.tree.get_node(1).data["category"].harsh_ir_limit == 0.5

        test_tablemodel.tree.get_node(1).data[
            "category"
        ].description = "Integrated Circuit"
        test_tablemodel.tree.get_node(1).data["category"].harsh_ir_limit = 0.8
        test_tablemodel.do_update(1)

        assert (
            test_tablemodel.tree.get_node(1).data["category"].description
            == "Integrated Circuit"
        )
        assert test_tablemodel.tree.get_node(1).data["category"].harsh_ir_limit == 0.8

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """do_update_all() should broadcast the succeed message on success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all_category")

        pub.sendMessage("request_update_all_category")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all_category")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_category")

        test_tablemodel.tree.get_node(1).data["category"].mild_maxt_limit = "Hi ya"
        test_tablemodel.do_update(1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_category")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """do_update() should return a zero error code on success."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_category"
        )

        test_tablemodel.tree.get_node(1).data["category"].mild_maxt_limit = "Hey bud"
        test_tablemodel.do_update(0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_category"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Category ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_category")

        test_tablemodel.do_select_all({"category_id": 1})
        test_tablemodel.do_update("skullduggery")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_category")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Category ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_category")

        test_tablemodel.tree.get_node(1).data.pop("category")
        test_tablemodel.do_update(1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_category")


@pytest.mark.usefixtures("test_tablemodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert _attributes["category_id"] == 1
        assert _attributes["category_type"] == "hardware"
        assert _attributes["name"] == "IC"
        assert _attributes["value"] == 1
        assert _attributes["description"] == "Integrated Circuit"
        assert _attributes["harsh_ir_limit"] == 0.8
        assert _attributes["mild_ir_limit"] == 0.9
        assert _attributes["harsh_pr_limit"] == 1.0
        assert _attributes["mild_pr_limit"] == 1.0
        assert _attributes["harsh_vr_limit"] == 1.0
        assert _attributes["mild_vr_limit"] == 1.0
        assert _attributes["harsh_deltat_limit"] == 0.0
        assert _attributes["mild_deltat_limit"] == 0.0
        assert _attributes["harsh_maxt_limit"] == 125.0
        assert _attributes["mild_maxt_limit"] == 125.0
        print("\033[36m\nsucceed_get_category_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["category"], RAMSTKCategoryRecord)
        print("\033[36m\nsucceed_get_category_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["category"].harsh_pr_limit == 0.8
        assert tree.get_node(1).data["category"].harsh_vr_limit == 1.1
        print("\033[36m\nsucceed_get_category_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_tablemodel):
        """do_get_attributes() should return a dict of site information attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_category_attributes")

        pub.sendMessage(
            "request_get_category_attributes2", attributes={"category_id": 1}
        )

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_category_attributes"
        )

    @pytest.mark.integration
    def test_on_get_data_manager_tree(self, test_tablemodel):
        """on_get_tree() should return the Category treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_category_tree"
        )

        pub.sendMessage("request_get_category_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_category_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_tablemodel):
        """do_set_attributes() should return None when successfully setting site
        information attributes."""

        pub.sendMessage(
            "request_set_category_attributes",
            node_id=1,
            package={"harsh_pr_limit": 0.8},
        )

        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_category_tree")

        pub.sendMessage(
            "request_set_category_attributes",
            node_id=1,
            package={"harsh_vr_limit": 1.1},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_category_tree")
