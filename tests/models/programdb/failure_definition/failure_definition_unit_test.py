# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.failure_definition.failure_definition.unit_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing failure definition module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKFailureDefinitionRecord
from ramstk.models.dbtables import RAMSTKFailureDefinitionTable


@pytest.fixture(scope="function")
def test_tablemodel(mock_program_dao):
    """Get a data manager instance for each test function."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKFailureDefinitionTable()
    dut.do_connect(mock_program_dao)

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_get_attributes, "request_get_definition_attributes")
    pub.unsubscribe(dut.do_set_attributes, "request_set_definition_attributes")
    pub.unsubscribe(dut.do_set_attributes, "wvw_editing_definition")
    pub.unsubscribe(dut.do_update, "request_update_definition")
    pub.unsubscribe(dut.do_get_tree, "request_get_definition_tree")
    pub.unsubscribe(dut.do_select_all, "selected_revision")
    pub.unsubscribe(dut.do_delete, "request_delete_definition")
    pub.unsubscribe(dut.do_insert, "request_insert_definition")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures("test_recordmodel", "test_tablemodel")
class TestCreateModels:
    """Class for model initialization test suite."""

    @pytest.mark.unit
    def test_record_model_create(self, test_recordmodel):
        """should return a record model instance."""
        assert isinstance(test_recordmodel, RAMSTKFailureDefinitionRecord)

        # Verify class attributes are properly initialized.
        assert test_recordmodel.__tablename__ == "ramstk_failure_definition"
        assert test_recordmodel.revision_id == 1
        assert test_recordmodel.function_id == 1
        assert test_recordmodel.definition_id == 1
        assert test_recordmodel.definition == "Mock Failure Definition 1"

    @pytest.mark.unit
    def test_table_model_create(self, test_tablemodel):
        """__init__() should return a Revision data manager."""
        assert isinstance(test_tablemodel, RAMSTKFailureDefinitionTable)
        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(test_tablemodel.dao, MockDAO)
        assert test_tablemodel._db_id_colname == "fld_definition_id"
        assert test_tablemodel._db_tablename == "ramstk_failure_definition"
        assert test_tablemodel._tag == "definition"
        assert test_tablemodel._root == 0
        assert test_tablemodel._revision_id == 0
        assert pub.isSubscribed(
            test_tablemodel.do_get_attributes,
            "request_get_definition_attributes",
        )
        assert pub.isSubscribed(test_tablemodel.do_select_all, "selected_revision")
        assert pub.isSubscribed(test_tablemodel.do_update, "request_update_definition")
        assert pub.isSubscribed(
            test_tablemodel.do_update_all, "request_update_all_definition"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_get_tree, "request_get_definition_tree"
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes,
            "request_set_definition_attributes",
        )
        assert pub.isSubscribed(
            test_tablemodel.do_set_attributes, "wvw_editing_definition"
        )
        assert pub.isSubscribed(test_tablemodel.do_delete, "request_delete_definition")
        assert pub.isSubscribed(
            test_tablemodel.do_insert,
            "request_insert_definition",
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    @pytest.mark.unit
    def test_do_select_all(self, test_attributes, test_tablemodel):
        """do_select_all() should return a Tree() object populated with
        RAMSTKFailureDefinition instances on success."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert isinstance(test_tablemodel.tree, Tree)
        assert isinstance(
            test_tablemodel.tree.get_node(1).data["definition"],
            RAMSTKFailureDefinitionRecord,
        )

    @pytest.mark.unit
    def test_do_select(self, test_attributes, test_tablemodel):
        """do_select() should return an instance of RAMSTKFailureDefinition on
        success."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        _failure_definition = test_tablemodel.do_select(1)

        assert isinstance(_failure_definition, RAMSTKFailureDefinitionRecord)
        assert _failure_definition.definition == "Mock Failure Definition 1"

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, test_attributes, test_tablemodel):
        """do_select() should return None when a non-existent Revision ID is
        requested."""
        test_tablemodel.do_select_all(attributes=test_attributes)

        assert test_tablemodel.do_select(100) is None


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    @pytest.mark.unit
    def test_do_insert_sibling(self, test_attributes, test_tablemodel):
        """should add new record to record tree and update last_id."""
        test_attributes["parent_id"] = 0
        test_attributes["record_id"] = 0
        test_tablemodel.do_select_all(attributes=test_attributes)
        test_tablemodel.do_insert(attributes=test_attributes)

        assert test_tablemodel.last_id == 3
        assert isinstance(
            test_tablemodel.tree[3].data["definition"],
            RAMSTKFailureDefinitionRecord,
        )


@pytest.mark.usefixtures("test_attributes", "test_tablemodel")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.unit
    def test_do_delete(self, test_attributes, test_tablemodel):
        """should remove record from record tree and update last_id."""
        test_tablemodel.do_select_all(attributes=test_attributes)
        _last_id = test_tablemodel.last_id
        test_tablemodel.do_delete(node_id=test_tablemodel.last_id)

        assert test_tablemodel.last_id == 1
        assert test_tablemodel.tree.get_node(_last_id) is None


@pytest.mark.usefixtures("test_attributes", "test_recordmodel")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_recordmodel):
        """should return a dict of attribute key:value pairs."""
        _attributes = test_recordmodel.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["revision_id"] == 1
        assert _attributes["function_id"] == 1
        assert _attributes["definition"] == "Mock Failure Definition 1"

    @pytest.mark.unit
    def test_set_record_model_attributes(self, test_attributes, test_recordmodel):
        """should return None on success."""
        test_attributes.pop("revision_id")
        test_attributes.pop("function_id")
        test_attributes.pop("definition_id")
        assert test_recordmodel.set_attributes(test_attributes) is None

    @pytest.mark.unit
    def test_set_record_model_attributes_none_value(
        self, test_attributes, test_recordmodel
    ):
        """should set an attribute to it's default value when the a None value."""
        test_attributes["definition"] = None

        test_attributes.pop("revision_id")
        test_attributes.pop("function_id")
        test_attributes.pop("definition_id")
        assert test_recordmodel.set_attributes(test_attributes) is None
        assert test_recordmodel.get_attributes()["definition"] == "Failure Definition"

    @pytest.mark.unit
    def test_set_record_model_attributes_unknown_attributes(
        self, test_attributes, test_recordmodel
    ):
        """should raise an AttributeError when passed an unknown attribute."""
        test_attributes.pop("revision_id")
        test_attributes.pop("function_id")
        test_attributes.pop("definition_id")
        with pytest.raises(AttributeError):
            test_recordmodel.set_attributes({"shibboly-bibbly-boo": 0.9998})
