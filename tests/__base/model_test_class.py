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

        _record = unit_test_table_model.do_select(1)

        assert isinstance(_record, self._record)

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


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class UnitTestGetterSetterMethods:
    """Class for unit testing table model methods that get or set."""

    __test__ = False

    _id_columns = []

    _test_attr = None
    _test_default_value = None

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_record_model):
        """Should return None on success."""
        for _id in self._id_columns:
            test_attributes.pop(_id)

        assert test_record_model.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self,
        test_attributes,
        test_record_model,
    ):
        """Should set an attribute to its default value when passed a None value."""
        test_attributes[self._test_attr] = None
        for _id in self._id_columns:
            test_attributes.pop(_id)

        assert test_record_model.set_attributes(test_attributes) is None
        assert (
            test_record_model.get_attributes()[self._test_attr]
            == self._test_default_value
        )

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self,
        test_attributes,
        test_record_model,
    ):
        """Should raise an AttributeError when passed an unknown attribute."""
        for _id in self._id_columns:
            test_attributes.pop(_id)

        with pytest.raises(AttributeError):
            test_record_model.set_attributes({"shibboly-bibbly-boo": 0.9998})


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

        assert integration_test_table_model.last_id == self._next_id

        pub.unsubscribe(self.on_succeed_insert_sibling, f"succeed_insert_{self._tag}")

    @pytest.mark.integration
    def test_do_insert_child(self, test_attributes, integration_test_table_model):
        """Should add a record under parent to the record tree and update last_id."""
        pub.subscribe(self.on_succeed_insert_child, f"succeed_insert_{self._tag}")

        test_attributes["parent_id"] = 1
        self._next_id = integration_test_table_model.last_id + 1
        assert integration_test_table_model.tree.get_node(self._next_id) is None

        pub.sendMessage(f"request_insert_{self._tag}", attributes=test_attributes)

        assert integration_test_table_model.last_id == self._next_id

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
