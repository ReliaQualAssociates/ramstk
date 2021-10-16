# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.nswc.nswc_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing NSWC module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKNSWCRecord, RAMSTKNSWCTable


@pytest.fixture(scope="class")
def test_tablemodel(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKNSWCTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_nswc_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_nswc_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_nswc")
    pub.unsubscribe(dut.do_set_tree, "succeed_calculate_nswc")
    pub.unsubscribe(dut.do_update, "request_update_nswc")
    pub.unsubscribe(dut.do_get_tree, "request_get_nswc_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_nswc")
    pub.unsubscribe(dut.do_insert, "request_insert_nswc")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["nswc"], RAMSTKNSWCRecord)
        print("\033[36m\nsucceed_retrieve_nswc topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_tablemodel):
        """should clear nodes from an existing records tree and re-populate."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_nswc")

        pub.sendMessage("selected_revision", attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_nswc")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the insert() method."""

    def on_succeed_insert_sibling(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(8).data["nswc"], RAMSTKNSWCRecord)
        assert tree.get_node(8).data["nswc"].hardware_id == 8
        print("\033[36m\nsucceed_insert_nswc topic was broadcast.")

    def on_fail_insert_no_hardware(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_hardware_id)=(9) is not present in table "
            '"ramstk_hardware".'
        )
        print("\033[35m\nfail_insert_nswc topic was broadcast on no hardware.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a record to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_nswc")

        assert test_tablemodel.tree.get_node(8) is None

        test_attributes["hardware_id"] = 8
        pub.sendMessage("request_insert_nswc", attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(8).data["nswc"],
            RAMSTKNSWCRecord,
        )

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_nswc")

    @pytest.mark.integration
    def test_do_insert_no_hardware(self, test_attributes, test_tablemodel):
        """should not add a record when passed a non-existent hardware ID."""
        pub.subscribe(self.on_fail_insert_no_hardware, "fail_insert_nswc")

        assert test_tablemodel.tree.get_node(9) is None

        test_attributes["hardware_id"] = 9
        pub.sendMessage("request_insert_nswc", attributes=test_attributes)

        assert test_tablemodel.tree.get_node(9) is None

        pub.unsubscribe(self.on_fail_insert_no_hardware, "fail_insert_nswc")


@pytest.mark.usefixtures("test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_nswc topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Nswc ID 300.")
        print("\033[35m\nfail_delete_nswc topic was broadcast on non-existent ID.")

    def on_fail_delete_no_data_package(self, error_message):
        assert error_message == ("Attempted to delete non-existent Nswc ID 2.")
        print("\033[35m\nfail_delete_nswc topic was broadcast on no data package.")

    @pytest.mark.integration
    def test_do_delete(self, test_tablemodel):
        """should remove record from record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_nswc")

        _last_id = test_tablemodel.last_id
        pub.sendMessage("request_delete_nswc", node_id=_last_id)

        assert test_tablemodel.last_id == 6
        assert test_tablemodel.tree.get_node(_last_id) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_nswc")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """should send the fail message when passed a non-existent record ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_nswc")

        pub.sendMessage("request_delete_nswc", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_nswc")

    @pytest.mark.integration
    def test_do_delete_no_data_package(self, test_tablemodel):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_delete_no_data_package, "fail_delete_nswc")

        test_tablemodel.tree.get_node(2).data.pop("nswc")
        pub.sendMessage("request_delete_nswc", node_id=2)

        pub.unsubscribe(self.on_fail_delete_no_data_package, "fail_delete_nswc")


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["nswc"].parent_id == 1
        assert tree.get_node(2).data["nswc"].Cac == 5
        assert tree.get_node(2).data["nswc"].Calt == 81
        print("\033[36m\nsucceed_update_nswc topic was broadcast.")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast for NSWC.")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for nswc "
            "ID 1 was the wrong type."
        )
        print("\033[35m\nfail_update_nswc topic was broadcast on wrong data type.")

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_nswc topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent nswc with nswc ID 100."
        )
        print("\033[35m\nfail_update_nswc topic was broadcast on non-existent ID.")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for nswc ID 1.")
        print("\033[35m\nfail_update_nswc topic was broadcast on no data package.")

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, "succeed_update_nswc")

        _nswc = test_tablemodel.do_select(2)
        _nswc.Cac = 5
        _nswc.Calt = 81
        pub.sendMessage("request_update_nswc", node_id=2, table="nswc")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_nswc")

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        _nswc = test_tablemodel.do_select(1)
        _nswc.Cac = 5
        _nswc.Calt = 81
        _nswc = test_tablemodel.do_select(2)
        _nswc.Cac = 12
        _nswc.Calt = 71

        pub.sendMessage("request_update_all_nswc")

        assert test_tablemodel.tree.get_node(1).data["nswc"].Cac == 5
        assert test_tablemodel.tree.get_node(1).data["nswc"].Calt == 81
        assert test_tablemodel.tree.get_node(2).data["nswc"].Cac == 12
        assert test_tablemodel.tree.get_node(2).data["nswc"].Calt == 71

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_nswc")

        _nswc = test_tablemodel.do_select(1)
        _nswc.Cac = {1: 2}
        pub.sendMessage("request_update_nswc", node_id=1, table="nswc")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_nswc")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """should send the fail message when attempting to update the root node."""
        pub.subscribe(self.on_fail_update_root_node_wrong_data_type, "fail_update_nswc")

        _nswc = test_tablemodel.do_select(1)
        _nswc.Calt = {1: 2}
        pub.sendMessage("request_update_nswc", node_id=0, table="nswc")

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_nswc"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """should send the fail message when updating a non-existent record ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_nswc")

        pub.sendMessage("request_update_nswc", node_id=100, table="nswc")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_nswc")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_nswc")

        test_tablemodel.tree.get_node(1).data.pop("nswc")
        pub.sendMessage("request_update_nswc", node_id=1, table="nswc")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_nswc")


@pytest.mark.usefixtures("test_tablemodel", "test_toml_user_configuration")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["hardware_id"] == 2
        assert attributes["Cac"] == 0.0
        assert attributes["Calt"] == 0.0
        assert attributes["Cb"] == 0.0
        assert attributes["Cbl"] == 0.0
        assert attributes["Cbt"] == 0.0
        assert attributes["Cbv"] == 0.0
        assert attributes["Cc"] == 0.0
        assert attributes["Ccf"] == 0.0
        assert attributes["Ccp"] == 0.0
        assert attributes["Ccs"] == 0.0
        assert attributes["Ccv"] == 0.0
        assert attributes["Ccw"] == 0.0
        assert attributes["Cd"] == 0.0
        assert attributes["Cdc"] == 0.0
        assert attributes["Cdl"] == 0.0
        assert attributes["Cdp"] == 0.0
        assert attributes["Cds"] == 0.0
        assert attributes["Cdt"] == 0.0
        assert attributes["Cdw"] == 0.0
        assert attributes["Cdy"] == 0.0
        assert attributes["Ce"] == 0.0
        assert attributes["Cf"] == 0.0
        assert attributes["Cg"] == 0.0
        assert attributes["Cga"] == 0.0
        assert attributes["Cgl"] == 0.0
        assert attributes["Cgp"] == 0.0
        assert attributes["Cgs"] == 0.0
        assert attributes["Cgt"] == 0.0
        assert attributes["Cgv"] == 0.0
        assert attributes["Ch"] == 0.0
        assert attributes["Ci"] == 0.0
        assert attributes["Ck"] == 0.0
        assert attributes["Cl"] == 0.0
        assert attributes["Clc"] == 0.0
        assert attributes["Cm"] == 0.0
        assert attributes["Cmu"] == 0.0
        assert attributes["Cn"] == 0.0
        assert attributes["Cnp"] == 0.0
        assert attributes["Cnw"] == 0.0
        assert attributes["Cp"] == 0.0
        assert attributes["Cpd"] == 0.0
        assert attributes["Cpf"] == 0.0
        assert attributes["Cpv"] == 0.0
        assert attributes["Cq"] == 0.0
        assert attributes["Cr"] == 0.0
        assert attributes["Crd"] == 0.0
        assert attributes["Cs"] == 0.0
        assert attributes["Csc"] == 0.0
        assert attributes["Csf"] == 0.0
        assert attributes["Cst"] == 0.0
        assert attributes["Csv"] == 0.0
        assert attributes["Csw"] == 0.0
        assert attributes["Csz"] == 0.0
        assert attributes["Ct"] == 0.0
        assert attributes["Cv"] == 0.0
        assert attributes["Cw"] == 0.0
        assert attributes["Cy"] == 0.0

        print("\033[36m\nsucceed_get_nswc_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["nswc"], RAMSTKNSWCRecord)
        print("\033[36m\nsucceed_get_nswc_tree topic was broadcast.")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data["nswc"].Cac == 65.5
        print("\033[36m\nsucceed_get_nswc_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, test_tablemodel):
        """should return the attributes dict."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_nswc_attributes")

        test_tablemodel.do_get_attributes(
            node_id=2,
            table="nswc",
        )

        pub.unsubscribe(self.on_succeed_get_attributes, "succeed_get_nswc_attributes")

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self):
        """should return the records tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_nswc_tree")

        pub.sendMessage("request_get_nswc_tree")

        pub.unsubscribe(self.on_succeed_get_data_manager_tree, "succeed_get_nswc_tree")

    @pytest.mark.integration
    def test_do_set_attributes(self):
        """should set the value of the attribute requested."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_nswc_tree")

        pub.sendMessage(
            "request_set_nswc_attributes",
            node_id=[2],
            package={"Cac": 65.5},
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_nswc_tree")
