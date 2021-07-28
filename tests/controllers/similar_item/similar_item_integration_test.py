# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.similar_item.similar_item_integration_test.py is part of The
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
from ramstk.controllers import amSimilarItem, dmSimilarItem
from ramstk.models.programdb import RAMSTKHardware, RAMSTKReliability, RAMSTKSimilarItem


@pytest.fixture(scope="class")
def test_analysismanager(test_toml_user_configuration):
    # Create the device under test (dut) and connect to the configuration.
    dut = amSimilarItem(test_toml_user_configuration)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.on_get_all_attributes, "succeed_get_similar_item_attributes")
    pub.unsubscribe(dut.on_get_tree, "succeed_get_similar_item_tree")
    pub.unsubscribe(dut.on_get_tree, "succeed_retrieve_similar_item")
    pub.unsubscribe(dut.on_get_tree, "succeed_update_similar_item")
    pub.unsubscribe(dut._do_calculate_similar_item, "request_calculate_similar_item")
    pub.unsubscribe(
        dut._do_roll_up_change_descriptions, "request_roll_up_change_descriptions"
    )
    pub.unsubscribe(dut._on_get_hardware_attributes, "succeed_get_hardwares_tree")

    # Delete the device under test.
    del dut


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = dmSimilarItem()
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
    pub.unsubscribe(dut._do_delete, "request_delete_hardware")
    pub.unsubscribe(dut._do_insert_similar_item, "request_insert_similar_item")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_datamanager")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["similar_item"], RAMSTKSimilarItem)
        print("\033[36m\nsucceed_retrieve_similar_item topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_datamanager):
        """do_select_all() should clear nodes from an existing allocation
        tree."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_similar_item")

        test_datamanager.do_select_all(attributes={"revision_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_similar_item")


@pytest.mark.usefixtures("test_datamanager")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 4
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(node_id).data["similar_item"], RAMSTKSimilarItem
        )
        assert tree.get_node(node_id).data["similar_item"].revision_id == 1
        assert tree.get_node(node_id).data["similar_item"].hardware_id == 4
        assert tree.get_node(node_id).data["similar_item"].parent_id == 1
        print("\033[36m\nsucceed_insert_similar_item topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  "
            "Database returned:\n\tKey (fld_revision_id)=(40) is not present "
            'in table "ramstk_revision".'
        )
        print("\033[35m\nfail_insert_similar_item topic was broadcast.")

    def on_fail_insert_no_hardware(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_hardware_id)=(15) is not present in table "
            '"ramstk_hardware".'
        )

    @pytest.mark.integration
    def test_do_insert_sibling(self):
        """do_insert() should send the success message after successfully
        inserting a new sibling hardware assembly."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_similar_item")

        pub.sendMessage("request_insert_similar_item", hardware_id=4, parent_id=1)

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_similar_item")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_datamanager):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_similar_item")

        _revision_id = test_datamanager._revision_id

        test_datamanager._revision_id = 40
        pub.sendMessage("request_insert_similar_item", hardware_id=8, parent_id=0)

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_similar_item")

        test_datamanager._revision_id = _revision_id

    @pytest.mark.integration
    def test_do_insert_no_hardware(self):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_no_hardware, "fail_insert_similar_item")

        pub.sendMessage("request_insert_similar_item", hardware_id=15, parent_id=0)

        pub.unsubscribe(self.on_fail_insert_no_hardware, "fail_insert_similar_item")


@pytest.mark.usefixtures("test_datamanager")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_similar_item topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent similar item "
            "record with hardware ID 300."
        )
        print("\033[35m\nfail_delete_similar_item topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent similar item record "
            "with hardware ID 2."
        )
        print("\033[35m\nfail_delete_similar_item topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete(self, test_datamanager):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_similar_item")

        pub.sendMessage("request_delete_hardware", node_id=3)

        assert test_datamanager.tree.get_node(3) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_similar_item")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """_do_delete() should send the fail message."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_similar_item")

        pub.sendMessage("request_delete_hardware", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_similar_item")

    @pytest.mark.integration
    def test_do_delete_not_in_tree(self, test_datamanager):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_similar_item")

        test_datamanager.tree.remove_node(2)
        pub.sendMessage("request_delete_hardware", node_id=2)

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
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for similar item "
            "ID 1 was the wrong type."
        )
        print("\033[35m\nfail_update_similar_item topic was broadcast")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_similar_item topic was broadcast")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent similar item with "
            "similar item ID 100."
        )
        print("\033[35m\nfail_update_similar_item topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for " "similar item ID 1."
        )
        print("\033[35m\nfail_update_similar_item topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_datamanager):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_similar_item")

        _similar_item = test_datamanager.do_select(1, table="similar_item")
        _similar_item.change_description_1 = "This is a description of the change."
        pub.sendMessage("request_update_similar_item", node_id=2, table="similar_item")

        assert (
            test_datamanager.do_select(1, table="similar_item").change_description_1
            == "This is a description of the change."
        )

        pub.unsubscribe(self.on_succeed_update, "succeed_update_similar_item")

    @pytest.mark.integration
    def test_do_update_all(self):
        """do_update_all() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        pub.sendMessage("request_update_all_similar_items")

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_similar_item")

        _similar_item = test_datamanager.do_select(1, table="similar_item")
        _similar_item.change_factor_1 = {1: 2}

        pub.sendMessage("request_update_similar_item", node_id=1, table="similar_item")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_similar_item")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_similar_item"
        )

        _similar_item = test_datamanager.do_select(1, table="similar_item")
        _similar_item.change_factor_1 = {1: 2}

        pub.sendMessage("request_update_similar_item", node_id=0, table="similar_item")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_similar_item"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """do_update() should return a non-zero error code when passed a
        Allocation ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_similar_item")

        pub.sendMessage(
            "request_update_similar_item", node_id=100, table="similar_item"
        )

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_similar_item")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_datamanager):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that has no data package."""
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
        assert isinstance(tree.get_node(1).data["similar_item"], RAMSTKSimilarItem)
        print("\033[36m\nsucceed_get_similar_item_tree topic was broadcast.")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert (
            tree.get_node(1).data["similar_item"].change_description_1
            == "Testing set name from moduleview."
        )
        print("\033[36m\nsucceed_get_requirement_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self):
        """do_get_attributes() should return a dict of hardware attributes on
        success."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_similar_item_attributes"
        )

        pub.sendMessage(
            "request_get_similar_item_attributes", node_id=2, table="similar_item"
        )

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_similar_item_attributes"
        )

    @pytest.mark.skip
    def test_on_get_attributes(self, mock_program_dao, test_toml_user_configuration):
        """_get_all_attributes() should update the attributes dict on
        success."""
        DUT = amSimilarItem(test_toml_user_configuration)

        DATAMGR = dmSimilarItem()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={"revision_id": 1})
        DATAMGR.do_get_attributes(node_id=2, table="similar_item")

        assert DUT._attributes["hardware_id"] == 2
        assert DUT._attributes["change_description_1"] == ""
        assert DUT._attributes["change_description_2"] == ""
        assert DUT._attributes["change_factor_1"] == 1.0
        assert DUT._attributes["change_factor_1"] == 1.0

    @pytest.mark.integration
    def test_on_get_data_manager_tree(self):
        """_on_get_tree() should assign the data manager's tree to the _tree
        attribute in response to the succeed_get_hardware_tree message."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_similar_item_tree"
        )

        pub.sendMessage("request_get_similar_item_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_similar_item_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self):
        """do_set_attributes() should send the success message."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_similar_item_tree")

        pub.sendMessage(
            "request_set_similar_item_attributes",
            node_id=[1],
            package={"change_description_1": "Testing set name from moduleview."},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_similar_item_tree")


@pytest.mark.usefixtures("test_analysismanager", "test_datamanager")
class TestAnalysisMethods:
    """Class for similar item analysis methods test suite."""

    @pytest.mark.integration
    def test_on_select_hardware(self, test_analysismanager, test_datamanager):
        """_on_select_hardware() should assign the node hazard rate to the
        _node_hazard_rate attribute."""
        _tree = Tree()
        _tree.create_node(tag="hardwares", identifier=0, parent=None)

        _hardware = RAMSTKHardware()
        _hardware.hardware_id = 1
        _reliability = RAMSTKReliability()
        _reliability.hazard_rate_active = 0.00032
        _tree.create_node(
            tag="hardware",
            identifier=1,
            parent=0,
            data={
                "hardware": _hardware,
                "reliability": _reliability,
            },
        )

        _hardware = RAMSTKHardware()
        _hardware.hardware_id = 2
        _reliability = RAMSTKReliability()
        _reliability.hazard_rate_active = 0.00018
        _tree.create_node(
            tag="hardware",
            identifier=2,
            parent=1,
            data={
                "hardware": _hardware,
                "reliability": _reliability,
            },
        )

        _hardware = RAMSTKHardware()
        _hardware.hardware_id = 3
        _reliability = RAMSTKReliability()
        _reliability.hazard_rate_active = 0.00014
        _tree.create_node(
            tag="hardware",
            identifier=3,
            parent=1,
            data={
                "hardware": _hardware,
                "reliability": _reliability,
            },
        )

        pub.sendMessage("succeed_get_hardwares_tree", tree=_tree)

        assert test_analysismanager._dic_hardware_hrs[1] == 0.00032
        assert test_analysismanager._dic_hardware_hrs[2] == 0.00018
        assert test_analysismanager._dic_hardware_hrs[3] == 0.00014
