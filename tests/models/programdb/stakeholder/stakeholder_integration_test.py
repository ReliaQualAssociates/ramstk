# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.stakeholder.stakeholder_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Stakeholder module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models import RAMSTKStakeholderRecord, RAMSTKStakeholderTable


@pytest.fixture(scope="class")
def test_tablemodel(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKStakeholderTable()
    dut.do_connect(test_program_dao)
    dut.do_select_all(attributes={"revision_id": 1})

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_stakeholder_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_stakeholder_attributes")
    pub.unsubscribe(dut.do_set_attributes, "lvw_editing_stakeholder")
    pub.unsubscribe(dut.do_update, "request_update_stakeholder")
    pub.unsubscribe(dut.do_get_tree, "request_get_stakeholder_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_stakeholder")
    pub.unsubscribe(dut.do_insert, "request_insert_stakeholder")
    pub.unsubscribe(dut.do_calculate_stakeholder, "request_calculate_stakeholder")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data, dict)
        assert isinstance(tree.get_node(1).data["stakeholder"], RAMSTKStakeholderRecord)
        print("\033[36m\nsucceed_retrieve_stakeholders topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes, test_tablemodel):
        """should clear nodes from an existing records tree and re-populate."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_stakeholders")

        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(
            test_tablemodel.tree.get_node(1).data["stakeholder"],
            RAMSTKStakeholderRecord,
        )

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_stakeholders")


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the insert() method."""

    def on_succeed_insert_sibling(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(3).data["stakeholder"], RAMSTKStakeholderRecord)
        assert tree.get_node(3).data["stakeholder"].stakeholder_id == 3
        assert tree.get_node(3).data["stakeholder"].description == "Stakeholder Input"
        print("\033[36m\nsucceed_insert_stakeholder topic was broadcast")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  "
            "Database returned:\n\tKey (fld_revision_id)=(40) is not present "
            'in table "ramstk_revision".'
        )
        print("\033[35m\nfail_insert_stakeholder topic was broadcast on no revision.")

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add a record to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_stakeholder")

        assert test_tablemodel.tree.get_node(3) is None

        pub.sendMessage("request_insert_stakeholder", attributes=test_attributes)

        assert test_tablemodel.last_id == 3

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_stakeholder")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_attributes, test_tablemodel):
        """should not add a record when passed a non-existent revision ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_stakeholder")

        test_attributes["revision_id"] = 40
        pub.sendMessage("request_insert_stakeholder", attributes=test_attributes)

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_stakeholder")


@pytest.mark.usefixtures("test_tablemodel")
class TestDeleteMethods:
    """Class for testing the delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_stakeholder topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == ("Attempted to delete non-existent Stakeholder ID 300.")
        print(
            "\033[35m\nfail_delete_stakeholder topic was broadcast on non-existent "
            "ID."
        )

    def on_fail_delete_no_data_package(self, error_message):
        assert error_message == ("Attempted to delete non-existent Stakeholder ID 1.")
        print(
            "\033[35m\nfail_delete_stakeholder topic was broadcast on no data package."
        )

    @pytest.mark.integration
    def test_do_delete(self, test_tablemodel):
        """should remove record from record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_stakeholder")

        pub.sendMessage("request_delete_stakeholder", node_id=test_tablemodel.last_id)

        assert test_tablemodel.last_id == 1
        assert test_tablemodel.tree.get_node(2) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_stakeholder")

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self, test_tablemodel):
        """should send the fail message when passed a non-existent record ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_stakeholder")

        pub.sendMessage("request_delete_stakeholder", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_stakeholder")

    @pytest.mark.integration
    def test_do_delete_no_data_package(self, test_tablemodel):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_delete_no_data_package, "fail_delete_stakeholder")

        test_tablemodel.tree.get_node(1).data.pop("stakeholder")
        pub.sendMessage("request_delete_stakeholder", node_id=1)

        pub.unsubscribe(self.on_fail_delete_no_data_package, "fail_delete_stakeholder")


@pytest.mark.usefixtures("test_tablemodel")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["stakeholder"].description == ("Test Stakeholder")
        print("\033[36m\nsucceed_update_stakeholder topic was broadcast")

    def on_succeed_update_all(self):
        print("\033[36m\nsucceed_update_all topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for stakeholder ID 1 was "
            "the wrong type."
        )
        print(
            "\033[35m\nfail_update_stakeholder topic was broadcast on wrong data "
            "type."
        )

    def on_fail_update_root_node_wrong_data_type(self, error_message):
        assert error_message == ("do_update: Attempting to update the root node 0.")
        print("\033[35m\nfail_update_stakeholder topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent stakeholder with stakeholder ID "
            "100."
        )
        print(
            "\033[35m\nfail_update_stakeholder topic was broadcast on non-existent ID."
        )

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for stakeholder ID 1."
        )
        print(
            "\033[35m\nfail_update_stakeholder topic was broadcast on no data package."
        )

    @pytest.mark.integration
    def test_do_update(self, test_tablemodel):
        """should update the attribute value for record ID."""
        pub.subscribe(self.on_succeed_update, "succeed_update_stakeholder")

        test_tablemodel.tree.get_node(1).data[
            "stakeholder"
        ].description = "Test Stakeholder"
        pub.sendMessage("request_update_stakeholder", node_id=1)

        assert (
            test_tablemodel.tree.get_node(1).data["stakeholder"].description
            == "Test Stakeholder"
        )

        pub.unsubscribe(self.on_succeed_update, "succeed_update_stakeholder")

    @pytest.mark.integration
    def test_do_update_all(self, test_tablemodel):
        """should update all records in the records tree."""
        pub.subscribe(self.on_succeed_update_all, "succeed_update_all")

        test_tablemodel.tree.get_node(1).data[
            "stakeholder"
        ].description = "Test Stakeholder 2"

        pub.sendMessage("request_update_all_stakeholder")

        assert (
            test_tablemodel.tree.get_node(1).data["stakeholder"].description
            == "Test Stakeholder 2"
        )

        pub.unsubscribe(self.on_succeed_update_all, "succeed_update_all")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_tablemodel):
        """should send the fail message when the wrong data type is assigned."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_stakeholder")

        _stakeholder = test_tablemodel.do_select(1)
        _stakeholder.user_float_1 = {1: 2}
        pub.sendMessage("request_update_stakeholder", node_id=1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_stakeholder")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, test_tablemodel):
        """should send the fail message when attempting to update the root node."""
        pub.subscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_stakeholder"
        )

        _stakeholder = test_tablemodel.do_select(1)
        _stakeholder.user_float_1 = {1: 2}

        pub.sendMessage("request_update_stakeholder", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "fail_update_stakeholder"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """should send the fail message when updating a non-existent record ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_stakeholder")

        pub.sendMessage("request_update_stakeholder", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_stakeholder")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_tablemodel):
        """should send the fail message when the record ID has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_stakeholder")

        test_tablemodel.tree.get_node(1).data.pop("stakeholder")
        pub.sendMessage("request_update_stakeholder", node_id=1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_stakeholder")


@pytest.mark.usefixtures("test_tablemodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["stakeholder_id"] == 1
        assert attributes["description"] == "Test Stakeholder Input"
        assert attributes["priority"] == 1
        print("\033[36m\nsucceed_get_stakeholder_attributes topic was broadcast")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data, dict)
        assert isinstance(tree.get_node(1).data["stakeholder"], RAMSTKStakeholderRecord)
        print("\033[36m\nsucceed_get_stakeholder_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        assert isinstance(tree, Tree)
        assert (
            tree.get_node(1).data["stakeholder"].description
            == "Testing set description from moduleview."
        )
        print("\033[36m\nsucceed_get_stakeholder_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self):
        """should return the attributes dict."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_stakeholder_attributes"
        )

        pub.sendMessage(
            "request_get_stakeholder_attributes", node_id=1, table="stakeholder"
        )

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_stakeholder_attributes"
        )

    @pytest.mark.integration
    def test_on_get_tree(self):
        """should return the records tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_stakeholder_tree"
        )

        pub.sendMessage("request_get_stakeholder_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_stakeholder_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, test_tablemodel):
        """should set the value of the attribute requested."""
        pub.subscribe(self.on_succeed_set_attributes, "succeed_get_stakeholder_tree")

        pub.sendMessage(
            "request_set_stakeholder_attributes",
            node_id=1,
            package={"description": "Testing set description from moduleview."},
        )

        assert (
            test_tablemodel.tree.get_node(1).data["stakeholder"].description
            == "Testing set description from moduleview."
        )

        pub.unsubscribe(self.on_succeed_set_attributes, "succeed_get_stakeholder_tree")


@pytest.mark.usefixtures("test_tablemodel")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    def on_succeed_calculate_stakeholder(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data, dict)
        assert tree.get_node(1).data["improvement"] == 1.2
        assert tree.get_node(1).data["overall_weight"] == 12.48
        print("\033[36m\nsucceed_calculate_stakeholder topic was broadcast.")

    @pytest.mark.integration
    def test_do_calculate_stakeholder(self, test_tablemodel):
        """should calculate the record's improvement factor and overall weight."""
        pub.subscribe(
            self.on_succeed_calculate_stakeholder, "succeed_calculate_stakeholder2"
        )

        _stakeholder = test_tablemodel.do_select(1)
        _stakeholder.planned_rank = 3
        _stakeholder.customer_rank = 2
        _stakeholder.priority = 4
        _stakeholder.user_float_1 = 2.6
        test_tablemodel.do_update(1)

        pub.sendMessage("request_calculate_stakeholder", node_id=1)

        _attributes = test_tablemodel.do_select(1).get_attributes()
        assert _attributes["improvement"] == 1.2
        assert _attributes["overall_weight"] == 12.48

        pub.unsubscribe(
            self.on_succeed_calculate_stakeholder, "succeed_calculate_stakeholder2"
        )
