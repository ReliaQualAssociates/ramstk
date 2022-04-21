# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.__base.model_test_class.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test meta-classes for database record, table, and view models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class UnitTestSelectMethods:
    """Class for unit testing table model select() and select_all() methods."""

    __test__ = False

    _do_select_msg = ""
    _record = None
    _tag = ""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, unit_test_table_model):
        """Should return record tree populated with record models."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        assert isinstance(
            unit_test_table_model.tree.get_node(1).data[self._tag],
            self._record,
        )
        assert isinstance(
            unit_test_table_model.tree.get_node(2).data[self._tag],
            self._record,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, unit_test_table_model):
        """Should return the record for the requested ID."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _function = unit_test_table_model.do_select(1)

        assert isinstance(_function, self._record)

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, unit_test_table_model):
        """Should return None when a non-existent ID is requested."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        assert unit_test_table_model.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class UnitTestInsertMethods:
    """Class for unit testing the table model do_insert() method."""

    __test__ = False

    _next_id = 0
    _record = None
    _tag = ""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, unit_test_table_model):
        """Should add a record to the record tree and update last_id."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        self._next_id = unit_test_table_model.last_id + 1

        unit_test_table_model.do_insert(attributes=test_attributes)

        assert unit_test_table_model.last_id == self._next_id
        assert isinstance(
            unit_test_table_model.tree.get_node(self._next_id).data[self._tag],
            self._record,
        )

    @pytest.mark.unit
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should add a record to the record tree and update last_id."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        self._next_id = unit_test_table_model.last_id + 1

        test_attributes["parent_id"] = 2
        unit_test_table_model.do_insert(attributes=test_attributes)

        assert unit_test_table_model.last_id == self._next_id
        assert isinstance(
            unit_test_table_model.tree.get_node(self._next_id).data[self._tag],
            self._record,
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class UnitTestDeleteMethods:
    """Class for unit testing the table model do_delete() method."""

    __test__ = False

    _next_id = 0
    _record = None
    _tag = ""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, unit_test_table_model):
        """Should remove a record from the record tree and update last_id."""
        unit_test_table_model.do_select_all(attributes=test_attributes)

        _last_id = unit_test_table_model.last_id
        self._next_id = unit_test_table_model.last_id - 1

        unit_test_table_model.do_delete(unit_test_table_model.last_id)

        assert unit_test_table_model.last_id == self._next_id
        assert unit_test_table_model.tree.get_node(_last_id) is None


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class SystemTestSelectMethods:
    """Class for system testing table model select() and select_all() methods."""

    __test__ = False

    _do_select_msg = ""
    _record = None
    _tag = ""

    def on_succeed_select_all(self, tree):
        """Listen for succeed_retrieve_all messages."""
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data[f"{self._tag}"], self._record)
        print(f"\033[36m\n\tsucceed_retrieve_all_{self._tag} topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all_populated_tree(self, test_attributes):
        """Should clear and then re-populate the record tree."""
        pub.subscribe(self.on_succeed_select_all, f"succeed_retrieve_all_{self._tag}")

        pub.sendMessage(self._do_select_msg, attributes=test_attributes)

        pub.unsubscribe(self.on_succeed_select_all, f"succeed_retrieve_all_{self._tag}")


@pytest.mark.usefixtures("test_attributes", "integration_test_table_model")
class SystemTestInsertMethods:
    """Class for system testing table model do_insert() method."""

    __test__ = False

    _next_id = 0
    _record = None
    _tag = ""

    def on_succeed_insert_sibling(self, tree):
        """Listen for succeed_insert messages."""
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(self._next_id).data[self._tag], self._record)
        print(
            f"\033[36m\n\tsucceed_insert_{self._tag} topic was broadcast on insert "
            f"sibling."
        )

    def on_succeed_insert_child(self, tree):
        """Listen for succeed_insert messages."""
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(self._next_id).data[self._tag], self._record)
        print(
            f"\033[36m\n\tsucceed_insert_{self._tag} topic was broadcast on insert "
            f"child."
        )

    def on_fail_insert_no_parent(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == "Parent node '40' is not in the tree"
        print(f"\033[35m\n\tfail_insert_{self._tag} topic was broadcast on no parent.")

    def on_fail_insert_no_revision(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_revision_id)=(40) is not present in table "
            '"ramstk_revision".'
        )
        print(
            f"\033[35m\n\tfail_insert_{self._tag} topic was broadcast on no "
            f"revision."
        )

    @pytest.mark.integration
    def test_do_insert_sibling(self, test_attributes, integration_test_table_model):
        """Should add a record to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_sibling, f"succeed_insert_{self._tag}")

        self._next_id = integration_test_table_model.last_id + 1
        assert integration_test_table_model.tree.get_node(self._next_id) is None

        pub.sendMessage(f"request_insert_{self._tag}", attributes=test_attributes)

        # assert integration_test_table_model.last_id == self._next_id

        pub.unsubscribe(self.on_succeed_insert_sibling, f"succeed_insert_{self._tag}")

    @pytest.mark.integration
    def test_do_insert_child(self, test_attributes, integration_test_table_model):
        """Should add a record under parent to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_child, f"succeed_insert_{self._tag}")

        test_attributes["parent_id"] = 1
        self._next_id = integration_test_table_model.last_id + 1
        assert integration_test_table_model.tree.get_node(self._next_id) is None

        pub.sendMessage(f"request_insert_{self._tag}", attributes=test_attributes)

        # assert integration_test_table_model.last_id == self._next_id

        pub.unsubscribe(self.on_succeed_insert_child, f"succeed_insert_{self._tag}")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_attributes, integration_test_table_model):
        """Should send the do_log_debug message when parent ID does not existent."""
        pub.subscribe(self.on_fail_insert_no_parent, "do_log_debug_msg")

        self._next_id = integration_test_table_model.last_id + 1
        assert integration_test_table_model.tree.get_node(self._next_id) is None

        test_attributes["parent_id"] = 40
        pub.sendMessage(f"request_insert_{self._tag}", attributes=test_attributes)

        assert integration_test_table_model.tree.get_node(self._next_id) is None

        pub.unsubscribe(self.on_fail_insert_no_parent, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_attributes, integration_test_table_model):
        """Should send the fail message when the revision ID does not exist."""
        pub.subscribe(self.on_fail_insert_no_revision, "do_log_debug_msg")

        self._next_id = integration_test_table_model.last_id + 1
        assert integration_test_table_model.tree.get_node(self._next_id) is None

        test_attributes["revision_id"] = 40
        test_attributes["parent_id"] = 1
        pub.sendMessage(f"request_insert_{self._tag}", attributes=test_attributes)

        assert integration_test_table_model.tree.get_node(self._next_id) is None

        pub.unsubscribe(self.on_fail_insert_no_revision, "do_log_debug_msg")


@pytest.mark.usefixtures("integration_test_table_model")
class SystemTestDeleteMethods:
    """Class for system testing table model do_insert() method."""

    __test__ = False

    _next_id = 0
    _record = None
    _tag = ""

    def on_succeed_delete(self, tree):
        """Listen for succeed_delete messages."""
        assert isinstance(tree, Tree)
        assert tree.get_node(3) is None
        print(
            f"\033[36m\n\tsucceed_delete_{self._tag} topic was broadcast on delete "
            f"with no child."
        )

    def on_succeed_delete_with_child(self, tree):
        """Listen for succeed_delete messages."""
        assert isinstance(tree, Tree)
        assert tree.get_node(1) is None
        assert tree.get_node(2) is None
        print(
            f"\033[36m\n\tsucceed_delete_{self._tag} topic was broadcast on delete "
            f"with child."
        )

    def on_fail_delete_non_existent_id(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        try:
            assert message == f"No data package for node ID 300 in module {self._tag}."
        except AssertionError:
            assert (
                message == f"Attempted to delete non-existent {self._tag.title()} "
                f"ID 300."
            )
            print(
                f"\033[35m\n\tfail_delete_{self._tag} topic was broadcast on non "
                f"existent ID."
            )

    def on_fail_delete_not_in_tree(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        try:
            assert message == f"No data package for node ID 2 in module {self._tag}."
            print(
                f"\033[35m\n\tfail_delete_{self._tag} topic was broadcast on node not "
                f"in tree."
            )
        except AssertionError:
            assert (
                message == f"Attempted to delete non-existent {self._tag.title()} "
                f"ID 2."
            )

    @pytest.mark.integration
    def test_do_delete(self, integration_test_table_model):
        """Should remove a record from the record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete, f"succeed_delete_{self._tag}")

        _last_id = integration_test_table_model.last_id
        pub.sendMessage(f"request_delete_{self._tag}", node_id=_last_id)

        assert integration_test_table_model.last_id == 2
        assert integration_test_table_model.tree.get_node(_last_id) is None

        pub.unsubscribe(self.on_succeed_delete, f"succeed_delete_{self._tag}")

    @pytest.mark.integration
    def test_do_delete_with_child(self, integration_test_table_model):
        """Should remove a record and children from record tree and update last_id."""
        pub.subscribe(self.on_succeed_delete_with_child, f"succeed_delete_{self._tag}")

        pub.sendMessage(f"request_delete_{self._tag}", node_id=1)

        assert integration_test_table_model.tree.get_node(2) is None
        assert integration_test_table_model.tree.get_node(1) is None

        pub.unsubscribe(
            self.on_succeed_delete_with_child, f"succeed_delete_{self._tag}"
        )

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self):
        """Should send the fail message when the node ID does not exist."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "do_log_debug_msg")

        pub.sendMessage(f"request_delete_{self._tag}", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "do_log_debug_msg")


@pytest.mark.usefixtures("integration_test_table_model")
class SystemTestUpdateMethods:
    """Class for system testing table model do_update() and do_update_all() methods."""

    __test__ = False

    _next_id = 0
    _record = None
    _tag = ""

    def on_succeed_update(self, tree):
        """Listen for succeed_update messages."""
        assert isinstance(tree, Tree)
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
            f"The value for one or more attributes for {self._tag} ID 1 was the wrong "
            f"type."
        )
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on wrong data "
            f"type."
        )

    def on_fail_update_root_node_wrong_data_type(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == "Attempting to update the root node 0."
        print(f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on root node.")

    def on_fail_update_non_existent_id(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert (
            message == f"Attempted to save non-existent {self._tag} with {self._tag} "
            f"ID 100."
        )
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on non-existent "
            f"ID."
        )

    def on_fail_update_no_data_package(self, logger_name, message):
        """Listen for do_log_debug messages."""
        assert logger_name == "DEBUG"
        assert message == f"No data package found for {self._tag} ID 1."
        print(
            f"\033[35m\n\tfail_update_{self._tag} topic was broadcast on no data "
            f"package."
        )

    @pytest.mark.integration
    def test_do_update(self, integration_test_table_model):
        """Should update record attribute."""
        pub.subscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

        integration_test_table_model.tree.get_node(1).data[
            "function"
        ].name = "Test Function"
        pub.sendMessage(f"request_update_{self._tag}", node_id=1)

        pub.unsubscribe(self.on_succeed_update, f"succeed_update_{self._tag}")

    @pytest.mark.integration
    def test_do_update_all(self, integration_test_table_model):
        """Should update all the records in the database."""
        pub.subscribe(self.on_succeed_update_all, f"succeed_update_all_{self._tag}")

        _function = integration_test_table_model.do_select(1)
        _function.name = "Big test function #1"
        _function = integration_test_table_model.do_select(2)
        _function.name = "Big test function #2"

        pub.sendMessage(f"request_update_all_{self._tag}")

        assert (
            integration_test_table_model.tree.get_node(1).data["function"].name
            == "Big test function #1"
        )
        assert (
            integration_test_table_model.tree.get_node(2).data["function"].name
            == "Big test "
            "function #2"
        )

        pub.unsubscribe(self.on_succeed_update_all, f"succeed_update_all_{self._tag}")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, integration_test_table_model):
        """Should send the do_log_debug message with wrong attribute data type."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

        integration_test_table_model.tree.get_node(1).data["function"].name = {1: 1.56}
        pub.sendMessage(f"request_update_{self._tag}", node_id=1)

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_root_node_wrong_data_type(self, integration_test_table_model):
        """Should send the do_log_debug message with wrong attribute data type."""
        pub.subscribe(self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg")

        integration_test_table_model.tree.get_node(1).data["function"].name = {1: 1.56}
        pub.sendMessage(f"request_update_{self._tag}", node_id=0)

        pub.unsubscribe(
            self.on_fail_update_root_node_wrong_data_type, "do_log_debug_msg"
        )

    @pytest.mark.integration
    def test_do_update_non_existent_id(self):
        """Should send the do_log_debug message with non-existent ID tree."""
        pub.subscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

        pub.sendMessage(f"request_update_{self._tag}", node_id=100)

        pub.unsubscribe(self.on_fail_update_non_existent_id, "do_log_debug_msg")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, integration_test_table_model):
        """Should send the do_log_debug message with no data package in tree."""
        pub.subscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")

        integration_test_table_model.tree.get_node(1).data.pop(self._tag)
        pub.sendMessage(f"request_update_{self._tag}", node_id=1)

        pub.unsubscribe(self.on_fail_update_no_data_package, "do_log_debug_msg")


@pytest.mark.usefixtures("integration_test_table_model")
class SystemTestGetterSetterMethods:
    """Class for system testing table model getter and setter methods."""

    __test__ = False

    _package = {}
    _record = None
    _tag = ""
    _test_id = 0

    def on_succeed_get_attributes(self, attributes):
        """Listen for succeed_get_attribute messages."""
        assert isinstance(attributes, dict)
        print(f"\033[36m\n\tsucceed_get_{self._tag}_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        """Listen for succeed_get_tree messages."""
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(self._test_id).data[self._tag], self._record)
        print(f"\033[36m\n\tsucceed_get_{self._tag}_tree topic was broadcast")

    def on_succeed_set_attributes(self, tree):
        """Listen for succeed_set messages."""
        assert isinstance(tree, Tree)
        print(f"\033[36m\n\tsucceed_set_{self._tag}_attributes topic was broadcast")

    @pytest.mark.integration
    def test_do_get_attributes(self, integration_test_table_model):
        """Should return the attribute dict."""
        pub.subscribe(
            self.on_succeed_get_attributes,
            f"succeed_get_{self._tag}_attributes",
        )

        integration_test_table_model.do_get_attributes(node_id=self._test_id)

        pub.unsubscribe(
            self.on_succeed_get_attributes, f"succeed_get_{self._tag}_attributes"
        )

    @pytest.mark.integration
    def test_on_get_table_model_tree(self):
        """Should return the table model treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, f"succeed_get_{self._tag}_tree"
        )

        pub.sendMessage(f"request_{self._tag}_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, f"succeed_get_{self._tag}_tree"
        )

    @pytest.mark.integration
    def test_do_set_attributes(self, integration_test_table_model):
        """Should set the attribute and send the succeed_get_tree message."""
        pub.subscribe(self.on_succeed_set_attributes, f"succeed_get_{self._tag}_tree")

        pub.sendMessage(
            f"request_set_{self._tag}_attributes",
            node_id=self._test_id,
            package=self._package,
        )

        pub.unsubscribe(self.on_succeed_set_attributes, f"succeed_get_{self._tag}_tree")
