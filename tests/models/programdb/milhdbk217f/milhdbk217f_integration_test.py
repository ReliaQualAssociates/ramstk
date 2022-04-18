# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.milhdbk217f.milhdbk217f_integration_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing MIL-HDBK-217F module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKMilHdbk217FRecord
from ramstk.models.dbtables import RAMSTKHardwareTable, RAMSTKMILHDBK217FTable


@pytest.fixture(scope="class")
def test_table_model(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKMILHDBK217FTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

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
    pub.unsubscribe(dut._do_update_tree, "succeed_delete_hardware")
    pub.unsubscribe(dut._do_update_tree, "succeed_insert_hardware")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_table_model")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["milhdbk217f"], RAMSTKMilHdbk217FRecord)
        print("\033[36m\n\tsucceed_retrieve_all_milhdbk217f topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_table_model):
        """should clear nodes from an existing records tree and re-populate."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_all_milhdbk217f")

        pub.sendMessage("selected_revision", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_all_milhdbk217f")


@pytest.mark.usefixtures("test_attributes", "test_table_model")
class TestInsertMethods:
    """Class for testing the insert() method."""

    def on_fail_insert_no_hardware(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_hardware_id)=(11) is not present in table "
            '"ramstk_hardware".'
        )
        print("\033[35m\n\tfail_insert_milhdbk217f topic was broadcast on no hardware.")

    @pytest.mark.integration
    def test_do_insert_sibling_assembly(
        self, test_attributes, test_table_model, test_hardware_table
    ):
        """should not add a record to the record tree and update last_id."""
        assert test_table_model.tree.get_node(9) is None

        pub.sendMessage(
            "request_insert_hardware",
            attributes={
                "revision_id": 1,
                "hardware_id": 9,
                "parent_id": 2,
                "part": 0,
            },
        )

        assert test_table_model.tree.get_node(9) is None

    @pytest.mark.integration
    def test_do_insert_part(
        self, test_attributes, test_table_model, test_hardware_table
    ):
        """should add a record to the record tree and update last_id."""
        assert test_table_model.tree.get_node(10) is None

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
            test_table_model.tree.get_node(10).data["milhdbk217f"],
            RAMSTKMilHdbk217FRecord,
        )
        assert test_table_model.tree.get_node(10).data["milhdbk217f"].revision_id == 1
        assert test_table_model.tree.get_node(10).data["milhdbk217f"].hardware_id == 10

    @pytest.mark.integration
    def test_do_insert_no_hardware(self, test_attributes, test_table_model):
        """should not add a record when passed a non-existent hardware ID."""
        pub.subscribe(self.on_fail_insert_no_hardware, "do_log_debug_msg")

        assert test_table_model.tree.get_node(11) is None

        test_attributes["hardware_id"] = 11
        test_attributes["parent_id"] = 1
        pub.sendMessage("request_insert_milhdbk217f", attributes=test_attributes)

        assert test_table_model.tree.get_node(11) is None

        pub.unsubscribe(self.on_fail_insert_no_hardware, "do_log_debug_msg")


@pytest.mark.usefixtures("test_table_model")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\n\tsucceed_delete_milhdbk217f topic was broadcast.")

    def on_fail_delete_non_existent_id(self, logger_name, message):
        assert logger_name == "DEBUG"
        try:
            assert message == "No data package for node ID 300 in module milhdbk217f."
        except AssertionError:
            assert message == "Attempted to delete non-existent Milhdbk217F ID 300."
            print(
                "\033[35m\n\tfail_delete_milhdbk217f topic was broadcast on "
                "non-existent ID."
            )

    def on_fail_delete_no_data_package(self, logger_name, message):
        assert logger_name == "DEBUG"
        # Two debug messages will be sent by two different methods under this scenario.
        try:
            assert message == "No data package for node ID 1 in module milhdbk217f."
            print(
                "\033[35m\n\tfail_delete_milhdbk217f topic was broadcast on no data "
                "package."
            )
        except AssertionError:
            assert message == "Attempted to delete non-existent Milhdbk217F ID 1."

    @pytest.mark.integration
    def test_do_delete(self, test_table_model):
        """should remove record from record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_milhdbk217f")

        _last_id = test_table_model.last_id
        pub.sendMessage("request_delete_milhdbk217f", node_id=_last_id)

        assert test_table_model.last_id == 1
        assert test_table_model.tree.get_node(_last_id) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_milhdbk217f")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """should send the fail message when passed a non-existent record ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "do_log_debug_msg")

        pub.sendMessage("request_delete_milhdbk217f", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_delete_no_data_package(self, test_table_model):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_delete_no_data_package, "do_log_debug_msg")

        test_table_model.tree.get_node(1).data.pop("milhdbk217f")
        pub.sendMessage("request_delete_milhdbk217f", node_id=1)

        pub.unsubscribe(self.on_fail_delete_no_data_package, "do_log_debug_msg")


@pytest.mark.usefixtures("test_table_model")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["milhdbk217f"].PiA == 5.0
        assert tree.get_node(2).data["milhdbk217f"].lambdaBD == 0.0045
        print("\033[36m\n\tsucceed_update_milhdbk217f topic was broadcast.")

    def on_succeed_update_all(self):
        print("\033[36m\n\tsucceed_update_all topic was broadcast for MIL-HDBK-217F.")

    def on_fail_update_wrong_data_type(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == (
            "The value for one or more attributes for milhdbk217f ID 1 was the wrong "
            "type."
        )
        print(
            "\033[35m\n\tfail_update_milhdbk217f topic was broadcast on wrong data "
            "type."
        )

    def on_fail_update_root_node_wrong_data_type(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == ("Attempting to update the root node 0.")
        print("\033[35m\n\tfail_update_milhdbk217f topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == (
            "Attempted to save non-existent milhdbk217f with milhdbk217f ID 100."
        )
        print(
            "\033[35m\n\tfail_update_milhdbk217f topic was broadcast on "
            "non-existent ID."
        )

    def on_fail_update_no_data_package(self, logger_name, message):
        assert logger_name == "DEBUG"
        assert message == ("No data package found for milhdbk217f ID 1.")
        print(
            "\033[35m\n\tfail_update_milhdbk217f topic was broadcast on no data "
            "package."
        )

    @pytest.mark.integration
    def test_do_update(self, test_table_model):
        """should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, "succeed_update_milhdbk217f")

        _milhdbk217f = test_table_model.do_select(1)
        _milhdbk217f.PiA = 5
        _milhdbk217f.lambdaBD = 0.0045
        pub.sendMessage("request_update_milhdbk217f", node_id=2)

        pub.unsubscribe(self.on_succeed_update, "succeed_update_milhdbk217f")

    @pytest.mark.integration
    def test_do_update_all(self, test_table_model):
        """should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all_milhdbk217f")

        _milhdbk217f = test_table_model.do_select(1)
        _milhdbk217f.PiA = 5.0
        _milhdbk217f.lambdaBD = 0.0045
        _milhdbk217f = test_table_model.do_select(8)
        _milhdbk217f.PiA = 1.2
        _milhdbk217f.lambdaBD = 0.0035

        pub.sendMessage("request_update_all_milhdbk217f")

        assert test_table_model.tree.get_node(1).data["milhdbk217f"].PiA == 5.0
        assert test_table_model.tree.get_node(1).data["milhdbk217f"].lambdaBD == 0.0045
        assert test_table_model.tree.get_node(8).data["milhdbk217f"].PiA == 1.2
        assert test_table_model.tree.get_node(8).data["milhdbk217f"].lambdaBD == 0.0035

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all_milhdbk217f")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_table_model):
        """should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

        _milhdbk217f = test_table_model.do_select(1)
        _milhdbk217f.lambdaBD = {1: 2}
        pub.sendMessage("request_update_milhdbk217f", node_id=1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_table_model):
        """should send the fail message when attempting to update the root node."""
        pub.subscribe(self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg")

        _milhdbk217f = test_table_model.do_select(1)
        _milhdbk217f.lambdaBD = {1: 2}
        pub.sendMessage("request_update_milhdbk217f", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """should send the fail message when updating a non-existent record ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

        pub.sendMessage("request_update_milhdbk217f", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_table_model):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")

        test_table_model.tree.get_node(1).data.pop("milhdbk217f")
        pub.sendMessage("request_update_milhdbk217f", node_id=1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")


@pytest.mark.usefixtures("test_table_model", "test_toml_user_configuration")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["hardware_id"] == 1
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

        print("\033[36m\n\tsucceed_get_milhdbk217f_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["milhdbk217f"], RAMSTKMilHdbk217FRecord)
        print("\033[36m\n\tsucceed_get_milhdbk217f_tree topic was broadcast.")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["milhdbk217f"].lambdaBD == 0.00655
        print("\033[36m\n\tsucceed_get_milhdbk217f_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_table_model):
        """should return the attribute dict."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_milhdbk217f_attributes"
        )

        test_table_model.do_get_attributes(node_id=1)

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
            node_id=1,
            package={"lambdaBD": 0.00655},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_milhdbk217f_tree")
