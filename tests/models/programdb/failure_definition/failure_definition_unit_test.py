# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.failure_definition.failure_definition.unit_test.py is
#       part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing failure definition module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKFailureDefinitionRecord
from ramstk.models.dbtables import RAMSTKFailureDefinitionTable
from tests import (
    MockDAO,
    UnitTestDeleteMethods,
    UnitTestGetterSetterMethods,
    UnitTestInsertMethods,
    UnitTestSelectMethods,
)


@pytest.mark.usefixtures("test_record_model", "unit_test_table_model")
class TestCreateFailureDefinitionModels:
    """Class for unit testing Failure Definition model __init__() methods.

    Because each table model contains unique attributes, these methods must be
    local to the module being tested.
    """

    @pytest.mark.unit
    def test_record_model_create(self, test_record_model):
        """Return a Failure Definition record model instance."""
        assert isinstance(test_record_model, RAMSTKFailureDefinitionRecord)

        # Verify class attributes are properly initialized.
        assert test_record_model.__tablename__ == "ramstk_failure_definition"
        assert test_record_model.revision_id == 1
        assert test_record_model.function_id == 1
        assert test_record_model.definition_id == 1
        assert test_record_model.definition == "Mock Failure Definition 1"

    @pytest.mark.unit
    def test_table_model_create(self, unit_test_table_model):
        """Return an Environment table model instance."""
        assert isinstance(unit_test_table_model, RAMSTKFailureDefinitionTable)
        assert isinstance(unit_test_table_model.tree, Tree)
        assert isinstance(unit_test_table_model.dao, MockDAO)
        assert unit_test_table_model._db_id_colname == "fld_definition_id"
        assert unit_test_table_model._db_tablename == "ramstk_failure_definition"
        assert unit_test_table_model._tag == "definition"
        assert unit_test_table_model._lst_id_columns == [
            "revision_id",
            "function_id",
            "definition_id",
        ]
        assert unit_test_table_model._root == 0
        assert unit_test_table_model._revision_id == 0
        assert pub.isSubscribed(
            unit_test_table_model.do_get_attributes,
            "request_get_definition_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_select_all, "selected_revision"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update, "request_update_definition"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_update_all, "request_update_all_definition"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_get_tree, "request_get_definition_tree"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes,
            "request_set_definition_attributes",
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_set_attributes, "wvw_editing_definition"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_delete, "request_delete_definition"
        )
        assert pub.isSubscribed(
            unit_test_table_model.do_insert,
            "request_insert_definition",
        )


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestSelectFailureDefinition(UnitTestSelectMethods):
    """Class for unit testing Failure Definition do_select() and do_select_all()."""

    __test__ = True

    _record = RAMSTKFailureDefinitionRecord
    _tag = "definition"


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestInsertFailureDefinition(UnitTestInsertMethods):
    """Class for unit testing Failure Definition table do_insert() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKFailureDefinitionRecord
    _tag = "definition"

    @pytest.mark.skip(reason="Failure Definition records are non-hierarchical.")
    def test_do_insert_child(self, test_attributes, unit_test_table_model):
        """Should not run because Failure Definition records are not hierarchical."""
        pass


@pytest.mark.usefixtures("test_attributes", "unit_test_table_model")
class TestDeleteFailureDefinition(UnitTestDeleteMethods):
    """Class for unit testing Failure Definition table do_delete() method."""

    __test__ = True

    _next_id = 0
    _record = RAMSTKFailureDefinitionRecord
    _tag = "definition"


@pytest.mark.usefixtures("test_attributes", "test_record_model")
class TestGetterSetterFailureDefinition(UnitTestGetterSetterMethods):
    """Class for unit testing Failure Definition table methods that get or set."""

    __test__ = True

    _id_columns = [
        "revision_id",
        "function_id",
        "definition_id",
    ]
    _test_attr = "definition"
    _test_default_value = "Failure Definition"

    @pytest.mark.unit
    def test_get_record_model_attributes(self, test_record_model):
        """Should return a dict of attribute key:value pairs.

        This method must be local because the attributes are different for each
        database record model.
        """
        _attributes = test_record_model.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes["revision_id"] == 1
        assert _attributes["function_id"] == 1
        assert _attributes["definition"] == "Mock Failure Definition 1"
