# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.milhdbk217f.milhdbk217f_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing MIL-HDBK-217F module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKMilHdbk217FRecord, RAMSTKMILHDBK217FTable


@pytest.fixture(scope="class")
def test_tablemodel(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMILHDBK217FTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_milhdbk217f_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_milhdbk217f_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_milhdbk217f")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_milhdbk217f")
    pub.unsubscribe(dut.do_update, "request_update_milhdbk217f")
    pub.unsubscribe(dut.do_get_tree, "request_get_milhdbk217f_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_milhdbk217f")
    pub.unsubscribe(dut.do_insert, "request_insert_milhdbk217f")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["milhdbk217f"], RAMSTKMilHdbkFRecord)
        print("\033[36m\nsucceed_retrieve_milhdbk217f topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_tablemodel):
        """should clear nodes from an existing records tree and re-populate."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_milhdbk217f")

        pub.sendMessage("selected_revision", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_milhdbk217f")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the insert() method."""

    def on_succeed_insert_sibling(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(8).data["milhdbk217f"], RAMSTKMilHdbk217FRecord)
        assert tree.get_node(8).data["milhdbk217f"].hardware_id == 8
        print("\033[36m\nsucceed_insert_milhdbk217f topic was broadcast.")

    def on_fail_insert_no_hardware(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_hardware_id)=(9) is not present in table "
            '"ramstk_hardware".'
        )
        print("\033[35m\nfail_insert_milhdbk217f topic was broadcast on no hardware.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a record to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_milhdbk217f")

        assert test_tablemodel.tree.get_node(8) is None

        test_attributes["hardware_id"] = 8
        test_attributes["parent_id"] = 1
        test_attributes["record_id"] = 8
        pub.sendMessage("request_insert_milhdbk217f", attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(8).data["milhdbk217f"],
            RAMSTKMilHdbk217FRecord,
        )

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_milhdbk217f")

    @pytest.mark.integration
    def test_do_insert_no_hardware(self, test_attributes, test_tablemodel):
        """should not add a record when passed a non-existent hardware ID."""
        pub.subscribe(self.on_fail_insert_no_hardware, "fail_insert_milhdbk217f")

        assert test_tablemodel.tree.get_node(9) is None

        test_attributes["hardware_id"] = 9
        test_attributes["parent_id"] = 1
        test_attributes["record_id"] = 9
        pub.sendMessage("request_insert_milhdbk217f", attributes=test_attributes)

        assert test_tablemodel.tree.get_node(9) is None

        pub.unsubscribe(self.on_fail_insert_no_hardware, "fail_insert_milhdbk217f")


@pytest.mark.usefixtures("test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_milhdbk217f topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Milhdbk217F ID 300.")
        print(
            "\033[35m\nfail_delete_milhdbk217f topic was broadcast on non-existent "
            "ID."
        )

    def on_fail_delete_no_data_package(self, error_message):
        assert error_message == ("Attempted to delete non-existent Milhdbk217F ID 2.")
        print(
            "\033[35m\nfail_delete_milhdbk217f topic was broadcast on no data "
            "package."
        )

    @pytest.mark.integration
    def test_do_delete(self, test_tablemodel):
        """should remove record from record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_milhdbk217f")

        _last_id = test_tablemodel.last_id
        pub.sendMessage("request_delete_milhdbk217f", node_id=_last_id)

        assert test_tablemodel.last_id == 6
        assert test_tablemodel.tree.get_node(_last_id) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_milhdbk217f")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """should send the fail message when passed a non-existent record ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_milhdbk217f")

        pub.sendMessage("request_delete_milhdbk217f", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_milhdbk217f")

    @pytest.mark.integration
    def test_do_delete_no_data_package(self, test_tablemodel):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_delete_no_data_package, "fail_delete_milhdbk217f")

        test_tablemodel.tree.get_node(2).data.pop("milhdbk217f")
        pub.sendMessage("request_delete_milhdbk217f", node_id=2)

        pub.unsubscribe(self.on_fail_delete_no_data_package, "fail_delete_milhdbk217f")


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["milhdbk217f"].PiA == 5.0
        assert tree.get_node(2).data["milhdbk217f"].lambdaBD == 0.0045
        print("\033[36m\nsucceed_update_milhdbk217f topic was broadcast.")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast for MIL-HDBK-217F.")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for milhdbk217f "
            "ID 1 was the wrong type."
        )
        print(
            "\033[35m\nfail_update_milhdbk217f topic was broadcast on wrong data "
            "type."
        )

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_milhdbk217f topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent milhdbk217f with "
            "milhdbk217f ID 100."
        )
        print(
            "\033[35m\nfail_update_milhdbk217f topic was broadcast on "
            "non-existent ID."
        )

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for milhdbk217f ID 1."
        )
        print(
            "\033[35m\nfail_update_milhdbk217f topic was broadcast on no data "
            "package."
        )

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, "succeed_update_milhdbk217f")

        _milhdbk217f = test_tablemodel.do_select(2)
        _milhdbk217f.PiA = 5
        _milhdbk217f.lambdaBD = 0.0045
        pub.sendMessage("request_update_milhdbk217f", node_id=2)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_milhdbk217f")

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        _milhdbk217f = test_tablemodel.do_select(1)
        _milhdbk217f.PiA = 5.0
        _milhdbk217f.lambdaBD = 0.0045
        _milhdbk217f = test_tablemodel.do_select(2)
        _milhdbk217f.PiA = 1.2
        _milhdbk217f.lambdaBD = 0.0035

        pub.sendMessage("request_update_all_milhdbk217f")

        assert test_tablemodel.tree.get_node(1).data["milhdbk217f"].PiA == 5.0
        assert test_tablemodel.tree.get_node(1).data["milhdbk217f"].lambdaBD == 0.0045
        assert test_tablemodel.tree.get_node(2).data["milhdbk217f"].PiA == 1.2
        assert test_tablemodel.tree.get_node(2).data["milhdbk217f"].lambdaBD == 0.0035

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_milhdbk217f")

        _milhdbk217f = test_tablemodel.do_select(1)
        _milhdbk217f.lambdaBD = {1: 2}
        pub.sendMessage("request_update_milhdbk217f", node_id=1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_milhdbk217f")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """should send the fail message when attempting to update the root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_milhdbk217f"
        )

        _milhdbk217f = test_tablemodel.do_select(1)
        _milhdbk217f.lambdaBD = {1: 2}
        pub.sendMessage("request_update_milhdbk217f", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_milhdbk217f"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """should send the fail message when updating a non-existent record ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_milhdbk217f")

        pub.sendMessage("request_update_milhdbk217f", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_milhdbk217f")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_milhdbk217f")

        test_tablemodel.tree.get_node(1).data.pop("milhdbk217f")
        pub.sendMessage("request_update_milhdbk217f", node_id=1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_milhdbk217f")


@pytest.mark.usefixtures("test_tablemodel", "test_toml_user_configuration")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["hardware_id"] == 2
        assert attributes["A1"] == 0.0
        assert attributes["A2"] == 0.0
        assert attributes["B1"] == 0.0
        assert attributes["B2"] == 0.0
        assert attributes["C1"] == 0.0
        assert attributes["C2"] == 0.0
        assert attributes["lambdaBD"] == 0.0
        assert attributes["lambdaBP"] == 0.0
        assert attributes["lambdaCYC"] == 0.0
        assert attributes["lambdaEOS"] == 0.0
        assert attributes["piA"] == 0.0
        assert attributes["piC"] == 0.0
        assert attributes["piCD"] == 0.0
        assert attributes["piCF"] == 0.0
        assert attributes["piCR"] == 0.0
        assert attributes["piCV"] == 0.0
        assert attributes["piCYC"] == 0.0
        assert attributes["piE"] == 0.0
        assert attributes["piF"] == 0.0
        assert attributes["piI"] == 0.0
        assert attributes["piK"] == 0.0
        assert attributes["piL"] == 0.0
        assert attributes["piM"] == 0.0
        assert attributes["piMFG"] == 0.0
        assert attributes["piN"] == 0.0
        assert attributes["piNR"] == 0.0
        assert attributes["piP"] == 0.0
        assert attributes["piPT"] == 0.0
        assert attributes["piQ"] == 0.0
        assert attributes["piR"] == 0.0
        assert attributes["piS"] == 0.0
        assert attributes["piT"] == 0.0
        assert attributes["piTAPS"] == 0.0
        assert attributes["piU"] == 0.0
        assert attributes["piV"] == 0.0

        print("\033[36m\nsucceed_get_milhdbk217f_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["milhdbk217f"], RAMSTKMilHdbk217FRecord)
        print("\033[36m\nsucceed_get_milhdbk217f_tree topic was broadcast.")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["milhdbk217f"].lambdaBD == 0.00655
        print("\033[36m\nsucceed_get_milhdbk217f_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_tablemodel):
        """should return the attributes dict."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_milhdbk217f_attributes"
        )

        test_tablemodel.do_get_attributes(
            node_id=2,
            table="milhdbk217f",
        )

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_milhdbk217f_attributes"
        )

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self):
        """should return the records tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_milhdbk217f_tree"
        )

        pub.sendMessage("request_get_milhdbk217f_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_milhdbk217f_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self):
        """should set the value of the attribute requested."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_milhdbk217f_tree")

        pub.sendMessage(
            "request_set_milhdbk217f_attributes",
            node_id=2,
            package={"lambdaBD": 0.00655},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_milhdbk217f_tree")
