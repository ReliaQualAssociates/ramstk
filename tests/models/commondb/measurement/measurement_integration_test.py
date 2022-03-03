# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.commondb.measurement.measurement_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Measurement module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMeasurementRecord
from ramstk.models.dbtables import RAMSTKMeasurementTable


@pytest.fixture(scope="class")
def test_tablemodel(test_common_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMeasurementTable()
    dut.do_connect(test_common_dao)
    dut.do_select_all({"measurement_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_measurement_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_measurement_attributes")
    pub.unsubscribe(dut.do_update, "request_update_measurement")
    pub.unsubscribe(dut.do_get_tree, "request_get_measurement_tree")
    pub.unsubscribe(dut.do_select_all, "request_get_measurement_attributes")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["measurement"], RAMSTKMeasurementRecord)
        # There should be a root node with no data package and a node with
        # the one RAMSTKMeasurementRecord record.
        assert len(tree.all_nodes()) == 2
        print("\033[36m\nsucceed_retrieve_measurement topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_tablemodel):
        """do_select_all() should clear nodes from an existing Measurement tree."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_measurement")

        test_tablemodel.do_select_all({"measurement_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_measurement")


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["measurement"].description == "New Measurement"
        assert tree.get_node(1).data["measurement"].code == "New Code"
        print("\033[36m\nsucceed_update_measurement topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for measurement ID 1 was "
            "the wrong type."
        )
        print("\033[35m\nfail_update_measurement topic was broadcast on wrong type.")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == "do_update: Attempting to update the root node 0."
        print("\033[35m\nfail_update_measurement topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent measurement with measurement ID "
            "skullduggery."
        )
        print(
            "\033[35m\nfail_update_measurement topic was broadcast on non-existent ID."
        )

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for measurement ID 1."
        )
        print(
            "\033[35m\nfail_update_measurement topic was broadcast on no data package."
        )

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_measurement")

        test_tablemodel.tree.get_node(1).data[
            "measurement"
        ].description = "New Measurement"
        test_tablemodel.tree.get_node(1).data["measurement"].code = "New Code"
        test_tablemodel.do_update(1)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_measurement")

        assert (
            test_tablemodel.tree.get_node(1).data["measurement"].description
            == "New Measurement"
        )
        assert test_tablemodel.tree.get_node(1).data["measurement"].code == "New Code"

        test_tablemodel.tree.get_node(1).data[
            "measurement"
        ].description = "Integrated Circuit"
        test_tablemodel.tree.get_node(1).data["measurement"].code = "Old Code"
        test_tablemodel.do_update(1)

        assert (
            test_tablemodel.tree.get_node(1).data["measurement"].description
            == "Integrated Circuit"
        )
        assert test_tablemodel.tree.get_node(1).data["measurement"].code == "Old Code"

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """do_update_all() should broadcast the succeed message on success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all_measurement")

        pub.sendMessage("request_update_all_measurement")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all_measurement")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_measurement")

        test_tablemodel.tree.get_node(1).data["measurement"].mild_maxt_limit = "Hi ya"
        test_tablemodel.do_update(1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_measurement")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """do_update() should return a zero error code on success."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_measurement"
        )

        test_tablemodel.tree.get_node(1).data["measurement"].mild_maxt_limit = "Hey bud"
        test_tablemodel.do_update(0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_measurement"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Measurement ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_measurement")

        test_tablemodel.do_select_all({"measurement_id": 1})
        test_tablemodel.do_update("skullduggery")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_measurement")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """do_update() should return a non-zero error code when passed a Measurement ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_measurement")

        test_tablemodel.tree.get_node(1).data.pop("measurement")
        test_tablemodel.do_update(1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_measurement")


@pytest.mark.usefixtures("test_tablemodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["measurement_id"] == 1
        assert attributes["measurement_type"] == "unit"
        assert attributes["code"] == "lbf"
        assert attributes["description"] == "Pounds Force"
        print("\033[36m\nsucceed_get_measurement_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["measurement"], RAMSTKMeasurementRecord)
        print("\033[36m\nsucceed_get_measurement_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["measurement"].description == "Pounds Force"
        assert tree.get_node(1).data["measurement"].code == "Red"
        assert tree.get_node(1).data["measurement"].measurement_type == "Some Kind"
        print("\033[36m\nsucceed_get_measurement_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_tablemodel):
        """do_get_attributes() should return a dict of site information attributes on
        success."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_measurement_attributes"
        )

        pub.sendMessage("request_get_measurement_attributes", node_id=1)

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_measurement_attributes"
        )

    @pytest.mark.integration
    def test_on_get_data_manager_tree(self, test_tablemodel):
        """on_get_tree() should return the Measurement treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_measurement_tree"
        )

        pub.sendMessage("request_get_measurement_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_measurement_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_tablemodel):
        """do_set_attributes() should return None when successfully setting site
        information attributes."""

        pub.sendMessage(
            "request_set_measurement_attributes",
            node_id=1,
            package={"measurement_type": "Some Kind"},
        )

        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_measurement_tree")

        pub.sendMessage(
            "request_set_measurement_attributes",
            node_id=1,
            package={"code": "Red"},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_measurement_tree")
