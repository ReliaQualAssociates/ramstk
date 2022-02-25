# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.model.model_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Model module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKModelRecord, RAMSTKModelTable


@pytest.fixture(scope="class")
def test_tablemodel(test_common_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKModelTable()
    dut.do_connect(test_common_dao)
    dut.do_select_all({"model_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_model_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_model_attributes")
    pub.unsubscribe(dut.do_update, "request_update_model")
    pub.unsubscribe(dut.do_get_tree, "request_get_model_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_model_attributes")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["model"], RAMSTKModelRecord)
        # There should be a root node with no data package and a node with
        # the one RAMSTKModelRecord record.
        assert len(tree.all_nodes()) == 2
        print("\033[36m\nsucceed_retrieve_model topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_tablemodel):
        """do_select_all() should clear nodes from an existing Model tree."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_model")

        test_tablemodel.do_select_all({"model_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_model")


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["model"].description == "New Model"
        assert tree.get_node(1).data["model"].model_type == "damage"
        print("\033[36m\nsucceed_update_model topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for model ID 1 was the "
            "wrong type."
        )
        print("\033[35m\nfail_update_model topic was broadcast on wrong type.")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_model topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent model with model ID "
            "skullduggery."
        )
        print("\033[35m\nfail_update_model topic was broadcast on non-existent ID.")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for model ID 1.")
        print("\033[35m\nfail_update_model topic was broadcast on no data package.")

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_model")

        test_tablemodel.tree.get_node(1).data["model"].description = "New Model"
        test_tablemodel.tree.get_node(1).data["model"].model_type = "damage"
        test_tablemodel.do_update(1)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_model")

        assert test_tablemodel.tree.get_node(1).data["model"].description == "New Model"
        assert test_tablemodel.tree.get_node(1).data["model"].model_type == "damage"

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """do_update_all() should broadcast the succeed message on success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        pub.sendMessage("request_update_all_model")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_model")

        test_tablemodel.tree.get_node(1).data["model"].model_type = "Hi ya"
        test_tablemodel.do_update(1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_model")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """do_update() should return a zero error code on success."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_model"
        )

        test_tablemodel.tree.get_node(1).data["model"].model_type = "Hey bud"
        test_tablemodel.do_update(0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_model"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Model ID that
        doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_model")

        test_tablemodel.do_select_all({"model_id": 1})
        test_tablemodel.do_update("skullduggery")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_model")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Model ID that
        doesn't exist."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_model")

        test_tablemodel.tree.get_node(1).data.pop("model")
        test_tablemodel.do_update(1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_model")


@pytest.mark.usefixtures("test_tablemodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["model_id"] == 1
        assert attributes["model_type"] == "damage"
        assert attributes["description"] == "Adhesion Wear Model for Bearings"
        print("\033[36m\nsucceed_get_model_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["model"], RAMSTKModelRecord)
        print("\033[36m\nsucceed_get_model_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["model"].description == "Big Model"
        assert tree.get_node(1).data["model"].model_type == "sexy"
        print("\033[36m\nsucceed_get_model_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_tablemodel):
        """do_get_attributes() should return a dict of site information attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_model_attributes")

        pub.sendMessage("request_get_model_attributes", node_id=1)

        pub.unsubscribe(self.on_succeed_get_attributes, "succeed_get_model_attributes")

    @pytest.mark.integration
    def test_on_get_data_manager_tree(self, test_tablemodel):
        """on_get_tree() should return the Model treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_model_tree")

        pub.sendMessage("request_get_model_tree")

        pub.unsubscribe(self.on_succeed_get_data_manager_tree, "succeed_get_model_tree")

    @pytest.mark.integration
    def test_do_set_attributes(self, test_tablemodel):
        """do_set_attributes() should return None when successfully setting site
        information attributes."""

        pub.sendMessage(
            "request_set_model_attributes",
            node_id=1,
            package={"model_type": "sexy"},
        )

        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_model_tree")

        pub.sendMessage(
            "request_set_model_attributes",
            node_id=1,
            package={"description": "Big Model"},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_model_tree")